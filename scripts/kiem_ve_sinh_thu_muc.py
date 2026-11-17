#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm vệ sinh thư mục dự án — dùng chung mọi loại dự án, chỉ thư viện chuẩn Python.

    python kiem_ve_sinh_thu_muc.py <thư_mục_dự_án> [--ngay-tam 7] [--bo-qua thu_muc1,thu_muc2]
                                   [--thu-muc-bao-cao reports,bao_cao] [--cho-ten "mermaidjs-v11,..."] [--ca-may]

Chỉ ĐỌC, không xoá/sửa gì. In danh sách theo mức:
  ⛔ phải xử lý · ⚠ nên xem. Mã thoát 1 nếu có ⛔.

Kiểm:
  1 GỐC        file ở gốc dự án không nằm trong danh sách cho phép (`.gocchophep` ở gốc, mỗi dòng một tên; không có thì dùng mặc định)
  2 TÊN        HẬU TỐ kiểu bản chép (_copy, _backup, _bak, _final, _enhanced, (2), " - Copy") → ⛔;
               hậu tố phiên bản (_v2, _new, _old, _ban2) → ⚠; tên có dấu cách/ngoặc → ⚠.
               Không bắt _moi, _cu: tiếng Việt không dấu dễ trùng (nhan_su_moi, cong_cu). Tên hợp lệ có số phiên bản → --cho-ten.
  3 TỰ NẠP     file trong chỗ AI tự đọc (.claude/ .agents/ .cursor/ .gemini/; thêm --ca-may: skills/agents cấp máy)
               có chữ "tài liệu cũ / deprecated / không bắt buộc" → phải chuyển đi, không chỉ đánh dấu
  4 TẠM        file tạm/log/cache (*.tmp, *.log, *.bak, ~$*, .DS_Store, Thumbs.db) cũ hơn N ngày; file rỗng
  5 BÁO CÁO    file .md tên kiểu báo cáo do agent sinh (summary, report, tong-ket, phan_tich, bao-cao…) không nằm
               trong thư mục báo cáo (tên thư mục ở bất kỳ cấp nào, vd plans/<ke-hoach>/reports/)
  6 MỒ CÔI     file .md ở gốc mà không file chỉ dẫn nào nhắc tới tên nó
  7 TRÙNG      hai file nội dung giống hệt nhau (≤ 20 MB, bỏ qua file rỗng; chỉ băm file trùng dung lượng)
  8 BÍ MẬT     file chữ có mẫu khoá API / mật khẩu (ngoài .env*) — chỉ in tên file + dòng + loại, KHÔNG in giá trị
