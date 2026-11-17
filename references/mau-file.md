# Mẫu file — chép rồi thay phần trong < >

## Mẫu A — file chỉ dẫn chính (vd `CLAUDE.md`)
File của AI khác chỉ trỏ về, không chép nội dung:
```markdown
# AGENTS.md — <TÊN DỰ ÁN>
Vai của bạn: <người kiểm độc lập / người thu thập dữ liệu>.
Đọc `CLAUDE.md` trước khi làm; mọi luật ở đó áp cho bạn. Riêng vai này: <1–3 dòng>.
```
File chính:
```markdown
# CHỈ DẪN GỐC — <TÊN DỰ ÁN> (bản <ngày>, <chủ dự án> duyệt)
Vai của bạn: <người làm / người kiểm độc lập / người thu thập dữ liệu>.

## 1. Đọc trước khi làm, theo thứ tự
1. `HUONG_DAN.md` — bảng việc: gặp việc gì → mở file nào → nộp gì → ai duyệt.
   Mỗi việc: mở đúng file ở cột MỞ trước khi làm (không làm theo trí nhớ); nộp kèm phiếu ✅/❌.
2. `kho_tri_thuc/<CACH_NGHI>.md` — cách nghĩ của nghề này.
3. `<nhom>/<ten>/THAM_SO.md` — tham số riêng của <khách hàng / module / sản phẩm / chi nhánh> đang làm.
<!-- Dự án phần mềm: thay mục 2–3 bằng `docs/kien-truc.md` và thêm mục "Lệnh": build · test (cả cách chạy 1 test) · lint · chạy local -->
<!-- vd: `npm run build` · `npm test -- -t "<tên>"` · `npm run lint` · `npm run dev` -->


## 2. Thứ tự ưu tiên khi mâu thuẫn
Lời <chủ dự án> > tài liệu mục 1 > tham số riêng > tài liệu cũ trong `tham_khao_cu/` (chỉ tra cứu).

## 3. Không bao giờ
- <tự gửi khách / tự xuất bản / tự tiêu tiền / tự deploy production / sửa DB production bằng tay>.
- Tự chấm điểm chính thức việc mình làm.
- Nói điều không có nguồn; bịa số, giá, cam kết (chưa có thì để `[...]` + ⚠).
- Chép khoá API ra ngoài `.env`.

## 4. Mặc định kỹ thuật
- <chỉ những điều đúng ở MỌI việc của dự án>
```

## Mẫu B — `HUONG_DAN.md`
```markdown
# HƯỚNG DẪN — <TÊN DỰ ÁN>
## 0. Ba luật làm việc
1. Mở đúng file ở cột MỞ trước khi làm; ghi `MỞ V<n> — <ngày> — đã đọc: …` vào nhật ký.
2. Nộp kèm phiếu ✅/❌ (`HUONG_DAN_TUNG_BUOC.md` §P).
3. Người làm không tự chấm mình.

## 1. Bảng việc
| # | Việc | MỞ trước | NỘP ra | MÁY chặn | AI duyệt |
|---|---|---|---|---|---|
| V0 | Cài máy mới | … | … | … | … |
| V1 | <việc đầu tiên của mỗi đơn vị việc> | … | … | … | … |

## 2. Ba tầng: Chung → Riêng → Đơn vị việc
## 3. Bản đồ thư mục
## 4. Công cụ theo việc
## 5. Việc đang treo (<ngày>)
```

## Mẫu C — Phiếu nộp (§P trong `HUONG_DAN_TUNG_BUOC.md`)
```markdown
### Phiếu nộp — V<n> <tên việc> — <đơn vị việc> — <ngày>
Đã mở: <file §mục>, <file §mục>
| Mục phải có (theo cột NỘP) | ✅/❌ | Ghi chú |
|---|---|---|
| … | | |
Máy chặn: <lệnh> → <kết quả: 0 ⛔>
Chưa làm / nghi ngờ: …
Người duyệt: …
```

