import copy
import json
import pathlib
import sys

import pytest
from jsonschema import Draft202012Validator, ValidationError

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_schema_examples import validate_examples


def test_all_adaptive_schema_examples_are_valid():
    assert validate_examples(ROOT) == []


@pytest.mark.parametrize(
    "example_name",
    [
        "intent-brief.json",
        "acceptance-contract.json",
        "execution-blueprint.json",
        "context-pack.json",
        "plan-revision.json",
        "decision-record.json",
        "learning-candidate.json",
        "counterfactual-eval-report.json",
        "hygiene-report.json",
    ],
)
def test_each_schema_example_has_negative_required_field_case(example_name):
    wrapper = json.loads(
        (ROOT / "examples" / "adaptive" / example_name).read_text(encoding="utf-8")
    )
    schema = json.loads(
        (ROOT / "schemas" / wrapper["schema"]).read_text(encoding="utf-8")
    )
    payload = copy.deepcopy(wrapper["payload"])
    required = schema["required"]
    assert required
    payload.pop(required[0], None)

    with pytest.raises(ValidationError):
        Draft202012Validator(schema).validate(payload)
