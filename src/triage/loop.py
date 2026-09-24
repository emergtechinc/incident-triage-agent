"""TICKET 5 — the stop_reason state machine.

Perceive-reason-act is not something the model does. The model answers ONCE and
stops. Every arrow in that diagram is code you write, and this file is that code.

The transition is reported in one field:

    end_turn     finished. Return the answer.
    tool_use     wants a tool. Run it, append ALL results as ONE user message, loop.
    max_tokens   truncated MID-SENTENCE. NOT done, though it looks it.
    refusal      declined. Do not retry unchanged.

The mistake that ships is `while stop_reason == "tool_use"` -- it treats every
other value as success, so a truncated half-answer reaches the user with nothing
logged anywhere.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Outcome:
    """What the loop produced, and why it ended."""

    status: str                      # "completed" | "truncated" | "refused" | "bounded"
    answer: str = ""
    reason: str = ""                 # for "bounded", which limit tripped
    turns: int = 0
    cost_usd: float = 0.0
    tool_calls: list[str] = field(default_factory=list)

    @property
    def is_answer(self) -> bool:
        """Only a completed run carries an answer you may show a user."""
        raise NotImplementedError("TICKET 5: see tests/test_loop.py")


def run(client, *, model: str, system: str, incident: str, bounds, tools, max_tokens: int = 1500):
    """Run the agent until it finishes or a bound stops it. Return an Outcome.

    `client` is anything with `.messages.create(...)` -- the real SDK client, or
    the FakeClient in tests. That seam is why this is testable without an API key.

    Each pass:
      1. check the bounds BEFORE spending
      2. call the model
      3. append the assistant's blocks VERBATIM (tool_use blocks included --
         drop them and the conversation is incoherent)
      4. if stop_reason is not tool_use, finish with the matching status
      5. otherwise run every requested tool, append ALL results as ONE user
         message, and loop
    """
    raise NotImplementedError("TICKET 5: see tests/test_loop.py")
