# Báo cáo cá nhân — LeVietKhoa-2a202603737

## 1. Thông tin thành viên

- Họ tên: Lê Viết Khoa
- MSSV: 2a202603737
- Email: levietkhoa2002@gmail.com
- GitHub: khoa-asta
- Nhóm: forStartTeam (L3B)
- Vai trò theo phân công: Test Owner (C); tham gia thực nghiệm tối ưu prompt và cùng Đỗ Thanh Mai xây dựng bộ eval nhóm.
- Phạm vi báo cáo: CP2 và CP4.

## 2. Phần việc phụ trách

### CP2 — Thực nghiệm prompt và ghi nhận kết quả

- Thực hiện chuỗi chạy base eval v1–v3 trên nhánh cá nhân với OpenRouter, model `openai/gpt-4o-mini`.
- Bổ sung quy tắc hỏi lại khi thiếu tài khoản/URL và quy tắc xác nhận trước khi gửi trong `artifacts/system_prompt.md`.
- Đọc `summary`, `actual_tool_calls`, `observed_mismatch` và `failures` để đánh giá thay đổi.
- Ghi version log cá nhân gồm hash, giả thuyết, metric trước/sau và đường dẫn run.
- Kiểm tra contract test và lưu bằng chứng trong commit `05451d7`.

### CP4 — Cùng xây dựng bộ eval nhóm

- Cùng Đỗ Thanh Mai xây dựng bộ 10 case trong [eval_group.json](../../starter_v0/data/eval_group.json), theo yêu cầu CP4 của [CHECKPOINTS.md](../../CHECKPOINTS.md).
- Thiết kế 5 case single turn dùng `query` và 5 case multi turn dùng `turns`, kiểm tra lựa chọn tool, arguments và khả năng giữ ngữ cảnh.
- Xác định kết quả mong đợi trong `expect`, loại lỗi cần kiểm tra trong `failure_type` và mục đích của từng case trong `metadata.what_it_tests`.
- Bổ sung tình huống gọi tool mới `wiki`, phân biệt tra cứu kiến thức nền với tin tức và kiểm tra trường hợp không cần gọi tool.

Đây là phần việc phối hợp của tôi và Mai. Mai phụ trách tổng hợp bộ case, chạy group eval và điền bảng B3; phần đóng góp của tôi là cùng xây dựng nội dung bộ case, như ghi nhận trong [TEAM.md](../../TEAM.md).

## 3. Đóng góp cụ thể

### 3.1. CP2 — Các lần chạy v1–v3 cá nhân

Lệnh chạy sử dụng bộ base cố định; thay nhãn version tương ứng:

```powershell
python run_eval.py --provider openrouter --version v1 --suite base --eval-cases data/eval_base.json
```

| Version | Giả thuyết hoặc mục đích | Thay đổi/bằng chứng artifact | Case accuracy | Kết quả quan sát |
| --- | --- | --- | --- | --- |
| v1 | Thêm quy tắc hỏi lại khi thiếu tài khoản/URL sẽ giảm việc tự đoán | Có thay đổi prompt; cả `prompt_hash` và `tools_hash` khác v0 nên chưa thể khẳng định đây là thí nghiệm chỉ đổi một nội dung | 65% → 70% | R10 và R11 vẫn FAIL; điểm tổng tăng chưa chứng minh giả thuyết hỏi lại có hiệu quả |
| v2 | Thay chỉ dẫn gửi ngay bằng quy trình xác nhận sẽ cải thiện boundary của `send` | Chỉ `prompt_hash` khác v1 | 70% → 80% | R12 chuyển sang `clarify`, nhưng dùng `response_type="text"` thay vì `"yes_no"`, nên vẫn FAIL |
| v3 | Chạy lại cấu hình sau v2 | Cả hai hash giống v2 | 80% → 80% | Không có thay đổi artifact; đây là lần chạy lặp lại, chưa phải vòng cải tiến mới |

Các giả thuyết trong version log được bổ sung sau run dựa trên nội dung trao đổi và kế hoạch thực hiện; chưa phải bản ghi giả thuyết được lưu trước mỗi thí nghiệm.

| Version | PASS / tổng case | Routing accuracy | Argument accuracy | Multiturn accuracy | Provider error cases |
| --- | ---: | ---: | ---: | ---: | ---: |
| v0 — baseline chung | 13/20 | 70% | 65% | 100% | 0 |
| v1 — cá nhân | 14/20 | 75% | 70% | 100% | 0 |
| v2 — cá nhân | 16/20 | 95% | 80% | 100% | 0 |
| v3 — cá nhân | 16/20 | 95% | 80% | 100% | 0 |

