# Mẫu file — chép rồi thay phần trong < >

## Mẫu A — `CLAUDE.md` (chép sang `AGENTS.md`, `GEMINI.md`, chỉ đổi dòng vai)
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
Lời <chủ dự án> > tài liệu mục 1 > tham số riêng. Tài liệu bỏ dùng → xoá, không giữ "chỉ tra cứu" (SKILL §4.7).

## 3. Không bao giờ
- <tự gửi khách / tự xuất bản / tự tiêu tiền / tự deploy production / sửa DB production bằng tay>.
- Tự chấm điểm chính thức việc mình làm.
- Nói điều không có nguồn.
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

| Lớp | File | Lịch | Rà ngay khi | Rà bằng cách | Lần rà gần nhất |
|---|---|---|---|---|---|
| 1 Chỉ dẫn gốc | CLAUDE.md · AGENTS.md · GEMINI.md | 3 tháng | Đổi hướng dự án | 3 file khớp nhau; mọi đường dẫn còn tồn tại | <ngày> |
| 2a Luật | … | 3 tháng | Lỗi lặp lần 2 | Mỗi luật kể được sự cố thật | <ngày> |
| 2b Máy chặn | … | 1 tháng | Đổi thước đo / tên file | Cố tình vi phạm 1 lần, máy có chặn không | <ngày> |
| 3 Quy trình | HUONG_DAN*, sơ đồ | 2–4 tuần | Máy mới làm sót; model mới | Cho phiên mới làm theo, ghi chỗ lạc | <ngày> |
| 4 Agent | … | Mỗi lần model đổi | Model / app cập nhật | Giao lại việc cũ đã biết đáp án | <ngày> |
| 5 Công cụ | cong_cu/, CLI, MCP, API | 1 tháng | Lỗi lạ; dịch vụ đổi | Chạy thử từng công cụ; ghi phiên bản | <ngày> |

## Tài liệu bỏ dùng
- Mặc định xoá (grep tên ra 0 chỗ dẫn). Chỉ giữ khi thật cần tra: đặt ngoài mọi chỗ AI tự nạp, ghi hạn rà 3 tháng; hết hạn không ai dẫn tới → xoá.
```
