#!/usr/bin/env python3
"""
C7 FRF → IR/HTML 후보 분류·변환 파이프라인.

운영 런타임에서 .frf 를 직접 읽지 않는다. 본 스크립트는 빌드/감사 단계에서만
사용하며, 승인된 IR 만 backend/app/services/print_templates/auto 로 수동 반영한다.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "도서물류관리프로그램" / "backend"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from debug.frf_decoder_poc import decode_frf  # noqa: E402
from app.services.print_ir_compiler import compile_ir_to_html  # noqa: E402


@dataclass(frozen=True)
class FormSpec:
    form_id: str
    patterns: tuple[str, ...]
    required_labels: tuple[str, ...]
    optional_labels: tuple[str, ...] = ()


C7_FORM_SPECS: tuple[FormSpec, ...] = (
    FormSpec(
        "sales_statement_base",
        ("Report_2_11*.frf",),
        ("거래명세서", "도서명", "금액", "비고"),
        ("공급받는자보관용", "공급자보관용", "합계금액", "총 부 수"),
    ),
    FormSpec(
        "outbound_statement_base",
        ("Report_4_51*.frf",),
        ("거래명세서", "도서명", "금액"),
        ("수량", "비고", "합계"),
    ),
    FormSpec(
        "return_receipt_base",
        ("Report_2_13*.frf",),
        ("도서명", "금액"),
        ("반품", "영수증", "수량", "비고"),
    ),
    FormSpec(
        "label_form",
        ("Report_1_21.frf", "Report_1_22.frf", "Report_1_23.frf", "Report_1_24.frf", "Report_1_25.frf"),
        ("[Gname]",),
        ("[Gpost]", "[Gadds]", "[Gposa]"),
    ),
    FormSpec(
        "invoice_base",
        ("Report_5_61*.frf", "Report_5_62*.frf"),
        ("청구",),
        ("합계", "금액", "거래처"),
    ),
    FormSpec(
        "tax_invoice_base",
        ("계산서.frf",),
        ("계산서",),
        ("공급자", "공급받는자", "합계"),
    ),
)


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def find_handoff_root(repo_root: Path = REPO_ROOT) -> Path:
    """WeLove_FTP/Welove_인수인계 의 유니코드 정규화 차이를 흡수해 찾는다."""
    ftp = repo_root / "WeLove_FTP"
    for p in ftp.iterdir():
        if p.is_dir() and _nfc(p.name) == "Welove_인수인계":
            return p
    raise FileNotFoundError("WeLove_FTP/Welove_인수인계 폴더를 찾을 수 없습니다.")


def _binding_texts(ir: dict[str, Any]) -> list[str]:
    out: list[str] = []
    for page in ir.get("pages") or []:
        for band in page.get("bands") or []:
            for obj in band.get("objects") or []:
                binding = obj.get("binding") or {}
                text = binding.get("raw") or binding.get("value")
                if text:
                    out.append(str(text))
    return out


def _quality(ir: dict[str, Any], texts: list[str], spec: FormSpec) -> dict[str, Any]:
    objects = [
        obj
        for page in ir.get("pages") or []
        for band in page.get("bands") or []
        for obj in band.get("objects") or []
    ]
    with_rect = [
        obj
        for obj in objects
        if (obj.get("rect_mm") or {}).get("w", 0) and (obj.get("rect_mm") or {}).get("h", 0)
    ]
    expressions = ir.get("expressions_dictionary") or {}
    joined = " ".join(texts)
    required_hit = [label for label in spec.required_labels if label in joined]
    optional_hit = [label for label in spec.optional_labels if label in joined]
    return {
        "object_total": len(objects),
        "coord_recovery": round(len(with_rect) / max(1, len(objects)), 4),
        "binding_fill": round(len(expressions) / max(1, len(objects)), 4),
        "required_hit": required_hit,
        "optional_hit": optional_hit,
        "required_pass": len(required_hit) == len(spec.required_labels),
        "decoder_warnings": len(ir.get("decoder_warnings") or []),
    }


def classify_candidates(root: Path, *, limit_per_spec: int = 50) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for spec in C7_FORM_SPECS:
        paths: list[Path] = []
        for pattern in spec.patterns:
            paths.extend(p for p in root.rglob(pattern) if p.is_file())
        for path in sorted(set(paths), key=lambda p: (p.name, len(str(p)), str(p)))[:limit_per_spec]:
            if path in seen:
                continue
            seen.add(path)
            try:
                ir = decode_frf(path)
                texts = _binding_texts(ir)
                q = _quality(ir, texts, spec)
                page = (ir.get("pages") or [{}])[0]
                entries.append(
                    {
                        "form_id": spec.form_id,
                        "variant": path.stem,
                        "path": str(path),
                        "rel": str(path.relative_to(REPO_ROOT)) if path.is_relative_to(REPO_ROOT) else str(path),
                        "page_size_mm": page.get("size_mm") or {},
                        "labels_sample": texts[:40],
                        "quality": q,
                    }
                )
            except Exception as exc:  # noqa: BLE001 - 감사 산출물에는 실패도 기록
                entries.append(
                    {
                        "form_id": spec.form_id,
                        "variant": path.stem,
                        "path": str(path),
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
    return entries


def write_inventory(entries: list[dict[str, Any]], *, out_json: Path, out_md: Path) -> None:
    out_json.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entry_count": len(entries),
        "entries": entries,
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# C7 FRF 템플릿 후보 인벤토리",
        "",
        f"- generated_at: `{payload['generated_at']}`",
        f"- entry_count: `{len(entries)}`",
        "",
        "| form_id | variant | required_pass | coord_recovery | binding_fill | path |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for e in entries:
        q = e.get("quality") or {}
        lines.append(
            "| {form_id} | {variant} | {required_pass} | {coord} | {binding} | `{path}` |".format(
                form_id=e.get("form_id", ""),
                variant=e.get("variant", ""),
                required_pass=q.get("required_pass", False),
                coord=q.get("coord_recovery", ""),
                binding=q.get("binding_fill", ""),
                path=e.get("rel") or e.get("path", ""),
            )
        )
    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def convert_entries(entries: list[dict[str, Any]], *, out_dir: Path, limit: int = 20) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    out_dir.mkdir(parents=True, exist_ok=True)
    for e in entries:
        if len(out) >= limit:
            break
        if not (e.get("quality") or {}).get("required_pass"):
            continue
        path = Path(str(e["path"]))
        form_id = str(e["form_id"])
        suffix = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:8]
        variant = f"{e['variant']}.{suffix}"
        dest = out_dir / form_id
        dest.mkdir(parents=True, exist_ok=True)
        ir = decode_frf(path)
        html, diag = compile_ir_to_html(ir, document_title=form_id, return_diagnostics=True)
        ir_path = dest / f"{variant}.ir.json"
        html_path = dest / f"{variant}.template.html"
        diag_path = dest / f"{variant}.diagnostics.json"
        ir_path.write_text(json.dumps(ir, ensure_ascii=False, indent=2), encoding="utf-8")
        html_path.write_text(html, encoding="utf-8")
        diag_path.write_text(json.dumps(diag, ensure_ascii=False, indent=2), encoding="utf-8")
        out.append(
            {
                "form_id": form_id,
                "variant": variant,
                "ir": str(ir_path.relative_to(REPO_ROOT)),
                "html": str(html_path.relative_to(REPO_ROOT)),
                "diagnostics": str(diag_path.relative_to(REPO_ROOT)),
            }
        )
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="C7 FRF 후보 분류 및 IR/HTML 변환")
    parser.add_argument("--root", type=Path, default=None, help="FRF 검색 루트 (기본: Welove_인수인계)")
    parser.add_argument("--limit-per-spec", type=int, default=50)
    parser.add_argument("--convert", action="store_true", help="required label 통과 후보를 IR/HTML로 변환")
    parser.add_argument("--convert-limit", type=int, default=20)
    parser.add_argument("--audit-json", type=Path, default=REPO_ROOT / "analysis/audit/frf-template-candidates.json")
    parser.add_argument("--audit-md", type=Path, default=REPO_ROOT / "analysis/audit/frf-template-candidates.md")
    parser.add_argument("--out-dir", type=Path, default=REPO_ROOT / "debug/output/frf_c7_candidates")
    args = parser.parse_args(argv)

    root = args.root or find_handoff_root()
    entries = classify_candidates(root, limit_per_spec=args.limit_per_spec)
    write_inventory(entries, out_json=args.audit_json, out_md=args.audit_md)
    converted: list[dict[str, Any]] = []
    if args.convert:
        converted = convert_entries(entries, out_dir=args.out_dir, limit=args.convert_limit)
    print(json.dumps({"entries": len(entries), "converted": converted}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
