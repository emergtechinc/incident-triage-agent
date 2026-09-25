# Setup and workflow

Everything from a fresh machine to your first merged pull request. **10 minutes to set up**, then
the ticket loop at the end is the same five minutes every time.

**You do not need an API key for any ticket.** Every test runs offline. Keys are for the live demos
in the curriculum repo — see [Your Anthropic API key](#your-anthropic-api-key) when you get one.

---

## 1. Python 3.10 or newer

```bash
python3 --version        # macOS / Linux
python --version         # Windows
```

| | |
|---|---|
| **macOS** | `brew install python@3.12`, or [python.org](https://www.python.org/downloads/). Note `/usr/bin/python3` is the system Python and is usually 3.9 — too old. |
| **Windows** | [python.org](https://www.python.org/downloads/) — **tick "Add python.exe to PATH"** on the first screen. |
| **Linux** | `sudo apt install python3 python3-venv` |

## 2. Git

```bash
git --version
```

Missing? [git-scm.com/downloads](https://git-scm.com/downloads), or `brew install git`.

## 3. Get the code and open it

```bash
mkdir -p ~/Documents/workspace/tvi && cd ~/Documents/workspace/tvi
git clone https://github.com/emergtechinc/incident-triage-agent.git
cd incident-triage-agent
code .                        # opens the folder in VS Code
```

Any folder works — use your own if you already keep projects elsewhere. If `code .` isn't found:
**File → Open Folder**.

## 4. Build the virtual environment

In VS Code's terminal (**Terminal → New Terminal**, or `` Ctrl+` ``), **from the project root**:

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

Your prompt now starts with `(.venv)`. **That's how you know it worked.**

> If PowerShell blocks the activate script, run once:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Two rules that prevent the one painful failure

**Never create a venv while another is active.** If your prompt already shows a `(something)`
prefix, run `deactivate` first.

**If your `python3` is managed by pyenv, conda or asdf, name the interpreter explicitly:**

```bash
/opt/homebrew/bin/python3.12 -m venv .venv      # example — a real path on your machine
```

Those tools resolve `python3` at the moment you call it, which can produce a venv where `pip` and
`python` serve *different* Python versions. Packages then install successfully and fail to import,
and nothing tells you why.

## 5. Point VS Code at that interpreter

**The step people skip, and then nothing works.** VS Code keeps its own interpreter setting,
separate from your terminal.

1. `Cmd+Shift+P` (macOS) / `Ctrl+Shift+P` (Windows, Linux)
2. Type **Python: Select Interpreter**
3. Choose the one showing **`.venv`**, inside your project folder

Bottom-right of the window should now read something like `Python 3.12.x ('.venv')`.

Skip this and the editor shows import errors on code that runs perfectly in the terminal.

## 6. Check it

```bash
python check_env.py
```

All `ok`, ending with `Test suite runs — 45 failed, 8 passed`.

**Those failures are correct.** Nothing is implemented yet — that's the starting line, and your
ticket is to turn some of them green. Anything marked `FAIL` prints its own fix.

## 7. Every new terminal

The venv is per-terminal:

```bash
cd ~/Documents/workspace/tvi/incident-triage-agent
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

Forgetting this causes most "it worked yesterday" reports.

---

# Doing a ticket

Claim one on [Issues](../../issues) — assign it to yourself. Then:

## 1. Branch, and push it straight away

```bash
git checkout -b ticket-3-bounds        # your ticket number and name
git push -u origin ticket-3-bounds
```

Push it even empty. It puts your work on the board, and a branch that exists is much easier to
continue than one you still have to start.

## 2. Read your tests before you write anything

Your ticket names a test file. **Open it first — it is a more precise specification than the ticket.**

```bash
pytest tests/test_bounds.py -v
```

Read a test name as a sentence. Read its assertion — that's the exact shape expected. Read the
comment above it — that's usually *why* the case matters.

## 3. Write the code, one test at a time

Open your module, e.g. `src/triage/bounds.py`. Its docstring says what it's for.

**Delete** the `raise NotImplementedError(...)` line — don't comment it out.

```bash
pytest tests/test_bounds.py::test_turn_cap_trips_and_names_itself -v   # one test
pytest tests/test_bounds.py -v                                          # the file
```

> VS Code's **Testing** panel (flask icon, left bar) shows the same thing with a tick per test and
> lets you run one by clicking it. Use whichever you prefer.

**Using AI to write it is expected** — but use your own, not the cohort key (see the key section
below for why), and be ready to explain your code in review. "The AI wrote it" isn't an answer.

## 4. Commit and push

```bash
git add src/triage/bounds.py
git commit -m "bounds: stop before spending, not after"
git push
```

Or VS Code's **Source Control** panel: type a message, **✓ Commit**, **Sync Changes**.

Say *what changed and why*. `bounds: stop before spending, not after` beats `updated bounds.py`.

## 5. Open the pull request

```bash
gh pr create --fill
```

Or use the **Compare & pull request** button GitHub shows after a push.

Add `Closes #3` so the issue closes on merge. In the description say what you did and anything you
were unsure about — *"I wasn't sure whether X"* is the most useful line in a pull request.

## 6. Then two things happen

**CI runs your tests** — green tick or red cross on the PR.
**Someone reviews it** — one approval from a person who didn't write it, then it merges.

And you review someone else's before you take another ticket.

---

## Your Anthropic API key

**Not needed for any ticket in this project.** Every test here runs offline. This section is for the
demos in the curriculum repo, where you call the real API.

You will be given a key. It looks like `sk-ant-...` and it is a password — treat it like one.

### Set it for your current terminal

**macOS / Linux**

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

**Windows (PowerShell)**

```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

Check it took, without printing it:

```bash
echo "key set: ${ANTHROPIC_API_KEY:+yes}"        # macOS / Linux
```
```powershell
if ($env:ANTHROPIC_API_KEY) { "key set: yes" }   # Windows
```

### Make it permanent

That export lasts for one terminal window. To set it once and forget it:

**macOS / Linux** — add the `export` line to `~/.zshrc` (or `~/.bashrc`), then `source ~/.zshrc`.

**Windows** — `setx ANTHROPIC_API_KEY "sk-ant-..."` in PowerShell, then **open a new terminal**
(`setx` does not affect the window you run it in).

### In a Colab notebook

Click the 🔑 in the left sidebar → **Add new secret** → name it exactly `ANTHROPIC_API_KEY` → paste
the value → switch on **Notebook access**. Done once, every notebook picks it up, and the key never
becomes part of the saved notebook.

### What you do NOT need

- **No `ANTHROPIC_BASE_URL`.** That is only for a proxy. With your own key the SDK talks to Anthropic
  directly.
- **No key in your code.** `anthropic.Anthropic()` reads the environment by itself.

### Using the key with Claude Code (in VS Code or the terminal)

**It works** — if `ANTHROPIC_API_KEY` is set, Claude Code prompts you once to approve that key
instead of opening a browser sign-in. The VS Code extension behaves the same way.

> **Do not use your cohort key for this.**
>
> The cohort spend cap is sized for the lesson steps — a handful of API calls each, cents per person.
> Claude Code is a different order of magnitude: it reads your files, loops over tool calls, and
> spends on every turn of every session. A few people using it for an afternoon can drain the shared
> pool, and then nobody can run a demo.
>
> **Your cohort key is for the lesson steps and the notebook. That is all.**

If you want Claude Code for your own work, use one of:

- **A Claude Pro or Max subscription** — flat monthly, no per-token billing. Sign in through the
  browser and leave `ANTHROPIC_API_KEY` unset.
- **Your own Console account and your own key**, with your own spend limit. Separate from the cohort
  pool entirely.

If you already have `ANTHROPIC_API_KEY` exported and want Claude Code to use your *subscription*
instead, unset it first — otherwise Claude Code offers the key and bills per token:

```bash
unset ANTHROPIC_API_KEY          # macOS / Linux
```
```powershell
Remove-Item Env:ANTHROPIC_API_KEY    # Windows PowerShell
```

### Four rules



1. **Never commit it.** `.env` is gitignored. If one ever lands in a commit, say so immediately —
   revoking takes thirty seconds and there is no version of this where hiding it is better.
2. **Never paste it in chat**, including the group.
3. **Never type it while screen sharing.**
4. **Your key has a spend cap and it is shared with everyone else on the cohort.** A runaway loop
   burns the pool, not just your share. That is not a warning — it is the reason the project you are
   building has a cost ceiling in it.

---

## Node — optional, and not needed for this project

Every ticket here is Python. Node is only for the TypeScript twin of one example in the curriculum
repo, which exists to show that the harness pattern is not the syntax.

Install it **per-user with nvm**, never system-wide — no `sudo`, and a `.nvmrc` pins the version per
project.

**macOS / Linux**

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
# reopen the terminal, then:
nvm install --lts
nvm alias default 'lts/*'
node --version
```

If `nvm` isn't found after reopening, add to `~/.zshrc` (or `~/.bashrc`):

```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

> `nvm` is a **shell function, not a program.** `which nvm` fails even when it's working —
> use `command -v nvm`.

**Windows** — use [nvm-windows](https://github.com/coreybutler/nvm-windows/releases), then
`nvm install lts` and `nvm use lts`.

---

---

## If something breaks

| Symptom | Cause |
|---|---|
| `ModuleNotFoundError: triage` | Not in the project root, or the venv isn't active. |
| `pytest: command not found` | `pip install pytest` with the venv active. |
| VS Code shows import errors, terminal is fine | Step 5 — select the `.venv` interpreter. |
| `(.venv)` gone from the prompt | New terminal. Activate again. |
| Multiple site-packages / installs "vanish" | The venv is broken. `check_env.py` names it; rebuild per its instructions. |
| Tests pass locally, CI fails | You didn't push, or you edited a test. Read what CI says. |
| `command not found: nvm` | It's a shell function, not a program. `command -v nvm`, and reopen the terminal. |

Stuck more than 30 minutes? **Comment on your issue** with what you tried. That's not failure —
it's how teams work, and someone has usually hit the same wall.

## Then

Pick a ticket from [Issues](../../issues) and read [README.md](README.md) for how we work.
