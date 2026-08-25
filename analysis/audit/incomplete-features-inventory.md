# 구현되지 못한 기능 인벤토리 (저장소 자동 산출)

생성: `2026-08-25T03:41:43.722019+00:00` (`debug/generate_incomplete_features_inventory.py`)

## 판정 기준 (합집합)

본 인벤토리는 계획서 「구현되지 못한 기능 목록」에 따라 **원천별 합집합** 을 기록한다. 단일 정의가 아니라 (A) UI placeholder (B) T-파이프라인 비완료 (C) form-registry preview/STUB (D) phase1 이지만 R/RU/STUB 인 부분 동등 (E) 백엔드 stub grep (F) crud-backlog §2.6 참조 를 모두 포함한다.

## 1. UI — `ScreenPlaceholder` 가 붙은 라우트

- (없음)

## 2. T1–T8 — `phase2-screen-cards.json` 에서 아직 done 아닌 task

> **드리프트 주의:** 카드의 레거시 ID·캡션과 해당 `route` 의 `page.tsx` 실구현 범위가 다를 수 있다. 판단은 API·화면 코드 우선.

- **Sobo43_shipping_ledger** (발송비내역) `/settlement/shipping-ledger` — {'T2': 'pending', 'T4': 'pending', 'T7': 'pending', 'T8': 'pending'}
  - blockers: ['DEC-040 재사용 검토', 't3_ssub_adapt', 'T4 test-cases·T7 회귀']
- **Sobo44_shipping_status** (발송비현황) `/settlement/shipping-status` — {'T2': 'pending', 'T4': 'pending', 'T7': 'pending', 'T8': 'pending'}
  - blockers: ['T2 SQL·t3_ssub_adapt', 'T4 test-cases·T7 회귀 — yaml v0.1 초안 반영됨']

## 3. `form-registry` — preview 또는 STUB

- (없음)

## 4. `form-registry` — phase1 이지만 부분 동등 (R / RU / STUB)

> 레거시 화면은 풀 CRUD 였지만 모던 화면이 조회·부분쓰기에 머문 항목.

### R (21건)
- `MenuBillingStatements` (내역서관리) `/billing/statements`
  - 허브 MVP (2026-05-15) — 입고·반품·거래·출고·택배·판매 리포트로 링크. 8종 단일 SQL은 후속
- `MenuShippingReturnsInventory` (반품재고관리(통합)) `/shipping/returns-inventory`
  - 허브 MVP (2026-05-15) — 정본 /returns/inventory 로 안내. 통합 전용 SQL 그리드는 후속
- `Sobo21` (거래 명세서) `/transactions/sales-statement`
  - 거래명세서 조회(Subu21). 메모 쓰기는 거래현황(메모) Sobo21_status_memo RU(PATCH /transactions/sales-statement/{key}/memo)로 분리
- `Sobo21_status_detail` (거래 현황(상세)) `/transactions/status?view=detail`
  - 레거시 Sobo24 거래현황 상세 — 전표 단위 라인(도서·수량·금액) 펼침. GET /transactions/status?view=detail
- `Sobo21_status_list` (거래 현황(LIST)) `/transactions/status?view=list`
  - 거래현황 목록 조회 — GET /transactions/status?view=list
- `Sobo21_status_summary` (거래 현황(요약)) `/transactions/status?view=summary`
  - 거래현황 기간 요약 집계 조회 — GET /transactions/status?view=summary
- `Sobo22_inbound_statement` (입고명세서) `/transactions/inbound-statement`
  - C1 phase1 — Menu202 입고명세서(조회·출력). GET /transactions/inbound-statement 는 inbound_service.list_receipts 재사용 facade(신규 SQL 0). 라인 펼침은 /inbound/receipts/{key} 지연 조회. C3 입고접수(/inbound/receipts)와 동일 Subu22 — variant 는 inbound_receipt.yaml 에만
- `Sobo25_status_detail` (입고 현황(상세)) `/transactions/inbound-status?view=detail`
  - C2 phase1 — 입고현황 상세(view=detail). 목록은 list 와 동일 facade, 행 펼침 시 /inbound/receipts/{key} 라인 지연 조회(신규 SQL 0)
