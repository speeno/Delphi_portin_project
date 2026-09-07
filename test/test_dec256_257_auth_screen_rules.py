"""DEC-256 / DEC-257 — 로그인·계정전환 화면 입력 검증 규칙(2026-09-07 사용자 목업) 정적 가드.

목업이 못박은 규칙:

  로그인 (DEC-256)
    1. 이메일 형식이 아니면 아이디 칸 아래 오류 — `@` 가 들어오면 사라진다.
    2. 비밀번호 8자 미만이면 오류 — 8자를 채우면 사라진다.
    3. 로그인 실패는 **비밀번호 칸 아래 인라인**으로 한 문장(팝업 아님).
    4. 조건을 채우기 전에는 「로그인」 버튼 비활성.

  계정 전환하기 (DEC-257)
    1. 모든 입력 필드가 채워질 때까지 「다음」 비활성.
    2. 일치하는 계정이 없으면 **팝업**으로 "입력하신 정보와 일치하는 계정이 없습니다".

로그인 규칙 1·2·4 는 `emailMode` 에서만 건다 — 레거시 델파이 비밀번호(`Gpass`)에는 길이
정책이 없어 break-glass 로 레거시 ID 로그인을 열어 둔 동안 짧은 비밀번호를 막으면 안 된다.
"""

import unittest
from pathlib import Path

FRONTEND = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"
LOGIN = FRONTEND / "app" / "(public)" / "login" / "page.tsx"
WIZARD = FRONTEND / "components" / "account" / "SwitchWizard.tsx"


class TestLoginValidationRules(unittest.TestCase):
    """DEC-256 — 로그인 화면 규칙 1~4."""

    def setUp(self) -> None:
        self.assertTrue(LOGIN.exists(), LOGIN)
        self.src = LOGIN.read_text(encoding="utf-8")

    def test_rule1_email_format_error(self) -> None:
        self.assertIn("이메일 주소 형식에 맞지 않습니다", self.src)
        self.assertIn("idFormatError", self.src)

    def test_rule2_password_min_length(self) -> None:
        self.assertIn("비밀번호는 최소 8자 이상 입력하셔야 합니다", self.src)
        self.assertIn("password.length < 8", self.src)

    def test_rule3_failure_message_is_inline_not_popup(self) -> None:
        self.assertIn("등록되지 않은 아이디이거나 비밀번호를 잘못 입력하셨습니다", self.src)
        # 로그인 실패는 인라인 — 목업 팝업(DEC-252)은 계정 전환 쪽에만 남는다.
        self.assertNotIn("AuthAlertDialog", self.src)

    def test_rule4_submit_disabled_until_valid(self) -> None:
        self.assertIn("canSubmit", self.src)
        self.assertIn("!canSubmit", self.src)

    def test_rules_gated_to_email_mode(self) -> None:
        """레거시 ID 로그인이 열려 있는 동안에는 형식·길이 규칙을 걸지 않는다."""
        self.assertIn("emailMode", self.src)
        for needle in ("idFormatError", "pwLengthError"):
            head = self.src.split(needle, 1)[1][:200]
            self.assertIn("emailMode", head, needle)


class TestSwitchValidationRules(unittest.TestCase):
    """DEC-257 — 계정 전환하기 1단계 규칙 1~2."""

    def setUp(self) -> None:
        self.assertTrue(WIZARD.exists(), WIZARD)
        self.src = WIZARD.read_text(encoding="utf-8")

    def test_rule1_next_disabled_until_all_fields_filled(self) -> None:
        self.assertIn("const canVerify", self.src)
        # 사용자(회사)·아이디·비밀번호 셋 다 본다.
        self.assertIn("orgSelect !==", self.src)
        self.assertIn("userId.trim().length > 0", self.src)
        self.assertIn("password.length > 0", self.src)
        self.assertIn("disabled={busy || !canVerify}", self.src)

    def test_rule1_exempt_when_org_options_unavailable(self) -> None:
        """콤보 API 가 실패해 옵션이 없으면 고를 수 없는 값을 요구하지 않는다."""
        self.assertIn("const orgRequired = orgOptions.length > 0", self.src)

    def test_rule2_no_match_popup_wording(self) -> None:
        self.assertIn("입력하신 정보와 일치하는 계정이 없습니다", self.src)
        self.assertIn("err.status === 401", self.src)
        # 한 문장 알림은 목업 팝업으로(DEC-252).
        self.assertIn("AuthAlertDialog", self.src)


if __name__ == "__main__":
    unittest.main()
