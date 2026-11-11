from __future__ import annotations

import os
from typing import Any

import requests

from tools._shared import TIMEOUT, err

SUPPORTED_LANGS = {"vi", "en"}
MAX_LIMIT = 10
SUMMARY_MAX_CHARS = 600
DEFAULT_USER_AGENT = "AI20k-Day03-Research-Agent/1.0 (educational lab)"


def _clamp_limit(limit: Any) -> int:
    """Model may send "3", 0, -1 or 99: coerce to int and keep it in 1..MAX_LIMIT."""
    try:
        value = int(limit)
    except (TypeError, ValueError):
        value = 3
    return max(1, min(value, MAX_LIMIT))


def _truncate(text: str, max_chars: int = SUMMARY_MAX_CHARS) -> str:
    text = (text or "").strip()
    return text if len(text) <= max_chars else text[:max_chars].rstrip() + "..."


def wiki_search(query: str = "", lang: str = "vi", limit: int = 3) -> dict[str, Any]:
    try:
        query = (query or "").strip() if isinstance(query, str) else ""
        if not query:
            raise ValueError("query must be a non-empty string")
        lang = (lang or "vi").strip().lower() if isinstance(lang, str) else ""
        if lang not in SUPPORTED_LANGS:
            raise ValueError(f"lang must be one of {sorted(SUPPORTED_LANGS)}, got {lang!r}")
        limit = _clamp_limit(limit)

        response = requests.get(
            f"https://{lang}.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "generator": "search",
                "gsrsearch": query,
                "gsrlimit": limit,
                "prop": "extracts|info",
                "exintro": 1,
                "explaintext": 1,
                "inprop": "url",
                "redirects": 1,
                "format": "json",
                "formatversion": 2,
            },
            headers={"User-Agent": os.getenv("WIKI_USER_AGENT", DEFAULT_USER_AGENT)},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            raise RuntimeError(data["error"].get("info", "Wikipedia API error"))

        pages = sorted(data.get("query", {}).get("pages", []), key=lambda page: page.get("index", 0))
        items = [{
            "title": page.get("title"),
            "url": page.get("fullurl") or f"https://{lang}.wikipedia.org/?curid={page.get('pageid')}",
            "source": f"{lang}.wikipedia.org",
            "summary": _truncate(page.get("extract", "")),
        } for page in pages]
        return {"tool": "wiki", "query": query, "lang": lang, "limit": limit, "items": items}
    except Exception as exc:
        return err("wiki", exc)
