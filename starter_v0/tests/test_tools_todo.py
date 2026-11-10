"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_my_new_tool_happy_path() -> None:
    pytest.skip(TODO)


def test_my_new_tool_bad_input_from_model() -> None:
    pytest.skip(TODO)


def test_my_new_tool_failure_returns_error_dict() -> None:
    pytest.skip(TODO)


# ---------------- wiki (D - 2A202603724_NgoChiVinh) ----------------

WIKI_PAGES = {"batchcomplete": True, "query": {"pages": [
    # API returns pages in arbitrary order; "index" is the search rank.
    {"pageid": 2, "index": 2, "title": "Trí tuệ nhân tạo tạo sinh", "extract": "AI tạo sinh...",
     "fullurl": "https://vi.wikipedia.org/wiki/Tr%C3%AD_tu%E1%BB%87_nh%C3%A2n_t%E1%BA%A1o_t%E1%BA%A1o_sinh"},
    {"pageid": 1, "index": 1, "title": "Trí tuệ nhân tạo", "extract": "x" * 700,
     "fullurl": "https://vi.wikipedia.org/wiki/Tr%C3%AD_tu%E1%BB%87_nh%C3%A2n_t%E1%BA%A1o"},
]}}


def test_wiki_sends_search_request_and_maps_pages_by_rank(fake_http) -> None:
    calls = fake_http(FakeResponse(WIKI_PAGES))

    result = TOOL_FUNCTIONS["wiki"](query="Trí tuệ nhân tạo", lang="vi", limit=2)

    assert len(calls) == 1
    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == "https://vi.wikipedia.org/w/api.php"
    assert calls[0]["params"]["gsrsearch"] == "Trí tuệ nhân tạo"
    assert calls[0]["params"]["gsrlimit"] == 2
    assert calls[0]["headers"]["User-Agent"]
    assert [item["title"] for item in result["items"]] == ["Trí tuệ nhân tạo", "Trí tuệ nhân tạo tạo sinh"]
    first = result["items"][0]
    assert first["url"] == "https://vi.wikipedia.org/wiki/Tr%C3%AD_tu%E1%BB%87_nh%C3%A2n_t%E1%BA%A1o"
    assert first["source"] == "vi.wikipedia.org"
    assert first["summary"] == "x" * 600 + "..."


def test_wiki_empty_query_or_bad_lang_returns_error_without_request(fake_http) -> None:
    calls = fake_http(FakeResponse(WIKI_PAGES))

    for bad_args in ({"query": ""}, {"query": "   "}, {"query": None}, {"query": "AI", "lang": "fr"}):
        result = TOOL_FUNCTIONS["wiki"](**bad_args)
        assert result["tool"] == "wiki"
        assert result["error"] == "ValueError"

    assert calls == []


def test_wiki_coerces_string_and_out_of_range_limit(fake_http) -> None:
    calls = fake_http(FakeResponse(WIKI_PAGES))

    for sent, expected in (("3", 3), (0, 1), (-5, 1), (99, 10), ("abc", 3)):
        assert TOOL_FUNCTIONS["wiki"](query="AI", limit=sent)["limit"] == expected

    assert [call["params"]["gsrlimit"] for call in calls] == [3, 1, 1, 10, 3]


def test_wiki_http_error_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(status_code=429))

    result = TOOL_FUNCTIONS["wiki"](query="AI")

    assert result == {"tool": "wiki", "error": "HTTPError", "message": "HTTP 429"}


def test_wiki_api_error_payload_and_no_match_are_handled(fake_http) -> None:
    fake_http(FakeResponse({"error": {"code": "badvalue", "info": "Unrecognized value"}}))
    assert TOOL_FUNCTIONS["wiki"](query="AI")["error"] == "RuntimeError"

    fake_http(FakeResponse({"batchcomplete": True}))  # what Wikipedia returns when nothing matches
    result = TOOL_FUNCTIONS["wiki"](query="asdkjqwlekjzzz", lang="en")
    assert result["items"] == []
    assert "error" not in result
