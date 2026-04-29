# CRUD 동등성 인벤토리 + 보강 마일스톤

**ID**: CRUD-BACKLOG
**일자**: 2026-04-23
**상태**: 1차 스캔 (페이지 주석 + master-api.ts grep 기반)
**연관**: [`docs/menu-roadmap-waves.md`](menu-roadmap-waves.md), [`legacy-analysis/decisions.md`](../legacy-analysis/decisions.md), [`도서물류관리프로그램/frontend/src/lib/form-registry.ts`](../도서물류관리프로그램/frontend/src/lib/form-registry.ts)

---

## 1. 인벤토리 방법

1. `frontend/src/app/(app)/**/page.tsx` 에서 `READ only` · `placeholder` · `stub` · `ScreenPlaceholder` grep — 1차 후보 도출.
2. `frontend/src/lib/master-api.ts` 의 export 목록에서 `*Update` / `*Create` / `*Delete` 유무 확인.
3. `analysis/screen_cards/<Form>.md` · `migration/contracts/*.yaml` 의 write 경로/blocker 대조.
4. SME 단계는 후속 — 본 문서는 1·2·3 만으로 채운 *씨앗 표* 이며 PR 시 갱신한다.

---

## 2. CRUD gap matrix (1차)

표기 의미: **R**=조회만 / **RU**=조회+부분쓰기 / **CRUD**=레거시 동등 / **STUB**=라우트만. `목표 wave` 가 비어 있으면 *현 사이클(P2)* 범위.

### 2.1 마스터 (`master`)

| 화면 ID | 캡션 | 현재 phase | 현재 CRUD | 레거시 연산 | 갭 (필요 보강) | 목표 CRUD | 목표 wave |
|---|---|---|---|---|---|---|---|
| Sobo11 | 거래처관리 | phase1 | RU | C/R/U/D | 신규(C) + 삭제(D) — 1차 미구현 | CRUD | p3 |
| Sobo14 | 도서관리 | phase1 | RU | C/R/U/D | 신규(C) + 삭제(D) | CRUD | p3 |
| Sobo17 | 출판사 | phase1 | R | C/R/U/D | 신규/수정/삭제 — 페이지 주석 *“1차 READ only · 수정은 후속”* | CRUD | p3 |
| Sobo38 | 도서코드 | phase1 | R | C/R/U/D | 페이지 주석 *“READ only (단순 조회)”* | RU | p3 |
| Sobo39 | 할인율 | phase1 | R | C/R/U/D | 페이지 주석 *“1차는 READ only”* | RU | p3 |
| Sobo45 | 물류비 | phase1 | R | C/R/U/D | 페이지 주석 *“1차 READ only”* | RU | p3 |
| Sobo16_special | 특별관리 | phase1 | RU | C/R/U | 신규(C)·삭제(D)·Gcode/Bcode 변경은 후속, Grat1/Gssum 부분 수정 완료 | RU | p2 |

### 2.2 출고/입고/거래 (`shipment`, `transactions`)

| 화면 ID | 캡션 | 현재 phase | 현재 CRUD | 갭 | 목표 CRUD | 목표 wave |
|---|---|---|---|---|---|---|
| Sobo22 / Sobo22_import | 입고접수 / 파일 업로드 | phase1 | CRUD | (정식 포팅) | CRUD | — |
| Sobo27 / Sobo27_new | 출고접수 (목록 / 신규) | phase1 | CRUD | (정식 포팅) | CRUD | — |
| Sobo21 / Sobo21_status_* | 거래명세서 / 거래현황 LIST/요약/메모 | phase1 | R | (조회 전용 화면) | R | — |
| Sobo29_other | 기타명세서 | phase2 | STUB | `ScreenPlaceholder` — 비정형 출력기, 레거시 SQL 미확정 | RU | p3 |

### 2.3 재고/원장 (`inventory`, `ledger`)

