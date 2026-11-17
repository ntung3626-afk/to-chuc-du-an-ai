---
name: to-chuc-du-an-ai
description: Dựng và giữ gọn cấu trúc file cho MỌI loại dự án làm cùng AI (Claude Code, Gemini/Antigravity, Codex, Cursor) — phần mềm (CRM, web, app, script), sản xuất/vận hành (nội dung, quảng cáo, bán hàng, kế toán, báo cáo), nghiên cứu/tư vấn. Dùng khi BẮT ĐẦU dự án mới, khi người dùng nói "tổ chức file", "dựng khung dự án", "hệ thống lộn xộn / AI làm sai phải nhắc lại / máy khác làm sót bước", hoặc khi rà soát một dự án đang chạy. Đưa ra 5 lớp (chỉ dẫn gốc → luật & máy chặn → quy trình → agent → công cụ), bảng việc "gặp việc gì → mở file nào → nộp gì → ai duyệt", khung thư mục theo loại dự án và lịch rà soát chống mục rữa.
---

# Tổ chức dự án làm cùng AI — dùng chung mọi ngành nghề

Mục tiêu: sau vài tuần dự án vẫn gọn, AI không phải nhắc lại, người/máy mới vào làm đúng ngay từ việc đầu.
Gốc của sự lộn xộn hầu như luôn là một trong ba điều, ở ngành nào cũng vậy:
1. **Xây ngọn trước gốc**: có agent, công cụ, giao diện đẹp mà chưa có file chỉ dẫn gốc rõ ràng.
2. **Tài liệu xếp theo tài liệu, không theo việc**: AI đọc cả đống mà không biết việc đang làm cần mở file nào → làm theo trí nhớ, sót bước.
3. **Xây xong để đó**: model mới, API đổi, luật mới chồng luật cũ, file cũ vẫn nằm chỗ AI tự đọc → hệ thống mục dần mà không ai biết vì sao.

## 1. Năm lớp — dựng ĐÚNG THỨ TỰ, từ lõi ra ngoài
Lõi ít đổi, xây một lần. Càng ra ngoài càng đổi nhanh, càng phải rà thường xuyên.

| # | Lớp | Là gì | Ví dụ phần mềm (CRM) | Ví dụ vận hành (quảng cáo, nội dung, kế toán) | Mục nhanh? |
|---|---|---|---|---|---|
| 1 | **Chỉ dẫn gốc** | `CLAUDE.md` · `AGENTS.md` · `GEMINI.md` — **bản chỉ đường** | Lệnh build/test, bản đồ thư mục, quy ước đặt tên | Đọc file nào trước, ai duyệt, điều cấm | Chậm nhất |
| 2 | **Luật + máy chặn** | Luật "luôn / không bao giờ"; máy chặn = công cụ tự từ chối chạy | Test, lint, typecheck, hook trước commit, CI | Script kiểm trước khi gửi khách / tiêu tiền / xuất bản | Trung bình |
| 3 | **Quy trình** | Việc lặp lại 5–15 lần: bảng việc + hướng dẫn từng bước + mẫu nộp | Thêm tính năng, sửa lỗi, migration, phát hành | Lên chiến dịch, làm một sản phẩm nội dung, chốt sổ tháng | Nhanh |
| 4 | **Agent** | Một VAI dùng nhiều quy trình | Người review code độc lập, người viết test | Người QC độc lập, người tải/trích dữ liệu | **Nhanh nhất** |
| 5 | **Công cụ & dữ liệu** | Script, CLI, MCP, API, cơ sở dữ liệu | DB, API bên thứ ba, gh, docker | Meta Ads, Google Drive, phần mềm kế toán | Trung bình |

Chi tiết từng lớp: `references/nam-lop-chi-tiet.md`. Khung thư mục theo loại dự án: `references/khung-theo-loai-du-an.md`. Mẫu chép dùng ngay: `references/mau-file.md`.

## 2. Khi BẮT ĐẦU dự án mới — làm theo thứ tự này
1. **Nhận diện loại dự án** (đọc thư mục hiện có trước, rồi mới hỏi): **phần mềm** · **sản xuất / vận hành** · **nghiên cứu / tư vấn** · lai. Mỗi loại một khung (`references/khung-theo-loai-du-an.md`).
2. **Hỏi người dùng tối đa 5 câu, gộp 1 lần** (bỏ câu đã biết từ thư mục): làm ra cái gì, cho ai · ai duyệt cuối ·
   có những AI nào cùng làm · **đơn vị việc lặp lại** là gì (một tính năng / một đơn hàng / một chiến dịch / một báo cáo / một sản phẩm nội dung…) ·
   có khoá API, tài khoản, dữ liệu khách hàng nào cần bảo vệ.
