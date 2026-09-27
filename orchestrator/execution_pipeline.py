from __future__ import annotations

from typing import Any

from github.service import GitHubService
from orchestrator.task_orchestrator import advance, create_task_execution
from verification.checks import command_exit_code, github_ci_status
from verification.evidence_builder import EvidenceBuilder
from verification.report import build_report
from verification.runtime import VerificationEvidence
from verification.service import VerificationService
from workspaces.service import WorkspaceService


class ExecutionPipeline:
    def __init__(
        self,
        github: GitHubService,
        workspaces: WorkspaceService,
        verification: VerificationService | None = None,
    ):
        self.github = github
        self.workspaces = workspaces
        self.verification = verification or VerificationService()
        self.evidence_builder = EvidenceBuilder()

    def start_task(
        self,
        *,
        task_id: str,
        repository: str,
        branch: str,
        triggers: set[str],
        flags: set[str],
        workspace_id: str,
        developer_agent: str = "developer",
    ) -> dict[str, Any]:
        execution = create_task_execution(task_id, triggers, flags)
        risk = execution["plan"]["risk"]

        execution = advance(execution, "READY")

        self.github.create_branch(
            repository=repository,
            task_id=task_id,
            agent=developer_agent,
            risk=risk,
            branch=branch,
        )

        self.workspaces.provision(
            workspace_id=workspace_id,
            task_id=task_id,
            repository=repository,
            branch=branch,
        )

        execution = advance(execution, "RUNNING")
        execution["repository"] = repository
        execution["branch"] = branch
        execution["workspace_id"] = workspace_id
        execution["triggers"] = sorted(triggers)
        return execution

    def run_command(self, execution: dict[str, Any], command: str) -> dict[str, Any]:
        result = self.workspaces.execute(execution["workspace_id"], command)
        return {
            "execution": execution,
            "command": command,
            "result": result,
        }

    def prepare_review(
        self,
        execution: dict[str, Any],
        *,
        title: str,
        body: str = "",
        developer_agent: str = "developer",
    ) -> dict[str, Any]:
        if execution["state"] != "RUNNING":
            raise RuntimeError("task_not_running")

        diff = self.workspaces.collect_diff(execution["workspace_id"])
        execution = advance(execution, "VERIFYING")

        pr = self.github.create_pull_request(
            repository=execution["repository"],
            task_id=execution["task_id"],
            agent=developer_agent,
            risk=execution["plan"]["risk"],
            branch=execution["branch"],
            title=title,
            body=body,
        )

        return {
            "execution": execution,
            "diff": diff,
            "pull_request": pr,
        }

    def verify(
        self,
        execution: dict[str, Any],
        *,
        evidence: VerificationEvidence,
    ) -> dict[str, Any]:
        if execution["state"] != "VERIFYING":
            raise RuntimeError("task_not_verifying")

        result = self.verification.evaluate(
            triggers=set(execution.get("triggers", [])),
            evidence=evidence,
        )

        if result.status == "VERIFIED":
            execution = advance(
                execution,
                "VERIFIED",
                verification_passed=True,
            )
        else:
            execution = advance(execution, "FAILED")

        execution["verification"] = {
            "status": result.status,
            "failures": list(result.failures),
        }

        return {
            "execution": execution,
            "verification": result,
        }

    def verify_from_sources(
        self,
        execution: dict[str, Any],
        *,
        requirement_ids: list[str],
        unit_result: dict[str, Any] | None,
        integration_result: dict[str, Any] | None,
        e2e_result: dict[str, Any] | None,
        diff_reviewed: bool,
        backend_verified: bool = False,
        frontend_verified: bool = False,
        database_verified: bool = False,
        notes: list[str] | None = None,
    ) -> dict[str, Any]:
        if execution["state"] != "VERIFYING":
            raise RuntimeError("task_not_verifying")

        checks = self.github.read_checks(
            repository=execution["repository"],
            ref=execution["branch"],
        )
        evidence = self.evidence_builder.from_sources(
            requirement_ids=requirement_ids,
            ci_status=github_ci_status(checks),
            unit_exit_code=command_exit_code(unit_result),
            integration_exit_code=command_exit_code(integration_result),
            e2e_exit_code=command_exit_code(e2e_result),
            diff_reviewed=diff_reviewed,
            backend_verified=backend_verified,
            frontend_verified=frontend_verified,
            database_verified=database_verified,
            notes=notes,
        )

        evaluated = self.verify(execution, evidence=evidence)
        evaluated["report"] = build_report(
            evaluated["execution"]["task_id"],
            evaluated["verification"],
        )
        return evaluated

    def teardown(self, execution: dict[str, Any]) -> dict[str, Any]:
        return self.workspaces.teardown(execution["workspace_id"])
