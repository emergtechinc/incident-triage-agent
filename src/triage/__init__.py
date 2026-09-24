"""A bounded agentic loop that triages production incidents.

Built by the cohort, one piece per ticket. Every module below is a ticket:

    pricing.py   price a call from reported token usage
    tools.py     the tool schemas the model reads, and the executor
    bounds.py    the three limits that stop a runaway loop
    results.py   turning tool output into what the API expects back
    loop.py      the stop_reason state machine
    cli.py       wiring it together

`fake.py` and `fixtures.py` are scaffold -- already working, do not change them.
"""