| 화면 ID | 캡션 | 현재 phase | 현재 CRUD | 비고 | 목표 CRUD | 목표 wave |
|---|---|---|---|---|---|---|
| Sobo31 / Sobo33_ledger / Sobo33_1_ledger | 도서별수불·도서수불장·통합 | phase1 | R | 조회 전용 | R | — |
| Sobo44_inv | 재고현황 | phase1 | R | 조회 전용 | R | — |
| Sobo32_ledger / Sobo32_1_ledger | 거래처원장·통합 | phase1 | R | 조회 전용 (DBGrid301 후속은 P3) | R | p3 |
| Sobo48_compare | 장부대조 | phase2 | STUB | `ScreenPlaceholder` + DEC-040 신규 SQL 0 정책 | R | p3 |
| Sobo34_4 | 기간별재고원장(상세) | phase2 | R | 조회 전용 (회귀 미통과) | R | p2 |

### 2.4 정산/발송 (`settlement`, `billing`)

| 화면 ID | 캡션 | 현재 phase | 현재 CRUD | 갭 | 목표 CRUD | 목표 wave |
|---|---|---|---|---|---|---|
| Sobo45_billing(_bill) / Sobo45_1_billing_bill | 청구서관리 / 택배 변형 | phase1 | RU | 청구서 마감 가드 (audit) — 발급 자동화는 차기 | CRUD | p2 |
| Sobo47_billing(_bill) | 청구금액(년월) | phase1 | R | 조회 전용 | R | — |
| Sobo41_cash(_bill) | 입금내역 | phase1 | RU | 입금 INSERT 동작, 취소 미동작 | CRUD | p2 |
| Sobo42_cash(_bill) / Sobo42_1_cash_bill | 입금현황 | phase1 | R | 조회 전용 | R | — |
| Sobo46_billing(_bill) | 청구서 인쇄 | phase2 | R | 인쇄 미리보기 (HTML/PDF) — 쓰기 없음 | R | p3 |
| Sobo49_tax(_bill) | 세금계산서 | phase2 | RU | DEC-035 외부 채널 발행 stub 배너 | CRUD | p3 |
| Settle_outstanding | 미수현황 | phase2 | R | 조회 전용 | R | p2 |
| Sobo41_slip | 입금전표 | phase2 | RU | INSERT 만 — 취소/수정 미구현 | CRUD | p2 |

### 2.5 내역서 / 통계 / 반품 / 택배 / 관리

| 화면 ID | 캡션 | 현재 phase | 현재 CRUD | 비고 | 목표 CRUD | 목표 wave |
|---|---|---|---|---|---|---|
| Sobo54 / Sobo57 / Sobo55 | 일별·기간 입고/반품 내역서 | phase1 | R | 조회 전용 | R | — |
| Sobo23 / Sobo24 / Sobo25 / Sobo51 | 반품명세서 / 반품재고(재생/해체/변경) | phase1 | CRUD | 정식 포팅 | CRUD | — |
| Sobo58 / Sobo34_4 | 기간 반품 / 기간 재고원장 | phase2 | R | 조회 전용 (회귀 미통과) | R | p2 |
| Sobo50_stats / Sobo51_stats / Sobo52_stats / Sobo53_stats | 매출·거래처·도서회전·분기 손익 | phase2 | R | 차트 조회 | R | p3 |
| Stats_monthly | 월별통계 | phase2 | R | 조회 전용 | R | p2 |
| Sobo36_stats_route / Sobo37_stats_route | 거래처·도서 통계(목록) | phase2 | R | 조회 전용 | R | p3 |
| Sobo43_stats_route | 출판사통계 | phase2 | STUB | `ScreenPlaceholder` — Subu43.pas 합계 미포팅 | R | p3 |
| Sobo28_delivery | 출고택배관리 | phase1 | RU | 내부 라인/메모 완료, 외부 택배사 API는 별도 후속 | RU | p4 |
| WebAdmHome / WebAdmUserSrv / WebAdmRBAC / WebAdmEnv / Subu10_id_logn | 관리 콘솔 | phase1 | RU/CRUD | admin-api 에 POST/PUT 존재 | CRUD | — |
| WebAdmAuditRotate | 감사 비밀번호 회전 | phase2 | RU | 회전 동작, 회귀 미통과 | RU | p2 |
| WebAdmOps / WebAdmAudit | 운영 모니터링·감사 통합 뷰 | phase2 | R | 조회 전용 | R | p2 |

### 2.6 placeholder / stub 일람