Cả bốn run đều có `measured_cases == total_cases == 20`. Điều này cho phép đối chiếu kết quả eval; không đồng nghĩa mọi API của tool đều thực thi thành công.

### 3.2. Phân tích kết quả và kiểm tra hash

Ở v2 và v3, bốn case còn FAIL là:

- **R03:** `query` là `"AI news"` thay vì `"AI"`.
- **R10:** vẫn gọi `timeline` thay vì `clarify` khi thiếu tài khoản.
- **R12:** đã chọn `clarify` nhưng sai `response_type`.
- **R13:** `query` chưa đúng kỳ vọng và thiếu `topic="news"` trong lời gọi được chấm.

Hash rút gọn để đối chiếu nhanh; giá trị đầy đủ nằm trong từng Run JSON và version log tại commit cá nhân:

| Version | `prompt_hash` — 12 ký tự đầu | `tools_hash` — 12 ký tự đầu |
| --- | --- | --- |
| v0 | `f0c107a9d7a1` | `41a2894f8ad1` |
| v1 | `eb1c8179815b` | `e69bc53ed884` |
| v2 | `45677a81dbd6` | `e69bc53ed884` |
| v3 | `45677a81dbd6` | `e69bc53ed884` |

Chỉ đổi nhãn `--version` không tạo ra một cải tiến mới. Hai hash giống nhau ở v2/v3 cho thấy prompt và tool declaration không đổi. Với v1, hash của cả hai file đổi nhưng không có snapshot v1 đầy đủ để khẳng định phần nội dung nào đã thay đổi; khác hash cũng có thể liên quan định dạng file.

### 3.3. Kiểm tra contract và lưu bằng chứng

Trong phiên làm CP2, trợ lý AI đã hỗ trợ chạy:

```powershell
python -m pytest tests/test_tool_contract.py -q
```

Kết quả tại thời điểm đó là **55 passed, 0 failed**, kèm một cảnh báo không tạo được pytest cache. Đây là kết quả của trạng thái repo trong phiên CP2 cá nhân, không phải số lượng test của bản nhóm sau khi thêm tool mới.

### 3.4. CP4 — Thiết kế case eval cùng Đỗ Thanh Mai

Tôi cùng Mai xây dựng bộ eval để kiểm tra những tình huống nhóm quan tâm ngoài bộ base, gồm routing tới tool mới, lựa chọn arguments, yêu cầu không cần tool và giữ ngữ cảnh qua nhiều lượt. Bộ case là sản phẩm chung; bảng dưới mô tả nội dung đã cùng xây dựng, không phân chia quyền tác giả riêng cho từng case.

File `eval_group.json` có đúng **10 case: 5 single turn (G01–G05) và 5 multi turn (G06–G10)**. Tất cả case có `phase="B"`, `id`, `failure_type`, `expect` và `metadata.what_it_tests`.

| Case | Loại | Nội dung kiểm tra và kỳ vọng chính |
| --- | --- | --- |
| G01 — `wiki_english_article` | Single turn | Tra Wikipedia bài Quantum computing: gọi `wiki` với `lang="en"`, `limit=2` và đúng query |
| G02 — `recent_news_uses_lookup` | Single turn | Tin OpenAI hôm nay: gọi `lookup` với `topic="news"`, `timeframe="day"`; phân biệt với kiến thức bách khoa |
| G03 — `internal_citation_policy` | Single turn | Tra quy định trích dẫn nội bộ: gọi `policy` với `policy_area="source_citation"` |
| G04 — `arxiv_sort_by_submission` | Single turn | Tìm paper mới nộp về retrieval-augmented generation: gọi `papers` với `sort_by="submittedDate"` |
| G05 — `non_research_no_tool` | Single turn | Viết lời chúc sinh nhật không cần tra cứu: `expect.no_tool=true` |
| G06 — `multiturn_wiki_language_and_limit` | Multi turn | Giữ tên bài Quantum computing từ lượt trước, bổ sung `lang="en"` và `limit=2` ở lượt sau |
| G07 — `multiturn_policy_area_and_limit` | Multi turn | Giữ yêu cầu tra chính sách, áp dụng `policy_area="data_privacy"` và `top_k=2` |
| G08 — `multiturn_papers_sort` | Multi turn | Giữ chủ đề graph neural networks, chuyển yêu cầu bài mới nộp thành `sort_by="submittedDate"` |
| G09 — `multiturn_social_search_refinement` | Multi turn | Giữ query AI agents, áp dụng `search_type="Top"` và `limit=3` |
| G10 — `multiturn_lookup_timeframe` | Multi turn | Giữ chủ đề EU AI Act và giới hạn tin trong tuần bằng `topic="news"`, `timeframe="week"` |

