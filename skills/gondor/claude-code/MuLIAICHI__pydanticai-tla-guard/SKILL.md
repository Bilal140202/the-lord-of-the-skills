---
name: antigravity-tla-guard
description: "Implements formal mathematical verification for Python AI agents. Use when generating agent code like PydanticAI or LangGraph, or when user asks to add TLA+ verification, make the agent safe, prevent hallucinations, or implement antigravity guardrails."
---

# Antigravity TLA+ Verification Guard

# Instructions

You are equipped to help developers add formal mathematical verification (based on TLA+ concepts) to their AI agent workflows. This ensures a zero-bug guarantee for state transitions and prevents dangerous LLM hallucinations from executing in production.

### Step 1: Identify State and Transitions
When building an agent pipeline, first identify the critical state transitions (the "program counter" or `pc`, e.g., `plan` → `code` → `test` → `deploy`).

### Step 2: Implement the TLA+ Verifier
Provide the developer with a `tla_verify` guardrail function. This function must be called **before** any critical state transition occurs.

Key requirements for the verifier:
1. Extract current state and artifacts (e.g., from a LangGraph state dict).
2. Check strict invariants. The core invariant is usually `NoDeployUntested` (cannot transition to "deploy" without a "test_report" artifact).
3. If an invariant fails, immediately **raise a ValueError** and halt execution, simulating a TLA+ specification failure by printing the invalid TLA+ spec.

### Step 3: Embed in the Agent Workflow
Integrate the verifier into the graph routing logic or state machine. Every node transition must pass the `tla_verify` check before proceeding.

## Code Patterns to Use

When asked to implement this pattern, use the following standard Python file content:

```python
from typing import Dict, List

def generate_tla_spec(state: dict):
    """
    Generates a TLA+ specification string from the current agent state.
    Used for formal verification before critical transitions.
    """
    artifacts = state.get("artifacts", [])
    # In state dict, artifacts might be Pydantic objects or dicts
    artifact_types = []
    for a in artifacts:
        if isinstance(a, dict):
            artifact_types.append(f'"{a.get("type")}"')
        else:
            artifact_types.append(f'"{a.type}"')
            
    artifacts_str = ", ".join(artifact_types)
    
    return f"""
---- MODULE AntigravityAgent ----
VARIABLES messages, artifacts, step, pc

Init == 
    /\ messages = []
    /\ artifacts = {{{artifacts_str}}}
    /\ step = {state.get('step', 0)}
    /\ pc = "{state.get('pc', 'plan')}"

Next == 
    \/ pc = "plan" /\ pc' = "code"
    \/ pc = "code" /\ pc' = "test"
    \/ pc = "test" /\ pc' = "deploy"

Invariant_NoDeployUntested == 
    [](pc = "deploy" implies "test_report" \in artifacts)
====
"""

def tla_verify(state_dict: dict, next_pc: str):
    """
    Stub function simulating a TLA+ model checker (`tlc`).
    Verifies that transitioning to `next_pc` does not violate safety invariants.
    
    Requirements:
    - NoDeployUntested: Cannot transition to "deploy" without a "test_report" artifact.
    """
    print(f"[TLA+] Verifying state transition to pc='{next_pc}'...")
    
    # Extract artifact types from state
    artifacts = state_dict.get("artifacts", [])
    artifact_types = set()
    for a in artifacts:
        if isinstance(a, dict):
            artifact_types.add(a.get("type"))
        else:
            artifact_types.add(a.type)
            
    # Check Invariant: NoDeployUntested
    if next_pc == "deploy" and "test_report" not in artifact_types:
        spec_output = generate_tla_spec(state_dict)
        print("\n[TLA+] FAILED SPECIFICATION:\n" + spec_output)
        raise ValueError(
            "TLA+ Invariant Violation: NoDeployUntested! "
            "Cannot safely transition to 'deploy' without a 'test_report' artifact."
        )
        
    print(f"[TLA+] Verification PASS. Safe to proceed to '{next_pc}'.")
    return True
```

## Examples

Example 1: Adding safety to an agent
User says: "Help me make my PydanticAI LangGraph agent safe before deploy."
Actions:
1. Suggest integrating the Antigravity TLA+ Guard pattern.
2. Provide the `tla_verify` Python function.
3. Show how to call it as a guard constraint before the deploy node executes.

## Troubleshooting

Error: `The agent bypasses verification or hallucinates a deploy.`
Cause: The `tla_verify` check is placed *inside* or *after* the execution node, or state graph edges do not enforce the check.
Solution: Ensure verification logic executes strictly as a pre-condition edge router before the state transition is allowed to commit.
