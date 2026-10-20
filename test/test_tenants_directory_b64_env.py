"""BLS_TENANTS_DIRECTORY_B64 — 고객사 목록(테넌트 시드)을 git 대신 환경변수로 주입 (DEC-411).

외부 협업 저장소(books-logistics-backend)에는 고객사 목록 파일을 넣지 않는다. 그 저장소로 로컬 구동 · 배포할 때
servers.yaml 의 BLS_SERVERS_YAML_B64 와 같은 방식으로 시드를 넣는다.

- 설정되면 파일 대신 env 시드를 쓰고, overlay 병합 규칙은 그대로.
- 해독 실패는 빈 목록(로그인 경로 판별 불가 → fail-closed), 첫 후보로 넘어가지 않는다.
- 미설정이면 종전처럼 파일.
"""

from __future__ import annotations

import base64
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.services import tenants_directory_service as tds

ENV = "BLS_TENANTS_DIRECTORY_B64"


def _tenant(tid: str, family: str, label: str = "") -> dict:
    return {
        "tenant_id": tid,
        "account_family": family,
        "tenant_label_kor": label or tid,
        "primary_server": "remote_9001",
        "db_name_logical": "test_db",
        "is_active": True,
    }


def _b64(tenants: list[dict]) -> str:
    return base64.b64encode(json.dumps({"tenants": tenants}, ensure_ascii=False).encode("utf-8")).decode("ascii")


class TenantsSeedFromEnv(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        self.seed = d / "seed.json"
        self.overlay = d / "overlay.json"
        self.seed.write_text(json.dumps({"tenants": [_tenant("file-t", "fam-file")]}), encoding="utf-8")
        self._p = [
            patch.object(tds, "TENANTS_DIRECTORY_PATH", self.seed),
            patch.object(tds, "TENANTS_OVERLAY_PATH", self.overlay),
        ]
        for p in self._p:
            p.start()
        self._env = os.environ.pop(ENV, None)
        tds.reload()

    def tearDown(self) -> None:
        os.environ.pop(ENV, None)
        if self._env is not None:
            os.environ[ENV] = self._env
        for p in self._p:
            p.stop()
        tds.reload()
        self.tmp.cleanup()

    def _ids(self) -> list[str]:
        return sorted(t["tenant_id"] for t in tds.list_all_active())

    def test_unset_reads_file(self) -> None:
        self.assertEqual(self._ids(), ["file-t"])

    def test_env_seed_replaces_file(self) -> None:
        os.environ[ENV] = _b64([_tenant("env-a", "fam-a"), _tenant("env-b", "fam-b", "시험 출판사")])
        tds.reload()
        self.assertEqual(self._ids(), ["env-a", "env-b"])
        self.assertEqual(tds.lookup_by_tenant_id("env-b")["tenant_label_kor"], "시험 출판사")

    def test_overlay_still_wins_over_env_seed(self) -> None:
        os.environ[ENV] = _b64([_tenant("env-a", "fam-a", "시드")])
        self.overlay.write_text(json.dumps({"tenants": [{"tenant_id": "env-a", "account_family": "fam-a", "tenant_label_kor": "오버레이"}]}), encoding="utf-8")
        tds.reload()
        self.assertEqual(tds.lookup_by_tenant_id("env-a")["tenant_label_kor"], "오버레이")

    def test_bad_value_is_empty_not_file_fallback(self) -> None:
        for bad in ("@@not-base64@@", base64.b64encode(b"not json").decode()):
            os.environ[ENV] = bad
            tds.reload()
            with self.assertLogs(tds.logger, level="ERROR"):
                self.assertEqual(self._ids(), [])

    def test_blank_value_means_unset(self) -> None:
        os.environ[ENV] = "   "
        tds.reload()
        self.assertEqual(self._ids(), ["file-t"])


if __name__ == "__main__":
    unittest.main()
