# Incident Triage Agent

An agent that investigates a production incident — gathering evidence with tools until it can name
a likely cause, and stopping before it can run up a bill.

**Built by the cohort, one piece per ticket.** Nobody builds it alone, and nobody waits on anybody:
every ticket is independent, and the scaffold that would block you is already done.

---

## Get set up

**Full instructions, all platforms: [SETUP.md](SETUP.md).** The short version:

```bash
git clone https://github.com/emergtechinc/incident-triage-agent.git
cd incident-triage-agent
python3 -m venv .venv && source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install pytest
python check_env.py
```

`check_env.py` verifies everything and tells you what to fix if not. Expect **41 failing tests** —
that is the starting line.

**No API key is needed — for any of it.** Every test drives a scripted fake client
(`src/triage/fake.py`), so the whole suite runs offline and CI costs nothing. That is not a
shortcut; it is how you test anything with a non-deterministic dependency.

## Before your first ticket

**[PRIMER.md](PRIMER.md)** — what a request and a response actually look like, and how to read a
failing test as your specification. Ten minutes, and it covers everything four of the seven tickets
need. The other three need nothing beyond ordinary Python.

## Take a ticket

Open [Issues](../../issues), find one nobody has taken, **assign it to yourself**.

```bash
git checkout -b ticket-3-bounds
# implement until your tests pass
pytest tests/test_bounds.py -v
git commit -am "bounds: the three limits"
git push -u origin ticket-3-bounds
gh pr create --fill          # or open it in the browser
```

Your pull request needs two things to merge:

- **CI green** — the tests decide correctness, not a person
- **one approving review** from someone who did not write it

## The rules

**Claim it, then work it.** An issue with no commits by the next session goes back in the pool. No
blame — it just means someone else can pick it up.

**Stuck for more than 30 minutes? Say so on the issue.** Describe what you tried. That is not
failure, it is how teams work, and someone will usually have hit the same wall.

**Review before you take a second ticket.** You do not open a second pull request until you have
reviewed someone else's. That is the point at which you see four other approaches to problems you
solved one way.

## What is already built

| File | |
|---|---|
| `src/triage/fake.py` | a scripted stand-in for the API client — this is why nothing needs a key |
| `src/triage/fixtures.py` | the incidents and the data the tools return |
| `tests/` | the full suite. It defines "done" for every ticket. |
| `.github/workflows/` | CI |

**Do not change those.** If a test seems wrong, say so on the issue — it might be. But make that
argument before changing it.

## What you are building

| Ticket | File | |
|---|---|---|
| 1 | `pricing.py` | price a call from reported token usage |
| 2 | `tools.py` | the schemas the model reads, and the executor |
| 3 | `bounds.py` | the three limits that stop a runaway loop |
| 4 | `results.py` | turning tool output into what the API expects back |
| 5 | `loop.py` | the `stop_reason` state machine |
| 6 | `cli.py` | wiring, and making a partial result visibly partial |

Each file's docstring explains what it is for and why it matters. Read it before you start — it is
shorter than the ticket.

## The thing this project is actually about

The fixture data is deliberately inconsistent: **the service reporting the problem has not deployed
in days, while something it depends on shipped 55 minutes ago.** No single tool call reaches that
conclusion. The agent has to gather evidence, notice the contradiction, and follow it.

That is why a loop exists at all — and why the interesting question is never *"does it work"* but
**"what stops it, and what does the worst case cost?"**
