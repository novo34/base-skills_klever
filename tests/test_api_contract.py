import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from api.contracts import failure, success
from api.router_contract import resolve_route


def test_api_route_maps_to_control_action():
    assert resolve_route(
        "POST",
        "/api/projects/{project_id}/orders/{order_id}/approve",
    ) == "APPROVE_TASK"


def test_api_route_rejects_unknown_route():
    try:
        resolve_route("POST", "/api/unknown")
    except KeyError as exc:
        assert "api_route_not_registered" in str(exc)
        return
    raise AssertionError("unknown API route must fail")


def test_api_response_contracts():
    ok = success({"status": "ACTIVE"}, request_id="REQ-1")
    assert ok.ok is True
    assert ok.error is None

    err = failure("forbidden", request_id="REQ-2")
    assert err.ok is False
    assert err.error == "forbidden"


def test_budget_api_route_maps_to_control_action():
    assert resolve_route(
        "POST",
        "/api/projects/{project_id}/budget",
    ) == "SET_BUDGET"
