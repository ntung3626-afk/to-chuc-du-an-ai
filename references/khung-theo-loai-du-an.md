# Khung thư mục theo loại dự án

Nguyên tắc chung: lớp chỉ dẫn (CLAUDE.md, bảng việc, rà soát) giống nhau ở mọi loại; **phần chứa sản phẩm** theo chuẩn của ngành.
Dự án lai (vd CRM + đội quảng cáo dùng CRM): mỗi phần một khung, một `CLAUDE.md` gốc trỏ tới cả hai.

## A. Phần mềm (CRM, web, app, API, script, MCP server)
```
<repo>/
├── CLAUDE.md · AGENTS.md            lệnh build / test / lint / chạy local · bản đồ module · quy ước · điều cấm
├── README.md                        cho NGƯỜI: dự án là gì, cài đặt, chạy
├── docs/
│   ├── HUONG_DAN.md                 bảng việc (thêm tính năng, sửa lỗi, migration, phát hành, xoay khoá…)
│   ├── kien-truc.md                 các module nói chuyện với nhau thế nào, dữ liệu đi đâu
│   ├── quyet-dinh/NNNN-<ten>.md     mỗi quyết định lớn một file (vì sao chọn X, bỏ Y) — không sửa, chỉ thêm
│   └── RA_SOAT_DINH_KY.md
├── src/ … tests/ … scripts/         THEO CHUẨN ngôn ngữ/framework — không tự chế
├── .env.example                     tên biến, không có giá trị · `.env` nằm trong .gitignore
└── .github/workflows/ (hoặc CI khác)  máy chặn chạy trên mọi PR
```
- **Máy chặn điển hình:** test + lint + typecheck chạy được bằng một lệnh và ghi trong `CLAUDE.md`; hook trước commit quét khoá lộ;
  CI chặn merge khi đỏ; migration DB phải có bản lùi (down) và chạy thử trên bản sao dữ liệu.
- **Đơn vị việc** = một nhánh / một PR / một issue: mô tả, tiêu chí xong, kết quả review.
- **Người kiểm độc lập** = review code bởi phiên/agent khác, theo checklist viết sẵn (đúng nghiệp vụ, bảo mật, dữ liệu khách hàng, hiệu năng).
- **CLAUDE.md cho code nên có:** lệnh chạy chính xác; module nào không được sửa tay (sinh tự động, vendor); quy ước đặt tên; cách chạy một test đơn lẻ;
  dữ liệu thật hay dữ liệu thử ở môi trường nào; điều cấm (đẩy thẳng lên nhánh chính, sửa DB production bằng tay, tắt test cho qua).
- **Bẫy riêng:** AI tạo file `*_new.py`, `*_v2.ts` thay vì sửa file cũ → cấm trong CLAUDE.md; tài liệu API viết tay lệch code → sinh tự động.

## B. Sản xuất / vận hành (nội dung, quảng cáo, bán hàng, chăm sóc khách, kế toán, nhân sự)
```
<du_an>/
├── CLAUDE.md                        file chỉ dẫn chính (AGENTS.md · GEMINI.md nếu có chỉ trỏ về đây)
├── HUONG_DAN.md                     bảng việc + bản đồ thư mục + công cụ theo việc + việc đang treo
├── HUONG_DAN_TUNG_BUOC.md           lệnh / thao tác cụ thể từng việc + phiếu nộp
├── RA_SOAT_DINH_KY.md
├── .env
├── kho_tri_thuc/                    tầng CHUNG: cách nghĩ, thước đo chất lượng, luật, mẫu
│   └── tham_khao_cu/
├── <nhom>/<ten>/                    tầng RIÊNG: một kênh / một khách hàng / một sản phẩm / một chi nhánh — tham số riêng
│   └── <don_vi_viec>/               tầng ĐƠN VỊ VIỆC: một sản phẩm nội dung / một chiến dịch / một đơn / một kỳ sổ
├── cong_cu/<nhom_viec>/             script theo việc
├── TIEN_DO.md                       (khi chạy hàng loạt) mẫu E
└── giao_viec/hop_thu/<ten_ai>/      hộp thư giữa các AI (nếu có nhiều AI), thư theo mẫu F, đã đọc → da_doc/
```
- **Máy chặn điển hình:** script kiểm trước khi xuất bản / gửi khách / tăng ngân sách / chốt sổ (đủ file, đúng định dạng, có kết quả QC, số khớp nguồn, **không còn `[...]` / ⚠ chưa xác nhận**).
- **Không bịa số:** bản nộp (kịch bản, báo giá, bài đăng, báo cáo) có số đo, giá, cam kết, chuyện khách thật chưa có nguồn → để `[...]` + ⚠, cuối file có danh sách "đội cần xác nhận trước khi dùng". Không dùng câu chứng nhận (đạt chuẩn, đạt TCVN…) khi chưa có giấy tờ.
- **Thước đo** (bảng chấm, checklist) viết thành file ở `kho_tri_thuc/`, mỗi việc cần chấm có **mẫu nhờ kiểm riêng**.
- **Bẫy riêng:** tham số của nhóm này chép sang nhóm khác (mỗi khách hàng / kênh / chi nhánh đo riêng); quyết định tiêu tiền hoặc gửi ra ngoài do AI tự làm.

## C. Nghiên cứu / tư vấn / viết (báo cáo, phân tích thị trường, hồ sơ, giáo trình)
```
<du_an>/
├── CLAUDE.md                        câu hỏi nghiên cứu, người đọc cuối, chuẩn trích dẫn, điều cấm (bịa nguồn)
├── HUONG_DAN.md                     bảng việc: thu nguồn → ghi chép → dàn ý → viết → kiểm sự thật → nộp
├── nguon/                           tài liệu gốc (không sửa) + `NGUON.md` (đường dẫn, ngày lấy)
├── ghi_chep/                        trích đoạn có mốc trang/giờ
├── ban_thao/                        một file mỗi sản phẩm — sửa tại chỗ, không v2/v3
├── kiem/                            bảng sự thật: mỗi khẳng định → nguồn + trích nguyên văn
└── RA_SOAT_DINH_KY.md
```
- **Máy chặn điển hình:** không nộp khi còn khẳng định chưa có dòng trong bảng sự thật.
- **Bẫy riêng:** AI tóm tắt từ trí nhớ thay vì từ nguồn đã tải; nguồn hết hạn (số liệu cũ) không ai rà.

## Đặt tên file (mọi loại)
- Tên tự giải thích, dài cũng được: đọc tên là biết file làm gì (`tai_phu_de_top_va_day.py`, `kiem-tra-truoc-khi-gui-khach.ts`).
- Một kiểu đặt tên trong một dự án; theo chuẩn của ngôn ngữ khi là code.
- Ngày trong tên theo dạng `YYYYMMDD` để tự xếp đúng thứ tự.
