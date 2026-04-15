#!/usr/bin/env python3
"""Generate phase1-structure markdown reports under docs/phase1-structure/."""
from __future__ import annotations

import csv
import hashlib
import io
import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "phase1-structure"
DO = ROOT / "\uB3C4\uC11C\uC720\uD1B5"  # doseryutong
HK = "\uD55C\uAD6D\uB3C4\uC11C\uC720\uD1B5"  # hanguk-doseo-yutong


def read_text_maybe_cp949(path: Path) -> str:
    raw = path.read_bytes()
    for enc in ("cp949", "utf-8-sig", "utf-8"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def parse_dpr_unit_names(text: str) -> list[str]:
    names: list[str] = []
    for m in re.finditer(
        r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s+in\s+['\"]([^'\"]+)['\"]",
        text,
        re.MULTILINE,
    ):
        names.append(m.group(1))
    return names


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    # --- 02 Chulpan catalog ---
    r = subprocess.run(
        ["find", str(ROOT), "-name", "Chulpan.dpr"],
        capture_output=True,
        text=True,
        check=False,
    )
    dprs = sorted(Path(x) for x in r.stdout.splitlines() if x.strip())
    by_parent: dict[str, list[str]] = defaultdict(list)
    for p in dprs:
        rel = p.relative_to(ROOT)
        parent = str(rel.parent) if rel.parent != Path(".") else "(root)"
        by_parent[parent].append(str(rel))

    r_b01 = subprocess.run(
        ["find", str(ROOT), "-name", "Base01.pas"],
        capture_output=True,
        text=True,
        check=False,
    )
    base01_n = len([x for x in r_b01.stdout.splitlines() if x.strip()])

    do_rel = str(DO.relative_to(ROOT)).replace("\\", "/")

    def chulpan_pattern(rel: str) -> str:
        if rel == "Chulpan.dpr":
            return "A_root"
        if rel.startswith("Interbase/"):
            return "B_interbase"
        if HK in rel:
            return "E_hanguk_tree"
        if re.match(r"^" + re.escape(do_rel + "/") + r"book_[^/]+/Chulpan\.dpr$", rel):
            return "C_book_member_top_level"
        if rel.startswith(do_rel + "/book_"):
            return "D_book_member_subtree"
        if rel.startswith(do_rel + "/chul_"):
            return "F_chul_branch"
        return "Z_other"

    by_pat: dict[str, list[str]] = defaultdict(list)
    for p in dprs:
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        by_pat[chulpan_pattern(rel)].append(rel)

    pat_descriptions = {
        "A_root": "Workspace root `Chulpan.dpr` (primary baseline)",
        "B_interbase": "`Interbase/` DB-variant line",
        "C_book_member_top_level": f"`{DO.name}/book_*/Chulpan.dpr` top-level only",
        "D_book_member_subtree": f"Nested `book_*` (`{DO.name}-New`, inner `{DO.name}`, ...)",
        "E_hanguk_tree": f"Contains `{HK}`",
        "F_chul_branch": f"`{DO.name}/chul_*` warehouse forks",
        "Z_other": "Other / unmatched pattern",
    }

    lines = ["# Variant catalog: all Chulpan.dpr paths\n\n"]
    lines.append(f"- Total **{len(dprs)}** `Chulpan.dpr` files under workspace root.\n")
    lines.append(f"- Total **`Base01.pas` paths** (find): **{base01_n}**.\n")
    lines.append(
        "- See also [04-variant-core-matrix.md](04-variant-core-matrix.md) for `Base01.pas` / `Chul.pas` hashes.\n\n"
    )
    lines.append("## Pattern grouping (naming-axis)\n\n")
    lines.append("| Group ID | Count | Meaning |\n|----------|------:|---------|\n")
    for gid in sorted(by_pat.keys()):
        desc = pat_descriptions.get(gid, "")
        lines.append(f"| `{gid}` | {len(by_pat[gid])} | {desc} |\n")
    lines.append("\n<details><summary>Paths per group (expand)</summary>\n\n")
    for gid in sorted(by_pat.keys()):
        lines.append(f"### `{gid}`\n\n")
        for rel in sorted(by_pat[gid]):
            lines.append(f"- `{rel}`\n")
        lines.append("\n")
    lines.append("</details>\n\n")
    lines.append("## By parent directory\n\n")
    for parent in sorted(by_parent.keys(), key=lambda s: (s.count("/"), s)):
        lines.append(f"## `{parent}`\n\n")
        for rel in sorted(by_parent[parent]):
            lines.append(f"- `{rel}`\n")
        lines.append("\n")
    (OUT / "02-variant-chulpan-catalog.md").write_text("".join(lines), encoding="utf-8")

    # --- 03 DPR uses diff ---
    root_dpr = ROOT / "Chulpan.dpr"
    root_units = set(parse_dpr_unit_names(read_text_maybe_cp949(root_dpr)))
    samples = [
        DO / "book_00(\uC704\uB7EC\uBE0C)" / "Chulpan.dpr",
        DO / "book_07(\uBD81\uC564\uBD81NEW)" / "Chulpan.dpr",
        DO / "book_04(\uD611\uC9C4\uB3C4\uC11C)" / "\uB3C4\uC11C\uC720\uD1B5-New" / "Chulpan.dpr",
        DO / "book_12(\uD50C\uB7EC\uC2A4\uBE44)" / "\uB3C4\uC11C\uC720\uD1B5-New" / "Chulpan.dpr",
        ROOT / "Interbase" / "Chulpan.dpr",
    ]
    lines = ["# Representative DPR diff: `uses` unit name sets vs root\n\n"]
    lines.append(f"- Baseline: root `Chulpan.dpr` unit count **{len(root_units)}**.\n\n")
    for sp in samples:
        if not sp.is_file():
            lines.append(f"## (missing) `{sp.relative_to(ROOT)}`\n\n")
            continue
        su = set(parse_dpr_unit_names(read_text_maybe_cp949(sp)))
        only_root = sorted(root_units - su)
        only_var = sorted(su - root_units)
        lines.append(f"## `{sp.relative_to(ROOT)}`\n\n")
        lines.append(f"- Variant unit count: **{len(su)}**\n")
        lines.append(
            f"- Only in baseline (-): **{len(only_root)}** / only in variant (+): **{len(only_var)}**\n\n"
        )
        if only_root[:40]:
            lines.append("### Units only in baseline (up to 40)\n\n")
            lines.append(", ".join(f"`{x}`" for x in only_root[:40]))
            lines.append("\n\n")
        if only_var[:40]:
            lines.append("### Units only in variant (up to 40)\n\n")
            lines.append(", ".join(f"`{x}`" for x in only_var[:40]))
            lines.append("\n\n")
        if not only_root and not only_var:
            lines.append("*(Same unit name set as baseline.)*\n\n")
    lines.append("## Notes\n\n")
    lines.append(
        "- Same unit *names* can still point to different `in '...'` paths; see [04-variant-core-matrix.md](04-variant-core-matrix.md).\n"
    )
    lines.append("- `Interbase/Chulpan.dpr` suggests DB stack fork (**plan type T4**).\n")
    (OUT / "03-variant-dpr-diff.md").write_text("".join(lines), encoding="utf-8")

    # --- 04 core matrix Base01 / Chul / Subu30 ---
    for name in ("Base01.pas", "Chul.pas", "Subu30.pas"):
        r2 = subprocess.run(
            ["find", str(ROOT), "-name", name],
            capture_output=True,
            text=True,
            check=False,
        )
        paths = sorted(Path(x) for x in r2.stdout.splitlines() if x.strip())
        lines = [f"# Same-name file matrix: `{name}`\n\n"]
        lines.append("| bytes | sha256[:16] | relative path |\n|------:|--------------|---------------|\n")
        for p in paths:
            try:
                sz = p.stat().st_size
                digest = sha256_file(p)
                rel = p.relative_to(ROOT)
            except OSError:
                continue
            lines.append(f"| {sz} | `{digest}` | `{rel}` |\n")
        lines.append("\n## Summary\n\n")
        by_hash: dict[str, list[str]] = defaultdict(list)
        for p in paths:
            try:
                d = sha256_file(p)
                by_hash[d].append(str(p.relative_to(ROOT)))
            except OSError:
                pass
        uniq = len(by_hash)
        lines.append(f"- Paths: **{len(paths)}**, distinct content hashes: **{uniq}**.\n")
        if uniq <= 10:
            for h, rs in sorted(by_hash.items(), key=lambda x: -len(x[1])):
                lines.append(f"- `{h}`: {len(rs)} path(s)\n")
        (OUT / f"04-matrix-{name.replace('.', '-')}").with_suffix(".md").write_text(
            "".join(lines), encoding="utf-8"
        )

    # merge 04 into one file for plan
    merged = ["# Core same-name matrix (Base01 / Chul / Subu30)\n\n"]
    for part in ("04-matrix-Base01-pas.md", "04-matrix-Chul-pas.md", "04-matrix-Subu30-pas.md"):
        merged.append((OUT / part).read_text(encoding="utf-8").replace("# Same-name file matrix:", "##"))
        merged.append("\n")
    merged.append("\n## T1-T4 hints (from matrix + DPR diff)\n\n")
    merged.append(
        "- **T4**: `Interbase/Base01.pas` vs root: different DB line (see [03-variant-dpr-diff.md](03-variant-dpr-diff.md)).\n"
    )
    merged.append(
        "- **T3**: Many distinct sha256 buckets for `Base01.pas` / `Chul.pas`: core forks across customers.\n"
    )
    merged.append(
        "- **T1 / T2**: Same hash in some `book_*` trees but different `uses` paths: correlate with [03-variant-dpr-diff.md](03-variant-dpr-diff.md) and [03b-variant-sample-diff-Subu30.md](03b-variant-sample-diff-Subu30.md).\n"
    )
    (OUT / "04-variant-core-matrix.md").write_text("".join(merged), encoding="utf-8")

    # --- 05 book registry ---
    book_dirs = sorted(
        [p for p in DO.iterdir() if p.is_dir() and p.name.startswith("book_")],
        key=lambda p: p.name,
    )

    def book_series_key(folder_name: str) -> str:
        if folder_name.startswith("book_kb"):
            return "book_kb"
        m = re.match(r"^(book_\d+)", folder_name)
        return m.group(1) if m else folder_name

    def member_label(folder_name: str) -> str:
        m = re.search(r"\(([^)]+)\)", folder_name)
        return m.group(1) if m else ""

    csv_buf = io.StringIO()
    csv_w = csv.writer(csv_buf)
    csv_w.writerow(
        [
            "folder",
            "book_series",
            "member_label",
            "chulpan_count",
            "chulpan_primary_relative",
            "chulpan_primary_absolute",
            "nested_note",
        ]
    )
    md = ["# Member registry (`book_*` under \uB3C4\uC11C\uC720\uD1B5)\n\n"]
    md.append(
        f"Immediate `book_*` folders under `{do_rel}/`. "
        "`Chulpan.dpr` counted with `find -maxdepth 6`. "
        "Absolute path = workspace + primary relative.\n\n"
    )
    md.append(
        "| folder | series | member (folder) | DPR # | first relative | absolute (primary) |\n"
        "|--------|--------|-----------------|------:|----------------|--------------------|\n"
    )
    for bd in book_dirs:
        r3 = subprocess.run(
            ["find", str(bd), "-maxdepth", "6", "-name", "Chulpan.dpr"],
            capture_output=True,
            text=True,
            check=False,
        )
        hits = [Path(x) for x in r3.stdout.splitlines() if x.strip()]
        primary_rel = hits[0].relative_to(ROOT) if hits else Path()
        primary_abs = str(hits[0].resolve()) if hits else ""
        note = "nested multiple" if len(hits) > 1 else ""
        ser = book_series_key(bd.name)
        ml = member_label(bd.name)
        prs = str(primary_rel) if hits else ""
        md.append(
            f"| `{bd.name}` | `{ser}` | {ml} | {len(hits)} | `{prs}` | `{primary_abs}` |\n"
        )
        csv_w.writerow([bd.name, ser, ml, len(hits), prs, primary_abs, note])
    md.append("\n## Same book_N, multiple members\n\n")
    md.append("| book_N | folders |\n|--------|--------|\n")
    by_num: dict[str, list[str]] = defaultdict(list)
    for bd in book_dirs:
        m = re.match(r"^(book_\d+)", bd.name)
        if m:
            by_num[m.group(1)].append(bd.name)
    for num in sorted(by_num.keys(), key=lambda x: int(x.split("_")[1])):
        names = by_num[num]
        if len(names) > 1:
            md.append(f"| {num} | {', '.join(f'`{n}`' for n in names)} |\n")
    (OUT / "05-book-member-registry.md").write_text("".join(md), encoding="utf-8")
    (OUT / "05-book-member-registry.csv").write_text(csv_buf.getvalue(), encoding="utf-8-sig")

    # --- 07 book delta (priority) ---
    md = ["# Member delta sheet (priority samples)\n\n"]
    md.append("Tags: **D_UI** (.dfm), **D_BIZ** (SQL/constants/logic), **D_CFG** (integration paths).\n\n")
    md.append("## Plan T1-T4 mapping (quick read)\n\n")
    md.append(
        "- **T1**: `Chulpan.dpr` `uses` differs mainly in `in` paths; unit names often match baseline (see DPR uses delta per folder).\n"
    )
    md.append(
        "- **T2**: Same unit set as baseline but a few `Subu*`/`Seok*` sources differ (business/FTP tweaks).\n"
    )
    md.append(
        "- **T3**: `Base01` / `Chul` content diverges (sha/size): menu/data model fork risk.\n"
    )
    md.append(
        "- **T4**: DB stack fork: see `Interbase` in [03-variant-dpr-diff.md](03-variant-dpr-diff.md) and `Interbase/Base01.pas` in matrix.\n\n"
    )

    def file_digest_pair(rel: Path) -> tuple[int, str] | None:
        p = ROOT / rel
        if not p.is_file():
            return None
        return p.stat().st_size, sha256_file(p)

    root_b01 = file_digest_pair(Path("Base01.pas"))
    root_chul = file_digest_pair(Path("Chul.pas"))
    root_s30 = file_digest_pair(Path("Subu30.pas"))

    targets = [
        DO / "book_07(\uBD81\uC564\uBD81)",
        DO / "book_07(\uBD81\uC564\uBD81Skin)",
        DO / "book_07(\uBD81\uC564\uBD81NEW)",
        DO / "book_07(up)",
        DO / "book_11(\uACE0\uB824\uCD9C\uD310\uBB3C\uB958)",
        DO / "book_11(\uC815\uC9C4\uBB3C\uB958)",
    ]
    for bd in targets:
        if not bd.is_dir():
            continue
        md.append(f"## `{bd.relative_to(ROOT)}`\n\n")
        r_dpr = subprocess.run(
            ["find", str(bd), "-maxdepth", "6", "-name", "Chulpan.dpr"],
            capture_output=True,
            text=True,
            check=False,
        )
        dpr_hits = [Path(x) for x in r_dpr.stdout.splitlines() if x.strip()]
        if dpr_hits:
            vtext = read_text_maybe_cp949(dpr_hits[0])
            vu = set(parse_dpr_unit_names(vtext))
            only_root = sorted(root_units - vu)
            only_var = sorted(vu - root_units)
            md.append(
                f"- **DPR uses delta vs root** (`{dpr_hits[0].relative_to(ROOT)}`): "
                f"only in baseline (-) **{len(only_root)}**, only in variant (+) **{len(only_var)}**.\n"
            )
        else:
            md.append("- **DPR uses delta**: *(no Chulpan.dpr under this folder within maxdepth 6)*\n")
        for fname, root_pair, label in (
            ("Base01.pas", root_b01, "D_BIZ / T3"),
            ("Chul.pas", root_chul, "shell / menu"),
            ("Subu30.pas", root_s30, "sample work form"),
        ):
            p = bd / fname
            if not p.is_file():
                md.append(f"- `{fname}`: *(not in folder; build may use root or other path)*\n")
                continue
            sz, d = p.stat().st_size, sha256_file(p)
            if root_pair and (sz, d) == root_pair:
                md.append(f"- `{fname}`: **identical to root** (size={sz}, sha={d})\n")
            else:
                md.append(
                    f"- `{fname}`: **differs from root** size={sz} sha={d} (root: {root_pair}) — `{label}`\n"
                )
        dfm = bd / "Subu30.dfm"
        if dfm.is_file():
            root_dfm = ROOT / "Subu30.dfm"
            rs = root_dfm.stat().st_size if root_dfm.is_file() else None
            ds = dfm.stat().st_size
            tag = "D_UI likely" if rs != ds else "D_UI same size (compare content separately)"
            md.append(f"- `Subu30.dfm`: size={ds} (root dfm size={rs}) — {tag}\n")
        md.append("\n")

    md.append("## book_11 pair: Base01 comparison\n\n")
    p1 = DO / "book_11(\uACE0\uB824\uCD9C\uD310\uBB3C\uB958)" / "Base01.pas"
    p2 = DO / "book_11(\uC815\uC9C4\uBB3C\uB958)" / "Base01.pas"
    if p1.is_file() and p2.is_file():
        md.append(f"- book_11 go-ryeo: size={p1.stat().st_size} sha={sha256_file(p1)}\n")
        md.append(f"- book_11 jeong-jin: size={p2.stat().st_size} sha={sha256_file(p2)}\n")
        md.append(
            "- Same content: **"
            + ("yes" if sha256_file(p1) == sha256_file(p2) else "no; separate D_BIZ maintenance")
            + "**\n"
        )
    (OUT / "07-book-member-delta.md").write_text("".join(md), encoding="utf-8")

    # --- variant sample diff (Subu30 root vs book_07 BukAndBuk) ---
    a = ROOT / "Subu30.pas"
    b = DO / "book_07(\uBD81\uC564\uBD81)" / "Subu30.pas"
    sample_md = ["# Sample unified diff: Subu30.pas (root vs doseryutong/book_07 buk-and-buk)\n\n"]
    if a.is_file() and b.is_file():
        proc = subprocess.run(
            ["diff", "-u", str(a), str(b)],
            capture_output=True,
            text=True,
            check=False,
        )
        out = proc.stdout
        sample_md.append("```diff\n")
        sample_md.append(out[:12000] if len(out) > 12000 else out)
        if len(out) > 12000:
            sample_md.append("\n... (truncated)\n")
        sample_md.append("\n```\n")
    else:
        sample_md.append("*(missing one of the files)*\n")
    (OUT / "03b-variant-sample-diff-Subu30.md").write_text("".join(sample_md), encoding="utf-8")

    print("phase1 reports written to", OUT)


if __name__ == "__main__":
    main()
