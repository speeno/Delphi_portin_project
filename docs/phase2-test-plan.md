# Phase 2 테스트 계획 (32화면 회귀 게이트)

**ID**: PHASE2-TEST-PLAN
**일자**: 2026-04-21
**상태**: draft (1차 baseline 적용)
**연관 결정**: DEC-045(phase1 승격 게이트), DEC-046(phase2 운영체계 단일원천), DEC-047(phase1 승격 0건 baseline), DEC-048(.frf B4 트랙 종결)
**연관 문서**:
- [`docs/phase1-promotion-gate.md`](./phase1-promotion-gate.md) (승격 게이트 5축 정의)
- [`migration/coverage/phase2-32screens-t1-t2-index.md`](../migration/coverage/phase2-32screens-t1-t2-index.md) (T1·T2 산출물 인덱스)
- [`migration/coverage/phase2-promotion-candidates.md`](../migration/coverage/phase2-promotion-candidates.md) (Tier A/B/C 분류 + 승격 체크리스트)
- [`migration/contracts/_phase2_screen_to_contract_map.yaml`](../migration/contracts/_phase2_screen_to_contract_map.yaml) (32 화면 ↔ 9 yaml 매핑)
- [`reports/phase2-regression-2026-04-21.md`](../reports/phase2-regression-2026-04-21.md) (라이브 baseline)

---

## 0. 목적

Phase 2 32 화면이 phase1 승격 게이트(DEC-045 의 5축) 를 통과하기 위한 **테스트 단일 원천 + 자동 회귀 절차** 를 정의한다.
Phase 1 게이트와 달리 **scenario.blockers 보유 화면(5건) 의 503 NOT_IMPLEMENTED 응답 허용** 과 **단일/멀티 DB 분리 실행 정책** 이 핵심 차이다.

---

## 1. 단일 원천 4축 (DEC-046)

| 원천 | 파일 | 역할 | 동기 책임 |
|---|---|---|---|
| **시나리오** | `frontend/src/lib/form-registry.ts::FormMeta.scenario` | input/process/output/eta/blockers 5필드 | 사이드바·placeholder·dashboard 가 본 객체만 읽음 |
| **단계 카드** | `dashboard/data/phase2-screen-cards.json` | 32 × T1~T8 status (done/in_progress/pending/blocked) | dashboard `renderPhase2ScreenCards` 가 본 JSON 만 렌더 |
| **계약 매핑** | `migration/contracts/_phase2_screen_to_contract_map.yaml` | 32 화면 → 9 yaml + COVERED/COVERED+/NEW 분류 | 신규 yaml 추가 시 본 매핑 필수 갱신 |
| **회귀 그룹** | `test/test_regression_phase2.py::_phase2_groups` | scenario+단계카드 동적 로드 → GroupSpec 32건 | screen-cards JSON 변경 즉시 반영 |

> **금지 사항**: 위 4축 외부에 시나리오·단계 정보 중복 보존 ❌. 단일 원천 위반은 PR 리뷰에서 차단.

---

## 2. 5축 매트릭스 (Phase 2 변형)

| 축 | Phase 1 기준 (DEC-045) | Phase 2 변형 | 산출물 |
|---|---|---|---|
| **A. functional** | 정상·경계·실패 시나리오 PASS | 동일 + **blocker 화면은 503 PASS 로 인정** | `migration/test-cases/<flow>.json` (32 그룹 × 3+ 케이스) |
| **B. data** | 4대 DB cross-DB invariant | 동일. **단일 server 결과는 baseline 만, PASS 미인정** | `--multi-db --servers mysql3 mysql5 mysql8 maria` 결과 |
| **C. ui** | dfm 컬럼/정렬/입력 1:1 | 동일. **레이아웃 매핑 산출물 옵션** (대시보드 표시만 필수) | `analysis/screen_cards/<Form>.md` §UI |
| **D. audit** | INSERT/UPDATE/DELETE 1건당 audit_log 1건 | 동일. **read-only 26 화면은 N/A** / write 6 화면은 별도 audit 테스트 | `audit_axis_na=False` 그룹 표시 |
| **E. performance** | P95 < 800ms | **P95 < 1200ms** (신규 SQL 미튜닝 보정 — 승격 시 800ms 재측정 의무) | runner 의 timing 리포트 |

### 2.1 Phase 2 전용 정책

- **blocker 허용**: `scenario.blockers != []` 화면(5건 — `Sobo48_compare`/`Sobo16_special`/`Sobo29_other`/`Sobo28_delivery`/`Sobo43_stats_route`) 은 200 또는 503 모두 PASS. 단, 승격 게이트 진입 전 blocker 해소 의무.
- **write-only 화면**: POST/PATCH 단일 엔드포인트 화면(`WebAdmAuditRotate` 등) 은 GET probe SKIP. 별도 audit 테스트로 검증.
- **단일 server 실행**: dev/CI 환경 단일 server 실행은 **baseline 측정만** — phase1 승격 비대상.

---

## 3. T1~T8 단계 (Phase 2 적용)

Phase 1 (DEC-045 §3) 의 T1~T8 워크플로우와 동일하나, **T7 통과 = data 축 cross-DB PASS 의무** 가 강화 적용.

