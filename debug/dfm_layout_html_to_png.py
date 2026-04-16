#!/usr/bin/env python3
"""
HTML 파일을 PNG로 캡처한다(Playwright).

  pip install playwright
  playwright install chromium

사용법:
  python3 debug/dfm_layout_html_to_png.py <file.html> <out.png>
  python3 debug/dfm_layout_html_to_png.py <file.html> <out.png> --width 960 --height 720
"""

import argparse
import os
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", help="로컬 HTML 파일")
    parser.add_argument("png", help="출력 PNG")
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=900)
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Playwright가 필요합니다: pip install playwright && playwright install chromium", file=sys.stderr)
        sys.exit(1)

    html_abs = Path(args.html).resolve().as_uri()
    out_png = Path(args.png).resolve()
    out_png.parent.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": args.width, "height": args.height})
        page.goto(html_abs, wait_until="networkidle")
        page.screenshot(path=str(out_png), full_page=True)
        browser.close()

    print(f"Wrote {out_png}")


if __name__ == "__main__":
    main()
