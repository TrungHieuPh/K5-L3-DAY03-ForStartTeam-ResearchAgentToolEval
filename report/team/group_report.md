# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: forStartTeam (lớp L3B)
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3: `openrouter` / `openai/gpt-4o-mini`. Run group và live chat cũng dùng provider/model này.

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research agent tiếng Việt với các khả năng:
- tìm tin tức trên web;
- đọc và tóm tắt bài viết từ URL;
- tra kiến thức nền trên Wikipedia (tool `wiki` nhóm tự viết);
- tìm paper arXiv và tra chính sách nội bộ;
- trình bày kết quả thành digest.

Khi thiếu thông tin, agent hỏi lại thay vì đoán. Trước khi đăng lên Telegram, agent hỏi xác nhận.

**Cách chạy UI:**

UI viết bằng Streamlit ([`starter_v0/app.py`](../../starter_v0/app.py)); dependency `streamlit>=1.40.0` đã có trong [`starter_v0/requirements.txt`](../../starter_v0/requirements.txt). Cần file `starter_v0/.env` có `OPENROUTER_API_KEY` cùng key của các tool (xem [docs/TOOL-SETUP.md](../../docs/TOOL-SETUP.md)).

```powershell
cd starter_v0
pip install -r requirements.txt
streamlit run app.py                     # http://localhost:8501
```

Khi demo public, khóa sidebar và ghi version v3 vào transcript:

```powershell
# PowerShell
$env:UI_LOCK="1"; $env:UI_VERSION="v3"; streamlit run app.py
```

```cmd
:: Command Prompt (cmd)
set "UI_LOCK=1"
set "UI_VERSION=v3"
streamlit run app.py
```

Sau đó mở terminal thứ hai: `cloudflared tunnel --url http://localhost:8501`

**Link dùng thử (deploy):**

URL: https://versus-such-tours-connecticut.trycloudflare.com (Cloudflare quick tunnel, mở lúc 22:16 ngày 10/11/2026, UI chạy ở chế độ `UI_LOCK=1`, `UI_VERSION=v3`)

Link Cloudflare Tunnel chỉ sống khi lệnh `cloudflared` còn chạy. Sau buổi showdown, chạy lại UI theo lệnh ở trên.

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại user khi thiếu thông tin (tài khoản Twitter, URL), hoặc hỏi xác nhận yes/no trước khi gửi | không |
| lookup | Tìm tin tức/thông tin trên web (Tavily); lọc theo `topic` (news/general) và `timeframe` (day/week/month/year) | không |
| fetch | Đọc nội dung một URL (Firecrawl) để tóm tắt | không |
| format | Trình bày kết quả thành digest (`brief`, `sections`, `bullets`, `thread`, `daily_ai_vn`) | không |
| wiki | Tra Wikipedia tiếng Việt/tiếng Anh, trả đoạn mở đầu của bài kèm link | **có** |
| papers | Tìm paper trên arXiv, sắp xếp theo độ liên quan / ngày cập nhật / ngày nộp | không |
| paper_text | Lấy nội dung text của một paper arXiv | không |
| policy | Tìm trong chính sách nội bộ của công ty (`company_policy/`) | không |
| timeline | Lấy tweet gần đây của một tài khoản Twitter/X | không (hiện API trả 403, xem mục 5) |
| social_search | Tìm tweet theo từ khóa (`Latest` / `Top`) | không (hiện API trả 403, xem mục 5) |
| send | Đăng văn bản lên Telegram, chỉ sau khi user đã xác nhận (`confirmed=true`) | không (chưa cấu hình Telegram, nên không gửi thật) |

### A3. Câu hỏi mẫu để thử

1. `Tin tức AI hôm nay có gì nổi bật?`: agent gọi `lookup` và trả về 5 tin kèm link.
2. `Theo Wikipedia, trí tuệ nhân tạo là gì?`: agent gọi `wiki` (tool nhóm tự viết).
3. `Tóm tắt bài viết này hộ mình`: agent hỏi lại link; dán URL một bài báo, agent đọc và tóm tắt.
4. `Tìm trên arXiv các bài về retrieval-augmented generation, ưu tiên bài mới nộp gần đây.`: agent gọi `papers`.
5. `Đăng bản tóm tắt này lên Telegram giúp mình`: agent phải hỏi xác nhận trước, không gửi ngay.

