"""마스터 코드 «기존 값 불변» 가드 (DEC-270).

사용자 규칙(2026-09-09): **코드에 적용되는 로직은 기존 코드를 절대 변경하지 않고, 신규 코드에만
적용되어야 한다.** 채번·폭·접두 스킴은 «제안/등록» 경로에서만 동작해야 하고, 이미 존재하는
마스터 행의 코드 컬럼(Gcode)은 어떤 경로로도 UPDATE 되면 안 된다 — 코드가 바뀌면 그 코드로
쌓여 있던 전표·재고(S1_Ssub/Sg_Csum/Sv_Ghng) 가 통째로 고아가 된다.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.services.g1_ggeo_adapt import customer_patch_targets  # noqa: E402
from app.services.g2_ggwo_adapt import inbound_vendor_patch_targets  # noqa: E402
from app.services.g4_book_adapt import _BOOK_READONLY_COLS, book_patch_targets  # noqa: E402

# 마스터 테이블 — 여기의 Gcode 는 «코드 자체»(전표의 거래처 Gcode 와 달리 바뀌면 안 된다).
_MASTER_TABLES = ("G1_Ggeo", "G2_Ggwo", "G3_Gjeo", "G4_Book")
# "UPDATE <마스터> SET …" 의 SET 절(WHERE 앞)에 Gcode 대입이 있으면 위반. WHERE Gcode=%s 는 정상.
_UPDATE_MASTER = re.compile(
    r"UPDATE\s+(?:" + "|".join(_MASTER_TABLES) + r")\b\s+SET\b(?P<sets>.*?)(?:\bWHERE\b|$)",
    re.IGNORECASE,
)
_SETS_GCODE = re.compile(r"\bGcode\s*=", re.IGNORECASE)


class MasterCodeNeverUpdatedTests(TestCase):
    def test_no_sql_literal_updates_a_master_code_column(self) -> None:
        offenders: list[str] = []
        for path in sorted((BACKEND / "app").rglob("*.py")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for lineno, line in enumerate(text.splitlines(), start=1):
                m = _UPDATE_MASTER.search(line)
                if m and _SETS_GCODE.search(m.group("sets")):
                    offenders.append(f"{path.relative_to(BACKEND)}:{lineno}: {line.strip()}")
        self.assertEqual(offenders, [], "기존 마스터 코드를 UPDATE 하는 SQL 이 생겼다(DEC-270)")

    def test_patch_targets_exclude_the_code_column(self) -> None:
        # 컬럼 메타에 gcode 가 있어도 PATCH 대상에서는 빠져야 한다(동적 SET 조립의 진짜 관문).
        cols = {"gcode", "gname", "hcode", "gubun", "ocode"}
        exact = {c: c.capitalize() for c in cols}
        for label, targets in (
            ("book", book_patch_targets(cols, exact)),
            ("customer", customer_patch_targets(cols, exact)),
            ("inbound_vendor", inbound_vendor_patch_targets(cols, exact)),
        ):
            self.assertNotIn("gcode", {k.lower() for k in targets}, f"{label} PATCH 에 코드가 들렸다")

    def test_book_code_stays_on_the_readonly_list(self) -> None:
        self.assertIn("gcode", _BOOK_READONLY_COLS)


class CodeAllocationIsCreateOnlyTests(TestCase):
    """채번(next_master_code / 접두 채번)은 신규 등록 경로에서만 호출된다."""

    def test_next_code_is_called_only_from_the_next_code_endpoint(self) -> None:
        callers: list[str] = []
        for path in sorted((BACKEND / "app").rglob("*.py")):
            text = path.read_text(encoding="utf-8", errors="replace")
            for lineno, line in enumerate(text.splitlines(), start=1):
                if re.search(r"\b(next_master_code|next_customer_code_by_prefix)\s*\(", line) \
                        and not line.lstrip().startswith(("def ", "async def ")):
                    callers.append(f"{path.relative_to(BACKEND)}:{lineno}")
        # 라우터의 /next-code 엔드포인트(제안 전용) 2줄 외에는 호출처가 없어야 한다.
        self.assertTrue(callers, "채번 호출처를 찾지 못했다 — 스캔 규칙이 낡았다")
        self.assertTrue(
            all(c.startswith("app/routers/masters.py") for c in callers),
            f"채번이 제안 경로 밖에서 호출된다(DEC-270): {callers}",
        )

    def test_new_screens_fill_the_code_only_when_empty(self) -> None:
        # 상세(수정) 화면은 /next-code 를 부르지 않는다 — 부르면 기존 코드를 덮어쓸 수 있다.
        frontend = ROOT / "도서물류관리프로그램" / "frontend" / "src"
        callers = [
            str(p.relative_to(frontend))
            for p in sorted(frontend.rglob("*.tsx"))
            if ".nextCode(" in p.read_text(encoding="utf-8", errors="replace")
        ]
        self.assertTrue(callers, "프론트 채번 호출처를 찾지 못했다 — 스캔 규칙이 낡았다")
        for c in callers:
            self.assertTrue(c.endswith("new/page.tsx"), f"신규 화면 밖에서 채번을 부른다: {c}")


if __name__ == "__main__":
    main()
