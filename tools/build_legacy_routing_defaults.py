#!/usr/bin/env python3
"""레거시 Delphi Chul.pas 라우팅 → 정본화 JSON 산출 (DSN-DEC-11).

목적
----
- ``extract_legacy_delphi_db_routing.py`` 가 만든 엑셀과 동일한 원천 스캔을
  재사용해 신규 시스템이 직접 소비 가능한 JSON 으로 한 번 더 가공한다.
- ``servers.yaml`` 의 ``host`` 필드를 기준으로 host_ip → ``remote_*`` server id
  매핑을 수행하고, 추출 row 마다 ``confidence`` 를 산정한다.

confidence 정책
----------------
- ``high``  — 기본값. 모든 필수 필드(host, database, account_family) 채워졌고
              host_ip 가 servers.yaml 에 알려진 IP 이며 folder↔DB 불일치 메모가 없음.
- ``low``   — 다음 중 하나 이상:
                - folder↔DB 불일치 메모(``mismatch_note``) 존재
                - host_ip 가 servers.yaml 에 없는 외부/미상 IP
                - ``Database`` 가 비어 있어 account_family 추론 실패

비밀 정책
---------
- 본 산출물은 host/db/login(naming) 만 보관, 실 비밀번호는 절대 포함하지 않는다.
- 결과 파일은 gitignored 디렉터리(``WeLove_FTP/``) 에 떨어진다.

사용
----
    python3 tools/build_legacy_routing_defaults.py            # dry-run 출력
    python3 tools/build_legacy_routing_defaults.py --apply    # 파일 저장
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
WELOVE = ROOT / "WeLove_FTP"
OUT_JSON = WELOVE / "legacy_delphi_routing_defaults.json"
SERVERS_YAML = ROOT / "도서물류관리프로그램" / "backend" / "servers.yaml"
SERVERS_YAML_EXAMPLE = ROOT / "도서물류관리프로그램" / "backend" / "servers.example.yaml"

sys.path.insert(0, str(ROOT / "tools"))
from extract_legacy_delphi_db_routing import _scan_chul_pas, GLOBS  # noqa: E402


def _load_yaml(path: Path) -> dict[str, Any]:
    """servers.yaml 를 의존성 없이 안전 로드. 기본 위치 → 예시 파일 순서."""
    try:
        import yaml  # type: ignore
    except ImportError:
        sys.stderr.write("[ERR] PyYAML 필요: pip install pyyaml\n")
        sys.exit(2)
    target = path if path.is_file() else SERVERS_YAML_EXAMPLE
    if not target.is_file():
        return {}
    raw = target.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        text = raw.decode("utf-8-sig")
    else:
        for enc in ("utf-8", "cp949", "euc-kr"):
            try:
                text = raw.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        else:
            text = raw.decode("utf-8", errors="replace")
    data = yaml.safe_load(text)
    return data if isinstance(data, dict) else {}


def build_host_ip_to_remote_id(servers_yaml_path: Path = SERVERS_YAML) -> dict[str, str]:
    """servers.yaml 의 ``servers[].host`` → ``servers[].id`` 사전 구성.

    빌드 도구와 백엔드(`tenants_directory_service.host_ip_to_remote_id`) 양쪽에서
    동일 매핑을 사용하기 위한 공용 헬퍼.
    """
    cfg = _load_yaml(servers_yaml_path)
    out: dict[str, str] = {}
    for srv in cfg.get("servers", []) or []:
        if not isinstance(srv, dict):
            continue
        host = (srv.get("host") or "").strip()
        sid = (srv.get("id") or "").strip()
        if host and sid:
            out[host] = sid
    return out


def _classify_row(row: dict[str, Any], host_to_remote: dict[str, str]) -> dict[str, Any]:
    host_ip = (row.get("host") or "").strip()
    db_name = (row.get("database") or "").strip()
    family = (row.get("inferred_family") or "").strip()
    mismatch = (row.get("folder_db_mismatch_note") or "").strip()
    remote_id = host_to_remote.get(host_ip) if host_ip else None
    unknown_host_ip = host_ip if (host_ip and not remote_id) else ""

    reasons: list[str] = []
    if mismatch:
        reasons.append("folder_db_mismatch")
    if unknown_host_ip:
        reasons.append("unknown_host_ip")
    if not db_name or not family:
        reasons.append("empty_database")
    confidence = "low" if reasons else "high"

    return {
        "build_folder": row.get("build_folder") or "",
        "rel_path": row.get("rel_path") or "",
        "host_ip": host_ip,
        "remote_id": remote_id or "",
        "unknown_host_ip": unknown_host_ip,
        "database": db_name,
        "account_family": family,
        "login_naming": row.get("login") or "",
        "password_naming": row.get("password_pattern") or "",
        "mismatch_note": mismatch,
        "confidence": confidence,
        "low_confidence_reasons": reasons,
        "config_ini_client_reads": row.get("config_ini_client_reads") or "",
        "alt_hosts_in_source_comments": row.get("alt_hosts_in_source_comments") or "",
        "connected_true_in_file": row.get("connected_true_in_file") or "",
    }


def collect_rows() -> list[dict[str, Any]]:
    if not WELOVE.is_dir():
        sys.stderr.write(f"[ERR] {WELOVE} 없음\n")
        sys.exit(2)
    paths: list[Path] = []
    for pat in GLOBS:
        paths.extend(sorted(WELOVE.glob(pat)))
    host_to_remote = build_host_ip_to_remote_id()
    out: list[dict[str, Any]] = []
    for p in paths:
        try:
            scanned = _scan_chul_pas(p)
        except Exception as exc:  # noqa: BLE001
            sys.stderr.write(f"[WARN] scan fail {p}: {exc}\n")
            continue
        out.append(_classify_row(scanned, host_to_remote))
    return out


def _summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    high = sum(1 for r in rows if r["confidence"] == "high")
    low = len(rows) - high
    families = sorted({r["account_family"] for r in rows if r["account_family"]})
    unknown_ips = sorted({r["unknown_host_ip"] for r in rows if r["unknown_host_ip"]})
    return {
        "total_builds": len(rows),
        "high_confidence": high,
        "low_confidence": low,
        "distinct_account_families": len(families),
        "unknown_host_ips": unknown_ips,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__ or "")
    parser.add_argument("--apply", action="store_true", help="결과를 JSON 파일로 저장")
    parser.add_argument("--out", type=Path, default=OUT_JSON, help="출력 파일 경로")
    args = parser.parse_args(argv)

    rows = collect_rows()
    summary = _summary(rows)

    payload = {
        "schema_version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "tools/build_legacy_routing_defaults.py (Chul.pas)",
        "secret_policy": "no passwords; naming patterns only (DSN-DEC-11)",
        "summary": summary,
        "rows": rows,
    }

    if args.apply:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"[OK] {len(rows)} rows → {args.out.relative_to(ROOT)}")
        print(f"     summary: {json.dumps(summary, ensure_ascii=False)}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        sys.stderr.write("[DRY] use --apply to save\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
