"""단독 배포(Render Docker) 경로에서 인쇄 파이프라인 회귀 가드.

배경
----
Render Docker 는 ``backend/`` 만 빌드해 모듈 경로가 ``/app/app/...`` (조상 4개)이 된다.
``Path(__file__).parents[4]`` 고정 인덱스는 이 경로에서 IndexError 를 던져
거래명세서 PDF 인쇄가 운영 500 으로 새는 회귀가 있었다 (2026-07-03).

가드 4종
--------
1. ``find_repo_file`` — 얕은 경로에서도 무예외 (None 반환).
2. ``resolve_profile`` — 계약 yaml 미발견 시 기본 프로필 dict (500 금지).
3. 번들 사본(backend/data/contracts) == 허브 정본(migration/contracts) — 파싱 내용 동기화.
4. backend/app 내 ``parents[4+]`` 고정 인덱스 재유입 금지 스캔.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

import yaml

from app.core.repo_paths import find_repo_file
from app.services import print_template_registry, sales_statement_print_profile

_HUB_ROOT = Path(__file__).resolve().parents[1]
_BACKEND = _HUB_ROOT / "도서물류관리프로그램" / "backend"


class FindRepoFileTests(TestCase):
    def test_shallow_docker_like_path_no_indexerror(self) -> None:
        # Render Docker: /app/app/services/... — 조상 4개뿐이어도 예외 없이 None.
        res = find_repo_file(
            "migration/contracts/print_sales_statement.yaml",
            start=Path("/app/app/services/sales_statement_print_profile.py"),
        )
        self.assertIsNone(res)

    def test_filesystem_root_start_no_indexerror(self) -> None:
        self.assertIsNone(find_repo_file("nonexistent/x.yaml", start=Path("/")))

    def test_finds_hub_contract_from_backend_module(self) -> None:
        # 개발(허브 중첩) 배치에서는 허브 정본을 찾는다.
        start = _BACKEND / "app" / "services" / "sales_statement_print_profile.py"
        res = find_repo_file("migration/contracts/print_sales_statement.yaml", start=start)
        self.assertEqual(res, _HUB_ROOT / "migration" / "contracts" / "print_sales_statement.yaml")


class ResolveProfileFallbackTests(TestCase):
    def tearDown(self) -> None:
        sales_statement_print_profile.clear_profile_cache_for_tests()

    def test_no_contract_found_returns_default_profile(self) -> None:
        sales_statement_print_profile.clear_profile_cache_for_tests()
        with patch.object(sales_statement_print_profile, "_contract_path", return_value=None):
            prof = sales_statement_print_profile.resolve_profile("remote_153")
        self.assertIsInstance(prof, dict)  # 예외 없이 기본 프로필 — 인쇄 500 금지

    def test_bundled_copy_used_when_hub_missing(self) -> None:
        sales_statement_print_profile.clear_profile_cache_for_tests()
        bundled = _BACKEND / "data" / "contracts" / "print_sales_statement.yaml"
        with patch.object(
            sales_statement_print_profile, "_contract_path", return_value=bundled,
        ):
            prof = sales_statement_print_profile.resolve_profile("remote_153")
        self.assertIsInstance(prof, dict)
        self.assertTrue(prof)  # 번들 사본은 실제 default 프로필을 담는다


class BundledContractSyncTests(TestCase):
    def test_bundled_copy_matches_hub_source(self) -> None:
        hub = _HUB_ROOT / "migration" / "contracts" / "print_sales_statement.yaml"
        bundled = _BACKEND / "data" / "contracts" / "print_sales_statement.yaml"
        self.assertTrue(hub.is_file(), str(hub))
        self.assertTrue(bundled.is_file(), f"번들 사본 누락: {bundled}")
        hub_data = yaml.safe_load(hub.read_text(encoding="utf-8"))
        bundled_data = yaml.safe_load(bundled.read_text(encoding="utf-8"))
        self.assertEqual(
            hub_data, bundled_data,
            "허브 정본과 번들 사본이 다릅니다 — 허브 편집 후 backend/data/contracts/ 로 복사하세요.",
        )


class ResolveIrPathDeployTests(TestCase):
    def test_relative_ir_path_missing_repo_returns_none(self) -> None:
        entry = {"mode": "auto", "ir_path": "debug/output/frf_converted_all/x.json"}
        with patch.dict(print_template_registry._WHITELIST, {"__t__": entry}), \
                patch.object(print_template_registry, "find_repo_file", return_value=None):
            res = print_template_registry._resolve_ir_path("__t__")
        self.assertIsNone(res)  # graceful fallback → manual 빌더


class DockerfileEngineGuardTests(TestCase):
    """WeasyPrint(>=53) dlopen 네이티브 의존 — 누락 시 운영 503 PR_ENGINE_UNAVAILABLE."""

    # weasyprint/text/ffi.py 가 dlopen 하는 라이브러리의 Debian 패키지 (harfbuzz-subset 은 선택이나 동봉).
    _REQUIRED_APT = (
        "libpango-1.0-0",
        "libpangoft2-1.0-0",
        "libharfbuzz0b",
        "libharfbuzz-subset0",
        "fonts-nanum",  # 한글 글리프 — 없으면 tofu
    )

    def test_dockerfile_installs_weasyprint_native_deps(self) -> None:
        text = (_BACKEND / "Dockerfile").read_text(encoding="utf-8")
        missing = [pkg for pkg in self._REQUIRED_APT if pkg not in text]
        self.assertEqual(missing, [], f"Dockerfile apt 목록에서 누락: {missing}")

    def test_dockerfile_has_buildtime_engine_check(self) -> None:
        text = (_BACKEND / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn(
            "from weasyprint import HTML", text,
            "빌드 타임 PDF 엔진 검증(RUN python -c ... write_pdf) 제거 금지 — 런타임 503 조기 차단",
        )


class NoFixedParentsIndexTests(TestCase):
    _BANNED = re.compile(r"\.parents\[[4-9]\]")

    def test_backend_app_has_no_parents_4_plus(self) -> None:
        offenders: list[str] = []
        for py in (_BACKEND / "app").rglob("*.py"):
            text = py.read_text(encoding="utf-8", errors="replace")
            if self._BANNED.search(text):
                offenders.append(str(py.relative_to(_BACKEND)))
        self.assertEqual(
            offenders, [],
            "parents[4+] 고정 인덱스는 Docker(/app) 경로에서 IndexError → "
            "app/core/repo_paths.find_repo_file 을 사용하세요.",
        )