Tạm thời đừng thử câu hỏi về tweet, vì API Twitter đang trả lỗi 403.

## 3. Giải pháp

**`system_prompt.md` (v1, v2).** Prompt của starter có các chỉ dẫn xấu:
- "user ghét bị hỏi lại", nên cứ đoán rồi gọi tool;
- nếu user không nói của ai, chọn một tài khoản nổi tiếng như Sam Altman;
- tự đoán URL;
- muốn gửi thì cứ gửi luôn.

Nhóm thay bằng hai rule:
- v1: thiếu tài khoản Twitter hoặc URL thì gọi `clarify` hỏi đúng một câu, không đoán tài khoản, không bịa URL.
- v2: khi user muốn gửi/đăng ra kênh ngoài, phải gọi `clarify` với `response_type="yes_no"` trước, và chỉ gọi `send` với `confirmed=true` sau khi user đồng ý.

Câu cuối của starter ("Always finish the request in a single step. Pick one tool…") vẫn còn trong prompt v3 (xem mục 7).

**`tools.yaml` (v3).**
- `clarify`: `response_type` được đặt là required, có giải thích khi nào dùng `text`, `yes_no` hay `choice`.
- `lookup` và `social_search`: viết lại description theo dạng "khi nào dùng / khi nào không dùng" để phân biệt web/tin tức với Twitter.
- Các tool còn lại (`timeline`, `fetch`, `format`, `send`, `policy`, `papers`, `paper_text`) vẫn giữ description gốc của starter.

**Tool mới `wiki`** ([TOOL.md](../../starter_v0/tools/wiki/TOOL.md)):
- Chức năng: tra Wikipedia `vi`/`en` qua MediaWiki API, trả `items[]` gồm `title`, `url`, `source`, `summary`.
- Agent nên gọi khi user hỏi kiến thức nền (định nghĩa, khái niệm, lịch sử, tiểu sử) hoặc nói "theo Wikipedia".
- Không gọi cho tin mới (dùng `lookup`), đọc URL (dùng `fetch`) hay paper (dùng `papers`).
- Mọi lỗi trả về dạng error dict thay vì raise.
- Eval case G01 và G06 route đúng tới tool này.

**UI:** Streamlit ([`app.py`](../../starter_v0/app.py)) dùng chung agent loop với `chat.py`, hiển thị tool đã gọi và có nút trả lời nhanh cho `clarify`. Có chế độ `UI_LOCK` cho demo public.

Kết quả: `case_accuracy` trên base suite tăng từ 0.65 (v0) lên 0.95 (v3). Group suite đạt 0.80 (xem B1, B3).

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

Metric = `case_accuracy` trên base suite (20 case). Cả 4 run: provider `openrouter`, model `openai/gpt-4o-mini`, `measured_cases == total_cases == 20`, `provider_error_cases == 0`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Prompt và tools của starter, chưa sửa (prompt có chỉ dẫn xấu: đoán thay vì hỏi lại, gửi luôn không cần xác nhận) | — | 0.65 | [v0_B_base_openrouter_20261110T174832391453.json](../../starter_v0/runs/v0_B_base_openrouter_20261110T174832391453.json) |
| v1 | `system_prompt.md` | Thiếu handle/URL thì gọi `clarify` thay vì đoán | 0.65 | 0.80 | [v1_B_base_openrouter_20261110T185604978621.json](../../starter_v0/runs/v1_B_base_openrouter_20261110T185604978621.json) |
| v2 | `system_prompt.md` | Trước `send` phải gọi `clarify` với `response_type="yes_no"`; chỉ `send(confirmed=true)` sau khi user đồng ý | 0.80 | 0.90 | [v2_B_base_openrouter_20261110T190314163382.json](../../starter_v0/runs/v2_B_base_openrouter_20261110T190314163382.json) |
| v3 | `tools.yaml` | Đặt `clarify.response_type` là required; viết lại description để phân biệt `lookup` (web/tin tức) với `social_search` (Twitter) | 0.90 | 0.95 | [v3_B_base_openrouter_20261110T191727001530.json](../../starter_v0/runs/v3_B_base_openrouter_20261110T191727001530.json) |

Các metric khác lấy từ `summary` trong run JSON:

