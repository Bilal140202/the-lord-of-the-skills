<!-- 
Thank you for contributing to the Universal AI Rules Suite!
Please fulfill the template below so we can rapidly review your PR.
-->

## Type of Change

<!-- Check all that apply with an "x" inside the brackets [x] -->
- [ ] 📜 Rule Addition (Adding a new rule to an existing phase)
- [ ] 🔧 Rule Fix/Adjustment (Modifying an existing rule for better AI compliance)
- [ ] 📁 New Phase/File (Adding an entirely new checklist file)
- [ ] 🔌 New Editor Adapter (Adding support for a new IDE/Agent)
- [ ] 📝 Documentation Update
- [ ] 🐛 Bug Fix

## Description

<!-- What does this PR do? Why is it necessary? -->
Please describe the changes you made here.

## The Problem (If applicable)

<!-- 
If modifying a rule, what bad AI behavior prompted this? 
Example: "Claude 3.5 Sonnet kept skipping dependency validation. This rule forces a STOP gate."
-->


## Validation Checklist

<!-- Ensure your PR meets the repo's design philosophy -->
- [ ] I have kept the rules formatted as `[ ]` actionable checkboxes.
- [ ] My added/modified rules are binary and verifiable (no vague "write clean code" instructions).
- [ ] I have not removed or degraded the Security Checkpoint or STOP gates.
- [ ] The file I modified is still under 400 lines.
- [ ] (If adding a file) I have added the new file to the routing table in `/.ai-suite/MASTER.md`.
- [ ] (If adding an adapter) I have updated `setup.sh` and the `README.md`.

## Additional Context

<!-- Screenshots, logs, or prompt examples that show the AI behaving better with this new rule -->
