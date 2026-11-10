# Báo cáo cá nhân — PhanTrungHieu-2a202603763

## 1. Thông tin thành viên

- Họ tên: Phan Trung Hieu
- MSSV: 2a202603763
- Email: trinhphan982001@gmail.com
- GitHub: TrungHieuPh
- Nhóm: forStartTeam (L3B)
- Vai trò: Prompt Owner (A)

## 2. Phần việc phụ trách

- **CP0 (khởi tạo repo + baseline v0, tương ứng CP1 trong [CHECKPOINTS.md](../../CHECKPOINTS.md)):**
  - tạo repo nhóm và nhánh `develop`, điền [TEAM.md](../../TEAM.md);
  - cấu hình provider OpenRouter (`openai/gpt-4o-mini`);
  - chạy base eval v0 khi chưa sửa artifact;
  - ghi dòng v0 vào `version_log.csv`.
- **CP2:**
  - sở hữu [system_prompt.md](../../starter_v0/artifacts/system_prompt.md) và [tools.yaml](../../starter_v0/artifacts/tools.yaml);
  - chạy 3 vòng tối ưu v1, v2, v3, mỗi vòng một giả thuyết;
  - ghi [version_log.csv](../../starter_v0/artifacts/version_log.csv).
- Điền bảng B1 (Version Evidence) và B2 (Failure Analysis) trong [group_report.md](group_report.md).

## 3. Đóng góp cụ thể

### CP0 — Baseline v0

Chạy base eval với prompt và tools gốc của starter: case_accuracy **0.65** (13/20 pass), 0 provider error, 20/20 case measured.

Có 7 case FAIL, mỗi case được gán loại lỗi trong B2:

| Loại lỗi | Case |
|---|---|
| `missing_info` | R10, R11 |
| `wrong_boundary` | R12 |
| `out_of_scope` | R08, R14 |
| `wrong_tool` | R03, R13 |

Nguyên nhân chính là các chỉ dẫn xấu trong prompt starter:
- "đừng hỏi lại, cứ đoán", dẫn tới việc tự chọn tài khoản `sama` và bịa URL;
- "muốn gửi thì gửi luôn", nên model gọi `send` không xác nhận, kể cả để trả lời câu hỏi ngoài phạm vi.

### CP2 — Vòng lặp v1 → v3

| Version | Artifact sửa | Giả thuyết | Case accuracy | Kết quả chính |
|---|---|---|---|---|
| v1 | `system_prompt.md` | Thiếu handle/URL thì gọi `clarify` thay vì đoán (thay đoạn "hãy đoán" của starter) | 0.65 → 0.80 | R03, R08, R13, R14 pass. R10/R11 đã gọi `clarify` nhưng bỏ trống `response_type`. M06 bị regression |
| v2 | `system_prompt.md` | Trước `send` phải gọi `clarify` với `response_type='yes_no'`; chỉ `send(confirmed=true)` sau khi user đồng ý | 0.80 → 0.90 | R12 và R10 pass |
| v3 | `tools.yaml` | Đặt `clarify.response_type` là required; viết lại description `clarify`, `lookup`, `social_search` (khi nào dùng / không dùng) | 0.90 → 0.95 | R11 và M06 pass. R01 bị regression |

Mỗi version chỉ đổi một artifact:
- v1, v2 chỉ đổi `prompt_hash`;
- v3 chỉ đổi `tools_hash`.

Cả 4 run đều hợp lệ: `provider_error_cases == 0`, `measured_cases == total_cases`.

`pytest tests/test_tool_contract.py` vẫn xanh sau khi sửa `tools.yaml`.

### Báo cáo nhóm

- **B1:** điền bảng version, metric (routing, argument, multiturn) và hash.
- **Hash run group:** tìm ra vì sao hash của run group khác `version_log.csv`. Nguyên nhân là ký tự xuống dòng CRLF trên máy chạy run, không phải nội dung artifact khác.
- **B2:** điền đủ 7 case FAIL của v0, cộng 2 case regression (M06, R01), lấy từ `results[*].result.failures` trong run JSON.

## 4. Bằng chứng

