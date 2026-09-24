"""Synthetic incidents and the data the tools return.

**Part of the scaffold. You do not need to change it.**

The data is deliberately *inconsistent*: the service reporting the problem has
not deployed in days, while something it depends on shipped 55 minutes ago. No
single tool call reaches that conclusion, which is what makes a loop necessary
rather than decorative.
"""

from __future__ import annotations

INCIDENTS = {
    "simple": (
        "[P4] Disk usage alert on build-agent-07: /var/log at 81% (threshold 80%). "
        "No build failures. Log rotation ran normally at 03:00."
    ),
    "moderate": (
        "[P2] Checkout API p99 latency 1.8s -> 6.4s over 40 minutes, error rate 0.3% -> 2.1%. "
        "DB connection pool at 94% of max. Two other services share that pool."
    ),
    "complex": (
        "[P1] Order totals wrong for a subset of EU customers since the 14th. "
        "Finance reports 0.4% of orders under-charged. Three changes landed that day. "
        "Staging does not reproduce it; staging uses a fixed FX rate."
    ),
}

METRICS = {
    "checkout-api": {
        "p99_ms": [(0, 1800), (-20, 4100), (-40, 6400), (-50, 1790)],
        "error_rate": [(0, 0.003), (-20, 0.019), (-50, 0.003)],
        "note": "degradation began ~45 minutes ago",
    },
    "payments-svc": {
        "p99_ms": [(0, 240), (-60, 245)],
        "error_rate": [(0, 0.001), (-60, 0.001)],
        "note": "healthy throughout",
    },
}

DEPLOYS = {
    "checkout-api": [{"version": "v9.2.0", "minutes_ago": 4320, "author": "team-checkout"}],
    "payments-svc": [{"version": "v4.12", "minutes_ago": 55, "author": "team-payments",
                      "summary": "connection pool sizing change"}],
}

DEPENDENCIES = {
    "checkout-api": ["payments-svc", "inventory-svc"],
    "payments-svc": ["postgres-primary"],
}

SYSTEM_PROMPT = (
    "You are a staff engineer triaging a production incident. "
    "Use the tools to gather evidence before concluding. "
    "State your hypothesis plainly, with the evidence that supports it."
)
