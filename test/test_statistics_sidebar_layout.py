"""DEC-348 — 통계관리 하위 메뉴 순서 (2026-09-30, 교문사 경리부 「카테고리 순서 변경요청」).

요청 순서: 도서별판매, 거래처별판매, 도서별판매(일별), 거래처판매(일별), 도서별판매(월별), 거래처판매(월별),
도서별판매(년/월), 거래처판매(년/월), 월별통계, 거래처통계(목록), 도서통계(목록), 도서별년말집계,
기간별 매출분석, 거래처별판매분석, 도서회전율, 분기/반기 손익.

배치표(SIDEBAR_LAYOUTS)가 있는 그룹은 **배치표에 적힌 폼만** 사이드바에 나온다 — 통계관리에 화면을 추가하고
배치표에 넣지 않으면 메뉴에서 사라지므로, 등록된 화면이 전부 배치표에 있는지도 함께 지킨다.
(런타임 없이 form-registry.ts 소스만 파싱 — test_shipment_sidebar_layout.py 와 같은 정책.)
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "form-registry.ts"

REQUESTED = [
    ("Sobo61", "도서별판매"),
    ("Sobo62", "거래처별판매"),
    ("Sobo79_3", "도서별판매(일별)"),
    ("Sobo79_4", "거래처판매(일별)"),
    ("Sobo79_1", "도서별판매(월별)"),
    ("Sobo79_2", "거래처판매(월별)"),
    ("Sobo73", "도서별판매(년/월)"),
    ("Sobo74", "거래처판매(년/월)"),
    ("Stats_monthly", "월별통계"),
    ("Sobo36_stats_route", "거래처통계(목록)"),
    ("Sobo37_stats_route", "도서통계(목록)"),
    ("Sobo67_yearbook", "도서별년말집계"),
    ("Sobo50_stats", "기간별 매출 분석"),
    ("Sobo51_stats", "거래처별 판매 분석"),
    ("Sobo52_stats", "도서 회전율"),
    ("Sobo53_stats", "분기/반기 손익"),
]


class StatisticsSidebarLayoutTest(TestCase):
    def setUp(self) -> None:
        self.src = REGISTRY.read_text(encoding="utf-8").replace("\r\n", "\n")

    def _layout_ids(self) -> list[str]:
        block = re.search(
            r"export const STATISTICS_SIDEBAR_LAYOUT:[\s\S]*?=\s*\[(?P<body>[\s\S]*?)\];", self.src
        )
        self.assertIsNotNone(block, "STATISTICS_SIDEBAR_LAYOUT 상수가 필요합니다.")
        return re.findall(r'formId:\s*"([^"]+)"', block.group("body"))

    def _registry_blocks(self) -> list[str]:
        body = self.src.split("export const FORM_REGISTRY: FormMeta[] = [", 1)[1]
        return [b for b in re.split(r"\n  \{\n", body) if 'menuGroup: "statistics"' in b.split("\n  },")[0]]

    def test_requested_order(self) -> None:
        ids = self._layout_ids()
        self.assertEqual(ids[: len(REQUESTED)], [fid for fid, _ in REQUESTED])

    def test_captions_match_the_request(self) -> None:
        for fid, caption in REQUESTED:
            with self.subTest(form_id=fid):
                m = re.search(
                    r'id:\s*"' + re.escape(fid) + r'",[\s\S]{0,600}?menuGroup:\s*"statistics"', self.src
                )
                self.assertIsNotNone(m, f"{fid} 는 통계관리 그룹")
                self.assertIn(f'caption: "{caption}"', m.group(0), fid)

    def test_layout_registered(self) -> None:
        block = re.search(r"export const SIDEBAR_LAYOUTS:[\s\S]*?=\s*\{(?P<body>[\s\S]*?)\};", self.src)
        self.assertIsNotNone(block)
        self.assertIn("statistics: STATISTICS_SIDEBAR_LAYOUT", block.group("body"))

    def test_every_visible_statistics_form_is_in_the_layout(self) -> None:
        """배치표에 없는 폼은 사이드바에서 사라진다 — 감춘(hidden) 폼만 빠질 수 있다."""
        ids = set(self._layout_ids())
        missing = []
        for blk in self._registry_blocks():
            head = blk.split("\n  },")[0]
            fid = re.search(r'id:\s*"([^"]+)"', head)
            if not fid:
                continue
            hidden = bool(re.search(r"\bhidden:\s*true", head)) or "hiddenReason" in head
            if not hidden and fid.group(1) not in ids:
                missing.append(fid.group(1))
        self.assertEqual(missing, [], "배치표에 없는 통계관리 화면(메뉴에서 사라진다)")

    def test_no_duplicates_and_no_unknown_forms(self) -> None:
        ids = self._layout_ids()
        self.assertEqual(len(ids), len(set(ids)))
        for fid in ids:
            self.assertRegex(self.src, r'id:\s*"' + re.escape(fid) + r'"', fid)


if __name__ == "__main__":
    main()