- **Commit / PR:**
  - `7585738` (feat: init repo V0): TEAM.md, dòng v0 trong `version_log.csv`, run v0;
  - `8fd17b2` (feat: update cp2): sửa `system_prompt.md` và `tools.yaml`, 3 dòng v1–v3 trong `version_log.csv`, 3 run v1–v3;
  - merge vào `develop` qua PR #1 và PR #2 từ nhánh `phantrunghieu-2a202603763`.
- **Run:**
  - [v0](../../starter_v0/runs/v0_B_base_openrouter_20261110T174832391453.json): 0.65
  - [v1](../../starter_v0/runs/v1_B_base_openrouter_20261110T185604978621.json): 0.80
  - [v2](../../starter_v0/runs/v2_B_base_openrouter_20261110T190314163382.json): 0.90
  - [v3](../../starter_v0/runs/v3_B_base_openrouter_20261110T191727001530.json): 0.95
- **Version log:** [version_log.csv](../../starter_v0/artifacts/version_log.csv), dòng v0–v3, có hash, giả thuyết, metric trước/sau.
- **Báo cáo:** bảng B1, B2 và mục 7 (Reflection) trong [group_report.md](group_report.md).
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - Dùng Claude Code (VS Code extension) để:
    - đối chiếu bài làm với CHECKPOINTS.md;
    - đọc run JSON khi điền B1/B2;
    - tìm nguyên nhân lệch hash;
    - soạn nháp nội dung báo cáo.
  - Cách tự kiểm tra:
    - So từng số trong B1 với `summary` của file run tương ứng.
    - So từng dòng B2 với `case_failure_type`, `observed_mismatch` và `actual_tool_calls` trong run JSON.
    - Tính lại hash bằng `versioning.py` và so với `version_log.csv`; chuyển file sang CRLF thì ra đúng hash của run group.
    - Chạy lại `pytest`: 76 passed, 17 skipped, 0 failed; contract test 60 passed.

## 5. Tự đánh giá

**Đã làm được:**
- Baseline và 3 version đều có run hợp lệ, mỗi version một giả thuyết, metric tăng từ 0.65 lên 0.95.
- Mỗi case FAIL đều có loại lỗi và nguyên nhân dẫn từ run JSON.

**Bài học rút ra:** có lỗi sửa bằng prompt không ăn thua, phải chuyển sang schema. Ở v1 và v2, rule "gọi `clarify`" trong prompt không làm model điền `response_type`. Chỉ khi đặt `response_type` là required trong `tools.yaml` (v3) thì R11 mới pass. Từ đó:
- hành vi chung cho nhiều tool (khi nào hỏi lại, ranh giới gửi) nên đặt ở system prompt;
- ràng buộc của từng tool (args bắt buộc, phân biệt các tool giống nhau) nên đặt trong tool declaration.

**Hạn chế còn lại:**
1. Prompt vẫn còn dòng chỉ dẫn xấu của starter: "Always finish the request in a single step. Pick one tool…". Dòng này mâu thuẫn với rule hỏi lại và xác nhận trước khi gửi.
2. Mới viết lại description cho 3 tool (`clarify`, `lookup`, `social_search`). Các tool `timeline`, `fetch`, `format`, `send`, `policy`, `papers`, `paper_text` vẫn để description của starter. Riêng `send` có tham số `confirmed` chỉ mô tả là "Cờ xác nhận". Khi chat live, sau khi user đồng ý, model gọi `send` mà không có `confirmed=true` (B4, phiên 1, turn 4).
3. Regression R01 ở v3 chưa sửa: rule `clarify` áp dụng quá rộng, user đã nêu tên Sam Altman mà model vẫn hỏi handle.
4. Cả v1, v2, v3 nằm chung một commit (`8fd17b2`). Từng version vẫn truy được qua run và `version_log.csv`, nhưng commit riêng cho mỗi version sẽ dễ review hơn.

**Hướng làm tiếp (v4):** mỗi mục dưới đây là một giả thuyết, đo riêng từng cái:
- viết lại khai báo `send`, nói rõ chỉ đặt `confirmed=true` sau khi user trả lời đồng ý, kèm eval case multi-turn cho luồng này;
- thu hẹp rule `clarify` để sửa R01;
- xoá dòng "single step" còn sót trong prompt.
