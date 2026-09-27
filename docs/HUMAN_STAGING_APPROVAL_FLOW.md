# Human staging approval flow

For functional or UI work, JEV must not ask for human approval immediately after automated verification.

The required flow is:

1. Task branch passes automated verification.
2. The specific task is integrated into the project's permanent `staging` environment.
3. Staging is confirmed online and connected to its separate staging database.
4. JEV exposes the staging URL to the human reviewer.
5. Human tests the change manually.
6. Human chooses Approve, Reject, or requests changes.
7. Only an approved task may receive a task-specific production PR.
8. JEV never promotes the complete staging branch merely because one task was approved.

The permanent staging environment remains available for future tasks.
