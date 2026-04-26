"""login_id_index rebuild — 서버 전체 Id_Logn 스캔 회귀 가드."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services import login_id_index_service


async def _fake_execute_query(server_id: str, sql: str, params: object | None = None):
    s = (sql or "").strip()
    if s.upper().startswith("SHOW DATABASES"):
        return [{"Database": "known_db"}, {"Database": "live_only_db"}, {"Database": "no_logn_db"}]
    if "SHOW TABLES FROM `known_db`" in s:
        return [{"Tables_in_known_db": "Id_Logn"}]
    if "SHOW TABLES FROM `live_only_db`" in s:
        return [{"Tables_in_live_only_db": "Id_Logn"}]
    if "SHOW TABLES FROM `no_logn_db`" in s:
        return [{"Tables_in_no_logn_db": "G1_Ggeo"}]
    if "FROM `known_db`.Id_Logn" in s:
        return [{"login_id": "known-user", "hcode": "1001"}]
    if "FROM `live_only_db`.Id_Logn" in s:
        return [{"login_id": "live-only-user", "hcode": "2002"}]
    raise AssertionError(f"unexpected query: {server_id} {sql}")


def test_login_id_index_rebuild_scans_live_databases(tmp_path, monkeypatch):
    monkeypatch.setattr(login_id_index_service, "LOGIN_ID_INDEX_PATH", tmp_path / "login_id_index.json")
    monkeypatch.setattr(
        login_id_index_service,
        "get_server_profiles",
        lambda: [{"id": "remote_test", "label": "test"}],
    )
    monkeypatch.setattr(
        "app.services.tenants_directory_service.list_all_active",
        lambda: [
            {
                "primary_server": "remote_test",
                "db_name_logical": "known_db",
                "tenant_id": "tenant-known",
                "account_family": "known",
                "is_active": True,
            }
        ],
    )
    monkeypatch.setattr(
        "app.services.tenants_directory_service.label_to_remote_id",
        lambda v: "remote_test" if v == "remote_test" else "",
    )
    monkeypatch.setattr("app.core.db.execute_query", _fake_execute_query)
    login_id_index_service.reload()
    login_id_index_service.reset_refresh_state_for_tests()

    import asyncio

    stats = asyncio.run(login_id_index_service.rebuild())

    assert stats["rows"] == 2
    assert stats["errors"] == []
    known = login_id_index_service.lookup("known-user")
    assert known["status"] == "single"
    assert known["route"]["db_name"] == "known_db"
    live_only = login_id_index_service.lookup("live-only-user")
    assert live_only["status"] == "single"
    assert live_only["route"]["db_name"] == "live_only_db"
    assert live_only["route"]["account_family"] == "live_only"