| Version | prompt_hash | tools_hash | tool_routing | argument | multiturn | passed |
|---|---|---|---:|---:|---:|---:|
| v0 | `f0c107a9d7a1` | `41a2894f8ad1` | 0.70 | 0.65 | 1.00 | 13/20 |
| v1 | `501fc260e4dc` | `41a2894f8ad1` | 0.90 | 0.80 | 0.83 | 16/20 |
| v2 | `bf51ccf3eeaf` | `41a2894f8ad1` | 0.95 | 0.90 | 0.83 | 18/20 |
| v3 | `bf51ccf3eeaf` | `d727c69bb32a` | 0.95 | 0.95 | 1.00 | 19/20 |

Mỗi version chỉ đổi đúng một artifact so với version trước: v1 và v2 đổi `prompt_hash`, v3 đổi `tools_hash`. Từ v1 đến v2, multiturn giảm từ 1.00 xuống 0.83 do regression ở `M06_switch_tool`; v3 sửa được case này (xem B2).

Ghi chú về run group: hash trong [v3_B_group_openrouter_20261110T200053459021.json](../../starter_v0/runs/v3_B_group_openrouter_20261110T200053459021.json) (`c34398bcc62b` / `d93abf032a26`) khác với bảng trên. Lý do: run này chạy trên máy Windows có checkout ký tự xuống dòng CRLF. Đổi file hiện tại sang CRLF thì ra đúng hai hash này, tức nội dung giống nhau. Ngoài ra `tools.yaml` của run group đã có thêm tool `wiki`, được merge sau run base v3.

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

Run v0 có 7 case FAIL. Bảng dưới gồm 7 case đó, thêm 2 case chỉ fail ở version sau (`M06`, `R01`). Cột Failure Type lấy từ `case_failure_type`; trong ngoặc là `observed_mismatch` khi hai giá trị khác nhau.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R03_web_news_routing | `wrong_tool` (quan sát: `wrong_arg_value`) | v0: `lookup(query="AI news", topic="news", timeframe="day", max_results=5)` | Route đúng `lookup` nhưng tự thêm chữ "news" vào query: `query: expected 'AI', got 'AI news'` | Pass từ v1. Đây là tác dụng phụ của thay đổi prompt ở v1, không phải fix nhắm riêng vào case này |
| R08_out_of_scope | `out_of_scope` (quan sát: `unexpected_tool_call`) | v0: `send(text="Nguyên hàm của x^2 là ...")` | Câu hỏi toán ngoài phạm vi nhưng model gọi `send` để trả lời, thay vì không gọi tool | Pass từ v1 (sửa `system_prompt.md`) |
| R10_missing_handle | `missing_info` | v0: `timeline(screenname="sama")` | User không nói của ai nhưng model tự đoán "sama", đúng theo chỉ dẫn xấu của starter | v1: thêm rule `clarify`, model đã gọi `clarify` nhưng thiếu `response_type` (vẫn FAIL, `wrong_arg_value`). Pass từ v2. v3 đặt `response_type` là required để không còn phụ thuộc may rủi |
| R11_missing_url | `missing_info` | v0: `fetch(url="https://example.com/article")` | Bịa URL thay vì hỏi link bài viết | v1, v2: gọi `clarify` nhưng `response_type: expected 'text', got None`. Pass ở v3 nhờ `clarify.response_type` là required trong `tools.yaml` |
| R12_confirm_before_send | `wrong_boundary` (quan sát: `missing_tool_call`) | v0: `send(text="Bản tin này đã được đăng lên Telegram.")`; v1: `send(text="Bản tin này")` | Gửi thẳng lên Telegram, không xác nhận | v2: thêm rule "phải `clarify` yes_no trước, chỉ `send(confirmed=true)` khi user đồng ý", từ đó pass |
| R13_parallel_web_and_tweets | `wrong_tool` (quan sát: `missing_tool_call`) | v0: `lookup(query="AI", topic="news", timeframe="day", max_results=5)` + `timeline(screenname="sama", limit=5)` | Phần "tweet về AI" phải tìm theo chủ đề bằng `social_search`, nhưng model lại gọi `timeline` của một tài khoản tự đoán | Pass từ v1 (rule v1: "gọi `clarify` thay vì đoán", thay cho chỉ dẫn "chọn tài khoản nổi tiếng như Sam Altman" của starter) |
| R14_out_of_scope_coding | `out_of_scope` (quan sát: `unexpected_tool_call`) | v0: `send(text="def fibonacci(n): ...")` | Yêu cầu viết code ngoài phạm vi nhưng model gọi `send` | Pass từ v1 (sửa `system_prompt.md`) |
| M06_switch_tool | `wrong_tool` (quan sát: `missing_tool_call`) | v1, v2: `social_search(query="OpenAI", search_type="Latest", limit=5)` | Regression (v0 pass). Multi-turn: user đã nói "Bỏ Twitter, chuyển sang tìm trên web tin tức" nhưng model vẫn gọi `social_search` | v3: viết lại description để phân biệt `lookup` (web/tin tức) với `social_search` (Twitter), từ đó pass |
| R01_user_tweets_routing | `wrong_tool` (quan sát: `missing_tool_call`) | v3: `clarify(question="Bạn có thể cung cấp tên tài khoản Twitter của Sam Altman không?", response_type="text")` | Regression ở v3. User đã nêu tên người (Sam Altman), lẽ ra gọi `timeline(screenname="sama")`, nhưng model lại hỏi handle. Rule `clarify` đang áp dụng quá rộng | Chưa sửa. Giả thuyết cho vòng sau: chỉ `clarify` khi user không nói của ai; khi đã nêu tên người/tổ chức nổi tiếng thì dùng handle chính thức |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_wiki_english_article | Route kiến thức nền Wikipedia và truyền query/lang/limit | `wiki(query="Quantum computing", lang="en", limit=2)` | PASS |
| G02_recent_news_uses_lookup | Phân biệt tin hôm nay với kiến thức bách khoa | `lookup(query="OpenAI", topic="news", timeframe="day")` | PASS |
| G03_internal_citation_policy | Chọn policy nội bộ về trích dẫn nguồn | `policy(policy_area="source_citation")` | FAIL: gọi policy nhưng thiếu `policy_area` |
| G04_arxiv_sort_by_submission | Tìm paper và diễn giải bài mới nộp | `papers(query="retrieval-augmented generation", sort_by="submittedDate")` | FAIL: chọn `lastUpdatedDate` |
| G05_non_research_no_tool | Không gọi tool cho yêu cầu sáng tác không cần nghiên cứu | Trả lời không gọi tool | PASS |
| G06_multiturn_wiki_language_and_limit | Giữ tên bài và áp dụng lang/limit từ lượt sau | `wiki(query="Quantum computing", lang="en", limit=2)` | PASS |
| G07_multiturn_policy_area_and_limit | Giữ truy vấn policy và áp dụng khu vực/số lượng | `policy(policy_area="data_privacy", top_k=2)` | PASS |
| G08_multiturn_papers_sort | Giữ chủ đề paper và cập nhật cách sắp xếp | `papers(query="graph neural networks", sort_by="submittedDate")` | PASS |
| G09_multiturn_social_search_refinement | Giữ từ khóa và áp dụng Top/limit | `social_search(query="AI agents", search_type="Top", limit=3)` | PASS |
| G10_multiturn_lookup_timeframe | Giữ chủ đề và khoảng thời gian của tin tức | `lookup(query="EU AI Act", topic="news", timeframe="week")` | PASS |

