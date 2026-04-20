#!/usr/bin/env python3
"""
워크스페이스 내 모든 `.frf` → Canonical IR (JSON) + HTML 템플릿 일괄 변환.

산출물:
  debug/output/frf_converted_all/<원본경로 상대디렉터리>/<파일명>.ir.json
  debug/output/frf_converted_all/<원본경로 상대디렉터리>/<파일명>.template.html

기본값은 레거시 정본 디렉터리만 (`legacy_delphi_source/legacy_source/Report`).
전체 저장소 스캔은 `--scan-repo`.

라이선스: 디코더 본문은 debug/frf_decoder_poc.py 의 BSD-2 고지 준수.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _ensure_backend_path(root: Path) -> None:
    backend = root / "도서물류관리프로그램" / "backend"
    if str(backend) not in sys.path:
        sys.path.insert(0, str(backend))


def _collect_frf_paths(roots: list[Path]) -> list[Path]:
    out: list[Path] = []
    for root in roots:
        if not root.is_dir():
            continue
        out.extend(sorted(root.rglob("*.frf")))
    # 안정 정렬 (경로 문자열)
    return sorted(set(out), key=lambda p: str(p))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Batch FRF → IR JSON + HTML template")
    parser.add_argument(
        "--scan-repo",
        action="store_true",
        help="저장소 전체에서 *.frf 검색 (기본은 legacy Report 디렉터리만)",
    )
    parser.add_argument(
        "--no-html",
        action="store_true",
        help="IR JSON 만 생성 (HTML 생략)",
    )
    # v0.5.0 (2026-04-20) — SVG 미리보기는 운영에 사용되지 않아 *기본 비활성*.
    # API 호환을 위해 ``compile_ir_to_svg`` 자체는 print_ir_compiler 에 존속
    # 유지하되, 본 배치는 더 이상 .preview.svg 파일을 생성하지 않는다.
    # 의도적으로 켜고 싶을 때만 ``--enable-svg`` 사용 (디버그 한정).
    parser.add_argument(
        "--no-svg",
        action="store_true",
        default=True,
        help="(기본 ON) SVG 미리보기 (.preview.svg) 생략 — 운영 미사용으로 제거",
    )
    parser.add_argument(
        "--enable-svg",
        action="store_true",
        help="(디버그 전용) SVG 미리보기 생성을 강제로 활성화",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="출력 루트 (기본: debug/output/frf_converted_all)",
    )
    parser.add_argument(
        "--debug-outline",
        action="store_true",
        help="HTML 컴파일러의 debug_outline 모드를 켠다 (객체 경계선 + legacy-id 표시)",
    )
    parser.add_argument(
        "--quality-report",
        action="store_true",
        help="배치 후 frf_quality_report 의 집계 요약을 호출해 stdout 에 동봉",
    )
    args = parser.parse_args(argv)
    # ``--enable-svg`` 는 ``--no-svg`` 기본값(True) 을 명시적으로 끈다.
    if args.enable_svg:
        args.no_svg = False

    root = _repo_root()
    out_root = args.out_dir or (root / "debug/output/frf_converted_all")
    out_root.mkdir(parents=True, exist_ok=True)

    if args.scan_repo:
        roots = [root]
    else:
        roots = [root / "legacy_delphi_source/legacy_source/Report"]

    if args.scan_repo:
        paths = sorted({p for p in root.rglob("*.frf") if p.is_file()}, key=lambda x: str(x))
        # 산출물 디렉터리 자체는 입력에서 제외
        paths = [p for p in paths if "debug/output/" not in str(p)]
    else:
        paths = _collect_frf_paths(roots)

    decoder_path = root / "debug" / "frf_decoder_poc.py"
    spec = importlib.util.spec_from_file_location("frf_decoder_poc", decoder_path)
    if spec is None or spec.loader is None:
        print(f"cannot load decoder: {decoder_path}", file=sys.stderr)
        return 2
    dec_mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name or "frf_decoder_poc"] = dec_mod
    spec.loader.exec_module(dec_mod)
    decode_frf = dec_mod.decode_frf
    decoder_version = getattr(dec_mod, "DECODER_VERSION", "?")

    compile_ir_to_html = None
    compile_ir_to_svg = None
    compiler_version = None
    if not args.no_html or not args.no_svg:
        _ensure_backend_path(root)
        from app.services.print_ir_compiler import (  # noqa: E402
            compile_ir_to_html as _c,
            compile_ir_to_svg as _csvg,
            COMPILER_VERSION as _cv,
        )

        compile_ir_to_html = _c if not args.no_html else None
        compile_ir_to_svg = _csvg if not args.no_svg else None
        compiler_version = _cv

    manifest: dict = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scan_repo": args.scan_repo,
        "roots": [str(r) for r in roots],
        "total_input": len(paths),
        "decoder_version": decoder_version,
        "compiler_version": compiler_version,
        "debug_outline": bool(args.debug_outline),
        "svg_preview": not args.no_svg,
        "ok": 0,
        "fail": 0,
        "entries": [],
    }

    svg_summary: dict[str, int] = {"svg_files": 0}

    binding_summary: dict[str, int] = {
        "files_with_placeholders": 0,
        "placeholders_total": 0,
        "literal_filled_total": 0,
        "binding_empty_total": 0,
    }

    for i, frf_path in enumerate(paths):
        rel = frf_path.relative_to(root)
        dest_dir = out_root / rel.parent
        dest_dir.mkdir(parents=True, exist_ok=True)
        stem = frf_path.stem
        ir_path = dest_dir / f"{stem}.ir.json"
        html_path = dest_dir / f"{stem}.template.html"
        svg_path = dest_dir / f"{stem}.preview.svg"

        entry: dict = {"rel": str(rel), "ir": str(ir_path.relative_to(root))}
        try:
            ir = decode_frf(frf_path)
            ir_path.write_text(json.dumps(ir, ensure_ascii=False, indent=2), encoding="utf-8")
            if compile_ir_to_svg is not None:
                svg = compile_ir_to_svg(
                    ir,
                    debug_outline=args.debug_outline,
                )
                svg_path.write_text(svg, encoding="utf-8")
                entry["svg"] = str(svg_path.relative_to(root))
                svg_summary["svg_files"] += 1
            if compile_ir_to_html is not None:
                html, diag = compile_ir_to_html(
                    ir,
                    debug_outline=args.debug_outline,
                    return_diagnostics=True,
                )
                html_path.write_text(html, encoding="utf-8")
                entry["html"] = str(html_path.relative_to(root))
                entry["compiler_diagnostics"] = {
                    "object_total": diag["object_total"],
                    "rendered_by_type": diag["rendered_by_type"],
                    "skipped_by_type": diag["skipped_by_type"],
                    "binding_placeholders_count": len(diag["binding_placeholders"]),
                    "binding_literal_filled": diag["binding_literal_filled"],
                    "binding_empty": diag["binding_empty"],
                }
                binding_summary["placeholders_total"] += len(diag["binding_placeholders"])
                binding_summary["literal_filled_total"] += diag["binding_literal_filled"]
                binding_summary["binding_empty_total"] += diag["binding_empty"]
                if diag["binding_placeholders"]:
                    binding_summary["files_with_placeholders"] += 1
            warns = ir.get("decoder_warnings") or []
            entry["decoder_warnings_count"] = len(warns)
            manifest["ok"] += 1
        except Exception as e:
            manifest["fail"] += 1
            entry["error"] = f"{type(e).__name__}: {e}"
            entry["traceback"] = traceback.format_exc()
        manifest["entries"].append(entry)
        if (i + 1) % 200 == 0:
            print(f"[frf_batch] progress {i + 1}/{len(paths)} …", file=sys.stderr)

    manifest["binding_summary"] = binding_summary
    manifest["svg_summary"] = svg_summary

    summary_path = out_root / "_batch_manifest.json"
    summary_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    quality_summary: dict | None = None
    if args.quality_report:
        try:
            quality_summary = _run_quality_report(root, out_root)
        except Exception as e:
            quality_summary = {"error": f"{type(e).__name__}: {e}"}

    print(
        json.dumps(
            {
                "ok": manifest["ok"],
                "fail": manifest["fail"],
                "out_root": str(out_root),
                "manifest": str(summary_path),
                "decoder_version": decoder_version,
                "compiler_version": compiler_version,
                "binding_summary": binding_summary,
                "svg_summary": svg_summary,
                "quality_summary": quality_summary,
            },
            ensure_ascii=False,
        )
    )
    return 0 if manifest["fail"] == 0 else 1


def _run_quality_report(root: Path, out_root: Path) -> dict:
    """frf_quality_report 를 in-process 로 호출해 요약을 가져온다 (READ-ONLY)."""
    qr_path = root / "debug" / "frf_quality_report.py"
    spec = importlib.util.spec_from_file_location("frf_quality_report", qr_path)
    if spec is None or spec.loader is None:
        return {"error": f"cannot load {qr_path}"}
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name or "frf_quality_report"] = mod
    spec.loader.exec_module(mod)
    paths = mod.collect_ir_paths(out_root)
    metrics = []
    for p in paths:
        try:
            ir = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        metrics.append(mod.evaluate_ir(ir, rel_path=str(p.relative_to(out_root))))
    return mod.aggregate(metrics)


if __name__ == "__main__":
    sys.exit(main())
