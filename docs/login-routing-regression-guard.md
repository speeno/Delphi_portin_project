# 통합 로그인 회귀 방지 가이드 (DSN-DEC-08)

| 항목 | 내용 |
| ------ | ------ |
| 추적 | DSN-DEC-08 / DSN-DEC-09 / DEC-051·052 재정의 |
| 단일 원천(설계) | [docs/decision-login-db-routing.md](decision-login-db-routing.md) §DSN-DEC-08 |
| 구현 진입점 | [도서물류관리프로그램/backend/app/routers/auth.py](../도서물류관리프로그램/backend/app/routers/auth.py) `POST /api/v1/auth/login` |
| 비밀 검증 | [도서물류관리프로그램/backend/app/services/auth_service.py](../도서물류관리프로그램/backend/app/services/auth_service.py) `authenticate_user` → 대상 서버의 ``<db>.Id_Logn`` |

## 1. 실제 동작 (코드 기준)

1. 프론트는 `userId`, `password`와 선택적으로 `tenantId`, `hcode`를 보낸다. ([auth-context.tsx](../도서물류관리프로그램/frontend/src/contexts/auth-context.tsx), [LoginRequest](../도서물류관리프로그램/backend/app/models/auth.py))
2. 백엔드가 `tenants_directory_service.resolve_login_route` / `resolve_login_route_candidates`로 `(remote_id, db_name)` 후보 목록을 만든다.
3. 인덱스 모호·미스 시 `login_id_index_service.lazy_refresh`가 **요청당 최대 1회** 호출될 수 있다 (DSN-DEC-09). 감사 로그의 `lazy_refresh_reason`은 `rebuilt` / `cooldown` / `busy` / `error` 중 하나다.
4. 후보를 **순서대로** 시도하며, 각 시도마다 `authenticate_user(server_id, user_id, password, db_name=...)`가 해당 서버에서 `Id_Logn`을 조회·레거시 비밀 검증을 수행한다.
5. 첫 성공 서버가 JWT 클레임 `sid`(데이터 서버)로 고정된다.

동명 `Gcode`가 여러 DB에 존재해 `index_ambiguous`가 된 경우의 정책은 **DSN-DEC-09 v2 (2026-04-27)** 로 갱신되었다.

| 모드 | 트리거 | 동작 |
| ------ | ------ | ------ |
| **default (narrowing)** | `BLS_LOGIN_AMBIGUOUS_PROBE` 미설정 또는 그 외 값 | 후보를 우선순위 순으로 시도하며, **사용자 비밀번호와 일치하는 첫 후보** 를 본인 계정으로 결정. 감사 로그에 `ambiguous_narrowed=true`, `candidate_attempts ≥ 2`, `resolved_via=candidate_probe` 가 남는다. |
| **strict (opt-in)** | `BLS_LOGIN_AMBIGUOUS_PROBE=block` (또는 `strict`/`0`/`false`/`no`) | `tenantId` / `hcode` 힌트 없이 임의 DB 순회 금지 → `reason=ambiguous_route`, `ambiguous_strict=true` 로 즉시 401. 보안 격리/감사 강화 환경 전용. |

> **변경 이유**: 운영 인덱스의 ambiguous 비율이 약 27%(예: 829/3084)에 달해, hcode 같은 내부 메타데이터를 모르는 일반 사용자가 영구 차단되는 회귀가 발생했다 (대표 사례: `미래가치` 가 `chul_05_db`/`chul_09_db` 양쪽에 존재). v1 의 무조건 차단은 `BLS_LOGIN_AMBIGUOUS_PROBE=block` 으로 보존된다.

`admin` 등 운영자 예외는 두 모드 모두 `auth_service.should_bypass_login_id_index_ambiguity()` 정책을 따른다.

**DEC-051(인증 서버 단일화) 운영 의미**: API 엔드포인트는 앱 한 곳이지만, **비밀번호 검증 DB는 메타가 고른 데이터 서버·논리 DB**이다. `BLS_AUTH_SERVER_ID`는 감사 로그·폴백 등에 쓰이며, “모든 사용자 비밀만 auth 서버 한 DB”가 아니다.

