# Setup — 10 minutes

**You do not need an Anthropic account or an API key for any of this project.** Every test runs
offline against a scripted stand-in for the API. Keys come later, for the live demos.

---

## 1. Python 3.10 or newer

Check what you have:

```bash
python3 --version        # macOS / Linux
python --version         # Windows
```

**3.10 or newer.** If it's older or the command isn't found:

| | |
|---|---|
| **macOS** | `brew install python@3.12` — or download from [python.org](https://www.python.org/downloads/). Note `/usr/bin/python3` is the system Python and is usually 3.9, too old. |
| **Windows** | [python.org](https://www.python.org/downloads/) — **tick "Add python.exe to PATH"** on the first screen. |
| **Linux** | `sudo apt install python3 python3-venv` (Debian/Ubuntu) |

## 2. Git

```bash
git --version
```

Missing? [git-scm.com/downloads](https://git-scm.com/downloads), or `brew install git`.

## 3. Get the code and build an environment

```bash
git clone https://github.com/emergtechinc/incident-triage-agent.git
cd incident-triage-agent
```

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

> If PowerShell blocks the activate script, run once:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Your prompt now starts with `(.venv)`. **That's how you know it worked.**

### Two rules that prevent the one painful failure

**Never create a venv while another one is active.** If your prompt already shows a `(something)`
prefix, run `deactivate` first.

**If your `python3` is managed by pyenv, asdf, conda or similar, name the interpreter explicitly:**

```bash
/opt/homebrew/bin/python3.12 -m venv .venv      # example — use a real path on your machine
```

Those tools resolve `python3` at the moment you call it, which can produce a venv where `pip` and
`python` serve *different* Python versions. Packages then install successfully and fail to import,
and nothing tells you why.

## 4. Check it

```bash
python check_env.py
```

Expected:

```
[  ok  ] Python — 3.12
[  ok  ] Virtual environment — .../incident-triage-agent/.venv
[  ok  ] Interpreter is inside it
[  ok  ] One site-packages tree
[  ok  ] pytest — 9.x
[  ok  ] Test suite runs — 41 failed, 2 passed
```

**41 failures is correct.** Nothing is implemented yet — that's the starting line, and your ticket is
to turn some of them green.

If anything says `FAIL`, it prints the fix. Run this first whenever something is strange; it's faster
than reading a stack trace.

## 5. Every new terminal

The venv is per-terminal. Each time you open a new one:

```bash
cd incident-triage-agent
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

Forgetting this causes most "it worked yesterday" reports.

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

## Then

Pick a ticket from [Issues](../../issues), assign it to yourself, and read
[README.md](README.md) for the branch-and-pull-request flow.

Stuck for more than 30 minutes? Say so on the issue, with what you tried. That's not failure —
it's how teams work.