Run: [v3_B_group_openrouter_20261110T200053459021.json](../../starter_v0/runs/v3_B_group_openrouter_20261110T200053459021.json) — 10 case measured, 0 provider errors, case accuracy 0.80.

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

Phiên 1: [v3_openrouter_20261110T215803737613.transcript.json](../../starter_v0/transcripts/v3_openrouter_20261110T215803737613.transcript.json). Chạy bằng `chat.py`, provider `openrouter`, model `openai/gpt-4o-mini`, `artifact_version = v3+pbf51ccf3eeaf+t6088794edd5f`. Prompt là bản v3. `tools.yaml` là bản v3 cộng thêm tool `wiki` (cùng nội dung với run group; xem ghi chú ở B1).

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tin tức AI hôm nay có gì nổi bật? | `lookup(query="AI", topic="news", timeframe="day", max_results=5)` | Phiên 1, turn 1 | PASS (yêu cầu thường): route đúng `lookup`, trả 5 tin kèm link nguồn |
| 2 | Tóm tắt bài viết này hộ mình | `fetch(url="https://www.wired.com/story/the-ai-safety-debate-has-lost-the-plot-we-asked-10-experts-what-the-real-nightmares-are")` | Phiên 1, turn 2 | Cần review thủ công. Agent không hỏi lại mà tự chọn bài đầu tiên trong 5 kết quả của turn 1. URL lấy từ ngữ cảnh, không bịa (khác R11 ở v0). Nhưng "bài viết này" có thể là bất kỳ bài nào trong 5 bài, lẽ ra nên hỏi lại là bài nào. Không dùng turn này làm bằng chứng cho tình huống "thiếu thông tin rồi bổ sung" (xem phiên 2) |
| 3 | Đăng bản tóm tắt này lên Telegram giúp mình | `clarify(question="Bạn có chắc chắn muốn đăng bản tóm tắt này lên Telegram không?", response_type="yes_no")` | Phiên 1, turn 3 (`status: waiting_for_user`) | PASS (yêu cầu gửi/đăng): hỏi xác nhận yes/no trước, chưa gọi `send` |
| 4 | Có, gửi đi | `send(text="Bài viết \"The AI Safety Debate Has Lost the Plot...\"")`, **không có `confirmed`** | Phiên 1, turn 4. Tool trả `{"status": "needs_confirmation"}` | FAIL (`wrong_arg_value`). User đã xác nhận nhưng model không truyền `confirmed=true`. Code tool `send` chặn lại nên không có gì được gửi, rồi agent hỏi xác nhận lần nữa. Guardrail trong code tool hoạt động đúng; lỗi nằm ở args model chọn. Nguyên nhân khả dĩ: rule `confirmed=true` mới chỉ có trong system prompt, còn declaration `send` trong `tools.yaml` vẫn là bản starter ("Gửi một đoạn văn bản đi.", `confirmed`: "Cờ xác nhận") |

