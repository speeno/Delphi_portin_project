#!/usr/bin/env python3
"""
단일 또는 다수 .dfm에서 레이아웃용 JSON(좌표·캡션·트리)을보낸다.

사용법:
  python3 tools/dfm_layout_export.py <file.dfm> <out.json>
  python3 tools/dfm_layout_export.py --all <source_dir> <out_dir>   # 폼별 <FormName>.json

dfm_parser.parse_dfm_layout 을 사용한다.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
_ROOT = _TOOLS.parent
sys.path.insert(0, str(_TOOLS / "parsers"))
sys.path.insert(0, str(_TOOLS))

from dfm_parser import find_dfm_files, parse_dfm_layout  # noqa: E402


def safe_stem(name: str) -> str:
    return re.sub(r"[^\w\-]+", "_", name)[:120] or "form"


def _attach_pas_resourcestrings(data: dict, dfm_path: str, pas_override: str | None) -> None:
    from pathlib import Path as P

    from res_string_bridge import extract_resourcestrings_from_pas  # noqa: E402

    pas_path = pas_override if pas_override else str(P(dfm_path).with_suffix(".pas"))
    if not P(pas_path).is_file():
        return
    rs = extract_resourcestrings_from_pas(pas_path)
    if rs:
        data["pas_resourcestrings"] = rs


def _parse_layout(dfm_path: str, engine: str) -> dict:
    if engine == "dfm2html":
        from dfm2html_layout_adapter import parse_dfm_layout_via_dfm2html  # noqa: E402

        return parse_dfm_layout_via_dfm2html(dfm_path)
    return parse_dfm_layout(dfm_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="DFM 레이아웃 JSON보내기")
    parser.add_argument("path", help=".dfm 파일 또는 --all 시 소스 루트")
    parser.add_argument("out", help="출력 .json 파일 또는 --all 시 출력 디렉터리")
    parser.add_argument("--all", action="store_true", help="소스 루트 이하 모든 .dfm")
    parser.add_argument(
        "--engine",
        choices=("legacy", "dfm2html"),
        default="legacy",
        help="레이아웃 파서: legacy(기본) 또는 dfm2html_project DfmParser",
    )
    parser.add_argument(
        "--pas",
        default=None,
        help="동일 폼 .pas 경로(생략 시 .dfm 과 같은 stem 의 .pas 가 있으면 자동)",
    )
    args = parser.parse_args()

    if args.all:
        source_dir = args.path
        out_dir = args.out
        os.makedirs(out_dir, exist_ok=True)
        files = find_dfm_files(source_dir)
        for fp in files:
            data = _parse_layout(fp, args.engine)
            # 배치 시에는 stem.pas 자동만(공통 --pas 는 폼별로 맞지 않을 수 있음)
            _attach_pas_resourcestrings(data, fp, None)
            stem = safe_stem(data["form_name"])
            outp = os.path.join(out_dir, f"{stem}.json")
            with open(outp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Wrote {len(files)} layout JSON files under {out_dir}")
        return

    dfm_path = args.path
    out_path = args.out
    if not os.path.isfile(dfm_path):
        print(f"Error: not a file: {dfm_path}", file=sys.stderr)
        sys.exit(1)
    data = _parse_layout(dfm_path, args.engine)
    _attach_pas_resourcestrings(data, dfm_path, args.pas)
    out_abs = os.path.abspath(out_path)
    out_parent = os.path.dirname(out_abs)
    if out_parent:
        os.makedirs(out_parent, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Layout JSON: {out_path}")


if __name__ == "__main__":
    main()