- `Sobo25_status_list` (입고 현황) `/transactions/inbound-status`
  - C2 phase1 — Menu205 입고현황(F25, 조회). Publisher 정본 publisher_source_root/Subu25(caption 입고현황) 재추출로 P0 해제. GET /transactions/inbound-status?view=list 는 inbound_service.list_receipts 재사용 facade(신규 SQL 0). Sobo25_inbound_status.md
- `Sobo25_status_summary` (입고 현황(요약)) `/transactions/inbound-status?view=summary`
  - C2 phase1 — 입고현황 요약(view=summary). inbound_service.period_report(기간 출판사/거래처 집계) 재사용 facade(신규 SQL 0)
- `Sobo26_production_stmt` (제작명세서) `/transactions/production/statement`
  - C6 phase1 — Menu206 제작명세서(F26, 조회). Publisher 정본 publisher_source_root/Subu26(caption 제작명세서) 재추출로 P0 해제. GET /transactions/production/statement = production_service.list_production_statement(S2_Ssub, Ycode=출판사). 인쇄 OOS(DEC-017). Sobo26_production_stmt.md
- `Sobo27_production_status` (제작현황) `/transactions/production/status`
  - C7 phase1 — Menu207 제작현황(F27, 조회). Publisher 정본 publisher_source_root/Subu27(caption 제작현황) 재추출로 P0 해제. GET /transactions/production/status = production_service.list_production_status(S2_Ssub, Bcode 범위 필터). Sobo27_production_status.md
- `Sobo28_withholding` (원천징수) `/transactions/withholding`
  - C8 phase1 — Menu208 원천징수(F28, 조회). Publisher 정본 publisher_source_root/Subu28(caption 원천징수관리) 재추출로 P0 해제. GET /transactions/withholding = withholding_service.list_withholding(S3_Ssub, 저자명 G3_Gjeo.Gposa). 인쇄 OOS(DEC-017). Sobo28_withholding.md
- `Sobo34_4` (기간별재고원장(상세)) `/returns/ledger`
  - 조회 전용 — 페이저 v1.2.0 (DEC-033 e/g 표준)
- `Sobo46_billing` (청구서 인쇄(미리보기)) `/settlement/billing?view=print`
  - 인쇄 미리보기만 — 쓰기 없음 (DEC-035 외부 채널 후속)
- `Sobo46_billing_bill` (청구서출력) `/settlement/billing?view=print`
  - 인쇄 미리보기만 — 쓰기 없음 (DEC-035 후속)
- `Sobo58` (기간별반품내역서) `/returns/period-report`
  - 조회 전용 — test_c4_returns_phase2 / test_returns_period_ledger_regression / DEC-028 data-legacy-id
- `Sobo59_1` (출고검증(1)) `/transactions/verification?v=1`
  - C3 phase1 — 정본 캡션은 「일별 내역서(요약)」(Subu59_1.dfm). GET /transactions/verification?v=1 = verification_service.list_verification(mode=summary, S1_Ssub 그룹 Bcode 제외). 검증 쓰기 없는 요약 조회(R). SME 확인 후 캡션 정정 가능. Sobo59_2.md
- `Sobo_author_history` (내역조회(저자)) `/transactions/author-history`
  - C10 phase1 — Publisher MySQL/Subu26_1(내역조회(저자)-거래현황) 정본 publisher_source_root 재추출로 P0 해제. GET /transactions/author-history = author_history_service.list_author_history(S1_Ssub 라인 Scode='X' + G4_Book.Gjeja 저자). 조회 전용. Sobo_author_history.md
- `WebAdmAudit` (감사 통합 뷰) `/admin/audit`
  - 조회 전용 — C14 phase2 회귀 통과
- `WebAdmOps` (운영 모니터링) `/admin/ops`
  - 조회 전용 — C14 phase2 회귀 통과

### RU (11건)
- `Sobo16_baebon` (배본처관리) `/master/baebon`
  - Sobo16 G6_Ggeo를 배본처(거래처/도서/물류코드) 중심으로 재표기
- `Sobo21_status_memo` (거래 현황(메모)) `/transactions/status?view=memo`
  - 거래현황 메모 조회+편집 — PATCH /transactions/sales-statement/{key}/memo (S1_Memo UPSERT, Subu21.pas L1452 동등)
