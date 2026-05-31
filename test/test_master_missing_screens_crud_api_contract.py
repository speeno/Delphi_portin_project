"""
account-menu-fxx-rbac Phase F-2 — 누락 기초관리 3화면 CRUD 회귀.

대상(동형 Ggeo-style 마스터 — 모두 본 폼 상세 명시 라우트로 승격됨):
  - 입고처관리   /api/v1/masters/inbound-vendors  (Sobo12 · G2_Ggwo · F12)
  - 기타거래처   /api/v1/masters/etc-customers    (Sobo15 · G5_Ggeo · F15)
  - 저자관리     /api/v1/masters/authors          (Sobo13 · G3_Gjeo · F13, 표시명 Gposa)

검증
----
- 5 라우트(GET 목록/단건, POST/PATCH/DELETE) 등록 + 쓰기 ``require_permission('master.write')`` 가드.
- 쓰기 권한 없는 사용자는 403 (계정 무관 — 가드는 권한 코드만 본다).
- 서비스는 monkeypatch 로 DB 부작용 0.
- G3 저자 표시명 컬럼이 ``Gposa`` 로 SQL 에 박히는지(동형 헬퍼 분기) 가드.
"""

from __future__ import annotations

import asyncio
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

# (route path, entity, service create fn name, 필수 표시명 필드, Fxx 키)
# 저자(Sobo13)는 표시명이 Gposa 라 생성 요청 필수 필드가 gposa (다른 화면은 gname).
# DEC-RBAC-04 — 화면별 require_fxx_write 가드 도입(account-menu-fxx-mapping §2.1).
_SCREENS = [
    ("inbound-vendors", "inbound_vendor", "create_inbound_vendor", "gname", "F12"),
    ("etc-customers", "etc_customer", "create_etc_customer", "gname", "F15"),
    ("authors", "author", "create_author", "gposa", "F13"),
]


def _user(perms: list[str], *, fxx_caps: dict[str, dict[str, bool]] | None = None) -> dict:
    return {
        "user_id": "t_f",
        "server_id": _SID,
        "role": "operator",
        "hcode": "BR01",
        "branch_id": "BR01",
        "permissions": list(perms),
        "tenant_id": "",
        "account_family": "",
        "active_build_id": "",
        "build_role": "",
        "account_type": "",
        "dist_hcode": "",
        "fxx_caps": dict(fxx_caps or {}),
    }


def _all_write_caps() -> dict[str, dict[str, bool]]:
    return {
        fkey: {"read": True, "write": True, "print": True}
        for *_rest, fkey in _SCREENS
    }


def _all_read_only_caps() -> dict[str, dict[str, bool]]:
    return {
        fkey: {"read": True, "write": False, "print": True}
        for *_rest, fkey in _SCREENS
    }


def _mk_overrides(perms: list[str], *, fxx_caps: dict[str, dict[str, bool]] | None = None):
    async def _ovr_user() -> dict:
        return _user(perms, fxx_caps=fxx_caps)

    async def _ovr_ctx() -> dict:
        return _user(perms, fxx_caps=fxx_caps)

    return _ovr_user, _ovr_ctx


