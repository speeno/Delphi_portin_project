# Hcode 격리 전면 적용 — DoD 체크리스트

작성: 2026-05-25 — Phase 4 결과.

본 문서는 「Hcode 격리 전면 적용 및 기본 hcode 자동 주입」의 완료 정의(DoD) 가
모두 통과되었음을 단일 정본으로 기록한다.

## 1. 코드 변경 요약

| 영역 | 변경 |
|------|------|
| 헬퍼 | [`enforce_hcode_isolation`](../../도서물류관리프로그램/backend/app/core/deps.py) — coalesce + tamper 가드 통합 단일 진입점 |
| P0 라우터 | `transactions(sales-statement, status)`, `outbound(orders, shipment-status)`, `inbound(receipts)`, `returns(list, daily, ledger, period-report)` |
| P1 라우터 | `settlement(billing, billing/period, cash, tax-invoice)`, `stats(5 main + 7 dashboards)`, `dashboard_external(weather-risk, delivery-route-risk, demand-forecast)` |
| 마스터/리포트 | `masters.special`, `reports.*`, `inventory.ledger` 가 enforce 로 통일 |
| 정적 감사 | [`tools/audit_router_hcode_coalesce.py`](../../tools/audit_router_hcode_coalesce.py) 신규 — 라우터 단계 회귀 가드 |
| 단위 테스트 | [`test/test_hcode_isolation_enforce.py`](../../test/test_hcode_isolation_enforce.py), [`test/test_routers_hcode_coalesce.py`](../../test/test_routers_hcode_coalesce.py) |
| 라이브 검증 | [`debug/probe_hcode_isolation_live.py`](../../debug/probe_hcode_isolation_live.py) |
| 계약 | [`migration/contracts/_hcode_query_policy.yaml`](../../migration/contracts/_hcode_query_policy.yaml) (단일 정본), [`docs/onboarding-rbac-menu-matrix.md`](../../docs/onboarding-rbac-menu-matrix.md) `ACC-DATA-03` 보강 |
| 프론트 | [`frontend/src/lib/api-client.ts`](../../도서물류관리프로그램/frontend/src/lib/api-client.ts) — 정책 docstring 추가 (행위는 변경 없음) |

## 2. 정적·단위 검증 (CI 가능)

| 항목 | 상태 | 결과 |
|------|------|------|
| `audit_domain_api_hcode_filter --strict` | ✅ green | `critical=0 warn=0` |
| `audit_router_hcode_coalesce --strict` | ✅ green | `endpoints=217 optional_hcode=36 critical=0 info=36` |
| `test_hcode_isolation_enforce` | ✅ 11/11 | T2_PUB / T2_DIST / super / inspect 시나리오 |
| `test_routers_hcode_coalesce` | ✅ 6/6 | P0 라우터 hcode 자동 주입 + tamper 403 |
| `test_masters_hcode_isolation` | ✅ 4/4 | masters_service `Hcode=%s` 절 |

## 3. 정책 매트릭스

| 계정 | 빈 hcode 처리 | 다른 hcode 명시 | 비고 |
|------|---------------|-----------------|------|
| **T1 (수퍼)** | 무필터 (전체) | 통과 | 점검 모드 가능 |
| **T2_DIST (총판)** | 무필터 (전체) | 통과 | DEC-033 (f) |
| **T2_PUB (출판)** | JWT scope 자동 주입 | 본인과 다르면 **403** | ACC-DATA-03 ✓ |
| **T3 단독** | 본인 hcode 명시 시만 | 통과 | (사실상 1 hcode) |
| **T3_LITE (chul_09 공유)** | JWT scope 자동 주입 | 본인과 다르면 **403** | ACC-DATA-03 ✓ |

## 4. 라이브 DB 검증 (운영 단계)

CI 환경에서는 4대 서버 직접 접속이 차단되어 본 단계는 운영자가 [`debug/probe_hcode_isolation_live.py`](../../debug/probe_hcode_isolation_live.py)
로 수동 실행해야 한다.

| 서버 | 검증 명령 (예) | 기대 결과 |
|------|----------------|-----------|
| `remote_138` | `PROBE_BASE=… PROBE_T2_PUB_TOKEN=… python3 debug/probe_hcode_isolation_live.py` | DoD 5 endpoint × 본인 hcode = 빈 hcode |
| `remote_153` | 동일 (위러브1·2·3 + 교문사 chul_09 SKU) | 동일 |
| `remote_154` | (호스트 차단 해소 후) 동일 | 동일 |
| `remote_155` | 동일 | 동일 |

## 5. 회귀 방지

- [`tools/audit_router_hcode_coalesce.py`](../../tools/audit_router_hcode_coalesce.py) `--strict` 를 PR pre-commit/CI 에 추가 권장 (별도 DEC).
- 신규 list/집계 GET 추가 시 `enforce_hcode_isolation(hcode, ctx)` 사용이 정본.
- 의도적 예외(예: 합성키 hcode) 는 함수 본문에 `# noqa: hcode-router-coalesce` 마커.

## 6. 알려진 비대상

