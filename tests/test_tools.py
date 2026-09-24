"""TICKET 2 — tool schemas the model can act on, and an executor that never raises."""

import json

from triage import tools


def test_three_tools_are_defined():
    names = {t["name"] for t in tools.TOOLS}
    assert names == {"get_service_metrics", "get_recent_deploys", "get_dependencies"}


def test_every_tool_has_a_description_and_a_schema():
    assert tools.TOOLS, "no tools defined"
    for tool in tools.TOOLS:
        assert tool.get("description"), f"{tool['name']} has no description"
        schema = tool.get("input_schema")
        assert schema and schema.get("type") == "object"
        assert "properties" in schema


def test_descriptions_are_differentiated():
    # Two tools whose descriptions could be swapped will get confused at runtime.
    descriptions = [t["description"].lower() for t in tools.TOOLS]
    assert len(descriptions) == 3, "expected three tools"
    assert len(set(descriptions)) == len(descriptions)
    for description in descriptions:
        assert len(description) > 40, "too terse to disambiguate at call time"


def test_every_tool_requires_a_service():
    assert tools.TOOLS, "no tools defined"
    for tool in tools.TOOLS:
        assert "service" in tool["input_schema"].get("required", [])


def test_metrics_returns_parseable_json():
    out = json.loads(tools.run_tool("get_service_metrics", {"service": "checkout-api"}))
    assert "p99_ms" in out


def test_deploys_shows_the_dependency_shipped_recently():
    # The fixture's whole point: checkout-api is stale, payments-svc is not.
    checkout = json.loads(tools.run_tool("get_recent_deploys", {"service": "checkout-api"}))
    payments = json.loads(tools.run_tool("get_recent_deploys", {"service": "payments-svc"}))
    assert checkout[0]["minutes_ago"] > 1000
    assert payments[0]["minutes_ago"] < 120


def test_dependencies_are_returned():
    out = json.loads(tools.run_tool("get_dependencies", {"service": "checkout-api"}))
    assert "payments-svc" in json.dumps(out)


def test_unknown_tool_returns_an_error_rather_than_raising():
    # The loop must keep going and tell the model what went wrong.
    out = json.loads(tools.run_tool("get_the_answer", {"service": "checkout-api"}))
    assert "error" in json.dumps(out).lower()


def test_unknown_service_returns_an_error_rather_than_raising():
    out = json.loads(tools.run_tool("get_service_metrics", {"service": "no-such-svc"}))
    assert "error" in json.dumps(out).lower()