class MissingScreensCrudRouterTests(TestCase):
    def setUp(self) -> None:
        self._prev_user = app.dependency_overrides.get(get_current_user)
        self._prev_ctx = app.dependency_overrides.get(get_user_context)
        u, c = _mk_overrides(["master.write"], fxx_caps=_all_write_caps())
        app.dependency_overrides[get_current_user] = u
        app.dependency_overrides[get_user_context] = c
        self.client = TestClient(app)

    def tearDown(self) -> None:
        for dep, prev in (
            (get_current_user, self._prev_user),
            (get_user_context, self._prev_ctx),
        ):
            if prev is not None:
                app.dependency_overrides[dep] = prev
            else:
                app.dependency_overrides.pop(dep, None)

    def test_post_calls_service_for_each_screen(self) -> None:
        for path, _entity, fn_name, name_field, _fkey in _SCREENS:
            async def fake_create(*, server_id: str, payload: dict, scope_hcode=None):  # noqa: ARG001
                self.assertEqual(server_id, _SID)
                self.assertEqual(payload.get("gcode"), "X001")
                return {"gcode": "X001", "created_at": "2026-05-30T00:00:00Z"}

            with patch.object(masters_service, fn_name, side_effect=fake_create):
                r = self.client.post(
                    f"/api/v1/masters/{path}",
                    json={"serverId": _SID, "gcode": "X001", name_field: "테스트"},
                )
            self.assertEqual(r.status_code, 201, f"{path}: {r.text}")
            self.assertEqual(r.json().get("gcode"), "X001", path)

    def test_post_bad_body_422_for_each_screen(self) -> None:
        for path, _entity, _fn, _name, _fkey in _SCREENS:
            r = self.client.post(f"/api/v1/masters/{path}", json={"serverId": _SID})
            self.assertEqual(r.status_code, 422, f"{path}: {r.text}")

    def test_post_forbidden_without_master_write(self) -> None:
        # 쓰기 권한이 없는(읽기만) 계정은 모든 화면에서 403 — DEC-RBAC-04 require_fxx_write 가드.
        # F12/F13/F15 가 R(읽기만)인 경우 write capability 가 false → 403.
        u, c = _mk_overrides(["master.book.read"], fxx_caps=_all_read_only_caps())
        app.dependency_overrides[get_current_user] = u
        app.dependency_overrides[get_user_context] = c
        for path, _entity, _fn, name_field, _fkey in _SCREENS:
            r = self.client.post(
                f"/api/v1/masters/{path}",
                json={"serverId": _SID, "gcode": "X002", name_field: "x"},
            )
            self.assertEqual(r.status_code, 403, f"{path}: {r.text}")


