# Phase 1 Component Fidelity Audit (36 폼 전수)

> **사이클**: audit_only — 코드/UX 변경 0. 본 문서는 [`phase1_component_re-audit`](../../.cursor/plans/phase1_component_re-audit_7dd5dd8c.plan.md) 산출물 §3 매트릭스 + 폼별 §A~§AG 5축 표.
>
> **단일 원천 원칙** — Phase 1 승격 게이트(DEC-045)·dfm 공식 입력(DEC-028)·컴포넌트 동등성 정기 재점검(DEC-053) 모두 본 파일을 참조한다. 대시보드/cursor rule/PR 리뷰가 동일 매트릭스를 인용한다.

## 0. 스코프 — phase1 감사 대상 36 폼 (회귀 매트릭스)

`도서물류관리프로그램/frontend/src/lib/form-registry.ts` 의 `phase: "phase1"` 항목 중 **본 파일 §2 매트릭스에 편입된 폼** = **36 행** (2026-04-29: Sobo58, Sobo16_special, Sobo28_delivery 편입). phase2/preview/inbox 항목은 §2 범위 밖.

DFM 보유 폼 = **31** (Subu*) + DFM 부재 Wave D = **4** (`WebAdm*`, OOS-MAS-1, DEC-022).

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

## 2. 인벤토리 + 매핑 매트릭스 (39 행)

