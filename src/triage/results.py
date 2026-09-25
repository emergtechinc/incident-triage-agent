"""TICKET 4 — turning tool output into what the API expects back.

Three things go wrong here, and two of them produce no error at all, which is
what makes them expensive:

  1. A failed tool result gets DROPPED. That leaves a tool_use block with no
     matching result, which is an invalid conversation.
  2. Parallel results get SPLIT across messages. One assistant turn may request
     several tools; all results belong in ONE user message. Split them and the
     model quietly stops making parallel calls -- no error, just slower agents.
  3. A retried turn re-runs a tool. If it books, charges, sends or deletes, that
     is a real second side effect.
"""

from __future__ import annotations


def tool_result(tool_use_id: str, content: str, *, is_error: bool = False) -> dict:
    """Build one tool_result block.

    Shape: {"type": "tool_result", "tool_use_id": ..., "content": ...}
    plus "is_error": True when the tool failed. Report failures honestly --
    told the truth, the model will usually work around it.
    """
    block = {"type": "tool_result", "tool_use_id": tool_use_id, "content": content,  "is_error": is_error,}
    if is_error:
        block[is_error] = True 
    return block

   
    


def results_message(results: list[dict]) -> dict:
    """Wrap ALL tool results into a SINGLE user message."""
    return {
        "role": "user",
        "content": results,
    }
