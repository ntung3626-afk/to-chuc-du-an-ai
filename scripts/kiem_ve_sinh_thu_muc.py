#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kiểm vệ sinh thư mục dự án — dùng chung mọi loại dự án, chỉ thư viện chuẩn Python.

    python kiem_ve_sinh_thu_muc.py <thư_mục_dự_án> [--ngay-tam 7] [--bo-qua thu_muc1,thu_muc2]

Chỉ ĐỌC, không xoá/sửa gì. In danh sách theo mức:
  ⛔ phải xử lý · ⚠ nên xem. Mã thoát 1 nếu có ⛔.

Kiểm:
  1 GỐC        file ở gốc dự án không nằm trong danh sách cho phép (`.gocchophep` ở gốc, mỗi dòng một tên; không có thì dùng mặc định)
  2 TÊN        tên kiểu bản sao/phiên bản: _v2, _new, _final, _old, _backup, copy, (2), "- Copy", _moi, _cu, _ban2 …; tên có dấu cách/ngoặc
  3 TỰ NẠP     file trong chỗ AI tự đọc (.claude/ .agents/ .cursor/ .gemini/) có chữ "cũ / old / deprecated / không bắt buộc" → phải chuyển đi, không chỉ đánh dấu
  4 TẠM        file tạm/log/cache (*.tmp, *.log, *.bak, ~$*, .DS_Store, Thumbs.db, __pycache__) cũ hơn N ngày; file rỗng
  5 BÁO CÁO    file .md tên kiểu báo cáo do agent sinh (summary, report, tong_ket, phan_tich, bao_cao…) nằm ngoài thư mục báo cáo đã định
  6 MỒ CÔI     file .md ở gốc / kho chỉ dẫn mà không file chỉ dẫn nào nhắc tới tên nó
  7 TRÙNG      hai file nội dung giống hệt nhau (≤ 20 MB, bỏ qua file rỗng)
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
TEN_BAO_CAO = re.compile(r"(?i)(summary|report|tong_?ket|tom_?tat|phan_?tich|bao_?cao|analysis|notes?_\d|recap)")


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
    ap.add_argument("--thu-muc-bao-cao", default="plans/reports,docs/reports,bao_cao,reports",
                    help="nơi được phép chứa báo cáo agent sinh")
    a = ap.parse_args()
    goc = Path(a.goc).resolve()
    bo_qua = BO_QUA_MAC_DINH | {x.strip() for x in a.bo_qua.split(",") if x.strip()}
    cho_bao_cao = [x.strip().replace("\\", "/") for x in a.thu_muc_bao_cao.split(",") if x.strip()]
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
        if p.suffix.lower() == ".md" and TEN_BAO_CAO.search(p.stem) and not any(rel.startswith(c + "/") for c in cho_bao_cao):
            loi["5 BÁO CÁO"].append(("⚠", f"{rel} — tên kiểu báo cáo agent sinh, nằm ngoài {cho_bao_cao}: ai đọc file này? không ai → xoá"))

    chi_dan = [p for p in goc.glob("*.md")] + [p for d in CHO_TU_NAP for p in (goc / d).rglob("*.md")] + list((goc / "docs").glob("*.md"))
    van_ban = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in chi_dan if p.is_file())
    for p in goc.glob("*.md"):
        if p.name not in GOC_MAC_DINH and van_ban.count(p.name) <= p.read_text(encoding="utf-8", errors="replace").count(p.name):
            loi["6 MỒ CÔI"].append(("⚠", f"{p.name} — không file chỉ dẫn nào nhắc tới: đưa vào bản đồ thư mục hoặc chuyển/xoá"))

    theo_bam = defaultdict(list)
    for p in tat_ca:
        try:
            co = p.stat().st_size
            if 0 < co <= 20 * 1024 * 1024:
                theo_bam[(co, hashlib.sha1(p.read_bytes()).hexdigest())].append(p.relative_to(goc).as_posix())
        except OSError:
            continue
    for ds in theo_bam.values():
        if len(ds) > 1:
            loi["7 TRÙNG"].append(("⚠", " = ".join(ds[:4]) + (f" (+{len(ds) - 4})" if len(ds) > 4 else "")))

    n_chan = 0
    for muc in ("1 GỐC", "2 TÊN", "3 TỰ NẠP", "4 TẠM", "5 BÁO CÁO", "6 MỒ CÔI", "7 TRÙNG"):
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
