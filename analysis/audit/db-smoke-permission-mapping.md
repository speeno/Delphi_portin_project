# 라우터별 권한 매핑·예외 분류 (DB 스모크 베이스라인)

_작성: 2026-05-04 — [`../포팅_완결_우선_계획_672e6c6a.plan.md`](../포팅_완결_우선_계획_672e6c6a.plan.md) §1 "스모크 DoD 확정 및 구현" 의 입력 자료_

> 본 메모는 `debug/probe_backend_all_servers.py` 의 live 스모크 결과(베이스라인 1회) 와 백엔드 라우터 코드의 인증·권한 의존성 인벤토리를 정적으로 매칭해 **그룹별 실패 원인 분류**를 산출한다. 후속: 옵션 A는 **DEC-062** 로 코드·런북에 반영되었다 (슈퍼유저 `get_current_user`/`get_user_context` 동시 override).

## 1. 산출 데이터 (artifacts)

| 파일 | 설명 |
|---|---|
| `artifacts/db-smoke-baseline.json` | 4대 서버 × 67그룹 raw 결과 (status/detail/body 머리) |
| `artifacts/router-auth-inventory.json` | 라우터 파일별 prefix · router-level deps · 라우트별 (메서드, 경로, route-level deps, 함수 시그니처 deps) |
| `artifacts/permission-mapping-classification.json` | 그룹 ↔ 라우트 ↔ 요구권한 ↔ 분류 라벨 |

## 2. 베이스라인 요약 (live)

- L2: 4대 서버 모두 `SELECT 1` 성공 (mysql3 138/153 = mysql>=4, 154/155 = mysql3 protocol).
- L4: **268건 중 100건 OK (4 서버 × 67 그룹 → 매트릭스가 전부 동일 패턴)**.
- 그룹 단위 분류:

| 분류 | 그룹 수 | 비고 |
|---|---:|---|
| PASS | 23 | dashboard.external.\*, stats.\* 일부, common.\*, ownership/auth-expired 음성 검증 등 |
| AUTH/direct-get_current_user | 28 | 라우트 본함수에 `Depends(get_current_user)` 직접 사용 → smoke ctx override 안 먹음 |
| AUTH/매칭실패(동일 패턴) | 9 | `returns.py` / `settlement.py` 에 `audit_router` 보조 APIRouter 가 한 파일 내 공존해 인벤토리 정적 매칭 실패. 코드 grep 으로 `_user=Depends(get_current_user)` 직접 의존 100% 확인 → **AUTH/direct 와 동일 부류** |
| PERMISSION/admin.user.read | 2 | smoke ctx 의 `permissions` 에 admin.user.\* 미포함 → `require_permission` 가드 403 |
| EXPECTED-OK | 2 | ownership.violation.expected_403, auth.expired_must_401 — 가드가 의도대로 작동 |
| EXPECTED-FAIL/PERM-PRE-EMPTS-\* | 2 | `must_409`/`must_428` 음성 검증이 권한 가드 (admin.user.write) 에 선차단되어 403 으로 떨어짐 — 매트릭스 의도와 다름 |
| EXPECTED-FAIL/401 | 1 | `print.return_receipt_pdf_variant_v4_must_422` 가 422 도달 전에 401 — 동일하게 `Depends(get_current_user)` 게이트가 우선 |

> 모든 실패가 4대 서버에서 **동일하게** 같은 status 로 떨어진다. 즉 베이스라인의 실패는 **스키마/테넌트 차이가 아니라 인증·권한 우회 매트릭스의 누락**이다 (DEC-033 §DoD 의 "알려진 스키마 차이" 예외와 무관).

## 3. 라우터별 인증·권한 의존성 인벤토리

