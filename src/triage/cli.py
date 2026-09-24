"""TICKET 6 — wire it together and print something a human can read.

    python -m triage.cli --incident moderate
    python -m triage.cli --incident complex --max-turns 3

Without --live it runs against a scripted fake client and needs no API key, so
anyone can see the agent work before they have credentials.
"""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """--incident {simple,moderate,complex}, --max-turns, --max-cost, --live."""
    raise NotImplementedError("TICKET 6: see tests/test_cli.py")


def format_outcome(outcome) -> str:
    """Render an Outcome for a terminal.

    A bounded or truncated run must be VISIBLY not-an-answer. A partial result
    dressed up as a finished one is the failure this whole build exists to avoid.
    """
    raise NotImplementedError("TICKET 6: see tests/test_cli.py")


def main(argv: list[str] | None = None) -> int:
    raise NotImplementedError("TICKET 6: see tests/test_cli.py")


if __name__ == "__main__":
    raise SystemExit(main())