## 2. 로그인 실패 시 점검 순서

1. **HTTP 401**: 사용자에게는 항상 동일 메시지일 수 있다. 서버 **`audit.auth` / `log_login_attempt`** JSON에서 `server_id`, `resolved_db`, `resolved_via`, `reason`, `candidate_count`, `candidate_attempts`, `candidate_sources`, `attempted_routes`, `directory_sweep`, `ambiguous_narrowed`, `ambiguous_strict`, `lazy_refreshed`, `lazy_refresh_reason`, `lazy_refresh_errors_count`, `index_hit`를 본다.
2. **즉시 진단 (계정별)**: [debug/diagnose_login_routing.py](../debug/diagnose_login_routing.py) 로 해당 `login_id` 의 인덱스/후보/정책 상태를 한 번에 덤프한다. 비밀번호가 있다면 `--probe` 로 후보별 인증 결과까지 수집(stdout 에 비밀번호 미인쇄). 사용 예시:

   ```bash
   PYTHONPATH=도서물류관리프로그램/backend \
     python3 debug/diagnose_login_routing.py 미래가치
   PYTHONPATH=도서물류관리프로그램/backend \
     python3 debug/diagnose_login_routing.py 미래가치 \
       --password '...' --probe --write-json /tmp/diag.json
   ```

3. **환경**: `BLS_AUTH_SERVER_ID`, `BLS_LOGIN_AMBIGUOUS_PROBE`(default narrowing / `block` strict), `BLS_LOGIN_DIRECTORY_SWEEP`, `BLS_LOGIN_SWEEP_MAX`, `BLS_LOGIN_INDEX_REFRESH_MIN_INTERVAL_SECS`, `BLS_ADMIN_USER_IDS`, `servers.yaml`의 `remote_*` 정의, DB 비밀(예: `BLS_MYSQL_ROOT_PASSWORD`), SSH 터널 설정.
4. **메타**: [migration/contracts/tenants_directory.yaml](../migration/contracts/tenants_directory.yaml) 및 시드가 해당 `user_id`·힌트(`tenant_id`/`hcode`)와 맞는지. 후보 0이면 전부 401로 수렴.
5. **인덱스**: `lazy_refresh_reason=rebuilt`인데도 실패하면 새 인덱스에도 해당 계정이 없거나 비밀번호 불일치다. `cooldown`/`busy`면 직전 갱신 또는 동시 갱신 때문에 재빌드가 생략된 것이다. `error` 또는 `lazy_refresh_errors_count>0`이면 4대 서버 일부 스캔 실패를 우선 본다.
6. **모호 라우팅 (default narrowing)**: `ambiguous_narrowed=true` 인데 401 이면 비밀번호 자체가 틀린 것(`reason=invalid_credentials_after_probe`)이다. `attempted_routes` 에 표시된 후보들 어디에도 비밀번호가 일치하지 않았음을 의미한다. 진단 스크립트의 `--probe` 로 동일 비밀번호를 다시 시도해 본다.
7. **모호 라우팅 (strict opt-in)**: `ambiguous_strict=true` 와 `reason=ambiguous_route` 가 함께 나오면 `BLS_LOGIN_AMBIGUOUS_PROBE=block` 환경이다. 사용자에게 `tenantId` / `hcode` 힌트 입력을 안내하거나 default 로 되돌려야 한다.
8. **저신뢰 스윕**: `directory_sweep=true`이면 인덱스 miss 상태에서 활성 테넌트 후보를 넓게 시도한 것이다. 성공하면 `remembered=true`로 다음 로그인은 인덱스 hit가 되어야 한다. 실패가 반복되면 인덱스 빌드 또는 테넌트 시드를 점검한다.
9. **연결**: 후보 `server_id`에 대해 L2 `SELECT 1` ([debug/probe_backend_all_servers.py](../debug/probe_backend_all_servers.py) 등).

