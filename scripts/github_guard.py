from __future__ import annotations

FORBIDDEN_DIRECT_BRANCHES = {"main", "master"}

AGENT_MUTATIONS = {
    "CREATE_BRANCH": {"developer", "integrator"},
    "WRITE_FILE": {"developer", "integrator"},
    "CREATE_COMMIT": {"developer", "integrator"},
    "CREATE_PULL_REQUEST": {"developer", "integrator"},
    "REQUEST_REVIEW": {"developer", "integrator", "verifier"},
    "MERGE_PULL_REQUEST": {"integrator"},
}


def authorize(operation: str, agent: str, risk: str, branch: str | None = None,
              verifier_passed: bool = False, human_approved: bool = False) -> tuple[bool, str]:
    allowed = AGENT_MUTATIONS.get(operation)
    if allowed is not None and agent not in allowed:
        return False, "agent_not_authorized"

    if operation in {"WRITE_FILE", "CREATE_COMMIT"} and branch in FORBIDDEN_DIRECT_BRANCHES:
        return False, "direct_default_branch_write_forbidden"

    if operation == "MERGE_PULL_REQUEST":
        if not verifier_passed:
            return False, "verification_required"
        if risk == "R4" and not human_approved:
            return False, "human_approval_required"

    return True, "ok"
