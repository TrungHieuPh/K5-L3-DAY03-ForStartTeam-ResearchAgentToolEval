---
name: wiki
track: core
kind: live_api
provider: Wikipedia (MediaWiki Action API)
requires_env: []
inputs: [query, lang, limit]
outputs: [items]
side_effect: false
---
# wiki

Searches Wikipedia (Vietnamese or English) and returns the intro summary of the
best-matching articles. No API key needed; an optional `WIKI_USER_AGENT` env var
overrides the default User-Agent header that Wikipedia asks clients to send.

- `query`: concept or article name. Vietnamese queries need full diacritics
  ("Trí tuệ nhân tạo", not "tri tue nhan tao").
- `lang`: `vi` (default) or `en`. Anything else returns an error dict.
- `limit`: 1–10 articles (default 3). Strings like `"3"` are coerced; out-of-range values are clamped.

Use it for background knowledge: definitions, concepts, history, people, organizations.
Do not use it for recent news or live events (use `lookup`), or to read a specific URL (use `fetch`).

Output: `items[]` with `title`, `url`, `source` (`vi.wikipedia.org` / `en.wikipedia.org`)
and `summary` (intro text, truncated to 600 chars). No match → `items: []`.
Errors (empty query, bad `lang`, HTTP error) return `{"tool": "wiki", "error", "message"}` instead of raising.
