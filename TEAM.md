# Team

## Thông tin nhóm

- Tên nhóm: forStartTeam
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-forStartTeam-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/TrungHieuPh/K5-L3-DAY03-ForStartTeam-ResearchAgentToolEval — nhánh `develop`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Phan Trung Hieu | 2a202603763 | 26ai.hieupt3@vinuni.edu.vn | TrungHieuPh | Prompt Owner (A) |
|   2 | Do Thanh Mai | 2A202603862 | 26ai.maidt@vinuni.edu.vn | Laurent2526 | Eval Owner (B) |
|   3 | Le Viet Khoa | 2A202603737 | 26ai.khoalv2@vinuni.edu.vn | khoa-asta | Test Owner (C) |
|   4 | Ngo Chi Vinh | 2A202603724 | 26ai.vinhnc2@vinuni.edu.vn | NgChiVinh | UI & Demo Owner (D) |

### Tóm tắt đóng góp theo checkpoint

| Thành viên | Checkpoint | Bằng chứng chính |
| ---------- | ---------- | ---------------- |
| Phan Trung Hieu | CP0 (khởi tạo repo + baseline v0), CP2 | Commit `7585738`, `8fd17b2`; PR #1, #2 |
| Le Viet Khoa | CP2, CP4 | Commit `05451d7` trên nhánh `2A202603737-LeVietKhoa` |
| Do Thanh Mai | CP4, CP5 | Commit `dddbe3e`; PR #4 |
| Ngo Chi Vinh | CP3, CP5 | Commit `3bd209e`, `52a7026`, `a3b394b`, `24e4b54`, `95bb0f9`, `bd37ecb`; PR #3 |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## Phan Trung Hieu — 2a202603763

### Phần việc phụ trách

- Vai trò A — Prompt Owner
- Sở hữu `starter_v0/artifacts/system_prompt.md` + `starter_v0/artifacts/tools.yaml`
- Chạy baseline `v0` và 3 vòng tối ưu `v1`, `v2`, `v3`
- Điền `starter_v0/artifacts/version_log.csv`
- Điền bảng B1 (Version Evidence), B2 (Failure Analysis) trong `report/team/group_report.md`
- Tool mới của cá nhân: (chọn tên, ví dụ `extract_entities`)

### Đóng góp cụ thể

- **CP0 (khởi tạo repo + baseline v0, tương ứng CP1 trong CHECKPOINTS.md):** tạo repo nhóm và nhánh `develop`, điền TEAM.md, cấu hình `.env` với provider OpenRouter, chạy base eval v0 khi chưa sửa artifact (case_accuracy 0.65), ghi dòng v0 vào `version_log.csv`.
- **CP2:** tối ưu qua 3 version, mỗi version một giả thuyết:
  - v1 (`system_prompt.md`): thiếu handle/URL thì gọi `clarify`, 0.65 → 0.80;
  - v2 (`system_prompt.md`): ranh giới xác nhận trước `send`, 0.80 → 0.90;
  - v3 (`tools.yaml`): `clarify.response_type` là required, viết lại description `lookup`/`social_search`, 0.90 → 0.95.
- Ghi các dòng v1–v3 (hash, giả thuyết, metric trước/sau) vào `version_log.csv`.

### Bằng chứng

- Commit `7585738` (feat: init repo V0), `8fd17b2` (feat: update cp2); PR #1, #2 từ nhánh `phantrunghieu-2a202603763`
- Run baseline: `starter_v0/runs/v0_B_base_openrouter_20261110T174832391453.json` (case_accuracy = 0.65)
- Run v1–v3: `starter_v0/runs/v1_B_base_openrouter_20261110T185604978621.json`, `v2_B_base_openrouter_20261110T190314163382.json`, `v3_B_base_openrouter_20261110T191727001530.json`
- `starter_v0/artifacts/version_log.csv` dòng v0–v3

## Do Thanh Mai — 2A202603862

### Phần việc phụ trách

