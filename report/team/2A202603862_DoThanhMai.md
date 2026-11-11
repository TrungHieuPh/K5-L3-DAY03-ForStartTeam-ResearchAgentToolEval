# Báo cáo cá nhân — Đỗ Thanh Mai-2A202603862

## 1. Thông tin thành viên

- Họ tên: Đỗ Thanh Mai
- MSSV: 2A202603862
- Email: 26ai.maidt@vinuini.edu.vn
- GitHub: Laurent2526
- Nhóm: forStartTeam (L3B)
- Vai trò: Eval Owner (B)

## 2. Phần việc phụ trách

- **CP4:**
  - viết đủ 10 case vào `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn);
  - đảm bảo có ít nhất 1 case trỏ tới tool mới của mỗi thành viên;
  - chạy `--suite group` với version v3;
  - điền bảng B3 (Team Eval Cases) trong [group_report.md](group_report.md).
- **CP5:**
  - chạy live chat `chat.py` để kiểm tra hành vi người dùng thực tế;
  - hoàn thiện phần A + B của báo cáo nhóm.
- Tool mới của cá nhân: `wiki` (được nhóm viết và đăng ký trong toolchain), đồng thời đảm bảo có case đánh giá route tới tool này.

## 3. Đóng góp cụ thể

### CP4 — Viết bộ case eval nhóm

Tôi chịu trách nhiệm tạo bộ đánh giá nhóm trong `starter_v0/data/eval_group.json` với tổng cộng 10 case, gồm:
- 5 case single turn;
- 5 case multi turn;
- có ít nhất 2 case kiểm tra route tới tool mới `wiki` của nhóm: G01 và G06.

Bộ case này được thiết kế để đánh giá:
- phân biệt giữa kiến thức nền (`wiki`) và tin tức mới (`lookup`);
- xác định đúng khi agent nên dùng `policy`, `papers`, `social_search` và `lookup`;
- kiểm tra khả năng giữ context trong multi-turn conversation.

Kết quả chạy `--suite group` với version v3:
- 10/10 case measured;
- 0 provider error;
- `case_accuracy = 0.80`.

Tôi cũng tham gia điền bảng B3 (Team Eval Cases) trong [group_report.md](group_report.md), dựa trên `results[*].result.failures` và `summary` từ run JSON thực tế.

### CP5 — Live chat và hoàn thiện báo cáo

Sau khi bộ case nhóm hoàn thành, tôi tiếp tục chạy các phiên live chat bằng `chat.py` để kiểm tra xem agent hoạt động ổn trong luồng tương tác thực tế, không chỉ trên test case tĩnh.

Trong quá trình này, tôi hỗ trợ:
- kiểm tra agent có gọi đúng tool khi người dùng hỏi tin tức, kiến thức nền, hay cần xác nhận trước khi gửi;
- đối chiếu transcript thực tế với yêu cầu của báo cáo nhóm;
- nộp phần A + B của báo cáo nhóm cho đúng cấu trúc và bằng chứng thực tế.

## 4. Bằng chứng

- **Commit / PR:**
  - `dddbe3e` — feat: update cp4
  - PR #4 từ nhánh `dothanhmai-2A202603862`
- **File chính:**
  - `starter_v0/data/eval_group.json`
  - `report/team/group_report.md`
  - `starter_v0/runs/v3_B_group_openrouter_20261110T200053459021.json`
  - `starter_v0/transcripts/v3_openrouter_20261110T215803737613.transcript.json`
  - `starter_v0/transcripts/v3_openrouter_20261110T220316474371.transcript.json`
- **Kết quả run group:**
  - `case_accuracy = 0.80`
  - `measured_cases = 10`
  - `provider_error_cases = 0`
- **Bảng đánh giá nhóm:** B3 trong [group_report.md](group_report.md)
- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  - Dùng VS Code / Claude Code để đọc run JSON và transcript, đối chiếu với `eval_group.json` và requirement của nhóm.
  - Cách tự kiểm tra:
    - so khớp từng case trong file JSON với `expected_tool`/`expected_behavior`;
    - so sánh kết quả thực tế trong run JSON với `summary` và `results[*].result.failures`;
    - kiểm tra transcript live có đúng tool call, đúng context và đúng flow xác nhận trước khi gửi.

## 5. Tự đánh giá

**Đã làm được:**
- Hoàn thành bộ case eval nhóm với 10 case phù hợp yêu cầu của checkpoint CP4.
- Đảm bảo có case kiểm tra `wiki`, tool mới của nhóm, và route đúng tool.
- Chạy suite group với version v3 thành công: 10/10 case measured, 0 provider error, case_accuracy 0.80.
- Tham gia hoàn thiện báo cáo nhóm và kiểm tra transcript live trên chat thực tế.

**Bài học rút ra:**
- Đối với eval suite, cần thiết kế cả case single-turn và multi-turn để đo đúng khả năng nhớ context và tool routing.
- Cần giữ ít nhất 1 case cho từng tool mới, để đảm bảo tool mới không bị bỏ sót trong benchmark.
- Live chat giúp phát hiện các lỗi mà test case static chưa bắt hết, đặc biệt là luồng xác nhận trước khi `send`.

**Hạn chế còn lại:**
1. Một số case trong nhóm vẫn có mức độ khó và phụ thuộc vào prompt/tool description; do đó, metrics của bộ nhóm chỉ đạt 0.80, chưa đạt mức hoàn hảo.
2. Extension của `wiki` và route logic cần tiếp tục cải thiện nếu muốn tối ưu cho các case dạng “người dùng đã nói tên nhân vật/tổ chức nhưng không đưa handle/URL”.

**Hướng làm tiếp:**
- Tăng độ chắc chắn của các case trong `eval_group.json` cho route tool và multi-turn context.
- Cộng thêm case kiểm tra `clarify`/`yes_no` trong luồng send xác nhận, vì đây là phần rất nhạy với hành vi live.
- Tiếp tục luyện tập với transcript thực tế để tinh chỉnh prompt và tool description cho bản v4 sau này.
