"""TICKET 3 — the three limits that stop a runaway loop.

They catch three different failures:

    max_turns    a model that keeps calling tools without converging.
                 Protects the LOGIC.
    max_cost     a few enormous turns rather than many small ones.
                 Protects the INVOICE -- the one teams forget.
    max_seconds  a slow tool, a hung request, a retry storm.
                 Protects the USER, who is still waiting.

An iteration cap alone feels safe and is not: ten turns over a context that
grows every turn is still an unbounded bill.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Bounds:
    """The limits, and the check that enforces them."""

    max_turns: int = 8
    max_cost_usd: float = 0.50
    max_seconds: float = 90.0

    def exceeded(self, *, turns: int, cost_usd: float, elapsed_seconds: float) -> str | None:
        """Return a human-readable reason if any bound is exceeded, else None.

        Checked BEFORE spending, not after. Returning a reason rather than a
        boolean means the caller can report WHICH limit stopped it, which is the
        difference between a partial result and a mystery.
        """
        raise NotImplementedError("TICKET 3: see tests/test_bounds.py")
