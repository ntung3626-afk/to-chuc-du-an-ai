# Năm lớp — chi tiết và cách làm đúng

## Lớp 1 — Chỉ dẫn gốc
- **Nội dung:** ai là chủ dự án, dự án làm gì · danh sách file phải đọc theo thứ tự (bắt đầu bằng bảng việc) · thứ tự ưu tiên khi mâu thuẫn ·
  ≤ 5 điều "không bao giờ" (khoá API, tự đăng/tự gửi ra ngoài, tự chấm mình, bịa dữ liệu…) · mặc định kỹ thuật thật sự dùng ở mọi việc.
- **Không chứa:** quy trình chi tiết, số liệu riêng, lịch sử sửa đổi. Những thứ đó ở lớp 3 hoặc tầng Riêng; lớp 1 chỉ trỏ tới.
- **Nhiều AI:** `CLAUDE.md`, `AGENTS.md`, `GEMINI.md` cùng nội dung từ mục 1 trở đi (kiểm bằng `diff`). Khác nhau chỉ ở phần vai của AI đó.
- **File chỉ dẫn chung của cả máy** (`~/.claude/CLAUDE.md`) được nạp vào MỌI dự án. Chỉ để điều đúng ở mọi dự án (ngôn ngữ trả lời, vài thói quen). Bộ luật của một ngành nghề khác đặt ở đây sẽ làm nhiễu mọi dự án.
- **Bài tập 5 phút:** viết 3 dòng — mình là ai và dùng AI làm gì · một điều AI luôn phải làm · một điều AI không bao giờ được làm.

## Lớp 2 — Luật và máy chặn
- **Luật** = gợi ý mạnh, AI có thể quên. **Máy chặn** = công cụ từ chối chạy, không quên được.
- Ứng viên làm luật: điều mình đã phải nhắc AI ≥ 2 lần. Ứng viên làm máy chặn: luật đã bị quên ≥ 2 lần, hoặc quên thì tốn tiền / không sửa được.
- Máy chặn tốt: đặt **ngay trước bước tốn kém** (merge/deploy, migration DB, gửi khách, tiêu tiền quảng cáo, xuất bản, chốt sổ); báo **lý do + file cần đọc + mẫu cần dùng**; kiểm điều có thể đo
  (file tồn tại, có ghi đúng tên thước đo, số lỗi ⛔ = 0), không kiểm cảm tính.
- Hook của Claude Code (settings.json) dùng cho việc gắn với sự kiện của chính công cụ (trước khi commit → quét khoá lộ). Kiểm theo nghiệp vụ thì đặt trong script của việc đó.
- Ghi sự cố cạnh mỗi luật: "luật X — vì ngày D, việc Y đã sai thế này".

## Lớp 3 — Quy trình
- **Bảng việc** (một trang, mỗi việc một dòng, đánh số V0, V1…): *việc* · *MỞ trước* (file + mục) · *NỘP ra* (tên file cụ thể) · *MÁY chặn* · *AI duyệt*.
- **Hướng dẫn từng bước** cùng số việc: lệnh chạy được ngay, bẫy hay gặp, việc tiếp theo.
- **Phiếu nộp** chung: việc gì · đã mở file nào · từng mục ✅/❌ · cái gì chưa làm và vì sao.
- **Sơ đồ đào tạo** (tuỳ chọn): sinh từ bảng việc; ghi rõ "sửa hướng dẫn thì sửa cả sơ đồ".
- Quy trình hai loại: *cần phán đoán* (viết, chọn, chấm — có người ở vòng lặp) và *máy móc* (tải, đo, đóng gói — một lệnh). Loại máy móc nên thành script.
- Model mới thông minh hơn → quy trình cũ thường **thừa chữ**; rà để cắt, không chỉ để thêm.

## Lớp 4 — Agent
- Agent = vai. Dựng agent khi đã có đủ quy trình mô tả trọn công việc của vai đó.
- Thứ tự dựng: vai mang lại nhiều nhất trước, đẩy tới giới hạn rồi mới dựng vai thứ hai. Vai đáng dựng sớm nhất thường là **người kiểm độc lập** (chấm theo thước đo, không phải người làm).
- Agent rẻ cho việc đọc dài / soi ảnh / tìm tài liệu giúp tiết kiệm cho agent chính.
- Nhiều AI làm chung: hộp thư theo thư mục, mỗi thư một việc, đầu thư có người gửi/nhận/thời gian/tham chiếu, trả lời XONG mới gửi việc mới.

## Lớp 5 — Công cụ và dữ liệu
- Script ở `cong_cu/<nhom_viec>/`, tên file dài cũng được nhưng đọc tên là biết làm gì.
- Mỗi công cụ có một dòng trong mục "công cụ theo việc" của bảng việc — công cụ không gắn với việc nào thì không ai dùng.
- Khoá API chỉ trong `.env`. Không ghi ra log, bộ nhớ, thư, gói gửi đi.
- CLI thường gọn và dễ kiểm hơn MCP; dùng cái nào chạy ổn hơn cho việc đó, ghi phiên bản đang dùng vào `RA_SOAT_DINH_KY.md`.
- Dịch vụ ngoài hay đổi (API, giới hạn tải, định dạng) → lớp này cần rà hằng tháng.
