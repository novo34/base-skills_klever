import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents_runtime.edit_protocol import (
    EditPlan,
    EditPolicyError,
    FileEdit,
    validate_edit_plan,
)


def valid_plan():
    return EditPlan(
        task_id="TASK-1",
        workspace_id="WS-1",
        branch="feat/TASK-1",
        edits=(
            FileEdit(
                path="app/contact/page.tsx",
                operation="UPDATE",
                content="export default function Page() {}",
            ),
        ),
    )


def test_edit_plan_accepts_scoped_task_edit():
    validate_edit_plan(
        valid_plan(),
        task_id="TASK-1",
        workspace_id="WS-1",
        branch="feat/TASK-1",
        allowed_roots=("app/contact",),
    )


def test_edit_plan_rejects_path_traversal():
    plan = EditPlan(
        task_id="TASK-1",
        workspace_id="WS-1",
        branch="feat/TASK-1",
        edits=(FileEdit(path="../secret", operation="UPDATE", content="x"),),
    )
    try:
        validate_edit_plan(
            plan,
            task_id="TASK-1",
            workspace_id="WS-1",
            branch="feat/TASK-1",
        )
    except EditPolicyError as exc:
        assert "path_traversal_forbidden" in str(exc)
        return
    raise AssertionError("path traversal must be rejected")


def test_edit_plan_rejects_wrong_workspace():
    try:
        validate_edit_plan(
            valid_plan(),
            task_id="TASK-1",
            workspace_id="WS-OTHER",
            branch="feat/TASK-1",
        )
    except EditPolicyError as exc:
        assert "workspace_mismatch" in str(exc)
        return
    raise AssertionError("workspace mismatch must fail")


def test_edit_plan_rejects_out_of_scope_file():
    try:
        validate_edit_plan(
            valid_plan(),
            task_id="TASK-1",
            workspace_id="WS-1",
            branch="feat/TASK-1",
            allowed_roots=("api",),
        )
    except EditPolicyError as exc:
        assert "edit_outside_allowed_scope" in str(exc)
        return
    raise AssertionError("out-of-scope edit must fail")


def test_edit_plan_rejects_main_branch():
    plan = EditPlan(
        task_id="TASK-1",
        workspace_id="WS-1",
        branch="main",
        edits=(FileEdit(path="app/page.tsx", operation="UPDATE", content="x"),),
    )
    try:
        validate_edit_plan(
            plan,
            task_id="TASK-1",
            workspace_id="WS-1",
            branch="main",
        )
    except EditPolicyError as exc:
        assert "default_branch_edit_forbidden" in str(exc)
        return
    raise AssertionError("main branch edit must fail")
