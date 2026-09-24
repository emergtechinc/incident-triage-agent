# Primer — what you need to know to do a ticket

Short on purpose. Three of the seven tickets need nothing beyond ordinary Python. The other four all
need the same one thing: **what a request and a response actually look like.** That is most of what
is below.

---

## 1. The whole API surface is one function

```python
client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1500,
    system="You are a staff engineer triaging an incident.",
    messages=[{"role": "user", "content": "Checkout latency spiked."}],
    tools=[...],
)
```

| Argument | |
|---|---|
| `model` | which model, as a string |
| `max_tokens` | a hard ceiling on **output**. Not a target — the model stops when it is done. |
| `system` | standing instructions: *how to behave* |
| `messages` | the conversation: *what you are asking* |
| `tools` | what it is allowed to reach for |

## 2. The response is a **list of typed blocks**, not a string

This surprises everyone.

```python
response.content   # [TextBlock(...), ToolUseBlock(...)]
```

Each block has a `.type`:

| `.type` | holds | has `.text`? |
|---|---|---|
| `text` | the words of the answer | **yes** |
| `tool_use` | a request to run a tool: `.id`, `.name`, `.input` | no |

So you never write `response.content[0].text`. You filter:

```python
answer = "".join(b.text for b in response.content if b.type == "text")
```

## 3. `stop_reason` says why it stopped — and it is the whole loop

```python
response.stop_reason
```

| value | meaning |
|---|---|
| `end_turn` | finished. This is an answer. |
| `tool_use` | it wants a tool. Run it, hand back the result, call again. |
| `max_tokens` | **cut off mid-sentence.** Not finished, though it reads like it. |
| `refusal` | declined. Do not retry unchanged. |

**The mistake that ships** is `while stop_reason == "tool_use"` — it treats every other value as
success, so a truncated half-answer reaches a user with nothing logged anywhere.

## 4. The API remembers nothing

Every call is independent. There is no session. You hold the conversation and **resend all of it,
every time**.

That single fact is why the loop exists, and why a long conversation gets more expensive each turn —
turn 10 pays for turns 1 through 9 again.

The cycle:

```
call the model
  ├─ stop_reason != "tool_use"  → done, handle the outcome
  └─ stop_reason == "tool_use"  → run the tools
                                  append the assistant's blocks VERBATIM
                                  append ALL results as ONE user message
                                  call again
```

Two details that are not style preferences:

**Append the assistant's blocks unchanged.** Not the text — the blocks. Drop the `tool_use` block
and the conversation is incoherent: a result arrives referring to a request that is no longer there.

**All tool results go in ONE user message.** One turn may request several tools. Splitting the
results across messages trains the model, over the conversation, to stop making parallel calls.
Nothing errors; your agent just gets slower.

## 5. A tool is a function you describe well enough to be chosen correctly

```python
{
    "name": "get_service_metrics",
    "description": "Latency and error-rate series for one service. "
                   "Use this to establish WHEN a problem started.",
    "input_schema": {
        "type": "object",
        "properties": {"service": {"type": "string"}},
        "required": ["service"],
    },
}
```

The description is documentation for a reader who consults it **at call time and cannot ask a
follow-up question.** Two tools whose descriptions could be swapped will get confused, and the fix is
a better description — never a sterner prompt.

Results go back like this:

```python
{"type": "tool_result", "tool_use_id": block.id, "content": "...", "is_error": False}
```

**`is_error=True` when the tool failed — and never drop a failed result.** A `tool_use` with no
matching result is an invalid conversation. Told the truth, the model usually works around it.

## 6. A tool can be a *decision*, not an action

This is the idea behind ticket 7, and it is the one worth sitting with.

`request_clarification(question)` and `escalate(reason, severity)` are tools like any other. The model
picks them the same way it picks anything else. But your loop reads that choice as **the end of the
run** rather than as more evidence-gathering.

That is how an agent gets the ability to say *"I don't know, and here is what would tell me"* — and
an agent that cannot say that will confidently guess instead.

---

## Reading a failing test as your specification

This is the actual skill for this project, and it is worth thirty seconds of deliberate practice.

Your ticket names a test file. **Read it first, before the module.** It is more precise than any
description, including the ticket's own.

```bash
pytest tests/test_bounds.py -v          # what am I being asked for?
pytest tests/test_bounds.py::test_cost_ceiling_trips_and_names_itself -v   # one at a time
```

Read the test name as a sentence — they are written to be read that way. Then read the assertion,
which tells you the exact shape expected. Then read the comment above it, which usually says *why*
the case matters.

Work **one test at a time**. Make it pass. Run the file. Move to the next.

And if a test looks wrong — say so on the issue before you change it. Sometimes it will be. But make
the argument first; a test you quietly edited is a specification nobody agreed to.
