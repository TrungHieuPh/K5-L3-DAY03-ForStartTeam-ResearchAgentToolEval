"""Streamlit UI for the Day03 Research Agent.

Run from starter_v0/:
    streamlit run app.py

Public demo (Cloudflare Tunnel): lock the sidebar so visitors cannot switch to a costly
model or relabel the transcript version:
    $env:UI_LOCK="1"; $env:UI_VERSION="v3"; streamlit run app.py

The UI reuses the exact same agent loop as chat.py (run_model_tool_loop), so a turn
here behaves like a turn in the CLI. Every session is saved as a transcript JSON in
transcripts/ with the same schema as chat.py (plus "interface": "streamlit").
"""
from __future__ import annotations

import html
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

from chat import (
    ARTIFACTS_DIR,
    ROOT,
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

PROVIDERS = ["openrouter", "openai", "anthropic", "gemini", "ollama"]
DEFAULT_PROVIDER = os.getenv("UI_PROVIDER", "openrouter")
# Label written into transcripts. Set it to the real artifact version (v1/v2/v3) before
# collecting evidence; "dev" makes accidental test sessions easy to spot and ignore.
DEFAULT_VERSION = os.getenv("UI_VERSION", "dev")
DEFAULT_MODEL = os.getenv("UI_MODEL", "")
LOCKED = os.getenv("UI_LOCK", "") == "1"
# The public tunnel link spends the host's API credit: cap turns per browser session.
MAX_TURNS_PER_SESSION = int(os.getenv("UI_MAX_TURNS", "20"))
HISTORY_WINDOW = 5
MAX_TOOL_ROUNDS = 4
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
TRANSCRIPTS_DIR = Path(os.getenv("UI_TRANSCRIPTS_DIR", ROOT / "transcripts"))

SAMPLE_QUESTIONS = [
    "Tin tức AI hôm nay có gì nổi bật?",
    "Theo Wikipedia, trí tuệ nhân tạo là gì?",
    "Tóm tắt 5 tweet mới nhất giúp mình",
    "Đăng bản tin này lên Telegram giúp mình",
]

# Each tool family is a "line" on the route map. Tools not listed here (teammates' new
# tools) fall back to OTHER_LINE, so the UI never needs editing when a tool is added.
LINES: dict[str, tuple[str, str]] = {
    "lookup": ("Tìm web", "#2563C9"),
    "timeline": ("Mạng xã hội", "#0F8F7E"),
    "social_search": ("Mạng xã hội", "#0F8F7E"),
    "fetch": ("Đọc tài liệu", "#7A4FD6"),
    "paper_text": ("Đọc tài liệu", "#7A4FD6"),
    "wiki": ("Tra cứu kiến thức", "#C27A12"),
    "papers": ("Tra cứu kiến thức", "#C27A12"),
    "policy": ("Tra cứu kiến thức", "#C27A12"),
    "clarify": ("Hỏi lại người dùng", "#D33F5B"),
    "format": ("Trình bày và gửi", "#44505C"),
    "send": ("Trình bày và gửi", "#44505C"),
}
OTHER_LINE = ("Tool khác", "#5E6B78")
ERROR_COLOR = "#D33F5B"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap');

:root {
  --paper: #F3F6F8; --ink: #17212B; --muted: #5E6B78; --rule: #D3DAE1;
  --rail: #C3CDD6; --ask: #D33F5B; --surface: #FFFFFF;
}
.stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea,
.stApp button, .stApp h1, .stApp h2, .stApp h3, .stApp summary {
  font-family: 'Be Vietnam Pro', system-ui, sans-serif;
}
.stApp p, .stApp li { line-height: 1.6; }

.ra-title { font-size: 2.4rem; font-weight: 700; letter-spacing: -0.025em; line-height: 1.1;
  margin: 0 0 .5rem; color: var(--ink); }
.ra-lede { font-size: 1.05rem; color: var(--muted); max-width: 58ch; margin: 0 0 1.75rem; }
.ra-try { font-weight: 600; color: var(--ink); margin: .25rem 0 .5rem; }

/* Route strip: a vertical line; each stop is one tool call, in the order the agent made them. */
.route { margin: .9rem 0 .5rem; padding: 1rem 1.1rem .4rem; background: var(--surface);
  border: 1px solid var(--rule); border-radius: 10px; }
.stop { position: relative; display: flex; gap: .7rem; align-items: flex-start; padding-bottom: .85rem; }
.stop:not(:last-child)::after { content: ""; position: absolute; left: 8px; top: 19px; bottom: 0;
  width: 3px; background: var(--rail); }
.stop-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: .1rem .5rem; }
.dot { position: relative; z-index: 1; flex: none; width: 19px; height: 19px; border-radius: 50%;
  background: var(--line); box-shadow: 0 0 0 3px var(--surface); }
