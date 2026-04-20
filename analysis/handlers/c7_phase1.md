# 이벤트 핸들러 · SQL 인덱스: C7 Phase 1 (라벨/송장 인쇄 — 양식 5종 + 라벨 1종)

_생성: 2026-04-20 — C7 Phase 1 T2_

> 5종 양식 (Sobo46/Sobo49/Sobo27/Sobo23/Sobo21) + 라벨 1종 (Seep13) 의 인쇄 진입점·새 엔드포인트·신규 SQL·메시지를 한 곳에 정리. 표기 규약은 `c5_phase2.md` §0 와 동일. **DEC-004 (하이브리드) / DEC-037 (WeasyPrint 단일 엔진) / DEC-038 (라벨 1종) / DEC-039 (.frf 참조용 카탈로그) 의 단일 운영 출처.**

## 0. Phase 1 진입 결정 요약

| 결정 ID | 내용 | 근거 |
| --- | --- | --- |
| DEC-037 | PDF 엔진 = WeasyPrint (Python) 단일 — A4/우편엽서 일관 | 사용자 결정 (이번 세션) |
| DEC-038 | 라벨 양식 = 1종 (Seep13 → Report_1_21.frf 등가) | 사용자 결정 (Phase 1 한정) |
| DEC-039 | `.frf` 자산 = 참조용 인벤토리만 (런타임 적재 0, 자동 변환 0) | `.frf` 가 FastReport VCL 4.x 바이너리 — Delphi/Designer 의존 |

## 1. Sobo46 — 청구서 PDF (P1-A)

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| `Button701.OnClick` (인쇄) | (Phase 2 = `window.print()`) | n/a | (재사용 SQL-ST-13/14/16) | `print_invoice_pdf` | `settlement_print_service.render_invoice_pdf_html` + `print_service.render_pdf` | `<a href="…/print.pdf" download>PDF 다운로드</a>` |
| `Button016/017Click` (일괄) | (out-of-scope) | 418/434 | — | — | — | (Phase 2) |

엔드포인트: `GET /api/v1/settlement/billing/{billing_key}/print.pdf` → 200 `application/pdf`.

## 2. Sobo49 — 세금계산서 PDF (P1-B)

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| `Button200.OnClick` (단건 인쇄) | `Button200Click` | 601 | (재사용 SQL-ST-18/19) | `print_tax_invoice_pdf` | `tax_invoice_service.render_tax_invoice_pdf_html` + `print_service.render_pdf` | `<a download>` |

엔드포인트: `GET /api/v1/settlement/tax-invoice/{billing_key}/print.pdf`.

## 3. Sobo27 — 출고 거래명세서 PDF (P1-C)

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| (행 액션) "명세서" | (Phase 2 — Subu27 Print_FormCanvas 후속) | n/a | (재사용 SQL-OUT-6) | `print_outbound_statement_pdf` | `outbound_service.render_outbound_statement_html` + `print_service.render_pdf` | `<a download>` (신규 `/print/outbound/[orderKey]`) |

엔드포인트: `GET /api/v1/print/outbound-statement/{order_key}.pdf`.

## 4. Sobo23 — 반품 영수증 PDF (P1-D)

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| (행 액션) "영수증" | (Phase 2 — `Print_*` 후속) | n/a | (재사용 SQL-RT-3~5) | `print_return_receipt_pdf` | `returns_service.render_return_receipt_html` + `print_service.render_pdf` | `<a download>` (신규 `/print/returns/[returnKey]`) |

엔드포인트: `GET /api/v1/print/return-receipt/{return_key}.pdf`.

## 5. Sobo21 — 거래명세서 PDF (P1-E)

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| (행 액션) "명세서" | (Phase 2 — `Print_*` 후속) | n/a | (재사용 SQL-INQ-2~3) | `print_sales_statement_pdf` | `transactions_service.render_sales_statement_html` + `print_service.render_pdf` | `<a download>` (신규 `/print/sales-statement/[orderKey]`) |

엔드포인트: `GET /api/v1/print/sales-statement/{order_key}.pdf`.

