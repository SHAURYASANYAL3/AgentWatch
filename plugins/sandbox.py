"""
AgentWatch Plugin Sandbox
Zero-trust plugin execution with permission manifests, sandboxing,
and signed plugin verification.
"""

from __future__ import annotations

import asyncio
import hashlib
import importlib.util
import json
import logging
import os
import sys
import tempfile
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

from agentwatch.core.schema import PluginManifest, PluginPermissions

logger = logging.getLogger(__name__)


class PluginStatus(str, Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    REJECTED = "rejected"
    DISABLED = "disabled"
    ACTIVE = "active"


class SandboxViolation(Exception):
    """Raised when a plugin attempts an operation outside its declared permissions."""
    pass


@dataclass
class PluginExecutionResult:
    plugin_id: str
    success: bool
    output: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float = 0.0
    violation: Optional[str] = None
    resources_accessed: List[str] = field(default_factory=list)


# ─────────────────────────────────────────────
# Permission enforcer
# ─────────────────────────────────────────────

class PermissionEnforcer:
    """
    Enforces plugin permission manifests at runtime.
    Wraps builtins and stdlib calls to intercept violations.
    """

    def __init__(self, manifest: PluginManifest):
        self._perms = manifest.permissions
        self._plugin_id = manifest.plugin_id
        self._violations: List[str] = []
        self._accessed: List[str] = []

    def _check(self, permission: str, context: str) -> None:
        allowed = getattr(self._perms, permission, False)
        if not allowed:
            msg = f"Plugin '{self._plugin_id}' attempted '{context}' without '{permission}' permission"
            self._violations.append(msg)
            raise SandboxViolation(msg)
        self._accessed.append(context)

    def safe_open(self, path: str, mode: str = "r", **kwargs):
        """Safe open() that enforces filesystem permissions."""
        is_write = any(c in mode for c in ("w", "a", "x", "+"))
        if is_write:
            self._check("filesystem_write", f"write:{path}")
        else:
            self._check("filesystem_read", f"read:{path}")
        return open(path, mode, **kwargs)

    def safe_exec(self, cmd: str, **kwargs) -> Any:
        """Safe subprocess execution."""
        self._check("subprocess_exec", f"exec:{cmd[:50]}")
        import subprocess
        return subprocess.run(cmd, shell=True, **kwargs)

    @property
    def violations(self) -> List[str]:
        return list(self._violations)

    @property
    def accessed_resources(self) -> List[str]:
        return list(self._accessed)


# ─────────────────────────────────────────────
# Plugin verifier
# ─────────────────────────────────────────────

class PluginVerifier:
    """
    Verifies plugin integrity via checksum and optional signature.
    """

    def __init__(self, trusted_keys: Optional[Dict[str, str]] = None):
        self._trusted_keys = trusted_keys or {}

    def verify_checksum(self, plugin_path: Path, manifest: PluginManifest) -> bool:
        """Verify SHA-256 checksum of plugin file."""
        if not manifest.checksum_sha256:
            logger.warning("Plugin %s has no checksum — treating as unverified", manifest.plugin_id)
            return False

        with open(plugin_path, "rb") as f:
            actual = hashlib.sha256(f.read()).hexdigest()

        if actual != manifest.checksum_sha256:
            logger.error(
                "Checksum mismatch for plugin %s: expected %s, got %s",
                manifest.plugin_id, manifest.checksum_sha256, actual,
            )
            return False
        return True

    def verify_signature(self, manifest: PluginManifest, plugin_bytes: bytes) -> bool:
        """
        Verify Ed25519 signature if available.
        Falls back to checksum-only verification.
        """
        if not manifest.signature:
            return False

        author = manifest.author
        if author not in self._trusted_keys:
            logger.warning("Unknown plugin author: %s", author)
            return False

        try:
            from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
            from cryptography.hazmat.primitives.serialization import load_pem_public_key
            import base64

            pub_key_pem = self._trusted_keys[author].encode()
            pub_key = load_pem_public_key(pub_key_pem)
            sig_bytes = base64.b64decode(manifest.signature)
            pub_key.verify(sig_bytes, plugin_bytes)
            return True
        except ImportError:
            logger.warning("cryptography package not installed — signature check skipped")
            return False
        except Exception as exc:
            logger.error("Signature verification failed: %s", exc)
            return False

    def compute_trust_level(self, manifest: PluginManifest, plugin_path: Path) -> int:
        """Compute effective trust level 0-5."""
        checksum_ok = self.verify_checksum(plugin_path, manifest)

        if not checksum_ok:
            return 0  # Untrusted

        if manifest.trust_level == 5:
            # Core plugin — requires valid signature
            plugin_bytes = plugin_path.read_bytes()
            if self.verify_signature(manifest, plugin_bytes):
                return 5
            return 2  # Checksum only

        return min(manifest.trust_level, 3)


# ─────────────────────────────────────────────
# Plugin sandbox
# ─────────────────────────────────────────────

class PluginSandbox:
    """
    Executes plugins in a restricted environment.
    Enforces permission manifests.
    Does NOT use OS-level isolation (that requires Docker/seccomp).
    For production, wrap in Docker container.
    """

    def __init__(self, timeout_seconds: float = 30.0):
        self._timeout = timeout_seconds

    async def execute(
        self,
        plugin_path: Path,
        manifest: PluginManifest,
        entry_point: str,
        inputs: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> PluginExecutionResult:
        """Execute a plugin function with permission enforcement."""
        start = time.monotonic()
        enforcer = PermissionEnforcer(manifest)

        try:
            result = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(
                    None,
                    self._run_in_process,
                    plugin_path,
                    manifest,
                    entry_point,
                    inputs,
                    enforcer,
                ),
                timeout=self._timeout,
            )
            elapsed_ms = (time.monotonic() - start) * 1000
            return PluginExecutionResult(
                plugin_id=manifest.plugin_id,
                success=True,
                output=result,
                execution_time_ms=elapsed_ms,
                resources_accessed=enforcer.accessed_resources,
            )

        except SandboxViolation as exc:
            elapsed_ms = (time.monotonic() - start) * 1000
            return PluginExecutionResult(
                plugin_id=manifest.plugin_id,
                success=False,
                error=str(exc),
                violation=str(exc),
                execution_time_ms=elapsed_ms,
            )
        except asyncio.TimeoutError:
            return PluginExecutionResult(
                plugin_id=manifest.plugin_id,
                success=False,
                error=f"Plugin timed out after {self._timeout}s",
                execution_time_ms=self._timeout * 1000,
            )
        except Exception as exc:
            elapsed_ms = (time.monotonic() - start) * 1000
            logger.error("Plugin %s failed: %s", manifest.plugin_id, exc, exc_info=True)
            return PluginExecutionResult(
                plugin_id=manifest.plugin_id,
                success=False,
                error=str(exc),
                execution_time_ms=elapsed_ms,
            )

    def _run_in_process(
        self,
        plugin_path: Path,
        manifest: PluginManifest,
        entry_point: str,
        inputs: Dict[str, Any],
        enforcer: PermissionEnforcer,
    ) -> Any:
        """Load and execute the plugin module in a restricted namespace."""
        # Build restricted builtins
        restricted_builtins = self._build_restricted_builtins(manifest, enforcer)

        # Load module source
        source = plugin_path.read_text()

        # Compile and execute in restricted namespace
        code = compile(source, str(plugin_path), "exec")
        namespace: Dict[str, Any] = {
            "__builtins__": restricted_builtins,
            "__name__": f"agentwatch.plugin.{manifest.plugin_id}",
        }

        exec(code, namespace)  # noqa: S102

        if entry_point not in namespace:
            raise ValueError(f"Entry point '{entry_point}' not found in plugin")

        fn = namespace[entry_point]
        if not callable(fn):
            raise ValueError(f"Entry point '{entry_point}' is not callable")

        return fn(**inputs)

    def _build_restricted_builtins(
        self, manifest: PluginManifest, enforcer: PermissionEnforcer
    ) -> Dict[str, Any]:
        """Build a restricted builtins dict based on plugin permissions."""
        import builtins as _builtins

        # Safe builtins available to all plugins
        safe = {
            "abs", "all", "any", "bool", "bytes", "callable", "chr", "dict",
            "divmod", "enumerate", "filter", "float", "format", "frozenset",
            "getattr", "hasattr", "hash", "hex", "id", "int", "isinstance",
            "issubclass", "iter", "len", "list", "map", "max", "min", "next",
            "object", "oct", "ord", "pow", "print", "range", "repr", "reversed",
            "round", "set", "setattr", "slice", "sorted", "str", "sum", "tuple",
            "type", "vars", "zip",
            # Exceptions
            "Exception", "ValueError", "TypeError", "KeyError", "IndexError",
            "RuntimeError", "NotImplementedError", "StopIteration",
        }

        restricted: Dict[str, Any] = {
            k: getattr(_builtins, k) for k in safe if hasattr(_builtins, k)
        }

        # Conditionally allow open()
        if manifest.permissions.filesystem_read or manifest.permissions.filesystem_write:
            restricted["open"] = enforcer.safe_open
        else:
            restricted["open"] = lambda *a, **k: (_ for _ in ()).throw(
                SandboxViolation("Plugin does not have filesystem permission")
            )

        # Block __import__ unless explicitly needed
        restricted["__import__"] = self._restricted_import(manifest.permissions)

        return restricted

    def _restricted_import(self, perms: PluginPermissions):
        """Return an import function that blocks dangerous modules."""
        BLOCKED_MODULES = {
            "os", "sys", "subprocess", "shutil", "socket", "urllib",
            "http", "ftplib", "smtplib", "ctypes", "importlib",
        }

        if perms.subprocess_exec:
            BLOCKED_MODULES.discard("subprocess")
        if perms.network_outbound:
            BLOCKED_MODULES.discard("urllib")
            BLOCKED_MODULES.discard("http")

        def _import(name: str, *args, **kwargs):
            base = name.split(".")[0]
            if base in BLOCKED_MODULES:
                raise SandboxViolation(f"Import of '{name}' is not permitted")
            return __import__(name, *args, **kwargs)

        return _import


# ─────────────────────────────────────────────
# Plugin Registry
# ─────────────────────────────────────────────

class PluginRegistry:
    """
    Manages plugin discovery, verification, and lifecycle.
    """

    def __init__(
        self,
        plugins_dir: Optional[Path] = None,
        sandbox: Optional[PluginSandbox] = None,
        verifier: Optional[PluginVerifier] = None,
    ):
        self._plugins_dir = plugins_dir or Path(".agentwatch/plugins")
        self._sandbox = sandbox or PluginSandbox()
        self._verifier = verifier or PluginVerifier()
        self._registry: Dict[str, Dict[str, Any]] = {}

    def register(
        self, manifest: PluginManifest, plugin_path: Path
    ) -> PluginStatus:
        """Register a plugin after verification."""
        if not plugin_path.exists():
            logger.error("Plugin file not found: %s", plugin_path)
            return PluginStatus.REJECTED

        trust_level = self._verifier.compute_trust_level(manifest, plugin_path)

        if trust_level == 0:
            logger.warning(
                "Plugin %s rejected: trust_level=0 (checksum mismatch or no checksum)",
                manifest.plugin_id,
            )
            status = PluginStatus.REJECTED
        else:
            status = PluginStatus.VERIFIED
            manifest.trust_level = trust_level

        self._registry[manifest.plugin_id] = {
            "manifest": manifest,
            "path": plugin_path,
            "status": status,
            "execution_count": 0,
            "error_count": 0,
        }
        logger.info(
            "Registered plugin %s (trust=%d, status=%s)",
            manifest.plugin_id, trust_level, status.value,
        )
        return status

    async def execute_plugin(
        self,
        plugin_id: str,
        entry_point: str,
        inputs: Dict[str, Any],
    ) -> PluginExecutionResult:
        """Execute a registered, verified plugin."""
        entry = self._registry.get(plugin_id)
        if not entry:
            return PluginExecutionResult(
                plugin_id=plugin_id,
                success=False,
                error=f"Plugin '{plugin_id}' not registered",
            )

        if entry["status"] in (PluginStatus.REJECTED, PluginStatus.DISABLED):
            return PluginExecutionResult(
                plugin_id=plugin_id,
                success=False,
                error=f"Plugin '{plugin_id}' is {entry['status'].value}",
            )

        result = await self._sandbox.execute(
            plugin_path=entry["path"],
            manifest=entry["manifest"],
            entry_point=entry_point,
            inputs=inputs,
        )

        entry["execution_count"] += 1
        if not result.success:
            entry["error_count"] += 1

        return result

    def list_plugins(self) -> List[Dict[str, Any]]:
        return [
            {
                "plugin_id": e["manifest"].plugin_id,
                "name": e["manifest"].name,
                "version": e["manifest"].version,
                "author": e["manifest"].author,
                "status": e["status"].value,
                "trust_level": e["manifest"].trust_level,
                "execution_count": e["execution_count"],
                "error_count": e["error_count"],
            }
            for e in self._registry.values()
        ]

    def disable_plugin(self, plugin_id: str) -> None:
        if plugin_id in self._registry:
            self._registry[plugin_id]["status"] = PluginStatus.DISABLED
            logger.info("Plugin %s disabled", plugin_id)
