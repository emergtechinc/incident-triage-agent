# Doing your ticket in VS Code — step by step

Follow this once and the rest of the tickets are the same five minutes.

---

## 1. Get the code

Open a terminal (**Terminal → New Terminal**, or `` Ctrl+` ``) and pick a folder you use for projects:

```bash
cd ~/projects                 # or wherever you keep code; Windows: cd C:\Users\<you>\projects
git clone https://github.com/emergtechinc/incident-triage-agent.git
cd incident-triage-agent
code .                        # opens this folder in VS Code
```

If `code .` isn't found: **File → Open Folder** and pick `incident-triage-agent`.

## 2. Make the virtual environment

In VS Code's terminal, **from the project root**:

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install pytest
```

Your prompt now starts with `(.venv)`.

> **Two rules.** Never create a venv while another is active — run `deactivate` first if your prompt
> already shows a `(something)`. And if your `python3` is managed by pyenv/conda/asdf, name the
> interpreter explicitly: `/opt/homebrew/bin/python3.12 -m venv .venv`.

## 3. Point VS Code at that interpreter

**This is the step people skip, and then nothing works.** VS Code has its own idea of which Python
to use, separate from your terminal.

1. `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Windows/Linux)
2. Type **Python: Select Interpreter**
3. Choose the one that says **`.venv`** and points inside your project folder

Bottom-right of the window should now show something like `Python 3.12.x ('.venv')`.

## 4. Check everything works

```bash
python check_env.py
```

You want all `ok`, ending with `Test suite runs — 45 failed, 8 passed`.

**Those failures are correct.** Nothing is implemented yet. Your ticket is to turn some of them green.

If anything says `FAIL`, it prints the fix.

## 5. Make your branch

Name it after your ticket:

```bash
git checkout -b ticket-3-bounds        # use YOUR ticket number and name
git push -u origin ticket-3-bounds
```

Push it straight away, even empty. It makes your work visible on the board.

## 6. Read your tests before you write anything

Your ticket names a test file. **Open it first** — it's a more precise specification than the ticket.

```bash
pytest tests/test_bounds.py -v
```

Read a test name as a sentence. Read its assertion — that's the exact shape expected. Read the
comment above it — that's usually *why* the case matters.

## 7. Write the code

Open your module — e.g. `src/triage/bounds.py`. Its docstring explains what it's for.

Delete the `raise NotImplementedError(...)` line and write the implementation. **Delete it — don't
comment it out.**

Work **one test at a time**:

```bash
pytest tests/test_bounds.py::test_turn_cap_trips_and_names_itself -v
```

Then the whole file:

```bash
pytest tests/test_bounds.py -v
```

> VS Code's **Testing** panel (the flask icon in the left bar) gives you the same thing with a green
> tick per test, and lets you run one by clicking it. Use whichever you prefer.

## 8. Commit and push

Terminal:

```bash
git add src/triage/bounds.py
git commit -m "bounds: stop before spending, not after"
git push
```

Or VS Code's **Source Control** panel (the branch icon): type a message, **✓ Commit**, then
**Sync Changes**.

Write the message about *what changed and why* — `bounds: stop before spending, not after` beats
`updated bounds.py`.

## 9. Open the pull request

```bash
gh pr create --fill          # if you have the GitHub CLI
```

Otherwise open the repo in a browser — GitHub shows a **Compare & pull request** button after a push.

In the description: what you did, and anything you were unsure about. *"I wasn't sure whether X"* is
the most useful line in a pull request.

Add `Closes #3` so the issue closes when it merges.

## 10. Then two things happen

**CI runs your tests** automatically. Green tick or red cross on the PR.

**Someone reviews it.** One approval from a person who didn't write it, then it merges.

And you review someone else's before you take another ticket.

---

## If something breaks

| Symptom | Fix |
|---|---|
| `ModuleNotFoundError: triage` | You're not in the project root, or the venv isn't active. |
| `pytest: command not found` | `pip install pytest` with the venv active. |
| VS Code shows import errors, terminal is fine | Step 3 — select the `.venv` interpreter. |
| `(.venv)` gone from the prompt | New terminal. `source .venv/bin/activate` again. |
| Tests pass locally, CI fails | You didn't push, or you edited a test. Check what CI says. |

Stuck more than 30 minutes? **Comment on your issue** with what you tried. That's not failure —
it's how teams work, and someone has usually hit the same wall.
