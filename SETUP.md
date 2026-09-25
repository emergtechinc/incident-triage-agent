# Setup — 10 minutes

**You do not need an API key for any ticket in this project.** Every test runs offline against a
scripted stand-in for the API. You will be given a key for the live demos in the curriculum repo —
see [Your Anthropic API key](#your-anthropic-api-key) below when you get it.

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

## Then

Pick a ticket from [Issues](../../issues), assign it to yourself, and read
[README.md](README.md) for the branch-and-pull-request flow.

Stuck for more than 30 minutes? Say so on the issue, with what you tried. That's not failure —
it's how teams work.
