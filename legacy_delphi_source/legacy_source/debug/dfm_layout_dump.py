# -*- coding: utf-8 -*-
"""Extract Left/Top/Width/Height (and ClientWidth/ClientHeight) from a Delphi text .dfm.

Prints UTF-8 JSON to stdout. Run from repo root (directory containing web/ and debug/):

  python3 debug/dfm_layout_dump.py Subu67.dfm
  python3 debug/dfm_layout_dump.py path/relative/to/repo/Subu12.dfm --max-depth 8

Input file encoding: utf-8-sig, utf-8, cp949, euc-kr. Assumes space-indented DFM.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

INT_KEYS = frozenset(
    {"Left", "Top", "Width", "Height", "ClientWidth", "ClientHeight"}
)


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw[3:].decode("utf-8-sig")
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def indent_len(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def parse_int_value(s: str) -> int | None:
    s = s.strip()
    if not s or s[0] in "'\"":
        return None
    m = re.match(r"^(-?\d+)\s*$", s)
    if not m:
        return None
    return int(m.group(1))


def _emit_path(
    popped: tuple[int, str, str, dict[str, int]],
    stack: list[tuple[int, str, str, dict[str, int]]],
    out: list[dict],
    max_depth: int,
) -> None:
    _ind, name, typ, props = popped
    if not props:
        return
    path_names = [x[1] for x in stack] + [name]
    if len(path_names) > max_depth:
        path_names = path_names[:max_depth]
    out.append({"path": ".".join(path_names), "type": typ, "geometry": props})


def parse_dfm_with_paths(text: str, max_depth: int) -> list[dict]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    stack: list[tuple[int, str, str, dict[str, int]]] = []
    out: list[dict] = []

    for line in lines:
        stripped = line.strip()
        ind = indent_len(line)

        if stripped.startswith("object ") and ": " in stripped:
            m = re.match(r"object\s+(\w+)\s*:\s*(\S+)", stripped)
            if not m:
                continue
            name, typ = m.group(1), m.group(2)
            while stack and stack[-1][0] >= ind:
                stack.pop()
            stack.append((ind, name, typ, {}))
            continue

        if stripped == "end":
            if not stack:
                continue
            while stack and stack[-1][0] > ind:
                popped = stack.pop()
                _emit_path(popped, stack, out, max_depth)
            if stack and stack[-1][0] == ind:
                popped = stack.pop()
                _emit_path(popped, stack, out, max_depth)
            continue

        if "=" in stripped and stack and not stripped.startswith("object "):
            parts = stripped.split("=", 1)
            key = parts[0].strip()
            if key in INT_KEYS and len(parts) == 2:
                val = parse_int_value(parts[1])
                if val is not None:
                    stack[-1][3][key] = val

    while stack:
        popped = stack.pop()
        _emit_path(popped, stack, out, max_depth)

    return out


def main() -> None:
    ap = argparse.ArgumentParser(description="Dump geometry from a Delphi .dfm text file.")
    ap.add_argument("dfm", type=str, help="Path to .dfm (relative to repo root or absolute)")
    ap.add_argument(
        "--max-depth",
        type=int,
        default=32,
        metavar="N",
        help="Max path segments per row (default 32)",
    )
    args = ap.parse_args()
    p = Path(args.dfm)
    if not p.is_file():
        p2 = ROOT / args.dfm
        if p2.is_file():
            p = p2
        else:
            print(f"File not found: {args.dfm}", file=sys.stderr)
            sys.exit(1)
    text = read_text(p)
    try:
        rel = str(p.relative_to(ROOT))
    except ValueError:
        rel = str(p)
    rows = parse_dfm_with_paths(text, max_depth=int(args.max_depth))
    doc = {"source": rel, "nodes": rows}
    sys.stdout.buffer.write(json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8"))
    sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