| # | form | route | menu | mapping | W | B | U | D | O | P0 | P1 | P2 | note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Sobo11 | /master/customer | master | [Sobo11.md](../layout_mappings/Sobo11.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 거래처 마스터 — Edit101 G1_Gbun-only 콤보·조인 정합, 구분 CRUD 접기(상세 통합, 2026-05) |
| 2 | Sobo14 | /master/book | master | [Sobo14.md](../layout_mappings/Sobo14.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 도서 마스터 — Edit101 G4_Gbun-only 콤보·이중 조인 정합, 분류 CRUD 접기(상세 통합) + 삭제(Button103) 복원 |
| 3 | Sobo17 | /master/publisher | master | [Sobo17.md](../layout_mappings/Sobo17.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 출판사·출고거래처 마스터 |
| 4 | Sobo38 | /master/book-code | master | [Sobo38.md](../layout_mappings/Sobo38.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | 도서코드 마스터 |
| 5 | Sobo39 | /master/discount | master | [Sobo39.md](../layout_mappings/Sobo39.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 할인율 — variant(base/v1/v2/v5) CRUD + `?type=` 별칭 호환 + 검색진행 상태 보강 |
| 6 | ~~Sobo45~~ | ~~/master/logistics-cost~~ | ~~master~~ | [Sobo45.md (DEPRECATED)](../layout_mappings/Sobo45.md) | DEP | DEP | DEP | DEP | DEP | 0 | 0 | 0 | **DEPRECATED 2026-04-23 (DEC-060)** — 「Sobo45 = 물류비」 매핑 추정 오류. 레거시 Subu45 = 청구서관리(Sobo45_billing, `/settlement/billing`) 가 정상. G5_Ggeo.Gposa 는 청구서관리 내부 lookup 으로 흡수. master_data.yaml v1.2.0 catalog/endpoint/customer_variants 동시 제거 |
| 7 | Sobo22 | /inbound/receipts | shipment | [Sobo22.md](../layout_mappings/Sobo22.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 입고접수 — Sobo22/22_1/22_2 변형 통합 (DEC-019) |
| 8 | Sobo22_import | /inbound/import | shipment | [Sobo38_inbound.md](../layout_mappings/Sobo38_inbound.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | Sobo38 의 입고 파일 업로드 분기 — 단일 입력 화면 |
| 9 | Sobo27 | /outbound/orders | shipment | [Sobo27.md](../layout_mappings/Sobo27.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 출고접수 — Sobo27/27_1 변형 통합, 종료일 deltas |
| 10 | Sobo21 | /transactions/sales-statement | transactions | [Sobo21.md](../layout_mappings/Sobo21.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 거래명세서 — 「거래관리」(Menu200) IA 정합으로 shipment→transactions 이동, DEC-017 인쇄 후속 |
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
| 34 | Sobo58 | /returns/period-report | returns | [Sobo58.md](../layout_mappings/Sobo58.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 기간별반품내역서 — C4 phase2 API + DEC-028 회귀 (`test_c4_returns_phase2`, `test_returns_period_ledger_regression`) |
| 35 | Sobo16_special | /master/special | master | [Sobo16.md](../layout_mappings/Sobo16.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 특별관리 — G6_Ggeo 조회 + 신규/수정/삭제 + 거래처/도서 검색축 lookup 보강 |
| 36 | Sobo28_delivery | /shipping/courier | delivery | [Sobo28.md](../layout_mappings/Sobo28.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | 택배관리 — 내부 라인/메모 완료, 외부 택배사 API 후속 (`test_sobo28_courier_legacy_ids`) |
| 37 | Sobo12 | /master/inbound-vendor | master | [Sobo12.md](../layout_mappings/Sobo12.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 1 | **Phase F** 입고처관리(G2_Ggwo/G2_Gbun) — 상세/구분 전체 필드 CRUD(Edit101~132, Edit201~202) + F12 caps + traceability 회귀 가드 |
| 38 | Sobo15 | /master/etc-customer | master | [Sobo15.md](../layout_mappings/Sobo15.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | **Phase F** 기타거래처(G5_Ggeo 출판/총판 정본) — F15 caps·G1↔G5 빌드변형 customer_variants. 거래처(Sobo11) 동형 패턴으로 본 폼 Panel002(Edit101~127·비율·발행유무) 전체 + G5_Gbun 구분 CRUD 복원, 목록/상세/신규 분리 라우트. g5_ggeo_adapt 멀티 DB |
| 39 | Sobo13 | /master/author | master | [Sobo13.md](../layout_mappings/Sobo13.md) | PASS | PASS | PASS | PASS | OOS | 0 | 0 | 0 | **Phase F** 저자관리(G3_Gjeo, 표시명 Gposa) — F13 caps. 본 폼 Panel002(Edit101~121) 전체 + G3_Gbun 구분 CRUD 복원, 목록/상세/신규 분리 라우트(거래처 패턴). 4서버 "김" 라이브 검증(138/153 PASS, 154/155 서버측 1129 block) |

### 2.1 합계 (P0/P1/P2)

| 합계 | 값 |
| --- | --- |
| Phase1 폼 | **39** |
| GAP-P0 (작업 차단) | **0** ✅ |
| GAP-P1 (데이터 누락) | **0** ✅ |
| GAP-P2 (UX 차이 / deltas 의 모던 신설 안내) | **20** (모두 매핑 §7 deltas 에 명시 — 의식적 차이) |
| OOS (의식적 비포함) | 39 폼 모두 §6 OOS 항목 보유 (Wave D 4 = 폼 전체 OOS) |

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

Sobo67_status 는 기존 승격 근거로 유지한다. 본 사이클에서는 Sobo58, Sobo16_special, Sobo28_delivery 를 §2 매트릭스에 추가 편입했다.

### 2.4 거래관리(Menu200 / ACC-MENU-NAV-02) 메뉴 IA 정합 (2026-05-31)

레거시 2번째 대메뉴 「거래관리」 스크린샷 구조를 모던 사이드바와 1:1 정합. 사이드바
그룹 라벨 「거래현황」→「거래관리」, `TRANSACTIONS_SIDEBAR_LAYOUT` 로 명세서 3종 →
거래/입고 현황 서브그룹 → 출고검증 3종 → 제작·원천·저자 → 신간발행 순서·구분선 보존.

| 화면 | route | 상태 | 비고 |
| --- | --- | --- | --- |
| 거래명세서 Sobo21 | /transactions/sales-statement | phase1 | shipment→transactions 이동 (중복 노출 제거) |
| 거래현황(상세) Sobo21_status_detail | /transactions/status?view=detail | phase1 | view=detail facade(=list 형태) + 행 펼침 라인 지연 조회(기존 detail API 재사용, 신규 SQL 0) |
| 입고명세서 Sobo22_inbound_statement | /transactions/inbound-statement | **phase1 (C1)** | Subu22 publisher Menu202 — `list_receipts` 재사용 facade(신규 SQL 0) + DBGrid101 9컬럼 펼침. 입고접수(C3)와 라우트 분리(Sobo22.md §7.1) |
| 입고현황 3뷰 Sobo25_status_* | /transactions/inbound-status?view=* | **phase1 (C2)** | Publisher 정본 publisher_source_root/Subu25(caption 입고현황) 재추출로 P0 해제. list/detail=list_receipts·summary=period_report 재사용 facade(신규 SQL 0). Sobo25_inbound_status.md |
| 출고검증 Sobo59_1/2/3 | /transactions/verification?v=* | **phase1 (C3·C4·C5)** | verification_service: GET 그룹 LIST(S1_Ssub Gubun='출고'·Ocode='B'·Scode='X', v=1 요약 R / v=2·individual 검증) + PATCH confirm/cancel(S1_Chek INSERT Yesno='1' / UPDATE Check='D', Subu59_2 Button102/103 동등). 검증 키 7컬럼. Sobo59_2.md |
| 제작명세/현황 Sobo26/27_* | /transactions/production/* | **phase1 (C6·C7)** | Publisher 정본 publisher_source_root/Subu26(제작명세서)·Subu27(제작현황) 재추출로 P0 해제. production_service(S2_Ssub, Ycode 색인, s2_ssub_adapt). 조회 전용 R. Sobo26/27_*.md |
| 원천징수 Sobo28_withholding | /transactions/withholding | **phase1 (C8)** | Publisher 정본 publisher_source_root/Subu28(원천징수관리) 재추출로 P0 해제. withholding_service(S3_Ssub, 저자명 G3_Gjeo.Gposa, s3_ssub_adapt). 조회 전용 R, 인쇄 OOS. Sobo28_withholding.md |
| 내역조회(저자) Sobo_author_history | /transactions/author-history | **phase1 (C10)** | Publisher MySQL/Subu26_1(내역조회(저자)-거래현황) 정본 publisher_source_root 재추출로 P0 해제. author_history_service(S1_Ssub 라인 Scode='X' + G4_Book.Gjeja). Sobo_author_history.md |
| 신간발행 Sobo29_new_release | /transactions/new-release | **phase1 (C9)** | `list_other_statements(jubun='신간')` 재사용 facade(신규 SQL 0) + 전체메모 재사용. 기타명세서와 전표구분만 다른 단일 폼 |

> scaffold = 라우트 + 사이드바 진입 + `ScreenPlaceholder`(시나리오·legacy_form 표시). 백엔드 SQL/계약은
> Phase 3·4 후속(고급 모델 권장 구간). phase1 승격은 화면별 5축 PASS + layout_mappings·`data-legacy-id` 검사 통과 후.
> **블록** 표시는 P0 조사(`analysis/audit/transactions-menu200-p0-form-mapping.md`)에서 Publisher 정본 DFM 부재가
> 확인된 화면 — `dfm-layout-input.mdc`(정본 DFM=공식 입력)에 따라 정본 확보 전 phase1 승격 금지.
> 회귀 가드: `test/test_transactions_sidebar_layout.py`(static IA), `test/test_shipment_sidebar_layout.py`(물류 IA),
> `test/test_c6_inquiry_phase2.py::test_view_detail_equivalent`(view=detail), `test/test_inbound_statement_phase1.py`(C1 facade·위젯),
> `test/test_new_release_phase1.py`(C9 신간 facade·전표구분 고정·위젯).

### 2.5 배본처관리 Sobo16_baebon — 운영 UI 감춤(2026-05)

운영 요청으로 「배본처관리」(Sobo16_baebon)를 **사이드바(`MASTER_SIDEBAR_LAYOUT`)·기초관리 허브(`master/page.tsx` 카드)** 에서 감췄다.

| 항목 | 처리 |
| --- | --- |
| 사이드바 | `MASTER_SIDEBAR_LAYOUT` 에서 항목 제거 |
| 기초관리 허브 | `MASTER_CARDS` 배본처 카드 제거 |
| registry menuId | `ACC-MENU-MASTERS-07` → `ACC-MENU-HIDDEN-MASTER-BAEBON` (show-first → `visible=false`, Sobo22_import 와 동일 패턴) |
| route `/master/baebon` | **유지** (북마크·운영 URL 직접 접근) |
| API·phase1 구현 | **유지** (기능 삭제·API 제거 아님 — 필요 시 내부/후속 재노출) |

> 기능·API·phase1 정합은 그대로 유지되므로 §2 매트릭스 합계·GAP-P0 영향 없음 (UI 노출 정책 변경만).
> 회귀 가드: `test/test_master_sidebar_layout.py`(layout 순서·HIDDEN menuId·route 유지).

### 2.6 출고관리(물류 셸 · Menu200/ACC-MENU-NAV-09) 사이드바 IA (2026-05-31)

물류 셸 「출고관리」를 `SHIPMENT_SIDEBAR_LAYOUT` 단일 원천으로 정렬했다. Publisher 「거래관리」
(transactions·NAV-02)와 동일 업무 화면은 **단일 route/API** 를 공유하되, 물류 셸 노출은
얇은 별칭(`*_shipment_alias`)으로만 추가한다 (DEC-049 billing 별칭과 동일 정책 — 정본은 transactions).

| 영역 | 폼 | route |
| --- | --- | --- |
| 자체 물류 | 출고접수 `Sobo27` / 출고현황 `Sobo67_status` / 입고접수 `Sobo22` | `/outbound/orders`·`/outbound/status`·`/inbound/receipts` |
| 공유 별칭 | 거래명세서·입고명세서·출고검증·신간발행 | `/transactions/*` (정본 동일) |

> **동시 노출 금지**: 일반 사용자는 RBAC 매트릭스상 NAV-02(publisher) 또는 NAV-09(물류) 중 한쪽만
> 가시하므로 두 그룹이 동시에 보이지 않는다(슈퍼유저 예외). 별칭은 배열상 정본 뒤에 두어
> `getFormByRoute` 가 항상 transactions 정본을 반환한다.
> 회귀 가드: `test/test_shipment_sidebar_layout.py`(layout 순서·별칭 route·NAV-09 게이트).

### 2.7 입고관리 대메뉴 신설 + 택배 한진 1차 (2026-06-01)

`inbound` 대메뉴를 신규 추가하고, 출고/거래에 흩어진 입고 항목을 `INBOUND_SIDEBAR_LAYOUT`
정본으로 재배치했다.

| 영역 | 항목 | route |
| --- | --- | --- |
| 입고접수 | Sobo22 | /inbound/receipts |
| 입고명세서 | Sobo22_inbound_statement | /transactions/inbound-statement |
| 입고현황 | Sobo25_status_list/detail/summary | /transactions/inbound-status?view=* |
| 입고내역서 | Sobo54 / Sobo57 | /inbound/reports/daily /period |
| 업로드(숨김) | Sobo22_import | /inbound/import |

추가로 Sobo28 택배관리는 `/api/v1/delivery/dispatch` 계층을 통해
운송장 저장 + 배송조회(한진 우선, 미설정/오류시 manual fallback)를 지원한다.
회귀 가드: `test/test_inbound_sidebar_layout.py`, `test/test_c2_delivery_dispatch.py`,
`test/test_hanjin_client.py`.

## 3. 폼별 5축 audit (31 DFM 폼 + 4 Wave D)

각 § 은 **2.5 매트릭스 1행 + 핵심 발견** 만 기록. 위젯 표·이벤트 매핑 등 풀 깊이는 `analysis/layout_mappings/<form>.md` (단일 원천) 가 가진다 — 여기서는 중복 기록 금지.

### §A. Sobo11 거래처관리 (master)

- **W**: PASS — Sobo11.md §3·§4 기준 목록(DBGrid101) + 상세/신규(Panel002·Panel004 통합: `Edit101` 드롭다운, `DBGrid201`, `Edit201/202`, `Button201~203`).
- **B**: PASS — `Subu11.pas`의 G1_Ggeo/G1_Gbun 저장·삭제 흐름을 `/api/v1/masters/customer*` + `/customer-categories*` CRUD로 복원. **H2_Gbun(지사)** 는 `Seok10` → `/customer/{gcode}/branches` CRUD + 거래명세서 `Edit106` 콤보 연동(2026-06).
- **U**: PASS — TabOrder hcode → hname → 조회 순(매핑 §3) 보존. 캘린더 OOS.
- **D**: PASS — `HCODE/HNAME/HTEL/HPOST/HBIGO` 1:1, 신설 `last_login`/`updated_at` 은 deltas.
- **O**: §6 — Edit107/108 출판사 검색·Panel004 자동알람 라디오·CornerButton Print/Bar 모두 OOS-MAS-2 (마스터는 read-only 인쇄 후속).

### §B. Sobo14 도서관리

- **W/B/U/D**: PASS — Sobo14.md §4·§4-1 기준 목록(DBGrid101) + 상세/신규(Panel002·Panel200 통합: `Edit101` 드롭다운, `DBGrid201`, `Edit201/202`, `Button201~203`). 본 폼 전체·재고 RO·체크박스 4종·NL ISBN. `g4_book_adapt` 멀티 DB.
- **O**: §6 Button103(삭제) UI 미노출(DEC-019)·Button701~703 라벨인쇄 (DEC-018 후속).

### §C. Sobo17 출판사·출고거래처

- 5축 PASS. DEC-019 폴더 변형(Subu17/Subu17_1/Subu17_a) 통합. 출고거래처 `OCODE` 와 출판사 `PCODE` 분리 폼 단일 라우트.
- **O**: 인쇄·라벨·출판사 그룹 통계.

### §D. Sobo38 도서코드

- 5축 PASS. Sobo38.md §3 — 단일 그리드 코드/명/구분.
- **deltas (P2)**: 모던 `usage_count` 컬럼 신설.

### §E. Sobo39 할인율(대표)

- 5축 PASS. variant `Sobo39_1/_2/_5` (할인율 2/기타/물류) 는 `variant` 정본 + `type` 별칭 호환으로 통합. 할인율 CRUD(등록/저장/삭제)와 검색진행 상태바를 phase1 운영 기준으로 반영.
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
- 2026-06: 목록/신규/상세 라인 입력에 `MasterLookupField`(publisher/book) 공통 검색창 적용.
- **deltas (P2)**: 종료일·거래처 코드·취소 포함·DataGridPager 모두 §7 명시. Subu27 vs Subu27_1 = UI diff 0행, 로직 22행 차이는 `customer_variants` 흡수.
- **O**: §6 — 자동알람 Panel004, 신간 필터 Panel005, 출고증 인쇄 라디오 Panel011, 진행 ProgressBar Panel007, DBGrid 이미지 컬럼, 출판사 검색 Edit102~105.

### §J. Sobo21 거래명세서

- 5축 PASS. Sobo21.md §3·§4·§5 — 목록 하단 참조·메모 패널(공통 컴포넌트) + 상세 라인. `stock_qty` S1_Ssub SUM·`customer-preview` API. UPSERT Button801·주소가져오기 802. 목록 `gcode` variants IN·`gjisa`(Edit106)·지사 로드 오류 표시. 조회 가드 `CUSTOMER_SHIPPING_STOP`/`BRANCH_SHIPPING_STOP`.
- 2026-06: 목록 `gcode` = `MasterLookupField(customer)`; 상세 G1 참조 패널 + Button802 주소 가져오기; 메모 필드 라벨 pas 정본(비고1/2·핸드폰·받는사람·우편번호).
- **deltas (P2)**: 종료일·페이지네이터·상세 라우트 분리·메모 신규/수정 안내.
- **O**: §6 — Edit106 전표구분 콤보, 출판사 검색 4종, 인쇄/바코드(DEC-017/018), 재고·전일미수·RTF 툴바.

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

*최종 업데이트: 2026-05-30 — account-menu-fxx-rbac Phase F: Sobo12(입고처)·Sobo15(기타거래처)·Sobo13(저자) 3화면 편입, phase1 감사 대상 39 폼. GAP-P0 = 0. 직전: 2026-04-29 36 폼 (Sobo58/16_special/28_delivery).*
*메뉴 노출(MENUVIS-DEC-07, 2026-05-30): 위 3화면이 일부 계정에서 사이드바에 보이지 않던 원인은 `account_type` 미매핑 시 RBAC 매트릭스가 사이드바를 0건으로 만들던 것. show-first 전환으로 메뉴는 기본 전체 노출, 라이선스(Fxx) 미보유는 disabled, 감추기는 관리자 `/admin/id-logn` 사용자별 설정으로만 적용. 회귀 가드: `test/test_menu_visibility_show_first.py`, `analysis/audit/menu-visibility-show-first-baseline.json`.*
