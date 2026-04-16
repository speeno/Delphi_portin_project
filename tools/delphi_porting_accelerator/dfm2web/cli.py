from __future__ import annotations

import argparse
import json
import traceback
from pathlib import Path

from .normalizer import normalize_node
from .parser import DfmParser, dump_tree_json
from .pas_analyzer import analyze_pas
from .renderer import HtmlRenderer
from .reporting import write_porting_reports
from .string_resolve import apply_resource_strings, build_string_id_map


def convert_one(
    dfm_path: Path,
    pas_path: Path | None,
    out_dir: Path,
    *,
    rc_id_map: dict[int, str] | None = None,
) -> None:
    parser = DfmParser()
    root = parser.parse_file(dfm_path)
    normalized = normalize_node(root, is_root=True)
    pas_analysis = analyze_pas(pas_path) if pas_path and pas_path.exists() else None
    unresolved: list[dict] = []
    if rc_id_map:
        pas_rs = pas_analysis.get('resourcestrings') if pas_analysis else None
        unresolved = apply_resource_strings(normalized, rc_id_map, pas_rs)
    out_dir.mkdir(parents=True, exist_ok=True)
    dump_tree_json(root, out_dir / f'{root.name}.tree.json')
    renderer = HtmlRenderer()
    renderer.write_outputs(out_dir, normalized, pas_analysis, unresolved_ids=unresolved)


def batch_convert(
    src_dir: Path,
    out_dir: Path,
    *,
    root_only: bool = False,
    rc_paths: list[Path] | None = None,
) -> None:
    if root_only:
        dfm_iter = sorted(src_dir.glob('*.dfm'))
    else:
        dfm_iter = sorted(src_dir.rglob('*.dfm'))
    out_dir.mkdir(parents=True, exist_ok=True)
    rc_id_map = build_string_id_map(rc_paths) if rc_paths else None
    errors: list[dict[str, str]] = []
    for dfm in dfm_iter:
        pas = dfm.with_suffix('.pas')
        try:
            convert_one(dfm, pas if pas.exists() else None, out_dir / dfm.stem, rc_id_map=rc_id_map)
        except Exception as exc:  # noqa: BLE001 — batch must continue per form
            errors.append(
                {
                    'dfm': str(dfm),
                    'error': str(exc),
                    'traceback': traceback.format_exc(),
                }
            )
    if errors:
        rep = out_dir / 'reports'
        rep.mkdir(parents=True, exist_ok=True)
        (rep / 'conversion_errors.json').write_text(
            json.dumps(errors, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    write_porting_reports(out_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description='Convert Delphi DFM/PAS to HTML layout and normalized JSON')
    sub = parser.add_subparsers(dest='command', required=True)

    convert = sub.add_parser('convert')
    convert.add_argument('--dfm', required=True)
    convert.add_argument('--pas')
    convert.add_argument('--out', required=True)
    convert.add_argument('--rc', action='append', default=[], help='.rc STRINGTABLE file (repeatable)')

    batch = sub.add_parser('batch')
    batch.add_argument('--src', required=True)
    batch.add_argument('--out', required=True)
    batch.add_argument('--rc', action='append', default=[], help='.rc STRINGTABLE file (repeatable)')
    batch.add_argument(
        '--root-only',
        action='store_true',
        help='Convert only *.dfm directly under --src (no subfolders)',
    )

    report = sub.add_parser('report', help='Re-generate reports from an existing batch output')
    report.add_argument('--dir', required=True, help='Batch output directory')

    args = parser.parse_args()
    rc_paths = [Path(p) for p in getattr(args, 'rc', None) or []]

    if args.command == 'convert':
        rc_map = build_string_id_map(rc_paths) if rc_paths else None
        convert_one(Path(args.dfm), Path(args.pas) if args.pas else None, Path(args.out), rc_id_map=rc_map)
    elif args.command == 'batch':
        batch_convert(Path(args.src), Path(args.out), root_only=bool(args.root_only), rc_paths=rc_paths or None)
    elif args.command == 'report':
        write_porting_reports(Path(args.dir))


if __name__ == '__main__':
    main()
