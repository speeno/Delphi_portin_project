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
| `courier.list_courier_lines` (`hcodeFrom`/`hcodeTo`) | 총판 운영 화면의 범위 검색 — `range_filter` 정책 |
| `courier.get_courier_memo` / `*memo` PATCH | hcode 가 합성키의 일부 — `key_identity` |
| 단건 처리 `*_key` 라우터 (POST/PUT/PATCH/DELETE) | hcode 는 키 식별자 |
| `inbound.daily_report`, `inbound.period_report` | hcode 파라미터 자체 없음 (`n_a`) |

## 7. 후속 작업 (선택)

- [`debug/probe_backend_all_servers.py`](../../debug/probe_backend_all_servers.py) 의 dependency override 를
  T2_PUB 컨텍스트 변종으로 확장하면 4대 DB 라이브 가드를 CI 에 자동 통합 가능.
- 프론트 `placeholder` 문구 통일은 별도 UX 개선 티켓에서 진행 (백엔드 회귀 0건이라 우선순위 낮음).
