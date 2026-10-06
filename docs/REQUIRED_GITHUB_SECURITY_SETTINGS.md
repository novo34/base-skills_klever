# Required GitHub Repository Security Settings

These settings are part of the JEV Foundation security model and must be enabled in GitHub repository administration.

## Supported governance mode

This repository is operated by a single human owner. GitHub does not permit an author to satisfy their own required approving review, so human-review requirements that would deadlock the repository are replaced by two independent required status checks:

- `validate`: executes the full Foundation validation/test suite on the PR revision.
- `independent-review`: runs from the trusted base revision via `pull_request_target`, reads the authoritative GitHub PR file list, does not execute PR-head code, and independently enforces risk/self-protection policy.

This is a deliberate single-operator control design, not a bypass of review.

## Required for `main`

- Protect the branch or apply an equivalent repository ruleset.
- Require pull requests before merging.
- Require the `validate` status check.
- Require the `independent-review` status check.
- Require branches to be up to date before merging.
- Require conversation resolution.
- Block force pushes.
- Block branch deletion.
- Set required approving reviews to **0** in single-operator mode.
- Do **not** require CODEOWNER approval in single-operator mode.
- Do not allow bypass for automation accounts except explicitly reviewed break-glass administration.

## Independent review invariants

The `independent-review` workflow must:

- use `pull_request_target`;
- check out the exact trusted base SHA, never the PR head;
- use read-only repository/pull-request permissions;
- obtain changed files from the GitHub API;
- include `previous_filename` so rename sources cannot disappear;
- require an explicit `JEV-RISK: R#` declaration;
- fail when declared risk is below derived risk;
- require R4 plus `JEV-INDEPENDENT-REVIEW: acknowledged` for changes to its own security/review surfaces;
- never execute scripts, binaries, workflow code, or dependencies from the untrusted PR head.

## CODEOWNERS

`.github/CODEOWNERS` remains the canonical ownership map for critical paths and future multi-reviewer operation. In current single-operator mode it is informational metadata consumed by governance/audit, not a required GitHub approval gate.

Critical owned paths include:

- `.github/`
- `scripts/`
- `authz/`
- `approvals/`
- `policies/`
- `models/credentials.py`
- `staging/`
- `agents_runtime/edit_protocol.py`

## Important limitation

A workflow stored only on a PR branch cannot protect its own first introduction. The initial bootstrap of `independent-review` therefore requires a one-time repository-settings transition. After the workflow exists on `main`, both `validate` and `independent-review` must be required by the repository ruleset before normal development continues.

The trusted-base design prevents a PR from weakening the independent gate merely by modifying its own copy of the workflow or review script.
