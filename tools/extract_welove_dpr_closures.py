#!/usr/bin/env python3
"""Extract credential-free DPR closure metadata from WeLove_FTP.

The WeLove FTP handover tree is intentionally gitignored and can contain
customer-specific copies of Delphi projects.  This tool records only source
topology (DPR/PAS/DFM paths and hashes) so porting contracts can reason about
build variants without copying DB credentials or Config.Ini values.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WELOVE_ROOT = ROOT / "WeLove_FTP"
ANALYSIS_DIR = ROOT / "analysis"
CLOSURES_OUT = ANALYSIS_DIR / "welove_dpr_closures.json"
BUILD_OUT = ANALYSIS_DIR / "welove_build_catalog_extended.json"
EXISTING_BUILDS = ANALYSIS_DIR / "welove_chul_builds.json"

SECRET_NAME_RE = re.compile(
    r"(password|passwd|gpass|username|user_name|db정보|암호|패스워드|비밀번호|credentials)",
    re.IGNORECASE,
)
ACCOUNT_FAMILY_RE = re.compile(r"\b(?:book|chul|sky|seak|well|welove)_[A-Za-z0-9]+(?:_[A-Za-z0-9]+)?\b", re.IGNORECASE)
USES_RE = re.compile(
    r"(?P<unit>[A-Za-z_][A-Za-z0-9_]*)\s+in\s+'(?P<path>[^']+)'(?:\s*\{(?P<form>[^}]+)\})?",
    re.IGNORECASE,
)
PROGRAM_RE = re.compile(r"\bprogram\s+([A-Za-z_][A-Za-z0-9_]*)\s*;", re.IGNORECASE)


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _rel_welove(path: Path) -> str:
    return path.relative_to(WELOVE_ROOT).as_posix()


def _read_text(path: Path) -> str:
    data = path.read_bytes()
    for enc in ("cp949", "utf-8", "euc-kr"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("cp949", errors="replace")


def _sha1(path: Path | None) -> str:
    if path is None or not path.exists() or not path.is_file():
        return ""
    h = hashlib.sha1()
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _md5(path: Path | None) -> str:
    if path is None or not path.exists() or not path.is_file():
        return ""
    h = hashlib.md5()  # noqa: S324 - content identity only, not security.
    with path.open("rb") as fp:
        for chunk in iter(lambda: fp.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _safe_resolve_dpr_path(dpr: Path, raw: str) -> Path:
    normalized = raw.replace("\\", "/")
    return (dpr.parent / normalized).resolve()


def _is_secret_adjacent(path: Path) -> bool:
    return any(SECRET_NAME_RE.search(part) for part in path.parts)


def _account_family_from_path(path: Path) -> str:
    parts = list(path.relative_to(WELOVE_ROOT).parts)
    for part in parts:
        match = ACCOUNT_FAMILY_RE.search(part)
        if match:
            return match.group(0).lower()
    return ""


def _execution_type(dpr: Path, program_name: str) -> str:
    name = dpr.name.lower()
    parent = "/".join(dpr.relative_to(WELOVE_ROOT).parts).lower()
    if name.startswith("mainupdate"):
        return "autoupdate"
    if program_name.lower().startswith("mainupdate"):
        return "autoupdate"
    if name == "project1.dpr":
        return "data-transfer-or-utility"
    if program_name.lower().startswith("chul001") or name == "chul001.dpr":
        return "alternate-chulpan"
    if "autoupdate" in parent or "updatex" in parent or "updatey" in parent:
        return "autoupdate"
    if "자료전송" in parent:
        return "data-transfer-or-utility"
    if name == "chulpan.dpr":
        return "main-chulpan"
    return "other"


def _load_existing_builds() -> list[dict[str, Any]]:
    if not EXISTING_BUILDS.exists():
        return []
    data = json.loads(EXISTING_BUILDS.read_text(encoding="utf-8"))
    return list(data.get("builds", []))


def _index_existing_builds() -> list[dict[str, str]]:
    indexed = []
    for row in _load_existing_builds():
        raw_path = str(row.get("path") or "")
        if not raw_path:
            continue
        indexed.append(
            {
                "build_id": str(row.get("build_id") or ""),
                "path": raw_path.rstrip("/"),
                "build_role": str(row.get("build_role") or ""),
                "account_family": str(row.get("account_family_inferred") or ""),
            }
        )
    return indexed


def _match_existing_build(rel_dpr: str, indexed: list[dict[str, str]]) -> dict[str, str]:
    best: dict[str, str] = {}
    best_len = -1
    for row in indexed:
        prefix = row["path"].replace("\\", "/").rstrip("/")
        if rel_dpr == prefix or rel_dpr.startswith(prefix + "/"):
            if len(prefix) > best_len:
                best = row
                best_len = len(prefix)
    return best


def parse_dpr(dpr: Path, indexed_builds: list[dict[str, str]]) -> dict[str, Any]:
    text = _read_text(dpr)
    program_match = PROGRAM_RE.search(text)
    program_name = program_match.group(1) if program_match else dpr.stem
    rel_dpr = _rel(dpr)
    rel_dpr_w = _rel_welove(dpr)
    build_match = _match_existing_build(rel_dpr, indexed_builds)

    units: list[dict[str, Any]] = []
    pas_hashes: list[str] = []
    dfm_hashes: list[str] = []
    missing_units: list[str] = []
    secret_adjacent = _is_secret_adjacent(dpr)

    for match in USES_RE.finditer(text):
        unit = match.group("unit")
        raw_path = match.group("path")
        form = (match.group("form") or "").strip()
        pas_path = _safe_resolve_dpr_path(dpr, raw_path)
        pas_exists = pas_path.exists() and pas_path.is_file()
        dfm_path = pas_path.with_suffix(".dfm") if pas_exists else None
        dfm_exists = bool(dfm_path and dfm_path.exists() and dfm_path.is_file())
        pas_sha1 = _sha1(pas_path if pas_exists else None)
        dfm_md5 = _md5(dfm_path if dfm_exists else None)
        if pas_sha1:
            pas_hashes.append(pas_sha1)
        if dfm_md5:
            dfm_hashes.append(dfm_md5)
        if not pas_exists:
            missing_units.append(unit)
        secret_adjacent = secret_adjacent or _is_secret_adjacent(pas_path)
        units.append(
            {
                "unit": unit,
                "declared_path": raw_path,
                "form": form,
                "resolved_pas_path": _rel(pas_path) if pas_exists else "",
                "resolved_dfm_path": _rel(dfm_path) if dfm_exists and dfm_path else "",
                "pas_sha1": pas_sha1,
                "dfm_md5": dfm_md5,
                "pas_exists": pas_exists,
                "dfm_exists": dfm_exists,
            }
        )

    closure_hash_input = "\n".join(
        sorted([u["unit"] + ":" + (u["pas_sha1"] or u["declared_path"]) for u in units])
    ).encode("utf-8")
    closure_hash = hashlib.sha1(closure_hash_input).hexdigest()
    account_family = _account_family_from_path(dpr) or build_match.get("account_family", "")

    return {
        "dpr_path": rel_dpr,
        "dpr_path_in_welove": rel_dpr_w,
        "program_name": program_name,
        "execution_type": _execution_type(dpr, program_name),
        "account_family": account_family,
        "existing_build_id": build_match.get("build_id", ""),
        "build_role": build_match.get("build_role", ""),
        "dpr_sha1": _sha1(dpr),
        "dpr_closure_hash": closure_hash,
        "unit_count": len(units),
        "missing_unit_count": len(missing_units),
        "missing_units": missing_units[:50],
        "pas_hash_count": len(set(pas_hashes)),
        "dfm_hash_count": len(set(dfm_hashes)),
        "has_secret_adjacent_path": secret_adjacent,
        "units": units,
    }


def build_extended_catalog(closures: list[dict[str, Any]]) -> dict[str, Any]:
    by_hash: dict[str, list[dict[str, str]]] = defaultdict(list)
    by_build: dict[str, dict[str, Any]] = {}
    by_account: dict[str, dict[str, Any]] = {}
    execution_counts = Counter(c["execution_type"] for c in closures)
    build_counts = Counter(c["existing_build_id"] or "UNMAPPED" for c in closures)

    for c in closures:
        by_hash[c["dpr_closure_hash"]].append(
            {
                "dpr_path": c["dpr_path"],
                "program_name": c["program_name"],
                "execution_type": c["execution_type"],
                "account_family": c["account_family"],
                "existing_build_id": c["existing_build_id"],
            }
        )
        build_id = c["existing_build_id"] or "UNMAPPED"
        build = by_build.setdefault(
            build_id,
            {
                "build_id": build_id,
                "dpr_count": 0,
                "execution_types": Counter(),
                "account_families": set(),
                "closure_hashes": set(),
                "sample_dpr_paths": [],
            },
        )
        build["dpr_count"] += 1
        build["execution_types"][c["execution_type"]] += 1
        if c["account_family"]:
            build["account_families"].add(c["account_family"])
        build["closure_hashes"].add(c["dpr_closure_hash"])
        if len(build["sample_dpr_paths"]) < 10:
            build["sample_dpr_paths"].append(c["dpr_path"])

        account = c["account_family"] or "unknown"
        acc = by_account.setdefault(
            account,
            {
                "account_family": account,
                "dpr_count": 0,
                "build_ids": set(),
                "execution_types": Counter(),
                "sample_dpr_paths": [],
            },
        )
        acc["dpr_count"] += 1
        acc["build_ids"].add(build_id)
        acc["execution_types"][c["execution_type"]] += 1
        if len(acc["sample_dpr_paths"]) < 10:
            acc["sample_dpr_paths"].append(c["dpr_path"])

    def _freeze_build(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "build_id": row["build_id"],
            "dpr_count": row["dpr_count"],
            "execution_types": dict(row["execution_types"]),
            "account_families": sorted(row["account_families"]),
            "closure_hash_count": len(row["closure_hashes"]),
            "sample_dpr_paths": row["sample_dpr_paths"],
        }

    def _freeze_account(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "account_family": row["account_family"],
            "dpr_count": row["dpr_count"],
            "build_ids": sorted(row["build_ids"]),
            "execution_types": dict(row["execution_types"]),
            "sample_dpr_paths": row["sample_dpr_paths"],
        }

    identical_groups = [
        {
            "dpr_closure_hash": h,
            "count": len(items),
            "items": items[:25],
        }
        for h, items in sorted(by_hash.items(), key=lambda kv: len(kv[1]), reverse=True)
        if len(items) > 1
    ]

    return {
        "source": "analysis/welove_dpr_closures.json",
        "secrets_policy": (
            "Credential-bearing files are not read. This catalog stores source paths, hashes, "
            "program names, build/account identifiers, and boolean secret-adjacent flags only."
        ),
        "totals": {
            "dpr_count": len(closures),
            "closure_hash_count": len(by_hash),
            "identical_closure_group_count": len(identical_groups),
            "execution_type_counts": dict(execution_counts),
            "existing_build_match_counts": dict(build_counts),
        },
        "builds": [_freeze_build(row) for row in sorted(by_build.values(), key=lambda r: r["build_id"])],
        "account_families": [
            _freeze_account(row)
            for row in sorted(by_account.values(), key=lambda r: (-r["dpr_count"], r["account_family"]))
        ],
        "identical_closure_groups": identical_groups[:100],
    }


def main() -> int:
    if not WELOVE_ROOT.exists():
        print(f"ERROR: WeLove_FTP not found: {WELOVE_ROOT}")
        return 1
    indexed_builds = _index_existing_builds()
    dprs = sorted(WELOVE_ROOT.rglob("*.dpr"), key=lambda p: _rel_welove(p))
    closures = [parse_dpr(dpr, indexed_builds) for dpr in dprs if not _is_secret_adjacent(dpr)]
    payload = {
        "source": "WeLove_FTP/**/*.dpr",
        "manual_id": "MAN-WELOVE-DPR-CLOSURE",
        "secrets_policy": (
            "Per docs/secrets-policy.md G3, this file contains no DB usernames, passwords, "
            "root credentials, Config.Ini values, or spreadsheet contents."
        ),
        "schema": {
            "dpr_closure_hash": "SHA1 over sorted unit name + PAS SHA1 references",
            "existing_build_id": "Matched against analysis/welove_chul_builds.json by path prefix, if any",
            "account_family": "Derived from non-secret folder names such as chul_09 or book_21",
        },
        "totals": {
            "dpr_count": len(closures),
            "main_chulpan_count": sum(1 for c in closures if c["execution_type"] == "main-chulpan"),
            "secret_adjacent_path_count": sum(1 for c in closures if c["has_secret_adjacent_path"]),
            "missing_unit_dpr_count": sum(1 for c in closures if c["missing_unit_count"] > 0),
        },
        "closures": closures,
    }
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    CLOSURES_OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    BUILD_OUT.write_text(
        json.dumps(build_extended_catalog(closures), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"wrote {_rel(CLOSURES_OUT)} ({len(closures)} dpr closures)")
    print(f"wrote {_rel(BUILD_OUT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
