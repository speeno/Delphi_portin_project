#!/usr/bin/env python3
"""Build WeLove porting coverage matrices from generated, secret-free inputs."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
ANALYSIS = ROOT / "analysis"
TENANTS = ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_seed.json"
CLOSURES = ANALYSIS / "welove_dpr_closures.json"
EXTENDED = ANALYSIS / "welove_build_catalog_extended.json"
RBAC = ROOT / "migration" / "contracts" / "rbac_menu_matrix.yaml"
FORCED_HIDDEN = ROOT / "migration" / "contracts" / "build_forced_hidden_menus.yaml"
LAYOUT_DIR = ANALYSIS / "layout_mappings"

OUT_TENANT = ANALYSIS / "welove_tenant_build_routing_matrix.json"
OUT_SCREEN = ANALYSIS / "welove_screen_contract_coverage.json"
DOC_OUT = ROOT / "docs" / "welove-dpr-closure-coverage.md"

FORM_RE = re.compile(r"^(?P<prefix>Sobo|Subu|Seep|Seak|Seek|Seok|Tong)(?P<num>\d+(?:_\d+)?)", re.IGNORECASE)

# Mapping note stems that do not match FORM_RE still need closure linkage (login shell vs Tong08 scan path).
# Values are lowercase PAS/unit stems present in welove_dpr_closures.json.
LAYOUT_NOTE_EXTRA_UNIT_ALIASES: dict[str, frozenset[str]] = {
    "Id_Logn": frozenset({"chul"}),
    "c8_scan_match": frozenset({"tong08", "tong07"}),
}


def _layout_candidates(form_id: str) -> set[str]:
    candidates = set(_form_candidates(form_id))
    candidates.update(LAYOUT_NOTE_EXTRA_UNIT_ALIASES.get(form_id, frozenset()))
    return candidates


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def _form_candidates(form_id: str) -> set[str]:
    out = {form_id.lower()}
    m = FORM_RE.match(form_id)
    if not m:
        return out
    num = m.group("num")
    for prefix in ("Sobo", "Subu", "Seep", "Seak", "Seek", "Seok", "Tong"):
        out.add(f"{prefix}{num}".lower())
    return out


def _build_id_to_closure_rows(closures: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in closures:
        bid = row.get("existing_build_id") or "UNMAPPED"
        out[bid].append(row)
    return out


def _menu_ids_by_build() -> dict[str, list[str]]:
    rbac = _load_yaml(RBAC)
    by_build: dict[str, set[str]] = defaultdict(set)
    for menu in rbac.get("menus") or []:
        if not isinstance(menu, dict):
            continue
        mid = str(menu.get("id") or "").strip()
        if not mid:
            continue
        for build in menu.get("source_builds") or []:
            by_build[str(build)].add(mid)
    return {k: sorted(v) for k, v in by_build.items()}


def _forced_hidden_by_build() -> dict[str, list[str]]:
    cfg = _load_yaml(FORCED_HIDDEN)
    out: dict[str, list[str]] = {}
    for build_id, row in (cfg.get("builds") or {}).items():
        out[str(build_id)] = sorted(str(x) for x in (row or {}).get("forced_hidden_acc_menu_ids") or [])
    return out


def build_tenant_matrix() -> dict[str, Any]:
    tenants = _load_json(TENANTS).get("tenants") or []
    ext = _load_json(EXTENDED)
    closures = _load_json(CLOSURES).get("closures") or []
    closure_by_build = _build_id_to_closure_rows(closures)
    forced_hidden = _forced_hidden_by_build()
    menu_ids = _menu_ids_by_build()

    rows = []
    for t in tenants:
        bid = str(t.get("active_build_id") or "").strip()
        build_closures = closure_by_build.get(bid, [])
        rows.append(
            {
                "tenant_id": t.get("tenant_id"),
                "tenant_label_kor": t.get("tenant_label_kor"),
                "account_family": t.get("account_family"),
                "active_build_id": bid,
                "build_role": t.get("build_role"),
                "default_account_type": t.get("default_account_type"),
                "primary_server": t.get("primary_server"),
                "db_name_logical": t.get("db_name_logical"),
                "closure_hashes": sorted({c.get("dpr_closure_hash") for c in build_closures if c.get("dpr_closure_hash")}),
                "execution_types": sorted({c.get("execution_type") for c in build_closures if c.get("execution_type")}),
                "menu_source_builds": menu_ids.get(_source_build_alias(bid), []),
                "forced_hidden_acc_menu_ids": forced_hidden.get(bid, []),
                "trace_status": "ok" if bid and build_closures else "build_catalog_only" if bid else "missing_active_build_id",
            }
        )

    return {
        "source": [
            "backend/data/tenants_directory_seed.json",
            "analysis/welove_dpr_closures.json",
            "analysis/welove_build_catalog_extended.json",
            "migration/contracts/rbac_menu_matrix.yaml",
            "migration/contracts/build_forced_hidden_menus.yaml",
        ],
        "secrets_policy": "No DB users/passwords. Routing keys and generated hashes only.",
        "totals": {
            "tenant_count": len(rows),
            "active_build_id_missing": sum(1 for r in rows if not r["active_build_id"]),
            "trace_status_counts": _count(row["trace_status"] for row in rows),
            "extended_dpr_count": ext.get("totals", {}).get("dpr_count", 0),
        },
        "rows": rows,
    }


def _source_build_alias(build_id: str) -> str:
    mapping = {
        "BLD-DIST-STD": "D-STD",
        "BLD-PUB-STD": "P-STD",
        "BLD-DIST-KBT": "D-KBT",
        "BLD-PUB-KBT": "P-KBT",
        "BLD-PUB-WAREHOUSE-WELOVE": "WH-WL",
        "BLD-PUB-WAREHOUSE-MS": "WH-MS",
        "BLD-PUB-WAREHOUSE-BOOKNBOOK-NEW": "WH-BB",
    }
    return mapping.get(build_id, build_id)


def _count(values) -> dict[str, int]:
    out: dict[str, int] = {}
    for value in values:
        out[str(value)] = out.get(str(value), 0) + 1
    return out


def build_screen_coverage() -> dict[str, Any]:
    closures = _load_json(CLOSURES).get("closures") or []
    layout_files = sorted(LAYOUT_DIR.glob("*.md"))
    entries = []
    for layout in layout_files:
        form_id = layout.stem
        candidates = _layout_candidates(form_id)
        variants: dict[tuple[str, str, str, str], dict[str, Any]] = {}
        for closure in closures:
            for unit in closure.get("units") or []:
                unit_name = str(unit.get("unit") or "").lower()
                pas_stem = Path(str(unit.get("resolved_pas_path") or "")).stem.lower()
                dfm_stem = Path(str(unit.get("resolved_dfm_path") or "")).stem.lower()
                if not ({unit_name, pas_stem, dfm_stem} & candidates):
                    continue
                key = (
                    closure.get("existing_build_id") or "UNMAPPED",
                    closure.get("account_family") or "",
                    unit.get("pas_sha1") or "",
                    unit.get("dfm_md5") or "",
                )
                variants.setdefault(
                    key,
                    {
                        "build_id": key[0],
                        "account_family": key[1],
                        "dpr_closure_hash": closure.get("dpr_closure_hash"),
                        "source_pas_path": unit.get("resolved_pas_path"),
                        "source_dfm_path": unit.get("resolved_dfm_path"),
                        "pas_sha1": key[2],
                        "dfm_md5": key[3],
                        "sample_dpr_path": closure.get("dpr_path"),
                        "dpr_count": 0,
                    },
                )
                variants[key]["dpr_count"] += 1
        entries.append(
            {
                "form_id": form_id,
                "mapping_note": layout.relative_to(ROOT).as_posix(),
                "candidate_units": sorted(candidates),
                "variant_count": len(variants),
                "customer_variants": sorted(
                    variants.values(),
                    key=lambda r: (r["build_id"], r["account_family"], r["source_pas_path"] or ""),
                )[:100],
            }
        )
    return {
        "source": [
            "analysis/layout_mappings/*.md",
            "analysis/welove_dpr_closures.json",
        ],
        "secrets_policy": "Screen coverage stores source topology and content hashes only.",
        "totals": {
            "mapping_note_count": len(entries),
            "covered_mapping_note_count": sum(1 for e in entries if e["variant_count"] > 0),
            "uncovered_mapping_note_count": sum(1 for e in entries if e["variant_count"] == 0),
        },
        "forms": entries,
    }


def write_doc(tenant_matrix: dict[str, Any], screen_coverage: dict[str, Any]) -> None:
    tt = tenant_matrix["totals"]
    st = screen_coverage["totals"]
    cov = st["covered_mapping_note_count"]
    total_maps = st["mapping_note_count"]
    unc = st["uncovered_mapping_note_count"]
    lines = [
        "# WeLove DPR Closure Coverage",
        "",
        "이 문서는 `WeLove_FTP` 고객별 Delphi 실행 파일을 포팅 계약에 연결하기 위한 **생성 산출물 요약·운영 원칙**입니다. 원본 자격증명 파일은 읽지 않고, 경로·해시·라우팅 키만 저장합니다.",
        "",
        "## 조사 결과 요약",
        "",
        "| 항목 | 값 |",
        "|------|-----|",
        f"| 활성 테넌트 | {tt['tenant_count']} |",
        f"| `active_build_id` 누락 | {tt['active_build_id_missing']} (게이트가 차단) |",
        f"| DPR 클로저 수 | {tt['extended_dpr_count']} |",
        f"| `layout_mappings` 대비 소스 커버 | {cov} / {total_maps} 매핑 노트 (`welove_screen_contract_coverage.json`) |",
        "| 비표준 매핑 노트 클로저 연결 | `Id_Logn` → `Chul.pas`, `c8_scan_match` → `Tong08`/`Tong07` (`tools/build_welove_porting_coverage.py`의 `LAYOUT_NOTE_EXTRA_UNIT_ALIASES`) |",
        "",
        "**테넌트 라우팅 키 순서:** `tenant_id` → `account_family` → `active_build_id` → `dpr_closure` (상세는 `welove_build_coverage.yaml`의 `tenant_routing_contract`).",
        "",
        "## Generated Artifacts",
        "",
        "- `analysis/welove_dpr_closures.json`: 468개 `.dpr`의 `uses` 클로저, PAS/DFM 경로, 해시.",
        "- `analysis/welove_build_catalog_extended.json`: 기존 빌드 카탈로그 + 미매핑 실행 파일 유형 + 동치 클로저 그룹.",
        "- `analysis/welove_tenant_build_routing_matrix.json`: `tenant_id -> account_family -> active_build_id -> dpr_closure` 추적.",
        "- `analysis/welove_screen_contract_coverage.json`: `layout_mappings/*.md` 화면별 `build_id` 소스 PAS/DFM 변형.",
        "- `migration/contracts/welove_build_coverage.yaml`: 위 산출물을 포팅 계약의 공통 참조로 고정 (`login_safety_contract` 포함).",
        "",
        "생성 스크립트: `tools/extract_welove_dpr_closures.py`, `tools/build_welove_porting_coverage.py`.",
        "",
        "## 포팅 적용 순서 (권장)",
        "",
        "1. **인벤토리 동기**: 로컬 `WeLove_FTP` 존재 시 스크립트로 JSON 재생성 → 계약 `artifacts` 경로와 불일치 없게 유지.",
        "2. **테넌트·빌드 정합**: `tenants_directory` 시드/런타임과 `welove_tenant_build_routing_matrix.json` 비교; 불일치는 DEC 또는 `customer_variants`에만 기록.",
        "3. **화면 계약**: 신규·수정 화면은 dfm→html 산출물( `.cursor/rules/dfm-layout-input.mdc`)을 공식 입력으로 두고, WeLove 소스 경로는 `welove_screen_contract_coverage.json`과 매핑 노트를 맞춘다.",
        "4. **메뉴·권한**: `rbac_menu_matrix.yaml`, `build_forced_hidden_menus.yaml`, 프런트 `account-menu-matrix.ts`가 `active_build_id`·claim과 일치하는지 확인.",
        "5. **회귀 게이트**: 아래 테스트·probe 실행 또는 CI 동등.",
        "",
        "## 로그인 보존 가드 (변경 금지 원칙)",
        "",
        "WeLove 메타 확장은 **부가 정보 보존**만 허용한다. 다음은 **변경하지 않는다**.",
        "",
        "- DSN-DEC-08 통합 로그인 흐름: `auth.login`, `tenants_directory`, `Id_Logn` 비밀번호 검증, `login_id_index` 해석.",
        "- 활성 테넌트 선택 후 DB 연결 및 JWT 발급 순서.",
        "",
        "**허용되는 추가 메타:** `active_build_id`, `account_family`, `build_role`, `warehouse_menu_tier`, 메뉴/권한 claim 등 계약에 명시된 필드의 유지·전달.",
        "",
        "**체크리스트 (코드 터치 전 필수):**",
        "",
        "- `docs/login-routing-regression-guard.md`",
        "- `migration/contracts/login.yaml`",
        "- `migration/contracts/tenants_directory.yaml`",
        "- `migration/contracts/welove_build_coverage.yaml` → `login_safety_contract`",
        "",
        "## 신규 시나리오·화면 입력 규칙",
        "",
        "- 레거시 소스 트리만으로 필드가 불명확하면 **`WeLove_FTP` 해당 `build_id` 경로**를 정본으로 삼는다.",
        "- 고객 간 차이는 **서비스/프론트 if/else 분기 금지** — `customer_variants`와 계약 데이터만 사용 (`welove_build_coverage.yaml` `schema_extensions.branch_rule`).",
        "- dfm 변형 폴더(`Subu22`, `Subu22_1` 등) 차이는 **코드 분기 금지**, 계약에 diff 기록 (DEC-028).",
        "",
        "## Current Totals",
        "",
        f"- Tenants: {tt['tenant_count']}",
        f"- Missing active_build_id: {tt['active_build_id_missing']}",
        f"- DPR closures: {tt['extended_dpr_count']}",
        f"- Mapping notes covered by WeLove source: {cov} / {total_maps}",
        f"- Uncovered mapping notes: {unc}",
        "",
        "## Regression Gate",
        "",
        "다음이 실패하면 병합·릴리스 전에 원인을 제거한다.",
        "",
        "### 필수 (계약 `welove_build_coverage.yaml`·`login_safety_contract`)",
        "",
        "- `test/test_welove_porting_coverage.py` — 활성 테넌트 `active_build_id`, 비밀 키 미유출, 소스 추적성, RBAC `source_builds` 정합 등.",
        "- `test/test_auth_login_dynamic_routing.py`",
        "- `test/test_auth_login_500_safety_net.py`",
        "- `test/test_auth_login_fixed_server.py`",
        "",
        "### 보조·운영",
        "",
        "- `debug/probe_backend_all_servers.py` (4대 서버 매트릭스, 멀티 DB 정책 DEC-033)",
        "",
        "`test/test_welove_porting_coverage.py`가 특히 다음을 차단합니다.",
        "",
        "- 모든 활성 테넌트는 `active_build_id`를 가져야 합니다.",
        "- 생성 산출물에는 DB 사용자/비밀번호 키가 없어야 합니다.",
        "- `Sobo14` 같은 완료 화면은 `customer_variants[].source_pas_path/source_dfm_path`로 추적 가능해야 합니다.",
        "- `rbac_menu_matrix.yaml`의 `source_builds`와 빌드 카탈로그 alias가 어긋나면 실패합니다.",
        "",
    ]
    DOC_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    tenant_matrix = build_tenant_matrix()
    screen_coverage = build_screen_coverage()
    OUT_TENANT.write_text(json.dumps(tenant_matrix, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_SCREEN.write_text(json.dumps(screen_coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    write_doc(tenant_matrix, screen_coverage)
    print(f"wrote {OUT_TENANT.relative_to(ROOT)}")
    print(f"wrote {OUT_SCREEN.relative_to(ROOT)}")
    print(f"wrote {DOC_OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
