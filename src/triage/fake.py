"""A stand-in for the Anthropic client that replays scripted responses.

**This file is part of the scaffold. You do not need to change it.**

Why it exists: an agent loop is a state machine driven by `stop_reason`, and you
cannot test a state machine against a live model -- the responses vary, the calls
cost money, and CI has no API key. So the tests drive the loop with a fake client
that returns exactly the sequence of responses a scenario needs.

This is not a testing trick. It is how you test any system with a non-deterministic
dependency: put a seam at the boundary and script the other side.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0


@dataclass
class TextBlock:
    text: str
    type: str = "text"


@dataclass
class ToolUseBlock:
    id: str
    name: str
    input: dict
    type: str = "tool_use"


@dataclass
class FakeResponse:
    """Shaped exactly like a real Messages API response, for the parts we read."""

    content: list
    stop_reason: str
    usage: Usage = field(default_factory=Usage)
    model: str = "fake-model"


@dataclass
class _Messages:
    parent: "FakeClient"

    def create(self, **kwargs):
        self.parent.calls.append(kwargs)
        if not self.parent.script:
            raise AssertionError(
                f"FakeClient ran out of scripted responses after "
                f"{len(self.parent.calls)} call(s). The loop called the API more "
                f"times than the scenario expected -- usually a missing stop condition."
            )
        return self.parent.script.pop(0)


class FakeClient:
    """Replays `script` in order. Records every request in `calls`."""

    def __init__(self, script: list[FakeResponse]):
        self.script = list(script)
        self.calls: list[dict] = []
        self.messages = _Messages(self)


# --- builders, so tests read as scenarios rather than as data structures ---

def says(text: str, *, in_tokens: int = 100, out_tokens: int = 50) -> FakeResponse:
    """A response that answers and finishes."""
    return FakeResponse([TextBlock(text)], "end_turn", Usage(in_tokens, out_tokens))


def wants_tool(name: str, args: dict, *, tool_id: str = "toolu_1",
               in_tokens: int = 100, out_tokens: int = 30) -> FakeResponse:
    """A response that requests one tool and waits."""
    return FakeResponse([ToolUseBlock(tool_id, name, args)], "tool_use",
                        Usage(in_tokens, out_tokens))


def wants_tools(*pairs, in_tokens: int = 100, out_tokens: int = 60) -> FakeResponse:
    """A response requesting SEVERAL tools in one turn -- parallel tool use."""
    blocks = [ToolUseBlock(f"toolu_{i}", name, args)
              for i, (name, args) in enumerate(pairs, start=1)]
    return FakeResponse(blocks, "tool_use", Usage(in_tokens, out_tokens))


def truncated(partial: str, *, in_tokens: int = 100, out_tokens: int = 4096) -> FakeResponse:
    """A response cut off mid-sentence because it hit max_tokens."""
    return FakeResponse([TextBlock(partial)], "max_tokens", Usage(in_tokens, out_tokens))


def refused(*, in_tokens: int = 100) -> FakeResponse:
    """A response the model declined to give."""
    return FakeResponse([], "refusal", Usage(in_tokens, 0))
