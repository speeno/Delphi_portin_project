"""DEC-282 — 조정 원장(원장변경 Sobo51 · 재고변경 Sobo52) 백엔드 가드 (2026-09-12).

레거시 「자료관리 > 원장변경/재고변경」 포팅. 두 화면은 같은 모양의 조정 테이블을 쓴다:
원장변경 = Sg_Gsum(Scode='X', 거래처), 재고변경 = Sg_Csum(Scode='A', 도서).
축 차이는 서비스의 ``_AXES`` **데이터**로만 표현한다(화면·테넌트 분기 금지).

⚠ ``Sg_Csum.Gbsum``(변경수량)은 재고 산식의 세 소스 중 하나(DEC-138/274) — 재고변경 저장은
재고를 움직인다. 모든 경로가 회사(Hcode)로 격리되어야 한다.

라이브 대조(읽기 전용, remote_153/chul_09_db/5019, 2026-01-01~09-12):
  재고변경 41행 · 대조 4,763 / 원장 4,232 / 변경 856 = 레거시 화면 일치
  원장변경 합계 161,184,072 / 164,026,187 / −1,000,000 = 레거시 화면 일치
"""

from __future__ import annotations

import asyncio
import re
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

_HUB = Path(__file__).resolve().parents[1]
_BACKEND = _HUB / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND))

from app.services import adjustment_ledger_service as svc  # noqa: E402


