# Báo cáo cá nhân — NgoChiVinh-2A202603724

## 1. Thông tin thành viên

- Họ tên: Ngo Chi Vinh
- MSSV: 2A202603724
- Email: chivinh251020@gmail.com
- GitHub: NgChiVinh
- Nhóm: forStartTeam (L3B)
- Vai trò: UI & Demo Owner (D)

## 2. Phần việc phụ trách

- **CP3 (tool mới và unit test):**
  - viết tool mới `wiki` của nhóm (sau khi thầy yêu cầu mỗi nhóm chỉ làm 1 tool, nhóm dùng tool này);
  - viết `TOOL.md`, đăng ký trong `tools/__init__.py` và `artifacts/tools.yaml`;
  - viết unit test cho `wiki` trong `tests/test_tools_todo.py`.
- **CP5 (UI và live chat):**
  - dựng UI Streamlit [`starter_v0/app.py`](../../starter_v0/app.py), thêm dependency vào `requirements.txt`;
  - mở link dùng thử qua Cloudflare Tunnel;
  - chạy `chat.py` ≥ 3 lượt live với v3 và lưu transcript.

## 3. Đóng góp cụ thể

### CP3 — Tool `wiki` và unit test

Tool [`starter_v0/tools/wiki/tool.py`](../../starter_v0/tools/wiki/tool.py) tra Wikipedia tiếng Việt hoặc tiếng Anh qua MediaWiki Action API (không cần API key), trả về `items[]` gồm `title`, `url`, `source`, `summary` cùng định dạng với `lookup`/`fetch`:

- input xấu từ model (`query` rỗng/`None`, `lang` ngoài `vi`/`en`) trả error dict **trước khi gọi mạng**;
- `limit` dạng chuỗi (`"3"`) hoặc ngoài khoảng (`0`, `99`) được đưa về 1–10;
- mọi lỗi (HTTP 429, lỗi API nằm trong response HTTP 200) trả `{tool, error, message}`, không raise;
- description trong `tools.yaml` ghi rõ khi nào dùng (định nghĩa, khái niệm, kiến thức nền) và khi nào **không** dùng (tin mới → `lookup`, URL cụ thể → `fetch`, paper → `papers`).

7 test function (9 test case tính cả parametrize), chạy offline bằng `fake_http`:

| Nhóm | Test |
|---|---|
| Happy path | gửi đúng URL/params/User-Agent, sắp xếp theo thứ hạng tìm kiếm, cắt summary ở 600 ký tự |
| Input xấu | query rỗng/`None`; `lang="fr"`; `limit` = `"3"`, `0`, `-5`, `99`, `"abc"` |
| Nhánh lỗi | HTTP 429; lỗi API trong response 200; không có kết quả (`items: []`, không coi là lỗi) |

Kết quả: `pytest` 76 passed, 17 skipped, 0 failed; contract test 60 passed. Trong run eval nhóm, 2 case route tới `wiki` (G01, G06) đều PASS.

### CP5 — UI và live chat

- UI dùng lại đúng vòng lặp agent của `chat.py` (`run_model_tool_loop`), nên một lượt trên UI giống một lượt trên CLI; mỗi phiên tự ghi transcript cùng schema với `chat.py`.
- Dưới mỗi câu trả lời hiển thị tool đã gọi, args và kết quả; tool lỗi hiện rõ, không bị che. Khi agent gọi `clarify`, câu hỏi hiện trong khung riêng, có nút Có/Không nếu là câu hỏi yes/no.
- Chế độ khoá `UI_LOCK=1` cho link public để người ngoài không đổi được model hoặc nhãn version.
- Chạy `chat.py --provider openrouter --version v3` 5 lượt live, đủ 3 loại lượt đề yêu cầu:

| Lượt | User | Tool | Kết quả |
|---|---|---|---|
| 1 | Tin tức AI hôm nay có gì nổi bật? | `lookup(topic=news, timeframe=day)` | 5 tin kèm nguồn |
| 2–3 | Tóm tắt 5 tweet mới nhất → Của Sam Altman | (hỏi lại) → `timeline(screenname=sama, limit=5)` | Hỏi lại thay vì đoán; args đúng, RapidAPI trả 403 |
| 4–5 | Đăng bản tin lên Telegram → Không | `clarify(response_type=yes_no)` | Xin xác nhận trước, không gọi `send` |

## 4. Bằng chứng

- **Commit / PR (nhánh `2A202603724_NgoChiVinh`):**
  - CP3: `3bd209e` (tool `wiki`), `52a7026` (đăng ký), `a3b394b`, `24e4b54` (unit test);
  - CP5: `95bb0f9` (UI Streamlit), `192207b` (transcript `chat.py` v3);
  - báo cáo: `0ab453a` (báo cáo cá nhân + mục của mình trong `TEAM.md`);
  - merge vào `develop` qua PR #3 và PR tiếp theo từ nhánh `2A202603724_NgoChiVinh`.
- **File:** [`tools/wiki/`](../../starter_v0/tools/wiki/), [`tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py) (mục `wiki`), [`app.py`](../../starter_v0/app.py), [`.streamlit/config.toml`](../../starter_v0/.streamlit/config.toml).
- **Eval:** [`runs/v3_B_group_openrouter_20261110T200053459021.json`](../../starter_v0/runs/v3_B_group_openrouter_20261110T200053459021.json) — `G01_wiki_english_article`, `G06_multiturn_wiki_language_and_limit` PASS.
- **Transcript:** [`transcripts/v3_openrouter_20261110T223818896136.transcript.json`](../../starter_v0/transcripts/v3_openrouter_20261110T223818896136.transcript.json).
- **Báo cáo nhóm:** bảng B5a (tool `wiki`, unit test, UI) trong [group_report.md](group_report.md).
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - Dùng trợ lý AI (Claude Code) để hỗ trợ viết code tool `wiki`, unit test, UI `app.py` và rà soát bài theo RUBRIC.
  - Cách tự kiểm tra:
    - chạy `pytest` (76 passed, 0 failed) và contract test sau mỗi thay đổi;
    - gọi thử `wiki` với Wikipedia thật (tiếng Việt, tiếng Anh, từ khoá vô nghĩa, input sai);
    - chạy thử UI với model thật và chụp màn hình để soát giao diện;
    - chạy thử eval case route tới `wiki` trước khi gửi nhóm;
    - đọc lại từng file trước khi commit. Tự giải thích được thiết kế tool và từng test.

## 5. Tự đánh giá

**Đã làm được:**
- Tool `wiki` đáp ứng đủ yêu cầu C4 (đúng contract, trả error dict thay vì raise, 7 test offline) và được model route đúng trong eval nhóm.
- UI hiển thị rõ tool nào được gọi, với args gì và kết quả ra sao, kể cả khi tool lỗi; transcript `chat.py` có đủ 3 loại lượt đề yêu cầu.

**Bài học rút ra:** eval đo việc model *chọn* tool và args, còn unit test đo *code* của tool, nên cần cả hai. Model không nhất quán việc có ghi tham số mặc định hay không (lúc có `lang="vi"`, lúc không), vì vậy eval case chỉ nên kiểm tra những args thật sự cần thiết.

**Hạn chế còn lại:**
1. Chưa làm bonus gửi Telegram thật.
2. Trong transcript, lượt 2 agent hỏi lại bằng text chứ không gọi tool `clarify`; lượt 3 `timeline` bị RapidAPI trả 403 nên chưa lấy được tweet thật.
3. Một số commit còn gộp nhiều thay đổi (ví dụ commit UI), có thể chia nhỏ hơn để dễ review.
