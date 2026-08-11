"""DEC-144 — 통계 필터바 Enter 흐름 마감: 집계단위 픽 필드화 + 룩업 빈값 Enter 통과.

2026-08-11 영업팀(기간별 매출분석·거래처별 판매분석):
① "집계단위 선택 후 '엔터' 조회가 안 됩니다" — 네이티브 <select> 드롭다운의
  확정 Enter 를 OS 메뉴가 소비(DOM 미도달). → LocalComboField(픽 필드) 교체:
  Enter=팝업→↑↓ 선택→Enter=값+다음 칸(마지막이면 자동 조회).
② "거래처코드 선택 후 '엔터'로 다음탭이 안 넘어갑니다" — 필터바 룩업에
  onKeyDown 미전달 → 빈값 Enter 가 다음 이동 대신 검색 팝업을 열었다
  (확립 규약: MLF 빈값 Enter 통과, DEC-104/105). no-op onKeyDown 전달로 통과.
  확정값 Enter 이동은 DEC-134 정확일치 자동확정 경로가 담당(기존 배포분).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class FilterBarEnterGuards(TestCase):
    def _src(self) -> str:
        return (FRONT / "components" / "stats" / "stats-filter-bar.tsx").read_text(
            encoding="utf-8"
        )

    def test_groupby_is_pick_field_not_native_select(self) -> None:
        src = self._src()
        self.assertIn("LocalComboField", src, "집계단위 픽 필드 회귀 — DEC-144")
        self.assertIn("advanceAfterSelect", src)
        # 집계단위 네이티브 select 부활 금지 (분기/년 등 showQuarter 계열은 범위 외).
        groupby_block = src.split("showGroupBy ?")[1].split(": null}")[0]
        self.assertNotIn("<select", groupby_block,
                         "집계단위가 네이티브 select 로 회귀 — Enter 확정이 OS 에 소비됨")
        self.assertIn("Combo_GroupBy", groupby_block, "Enter 스톱 id 유지")

    def test_lookups_pass_noop_onkeydown(self) -> None:
        # MLF 빈값 Enter 통과 규약(DEC-104/105) — 룩업 5개 모두 onKeyDown 전달.
        src = self._src()
        self.assertGreaterEqual(
            src.count("onKeyDown={() => {}}"), 5,
            "필터바 룩업 빈값 Enter 통과(no-op onKeyDown) 회귀 — DEC-144",
        )


if __name__ == "__main__":
    main()
