import subprocess
import time

issues = [
    {"title": "Security: Use of assert detected in agentwatch/adapters/claude_code.py:368", "body": "Bandit scan found a LOW severity issue: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code."},
    {"title": "Security: Try, Except, Pass detected in agentwatch/adapters/langchain.py:116", "body": "Bandit scan found a LOW severity issue: Try, Except, Pass detected."},
    {"title": "Security: Possible binding to all interfaces in agentwatch/api/server.py:1042", "body": "Bandit scan found a MEDIUM severity issue: Possible binding to all interfaces (e.g. 0.0.0.0)."},
    {"title": "Security: Possible binding to all interfaces in agentwatch/cli/main.py:423", "body": "Bandit scan found a MEDIUM severity issue: Possible binding to all interfaces (e.g. 0.0.0.0)."},
    {"title": "Security: Bidirectional control characters in agentwatch/core/injection.py:26", "body": "Bandit scan found a HIGH severity issue: A Python source file contains bidirectional control characters ('\\u202a')."},
    {"title": "Security: Weak pseudo-random generator in agentwatch/orchestration/shapley.py:58", "body": "Bandit scan found a LOW severity issue: Standard pseudo-random generators are not suitable for security/cryptographic purposes."},
    {"title": "Security: Weak pseudo-random generator in agentwatch/platform/prompts.py:90", "body": "Bandit scan found a LOW severity issue: Standard pseudo-random generators are not suitable for security/cryptographic purposes."},
    {"title": "Security: Subprocess module security implications in agentwatch/plugins/sandbox.py:129", "body": "Bandit scan found a LOW severity issue: Consider possible security implications associated with the subprocess module."},
    {"title": "Security: Untrusted input in subprocess call in agentwatch/plugins/sandbox.py:131", "body": "Bandit scan found a LOW severity issue: subprocess call - check for execution of untrusted input."},
    {"title": "Security: Possible binding to all interfaces in agentwatch/security/exfiltration.py:31", "body": "Bandit scan found a MEDIUM severity issue: Possible binding to all interfaces."},
    {"title": "Security: Weak pseudo-random generator in agentwatch/tracing/sampling.py:34", "body": "Bandit scan found a LOW severity issue: Standard pseudo-random generators are not suitable for security/cryptographic purposes."},
    {"title": "Security: Weak pseudo-random generator in agentwatch/tracing/sampling.py:58", "body": "Bandit scan found a LOW severity issue: Standard pseudo-random generators are not suitable for security/cryptographic purposes."},
    {"title": "Security: Weak pseudo-random generator in agentwatch/tracing/sampling.py:86", "body": "Bandit scan found a LOW severity issue: Standard pseudo-random generators are not suitable for security/cryptographic purposes."},
    {"title": "Type Error: Need type annotation for 'seen' in agentwatch/orchestration/deadlock.py:37", "body": "Mypy reported: Need type annotation for 'seen'"},
    {"title": "Type Error: Incompatible types in assignment in agentwatch/orchestration/shapley.py:60", "body": "Mypy reported: Incompatible types in assignment (expression has type 'list[str]', variable has type 'tuple[str, ...]')"},
    {"title": "Type Error: Incompatible type for 'shuffle' in agentwatch/orchestration/shapley.py:61", "body": "Mypy reported: Argument 1 to 'shuffle' of 'Random' has incompatible type"},
    {"title": "Type Error: Name 'prefix' already defined in agentwatch/orchestration/shapley.py:62", "body": "Mypy reported: Name 'prefix' already defined on line 48"},
    {"title": "Type Error: Incompatible types in assignment in agentwatch/memory/engine.py:376", "body": "Mypy reported: Incompatible types in assignment (expression has type 'float', variable has type 'int')"},
    {"title": "Type Error: Need type annotation for 'tool_counts' in agentwatch/tracing/trajectory.py:96", "body": "Mypy reported: Need type annotation for 'tool_counts'"},
    {"title": "Type Error: Incompatible argument to 'pop' in agentwatch/tracing/audit.py:96", "body": "Mypy reported: Argument 2 to 'pop' of 'dict' has incompatible type 'None'; expected 'AuditEntry'"},
    {"title": "Type Error: Incompatible type for '_safe_stdev' in agentwatch/scoring/silence.py:79", "body": "Mypy reported: Argument 1 to '_safe_stdev' has incompatible type 'list[int]'; expected 'list[float]'"},
    {"title": "Type Error: Incompatible type for '_safe_stdev' in agentwatch/scoring/silence.py:83", "body": "Mypy reported: Argument 1 to '_safe_stdev' has incompatible type 'list[int]'; expected 'list[float]'"},
    {"title": "Type Error: Incompatible type for 'float' in agentwatch/reasoning/auditor.py:95", "body": "Mypy reported: Argument 1 to 'float' has incompatible type 'object'"},
    {"title": "Type Error: 'object' has no attribute '__iter__' in agentwatch/reasoning/auditor.py:98", "body": "Mypy reported: 'object' has no attribute '__iter__'"},
    {"title": "Type Error: Invalid type for function list in agentwatch/plugins/registry.py:82", "body": "Mypy reported: Function 'agentwatch.plugins.registry.PluginRegistry.list' is not valid as a type"},
    {"title": "Type Error: Incompatible argument for 'max' in agentwatch/platform/intelligence.py:118", "body": "Mypy reported: Argument 'key' to 'max' has incompatible type"},
    {"title": "Type Error: Incompatible type for 'HttpEventForwarder' in agentwatch/core/http_forwarder.py:64", "body": "Mypy reported: Argument 1 to 'HttpEventForwarder' has incompatible type 'str | None'"},
    {"title": "Type Error: 'None' has no attribute 'matches' in agentwatch/core/event_bus.py:250", "body": "Mypy reported: Item 'None' of 'EventFilter | None' has no attribute 'matches'"},
    {"title": "Type Error: Incompatible dict entry type in agentwatch/cost/comparator.py:35", "body": "Mypy reported: Dict entry 0 has incompatible type 'str': 'str'; expected 'str': 'float'"},
    {"title": "Type Error: Incompatible argument type for 'group' in agentwatch/core/policy_dsl.py:89", "body": "Mypy reported: Argument 1 to 'group' of 'Match' has incompatible type"},
    {"title": "Type Error: Incompatible argument type for 'append' in agentwatch/core/policy_dsl.py:90", "body": "Mypy reported: Argument 1 to 'append' of 'list' has incompatible type"},
    {"title": "Type Error: Value not indexable in agentwatch/core/policy_dsl.py:164", "body": "Mypy reported: Value of type 'tuple[str, str] | None' is not indexable"},
    {"title": "Type Error: Incompatible argument type for 'remediation' in agentwatch/governance/causal.py:82", "body": "Mypy reported: Argument 'remediation' to 'AttributionReport' has incompatible type"},
    {"title": "Type Error: Missing named argument 'risk_level' in agentwatch/core/safety.py:681", "body": "Mypy reported: Missing named argument 'risk_level' for 'SafetyCheckData'"},
    {"title": "Type Error: Missing named argument 'risk_score' in agentwatch/core/safety.py:681", "body": "Mypy reported: Missing named argument 'risk_score' for 'SafetyCheckData'"},
    {"title": "Type Error: Incompatible argument 'risk_level' in agentwatch/api/server.py:435", "body": "Mypy reported: Argument 'risk_level' to 'SafetyCheckData' has incompatible type 'str'"},
    {"title": "Type Error: Incompatible argument type in agentwatch/cli/main.py:161", "body": "Mypy reported: Argument 1 to 'set_approval_callback' of 'SafetyEngine' has incompatible type"},
    {"title": "Type Error: Incompatible argument type 'evidence' in tests/test_safety.py:341", "body": "Mypy reported: Argument 'evidence' to 'StepAudit' has incompatible type 'dict[Never, Never]'; expected 'list[str]'"}
]

print(f"Creating {len(issues)} issues on GitHub...")

for i, issue in enumerate(issues, 1):
    print(f"[{i}/{len(issues)}] Creating: {issue['title']}")
    cmd = [
        "gh", "issue", "create",
        "--title", issue["title"],
        "--body", issue["body"]
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Success: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create issue. Error: {e.stderr}")
    
    time.sleep(2)

print("Done creating issues!")
