from __future__ import annotations

from budgets.runtime import BudgetPolicy, validate_policy


class BudgetPolicyRegistry:
    def __init__(self):
        self._policies: dict[str, BudgetPolicy] = {}

    def set(self, policy: BudgetPolicy) -> BudgetPolicy:
        ok, failures = validate_policy(policy)
        if not ok:
            raise ValueError(",".join(failures))
        self._policies[policy.project_id] = policy
        return policy

    def get(self, project_id: str) -> BudgetPolicy | None:
        return self._policies.get(project_id)

    def require(self, project_id: str) -> BudgetPolicy:
        policy = self.get(project_id)
        if policy is None:
            raise KeyError("budget_policy_not_found")
        return policy