| 라우터 파일 | prefix | router-level dep | 라우트 수 | direct `get_current_user` | via `get_user_context` | `require_permission` 라우트 | 사용 권한코드 |
|---|---|---|---:|---:|---:|---:|---|
| admin.py | /api/v1/admin | – | 39 | 12 | 25 | 24 | admin.user.read, admin.user.write |
| admin_whitelist.py | /api/v1/admin/whitelist | – | 8 | 8 | 0 | 0 | – |
| auth.py | /api/v1/auth | – | 3 | 1 | 0 | 0 | – |
| courier.py | /api/v1/shipping/courier | require_server_ownership(serverId) | 3 | 3 | 0 | 0 | – |
| dashboard_external.py | /api/v1/dashboard/external | require_server_ownership(serverId) | 11 | 0 | 0 | 0 | – |
| inbound.py | /api/v1/inbound | require_server_ownership(serverId) | 8 | 8 | 0 | 0 | – |
| integrations_nl.py | /api/v1/integrations/nl | require_server_ownership(serverId) | 4 | 0 | 0 | 0 | – |
| inventory.py | /api/v1/inventory | require_server_ownership(serverId) | 1 | 1 | 0 | 0 | – |
| ledger.py | /api/v1/ledger | require_server_ownership(serverId) | 4 | 4 | 0 | 0 | – |
| masters.py | /api/v1/masters | require_server_ownership(serverId) | 17 | 17 | 0 | 0 | – |
| me.py | /api/v1/me | – | 8 | 8 | 0 | 0 | – |
| ops.py | (none) | – | 7 | 0 | 1 | 7 | admin.audit.read, admin.health.read, admin.metrics.read |
| outbound.py | /api/v1/outbound | require_server_ownership(serverId) | 6 | 6 | 0 | 0 | – |
| print.py | /api/v1/print | require_server_ownership(serverId) | 6 | 6 | 0 | 0 | – |
| public_lookup.py | /api/v1/public | – | 4 | 0 | 0 | 0 | – |
| public_signup.py | /api/v1/public | – | 3 | 0 | 0 | 0 | – |
| reports.py | /api/v1/reports | require_server_ownership(serverId) | 3 | 3 | 0 | 0 | – |
| returns.py | /api/v1/audit (※ `router=/api/v1/returns` + `audit_router=/api/v1/audit` 동거) | require_server_ownership(serverId) | 20 | 20 | 0 | 0 | – |
| scan.py | /api/v1/scan | – | 1 | 1 | 0 | 0 | – |
| servers.py | /api/v1 | – | 1 | 0 | 0 | 0 | – |
| settlement.py | /api/v1/audit (※ 위와 동일 패턴) | require_server_ownership(serverId) | 23 | 23 | 0 | 0 | – |
| stats.py | /api/v1/stats | require_server_ownership(serverId) | 14 | 0 | 2 | 5 | admin.stats.{book,customer,quarterly,sales} |
| transactions.py | /api/v1/transactions | require_server_ownership(serverId) | 6 | 6 | 0 | 0 | – |

> 인벤토리 결과의 핵심 분류 두 축은:
>
> - **인증 게이트 형태**: `Depends(get_current_user)` 직접 (= JWT 강제) vs `Depends(get_user_context)` (= ctx 합성, override 가능).
> - **권한 게이트**: `require_permission(code)` 적용 여부 + 어떤 코드.

## 4. 스모크 그룹 ↔ 라우트 ↔ 요구권한 매트릭스

스모크 67그룹은 `_routes_for(server_id, args)` 매트릭스에서 추출한다. 베이스라인 status 가 4대 서버 모두 동일하므로 한 행으로 표기한다.

### 4-A. PASS (23) — 현재 정책으로 통과

| 그룹 | 라우터 | 요구 권한코드 | 비고 |
|---|---|---|---|
| common.servers | servers.py | – | public |
| common.health | (별도 등록) | – | public |
| stats.sales_period | stats.py | admin.stats.sales | smoke ctx 에 사전 부여됨 |
| stats.customer_analysis | stats.py | admin.stats.customer | 동상 |
| stats.book_turnover | stats.py | admin.stats.book | 동상 |
| stats.quarterly_summary | stats.py | admin.stats.quarterly | 동상 |
| stats.publisher | stats.py | admin.stats.customer | 동상 |
| stats.dashboard.\* (6) | stats.py | – | get_user_context 또는 권한가드 없음 |
| dashboard.external.\* (11) | dashboard_external.py | – | router-level ownership 만 |