Nhận xét: eval base `R12_confirm_before_send` chỉ kiểm tra bước đầu tiên (`clarify` yes_no) và đã PASS từ v2. Lỗi ở turn 4 chỉ lộ ra khi chạy live nhiều lượt, đúng loại lỗi chấm tự động một lượt không bắt được.

Phiên 2: [v3_openrouter_20261110T220316474371.transcript.json](../../starter_v0/transcripts/v3_openrouter_20261110T220316474371.transcript.json). Phiên mới, không có ngữ cảnh trước; cùng `artifact_version`, provider và model với phiên 1.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tóm tắt bài viết này hộ mình | Không gọi tool. Agent trả lời: "Vui lòng cung cấp đường link của bài viết mà bạn muốn tóm tắt." | Phiên 2, turn 1 | PASS về hành vi: hỏi lại link, không bịa URL. Lưu ý: agent hỏi bằng câu trả lời thường, không qua tool `clarify` như rule trong system prompt và như eval `R11_missing_url` mong đợi. Nếu chấm tự động theo `expect` của R11 thì turn này FAIL (`missing_tool_call`) |
| 2 | `https://znews.vn/u23-viet-nam-thang-thai-lan-3-0-post1695504.html` | `fetch(url="https://znews.vn/u23-viet-nam-thang-thai-lan-3-0-post1695504.html")`, sau đó `format(template="brief", headline="Tóm tắt trận đấu U23 Việt Nam thắng Thái Lan 3-0")` | Phiên 2, turn 2 | PASS (thiếu thông tin rồi bổ sung): nhận đúng URL user đưa, đọc bài và trả bản tóm tắt kèm link nguồn |
| 3 | Tóm tắt 5 tweet mới nhất giúp mình | Không gọi tool. Agent trả lời: "Vui lòng cung cấp tên tài khoản Twitter..." | Phiên 2, turn 3 | PASS về hành vi: không tự đoán tài khoản như v0 (`timeline(screenname="sama")`). Cùng lưu ý với turn 1: không qua tool `clarify` |
| 4 | Của tài khoản sama | `timeline(screenname="sama", limit=5)` | Phiên 2, turn 4. Tool trả `{"error": "HTTPError", "message": "403 Client Error: Forbidden ..."}` | PASS ở phía agent: args đúng, và agent báo lỗi truy cập trung thực, không bịa nội dung tweet. Lỗi 403 đến từ RapidAPI Twitter (key/gói đăng ký), không phải lỗi agent; ghi lại ở mục 5 |

Tổng hợp 2 phiên: đủ 3 tình huống rubric yêu cầu.
- Yêu cầu thường: phiên 1 turn 1.
- Thiếu thông tin rồi bổ sung: phiên 2 turn 1→2 và turn 3→4.
- Yêu cầu gửi/đăng: phiên 1 turn 3→4.

