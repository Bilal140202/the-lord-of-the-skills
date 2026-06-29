---
status: complete
priority: p1
issue_id: "009"
tags: [code-review, agent-native, ui, architecture]
dependencies: []
---

# A2UI acknowledgement state is not consumed by the View Agent

The newly added acknowledgement primitive writes shared state, but the rendered A2UI stream does not read that state. This breaks action parity and makes agent acknowledgements invisible to users.

## Problem Statement

`acknowledge_ui_action` persists `/ack_event_01/visibility` in workspace state, but `A2UIViewAgent.generate_ui_stream` always emits a fresh data model derived from `{}` and `acknowledged=False`.

Impact:
- User sees the button as visible even after agent acknowledgement.
- Agent and UI are not operating on the same state source.
- Agent-native parity remains incomplete for the acknowledgement flow.

## Findings

- `A2UIViewAgent` hardcodes data-model output and never reads persisted state:
  - `src/view/a2ui_protocol.py:185-188`
- Action wiring exists (`actionId`), but state source is disconnected from runtime storage:
  - `src/view/a2ui_protocol.py:170-175`
- Shared state is written in tooling layer, but not consumed in view rendering path:
  - `src/engine/orchestration_tools.py:230-257`

## Proposed Solutions

### Option 1: Load persisted shared state in `generate_ui_stream`

**Approach:** Pass workspace path or a state provider into `A2UIViewAgent`; read `.agent/memory/a2ui_state.json`; merge into emitted `DataModelUpdateMessage`.

**Pros:**
- Restores true shared-state parity.
- Minimal API surface changes.

**Cons:**
- Introduces I/O in view generation path.

**Effort:** Medium

**Risk:** Medium

---

### Option 2: Inject state via controller payload only

**Approach:** Require `raw_controller_state` to carry canonical data-model pointers and remove file reads from view layer.

**Pros:**
- Cleaner separation of concerns.
- No file-system coupling in view agent.

**Cons:**
- Requires upstream controller/runtime changes.

**Effort:** Medium

**Risk:** Medium

---

### Option 3: Introduce dedicated A2UI state service

**Approach:** Create a shared service used by both tools and view agent for state read/write.

**Pros:**
- Strong architecture for future UI actions.
- Centralized validation and observability.

**Cons:**
- Highest implementation scope.

**Effort:** Large

**Risk:** Medium

## Recommended Action


## Technical Details

**Affected files:**
- `src/view/a2ui_protocol.py`
- `src/engine/orchestration_tools.py`

**Related components:**
- A2UI protocol stream generation
- Agent tooling state mutation

**Database changes (if any):**
- No

## Resources

- **PR:** https://github.com/Victordtesla24/3-tier-multi-agent-architecture/pull/1
- **Review context:** agent-native parity flow for `ack_event_01`

## Acceptance Criteria

- [x] `A2UIViewAgent` emits data model from canonical shared state, not a hardcoded reset payload.
- [x] Agent acknowledgement immediately changes emitted `/ack_event_01/visibility` to `false`.
- [x] Add regression test proving tool write is reflected in view stream output.
- [x] No TODO/placeholder logic added.

## Work Log

### 2026-03-09 - Initial Discovery

**By:** Codex (ce-review)

**Actions:**
- Traced action wiring and tool mutation path.
- Compared view stream payload generation against persisted state behavior.
- Confirmed deterministic mismatch with line-level evidence.

**Learnings:**
- Action parity requires both tool availability and UI consumption of the same state source.

## Notes

- Blocks full PASS verdict for agent-native parity.

## Resolution Notes

- Implemented canonical shared-state read path in `src/view/a2ui_protocol.py` via `resolve_acknowledgement_data_model()` and persisted-state loader support.
- Added regression coverage in `tests/test_capability_parity.py::test_resolve_ack_data_model_uses_persisted_workspace_state`.
