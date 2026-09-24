"""TICKET 2 — the tool schemas the model reads, and the executor that runs them.

A tool description is documentation for a reader that consults it at call time
and cannot ask a follow-up question. Two tools with vague, overlapping
descriptions get confused, and the fix is a better description -- not a sterner
prompt.

Three tools, backed by `fixtures.py`:
    get_service_metrics(service, hours) -> latency and error-rate series
    get_recent_deploys(service)         -> deployments, most recent first
    get_dependencies(service)           -> what shares infrastructure with it
"""

from __future__ import annotations

# A list of tool definitions in the shape the Messages API expects:
#   {"name": ..., "description": ..., "input_schema": {...}}
#
# The schema is JSON Schema: {"type": "object", "properties": {...}, "required": [...]}
TOOLS: list[dict] = []   # TICKET 2: define the three tools


def run_tool(name: str, args: dict) -> str:
    """Execute one tool and return its result as a JSON string.

    The model reads this text, so it must be parseable and self-describing.
    An unknown tool name must return an error payload, never raise -- the loop
    has to keep going and tell the model what went wrong.
    """
    raise NotImplementedError("TICKET 2: see tests/test_tools.py")
