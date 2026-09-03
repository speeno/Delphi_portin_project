"""ACM — 프론트 비밀번호 규칙 실시간 체크가 백엔드 정책과 어긋나지 않는지 정적 가드.

프론트 `PasswordRules.passwordRules()` 와 백엔드 `account_secret_codec.validate_password_policy()`
는 같은 규칙(8~64자 + 영문 1자 이상 + 숫자 1자 이상)을 따라야 한다. 한쪽만 바뀌면 화면은 통과인데
제출은 422 로 막히는(또는 그 반대) 회귀가 난다.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import account_secret_codec as codec  # noqa: E402

RULES_TSX = (
    ROOT / "도서물류관리프로그램" / "frontend" / "src" / "components" / "account" / "PasswordRules.tsx"
)


class PasswordRuleParityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.src = RULES_TSX.read_text(encoding="utf-8")

    def test_frontend_rules_exist(self):
        self.assertIn("export function passwordRules", self.src)
        for token in ("pw.length >= 8", "pw.length <= 64", "/[A-Za-z]/.test(pw)", "/\\d/.test(pw)"):
            self.assertIn(token, self.src, f"프론트 규칙 누락: {token}")

    def test_rule_count_matches_backend_dimensions(self):
        """`passwordRules()` 안의 규칙은 백엔드 정책 축과 같은 3개 (길이·영문·숫자).

        확인 일치 규칙은 `showMatch` 옵션으로 함수 밖에서 덧붙이므로 이 3개에 포함되지 않는다.
        """
        body = self.src.split("export function passwordRules", 1)[1].split("\n}", 1)[0]
        labels = re.findall(r'label: "([^"]+)"', body)
        self.assertEqual(len(labels), 3, labels)

    def test_backend_accepts_exactly_what_frontend_marks_valid(self):
        def frontend_ok(pw: str) -> bool:
            return 8 <= len(pw) <= 64 and bool(re.search(r"[A-Za-z]", pw)) and bool(re.search(r"\d", pw))

        samples = [
            "abc12345", "a1" * 32, "a1" * 33, "short1", "onlyletters", "12345678",
            "Pass word 1", "한글비밀번호1a", "", "a" * 63 + "1", "a" * 64 + "1",
        ]
        for pw in samples:
            with self.subTest(pw=pw[:12]):
                self.assertEqual(
                    frontend_ok(pw),
                    codec.validate_password_policy(pw) is None,
                    f"규칙 불일치: {pw[:16]!r}",
                )


if __name__ == "__main__":
    unittest.main()
