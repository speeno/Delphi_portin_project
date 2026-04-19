# 화면 카드: C5 정산 통합 (Sobo45/45_1/47/41/42/42_1/46/49)

_생성: 2026-04-19 — C5 Phase 1 T1 매핑 노트 동반_
_갱신: 2026-04-19 — C5 Phase 2 T1 (Sobo46/49 + 재집계 + audit 회전 UI)_

> **C5 통합 카드** — 청구서관리(Sobo45) / 청구금액 년월(Sobo47) / 입금내역(Sobo41) / 입금현황(Sobo42, Sobo42_1) / 청구서관리 택배(Sobo45_1) 6개 폼을 Phase 1 로, 청구서출력(Sobo46) / 세금계산서발행(Sobo49) 2개 폼을 Phase 2 로 단일 시나리오에 통합. 폼별 위젯·이벤트 1:1 매핑은 [`analysis/layout_mappings/Sobo*_billing.md`](../layout_mappings/) / [`Sobo*_cash.md`](../layout_mappings/) / [`Sobo*_tax.md`](../layout_mappings/) 참조. 폼별 자동 생성 카드(`Sobo45.md` 등)는 정적 분석 보존용 — 본 카드는 포팅 컨텍스트.

## 0. 한눈 요약

- 매핑 시나리오: **C5 정산 (일·월 마감)**
- Phase 분할: Phase 1 = 청구·집계·입금 + 마감 가드 (45/45_1/47/41/42/42_1) / **Phase 2 = 청구서출력(46)·세금계산서(49)·재집계 잡·audit 회전 UI** (본 카드 §10 참조)
- 핵심 테이블: `T2_Ssub` (청구 헤더·집계), `T3_Ssub` (청구 상세), `T5_Ssub` (입금), `Sv_Ghng` (변동 트리거), `G7_Ggeo` (거래처)
- 마감 정책: `T2_Ssub.Yesno='1'` 분기 보존 (DEC-031, **이번 세션 결정**) — `application_settings.settlement.close_until` 키 미도입
- 패스워드 게이팅: DEC-029 `AuditPasswordModal` (scope=`settlement_confirm`, `gpass_change`)

## 1. 폼별 1줄 요약

| 폼 | 캡션 | 핵심 SQL | 모던 라우트 | 매핑 노트 | 자동 생성 카드 |
| --- | --- | --- | --- | --- | --- |
| Sobo45 | 청구서관리 | `INSERT/UPDATE T2_Ssub` 다수 (≈2644~2971), `Yesno='1'` 마감 분기 (840·979·1051) | `/settlement/billing` | [`Sobo45_billing.md`](../layout_mappings/Sobo45_billing.md) | [`Sobo45.md`](Sobo45.md) |
| Sobo45_1 | 청구서관리 — 택배 | 동상 (변형) — `nForm='45_1'`, 컬럼 5~7 택배비 大/中/小 | `/settlement/billing?variant=takbae` | [`Sobo45_1_billing.md`](../layout_mappings/Sobo45_1_billing.md) | [`Sobo45_1.md`](Sobo45_1.md) |
| Sobo47 | 청구금액(년월) | `Select Gdate, Sum(Sum26..28) From T2_Ssub Group By Gdate` (271~316) | `/settlement/period` | [`Sobo47_billing.md`](../layout_mappings/Sobo47_billing.md) | [`Sobo47.md`](Sobo47.md) |
| Sobo41 | 입금내역 | `Select * From T5_Ssub` + `INSERT/UPDATE T5_Ssub` (DataModule 위임 → 모던 직접 SQL) | `/settlement/cash` | [`Sobo41_cash.md`](../layout_mappings/Sobo41_cash.md) | [`Sobo41.md`](Sobo41.md) |
| Sobo42 | 입금현황(거래처별) | `Select Hcode, Sum(Sum26..28) From T2_Ssub Group By Hcode` (≈278) | `/settlement/cash-status?variant=hcode` | [`Sobo42_cash.md`](../layout_mappings/Sobo42_cash.md) | [`Sobo42.md`](Sobo42.md) |
| Sobo42_1 | 입금현황(년월별) | 동상 (변형) — `Group By Gdate`, `GPSUM` 컬럼 추가 | `/settlement/cash-status?variant=sdate` | [`Sobo42_1_cash.md`](../layout_mappings/Sobo42_1_cash.md) | [`Sobo42_1.md`](Sobo42_1.md) |
| Sobo46 | **청구서출력 [Phase 2]** | `SELECT Sum01..Sum69, T3_Ssub 라인 FROM T2_Ssub/T3_Ssub WHERE 월키` (485~736) | `/settlement/billing/[billingKey]/print` | [`Sobo46_billing.md`](../layout_mappings/Sobo46_billing.md) | [`Sobo46.md`](Sobo46.md) |
| Sobo49 | **세금계산서발행 [Phase 2]** | `SELECT/UPDATE T2_Ssub.Chek3,Sdate WHERE Gdate,Hcode` (327~773) | `/settlement/tax-invoice` + `/[billingKey]/print` | [`Sobo49_tax.md`](../layout_mappings/Sobo49_tax.md) | [`Sobo49.md`](Sobo49.md) |

