from __future__ import annotations

from channels.runtime import ChannelMessage, validate_channel_message
from intake.runtime import IntakeMessage
from intake.service import MultimodalIntakeService
from orders.runtime import WorkOrder


class ChannelIngressService:
    def __init__(self, intake: MultimodalIntakeService | None = None):
        self.intake = intake or MultimodalIntakeService()

    def to_intake(
        self,
        message: ChannelMessage,
        *,
        intake_id: str,
        intake_type: str = "GENERAL",
        target_repository: str | None = None,
        target_area: str | None = None,
    ) -> IntakeMessage:
        ok, failures = validate_channel_message(message)
        if not ok:
            raise ValueError(",".join(failures))

        return IntakeMessage(
            intake_id=intake_id,
            actor=message.actor,
            project_id=message.project_id,
            text=message.text,
            intake_type=intake_type,
            target_repository=target_repository,
            target_area=target_area,
            attachments=message.attachments,
        )

    def to_work_order(
        self,
        message: ChannelMessage,
        *,
        intake_id: str,
        order_id: str,
        title: str,
        intake_type: str = "GENERAL",
        target_repository: str | None = None,
        target_area: str | None = None,
    ) -> WorkOrder:
        intake = self.to_intake(
            message,
            intake_id=intake_id,
            intake_type=intake_type,
            target_repository=target_repository,
            target_area=target_area,
        )
        return self.intake.to_work_order(
            intake,
            order_id=order_id,
            title=title,
        )
