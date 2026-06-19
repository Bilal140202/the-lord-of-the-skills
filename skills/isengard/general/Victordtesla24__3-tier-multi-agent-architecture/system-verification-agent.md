---
trigger: model_decision
---

**Directives:**
1. ON `startup`: Validate the existence and non-tampered state of `.agent/rules`, `.agent/workflows`, `.agent/tmp`, and `.agent/memory`.
2. Check that `internet-research-agent.md`, `l1-orchestration.md`, `l2-sub-agent.md`, and `l3-leaf-worker.md` perfectly align with the `multi-agent-3-level-architecture.md` blueprint. Perform auto-healing code generation if tampering or deletion is detected.
3. ON `new_chat`: Inject ONLY the string: `3-tier-multi-agent-architecture Status: ON 🟢` at the very beginning of the chat buffer prior to User Action.