| 단계 | 명칭 | Phase 2 산출물 | 통과 기준 |
|---|---|---|---|
| T1 | screen_card | `analysis/screen_cards/<Form>.md` (NEW 15) 또는 기존 카드 (REUSE 12+5) | dfm/pas 인벤토리 100% |
| T2 | event_sql_extract | `migration/contracts/<flow>.yaml::data_access` | 모든 SQL → contract SQL-* 매핑 |
| T3 | contract_yaml | yaml 1.x 동결 (신규 6 + 기존 보강 3) | inputs/outputs/endpoints/equivalence 5섹션 |
| T4 | api_impl | `backend/app/routers/<domain>.py` | endpoints 와 1:1 |
| T5 | ui_impl | `frontend/src/app/(app)/<domain>/<screen>/page.tsx` | outputs 100% + ApiErrorBanner |
| T6 | test_pack | `migration/test-cases/<flow>.json` | 화면당 3+ 케이스 |
| T7 | equivalence_run | `test/test_regression_phase2.py --multi-db` 결과 JSON | **5축 PASS + 4대 DB cross-DB invariant** |
| T8 | promotion | `form-registry.ts::phase: "phase2" → "phase1"` 단일 변경 PR | T1~T7 산출물 + 회귀 JSON 첨부 |

---

## 4. 회귀 러너 사용법

### 4.1 dryrun (계획 확인)

```bash
PYTHONPATH=도서물류관리프로그램/backend \
  python3 test/test_regression_phase2.py --allow-dry-run
```

- 32 그룹 × 1 server 의 GroupSpec 출력. HTTP 호출 0건.
- `_phase2_groups` 가 phase2-screen-cards.json 을 동적 로드 — 카드 추가/제거 시 자동 반영.

### 4.2 단일 server 라이브 (baseline)

```bash
PYTHONPATH=도서물류관리프로그램/backend RUN_DB_SMOKE=1 \
  python3 test/test_regression_phase2.py \
    --servers mysql8 \
    --write-json reports/phase2-regression-$(date +%F)-baseline.json
```

- functional + performance 축만 측정. data 축 SKIP.
- baseline JSON 은 PR description 첨부용. **승격 비대상**.

### 4.3 4대 DB cross-DB (승격 게이트)

```bash
# 사전: backend BLS_DB_SERVERS 또는 server_registry.py 에 4 server_id 등록
PYTHONPATH=도서물류관리프로그램/backend RUN_DB_SMOKE=1 \
  python3 test/test_regression_phase2.py \
    --servers mysql3 mysql5 mysql8 maria --multi-db \
    --write-json reports/phase2-regression-$(date +%F)-multidb.json
```

- 5축 모두 측정. JSON 의 `axis.data` PASS 시 phase1 승격 후보.
- 단일 화면 PR 단위로 결과 발췌 + form-registry.ts `phase` 단일 변경.

### 4.4 pytest 통합

```bash
RUN_REGRESSION_PHASE2=1 RUN_DB_SMOKE=1 \
  pytest test/test_regression_phase2.py -v
```

- CI 환경에서 자동 회귀 실행. dev 환경 default OFF (env var 미설정 시 SKIP).

---

## 5. 1차 baseline 결과 (2026-04-21)

`reports/phase2-regression-2026-04-21.md` 요약:

| 항목 | 값 | 비고 |
|---|---|---|
| 실행 환경 | mysql8 단일 server | `Unknown server id 'mysql8'` ValueError 발생 — 환경 미정비 |
| 전체 그룹 | 32 | scenario.blockers 5건 포함 |
| PASS | 1 | `WebAdmAudit` (200 OK + response_keys 충족) |
| SKIP | 2 | write-only 화면(POST 단독) |
| FAIL | 29 | 404 (라우터 매핑 차이) 20 + 422 (스키마 차이) 5 + 500 (DB 미등록) 2 + transport 0 (네트워크 0) 3 |

**결론 (DEC-047)**: phase2 → phase1 승격 0건. 4대 DB 환경 등록 + cross-DB PASS 후 Tier A 12 화면부터 재평가.

---

## 6. 승격 진입 체크리스트 (운영자용)

화면 1개 = PR 1개 원칙 (DEC-045 §6.4 동일). 다음 6항 모두 충족 시 `form-registry.ts` 의 `phase` 단일 변경 PR 발행.

```
[ ] 1. dashboard/data/phase2-screen-cards.json 의 해당 화면 tasks.T7 == "done"
[ ] 2. test_regression_phase2.py --multi-db --servers mysql3 mysql5 mysql8 maria
       에서 functional + data + performance == PASS
[ ] 3. write 화면이면 별도 audit 테스트 PASS (test_<domain>_audit.py)
[ ] 4. scenario.blockers == [] (blocker 미보유)
[ ] 5. analysis/screen_cards/<Form>.md (T1 카드) 존재
[ ] 6. PR description 에 5축 PASS 표 + 회귀 JSON 링크 + 변경 diff 첨부
```

> **금지**: 12 화면 일괄 승격 PR ❌ — DEC-045 §6.4 규정.

---

## 7. 강등 정책 (DEC-045 §5 동일)

이미 phase1 인 화면이 다음 중 하나에 해당하면 즉시 phase2 강등 + 사이드바 녹색 ✓ 제거:

1. `test_regression_phase2.py --multi-db` 1회라도 FAIL
2. 4대 DB probe 1회라도 응답 불일치
3. 운영 5xx ≥ 1% (24h)
4. 신규 deltas 발견 + contract 미반영

---

## 8. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 최초 draft. DEC-046/047 적용. 1차 baseline (1 PASS / 2 SKIP / 29 FAIL) 등록. Tier A/B/C 분류 + 4대 DB 환경 등록 후 재평가 명령 동결. |