3. **Dựng khung thư mục** theo đúng loại. Dự án phần mềm: **không phá cấu trúc chuẩn của ngôn ngữ/framework** — chỉ thêm lớp chỉ dẫn và quy trình bên cạnh.
4. **Viết lớp 1 trước tiên** (mẫu A): ai, làm gì, đọc file nào theo thứ tự, ưu tiên khi mâu thuẫn, ≤ 5 điều "không bao giờ", lệnh chạy/kiểm cơ bản. Dưới 40 dòng.
5. **Viết bảng việc** (mẫu B): mỗi việc lặp lại một dòng. Lúc đầu 3–5 việc đã biết chắc.
6. **Tạo `RA_SOAT_DINH_KY.md`** (mẫu D) ngay từ ngày đầu, ghi ngày.
7. **Dừng.** Luật, agent, công cụ chỉ thêm khi gặp vấn đề thật (mục 4). Một file chỉ dẫn tốt + một quy trình + một máy chặn là đủ chạy.

## 3. Ba tầng — áp cho mọi loại dự án
**Chung** (cách làm đúng ở mọi đơn vị việc) → **Riêng** (một khách hàng / một module / một kênh / một sản phẩm) → **Đơn vị việc** (một tính năng, một đơn, một chiến dịch: nhật ký quyết định, bản nộp, kết quả kiểm).
Thắng khi mâu thuẫn: lời chủ dự án > Chung > Riêng > Đơn vị việc > tài liệu cũ.
**Không chép trùng nội dung giữa các tầng — trỏ tới nhau.**

## 4. Luật vận hành (mỗi luật có sự cố thật đứng sau)
1. **Theo việc, không theo tài liệu.** Bảng việc có 4 cột: *MỞ trước* · *NỘP ra* · *MÁY chặn* · *AI duyệt*. Bắt đầu việc nào thì mở đúng các file ở cột MỞ, ghi một dòng `MỞ V<n> — <ngày> — đã đọc: …` vào nhật ký. Không làm theo trí nhớ.
2. **Mỗi việc một mẫu riêng.** Hai việc na ná nhau (review bản thiết kế / review code; kiểm nội dung / kiểm thành phẩm; duyệt ngân sách / duyệt báo cáo) mà dùng chung một mẫu → AI chấm nhầm thước đo. Mẫu nằm ngay trong file thước đo của việc đó, bảng việc trỏ đúng mẫu.
3. **Máy chặn hơn lời nhắc.** Điều gì đã bị quên 2 lần → viết thành kiểm tra tự động, đặt ngay trước bước tốn kém hoặc không quay lại được (merge/deploy, migration DB, gửi khách, tiêu tiền quảng cáo, xuất bản). Báo lý do + file cần đọc.
4. **Luật từ sự cố, không từ tưởng tượng.** Chỉ thêm luật khi AI đã làm sai phải nhắc lại. Ghi sự cố ngay cạnh luật. Luật không còn lý do → bỏ.
5. **Người làm không tự chấm mình.** Kết quả quan trọng có người/AI độc lập kiểm theo thước đo viết sẵn (test, checklist, bảng chấm); chủ dự án chốt.
6. **Sửa tại chỗ, không tạo bản "mới", "v2", "final", "_enhanced".** Hai bản cùng tồn tại = AI đọc nhầm bản. Với code: dùng git, không nhân bản file.
7. **File cũ không được nằm ở chỗ AI tự nạp** (`.claude/`, `.agents/`, `.cursor/`, gốc dự án, thư mục skills, `~/.claude/`). Ghi chữ "cũ" trong file là KHÔNG đủ: skill/agent cũ vẫn tự bật theo mô tả. Chuyển vào `tham_khao_cu/` hoặc xoá.
8. **Nhiều AI làm chung: mỗi lần một việc** qua hộp thư (hoặc issue/ticket); việc mới chỉ giao sau khi việc trước báo XONG.
9. **Một nguồn sự thật cho mỗi điều.** Tài liệu nào sinh từ tài liệu khác (sơ đồ, README, tài liệu API) → ghi rõ "sửa A thì sửa cả B", hoặc sinh tự động.
10. **Bí mật chỉ ở một chỗ** (`.env` hoặc kho bí mật). Không ghi ra log, bộ nhớ AI, thư, gói gửi đi, commit.

## 5. Vệ sinh file — ghi, sửa, dọn, file do agent sinh
**Ghi file**
- **Chỉ ghi vào chỗ đã định.** Sản phẩm của một việc chỉ nằm ở chỗ cột NỘP của bảng việc ghi. Không có trong cột NỘP = không được tạo trong dự án.
- **Nháp và tạm ra ngoài dự án** (thư mục tạm của phiên / `_nhap/` có trong `.gitignore`). Agent muốn thử, chạy thử, ghi kết quả trung gian → ghi ở đó, không ở gốc, không cạnh sản phẩm.
- **Gốc dự án có danh sách cho phép** (`.gocchophep`, mỗi dòng một tên). File mới ở gốc phải được thêm vào danh sách và bản đồ thư mục, nếu không là rác.
- **Báo cáo / tóm tắt / phân tích do agent sinh:** mặc định trả lời trong khung chat, KHÔNG tạo file. Chỉ tạo khi người dùng xin hoặc khi đó là bản NỘP của việc; khi tạo thì vào một thư mục báo cáo cố định, tên có ngày `YYYYMMDD-<chu-de>.md`.
- **Agent con** (subagent) nhận rõ trong lời giao: được ghi vào đâu, không được tạo file nào khác.

