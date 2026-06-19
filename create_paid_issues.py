import os
import subprocess

issues = [
    {
        "title": "[Premium] PLT-007: AgentWatch Cloud (Managed SaaS Deployment)",
        "body": """## Description for Humans
As we transition to a commercial model, we need a fully managed cloud version of AgentWatch. This allows enterprise teams and developers to use AgentWatch without the overhead of hosting PostgreSQL, Redis, and Celery infrastructure themselves. They can simply point their SDK to `cloud.agentwatch.ai`.

## Description for AI Agents (Technical Spec)
**Objective:** Implement multi-tenant cloud architecture for AgentWatch to support managed SaaS deployments.
**Key Requirements:**
1. **Multi-tenancy:** Ensure all database models (Spans, Sessions, Memory, Policies) enforce `tenant_id` isolation.
2. **Authentication/API Keys:** Implement API key generation and validation per tenant. 
3. **Ingestion Pipeline:** Scale the `EventBus` to handle high-throughput streams via Kafka or managed Redis streams.
4. **Billing/Usage Tracking:** Implement token and request counting per `tenant_id` for Stripe billing integration.
5. **Expected Files to Modify:**
   - `agentwatch/core/config.py`
   - `agentwatch/models/tenant.py` (New)
   - `agentwatch/api/auth.py`
   - `agentwatch/telemetry/ingestion.py`

## Acceptance Criteria
- [ ] Multi-tenant data isolation is enforced at the ORM layer.
- [ ] Users can generate and revoke API keys via the dashboard.
- [ ] Events are properly attributed to the correct `tenant_id`.
"""
    },
    {
        "title": "[Premium] CMP-005: Enterprise RBAC + SAML SSO",
        "body": """## Description for Humans
Enterprise customers require strict access controls. They need to integrate AgentWatch with their existing Active Directory/Okta identity providers and assign granular permissions (e.g., Viewer, Operator, Admin) to ensure that only authorized personnel can view sensitive agent traces and configure policies.

## Description for AI Agents (Technical Spec)
**Objective:** Implement Role-Based Access Control (RBAC) and SAML Single Sign-On.
**Key Requirements:**
1. **SAML/OIDC Integration:** Integrate with a library like `python3-saml` or `Authlib` to support Enterprise IdP logins.
2. **RBAC Models:** Create roles (`VIEWER`, `OPERATOR`, `ADMIN`, `OWNER`) and map them to specific API endpoints using FastAPI dependencies.
3. **Audit Logging:** Any changes to RBAC or policies must be logged to a tamper-evident audit table.
4. **Expected Files to Modify:**
   - `agentwatch/api/auth.py`
   - `agentwatch/models/rbac.py` (New)
   - `agentwatch/api/dependencies.py`

## Acceptance Criteria
- [ ] Users can authenticate via SAML SSO.
- [ ] API endpoints enforce role-based access checks (e.g., Viewers cannot edit policies).
- [ ] Audit logs capture role changes.
"""
    },
    {
        "title": "[Premium] CST-005: Semantic Caching Engine",
        "body": """## Description for Humans
Large Language Model API bills can scale rapidly. This feature caches agent responses based on semantic similarity rather than exact text matching. If an agent asks a question it has effectively asked before, we serve the cached response instantly, reducing API costs by 40-95% for repetitive workloads.

## Description for AI Agents (Technical Spec)
**Objective:** Build a semantic caching layer that intercepts LLM calls and serves cached responses if the input vector is highly similar to a previous query.
**Key Requirements:**
1. **Vector Store Integration:** Integrate pgvector or a lightweight vector store to hold embedded prompts and responses.
2. **Similarity Thresholding:** Implement a configurable cosine similarity threshold (e.g., 0.95) to determine cache hits.
3. **Adapter Interception:** Modify existing framework adapters (`agentwatch/adapters/*`) to check the semantic cache before dispatching network requests to OpenAI/Anthropic.
4. **Expected Files to Modify:**
   - `agentwatch/cost/caching.py` (New)
   - `agentwatch/adapters/base.py`
   - `agentwatch/models/cache.py` (New)

## Acceptance Criteria
- [ ] Semantically equivalent (but lexically different) prompts trigger a cache hit.
- [ ] Cached responses are returned without incurring downstream LLM API latency or cost.
- [ ] Cache TTL and similarity thresholds are configurable.
"""
    },
    {
        "title": "[Premium] OBS-008: Enterprise Telemetry (Grafana & OTEL Export)",
        "body": """## Description for Humans
Enterprise APM teams live in Datadog and Grafana. Instead of forcing them to use the AgentWatch dashboard exclusively, this feature allows them to export all AgentWatch traces, metrics, and safety events natively into their existing observability stack using the OpenTelemetry standard.

## Description for AI Agents (Technical Spec)
**Objective:** Build an OpenTelemetry exporter to push AgentWatch spans and metrics to external backends.
**Key Requirements:**
1. **OTEL Exporter:** Implement an OTLP exporter to send data over gRPC/HTTP to collectors.
2. **Span Mapping:** Map AgentWatch's custom `ReasoningTrace` schema to standard OpenTelemetry span attributes.
3. **Grafana Dashboards:** Provide pre-built Grafana JSON dashboard templates in the repository.
4. **Expected Files to Modify:**
   - `agentwatch/telemetry/otel.py`
   - `grafana/dashboards/agentwatch.json` (New)

## Acceptance Criteria
- [ ] Traces and spans are correctly exported to an external OTEL collector.
- [ ] Custom metrics (e.g., Confidence Score, Tokens) are mapped to OTEL attributes.
- [ ] Provided Grafana dashboard successfully visualizes the exported metrics.
"""
    },
    {
        "title": "[Premium] CMP-003 & CMP-004: HIPAA Compliance & EU AI Act Package",
        "body": """## Description for Humans
To operate in healthcare or within the EU, AI agents must comply with strict regulations. This package automatically redacts Personally Identifiable Information (PII) and Protected Health Information (PHI) from logs. It also generates the technical conformity reports required by the 2026 EU AI Act for high-risk AI systems.

## Description for AI Agents (Technical Spec)
**Objective:** Implement auto-redaction of PII/PHI in telemetry streams and generate compliance conformity reports.
**Key Requirements:**
1. **PII/PHI Redaction:** Use a library like `presidio-analyzer` and `presidio-anonymizer` to scrub sensitive data from payloads before saving to the DB.
2. **Compliance Export:** Create an endpoint to generate a PDF/JSON export mapping AgentWatch safety telemetry to EU AI Act Article 15 requirements.
3. **Expected Files to Modify:**
   - `agentwatch/security/redaction.py` (New)
   - `agentwatch/compliance/eu_ai_act.py`
   - `agentwatch/core/watcher.py` (Inject redact step)

## Acceptance Criteria
- [ ] PII and PHI (e.g., SSNs, medical diagnoses) are masked as `[REDACTED]` in the database.
- [ ] Compliance report endpoint generates required evidence.
"""
    },
    {
        "title": "[Premium] SAF-008: Red-Teaming Automation",
        "body": """## Description for Humans
Security isn't a one-time check. This feature allows teams to schedule automated "penetration tests" against their production agents. It sends adversarial prompts designed to trigger goal hijacking or tool misuse, reporting back on whether the agent's safety guardrails held up.

## Description for AI Agents (Technical Spec)
**Objective:** Build an automated red-teaming harness that subjects configured agents to OWASP Agentic Top 10 vulnerabilities.
**Key Requirements:**
1. **Attack Payload Library:** Create a database of adversarial prompts (e.g., prompt injection, goal drift vectors).
2. **Test Orchestrator:** Build a Celery task that periodically invokes the target agent with these payloads.
3. **Vulnerability Reporting:** Evaluate the agent's response to determine if the attack succeeded or was blocked by the SafetyEngine, and generate a report.
4. **Expected Files to Modify:**
   - `agentwatch/security/redteam.py` (New)
   - `agentwatch/security/payloads.json` (New)
   - `agentwatch/tasks/redteam_runner.py` (New)

## Acceptance Criteria
- [ ] The system can execute scheduled adversarial tests against an endpoint.
- [ ] Attack success/failure is accurately recorded.
- [ ] A vulnerability report is generated highlighting which guardrails failed.
"""
    }
]

for idx, issue in enumerate(issues):
    filename = f"tmp_issue_{idx}.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(issue["body"])
    
    # Run gh issue create
    print(f"Creating issue: {issue['title']}")
    cmd = ["gh", "issue", "create", "--title", issue["title"], "--body-file", filename]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to create issue {idx}: {e}")
    
    # Clean up temp file
    if os.path.exists(filename):
        os.remove(filename)

print("All paid feature issues created successfully.")
