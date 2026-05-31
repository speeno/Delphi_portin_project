"""Phase E — 전 계정 Fxx→caps 결정적 해석 커버리지 가드 (ungated 0)."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import TestCase, main

_ROOT = Path(__file__).resolve().parent.parent
_BACKEND = _ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND))
sys.path.insert(0, str(_ROOT / "debug"))

from probe_account_fxx_caps import derive_account_derivation  # noqa: E402
from app.services.auth_service import _load_legacy_permission_index  # noqa: E402


class AccountMenuFidelityCoverageTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        audit_path = _ROOT / "analysis" / "audit" / "account-menu-fxx-all.json"
        cls.catalog = _load_legacy_permission_index()
        cls.rows: list[dict] = []
        if not audit_path.is_file():
            return
        doc = json.loads(audit_path.read_text(encoding="utf-8"))
        for sid, sdata in (doc.get("servers") or {}).items():
            if not isinstance(sdata, dict):
                continue
            for row in sdata.get("login_rows") or []:
                if isinstance(row, dict):
                    r = dict(row)
                    r["server_id"] = sid
                    cls.rows.append(r)

    def test_all_accounts_deterministic_caps(self) -> None:
        if not self.rows:
            self.skipTest("account-menu-fxx-all.json 없음 — Phase A probe 수동 실행 필요")
        ungated: list[str] = []
        unmapped_total = 0
        for row in self.rows:
            fxx = row.get("fxx") or {}
            granted = {
                k for k, v in fxx.items() if str(v or "").strip().upper() in ("O", "R")
            }
            if not granted:
                continue
            fk = row.get("four_key") or {}
            label = f"{row.get('server_id')}:{fk.get('gcode')}:{fk.get('hcode')}"
            d = derive_account_derivation(fxx, self.catalog)
            if d.get("login_profile") in (None, ""):
                ungated.append(f"{label}:no_profile")
            if not d.get("permissions") and not d.get("role"):
                ungated.append(f"{label}:no_perms")
            for fkey in d.get("unmapped_fkeys") or []:
                if fkey in self.catalog:
                    unmapped_total += 1
        self.assertEqual(ungated, [], f"ungated 계정: {ungated[:8]}")
        self.assertEqual(
            unmapped_total,
            0,
            "카탈로그 미매핑 f-컬럼이 있음 — permission-keys-catalog 정합 필요",
        )

    def test_focus_gyomunsa_gyeongri_differ(self) -> None:
        if not self.rows:
            self.skipTest("account-menu-fxx-all.json 없음")
        by_gcode: dict[str, dict] = {}
        for row in self.rows:
            fk = row.get("four_key") or {}
            gc = fk.get("gcode")
            if gc in ("교문사", "경리부") and row.get("server_id") == "remote_153":
                by_gcode[gc] = row
        if "교문사" not in by_gcode or "경리부" not in by_gcode:
            self.skipTest("집중 계정 행 없음")
        gy = derive_account_derivation(by_gcode["교문사"]["fxx"], self.catalog)
        gr = derive_account_derivation(by_gcode["경리부"]["fxx"], self.catalog)
        self.assertEqual(gy["login_profile"], "publisher_main")
        self.assertEqual(gr["login_profile"], "department_accounting")
        self.assertNotEqual(set(gy["permissions"]), set(gr["permissions"]))


if __name__ == "__main__":
    main(verbosity=2)