## 6. Seep13 — 라벨 PDF (P1-F)

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| `Button2.OnClick` (라벨 인쇄) | `Button2Click` (FastReport `LoadFromFile`+`PrintPreparedReport`) | 580 | SQL-PR-6 (신규) | `print_label_pdf` | `label_service.render_label_html` + `print_service.render_pdf` | `<a download>` (신규 `/print/label/[shipmentKey]`) |
| `Button3.OnClick` (미리보기) | (페이지 자체) | 626 | (동일) | (동일) | (동일) | 페이지 본문 |
| `Button4.OnClick` (프린터 설정) | — | 669 | — | — | — | (브라우저 다이얼로그) |
| `frDBDataSet00_01Next` (필터) | `frDBDataSet00_01Next` | 1232 | SQL-PR-6 query | (동일) | (`?include_oversea` / `?from`/`to`) | URL 쿼리 |

엔드포인트: `GET /api/v1/print/label/{shipment_key}.pdf?form=1&include_oversea=true&from=N&to=M`.

## 7. SQL 인덱스 — C7 Phase 1 신규 / 재사용

| ID | 폼 | 종류 | 테이블 | 요약 | 상태 |
| --- | --- | --- | --- | --- | --- |
| SQL-PR-1 | Sobo46 → P1-A | (재사용) | `T2_Ssub`+`T3_Ssub`+`G7_Ggeo` | SQL-ST-13/14/16 그대로 | reuse |
| SQL-PR-2 | Sobo49 → P1-B | (재사용) | `T2_Ssub`+`G7_Ggeo` | SQL-ST-18/19 그대로 | reuse |
| SQL-PR-3 | Sobo27 → P1-C | (재사용) | `S1_Ssub`+조인 | SQL-OUT-6 (`get_order_detail`) 그대로 | reuse |
| SQL-PR-4 | Sobo23 → P1-D | (재사용) | `R*_Ssub`+조인 | SQL-RT-3~5 (`get_return_detail`) 그대로 | reuse |
| SQL-PR-5 | Sobo21 → P1-E | (재사용) | `T1_Ssub`/`T1_Sub`+조인 | SQL-INQ-2~3 (`get_sales_statement_detail`) 그대로 | reuse |
| **SQL-PR-6** | Seep13 → P1-F | SELECT | `oSqry` (호출자 세팅) → 모던은 `Sg_Csum` 또는 출고/반품 detail 의 수신자 컬럼 | `SELECT Gname, Gposa, Gjice, Gadds, Gpost, Scode, Gbigo FROM Sg_Csum WHERE Skey = %s` (단건 라벨) — 호출 컨텍스트가 N건이면 N번 반복 (Phase 1) | new |

> **신규 SQL = 1건만**. 5종 양식 데이터는 100% 기존 list/detail SQL 재사용 (SRP — 빌더는 출력 변환만).

## 8. PDF 빌더 공통 규약 (`print_service.render_pdf`)

```python
# print_service.py — DEC-037 단일 엔진
async def render_pdf(html: str, *, base_url: str | None = None) -> bytes:
    """
    HTML → PDF (WeasyPrint).

    - base_url: @font-face / 이미지 경로의 기준 (기본 backend/static).
    - 반환: PDF 바이트 (`%PDF-` 시그니처 + EOF `%%EOF`).
    - graceful fallback: weasyprint 미설치 시 503 + 'PDF 엔진 미사용' (Phase 1 게이트).
    """
    try:
        from weasyprint import HTML
    except ImportError:
        raise HTTPException(503, "PDF 엔진이 설치되지 않았습니다. (DEC-037)")
    return HTML(string=html, base_url=base_url or _fonts_base()).write_pdf()
```

> 모든 5종 양식 + 라벨 = 동일 함수 호출. **양식별 분기 0** (DIP — 빌더가 HTML 만 책임).

## 9. 메시지 카탈로그 — C7 Phase 1 신규 (`i18n/messages/c7.ko.json`)

신규 파일 — C5/C6 키와 충돌 방지를 위해 prefix `c7.print.*`, `c7.label.*`, `c7.engine.*` 로 분리.

