#!/usr/bin/env python3
"""레거시 ``Config.Ini`` 인벤토리 — Uses/Name/Base 수집 + 시드/매트릭스 라벨 대조 (DSN-DEC-12 보조).

목적
----
``WeLove_FTP/**/Config.Ini`` 의 ``[Client]`` 섹션 (`Uses`, `Name`, `Base`, `PORT`, `PCIP1`)
을 수집해 다음 두 산출물을 만든다.

1. ``analysis/welove_config_ini_inventory.json`` — 빌드 폴더별 1행 표
   (``account_family_inferred``, ``config_kind``, ``customer_folder``, 선택 ``remote_code``).
2. ``analysis/welove_config_ini_label_diff.json`` — 시드/매트릭스의 ``tenant_label_kor`` 와
   ``Config.Ini.[Client].Name`` / ``Uses`` 의 1:1 대조 누락 리포트.

DSN-DEC-12 와의 관계
--------------------
Config.Ini 만으로는 공유 DB 의 ``hcode_in`` 격리 키를 채울 수 없다 — 이 도구는 **보조 정합**
용이며, 라벨/빌드 폴더 매칭 누락만 잡는다 ([`docs/welove-cross-tenant-exposure-runbook.md`](../docs/welove-cross-tenant-exposure-runbook.md)).

비밀 정책 (G3)
---------------
- ``UserName`` / ``Password`` 필드는 base64 추정 placeholder 만 (``MA==``=='0' 등) 이 들어
  있고, 본 도구는 **이 두 필드를 출력하지 않는다.**
- ``Base`` 의 GDB 경로는 레거시 빌드 메타로만 사용 (실파일 위치는 운영자 PC).

사용
----
    python3 tools/inventory_legacy_config_ini.py
    python3 tools/inventory_legacy_config_ini.py --root WeLove_FTP/도서유통-출판
    python3 tools/inventory_legacy_config_ini.py --strict   # tenant_label 미매칭 1건 이상 시 exit 2
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = REPO_ROOT / "WeLove_FTP"
DEFAULT_INVENTORY_OUT = REPO_ROOT / "analysis" / "welove_config_ini_inventory.json"
DEFAULT_DIFF_OUT = REPO_ROOT / "analysis" / "welove_config_ini_label_diff.json"
DEFAULT_SEED_PATH = (
    REPO_ROOT / "도서물류관리프로그램" / "backend" / "data" / "tenants_directory_seed.json"
)
DEFAULT_MATRIX_PATH = REPO_ROOT / "analysis" / "welove_db_route_matrix.json"


_PUBLIC_KEYS = ("Name", "Base", "Uses", "PCIP1", "PORT")
_OMITTED_KEYS = {"username", "password"}  # G3 — 본 도구는 출력하지 않음.


def _decode_bytes(b: bytes) -> str:
    """Config.Ini 는 cp949/utf-8 혼재 — 양쪽 시도."""
    for enc in ("cp949", "utf-8", "euc-kr", "latin-1"):
        try:
            return b.decode(enc)
        except UnicodeDecodeError:
            continue
    return b.decode("utf-8", errors="replace")


_SECTION_RE = re.compile(r"^\s*\[([^\]]+)\]\s*$")
_KV_RE = re.compile(r"^\s*([^=;#\s][^=]*?)\s*=\s*(.*?)\s*$")


def parse_ini(text: str) -> dict[str, dict[str, str]]:
    """단순 INI 파서 (configparser 가 cp949 mojibake 키에서 오류 → 자체 구현)."""
    sections: dict[str, dict[str, str]] = {}
    current: str | None = None
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith((";", "#")):
            continue
        m = _SECTION_RE.match(raw)
        if m:
            current = m.group(1).strip()
            sections.setdefault(current, {})
            continue
        if current is None:
            continue
        kv = _KV_RE.match(raw)
        if kv:
            sections[current][kv.group(1).strip()] = kv.group(2).strip()
    return sections


def _remote_public(remote: dict[str, str]) -> dict[str, str]:
    """``[Remote]`` 공개 필드만 (G3 — 자격 증명 키 제외)."""
    return {
        k: v
        for k, v in remote.items()
        if k.lower() not in _OMITTED_KEYS
    }


def _client_row(path: Path, root: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    text = _decode_bytes(raw)
    parsed = parse_ini(text)
    client = parsed.get("Client", {}) or parsed.get("client", {})
    sanitized = {
        k: v for k, v in client.items()
        if k.lower() not in _OMITTED_KEYS
    }
    remote = parsed.get("Remote", {}) or parsed.get("remote", {})
    remote_pub = _remote_public(remote)
    if path.is_absolute() and root in path.parents:
        rel = path.relative_to(root)
    else:
        rel = path.relative_to(REPO_ROOT)
    config_path = str(rel)
    parent_name = rel.parent.name if rel.parent.parts else ""
    account_family = infer_account_family(config_path)
    row: dict[str, Any] = {
        "config_path": config_path,
        "build_folder": rel.parent.parts[0] if rel.parent.parts else "",
        "build_subpath": str(rel.parent),
        "account_family_inferred": account_family,
        "config_kind": infer_config_kind(config_path, account_family),
        "customer_folder": infer_customer_folder(parent_name),
        "customer_folder_raw": parent_name,
        "name": sanitized.get("Name", ""),
        "uses": sanitized.get("Uses", ""),
        "base": sanitized.get("Base", ""),
        "pcip1": sanitized.get("PCIP1", ""),
        "port": sanitized.get("PORT", "") or sanitized.get("Port", ""),
        "_client_keys": sorted(sanitized.keys()),
    }
    if remote_pub.get("Code"):
        row["remote_code"] = remote_pub["Code"]
    if len(remote_pub) > 1 or (remote_pub and "Code" not in remote_pub):
        row["remote_public"] = remote_pub
    return row


def collect_inventory(root: Path) -> list[dict[str, Any]]:
    if not root.exists():
        return []
    rows: list[dict[str, Any]] = []
    for p in sorted(root.rglob("Config.Ini")):
        try:
            rows.append(_client_row(p, root))
        except Exception as e:  # noqa: BLE001
            print(f"[WARN] {p}: {e}", file=sys.stderr)
    return rows


def _read_json(path: Path) -> Any:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"[WARN] cannot read {path}: {e}", file=sys.stderr)
        return None


def _seed_labels(seed_doc: dict[str, Any] | None) -> set[str]:
    if not isinstance(seed_doc, dict):
        return set()
    return {
        (t.get("tenant_label_kor") or "").strip()
        for t in seed_doc.get("tenants") or []
        if (t.get("tenant_label_kor") or "").strip()
    }


def _matrix_labels(matrix_doc: Any) -> set[str]:
    """welove_db_route_matrix.json — 다양한 형태(list / dict)를 모두 다룬다."""
    found: set[str] = set()

    def _walk(node: Any) -> None:
        if isinstance(node, dict):
            for k in ("tenant_label_kor", "tenant_name_kor", "label_kor", "tenant_label"):
                v = node.get(k)
                if isinstance(v, str) and v.strip():
                    found.add(v.strip())
            for v in node.values():
                _walk(v)
        elif isinstance(node, list):
            for v in node:
                _walk(v)

    _walk(matrix_doc)
    return found


_PUNCT_RE = re.compile(r"[\s\(\)\[\]\.,/\\\-_·＿\(\)（）「」【】《》'\"\?]+")

# 경로·폴더명에서 SKU family 추론 (chul_03(한강도서) → chul_03)
_ACCOUNT_FAMILY_RE = re.compile(
    r"(chul_[A-Za-z0-9_]+|book_[A-Za-z0-9_]+|sky_[A-Za-z0-9_]+)",
    re.IGNORECASE,
)
# chul_03(한강도서) 형태 직상위 폴더 — 괄호 안 한글 라벨
_SKU_FOLDER_PARENS_RE = re.compile(
    r"^(?P<prefix>(?:chul|book|sky)_[A-Za-z0-9_]+)\((?P<label>[^)]+)\)$",
    re.IGNORECASE,
)

_CONFIG_KIND_INFRA_MYSQL_SEGMENTS = frozenset({"MySQL", "MsSQL"})


def infer_account_family(config_path: str) -> str | None:
    """``config_path`` 전체에서 첫 ``chul_*`` / ``book_*`` / ``sky_*`` 토큰."""
    m = _ACCOUNT_FAMILY_RE.search(config_path.replace("\\", "/"))
    return m.group(1).lower() if m else None


def infer_customer_folder(parent_dir_name: str) -> str:
    """``Config.Ini`` 직상위 폴더명 — SKU+괄호 라벨이면 괄호 안 한글명."""
    name = (parent_dir_name or "").strip()
    if not name:
        return ""
    m = _SKU_FOLDER_PARENS_RE.match(name)
    if m:
        return m.group("label").strip()
    return name


def infer_config_kind(config_path: str, account_family: str | None = None) -> str:
    """경로 세그먼트로 빌드 종류 분류 (카탈로그·overlay 보조)."""
    norm = config_path.replace("\\", "/")
    parts = norm.split("/")
    family = account_family if account_family is not None else infer_account_family(norm)

    if "자료전송" in parts:
        return "data_transfer"
    if family:
        return "customer_build"
    if "Login" in parts:
        return "infra_login"
    if any(
        p in _CONFIG_KIND_INFRA_MYSQL_SEGMENTS or p.startswith("MySQL-")
        for p in parts
    ):
        return "infra_mysql"
    if len(parts) <= 2:
        return "root_other"
    return "customer_build"


def _normalize_label(label: str) -> str:
    """공백·괄호·특수문자 제거 + 소문자 — 부분 매칭 보조."""
    return _PUNCT_RE.sub("", (label or "").lower())


def _label_match(candidate: str, normalized_pool: set[str]) -> bool:
    """후보가 풀 라벨 중 하나에 포함되거나, 풀 라벨이 후보에 포함되면 매치로 간주."""
    n = _normalize_label(candidate)
    if not n:
        return False
    if n in normalized_pool:
        return True
    return any(n in p or (p and p in n) for p in normalized_pool)


def build_diff(
    inventory: list[dict[str, Any]],
    seed_labels: set[str],
    matrix_labels: set[str],
) -> dict[str, Any]:
    """``Name`` / ``Uses`` 가 시드 또는 매트릭스 라벨에 없는 항목을 잡는다.

    매칭은 정규화 라벨(공백·괄호·접두 제거)을 사용한 부분 포함 매치까지 허용한다.
    """
    seed_norm = {_normalize_label(s) for s in seed_labels if s}
    seed_norm.discard("")
    matrix_norm = {_normalize_label(s) for s in matrix_labels if s}
    matrix_norm.discard("")
    missing: list[dict[str, Any]] = []
    for r in inventory:
        candidates = [c for c in (r.get("name", ""), r.get("uses", "")) if c.strip()]
        in_seed = any(_label_match(c, seed_norm) for c in candidates)
        in_matrix = any(_label_match(c, matrix_norm) for c in candidates)
        if not (in_seed or in_matrix):
            missing.append(
                {
                    "config_path": r["config_path"],
                    "name": r["name"],
                    "uses": r["uses"],
                    "in_seed": in_seed,
                    "in_matrix": in_matrix,
                }
            )
    return {
        "summary": {
            "total_configs": len(inventory),
            "missing_label_match": len(missing),
            "seed_labels": len(seed_labels),
            "matrix_labels": len(matrix_labels),
        },
        "missing_label_match": missing,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    parser.add_argument("--seed", default=str(DEFAULT_SEED_PATH))
    parser.add_argument("--matrix", default=str(DEFAULT_MATRIX_PATH))
    parser.add_argument("--inventory-out", default=str(DEFAULT_INVENTORY_OUT))
    parser.add_argument("--diff-out", default=str(DEFAULT_DIFF_OUT))
    parser.add_argument(
        "--strict",
        action="store_true",
        help="missing_label_match > 0 이면 exit 2 (PR/CI 가드용)",
    )
    args = parser.parse_args(argv)

    root = Path(args.root)
    inv = collect_inventory(root)
    inv_doc = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "count": len(inv),
        "items": inv,
    }
    Path(args.inventory_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.inventory_out).write_text(
        json.dumps(inv_doc, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    seed_doc = _read_json(Path(args.seed))
    matrix_doc = _read_json(Path(args.matrix))
    diff = build_diff(inv, _seed_labels(seed_doc), _matrix_labels(matrix_doc))
    Path(args.diff_out).write_text(
        json.dumps(diff, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"[OK] inventory  → {args.inventory_out} ({len(inv)} 건)")
    print(
        f"[OK] label diff → {args.diff_out} (missing={diff['summary']['missing_label_match']})"
    )
    if args.strict and diff["summary"]["missing_label_match"] > 0:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