## 2. UI 구성 (영역 패턴)

모든 폼이 **상단 검색 패널 + 중단 그리드(+선택적 하단 입력 패널) + 푸터 액션** 4영역 패턴을 공유. 변형은 데이터셋 위치(전역 DataModule vs 폼 로컬 ClientDataSet) 와 컬럼 의미 차이만 가짐 — 위젯 ID 자체는 거의 동일.

| 영역 | 공통 dfm 컨테이너 | 모던 매핑 패턴 |
| --- | --- | --- |
| 상단 검색 | `Panel001` (TFlatPanel, TabOrder 0) | `<section>` + 거래처 + 일자/년월 + 조회 버튼 |
| 중단 그리드 | `Panel002` 내 `DBGrid101` 또는 `DBGrid201` | `<DataGrid>` (DataGridPager) |
| 하단 입력 | `Panel003` (있는 폼만 — Sobo41) | 우측 슬라이드 폼 또는 모달 |
| 푸터 액션 | Button701/702 (인쇄/마감) | 헤더 액션 버튼 (Phase 1 = 마감/취소) |

## 3. 이벤트 흐름 — C5 공통

| dfm 이벤트 | 모던 핸들러 | 비고 |
| --- | --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → `useDynamicPageSize` → `load()` | C6 패턴 재사용 |
| `Button101Click` (조회) | `onSearch` → `settlementApi.<method>()` | 모든 폼 공통 |
| `Button700/701Click` (저장/취소) | `onSave` / `onReset` | Sobo41 입력 패널 |
| `Button702Click` (마감) | `onConfirmClose` → `AuditPasswordModal` (scope=`settlement_confirm`) | DEC-029 게이팅 |
| `DBGrid201Columns10UpdateData` | 라인 셀 편집 → `settlementApi.upsertLine()` | Sobo45 청구 라인 |
| `Button004Click` (Subu45.pas 372~381) | `AuditPasswordModal` rotate 액션 | DEC-032 — InputBox 평문 폐기 |

## 4. 데이터 액세스 (SQL 인덱스 — Phase 1 핵심)

