"""TICKET 7 — letting the agent decide it cannot answer yet.

The agent so far has one ending: gather evidence, then conclude. Real triage has
three, and the interesting two are the ones where it declines to conclude:

    answer        enough evidence, here is the hypothesis
    clarify       a question only a human can settle -- ask, do not guess
    escalate      beyond what this agent should decide alone -- hand it over

The mechanism is the same one you already have: **these are tools.** The model
chooses `request_clarification` or `escalate` the same way it chooses
`get_service_metrics`, and the loop reads that choice as a terminal state rather
than as more evidence-gathering.

That is the whole idea, and it is why it is worth building. An agent that cannot
say "I do not know, and here is what would tell me" will confidently guess
instead -- which is the expensive failure.
"""

from __future__ import annotations

# Two more tool definitions, in the same shape as TOOLS in tools.py.
#
#   request_clarification(question)     -- ask the human one specific question
#   escalate(reason, severity)          -- hand off; severity is low|medium|high|critical
#
# Their descriptions must make clear WHEN to reach for them, or the model will
# either never use them or use them instead of doing the work.
ROUTING_TOOLS: list[dict] = []   # TICKET 7


def disposition(tool_calls: list[str]) -> str:
    """Given the tool names called during a run, return the terminal disposition.

    Returns "escalate", "clarify", or "answer".

    Precedence matters and is not arbitrary: if the agent escalated at any point,
    that outranks a clarification request, which outranks an ordinary answer.
    An escalation that gets downgraded because a later turn asked a question is
    exactly the bug this ordering prevents.
    """
    raise NotImplementedError("TICKET 7: see tests/test_routing.py")


def handoff_note(disposition_value: str, detail: str) -> str:
    """One line a human reads first, when the agent did not answer.

    Must name the disposition and carry the detail. A handoff that does not say
    what it wants is a handoff nobody acts on.
    """
    raise NotImplementedError("TICKET 7: see tests/test_routing.py")
