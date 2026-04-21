# 레거시 .frf ↔ 호출 화면/유닛 ↔ 웹 라우트 매핑

**ID**: FRF-TO-SCREEN-USAGE-MAP
**일자**: 2026-04-21
**연관 문서**: [`migration/coverage/frf-html-form-catalog.md`](./frf-html-form-catalog.md), [`docs/print-html-status.md`](../../docs/print-html-status.md), [`legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md`](../../legacy_delphi_source/legacy_source/docs/phase1-structure/11-screen-business-flows.md)
**연관 결정**: DEC-037 / DEC-038 / DEC-039 / DEC-048 / DEC-050(예정)

---

## 0. 인벤토리 방법

레거시 정본 트리(`legacy_delphi_source/legacy_source/`) 의 `*.pas` 에서 `Report\Report_X_Y.frf` 패턴을 grep 한 결과:

| 호출 유닛 | `.frf` 참조 횟수 | 비고 |
|---|---:|---|
| [`Tong04.pas`](../../legacy_delphi_source/legacy_source/Tong04.pas) | **152** | 인쇄 디스패처 — `TTong40.PrinTing00(St0,St1,...)` 단일 진입점 |
| [`Seep13.pas`](../../legacy_delphi_source/legacy_source/Seep13.pas) | 10 | 라벨 5종(`Report_1_21`~`1_25`) 디자인/인쇄 두 분기 |
| [`Subu99.pas`](../../legacy_delphi_source/legacy_source/Subu99.pas) | 2 | `Report_3_91/3_92` 자체 호출 |
| [`Subu39.pas`](../../legacy_delphi_source/legacy_source/Subu39.pas) | 2 | `Report_3_91/3_92` 자체 호출 |
| [`Seep11.pas`](../../legacy_delphi_source/legacy_source/Seep11.pas) | 2 | `Report_1_11` 두 분기 |
| [`Subu33.pas`](../../legacy_delphi_source/legacy_source/Subu33.pas) | 1 | `Report_3_33` |
| **합계 직접 호출** | **169** | |

추가로 모든 `Subu*.pas` 가 [`Tong04.pas`](../../legacy_delphi_source/legacy_source/Tong04.pas) 의 `Tong40.PrinTing00(St0,St1,...)` 헬퍼를 통해 인쇄를 위임한다 (디스패처 패턴). 디스패처 첫 인자(`St0`) 가 인쇄 도메인 코드: `'21'`, `'22'`, `'24'`, `'32'`, `'49'` 등.

레거시 정본 `.frf` 고유 ID 종류: **97종** (위 grep 결과 `sort -u | wc -l`).

---

## 1. 호출 화면 ↔ .frf 매핑 (주요 P0/P1)

운영 결합 대상 후보. **웹 라우트 = 운영 사용 중** 이면 [`migration/coverage/frf-html-form-catalog.md`](./frf-html-form-catalog.md) §5 의 `manual_in_use` 분류와 1:1 정합.

| # | 레거시 화면 | 호출 유닛 | 디스패처 코드 | `.frf` (레거시 정본) | 웹 라우트 | 운영 결합 상태 | 우선 |
|---|---|---|---|---|---|---|---|
| 1 | Sobo46 청구서출력 | [`Subu46.pas`](../../legacy_delphi_source/legacy_source/Subu46.pas) → `Tong04.Print_46_01/02` | (직접) | **`Report_4_51.frf`** (137 복제) | [`/settlement/billing/{key}/print`](도서물류관리프로그램/frontend/src/app/(app)/settlement/billing) | manual ([`settlement_print_service.py`](../../도서물류관리프로그램/backend/app/services/settlement_print_service.py)) | **P0** |
| 2 | Sobo49 세금계산서 | [`Subu49.pas`](../../legacy_delphi_source/legacy_source/Subu49.pas) → `Tong40.PrinTing00('49',...)` | `'49'` | **`Report_2_11.frf`** + `Report_2_13.frf` + `Report_2_19.frf` (210+ 복제) | [`/settlement/tax-invoice/{key}/print`](도서물류관리프로그램/frontend/src/app/(app)/settlement/tax-invoice) | manual ([`tax_invoice_service.py`](../../도서물류관리프로그램/backend/app/services/tax_invoice_service.py)) | **P0** |
| 3 | Seep13 출고/배송 라벨 | [`Seep13.pas`](../../legacy_delphi_source/legacy_source/Seep13.pas) | (직접 LoadFromFile) | **`Report_1_21~1_25.frf`** (5종) | [`/api/v1/print/label/{n}.pdf`](도서물류관리프로그램/backend/app/routers/print.py) | **`Report_1_21` 만 IR** + 4종 manual ([`label_service.py`](../../도서물류관리프로그램/backend/app/services/label_service.py)) | **P1** |
| 4 | 세금/명세 분기 (`'21'/'22'`) | 다수 `Subu*.pas` → `Tong40.PrinTing00('21'/'22',...)` | `'21'` `'22'` | `Report_2_11/2_13/2_14/2_19.frf` | (포함) tax-invoice / billing | manual | P0~P1 |
| 5 | 일별/기간 내역서 (`'24'`) | [`Subu26.pas`](../../legacy_delphi_source/legacy_source/Subu26.pas) 등 → `'24'` | `'24'` | `Report_2_41/2_42/3_11/3_12.frf` | 부분(`reports/book-sales`,`customer-sales` JSON) | partial gap | P2 |
| 6 | Tong04 정산 변형 (`Report_4_95/96`) | [`Tong04.pas`](../../legacy_delphi_source/legacy_source/Tong04.pas) ll. 538~597 | (직접) | `Report_4_95.frf` + `Report_4_96.frf` | — | gap | P2 |
| 7 | Tong04 명세 변형 (`Report_2_12`) | [`Tong04.pas`](../../legacy_delphi_source/legacy_source/Tong04.pas) ll. 2629~3028 | (직접) | `Report_2_12.frf` | — | gap | P2 |
| 8 | Tong04 통계 (`Report_3_*`) | [`Tong04.pas`](../../legacy_delphi_source/legacy_source/Tong04.pas) ll. 3064~ | (직접) | `Report_3_11/12/21/22/31~34/41/45.frf` | 부분 ([`stats/*`](도서물류관리프로그램/frontend/src/app/(app)/stats)) | partial gap | P2 |
| 9 | Subu99 발주/특수 통계 | [`Subu99.pas`](../../legacy_delphi_source/legacy_source/Subu99.pas) | (직접) | `Report_3_91/92.frf` | — | gap | P3 |
| 10 | Subu39 출고내역서 (캡션) | [`Subu39.pas`](../../legacy_delphi_source/legacy_source/Subu39.pas) | (직접) | `Report_3_91/92.frf` | — (DEC-023 으로 폼 자체는 할인율 마스터로 재용도화) | gap | P3 |
| 11 | Subu33 도서수불 | [`Subu33.pas`](../../legacy_delphi_source/legacy_source/Subu33.pas) | (직접) | `Report_3_33.frf` | [`/ledger/book*`](도서물류관리프로그램/frontend/src/app/(app)/ledger) | gap (출력만) | P3 |
| 12 | Seep11 (특수) | [`Seep11.pas`](../../legacy_delphi_source/legacy_source/Seep11.pas) | (직접) | `Report_1_11.frf` | — | gap | P3 |