.stop.error .dot { background: var(--surface); border: 4px solid var(--ask); width: 19px; height: 19px;
  box-sizing: border-box; }
.stop.end .dot { background: var(--ink); }
.stop-name { font-weight: 600; color: var(--line); line-height: 1.2; }
.stop.end .stop-name { color: var(--ink); }
.stop-line { font-size: .78rem; color: var(--muted); line-height: 1.3; }
.stop-args { font-size: .82rem; color: var(--ink); line-height: 1.35; margin-top: .15rem; word-break: break-word; }
.stop-result { font-size: .82rem; color: var(--muted); margin-top: .1rem; }
.stop.error .stop-result, .stop.ask .stop-result { color: var(--ask); font-weight: 500; }

.ask-box { border-left: 4px solid var(--ask); background: #FCEFF2; border-radius: 0 10px 10px 0;
  padding: .8rem 1rem; margin: .2rem 0 .6rem; }
.ask-box .ask-title { font-weight: 600; color: var(--ask); margin-bottom: .2rem; }
.ask-box p { margin: 0; color: var(--ink); }

.legend { display: flex; gap: .65rem; margin: 0 0 .9rem; }
.legend .bar { flex: none; width: 5px; border-radius: 3px; background: var(--line); }
.legend .legend-name { font-weight: 600; color: var(--ink); font-size: .92rem; }
.legend .legend-tool { font-size: .82rem; color: var(--muted); line-height: 1.4; margin-top: .15rem; }
.legend code { font-size: .78rem; }

