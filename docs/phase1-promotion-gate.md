# Phase1 승격 게이트 (사이드바 녹색 체크 정의)

**ID**: PHASE1-PROMOTION-GATE
**일자**: 2026-04-21
**상태**: draft (DEC-NN 등록 전 1차 동결)
**연관 결정**: DEC-001(8계층 하네스), DEC-003(권장 포팅 순서), DEC-NN(승격 정의)

---

## 1. 배경

기존 `frontend/src/lib/form-registry.ts` 는 화면별 `phase` 값(`"phase1" | "phase2" | "preview"`) 으로
사이드바(`components/layout/sidebar.tsx`) 에서 다음과 같이 표시한다:

- `phase === "phase1"` → 녹색 체크 표시 (1차 포팅 완료)
- `phase === "phase2"` → 회색 dot (진행 중)
- `phase === "preview"` 또는 미설정 → 표시 없음

지금까지 `phase1` 은 **"UI 가 화면에 떠 있고 백엔드 라우트가 200 을 반환한다"** 수준에서 부여되었으나,
사용자 합격선("기존 사용자가 같은 결과를 얻는다") 과 괴리가 발생하였다.

본 게이트는 **"녹색 체크 = 레거시 동등성 + 자동 회귀 통과"** 로 정의를 강화하여
사이드바 표시가 비즈니스/QA 의 실제 수용 상태와 일치하도록 한다.

---

## 2. 승격 기준 (필수 5축)

화면이 `phase2 → phase1` 로 승격되려면 아래 **5축 모두** PASS 해야 한다.
(축 정의는 `migration/contracts/<flow>.yaml` 의 `equivalence:` 섹션과 동일)

| 축 | 기준 | 산출물 |
|---|---|---|
| **A. functional** | 정상·경계·실패 시나리오 모두 PASS. 레거시 이벤트 핸들러 분기와 1:1 매핑된 테스트가 존재. | `test/test_<flow>_phase1.py` 또는 `test/regression_phase1.py` 의 해당 케이스 |
| **B. data** | 4대 DB 서버(MySQL 3.23 / 5.x / 8.x / MariaDB) 모두에서 동일 입력→동일 raw row. EUC-KR/UTF-8 인코딩 처리 포함. | `migration/test-cases/<flow>.json` + `debug/probe_backend_all_servers.py` 결과표 |
| **C. ui** | 컬럼 라벨·정렬·필수 입력·기본값·페이지네이션이 레거시 dfm 과 동일. 한글 컬럼 라벨 100% 매핑. | `analysis/screen_cards/<Form>.md` §UI + 시각 회귀 스냅샷 (선택) |
| **D. audit** | INSERT/UPDATE/DELETE 1건마다 `audit_log` 1건. 호출자 identity(`sub`/`hcode`/`role`) 포함. | `app/services/audit_service.py` 통합 + 회귀 테스트의 audit assert |
| **E. performance** | 1만 행 응답 P95 < 800ms (페이지네이션 limit 100 기본). 5xx 재시도 0회. | `test/regression_phase1.py` 의 timing 리포트 |

> **부재 시**: 5축 중 하나라도 결측이거나 FAIL 이면 `phase` 는 `phase2` 유지.

---

## 3. T-Phase 워크플로우 (T1 ~ T8)

각 화면의 승격 절차는 다음 8단계를 순서대로 통과한다.

| 단계 | 명칭 | 산출물 | 통과 기준 |
|---|---|---|---|
| **T1** | screen_card | `analysis/screen_cards/<Form>.md` | 레거시 dfm/pas 의 컴포넌트·이벤트·SQL 인벤토리 100% |
| **T2** | event_sql_extract | T1 의 §데이터접근 + `migration/contracts/<flow>.yaml::data_access` | Subu*.pas 의 모든 SQL 문이 contract 의 SQL-* 항목으로 매핑 |
| **T3** | contract_yaml | `migration/contracts/<flow>.yaml` (1.x 동결) | inputs/outputs/endpoints/deltas/equivalence 5섹션 완비 |
| **T4** | api_impl | `backend/app/routers/<domain>.py` + `services/*` | contract 의 endpoints 와 1:1 (path/method/auth/스키마) |
| **T5** | ui_impl | `frontend/src/app/(app)/<domain>/<screen>/page.tsx` | contract.outputs 100% 표시 + ApiErrorBanner 사용 |
| **T6** | test_pack | `migration/test-cases/<flow>.json` + `test/test_<flow>_phase1.py` | 정상/경계/실패 7건 이상, 4대 DB probe 포함 |
| **T7** | equivalence_run | `test/regression_phase1.py` 결과 (`reports/regression-<date>.json`) | 5축 모두 PASS, 회귀 0건 |
| **T8** | promotion | `form-registry.ts` `phase: "phase2" → "phase1"` PR | T1~T7 산출물 PR description 첨부, 리뷰어 approve |