- `Sobo28_delivery` (택배관리) `/shipping/courier`
  - 내부 S1_Ssub 라인 조회 + S1_Memo 조회/저장 완료 — 외부 택배사 API는 별도 후속
- `Sobo29_new_release` (신간발행) `/transactions/new-release`
  - Menu209 신간발행 — 2026-08-25(DEC-195) 입고현황과 같은 3뷰 공용 축(TransactionStatusScreen NEW_RELEASE_AXIS, kind=inbound). GET /transactions/new-release?view=summary|detail|list 는 _status_axis_facade(입고 + Pubun='신간', Scode='Y'+Gcode<>'', 표시명 G2_Ggwo). 편집은 ReceiptDetailDialog(PUT /inbound/receipts/{key}). 종전 기타명세서 facade·전체메모 편집은 폐기.
- `Sobo29_other` (기타명세서) `/transactions/other`
  - S1_Ssub 신간/기타 명세 조회 + S1_Memo 전체메모 저장
- `Sobo48_compare` (출판사관리(설정)) `/ledger/comparison`
  - G7_Ggeo 출판사 설정 조회 + Chek3/Scode 부분 저장
- `Sobo49_tax` (세금계산서 발행) `/settlement/tax-invoice`
  - DEC-035 외부 채널 발행 stub 배너 — 실제 발행은 후속
- `Sobo49_tax_bill` (세금계산서) `/settlement/tax-invoice`
  - DEC-035 외부 채널 발행 stub 배너 — 실제 발행은 후속
- `Sobo59_2` (출고검증(2)) `/transactions/verification?v=2`
  - C4 phase1 — 「출고 검증관리」(Subu59_2). GET /transactions/verification?v=2 = list_verification(mode=book), PATCH /transactions/verification = confirm/cancel(S1_Chek INSERT Yesno='1' / UPDATE Check='D', Subu59_2.pas Button102/103 동등). 검증 키=(Hcode,Gdate,Scode,Gcode,Jubun,Gjisa,Bcode). Sobo59_2.md
- `Sobo59_3` (출고검증(개별)) `/transactions/verification?v=individual`
  - C5 phase1 — 「출고 검증관리(개별)」(Subu59_3). GET /transactions/verification?v=individual = list_verification(mode=book), PATCH = confirm/cancel(S1_Chek). v=2와 동일 검증 키·쓰기, 개별(라인) 선택 UI. T4_Ssub 개별 바코드 적재는 후속(OOS). Sobo59_3.md
- `WebAdmAuditRotate` (감사 비밀번호 회전) `/admin/audit-rotate`
  - 회전(write) 동작 — C5 phase2 회귀 통과


## 5. 백엔드 stub grep (`app/routers/*.py`)

- `도서물류관리프로그램/backend/app/routers/_stub.py:10` — `503 + ``code=NOT_IMPLEMENTED`` 면 「준비 중」 으로 정확히 표시된다.`
- `도서물류관리프로그램/backend/app/routers/_stub.py:27` — `"""이름이 무엇이든 503 응답. 프론트는 NOT_IMPLEMENTED 로 인식."""`
- `도서물류관리프로그램/backend/app/routers/_stub.py:29` — `status_code=status.HTTP_503_SERVICE_UNAVAILABLE,`
- `도서물류관리프로그램/backend/app/routers/_stub.py:31` — `"code": "NOT_IMPLEMENTED",`
- `도서물류관리프로그램/backend/app/routers/returns.py:755` — `status_code=status.HTTP_501_NOT_IMPLEMENTED,`
- `도서물류관리프로그램/backend/app/routers/settlement.py:1174` — `result = await tax_invoice_service.issue_external_stub(`

## 6. `docs/crud-backlog.md` §2.6 참조 (문서 불릿)

- `Sobo49_tax` — DEC-035 외부 발행 stub 배너 (세금계산서)
- `Sobo43_shipping_ledger` / `Sobo44_shipping_status` — 발송비 진짜 도메인 API scaffold (빈 목록; wrong_id `Sobo43_stats_route`/`Sobo44_inv` 와 분리)

## 갱신·CI

```bash
python3 debug/generate_incomplete_features_inventory.py            # 갱신
python3 debug/generate_incomplete_features_inventory.py --check    # CI: 미갱신이면 exit 1
```

산출: `analysis/audit/incomplete-features-inventory.md` · `.json`

