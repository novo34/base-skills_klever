# JEV GitHub Engine

The GitHub layer is deliberately split into three parts:

1. **Policy guard/runtime** — decides whether an operation is allowed.
2. **Service** — exposes safe application-level GitHub operations.
3. **Adapter** — performs the already-authorized operation using a GitHub App, connector or another transport.

This separation is intentional. A GitHub transport must never decide policy.

## Flow

Task -> JEV policy -> GitHubService -> Adapter -> GitHub

If policy rejects an operation, the adapter is never called.

## Initial supported actions

- read repository
- create task branch
- write file to task branch
- create pull request
- read CI/check status
- merge pull request through integrator gate

Direct writes to main/master remain forbidden.
