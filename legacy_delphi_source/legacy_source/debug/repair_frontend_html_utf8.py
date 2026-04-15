"""
Re-save Seak80 sample frontend *.html as UTF-8 (LF).

If an editor saves Korean as CP949 while <meta charset="UTF-8"> stays, browsers show
mojibake. This script reads each file as UTF-8, else CP949/EUC-KR, then writes UTF-8.

Run: python3 debug/repair_frontend_html_utf8.py
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "web" / "seak80-sample" / "frontend"


def load_text(path: Path) -> str:
    b = path.read_bytes()
    if b.startswith(b"\xef\xbb\xbf"):
        return b[3:].decode("utf-8-sig")
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("utf-8", errors="replace")


def main() -> None:
    for p in sorted(ROOT.glob("*.html")):
        s = load_text(p)
        p.write_text(s, encoding="utf-8", newline="\n")
        p.read_bytes().decode("utf-8")
        print("OK", p.name)


if __name__ == "__main__":
    main()
