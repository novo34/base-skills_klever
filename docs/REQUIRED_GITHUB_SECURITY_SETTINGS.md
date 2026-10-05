# Required GitHub Repository Security Settings

These settings are part of the JEV Foundation security model and must be enabled in GitHub repository administration.

## Required for `main`

- Protect the branch or apply an equivalent repository ruleset.
- Require pull requests before merging.
- Require at least one approving review.
- Require review from CODEOWNERS.
- Require the `Validate JEV foundation / validate` status check.
- Dismiss stale approvals when new commits are pushed.
- Require conversation resolution.
- Block force pushes.
- Block branch deletion.
- Do not allow bypass for automation accounts except explicitly reviewed break-glass administration.

## Recommended for `jev-v7-foundation`

- Require pull requests for changes to governance/security-critical files when feasible.
- Require the same validation workflow.
- Require CODEOWNER review for critical paths.

## Critical owned paths

Defined in `.github/CODEOWNERS`, including:

- `.github/`
- `scripts/`
- `authz/`
- `approvals/`
- `policies/`
- `models/credentials.py`
- `staging/`
- `agents_runtime/edit_protocol.py`

## Important limitation

CODEOWNERS does not enforce review by itself. Enforcement requires GitHub branch protection or a repository ruleset with "Require review from Code Owners" enabled.

The Foundation CI cannot safely self-protect against a malicious PR that modifies its own workflow unless repository-level branch protection/rulesets enforce review and required checks outside the PR-controlled code.
