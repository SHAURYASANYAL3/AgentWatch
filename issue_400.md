## Description for Humans
When a team of 5 AI agents fails a complex task, who is to blame? Agent 4 failed the final step, but it only failed because Agent 2 hallucinated a file path 3 hours earlier. We need a "God's Eye Debugger" that not only finds the root cause, but automatically rewinds time, forks the universe, runs the agents in an alternate reality to see what *would* have happened, and calculates the exact percentage of blame for every decision across the entire team.

## Description for AI Agents (Technical Spec)
**Objective:** Build a non-linear, deterministic time-traveling execution environment for multi-agent Directed Acyclic Graphs (DAGs) and calculate exact causal blame using Shapley values over a distributed temporal knowledge graph.

**Key Requirements:**
1. **Deterministic Universe Forking:** Implement a snapshot-and-fork mechanism (`agentwatch/replay/forking.py`) that can serialize the entire memory, context window, and latent state of a 5-agent CrewAI/LangGraph system at any arbitrary timestamp.
2. **Counterfactual Execution Engine:** The engine must inject a mutated tool response (the "counterfactual") at step $N$, and recursively predict the cascading effects on steps $N+1$ to $M$ across *all other agents* without suffering context-desync.
3. **Shapley Value Computation:** Calculate the marginal contribution of every single reasoning step to the final failure state. This requires calculating the power set of all agent decisions ($O(2^n)$ complexity) and aggregating the causal attribution.
4. **Expected Files to Modify:**
   - `agentwatch/orchestration/shapley.py` (needs to implement the $O(2^n)$ causal math)
   - `agentwatch/replay/counterfactual.py` (needs a state-machine that can fork multi-agent universes)
   - `agentwatch/memory/causal_graph.py` (needs to support overlapping alternate timelines)

## Acceptance Criteria
- [ ] If an agent crew fails, the system outputs: *"Agent 2's reasoning step #4 was 73.4% causally responsible for the failure."*
- [ ] The engine can successfully fork a 100-step multi-agent session, alter step 10, and accurately resolve the remaining 90 steps in an alternate timeline.
- [ ] Memory isolation guarantees that alternate timelines do not bleed into the production causal graph.
- [ ] Time complexity for Shapley approximation must run in under 5 seconds (good luck).