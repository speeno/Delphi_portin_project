"""DEC-139 — 거래처판매 수금액(H1_Ssub 입출금) 집계 회귀 가드.

2026-08-11 교문사-경리부: "거래처판매 수금액이 안 잡힙니다" — 종전 구현이
H1_Ssub 집계를 "후속 C5 이연(D-INQ-4)"으로 0 채움하던 것을 구현.

레거시 정본(출판 Subu62.pas L410~L486):
- 거래처(X/Z) 모드: 수금액 = Σ입금 − Σ출금 / 입고처(Y) 모드: Σ출금 − Σ입금.
- Gcode 단위 집계 → 본사행(gjisa='')의 gjsum 에 부여(DEC-132 필드 의미 정정).
- 수금만 있고 판매가 없는 거래처는 행 신설(레거시 Append 동등).

라이브 대사(2026-08-11): 00227 영광도서 수금액 1,700,000 — 레거시
거래처거래원장 합계와 정확 일치(출고 67/출고액 1,760,365/반품 -2 동시 일치).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import reports_service as rpt  # noqa: E402

S1_ROWS = [
    {"Hcode": "5019", "Gcode": "00227", "Scode": "X", "Gubun": "출고", "Pubun": "",
     "Gjisa": "", "Gdate": "2026.01.26", "Gsqut": 4, "Gssum": 95200},
]


def _fake_db(h1_rows):
    async def fake_exec(server_id, sql, params=()):
        if "FROM H1_Ssub" in sql:
            return h1_rows
        if "FROM S1_Ssub" in sql:
            return S1_ROWS
        return []

    async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
        return [
            {"hcode": "5019", "gcode": k,
             "gname": "영광도서" if k == "00227" else f"거래처{k}"}
            for k in keys
        ]

    return patch.object(rpt, "execute_query", fake_exec), \
        patch.object(rpt, "in_clause_lookup", fake_in)


class CollectionAmountTests(IsolatedAsyncioTestCase):
    async def _run(self, h1_rows, scope="X"):
        p1, p2 = _fake_db(h1_rows)
        with p1, p2:
            return await rpt.get_customer_sales(
                server_id="remote_1", hcode="5019",
                date_from="2026.01.01", date_to="2026.08.10", scope=scope,
            )

    async def test_deposit_minus_withdrawal_on_customer_mode(self) -> None:
        res = await self._run([
            {"Hcode": "5019", "Gcode": "00227", "Gubun": "입금", "Gssum": 2_000_000},
            {"Hcode": "5019", "Gcode": "00227", "Gubun": "출금", "Gssum": 300_000},
        ])
        row = next(r for r in res["rows"] if r["gcode"] == "00227")
        self.assertEqual(row["gjsum"], 1_700_000, "수금액 = 입금 − 출금 (X 모드)")
        # 기존 판매 집계 불변.
        self.assertEqual((row["goqut"], row["gosum"]), (4, 95200))

    async def test_vendor_mode_sign_flipped(self) -> None:
        res = await self._run(
            [
                {"Hcode": "5019", "Gcode": "00227", "Gubun": "입금", "Gssum": 500},
                {"Hcode": "5019", "Gcode": "00227", "Gubun": "출금", "Gssum": 800},
            ],
            scope="Y",
        )
        row = next(r for r in res["rows"] if r["gcode"] == "00227")
        self.assertEqual(row["gjsum"], 300, "입고처(Y) 모드 = 출금 − 입금")

    async def test_collection_only_customer_gets_new_row_with_name(self) -> None:
        res = await self._run([
            {"Hcode": "5019", "Gcode": "00999", "Gubun": "입금", "Gssum": 400_000},
        ])
        row = next(r for r in res["rows"] if r["gcode"] == "00999")
        self.assertEqual(row["gjsum"], 400_000)
        self.assertEqual(row["gname"], "거래처00999", "H1 전용 거래처 이름 lookup")
        self.assertEqual(row["goqut"], 0)

    async def test_h1_absent_tenant_falls_back_to_zero(self) -> None:
        async def fake_exec(server_id, sql, params=()):
            if "FROM H1_Ssub" in sql:
                raise RuntimeError("Table 'H1_Ssub' doesn't exist")
            if "FROM S1_Ssub" in sql:
                return S1_ROWS
            return []

        async def fake_in(server_id, *, sql_template, keys, prefix_params=()):
            return []

        with patch.object(rpt, "execute_query", fake_exec), \
                patch.object(rpt, "in_clause_lookup", fake_in):
            res = await rpt.get_customer_sales(
                server_id="remote_1", hcode="5019",
                date_from="2026.01.01", date_to="2026.08.10",
            )
        row = res["rows"][0]
        self.assertEqual(row["gjsum"], 0, "H1 부재 테넌트는 0 유지(500 금지)")


if __name__ == "__main__":
    main()