다음은 `ScreenPlaceholder` 또는 `DEC-035 stub` 배너를 사용 중인 화면 — `crudParity: "STUB"` 으로 단일 분류한다.

- `Sobo29_other` (기타명세서)
- `Sobo48_compare` (장부대조)
- `Sobo43_stats_route` (출판사통계)
- (할인율 변형) `/master/discount/[type]` 라우트는 메뉴 미노출 — 별도 등록 없음.

---

## 3. CRUD 보강 절차 (G0 ~ G4)

각 갭 화면에 한 줄 마일스톤을 부여한다 (단계는 [`docs/menu-roadmap-waves.md`](menu-roadmap-waves.md) §6 와 정합).

| 단계 | 산출 | 위치 |
|---|---|---|
| **G0** 갭 확정 | 레거시 버튼·SQL 목록 vs 웹 API | `analysis/screen_cards/<Form>.md` §CRUD 갭 |
| **G1** 계약·테스트 보강 | yaml + test-cases JSON | `migration/contracts/<flow>.yaml` |
| **G2** 백엔드 라우트 | POST/PATCH/DELETE + audit_log | `app/services/<flow>_service.py` + 라우터 |
| **G3** 프론트 폼·그리드 | 신규/편집 다이얼로그 + 행 액션 | `app/(app)/<area>/page.tsx` |
| **G4** 5축 재통과 | `crudParity: CRUD` 로 상향 + `roadmapWave` 정리 | `form-registry.ts` |

---

## 4. 우선순위 권고 (P2 → P3 → P4)

### P2 (현 사이클 내 정리 권장 — 비즈니스 영향 큼)

| 화면 | 보강 핵심 | 의존 |
|---|---|---|
| Sobo16_special | `ScreenPlaceholder` → 실제 폼 (특별관리 분류 카탈로그 합의) | `master-special-implementation-plan.md` |
| Sobo41_slip / Sobo41_cash | 입금 취소/수정 (audit) | DEC-031/032 |
| Sobo45_billing(_bill) | 청구서 자동 발급 + 마감 가드 | DEC-031 |
| Sobo48_compare | 단일 SQL 합의 → 1차 조회 화면 | DEC-040 |
| WebAdmAuditRotate / WebAdmOps / WebAdmAudit | 5축 PASS → phase1 승격 | docs/phase1-promotion-gate.md |

### P3 (차기 분기)

| 화면 | 보강 핵심 |
|---|---|
| 출판사·할인율·물류비·도서코드·도서·거래처 마스터 | 신규(C) + 수정(U) + 삭제(D) 폼 (마스터 전영역) |
| Sobo32_ledger / Sobo32_1_ledger | DBGrid301 (계좌 잔액 분해) — `customer-ledger-implementation-plan.md` §8 |
| Sobo46_billing / Sobo49_tax | 인쇄·세금 PDF 양식 + 외부 채널 실연동 |
| Sobo50~53_stats / Sobo36/37/43_stats_route | recharts 시각화 보강 + 정책 확장 |
| Sobo29_other | 비정형 명세 출력기 SQL 합의 |

### P4 (장기·인프라)

| 영역 | 보강 핵심 |
|---|---|
| Sobo28_delivery | 택배사 API 연동 (외부 채널 합의) |
| 컷오버 런타임 검증 | C15 어댑터 + 운영 전환 (DEC-CUT 계열) |
| 인쇄 Phase 3 후 per-form 화이트리스트 | `docs/print-html-status.md` DEC-050 예정 |

---

## 5. 갱신 정책

- 본 표는 [`form-registry.ts`](../도서물류관리프로그램/frontend/src/lib/form-registry.ts) 의 `crudParity` / `roadmapWave` 가 변경될 때 함께 PR 로 갱신한다.
- `test/test_form_registry_metadata.py` 가 “phase1 + R/RU/STUB 인데 갭 사유 없음” 을 1차에는 *경고*, 2차 사이클에 *에러* 로 승격.
- SME 검토 후 정확도가 올라가면 표의 “레거시 연산” 칸을 `frontend/src/lib/legacy-form-overrides` 또는 `analysis/screen_cards/*` 에서 가져온 단일 원천으로 대체.