## 3. 변경 시 준수 규칙 (회귀 방지)

| 영역 | 규칙 |
| ------ | ------ |
| 요청 스키마 | `LoginRequest`의 `userId`/`user_id`/`username`, `tenantId`/`tenant_id`, `hcode` **AliasChoices 유지**. 프론트는 camelCase 단일 경로. |
| 라우터 | `auth.py`의 후보 빌드·`lazy_refresh`·재시도 블록을 바꿀 때는 **전체 플로우**와 감사 필드를 한 번에 리뷰한다. |
| 후보 쌍 | `authenticate_user`에 넘기는 `(server_id, db_name)`은 **tenants_directory / 라우트 메타**에서만 나와야 한다. 임의 `remote_*` 하드코딩 금지. |
| 모호 ID (default) | DSN-DEC-09 v2 — `index_ambiguous` 후보를 비밀번호로 narrow 한다. `_try_candidates` 의 첫 성공 반환 시맨틱과 감사 필드(`ambiguous_narrowed`, `candidate_attempts`, `attempted_routes`)는 변경 금지. |
| 모호 ID (strict opt-in) | `BLS_LOGIN_AMBIGUOUS_PROBE=block` 일 때만 `tenantId`/`hcode` 힌트 없는 시도를 즉시 401 로 차단. 운영자 예외는 `should_bypass_login_id_index_ambiguity()`로만 허용. `ambiguous_strict=true` 신호 보존. |
| 감사 | `log_login_attempt` 필드 이름·의미 삭제/무명 변경 금지 (운영 추적). 특히 `lazy_refresh_reason`, `candidate_sources`, `attempted_routes`, `directory_sweep`, `ambiguous_narrowed`, `ambiguous_strict`는 장애 분석용이다. |
| 문서·계약 | 설계와 충돌하면 **DEC/YAML 먼저** 고친 뒤 코드. |
| 테스트 | Auth 터치 PR: `test/test_auth_login_fixed_server.py`, `test/test_c1_login_phase1.py`, `test/test_auth_login_dynamic_routing.py` **필수 통과**. |

## 4. PR 체크리스트 (복붙용)

- [ ] `LoginRequest` 별칭·필수 필드 변경 없음 (또는 프론트+문서 동시 갱신)
- [ ] `resolve_login_route*` / `lazy_refresh` / `authenticate_user` 시그니처 변경 시 위 테스트 갱신 및 실행
- [ ] `tenants_directory`·인덱스 시드 변경 시 해당 `user_id`로 로그인 스모크 + [debug/diagnose_login_routing.py](../debug/diagnose_login_routing.py) 1건
- [ ] 실패 시 `log_login_attempt`에 원인 추적 가능한 키(`reason`, `candidate_sources`, `lazy_refresh_reason`, `directory_sweep`, `ambiguous_narrowed`, `ambiguous_strict`)가 남는지 확인
- [ ] 동일 `Gcode` 복수 DB 케이스: default 모드는 비밀번호 narrow, strict 모드(`BLS_LOGIN_AMBIGUOUS_PROBE=block`)는 즉시 401 — 양쪽 모두 회귀 테스트 통과
- [ ] 본 문서 §1·[decision-login-db-routing.md](decision-login-db-routing.md) DSN-DEC-08/09과 서술 충돌 없음

## 5. DB 스모크와 로그인

`RUN_DB_SMOKE=1` 매트릭스는 로그인 POST를 포함하지 않을 수 있다. 멀티 DB 회귀는 **§4 테스트 + 수동 로그인 1건**(대표 `remote_*`·대표 테넌트)을 권장한다.

## 6. 참고 링크

- [docs/onboarding-account-type-resolution.md](onboarding-account-type-resolution.md) (ACTR, JWT 계정 유형)
- [migration/contracts/login.yaml](../migration/contracts/login.yaml) (계약이 있으면 버전 정합)
