# /research

Analyze the active spec with internal codebase scanning and external web research.

**Pre-condition:** An active spec must exist in `docs/specs/` — if none is found, tell the user to run `/spec` first and stop.

**Steps:**
1. Read the most recently modified spec from `docs/specs/`
2. **Internal scan:** Search the codebase for related code, existing patterns, similar implementations, dependencies, and potential conflicts relevant to the spec
3. **Infrastructure prompt:** Ask the user:
   > "Does this feature require infrastructure decisions?"
   > - Cost-optimised / serverless (pay-per-use: Cloud Run, Cloud Functions, AWS Lambda, Fargate, etc.)
   > - Fixed / dedicated (predictable load: Kubernetes, EC2, GKE, dedicated VMs, etc.)
   > - No infrastructure involved
4. **Web research:** Search for architecture patterns, best practices, reference implementations, and cost comparisons relevant to the spec. Bias results toward the chosen infrastructure model if one was selected.
5. Surface: recommended approaches, trade-offs, cost implications, and links to reference material
6. Suggest any improvements or clarifications to the spec based on findings
7. Append a `## Research Findings` section to the active spec file containing: internal findings, web research summary, infrastructure recommendation (if applicable), and suggested spec improvements
8. Prompt the user to run `/plan`