def _run(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


ROWS = [
    {"id": 1, "Gdate": "2026.01.14", "Gcode": "80063", "Gssum": 25, "Gosum": 51, "Gbsum": -26, "Gbigo": "실재고"},
    {"id": 2, "Gdate": "2026.01.31", "Gcode": "1108", "Gssum": -140, "Gosum": -153, "Gbsum": 13, "Gbigo": "정용섭"},
]


class AxisDataTests(TestCase):
    def test_two_axes_are_data_not_branches(self) -> None:
        a = svc.axes()
        self.assertEqual(set(a), {"customer", "book"})
        self.assertTrue(a["book"]["auto_ledger_value"], "재고변경은 원장재고 자동조회 지원")
        self.assertFalse(a["customer"]["auto_ledger_value"], "원장변경은 1차 미지원(직접 입력)")

    def test_axis_tables_and_scodes(self) -> None:
        self.assertEqual(svc.axis_config("customer")["table"], "Sg_Gsum")
        self.assertEqual(svc.axis_config("customer")["scode"], "X")
        self.assertEqual(svc.axis_config("book")["table"], "Sg_Csum")
        self.assertEqual(svc.axis_config("book")["scode"], "A")

    def test_unknown_axis_raises(self) -> None:
        with self.assertRaises(svc.UnknownAxisError):
            svc.axis_config("nope")

    def test_service_has_no_tenant_literals(self) -> None:
        src = (_BACKEND / "app" / "services" / "adjustment_ledger_service.py").read_text(encoding="utf-8")
        for needle in ("5019", "remote_153", "chul_09", "교문사"):
            self.assertNotIn(needle, src, f"서비스에 테넌트 리터럴 {needle}")

    def test_sql_is_mysql3_safe(self) -> None:
        src = (_BACKEND / "app" / "services" / "adjustment_ledger_service.py").read_text(encoding="utf-8")
        self.assertNotRegex(src, re.compile(r"\bCAST\s*\(|\bCASE\s+WHEN\b|COALESCE\s*\(", re.I))
        self.assertNotRegex(src, re.compile(r"FROM\s*\(\s*SELECT", re.I), "파생 테이블 금지(1064)")

    def test_gdate_normalized_to_legacy_format(self) -> None:
        self.assertEqual(svc.normalize_gdate("2026-09-12"), "2026.09.12")
        self.assertEqual(svc.normalize_gdate("20260912"), "2026.09.12")
        self.assertEqual(svc.normalize_gdate("2026.9.2"), "2026.09.02")


class ListTests(TestCase):
    def _call(self, axis="book", q=None, limit=100, offset=0):
        async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
            self.seen = (sql, tuple(params))
            return list(ROWS)

        async def fake_in(server_id, *, sql_template, keys, prefix_params=(), chunk_size=None):  # noqa: ANN001
            return [{"Gcode": "80063", "Gname": "원서A"}, {"Gcode": "1108", "Gname": "패션"}]

        with patch.object(svc, "execute_query", new=AsyncMock(side_effect=fake_exec)), \
             patch("app.core.sql_mysql3.in_clause_lookup", new=AsyncMock(side_effect=fake_in)):
            return _run(svc.list_adjustments(
                server_id="s", axis=axis, hcode="5019",
                date_from="2026-01-01", date_to="2026-09-12", q=q, limit=limit, offset=offset,
            ))

    def test_rows_are_hcode_and_axis_scoped(self) -> None:
        out = self._call()
        sql, params = self.seen
        self.assertIn("Sg_Csum", sql)
        self.assertIn("Hcode = %s", sql)
        self.assertIn("Scode = %s", sql)
        self.assertEqual(params[:2], ("5019", "A"))
        self.assertEqual(params[2:], ("2026.01.01", "2026.09.12"), "일자는 레거시 표기로 정규화")
        self.assertEqual(out["items"][0]["gname"], "원서A", "코드→이름 보충")

    def test_totals_cover_whole_result_not_page(self) -> None:
        out = self._call(limit=1)
        self.assertEqual(len(out["items"]), 1)
        self.assertEqual(out["page"]["total"], 2)
        self.assertEqual(out["totals"], {"gssum": -115, "gosum": -102, "gbsum": -13})

    def test_q_filters_code_name_and_memo(self) -> None:
        self.assertEqual(len(self._call(q="80063")["items"]), 1)
        self.assertEqual(len(self._call(q="패션")["items"]), 1)
        self.assertEqual(len(self._call(q="정용섭")["items"]), 1)
        self.assertEqual(len(self._call(q="없는말")["items"]), 0)


class WriteTests(TestCase):
    def test_create_defaults_diff_to_matched_minus_ledger(self) -> None:
        seen: dict = {}

        async def fake_tx(server_id, statements):  # noqa: ANN001
            seen["sql"], seen["params"] = statements[0]
            return [1]

        async def fake_exec(server_id, sql, params=()):  # noqa: ANN001
            if "MAX(id)" in sql:
                return [{"id": 7}]
            return [{"id": 7, "Gdate": "2026.09.12", "Gcode": "3253", "Gssum": 10, "Gosum": 4, "Gbsum": 6, "Gbigo": ""}]

        async def fake_in(server_id, **kw):  # noqa: ANN001
            return []

        with patch.object(svc, "execute_in_transaction", new=AsyncMock(side_effect=fake_tx)), \
             patch.object(svc, "execute_query", new=AsyncMock(side_effect=fake_exec)), \
             patch("app.core.sql_mysql3.in_clause_lookup", new=AsyncMock(side_effect=fake_in)):
            row = _run(svc.create_adjustment(
                server_id="s", axis="book", hcode="5019",
                payload={"gdate": "2026-09-12", "gcode": "3253", "gssum": 10, "gosum": 4, "gbigo": ""},
            ))
        self.assertEqual(row["id"], 7)
        self.assertIn("INSERT INTO Sg_Csum", seen["sql"])
        self.assertEqual(seen["params"][0], "5019", "회사 코드가 첫 바인딩")
        self.assertEqual(seen["params"][2], "A", "축 Scode 고정")
        self.assertEqual(seen["params"][6], 6, "변경수량 기본 = 대조 − 원장")

    def test_create_requires_date_and_code(self) -> None:
        with self.assertRaises(ValueError):
            _run(svc.create_adjustment(server_id="s", axis="book", hcode="5019",
                                       payload={"gdate": "", "gcode": "3253"}))
        with self.assertRaises(ValueError):
            _run(svc.create_adjustment(server_id="s", axis="book", hcode="5019",
                                       payload={"gdate": "2026-09-12", "gcode": ""}))

    def test_update_and_delete_are_row_isolated(self) -> None:
        seen: list = []

        async def fake_tx(server_id, statements):  # noqa: ANN001
            seen.append(statements[0])
            return [0]  # 0행 = 없거나 다른 회사 행

        with patch.object(svc, "execute_in_transaction", new=AsyncMock(side_effect=fake_tx)):
            with self.assertRaises(svc.AdjustmentNotFoundError):
                _run(svc.update_adjustment(server_id="s", axis="book", hcode="5019",
                                           row_id=9, payload={"gssum": 1}))
            with self.assertRaises(svc.AdjustmentNotFoundError):
                _run(svc.delete_adjustment(server_id="s", axis="book", hcode="5019", row_id=9))
        for sql, params in seen:
            self.assertIn("Hcode = %s", sql, "행 격리 없는 쓰기 금지")
            self.assertIn("Scode = %s", sql)
            self.assertIn("5019", [str(p) for p in params])


class LedgerValueTests(TestCase):
    def test_book_axis_uses_verified_stock_formula(self) -> None:
        with patch("app.services.reports_service._fetch_stock_asof",
                   new=AsyncMock(return_value={"3253": 869})) as f:
            out = _run(svc.ledger_value(server_id="s", axis="book", hcode="5019",
                                        gcode="3253", asof="2026-04-23"))
        self.assertEqual(out, {"supported": True, "gosum": 869})
        kw = f.await_args.kwargs
        self.assertEqual(kw["asof"], "2026.04.23")
        self.assertEqual(kw["axis_like"], "%A%", "레거시 Subu52 는 본사 축으로 계산")
        self.assertEqual(kw["hcode"], "5019")

    def test_customer_axis_is_not_supported_yet(self) -> None:
        out = _run(svc.ledger_value(server_id="s", axis="customer", hcode="5019",
                                    gcode="2057", asof="2026-01-26"))
        self.assertEqual(out, {"supported": False, "gosum": 0})


class RouterWiringTests(TestCase):
    def test_routes_registered_and_hcode_enforced(self) -> None:
        src = (_BACKEND / "app" / "routers" / "ledger_adjustments.py").read_text(encoding="utf-8")
        self.assertIn('prefix="/api/v1/ledger/adjustments"', src)
        self.assertIn("enforce_hcode_identity", src)
        self.assertIn("require_server_ownership", src)
        main = (_BACKEND / "app" / "main.py").read_text(encoding="utf-8")
        self.assertIn("ledger_adjustments.router", main)

    def test_smoke_matrix_registers_the_new_get(self) -> None:
        probe = (_HUB / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("ledger/adjustments", probe, "새 라우터 GET 은 스모크 매트릭스에 등록한다")


if __name__ == "__main__":
    main()