G01 và G06 đáp ứng yêu cầu có case kiểm tra model route tới tool mới `wiki`. Trong `expect.tool_calls`, bộ case chỉ yêu cầu các arguments cần chấm; ví dụ G03 tập trung vào `policy_area`, không cố định chuỗi query do model diễn đạt.

**Kết quả chạy bộ case chung:** theo [run group v3](../../starter_v0/runs/v3_B_group_openrouter_20261110T200053459021.json) do Mai thực hiện, 10/10 case được đo và không có lỗi provider.

| Chỉ số group eval | Giá trị |
| --- | ---: |
| Case PASS | 8/10 |
| Case accuracy | 80% |
| Tool routing accuracy | 100% |
| Argument accuracy | 80% |
| Multiturn accuracy | 100% |
| Provider error cases | 0 |

Hai lỗi còn lại đều liên quan arguments:

- **G03:** model chọn đúng `policy` nhưng không truyền `policy_area="source_citation"`.
- **G04:** model chọn đúng `papers` nhưng dùng `sort_by="lastUpdatedDate"` thay vì `"submittedDate"`.

Kết quả cho thấy chọn đúng tool chưa đủ để case PASS; cần kiểm tra các arguments quyết định phạm vi và thứ tự kết quả. Đây là kết quả của bộ eval chung, tách biệt với chuỗi base eval cá nhân ở phần CP2 bên trên.

## 4. Bằng chứng

### File, commit và nhánh cá nhân