## Mẫu D — `RA_SOAT_DINH_KY.md`
```markdown
# RÀ SOÁT ĐỊNH KỲ — lập <ngày>
Mỗi thứ Hai mở file này, làm các dòng đến hạn, ghi ngày. Có sự kiện ở cột "Rà ngay khi" thì rà ngay.

Quyết định mỗi lần rà: **giữ / sửa / thay / bỏ**. Ngày chỉ là lời nhắc; có sự kiện thì rà ngay.

| Lớp | File | Chủ | Lịch | Rà ngay khi | Rà bằng cách | Lần rà gần nhất | Quyết định |
|---|---|---|---|---|---|---|---|
| 1 Chỉ dẫn gốc | CLAUDE.md (+ AGENTS.md, GEMINI.md chỉ trỏ về) | <chủ dự án> | 3 tháng | Đổi hướng dự án | File phụ chỉ trỏ về file chính; mọi đường dẫn còn tồn tại | <ngày> | |
| 2a Luật | … | | 3 tháng | Lỗi lặp lần 2 | Mỗi luật kể được sự cố thật | <ngày> | |
| 2b Máy chặn | … | | 1 tháng | Đổi thước đo / tên file | Cố tình vi phạm 1 lần, máy có chặn không | <ngày> | |
| 3 Quy trình | HUONG_DAN*, sơ đồ | | 2–4 tuần | Máy mới làm sót; model mới | Cho phiên mới làm theo, ghi chỗ lạc | <ngày> | |
| 4 Agent | … | | Mỗi lần model đổi | Model / app cập nhật | Giao lại việc cũ đã biết đáp án | <ngày> | |
| 5 Công cụ | cong_cu/, CLI, MCP, API | | 1 tháng | Lỗi lạ; dịch vụ đổi | Chạy lệnh kiểm chỉ đọc của từng công cụ; ghi phiên bản | <ngày> | |
| Bộ nhớ AI | ~/.claude/projects/<dự án>/memory/ … | | 1 tháng | Đổi tên/chuyển file; luật mới | Mỗi ghi nhớ còn đúng không, file nó nhắc còn không | <ngày> | |

## Kho cũ
- `kho_tri_thuc/tham_khao_cu/` — chỉ tra cứu, AI không tự nạp. Rà 3 tháng: không còn ai dẫn tới → xoá.
```

## Mẫu E — `TIEN_DO.md` (việc chạy hàng loạt)
```markdown
# TIẾN ĐỘ — <tên đợt việc> (lập <ngày>)
Mỗi dòng một đơn vị việc, mỗi cột một bước. Làm xong bước nào ghi ngay "xong <ngày>"; đang chờ ai thì ghi "đã giao <ai>".
Phiên mới / máy khác: đọc file này trước, làm tiếp dòng đầu tiên chưa xong.

| # | Đơn vị | Bước 1 <tên> | Bước 2 <tên> | Bước 3 <tên> | Nộp | Ghi chú |
|---|---|---|---|---|---|---|
| 1 | <tên> | xong 17/11 | đã giao <ai> | | | |
```

## Mẫu F — Thư giữa các AI (`giao_viec/hop_thu/<nguoi_nhan>/<YYYYMMDD-HHMMSS>_<chu-de>.md`)
```markdown
Từ: <AI gửi>
Gửi: <AI nhận>
Về: <việc> — trả lời thư <tên thư> (nếu có)
---
Trạng thái (khi trả lời): XONG | XONG_CÓ_LO_NGẠI | KẸT | CẦN_THÊM_THÔNG_TIN

Việc: <một việc duy nhất>
Đọc: <file/thư mục được đọc>
Cấm đọc: .env, <thư mục bí mật>, file có chữ key/secret/token/mat-khau
Ghi vào: <đường dẫn nộp> — không tạo file nào khác
Hỏi người trước khi: <tiêu tiền / đăng nhập / gửi ra ngoài / xoá>
Xong khi: <tiêu chí>
```
Thư chỉ báo nhận / cảm ơn: không trả lời, chuyển vào `da_doc/`.
