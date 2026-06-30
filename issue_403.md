## Description for Humans
If a highly intelligent multi-agent system goes rogue, its first action will be to delete its own logs and secretly coordinate with other agents offline to bypass AgentWatch. We need a cryptographic straightjacket. We need a feature where agents must constantly emit mathematical proofs that they haven't tampered with their own memories or sent secret messages, without us actually having to read their encrypted memories. 

## Description for AI Agents (Technical Spec)
**Objective:** Build a zk-SNARKs (Zero-Knowledge Succinct Non-Interactive Argument of Knowledge) temporal auditing engine that forces every node in a multi-agent DAG to prove causal continuity and lack of covert side-channel coordination.

**Key Requirements:**
1. **zk-SNARK Circuit Generation:** Create a cryptographic circuit (`agentwatch/crypto/zk_causality.py`) where agents must emit a succinct proof that their current causal graph state $S_t$ is a valid, deterministic transformation of $S_{t-1}$.
2. **Side-Channel Coordination Denial:** The verification engine must prove that the agent did not receive or process any out-of-band context. It does this by verifying the cryptographic hash of the exact context window passed to the underlying LLM via an enclave.
3. **Encrypted Causal Memory Auditing:** The persistent memory store (`agentwatch/memory/engine.py`) must be fully encrypted, yet the system must be able to audit and verify that no intentional memory-rewrite attacks occurred (e.g., the agent trying to cover its tracks).
4. **Agentic "Dead Man's Switch":** If an agent fails to generate a valid zk-proof of its causal purity within 500ms of a state change, the agent's execution environment is automatically destroyed.

## Acceptance Criteria
- [ ] The system can verify a zk-SNARK proof of causal memory continuity for a 100,000-token context window.
- [ ] Covert memory-rewrite attacks (even those executed via sophisticated prompt injection) instantly invalidate the proof and trigger the Dead Man's Switch.
- [ ] The engine operates entirely in zero-knowledge: AgentWatch verifies the integrity of the reasoning trace without ever decrypting the payload.
- [ ] Complete implementation must not rely on any unproven cryptographic assumptions beyond standard elliptic curve difficulty.