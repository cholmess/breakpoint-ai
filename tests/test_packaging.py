import json
from importlib import resources


def test_default_policies_json_is_packaged():
    resource = resources.files("breakpoint.config").joinpath("default_policies.json")
    with resource.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    assert "cost_policy" in payload
    assert "pii_policy" in payload
    assert "drift_policy" in payload
