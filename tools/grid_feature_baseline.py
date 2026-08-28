#!/usr/bin/env python3
"""표(목록) 기능 기준선 — 디자인 변경이 기존 표 기능을 떨어뜨리지 않았는지 확인 (DEC-212, 2026-08-26).

사용자 규칙(2026-08-26): "이번 디자인 변경으로 이런 기존 기능에 대한 누락이나 제거는 이후에 꼭 확인 과정을
거쳐서 진행해야 한다." — 화면별로 표 기능 지표를 세어 `analysis/audit/grid-feature-baseline.json` 에 기록하고,
CI(테스트)에서 **어느 화면이든 지표가 기준선보다 줄면 실패**한다.

지표(파일당 출현 수)
  data_grid          <DataGrid            공용 표 사용
  column_settings    <GridColumnSettings  컬럼 추가/삭제(표시) 설정
  sortable           sortable: true       정렬 가능 컬럼
  reorder            onColumnReorder      컬럼 좌우 드래그 이동
  resize             onColumnResize       컬럼 폭 조절
  keyboard           enableKeyboardNav    키보드 행 이동
  pager              pager={              페이저

사용
  python3 tools/grid_feature_baseline.py            # 기준선 재생성(의도한 변경 후)
  python3 tools/grid_feature_baseline.py --check    # 현재 vs 기준선 — 줄어든 지표가 있으면 exit 1
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
BASELINE = ROOT / "analysis" / "audit" / "grid-feature-baseline.json"

METRICS = {
    "data_grid": "<DataGrid",
    "column_settings": "<GridColumnSettings",
    "sortable": "sortable: true",
    "reorder": "onColumnReorder",
    "resize": "onColumnResize",
    "keyboard": "enableKeyboardNav",
    "pager": "pager={",
    "freeze": "frozenUntil={",
}


def scan() -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    files = sorted(list((FRONT / "app" / "(app)").glob("**/*.tsx")) + list((FRONT / "components").glob("**/*.tsx")))
    for f in files:
        rel = str(f.relative_to(FRONT))
        if rel.startswith("components/data-grid/"):
            continue  # 공용 구현 자체는 제외
        src = f.read_text(encoding="utf-8")
        counts = {k: src.count(v) for k, v in METRICS.items()}
        if any(counts.values()):
            out[rel] = counts
    return out


def check(current: dict[str, dict[str, int]], baseline: dict[str, dict[str, int]]) -> list[str]:
    problems: list[str] = []
    for rel, base in baseline.items():
        cur = current.get(rel)
        if cur is None:
            problems.append(f"{rel}: 파일이 사라짐(표 기능 {sum(base.values())}개)")
            continue
        for k, b in base.items():
            if cur.get(k, 0) < b:
                problems.append(f"{rel}: {k} {b} → {cur.get(k, 0)}")
    return problems


def main() -> int:
    current = scan()
    if "--check" in sys.argv:
        if not BASELINE.exists():
            print(f"[grid-feature-baseline] 기준선 없음: {BASELINE}")
            return 2
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))["files"]
        problems = check(current, baseline)
        if problems:
            print("[grid-feature-baseline] 표 기능이 기준선보다 줄었습니다 — 의도한 변경이면 기준선을 재생성하세요:")
            for p in problems:
                print("  -", p)
            return 1
        print(f"[grid-feature-baseline] OK — {len(baseline)} files, 줄어든 지표 없음")
        return 0
    BASELINE.parent.mkdir(parents=True, exist_ok=True)
    BASELINE.write_text(
        json.dumps({"metrics": METRICS, "files": current}, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"[grid-feature-baseline] wrote {BASELINE} ({len(current)} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
