#!/usr/bin/env python3
"""
레거시 델파이 소스 UTF-8 스캔·매니페스트·선택 변환.

`delphi_source_encoding` 과 동일한 디코드 순서로 텍스트를 얻은 뒤,
UTF-8(BOM 제거 본문) 바이트가 원본과 같으면 skip, 다르면 convert 후보.

사용법:
  python3 tools/legacy_source_utf8_scan.py --root legacy_delphi_source/legacy_source \\
    --out analysis/legacy_utf8_manifest.json

  python3 tools/legacy_source_utf8_scan.py --root ... --out manifest.json \\
    --apply --dest-root /path/to/legacy_source_utf8_mirror

  python3 tools/legacy_source_utf8_scan.py --root ... --out manifest.json \\
    --apply --in-place
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

_TOOLS = Path(__file__).resolve().parent
_PARSERS = _TOOLS / "parsers"
if str(_PARSERS) not in sys.path:
    sys.path.insert(0, str(_PARSERS))

from delphi_source_encoding import (  # noqa: E402
    classify_delphi_source_bytes,
    decode_delphi_raw_bytes,
)

TEXT_EXTENSIONS = frozenset({".pas", ".dfm", ".dpr", ".inc"})


def _skip_path(rel: Path) -> bool:
    name = rel.name
    if name.startswith("~") or name.startswith("."):
        return True
    if ".~" in name or name.endswith(".bak"):
        return True
    return False


def tier_for(rel: Path) -> int:
    """1=Data/ 이하, 2=그 외, 3=.dpr(프로젝트 진입점 우선 표기)."""
    suf = rel.suffix.lower()
    if suf == ".dpr":
        return 3
    parts = rel.parts
    if parts and parts[0] == "Data":
        return 1
    return 2


def iter_text_files(root: Path):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            rel = p.relative_to(root)
        except ValueError:
            continue
        if _skip_path(rel):
            continue
        yield p, rel


def scan_root(root: Path) -> dict:
    files: list[dict] = []
    summary = {"skip": 0, "convert": 0}
    for abs_p, rel in iter_text_files(root):
        raw = abs_p.read_bytes()
        cl = classify_delphi_source_bytes(raw)
        action = cl["action"]
        summary[action] += 1
        files.append(
            {
                "path": str(rel).replace("\\", "/"),
                "tier": tier_for(rel),
                "action": action,
                "inferred_encoding": cl["inferred_encoding"],
                "has_bom": cl["has_bom"],
                "size_bytes": len(raw),
            }
        )
    files.sort(key=lambda x: (x["tier"], x["path"]))
    return {
        "root": str(root.resolve()),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "files": files,
    }


def apply_manifest(manifest: dict, root: Path, dest_root: Path | None, in_place: bool) -> None:
    """convert 는 UTF-8(무BOM) 저장, skip 은 dest 미러 시 원본 복사."""
    root = root.resolve()
    files = manifest.get("files") or []
    written = 0
    copied = 0
    for entry in files:
        rel = Path(entry["path"])
        src = root / rel
        if not src.is_file():
            continue
        raw = src.read_bytes()
        text, _ = decode_delphi_raw_bytes(raw)
        utf8_bytes = text.encode("utf-8")
        action = entry.get("action")
        if in_place:
            if action != "convert":
                continue
            src.write_bytes(utf8_bytes)
            written += 1
            continue
        if dest_root is None:
            raise SystemExit("--apply with mirror requires --dest-root")
        dst = dest_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if action == "convert":
            dst.write_bytes(utf8_bytes)
            written += 1
        else:
            shutil.copy2(src, dst)
            copied += 1
    mode = "in_place" if in_place else f"mirror->{dest_root}"
    print(f"apply done ({mode}): convert_written={written}, skip_copied={copied}")


def main() -> None:
    ap = argparse.ArgumentParser(description="레거시 소스 UTF-8 스캔·매니페스트·선택 변환")
    ap.add_argument("--root", type=Path, required=True, help="스캔 루트(예: legacy_delphi_source/legacy_source)")
    ap.add_argument("--out", type=Path, required=True, help="매니페스트 JSON 경로")
    ap.add_argument("--apply", action="store_true", help="변환 적용(기본은 매니페스트만)")
    ap.add_argument(
        "--dest-root",
        type=Path,
        default=None,
        help="미러 출력 루트(convert/skip 모두 반영). --apply 시 --in-place 와 배타.",
    )
    ap.add_argument(
        "--in-place",
        action="store_true",
        help="convert 대상만 원본 경로에 UTF-8(무BOM) 덮어쓰기(되돌리기 어려움)",
    )
    args = ap.parse_args()

    root = args.root
    if not root.is_dir():
        print(f"Error: not a directory: {root}", file=sys.stderr)
        sys.exit(1)

    manifest = scan_root(root)
    out_path = args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote manifest: {out_path}")
    s = manifest["summary"]
    print(f"summary: skip={s['skip']} convert={s['convert']} total={s['skip'] + s['convert']}")

    if args.apply:
        if args.in_place and args.dest_root:
            print("Error: use only one of --in-place or --dest-root", file=sys.stderr)
            sys.exit(1)
        if not args.in_place and args.dest_root is None:
            print("Error: --apply requires --dest-root (mirror) or --in-place", file=sys.stderr)
            sys.exit(1)
        apply_manifest(manifest, root, args.dest_root, args.in_place)


if __name__ == "__main__":
    main()
