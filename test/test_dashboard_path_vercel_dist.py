"""Vercel /dashboard/dist 404 회귀 — 총판 대시보드 URL 은 /dashboard/distributor."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
DASHBOARD_PATH_TS = FRONTEND / "src" / "lib" / "dashboard-path.ts"
NEXT_CONFIG = FRONTEND / "next.config.ts"
DASHBOARD_APP = FRONTEND / "src" / "app" / "(app)" / "dashboard"


def test_t2_dist_path_in_dashboard_path_module():
    text = DASHBOARD_PATH_TS.read_text(encoding="utf-8")
    assert 'return DISTRIBUTOR_DASHBOARD_PATH' in text
    assert '"/dashboard/distributor"' in text
    assert 'LEGACY_DIST_DASHBOARD_PATH = "/dashboard/dist"' in text


def test_legacy_dist_redirect_in_next_config():
    text = NEXT_CONFIG.read_text(encoding="utf-8")
    assert 'source: "/dashboard/dist"' in text
    assert 'destination: "/dashboard/distributor"' in text


def test_distributor_page_exists_dist_route_removed():
    assert (DASHBOARD_APP / "distributor" / "page.tsx").is_file()
    assert not (DASHBOARD_APP / "dist" / "page.tsx").exists()
