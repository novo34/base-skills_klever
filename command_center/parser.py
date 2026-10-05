from __future__ import annotations

import re

from command_center.runtime import CommandIntent


def parse_command(*, intent_id: str, actor: str, text: str) -> CommandIntent:
    normalized = " ".join(text.strip().split())
    lower = normalized.lower()

    if lower.startswith("pausa "):
        project = normalized.split(" ", 1)[1].strip()
        return CommandIntent(
            intent_id=intent_id,
            actor=actor,
            text=normalized,
            project_id=project.lower(),
            action="PAUSE_PROJECT",
            confidence=0.99,
            requires_confirmation=False,
        )

    if lower.startswith("reanuda "):
        project = normalized.split(" ", 1)[1].strip()
        return CommandIntent(
            intent_id=intent_id,
            actor=actor,
            text=normalized,
            project_id=project.lower(),
            action="RESUME_PROJECT",
            confidence=0.99,
            requires_confirmation=False,
        )

    budget = re.match(r"no gastes más de\s+chf\s*([0-9]+(?:\.[0-9]+)?)\s+en\s+(.+)", lower)
    if budget:
        amount = float(budget.group(1))
        project = budget.group(2).strip()
        return CommandIntent(
            intent_id=intent_id,
            actor=actor,
            text=normalized,
            project_id=project.lower(),
            action="SET_BUDGET",
            confidence=0.98,
            requires_confirmation=True,
            payload={"limit_chf": amount},
        )

    if lower.startswith("audita "):
        target = normalized.split(" ", 1)[1].strip()
        return CommandIntent(
            intent_id=intent_id,
            actor=actor,
            text=normalized,
            action="REQUEST_AUDIT",
            target_id=target,
            confidence=0.95,
            requires_confirmation=False,
        )

    return CommandIntent(
        intent_id=intent_id,
        actor=actor,
        text=normalized,
        confidence=0.0,
        requires_confirmation=True,
    )
