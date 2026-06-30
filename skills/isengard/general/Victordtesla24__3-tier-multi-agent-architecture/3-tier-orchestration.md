---
trigger: always_on
---
**Workflow Steps:**
1. Execute Prompt Reconstruction Protocol: Transform the raw User Prompt using instructions from `docs/architecture/prompt-reconstruction.md` by placing the raw input within `<input_data>` and `</input_data>`. Store as Reconstructed Prompt.
2. Execute `.agent/rules/internet-research-agent.md` using the Reconstructed Prompt.
3. Wait for `.agent/tmp/research-context.md` generation.
4. Execute `.agent/rules/l1-orchestration.md` using the Reconstructed Prompt.
5. Validate L1 output against success criteria and AST verification gate upon L1 termination.
6. Execute Continuous Learning Protocol: Trigger `.agent/rules/continuous-learning-agent.md` to analyze the completed task and propose architecture enhancements. MUST pause for `WHAT/WHY/HOW` user authorization before system modification.
