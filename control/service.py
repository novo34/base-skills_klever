from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable

from approvals.runtime import Approval
from audit.service import AuditService
from control.runtime import ControlCommand, validate_command
from management.dashboard import build_dashboard
from orders.runtime import WorkOrder
from orders.service import WorkOrderService
from projects.service import ProjectService
from reports.service import ReportService


class ControlService:
    def __init__(
        self,
        *,
        projects: ProjectService,
        orders: WorkOrderService,
        reports: ReportService,
        audit: AuditService | None = None,
        clock: Callable[[], str] | None = None,
    ):
        self.projects = projects
        self.orders = orders
        self.reports = reports
        self.audit = audit
        self.clock = clock or (lambda: datetime.now(timezone.utc).isoformat())

    def _audit_success(
        self,
        command: ControlCommand,
        *,
        object_type: str,
        object_id: str,
        rationale: str | None = None,
    ) -> None:
        if self.audit is None:
            return
        self.audit.record(
            event_id=f"AUD-{command.command_id}",
            actor=command.actor,
            actor_type="human",
            action=command.action,
            project_id=command.project_id,
            object_type=object_type,
            object_id=object_id,
            task_id=command.target_id,
            result="SUCCESS",
            timestamp=self.clock(),
            rationale=rationale,
        )

    def execute(
        self,
        command: ControlCommand,
        *,
        approvals: list[Approval] | None = None,
        all_orders: list[WorkOrder] | None = None,
        monthly_cost_chf: float = 0.0,
    ) -> dict:
        ok, failures = validate_command(command)
        if not ok:
            raise ValueError(",".join(failures))

        approvals = approvals or []
        all_orders = all_orders or []

        if command.action == "GET_PROJECT_STATUS":
            project = self.projects.get(command.project_id)
            return {
                "project_id": project.project_id,
                "name": project.name,
                "status": project.status,
                "repository": project.repository,
                "staging_url": project.staging_url,
            }

        if command.action == "GET_DASHBOARD":
            return build_dashboard(
                projects=self.projects.list(),
                orders=all_orders,
                approvals=approvals,
                monthly_cost_chf=monthly_cost_chf,
            )

        if command.action == "GET_REPORT":
            project = self.projects.get(command.project_id)
            return self.reports.project_report(
                project=project,
                orders=all_orders,
                approvals=approvals,
            )

        if command.action == "CREATE_ORDER":
            payload = command.payload or {}
            order = WorkOrder(
                order_id=payload["order_id"],
                project_id=command.project_id,
                title=payload["title"],
                description=payload["description"],
                status=payload.get("status", "QUEUED"),
                priority=payload.get("priority", "NORMAL"),
                requirement_ids=tuple(payload.get("requirement_ids", [])),
                created_by=command.actor,
                budget_limit_chf=payload.get("budget_limit_chf"),
            )
            result = self.orders.create(order)
            self._audit_success(command, object_type="order", object_id=order.order_id)
            return result

        if command.action == "PAUSE_PROJECT":
            project = self.projects.set_status(command.project_id, "PAUSED")
            self._audit_success(command, object_type="project", object_id=project.project_id)
            return {"project": project}

        if command.action == "RESUME_PROJECT":
            project = self.projects.set_status(command.project_id, "ACTIVE")
            self._audit_success(command, object_type="project", object_id=project.project_id)
            return {"project": project}

        if command.action == "RETRY_TASK":
            if not command.target_id:
                raise ValueError("target_id_required")
            order = self.orders.retry(command.target_id)
            self._audit_success(command, object_type="order", object_id=order.order_id)
            return {"order": order}

        if command.action == "REQUEST_AUDIT":
            if not command.target_id:
                raise ValueError("target_id_required")
            order = self.orders.request_audit(command.target_id)
            self._audit_success(command, object_type="order", object_id=order.order_id)
            return {"order": order}

        if command.action in {"APPROVE_TASK", "REQUEST_CHANGES", "REJECT_TASK"}:
            if not command.target_id:
                raise ValueError("target_id_required")

            desired = {
                "APPROVE_TASK": "APPROVED",
                "REQUEST_CHANGES": "CHANGES_REQUESTED",
                "REJECT_TASK": "REJECTED",
            }[command.action]

            current = self.orders.get(command.target_id)
            if current.status != "AWAITING_HUMAN":
                raise ValueError("order_not_awaiting_human")

            order = self.orders.update_status(command.target_id, desired)
            self._audit_success(
                command,
                object_type="order",
                object_id=order.order_id,
                rationale=(command.payload or {}).get("note"),
            )
            return {"order": order}

        raise NotImplementedError(command.action)
