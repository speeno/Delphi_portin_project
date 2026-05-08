"""
C9 Sobo39 할인율 — variant=base|v1|v2|v5 + CRUD 회귀 (v1.4.0).

서비스 ``_g7_ggeo_columns_lower`` 는 테스트에서 고정 컬럼 집합으로 패치.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import masters_service  # noqa: E402

_SID = "remote_138"

_FAKE_G7 = frozenset({"gcode", "gname", "gpper", "gpper1", "gpper2", "gpper5", "ocode", "hcode"})


async def _fake_cols(_server_id: str) -> frozenset[str]:  # noqa: ARG001
    return _FAKE_G7


def _user_write() -> dict:
    return {
        "user_id": "t_dis",
        "server_id": _SID,
        "role": "operator",
        "hcode": "BR01",
        "permissions": ["master.write"],
    }


async def _override_user() -> dict:
    return _user_write()


async def _override_ctx() -> dict:
    u = _user_write()
    return {
        "user_id": u["user_id"],
        "server_id": u["server_id"],
        "role": u["role"],
        "hcode": u["hcode"],
        "branch_id": u["hcode"],
        "permissions": list(u["permissions"]),
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "",
        "build_role": "",
        "account_type": "",
        "dist_hcode": "",
    }


class DiscountVariantServiceTests(TestCase):
    def test_gpper_sql_column_respects_variant(self) -> None:
        self.assertEqual(masters_service._gpper_sql_column(_FAKE_G7, "base"), "Gpper")
        self.assertEqual(masters_service._gpper_sql_column(_FAKE_G7, "v1"), "Gpper1")
        self.assertEqual(masters_service._gpper_sql_column(_FAKE_G7, "v2"), "Gpper2")
        self.assertEqual(masters_service._gpper_sql_column(_FAKE_G7, "v5"), "Gpper5")

    def test_gpper_fallback_when_variant_column_missing(self) -> None:
        minimal = frozenset({"gcode", "gname", "gpper"})
        self.assertEqual(masters_service._gpper_sql_column(minimal, "v1"), "Gpper")


class DiscountCrudRouterTests(TestCase):
    def setUp(self) -> None:
        self._prev_user = app.dependency_overrides.get(get_current_user)
        self._prev_ctx = app.dependency_overrides.get(get_user_context)
        app.dependency_overrides[get_current_user] = _override_user
        app.dependency_overrides[get_user_context] = _override_ctx
        self.client = TestClient(app)

    def tearDown(self) -> None:
        if self._prev_user is not None:
            app.dependency_overrides[get_current_user] = self._prev_user
        else:
            app.dependency_overrides.pop(get_current_user, None)
        if self._prev_ctx is not None:
            app.dependency_overrides[get_user_context] = self._prev_ctx
        else:
            app.dependency_overrides.pop(get_user_context, None)

    def test_discount_list_includes_variant(self) -> None:
        async def fake_list(*, server_id: str, **kwargs):  # noqa: ARG001
            self.assertEqual(kwargs.get("variant"), "v1")
            return {
                "variant": "v1",
                "items": [],
                "page": {"limit": 20, "offset": 0, "total": 0, "has_more": False},
            }

        with patch.object(masters_service, "list_discounts", side_effect=fake_list):
            r = self.client.get(f"/api/v1/masters/discount?serverId={_SID}&variant=v1&limit=20")
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json().get("variant"), "v1")

    def test_patch_discount_missing_row(self) -> None:
        async def fake_upd(*, server_id: str, gcode: str, variant: str | None, payload: dict):  # noqa: ARG001
            self.assertEqual(gcode, "ZZZZZ")
            self.assertEqual(variant, "v2")
            self.assertIn("gpper", payload)
            return None

        with (
            patch.object(masters_service, "_g7_ggeo_columns_lower", side_effect=_fake_cols),
            patch.object(masters_service, "update_discount_master", side_effect=fake_upd),
        ):
            r = self.client.patch(
                f"/api/v1/masters/discount/ZZZZZ?variant=v2",
                json={"serverId": _SID, "gpper": 1.5},
            )
        self.assertEqual(r.status_code, 404, r.text)


class DiscountCrudStatic(TestCase):
    def test_router_tokens(self) -> None:
        src = (BACKEND / "app" / "routers" / "masters.py").read_text(encoding="utf-8")
        for token in (
            '@router.get("/discount/{gcode}"',
            "async def create_discount",
            "async def update_discount",
            "async def delete_discount",
            "list_discounts",
        ):
            self.assertIn(token, src)


if __name__ == "__main__":
    main(verbosity=2)
