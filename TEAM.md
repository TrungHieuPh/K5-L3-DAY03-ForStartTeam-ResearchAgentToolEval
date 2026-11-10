# Team

## Thông tin nhóm

- Tên nhóm: forStartTeam
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-forStartTeam-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt: https://github.com/TrungHieuPh/K5-L3-DAY03-ForStartTeam-ResearchAgentToolEval — nhánh `develop`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Phan Trung Hieu | 2a202603763 | trinhphan982001@gmail.com | TrungHieuPh | Prompt Owner (A) |
|   2 | Do Thanh Mai |  |  | Laurent2526 | Eval Owner (B) |
|   3 | Le Viet Khoa |  |  | khoa-asta | Test Owner (C) |
|   4 | Ngo Chi Vinh |  |  | NgChiVinh | UI & Demo Owner (D) |

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

-

### Bằng chứng

- Run baseline: `starter_v0/runs/v0_B_base_openrouter_20261110T174832391453.json` (case_accuracy = 0.65)
- `starter_v0/artifacts/version_log.csv` dòng v0

## Do Thanh Mai — MSSV

### Phần việc phụ trách

- Vai trò B — Eval Owner
- Viết đủ 10 case vào `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn)
- Bảo đảm ≥ 1 case trỏ tới tool mới của mỗi thành viên
- Chạy `--suite group` với v3
- Điền bảng B3 (Team Eval Cases) trong `group_report.md`
- Tool mới của cá nhân: (ví dụ `translate`)

### Đóng góp cụ thể

-

### Bằng chứng

-

## Le Viet Khoa — MSSV

### Phần việc phụ trách

- Vai trò C — Test Owner
- Giữ `pytest` 0 failed sau mỗi lần merge PR
- Điền các stub `pytest.skip(TODO)` trong `tests/test_tools_todo.py`
- Điền bảng B5a (Required Evidence) trong `group_report.md`
- Tool mới của cá nhân: (ví dụ `summarize`)

### Đóng góp cụ thể

-

### Bằng chứng

-

## Ngo Chi Vinh — MSSV

### Phần việc phụ trách

- Vai trò D — UI & Demo Owner
- Dựng `app.py` (Streamlit) + thêm dependency vào `requirements.txt`
- Deploy qua Cloudflare Tunnel, lấy link dùng thử
- Chạy `chat.py` ≥ 3 lượt live, lưu `transcripts/*.transcript.json`
- Viết **Phần A** `group_report.md` trước 16:30 (Team showdown)
- Tool mới của cá nhân: (ví dụ `rss_feed`)

### Đóng góp cụ thể

-

### Bằng chứng

-
