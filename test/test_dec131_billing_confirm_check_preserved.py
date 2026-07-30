"""DEC-131 — 청구서 확정 체크(레거시 CheckBox1=T2.Yesno='1') 보존 회귀 가드.

배경(2026-07-30 사용자 보고)
---------------------------
총판(물류) 청구서관리의 '확인' 체크박스(레거시 Subu45 CheckBox1)는 청구서 발급 후
명세표(거래명세서)가 바뀌어도 청구서 금액이 변하지 않게 하는 잠금이다. 레거시는
T2_Ssub.Yesno='1'(점 표기 월 '2026.07' 행)에 기록하고, 열람 시(DBGrid101DblClick)
체크면 재계산(Button811/812)을 건너뛴다. 저장(Button301) 시 체크면 T3 전 라인도
Yesno='1' 로 잠근다.

웹 결함(교정 대상)
------------------
- `_SQL_CHECK_YESNO` 가 원시 'YYYYMM' 정확 매칭 + LIMIT 1 이라 레거시 확정 행과
  중복 행(유니크 키 부재)을 못 봄 → 확정 월이 재집계로 덮임.
- confirm/cancel 원시 키 UPDATE → 레거시 행만 있는 월에서 0행 갱신(무음 no-op).
- 수동 lines 집계가 T3 잠금 라인을 무가드 DELETE.
- recalc 의 ON DUPLICATE KEY 는 유니크 키 부재로 무력 — 호출마다 중복 '0' 행 삽입.
- 상세 헤더 LIMIT 1 임의 행 — 확정 행 우선이어야 함.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import settlement_service as ss  # noqa: E402
from app.services.settlement_service import PeriodClosedError  # noqa: E402

HCODE = "0013"
MONTH = "202607"


class _Db:
    """SQL 라우팅 페이크 — 실행 이력 캡처."""

    def __init__(self, *, t2_rows=None, t3_locked=None):
        self.t2_rows = t2_rows or []
        self.t3_locked = t3_locked or []
        self.executed: list[tuple[str, tuple]] = []

    async def execute_query(self, server_id, sql, params=None):  # noqa: ARG002
        self.executed.append((sql, tuple(params or ())))
        if "FROM T2_Ssub" in sql and "Yesno" in sql and sql.strip().startswith("SELECT"):
            return self.t2_rows
        if "FROM T3_Ssub" in sql and "Yesno='1'" in sql:
            return self.t3_locked
        return []

    async def execute_in_transaction(self, server_id, statements):  # noqa: ARG002
        self.executed.extend((sql, tuple(p or ())) for sql, p in statements)

    def patches(self):
        return (
            patch.object(ss, "execute_query", new=self.execute_query),
            patch.object(ss, "execute_in_transaction", new=self.execute_in_transaction),
        )


def _run(coro):
    return asyncio.run(coro)


class LegacyConfirmedGuardTests(TestCase):
    """레거시 점 표기('2026.07') 확정 행도 마감 가드가 감지해야 한다."""

    def test_assert_period_open_sees_legacy_dot_row(self) -> None:
        # 월키 정규화 SELECT 가 레거시 행을 돌려주는 상황 — Yesno='1' 이면 423.
        db = _Db(t2_rows=[{"Yesno": "1"}])
        p1, p2 = db.patches()
        with p1, p2, self.assertRaises(PeriodClosedError):
            _run(ss.assert_period_open(server_id="remote_1", gdate=MONTH, hcode=HCODE))

    def test_assert_period_open_sees_confirmed_among_duplicates(self) -> None:
        # 중복 행(웹 '0' + 레거시 확정 '1') — LIMIT 1 임의 행이 아니라 전 행 검사.
        db = _Db(t2_rows=[{"Yesno": "0"}, {"Yesno": "1"}])
        p1, p2 = db.patches()
        with p1, p2, self.assertRaises(PeriodClosedError):
            _run(ss.assert_period_open(server_id="remote_1", gdate=MONTH, hcode=HCODE))

    def test_aggregate_blocked_on_confirmed_month(self) -> None:
        db = _Db(t2_rows=[{"Yesno": "1"}])
        p1, p2 = db.patches()
        with p1, p2, self.assertRaises(PeriodClosedError):
            _run(ss.aggregate_billing(
                server_id="remote_1", gdate=MONTH, hcode=HCODE,
                lines=[{"gdate": "2026.07.01", "gsqut": 1, "gssum": 100}],
            ))

    def test_legacy_empty_yesno_stays_open(self) -> None:
        # 레거시 미체크는 Yesno='' — 마감 아님(재집계 허용).
        db = _Db(t2_rows=[{"Yesno": ""}])
        p1, p2 = db.patches()
        with p1, p2:
            _run(ss.assert_period_open(server_id="remote_1", gdate=MONTH, hcode=HCODE))


class ManualAggregateLockPreservedTests(TestCase):
    """수동 lines 집계 — T3 잠금 라인 보존 + 확정 헤더 보존 + 중복 UPSERT 제거."""

    def _aggregate(self, db: _Db):
        p1, p2 = db.patches()
        with p1, p2:
            return _run(ss.aggregate_billing(
                server_id="remote_1", gdate=MONTH, hcode=HCODE,
                lines=[
                    {"gdate": "2026.07.01", "gsqut": 1, "gssum": 100},
                    {"gdate": "2026.07.15", "gsqut": 2, "gssum": 200},
                ],
            ))

    def test_locked_line_not_deleted_and_not_reinserted(self) -> None:
        db = _Db(t2_rows=[{"Yesno": "0"}], t3_locked=[{"Gdate": "2026.07.15"}])
        self._aggregate(db)
        deletes = [s for s, _ in db.executed if s.startswith("DELETE FROM T3_Ssub")]
        self.assertEqual(len(deletes), 1)
        self.assertIn("<> '1'", deletes[0], "잠금 라인('1')은 DELETE 대상이 아니어야 함")
        inserted_gdates = [
            p[0] for s, p in db.executed if s.startswith("INSERT INTO T3_Ssub")
        ]
        self.assertEqual(inserted_gdates, ["2026.07.01"], "잠금 일자(15일)는 재삽입 금지")

    def test_t2_rebuild_preserves_confirmed_and_no_upsert(self) -> None:
        db = _Db(t2_rows=[{"Yesno": "0"}])
        self._aggregate(db)
        t2_deletes = [s for s, _ in db.executed if s.startswith("DELETE FROM T2_Ssub")]
        self.assertEqual(len(t2_deletes), 1)
        self.assertIn("<> '1'", t2_deletes[0])
        t2_inserts = [s for s, _ in db.executed if s.startswith("INSERT INTO T2_Ssub")]
        self.assertEqual(len(t2_inserts), 1)
        self.assertNotIn("ON DUPLICATE KEY", t2_inserts[0])


class ConfirmLocksLinesTests(TestCase):
    """확정 = 레거시 CheckBox1 체크 저장 — T2 '1' + T3 전 라인 잠금, 월키 정규화."""

    def test_confirm_updates_t2_and_locks_t3(self) -> None:
        db = _Db(t2_rows=[{"Yesno": "0"}])
        p1, p2 = db.patches()
        with p1, p2:
            res = _run(ss.confirm_billing(server_id="remote_1", gdate=MONTH, hcode=HCODE))
        self.assertEqual(res["yesno"], "1")
        updates = [s for s, _ in db.executed if s.startswith("UPDATE")]
        self.assertTrue(any("T2_Ssub SET Yesno='1'" in s for s in updates))
        self.assertTrue(
            any("T3_Ssub SET Yesno='1'" in s for s in updates),
            "확정 시 T3 전 라인 잠금(레거시 Button301 동등)이 실행되어야 함",
        )
        # 월키 정규화 — 레거시 점 표기 행 포함.
        norm = "REPLACE(REPLACE(REPLACE(TRIM("
        for s in updates:
            self.assertIn(norm, s)

    def test_confirm_already_confirmed_duplicate_raises(self) -> None:
        db = _Db(t2_rows=[{"Yesno": "0"}, {"Yesno": "1"}])
        p1, p2 = db.patches()
        with p1, p2, self.assertRaises(PeriodClosedError):
            _run(ss.confirm_billing(server_id="remote_1", gdate=MONTH, hcode=HCODE))


class RecalcNoDuplicateInsertTests(TestCase):
    """recalc — 기존 헤더는 UPDATE(확정 제외 가드), 미존재만 INSERT. 중복 삽입 금지."""

    def _run_recalc(self, db: _Db):
        async def fake_eq(server_id, sql, params=None):  # noqa: ARG001
            db.executed.append((sql, tuple(params or ())))
            if "GssumSum" in sql:
                return [{"Hcode": HCODE, "GssumSum": 1000},
                        {"Hcode": "0007", "GssumSum": 500}]
            if "RGssum" in sql:
                return []
            if "FROM T2_Ssub" in sql:
                # 0013 은 레거시 점 표기 확정 행 존재, 0007 은 T2 미존재.
                return [{"Hcode": HCODE, "Yesno": "1"}]
            return []

        with patch.object(ss, "execute_query", new=fake_eq), patch.object(
            ss, "execute_in_transaction", new=db.execute_in_transaction
        ):
            return _run(ss.recalc_billing(server_id="remote_1", gdate=MONTH))

    def test_confirmed_skipped_and_missing_inserted(self) -> None:
        db = _Db()
        res = self._run_recalc(db)
        self.assertIn(HCODE, res["skipped_closed"], "레거시 확정 행은 일괄 recalc 제외")
        inserts = [(s, p) for s, p in db.executed if s.startswith("INSERT INTO T2_Ssub")]
        updates = [(s, p) for s, p in db.executed if s.startswith("UPDATE T2_Ssub")]
        self.assertEqual(len(inserts), 1, "T2 미존재 거래처(0007)만 INSERT")
        self.assertEqual(inserts[0][1][1], "0007")
        self.assertNotIn("ON DUPLICATE KEY", inserts[0][0])
        for s, _ in updates:
            self.assertIn("<> '1'", s, "UPDATE 는 확정('1') 행 제외 가드 필수")


class DetailPrefersConfirmedRowTests(TestCase):
    """상세 헤더 — 중복 행에서 확정('1') 행 우선 (프론트 자동집계 게이트 신뢰성)."""

    def test_header_sql_orders_confirmed_first(self) -> None:
        self.assertIn("ORDER BY IF(IFNULL(Yesno,'0')='1',0,1)", ss._SQL_BILLING_HEADER)


if __name__ == "__main__":
    main()
