from __future__ import annotations

from intake.runtime import IntakeMessage, validate_intake
from orders.runtime import WorkOrder


VISUAL_WORK_TYPES = {
    "IMAGE_REPLACEMENT",
    "IMAGE_GENERATION",
    "IMAGE_EDIT",
    "UI_REFERENCE_REDESIGN",
}


class MultimodalIntakeService:
    def to_work_order(
        self,
        message: IntakeMessage,
        *,
        order_id: str,
        title: str,
        priority: str = "NORMAL",
    ) -> WorkOrder:
        ok, failures = validate_intake(message)
        if not ok:
            raise ValueError(",".join(failures))

        reference_ids = tuple(
            item.attachment_id
            for item in message.attachments
        )
        reference_bindings = tuple(
            (item.attachment_id, item.role)
            for item in message.attachments
        )

        return WorkOrder(
            order_id=order_id,
            project_id=message.project_id,
            title=title,
            description=message.text,
            status="QUEUED",
            priority=priority,
            created_by=message.actor,
            target_repository=message.target_repository,
            work_type=message.intake_type,
            reference_ids=reference_ids,
            reference_bindings=reference_bindings,
            target_area=message.target_area,
        )

    def requires_manual_staging_review(self, message: IntakeMessage) -> bool:
        return message.intake_type in VISUAL_WORK_TYPES