| 항목 | 사유 |
|------|------|
| 단건 처리 `*_key` 라우터 (order_key/return_key/billing_key 의 POST/PUT/PATCH) | hcode 는 합성키 식별자 — `key_identity` |
| `inbound.daily_report`, `inbound.period_report` | hcode 파라미터 자체 없음 (`n_a`) |
| `public_lookup.activate_lookup` | 로그인 이전 공개 계정복구 — 인증 컨텍스트 없음 (`# noqa` 명시) |

> 2026-05-29: `courier.list_courier_lines`(`hcodeFrom`/`hcodeTo`)와
> `courier.*memo` 는 더 이상 비대상이 아니다 — §8 갭 클로즈로 `scope_identity`
> 가드가 적용되어 격리 계정의 타사 hcode 접근을 403 으로 차단한다.

## 7. 후속 작업 (선택)

- [`debug/probe_backend_all_servers.py`](../../debug/probe_backend_all_servers.py) 의 dependency override 를
  T2_PUB 컨텍스트 변종으로 확장하면 4대 DB 라이브 가드를 CI 에 자동 통합 가능.
- 프론트 `placeholder` 문구 통일은 별도 UX 개선 티켓에서 진행 (백엔드 회귀 0건이라 우선순위 낮음).

## 8. ACC-DATA-03 갭 클로즈 (2026-05-29)

Phase 4 에서 list/집계 GET 의 `hcode` Query 는 막혔으나, **식별자 파라미터로 Hcode 를
우회**하는 경로가 남아 있었다(도서 마스터 125,861건 노출과 동일 클래스). 본 단계에서
일반화 가드로 폐쇄했다.

### 8.1 폐쇄한 우회 경로

| 라우터/엔드포인트 | 우회 벡터 | 적용 가드 |
|---|---|---|
| `ledger.get_customer_ledger` | `customerCode` → 서비스에서 그대로 `Hcode` | `enforce_hcode_identity` |
| `ledger.get_integrated_customer_ledger` | `customerPattern` → `Hcode LIKE` | `enforce_hcode_pattern` + 서비스 `scope_hcode` 정확일치 |
| `ledger.list_publisher_settings` (`/comparison`) | `G7_Ggeo` 전체(hcode 필터 없음) | `resolve_scope_hcode` → 서비스 `Gcode=%s` |
| `ledger.patch_publisher_setting` | `gcode` 쓰기 | `enforce_hcode_identity` |
| `courier.list_courier_lines` | `hcodeFrom`/`hcodeTo` 구간 | `enforce_hcode_range` |
| `courier.get/patch_courier_memo` | `hcode` 단건 | `enforce_hcode_identity` |
| `scan.scan_match` | body `hcode` | `enforce_hcode_identity` |
| `transactions.upsert_other_statement_memo` | body `hcode` (PATCH) | `enforce_hcode_identity` |

세 라우터(`ledger`/`courier`/`scan`)는 `get_current_user` → `get_user_context` 로
전환해 `account_type`/점검 오버레이를 반영한다.

### 8.2 신규 헬퍼·최후 방어선

| 항목 | 위치 |
|---|---|
| `enforce_hcode_identity` / `enforce_hcode_range` / `enforce_hcode_pattern` | [`deps.py`](../../도서물류관리프로그램/backend/app/core/deps.py) |
| `guard_scope_bound` (런타임 회귀 검출) + `append_hcode_clause(guard=True)` | [`hcode_isolation.py`](../../도서물류관리프로그램/backend/app/core/hcode_isolation.py) |
| 요청 범위 scope ContextVar | [`hcode_scope_context.py`](../../도서물류관리프로그램/backend/app/core/hcode_scope_context.py) |

`BLS_HCODE_SCOPE_GUARD=strict` 면 multi-tenant 테이블 scope 누락 시 `RuntimeError`
(테스트/CI 권장), 기본 `warn` 은 `audit.hcode_scope` 로그.

### 8.3 검증 결과 (2026-05-29)

| 항목 | 상태 | 결과 |
|---|---|---|
| `audit_router_hcode_coalesce --strict` (식별자/POST·PATCH 확장) | ✅ green | `endpoints=218 scope_idents=44 critical=0 info=43 skipped_noqa=1` |
| `audit_domain_api_hcode_filter --strict` | ✅ green | `critical=0 warn=0` |
| `test_hcode_identifier_guards` | ✅ 20/20 | identity/range/pattern + guard strict/warn |
| `test_ledger_courier_scan_hcode_isolation` | ✅ 13/13 | 타사 식별자 403 + 본인/빈값 scope 강제 + 총판 광역 |
| 기존 hcode 스위트 회귀 | ✅ 32/32 | enforce/masters/coalesce/book-sales/audit |

### 8.4 감사 도구 확장

[`audit_router_hcode_coalesce.py`](../../tools/audit_router_hcode_coalesce.py) 가
GET 의 optional `hcode` 뿐 아니라 **식별자 파라미터**(`customerCode`/`customerPattern`/
`hcodeFrom`/`hcodeTo`) 와 **POST/PATCH body `hcode`** 까지 critical 로 탐지한다.
신규 헬퍼 3종이 `_ALLOWED_HELPERS` 에 등록됐다.
