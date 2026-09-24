"""TICKET 7 — the agent declining to conclude, on purpose."""

from triage import routing


def test_two_routing_tools_are_defined():
    names = {t["name"] for t in routing.ROUTING_TOOLS}
    assert names == {"request_clarification", "escalate"}


def test_routing_tools_have_usable_schemas():
    assert routing.ROUTING_TOOLS, "no routing tools defined"
    by_name = {t["name"]: t for t in routing.ROUTING_TOOLS}

    clarify = by_name["request_clarification"]["input_schema"]
    assert "question" in clarify["properties"]
    assert "question" in clarify.get("required", [])

    escalate = by_name["escalate"]["input_schema"]
    assert "reason" in escalate["properties"]
    assert "severity" in escalate["properties"]


def test_descriptions_say_when_to_reach_for_them():
    assert routing.ROUTING_TOOLS, "no routing tools defined"
    for tool in routing.ROUTING_TOOLS:
        assert len(tool.get("description", "")) > 50, (
            f"{tool['name']}: too terse to tell the model WHEN to use it"
        )


def test_no_routing_tool_called_means_an_answer():
    assert routing.disposition(["get_service_metrics", "get_recent_deploys"]) == "answer"


def test_an_empty_run_is_still_an_answer():
    assert routing.disposition([]) == "answer"


def test_a_clarification_request_is_not_an_answer():
    assert routing.disposition(["get_service_metrics", "request_clarification"]) == "clarify"


def test_an_escalation_is_not_an_answer():
    assert routing.disposition(["get_service_metrics", "escalate"]) == "escalate"


def test_escalation_outranks_clarification_regardless_of_order():
    # An escalation downgraded because a later turn asked a question is the bug
    # this precedence exists to prevent.
    assert routing.disposition(["escalate", "request_clarification"]) == "escalate"
    assert routing.disposition(["request_clarification", "escalate"]) == "escalate"


def test_handoff_note_names_the_disposition_and_the_detail():
    note = routing.handoff_note("escalate", "three changes landed the same day")
    assert "escalat" in note.lower()
    assert "three changes" in note


def test_a_clarification_handoff_carries_the_question():
    note = routing.handoff_note("clarify", "Which region are the affected customers in?")
    assert "region" in note
