# 통합 로그인 회귀 방지 가이드 (DSN-DEC-08)

| 항목 | 내용 |
|------|------|
| 추적 | DSN-DEC-08 / DSN-DEC-09 / DEC-051·052 재정의 |
| 단일 원천(설계) | [docs/decision-login-db-routing.md](decision-login-db-routing.md) §DSN-DEC-08 |
| 구현 진입점 | [도서물류관리프로그램/backend/app/routers/auth.py](../도서물류관리프로그램/backend/app/routers/auth.py) `POST /api/v1/auth/login` |
| 비밀 검증 | [도서물류관리프로그램/backend/app/services/auth_service.py](../도서물류관리프로그램/backend/app/services/auth_service.py) `authenticate_user` → 대상 서버의 ``<db>.Id_Logn`` |

## 1. 실제 동작 (코드 기준)

1. 프론트는 `userId`, `password`와 선택적으로 `tenantId`, `hcode`를 보낸다. ([auth-context.tsx](../도서물류관리프로그램/frontend/src/contexts/auth-context.tsx), [LoginRequest](../도서물류관리프로그램/backend/app/models/auth.py))
2. 백엔드가 `tenants_directory_service.resolve_login_route` / `resolve_login_route_candidates`로 `(remote_id, db_name)` 후보 목록을 만든다.
3. 인덱스 모호·미스 시 `login_id_index_service.lazy_refresh`가 **요청당 제한적으로** 호출될 수 있다 (DSN-DEC-09).
4. 후보를 **순서대로** 시도하며, 각 시도마다 `authenticate_user(server_id, user_id, password, db_name=...)`가 해당 서버에서 `Id_Logn`을 조회·레거시 비밀 검증을 수행한다.
5. 첫 성공 서버가 JWT 클레임 `sid`(데이터 서버)로 고정된다.

**DEC-051(인증 서버 단일화) 운영 의미**: API 엔드포인트는 앱 한 곳이지만, **비밀번호 검증 DB는 메타가 고른 데이터 서버·논리 DB**이다. `BLS_AUTH_SERVER_ID`는 감사 로그·폴백 등에 쓰이며, “모든 사용자 비밀만 auth 서버 한 DB”가 아니다.

## 2. 로그인 실패 시 점검 순서

1. **HTTP 401**: 사용자에게는 항상 동일 메시지일 수 있다. 서버 **`audit.auth` / `log_login_attempt`** JSON에서 `server_id`, `resolved_db`, `resolved_via`, `reason`, `candidate_count`, `lazy_refreshed`, `index_hit`를 본다.
2. **환경**: `BLS_AUTH_SERVER_ID`, `servers.yaml`의 `remote_*` 정의, DB 비밀(예: `BLS_MYSQL_ROOT_PASSWORD`), SSH 터널 설정.
3. **메타**: [migration/contracts/tenants_directory.yaml](../migration/contracts/tenants_directory.yaml) 및 시드가 해당 `user_id`·힌트(`tenant_id`/`hcode`)와 맞는지. 후보 0이면 전부 401로 수렴.
4. **인덱스**: `lazy_refresh` 실패·모호(`ambiguous`) 로그. 필요 시 `backend/data/login_id_index.json` 갱신 절차(운영 런북) 확인.
5. **연결**: 후보 `server_id`에 대해 L2 `SELECT 1` ([debug/probe_backend_all_servers.py](../debug/probe_backend_all_servers.py) 등).
6. **UI**: 동일 ID가 여러 테넌트 DB에 있으면 로그인 화면 **「회사 정보로 라우팅」**에서 `tenantId` 또는 `hcode` 입력.

## 3. 변경 시 준수 규칙 (회귀 방지)

| 영역 | 규칙 |
|------|------|
| 요청 스키마 | `LoginRequest`의 `userId`/`user_id`/`username`, `tenantId`/`tenant_id`, `hcode` **AliasChoices 유지**. 프론트는 camelCase 단일 경로. |
| 라우터 | `auth.py`의 후보 빌드·`lazy_refresh`·재시도 블록을 바꿀 때는 **전체 플로우**와 감사 필드를 한 번에 리뷰한다. |
| 후보 쌍 | `authenticate_user`에 넘기는 `(server_id, db_name)`은 **tenants_directory / 라우트 메타**에서만 나와야 한다. 임의 `remote_*` 하드코딩 금지. |
| 감사 | `log_login_attempt` 필드 이름·의미 삭제/무명 변경 금지 (운영 추적). |
| 문서·계약 | 설계와 충돌하면 **DEC/YAML 먼저** 고친 뒤 코드. |
| 테스트 | Auth 터치 PR: `test/test_auth_login_fixed_server.py`, `test/test_c1_login_phase1.py` **필수 통과**. |

## 4. PR 체크리스트 (복붙용)

- [ ] `LoginRequest` 별칭·필수 필드 변경 없음 (또는 프론트+문서 동시 갱신)
- [ ] `resolve_login_route*` / `lazy_refresh` / `authenticate_user` 시그니처 변경 시 위 테스트 갱신 및 실행
- [ ] `tenants_directory`·인덱스 시드 변경 시 해당 `user_id`로 로그인 스모크
- [ ] 실패 시 `log_login_attempt`에 원인 추적 가능한 키가 남는지 확인
- [ ] 본 문서 §1·[decision-login-db-routing.md](decision-login-db-routing.md) DSN-DEC-08과 서술 충돌 없음

## 5. DB 스모크와 로그인

`RUN_DB_SMOKE=1` 매트릭스는 로그인 POST를 포함하지 않을 수 있다. 멀티 DB 회귀는 **§4 테스트 + 수동 로그인 1건**(대표 `remote_*`·대표 테넌트)을 권장한다.

## 6. 참고 링크

- [docs/onboarding-account-type-resolution.md](onboarding-account-type-resolution.md) (ACTR, JWT 계정 유형)
- [migration/contracts/login.yaml](../migration/contracts/login.yaml) (계약이 있으면 버전 정합)