| ID | 폼 | 종류 | 테이블 | 요약 |
| --- | --- | --- | --- | --- |
| SQL-ST-1 | Sobo45 | INSERT/UPDATE | `T2_Ssub` | 청구 헤더 UPSERT (월키, hcode) |
| SQL-ST-2 | Sobo45 | INSERT/UPDATE | `T3_Ssub` | 청구 상세 라인 UPSERT |
| SQL-ST-3 | Sobo45 | UPDATE | `T2_Ssub.Yesno` | 마감 확정 `Yesno='1'` (audit_token 필요) |
| SQL-ST-4 | Sobo45 | UPDATE | `T2_Ssub.Yesno` | 소프트 취소 `Yesno='2'` (DEC-012) |
| SQL-ST-5 | Sobo45 | UPDATE | `Sv_Ghng` | `_Sv_Ghng_` 트리거 (Tong40, 3282~3304) |
| SQL-ST-6 | Sobo47 | SELECT | `T2_Ssub` | `Group By Gdate` 월합계 |
| SQL-ST-7 | Sobo41 | SELECT | `T5_Ssub` ⨝ `G7_Ggeo` | 입금 내역 조회 |
| SQL-ST-8 | Sobo41 | INSERT | `T5_Ssub` | 입금 신규 |
| SQL-ST-9 | Sobo41 | UPDATE | `T5_Ssub` | 입금 수정 |
| SQL-ST-10 | Sobo42 | SELECT | `T2_Ssub` ⨝ `T5_Ssub` | 거래처별 입금현황 (`Group By Hcode`) |
| SQL-ST-11 | Sobo42_1 | SELECT | `T2_Ssub` ⨝ `T5_Ssub` | 년월별 입금현황 (`Group By Gdate`, GPSUM 추가) |
| SQL-ST-12 | Sobo45 | UPDATE | `Id_Logn.Gpass` | (DEC-032: AuditPasswordModal rotate 로 이관) |
| SQL-ST-13 | Sobo46 | SELECT | `T2_Ssub` (1행) | 청구 헤더 67 합계 (Sum01~Sum69 + Gsusu/Vdate/Bigo*) |
| SQL-ST-14 | Sobo46 | SELECT | `T3_Ssub` (≤31) | 일별 라인 16컬럼 (GDATE/GQUT1~7/NAME1/NAME2/GNAME/GCODE/GSQUT/GSSUM/YESNO) |
| SQL-ST-15 | Sobo46 | SELECT | `T2_Ssub` ⨝ `G7_Ggeo` | 거래처 검색 (월/하코드/Bcode='완료'/Yesno='O') |
| SQL-ST-16 | Sobo46 | SELECT (lookup) | `G7_Ggeo` | `Seek_Ggeo`/`Seek_Name` (거래처명·주소) |
| SQL-ST-17 | Sobo46 | SELECT | `T2_Ssub` (조회월 콤보) | `FormShow` 콤보 채움 |
| SQL-ST-18 | Sobo49 | SELECT | `T2_Ssub` | 월/거래처 발행대상 (`Sum27<>0`, `Hcode,Sum26,Sum27,Sum28,Chek3,Sdate`) |
| SQL-ST-19 | Sobo49 | SELECT (lookup) | `G7_Ggeo` | 거래처명 보강 |
| SQL-ST-20 | Sobo49 | UPDATE | `T2_Ssub.Chek3` | **Chek3 토글 — 단건/일괄 단일 SQL 헬퍼** (3곳 중복 흡수, DEC-036) |
| SQL-ST-21 | Sobo49 | UPDATE | `T2_Ssub.Sdate` | `BeforePost` Sdate 변경 (월키 + Hcode) |
| SQL-ST-22 | Sobo49 | (audit) | `audit_settlement` | 발행 stub 호출 audit 영속화 (`tax_issued_stub`, DEC-035) |
| SQL-ST-23 | (재집계) | UPSERT | `T2_Ssub.Sum26~28` | 출고/반품 원천(`S1_Ssub`/`R*_Ssub`) → `T2_Ssub` 재집계 (`recalc_billing`) |

## 5. DB 영향 — Phase 1 테이블

| table | C | R | U | D | total | write? |
| --- | --- | --- | --- | --- | --- | --- |
| T2_Ssub | ✓ | ✓ | ✓ | (soft `Yesno=2`) | 다수 | ✓ |
| T3_Ssub | ✓ | ✓ | ✓ | — | 다수 | ✓ |
| T5_Ssub | ✓ | ✓ | ✓ | (soft) | 다수 | ✓ |
| Sv_Ghng | — | ✓ | ✓ | — | trigger | ✓ |
| G7_Ggeo | — | ✓ | — | — | join only | — |
| Id_Logn | — | — | (Gpass — Audit 이관) | — | — | ✓ |

트랜잭션 경계: 청구 1건 = (`DELETE FROM T3_Ssub WHERE 월` → `INSERT 다건` → `UPSERT T2_Ssub` → 트리거 `Sv_Ghng`) 한 BEGIN/COMMIT, `app.core.db.execute_transactional_block` 사용.

## 6. 검증 규칙 (Phase 1)

