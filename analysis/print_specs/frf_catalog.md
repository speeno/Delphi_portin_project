# C7 Phase 1 — `.frf` 자산 카탈로그 (DEC-039 / T9)

본 문서는 레거시 `.frf` (FastReport VCL 4.x 바이너리) 자산을 **참조용 정본** 으로 인벤토리한다. **런타임 적재 0 / 자동 변환 0** (DEC-039) — Phase 1 의 5 양식 + 1 라벨 HTML/CSS 는 본 정본을 **수동으로 재현** 한 결과이다. 자동 파서 R&D 는 별도 작업 (T10).

## 0. 정본 위치

- **정본 (single source of truth)**: `legacy_delphi_source/legacy_source/Report/` — 98 건.
- **배포 미러 (동일 또는 구버전, 1646 건 변형 포함)**: `WeLove_FTP/book_*/AutoUpdateX/Report/` — 운영 배포 패키지의 동봉본. **인벤토리 대상에서 제외** (정본만 추적).

## 1. 인벤토리 (98 건)

### 1.1. 카테고리별 요약

| 접두어 | 건수 | 의미 (Tong04.pas / Seep13.pas 호출 기준) |
| --- | --- | --- |
| `Report_1_*` | 9 | 라벨 (Seep13) — `1_21`/`1_22`/`1_23`/`1_24`/`1_25`/`1_61`/`1_62`/`1_71`/`1_11` |
| `Report_2_*` | 12 | 거래명세서/송장 (Tong04 `Print_Sobo27/21/23/29` 류) |
| `Report_3_*` | 14 | 발주/입고 (Tong04 `Print_Subu13/12/...`) |
| `Report_4_*` | 16 | 출고/주문 (Tong04 `Print_Subu27/22/41/...`) |
| `Report_5_*` | 16 | 정산/청구 (Tong04 `Print_Subu46/45/41/...`) |
| `Report_6_*` | 30 | 통계/현황 (Tong04 `Print_Subu61~99/...`) |
| `계산서.frf` | 1 | 세금계산서 (Sobo49 — `Tong60.frReport49_*.LoadFromFile`) |
| **합계** | **98** | |

### 1.2. 전체 정본 목록 (sort)

```
Report_1_11.frf
Report_1_21.frf      ← C7 Phase 1 P1-F (라벨 form=1, 우편엽서)
Report_1_22.frf
Report_1_23.frf
Report_1_24.frf
Report_1_25.frf
Report_1_61.frf
Report_1_62.frf
Report_1_71.frf
Report_2_11-.frf
Report_2_12.frf
Report_2_13-1.frf
Report_2_13-2.frf
Report_2_13-3.frf
Report_2_13-5.frf
Report_2_13.frf
Report_2_14.frf
Report_2_19.frf
Report_2_41.frf
Report_2_46.frf
Report_2_51.frf
Report_3_11.frf
Report_3_12.frf
Report_3_21.frf
Report_3_22.frf
Report_3_31.frf
Report_3_32.frf
Report_3_41.frf
Report_3_42.frf
Report_3_43.frf
Report_3_44.frf
Report_3_45.frf
Report_3_91-1.frf
Report_3_91.frf
Report_3_92.frf
Report_4_11.frf
Report_4_21.frf
Report_4_31.frf
Report_4_41.frf
Report_4_51-0.frf
Report_4_51-1.frf
Report_4_51-2.frf
Report_4_51-3.frf
Report_4_51-4.frf
Report_4_51-5.frf
Report_4_51-6.frf
Report_4_51-7.frf
Report_4_51-8.frf
Report_4_51-9.frf
Report_4_51.frf
Report_4_52.frf
Report_4_71.frf
Report_4_94.frf
Report_4_96.frf
Report_5_21.frf
Report_5_31.frf
Report_5_32.frf
Report_5_41.frf
Report_5_42.frf
Report_5_51.frf
Report_5_52.frf
Report_5_53.frf
Report_5_54.frf
Report_5_61.frf
Report_5_62.frf
Report_5_63.frf
Report_5_64.frf
Report_5_71.frf
Report_5_72.frf
Report_5_81.frf
Report_5_82.frf
Report_5_91.frf
Report_5_92.frf
Report_6_11.frf
Report_6_12.frf
Report_6_21.frf
Report_6_22.frf
Report_6_31.frf
Report_6_32.frf
Report_6_41.frf
Report_6_42.frf
Report_6_51-.frf
Report_6_51.frf
Report_6_52-.frf
Report_6_52.frf
Report_6_61-.frf
Report_6_61.frf
Report_6_62-.frf
Report_6_62.frf
Report_6_71.frf
Report_6_72.frf
Report_6_81.frf
Report_6_82.frf
Report_6_91.frf
Report_6_92.frf
Report_6_93.frf
Report_6_99.frf
계산서.frf            ← C7 Phase 1 P1-B (세금계산서 — Sobo49)
```

전체 98 건 (`find legacy_delphi_source/legacy_source/Report -name '*.frf' -type f | wc -l == 98` 검증).

## 2. C7 Phase 1 5 양식 + 1 라벨 ↔ `.frf` 매핑

> **명명 가이드 (혼동 방지)**: 화면(Sobo*)과 `.frf` 번호는 **1:1 이 아니다**. 청구서(Sobo46) ↔ `Report_5_61/62`, 출고 거래명세(Sobo27) ↔ `Report_4_51*`, 반품 영수증(Sobo23) ↔ `Report_2_13*`, 거래명세(Sobo21) ↔ `Report_2_11*`, 세금계산서(Sobo49) ↔ `계산서.frf`, 라벨(Seep13) ↔ `Report_1_21~25`. 매핑은 본 §2 표가 단일 정본 — 「Report 번호 = Sobo 번호」 같은 직관적 추정 금지.

