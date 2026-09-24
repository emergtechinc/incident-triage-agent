#!/usr/bin/env python3
"""Environment check — run this first, and whenever something looks wrong.

    python check_env.py

No API key, no network. Every failure prints what to do about it.

The check that earns its keep is "one site-packages tree". A virtual environment
makes exactly one promise -- that `pip` and `python` serve the same interpreter,
so a package you install is a package you can import. When that quietly stops
holding, the symptom is baffling: pip reports success, python says the module is
missing, and every "is my venv active?" check passes because it IS active.
"""

from __future__ import annotations

import glob
import os
import subprocess
import sys
from pathlib import Path

OK, WARN, BAD = "  ok  ", " warn ", " FAIL "
_failed = False


def report(status, label, detail="", fix=""):
    global _failed
    if status == BAD:
        _failed = True
    print(f"[{status}] {label}" + (f" — {detail}" if detail else ""))
    for line in (fix or "").strip().splitlines():
        print(f"         {line}")


def main() -> int:
    print("\n  Environment check\n")

    major, minor = sys.version_info[:2]
    if (major, minor) >= (3, 10):
        report(OK, "Python", f"{major}.{minor}")
    else:
        report(BAD, "Python", f"{major}.{minor} — need 3.10+",
               fix="macOS: /usr/bin/python3 is the system Python and is too old.\n"
                   "Install from python.org or Homebrew, then rebuild the venv.")

    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        report(OK, "Virtual environment", venv)
        if Path(sys.executable).is_relative_to(Path(venv)):
            report(OK, "Interpreter is inside it", sys.executable)
        else:
            report(BAD, "Interpreter is NOT inside the venv", sys.executable,
                   fix="Rebuild it — see the bottom of this output.")

        trees = sorted(glob.glob(os.path.join(venv, "lib", "python*", "site-packages")))
        if len(trees) <= 1:
            report(OK, "One site-packages tree")
        else:
            report(BAD, "Multiple site-packages trees",
                   ", ".join(Path(t).parent.name for t in trees),
                   fix="pip writes to one and python reads the other, so installs\n"
                       "appear to succeed and then vanish. Rebuild — reinstalling will not help.")
    else:
        report(WARN, "Virtual environment", "none active",
               fix="You are using your system Python. Not fatal, but activate the venv:\n"
                   "  macOS/Linux:  source .venv/bin/activate\n"
                   "  Windows:      .venv\\Scripts\\activate")

    try:
        import pytest
        report(OK, "pytest", pytest.__version__)
    except ImportError:
        report(BAD, "pytest", "not installed", fix="pip install pytest")

    if Path("src/triage/fake.py").exists():
        report(OK, "Repository layout", "running from the repo root")
    else:
        report(BAD, "Repository layout", "src/triage not found",
               fix="Run this from the repository root, not from a subfolder.")

    if not _failed:
        try:
            out = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q", "--no-header"],
                                 capture_output=True, text=True, timeout=120).stdout
            tail = [l for l in out.strip().splitlines() if "passed" in l or "failed" in l]
            report(OK, "Test suite runs", tail[-1] if tail else "ran")
            print("\n  Failures are expected — 41 of them. That is the starting line.")
        except Exception as exc:                               # noqa: BLE001
            report(WARN, "Test suite", f"could not run: {exc}")

    print()
    if _failed:
        print("  Rebuild the environment — from the REPO ROOT, with no venv active:\n")
        print("      deactivate                  # repeat until no (venv) prefix remains")
        print("      rm -rf .venv                # Windows: rmdir /s .venv")
        print("      python3 -m venv .venv       # name an explicit python3.10+ if yours is managed")
        print("      source .venv/bin/activate   # Windows: .venv\\Scripts\\activate")
        print("      pip install pytest")
        print("      python check_env.py\n")
        return 1

    print("  Ready. Pick a ticket: https://github.com/emergtechinc/incident-triage-agent/issues\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
