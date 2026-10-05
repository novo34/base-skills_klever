from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from models.gateway import ModelGateway
from models.gateway_contract import ModelRequest


@dataclass(frozen=True)
class ArchitectTask:
    task_id: str
    project_id: str
    objective: str
    constraints: tuple[str, ...]
    requirement_ids: tuple[str, ...]
    provider: str
    model: str
    fallback_chain: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class ArchitectureOutput:
    task_id: str
    adr: str
    workplan: tuple[str, ...]
    risk_assessment: str
    provider: str
    model: str


class ArchitectAgent:
    def __init__(self, *, gateway: ModelGateway):
        self.gateway = gateway

    def build_prompt(self, task: ArchitectTask) -> str:
        constraints = "\n".join(f"- {item}" for item in task.constraints)
        requirements = ", ".join(task.requirement_ids)
        return (
            f"Architecture task: {task.task_id}\n"
            f"Objective: {task.objective}\n"
            f"Requirements: {requirements}\n"
            f"Constraints:\n{constraints}\n"
            "Return architecture guidance only. Do not modify code. "
            "Output must include ADR, WORKPLAN and RISK_ASSESSMENT sections."
        )

    def plan(self, task: ArchitectTask) -> ArchitectureOutput:
        response = self.gateway.execute(
            ModelRequest(
                request_id=f"MODEL-{task.task_id}-ARCH",
                project_id=task.project_id,
                task_id=task.task_id,
                agent_role="architect",
                provider=task.provider,
                model=task.model,
                prompt=self.build_prompt(task),
            ),
            fallback_chain=task.fallback_chain,
        )

        content = response.content
        return ArchitectureOutput(
            task_id=task.task_id,
            adr=content,
            workplan=(content,),
            risk_assessment=content,
            provider=response.provider,
            model=response.model,
        )
