#!/usr/bin/env python3
"""Extract DB-route metadata from `DB정보 엑셀정리.xlsx`.

Strict policy (G3 — secrets-policy):
  * **Never** copy DB users / passwords / root credentials into the repo.
  * Only logical metadata is exported: server IP/label, tenant (publisher /
    distributor) name, database name, account-prefix family.
  * The presence of credentials in the source file is recorded as a flag
    (``has_credentials_in_source: true``) so reviewers know to handle the
    source via vault / out-of-repo storage.

Output:
  analysis/welove_db_route_matrix.json - routing meta only (no secrets)
"""

from __future__ import annotations

import json
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "WeLove_FTP/Welove_인수인계/셋팅방법/DB정보, DB_FTP 엑셀/DB정보 엑셀정리.xlsx"
JSON_OUT = ROOT / "analysis/welove_db_route_matrix.json"


HEADER_TOKENS = ("서버", "물류사명", "디비사용자", "디비패스워드", "디비명")


def _norm(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _account_family(user_id: str) -> str:
    """Return the family prefix (book_01, chul_05, sky_01, etc.) without secret."""
    if not user_id:
        return ""
    if user_id.endswith("_user"):
        return user_id[:-5]
    return user_id.split("_user", 1)[0]


def _server_id(server_label: str) -> str:
    """Map '115.68.3.155(서버2)' to a stable logical id."""
    label = server_label or ""
    # The MD5 of the IP would leak. Use the human label suffix or last octet.
    if "(" in label:
        return label.split("(", 1)[1].rstrip(")")
    return label


def main() -> int:
    if not XLSX.exists():
        print(f"ERROR: source not found: {XLSX}")
        return 1

    wb = openpyxl.load_workbook(str(XLSX), data_only=True)
    sh = wb["Sheet1"]
    routes: list[dict] = []

    server_meta: dict[str, dict] = {}

    for row in sh.iter_rows(values_only=True):
        cells = [_norm(v) for v in row]
        if not any(cells):
            continue
        # Detect header row (server·tenant·user·pass·db labels).
        if "서버" in cells and "물류사명(업체명)" in cells:
            continue
        # Each data row layout: [_, _, server, tenant, user, pass, db, note]
        if len(cells) < 7:
            continue
        server_label, tenant, user_id, password, db_name = cells[2], cells[3], cells[4], cells[5], cells[6]
        note = cells[7] if len(cells) >= 8 else ""
        if not server_label or not tenant:
            continue
        sid = _server_id(server_label)
        family = _account_family(user_id)
        routes.append(
            {
                "server_label_raw": server_label,
                "server_id": sid,
                "tenant_name_kor": tenant,
                "db_name_logical": db_name.strip() if db_name else "",
                "account_family": family,
                "note": note,
                "has_credentials_in_source": bool(user_id and password),
            }
        )
        server_meta.setdefault(
            sid,
            {
                "server_id": sid,
                "raw_label": server_label,
                "tenant_count": 0,
            },
        )
        server_meta[sid]["tenant_count"] += 1

    # Compute stable mapping: server -> family -> {tenant, db_name}
    by_family: dict[str, dict[str, list[dict]]] = {}
    for r in routes:
        by_family.setdefault(r["server_id"], {}).setdefault(r["account_family"], []).append(
            {
                "tenant_name_kor": r["tenant_name_kor"],
                "db_name_logical": r["db_name_logical"],
                "note": r["note"],
            }
        )

    payload = {
        "source": "WeLove_FTP/Welove_인수인계/셋팅방법/DB정보, DB_FTP 엑셀/DB정보 엑셀정리.xlsx",
        "manual_id": "MAN-017",
        "secrets_policy": (
            "Per docs/secrets-policy.md: 사용자/비밀번호/root 토큰은 본 JSON 에 포함하지 않는다."
            " has_credentials_in_source 가 true 면 원본 엑셀에 자격증명이 평문으로 존재함을 의미하며,"
            " 운영 vault 또는 환경변수로 이전 후 원본은 작업자 PC 한정 보존한다."
        ),
        "schema": {
            "server_id": "logical id derived from sheet column '서버' (예: 서버1·서버2·서버3·서버4)",
            "account_family": "user-id prefix without _user suffix (예: chul_05, book_07, sky_01) — credential-free",
            "db_name_logical": "database name as written; secrets stripped",
            "tenant_name_kor": "korean tenant label (publisher/distributor) — used for UX and onboarding",
        },
        "servers": list(server_meta.values()),
        "routes": routes,
        "by_family": by_family,
        "totals": {
            "servers": len(server_meta),
            "routes": len(routes),
            "credential_rows_in_source": sum(1 for r in routes if r["has_credentials_in_source"]),
        },
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    with JSON_OUT.open("w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)
    print(
        f"wrote {JSON_OUT.relative_to(ROOT)} ({payload['totals']['routes']} routes,"
        f" {payload['totals']['servers']} servers, no secrets)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
