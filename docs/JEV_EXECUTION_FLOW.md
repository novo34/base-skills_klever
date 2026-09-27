# JEV executable task flow

The canonical flow is:

1. Receive a task.
2. Classify risk.
3. Resolve relevant skills.
4. Select required agents and model tier.
5. Create a dedicated task branch.
6. Provision an isolated development workspace.
7. Implement and run automated tests.
8. Create the task pull request and collect CI evidence.
9. Run the Verification Engine.
10. If verification fails, return the task to corrective work.
11. If VERIFIED, integrate that specific task into the project's permanent staging branch.
12. Confirm the permanent staging environment is online:
    - web reachable
    - backend reachable
    - staging database connected
    - migrations current
13. Expose the staging URL for manual human testing.
14. Human chooses APPROVED, CHANGES_REQUESTED, or REJECTED.
15. Only APPROVED tasks may receive a task-specific production PR.
16. The Integrator may merge that production PR only with verification and human approval.
17. The complete staging branch is never promoted wholesale to main.
18. Development workspaces may be destroyed after execution; the permanent staging environment and its staging database remain.

## Canonical branch model

- `main`: production
- `staging`: permanent online test environment
- `feat/TASK-...`: isolated task development

Human approval is required for every merge to production in the current JEV policy.
