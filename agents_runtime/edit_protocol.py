from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath


class EditPolicyError(PermissionError):
    pass


@dataclass(frozen=True)
class FileEdit:
    path: str
    operation: str
    content: str | None = None


@dataclass(frozen=True)
class EditPlan:
    task_id: str
    workspace_id: str
    branch: str
    edits: tuple[FileEdit, ...]


ALLOWED_OPERATIONS = {"CREATE", "UPDATE", "DELETE"}


def _normalized_relative_path(path: str) -> PurePosixPath:
    if not path or path.startswith("/") or "\\" in path:
        raise EditPolicyError("invalid_edit_path")
    candidate = PurePosixPath(path)
    if ".." in candidate.parts:
        raise EditPolicyError("path_traversal_forbidden")
    posix = candidate.as_posix()
    if (
        posix == ".git"
        or posix.startswith(".git/")
        or posix == ".github/workflows"
        or posix.startswith(".github/workflows/")
    ):
        raise EditPolicyError("protected_path")
    return candidate


def validate_edit_plan(
    plan: EditPlan,
    *,
    task_id: str,
    workspace_id: str,
    branch: str,
    allowed_roots: tuple[str, ...] = (),
) -> None:
    if plan.task_id != task_id:
        raise EditPolicyError("task_mismatch")
    if plan.workspace_id != workspace_id:
        raise EditPolicyError("workspace_mismatch")
    if plan.branch != branch:
        raise EditPolicyError("branch_mismatch")
    if branch in {"main", "master"}:
        raise EditPolicyError("default_branch_edit_forbidden")
    if not plan.edits:
        raise EditPolicyError("empty_edit_plan")

    normalized_roots = tuple(
        str(_normalized_relative_path(root)).rstrip("/")
        for root in allowed_roots
    )

    seen: set[str] = set()
    for edit in plan.edits:
        if edit.operation not in ALLOWED_OPERATIONS:
            raise EditPolicyError("unsupported_edit_operation")

        normalized = str(_normalized_relative_path(edit.path))
        if normalized in seen:
            raise EditPolicyError("duplicate_edit_path")
        seen.add(normalized)

        if normalized_roots and not any(
            normalized == root or normalized.startswith(root + "/")
            for root in normalized_roots
        ):
            raise EditPolicyError("edit_outside_allowed_scope")

        if edit.operation in {"CREATE", "UPDATE"} and edit.content is None:
            raise EditPolicyError("edit_content_required")
        if edit.operation == "DELETE" and edit.content is not None:
            raise EditPolicyError("delete_content_must_be_empty")
