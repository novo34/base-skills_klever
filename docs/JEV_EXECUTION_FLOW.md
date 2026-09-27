# JEV executable task flow

The current foundation now supports an executable orchestration path:

1. Receive a task.
2. Classify risk.
3. Resolve relevant skills.
4. Select required agents and model tier.
5. Move task from PLANNED to READY.
6. Create a dedicated Git branch.
7. Provision an isolated workspace.
8. Move task to RUNNING.
9. Execute allow-listed commands in the workspace.
10. Collect the resulting diff.
11. Open a pull request.
12. Move task to VERIFYING.
13. Record verifier outcome.
14. Move to VERIFIED or FAILED.
15. Destroy the workspace.

Important: this foundation deliberately stops before autonomous merge. Merge remains a separately gated action handled only after verification and, for R4, human approval.
