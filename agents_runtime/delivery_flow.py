from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from agents_runtime.delivery_adapter import DeveloperDeliveryAdapter
from agents_runtime.developer import DeveloperAgent, DeveloperTask
from agents_runtime.edit_protocol import EditPlan, validate_edit_plan


@dataclass(frozen=True)
class DeveloperDeliveryRequest:
    task: DeveloperTask
    edit_plan: EditPlan
    validation_commands: tuple[str, ...]
    allowed_roots: tuple[str, ...]
    commit_message: str
    pull_request_title: str
    pull_request_body: str = ""
    base_branch: str = "main"


class DeveloperDeliveryFlow:
    def __init__(
        self,
        *,
        developer: DeveloperAgent,
        delivery: DeveloperDeliveryAdapter,
    ):
        self.developer = developer
        self.delivery = delivery

    def run(self, request: DeveloperDeliveryRequest) -> dict[str, Any]:
        task = request.task

        validate_edit_plan(
            request.edit_plan,
            task_id=task.task_id,
            workspace_id=task.workspace_id,
            branch=task.branch,
            allowed_roots=request.allowed_roots,
        )

        self.delivery.apply_edit_plan(task.workspace_id, request.edit_plan)

        validation_results = self.developer.execute_commands(
            task,
            request.validation_commands,
        )
        failures = [
            item
            for item in validation_results
            if item["result"].get("exit_code") not in {0, None}
        ]
        diff = self.developer.collect_diff(task)

        if failures:
            return {
                "task_id": task.task_id,
                "status": "FAILED_VALIDATION",
                "stage": "validation",
                "validation": validation_results,
                "failures": failures,
                "diff": diff,
                "commit": None,
                "pull_request": None,
            }

        commit = self.delivery.commit_and_push(
            task.workspace_id,
            branch=task.branch,
            message=request.commit_message,
        )

        if commit.branch != task.branch:
            raise RuntimeError("delivery_commit_branch_mismatch")

        pull_request = self.delivery.create_pull_request(
            repository=task.repository,
            task_id=task.task_id,
            branch=task.branch,
            base_branch=request.base_branch,
            title=request.pull_request_title,
            body=request.pull_request_body,
        )

        return {
            "task_id": task.task_id,
            "status": "PR_OPEN",
            "stage": "delivery",
            "validation": validation_results,
            "failures": [],
            "diff": diff,
            "commit": commit,
            "pull_request": pull_request,
            "next_role": "verifier",
        }
