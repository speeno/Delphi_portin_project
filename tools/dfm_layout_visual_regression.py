#!/usr/bin/env python3
"""
레이아웃 JSON → HTML → PNG 후 기준 PNG와 바이트를 비교한다(선택 CI/로컬).

  pip install playwright
  playwright install chromium

환경 변수 DFM_VISUAL_UPDATE=1 이면 baseline PNG 를 덮어쓴다.

사용법:
  python3 tools/dfm_layout_visual_regression.py <layout.json> <baseline.png>
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT / "parsers") not in sys.path:
    sys.path.insert(0, str(_ROOT / "parsers"))

from dfm_layout_to_html import build_html  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="DFM 레이아웃 HTML PNG 시각 회귀")
    parser.add_argument("layout_json", help="parse_dfm_layout / dfm_layout_export JSON")
    parser.add_argument("baseline_png", help="기준 PNG 경로")
    args = parser.parse_args()

    layout_path = Path(args.layout_json)
    baseline = Path(args.baseline_png)
    doc_text = layout_path.read_text(encoding="utf-8")

    import json

    doc = json.loads(doc_text)
    html_str = build_html(doc)

    png_script = _ROOT.parent / "debug" / "dfm_layout_html_to_png.py"
    if not png_script.is_file():
        print("debug/dfm_layout_html_to_png.py 가 없습니다.", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as td:
        html_path = Path(td) / "layout.html"
        html_path.write_text(html_str, encoding="utf-8")
        out_png = Path(td) / "capture.png"
        cmd = [
            sys.executable,
            str(png_script),
            str(html_path),
            str(out_png),
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(e.stderr or e.stdout or str(e), file=sys.stderr)
            return 2
        except FileNotFoundError:
            print("python 실행 또는 스크립트 경로 오류", file=sys.stderr)
            return 2

        got = out_png.read_bytes()
        update = os.environ.get("DFM_VISUAL_UPDATE", "").strip() in ("1", "true", "yes")

        if not baseline.is_file() or update:
            baseline.parent.mkdir(parents=True, exist_ok=True)
            baseline.write_bytes(got)
            action = "wrote baseline" if update or not baseline.is_file() else "wrote"
            print(f"{action}: {baseline}")
            return 0

        exp = baseline.read_bytes()
        if exp != got:
            print(f"PNG mismatch: {baseline} ({len(exp)} vs {len(got)} bytes)", file=sys.stderr)
            return 1
        print("PNG OK:", baseline)
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
