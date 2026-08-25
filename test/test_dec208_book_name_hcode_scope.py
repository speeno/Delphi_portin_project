"""DEC-208 — 입고·출고 상세 도서명은 로그인 출판사(hcode) 스코프로 (2026-08-26 사용자 보고).

보고: 신간발행 우측 「선택 전표 라인」에 (1) 전표의 재생 라인까지 함께 보이고 (2) 3063 이 「당신을버릴때」로
나옴 — 교문사 도서가 아님(레거시: 「패션과 영상문화 2판」).

원인/결정
--------
- (2) `inbound_service._fetch_product_names`/`outbound_service._fetch_product_names` 가 G4_Book 을
  **Hcode 없이** 코드로만 찾아 다른 출판사의 같은 코드 도서명을 가져왔다(fail-open). →
  `scope_hcode` 가 있으면 `book_meta_lookup.fetch_book_meta`(로그인 출판사 → Hcode='' 공용 마스터
  2단계, 레거시 Subu24 동등)만 쓴다. 다른 테넌트 행은 절대 쓰지 않는다.
- (1) 신간발행 축(`NEW_RELEASE_AXIS.linePubun="신간"`)은 우측 라인을 전표구분 「신간」으로 거른다 —
  목록 행의 항목수/수량(신간 롤업)과 같은 범위. 입고현황 축은 모든 라인.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"

from app.services import inbound_service as inb  # noqa: E402
from app.services import outbound_service as outb  # noqa: E402


class ScopedProductNames(IsolatedAsyncioTestCase):
    async def test_inbound_uses_hcode_scoped_meta(self) -> None:
        seen: dict = {}

        async def fake_meta(server_id, hcode, bcodes, **kw):
            seen.update(server_id=server_id, hcode=hcode, bcodes=list(bcodes))
            return {"3063": {"gname": "패션과 영상문화 2판", "gdang": 20000, "gisbn": ""}}

        async def boom(*a, **k):
            raise AssertionError("무스코프 IN 조회가 실행되면 안 된다")

        with patch.object(inb, "fetch_book_meta", fake_meta), patch.object(inb, "in_clause_lookup", boom):
            names = await inb._fetch_product_names("remote_153", ["3063", "3422"], scope_hcode="5019")
        self.assertEqual(seen["hcode"], "5019")
        self.assertEqual(names, {"3063": "패션과 영상문화 2판"}, "스코프 밖 코드는 이름 없음(다른 테넌트 도서명 금지)")

    async def test_outbound_uses_hcode_scoped_meta(self) -> None:
        async def fake_meta(server_id, hcode, bcodes, **kw):
            self.assertEqual(hcode, "5019")
            return {"208": {"gname": "2026 자동차정비산업기사실기", "gdang": 18000, "gisbn": "9788900000000"}}

        async def boom(*a, **k):
            raise AssertionError("무스코프 IN 조회가 실행되면 안 된다")

        with patch.object(outb, "fetch_book_meta", fake_meta), patch.object(outb, "in_clause_lookup", boom):
            m = await outb._fetch_product_names("remote_153", ["208"], scope_hcode="5019")
        self.assertEqual(m["208"]["gname"], "2026 자동차정비산업기사실기")

    async def test_unscoped_path_kept_for_admin_wide_lists(self) -> None:
        calls = []

        async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
            calls.append(sql_template)
            return [{"bcode": "1", "gname": "x"}]

        with patch.object(inb, "in_clause_lookup", fake_in):
            names = await inb._fetch_product_names("remote_153", ["1"])
        self.assertEqual(names, {"1": "x"})
        self.assertTrue(calls and "G4_Book" in calls[0])


class CallersPassScope(TestCase):
    def test_inbound_detail_and_lists_pass_hcode(self) -> None:
        src = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "services" / "inbound_service.py").read_text(encoding="utf-8")
        self.assertIn("_fetch_product_names(server_id, bcodes, scope_hcode=hcode)", src)
        self.assertEqual(src.count("_fetch_product_names(server_id, bcodes, scope_hcode=hc) if bcodes else {}"), 2)

    def test_outbound_detail_passes_hcode(self) -> None:
        src = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "services" / "outbound_service.py").read_text(encoding="utf-8")
        self.assertIn("_fetch_product_names(server_id, bcodes, scope_hcode=hcode)", src)


class NewReleaseLineFilter(TestCase):
    def test_axis_filters_right_pane_lines_to_new_release(self) -> None:
        src = (FRONT / "components" / "transactions" / "transaction-status-screen.tsx").read_text(encoding="utf-8")
        self.assertIn("linePubun?: string;", src)
        i = src.index("export const NEW_RELEASE_AXIS")
        self.assertIn('linePubun: "신간"', src[i : i + 800])
        j = src.index("export const INBOUND_STATUS_AXIS")
        self.assertNotIn("linePubun", src[j : src.index("};", j)], "입고현황 축은 모든 라인")
        self.assertIn('axis.linePubun ? res.lines.filter((ln) => (ln.pubun ?? "") === axis.linePubun) : res.lines', src)


if __name__ == "__main__":
    main()