"""
import argparse
import hashlib
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BO_QUA_MAC_DINH = {".git", "node_modules", ".venv", "venv", "dist", "build", ".next", "__pycache__", ".idea", ".vscode"}
GOC_MAC_DINH = {"CLAUDE.md", "AGENTS.md", "GEMINI.md", "README.md", "HUONG_DAN.md", "HUONG_DAN_TUNG_BUOC.md", "RA_SOAT_DINH_KY.md",
                ".env", ".env.example", ".gitignore", ".gocchophep", "package.json", "package-lock.json", "pnpm-lock.yaml",
                "pyproject.toml", "requirements.txt", "tsconfig.json", "Makefile", "Dockerfile", "docker-compose.yml", "LICENSE"}
# Chỉ bắt HẬU TỐ ở cuối tên: tiếng Việt không dấu dễ trùng (cong_cu = công cụ, nhan_su_moi, phong_tam_giam, new_mexico).
TEN_BAN_CHEP = re.compile(r"(?i)([_\-. ](copy|backup|bak|enhanced|final)$|\(\d+\)$|\s-\sCopy$|^copy of\b)")   # ⛔ bản chép
TEN_PHIEN_BAN = re.compile(r"(?i)[_\-. ](v\d+|new|old|ban\d+)$")                                             # ⚠ phiên bản trong tên
CHO_TU_NAP = (".claude", ".agents", ".cursor", ".gemini")
CHU_CU = re.compile(r"(?i)(tài liệu cũ|không bắt buộc|deprecated|\bobsolete\b|\[old\]|lỗi thời)")
DUOI_TAM = {".tmp", ".log", ".bak", ".swp", ".old", ".orig"}
TEN_TAM = re.compile(r"^(~\$|\.DS_Store$|Thumbs\.db$|desktop\.ini$)")
TEN_BAO_CAO = re.compile(r"(?i)(summary|report|tong[_-]?ket|tom[_-]?tat|phan[_-]?tich|bao[_-]?cao|analysis|notes?[_-]\d|recap)")
# Mẫu khoá lộ: (tên loại, regex). Chỉ báo tên loại, không in giá trị.
MAU_BI_MAT = [
    ("Anthropic/OpenAI key", re.compile(r"\bsk-(?:ant-)?[A-Za-z0-9_\-]{20,}")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Facebook/Meta token", re.compile(r"\bEAA[A-Za-z0-9]{40,}")),
    ("GitHub token", re.compile(r"\b(?:ghp|gho|ghs|github_pat)_[A-Za-z0-9_]{20,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("Mật khẩu gán thẳng", re.compile(r"(?i)\b(password|passwd|pwd|mat_?khau|api_?key|secret|token)\s*[:=]\s*['\"][^'\"\s<>{}$]{8,}['\"]")),
]
DUOI_CHU = {".md", ".txt", ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
            ".sh", ".ps1", ".bat", ".html", ".csv", ".sql", ".php", ".go", ".java", ".rb", ".mdc"}


def _la_lien_ket(p: Path) -> bool:
    """Junction (Windows) / symlink: trỏ sang chỗ khác → không đi vào, kẻo đếm trùng file thật."""
    try:
        return p.is_symlink() or (hasattr(p, "is_junction") and p.is_junction())
    except OSError:
        return True


def duyet(goc: Path, bo_qua: set):
    """Trả (danh sách file, danh sách thư mục), không đi qua liên kết."""
    files, dirs = [], []
    for thu_muc, cac_thu_muc, cac_file in os.walk(goc):
        cac_thu_muc[:] = [d for d in cac_thu_muc if d not in bo_qua and not _la_lien_ket(Path(thu_muc) / d)]
        dirs += [Path(thu_muc) / d for d in cac_thu_muc]
        files += [Path(thu_muc) / ten for ten in cac_file]
    return files, dirs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("goc")
    ap.add_argument("--ngay-tam", type=int, default=7, help="file tạm cũ hơn N ngày thì báo")
    ap.add_argument("--bo-qua", default="", help="thêm thư mục bỏ qua, cách nhau dấu phẩy")
    ap.add_argument("--thu-muc-bao-cao", default="reports,bao_cao,bao-cao",
                    help="tên thư mục được phép chứa báo cáo agent sinh (khớp ở bất kỳ cấp nào); có '/' thì khớp đầu đường dẫn")
    ap.add_argument("--cho-ten", default="", help="tên (không đuôi) được phép dù trông như phiên bản, cách nhau dấu phẩy")
    ap.add_argument("--ca-may", action="store_true",
                    help="soi thêm skills/agents cấp máy ($CLAUDE_CONFIG_DIR hoặc ~/.claude) cho mục 3 TỰ NẠP")
    a = ap.parse_args()
    goc = Path(a.goc).resolve()
    bo_qua = BO_QUA_MAC_DINH | {x.strip() for x in a.bo_qua.split(",") if x.strip()}
    cho_bao_cao = [x.strip().replace("\\", "/").strip("/") for x in a.thu_muc_bao_cao.split(",") if x.strip()]
    cho_ten = {x.strip().lower() for x in a.cho_ten.split(",") if x.strip()}

    def trong_cho_bao_cao(rel: str) -> bool:
        thu_muc = rel.split("/")[:-1]
        for c in cho_bao_cao:
            if "/" in c:
                if rel.startswith(c + "/"):
                    return True
            elif c in thu_muc:
                return True
        return False
    f_cho_phep = goc / ".gocchophep"
    cho_phep = ({l.strip() for l in f_cho_phep.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
                if f_cho_phep.is_file() else GOC_MAC_DINH)

    loi = defaultdict(list)  # mục → [(mức, chi tiết)]
    tat_ca, cac_thu_muc = duyet(goc, bo_qua)
    gio = time.time()

    for p in sorted(goc.iterdir()):
        if p.is_file() and p.name not in cho_phep:
            loi["1 GỐC"].append(("⚠", f"{p.name} — không có trong danh sách gốc cho phép (.gocchophep)"))

    for p, la_file in [(f, True) for f in tat_ca] + [(d, False) for d in cac_thu_muc]:
        rel = p.relative_to(goc).as_posix()
        ten = p.stem if la_file else p.name
        if ten.lower() in cho_ten:
            continue
        if TEN_BAN_CHEP.search(ten):
            loi["2 TÊN"].append(("⛔", f"{rel} — tên kiểu bản chép: gộp về file gốc, bản cũ để git/lưu trữ"))
        elif TEN_PHIEN_BAN.search(ten):
            loi["2 TÊN"].append(("⚠", f"{rel} — phiên bản trong tên: xong việc thì giữ 1 bản tên cố định, xoá bản nháp"))
        elif re.search(r"[ ()]", p.name):
            loi["2 TÊN"].append(("⚠", f"{rel} — tên có dấu cách/ngoặc (khó gõ lệnh, dễ là bản chép trùng)"))

    for p in tat_ca:
        rel = p.relative_to(goc).as_posix()
        phan = rel.split("/")
        try:
            tuoi = (gio - p.stat().st_mtime) / 86400
            co = p.stat().st_size
        except OSError:
            continue
        if phan[0] in CHO_TU_NAP and p.suffix.lower() in (".md", ".mdc", ".json", ".toml", ".yaml", ".yml"):
            try:
                if CHU_CU.search(p.read_text(encoding="utf-8", errors="replace")[:3000]):
                    loi["3 TỰ NẠP"].append(("⛔", f"{rel} — đánh dấu cũ nhưng vẫn ở chỗ AI tự nạp: chuyển ra ngoài hoặc xoá"))
            except OSError:
                pass
        if (p.suffix.lower() in DUOI_TAM or TEN_TAM.search(p.name)) and tuoi > a.ngay_tam:
            loi["4 TẠM"].append(("⚠", f"{rel} — file tạm/log {tuoi:.0f} ngày"))
        elif co == 0 and p.name not in ("__init__.py", ".gitkeep", ".keep"):
            loi["4 TẠM"].append(("⚠", f"{rel} — file rỗng"))
        if p.suffix.lower() == ".md" and TEN_BAO_CAO.search(p.stem) and not trong_cho_bao_cao(rel):
            loi["5 BÁO CÁO"].append(("⚠", f"{rel} — tên kiểu báo cáo agent sinh, không nằm trong thư mục {cho_bao_cao}: ai đọc file này? không ai → xoá"))
        if (p.suffix.lower() in DUOI_CHU and not p.name.startswith(".env") and co <= 1024 * 1024):
            try:
                for so_dong, dong in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                    loai = next((ten_loai for ten_loai, mau in MAU_BI_MAT if mau.search(dong)), None)
                    if loai:
                        loi["8 BÍ MẬT"].append(("⛔", f"{rel}:{so_dong} — nghi lộ {loai}: chuyển vào .env, xoay khoá nếu đã commit/gửi đi"))
                        break  # một file báo một lần là đủ
            except OSError:
                pass

    if a.ca_may:
        cau_hinh = Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude")
        for vung in ("skills", "agents", "commands", "rules"):
            for p in (cau_hinh / vung).rglob("*.md") if (cau_hinh / vung).is_dir() else []:
                try:
                    if CHU_CU.search(p.read_text(encoding="utf-8", errors="replace")[:3000]):
                        loi["3 TỰ NẠP"].append(("⛔", f"[máy] {p} — đánh dấu cũ nhưng vẫn ở chỗ AI tự nạp cho MỌI dự án"))
                except OSError:
                    pass

    chi_dan = [p for p in goc.glob("*.md")] + [p for d in CHO_TU_NAP for p in (goc / d).rglob("*.md")] + list((goc / "docs").glob("*.md"))
    van_ban = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in chi_dan if p.is_file())
    for p in goc.glob("*.md"):
        if p.name not in GOC_MAC_DINH and van_ban.count(p.name) <= p.read_text(encoding="utf-8", errors="replace").count(p.name):
            loi["6 MỒ CÔI"].append(("⚠", f"{p.name} — không file chỉ dẫn nào nhắc tới: đưa vào bản đồ thư mục hoặc chuyển/xoá"))

    # Gom theo dung lượng trước; chỉ băm nhóm có ≥ 2 file (thư mục nhiều video/phụ đề vẫn nhanh).
    theo_co = defaultdict(list)
    for p in tat_ca:
        try:
            co = p.stat().st_size
            if 0 < co <= 20 * 1024 * 1024:
                theo_co[co].append(p)
        except OSError:
            continue
    theo_bam = defaultdict(list)
    for co, nhom in theo_co.items():
        if len(nhom) < 2:
            continue
        for p in nhom:
            try:
                theo_bam[(co, hashlib.sha1(p.read_bytes()).hexdigest())].append(p.relative_to(goc).as_posix())
            except OSError:
                continue
    for ds in theo_bam.values():
        if len(ds) > 1:
            loi["7 TRÙNG"].append(("⚠", " = ".join(ds[:4]) + (f" (+{len(ds) - 4})" if len(ds) > 4 else "")))

    n_chan = 0
    for muc in ("1 GỐC", "2 TÊN", "3 TỰ NẠP", "4 TẠM", "5 BÁO CÁO", "6 MỒ CÔI", "7 TRÙNG", "8 BÍ MẬT"):
        ds = loi.get(muc, [])
        print(f"\n[{muc}] {'✅ sạch' if not ds else f'{len(ds)} mục'}")
        for muc_do, chi_tiet in ds[:40]:
            print(f"  {muc_do} {chi_tiet}")
        if len(ds) > 40:
            print(f"  … còn {len(ds) - 40} mục")
        n_chan += sum(1 for m, _ in ds if m == "⛔")
    print(f"\n{len(tat_ca)} file đã soi · {n_chan} ⛔ · chỉ đọc, chưa xoá gì")
    return 1 if n_chan else 0


if __name__ == "__main__":
    sys.exit(main())