### 4-B. AUTH 실패 (37) — `Depends(get_current_user)` 우회 누락

| 그룹 | 라우터/함수 | router_deps | 요구 권한코드 | 메모 |
|---|---|---|---|---|
| masters.{customer,book,publisher,special} | masters.py | ownership(serverId) | – | 시그니처에 `Depends(get_current_user)` |
| outbound.{orders,shipment_status} | outbound.py | ownership | – | 동상 |
| shipping.courier_lines | courier.py | ownership | – | 동상 |
| inbound.receipts | inbound.py | ownership | – | 동상 |
| returns.list, returns.period_report | returns.py (router=`/api/v1/returns`) | ownership | – | 동상 |
| settlement.{cash,cash_status_hcode,cash_status_sdate,billing,tax_invoice,outstanding,invoice_pdf} | settlement.py | ownership | – | 동상 |
| settlement.audit_settlement | settlement.py(`audit_router`)/returns.py(`audit_router`) | – | – | audit_router 는 ownership 없음. AUTH 만 |
| transactions.{statement,status.list,status.summary,status.memo,other} | transactions.py | ownership | – | 동상 |
| inventory.ledger | inventory.py | ownership | – | 동상 |
| reports.book_sales | reports.py | ownership | – | 동상 |
| ledger.publisher_settings | ledger.py | ownership | – | 동상 |
| print.\* (10) | print.py | ownership | – | layouts/pdf/svg 모두 직접 게이트 |
| scan.match | scan.py | – | – | POST. ownership 없음 + AUTH 직접 |
| me.profile | me.py | – | – | 동상 |

### 4-C. PERMISSION 실패 (2) — admin.user.read 누락

| 그룹 | 라우트 | 요구 권한코드 |
|---|---|---|
| admin.id_logn_list | admin.py::list_id_logn (`require_permission("admin.user.read")`) | admin.user.read |
| admin.id_logn_permission_defaults | admin.py::get_id_logn_permission_defaults | admin.user.read |

### 4-D. EXPECTED 음성 검증 (5)

| 그룹 | 의도 | 실제 | 분류 |
|---|---|---|---|
| ownership.violation.expected_403 | 403 OWNERSHIP_VIOLATION | 403 | OK (가드 정상) |
| auth.expired_must_401 | 401 | 401 | OK (가드 정상) |
| admin.permission_matrix_stale_must_409 | If-Match stale → 409 | 403 (admin.user.write 가드 선차단) | **PERM-PRE-EMPTS-IFMATCH** |
| concurrency.precondition_required_must_428 | If-Match 누락 → 428 | 403 (동상) | **PERM-PRE-EMPTS-CONCURRENCY** |
| print.return_receipt_pdf_variant_v4_must_422 | variant=v4 → 422 PR_VARIANT_UNSUPPORTED | 401 (`Depends(get_current_user)` 선차단) | **AUTH-PRE-EMPTS-422** |

## 5. 분류표 (요약)

| 분류 | 그룹 수 | 근본 원인 | 일반화 가능 처방(권한·인증 매핑 관점) |
|---|---:|---|---|
| AUTH | 37 | smoke 가 `get_user_context` 만 override → `get_current_user` 직접 사용 라우트는 401 | (A) `get_current_user` 도 함께 override (전 라우터 통합) — 또는 (B) AUTH 그룹은 매트릭스에서 분리하고 별도 인증 매트릭스로 검증 |
| PERMISSION | 2 (+EXPECTED 2건 영향) | smoke ctx `permissions` 에 admin.user.\* 미포함 | (A) smoke 슈퍼유저 ctx (`permissions=['*']` 또는 `role='admin'`) 로 슈퍼유저 우회 — 또는 (B) admin.\* 그룹 분리 |
| OWNERSHIP | 1 (음성) | 의도된 가드 — 변경 불필요 | – |
| SCHEMA / STATE | 0 | 베이스라인 1회에서 알려진 스키마 차이는 발견되지 않음 | – |
| UNKNOWN | 0 | – | – |