class MissingScreensServiceTests(TestCase):
    """G3 Gposa·G2_Ggwo·G5_Ggeo 표시 컬럼·테이블 가드 — column meta 어댑터까지 모킹.

    list_* 함수는 schema 어댑터에서 SHOW COLUMNS 를 호출하므로 실제 DB 없이
    실행하려면 g{2,3,5}_*_column_meta 와 execute_query 를 함께 모킹해야 한다.
    """

    @staticmethod
    def _columns(field_lowers: tuple[str, ...]) -> tuple[set[str], dict[str, str]]:
        # exact 표기는 PascalCase 첫글자 + 나머지 그대로 (legacy 패턴).
        exact = {lower: lower[:1].upper() + lower[1:] for lower in field_lowers}
        return set(field_lowers), exact

    def _patch_g3_meta(self):
        from app.services import g3_gjeo_adapt
        from app.services import masters_service as ms

        gjeo_meta = self._columns((
            "gcode", "gposa", "gname", "hcode", "gubun", "date1", "gjice",
            "gtel1", "gtel2",
        ))
        gbun_meta = self._columns(("gcode", "gname"))

        async def _gjeo(_sid):
            return gjeo_meta

        async def _gbun(_sid):
            return gbun_meta

        return [
            patch.object(ms, "g3_gjeo_column_meta", side_effect=_gjeo),
            patch.object(ms, "g3_gbun_column_meta", side_effect=_gbun),
            patch.object(g3_gjeo_adapt, "g3_gjeo_column_meta", side_effect=_gjeo),
            patch.object(g3_gjeo_adapt, "g3_gbun_column_meta", side_effect=_gbun),
        ]

    def _patch_g2_meta(self):
        from app.services import g2_ggwo_adapt
        from app.services import masters_service as ms

        ggwo_meta = self._columns((
            "gcode", "gname", "hcode", "gubun", "guper", "gtel1", "gtel2",
            "gpost", "gjuso", "jubun", "gnumb",
        ))
        gbun_meta = self._columns(("gcode", "gname"))

        async def _ggwo(_sid):
            return ggwo_meta

        async def _gbun(_sid):
            return gbun_meta

        return [
            patch.object(ms, "g2_ggwo_column_meta", side_effect=_ggwo),
            patch.object(ms, "g2_gbun_column_meta", side_effect=_gbun),
            patch.object(g2_ggwo_adapt, "g2_ggwo_column_meta", side_effect=_ggwo),
            patch.object(g2_ggwo_adapt, "g2_gbun_column_meta", side_effect=_gbun),
        ]

    def _patch_g5_meta(self):
        from app.services import g5_ggeo_adapt
        from app.services import masters_service as ms

        ggeo_meta = self._columns((
            "gcode", "gname", "hcode", "gubun", "guper", "gtel1", "gtel2",
            "gpost", "gjuso",
        ))
        gbun_meta = self._columns(("gcode", "gname"))

        async def _ggeo(_sid):
            return ggeo_meta

        async def _gbun(_sid):
            return gbun_meta

        return [
            patch.object(ms, "g5_ggeo_column_meta", side_effect=_ggeo),
            patch.object(ms, "g5_gbun_column_meta", side_effect=_gbun),
            patch.object(g5_ggeo_adapt, "g5_ggeo_column_meta", side_effect=_ggeo),
            patch.object(g5_ggeo_adapt, "g5_gbun_column_meta", side_effect=_gbun),
        ]

    def test_author_list_uses_gposa_name_column(self) -> None:
        captured: dict[str, str] = {}

        async def fake_exec(server_id, sql, params):  # noqa: ARG001
            if "row_count" not in sql and "gname" in sql:
                captured["sql"] = sql
            return []

        patches = self._patch_g3_meta() + [
            patch.object(masters_service, "execute_query", side_effect=fake_exec),
        ]
        for p in patches:
            p.start()
        try:
            asyncio.run(masters_service.list_authors(server_id=_SID, limit=1))
        finally:
            for p in patches:
                p.stop()
        self.assertIn("Gposa", captured.get("sql", ""), "저자 목록은 Gposa 를 표시명으로 사용해야 한다")
        self.assertIn("FROM G3_Gjeo", captured.get("sql", ""))

    def test_inbound_and_etc_use_correct_tables(self) -> None:
        for fn, table, meta_method in (
            (masters_service.list_inbound_vendors, "G2_Ggwo", self._patch_g2_meta),
            (masters_service.list_etc_customers, "G5_Ggeo", self._patch_g5_meta),
        ):
            captured: dict[str, str] = {}

            async def fake_exec(server_id, sql, params, _cap=captured):  # noqa: ARG001
                if "row_count" not in sql and "gname" in sql:
                    _cap["sql"] = sql
                return []

            patches = meta_method() + [
                patch.object(masters_service, "execute_query", side_effect=fake_exec),
            ]
            for p in patches:
                p.start()
            try:
                asyncio.run(fn(server_id=_SID, limit=1))
            finally:
                for p in patches:
                    p.stop()
            self.assertIn(f"FROM {table}", captured.get("sql", ""))


class MissingScreensStatic(TestCase):
    def test_routes_registered(self) -> None:
        from app.routers import masters as m

        paths = {r.path for r in m.router.routes}
        for path in ("inbound-vendors", "etc-customers", "authors"):
            self.assertIn(f"/api/v1/masters/{path}", paths)
            self.assertIn(f"/api/v1/masters/{path}/{{gcode}}", paths)

    def test_router_uses_master_write_guard(self) -> None:
        src = (BACKEND / "app" / "routers" / "masters.py").read_text(encoding="utf-8")
        for token in ("_mount_simple_master", "_SimpleMasterSpec", "_MASTER_WRITE_PERM", "write_dep"):
            self.assertIn(token, src)


if __name__ == "__main__":
    main(verbosity=2)
