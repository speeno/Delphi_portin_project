"""DEC-256 · DEC-257 · DEC-258 — 로그인·계정전환 화면 입력 검증 규칙(2026-09-07 목업) 정적 가드.

목업이 못박은 규칙:

  로그인 (DEC-256)
    1. 이메일 형식이 아니면 아이디 칸 아래 오류 — `@` 가 들어오면 사라진다.
    2. 비밀번호 8자 미만이면 오류 — 8자를 채우면 사라진다.
    3. 로그인 실패는 **비밀번호 칸 아래 인라인**으로 한 문장(팝업 아님).
    4. 조건을 채우기 전에는 「로그인」 버튼 비활성.

  계정 전환하기 1단계 — 계정 확인 (DEC-257)
    1. 모든 입력 필드가 채워질 때까지 「다음」 비활성.
    2. 일치하는 계정이 없으면 **팝업**으로 "입력하신 정보와 일치하는 계정이 없습니다".

  계정 전환하기 2단계 — 이메일 입력 (DEC-258)
    1. `@` 가 나올 때까지 「이메일 주소 형식에 맞지 않습니다」 인라인.
    2. 쓸 수 없는 주소는 팝업 「아이디 입력 오류 / 이미 사용 중인 이메일 주소입니다.」.
    3. 유효한 주소가 되기 전까지 「인증번호 발송」 비활성.

  계정 전환하기 3단계 — 인증번호 (DEC-259)
    1. 인증 시간 초과는 **토스트**로 "인증 시간이 초과되었습니다. 인증번호를 재발송해 주세요."
    2. 인증번호 불일치는 "인증번호가 일치하지 않습니다. 다시 입력해 주세요."

로그인 규칙 1·2·4 는 `emailMode` 에서만 건다 — 레거시 델파이 비밀번호(`Gpass`)에는 길이
정책이 없어 break-glass 로 레거시 ID 로그인을 열어 둔 동안 짧은 비밀번호를 막으면 안 된다.
"""

import unittest
from pathlib import Path

FRONTEND = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"
LOGIN = FRONTEND / "app" / "(public)" / "login" / "page.tsx"
WIZARD = FRONTEND / "components" / "account" / "SwitchWizard.tsx"
SHELL = FRONTEND / "components" / "account" / "AuthCardShell.tsx"


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
        # 목업(2026-09-07) — 제목 「계정 찾기 오류」 + 본문 한 문장.
        self.assertIn('title: "계정 찾기 오류"', self.src)
        self.assertIn("입력하신 정보와 일치하는 계정이 없습니다.", self.src)
        self.assertIn("err.status === 401", self.src)
        # 한 문장 알림은 목업 팝업으로(DEC-252).
        self.assertIn("AuthAlertDialog", self.src)


class TestSwitchEmailStepRules(unittest.TestCase):
    """DEC-258 — 계정 전환하기 2단계(이메일 입력) 규칙 1~3."""

    def setUp(self) -> None:
        self.assertTrue(WIZARD.exists(), WIZARD)
        self.src = WIZARD.read_text(encoding="utf-8")

    def test_rule1_email_format_error_until_at_sign(self) -> None:
        self.assertIn("이메일 주소 형식에 맞지 않습니다", self.src)
        self.assertIn("emailFormatError", self.src)
        # `@` 가 들어오면 사라진다 — 로그인 규칙 1과 같은 기준.
        self.assertIn('!emailTrimmed.includes("@")', self.src)

    def test_rule2_email_taken_is_popup(self) -> None:
        """목업 「아이디 입력 오류」 — 이 건만 팝업, 형식 오류(규칙 1)는 인라인."""
        self.assertIn('title: "아이디 입력 오류"', self.src)
        self.assertIn("이미 사용 중인 이메일 주소입니다.", self.src)
        self.assertIn('c === "ACCT_EMAIL_TAKEN"', self.src)

    def test_rule3_send_disabled_until_valid_email(self) -> None:
        self.assertIn("const emailValid", self.src)
        self.assertIn("disabled={busy || !emailValid}", self.src)

    def test_inline_error_not_popup(self) -> None:
        """2단계 오류는 입력칸 바로 아래 인라인 — 고칠 입력이 화면에 있다."""
        self.assertIn('id="sw-email-error"', self.src)
        self.assertIn("text-xs text-destructive", self.src)


class TestSwitchCodeStepRules(unittest.TestCase):
    """DEC-259 — 계정 전환하기 3단계(인증번호) 오류 두 가지."""

    def setUp(self) -> None:
        self.assertTrue(WIZARD.exists(), WIZARD)
        self.assertTrue(SHELL.exists(), SHELL)
        self.src = WIZARD.read_text(encoding="utf-8")
        self.shell = SHELL.read_text(encoding="utf-8")

    def test_messages_are_toasts_not_popup(self) -> None:
        self.assertIn("인증 시간이 초과되었습니다. 인증번호를 재발송해 주세요.", self.src)
        self.assertIn("인증번호가 일치하지 않습니다. 다시 입력해 주세요.", self.src)
        self.assertIn("useAuthToast", self.src)
        self.assertIn("showToast(MSG_CODE_EXPIRED)", self.src)
        self.assertIn("showToast(expiresLeft <= 0 ? MSG_CODE_EXPIRED : MSG_CODE_MISMATCH)", self.src)

    def test_expiry_split_is_client_side(self) -> None:
        """백엔드는 만료/불일치를 한 코드로 합쳐 준다 — 화면 카운트다운으로 갈라야 두 문구가 나온다."""
        self.assertIn('apiErrorCode(err) === "ACCT_CODE_INVALID"', self.src)
        self.assertIn("expiresLeft <= 0", self.src)

    def test_toast_is_shared_shell_component(self) -> None:
        self.assertIn("export function useAuthToast", self.shell)
        self.assertIn('data-legacy-id="WebAcct.Toast"', self.shell)
        # 어느 테마에서나 같은 밝은 시안 — 반투명이면 다크에서 대비가 무너진다.
        self.assertIn("color-mix(in_srgb,var(--vivid-sky)_70%,white)", self.shell)
        self.assertIn("text-[var(--nav-active-foreground)]", self.shell)

    def test_countdown_turns_red_near_expiry(self) -> None:
        self.assertIn('expiresLeft <= 60 ? "text-destructive" : "text-link"', self.src)


if __name__ == "__main__":
    unittest.main()