</style>
"""


# ---------------------------------------------------------------- state

def new_transcript(provider_name: str, model: str | None, version: str) -> dict[str, Any]:
    artifact = build_artifact_version(version, SYSTEM_PROMPT_PATH, TOOLS_PATH)
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([safe_slug(version), safe_slug(provider_name), "ui", timestamp])
    return {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact),
        "provider": provider_name,
        "model": model,
        "interface": "streamlit",
        "system_prompt": str(SYSTEM_PROMPT_PATH.relative_to(ROOT)),
        "tools": str(TOOLS_PATH.relative_to(ROOT)),
        "history_window": HISTORY_WINDOW,
        "max_tool_rounds": MAX_TOOL_ROUNDS,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }


def reset_session(provider_name: str, model: str | None, version: str) -> None:
    st.session_state.history = []  # model context: user/assistant text pairs, like chat.py
    st.session_state.transcript = new_transcript(provider_name, model, version)
    st.session_state.config = (provider_name, model, version)


# ---------------------------------------------------------------- helpers

def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def short(value: Any, limit: int = 48) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def describe_result(tool: str, result: Any) -> tuple[str, str]:
    """Return (kind, plain-language outcome) for one tool call."""
    if not isinstance(result, dict):
        return "ok", "Xong"
    if result.get("error"):
        return "error", f"Lỗi {result['error']}: {short(result.get('message', ''), 70)}"
    if result.get("awaiting_user"):
        return "ask", "Đang chờ bạn trả lời"
    if "items" in result:
        count = len(result.get("items") or [])
        return "ok", f"{count} kết quả" if count else "Không có kết quả"
    if result.get("status"):
        return "ok", f"Trạng thái: {result['status']}"
    if "markdown" in result:
        return "ok", "Đã trình bày bản tin"
    return "ok", "Xong"


def find_question(turn: dict[str, Any]) -> dict[str, Any] | None:
    """The clarify result that paused this turn, if any."""
    for rnd in reversed(turn.get("rounds") or []):
        for event in rnd.get("tool_results", []):
            result = event.get("result")
            if isinstance(result, dict) and result.get("awaiting_user"):
                return result
    return None


def quick_replies(question: dict[str, Any]) -> list[str]:
    if question.get("response_type") == "yes_no":
        return ["Có", "Không"]
    return [str(option) for option in question.get("options") or []][:6]


# ---------------------------------------------------------------- rendering

def stop_html(kind: str, color: str, name: str, line_name: str = "", args_text: str = "", outcome: str = "") -> str:
    parts = [f'<div class="stop {kind}" role="listitem" style="--line:{color}"><span class="dot"></span><div>',
             f'<div class="stop-head"><span class="stop-name">{esc(name)}</span>']
    if line_name:
        parts.append(f'<span class="stop-line">{esc(line_name)}</span>')
    parts.append("</div>")
    if args_text:
        parts.append(f'<div class="stop-args">{esc(args_text)}</div>')
    if outcome:
        parts.append(f'<div class="stop-result">{esc(outcome)}</div>')
    parts.append("</div></div>")
    return "".join(parts)


def route_html(turn: dict[str, Any]) -> str:
    stops: list[str] = []
    for rnd in turn.get("rounds") or []:
        events = rnd.get("tool_results") or []
        for event in events:
            tool = event.get("tool", "?")
            line_name, color = LINES.get(tool, OTHER_LINE)
            if len(events) > 1:
                line_name += ", chạy song song"
            kind, outcome = describe_result(tool, event.get("result"))
            args = dict(event.get("args") or {})
            if kind == "ask":
                args.pop("question", None)  # the question itself is shown in the ask box below
            args_text = ", ".join(f"{k}: {short(v, 40)}" for k, v in list(args.items())[:4])
            stops.append(stop_html(kind, ERROR_COLOR if kind == "error" else color, tool, line_name,
                                   args_text, outcome))

    status = turn.get("status")
    if status == "answered":
        if stops:
            stops.append(stop_html("end", "#17212B", "Trả lời"))
        else:
            stops.append(stop_html("end", "#17212B", "Trả lời trực tiếp", outcome="Không gọi tool nào"))
    elif status == "max_tool_rounds":
        stops.append(stop_html("error", ERROR_COLOR, "Dừng",
                               outcome=f"Đã gọi tool {MAX_TOOL_ROUNDS} vòng mà chưa xong"))
    return f'<div class="route" role="list" aria-label="Đường đi của agent">{"".join(stops)}</div>'


def render_details(turn: dict[str, Any]) -> None:
    rounds = [r for r in turn.get("rounds") or [] if r.get("tool_results")]
    if not rounds:
        return
    with st.expander("Chi tiết từng tool: args và JSON trả về", expanded=False):
        for rnd in rounds:
            st.markdown(f"**Vòng {rnd.get('round')}**")
            if rnd.get("assistant_text"):
                st.caption(f"Model ghi chú: {rnd['assistant_text']}")
            for event in rnd["tool_results"]:
                args = json.dumps(event.get("args", {}), ensure_ascii=False)
                st.code(f"{event.get('tool')}({args})", language="python")
                result = event.get("result", {})
                if isinstance(result, dict) and result.get("error"):
                    # Never hide tool failures: they are evidence (rubric C6).
                    st.error(f"Tool trả lỗi {result.get('error')}: {result.get('message', '')}")
                st.json(result, expanded=False)


def render_turn(turn: dict[str, Any]) -> None:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        status = turn.get("status")
        if status == "provider_error":
            error = str(turn.get("error", ""))
            hint = " Kiểm tra key trong starter_v0/.env rồi gửi lại câu hỏi." if "API key" in error else ""
            st.error(f"Không gọi được model: {error}.{hint}")
            return
        st.markdown(route_html(turn), unsafe_allow_html=True)
        if status == "waiting_for_user":
            question = find_question(turn) or {}
            text = question.get("question") or turn.get("assistant_text") or ""
            st.markdown(
                f'<div class="ask-box"><div class="ask-title">Agent cần bạn trả lời trước khi làm tiếp</div>'
                f"<p>{esc(text)}</p></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(turn.get("assistant_text") or "_Model không trả về nội dung._")
        render_details(turn)


def render_legend(declarations: list[dict[str, Any]]) -> None:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for tool in declarations:
        groups.setdefault(LINES.get(tool["name"], OTHER_LINE), []).append(tool)
    for (line_name, color), tools in groups.items():
        rows = "".join(
            f'<div class="legend-tool"><code>{esc(t["name"])}</code> '
            f'{esc(short((t.get("description") or "").strip().split(". ")[0], 90))}</div>'
            for t in tools
        )
        st.markdown(
            f'<div class="legend" style="--line:{color}"><span class="bar"></span>'
            f'<div><div class="legend-name">{esc(line_name)}</div>{rows}</div></div>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------- agent turn

def run_turn(user_text: str, provider_name: str, model: str | None) -> dict[str, Any]:
    system_prompt = SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")
    openai_tools = to_openai_tools(load_tool_declarations(TOOLS_PATH))
    transcript = st.session_state.transcript
    messages = [
        {"role": "system", "content": system_prompt},
        *trim_history(st.session_state.history, HISTORY_WINDOW),
        {"role": "user", "content": user_text},
    ]
    turn: dict[str, Any] = {
        "turn_index": len(transcript["turns"]) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    try:
        provider = make_provider(provider_name)
        result = run_model_tool_loop(
            provider=provider,
            messages=messages,
            tools=openai_tools,
            model=model,
            max_tool_rounds=MAX_TOOL_ROUNDS,
        )
        turn.update(result)
        st.session_state.history.append({"role": "user", "content": user_text})
        st.session_state.history.append({"role": "assistant", "content": result["assistant_text"]})
    except Exception as exc:  # same handling as chat.py: keep the error as evidence
        turn.update({"status": "provider_error", "error": f"{type(exc).__name__}: {exc}"})
    turn["ended_at"] = now_iso()
    transcript["turns"].append(turn)
    write_transcript(TRANSCRIPTS_DIR / f"{transcript['transcript_id']}.transcript.json", transcript)
    return turn


# ---------------------------------------------------------------- page

st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)
declarations = load_tool_declarations(TOOLS_PATH)

with st.sidebar:
    with st.expander("Cấu hình model", expanded=not LOCKED):
        if LOCKED:
            st.caption("Cấu hình đang khoá cho buổi demo.")
        provider_name = st.selectbox(
            "Provider", PROVIDERS, disabled=LOCKED,
            index=PROVIDERS.index(DEFAULT_PROVIDER) if DEFAULT_PROVIDER in PROVIDERS else 0,
        )
        model_input = st.text_input("Model", value=DEFAULT_MODEL, disabled=LOCKED,
                                    placeholder="Để trống để dùng model mặc định")
        version = st.text_input("Nhãn version ghi vào transcript", value=DEFAULT_VERSION,
                                disabled=LOCKED).strip() or "dev"
    model = model_input.strip() or None

    if "transcript" not in st.session_state or st.session_state.config != (provider_name, model, version):
        reset_session(provider_name, model, version)
    if st.button("Bắt đầu cuộc trò chuyện mới", use_container_width=True):
        reset_session(provider_name, model, version)

    st.markdown("#### Các tuyến tool")
    st.caption("Mỗi câu trả lời có một dải hành trình. Màu ga cho biết agent đã dùng loại tool nào.")
    render_legend(declarations)

    transcript = st.session_state.transcript
    with st.expander("Thông tin kỹ thuật", expanded=False):
        st.caption(f"Phiên bản prompt và tools: `{transcript['artifact_version']}`")
        st.caption(f"Transcript: `transcripts/{transcript['transcript_id']}.transcript.json`")
        st.caption(f"Đã dùng {len(transcript['turns'])} trên {MAX_TURNS_PER_SESSION} lượt của phiên này")

st.markdown(
    '<h1 class="ra-title">Research Agent</h1>'
    '<p class="ra-lede">Hỏi một câu. Agent tự chọn tool phù hợp, chạy thật, rồi cho bạn thấy '
    "đường nó đã đi để có câu trả lời. Thiếu thông tin hay sắp đăng gì lên Telegram, agent sẽ hỏi lại bạn trước.</p>",
    unsafe_allow_html=True,
)

turns = st.session_state.transcript["turns"]
for past_turn in turns:
    render_turn(past_turn)

clicked = None
if not turns:
    st.markdown('<p class="ra-try">Chưa biết hỏi gì? Thử một câu:</p>', unsafe_allow_html=True)
    for question in SAMPLE_QUESTIONS:
        if st.button(question, key=f"sample-{question}", use_container_width=True):
            clicked = question
elif turns[-1].get("status") == "waiting_for_user":
    replies = quick_replies(find_question(turns[-1]) or {})
    if replies:
        columns = st.columns(len(replies))
        for column, reply in zip(columns, replies):
            if column.button(reply, key=f"reply-{len(turns)}-{reply}", use_container_width=True):
                clicked = reply

limit_reached = len(turns) >= MAX_TURNS_PER_SESSION
typed = st.chat_input(
    "Phiên này đã hết lượt. Bấm “Bắt đầu cuộc trò chuyện mới” ở thanh bên." if limit_reached
    else "Hỏi agent, hoặc trả lời câu agent vừa hỏi",
    disabled=limit_reached,
)
user_text = (typed or clicked or "").strip()

if user_text and not limit_reached:
    with st.spinner("Agent đang chọn tool và chạy…"):
        run_turn(user_text, provider_name, model)
    st.rerun()