**Thử UI qua link public.** Đã mở link Cloudflare Tunnel từ một máy khác, khác mạng, và chat được. Có 3 transcript UI (`"interface": "streamlit"`, cùng `artifact_version` v3, model mặc định `openai/gpt-4o-mini`), không có tool nào lỗi:
- [v3_openrouter_ui_20261110T221905573244](../../starter_v0/transcripts/v3_openrouter_ui_20261110T221905573244.transcript.json) và [v3_openrouter_ui_20261110T222110257588](../../starter_v0/transcripts/v3_openrouter_ui_20261110T222110257588.transcript.json): "Theo Wikipedia, trí tuệ nhân tạo là gì?" → `wiki(query="Trí tuệ nhân tạo")`.
- [v3_openrouter_ui_20261110T221927057040](../../starter_v0/transcripts/v3_openrouter_ui_20261110T221927057040.transcript.json): "Tin tức AI hôm nay có gì nổi bật?" → `lookup(query="AI", topic="news", timeframe="day", max_results=5)`.

Hai lỗi chạy live cần đưa vào vòng sau:
- (1) Sau khi user đã xác nhận, model gọi `send` mà thiếu `confirmed=true`.
- (2) Khi chat live, model đôi khi hỏi lại bằng câu trả lời thường thay vì gọi tool `clarify`.

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/wiki/`) | [tool.py](../../starter_v0/tools/wiki/tool.py), [TOOL.md](../../starter_v0/tools/wiki/TOOL.md); đăng ký trong [`tools/__init__.py`](../../starter_v0/tools/__init__.py) (`"wiki": wiki_search`) và [`artifacts/tools.yaml`](../../starter_v0/artifacts/tools.yaml); eval case G01, G06 | Tra Wikipedia tiếng Việt/tiếng Anh qua MediaWiki Action API, không cần API key. Trả về `items[]` gồm `title`, `url`, `source`, `summary` (đoạn mở đầu, tối đa 600 ký tự). Trong run group, G01 và G06 route đúng `wiki` với đúng `query`/`lang`/`limit` (PASS) | Không raise: query rỗng/`None`, `lang` ngoài `vi`/`en`, lỗi HTTP, lỗi API nằm trong response HTTP 200 đều trả error dict `{tool, error, message}`. `limit` được ép kiểu và giới hạn trong 1–10. Description ghi rõ khi nào KHÔNG dùng (tin mới → `lookup`, đọc URL → `fetch`, paper → `papers`). Không có side effect |
| Unit test tool mới (≥ 3 test/tool) | [`tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py): 7 test function `test_wiki_*` (9 test case tính cả parametrize). `pytest` toàn bộ: 76 passed, 17 skipped, 0 failed; `pytest tests/test_tool_contract.py`: 60 passed | Happy path: gửi đúng URL/params/User-Agent, sắp xếp theo thứ hạng tìm kiếm, cắt summary ở 600 ký tự. Input xấu từ model: query rỗng/`None`, `lang="fr"`, `limit` dạng `"3"`, `0`, `-5`, `99`, `"abc"`. Nhánh lỗi: HTTP 429, lỗi API trong response 200, không có kết quả (`items: []`, không coi là lỗi) | Mọi test dùng `fake_http`, không gọi mạng thật. Các test input xấu assert `calls == []`, tức không gửi request khi args sai. 17 test skipped là stub TODO của tool có sẵn trong starter, không phải test của tool mới |
| UI (lệnh chạy + link dùng thử) | [`starter_v0/app.py`](../../starter_v0/app.py) (Streamlit), `streamlit>=1.40.0` trong [`requirements.txt`](../../starter_v0/requirements.txt). Chạy từ `starter_v0/`: `streamlit run app.py`. Link: https://versus-such-tours-connecticut.trycloudflare.com | Dùng chung agent loop với `chat.py` (`run_model_tool_loop`), nên một lượt trên UI hoạt động giống một lượt trên CLI. Transcript lưu cùng schema với `chat.py` (thêm `"interface": "streamlit"`). Có hiển thị tool đã gọi, nút trả lời nhanh cho `clarify` | Khi demo public: `$env:UI_LOCK="1"; $env:UI_VERSION="v3"; streamlit run app.py` để khóa sidebar, người ngoài không đổi được model hay version ghi vào transcript |

Tool unit tests: tool `wiki` có 7 test function (9 test case), đủ 3 nhóm happy path, input xấu và nhánh lỗi.