| Form ID | Sobo/Seep | `.frf` 정본 (수동 재현 대상) | 참조 호출 (.pas) | HTML/CSS 빌더 (모던) |
| --- | --- | --- | --- | --- |
| **P1-A** 청구서 | Sobo46 | `Report_5_61.frf` (월별 청구) + `Report_5_62.frf` (월별 청구 상세) | `Tong04.pas Print_Subu46` (추정 — `Tong60.frReport46_*`) | `app/services/settlement_print_service.py::render_invoice_pdf_html` |
| **P1-B** 세금계산서 | Sobo49 | `계산서.frf` | `Tong04.pas` (Subu49 호출) | `app/services/tax_invoice_service.py::render_tax_invoice_pdf_html` |
| **P1-C** 출고 거래명세서 | Sobo27 | `Report_4_51.frf` 또는 `Report_4_51-{0~9}.frf` (10 변형 — 거래처별 양식) | `Tong04.pas Print_Subu27 / Print_Sobo27` | `app/services/outbound_service.py::render_outbound_statement_html` |
| **P1-D** 반품 영수증 | Sobo23 | `Report_2_13.frf` 또는 `Report_2_13-{1,2,3,5}.frf` (4 변형 — 거래처별 양식) | `Tong04.pas Print_Sobo23` | `app/services/returns_service.py::render_return_receipt_html` |
| **P1-E** 거래명세서 | Sobo21 | `Report_2_11.frf` 또는 `Report_2_11-.frf` | `Tong04.pas Print_Sobo21` (L232/253) | `app/services/transactions_service.py::render_sales_statement_html` |
| **P1-F** 라벨 (우편엽서) | Seep13 form=1 | `Report_1_21.frf` | `Seep13.pas frReport00_01.LoadFromFile(Edits[1].Text)` | `app/services/label_service.py::render_label_html` |

### 2.1. Phase 1 변형 (`*-N.frf`) 처리 정책

- **P1-C 의 `Report_4_51-{0~9}.frf`** (10 변형) 와 **P1-D 의 `Report_2_13-{1,2,3,5}.frf`** (4 변형) 은 거래처별 양식 변형. Phase 1 = **기본 양식 1 종 (`-` 접미사 없는 정본) 만 수동 재현**. 거래처별 차이는 `migration/contracts/print_invoice.yaml customer_variants` 에 항목별 diff 로 기록 (Phase 2 이후).
- **P1-F 의 라벨 form 2~5** (`Report_1_22~25.frf`) 는 **out-of-scope (DEC-038)**. `?form=1` 고정.

### 2.2. Phase 1 비대상 (96 건 중 92 건은 모두 다른 시나리오 / 후속 페이즈)

- **C8 바코드 (Report_1_11/61/62/71)**: 라벨 캔버스 — 후속 시나리오.
- **C3 입고/발주 (Report_3_*)**: C3 페이즈에서 별도 인쇄 추가 시.
- **C6/C9 통계 (Report_5_*/6_*)**: 정산/통계/현황 인쇄 — Phase 2 이후.

## 3. 자동 변환 정책 (DEC-039 재확인)

- **런타임 적재 0**: 모던 백엔드는 `.frf` 파일을 **읽지 않는다**. 모든 PDF 생성은 Python HTML 빌더 → WeasyPrint (DEC-037) 한 경로로만 흐른다.
- **자동 변환 0**: `.frf` → HTML/CSS 자동 변환기 **금지**. 모든 양식은 정본을 **수동으로 재현** 한 결과 (디자인 책임 = 개발자).
- **푸터 안내**: PDF 푸터에 "본 양식은 참조용 .frf 정본 (`<frf 파일명>`) 을 수동 재현한 결과" 메시지 부착 (i18n `c7.frf.reference_only`).
- **R&D 분리 (T10)**: FastReport VCL 4.x OSS 파서 분석 → 자체 구현 가능성 리서치 보고서 (`analysis/research/c7_frf_parser_oss_research.md`) 산출. 자동 변환 가능성 재검토 후 후속 페이즈 적용 여부 결정.

## 4. 회귀 가드

- 본 카탈로그 누락 0 건 검증: `find legacy_delphi_source/legacy_source/Report -name '*.frf' -type f | wc -l == 98`.
- C7 Phase 1 5 양식 + 1 라벨 매핑 표 (§2) 의 `.frf` 정본이 모두 §1.2 목록에 존재.
- `print_service.py` 가 `.frf` 파일을 읽지 않음 (코드 grep — `.frf` 문자열 0 건).

## 5. 후속 작업 트리거

- **Phase 2** 진입 시: `Report_4_51-N` / `Report_2_13-N` 변형 정본을 `customer_variants` 에 흡수.
- **T10 OSS 파서 R&D** 결과 = 가능 → Phase 3 에서 일괄 자동 변환 정책 검토.
- **새 인쇄 양식 요구** 시: 본 카탈로그를 갱신하고 새 row 를 §2 매핑 표에 추가.

## 참조

- `legacy-analysis/decisions.md` DEC-039 (`.frf` 정본 = 참조용)
- `analysis/print_specs/c7_phase1.md` (5 양식 + 1 라벨 인쇄 사양)
- `analysis/research/c7_frf_parser_oss_research.md` (T10 — 파서 R&D, 별도 작업)
- 정본: `legacy_delphi_source/legacy_source/Report/`
