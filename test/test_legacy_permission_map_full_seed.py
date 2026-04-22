"""DEC-056 회귀 — legacy_permission_map 시드가 카탈로그 §1+§4 의 정본 키와 1:1 정합한지 검증.

배경
----
- 기존 시드는 3건만(F21/F22/F26) 등록되어 있어, Id_Logn Fxx 매트릭스 어댑터가
  반환하는 80셀 중 47건이 매핑 미스로 폐기되어 사용자 권한이 누락되는
  회귀가 발생했다.
- 본 테스트는 ``data/web_admin.json`` 영속 시드와 ``admin_service._empty_state()``
  의 신규 환경 부트스트랩 시드 양쪽 모두가 카탈로그와 정합하는지 검증한다.

검증 항목
---------
1. ``data/web_admin.json::legacy_permission_map`` 의 fkey 셋이 카탈로그 §1+§4 의
   정본 키와 정확히 일치한다.
2. ``admin_service._empty_state()::legacy_permission_map`` 도 동일.
3. 매핑은 1:1 (동일 fkey 중복 등록 없음 + 동일 permission_code 중복 없음).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from unittest import TestCase, main


_REPO_ROOT = Path(__file__).resolve().parent.parent
_BACKEND_ROOT = _REPO_ROOT / "도서물류관리프로그램" / "backend"
_WEB_ADMIN_PATH = _BACKEND_ROOT / "data" / "web_admin.json"
_CATALOG_PATH = _REPO_ROOT / "legacy-analysis" / "permission-keys-catalog.md"


def _parse_catalog_keys() -> dict[str, str]:
    """카탈로그 §1·§4 의 'Fxx → permission_code' 매핑 추출 (예약 행 F61~F89 제외)."""
    text = _CATALOG_PATH.read_text(encoding="utf-8")
    mapping: dict[str, str] = {}
    pattern = re.compile(
        r"^\|\s*(F\d+\w*)\s*\|\s*`([\w\.]+)`\s*\|",
        re.MULTILINE,
    )
    for m in pattern.finditer(text):
        fkey, code = m.group(1), m.group(2)
        if fkey == "F61~F89":
            continue
        mapping[fkey] = code
    return mapping


class LegacyPermissionMapFullSeedTest(TestCase):
    """카탈로그 §1+§4 ↔ 시드 1:1 정합 회귀."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = _parse_catalog_keys()

    def test_web_admin_json_seed_matches_catalog(self) -> None:
        data = json.loads(_WEB_ADMIN_PATH.read_text(encoding="utf-8"))
        seeded = {
            entry["fkey"]: entry["permission_code"]
            for entry in data.get("legacy_permission_map", [])
        }
        catalog_keys = set(self.catalog.keys())
        seeded_keys = set(seeded.keys())
        missing = catalog_keys - seeded_keys
        extra = seeded_keys - catalog_keys
        self.assertSetEqual(
            missing, set(),
            f"web_admin.json::legacy_permission_map 에 누락된 정본 fkey: {sorted(missing)}",
        )
        self.assertSetEqual(
            extra, set(),
            f"web_admin.json::legacy_permission_map 에 카탈로그에 없는 fkey: {sorted(extra)}",
        )
        for fkey, code in self.catalog.items():
            self.assertEqual(
                seeded[fkey], code,
                f"카탈로그 {fkey} → {code} 가 시드와 다름: {seeded[fkey]}",
            )

    def test_admin_service_empty_state_matches_web_admin_json(self) -> None:
        # admin_service.py 임포트 — sys.path 추가 (backend/app)
        sys.path.insert(0, str(_BACKEND_ROOT))
        try:
            from app.services import admin_service  # noqa: WPS433 — 지연 임포트 의도
            empty_seed = {
                entry["fkey"]: entry["permission_code"]
                for entry in admin_service._empty_state()["legacy_permission_map"]
            }
        finally:
            while str(_BACKEND_ROOT) in sys.path:
                sys.path.remove(str(_BACKEND_ROOT))

        json_seed = {
            entry["fkey"]: entry["permission_code"]
            for entry in json.loads(_WEB_ADMIN_PATH.read_text(encoding="utf-8")).get(
                "legacy_permission_map", []
            )
        }
        self.assertEqual(
            empty_seed, json_seed,
            "_empty_state() 시드가 data/web_admin.json 과 정합 불일치 — "
            "신규 환경 부트스트랩 시 매핑 누락 회귀 위험",
        )

    def test_no_duplicate_fkey_or_permission_code(self) -> None:
        data = json.loads(_WEB_ADMIN_PATH.read_text(encoding="utf-8"))
        entries = data.get("legacy_permission_map", [])
        fkeys = [e["fkey"] for e in entries]
        codes = [e["permission_code"] for e in entries]
        self.assertEqual(len(fkeys), len(set(fkeys)),
                         f"중복 fkey 발견: {sorted(set(k for k in fkeys if fkeys.count(k) > 1))}")
        self.assertEqual(len(codes), len(set(codes)),
                         f"중복 permission_code 발견: {sorted(set(c for c in codes if codes.count(c) > 1))}")


if __name__ == "__main__":
    main(verbosity=2)