| 규칙 ID | 메시지 (레거시 한글 보존) | HTTP | 적용 위치 |
| --- | --- | --- | --- |
| ST-RULE-1 | "마감된 자료입니다." | 423 | `T2_Ssub.Yesno='1'` 인 월에 쓰기 |
| ST-RULE-2 | "비밀번호가 일치하지 않습니다." | 401 | `AuditPasswordModal` 검증 실패 |
| ST-RULE-3 | "이미 취소된 자료입니다." | 409 | `Yesno='2'` 인 행 재취소 |
| ST-RULE-4 | "결재구분을 선택하세요." | 422 | `T5_Ssub.PUBUN` 미선택 |
| ST-RULE-5 | "거래처를 선택하세요." | 422 | `T2_Ssub.Hcode` 누락 |

> 정확한 한글 문자열은 `i18n/messages/c5.ko.json` (T2 신설) 에서 단일 출처로 관리 — 레거시 메시지 박스 캡처를 그대로 보존.

## 7. 고객사 분기 (`customer_variants`)

| variant | 폼 | 차이 | contract 위치 |
| --- | --- | --- | --- |
| `takbae` | Sobo45_1 | 컬럼 5~7 택배비 大/中/小, 폼 로컬 `T4_Sub51/52` | `settlement_billing.yaml: customer_variants.takbae` |
| `cash_status_sdate` | Sobo42_1 | 집계키 `Gdate`, `GPSUM` 컬럼 추가 | `settlement_billing.yaml: customer_variants.cash_status_sdate` |

> DEC-019 — 단일 모던 컴포넌트 + 데이터 주도 분기 (코드 분기 금지).

## 8. 관련 OQ·GAP·DEC

- Open Questions:
  - **OQ-ST-1** 세금계산서 외부 발행 채널 (홈택스/이메일 등) — **Phase 2 종결: stub (DEC-035)**
  - **OQ-ST-2** `Chek3` 의미 (세금계산서 발행 플래그) — **Phase 2 종결: `'1'`=발행/영수, `'0'`=미발행/청구 (DEC-036)**
  - **OQ-ST-3** 취소 시 `Yesno` 값 (`'2'` 추정 — DEC-012 패턴) — Phase 1 T3 확정 필요
  - **OQ-ST-4** 입금수단(`PUBUN`) 코드표 — 카탈로그 조회 후 enum 화
  - **OQ-ST-5** F43–F47 권한 적용 시점 — DEC-009 따라 1차 미적용, C10 통합
- Decisions:
  - **DEC-031**: C5 마감 정책 — `T2_Ssub.Yesno` 보존 (Phase 1 결정)
  - **DEC-032**: 평문 Gpass 변경 → AuditPasswordModal rotate 이관 (Phase 1)
  - **DEC-034** (Phase 2 신설): C5 Phase 2 인쇄 = HTML 미리보기, PDF/실인쇄/일괄 = C7 이연
  - **DEC-035** (Phase 2 신설): 세금계산서 외부 발행 채널 stub (`/issue` → 200 NOT_INTEGRATED + audit 영속화)
  - **DEC-036** (Phase 2 신설): Chek3 단건/일괄 토글 단일 SQL 헬퍼 흡수, `Code1↔Chek3` 매핑 동결 (`'1'`=발행)
  - DEC-009/012/019/024/028/029 — 기존 동결 사항 준수
- Gap Report: [`docs/db-logic-porting-gap-report.md`](../../docs/db-logic-porting-gap-report.md) — `T2_Ssub` / `T3_Ssub` / `T5_Ssub` 매핑 갱신 필요

## 9. 인쇄·바코드 연관

- Phase 2 (Sobo46 청구서출력 / Sobo49 세금계산서) 가 인쇄 진입점 — **HTML 미리보기**까지만 (DEC-034) → 풀 PDF/실인쇄는 **C7 인쇄 모듈** 후속
- Phase 1 본 카드 범위에서는 인쇄 트리거 미포함 (`Button702Click` 등 인쇄 버튼은 out-of-scope)

## 10. Phase 2 신규 범위 (Sobo46/49 + 재집계 + audit 회전 UI)

