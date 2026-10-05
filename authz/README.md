# JEV Authorization

Authorization is enforced server-side, not merely by hiding UI controls.

Initial roles:

- ADMIN
- PROJECT_MANAGER
- DEVELOPER
- AUDITOR
- CLIENT

Every control command must pass two checks:

1. the role is allowed to perform the action;
2. the actor is allowed to access the target project.

Agents use their own capability contracts and do not inherit human permissions automatically.
