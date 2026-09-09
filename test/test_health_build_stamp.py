"""헬스 응답에 배포 커밋 스탬프 (2026-09-09).

"고쳤는데 운영에는 그대로다" 진단은 코드 / **배포본** / 클라이언트 3계층으로 갈린다.
배포본 계층을 외부에서 한 번의 요청으로 끝내려고 ``GET /api/v1/health`` 가 빌드 커밋과
프로세스 부팅 시각을 함께 돌려준다. Render 는 ``RENDER_GIT_COMMIT``/``RENDER_GIT_BRANCH``
를 자동 주입한다(공개 커밋 SHA — 비밀 아님). 값이 없으면 키를 생략해 로컬 응답은 그대로다.
"""

from __future__ import annotations

import importlib
import os
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))


from app.main import app  # noqa: E402

client = TestClient(app)
_BUILD_ENV_KEYS = ("RENDER_GIT_COMMIT", "RENDER_GIT_BRANCH", "BLS_BUILD_COMMIT", "BLS_BUILD_BRANCH")


class HealthBuildStampTests(TestCase):
    def setUp(self) -> None:
        for key in _BUILD_ENV_KEYS:
            os.environ.pop(key, None)

    def test_health_is_still_ok_without_build_env(self) -> None:
        body = client.get("/api/v1/health").json()
        self.assertEqual(body["status"], "ok")
        self.assertIn("startedAt", body)
        self.assertNotIn("commit", body)  # 로컬은 종전과 같은 모양
        self.assertNotIn("branch", body)

    def test_health_reports_the_deployed_commit(self) -> None:
        env = {"RENDER_GIT_COMMIT": "6e83558ede1aa677e62d9a296f02915e70383fe4",
               "RENDER_GIT_BRANCH": "main"}
        with patch.dict(os.environ, env, clear=False):
            body = client.get("/api/v1/health").json()
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["commit"], "6e83558ede1a")  # 앞 12자
        self.assertEqual(body["branch"], "main")

    def test_started_at_is_stable_across_requests(self) -> None:
        # 부팅 시각은 프로세스 시작 시각 — 요청마다 바뀌면 재배포 판별에 못 쓴다.
        first = client.get("/api/v1/health").json()["startedAt"]
        self.assertEqual(client.get("/api/v1/health").json()["startedAt"], first)


if __name__ == "__main__":
    main()