> **승격 PR 템플릿**: 본문에 T1~T7 산출물 7개 링크 + T7 결과 요약(5축 PASS/FAIL 표) 필수.

---

## 4. 사이드바 표시 정책

`components/layout/sidebar.tsx` 의 표시 규칙을 다음으로 명문화한다 (코드 변경 없음 — 정책 문서화만).

```
form.phase === "phase1"  → ✓ (녹색)  // T8 통과 = 5축 PASS
form.phase === "phase2"  → ●  (회색)  // 작업 중 (T1~T7 중 어느 단계든)
form.phase === "preview" → 없음        // 메뉴 노출만, 인사이드 placeholder
미설정                    → 없음
```

**사용자 메시지**:
- 녹색 체크 옆에 hover tooltip 으로 "T7 통과: <YYYY-MM-DD> · 5축 PASS" 표시(향후 enhancement).
- placeholder 화면은 `screen-placeholder.tsx` 를 통해 "준비 중 (Phase 2)" 안내.

---

## 5. 강등 정책 (regression 발생 시)

이미 `phase1` 인 화면이 다음 중 하나에 해당하면 즉시 `phase2` 로 강등하고 사이드바 녹색 체크를 제거한다:

1. **회귀 테스트 FAIL**: `test/regression_phase1.py` 가 1회라도 FAIL.
2. **DB probe FAIL**: `debug/probe_backend_all_servers.py` 에서 4대 DB 중 하나라도 응답 불일치.
3. **레거시 동등성 위반 보고**: `legacy-analysis/` 내에 신규 deltas 가 추가되고 contract 미반영.
4. **5xx 비율 임계 초과**: 운영 모니터링에서 24h 5xx ≥ 1% (운영 단계 도입 후).

강등 시 별도 PR 로 `phase` 를 회귀시키고 강등 사유를 PR body 에 기록한다.

---

## 6. 12개 재사용 화면 — 1차 적용 대상

본 게이트의 **첫 적용군**(현재 phase=`phase2` 이며 백엔드 API 가 이미 동작하는 화면):

| # | flow_id | 화면 (UI 경로) | contract 파일 |
|---|---|---|---|
| 1 | C2-outbound | `outbound/status` | `migration/contracts/outbound_order.yaml` |
| 2 | C2-inventory | `inventory/status` | (신규 작성 — `inventory_status.yaml`) |
| 3 | C5-billing | `settlement/outstanding` | `migration/contracts/settlement_billing.yaml` |
| 4 | C5-billing | `settlement/payment-slip` | (위와 공유) |
| 5 | C6-sales | `transactions/status` | `migration/contracts/sales_inquiry.yaml` |
| 6 | C6-ledger | `ledger/customer` | (위와 공유) |
| 7 | C6-ledger-int | `ledger/customer-integrated` | (위와 공유) |
| 8 | C6-ledger | `ledger/book` | (위와 공유) |
| 9 | C6-ledger-int | `ledger/book-integrated` | (위와 공유) |
| 10 | C14-stats | `stats/monthly` | `migration/contracts/stats_reports.yaml` |
| 11 | C14-stats | `stats/customer` | (위와 공유) |
| 12 | C14-stats | `stats/book` | (위와 공유) |

> **현재 상태**: 12개 모두 `frontend/src/lib/form-registry.ts` 에서 `phase: "phase2"` 로 강등 또는 신설.
> T1~T7 통과 화면만 개별 PR 단위로 `phase: "phase1"` 승격 (`phase1_promotion_apply` 작업).

---

## 7. 운영 책임

- **승격 결정**: 메인개발자 + QA(레거시 담당자) 합의.
- **회귀 모니터링**: CI 의 `pytest test/regression_phase1.py` job 이 실패하면 자동 슬랙 알림.
- **문서 갱신**: 본 문서는 게이트 정책 변경 시 PR 단위 갱신, `decisions.md` 의 DEC-NN 와 동기.

---

## 8. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 최초 draft. 5축 + T1~T8 + 12개 1차 적용 대상 명시. |
