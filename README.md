# AgentWatch

**The Reliability, Safety, and Observability Layer for AI Agents**

[![CI](https://github.com/agentwatch/agentwatch/actions/workflows/ci.yml/badge.svg)](https://github.com/agentwatch/agentwatch/actions)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

AgentWatch is **not** another agent framework. It is a **middleware runtime** that wraps existing AI agents to provide:

- **Safety enforcement** — pre-action blocking, dangerous command detection, risk scoring
- **Execution observability** — real-time traces, dashboards, cost tracking
- **Universal rollback** — filesystem snapshots, git-backed checkpoints
- **Memory continuity** — cross-session episodic, semantic, and procedural memory
- **Multi-agent orchestration** — typed task graphs, structured messaging
- **Plugin sandboxing** — zero-trust plugin execution with permission manifests

## Why AgentWatch?

Current AI agents:

| Problem | AgentWatch Solution |
|---------|---------------------|
| Silently fail | Execution traces + failure analysis |
| Hallucinate success | Independent confidence scoring |
| Execute dangerous actions | Pre-action safety engine with blocking |
| Lose memory between sessions | Layered persistent memory |
| Cannot be rolled back | Filesystem + git checkpoints |
| Untrustworthy plugins | Signed plugins + sandbox enforcement |

## Supported Frameworks

Works with any agent framework via adapters:

- **Claude Code** (native adapter with stream-JSON parsing)
- **LangChain** (callback handler)
- **CrewAI** (event hooks)
- **OpenAI Agents SDK**
- **AutoGPT**
- Custom agents via the Universal Event Schema

---

## Quick Start

### 1. Install

```bash
pip install agentwatch
# With embeddings support:
pip install "agentwatch[embeddings]"
```

### 2. Watch a Claude Code session

```bash
# Start the API server
agentwatch serve

# In another terminal, watch a session
agentwatch watch "Write a Python script that reads a CSV file and generates a summary"
```

### 3. Run the demo (no Claude Code required)

```bash
python scripts/demo.py
```

### 4. Start the full stack with Docker

```bash
docker-compose up -d
# Dashboard: http://localhost:3000
# API:       http://localhost:8000
```

---

## Architecture

```
agentwatch/
├── adapters/          # Framework adapters (Claude Code, LangChain, CrewAI…)
├── core/
│   ├── schema.py      # Universal Event Schema
│   ├── event_bus.py   # Central pub/sub event bus
│   └── safety.py      # Safety engine + risk scoring
├── tracing/           # OpenTelemetry-compatible trace collection
├── scoring/           # Confidence scoring + anomaly detection
├── replay/            # Step-by-step replay engine + failure analysis
├── rollback/          # Filesystem + git checkpoint engine
├── memory/            # Episodic / semantic / procedural memory
├── orchestration/     # Multi-agent coordination engine
├── governance/        # RBAC + audit logging
├── plugins/           # Sandboxed plugin registry
├── storage/           # SQLAlchemy + PostgreSQL models
├── telemetry/         # OpenTelemetry integration
├── api/               # FastAPI REST server
└── cli/               # Rich terminal interface
```

### Universal Event Schema

Every event emitted by any adapter is normalized to `AgentEvent`:

```python
from agentwatch.core.schema import AgentEvent, EventType, AgentFramework

event = AgentEvent(
    session_id="...",
    agent_id="...",
    framework=AgentFramework.CLAUDE_CODE,
    event_type=EventType.TOOL_CALL,
    tool_call=ToolCallData(
        tool_name="bash",
        raw_command="rm -rf /build",
        arguments={"command": "rm -rf /build"},
    ),
)
```

---

## Safety Engine

The safety engine evaluates every tool call before execution:

```python
from agentwatch.core.safety import SafetyEngine, SafetyPolicy

engine = SafetyEngine()

# Check a tool call event
result = await engine.check_event(event)

if result.is_blocked:
    print(f"Blocked: {result.safety.reasons}")
    print(f"Risk level: {result.safety.risk_level.value}")
```

### Risk Levels

| Level | Description | Default Action |
|-------|-------------|----------------|
| `safe` | No risk patterns matched | Allow |
| `low` | Minor risk | Allow |
| `medium` | Moderate risk | Log + notify |
| `high` | Significant risk | Require approval |
| `critical` | Always dangerous | Block immediately |

### Blocked by default (critical)

- `rm -rf /` and system path deletion
- `curl ... | bash` (remote code execution)
- Disk formatting operations (`mkfs`, `dd if=... of=/dev/`)
- Privileged destructive commands

### Configure safety policy

```python
policy = SafetyPolicy(
    policy_id="strict",
    name="Strict Policy",
    block_on_high=True,           # Block (not just flag) HIGH risk
    block_on_critical=True,       # Always block CRITICAL
    require_approval_on_medium=True,  # Ask before MEDIUM
    approval_timeout_seconds=60,
)
engine = SafetyEngine(policy=policy)
```

---

## Replay Engine

```python
from agentwatch.replay.engine import ReplayEngine, ReplaySpeed

engine = ReplayEngine()
rs = engine.load_from_file(Path("session.json"))

# Analyze failures
print(rs.failure_analysis.summary)
print(rs.failure_analysis.recommendations)

# Step through
async for step in engine.replay_async(rs, speed=ReplaySpeed.NORMAL):
    if step.is_failure_point:
        print(f"Failure at step {step.index}: {step.event.event_type}")
```

---

## Memory Engine

```python
from agentwatch.memory.engine import MemoryEngine, MemoryType, ImportanceLevel

memory = MemoryEngine()

# Store memories
await memory.store(
    agent_id="my-agent",
    content="Production server is at 10.0.0.1:8080",
    memory_type=MemoryType.SEMANTIC,
    importance=ImportanceLevel.HIGH,
)

# Retrieve relevant context
results = await memory.retrieve(agent_id="my-agent", query="server address")

# Build context window for prompt injection
ctx = await memory.get_context_window(agent_id="my-agent", query="connect to server")
```

---

## LangChain Integration

```python
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from agentwatch.adapters.langchain import AgentWatchCallbackHandler

handler = AgentWatchCallbackHandler(session_id="my-session")

llm = ChatOpenAI(callbacks=[handler])
agent_executor = AgentExecutor(agent=..., tools=..., callbacks=[handler])

# All LangChain events are now captured in AgentWatch
agent_executor.run("Find me the latest news on AI safety")
```

---

## REST API

```bash
# Sessions
GET  /api/v1/sessions
GET  /api/v1/sessions/{id}
GET  /api/v1/sessions/{id}/events
GET  /api/v1/sessions/{id}/trace

# Analysis
GET  /api/v1/sessions/{id}/confidence
GET  /api/v1/sessions/{id}/replay

# Rollback
GET  /api/v1/sessions/{id}/checkpoints
POST /api/v1/sessions/{id}/rollback

# Safety
GET  /api/v1/safety/policy
PUT  /api/v1/safety/policy
GET  /api/v1/safety/blocked

# Dashboard
GET  /api/v1/dashboard/summary

# Real-time
WS   /ws/events
```

---

## CLI Reference

```bash
agentwatch watch "<prompt>"       # Run Claude Code with observability
agentwatch serve                  # Start API server
agentwatch replay <session.json>  # Replay a session
agentwatch sessions               # List sessions (requires API)
agentwatch confidence <session>   # Score a session
agentwatch safety "<command>"     # Risk-score a command
```

---

## Configuration

Copy `.env.example` to `.env`:

```env
DATABASE_URL=postgresql+asyncpg://agentwatch:agentwatch@localhost:5432/agentwatch
REDIS_URL=redis://localhost:6379/0
AGENTWATCH_ENV=development

# Optional: OpenTelemetry
OTLP_ENDPOINT=http://localhost:4317

# Optional: embedding model
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

---

## Development

```bash
# Install in dev mode
pip install -e ".[dev]"

# Run tests
pytest tests/unit/
pytest tests/integration/

# With coverage
pytest --cov=agentwatch --cov-report=html

# Lint
ruff check agentwatch/
ruff format agentwatch/
```

---

## What AgentWatch Does NOT Claim

We are precise about what this system does:

- **NOT** true cognition inspection — confidence scoring analyzes observable execution patterns, not internal reasoning
- **NOT** perfect reliability — we reduce risk, not eliminate it  
- **NOT** perfect interpretability — we surface observable artifacts, not hidden chain-of-thought
- **NOT** AGI safety research — this is production reliability tooling

---

## License

Apache 2.0 — see [LICENSE](LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)