**Sửa file**
- Sửa tại chỗ. Muốn giữ bản cũ → git, hoặc thư mục lưu trữ có ngày; không để `_v2`, `_final`, `_moi` cạnh nhau. Nháp có số phiên bản (`thumb_v1..v4`) được phép trong lúc làm, **xong việc giữ một bản tên cố định**, xoá phần còn lại.
- **File do máy sinh ghi rõ ở dòng đầu** "SINH TỰ ĐỘNG bởi <công cụ> — không sửa tay, sửa ở <nguồn>". Người/AI sửa tay file sinh = mất ở lần chạy sau.
- **Mỗi file chỉ dẫn có một chủ** (người hoặc vai được sửa); file của chủ dự án (CLAUDE.md, luật) AI chỉ đề xuất sửa.
- **Đổi tên / chuyển file → tìm mọi chỗ nhắc tới tên cũ và sửa hết** (`grep` tên cũ phải ra 0). Ghi một dòng vào nhật ký: đổi gì, vì sao.
- Sửa đúng phần cần sửa; không định dạng lại, viết lại phần không liên quan (làm nhiễu so sánh, dễ mất nội dung).

**Dọn**
- **Bước cuối của mỗi đơn vị việc là "Dọn"** (một dòng trong bảng việc): xoá nháp, file tạm, bản trung gian; chỉ giữ bản NỘP và nhật ký.
- Hạn giữ: tạm/log/cache 7 ngày · nháp tới khi đơn vị việc xong · lưu trữ 3 tháng rồi rà (không ai dẫn tới → xoá).
- Bản sao có chủ đích (gói giao khách, bản phát hành) ghi rõ trong bản đồ là bản sao, không sửa vào bản sao.
- **Máy kiểm:** `python scripts/kiem_ve_sinh_thu_muc.py <dự_án>` (chỉ đọc) — gốc lạ, tên bản chép/phiên bản, file cũ ở chỗ AI tự nạp, tạm/rỗng, báo cáo lạc chỗ, file mồ côi, file trùng. Chạy mỗi tuần trong lịch rà soát và trước khi đóng gói/chuyển máy; ⛔ phải xử lý.

## 6. Rà soát chống mục rữa
- `RA_SOAT_DINH_KY.md`: mỗi lớp ghi file nào · lịch rà · sự kiện buộc rà ngay · cách rà · ngày rà gần nhất.
- Lịch gợi ý: agent → mỗi lần model đổi · quy trình → 2–4 tuần · công cụ, máy chặn → 1 tháng (sớm hơn khi thư viện/API đổi) · luật, chỉ dẫn gốc → 3 tháng.
- Phép rà nhanh nhất cho quy trình: **cho một máy/phiên mới làm theo đúng hướng dẫn**, ghi chỗ nó lạc. Chỗ lạc là lỗi của hướng dẫn, không phải của AI.
- Model mới ra: giao lại một việc cũ đã biết đáp án, so kết quả.
- File chỉ dẫn chung của cả máy (`~/.claude/CLAUDE.md`, skills, agents toàn cục) nạp vào MỌI dự án → chỉ để điều đúng ở mọi dự án; bộ luật của một ngành đặt ở đây sẽ làm nhiễu dự án ngành khác.

## 7. Khi rà một dự án ĐANG lộn xộn
1. Chạy `scripts/kiem_ve_sinh_thu_muc.py`, rồi kiểm kê: mọi file chỉ dẫn (`*.md` ở gốc, `.claude/`, `.agents/`, `.cursor/`, skills, agents, cả cấp dự án lẫn cấp máy) và đếm theo vùng.
2. Tìm **hai nguồn nói khác nhau** về cùng một việc; skill/agent/luật cũ còn ở chỗ tự nạp; file "_v2/_new/_final".
3. Tìm việc có hai mẫu (hoặc không có mẫu), và việc không có máy chặn dù đã từng bị quên.
4. Báo người dùng bảng "lớp · tình trạng · chỗ hỏng" trước; xoá/chuyển file chỉ sau khi người dùng đồng ý (trừ khi đã được giao toàn quyền thư mục).
5. Sửa xong: cập nhật bản đồ thư mục, `RA_SOAT_DINH_KY.md`, và mọi chỗ trỏ tới file đã chuyển (`grep` tên cũ phải ra 0).

## 8. Ba lỗi hay gặp nhất
- Dựng 10 agent ngay từ đầu → không ai bảo trì. **Một agent dùng hằng ngày hơn mười agent bị bỏ quên.**
- Nhồi mọi thứ vào `CLAUDE.md` → AI đọc chậm, bỏ sót. Giữ nó là bản chỉ đường.
- Gửi hệ thống sang máy khác bằng cách chép đè → file đã xoá ở máy gốc vẫn còn ở máy kia. Dùng git, hoặc đóng gói sạch kèm danh sách file phải xoá.
