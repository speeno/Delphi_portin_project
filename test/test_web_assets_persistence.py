"""로고·도장 이미지 DB 영속화(Web_Print_Assets) 회귀 가드 — DEC-073.

배경: 업로드 로고(data/uploads/)·테넌트 도장(data/tenant_print/)은 Render 임시
FS + .dockerignore 제외라 재배포 시 소실(도장은 운영에서 아예 미출력).
DEC-070 패턴 확장 — DB 정본(base64 MEDIUMTEXT) + 파일 캐시 + 히드레이션.

가드: (1) put/get base64 왕복 + REPLACE INTO 형태, (2) 상한 초과/실패 graceful,
(3) 도장 히드레이션이 파일 캐시를 실제 복원(임시 디렉토리) + 프로세스당 1회,
(4) 업로드/삭제 엔드포인트 이중 기록, (5) 인쇄 엔드포인트 히드레이션 훅.
"""

from __future__ import annotations

import base64
import os
import sys
import tempfile
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers import me as me_router  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import tenant_print_assets, web_assets_db  # noqa: E402

_SID = "remote_1"
# 1x1 PNG
_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


def _auth() -> dict:
    return {"user_id": "u1", "server_id": _SID, "hcode": "H1", "role": "operator", "permissions": []}


class WebAssetsDbTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        web_assets_db.clear_ensured_for_tests()

    async def test_put_get_roundtrip_base64(self) -> None:
        store: dict = {}

        async def fake_eq(server_id, sql, params=()):  # noqa: ANN001, ARG001
            s = sql.strip().upper()
            if s.startswith("REPLACE"):
                store["row"] = params
                return []
            if s.startswith("SELECT"):
                if "row" not in store:
                    return []
                p = store["row"]
                return [{"Ext": p[3], "DataB64": p[4]}]
            return []

        with patch.object(web_assets_db, "execute_query", side_effect=fake_eq):
            ok = await web_assets_db.put_asset(
                server_id=_SID, hcode="H1", user_id="u1", kind="logo",
                data=_PNG, ext="png",
            )
            got = await web_assets_db.get_asset(
                server_id=_SID, hcode="H1", user_id="u1", kind="logo",
            )
        self.assertTrue(ok)
        self.assertIsNotNone(got)
        self.assertEqual(got[0], _PNG)  # base64 왕복 무손실
        self.assertEqual(got[1], "png")
        self.assertEqual(store["row"][0], "H1")  # hcode 격리 바인드

    async def test_put_rejects_oversize(self) -> None:
        with patch.object(web_assets_db, "execute_query", AsyncMock(return_value=[])):
            ok = await web_assets_db.put_asset(
                server_id=_SID, hcode="H1", user_id="u1", kind="logo",
                data=b"x" * (web_assets_db._MAX_ASSET_BYTES + 1), ext="png",
            )
        self.assertFalse(ok)

    async def test_get_graceful_on_db_failure(self) -> None:
        async def boom(*a, **k):  # noqa: ANN001, ARG001
            raise RuntimeError("db down")

        with patch.object(web_assets_db, "execute_query", side_effect=boom):
            self.assertIsNone(
                await web_assets_db.get_asset(
                    server_id=_SID, hcode="", user_id="", kind="sales_statement_seal",
                )
            )


class SealHydrationTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        os.environ["BLS_TENANT_PRINT_ASSETS_DIR"] = self._tmp.name
        os.environ["BLS_TENANT_PRINT_META_PATH"] = str(Path(self._tmp.name) / "meta.json")
        tenant_print_assets.clear_hydrated_for_tests()

    def tearDown(self) -> None:
        os.environ.pop("BLS_TENANT_PRINT_ASSETS_DIR", None)
        os.environ.pop("BLS_TENANT_PRINT_META_PATH", None)
        tenant_print_assets.clear_hydrated_for_tests()
        self._tmp.cleanup()

    async def test_hydrate_restores_file_cache_from_db(self) -> None:
        self.assertIsNone(tenant_print_assets.read_seal_bytes(_SID))  # 배포 직후 상태
        with patch.object(web_assets_db, "get_asset", AsyncMock(return_value=(_PNG, "png"))):
            await tenant_print_assets.hydrate_seal_from_db(_SID)
        self.assertEqual(tenant_print_assets.read_seal_bytes(_SID), _PNG)  # 복원됨

    async def test_hydrate_runs_once_per_server(self) -> None:
        get_mock = AsyncMock(return_value=None)
        with patch.object(web_assets_db, "get_asset", get_mock):
            await tenant_print_assets.hydrate_seal_from_db(_SID)
            await tenant_print_assets.hydrate_seal_from_db(_SID)
        get_mock.assert_awaited_once()  # RTT 절약 — 프로세스당 1회

    async def test_hydrate_skips_when_file_cache_valid(self) -> None:
        tenant_print_assets.save_seal_bytes(_SID, _PNG)
        get_mock = AsyncMock(return_value=None)
        with patch.object(web_assets_db, "get_asset", get_mock):
            await tenant_print_assets.hydrate_seal_from_db(_SID)
        get_mock.assert_not_awaited()


