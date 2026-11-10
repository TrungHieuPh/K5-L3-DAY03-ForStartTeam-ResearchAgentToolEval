# Báo cáo cá nhân — NgoChiVinh-2A202603724

## 1. Thông tin thành viên

- Họ tên: Ngô Chí Vinh
- MSSV: 2A202603724
- Email: chivinh251020@gmail.com

## 2. Phần việc phụ trách

- Viết tool mới `wiki` của nhóm (code, `TOOL.md`, đăng ký, unit test).
- Làm UI Streamlit `starter_v0/app.py` để chạy thử agent.
- Chạy `chat.py` ≥ 3 lượt live và lưu transcript.

## 3. Đóng góp cụ thể

- **Tool `wiki`** (`starter_v0/tools/wiki/`): tra Wikipedia tiếng Việt/tiếng Anh, trả về đoạn tóm tắt mở đầu kèm link. Input xấu (`query` rỗng, `lang` ngoài `vi`/`en`) trả error dict mà không gọi mạng; `limit` dạng chuỗi hoặc ngoài khoảng được đưa về 1–10; mọi lỗi API trả error dict, không raise. Đăng ký trong `tools/__init__.py` và khai báo trong `artifacts/tools.yaml` (ghi rõ khi nào dùng / không dùng).
- **Unit test** (`starter_v0/tests/test_tools_todo.py`, mục `wiki`): 7 test chạy offline — 1 happy path, 3 input xấu (query rỗng, lang sai, limit sai kiểu/ngoài khoảng), 3 nhánh lỗi (HTTP 429, lỗi API trong response 200, không có kết quả).
- **UI** (`starter_v0/app.py`): dùng lại vòng lặp agent của `chat.py`, hiển thị tool được gọi, args, kết quả và lỗi tool; thêm `streamlit` vào `requirements.txt`.

## 4. Bằng chứng

- File/commit/PR:
  - `3bd209e` feat(tool): add wiki tool (Wikipedia search + intro summary)
  - `52a7026` feat(tool): register wiki in TOOL_FUNCTIONS and tools.yaml
  - `a3b394b` test(wiki): add 5 unit tests (happy path, bad input, error paths)
  - `24e4b54` test(wiki): one behaviour per test; mark wiki as bonus track
  - `95bb0f9` feat(ui): add Streamlit app with tool route view, clarify quick replies and demo lock
  - PR #3 `2A202603724_NgoChiVinh` → `develop`
  - `pytest`: 76 passed, 0 failed
  - Eval route tới `wiki` trong `starter_v0/runs/v3_B_group_openrouter_20261110T200053459021.json`: `G01_wiki_english_article` PASS, `G06_multiturn_wiki_language_and_limit` PASS
  - Transcript `chat.py` (v3, 5 lượt): `starter_v0/transcripts/v3_openrouter_20261110T223818896136.transcript.json` — commit `192207b`
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: dùng trợ lý AI (Claude Code) để hỗ trợ viết code tool `wiki`, unit test, UI `app.py` và rà soát bài theo RUBRIC. Tự kiểm tra bằng cách: chạy `pytest` (76 passed, 0 failed); gọi thử `wiki` với Wikipedia thật; chạy thử UI với model thật; chạy thử eval case route tới `wiki` trước khi gửi nhóm; đọc lại từng file trước khi commit. Tự giải thích được thiết kế của tool và từng test.

## 5. Tự đánh giá

- **Làm tốt:** tool `wiki` đáp ứng đủ yêu cầu C4 (đúng contract, trả error dict thay vì raise, 7 test chạy offline) và được model route đúng trong eval nhóm (G01, G06 PASS). UI hiển thị rõ tool nào được gọi, với args gì và kết quả ra sao, kể cả khi tool lỗi.
- **Chưa tốt:** chưa kịp làm bonus gửi Telegram thật; một số commit còn gộp nhiều thay đổi, có thể chia nhỏ hơn; transcript `chat.py` chạy muộn vì phải chờ prompt v3.
- **Học được:** eval đo việc model *chọn* tool và args, còn unit test đo *code* của tool, nên cần cả hai. Model không nhất quán việc có ghi tham số mặc định hay không, vì vậy eval case chỉ nên kiểm tra những args thật sự cần thiết.
