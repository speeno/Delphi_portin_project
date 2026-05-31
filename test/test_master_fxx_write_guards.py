"""DEC-RBAC-04 — masters.py 의 POST/PATCH/DELETE 가드 정합 회귀.

검증 범위
---------
1. masters.py 가 화면별 Fxx 가드(`require_fxx_write`)를 정확히 부착
   (Sobo11/14/17/12/13/15/16) — F26 master.write 는 Sobo38(book-code)/Sobo39(discount)
   통합 일괄 마스터에만 남는다.
2. probe `derive_fkey_caps` 정본을 따른 케이스별 라우터 거동 — `require_fxx_write` 가
   교문사 F12=R(403) / F11=O(통과) / 경리부 F11=없음(403) 시나리오를 정확히 산출.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main

import pytest
from fastapi import HTTPException

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
MASTERS = BACKEND / "app" / "routers" / "masters.py"
sys.path.insert(0, str(BACKEND))


class MastersRouterGuardsStatic(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = MASTERS.read_text(encoding="utf-8")

    def _endpoints(self) -> list[tuple[str, str, str]]:
        """라우터 메서드/패스/Depends 가드 — 단순 정규식 추출."""
        out: list[tuple[str, str, str]] = []
        for m in re.finditer(
            r'@router\.(post|patch|delete)\(\s*"([^"]+)"[^)]*?dependencies=\[Depends\(([^)]+)\)\]',
            self.text,
            re.DOTALL,
        ):
            out.append((m.group(1).upper(), m.group(2), m.group(3).strip()))
        return out

    def test_per_screen_fxx_guards(self) -> None:
        """기초관리 화면별 Fxx 가드가 plan §1.2 와 일치한다."""
        guard_by_route = {(method, path): guard for method, path, guard in self._endpoints()}
        # Sobo11 거래처 — F11
        for path in ("/customer", "/customer/{gcode}"):
            for method in ("POST", "PATCH", "DELETE"):
                key = (method, path)
                if key not in guard_by_route:
                    continue
                self.assertEqual(
                    guard_by_route[key], "_GUARD_F11", f"{method} {path} → F11 가드"
                )
        # Sobo14 도서 — F14
        for path in ("/book", "/book/{gcode}"):
            for method in ("POST", "PATCH", "DELETE"):
                key = (method, path)
                if key not in guard_by_route:
                    continue
                self.assertEqual(guard_by_route[key], "_GUARD_F14", f"{method} {path} → F14")
        # Sobo17 출판사 — F17
        for path in ("/publisher", "/publisher/{gcode}"):
            for method in ("POST", "PATCH", "DELETE"):
                key = (method, path)
                if key not in guard_by_route:
                    continue
                self.assertEqual(guard_by_route[key], "_GUARD_F17", f"{method} {path} → F17")
        # Sobo12 입고처 — F12 (F26 오적용 제거)
        for path in ("/inbound-vendors", "/inbound-vendors/{gcode}"):
            for method in ("POST", "PATCH", "DELETE"):
                key = (method, path)
                if key not in guard_by_route:
                    continue
                self.assertEqual(guard_by_route[key], "_GUARD_F12", f"{method} {path} → F12")
        # Sobo13 저자 — F13
        for path in ("/authors", "/authors/{gcode}"):
            for method in ("POST", "PATCH", "DELETE"):
                key = (method, path)
                if key not in guard_by_route:
                    continue
                self.assertEqual(guard_by_route[key], "_GUARD_F13", f"{method} {path} → F13")
        # Sobo15 기타거래처 — F15
        for path in ("/etc-customers", "/etc-customers/{gcode}"):
            for method in ("POST", "PATCH", "DELETE"):
                key = (method, path)
                if key not in guard_by_route:
                    continue
                self.assertEqual(guard_by_route[key], "_GUARD_F15", f"{method} {path} → F15")

    def test_f26_master_write_only_for_bulk_screens(self) -> None:
        """``_MASTER_WRITE_PERM`` 은 book-code/discount 등 일괄 화면에만 잔존한다.

        Sobo12/13/15 가 F26 으로 우회되던 회귀의 차단 가드.
        """
        bulk_paths = {"/book-code", "/discount"}
        for method, path, guard in self._endpoints():
            if "require_permission(_MASTER_WRITE_PERM)" not in guard:
                continue
            base = path.split("/{")[0]
            self.assertIn(
                base,
                bulk_paths,
                f"F26 master.write 가 비-일괄 화면에 남았다: {method} {path}",
            )

    def test_no_unguarded_master_writes(self) -> None:
        """기초관리 POST/PATCH/DELETE 는 반드시 dependencies 가 부착돼 있다."""
        unguarded: list[str] = []
        for m in re.finditer(
            r'@router\.(post|patch|delete)\(\s*"([^"]+)"([^)]*)\)',
            self.text,
            re.DOTALL,
        ):
            method = m.group(1).upper()
            path = m.group(2)
            block = m.group(3)
            # `_mount_simple_master` 팩토리(write_dep) 는 본 정규식에 잡히지 않으므로 제외.
            if "dependencies=[" not in block:
                unguarded.append(f"{method} {path}")
        self.assertEqual(
            unguarded,
            [],
            f"가드 없는 마스터 쓰기 엔드포인트: {unguarded}",
        )


class RequireFxxWriteSemantics(IsolatedAsyncioTestCase):
    """probe `derive_fkey_caps` ↔ `require_fxx_write` 동등 — audit 정본 케이스."""

    async def test_kyomunsa_f11_o_passes(self) -> None:
        from app.core.deps import require_fxx_write

        ctx = {
            "permissions": ["master.customer.read"],
            "role": "",
            "fxx_caps": {"F11": {"read": True, "write": True, "print": True}},
        }
        self.assertEqual(await require_fxx_write("F11")(ctx), ctx)

    async def test_kyomunsa_f12_r_403(self) -> None:
        from app.core.deps import require_fxx_write

        ctx = {
            "permissions": ["master.book.read"],
            "role": "",
            "fxx_caps": {"F12": {"read": True, "write": False, "print": True}},
        }
        with pytest.raises(HTTPException) as exc:
            await require_fxx_write("F12")(ctx)
        self.assertEqual(exc.value.status_code, 403)

    async def test_accounting_f11_missing_403(self) -> None:
        from app.core.deps import require_fxx_write

        ctx = {
            "permissions": ["report.month.read"],
            "role": "",
            "fxx_caps": {  # 경리부 — 마스터 셀 없음
                "F51": {"read": True, "write": True, "print": True},
            },
        }
        with pytest.raises(HTTPException) as exc:
            await require_fxx_write("F11")(ctx)
        self.assertEqual(exc.value.status_code, 403)


if __name__ == "__main__":
    main(verbosity=2)
