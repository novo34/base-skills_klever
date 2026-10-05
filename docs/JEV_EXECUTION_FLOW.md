# JEV adaptive executable task flow

The canonical adaptive flow is:

1. Receive human intent.
2. Build IntentBrief and determine ambiguity, change radius and required documentation depth.
3. Build AcceptanceContract with observable criteria, constraints and evidence.
4. Classify risk using declared signals and affected paths/surfaces.
5. Build a bounded ContextPack and retrieval budget.
6. Create/version an ExecutionBlueprint with DAG, capabilities, evidence, rollback and exit criteria.
7. Compile an AdaptiveWorkflow. Risk can increase depth/gates; adaptive logic cannot reduce mandatory controls.
8. Resolve skills, authority roles, model tier and harness capabilities.
9. Create a dedicated task branch and isolated workspace.
10. Execute source-grounded incremental development.
11. Apply TDD/debugging/simplification and repository-hygiene gates as applicable.
12. If new facts invalidate the plan, create a PlanRevision and revalidate DAG/risk/budget/evidence before resuming.
13. Create the task pull request and collect CI/API/browser/database/runtime/trace/hygiene evidence as applicable.
14. Run independent verification plus adversarial doubt review.
15. If verification fails or critical evidence is missing, return to corrective work or BLOCKED.
16. If VERIFIED, integrate that exact task into permanent staging.
17. Confirm staging web/backend/database/migrations/E2E evidence where applicable.
18. Expose exact staging result and evidence for human review.
19. Human explicitly chooses APPROVED, CHANGES_REQUESTED or REJECTED.
20. Integrator may prepare production promotion only for the approved blueprint revision and exact approved task/PR scope.
21. A task reaches DONE only after selective production promotion succeeds.
22. Post-task observations may become LearningCandidates; they are not automatically global rules.
23. Improvement candidates require replay/counterfactual evaluation and, where applicable, human approval + isolated canary + rollback proof.

## Canonical branch model

- `main`: production
- `staging`: permanent online test environment
- `feat/TASK-...`: isolated task development

Human approval is required for every production merge in current policy.

## Canonical lifecycle states

`PLANNED` → `READY` → `RUNNING` → `VERIFYING` → `VERIFIED` → `STAGING` → `AWAITING_HUMAN` → `APPROVED` → `DONE`

Controlled alternatives: `BLOCKED`, `FAILED`, `CHANGES_REQUESTED`, `REJECTED`.

No transition may bypass the state machine. `VERIFIED` never means production approval.

The `APPROVED → DONE` transition requires a structured task-specific promotion with `status=PROMOTED_TO_MAIN`, production PR and promoted commit. The whole staging branch is never promoted implicitly.

## Adaptive invariants

- stale blueprint revisions cannot execute/integrate;
- missing REQUIRED context blocks execution;
- missing harness capability returns BLOCKED/unsupported;
- verifier cannot repair reviewed code;
- uncertain dynamic code is never auto-deleted;
- cleanup debt cannot silently regress;
- learned candidates cannot self-promote;
- self-improvement cannot weaken protected safety controls.
