"""마스터 코드 폭 가드 회귀 (DEC-262) — "저장은 됐는데 상세는 404" 재발 방지.

사고(2026-09-08, 교문사 hcode=5019 / remote_153): 거래처 자동채번이 ``J000001``(7자)을
만들었지만 ``G1_Ggeo.Gcode`` 는 ``varchar(5)`` 라 레거시 MySQL(비-strict)이 ``J0000`` 으로
**조용히 잘라** 저장 → 등록 직후 ``GET /masters/customer/J000001`` 이 404.
도서(``G4_Book.Gcode`` varchar(10))·입고처·저자도 동형.

가드 두 겹:
1. 등록 전 ``ensure_code_fits`` 가 폭 초과를 ValueError(MASTER_CODE_TOO_LONG) 로 차단.
2. 라우터가 이를 422 + 한국어 메시지로 변환(``_master_value_error_detail``).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.routers import masters as masters_router  # noqa: E402
from app.services import master_code_width as mcw  # noqa: E402
from app.services import masters_service as ms  # noqa: E402


def _show_columns(type_by_field: dict[str, str]):
    async def fake_exec(_sid, sql, _params=()):
        assert "SHOW COLUMNS" in sql, sql
        return [{"Field": f, "Type": t} for f, t in type_by_field.items()]

    return fake_exec


class CodeColumnMaxLenTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        mcw.clear_code_width_cache_for_tests()

    async def test_reads_varchar_width(self) -> None:
        with patch.object(mcw, "execute_query", side_effect=_show_columns({"Gcode": "varchar(5)"})):
            self.assertEqual(await mcw.code_column_max_len("s", "G1_Ggeo"), 5)

    async def test_reads_char_and_bytes_type(self) -> None:
        # MySQL 3.23 raw 프로토콜은 Type 을 bytes 로 돌려준다.
        async def fake_exec(_sid, _sql, _params=()):
            return [{"Field": "Gcode", "Type": b"char(10)"}]

        with patch.object(mcw, "execute_query", side_effect=fake_exec):
            self.assertEqual(await mcw.code_column_max_len("s", "G4_Book"), 10)

    async def test_non_char_column_returns_none(self) -> None:
        with patch.object(mcw, "execute_query", side_effect=_show_columns({"Gcode": "int(11)"})):
            self.assertIsNone(await mcw.code_column_max_len("s", "T"))

    async def test_query_failure_returns_none_and_does_not_raise(self) -> None:
        async def boom(_sid, _sql, _params=()):
            raise RuntimeError("no db")

        with patch.object(mcw, "execute_query", side_effect=boom):
            self.assertIsNone(await mcw.code_column_max_len("s", "T"))

    async def test_result_is_cached(self) -> None:
        calls = {"n": 0}

        async def counting(_sid, _sql, _params=()):
            calls["n"] += 1
            return [{"Field": "Gcode", "Type": "varchar(5)"}]

        with patch.object(mcw, "execute_query", side_effect=counting):
            await mcw.code_column_max_len("s", "G1_Ggeo")
            await mcw.code_column_max_len("s", "G1_Ggeo")
        self.assertEqual(calls["n"], 1)


class EnsureCodeFitsTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        mcw.clear_code_width_cache_for_tests()

    async def _ensure(self, code: str, width_type: str = "varchar(5)") -> None:
        with patch.object(mcw, "execute_query", side_effect=_show_columns({"Gcode": width_type})):
            await mcw.ensure_code_fits(
                server_id="s", table="G1_Ggeo", code=code, label="거래처코드"
            )

    async def test_fits_exactly(self) -> None:
        await self._ensure("J0000")  # 예외 없음

    async def test_too_long_raises_with_korean_message(self) -> None:
        with self.assertRaises(ValueError) as ctx:
            await self._ensure("J000001")
        text = str(ctx.exception)
        self.assertTrue(text.startswith("MASTER_CODE_TOO_LONG:"), text)
        self.assertIn("거래처코드", text)
        self.assertIn("최대 5자", text)

    async def test_unknown_width_does_not_block(self) -> None:
        await self._ensure("A" * 40, width_type="int(11)")


class CreateMasterCodeGuardTests(IsolatedAsyncioTestCase):
    """등록 경로가 INSERT 전에 폭을 검사한다 — 잘린 행이 남지 않아야 한다."""

    async def test_create_customer_rejects_too_long_code_before_insert(self) -> None:
        inserted: list = []

        async def fake_meta(_sid):
            cols = {"gcode", "gname", "hcode", "gubun"}
            return cols, {c: c.capitalize() for c in cols}

        async def fake_exec(_sid, _sql, _params=()):
            return []

        async def fake_tx(_sid, stmts):
            inserted.extend(stmts)

        async def fake_fits(*, server_id, table, code, column="Gcode", label="코드"):  # noqa: ARG001
            raise ValueError(f"MASTER_CODE_TOO_LONG:{label}는 최대 5자입니다 (입력 {len(code)}자: {code}).")

        with patch.object(ms, "g1_geo_column_meta", new=fake_meta), \
                patch.object(ms, "execute_query", side_effect=fake_exec), \
                patch.object(ms, "execute_in_transaction", side_effect=fake_tx), \
                patch.object(ms, "ensure_code_fits", side_effect=fake_fits):
            with self.assertRaises(ValueError) as ctx:
                await ms.create_customer_master(
                    server_id="s", payload={"gcode": "J000001", "gname": "교문사 테스트"}
                )
        self.assertIn("MASTER_CODE_TOO_LONG", str(ctx.exception))
        self.assertEqual(inserted, [])  # INSERT 미실행

    @staticmethod
    def _fake_db(codes: list[str], captured: dict | None = None):
        """코드 목록 하나로 채번이 쓰는 3종 쿼리(자리수 분포/MAX/중복검사)를 흉내낸다."""
        pool = [c for c in codes if c and c[0] <= "8"]  # SUBSTRING(Gcode,1,1) <= '8'

        async def fake_exec(_sid, sql, params=()):
            if "GROUP BY LENGTH(Gcode)" in sql:
                dist: dict[int, int] = {}
                for c in pool:
                    dist[len(c)] = dist.get(len(c), 0) + 1
                return [{"code_len": n, "row_count": c} for n, c in sorted(dist.items())]
            if "MAX(Gcode)" in sql:
                if captured is not None:
                    captured["sql"], captured["params"] = sql, params
                cand = [c for c in pool if len(c) == params[-1]]
                return [{"mx": max(cand) if cand else None}]
            return [{"Gcode": params[0]}] if params[0] in codes else []

        return fake_exec

    async def test_next_master_code_follows_existing_code_width(self) -> None:
        # DEC-270 — 자리수를 5로 박아 두면 4자리 테넌트의 기존 코드가 집계에서 전부 빠져
        # '00001' 부터 기존 체계와 무관한 코드를 제안했다. 자리수는 실데이터에서 뽑는다.
        captured: dict = {}
        codes = [str(i) for i in range(1, 3419)]  # 1~3418 (1~4자리, 0-패딩 없음)

        async def fake_width(_sid, _table, _column="Gcode"):
            return 10  # G4_Book.Gcode varchar(10)

        with patch.object(ms, "execute_query", side_effect=self._fake_db(codes, captured)), \
                patch.object(ms, "code_column_max_len", side_effect=fake_width):
            code = await ms.next_master_code(server_id="s", table="G4_Book", width=5)
        self.assertEqual(code, "3419")          # 기존 체계(1번부터) 다음 번호
        self.assertEqual(captured["params"][-1], 4)  # 폭 5 고정이 아니라 데이터에서 뽑은 4

    async def test_next_master_code_keeps_zero_padded_scheme(self) -> None:
        # 0-패딩 고정폭 테넌트는 패딩을 그대로 유지한다(00800 → 00801).
        codes = [str(i).zfill(5) for i in range(1, 801)]

        async def fake_width(_sid, _table, _column="Gcode"):
            return 5

        with patch.object(ms, "execute_query", side_effect=self._fake_db(codes)), \
                patch.object(ms, "code_column_max_len", side_effect=fake_width):
            code = await ms.next_master_code(server_id="s", table="G1_Ggeo")
        self.assertEqual(code, "00801")

    async def test_next_master_code_ignores_outlier_long_code(self) -> None:
        # ISBN 등 이물 코드 1건이 자리수를 가로채면 폭 초과(DEC-262)로 되돌아간다 — 유의미한
        # 행 수(전체 1% 또는 최소 2건)를 가진 구간만 자리수 후보로 본다.
        codes = [str(i) for i in range(1, 3419)] + ["9788912345"[:10].replace("9", "8", 1)]

        async def fake_width(_sid, _table, _column="Gcode"):
            return 10

        with patch.object(ms, "execute_query", side_effect=self._fake_db(codes)), \
                patch.object(ms, "code_column_max_len", side_effect=fake_width):
            code = await ms.next_master_code(server_id="s", table="G4_Book", width=5)
        self.assertEqual(code, "3419")

    async def test_next_master_code_skips_codes_already_taken(self) -> None:
        # 교문사(5019) 실사고: 제안 코드가 이미 쓰이고 있으면 409 — 빈 번호까지 밀어야 한다.
        codes = [str(i) for i in range(1, 3419)]
        asked: list[str] = []

        async def fake_width(_sid, _table, _column="Gcode"):
            return 10

        async def fake_taken(*, server_id, table, code, scope_hcode):  # noqa: ARG001
            asked.append(code)
            return code in {"3419", "3420"}

        with patch.object(ms, "execute_query", side_effect=self._fake_db(codes)), \
                patch.object(ms, "code_column_max_len", side_effect=fake_width), \
                patch.object(ms, "_master_code_taken", side_effect=fake_taken):
            code = await ms.next_master_code(server_id="s", table="G4_Book", width=5)
        self.assertEqual(code, "3421")
        self.assertEqual(asked, ["3419", "3420", "3421"])

    async def test_next_master_code_excludes_letter_codes_from_max(self) -> None:
        # 문자 코드(J0000)가 MAX 를 가로채면 숫자 폴백 '00001' 로 떨어진다(DEC-262).
        captured: dict = {}
        codes = ["J0000", "J0001"] + [str(i).zfill(5) for i in range(1, 131)]

        async def fake_width(_sid, _table, _column="Gcode"):
            return 5

        with patch.object(ms, "execute_query", side_effect=self._fake_db(codes, captured)), \
                patch.object(ms, "code_column_max_len", side_effect=fake_width):
            code = await ms.next_master_code(server_id="s", table="G1_Ggeo")
        self.assertEqual(code, "00131")
        self.assertIn("SUBSTRING(Gcode,1,1) <= '8'", captured["sql"])

    async def test_next_master_code_falls_back_when_wider_than_column(self) -> None:
        async def fake_exec(_sid, sql, _params=()):
            return [{"mx": "9999999999"}] if "MAX(Gcode)" in sql else []

        async def fake_width(_sid, _table, _column="Gcode"):
            return 10

        with patch.object(ms, "execute_query", side_effect=fake_exec), \
                patch.object(ms, "code_column_max_len", side_effect=fake_width):
            code = await ms.next_master_code(server_id="s", table="G4_Book", width=10)
        self.assertEqual(code, "")  # 11자 제안 대신 수기 입력 폴백


class RouterErrorDetailTests(TestCase):
    def test_prefixed_value_error_becomes_typed_detail(self) -> None:
        detail = masters_router._master_value_error_detail(
            ValueError("MASTER_CODE_TOO_LONG:거래처코드는 최대 5자입니다 (입력 7자: J000001).")
        )
        self.assertEqual(detail["code"], "MASTER_CODE_TOO_LONG")
        self.assertTrue(detail["message"].startswith("거래처코드는 최대 5자"))

    def test_plain_value_error_keeps_master_invalid(self) -> None:
        detail = masters_router._master_value_error_detail(ValueError("gcode/gname are required"))
        self.assertEqual(detail["code"], "MASTER_INVALID")
        self.assertEqual(detail["message"], "gcode/gname are required")

    def test_colon_in_plain_message_is_not_mistaken_for_a_code(self) -> None:
        detail = masters_router._master_value_error_detail(ValueError("bad value: 3"))
        self.assertEqual(detail["code"], "MASTER_INVALID")


if __name__ == "__main__":
    main()
