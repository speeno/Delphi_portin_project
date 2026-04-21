# Phase 1 Component Fidelity Audit (33 폼 전수)

> **사이클**: audit_only — 코드/UX 변경 0. 본 문서는 [`phase1_component_re-audit`](../../.cursor/plans/phase1_component_re-audit_7dd5dd8c.plan.md) 산출물 §3 매트릭스 + 폼별 §A~§AG 5축 표.
>
> **단일 원천 원칙** — Phase 1 승격 게이트(DEC-045)·dfm 공식 입력(DEC-028)·컴포넌트 동등성 정기 재점검(DEC-053) 모두 본 파일을 참조한다. 대시보드/cursor rule/PR 리뷰가 동일 매트릭스를 인용한다.

## 0. 스코프 — phase1 33 폼 (form-registry.ts ::phase=phase1)

`도서물류관리프로그램/frontend/src/lib/form-registry.ts` 의 `phase: "phase1"` = **33 행** (자동 추출 검증). 본 사이클 대상은 33 행 전체 (phase2/preview/inbox/preview 제외).

DFM 보유 폼 = **29** (Subu*) + DFM 부재 Wave D = **4** (`WebAdm*`, OOS-MAS-1, DEC-022).

## 1. Audit 방법

폼 1개당 **5 축** 한 단어 평가 → `PASS` / `OOS` / `GAP-P0` / `GAP-P1` / `GAP-P2`.

| 축 | 의미 | 입력 산출물 | PASS 기준 |
| --- | --- | --- | --- |
| W (Widget) | dfm 위젯 누락 0 | `<Sobo*>.tree.json` leaf + `analysis/layout_mappings/<Sobo*>.md` §3·§4·§5 | 매핑 노트의 부착 대상 위젯이 모던 페이지 DOM 에 `data-legacy-id`/`legacyId` 부착 + §6 out-of-scope 가 코드에 우연 진입 0 |
| B (Business logic) | OnClick/OnChange/SQL 의미 보존 | `<Sobo*>.pas_analysis.json` + `migration/contracts/*.yaml` | 매핑 §8 이벤트 매핑의 모던 핸들러가 동일 의미를 수행 (read-only/CRUD/취소/메모 UPSERT 등) |
| U (User flow) | TabOrder·단축키·토글·라디오·다이얼로그 | 매핑 §3 TabOrder 보존 표 + 매핑 §10 회귀 가드 체크리스트 | 키보드 흐름 + 모달리스/다이얼로그 흐름이 매핑 노트와 일치 |
| D (Data) | 표시 컬럼·집계·필터 기본값 | 매핑 §4 (DBGrid 컬럼) + contract `equivalence.data` | DBGrid FieldName 1:1 매핑 (의미 일치 컬럼 0 누락; 보강 컬럼은 §7 deltas 로 명시) |
| O (Out-of-scope) | 의식적 비포함 항목 | 매핑 §6 out-of-scope + contract `out_of_scope` | 매핑·contract·코드 3 곳에서 동일 항목 명시 |

P0 = 사용자 작업이 막힘 (예: 본사/창고 토글 부재로 데이터가 비어 보임 — 본 사이클 직전 핫픽스). P1 = 데이터 누락 (조회 결과 컬럼/합계 누락). P2 = UX 차이 (미설정 안내·라벨 미세 차이).

## 2. 인벤토리 + 매핑 매트릭스 (33 행)

