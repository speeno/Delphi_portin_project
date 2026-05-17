"""플랫폼 공개 API — GET /public/portal, notices."""

from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402
from app.services import platform_portal_service as pps  # noqa: E402


class PlatformPortalPublicTests(TestCase):
    def setUp(self) -> None:
        self._tmpdir = tempfile.TemporaryDirectory()
        self._path = Path(self._tmpdir.name) / "platform_portal.json"
        self._prev = pps.PORTAL_PATH
        pps.PORTAL_PATH = self._path
        now = datetime.now(timezone.utc)
        past = (now - timedelta(days=1)).isoformat()
        future = (now + timedelta(days=7)).isoformat()
        expired = (now - timedelta(hours=1)).isoformat()
        state = {
            "slogan": {
                "headline": "테스트 헤드",
                "subline": "테스트 서브",
                "updated_at": past,
                "updated_by": "test",
            },
            "notices": [
                {
                    "id": "n-critical",
                    "title": "긴급 점검",
                    "summary": "요약",
                    "body": "본문 긴급",
                    "severity": "critical",
                    "published_at": past,
                    "expires_at": future,
                    "is_published": True,
                    "created_at": past,
                    "updated_at": past,
                    "updated_by": "test",
                },
                {
                    "id": "n-info-1",
                    "title": "일반 공지 1",
                    "summary": "",
                    "body": "본문1",
                    "severity": "info",
                    "published_at": past,
                    "expires_at": None,
                    "is_published": True,
                    "created_at": past,
                    "updated_at": past,
                    "updated_by": "test",
                },
                {
                    "id": "n-expired",
                    "title": "만료됨",
                    "summary": "",
                    "body": "",
                    "severity": "info",
                    "published_at": past,
                    "expires_at": expired,
                    "is_published": True,
                    "created_at": past,
                    "updated_at": past,
                    "updated_by": "test",
                },
            ],
        }
        self._path.write_text(json.dumps(state, ensure_ascii=False), encoding="utf-8")
        self.client = TestClient(app)

    def tearDown(self) -> None:
        pps.PORTAL_PATH = self._prev
        self._tmpdir.cleanup()

    def test_portal_snapshot(self) -> None:
        r = self.client.get("/api/v1/public/portal")
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertEqual(body["slogan"]["headline"], "테스트 헤드")
        self.assertIsNotNone(body.get("urgentNotice") or body.get("urgent_notice"))
        urgent = body.get("urgentNotice") or body.get("urgent_notice")
        self.assertEqual(urgent["id"], "n-critical")
        recent = body.get("recentNotices") or body.get("recent_notices")
        self.assertEqual(len(recent), 1)
        self.assertEqual(recent[0]["id"], "n-info-1")

    def test_list_notices_excludes_expired(self) -> None:
        r = self.client.get("/api/v1/public/notices")
        self.assertEqual(r.status_code, 200, r.text)
        ids = {x["id"] for x in r.json()["items"]}
        self.assertIn("n-critical", ids)
        self.assertIn("n-info-1", ids)
        self.assertNotIn("n-expired", ids)

    def test_notice_detail_404_when_expired(self) -> None:
        r = self.client.get("/api/v1/public/notices/n-expired")
        self.assertEqual(r.status_code, 404)


if __name__ == "__main__":
    main()
