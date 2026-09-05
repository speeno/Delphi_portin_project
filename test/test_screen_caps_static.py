"""Phase D/E — form-registry 화면 caps 매핑 정적 회귀 (누락 0)."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import TestCase, main

_REPO = Path(__file__).resolve().parent.parent
_FRONTEND = _REPO / "도서물류관리프로그램" / "frontend"
_FORM_REGISTRY = _FRONTEND / "src" / "lib" / "form-registry.ts"
_SCREEN_CAPS = _FRONTEND / "src" / "lib" / "screen-caps.ts"
_USE_PERMS = _FRONTEND / "src" / "lib" / "use-permissions.ts"
_GATES = _FRONTEND / "src" / "components" / "auth" / "permission-gates.tsx"
_SIDEBAR = _FRONTEND / "src" / "components" / "app-shell" / "sidebar.tsx"
_AUTH_CTX = _FRONTEND / "src" / "contexts" / "auth-context.tsx"


class ScreenCapsStaticTest(TestCase):
    def test_infrastructure_exports(self) -> None:
        caps = _SCREEN_CAPS.read_text(encoding="utf-8")
        perms = _USE_PERMS.read_text(encoding="utf-8")
        gates = _GATES.read_text(encoding="utf-8")
        self.assertIn("deriveScreenCaps", caps)
        self.assertIn("useScreenCaps", perms)
        self.assertIn("getScreenCaps", perms)
        self.assertIn("WriteGate", gates)
        self.assertIn("PrintGate", gates)

    def test_routed_phase12_forms_have_required_permission(self) -> None:
        """라우트가 있는 phase1/phase2 화면은 caps 도출용 requiredPermission 필수."""
        text = _FORM_REGISTRY.read_text(encoding="utf-8")
        blocks = re.findall(
            r"\{[^{}]*route:\s*\"[^\"]+\"[^{}]*phase:\s*\"phase[12]\"[^{}]*\}",
            text,
            re.DOTALL,
        )
        missing: list[str] = []
        for block in blocks:
            id_m = re.search(r'id:\s*"([^"]+)"', block)
            if not id_m:
                continue
            fid = id_m.group(1)
            # DEC-124(2026-07-24) — 총판 전용 출고내역서(Sobo39 /outbound/statement)는
            # 메뉴 매트릭스를 우회(`menuId: null`)하고 `distributorOnly` 플래그로만 노출을
            # 게이팅하는 읽기 전용 화면(caps 소비 없음, 백엔드 총판 게이트 별도). 그 두
            # 표식이 함께 있는 블록만 예외 — 나머지 라우트 폼은 종전대로 필수.
            if re.search(r"distributorOnly:\s*true", block) and re.search(
                r"menuId:\s*null", block
            ):
                continue
            if "requiredPermission:" not in block:
                missing.append(fid)
        self.assertEqual(
            missing,
            [],
            f"requiredPermission 누락 phase1/2 라우트 폼: {missing[:12]}",
        )

    def test_sidebar_hides_inaccessible_menus(self) -> None:
        """DEC-243 (2026-09-06 사용자 "접근이 안되면 보이지도 않게") — MENUVIS-DEC-06 UX 를 대체.

        종전에는 레거시 ShowMessage(E_Connect) 를 흉내 내 Fxx=X·라이선스 미보유 화면을 회색
        disabled 로 노출했다. 이제 사이드바 ``isVisibleForm`` 은 ① 매트릭스 ``visible``,
        ② 라이선스 미보유 ``disabled``, ③ ``canAccessScreen``(Fxx read/권한) 을 모두 숨김으로
        판정한다. 백엔드 PermissionGuard(L1)는 불변 — 직접 URL 은 화면 canRead 게이트가 막는다.
        권한 로딩 중에는 caps 로 숨기지 않는다(빈 사이드바 깜빡임 방지).
        """
        text = _SIDEBAR.read_text(encoding="utf-8")
        self.assertIn("if (!menuState.visible || menuState.disabled) return false;", text)
        self.assertIn("if (perms.isLoading) return true;", text)
        self.assertIn("return perms.canAccessScreen(form);", text)
        # disabled(회색) 렌더 분기는 도달 불가라 제거됐다.
        self.assertNotIn("menuDisabled", text)
        self.assertNotIn("읽기 전용으로 표시됩니다", text)

    def test_master_forms_have_license_fkey(self) -> None:
        """DEC-RBAC-04 — 기초관리 핵심 마스터 화면은 ``licenseFkey`` 가 부착돼야 한다.

        ``.read`` 만으로 ``canWrite=true`` 가 되는 회귀를 차단하기 위해 caps 산출의
        단일 정본을 ``licenseFkey`` + JWT ``fxx_caps`` 셀로 강제한다.
        """
        text = _FORM_REGISTRY.read_text(encoding="utf-8")
        # form 블록을 안전하게 추출 (중첩 객체 없는 단순 폼만 — 본 검사 대상)
        blocks = re.findall(
            r"\{\s*id:\s*\"(Sobo[^\"]+)\",[^{}]*\}",
            text,
            re.DOTALL,
        )
        master_required = {
            "Sobo11": "F11",
            "Sobo12": "F12",
            "Sobo13": "F13",
            "Sobo14": "F14",
            "Sobo15": "F15",
            "Sobo17": "F17",
            "Sobo11_gbun": "F11",
            "Sobo14_gbun": "F14",
        }
        # raw block 추출 (id 매칭 → 본문)
        for fid, expected in master_required.items():
            pattern = re.compile(
                r"\{\s*id:\s*\"" + re.escape(fid) + r"\",[^{}]*?(?=\n\s*\})",
                re.DOTALL,
            )
            m = pattern.search(text)
            self.assertIsNotNone(m, f"form-registry 에 {fid} 가 없다")
            block = m.group(0)
            self.assertIn(
                f'licenseFkey: "{expected}"',
                block,
                f"{fid} 에 licenseFkey: \"{expected}\" 부착 누락 (DEC-RBAC-04).",
            )

    def test_screen_caps_does_not_use_read_only_for_write(self) -> None:
        """`.read` 코드 보유만으로 ``canWrite=true`` 되던 L53 회귀의 정적 차단."""
        caps = _SCREEN_CAPS.read_text(encoding="utf-8")
        # 회귀 시그니처: ``hasWrite = resolver.has(writeCode) || resolver.has(code)``
        self.assertNotRegex(
            caps,
            r"hasWrite\s*=\s*resolver\.has\(writeCode\)\s*\|\|\s*resolver\.has\(code\)",
            "deriveScreenCaps 가 `.read` 만으로 canWrite=true 가 되는 구문을 다시 도입했다.",
        )
        # 신규 정본 시그니처가 있어야 한다 — fxx_caps 우선 폴백.
        self.assertIn("fxxCaps", caps)
        self.assertIn("licenseFkey", caps)

    def test_auth_context_user_info_has_fxx_caps(self) -> None:
        """JWT ↔ 프론트 UserInfo 가 ``fxx_caps`` 필드를 정의한다."""
        text = _AUTH_CTX.read_text(encoding="utf-8")
        self.assertIn("fxx_caps", text)
        self.assertIn("fxxCaps", text)


if __name__ == "__main__":
    main(verbosity=2)
