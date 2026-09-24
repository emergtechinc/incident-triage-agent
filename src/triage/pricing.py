"""TICKET 1 — price a call from what the API reports it used.

Pure arithmetic. No network, no imports beyond the standard library.

Rates are dollars per million tokens, verified 2026-09-23. Model identifier
strings are complete as written -- appending a date suffix produces a model
that does not exist.
"""

from __future__ import annotations

RATES_TAKEN_ON = "2026-09-23"

RATES = {
    "claude-opus-5-5":  {"in": 4.00, "out": 20.00},
    "claude-opus-5":    {"in": 5.00, "out": 25.00},
    "claude-sonnet-5":  {"in": 2.00, "out": 10.00},
    "claude-haiku-4-5": {"in": 1.00, "out":  5.00},
}


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """Return the dollar cost of one call.

    Rates are per MILLION tokens, so both sides divide by 1_000_000.

    Raise KeyError with a helpful message for an unknown model -- a typo in a
    model id must not silently price as something else.
    """
    raise NotImplementedError("TICKET 1: see tests/test_pricing.py")


def cost_of_response(model: str, usage) -> float:
    """Price a response object directly.

    `usage` has `.input_tokens` and `.output_tokens`. Read them off the response
    rather than estimating -- the model decides how much output to generate, so
    the reported figure is the only honest one.
    """
    raise NotImplementedError("TICKET 1: see tests/test_pricing.py")
