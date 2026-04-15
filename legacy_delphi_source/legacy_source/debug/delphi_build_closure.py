#!/usr/bin/env python3
"""Resolve Delphi project unit closure from Chulpan.dpr + recursive local unit search."""
from __future__ import annotations

import re
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DPR_PATH = ROOT / "Chulpan.dpr"
# Path segments as Unicode escapes (stable on all locales)
_DO = "\uB3C4\uC11C\uC720\uD1B5"  # ????????
_BOOK_KB = "book_kb(\uBC18\uD488\uACFC)"  # book_kb(?????)

EXTRA_DIRS = [
    ROOT,
    ROOT / "Data",
    ROOT / _DO,
    ROOT / _DO / _BOOK_KB,
]


def norm_rel(p: str) -> Path:
    p = p.strip().strip("'").strip('"')
    p = p.replace("\\", "/")
    return (ROOT / p).resolve()


def parse_dpr_uses(text: str) -> list[tuple[str, Path | None]]:
    out: list[tuple[str, Path | None]] = []
    for m in re.finditer(
        r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s+in\s+['\"]([^'\"]+)['\"]",
        text,
        re.MULTILINE,
    ):
        uname, rel = m.group(1), m.group(2)
        path = norm_rel(rel)
        out.append((uname, path))
    return out


USES_RE = re.compile(
    r"^\s*uses\s*(.*?)(?:\n\s*implementation\b|\Z)",
    re.DOTALL | re.IGNORECASE,
)
UNIT_CHUNK = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*(?:in\s+['\"]([^'\"]+)['\"])?\s*,")


def extract_uses_block(pas_text: str) -> str:
    m = USES_RE.search(pas_text)
    return m.group(1) if m else ""


def parse_uses_names_and_paths(block: str) -> list[tuple[str, str | None]]:
    items: list[tuple[str, str | None]] = []
    for m in UNIT_CHUNK.finditer(block + ","):
        items.append((m.group(1), m.group(2)))
    return items


def build_unit_index() -> dict[str, list[Path]]:
    """Index only root/Data/doseo top-level/book_kb to avoid wrong customer .pas matches."""
    idx: dict[str, list[Path]] = {}
    for p in ROOT.glob("*.pas"):
        idx.setdefault(p.stem, []).append(p.resolve())
    data = ROOT / "Data"
    if data.is_dir():
        for p in data.glob("*.pas"):
            idx.setdefault(p.stem, []).append(p.resolve())
    do = ROOT / _DO
    if do.is_dir():
        for p in do.glob("*.pas"):
            idx.setdefault(p.stem, []).append(p.resolve())
        bk = do / _BOOK_KB
        if bk.is_dir():
            for p in bk.glob("*.pas"):
                idx.setdefault(p.stem, []).append(p.resolve())
    return idx


UNIT_INDEX: dict[str, list[Path]] | None = None


def find_unit_file(unit: str, hint_dir: Path) -> Path | None:
    global UNIT_INDEX
    if UNIT_INDEX is None:
        UNIT_INDEX = build_unit_index()
    candidates = [hint_dir / f"{unit}.pas"]
    for d in EXTRA_DIRS:
        candidates.append(d / f"{unit}.pas")
    for p in candidates:
        if p.is_file():
            return p.resolve()
    hits = UNIT_INDEX.get(unit, [])
    if not hits:
        return None
    hint_r = hint_dir.resolve()
    for h in hits:
        if h.parent == hint_r:
            return h
    return min(hits, key=lambda x: len(x.parts))


def read_dpr_text() -> str:
    raw = DPR_PATH.read_bytes()
    for enc in ("cp949", "euc_kr", "utf-8-sig", "utf-8"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def closure_from_dpr() -> tuple[list[tuple[str, Path]], list[str]]:
    text = read_dpr_text()
    dpr_units = parse_dpr_uses(text)
    missing: list[str] = []
    resolved: list[tuple[str, Path]] = []
    for uname, path in dpr_units:
        if path is None or not path.is_file():
            missing.append(f"{uname}: {path}")
            continue
        resolved.append((uname, path))

    seen_paths: set[Path] = {p for _, p in resolved}
    queue: deque[Path] = deque(seen_paths)

    def process_file(pas_path: Path, content: str, start_slice: slice | None) -> None:
        chunk = content[start_slice] if start_slice else content
        low = chunk.lower()
        impl_idx = low.find("\nimplementation")
        iface = chunk[:impl_idx] if impl_idx != -1 else chunk
        block = extract_uses_block(iface)
        if not block and impl_idx != -1:
            block = extract_uses_block(chunk[impl_idx:])
        items = parse_uses_names_and_paths(block)
        hint = pas_path.parent
        for dep, in_path in items:
            if dep in {"SysInit", "System"}:
                continue
            if in_path:
                target = norm_rel(in_path)
                if target.is_file() and target not in seen_paths:
                    seen_paths.add(target)
                    queue.append(target)
                continue
            target = find_unit_file(dep, hint)
            if target and target not in seen_paths:
                seen_paths.add(target)
                queue.append(target)

    while queue:
        pas_path = queue.popleft()
        try:
            content = pas_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        process_file(pas_path, content, None)

    for pas_path in list(seen_paths):
        try:
            content = pas_path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        low = content.lower()
        impl_idx = low.find("\nimplementation")
        if impl_idx == -1:
            continue
        process_file(pas_path, content, slice(impl_idx, None))

    ordered = sorted(seen_paths, key=lambda p: str(p))
    return [(p.stem, p) for p in ordered], missing


def main() -> None:
    units, miss = closure_from_dpr()
    out_dir = ROOT / "docs" / "phase1-structure"
    out_dir.mkdir(parents=True, exist_ok=True)
    title = "\uBE4C\uB4DC \uD074\uB85C\uC800 (Chulpan.dpr \uAE30\uC900, \uC815\uC801 uses \uCD94\uC815)"
    lines = [f"# {title}\n\n", f"- DPR: `{DPR_PATH}`\n"]
    lines.append(f"- \uCD94\uC815 \uC720\uB2DB \uC218: **{len(units)}**\n\n")
    lines.append("| Unit | Path |\n|------|------|\n")
    for name, p in units:
        try:
            rel = p.relative_to(ROOT)
        except ValueError:
            rel = p
        lines.append(f"| {name} | `{rel}` |\n")
    if miss:
        lines.append("\n## DPR \uACBD\uB85C \uB204\uB77D/\uBD88\uC77C\uCE58\n\n")
        for m in miss:
            lines.append(f"- {m}\n")
    (out_dir / "01-build-closure.md").write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {out_dir / '01-build-closure.md'} units={len(units)}")


if __name__ == "__main__":
    main()