class RouterDualWriteTests(TestCase):
    def setUp(self) -> None:
        self._p1 = app.dependency_overrides.get(get_current_user)
        self._p2 = app.dependency_overrides.get(get_user_context)
        app.dependency_overrides[get_current_user] = _auth
        app.dependency_overrides[get_user_context] = _auth
        self.client = TestClient(app)
        self._tmp = tempfile.TemporaryDirectory()
        os.environ["BLS_USER_PROFILES_PATH"] = str(Path(self._tmp.name) / "profiles.json")
        os.environ["BLS_USER_UPLOADS_DIR"] = str(Path(self._tmp.name) / "uploads")
        os.environ["BLS_TENANT_PRINT_ASSETS_DIR"] = str(Path(self._tmp.name) / "tenant_print")
        os.environ["BLS_TENANT_PRINT_META_PATH"] = str(Path(self._tmp.name) / "meta.json")
        tenant_print_assets.clear_hydrated_for_tests()

    def tearDown(self) -> None:
        for k in ("BLS_USER_PROFILES_PATH", "BLS_USER_UPLOADS_DIR",
                  "BLS_TENANT_PRINT_ASSETS_DIR", "BLS_TENANT_PRINT_META_PATH"):
            os.environ.pop(k, None)
        tenant_print_assets.clear_hydrated_for_tests()
        self._tmp.cleanup()
        for dep, prev in ((get_current_user, self._p1), (get_user_context, self._p2)):
            if prev is not None:
                app.dependency_overrides[dep] = prev
            else:
                app.dependency_overrides.pop(dep, None)

    def test_logo_upload_dual_writes_db(self) -> None:
        put_mock = AsyncMock(return_value=True)
        with patch.object(me_router.web_assets_db, "put_asset", put_mock), \
                patch.object(me_router.user_prefs_db, "get_user_prefs", AsyncMock(return_value=None)):
            r = self.client.post(
                "/api/v1/me/logo",
                files={"file": ("logo.png", _PNG, "image/png")},
            )
        self.assertEqual(r.status_code, 200, r.text)
        put_mock.assert_awaited_once()
        self.assertEqual(put_mock.await_args.kwargs["kind"], "logo")
        self.assertEqual(put_mock.await_args.kwargs["hcode"], "H1")
        self.assertEqual(put_mock.await_args.kwargs["data"], _PNG)

    def test_seal_upload_dual_writes_db(self) -> None:
        persist_mock = AsyncMock(return_value=True)
        with patch.object(me_router.tenant_print_assets, "persist_seal_db", persist_mock):
            r = self.client.post(
                "/api/v1/me/tenant-print/seal",
                files={"file": ("seal.png", _PNG, "image/png")},
            )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertTrue(r.json()["persisted_db"])
        persist_mock.assert_awaited_once()

    def test_profile_get_restores_logo_from_db(self) -> None:
        """재배포 후(파일 무) 프로필 조회 → DB 로고로 파일 캐시 복원 + logo_url 반환."""
        with patch.object(me_router.user_prefs_db, "get_user_prefs", AsyncMock(return_value=None)), \
                patch.object(me_router.web_assets_db, "get_asset",
                             AsyncMock(return_value=(_PNG, "png"))):
            r = self.client.get("/api/v1/me/profile")
        self.assertEqual(r.status_code, 200, r.text)
        self.assertTrue(r.json()["logo_url"].startswith("/uploads/"))
        # 파일 캐시 실제 생성 확인
        from app.services import user_profile_service
        prof = user_profile_service.get_profile(_SID, "u1")
        self.assertEqual(user_profile_service.read_logo_bytes(prof["logo_relpath"]), _PNG)


class PrintHydrationHookTests(TestCase):
    def setUp(self) -> None:
        self._p1 = app.dependency_overrides.get(get_current_user)
        self._p2 = app.dependency_overrides.get(get_user_context)
        app.dependency_overrides[get_current_user] = _auth
        app.dependency_overrides[get_user_context] = _auth
        self.client = TestClient(app)

    def tearDown(self) -> None:
        for dep, prev in ((get_current_user, self._p1), (get_user_context, self._p2)):
            if prev is not None:
                app.dependency_overrides[dep] = prev
            else:
                app.dependency_overrides.pop(dep, None)

    def test_batch_pdf_hydrates_seal_before_render(self) -> None:
        from app.routers import print as print_router
        from app.services import print_log_db, print_service, transactions_service as tx

        hydrate_mock = AsyncMock()

        async def fake_detail(**kwargs):  # noqa: ANN001
            return {"order_key": {"gdate": "2026.07.04", "hcode": "H1",
                                  "jubun": kwargs["jubun"], "gjisa": ""},
                    "customer": {}, "lines": []}

        with patch.object(print_router.tenant_print_assets, "hydrate_seal_from_db", hydrate_mock), \
                patch.object(tx, "get_sales_statement_detail", side_effect=fake_detail), \
                patch.object(tx, "render_sales_statements_combined_html", return_value="<html/>"), \
                patch.object(print_service, "render_pdf", return_value=b"%PDF-1.4 f"), \
                patch.object(print_log_db, "record_printed", AsyncMock(return_value=1)):
            r = self.client.get(
                f"/api/v1/print/sales-statement/batch.pdf?serverId={_SID}"
                "&keys=2026.07.04%7CH1%7C00001%7C"
            )
        self.assertEqual(r.status_code, 200, r.text)
        hydrate_mock.assert_awaited_once_with(_SID)