> "`return_receipt_pdf_variant_v4_must_422`" 와 같은 음성 검증이 인증/권한 가드에 선차단되는 것 자체는 **가드 우선순위가 정상 작동**한다는 신호다. 다만 매트릭스 의도(상태 가드 검증) 는 도달하지 못하므로, 옵션 A 채택 시 가드 통과 → 의도된 4xx 코드까지 도달해야 매트릭스가 진짜 음성을 본다.

## 6. 옵션 A vs 옵션 B — 권한 매핑 관점 비교

| 항목 | 옵션 A: 전 라우터 dependency_overrides 통합 | 옵션 B: 매트릭스 분리(인증·권한 검증을 별도 그룹으로) |
|---|---|---|
| 처방 | smoke `_smoke_test_client` 가 `get_current_user` 와 `get_user_context` 를 모두 override + 슈퍼유저 ctx (`permissions=['*']`) | 본 매트릭스(SQL/스키마 회귀)는 양성만 유지. 인증·권한 가드는 별도 단위 테스트(test/test_router_permission_matrix_static.py 등) 로 정적 검증 |
| 매트릭스 통과 가능성 | AUTH 37 + PERMISSION 2 + EXPECTED-FAIL 3 → **42 그룹 추가 통과 가능**. 전체 67/67 200/의도 status 도달 가능 | 본 매트릭스는 PASS 23 + 음성 가드(2) 만 측정. 추가로 단위 테스트 한 묶음 |
| 음성 검증 가치 | `expected_403/401/422/409/428` 모두 가드 선차단 없이 의도 status 까지 도달 → 진짜 회귀 검증 | 가드별 단위 테스트 책임으로 이전. 매트릭스에서는 음성 검증 비중 축소 |
| 위험 | 슈퍼유저 ctx 가 RBAC 회귀를 가릴 수 있음 → 음성 검증 그룹(`expected_*`) 로 보완 필요 | 가드 회귀가 매트릭스에 보이지 않음. 단위 테스트 누락 시 사각지대 |
| 권한 카탈로그 정합 | `legacy-analysis/permission-keys-catalog.md` v1.2 의 30 정본 + 7 확장 = 52 키와 1:1 일치 — `*` 우회 1줄로 종결 | 가드별 단위 테스트가 카탈로그와 1:1 일치하도록 fail-fast (`test_G_05_unknown_permission_code_fails_fast` 와 동일 톤) |
| DEC 정합 | DEC-041 (RBAC 표준 응답 트리) 와 충돌 없음 — 슈퍼유저는 본 가드의 단일 규칙(LSP) 통과 | 동상. 단 본 매트릭스의 의미가 "데이터 회귀 가드" 로 좁혀짐을 DEC 갱신 필요 |
| 작업 범위 | probe `_smoke_test_client` 1개 함수 + smoke ctx 1줄 (`permissions=['*']` 또는 `role='admin'`) | probe 매트릭스 그룹 50%+ 이동 + 새 단위 테스트 묶음 + DEC 갱신 |
| 현 멀티 DB 정책 정합 | DEC-033 §DoD ("L4 매트릭스 GET = 200 또는 알려진 스키마 차이로 reason 분류") 와 그대로 호환 | DoD 자체를 재정의해야 함 (분리된 매트릭스의 DoD 추가) |

### 권고

