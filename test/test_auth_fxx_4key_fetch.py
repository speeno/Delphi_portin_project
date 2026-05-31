"""Phase C — fetch_fxx_matrix 3-key (hcode+gname+gcode) 정합 회귀."""
from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, main
from unittest.mock import AsyncMock, patch

_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))

from app.core.auth_provider import LegacyIdLognProvider, parse_fxx_row  # noqa: E402


class FetchFxxFourKeyTest(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.provider = LegacyIdLognProvider()

    async def test_three_key_query_no_limit(self) -> None:
        gy = {"f11": "O", "hcode": "5019", "gname": "교문사", "gcode": "교문사"}
        ac = {"f51": "O", "hcode": "5019", "gname": "교문사", "gcode": "경리부"}
        mock_eq = AsyncMock(side_effect=[[gy], [ac]])
        with patch("app.core.db.execute_query", new=mock_eq):
            r1 = await self.provider.fetch_fxx_matrix(
                "remote_153",
                "교문사",
                db_name="chul_09_db",
                hcode="5019",
                gname="교문사",
            )
            r2 = await self.provider.fetch_fxx_matrix(
                "remote_153",
                "경리부",
                db_name="chul_09_db",
                hcode="5019",
                gname="교문사",
            )
        self.assertEqual(r1, {"F11": "O"})
        self.assertEqual(r2, {"F51": "O"})
        sql1 = mock_eq.await_args_list[0].args[1]
        self.assertIn("hcode = %s AND gname = %s AND gcode = %s", sql1)
        self.assertNotIn("LIMIT", sql1.upper())

    async def test_same_hcode_different_gcode_isolated(self) -> None:
        """5019·동일 gname — 교문사 vs 경리부 Fxx 분리."""
        rows_by_gcode = {
            "교문사": {"F11": "R", "F51": "X"},
            "경리부": {"F51": "O", "F11": "X"},
        }

        async def _fake_eq(_sid, sql, params):
            gcode = params[2]
            row = rows_by_gcode.get(gcode, {})
            return [row] if row else []

        with patch("app.core.db.execute_query", new=AsyncMock(side_effect=_fake_eq)):
            gy = await self.provider.fetch_fxx_matrix(
                "remote_153", "교문사", hcode="5019", gname="교문사"
            )
            gr = await self.provider.fetch_fxx_matrix(
                "remote_153", "경리부", hcode="5019", gname="교문사"
            )
        self.assertEqual(gy.get("F11"), "R")
        self.assertEqual(gy.get("F51"), "X")
        self.assertEqual(gr.get("F51"), "O")
        self.assertEqual(gr.get("F11"), "X")


class MergePermissionsGyomunsaGyeongriTest(IsolatedAsyncioTestCase):
    async def test_gyomunsa_vs_gyeongri_different_permissions(self) -> None:
        from app.services import auth_service

        catalog = {
            "F11": "master.customer.read",
            "F14": "master.alt.read",
            "F17": "master.book_code.write",
            "F51": "report.kpi.read",
            "F52": "report.kpi.write",
            "F53": "report.delivery.read",
            "F54": "report.return.read",
            "F55": "report.book.read",
        }
        gyomunsa = {
            "F11": "O",
            "F14": "O",
            "F17": "O",
            "F51": "X",
        }
        gyeongri = {
            "F51": "O",
            "F52": "O",
            "F53": "O",
            "F54": "O",
            "F55": "O",
        }
        _, perms_gy = auth_service._merge_fxx_to_permissions(gyomunsa, catalog)
        _, perms_gr = auth_service._merge_fxx_to_permissions(gyeongri, catalog)
        self.assertIn("master.customer.read", perms_gy)
        self.assertNotIn("report.kpi.read", perms_gy)
        self.assertIn("report.kpi.read", perms_gr)
        self.assertNotIn("master.customer.read", perms_gr)
        self.assertNotEqual(set(perms_gy), set(perms_gr))


class InferLoginProfileDominanceTest(IsolatedAsyncioTestCase):
    def test_accounting_wins_over_residual_f11(self) -> None:
        from app.services import auth_service

        fxx = {
            "F11": "R",
            "F51": "O",
            "F52": "O",
            "F53": "O",
            "F54": "O",
            "F55": "O",
        }
        self.assertEqual(
            auth_service.infer_login_profile(fxx),
            "department_accounting",
        )


if __name__ == "__main__":
    main(verbosity=2)