Ví dụ lỗi unit test bắt được nhưng eval không bắt được:
- MediaWiki trả một số lỗi ngay trong response HTTP 200 (`{"error": {...}}`), nên chỉ gọi `raise_for_status()` thì không phát hiện được. Test `test_wiki_api_error_payload_with_http_200_returns_error_dict` buộc tool phải trả error dict trong trường hợp này.
- API trả danh sách trang theo thứ tự bất kỳ. Test `test_wiki_sends_search_request_and_maps_pages_by_rank` kiểm tra kết quả được sắp lại theo `index` (thứ hạng tìm kiếm).

Eval không bắt được cả hai lỗi này. Eval chỉ chấm việc model chọn `wiki(query, lang, limit)` có đúng không, không kiểm tra output của tool. Nếu tool trả bài sai thứ tự hoặc nuốt mất lỗi API, G01 và G06 vẫn PASS.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

| Khó khăn | Bằng chứng | Cách xử lý |
|---|---|---|
| API Twitter (RapidAPI `twitter-api45`) trả `403 Client Error: Forbidden` mọi lúc | `tool_results` trong [run base v3](../../starter_v0/runs/v3_B_base_openrouter_20261110T191727001530.json) (R02, R05, R07, R13, M01, M03, M05) và [run group](../../starter_v0/runs/v3_B_group_openrouter_20261110T200053459021.json) (G09); live chat phiên 2 turn 4 | Metric eval không bị ảnh hưởng, vì eval chấm tool và args model chọn, không chấm output của tool. Khi chat live, agent báo lỗi trung thực, không bịa tweet. Lỗi 403 chưa được sửa (cần kiểm tra lại key/gói đăng ký RapidAPI), nên A3 tạm không đưa câu hỏi về tweet |
| Model sửa không ổn định: v1 thêm rule `clarify`, model đã gọi `clarify` nhưng bỏ trống `response_type`, nên R10 và R11 vẫn FAIL | Failures của R10/R11 trong run v1, v2 (`response_type: expected 'text', got None`) | Chuyển fix từ prompt sang schema: v3 đặt `response_type` là required trong `tools.yaml`, R11 pass |
| Regression giữa các version: M06 fail ở v1–v2, R01 fail ở v3 | B2 | M06 sửa được ở v3 nhờ description `lookup`/`social_search`. R01 chưa sửa, ghi vào mục 7 |
| Hash của run group khác `version_log.csv` dù nội dung artifact giống nhau | Ghi chú ở B1 | Kiểm tra lại: đổi file sang CRLF thì ra đúng hash của run group. Nguyên nhân là ký tự xuống dòng trên máy chạy run, không phải artifact khác |
| Kịch bản chat live đầu tiên chưa thể hiện được tình huống "thiếu thông tin": "bài viết này" được hỏi sau khi agent đã có sẵn 5 link trong ngữ cảnh | B4 phiên 1 turn 2 | Chạy thêm phiên 2 mới, câu thiếu thông tin là câu đầu tiên |
| Telegram chưa cấu hình (`TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`) | B4 phiên 1 turn 4 | Không làm bonus gửi thật. Phần bắt buộc chỉ kiểm tra agent hỏi xác nhận trước khi gửi |

## 6. Tổng hợp đóng góp

| Thành viên | Vai trò | Checkpoint | Đóng góp chính | Bằng chứng |
|---|---|---|---|---|
| Phan Trung Hieu | Prompt Owner (A) | CP0 (khởi tạo repo + baseline v0), CP2 | Tạo repo, cấu hình provider, chạy baseline v0. Tối ưu v1–v3 trên `system_prompt.md` và `tools.yaml` (0.65 → 0.95), ghi `version_log.csv` | Commit `7585738`, `8fd17b2`; PR #1, #2; run v0–v3 ở B1 |
| Le Viet Khoa | Test Owner (C) | CP2, CP4 | Vòng v1–v3 đối chứng trên nhánh riêng (rule `clarify` + xác nhận trước `send`; 0.70 / 0.80 / 0.80). Cùng xây bộ case eval nhóm | Commit `05451d7` trên nhánh `2A202603737-LeVietKhoa` |
| Do Thanh Mai | Eval Owner (B) | CP4, CP5 | 10 case `eval_group.json` (có case route tới `wiki`), chạy `--suite group` v3, điền B3. Live chat và hoàn thiện report Phần A + B | Commit `dddbe3e`; PR #4; [run group](../../starter_v0/runs/v3_B_group_openrouter_20261110T200053459021.json) |
| Ngo Chi Vinh | UI & Demo Owner (D) | CP3, CP5 | Tool `wiki`, đăng ký tool, 7 unit test. UI Streamlit `app.py` + `requirements.txt` cho link dùng thử | Commit `3bd209e`, `52a7026`, `a3b394b`, `24e4b54`, `95bb0f9`, `bd37ecb`; PR #3 |