| # | 기능 | 폼 | 모던 라우트 | 백엔드 엔드포인트 | DEC |
| --- | --- | --- | --- | --- | --- |
| P2-A | 청구서 1매 미리보기 | Sobo46 | `/settlement/billing/[billingKey]/print` | `GET /settlement/billing/{key}/print-data`, `GET .../print` | DEC-034 |
| P2-B | 세금계산서 목록 + Chek3 토글 | Sobo49 | `/settlement/tax-invoice` | `GET /settlement/tax-invoice`, `POST .../{key}/chek3`(bulk:bool) | DEC-036 |
| P2-B' | 세금계산서 외부 발행 stub | Sobo49 | (목록 행 액션) | `POST /settlement/tax-invoice/{key}/issue` → `200 NOT_INTEGRATED` | DEC-035 |
| P2-B'' | 세금계산서 1매 미리보기 | Sobo49 | `/settlement/tax-invoice/[billingKey]/print` | `GET .../{key}/print` | DEC-034 |
| P2-C | 청구 재집계 | (Sobo45 푸터) | `/settlement/billing` (재집계 버튼) | `POST /settlement/billing/recalc` | (마감 가드 재사용) |
| P2-D | audit 회전 UI | (운영) | `/admin/audit-rotate` | `GET /audit/settlement`, 기존 rotate API 재사용 | (DEC-029/032) |

## 11. 포팅 체크리스트

- [x] T1 — 매핑 노트 6개 작성 완료 (Phase 1)
- [x] T1 — 매핑 노트 2개 추가 (Sobo46/49) + 본 카드 갱신 (Phase 2)
- [x] T2 — 이벤트 핸들러·SQL 인덱스 정리 (`analysis/handlers/c5_phase1.md`)
- [ ] T2 — Phase 2 핸들러 (`analysis/handlers/c5_phase2.md`)
- [x] T3 — `migration/contracts/settlement_billing.yaml` v1.0.0 (Phase 1)
- [ ] T3 — `settlement_billing.yaml` v1.1.0 (Phase 2 8 endpoints)
- [x] T4 — 백엔드 Phase 1 (settlement.py, settlement_service, cash_service)
- [ ] T5 — Phase 2 백엔드 (settlement_print_service, tax_invoice_service, recalc, audit list)
- [x] T5 — `migrations/2026_05_01_c5_phase1.sql` (audit_settlement, application_settings 키)
- [ ] T6 — Phase 2 프론트 (`/settlement/billing/[key]/print`, `/tax-invoice`, `/admin/audit-rotate`)
- [x] T7 — `test/test_c5_settlement_phase1.py`
- [ ] T7 — `test/test_c5_settlement_phase2.py`
- [x] T8 — DEC-031/032 추가
- [x] T8 — DEC-034/035/036 추가, OQ-ST-1/2 종결, 대시보드/문서 갱신

## 12. 참조

- 매핑 노트:
  - [`Sobo45_billing.md`](../layout_mappings/Sobo45_billing.md), [`Sobo45_1_billing.md`](../layout_mappings/Sobo45_1_billing.md)
  - [`Sobo47_billing.md`](../layout_mappings/Sobo47_billing.md)
  - [`Sobo41_cash.md`](../layout_mappings/Sobo41_cash.md)
  - [`Sobo42_cash.md`](../layout_mappings/Sobo42_cash.md), [`Sobo42_1_cash.md`](../layout_mappings/Sobo42_1_cash.md)
  - [`Sobo46_billing.md`](../layout_mappings/Sobo46_billing.md), [`Sobo49_tax.md`](../layout_mappings/Sobo49_tax.md) (Phase 2)
- 입력 산출물:
  - `tools/.../legacy_source_root/Subu41/`, `Subu42/`, `Subu42_1/`, `Subu45/`, `Subu45_1/`, `Subu47/` (Phase 1)
  - `Subu46/`, `Subu49/` (Phase 2)
- 계획서: [`docs/core-scenarios-porting-plan.md`](../../docs/core-scenarios-porting-plan.md) §C5
- 결정 로그: [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md) (DEC-031/032/033/034/035)
- 자동 생성 폼별 카드: [`Sobo45.md`](Sobo45.md), [`Sobo45_1.md`](Sobo45_1.md), [`Sobo47.md`](Sobo47.md), [`Sobo41.md`](Sobo41.md), [`Sobo42.md`](Sobo42.md), [`Sobo42_1.md`](Sobo42_1.md), [`Sobo46.md`](Sobo46.md), [`Sobo49.md`](Sobo49.md)
- 선례 카드: [`Sobo23.md`](Sobo23.md) (C4 반품 — 마감/Audit 패턴)
