"""TICKET 4 — the three tool-result mistakes that produce no error."""

from triage import results


def test_tool_result_has_the_shape_the_api_expects():
    r = results.tool_result("toolu_1", '{"ok": true}')
    assert r["type"] == "tool_result"
    assert r["tool_use_id"] == "toolu_1"
    assert r["content"] == '{"ok": true}'


def test_a_success_is_not_flagged_as_an_error():
    r = results.tool_result("toolu_1", "fine")
    assert not r.get("is_error", False)


def test_a_failure_is_reported_honestly():
    # Told the truth, the model usually works around it. Hidden, it cannot.
    r = results.tool_result("toolu_1", "ServiceUnavailable: 503", is_error=True)
    assert r["is_error"] is True
    assert "503" in r["content"]


def test_results_go_back_as_a_single_user_message():
    # Splitting parallel results across messages trains the model out of making
    # parallel calls. No error is raised -- the agents just get slower.
    rs = [results.tool_result(f"toolu_{i}", "x") for i in (1, 2, 3)]
    message = results.results_message(rs)
    assert message["role"] == "user"
    assert isinstance(message["content"], list)
    assert len(message["content"]) == 3


def test_a_failed_result_is_never_dropped():
    # A tool_use block with no matching result is an invalid conversation.
    rs = [
        results.tool_result("toolu_1", "ok"),
        results.tool_result("toolu_2", "boom", is_error=True),
    ]
    message = results.results_message(rs)
    ids = {block["tool_use_id"] for block in message["content"]}
    assert ids == {"toolu_1", "toolu_2"}