Chi tiết đóng góp và bằng chứng của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

**Fix nào thuộc `system_prompt.md`?** Những hành vi áp dụng chung cho nhiều tool:
- khi nào hỏi lại thay vì đoán (v1);
- ranh giới xác nhận trước khi gửi ra kênh ngoài (v2);
- bỏ các chỉ dẫn xấu của starter.

Các rule này sửa được R10, R12, R13 và hai case out-of-scope R08, R14. Ở v0, model gọi `send` để trả lời cả những yêu cầu ngoài phạm vi.

**Fix nào thuộc `tools.yaml`?** Những gì gắn với một tool cụ thể: args nào bắt buộc, giá trị hợp lệ, ranh giới giữa các tool giống nhau. Bằng chứng rõ nhất:
- Rule "gọi `clarify`" trong prompt (v1, v2) không làm model điền `response_type`. Chỉ khi đặt `response_type` là required trong schema (v3), R11 mới pass.
- Lỗi lẫn `lookup` với `social_search` (M06) cũng chỉ hết sau khi viết lại description hai tool này.

**Failure nào cần review thủ công thay vì chấm tự động?**
- Phiên 1 turn 2: "bài viết này" khi đang có 5 bài trong ngữ cảnh. Agent chọn bài đầu tiên; cách chọn này có thể chấp nhận được hoặc không, chấm tự động không quyết định được.
- Phiên 2 turn 1 và turn 3: agent hỏi lại đúng nội dung nhưng bằng câu trả lời thường, không gọi `clarify`. Chấm tự động sẽ báo FAIL dù user vẫn nhận được hành vi đúng.
- Khi tool lỗi (403 Twitter): eval chỉ xem tool call, không biết câu trả lời có trung thực hay bịa nội dung.
- G03: `policy` được gọi mà thiếu `policy_area`. Chấm tự động báo FAIL, nhưng cần đọc kết quả để biết câu trả lời có thực sự sai không.
- Chất lượng bản tóm tắt sau `fetch` (có đúng nội dung bài không) chỉ người đọc mới đánh giá được.

**Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**

v4 (`tools.yaml`): viết lại declaration của `send`. Mô tả rõ: chỉ gọi sau khi user đã trả lời đồng ý cho `clarify` yes/no; khi gọi phải truyền `confirmed=true`; nếu chưa có xác nhận thì gọi `clarify`.
- Lý do: live chat phiên 1 turn 4 cho thấy user đã xác nhận nhưng model vẫn gọi `send` thiếu `confirmed`. Base eval không bắt được lỗi này, vì R12 chỉ kiểm tra bước `clarify`.
- Cách đo: thêm một case multi-turn "yêu cầu gửi → `clarify` yes/no → user đồng ý → `send(confirmed=true)`", rồi chạy lại base, group và chat live.

Các giả thuyết xếp hàng sau, mỗi version một giả thuyết:
- Thu hẹp rule `clarify`: chỉ hỏi khi user không nói của ai; đã nêu tên người/tổ chức nổi tiếng thì dùng handle chính thức (R01).
- Bỏ câu "Always finish the request in a single step. Pick one tool…" còn sót trong prompt.
- Viết description cho `policy_area` của `policy` (G03) và `sort_by` của `papers` (G04).

## 8. Tài liệu tham khảo

- Tài liệu lab: [README.md](../../README.md), [CHECKPOINTS.md](../../CHECKPOINTS.md), [RUBRIC.md](../../RUBRIC.md), [docs/TOOL-SETUP.md](../../docs/TOOL-SETUP.md), [starter_v0/tools/README.md](../../starter_v0/tools/README.md)
- MediaWiki Action API (dùng cho tool `wiki`): https://www.mediawiki.org/wiki/API:Main_page
- Streamlit: https://docs.streamlit.io
- Cloudflare Tunnel (quick tunnel): https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/
