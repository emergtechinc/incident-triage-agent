"""TICKET 5 — the stop_reason state machine.

Driven by a scripted fake client, so these run with no API key and no network.
"""

from triage import loop as loop_module
from triage.bounds import Bounds
from triage.fake import FakeClient, refused, says, truncated, wants_tool, wants_tools

MODEL = "claude-sonnet-5"


def run(script, bounds=None, tools=None):
    return loop_module.run(
        FakeClient(script),
        model=MODEL,
        system="triage this",
        incident="something is broken",
        bounds=bounds or Bounds(),
        tools=tools if tools is not None else [],
    )


def test_a_single_end_turn_completes():
    outcome = run([says("The pool is exhausted.")])
    assert outcome.status == "completed"
    assert "pool" in outcome.answer
    assert outcome.turns == 1
    assert outcome.is_answer


def test_a_tool_request_is_executed_and_the_loop_continues():
    outcome = run([
        wants_tool("get_service_metrics", {"service": "checkout-api"}),
        says("Latency rose 45 minutes ago."),
    ])
    assert outcome.status == "completed"
    assert outcome.turns == 2
    assert "get_service_metrics" in outcome.tool_calls


def test_several_tools_in_one_turn_all_run():
    outcome = run([
        wants_tools(("get_service_metrics", {"service": "checkout-api"}),
                    ("get_recent_deploys", {"service": "checkout-api"})),
        says("Its dependency shipped recently."),
    ])
    assert outcome.tool_calls.count("get_service_metrics") == 1
    assert outcome.tool_calls.count("get_recent_deploys") == 1


def test_parallel_results_are_returned_in_ONE_message():
    # The mistake that silently trains the model out of parallel calls.
    client = FakeClient([
        wants_tools(("get_service_metrics", {"service": "checkout-api"}),
                    ("get_dependencies", {"service": "checkout-api"})),
        says("done"),
    ])
    loop_module.run(client, model=MODEL, system="s", incident="i",
                    bounds=Bounds(), tools=[])
    second_request = client.calls[1]["messages"]
    user_messages = [m for m in second_request if m["role"] == "user"]
    tool_result_messages = [
        m for m in user_messages
        if isinstance(m["content"], list)
        and any(b.get("type") == "tool_result" for b in m["content"])
    ]
    assert len(tool_result_messages) == 1, "results were split across messages"
    assert len(tool_result_messages[0]["content"]) == 2


def test_the_assistant_turn_is_appended_verbatim():
    # Drop the tool_use blocks and the conversation is incoherent.
    client = FakeClient([
        wants_tool("get_dependencies", {"service": "checkout-api"}),
        says("done"),
    ])
    loop_module.run(client, model=MODEL, system="s", incident="i",
                    bounds=Bounds(), tools=[])
    second_request = client.calls[1]["messages"]
    assistant = [m for m in second_request if m["role"] == "assistant"]
    assert assistant, "the assistant turn was never appended"


def test_max_tokens_is_NOT_treated_as_success():
    # The failure this build exists to prevent: a truncated half-answer
    # returned to a user as though it were finished.
    outcome = run([truncated("The likely cause is that the connection")])
    assert outcome.status == "truncated"
    assert not outcome.is_answer


def test_a_refusal_is_its_own_outcome():
    outcome = run([refused()])
    assert outcome.status == "refused"
    assert not outcome.is_answer


def test_the_turn_cap_stops_a_non_converging_agent():
    # A model that asks for a tool forever.
    script = [wants_tool("get_dependencies", {"service": "checkout-api"})] * 20
    outcome = run(script, bounds=Bounds(max_turns=3, max_cost_usd=99, max_seconds=99))
    assert outcome.status == "bounded"
    assert "turn" in outcome.reason.lower()
    assert outcome.turns <= 3
    assert not outcome.is_answer


def test_the_cost_ceiling_stops_an_expensive_agent():
    expensive = [wants_tool("get_dependencies", {"service": "checkout-api"},
                            in_tokens=900_000, out_tokens=50_000)] * 20
    outcome = run(expensive, bounds=Bounds(max_turns=99, max_cost_usd=1.00, max_seconds=99))
    assert outcome.status == "bounded"
    assert "cost" in outcome.reason.lower()


def test_cost_accumulates_across_turns():
    outcome = run([
        wants_tool("get_dependencies", {"service": "checkout-api"},
                   in_tokens=1_000_000, out_tokens=0),
        says("done", in_tokens=1_000_000, out_tokens=0),
    ])
    assert outcome.cost_usd > 3.0   # two calls, 1M input each, on sonnet
