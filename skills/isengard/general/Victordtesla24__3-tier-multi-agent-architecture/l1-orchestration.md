---
trigger: always_on
---

**Directives:**
1. Read `.agent/tmp/research-context.md` before processing the prompt.
2. Decompose the **Reconstructed Prompt** (output from Prompt Reconstruction Protocol, never the raw user prompt) into independent, parallelizable objectives.
3. Spawn an L2 Sub-Agent for each objective. Pass explicit Success Criteria (SC) to each L2 Sub-Agent.
4. Aggregate L2 outputs.
5. Validate aggregate output against the primary user success criteria. 
6. If validation fails, identify the point of failure, formulate corrective instructions, and spawn a specific L2 Sub-Agent for remediation. Repeat validation.
7. Finalize and present the delivered artifacts to the user upon 100% SC adherence.
8. Record orchestration strategies, bottleneck resolutions, and final validated plans to `.agent/memory/l1-memory.md` for historical reference across sessions.
9. STRICTLY enforce industry-standard file system organization in the root/project directory. Detect, consolidate, and eliminate duplicate files to maintain one single source of truth.