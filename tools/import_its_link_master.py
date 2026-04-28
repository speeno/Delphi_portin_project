#!/usr/bin/env python3
"""ITS 노드별 링크정보 CSV를 대시보드용 경량 JSON으로 변환한다.

사용 예:
  python3 tools/import_its_link_master.py \
    "/Users/speeno/Downloads/노드별 링크정보_2023.csv" \
    --output "도서물류관리프로그램/backend/data/its/link_master.json" \
    --link-id 1000000301 --link-id 1000000302
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def _open_csv(path: Path):
    for enc in ("utf-8-sig", "cp949", "euc-kr"):
        try:
            f = path.open("r", encoding=enc, newline="")
            sample = f.read(2048)
            f.seek(0)
            if "LINK_ID" in sample or "링크" in sample or "¸µÅ©" in sample:
                return f
            f.close()
        except UnicodeDecodeError:
            continue
    return path.open("r", encoding="utf-8", errors="replace", newline="")


def _norm(row: dict[str, str]) -> dict[str, object]:
    def pick(*keys: str) -> str:
        lowered = {str(k).lower(): v for k, v in row.items()}
        for key in keys:
            if key in row:
                return (row.get(key) or "").strip()
            val = lowered.get(key.lower())
            if val is not None:
                return str(val).strip()
        return ""

    raw_len = pick("len", "연장(M)", "¿¬Àå(M)")
    try:
        length_m = float(raw_len)
    except ValueError:
        length_m = 0.0
    return {
        "link_id": pick("LINK_ID", "링크아이디", "¸µÅ©¾ÆÀÌµð"),
        "from_node": pick("F_NODE", "시점노드", "½ÃÁ¡³ëµå"),
        "from_node_name": pick("NODE_NAME", "시점노드명", "½ÃÁ¡³ëµå¸í"),
        "to_node": pick("T_NODE", "종점노드", "Á¾Á¡³ëµå"),
        "to_node_name": pick("T_NODE_NAME", "종점노드명"),
        "road_rank": pick("ROAD_RANK", "도로등급"),
        "road_name": pick("ROAD_NAME", "도로명"),
        "length_m": length_m,
        "organ": pick("organ", "링크권역"),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path")
    ap.add_argument("--output", required=True)
    ap.add_argument("--link-id", action="append", default=[])
    args = ap.parse_args()

    source = Path(args.csv_path)
    wanted = {str(x).strip() for x in args.link_id if str(x).strip()}
    out: dict[str, dict[str, object]] = {}
    with _open_csv(source) as f:
        reader = csv.DictReader(f)
        for row in reader:
            norm = _norm(row)
            link_id = str(norm.get("link_id") or "").strip()
            if not link_id:
                continue
            if wanted and link_id not in wanted:
                continue
            out[link_id] = norm

    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {len(out)} links to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
