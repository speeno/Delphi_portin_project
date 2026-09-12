"""DEC-280 — 폐기 접수: 거래처 「애플2」 고정 해지(기타거래처 선택) + 비율 기본 0 (2026-09-12).

사용자 확정: ① 금액은 **현행 유지(0)** — 레거시 관례(Grat1/Gssum=0, DEC-190)를 그대로 두되
화면 기본 할인율 0.7 이 「금액이 왜 0이냐」는 혼동을 만들었으므로 **화면 기본값도 0** 으로 맞춘다.
② 거래처는 **기타거래처(G5_Ggeo)에서 고른다. 비우면 종전대로 「애플2」**.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

_HUB = Path(__file__).resolve().parents[1]
_BACKEND = _HUB / "도서물류관리프로그램" / "backend"
_FE = _HUB / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(_BACKEND))

from app.services import returns_service as rs  # noqa: E402


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class ScrapCustomerResolveTests(TestCase):
    def test_picked_code_is_used_when_present(self) -> None:
        rows = [{"Gcode": "05777", "Gname": "다른기타처"}]
        with patch.object(rs, "execute_query", new=AsyncMock(return_value=rows)) as q:
            code, name = _run(rs.resolve_scrap_customer("remote_153", "5019", "05777"))
        self.assertEqual((code, name), ("05777", "다른기타처"))
        sql, params = q.await_args.args[1], q.await_args.args[2]
        self.assertIn("G5_Ggeo", sql, "기타거래처 마스터에서만 고른다")
        self.assertIn("Hcode = %s", sql)
        self.assertEqual(params, ("5019", "05777"), "회사 범위 안에서 조회")

    def test_picked_code_not_found_fails_closed(self) -> None:
        with patch.object(rs, "execute_query", new=AsyncMock(return_value=[])):
            with self.assertRaises(rs.ScrapCustomerMissingError):
                _run(rs.resolve_scrap_customer("remote_153", "5019", "09999"))

    def test_blank_falls_back_to_legacy_apple2(self) -> None:
        rows = [{"Gcode": "05210", "Gname": "애플2"}]
        with patch.object(rs, "execute_query", new=AsyncMock(return_value=rows)) as q:
            code, name = _run(rs.resolve_scrap_customer("remote_153", "5019", ""))
        self.assertEqual((code, name), ("05210", "애플2"))
        self.assertIn(rs.SCRAP_CUSTOMER_NAME, q.await_args.args[2])

    def test_scrap_insert_keeps_zero_rate_and_amount(self) -> None:
        """금액 현행 유지 — INSERT 는 Grat1/Gssum 0 고정 그대로여야 한다."""
        self.assertIn("'N', %s, %s, 0, 0, %s, NOW())", rs.SQL_INSERT_SCRAP_LINE)


class ScrapScreenTests(TestCase):
    def setUp(self) -> None:
        self.page = (_FE / "app" / "(app)" / "returns" / "scrap" / "new" / "page.tsx").read_text(encoding="utf-8")
        self.axis = (_FE / "components" / "outbound" / "order-line-grid.tsx").read_text(encoding="utf-8")

    def test_customer_is_pickable_from_etc_master(self) -> None:
        self.assertIn('lookupKind="etcCustomer"', self.page)
        self.assertNotIn("애플2 (폐기 전용, 고정)", self.page, "고정 칩은 사라져야 한다")
        self.assertIn("gcode: gcode.trim() || undefined", self.page, "비우면 서버 기본값(애플2)")

    def test_etc_customer_lookup_registered(self) -> None:
        cfg = (_FE / "lib" / "master-lookup-config.ts").read_text(encoding="utf-8")
        self.assertIn('| "etcCustomer"', cfg)
        self.assertIn("etcCustomerApi.list", cfg)

    def test_scrap_rate_default_is_zero(self) -> None:
        self.assertIn("newLine: { ...RETURN_LINE_AXIS.newLine, grat1: 0 }", self.axis)
        self.assertIn("createReturnLine(SCRAP_PUBUN_OPTIONS[0], 0)", self.page)


if __name__ == "__main__":
    main()