- Vai trò B — Eval Owner
- Viết đủ 10 case vào `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn)
- Bảo đảm ≥ 1 case trỏ tới tool mới của mỗi thành viên
- Chạy `--suite group` với v3
- Điền bảng B3 (Team Eval Cases) trong `group_report.md`
- Tool mới của cá nhân: (ví dụ `translate`)

### Đóng góp cụ thể

- **CP4:** viết 10 case vào `starter_v0/data/eval_group.json` (5 single turn `query`, 5 multi turn `turns`), có case G01 và G06 kiểm tra route tới tool mới `wiki`. Chạy `--suite group` với v3 (10/10 case measured, 0 provider error, case_accuracy 0.80). Điền bảng B3 trong group report.
- **CP5:** chạy live chat `chat.py` và hoàn thiện group report Phần A + B.

### Bằng chứng

- Commit `dddbe3e` (feat: update cp4); PR #4 từ nhánh `dothanhmai-2A202603862`
- `starter_v0/data/eval_group.json`
- Run group: `starter_v0/runs/v3_B_group_openrouter_20261110T200053459021.json`
- Bảng B3 trong `report/team/group_report.md`
- Transcript live chat: `starter_v0/transcripts/v3_openrouter_20261110T215803737613.transcript.json`, `v3_openrouter_20261110T220316474371.transcript.json`

## Le Viet Khoa — 2A202603737

### Phần việc phụ trách

- Vai trò C — Test Owner
- Giữ `pytest` 0 failed sau mỗi lần merge PR
- Điền các stub `pytest.skip(TODO)` trong `tests/test_tools_todo.py`
- Điền bảng B5a (Required Evidence) trong `group_report.md`
- Tool mới của cá nhân: (ví dụ `summarize`)

### Đóng góp cụ thể

- **CP2:** chạy một vòng tối ưu v1–v3 độc lập trên nhánh riêng để đối chứng. Viết rule `clarify` (thiếu account/URL thì hỏi lại, không bịa) và rule xác nhận `yes_no` trước `send` trong `system_prompt.md`, ghi 3 dòng vào `version_log.csv`. Kết quả: v1 0.70, v2 0.80, v3 0.80 (v3 chạy lại cùng hash với v2). Bộ v1–v3 nộp chính thức trên `develop` là bộ của Hieu.
- **CP4:** cùng Mai xây dựng bộ case eval nhóm.

### Bằng chứng

- Commit `05451d7` (Record CP2 prompt changes and v1-v3 evaluation evidence) trên nhánh `2A202603737-LeVietKhoa`, chưa merge vào `develop`
- Run trên nhánh đó: `v1_B_base_openrouter_20261110T190214407873.json`, `v2_B_base_openrouter_20261110T190628210275.json`, `v3_B_base_openrouter_20261110T191107323297.json` (0 provider error, 20/20 case measured)

## Ngo Chi Vinh — 2A202603724

### Phần việc phụ trách

- Vai trò D — UI & Demo Owner
- Dựng `app.py` (Streamlit) + thêm dependency vào `requirements.txt`
- Deploy qua Cloudflare Tunnel, lấy link dùng thử
- Chạy `chat.py` ≥ 3 lượt live, lưu `transcripts/*.transcript.json`
- Viết **Phần A** `group_report.md` trước 16:30 (Team showdown)
- Tool mới của cá nhân: `wiki` (tool mới duy nhất của nhóm)

### Đóng góp cụ thể

- **CP3:** viết tool mới `wiki` (`starter_v0/tools/wiki/tool.py` + `TOOL.md`) tra cứu Wikipedia vi/en qua MediaWiki API. Lỗi được trả về dạng error dict, không raise. Đăng ký tool trong `tools/__init__.py` (`TOOL_FUNCTIONS`) và `artifacts/tools.yaml`. Viết 7 test (9 test item) trong `tests/test_tools_todo.py` cho happy path, input xấu từ model và nhánh lỗi. `pytest`: 0 failed.
- **CP5:** dựng UI Streamlit `starter_v0/app.py`, gồm hiển thị tool route, nút trả lời nhanh cho `clarify` và chế độ khóa demo `UI_LOCK`. Thêm `.streamlit/config.toml` và dependency vào `requirements.txt`. UI này dùng cho link dùng thử ở Phần A.

### Bằng chứng

- Commit `3bd209e`, `52a7026` (tool `wiki` + đăng ký), `a3b394b`, `24e4b54` (unit test), `95bb0f9` (UI Streamlit), `bd37ecb` (transcript UI); PR #3 từ nhánh `2A202603724_NgoChiVinh`
- `starter_v0/tools/wiki/`, `starter_v0/tests/test_tools_todo.py`, `starter_v0/app.py`
- Bảng B5a trong `report/team/group_report.md`
