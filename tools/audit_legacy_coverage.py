"""레거시 포팅 누락 회귀 가드 (DEC-054).

`legacy_source/*.dfm` 의 root form Caption 인벤토리(`analysis/form_inventory.json`)
와 프런트 `form-registry.ts` 를 비교해 다음 4 카테고리로 분류한다.

  - missing       : DFM caption 있지만 registry id 에도 없고
                    어떤 entry 의 scenario.legacy_form 에서도 참조되지 않음
  - caption_mismatch : DFM form_name == registry id 인데
                       caption(공백·괄호 정규화 후) 불일치
  - allowed       : 위 둘 중 하나에 해당하지만 coverage-allowlist.yaml 매칭
  - ok            : DFM ↔ registry 의도 일치

사용:
  python3 tools/audit_legacy_coverage.py            # report 만 갱신
  python3 tools/audit_legacy_coverage.py --check    # 신규 위반 시 non-zero exit
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
INVENTORY_PATH = REPO_ROOT / "analysis" / "form_inventory.json"
REGISTRY_PATH = (
    REPO_ROOT / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "form-registry.ts"
)
ALLOWLIST_PATH = REPO_ROOT / "legacy-analysis" / "coverage-allowlist.yaml"
REPORT_PATH = REPO_ROOT / "analysis" / "audit" / "legacy-coverage-report.json"
LEGACY_SOURCE_DIR = REPO_ROOT / "legacy_delphi_source" / "legacy_source"


# ───────────────────────── data shapes ─────────────────────────


@dataclass
class DfmEntry:
    form_name: str
    form_class: str
    file: str
    caption: str


@dataclass
class RegistryEntry:
    id: str
    caption: str
    legacy_form: str | None = None  # scenario.legacy_form (.dfm suffix 제거 후)


@dataclass
class Allowlist:
    missing_form_names: dict[str, dict[str, Any]] = field(default_factory=dict)
    mismatch_form_names: dict[str, dict[str, Any]] = field(default_factory=dict)
    # registry id 만 존재 (DFM form_name 으로는 미존재) 신규 포팅 의도 deferral.
    # baseline/mismatch 에 영향 없음 — surface 만.
    intentional_new_form_names: dict[str, dict[str, Any]] = field(default_factory=dict)


# ───────────────────────── loaders ─────────────────────────


def load_dfm_inventory(inventory_path: Path = INVENTORY_PATH) -> list[DfmEntry]:
    """root *.dfm (= legacy_source 직속) + caption non-null 만 후보로 채택.

    서브디렉토리(Interbase/, Data/, version/ …) 는 백업·대체 구현이라 제외 — 같은
    `form_name` 다중 caption 충돌 회피.
    """
    raw = json.loads(inventory_path.read_text(encoding="utf-8"))
    legacy_root = LEGACY_SOURCE_DIR.resolve()
    seen: dict[str, DfmEntry] = {}
    for item in raw:
        caption = item.get("caption")
        if not isinstance(caption, str) or not caption.strip():
            continue
        file_path = Path(item["file"]).resolve()
        try:
            rel = file_path.relative_to(legacy_root)
        except ValueError:
            continue
        # 루트 직속 .dfm 만 (Path.parts == ('Subu67.dfm',))
        if len(rel.parts) != 1:
            continue
        form_name = item["form_name"]
        if form_name in seen:
            continue
        seen[form_name] = DfmEntry(
            form_name=form_name,
            form_class=item.get("form_class", ""),
            file=str(file_path),
            caption=caption.strip(),
        )
    return sorted(seen.values(), key=lambda e: e.form_name.lower())


_ENTRY_OPEN_RE = re.compile(r"^\s*\{\s*$")
_ID_RE = re.compile(r'^\s*id:\s*"([^"]+)"\s*,?\s*$')
_CAPTION_RE = re.compile(r'^\s*caption:\s*"([^"]+)"\s*,?\s*$')
_LEGACY_FORM_RE = re.compile(r'^\s*legacy_form:\s*"([^"]+)"\s*,?\s*$')


def parse_form_registry(registry_path: Path = REGISTRY_PATH) -> list[RegistryEntry]:
    """form-registry.ts 의 FORM_REGISTRY 배열 entry 를 텍스트 정규식으로 추출.

    AST 파서(typescript) 도입 회피 (사용자 룰 — 단순 정규식 + 4 필드만).
    `id`/`caption`/`legacy_form` 만 surface 한다 (folder/menuGroup/route 비교 불필요).
    """
    text = registry_path.read_text(encoding="utf-8")
    # FORM_REGISTRY 배열 본문만 추출
    m = re.search(r"FORM_REGISTRY[^=]*=\s*\[(.+)\];", text, re.DOTALL)
    body = m.group(1) if m else text

    entries: list[RegistryEntry] = []
    current_id: str | None = None
    current_caption: str | None = None
    current_legacy: str | None = None

    for line in body.splitlines():
        # id 출현 시 새 entry 시작 — 이전 entry flush
        id_m = _ID_RE.match(line)
        if id_m:
            if current_id is not None and current_caption is not None:
                entries.append(
                    RegistryEntry(
                        id=current_id,
                        caption=current_caption,
                        legacy_form=current_legacy,
                    )
                )
            current_id = id_m.group(1)
            current_caption = None
            current_legacy = None
            continue
        cap_m = _CAPTION_RE.match(line)
        if cap_m and current_id is not None and current_caption is None:
            current_caption = cap_m.group(1)
            continue
        leg_m = _LEGACY_FORM_RE.match(line)
        if leg_m and current_id is not None and current_legacy is None:
            current_legacy = re.sub(r"\.dfm$", "", leg_m.group(1), flags=re.IGNORECASE)
            continue
    if current_id is not None and current_caption is not None:
        entries.append(
            RegistryEntry(
                id=current_id,
                caption=current_caption,
                legacy_form=current_legacy,
            )
        )
    return entries


def load_allowlist(allowlist_path: Path = ALLOWLIST_PATH) -> Allowlist:
    if not allowlist_path.exists():
        return Allowlist()
    raw = yaml.safe_load(allowlist_path.read_text(encoding="utf-8")) or {}
    missing = {}
    for item in raw.get("missing_forms", []) or []:
        if isinstance(item, dict) and item.get("form_name"):
            missing[item["form_name"]] = {
                "reason": item.get("reason", ""),
                "until": item.get("until", ""),
            }
    mismatch = {}
    for item in raw.get("caption_mismatches", []) or []:
        if isinstance(item, dict) and item.get("form_name"):
            mismatch[item["form_name"]] = {
                "reason": item.get("reason", ""),
                "until": item.get("until", ""),
            }
    intent = {}
    for item in raw.get("intentional_new_forms", []) or []:
        if isinstance(item, dict) and item.get("form_name"):
            intent[item["form_name"]] = {
                "reason": item.get("reason", ""),
                "until": item.get("until", ""),
            }
    return Allowlist(
        missing_form_names=missing,
        mismatch_form_names=mismatch,
        intentional_new_form_names=intent,
    )


# ───────────────────────── core compare ─────────────────────────


_WS_RE = re.compile(r"\s+")


def normalize_caption(text: str) -> str:
    """공백·전각 괄호 정규화 — Caption 정확 비교용."""
    out = _WS_RE.sub("", text or "")
    return out.strip()


_SUFFIX_SPLIT_RE = re.compile(r"^([A-Za-z]+\d+(?:_\d+)?)(?:_[A-Za-z][A-Za-z0-9]*)+$")


def derive_base_form(registry_id: str) -> str:
    """`Sobo67_status` → `Sobo67`. suffix 가 없으면 그대로 반환.

    DFM form_name 명명 규약(`Sobo<digits>(_<digits>)?`)을 base 로 보고
    영문 suffix(_status, _yearbook, _ledger, _stats …)는 derivative 로 해석.
    """
    m = _SUFFIX_SPLIT_RE.match(registry_id)
    return m.group(1) if m else registry_id


def map_registry_to_dfm(
    registry_entries: list[RegistryEntry],
    dfm_form_names: set[str],
) -> dict[str, str | None]:
    """각 registry id → 매칭되는 DFM form_name (없으면 None).

    우선순위:
      1. legacy_form 명시 (e.g. legacy_form: "Sobo67.dfm")
      2. id 정확 일치
      3. id 의 base prefix 일치 (Sobo67_status → Sobo67)
    """
    out: dict[str, str | None] = {}
    for e in registry_entries:
        if e.legacy_form and e.legacy_form in dfm_form_names:
            out[e.id] = e.legacy_form
            continue
        if e.id in dfm_form_names:
            out[e.id] = e.id
            continue
        base = derive_base_form(e.id)
        if base != e.id and base in dfm_form_names:
            out[e.id] = base
            continue
        out[e.id] = None
    return out


def run_audit(
    inventory_path: Path = INVENTORY_PATH,
    registry_path: Path = REGISTRY_PATH,
    allowlist_path: Path = ALLOWLIST_PATH,
) -> dict[str, Any]:
    dfm_entries = load_dfm_inventory(inventory_path)
    registry_entries = parse_form_registry(registry_path)
    allowlist = load_allowlist(allowlist_path)

    dfm_by_name: dict[str, DfmEntry] = {d.form_name: d for d in dfm_entries}
    dfm_form_names = set(dfm_by_name.keys())
    registry_to_dfm = map_registry_to_dfm(registry_entries, dfm_form_names)
    # DFM → 매칭된 registry entry 목록 (1:N — 한 DFM 이 여러 registry id 로 분기 가능)
    dfm_to_registry: dict[str, list[RegistryEntry]] = {}
    for e in registry_entries:
        dfm_name = registry_to_dfm.get(e.id)
        if dfm_name:
            dfm_to_registry.setdefault(dfm_name, []).append(e)

    missing: list[dict[str, Any]] = []
    caption_mismatch: list[dict[str, Any]] = []
    allowed: list[dict[str, Any]] = []
    ok: list[dict[str, Any]] = []

    # 축 1: DFM 기준 — registry 매핑 자체가 없으면 missing
    for dfm in dfm_entries:
        regs = dfm_to_registry.get(dfm.form_name, [])
        if not regs:
            entry = {
                "form_name": dfm.form_name,
                "form_class": dfm.form_class,
                "dfm_caption": dfm.caption,
                "file": dfm.file,
            }
            if dfm.form_name in allowlist.missing_form_names:
                a = allowlist.missing_form_names[dfm.form_name]
                allowed.append(
                    {
                        **entry,
                        "category": "missing",
                        "reason": a["reason"],
                        "until": a["until"],
                    }
                )
            else:
                missing.append(entry)

    # 축 2: registry 기준 — caption 비교 (form_name = registry id 로 surface)
    for reg in registry_entries:
        dfm_name = registry_to_dfm[reg.id]
        if dfm_name is None:
            # registry id 가 어떤 DFM 과도 매칭되지 않음 — 신규 포팅 추정 (등록 OK).
            continue
        dfm = dfm_by_name[dfm_name]
        if normalize_caption(reg.caption) == normalize_caption(dfm.caption):
            ok.append(
                {
                    "form_name": reg.id,
                    "dfm_form_name": dfm_name,
                    "caption": dfm.caption,
                }
            )
        else:
            entry = {
                "form_name": reg.id,
                "dfm_form_name": dfm_name,
                "registry_caption": reg.caption,
                "dfm_caption": dfm.caption,
                "file": dfm.file,
            }
            if reg.id in allowlist.mismatch_form_names:
                a = allowlist.mismatch_form_names[reg.id]
                allowed.append(
                    {
                        **entry,
                        "category": "caption_mismatch",
                        "reason": a["reason"],
                        "until": a["until"],
                    }
                )
            else:
                caption_mismatch.append(entry)

    # allowlist 자체에 등록됐지만 DFM 인벤토리·registry 어디에도 없는 경우 — cleanup 힌트
    by_id_set = {e.id for e in registry_entries}
    stale_candidates = (
        list(allowlist.missing_form_names.keys())
        + list(allowlist.mismatch_form_names.keys())
    )
    truly_stale = [
        n
        for n in stale_candidates
        if n not in dfm_form_names and n not in by_id_set
    ]
    # intentional_new_forms — yaml 명시분 + missing/mismatch 중 registry id 만 존재하는 것
    # 두 source 합집합. Sobo67_yearbook 같이 신규 포팅 화면 추적용.
    intentional_new_form = sorted(
        set(allowlist.intentional_new_form_names.keys())
        | {n for n in stale_candidates if n in by_id_set and n not in dfm_form_names}
    )

    summary = {
        "total_dfm_candidates": len(dfm_entries),
        "registry_entries": len(registry_entries),
        "ok": len(ok),
        "missing_forms": len(missing),
        "caption_mismatches": len(caption_mismatch),
        "allowed": len(allowed),
    }
    return {
        "generated_at": datetime.now(tz=timezone.utc).isoformat(),
        "summary": summary,
        "missing_forms": sorted(missing, key=lambda x: x["form_name"].lower()),
        "caption_mismatches": sorted(
            caption_mismatch, key=lambda x: x["form_name"].lower()
        ),
        "allowed": sorted(allowed, key=lambda x: x["form_name"].lower()),
        "ok": sorted(ok, key=lambda x: x["form_name"].lower()),
        "stale_allowlist": sorted(truly_stale),
        "intentional_new_forms": list(intentional_new_form),
    }


def write_report(report: dict[str, Any], path: Path = REPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# ───────────────────────── helpers (test 노출) ─────────────────────────


def unallowed_missing(report: dict[str, Any]) -> list[dict[str, Any]]:
    """allowlist 매칭되지 않은 신규 missing 만 반환 (CI gate 용)."""
    return list(report.get("missing_forms", []))


def unallowed_mismatches(report: dict[str, Any]) -> list[dict[str, Any]]:
    """allowlist 매칭되지 않은 신규 caption mismatch 만 반환."""
    return list(report.get("caption_mismatches", []))


def find_entry(rows: list[dict[str, Any]], form_name: str) -> dict[str, Any] | None:
    for row in rows:
        if row.get("form_name") == form_name:
            return row
    return None


def find_caption_diff(
    report: dict[str, Any], registry_id: str
) -> dict[str, Any] | None:
    """caption 비교 결과를 mismatch + allowed(category=caption_mismatch) 통합 검색.

    Sobo67_status 같이 baseline 등재된 항목도 surface 되어야 가드 살아있음 검증 가능.
    """
    for row in report.get("caption_mismatches", []):
        if row.get("form_name") == registry_id:
            return row
    for row in report.get("allowed", []):
        if (
            row.get("form_name") == registry_id
            and row.get("category") == "caption_mismatch"
        ):
            return row
    return None


# ───────────────────────── CLI ─────────────────────────


def _cli() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="신규 missing 또는 caption_mismatch 가 있으면 non-zero exit (CI 게이트).",
    )
    args = parser.parse_args()

    report = run_audit()
    write_report(report)

    s = report["summary"]
    print(
        f"[legacy-coverage] dfm={s['total_dfm_candidates']} "
        f"registry={s['registry_entries']} ok={s['ok']} "
        f"missing={s['missing_forms']} mismatch={s['caption_mismatches']} "
        f"allowed={s['allowed']}"
    )
    if args.check:
        if report["missing_forms"]:
            print(
                "✗ 신규 missing form 발견:",
                ", ".join(e["form_name"] for e in report["missing_forms"]),
                file=sys.stderr,
            )
        if report["caption_mismatches"]:
            print(
                "✗ 신규 caption mismatch:",
                ", ".join(e["form_name"] for e in report["caption_mismatches"]),
                file=sys.stderr,
            )
        if report["missing_forms"] or report["caption_mismatches"]:
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(_cli())
