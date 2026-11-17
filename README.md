# to-chuc-du-an-ai

Skill cho Claude Code / claude.ai: dựng và giữ gọn cấu trúc file cho **mọi loại dự án làm cùng AI**
(phần mềm, sản xuất / vận hành, nghiên cứu / tư vấn).

- 5 lớp từ lõi ra ngoài: chỉ dẫn gốc → luật & máy chặn → quy trình → agent → công cụ
- Bảng việc "gặp việc gì → mở file nào → nộp gì → ai duyệt"
- Khung thư mục theo loại dự án, vệ sinh file (ghi, sửa, dọn, file do agent sinh), lịch rà soát chống mục rữa
- `scripts/kiem_ve_sinh_thu_muc.py`: kiểm vệ sinh thư mục (chỉ đọc, Python thuần)

## Cài
**Claude Code**
```bash
git clone https://github.com/ntung3626-afk/to-chuc-du-an-ai.git ~/.claude/skills/to-chuc-du-an-ai
```
Nếu máy đặt thư mục cấu hình chỗ khác (biến `CLAUDE_CONFIG_DIR`, vd `D:\.claude`) thì clone vào `$CLAUDE_CONFIG_DIR/skills/to-chuc-du-an-ai`.
Windows PowerShell: `git clone https://github.com/ntung3626-afk/to-chuc-du-an-ai.git "$env:USERPROFILE\.claude\skills\to-chuc-du-an-ai"`.

Mở dự án mới và nói "dựng khung dự án" hoặc "tổ chức file cho dự án này".

**claude.ai**: nén thư mục (SKILL.md ở gốc file zip) → Settings → Capabilities → Skills → tải lên.

**Kiểm vệ sinh một dự án**
```bash
python scripts/kiem_ve_sinh_thu_muc.py <thư_mục_dự_án>            # chỉ dự án
python scripts/kiem_ve_sinh_thu_muc.py <thư_mục_dự_án> --ca-may   # thêm skills/agents cấp máy
```
