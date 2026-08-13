"""DEC-150 — 지점관리(H2_Gbun) 패널 라벨 = Seok01.dfm 정본 캡션 회귀 가드.

2026-08-13 영업팀 확인 요청("내용각각→지점관리, 지점별 공급율") 분석 결과:
기능·데이터·격리는 웹에 이미 이식돼 있고(거래처 상세 지점 패널, 전자책 5097
B2B/C|50% 조회 확인), 유일한 갭 = 라벨이 DFM 정본과 어긋난 오라벨.

정본(유통 chul_09·출판 New 전 빌드 Seok01.dfm 동일):
  지역(JUBUN) · 지점명(GNAME) · 코드(ONAME) · 구분(GDATE) · 번호(GNUM1) · 출고정지(GBIGO)
종전 웹 오라벨: 지사코드(jubun)/담당(oname)/일자(gdate)/정지사유(gbigo).
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
PANEL = (ROOT / "도서물류관리프로그램" / "frontend" / "src" / "components"
         / "master" / "customer-branch-panel.tsx")
COLLAPSIBLE = (ROOT / "도서물류관리프로그램" / "frontend" / "src" / "components"
               / "master" / "customer-branch-collapsible.tsx")


class BranchPanelLabelGuard(TestCase):
    def test_grid_columns_match_dfm_captions(self) -> None:
        src = PANEL.read_text(encoding="utf-8")
        for needle in (
            '{ key: "jubun", label: "지역"',
            '{ key: "gname", label: "지점명"',
            '{ key: "oname", label: "코드"',
            '{ key: "gdate", label: "구분"',
            '{ key: "gbigo", label: "출고정지"',
        ):
            self.assertIn(needle, src)
        for stale in ('label: "지사코드"', 'label: "담당"', 'label: "정지사유"'):
            self.assertNotIn(stale, src, "구 오라벨 재발 금지")

    def test_form_labels_match_dfm_captions(self) -> None:
        src = PANEL.read_text(encoding="utf-8")
        for needle in (
            '<Label htmlFor="branch-jubun">지역</Label>',
            '<Label htmlFor="branch-gname">지점명</Label>',
            '<Label htmlFor="branch-oname">코드</Label>',
            '<Label htmlFor="branch-gdate">구분</Label>',
            '<Label htmlFor="branch-gnum1">번호</Label>',
            '<Label htmlFor="branch-gbigo">출고정지 사유</Label>',
        ):
            self.assertIn(needle, src)

    def test_collapsible_titled_after_legacy_popup(self) -> None:
        src = COLLAPSIBLE.read_text(encoding="utf-8")
        self.assertIn('title="지점관리 (지사)"', src)
        self.assertIn("공급율", src, "지점명 공급율 기입 관례 안내 유지")


if __name__ == "__main__":
    main()