---

## 2. `Report_X_Y` 정본 그룹 분류 (97 ID)

[`Tong04.pas`](../../legacy_delphi_source/legacy_source/Tong04.pas) 호출 컨텍스트 + ID prefix 기준 1차 분류 (T1 카드용 Hint, 정확한 도메인은 후속 SME 협의로 확정).

| ID prefix | 추정 도메인 | 정본 ID 수 (예시) | 운영 매핑 후보 |
|---|---|---|---|
| `Report_1_*` | 라벨/우편엽서 (5), `_11` 영수, `_40/61/62/71` 출고 | 11~ | label_service · outbound print |
| `Report_2_*` | 세금계산서/거래명세서/영수 | 16~ | tax_invoice_service · settlement_print_service |
| `Report_3_*` | 통계/현황/내역서 | 16~ | reports.py JSON (PDF 미구현) |
| `Report_4_*` | 청구서/정산 | 16~ | settlement_print_service |
| `Report_5_*` | 미정 (분석 필요) | 21~ | TBD (SME 협의) |
| `Report_6_*` | 라벨/특수 | 17~ | TBD |

전체 1744 복제 중 legacy 정본 비율은 [`migration/coverage/frf-html-form-catalog.md`](./frf-html-form-catalog.md) §2 참조 (98 파일 = 78 unique ID).

---

## 3. 우선순위 동결 (P0~P3)

| Priority | 정의 | 항목 |
|---|---|---|
| **P0** | 운영 사용 중 + 변환 자산 시각 회귀로 정합도 향상 | Sobo46 청구서(`Report_4_51`), Sobo49 세금(`Report_2_11/2_13/2_19`) |
| **P1** | 운영 부분 결합 — 화이트리스트 PR 1~4건으로 즉시 확장 | 라벨 4종 (`Report_1_22~1_25`), Seep13 직접 호출분 |
| **P2** | 미구현 운영 라우트 + 변환 자산 존재 → T1 카드부터 신설 | Tong04 `Report_4_95/96` 정산 변형, `Report_2_12` 명세 변형, `Report_3_*` 통계 |
| **P3** | 카탈로그 보존 + SME 가 정본 지정 시 승격 | WeLove_FTP 고객 복제본 1646건, Subu99/39/33/11 등 단일 호출 |

---

## 4. 게이트 메커니즘 정합

- **opt-in PR 단위**: 본 표의 우선순위는 추천이며, 운영 결합은 [`backend/app/services/print_template_registry.py`](../../도서물류관리프로그램/backend/app/services/print_template_registry.py) (예정) 화이트리스트 등록 PR 단위로만 발생.
- **품질 게이트**: [`migration/coverage/frf-html-form-catalog.md`](./frf-html-form-catalog.md) §3 의 HIGH 버킷(996건) 만 SOP-A 직행 가능. MID/LOW 는 시각 회귀 또는 SOP-B(manual) 강제.
- **DEC-039 영속**: 본 표는 매핑·우선순위만 정의. **자동 sync 코드는 작성 0** (`debug/output/frf_converted_all/` → `print_templates/auto/` 자동 복사 스크립트 금지).

---

## 5. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 1차 작성. 169 직접 호출 + 디스패처(`PrinTing00`) 경유 매핑 동결. P0 (Sobo46/49) 2건 + P1 (라벨 4종) 4건 + P2 (Tong04 변형 6건) + P3 (1646 고객 복제본 보존). |
