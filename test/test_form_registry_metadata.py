"""DEC-059 — `FormMeta` 3축 메타(`phase` ∥ `roadmapWave` ∥ `crudParity`) 정적 회귀 가드.

대상
-----
- ``도서물류관리프로그램/frontend/src/lib/form-registry.ts`` 의 `FORM_REGISTRY` 항목.

검증 (docs/menu-roadmap-waves.md §5)
------------------------------------
1. **허용값**
   - `roadmapWave` 가 정의되어 있다면 ``"p2" | "p3" | "p4"`` 중 하나.
   - `crudParity` 가 정의되어 있다면 ``"R" | "RU" | "CRUD" | "STUB"`` 중 하나.
2. **일관성**
   - `phase === "phase1"` + `crudParity ∈ {R, RU, STUB}` 행은 반드시
     `crudNotes` (또는 `scenario.blockers`) 에 한 줄 이상 사유 보유 —
     "녹색 = 레거시 동일" 오해 차단.
3. **인벤토리 베이스라인**
   - 1차 인벤토리(`docs/crud-backlog.md`) 에서 식별된 핵심 R/RU/STUB 화면 6건이
     실제 `form-registry.ts` 에 채워졌는지 회귀 확인 — 다음 사이클 §5.4
     "phase1 화면은 crudParity 비어있으면 안 됨" 에러 승격 전 단계.

격리
-----
- TS 파일을 정규식으로 파싱(파서/노드 의존 0). DB·네트워크 0.
- 사용자 룰 부합 — 신규 모듈 0(``test_legacy_coverage_audit.py`` 정규식 파싱
  컨벤션 1:1 재사용).
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = (
    REPO_ROOT
    / "도서물류관리프로그램"
    / "frontend"
    / "src"
    / "lib"
    / "form-registry.ts"
)

ALLOWED_WAVES = {"p2", "p3", "p4"}
ALLOWED_CRUD = {"R", "RU", "CRUD", "STUB"}
PARTIAL_CRUD = {"R", "RU", "STUB"}


def _registry_text() -> str:
    return REGISTRY_PATH.read_text(encoding="utf-8")


def _parse_entries(text: str) -> list[dict]:
    """`FORM_REGISTRY` 의 각 객체 리터럴을 dict 로 환원.

    값 추출은 *문자열 리터럴* 만 본다 (3축 메타는 모두 string literal).
    `scenario.blockers` 는 단순 *존재 여부* 만 확인하면 충분(문자열 배열).
    """
    # `export const FORM_REGISTRY: FormMeta[] = [` 의 *마지막* `[` 만 잡아야 한다
    # (앞쪽 `FormMeta[]` 의 `[` 와 충돌 회피).
    m = re.search(r"export const FORM_REGISTRY[^=]*=\s*\[", text)
    assert m is not None, "FORM_REGISTRY 선언이 사라졌다"
    array_start = m.end() - 1  # 마지막 `[` 의 위치
    body = text[array_start:]
    entries: list[dict] = []
    bracket_depth = 0
    brace_depth = 0
    capturing = False
    buf: list[str] = []
    for ch in body:
        if ch == "[":
            bracket_depth += 1
            continue
        if ch == "]":
            bracket_depth -= 1
            if bracket_depth == 0:
                break
            continue
        if ch == "{":
            brace_depth += 1
            if bracket_depth == 1 and brace_depth == 1:
                capturing = True
                buf = []
        if capturing:
            buf.append(ch)
        if ch == "}":
            brace_depth -= 1
            if capturing and brace_depth == 0:
                entries.append(_object_to_dict("".join(buf)))
                capturing = False
    return entries


_KV = re.compile(r'(?P<key>\w+)\s*:\s*"(?P<val>[^"\\]*(?:\\.[^"\\]*)*)"')
_BLOCKERS = re.compile(r"blockers\s*:\s*\[")


def _object_to_dict(literal: str) -> dict:
    out: dict = {}
    for m in _KV.finditer(literal):
        key = m.group("key")
        if key in {
            "id",
            "folder",
            "caption",
            "menuGroup",
            "route",
            "phase",
            "requiredPermission",
            "roadmapWave",
            "crudParity",
            "crudNotes",
        }:
            out.setdefault(key, m.group("val"))
    out["_has_blockers"] = bool(_BLOCKERS.search(literal))
    return out


class FormRegistryMetaShapeTests(TestCase):
    """허용값 + 일관성 1차."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.entries = _parse_entries(_registry_text())
        assert cls.entries, "FORM_REGISTRY 파싱이 0건이 되면 가드 의미가 사라진다"

    def test_roadmap_wave_allowed_values(self) -> None:
        bad = [
            (e.get("id"), e.get("roadmapWave"))
            for e in self.entries
            if e.get("roadmapWave") and e.get("roadmapWave") not in ALLOWED_WAVES
        ]
        self.assertEqual(
            bad,
            [],
            "roadmapWave 는 'p2'|'p3'|'p4' 중 하나여야 한다 (docs/menu-roadmap-waves.md §2).",
        )

    def test_crud_parity_allowed_values(self) -> None:
        bad = [
            (e.get("id"), e.get("crudParity"))
            for e in self.entries
            if e.get("crudParity") and e.get("crudParity") not in ALLOWED_CRUD
        ]
        self.assertEqual(
            bad,
            [],
            "crudParity 는 'R'|'RU'|'CRUD'|'STUB' 중 하나여야 한다 (docs/menu-roadmap-waves.md §4).",
        )

    def test_phase1_partial_crud_must_have_reason(self) -> None:
        """`phase1` + `R`/`RU`/`STUB` 행은 `crudNotes` 또는 `scenario.blockers` 필수.

        목적: 사이드바 녹색 체크가 "레거시와 완전 동일" 로 오해되는 것을 차단
        (예: master/publisher 1차 READ only).
        """
        offenders = []
        for e in self.entries:
            if e.get("phase") != "phase1":
                continue
            if e.get("crudParity") not in PARTIAL_CRUD:
                continue
            has_notes = bool((e.get("crudNotes") or "").strip())
            has_blockers = bool(e.get("_has_blockers"))
            if not (has_notes or has_blockers):
                offenders.append(e.get("id"))
        self.assertEqual(
            offenders,
            [],
            "phase1 + R/RU/STUB 행은 crudNotes 또는 scenario.blockers 사유가 필요하다 "
            "(docs/menu-roadmap-waves.md §5.3).",
        )