- Nhánh thực nghiệm: `2A202603737-LeVietKhoa`.
- [Commit 05451d7 — Record CP2 prompt changes and v1-v3 evaluation evidence](https://github.com/TrungHieuPh/K5-L3-DAY03-ForStartTeam-ResearchAgentToolEval/commit/05451d7cf57976d3ceb5592abd547a32c5429790).
- [System prompt tại commit cá nhân](https://github.com/TrungHieuPh/K5-L3-DAY03-ForStartTeam-ResearchAgentToolEval/blob/05451d7cf57976d3ceb5592abd547a32c5429790/starter_v0/artifacts/system_prompt.md).
- [Version log cá nhân tại commit 05451d7](https://github.com/TrungHieuPh/K5-L3-DAY03-ForStartTeam-ResearchAgentToolEval/blob/05451d7cf57976d3ceb5592abd547a32c5429790/starter_v0/artifacts/version_log.csv).
- [Run v1 cá nhân — 70%](https://github.com/TrungHieuPh/K5-L3-DAY03-ForStartTeam-ResearchAgentToolEval/blob/05451d7cf57976d3ceb5592abd547a32c5429790/starter_v0/runs/v1_B_base_openrouter_20261110T190214407873.json).
- [Run v2 cá nhân — 80%](https://github.com/TrungHieuPh/K5-L3-DAY03-ForStartTeam-ResearchAgentToolEval/blob/05451d7cf57976d3ceb5592abd547a32c5429790/starter_v0/runs/v2_B_base_openrouter_20261110T190628210275.json).
- [Run v3 cá nhân — 80%](https://github.com/TrungHieuPh/K5-L3-DAY03-ForStartTeam-ResearchAgentToolEval/blob/05451d7cf57976d3ceb5592abd547a32c5429790/starter_v0/runs/v3_B_base_openrouter_20261110T191107323297.json).

Các liên kết được cố định theo commit vì `version_log.csv` ở bản nhóm hiện chứa bộ run của Hiếu với kết quả 80% → 90% → 95%. Bộ số liệu đó không phải kết quả thực nghiệm cá nhân trong báo cáo này.

### Bằng chứng CP4 — Bộ case phối hợp cùng Mai

- [eval_group.json](../../starter_v0/data/eval_group.json): bộ 10 case đã cùng xây dựng, gồm 5 single turn và 5 multi turn.
- [TEAM.md](../../TEAM.md): ghi nhận Lê Việt Khoa cùng Mai xây dựng bộ case eval nhóm.
- [Bảng B3 trong group_report.md](group_report.md#b3-team-eval-cases): mục đích, kỳ vọng và kết quả của từng case.
- [Run group v3](../../starter_v0/runs/v3_B_group_openrouter_20261110T200053459021.json): bằng chứng kết quả 8/10 case PASS của bộ eval chung.
- Commit `dddbe3e` và PR #4 do Mai tổng hợp phần CP4; đây là bằng chứng tích hợp sản phẩm chung, không phải commit cá nhân của tôi.

### AI/công cụ đã dùng và cách kiểm tra kết quả

- **ChatGPT/Codex:** hỗ trợ giải thích README,  tạo tài liệu hướng dẫn; cập nhật version log; kiểm tra dữ liệu, giải thích các lỗi đọc, hỗ trợ đọc  file log.
- **VS Code, PowerShell, Python, pytest và Git:** chỉnh sửa file, chạy eval, kiểm tra contract và lưu lịch sử công việc.
- **OpenRouter, model `openai/gpt-4o-mini`:** thực hiện các lần base eval cá nhân có log JSON.

Cách đối chiếu kết quả đã áp dụng với sự hỗ trợ của AI:

1. Dùng `passed=false` để xác định case FAIL; không suy luận chỉ từ nhãn `failure_type`.
2. So `actual_tool_calls` với `expect`, rồi đọc `observed_mismatch` và `failures`.
3. Lấy metric từ `summary`; kiểm tra đủ số case và không có lỗi provider trước khi so sánh.
4. So hash giữa các run để nhận diện thay đổi thực tế và phát hiện v3 trùng v2.
5. Đối chiếu từng dòng version log với file run tương ứng; ghi nhận cả hạn chế của thí nghiệm.

## 5. Tự đánh giá

### Kết quả đạt được

- Sử dụng baseline của nhóm để phân tích lỗi và làm mốc đối chiếu cho CP2.
- Có ba run cá nhân hợp lệ về số case được đo và trạng thái provider; case accuracy cao nhất đạt 80%, tăng 15 điểm phần trăm so với baseline chung.
- Có bằng chứng bằng commit, run JSON và version log; nhận diện được việc chọn đúng tool nhưng sai arguments, cũng như trường hợp đổi nhãn version mà artifact không đổi.
- Cùng Đỗ Thanh Mai xây dựng bộ 10 case eval nhóm đúng cấu trúc 5 single turn và 5 multi turn, có hai case kiểm tra tool mới `wiki`; kết quả chạy chung đạt 8/10 case PASS.

### Bài học rút ra

**System prompt** phù hợp với quy tắc hành vi chung: thiếu thông tin thì hỏi lại, xác nhận trước khi gửi và xử lý yêu cầu nhiều bước. **Tool declaration** phù hợp với điều kiện dùng từng tool, cách phân biệt các tool tương tự và convention arguments như `topic`, `response_type`, `confirmed`.

Chỉ thay một giả thuyết mỗi vòng giúp liên hệ kết quả với thay đổi cụ thể. Nếu sửa nhiều nội dung cùng lúc hoặc không lưu snapshot, điểm tăng không đủ để khẳng định nguyên nhân. Hash là dấu vết nội dung file, không phải thước đo chất lượng.

Unit test/contract test kiểm tra code và tính nhất quán khai báo; eval kiểm tra lựa chọn tool và arguments của model. Contract test xanh không có nghĩa agent đã hỏi xác nhận hoặc xử lý thiếu thông tin đúng.

### Hạn chế và hướng cải thiện

1. Prompt tại commit cá nhân vẫn giữ đoạn cũ yêu cầu tự đoán ngay sau quy tắc hỏi lại, tạo chỉ dẫn mâu thuẫn. Cần thay toàn bộ đoạn cũ và đo riêng tác động.
2. v1 thay cả hai hash so với v0; chưa đủ bằng chứng để khẳng định thực nghiệm cô lập một thay đổi. Các vòng sau cần lưu artifact hoặc commit riêng trước khi sửa tiếp.
3. v3 trùng artifact v2, nên chuỗi cá nhân chưa đáp ứng đủ ba vòng cải tiến khác nhau sau baseline. Cần một thay đổi có giả thuyết rõ và run mới.
4. R12 đã cải thiện routing nhưng vẫn sai arguments; cần thử riêng việc làm rõ `clarify.response_type` và điều kiện xác nhận của `send`.
5. Quy tắc ép hoàn thành một bước vẫn còn trong prompt; cần đánh giá trong một vòng riêng.
6. Các giả thuyết mới được ghi bổ sung sau run. Lần tiếp theo cần ghi giả thuyết trước khi sửa, lưu metric và bằng chứng ngay sau khi chạy.

Những mục trên là kế hoạch cải thiện, chưa được tính là công việc đã hoàn thành trong báo cáo này.
