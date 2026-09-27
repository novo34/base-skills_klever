from __future__ import annotations

from typing import Any

from agents_runtime.developer import DeveloperAgent, DeveloperTask


class DeveloperFlow:
    def __init__(self, developer: DeveloperAgent):
        self.developer = developer

    def run(
        self,
        task: DeveloperTask,
        *,
        validation_commands: tuple[str, ...],
    ) -> dict[str, Any]:
        plan = self.developer.plan(task)
        results = self.developer.execute_commands(task, validation_commands)

        failed = [
            item for item in results
            if item["result"].get("exit_code") not in {0, None}
        ]
        diff = self.developer.collect_diff(task)

        return {
            "task_id": task.task_id,
            "plan": plan,
            "commands": results,
            "diff": diff,
            "status": "FAILED" if failed else "READY_FOR_REVIEW",
            "failures": failed,
        }