| # | form | route | menu | mapping | W | B | U | D | O | P0 | P1 | P2 | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Sobo11 | /master/customer | master | [Sobo11.md](../layout_mappings/Sobo11.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 거래처 마스터 — DEC-019 다중 변형 통합 + DEC-023 단일 원천 |
| 2 | Sobo14 | /master/book | master | [Sobo14.md](../layout_mappings/Sobo14.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 도서 마스터 — 가격 이력 컬럼 모던 신설 (deltas) |
| 3 | Sobo17 | /master/publisher | master | [Sobo17.md](../layout_mappings/Sobo17.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 출판사·출고거래처 마스터 |
| 4 | Sobo38 | /master/book-code | master | [Sobo38.md](../layout_mappings/Sobo38.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 도서코드 마스터 |
| 5 | Sobo39 | /master/discount | master | [Sobo39.md](../layout_mappings/Sobo39.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 할인율 — 변형 39_1/39_2/39_5 는 `?type=` 통합 |
| 6 | Sobo45 | /master/logistics-cost | master | [Sobo45.md](../layout_mappings/Sobo45.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 물류비 — `Sobo45_billing` 과 ID 충돌 회피 |
| 7 | Sobo22 | /inbound/receipts | shipment | [Sobo22.md](../layout_mappings/Sobo22.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 입고접수 — Sobo22/22_1/22_2 변형 통합 (DEC-019) |
| 8 | Sobo22_import | /inbound/import | shipment | [Sobo38_inbound.md](../layout_mappings/Sobo38_inbound.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | Sobo38 의 입고 파일 업로드 분기 — 단일 입력 화면 |
| 9 | Sobo27 | /outbound/orders | shipment | [Sobo27.md](../layout_mappings/Sobo27.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 출고접수 — Sobo27/27_1 변형 통합, 종료일 deltas |
| 10 | Sobo21 | /transactions/sales-statement | shipment | [Sobo21.md](../layout_mappings/Sobo21.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 거래명세서 — DEC-017 인쇄 후속 |
| 11 | Sobo31 | /inventory/ledger | ledger | [Sobo31.md](../layout_mappings/Sobo31.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 도서별수불원장 — DBGrid201 거래처 분배는 C5 후속 |
| 12 | Sobo61 | /reports/book-sales | statistics | [Sobo61.md](../layout_mappings/Sobo61.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 도서별 판매 — DBGrid201 거래처 분배는 Sobo62 분리 |
| 13 | Sobo62 | /reports/customer-sales | statistics | [Sobo62.md](../layout_mappings/Sobo62.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 거래처별 판매 — Sobo61 의 분배 그리드 분리 형태 |
| 14 | Sobo23 | /returns/receipts | returns | [Sobo23.md](../layout_mappings/Sobo23.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 반품명세서 — Sobo23_1 라인 다이얼로그 통합 |
| 15 | Sobo24 | /returns/inventory | returns | [Sobo24.md](../layout_mappings/Sobo24.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 반품재고(재생) — 통합 탭 |
| 16 | Sobo25 | /returns/inventory | returns | [Sobo25.md](../layout_mappings/Sobo25.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 반품재고(해체) — 통합 탭 |
| 17 | Sobo51 | /returns/inventory | returns | [Sobo51.md](../layout_mappings/Sobo51.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 반품재고(변경) — DEC-029 audit 비밀번호 게이트 |
| 18 | Sobo55 | /returns/reports | returns | [Sobo55.md](../layout_mappings/Sobo55.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 일별반품내역서 |
| 19 | Sobo45_billing | /settlement/billing | settlement | [Sobo45_billing.md](../layout_mappings/Sobo45_billing.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 청구서관리 — DEC-031/036 마감 가드 |
| 20 | Sobo47_billing | /settlement/period | settlement | [Sobo47_billing.md](../layout_mappings/Sobo47_billing.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 청구금액(년월) |
| 21 | Sobo41_cash | /settlement/cash | settlement | [Sobo41_cash.md](../layout_mappings/Sobo41_cash.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 입금내역 |
| 22 | Sobo42_cash | /settlement/cash-status | settlement | [Sobo42_cash.md](../layout_mappings/Sobo42_cash.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 입금현황 — variant=hcode/sdate 통합 분기 (Sobo42_1) |
| 23 | Sobo45_billing_bill | /settlement/billing | billing | [Sobo45_billing.md](../layout_mappings/Sobo45_billing.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | DEC-049 IA 별칭 — 정본 라우트 동일 |
| 24 | Sobo45_1_billing_bill | /settlement/billing?variant=takbae | billing | [Sobo45_1_billing.md](../layout_mappings/Sobo45_1_billing.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | DEC-049 IA 별칭 (택배 변형) |
| 25 | Sobo47_billing_bill | /settlement/period | billing | [Sobo47_billing.md](../layout_mappings/Sobo47_billing.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | DEC-049 IA 별칭 |
| 26 | Sobo41_cash_bill | /settlement/cash | billing | [Sobo41_cash.md](../layout_mappings/Sobo41_cash.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | DEC-049 IA 별칭 |
| 27 | Sobo42_cash_bill | /settlement/cash-status?variant=hcode | billing | [Sobo42_cash.md](../layout_mappings/Sobo42_cash.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | DEC-049 IA 별칭 (거래처별) |
| 28 | Sobo42_1_cash_bill | /settlement/cash-status?variant=sdate | billing | [Sobo42_1_cash.md](../layout_mappings/Sobo42_1_cash.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | DEC-049 IA 별칭 (일자별) |
| 29 | WebAdmHome | /admin | admin | (DFM 부재) | OOS | OOS | OOS | OOS | OOS | 0 | 0 | 0 | Wave D — DEC-022 OOS-MAS-1 (신규 도메인) |
| 30 | WebAdmUserSrv | /admin/user-servers | admin | (DFM 부재) | OOS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | DEC-052 1:1 라디오 + 미설정 경고 배지 |
| 31 | WebAdmRBAC | /admin/rbac | admin | (DFM 부재) | OOS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | C10 Phase 1 — 역할/권한 매트릭스 |
| 32 | WebAdmEnv | /admin/settings | admin | (DFM 부재) | OOS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 환경설정(개정) — Sobo19 레거시와 분리 (DEC-019) |
| 33 | Subu10_id_logn | /admin/id-logn | admin | [Id_Logn.md](../layout_mappings/Id_Logn.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | C10 풀 스코프 — F11~F89 메뉴 매트릭스 |

### 2.1 합계 (P0/P1/P2)

| 합계 | 값 |
| --- | --- |
| Phase1 폼 | **33** |
| GAP-P0 (작업 차단) | **0** ✅ |
| GAP-P1 (데이터 누락) | **0** ✅ |
| GAP-P2 (UX 차이 / deltas 의 모던 신설 안내) | **15** (모두 매핑 §7 deltas 에 명시 — 의식적 차이) |
| OOS (의식적 비포함) | 33 폼 모두 §6 OOS 항목 보유 (Wave D 4 = 폼 전체 OOS) |

> **GAP-P0 = 0 ✅** — 본 사이클의 phase1 승격 게이트 (DEC-053 §결정) 통과.

### 2.2 본 사이클 직전 GAP-P0 회수 1건 (사례 기록 — 재발 방지 근거)

| 폼 | 항목 | 발견 시점 | 해결 결정 | 상태 |
| --- | --- | --- | --- | --- |
| Sobo67 (phase2) | Panel102 본사/창고 토글 부재 → outbound list `Ocode='B'` 강제 → 본사 데이터 비어 보임 | 2026-04-21 사용자 보고 | DEC-051/052 동결 직전 핫픽스 — `store_kind` 쿼리 + 라디오 그룹 신설 + mysql3_protocol 분기 | RESOLVED |

본 사례는 phase1 폼은 아니나, **5축 D(Data) 누락이 사용자 차단으로 이어진 정확한 예시**. DEC-053 의 P0 정의는 본 사례를 모범으로 한다.

### 2.3 phase1 정식 승격 1건 — Sobo67_status (2026-04-21)

| 폼 | route | menu | 승격 근거 (5축) | 상태 |
| --- | --- | --- | --- | --- |
| Sobo67_status | /outbound/status | shipment | W: Panel102 본사/창고/전체 라디오 토글 복원 · B: GET `/api/v1/outbound/shipment-status?store_kind=A\|B\|ALL` Sobo67 의미 보존 · U: 라디오 + 페이지네이션 + 그리드(키보드 흐름 보존) · D: 일자×거래처 매트릭스 + 합계/취소 카운트(Sobo67 DBGrid 동등) + `count_grouped` 서버 집계 + `in_clause_lookup` 청크 마스터 룩업 · O: 인쇄·전표편집은 §6 OOS 명시 (DEC-017 인쇄 포팅 후속) | PASS (P0=0, P1=0, P2=0) |

§2.1 합계 매트릭스는 본 사이클 동결(33행) 유지. **Sobo67_status 의 34행 정식 편입은 다음 audit 사이클에서 처리**(form-registry phase1 라벨/사이드바 표기/대시보드 카드 T8=done 은 본 변경에서 동기화 완료). 본 합류로 sidebar P2 배지 → `CheckCircle2` 초록 체크로 마무리.

## 3. 폼별 5축 audit (29 DFM 폼 + 4 Wave D)

각 § 은 **2.5 매트릭스 1행 + 핵심 발견** 만 기록. 위젯 표·이벤트 매핑 등 풀 깊이는 `analysis/layout_mappings/<form>.md` (단일 원천) 가 가진다 — 여기서는 중복 기록 금지.

### §A. Sobo11 거래처관리 (master)

- **W**: PASS — Sobo11.md §3 부착 대상 17 종(`Edit101~108`/`Panel101~104`/`DBGrid101.HCODE/HNAME/HTEL1/HPOST/HBIGO`/`Button101`/`dxButton1`) 매핑됨. DEC-019 변형(7폴더) 통합으로 `Sobo11_*` variant 분기 0 건.
- **B**: PASS — `Subu11.pas` Button101Click(L312, S2 조회) → `customers_service.list_customers` 의미 일치. master CRUD UPSERT는 detail 라우트에서.
- **U**: PASS — TabOrder hcode → hname → 조회 순(매핑 §3) 보존. 캘린더 OOS.
- **D**: PASS — `HCODE/HNAME/HTEL/HPOST/HBIGO` 1:1, 신설 `last_login`/`updated_at` 은 deltas.
- **O**: §6 — Edit107/108 출판사 검색·Panel004 자동알람 라디오·CornerButton Print/Bar 모두 OOS-MAS-2 (마스터는 read-only 인쇄 후속).

### §B. Sobo14 도서관리

- **W/B/U/D**: PASS — Sobo14.md §3·§4 매핑된 `BCODE/BNAME/BAUTH/BPUBL/BPRIC/BBIGO` + Sobo14_price 가격이력 합본. **deltas (P2)**: `price_history` 그리드 모던 신설.
- **O**: §6 Edit107/108 검색·Button701~703 라벨인쇄 (DEC-018 후속).

### §C. Sobo17 출판사·출고거래처

- 5축 PASS. DEC-019 폴더 변형(Subu17/Subu17_1/Subu17_a) 통합. 출고거래처 `OCODE` 와 출판사 `PCODE` 분리 폼 단일 라우트.
- **O**: 인쇄·라벨·출판사 그룹 통계.

### §D. Sobo38 도서코드

- 5축 PASS. Sobo38.md §3 — 단일 그리드 코드/명/구분.
- **deltas (P2)**: 모던 `usage_count` 컬럼 신설.

### §E. Sobo39 할인율(대표)

- 5축 PASS. variant `Sobo39_1/_2/_5` (할인율 2/기타/물류) 는 사이드바 별 항목 + 모던 `?type=` 단일 라우트로 통합. variant 폴더의 컬럼 차이 0건.
- **O**: §6 — 일자별 할인 캘린더, 거래처 그룹 할인 (Phase 2 OQ-MAS-3).

### §F. Sobo45 물류비

- 5축 PASS. 매핑 노트 §3 TabOrder hcode → 일자 → 금액. CRUD R/U.
- **O**: 인쇄, 영수증 폼.

### §G. Sobo22 입고접수

- W/B/U/D PASS — Sobo22.md §3 부착 26 종. 변형 Subu22/22_1/22_2 통합 (`customer_variants`).
- **deltas (P2)**: 모던 신규 종료일 입력 + DataGridPager + 신규 등록 폼 분리 (`new/page.tsx`). 모두 §7 deltas 명시.
- **O**: ProgressBar 진행 표시, 출판사 검색 Edit107/108, 자동알람 Panel004.

### §H. Sobo22_import 입고 파일 업로드

- Sobo38_inbound.md §3 부착됨. 파일 드롭존 + 미리보기 그리드. 5축 PASS.
- **O**: 진행 표시 패널.

### §I. Sobo27 출고접수

- W/B/U/D PASS — Sobo27.md §3·§4 부착 ~10 종 (`Edit101`,`Panel101`,`Button101`/`dxButton1`,`Button201`,`DBGrid101.GCODE/GOQUT/GSQUT/CODE3`,`StBar101`,`FormClose`).
- **deltas (P2)**: 종료일·거래처 코드·취소 포함·DataGridPager 모두 §7 명시. Subu27 vs Subu27_1 = UI diff 0행, 로직 22행 차이는 `customer_variants` 흡수.
- **O**: §6 — 자동알람 Panel004, 신간 필터 Panel005, 출고증 인쇄 라디오 Panel011, 진행 ProgressBar Panel007, DBGrid 이미지 컬럼, 출판사 검색 Edit102~105.

### §J. Sobo21 거래명세서

- 5축 PASS. Sobo21.md §3·§4·§5 — 목록 + 상세 메모 카드. UPSERT(저장) Button801 매핑.
- **deltas (P2)**: 종료일·페이지네이터·상세 라우트 분리·메모 신규/수정 안내.
- **O**: §6 — Edit106 전표구분 콤보, 출판사 검색 4종, 인쇄/바코드(DEC-017/018), 라인 단가/할인 GDANG/GRAT1.

### §K. Sobo31 도서별수불원장

- W/B/U/D PASS — Sobo31.md §3·§4 부착, 시계열 그리드 `GDATE/GIQUT/GOQUT/GJQUT/GBQUT/GPQUT` 1:1.
- **deltas (P2)**: 모던 입고액/출고액/재고액 금액 컬럼은 §7 deltas (Sg_Csum 보강). DBGrid201 거래처 분배는 §6 OOS (C5 후속).
- **O**: §6 — 본사/지점 토글, 신간 라디오, 진행 패널, 출판사 검색.

### §L. Sobo61 도서별 판매

- W/B/U/D PASS — Sobo61.md §3·§4 부착. 단일 도서별 합계 그리드 (mid 만).
- **deltas (P2)**: 모던 hcode 입력 신설(dfm 본사 단일 가정 → 명시 입력). DBGrid201 거래처 분배는 Sobo62 로 분리.
- **O**: §6 — 지점별검색 CheckBox1, 본사출고제외 CheckBox2 → 백엔드 scope 파라미터 흡수.

### §M. Sobo62 거래처별 판매

- 5축 PASS. Sobo61 의 DBGrid201 분배 그리드를 정식 화면으로 분리.
- **deltas (P2)**: `?hcode=` 단일 거래처 + 페이지네이션.
- **O**: §6 — 인쇄/엑셀 추출은 후속.

### §N. Sobo23 반품명세서

- W/B/U/D PASS — Sobo23.md §3·§4·§5 부착 ~20종. Sobo23_1 라인 다이얼로그 통합 (`Sobo23_1.md`). DataImportModal (`Sobo23_1_chul08`) 임베드.
- **deltas (P2)**: 종료일·페이지네이터·상세 라우트·취소 포함 토글·신규 등록 라우트·메모 UPSERT 안내.
- **O**: §6 — Edit102 combo 전표구분, 출판사 검색 Edit107/108, 인쇄 Button701/702/901, 라벨 코너 Label301~309 + CornerButton1~9, 라인 단가/할인 GDANG/GRAT1.

### §O. Sobo24 반품재고(재생)

- 5축 PASS. 통합 탭 페이지 (`/returns/inventory`) 의 「재생」 탭. Subu24.pas 의 G_Pcom 패스워드 게이트 → DEC-029 audit 비밀번호 게이트로 일반화.
- **O**: §6 — 인쇄/라벨, 변경 이력 그리드.

### §P. Sobo25 반품재고(해체)

- 5축 PASS. 동일 라우트의 「해체」 탭. 의미 일치.
- **O**: §6 — 동일 OOS 항목 (인쇄/이력 그리드).

### §Q. Sobo51 반품재고(변경)

- 5축 PASS. 동일 라우트의 「변경」 탭. **DEC-029 audit 비밀번호 게이트 보존** (B 축 PASS).
- **O**: §6 — 인쇄/이력.

### §R. Sobo55 일별반품내역서

- 5축 PASS. Sobo55.md §3·§4 — 일자별 GROUP BY 그리드.
- **deltas (P2)**: 페이지네이터, CSV 다운로드.
- **O**: §6 — 진행 패널, 출판사 분배.

### §S. Sobo45_billing 청구서관리

- W/B/U/D PASS — Sobo45_billing.md §3·§4 부착. DEC-031/036 마감 가드 (Y/N) 보존.
- **deltas (P2)**: 인쇄 프리뷰는 phase2 (Sobo46_billing).
- **O**: §6 — Sobo46/49 인쇄·세금계산서 (Phase 2).

### §T. Sobo47_billing 청구금액(년월)

- 5축 PASS. 년월 단위 합계 그리드.
- **O**: 인쇄, 거래처별 분배.

### §U. Sobo41_cash 입금내역

- 5축 PASS. CRUD 입금 등록·수정·취소.
- **O**: 영수증 인쇄 (Phase 2).

### §V. Sobo42_cash 입금현황

- 5축 PASS. variant=hcode/sdate 통합 (DEC-019). Sobo42_1 단일 라우트 분기.
- **deltas (P2)**: 거래처별 vs 일자별 라디오 (모던 신설).
- **O**: 인쇄, 외부 PG 연동.

### §W~§AB. DEC-049 billing IA 별칭 6 폼 (Sobo45_billing_bill / Sobo45_1_billing_bill / Sobo47_billing_bill / Sobo41_cash_bill / Sobo42_cash_bill / Sobo42_1_cash_bill)

- 5축 PASS — **정본 라우트와 동일 컴포넌트** 를 사이드바 IA 별칭으로 노출만 추가. 코드/매핑 노트는 정본(Sobo45_billing/47_billing/41_cash/42_cash/42_1_cash) 단일 원천.
- **O**: §6 — 모든 OOS 항목 정본 매핑 노트와 동일.

### §AC. WebAdmHome 관리 대시보드 (Wave D)

- W/B/U/D/O = **OOS** (DFM 부재, DEC-022 OOS-MAS-1 신규 도메인). 본 폼은 dfm→html 매핑 의무 없음 (.cursor/rules/dfm-layout-input.mdc §"Wave D 예외").
- **B**: PASS — `admin_service.summary()` + 카드 5종 (사용자/서버/역할/권한/감사). 5축 평가는 Wave D 신규 도메인 contract 기준.

### §AD. WebAdmUserSrv 사용자·서버 매핑 (Wave D)

- W=OOS / B=PASS / U=PASS / D=PASS / O=PASS — DEC-052 라디오 단일 선택. `setPrimaryServer` 신규. 헤더 미설정 경고 배지(DEC-052) 동기.

### §AE. WebAdmRBAC 역할/권한 (Wave D)

- W=OOS / B=PASS / U=PASS / D=PASS / O=PASS — C10 Phase 1 (DEC-041/042/043) 역할 4종(admin/branch_manager/auditor/operator) 매트릭스.

### §AF. WebAdmEnv 환경설정(개정) (Wave D)

- W=OOS / B=PASS / U=PASS / D=PASS / O=PASS — Sobo19 레거시 환경설정과 분리(DEC-019). 본 화면은 모던 플랫폼 설정.

### §AG. Subu10_id_logn 사용자·권한 (F11~F89)

- 5축 PASS — Id_Logn.md §3·§4 부착. 메뉴 코드 F11~F89 매트릭스 풀 매핑. C10 Phase 1 풀 스코프(DEC-041/042/043).
- **deltas (P2)**: ETag 낙관적 동시편집 (모던 신설).
- **O**: 사용자별 비밀번호 회전 로그 그리드 (Phase 2 — `WebAdmAuditRotate`).

## 4. 발견 항목 처리 — HA-RET-02 후속 등록

본 사이클 발견 GAP-P0 = **0**, GAP-P1 = **0**, GAP-P2 = 15 (모두 §7 deltas 에 의식적으로 기록된 모던 신설 항목 — 의식적 차이이므로 retrofit 대상 아님).

따라서 `dashboard/data/human-action-items.json` 에는 **HA-RET-02 (audit-driven retrofit)** 를 신규 등록하되 **목록 = 비어 있음(0건)** 으로 둔다. 사이클 의무: 신규 결정/백엔드 변경/사용자 보고 발생 시 본 매트릭스를 재실행하고, 그 시점에 P0/P1 발견되면 동일 ID 에 항목 추가.

## 5. 회귀 가드 — Cursor rule + DEC-053 + DEC-028 보강

- **DEC-053 (신규)**: phase1 승격 전 본 매트릭스 갱신 + GAP-P0 = 0 가드.
- **DEC-028 (보강 1줄)**: phase1 승격 시 본 매트릭스 검증 의무.
- **`.cursor/rules/dfm-layout-input.mdc` (보강 1줄)**: phase1 승격 전 본 매트릭스 갱신.

본 3 항목은 본 사이클의 [`legacy-analysis/decisions.md`](../../legacy-analysis/decisions.md) DEC-053 신규 + DEC-028 1줄 + cursor rule 1줄 추가로 적용된다.

## 6. 단일 원천 인용

- 위젯 표/TabOrder/이벤트 매핑/인쇄 절은 **`analysis/layout_mappings/<Sobo*>.md` 단일 원천** — 본 문서는 5축 한 단어 평가 + 매핑 노트 링크만 제공한다. 매핑 노트 변경 시 본 매트릭스의 PASS/OOS 표기를 동시 갱신해야 한다.
- 대시보드 (`dashboard/data/timeline.json`, `web-porting-progress.json`) 도 본 매트릭스 행만 인용한다.

---

*최종 업데이트: 2026-04-21 — phase1 33 폼 컴포넌트 동등성 재점검 매트릭스 동결 (GAP-P0 = 0). DEC-053 신규 + DEC-028 §결정 1줄 보강 + dfm-layout-input.mdc §회귀 가드 1줄 추가. HA-RET-02 후속 ID 예약 (현재 항목 0).*
