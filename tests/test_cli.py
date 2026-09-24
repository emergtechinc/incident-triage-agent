"""TICKET 6 — the wiring, and making a partial result visibly partial."""

from triage import cli
from triage.loop import Outcome


def test_parser_accepts_the_documented_flags():
    p = cli.build_parser()
    args = p.parse_args(["--incident", "complex", "--max-turns", "3"])
    assert args.incident == "complex"
    assert args.max_turns == 3


def test_incident_defaults_to_something_runnable():
    args = cli.build_parser().parse_args([])
    assert args.incident in {"simple", "moderate", "complex"}


def test_a_completed_run_shows_the_answer():
    text = cli.format_outcome(
        Outcome(status="completed", answer="The dependency's pool change.",
                turns=3, cost_usd=0.0123)
    )
    assert "dependency" in text


def test_a_bounded_run_is_VISIBLY_not_an_answer():
    # A partial result dressed up as a finished one is the failure to avoid.
    text = cli.format_outcome(
        Outcome(status="bounded", reason="max_turns (3)", turns=3, cost_usd=0.05)
    ).lower()
    assert "max_turns" in text or "turn" in text
    assert any(w in text for w in ("stopped", "bounded", "incomplete", "partial", "not "))


def test_a_truncated_run_is_VISIBLY_not_an_answer():
    text = cli.format_outcome(
        Outcome(status="truncated", answer="The likely cause is", turns=1)
    ).lower()
    assert any(w in text for w in ("truncated", "cut off", "incomplete", "not "))


def test_the_run_always_reports_what_it_spent():
    text = cli.format_outcome(Outcome(status="completed", answer="x", turns=2, cost_usd=0.0456))
    assert "0.04" in text or "$" in text
