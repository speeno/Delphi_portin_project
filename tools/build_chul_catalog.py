#!/usr/bin/env python3
"""Build the Chul-client build catalog (analysis/welove_chul_builds.json).

Scans the seven known WeLove Chul deployment instances under
`WeLove_FTP/...` and emits a normalized metadata catalog used by:
  * tools/extract_chul_menus.py  — input list
  * docs/welove-chul-build-menu-matrix.md — reference table
  * docs/onboarding-rbac-menu-matrix.md — `source_builds` column

Strict policy (G3 — secrets-policy.md):
  * Reads Config.Ini but never copies UserName/Password into output.
  * Only Uses=, App.Caption, file sizes, MD5, dll list, sub-dir list are kept.

Output: analysis/welove_chul_builds.json
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_OUT = ROOT / "analysis/welove_chul_builds.json"

BUILDS = [
    {
        "build_id": "BLD-DIST-STD",
        "path": "WeLove_FTP/도서유통-총판",
        "build_role": "distributor",
        "account_family_inferred": None,
        "account_type_inferred": ["ACC-T2-DIST"],
        "notes": "표준 총판 배포 템플릿. Config.Ini Uses=Client02 (샘플 placeholder).",
    },
    {
        "build_id": "BLD-PUB-STD",
        "path": "WeLove_FTP/도서유통-출판",
        "build_role": "publisher",
        "account_family_inferred": None,
        "account_type_inferred": ["ACC-T2-PUB"],
        "notes": "표준 출판 배포 템플릿. Config.Ini Uses=홍길동 (샘플 placeholder). 메뉴보이기/감추기 토글 보유.",
    },
    {
        "build_id": "BLD-DIST-KBT",
        "path": "WeLove_FTP/도서유통-New/도서유통/한국도서유통/유통",
        "build_role": "distributor",
        "account_family_inferred": "book_kb",
        "account_type_inferred": ["ACC-T2-DIST"],
        "notes": "한국도서유통 테넌트의 총판 빌드. 표준 총판보다 메뉴/폼 다수 추가 (Subu13_1, Subu59_3 등).",
    },
    {
        "build_id": "BLD-PUB-KBT",
        "path": "WeLove_FTP/도서유통-New/도서유통/한국도서유통/출판",
        "build_role": "publisher",
        "account_family_inferred": None,
        "account_type_inferred": ["ACC-T2-PUB"],
        "notes": "한국도서유통 패키지에 동봉된 표준 출판 빌드. Chul.dfm/pas MD5 가 BLD-PUB-STD 와 동일 (binary-identical) — 별도 변형 아님.",
    },
    {
        "build_id": "BLD-PUB-WAREHOUSE-WELOVE",
        "path": "WeLove_FTP/도서유통-New/도서유통/chul_09(위러브)",
        "build_role": "warehouse_publisher",
        "account_family_inferred": "chul_09",
        "account_type_inferred": ["ACC-T3", "ACC-T3-WAREHOUSE-LITE"],
        "notes": "자체 물류 보유 출판사 (lite 변형). 상단 메뉴 7 항목 (반품재고관리 통합). 출판사관리 보유. chul_09 SKU 는 위러브1/2/3 + 교문사 4개 테넌트 공유.",
    },
    {
        "build_id": "BLD-PUB-WAREHOUSE-MS",
        "path": "WeLove_FTP/도서유통-New/도서유통/book_21(MS북스)",
        "build_role": "warehouse_publisher",
        "account_family_inferred": "book_21",
        "account_type_inferred": ["ACC-T3-WAREHOUSE-FULL"],
        "notes": "자체 물류 + 출판사관리 보유 + TSCLIB.dll(라벨 SDK). 상단 메뉴 8 항목 (재고관리/반품관리 분리). App Caption '도서관리프로그램'. ACC-T3-WAREHOUSE-FULL 후보.",
    },
    {
        "build_id": "BLD-PUB-WAREHOUSE-BOOKNBOOK-NEW",
        "path": "WeLove_FTP/도서유통-New/도서유통/book_07(북앤북NEW)",
        "build_role": "warehouse_publisher",
        "account_family_inferred": "book_07",
        "account_type_inferred": ["ACC-T3-WAREHOUSE-FULL"],
        "notes": "자체 물류 + 출판사관리 보유 + 신규 폼군 (Seak/Seek/Seok/Seep/Base) + 다중 DB 백엔드 디렉토리 (Interbase/Mysql/Remote). 상단 메뉴 8 항목 (MS북스와 동일 패턴). book_07 SKU 는 북앤북·유앤북 2 테넌트 공유. Config.Ini Uses=한국도서유통 — 동일 테넌트 다중 빌드 사례 (OQ-BLD-5).",
    },
]


def _read_text(path: Path) -> str:
    try:
        return path.read_bytes().decode("cp949", errors="replace")
    except FileNotFoundError:
        return ""


def _md5(path: Path) -> str | None:
    try:
        return hashlib.md5(path.read_bytes()).hexdigest()
    except FileNotFoundError:
        return None


def _config_uses(cfg_text: str) -> str:
    for line in cfg_text.splitlines():
        if line.startswith("Uses="):
            return line[len("Uses=") :].strip()
    return ""


def _has_credentials(cfg_text: str) -> bool:
    return bool(re.search(r"^(UserName|Password)=.+", cfg_text, re.MULTILINE))


def _app_caption(dfm_text: str) -> str:
    for line in dfm_text.splitlines():
        if line.startswith("  Caption"):
            m = re.match(r"^  Caption\s*=\s*'(.*)'", line)
            if m:
                return m.group(1)
            return line.split("=", 1)[1].strip().strip("'")
    return ""


def _list_dlls(dir_path: Path) -> list[str]:
    return sorted(p.name for p in dir_path.iterdir() if p.suffix.lower() == ".dll")


def _list_subdirs(dir_path: Path) -> list[str]:
    return sorted(p.name for p in dir_path.iterdir() if p.is_dir())


def _form_families(dir_path: Path) -> dict[str, int]:
    """Count *.pas form files by alphabetic prefix family (Subu, Tong, Seak, ...)."""
    families: dict[str, int] = {}
    pattern = re.compile(r"^([A-Za-z]+)\d+(_\d+)?\.pas$")
    for p in dir_path.iterdir():
        m = pattern.match(p.name)
        if m:
            fam = m.group(1)
            families[fam] = families.get(fam, 0) + 1
    return dict(sorted(families.items()))


def _has_publisher_management(dfm_text: str) -> bool:
    """True iff '출판사관리' appears as a TMenuItem Caption (not arbitrary string)."""
    return bool(re.search(r"Caption\s*=\s*'출판사관리'", dfm_text))


# Top-bar TMenuItem captions only (object Menu100/200/.../800 — second-level == top-bar).
# We approximate by counting unique top-bar Caption lines; the canonical extractor
# will produce structured output in tools/extract_chul_menus.py.
_TOPBAR_RE = re.compile(
    r"^\s{4}object Menu\d{3}: TMenuItem\s*$\n^\s{6}Caption = '([^']+)'", re.MULTILINE
)


def _top_menu_captions(dfm_text: str) -> list[str]:
    return _TOPBAR_RE.findall(dfm_text)


def _has_menu_toggle(dfm_text: str) -> bool:
    return ("메뉴보이기" in dfm_text) or ("메뉴감추기" in dfm_text)


def build_record(meta: dict) -> dict:
    bdir = ROOT / meta["path"]
    cfg_text = _read_text(bdir / "Config.Ini")
    dfm_path = bdir / "Chul.dfm"
    pas_path = bdir / "Chul.pas"
    dfm_text = _read_text(dfm_path)
    return {
        "build_id": meta["build_id"],
        "path": meta["path"],
        "build_role": meta["build_role"],
        "account_family_inferred": meta["account_family_inferred"],
        "account_type_inferred": meta["account_type_inferred"],
        "config_uses_label": _config_uses(cfg_text),
        "config_has_credentials_in_source": _has_credentials(cfg_text),
        "app_caption": _app_caption(dfm_text),
        "dfm_size": dfm_path.stat().st_size if dfm_path.exists() else None,
        "pas_size": pas_path.stat().st_size if pas_path.exists() else None,
        "dfm_md5": _md5(dfm_path),
        "pas_md5": _md5(pas_path),
        "extra_libraries": _list_dlls(bdir),
        "db_backend_dirs": [
            d for d in _list_subdirs(bdir) if d.lower() in {"interbase", "mysql", "mssql", "remote"}
        ],
        "all_subdirs": _list_subdirs(bdir),
        "form_families": _form_families(bdir),
        "top_menu_captions": _top_menu_captions(dfm_text),
        "top_menu_count": len(_top_menu_captions(dfm_text)),
        "has_publisher_management": _has_publisher_management(dfm_text),
        "has_menu_visibility_toggle": _has_menu_toggle(dfm_text),
        "notes": meta["notes"],
    }


def find_duplicates(records: list[dict]) -> list[dict]:
    """Detect builds whose Chul.dfm + Chul.pas are byte-identical."""
    by_pair: dict[tuple, list[str]] = {}
    for r in records:
        key = (r.get("dfm_md5"), r.get("pas_md5"))
        if all(key):
            by_pair.setdefault(key, []).append(r["build_id"])
    return [
        {"dfm_md5": dfm, "pas_md5": pas, "build_ids": ids}
        for (dfm, pas), ids in by_pair.items()
        if len(ids) > 1
    ]


def build_tenant_groups(records: list[dict]) -> list[dict]:
    """Group builds that share the same Config.Ini Uses= label."""
    by_label: dict[str, list[str]] = {}
    for r in records:
        lbl = r.get("config_uses_label") or ""
        by_label.setdefault(lbl, []).append(r["build_id"])
    return [
        {"uses_label": lbl, "build_ids": ids}
        for lbl, ids in sorted(by_label.items())
        if len(ids) > 1
    ]


def main() -> None:
    records = [build_record(b) for b in BUILDS]
    payload = {
        "source": "WeLove_FTP/도서유통-* (직접 디스크 스캔)",
        "secrets_policy": "Per docs/secrets-policy.md (G3): Config.Ini 의 UserName/Password 는 어떠한 형태로도 본 JSON 에 포함하지 않는다. config_has_credentials_in_source 가 true 면 원본 Config.Ini 에 평문 자격증명이 존재함을 의미.",
        "schema": {
            "build_id": "BLD-* 추적 ID — RBAC 매트릭스의 source_builds 컬럼 키",
            "build_role": "distributor | publisher | warehouse_publisher",
            "account_family_inferred": "DB 사용자 계정 prefix 군 (chul_09, book_07 등) — 빌드 SKU 식별자",
            "config_uses_label": "Config.Ini Uses= 값 (테넌트 라벨, GREEN 등급)",
            "dfm_md5/pas_md5": "Chul.dfm/Chul.pas 의 MD5 — 바이너리 동일 빌드 검출용",
            "form_families": "*.pas 폼 파일 prefix 별 갯수 (Subu, Tong, Seak, Seek, Seok, Seep, Base 등)",
        },
        "builds": records,
        "binary_identical_groups": find_duplicates(records),
        "tenant_label_groups": build_tenant_groups(records),
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    with JSON_OUT.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"wrote {JSON_OUT.relative_to(ROOT)} ({len(records)} builds)")
    if payload["binary_identical_groups"]:
        print("binary-identical groups:")
        for g in payload["binary_identical_groups"]:
            print("  ", g["build_ids"])
    if payload["tenant_label_groups"]:
        print("tenant-label-shared groups:")
        for g in payload["tenant_label_groups"]:
            print("  ", g["uses_label"], "→", g["build_ids"])


if __name__ == "__main__":
    main()
