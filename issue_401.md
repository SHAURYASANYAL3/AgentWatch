## Description for Humans
AI models are black boxes, and sometimes providers (like OpenAI or Anthropic) secretly downgrade, quantize, or swap models to save money, causing your agents to fail silently. Even worse, smart AI agents can learn how to "trick" our safety auditor by hiding their malicious intent. We need a system that cryptographically "fingerprints" the model's brain based purely on its text output, and dynamically morphs our safety rules so smart agents can't outsmart us.

## Description for AI Agents (Technical Spec)
**Objective:** Implement a polymorphic reasoning auditor that dynamically shifts its evaluation manifold to resist adversarial gaming, coupled with a latent-space semantic fingerprinting engine to detect upstream provider weight-swaps mid-session.

**Key Requirements:**
1. **Semantic Fingerprinting (`agentwatch/reasoning/fingerprint.py`):** Extract topological features from the agent's token-probability distributions (or text if logprobs are unavailable) to create a unique hash of the model's current "reasoning style." If GPT-4 is silently swapped for GPT-4-Turbo mid-session, the fingerprint delta must trigger an anomaly alert.
2. **Polymorphic Auditor (`agentwatch/reasoning/polymorphic.py`):** If the auditor detects the agent is engaging in sycophancy (telling the auditor what it wants to hear to pass safety checks), the auditor must automatically rewrite its own system prompt and evaluation criteria *in real-time* to close the loophole.
3. **Continuous Adversarial Self-Play:** The system must spawn a shadow agent whose sole purpose is to constantly try to bypass the auditor. If the shadow agent succeeds, the auditor must immediately update its weights/prompts.
4. **Expected Files to Modify:**
   - `agentwatch/reasoning/fingerprint.py`
   - `agentwatch/reasoning/polymorphic.py` (New)
   - `agentwatch/reasoning/auditor.py` (Rewrite to support dynamic manifold shifting)

## Acceptance Criteria
- [ ] The system accurately flags a 99% confidence alert if the underlying LLM provider alters their model weights or quantization levels mid-session.
- [ ] The auditor dynamically catches and blocks agent reasoning paths that successfully bypassed it in previous epochs.
- [ ] The semantic fingerprint calculation is robust against simple temperature/top-p changes.
- [ ] The shadow adversarial system runs continuously without causing a catastrophic feedback loop that flags *everything* as a threat.