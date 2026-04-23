#!/usr/bin/env python3
"""레거시 DFM Caption ↔ 모던 form-registry 동등성 매트릭스 생성기 (DEC-061).

입력:
  - ``legacy_delphi_source/legacy_source/*.dfm`` (루트 ``object Sobo*:`` + ``Caption``)
  - ``도서물류관리프로그램/frontend/src/lib/form-registry.ts``

출력:
  - ``docs/delphi-form-screen-equivalence-matrix.md`` — 인간용 표 (항상 참고)
  - ``analysis/audit/delphi-form-screen-matrix.json`` — 도구용

사용:
  python3 tools/delphi_form_screen_matrix.py              # 두 파일 갱신
  python3 tools/delphi_form_screen_matrix.py --check      # 등록된 ``Subu*`` 폴더에 DFM 파일 없으면 실패
  python3 tools/delphi_form_screen_matrix.py --strict     # 위 + 단일 매핑 제목 불일치(CAPTION_DIFF) 도 실패

포팅 파이프라인: 포팅/검증 사이클 시작 시 본 스크립트 실행 → 표 갱신 후 차이 검토.
제목 동등성은 표에서 항상 확인 가능. CI 기본은 **DFM 존재**만 게이트; 제목까지 게이트하려면 ``--strict``.
재발 방지는 ``legacy-analysis/decisions.md`` DEC-060·DEC-061 과 짝을 이룸.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LEGACY_DFM_ROOT = ROOT / "legacy_delphi_source" / "legacy_source"
FORM_REGISTRY_TS = ROOT / "도서물류관리프로그램" / "frontend" / "src" / "lib" / "form-registry.ts"
OUT_MD = ROOT / "docs" / "delphi-form-screen-equivalence-matrix.md"
OUT_JSON = ROOT / "analysis" / "audit" / "delphi-form-screen-matrix.json"

# Interbase/Data/version/복사본 등 비주류 DFM 스캔 제외 (주 소스 트리만)
SKIP_SUBPATH_PARTS = frozenset({"Interbase", "Data", "version"})


def _decode_dfm_caption_fragment(raw: str) -> str:
    """DFM 문자열 리터럴 내용(raw, 작은따옴표 안)을 UTF-8 문자열로."""
    if not raw:
        return ""
    # Delphi #13#10 등 → 줄바꿈 치환 (표시 단순화)
    tmp = raw
    tmp = re.sub(r"#(\d+)", lambda m: chr(int(m.group(1))), tmp)

    raw_b = raw.encode("latin1", errors="surrogateescape")
    for enc in ("euc-kr", "cp949"):
        try:
            return raw_b.decode(enc)
        except UnicodeDecodeError:
            continue
    try:
        return raw_b.decode("utf-8")
    except UnicodeDecodeError:
        return raw


def extract_root_form_and_caption(dfm_path: Path) -> tuple[str | None, str]:
    """첫 번째 폼 객체 이름(Sobo*)와 루트 Caption."""
    data = dfm_path.read_bytes()
    # 헤더 ~500줄 내 루트 폼 검색 (대형 DFM 회피)
    head = data[: min(len(data), 400_000)]
    text = head.decode("latin1", errors="replace")

    m_obj = re.search(r"(?im)^object\s+(Sobo\S+)\s*:\s*T\S+", text)
    form_name = m_obj.group(1) if m_obj else None

    m_cap = re.search(r"(?im)^\s*Caption\s*=\s*'((?:[^'\\]|\\.|'')*)'", text)
    if not m_cap:
        return form_name, ""
    inner = m_cap.group(1).replace("''", "'")
    caption = _decode_dfm_caption_fragment(inner)
    return form_name, caption.strip()


def _skip_path(p: Path) -> bool:
    parts = set(p.parts)
    return bool(parts & SKIP_SUBPATH_PARTS) or "복사본" in p.name


def scan_legacy_dfms() -> dict[str, dict]:
    """키 = dfm 스템 (예: Subu45_1). 값 = form_object, caption_utf8, path."""
    inv: dict[str, dict] = {}
    for dfm in sorted(LEGACY_DFM_ROOT.rglob("*.dfm")):
        if _skip_path(dfm):
            continue
        stem = dfm.stem
        if not stem.startswith("Subu"):
            continue
        form_obj, cap = extract_root_form_and_caption(dfm)
        inv[stem] = {
            "dfm_path": str(dfm.relative_to(ROOT)),
            "form_object": form_obj or "",
            "caption": cap,
        }
    return inv


def extract_braced_object(src: str, start_i: int) -> tuple[str, int]:
    """src[start_i] == '{'. 최상위 객체 문자열과 종료 인덱스(다음 문자) 반환."""
    assert src[start_i] == "{"
    depth = 0
    i = start_i
    in_str = False
    escape = False
    quote = ""
    n = len(src)
    while i < n:
        c = src[i]
        if not in_str:
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return src[start_i : i + 1], i + 1
        if not in_str and c in "\"'":
            in_str = True
            quote = c
            escape = False
            i += 1
            continue
        if in_str:
            if escape:
                escape = False
            elif c == "\\":
                escape = True
            elif c == quote:
                in_str = False
            i += 1
            continue
        i += 1
    raise ValueError("unbalanced brace in FORM_REGISTRY")


def parse_ts_flat_fields(obj_src: str) -> dict[str, str]:
    """최상위 `id` / `folder` / `caption` / `route` 만 (시나리오 중첩 제외)."""
    out: dict[str, str] = {}
    for line in obj_src.splitlines():
        line = line.strip()
        for key in ("id", "folder", "caption", "route"):
            prefix = f"{key}:"
            if line.startswith(prefix):
                rest = line[len(prefix) :].strip()
                m = re.match(r'^"([^"]*)"(?:,)?$', rest)
                if m:
                    out[key] = m.group(1)
    return out


def parse_form_registry_entries(ts_path: Path) -> list[dict[str, str]]:
    text = ts_path.read_text(encoding="utf-8")
    marker = "export const FORM_REGISTRY: FormMeta[] = ["
    pos = text.index(marker) + len(marker)
    entries: list[dict[str, str]] = []
    i = pos
    n = len(text)
    while i < n:
        while i < n and text[i] in " \t\r\n":
            i += 1
        if i >= n:
            break
        if text[i] == "]":
            break
        if text.startswith("//", i):
            while i < n and text[i] != "\n":
                i += 1
            continue
        if text[i] == ",":
            i += 1
            continue
        if text[i] != "{":
            i += 1
            continue
        try:
            obj_src, i = extract_braced_object(text, i)
        except ValueError:
            break
        fields = parse_ts_flat_fields(obj_src)
        if fields.get("id") and fields.get("folder") and fields.get("caption"):
            entries.append(fields)
    return entries


def normalize(s: str) -> str:
    return re.sub(r"\s+", "", s or "")


# 모던 표시명이 레거시와 의도적으로 다른 경우 (수동 allowlist)
CAPTION_ALLOWLIST_MISMATCH: frozenset[tuple[str, str, str]] = frozenset(
    {
        ("Subu11", "거래처관리-통합", "거래처관리(마스터)"),
        ("Subu14", "도서관리-통합", "도서관리(마스터)"),
        ("Subu14", "도서관리", "도서관리(마스터)"),
        ("Subu17", "출판사관리", "출판사·출고거래처(마스터)"),
    }
)

# 제목 유사도(0~1) — 이상이면 NEAR_MATCH 로 보고 --check 기본 통과
CAPTION_SIMILARITY_OK = 0.78


def _caption_ratio(a: str, b: str) -> float:
    a, b = normalize(a), normalize(b)
    if not a and not b:
        return 1.0
    return difflib.SequenceMatcher(None, a, b).ratio()


def is_web_only_folder(folder: str) -> bool:
    return folder.startswith("_")


PLACEHOLDER_CAPTION_RE = re.compile(r"^Sobo\d+[A-Za-z\d_]*$")


def is_placeholder_legacy_caption(caption: str) -> bool:
    """Subu38 등 빈 껍데기 폼은 Caption 이 식별자 그대로인 경우가 있음."""
    c = caption.strip()
    return bool(c and PLACEHOLDER_CAPTION_RE.match(c))


def classify_row(
    folder: str,
    modern_caption: str,
    leg: dict | None,
    *,
    folder_entry_count: int,
) -> tuple[str, str]:
    """(status, note).

    MULTI_MAP: 동일 Subu 폴더에 복수 모던 메타(파생 라우트) — 루트 DFM Caption 과
    모던 표기가 어긋나는 것이 정상일 수 있음 (--check 에서 제외).
    """
    if is_web_only_folder(folder):
        return "WEB_ONLY", "Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1)"
    if not leg or not leg.get("caption"):
        return "LEGACY_MISSING", f"DFM `{folder}.dfm` 없음 또는 루트 Caption 추출 실패"
    lc = leg["caption"].strip()
    mc = modern_caption.strip()

    if folder_entry_count > 1:
        return (
            "MULTI_MAP",
            "동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019)",
        )

    if is_placeholder_legacy_caption(lc):
        return (
            "DFM_PLACEHOLDER",
            f"루트 Caption 이 식별자 수준「{lc}」— 실제 화면은 변형 폴더·주 폼 참조",
        )

    if normalize(lc) == normalize(mc):
        return "MATCH", ""
    if (folder, lc, mc) in CAPTION_ALLOWLIST_MISMATCH:
        return "OK_EXEMPT", "DEC-023 표기 통일(allowlist)"
    r = _caption_ratio(lc, mc)
    if r >= CAPTION_SIMILARITY_OK:
        return "NEAR_MATCH", f"유사도 {r:.2f} (≥{CAPTION_SIMILARITY_OK})"
    if lc in mc or mc in lc:
        return "CAPTION_DIFF", f"포함 관계·수동검토: DFM「{lc}」↔「{mc}」 (r={r:.2f})"
    return "CAPTION_DIFF", f"DFM「{lc}」↔모던「{mc}」 (r={r:.2f})"


def build_rows(
    legacy: dict[str, dict], modern: list[dict[str, str]]
) -> list[dict]:
    rows: list[dict] = []
    folder_counts = Counter(mm["folder"] for mm in modern)
    for m in modern:
        folder = m["folder"]
        leg = legacy.get(folder)
        st, note = classify_row(
            folder,
            m["caption"],
            leg,
            folder_entry_count=folder_counts[folder],
        )
        rows.append(
            {
                "modern_id": m["id"],
                "folder": folder,
                "route": m.get("route", ""),
                "modern_caption": m["caption"],
                "legacy_form_object": (leg or {}).get("form_object", ""),
                "legacy_caption": (leg or {}).get("caption", ""),
                "legacy_dfm": (leg or {}).get("dfm_path", ""),
                "status": st,
                "note": note,
            }
        )
    # 레거시만 있고 레지스트리에 없는 폴더 (참고용)
    used_folders = {m["folder"] for m in modern}
    orphan = []
    for stem, info in legacy.items():
        if stem not in used_folders:
            orphan.append({"folder": stem, **info})
    return rows, orphan


def write_markdown(rows: list[dict], orphans: list[dict], ts_path: Path) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        "# 델파이 폼 ↔ 모던 화면 동등성 매트릭스",
        "",
        "> **자동 생성** — `python3 tools/delphi_form_screen_matrix.py` 로 갱신. 직접 편집하지 마세요.",
        f"> **생성 시각 (UTC)**: {now}",
        "",
        "## 목적",
        "",
        "- 레거시 `Subu*.dfm` 루트 **Caption** 과 모던 `form-registry.ts` 의 **caption** 을 나란히 두어,",
        "  포팅 시 **제목 불일치·폴더 오매칭**(예: DEC-060 사례) 재발을 방지한다.",
        "- **동등성**: 문자열이 완전히 같으면 `MATCH`. 의도적 표기 차이는 코드 내 allowlist + 본 표 `note` 로 관리한다.",
        "",
        "## 파이프라인에서의 위치",
        "",
        "1. 화면 포팅/계약 수정 전: `python3 tools/delphi_form_screen_matrix.py` 실행 → 본 문서·JSON 갱신.",
        "2. `status` 가 `CAPTION_DIFF` 인 행을 우선 검토 — DFM Caption 재확인 (`iconv -f EUC-KR -t UTF-8 Subu*.dfm`).",
        "3. CI/로컬 체크: `python3 tools/delphi_form_screen_matrix.py --check` — 등록된 **`Subu*`** 폴더에 대응 `Subu*.dfm` 이 없으면 실패. 제목 불일치까지 게이트하려면 `--strict` (단일 매핑 `CAPTION_DIFF` 포함). `WEB_ONLY`(`_WebAdm`) 는 제외.",
        "",
        "## 표 — form-registry 등록 화면 (폴더 = DFM 스템)",
        "",
        "| 상태 | 모던 ID | 폴더(DFM) | 모던 caption | 레거시 Caption (DFM) | 레거시 폼 객체 | 라우트 | 비고 |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in sorted(rows, key=lambda x: (x["folder"], x["modern_id"])):
        lines.append(
            f"| {r['status']} | `{r['modern_id']}` | `{r['folder']}` | {r['modern_caption']} | "
            f"{r['legacy_caption'] or '—'} | `{r['legacy_form_object'] or '—'}` | "
            f"`{r['route'] or '—'}` | {r['note']} |"
        )
    lines.extend(
        [
            "",
            "## 참고 — 레지스트리 미등록 DFM (주 트리만)",
            "",
            "아래는 `legacy_source` 에 존재하나 현재 `FORM_REGISTRY` 에 `folder` 가 없는 스템입니다.",
            "신규 포팅 후보이거나 통계/분기 전용일 수 있습니다.",
            "",
            "| DFM 스템 | 레거시 Caption | 경로 |",
            "| --- | --- | --- |",
        ]
    )
    for o in sorted(orphans, key=lambda x: x["folder"])[:80]:
        lines.append(
            f"| `{o['folder']}` | {o.get('caption', '')} | `{o.get('dfm_path', '')}` |"
        )
    if len(orphans) > 80:
        lines.append(f"| … | ({len(orphans) - 80}건 생략) | |")
    lines.extend(
        [
            "",
            "## 관련 결정·규칙",
            "",
            "- **DEC-060**: DFM Caption 대조 게이트 — 테이블 컬럼만으로 폼 의미 추정 금지.",
            "- **DEC-023**: 마스터 단일 원천 — 모던 caption 의 `(마스터)` 등 접미는 레거시와 다를 수 있음 (allowlist).",
            "",
            f"- 소스: `{ts_path.relative_to(ROOT)}`",
            f"- DFM 루트: `{LEGACY_DFM_ROOT.relative_to(ROOT)}/Subu*.dfm`",
        ]
    )
    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(payload: dict) -> None:
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="Delphi DFM ↔ form-registry matrix")
    ap.add_argument(
        "--check",
        action="store_true",
        help="Subu* 레거시 폴더에 dfm 없으면 종료 코드 1",
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="--check 에 더해 단일 매핑 CAPTION_DIFF 도 종료 코드 1",
    )
    args = ap.parse_args()
    if args.strict:
        args.check = True

    if not FORM_REGISTRY_TS.is_file():
        print("ERROR: form-registry.ts not found", file=sys.stderr)
        return 2

    legacy = scan_legacy_dfms()
    modern = parse_form_registry_entries(FORM_REGISTRY_TS)
    rows, orphans = build_rows(legacy, modern)

    # --check: Subu* 트랙에서 DFM 누락 또는 심한 제목 불일치만 실패
    subu_missing = [
        r
        for r in rows
        if r["folder"].startswith("Subu") and r["status"] == "LEGACY_MISSING"
    ]
    subu_diff = [
        r
        for r in rows
        if r["folder"].startswith("Subu")
        and r["status"] == "CAPTION_DIFF"
    ]
    check_fail = list(subu_missing)
    if args.strict:
        check_fail = subu_missing + subu_diff

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "summary": {
            "registry_forms": len(rows),
            "legacy_dfm_subu_stems": len(legacy),
            "orphan_legacy_stems": len(orphans),
            "subu_caption_diff": len(subu_diff),
            "subu_legacy_missing": len(subu_missing),
        },
        "rows": rows,
        "orphans_sample": orphans[:200],
    }
    write_json(payload)
    write_markdown(rows, orphans, FORM_REGISTRY_TS)

    print(
        f"[delphi_form_screen_matrix] rows={len(rows)} orphans={len(orphans)} "
        f"subu_diff={len(subu_diff)} subu_missing={len(subu_missing)} → {OUT_MD.relative_to(ROOT)}"
    )
    if args.check and check_fail:
        msg = (
            "FAIL — Subu* legacy DFM missing (--check)"
            if not args.strict
            else "FAIL — Subu* DFM missing or single-map CAPTION_DIFF (--check --strict)"
        )
        print(msg, file=sys.stderr)
        for r in check_fail[:50]:
            print(
                f"  {r['modern_id']} ({r['folder']}): {r['status']} — {r['note']}",
                file=sys.stderr,
            )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
