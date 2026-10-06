# Required GitHub Repository Security Settings

These settings are part of the JEV Foundation security model and must be
enabled in GitHub repository administration.

## Supported operating mode

This repository currently uses **single-operator mode**. The repository owner
must not be forced to satisfy an impossible self-review requirement. Instead,
merge authorization relies on two independent required status checks:

- `validate`: executes the complete Foundation validation/test suite on the PR.
- `independent-review`: executes trusted policy code from the PR base revision,
  reads the authoritative GitHub PR file list, includes previous filenames for
  renames, derives risk, and refuses security-gate/self-protection changes that
  do not satisfy the required R4 acknowledgement.

The independent-review workflow uses `pull_request_target` only as a
**base-controlled policy evaluator**. It does not checkout, import, source, or
execute code from the PR head and has read-only repository/PR permissions.

## Required for `main` in single-operator mode

- Protect the branch or apply an equivalent repository ruleset.
- Require pull requests before merging.
- Require **0 human approvals** while there is only one authorized human
  operator; self-approval is not treated as independent review.
- Do **not** require CODEOWNER approval while the sole CODEOWNER is also the PR
  author. CODEOWNERS remains the ownership map for critical paths.
- Require the `validate` status check.
- Require the `independent-review` status check.
- Require branches to be up to date before merging.
- Require conversation resolution.
- Block force pushes.
- Block branch deletion.
- Do not configure automation bypasses except explicitly reviewed break-glass
  administration.

If a second trusted human maintainer is added later, human approval and
CODEOWNER-review requirements may be re-enabled as an additional gate; they do
not replace the two required automated checks.

## Critical owned/self-protection paths

Defined by `.github/CODEOWNERS` and the independent-review policy, including:

- `.github/`
- `scripts/`
- `authz/`
- `authorization/`
- `auth/`
- `approvals/`
- `policies/`
- `models/credentials.py`
- `secrets/`
- `credentials/`
- `staging/`
- `agents_runtime/edit_protocol.py`
- database schema/migration surfaces
- API contract surfaces
- production/deployment surfaces

Changes to the review mechanism itself are self-protection changes and require
`JEV-RISK: R4` plus:

`JEV-INDEPENDENT-REVIEW: acknowledged`

## Structural limitation and mitigation

A workflow stored only on a PR branch can attempt to weaken its own validation.
For that reason, the independent-review check runs trusted code from the
**target branch revision**, not from the PR head. Its file list comes from the
GitHub Pull Request Files API rather than PR-controlled scripts.

Repository rulesets are still an external control boundary. CI can verify
repository-visible state, but repository administrators must keep the required
checks and branch restrictions enabled.
