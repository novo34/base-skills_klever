import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("trace_requirement", ROOT / "scripts" / "trace_requirement.py")
trace_requirement = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(trace_requirement)


def test_requirement_trace_record():
    record = trace_requirement.build_record(
        "REQ-PLN-041",
        "docs/product-specs/SPEC.md",
        "VERIFYING",
        "TASK-041",
        "feat/REQ-PLN-041-rest-period",
        123,
        ["src/rest.py"],
        ["tests/unit/test_rest.py"],
        ["tests/integration/test_rest.py"],
        ["tests/e2e/test_rest.py"],
        "PASS",
    )

    assert record["id"] == "REQ-PLN-041"
    assert record["implementation"]["pull_request"] == 123
    assert record["verification"]["result"] == "PASS"
    assert record["verification"]["e2e_tests"]


def test_invalid_requirement_id_rejected():
    try:
        trace_requirement.build_record(
            "PLN-41",
            "SPEC.md",
            "PLANNED",
            "TASK-1",
            "feat/x",
            None,
            [],
            [],
            [],
            [],
            "NOT_RUN",
        )
    except ValueError:
        return
    raise AssertionError("invalid requirement id must fail")
