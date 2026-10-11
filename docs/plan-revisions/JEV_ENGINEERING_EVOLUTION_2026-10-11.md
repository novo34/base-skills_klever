# PlanRevision — JEV engineering quality evolution

Date: 2026-10-11
Status: PROPOSED — pending review, gates and merge
Canonical base: main
Active controlled task unchanged: PLT-009 (IN_PROGRESS)
Scope: plan-only change; no runtime code or existing PRD/SPEC/ROADMAP replaced.

## Why
Integrate 12 scoped improvements identified while inspecting Ponytail, Pstack and Thermos against Foundation v8 and JEV Platform. The review was differential and partial: third-party suites and all-repo penetration tests were NOT executed. No benchmark superiority is claimed.

## Existing ownership (must reuse, not duplicate)
- FND skills 10, 13, 25, 27, 28, 29, 30, 31, 49, 51–54, 59, 91, 92.
- Platform planned work PLT-014/015/016, PLT-041/042, PLT-045/046, PLT-048.
- Platform queue and worker code at packages/queue/src/service.ts, apps/worker/src/runtime.ts.

## New proposed task references
- PLT-050 autonomous completion and corrective loop
- PLT-051 external research on stalled failures
- PLT-052 pre-creation code reuse discovery
- PLT-053 safe automated cleanup
- PLT-054 multi-lens independent PR verification
- PLT-055 artifact-bound test and review freshness
- PLT-056 retry classification and durable resume
- PLT-057 precise symbol/reference index
- PLT-058 behavioral-equivalence refactoring
- PLT-059 blind comparative skill/agent evaluation
- PLT-060 metric-driven iterative optimization
- PLT-061 browser and visual regression evidence

## First execution track: PLT-050 after prerequisites
1. Trace completion state across Platform WorkOrders, Queue, Worker, Agent and Verifier.
2. Add failed-verification -> diagnosis -> proposed fix -> test -> independent verification transitions; no auto-approval.
3. Persist attempt and checkpoint with task, blueprint revision, artifact SHA, error class, hypotheses, external-source provenance when used, budgets and result.
4. Test failing-then-passing case, repeated failure with strategy change, timeout/budget stop, process crash/resume, stale evidence and unauthorized action denial.
5. Verify through CI, independent review, and actual workspace integration once their prerequisite Platform tasks are available.

## Integration invariants
- Planned tasks remain TODO, with controlled order enforced by the canonical backlog.
- PLT-009 remains IN_PROGRESS. No next task starts before the Development Control Gate allows it.
- Foundation defines contracts; Platform implements runtime.
- Codex, DeepSeek and Antigravity capabilities must be validated through adapters, never inferred from another editor's plugin.
- Source-grounded online research is required for stalled technical diagnosis when available and authorized; source contents are untrusted data.
- No unbounded loops, unsafe code execution, silent deletion, weakening risk gates, or unauthorized production merges.
- Existing PRD/SPEC/ROADMAP remain unchanged until a traced PlanRevision is accepted and downstream documentation impact is assessed.

## Gates before promotion
- Verify unique task IDs, syntax/schema, dependency graph and controlled order.
- Verify acceptance and traceability against existing tasks; no duplicated capability implementation.
- Run Foundation validators and existing tests; execute Platform integration suites when runtime phase begins.
- Independent review, operator approval and merge into main.
