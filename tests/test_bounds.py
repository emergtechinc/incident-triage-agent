"""TICKET 3 — three limits, three different failures."""

from triage.bounds import Bounds


def test_within_all_limits_returns_none():
    b = Bounds(max_turns=8, max_cost_usd=0.50, max_seconds=90)
    assert b.exceeded(turns=3, cost_usd=0.10, elapsed_seconds=10) is None


def test_turn_cap_trips_and_names_itself():
    b = Bounds(max_turns=2, max_cost_usd=10.0, max_seconds=900)
    reason = b.exceeded(turns=2, cost_usd=0.01, elapsed_seconds=1)
    assert reason and "turn" in reason.lower()


def test_cost_ceiling_trips_and_names_itself():
    b = Bounds(max_turns=100, max_cost_usd=0.25, max_seconds=900)
    reason = b.exceeded(turns=1, cost_usd=0.25, elapsed_seconds=1)
    assert reason and "cost" in reason.lower()


def test_wall_clock_trips_and_names_itself():
    b = Bounds(max_turns=100, max_cost_usd=10.0, max_seconds=30)
    reason = b.exceeded(turns=1, cost_usd=0.01, elapsed_seconds=30)
    assert reason and ("second" in reason.lower() or "time" in reason.lower())


def test_cost_can_trip_on_the_very_first_turn():
    # Iterations protect the logic; only cost protects the invoice. One enormous
    # turn must be stoppable without waiting for a turn count to climb.
    b = Bounds(max_turns=100, max_cost_usd=0.10, max_seconds=900)
    assert b.exceeded(turns=1, cost_usd=5.00, elapsed_seconds=1) is not None


def test_defaults_are_bounded_not_infinite():
    b = Bounds()
    assert b.max_turns < 1000 and b.max_cost_usd < 100 and b.max_seconds < 3600
