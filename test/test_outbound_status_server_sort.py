"""출고현황(Subu24) 서버 정렬 회귀 — 전체 결과 정렬 후 페이징.

사용자 보고(2026-07-05): 출고현황 표에서 정렬 시 로딩된 페이지만 정렬됨(클라이언트 정렬).
서버가 ORDER BY 로 전체 정렬 후 LIMIT/OFFSET 하도록 변경. 방출 SQL 의 ORDER BY 절을 검증.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import transactions_service as tx  # noqa: E402


async def _capture_slip_sql(*, sort_by, sort_dir) -> str:
    captured: dict = {}

    async def fake_exec(_sid, sql, _params=()):
        captured["sql"] = sql
        return []

    async def fake_cols(_sid):
        return {"idnum", "gdang", "grat1", "pubun"}

    async def fake_g1(*a, **kw):
        return {}

    async def fake_count(*a, **kw):
        return 0

    with patch.object(tx, "execute_query", side_effect=fake_exec), \
         patch("app.services.s1_ssub_adapt.s1_column_names", side_effect=fake_cols), \
         patch.object(tx, "fetch_g1_customer_gnames", side_effect=fake_g1), \
         patch.object(tx, "count_grouped", side_effect=fake_count):
        await tx.list_outbound_status_slips(
            server_id="remote_1", date_from="2026-04-01", date_to="2026-04-30",
            limit=10, offset=0, sort_by=sort_by, sort_dir=sort_dir,
        )
    return captured["sql"]


async def _capture_line_sqls(*, sort_by, sort_dir) -> list[str]:
    captured: list[str] = []

    async def fake_exec(_sid, sql, _params=()):
        captured.append(sql)
        return []

    async def fake_cols(_sid):
        return {"idnum", "gdang", "grat1", "pubun"}

    async def fake_books(*a, **kw):
        return {}

    async def fake_g1(*a, **kw):
        return {}

    with patch.object(tx, "execute_query", side_effect=fake_exec), \
         patch("app.services.s1_ssub_adapt.s1_column_names", side_effect=fake_cols), \
         patch.object(tx, "_fetch_outbound_book_names", side_effect=fake_books), \
         patch.object(tx, "fetch_g1_customer_gnames", side_effect=fake_g1):
        await tx.list_outbound_status_lines(
            server_id="remote_1", date_from="2026-04-01", date_to="2026-04-30",
            limit=10, offset=0, sort_by=sort_by, sort_dir=sort_dir,
        )
    return captured


class OutboundStatusSlipSortTest(IsolatedAsyncioTestCase):
    async def test_default_order_by(self) -> None:
        # 기본 2차 정렬 = 전표번호(idnum alias) — DEC-118(2026-07-21)/DEC-099·108
        # (전표번호 정본=Idnum, Jubun 은 거래처별 차수라 정렬키로 쓰지 않음).
        sql = await _capture_slip_sql(sort_by=None, sort_dir=None)
        self.assertIn("ORDER BY Gdate DESC, idnum", sql)
        self.assertIn("LIMIT %s OFFSET %s", sql)

    async def test_amount_desc(self) -> None:
        sql = await _capture_slip_sql(sort_by="amount", sort_dir="desc")
        self.assertIn("ORDER BY amount DESC", sql)

    async def test_customer_name_sorts_by_code(self) -> None:
        sql = await _capture_slip_sql(sort_by="customer_name", sort_dir="asc")
        self.assertIn("ORDER BY Gcode ASC", sql)

    async def test_unknown_key_falls_back(self) -> None:
        sql = await _capture_slip_sql(sort_by="__evil__ DROP", sort_dir="desc")
        self.assertIn("ORDER BY Gdate DESC, idnum", sql)  # DEC-118 기본 정렬로 폴백
        self.assertNotIn("DROP", sql)

    async def test_no_coalesce_anywhere(self) -> None:
        sql = await _capture_slip_sql(sort_by="qty", sort_dir="asc")
        self.assertNotIn("COALESCE", sql)

    async def test_group_by_includes_gjisa_and_idnum(self) -> None:
        """1전표=1행 — GROUP BY 에 Idnum·Gjisa 포함(전표 흡수 버그 방지, 2026-07-20).

        같은 거래처·Jubun 이지만 지점(Gjisa)만 다른 전표(예: 영풍문고 온라인/종각)가
        한 행으로 흡수돼 낮은 Idnum 전표(전표 2)가 누락되던 회귀 차단.
        """
        sql = await _capture_slip_sql(sort_by="qty", sort_dir="asc")
        gb = sql.split("GROUP BY", 1)[1]
        self.assertIn("IFNULL(Gjisa,'')", gb)
        self.assertIn("IFNULL(Idnum,0)", gb)
        # SELECT 에도 gjisa 노출(order_key 구분용).
        self.assertIn("IFNULL(Gjisa,'') AS gjisa", sql)


class OutboundStatusLineSortTest(IsolatedAsyncioTestCase):
    async def test_default_order_by(self) -> None:
        sqls = await _capture_line_sqls(sort_by=None, sort_dir=None)
        joined = " ".join(sqls)
        # 라인 기본 정렬도 전표번호(idnum alias) 2차 — DEC-118/DEC-099·108.
        self.assertIn("ORDER BY Gdate, idnum", joined)

    async def test_gssum_desc(self) -> None:
        sqls = await _capture_line_sqls(sort_by="gssum", sort_dir="desc")
        self.assertTrue(any("ORDER BY gssum DESC" in s for s in sqls))

    async def test_bname_sorts_by_bcode(self) -> None:
        sqls = await _capture_line_sqls(sort_by="bname", sort_dir="asc")
        self.assertTrue(any("ORDER BY Bcode ASC" in s for s in sqls))


if __name__ == "__main__":
    main()