| 키 | 한글 | 비고 |
| --- | --- | --- |
| `c7.print.downloading` | "PDF 를 생성 중입니다…" | 다운로드 시작 전 토스트 |
| `c7.print.ready` | "PDF 다운로드가 시작되었습니다." | 응답 200 후 |
| `c7.print.failed` | "PDF 생성에 실패했습니다. 잠시 후 다시 시도하세요." | 5xx 응답 시 |
| `c7.print.no_data` | "인쇄할 자료가 없습니다." | 빈 detail 응답 시 placeholder PDF 안내 |
| `c7.print.preview_only_native` | "프린터 직결은 미지원입니다. 다운로드 후 시스템 인쇄를 사용하세요." | OQ-002 잔존 가시화 |
| `c7.label.single_form_only` | "Phase 1 라벨은 우편엽서 1종만 지원합니다. 다른 라벨은 후속 사이클에서 추가됩니다." | DEC-038 가시화 |
| `c7.label.postal_format` | "우편번호는 5자리 한국 우편번호 기준입니다." | Phase 1 단순화 |
| `c7.engine.unavailable` | "PDF 엔진이 설치되지 않아 미리보기로만 제공됩니다." | DEC-037 fallback (503) |
| `c7.engine.weasyprint_required` | "서버에 WeasyPrint 가 설치되지 않았습니다. 관리자에게 문의하세요." | 동일 fallback 운영자 메시지 |
| `c7.frf.reference_only` | "본 양식은 참조용 .frf 정본을 수동 재현한 결과입니다. 디자인 변경은 별도 절차를 따릅니다." | DEC-039 가시화 (PDF 워터마크 후보) |

## 10. 회귀 가드 (T7 매트릭스 5건)

- 5종 + 라벨 6 엔드포인트 × `%PDF-` 시그니처 + Content-Type = `application/pdf` 검사 (T4 `pytest -k pdf_signature`).
- 5종 × pypdf 텍스트 추출 → 헤더 거래처명/일자 등가 (T4 `pytest -k pdf_text`).
- WeasyPrint 미설치 환경 fallback 503 + 키 `c7.engine.unavailable` (T4 `pytest -k engine_fallback`).
- 마감 워터마크 (P1-A/B 한정) 2케이스 (T4 `pytest -k closed_watermark`).
- DEC-028 grep — `data-legacy-id` 가 6 엔드포인트 모두 1:1 흡수 (T7 정적 검사 1건 — `print_specs/c7_phase1.md` §8 와 동일 규약).

## 11. 참조

- 화면 카드 / 매핑 노트:
  - [`Sobo46_billing.md`](../layout_mappings/Sobo46_billing.md) §10 PDF 절
  - [`Sobo49_tax.md`](../layout_mappings/Sobo49_tax.md) §10 PDF 절
  - [`Sobo27.md`](../layout_mappings/Sobo27.md) §11 PDF 절
  - [`Sobo23.md`](../layout_mappings/Sobo23.md) §11 PDF 절
  - [`Sobo21.md`](../layout_mappings/Sobo21.md) §11 PDF 절
  - [`Seep13_label.md`](../layout_mappings/Seep13_label.md) (라벨 단일 진실원)
- 인쇄 사양: [`analysis/print_specs/c7_phase1.md`](../print_specs/c7_phase1.md)
- contract:
  - [`migration/contracts/print_invoice.yaml`](../../migration/contracts/print_invoice.yaml) v1.0.0 (T3 신설 — 5종 양식)
  - [`migration/contracts/print_label.yaml`](../../migration/contracts/print_label.yaml) v1.0.0 (T3 신설 — 라벨)
  - [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) v1.2.0 (T3 — print.pdf 2건 흡수)
- backend (T5):
  - `app/services/print_service.py` (T5a 신설 — WeasyPrint 단일 엔진)
  - `app/services/label_service.py` (T5b 신설 — Seep13 P1-F 빌더)
  - `app/routers/print.py` (T5b 신설 — 4 엔드포인트: outbound-statement / return-receipt / sales-statement / label)
  - `app/routers/settlement.py` (T5b 보강 — print.pdf 2건 추가)
  - `app/services/{outbound,returns,transactions}_service.py` (T5c — `render_*_html` 추가, 신규 SQL 0)
- frontend (T6):
  - `lib/print-api.ts` (T6a 신설 — PDF 다운로드 헬퍼)
  - 기존 `/settlement/billing/[billingKey]/print/page.tsx`, `/settlement/tax-invoice/[billingKey]/print/page.tsx` (T6a — 다운로드 버튼 추가)
  - 신규 `/print/outbound/[orderKey]/page.tsx`, `/print/returns/[returnKey]/page.tsx`, `/print/sales-statement/[orderKey]/page.tsx`, `/print/label/[shipmentKey]/page.tsx` (T6b)
- i18n: [`i18n/messages/c7.ko.json`](../../i18n/messages/c7.ko.json) (T2 신설)
- 결정: DEC-004, DEC-009, DEC-017, DEC-031, DEC-037, DEC-038, DEC-039
- 잔존 OQ: OQ-002 (프린터 직결 — Phase 1 미해소)
- 선례 핸들러: [`c5_phase2.md`](c5_phase2.md), [`c4_phase1.md`](c4_phase1.md)
