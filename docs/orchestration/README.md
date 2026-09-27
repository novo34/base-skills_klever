# JEV orchestration state

This directory is the repository-level source of truth for multi-agent work.

Runtime projects using JEV should maintain:

- `WORKPLAN.md`: approved roles, scope, dependencies and gates.
- `HANDOFFS.md`: append-only handoff log.
- `STATE.json`: machine-readable current task and lock state.
- `DECISIONS.md`: approved architectural/critical decisions.
- `REQUIREMENTS.json`: PRD/SPEC requirement traceability.
- `LOCKS.json`: active file or subsystem ownership locks.

JEV must read current orchestration state before an agent receives write access.