- **옵션 A 채택**(`get_current_user` 도 override + 슈퍼유저 ctx)을 권고한다. 이유:
  1. 본 매트릭스의 목적은 **데이터/SQL 회귀** 검증인데, 인증·권한 게이트가 SQL 도달을 막는 현상은 매트릭스 의미를 흐린다. A 는 가드 통과 → SQL 도달 까지 결정적이다.
  2. RBAC 회귀는 이미 `expected_*` 음성 검증 그룹 5개로 가드 작동 자체를 별도 검증한다. 슈퍼유저 ctx 가 가드를 우회해도 음성 검증은 유지된다.
  3. 변경 범위가 probe 1개 함수 + ctx 1줄 (`permissions=['*']`) 로 최소다 — 사용자 룰(SOLID/recursive 회귀 회피) 과 정합.
  4. `legacy-analysis/permission-keys-catalog.md` v1.2 의 슈퍼유저 단일 규칙 (LSP — `role='admin' or hcode='0000' or '*' in permissions`) 을 그대로 활용.

## 7. 후속 액션 (코드 미변경 — 결정 후 실행)

1. **DEC-058 확장 또는 신규 DEC**: 옵션 A 채택을 `legacy-analysis/decisions.md` 에 1항으로 등록 (probe 슈퍼유저 ctx 정책 + 매트릭스 의미 명확화).
2. **probe 변경 (옵션 A)**:
   - `_smoke_test_client` 가 `get_user_context` 외에 `app.routers.auth.get_current_user` 도 override.
   - smoke ctx: `role='admin'` + `permissions=['*']` + `hcode='0000'` 중 하나 (단일 규칙) — 현재 ctx 의 admin.stats.\* 4건 부여 코드는 `permissions=['*']` 로 단일화하여 카탈로그 변경에도 무영향.
3. **음성 검증 보존**: `auth.expired_must_401` 은 `headers_no_auth=True` 로 override 일시 해제 경로가 이미 매트릭스에 있음 — probe 측 처리 검증 보강 필요(`probe_routes` 가 무인증 호출 시 `dependency_overrides` 우회).
4. **CI 정책**: `.github/workflows/db-smoke.yml` 의 dry-run 부분에는 영향 없음. live 실행 후 67/67 통과를 신규 DoD 로 확정.
5. **회귀 가드**: `test/test_db_smoke_static.py` 신규 1건 — `_routes_for` 의 모든 그룹이 라우터 인벤토리와 매칭(없으면 fail). `permission-mapping-classification.json` 의 `class != "PASS|EXPECTED-OK"` 가 0 이어야 한다는 정적 검사도 동시 수록.

## 8. 부록 — 인벤토리 매칭 한계

- `returns.py` / `settlement.py` 는 한 파일에 `router` (`/api/v1/{returns,settlement}`) 와 `audit_router` (`/api/v1/audit`) 두 APIRouter 를 동시 등록한다. 본 정적 매칭 스크립트는 `APIRouter()` 첫 발견 prefix 만 사용하므로, 9건이 일시적으로 "매칭 실패" 로 분류되었다. 코드 grep 으로 동일 파일 내 모든 라우트 본함수가 `_user=Depends(get_current_user)` 를 직접 받음을 100% 확인 → AUTH/direct 와 동일 부류로 처리한다.
- 향후 회귀 가드(7-5)에서 보조 APIRouter 변수도 함께 추적하도록 정적 매칭을 강화한다(`var=APIRouter(...)` AST 추출을 변수명 단위로 다중 추적).

## 9. 트레이서

- DEC-033 — 멀티 DB 호환·매트릭스 등록 의무 (본 분석은 그 회귀 가드의 베이스라인).
- DEC-041 — RBAC 표준 응답 트리 (`require_permission` / `require_role` / `assert_*_ownership`) — 본 메모의 가드 분류 근거.
- DEC-056 — `legacy_permission_map` v1.2 (52 정본 키 일괄 시드).
- DEC-058 — M2 사이드바 게이팅(권한 코드 ↔ 메뉴 매트릭스).
- 권한 카탈로그: `legacy-analysis/permission-keys-catalog.md`.
- 런북: `docs/db-smoke-runbook.md`.
- 데이터: `artifacts/db-smoke-baseline.json`, `artifacts/router-auth-inventory.json`, `artifacts/permission-mapping-classification.json`.