class FormRegistryInventoryBaselineTests(TestCase):
    """1차 인벤토리(`docs/crud-backlog.md`) 회귀 가드.

    핵심 R/RU/STUB 6건이 실제 `form-registry.ts` 에 채워졌는지 검증 —
    drift 발생 시 즉시 FAIL.
    """

    @classmethod
    def setUpClass(cls) -> None:
        entries = _parse_entries(_registry_text())
        # 같은 id 가 복수 라우트로 등록될 수 있다(DEC-124: 총판 출고내역서가 할인율과 같은
        # 레거시 폴더 Subu39 를 공유해 `id: "Sobo39"` 두 건 — 매트릭스 MULTI_MAP). 마지막
        # 항목이 앞 항목을 덮어쓰지 않도록 route 별 사전을 함께 둔다.
        cls.by_id = {e["id"]: e for e in entries if e.get("id")}
        cls.by_route = {e["route"]: e for e in entries if e.get("route")}

    def _assert(
        self, form_id: str, *, wave: str | None, crud: str, route: str | None = None
    ) -> None:
        e = self.by_route.get(route) if route else self.by_id.get(form_id)
        self.assertIsNotNone(e, f"{form_id} 가 form-registry 에서 사라졌다")
        if route:
            self.assertEqual(e.get("id"), form_id, f"{route} 의 id")
        self.assertEqual(e.get("roadmapWave"), wave, f"{form_id}.roadmapWave")
        self.assertEqual(e.get("crudParity"), crud, f"{form_id}.crudParity")

    def test_publisher_master_read_only(self) -> None:
        self._assert("Sobo17", wave=None, crud="CRUD")

    def test_book_code_master_read_only(self) -> None:
        self._assert("Sobo38", wave=None, crud="CRUD")

    def test_customer_master_read_update(self) -> None:
        self._assert("Sobo11", wave=None, crud="CRUD")

    def test_special_master_g6_read_update(self) -> None:
        """Sobo16은 G6_Ggeo 목록 + 신규/수정/삭제를 모두 지원한다."""
        self._assert("Sobo16_special", wave="p2", crud="CRUD")

    def test_discount_master_crud(self) -> None:
        # 할인율(마스터) 항목 — 같은 id 의 총판 출고내역서(/outbound/statement, DEC-124)와
        # 구분하기 위해 route 로 선택. 사이드바 숨김(DEC-155)과 무관하게 CRUD 구현은 유지.
        self._assert("Sobo39", wave=None, crud="CRUD", route="/master/discount")

    def test_delivery_management_courier_ru(self) -> None:
        """내부 라인/메모 API 구현 — 외부 택배사 API는 STUB 아님(courier_management.yaml 일정 분리)."""
        self._assert("Sobo28_delivery", wave="p4", crud="RU")

    def test_tax_invoice_external_channel_stub(self) -> None:
        self._assert("Sobo49_tax", wave="p3", crud="RU")

    def test_master_menu_group_has_no_p3_wave(self) -> None:
        offenders = []
        for e in self.by_id.values():
            if e.get("menuGroup") != "master":
                continue
            if e.get("roadmapWave") == "p3":
                offenders.append(e.get("id"))
        self.assertEqual(
            offenders,
            [],
            "기초관리(master) 메뉴는 roadmapWave 'p3'(W3) 없이 정리되어야 한다.",
        )
