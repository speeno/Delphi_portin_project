"""DEC-133 — 새 배포 감지 배너 + 낡은 번들 진단 회귀 가드.

배경(2026-08-08): "도서코드 '기계' Enter 임의선택이 여전하다" 보고 — 조사 결과
코드·프로덕션 번들 모두 수정 포함(청크 minified 시그니처로 확인), 원인은 7/30 부터
열려 있던 워크스페이스 창(iframe)의 **수정 이전 번들**. 재발 방지로 빌드 스탬프
(version.json) 폴링 배너 신설.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))


class VersionStampTests(TestCase):
    def test_prebuild_writes_version_json(self) -> None:
        pkg = json.loads((FRONTEND / "package.json").read_text("utf-8"))
        self.assertEqual(pkg["scripts"].get("prebuild"), "node scripts/write-version.mjs")
        src = (FRONTEND / "scripts/write-version.mjs").read_text("utf-8")
        self.assertIn("public/version.json", src.replace('", "', "/"))
        # Vercel 환경변수 우선 — frontend/ 중첩 .git(초기화 잔재)이 rev-parse 를 가로챈다.
        self.assertLess(
            src.find("process.env.VERCEL_GIT_COMMIT_SHA"),
            src.find('execSync("git rev-parse'),
        )

    def test_version_json_gitignored(self) -> None:
        gi = (FRONTEND / ".gitignore").read_text("utf-8")
        self.assertIn("/public/version.json", gi)


class BannerBehaviorTests(TestCase):
    def setUp(self) -> None:
        self.src = (
            FRONTEND / "src/components/app-shell/new-version-banner.tsx"
        ).read_text("utf-8")

    def test_polls_no_store_and_focus(self) -> None:
        self.assertIn('cache: "no-store"', self.src)
        self.assertIn('addEventListener("focus"', self.src)
        self.assertIn("setInterval", self.src)

    def test_no_auto_reload(self) -> None:
        # 자동 리로드 금지 — reload 는 버튼 onClick 에서만(입력 중 데이터 보호).
        self.assertEqual(self.src.count("window.location.reload()"), 1)
        self.assertIn("onClick={() => window.location.reload()}", self.src)

    def test_mounted_in_shell_layout(self) -> None:
        layout = (FRONTEND / "src/app/(app)/layout.tsx").read_text("utf-8")
        self.assertIn("<NewVersionBanner />", layout)
        # 셸(비-embed) 분기에만 — embed(iframe) 분기에는 없어야 한다.
        embed_part = layout.split("if (embed)")[1].split("return (")[1]
        chromeless = embed_part.split("  }")[0]
        self.assertNotIn("NewVersionBanner", chromeless)


class MlfEnterGuardAnchorTests(TestCase):
    """오늘 진단의 앵커 — MLF Enter 확정 규칙(코드 접두/명칭 정확 일치만 자동확정) 유지."""

    def test_confirm_enter_guard_present(self) -> None:
        src = (
            FRONTEND / "src/components/master/master-lookup-field.tsx"
        ).read_text("utf-8")
        self.assertIn("code.startsWith(term)", src)
        self.assertIn("name === term", src)


if __name__ == "__main__":
    main()
