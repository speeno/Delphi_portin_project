# Phase 2 → Phase 1 승격 후보 (5축 게이트 적용)

**ID**: PHASE2-PROMOTION-CANDIDATES
**일자**: 2026-04-21
**연관 문서**:
- [`docs/phase1-promotion-gate.md`](../../docs/phase1-promotion-gate.md) §2 (5축 정의)
- [`reports/phase2-regression-2026-04-21.md`](../../reports/phase2-regression-2026-04-21.md) (라이브 baseline)
- [`dashboard/data/phase2-screen-cards.json`](../../dashboard/data/phase2-screen-cards.json) (단계 카드)
- 사용자 정책: "테스트 및 동작이 레거시코드 비즈니스로직 및 쿼리 등이 적절하게 동일성을 갖게 적용이 완료되고 테스트가 완료된 이후에 녹색 표시"

---

## 0. 결론

본 PR(F1~F6) 시점에서 **5축 모두 PASS 상태인 화면은 0건** — `phase: "phase2" → "phase1"` 승격은 **0건**.

근거:
1. **data 축 (4대 DB cross-DB invariant)** 측정이 환경 미등록(`Unknown server id 'mysql8'`)으로 SKIP 상태 — 32 화면 모두 적용.
2. **functional 축**: 32 화면 중 1 PASS (`WebAdmAudit`), 2 SKIP, 29 FAIL (404 라우트 미등록 20 + 422 스키마 5 + 500 DB 미등록 2 + 0 transport 3).
3. **audit 축**: read-only 화면 26개 NA, write 화면 6개 (`WebAdmAuditRotate`/`Sobo46_billing`/`Sobo49_tax`/`Sobo28_delivery`/`Sobo41_slip`/`Sobo16_special`) 는 별도 phase2 audit 테스트 필요.

따라서 **사용자 정책에 따라 본 PR 은 `form-registry.ts` 의 `phase` 필드를 변경하지 않는다.** 사이드바 녹색 체크는 phase1 12 화면 기존 상태 그대로 유지.

---

## 1. 승격 후보 분류 (이론적 — 환경 등록 후 검증 필요)

phase2-screen-cards.json 의 `tasks.T7` 가 `done` 인 화면이 5축 후보. 본 PR 시점은 모두 `in_progress` (T7 회귀 진행 중).

### 1.1 Tier A — 백엔드·프론트 완료, T7 진행 중 (12 화면)

dashboard `tasks` 가 `T1~T6 == done` 인 화면. 4대 DB 환경 등록 + cross-DB invariant PASS 시 즉시 승격 가능.

| 화면 | 라우트 | 비고 |
|---|---|---|
| `Sobo54` | `/inbound/reports/daily` | 백엔드+프론트 done — 422 (러너 query 보강) |
| `Sobo57` | `/inbound/reports/period` | 백엔드+프론트 done — 500 (DB 미등록) |
| `Sobo34_4` | `/returns/ledger` | 백엔드+프론트 done — transport 0 (라우터 매핑 누락) |
| `Sobo58` | `/returns/period-report` | 백엔드+프론트 done — 404 (라우터 path 차이) |
| `Sobo49_tax` | `/settlement/tax-invoice` | 백엔드+프론트 done — 422 |
| `Sobo50_stats` | `/stats/sales-period` | 백엔드+프론트 done — 422 |
| `Sobo51_stats` | `/stats/customer-analysis` | 백엔드+프론트 done — 500 |
| `Sobo52_stats` | `/stats/book-turnover` | 백엔드+프론트 done — 422 |
| `Sobo53_stats` | `/stats/quarterly-summary` | 백엔드+프론트 done — 422 |
| `WebAdmOps` | `/admin/ops` | 백엔드+프론트 done — 200 OK (response_keys 미부합 FAIL) |
| `WebAdmAudit` | `/admin/audit` | 백엔드+프론트 done — **PASS** ✅ (1차 단일 PASS) |
| `WebAdmAuditRotate` | `/admin/audit-rotate` | POST-only SKIP — 별도 audit 테스트로 검증 |

> Tier A 12 화면은 본 PR 의 추가 보강(F2-라우터 매핑 / 러너 query 정밀화)으로 PASS 전환 가능.

### 1.2 Tier B — T5 백엔드 done, T6 프론트 in_progress (15 화면)

```
Sobo46_billing, Sobo67_status, Sobo44_inv,
Sobo32_ledger, Sobo32_1_ledger, Sobo33_ledger, Sobo33_1_ledger,
Sobo21_status_list, Sobo21_status_summary, Sobo21_status_memo,
Settle_outstanding, Sobo41_slip,
Stats_monthly, Sobo36_stats_route, Sobo37_stats_route
```

T6 프론트 통합 후 T7 회귀 + cross-DB PASS 시 승격.

### 1.3 Tier C — Blocker 보유 (5 화면)

`Sobo48_compare`, `Sobo16_special`, `Sobo29_other`, `Sobo28_delivery`, `Sobo43_stats_route` — `scenario.blockers` 명시.

본 5건은 blocker 해소 전까지 phase1 승격 비대상. `_stub.py` 503 NOT_IMPLEMENTED 응답으로 운영.

---

## 2. 승격 진입 체크리스트 (운영자용)

화면 단위로 다음을 모두 충족 시 PR 에서 `form-registry.ts` 의 `phase: "phase2" → "phase1"` 단일 변경 + 사이드바 녹색 체크 자동 노출.

```
[ ] 1. dashboard/data/phase2-screen-cards.json 의 해당 화면 tasks.T7 == "done"
[ ] 2. test_regression_phase2.py --multi-db --servers mysql3 mysql5 mysql8 maria
       에서 functional+data+performance == PASS
[ ] 3. write 화면이면 audit 축 별도 테스트 PASS (test_<domain>_audit.py)
[ ] 4. UI 축: layout_mappings/<Form>.md 가 존재 (선택 — 시각 회귀 도구)
[ ] 5. blocker 미보유 (scenario.blockers == [])
[ ] 6. PR description 에 본 5축 결과 첨부 (regression JSON link)
```

---

## 3. 4대 DB 환경 등록 후 재실행 명령

```bash
# 1. 환경변수 / 설정에 mysql3 / mysql5 / mysql8 / maria 4 server_id 등록
#    (도서물류관리프로그램/backend/app/db/server_registry.py 또는 BLS_DB_SERVERS)

# 2. 라이브 회귀 (4대 동시)
PYTHONPATH=도서물류관리프로그램/backend RUN_DB_SMOKE=1 \
  python3 test/test_regression_phase2.py \
    --servers mysql3 mysql5 mysql8 maria --multi-db \
    --write-json reports/phase2-regression-$(date +%F)-multidb.json

# 3. 결과 분석 + 본 문서 §1 갱신 + form-registry.ts 단일 변경 PR
```

---

## 4. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 1차 작성. 0건 승격. Tier A 12 / Tier B 15 / Tier C 5. 4대 DB 환경 등록 + cross-DB PASS 후 재평가. |
