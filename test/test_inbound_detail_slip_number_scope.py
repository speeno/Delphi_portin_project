"""입고 상세 전표번호/행 스코프 회귀 — 2026-08-22 사용자 "전표번호 이상" 리포트.

증상
----
입고접수 상세의 전표번호가 목록과 달랐다. 원인 2계층:

1. **백엔드 (근본 원인)** — 상세/수정/취소 SQL 이 헤더키
   ``(Gdate, Hcode, Gcode, Jubun)`` 만 쓰고 ``Scode='Y'`` 를 걸지 않았다.
   이 좌표는 거래처 간 **공유 키**라(DEC-080 SLIP_KEY_AMBIGUOUS) 같은 키에 출고
   (``Scode='X'``) 행이 함께 있을 수 있고, 목록은 ``Scode='Y'`` 로 입고만 집계하므로
   상세의 ``MAX(Idnum+0)`` 가 **출고 전표의 Idnum** 을 집어 번호가 어긋났다.
   같은 이유로 상세 라인에 출고 라인이 섞이고, 취소/라인 UPDATE·DELETE 가 출고
   전표를 함께 건드릴 수 있었다(데이터 훼손 위험).

2. **프론트 (증상 증폭)** — 상세가 ``formatIdnumDisplay(idnum) || receipt_key.jubun``
   으로 폴백해, Idnum 이 0 이면 12자리 **Jubun(거래처별 차수)** 을 전표번호 자리에
   노출했다. DEC-108 이 감사 대상으로 남겨둔
   "``inbound/receipts/[receiptKey]:271`` (입고 체계 확인 요)" 항목이다.
   레거시 정본 Sobo22 는 ``Edit109 = Format('%05s', Idnum)`` 이므로 Idnum 이 정본이고,
   없으면 목록과 동일하게 ``—`` 로 둔다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

import app.services.inbound_service as inb  # noqa: E402

KEY = dict(gdate="2026.08.21", hcode="5019", gcode="V001", jubun="120000000001")


class InboundRowScopeSqlTests(TestCase):
    """§1 — S1_Ssub 를 건드리는 모든 입고 SQL 이 Scode='Y' 로 좁혀져 있다."""

    def test_s1_ssub_statements_carry_scode(self) -> None:
        for name in (
            "SQL_DETAIL_LINES",
            "SQL_UPDATE_LINE",
            "SQL_DELETE_LINE",
            "SQL_CANCEL_RECEIPT",
        ):
            sql = getattr(inb, name)
            self.assertIn("S1_Ssub", sql, name)
            self.assertIn("Scode='Y'", sql, f"{name} 에 Scode='Y' 스코프가 없다")

    def test_memo_statements_do_not_carry_scode(self) -> None:
        """S1_Memo 에는 Scode 컬럼이 없다 — 붙이면 1054 로 상세가 깨진다."""
        for name in ("SQL_MEMO_SELECT", "SQL_MEMO_UPDATE"):
            sql = getattr(inb, name)
            self.assertIn("S1_Memo", sql, name)
            self.assertNotIn("Scode", sql, f"{name} 에 Scode 가 붙으면 안 된다")


class InboundDetailIdnumScopeTests(TestCase):
    """§2 — 상세 MAX(Idnum) 가 같은 좌표의 출고 행을 집지 않는다."""

    def _detail(self, *, capture: list):
        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001
            capture.append(sql)
            if "MAX(Idnum" in sql:
                return [{"idnum": 42}]
            if "FROM S1_Ssub" in sql and "SELECT Gdate" in sql:
                return [{
                    "Gdate": KEY["gdate"], "Hcode": KEY["hcode"], "Gcode": KEY["gcode"],
                    "Jubun": KEY["jubun"], "Gjisa": "", "Bcode": "B1", "Pubun": "",
                    "Gsqut": 3, "Gdang": 10000, "Grat1": 70, "Gssum": 21000,
                    "Gbigo": "", "Yesno": "0", "Gubun": "입고", "Ocode": "A", "Scode": "Y",
                }]
            return []

        async def noop(*a, **k):  # noqa: ANN001, ANN202
            return {}

        with patch.object(inb, "execute_query", new=AsyncMock(side_effect=fake_eq)), \
             patch.object(inb, "_present_cols", new=AsyncMock(return_value={"idnum"})), \
             patch.object(inb, "_fetch_product_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "_fetch_publisher_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "_fetch_vendor_names", new=AsyncMock(return_value={})), \
             patch.object(inb, "_attach_isbn", new=AsyncMock(side_effect=noop)):
            return asyncio.run(inb.get_receipt_detail(server_id="remote_153", **KEY))

    def test_idnum_query_is_scoped_to_inbound_rows(self) -> None:
        seen: list[str] = []
        detail = self._detail(capture=seen)
        idnum_sqls = [s for s in seen if "MAX(Idnum" in s]
        self.assertTrue(idnum_sqls, "MAX(Idnum) 조회가 실행되지 않았다")
        for sql in idnum_sqls:
            self.assertIn("Scode='Y'", sql, "전표번호 조회가 출고 행까지 스캔한다")
        self.assertEqual(detail["idnum"], 42)

    def test_detail_lines_query_is_scoped(self) -> None:
        seen: list[str] = []
        self._detail(capture=seen)
        line_sqls = [s for s in seen if "SELECT Gdate" in s and "FROM S1_Ssub" in s]
        self.assertTrue(line_sqls)
        for sql in line_sqls:
            self.assertIn("Scode='Y'", sql, "상세 라인 조회에 출고 라인이 섞일 수 있다")


class InboundCancelScopeTests(TestCase):
    """§3 — 소프트 취소가 같은 좌표의 출고 전표를 함께 취소하지 않는다."""

    def test_cancel_reads_and_writes_only_inbound_rows(self) -> None:
        seen: list[str] = []

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001
            seen.append(sql)
            return [{"Yesno": "0"}]

        async def fake_tx(server_id, statements):  # noqa: ANN001
            seen.extend(s for s, _ in statements)
            return None

        with patch.object(inb, "execute_query", new=AsyncMock(side_effect=fake_eq)), \
             patch.object(inb, "execute_in_transaction", new=AsyncMock(side_effect=fake_tx)):
            asyncio.run(inb.cancel_receipt(server_id="remote_153", **KEY))

        touched = [s for s in seen if "S1_Ssub" in s]
        self.assertTrue(touched)
        for sql in touched:
            self.assertIn("Scode='Y'", sql, f"입고 취소가 출고 행을 건드린다: {sql[:90]}")


class SlipNumberFrontendTests(TestCase):
    """§4 — 상세 화면이 Jubun 을 전표번호로 표시하지 않는다 (DEC-108 감사 항목 종결)."""

    def setUp(self) -> None:
        self.detail = (
            FRONT / "app" / "(app)" / "inbound" / "receipts" / "[receiptKey]" / "page.tsx"
        ).read_text(encoding="utf-8")
        self.new = (
            FRONT / "app" / "(app)" / "inbound" / "receipts" / "new" / "page.tsx"
        ).read_text(encoding="utf-8")

    def test_detail_does_not_fall_back_to_jubun(self) -> None:
        self.assertIn("formatIdnumDisplay(detail.idnum)", self.detail)
        self.assertNotIn(
            "formatIdnumDisplay(detail.idnum) || detail.receipt_key.jubun", self.detail
        )

    def test_new_page_banner_shows_idnum_not_jubun(self) -> None:
        """저장 배너도 서버 채번 Idnum 을 쓴다(종전 `savedKey.jubun` 노출)."""
        self.assertIn("formatIdnumDisplay(savedIdnum)", self.new)
        self.assertNotIn("savedKey.jubun}이(가) 저장", self.new)


if __name__ == "__main__":
    main()
