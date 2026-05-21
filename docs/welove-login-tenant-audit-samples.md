# WeLove 통합 로그인 — 고객별 라우팅 샘플 매트릭스 (DSN-DEC-08/09 + DSN-DEC-12)

| 항목 | 내용 |
| ---- | ---- |
| 작성일 | 2026-05-21 |
| 추적 | DSN-DEC-08 / DSN-DEC-09 / **DSN-DEC-12 (신설 — 테넌트 소유성 가드)** |
| 단일 원천(시드) | [도서물류관리프로그램/backend/data/tenants_directory_seed.json](../도서물류관리프로그램/backend/data/tenants_directory_seed.json) |
| 단일 원천(레거시) | [analysis/welove_db_route_matrix.json](../analysis/welove_db_route_matrix.json) |
| 진단 도구 | [debug/diagnose_login_routing.py](../debug/diagnose_login_routing.py) |
| 비밀 정책 | 자격증명 0건 — [docs/secrets-policy.md](secrets-policy.md) G3 준수. 본 문서에는 ID 라벨/회사명만 기록한다. |

---

## 0. 본 문서의 목적

레거시 델파이는 **고객사별 EXE + Config.Ini** 모델로 사실상 단일 테넌트로 운영되었다(DEC-008). 웹 통합 포팅 후 다음 사고가 보고되었다.

> "로그인 후 출력되는 데이터가 **다른 회사의 데이터**가 출력되고 있다."

원인은 **동일 DB(`db_name_logical`)에 N 테넌트가 매핑된 공유 DB 운영 패턴** 과, 인덱스/디렉터리가 `tenant_id` 보강 없이 라우팅을 결정하면서 첫 매치 테넌트로 사용자 컨텍스트가 고정되는 결함이다. 본 매트릭스는 각 케이스의 **기대 결과(remote_id / db_name / hcode 패턴)** 를 정의해 회귀 테스트와 운영 검증의 단일 정본을 만든다.

---

## 1. 카테고리별 라우팅 기대값

### A) 단독 DB 테넌트 (1:1 매핑 — 기준 케이스)

| # | 라벨 | account_family | primary_server (라벨) | 기대 remote_id | 기대 db_name | 기대 hcode 패턴 | 위험도 |
|---|------|-----------------|------------------------|------------------|----------------|------------------|--------|
| A1 | 중앙라인(한강북) | `chul_05` | 서버3 | `remote_153` | `chul_05_db` | `*` (총판 본사) | 낮음 |
| A2 | 북앤더 | `chul_08` | 서버3 | `remote_153` | `chul_08_db` | `*` | 낮음 |
| A3 | 진성사 | `book_01` | 서버1 | `remote_154` | `book_01_db` | 출판사 hcode | 낮음 |
| A4 | 한강물류 | `chul_01` | 서버2 | `remote_155` | `chul_01_db` | `*` | 낮음 |
| A5 | MS북스 | `book_21` | 서버4 | `remote_138` | `book_21_db` | `*` | 낮음 |

> 기준 합격선 — 본 케이스에서 다른 회사 데이터가 보이면 인덱스/시드 1차 정합 깨짐.

### B) 공유 DB — 동일 `db_name_logical` 다중 테넌트 (위험 핵심)

| # | 라벨 | account_family | primary_server | 기대 remote_id | 기대 db_name | 동일 DB 공유 라벨 | 식별 키 | 위험도 |
|---|------|-----------------|------------------|------------------|----------------|--------------------|----------|--------|
| B1 | 위러브1 | `chul_09` | 서버1 | `remote_154` | `chul_09_db` | 위러브2/3, 교문사 (총 4) | hcode + tenant_id | **높음** |
| B2 | 위러브2 | `chul_09` | 서버2 | `remote_155` | `chul_09_db` | 동상 | 동상 | **높음** |
| B3 | 위러브3 | `chul_09` | 서버3 | `remote_153` | `chul_09_db` | 동상 | 동상 | **높음** |
| B4 | 교문사 | `chul_09` | 서버3 | `remote_153` | `chul_09_db` | 동상 | hcode (서버3 내 분리) | **높음** |
| B5 | 북앤북 | `book_07` | 서버1 | `remote_154` | `book_07_db` | 유앤북 | hcode | **높음** |
| B6 | 유앤북 | `book_07` | 서버4 | `remote_138` | `book_07_db` | 북앤북 | hcode | **높음** |

> 본 카테고리가 사고의 정확한 발화점이다. **`(remote_id, db_name)` 만으로 테넌트 식별 불가** → `(remote_id, db_name, hcode)` 또는 `tenant_id` 명시 필요. 라우팅이 "첫 매치 테넌트" 로 fail-open 되면 즉시 타사 데이터 노출.

### C) 한국도서유통 — Uses 라벨 동음, 빌드 다종 (`book_kb`)

| # | 라벨(시드) | account_family | build_role | active_build_id | parent_tenant_id | 기대 db_name | 식별 키 |
|---|-------------|-----------------|-------------|-------------------|---------------------|----------------|----------|
| C1 | 한국도서유통 | `book_kb` | distributor | `BLD-DIST-KBT` | (none) | `book_kb_db` | tenant_id |
| C2 | 한국도서유통(출판) | `book_kb` | publisher | `BLD-PUB-KBT` | C1 | `book_kb_db` | tenant_id (parent=C1) |

> Uses 라벨이 `한국도서유통` 으로 동음 — `(tenant_id, build_role)` 쌍으로만 단일화 가능 (DSN-DEC-06).

### D) 슈퍼관리자 / 운영자 (락아웃 회피)

| # | login_id 패턴 | hcode | account_type | 라우팅 | 비고 |
|---|----------------|--------|----------------|---------|------|
| D1 | `admin` (BLS_ADMIN_USER_IDS) | `0000` 또는 임의 | T1 | `BLS_AUTH_SERVER_ID` 폴백 OK | `should_bypass_login_id_index_ambiguity()` 통과 |
| D2 | `web_admin.json::role-admin` | 임의 | T1 | 동상 | 동상 |

### E) 동명 ID — 인덱스 ambiguous

| # | 시나리오 | 정책 (default) | 정책 (strict opt-in) |
|---|----------|------------------|------------------------|
| E1 | `미래가치` 가 `chul_05_db` + `chul_09_db` 양쪽에 존재, 비밀번호는 한쪽만 일치 | 비밀번호 narrowing (DSN-DEC-09 v2) — 매치 후보 1건 결정, 감사 `ambiguous_narrowed=true` | `BLS_LOGIN_AMBIGUOUS_PROBE=block` → 즉시 401 |
| E2 | 동명 ID + 양쪽 모두 비밀번호 일치(드문 케이스) | 우선순위 첫 후보로 결정 + `candidate_attempts > 1` 감사 | E1 strict 적용 |

### F) 인덱스 miss + directory_sweep

| # | 시나리오 | 동작 | 위험 |
|---|----------|--------|------|
| F1 | 신규 가입자 인덱스 미반영 | `BLS_LOGIN_DIRECTORY_SWEEP=1` 일 때 활성 테넌트 N건 시도 | sweep 후 첫 성공 DB 가 우연히 타사이면 노출 → DSN-DEC-12 가드로 차단 |

---

## 2. 검증 절차 (대표 계정 풀 PASS)

대표 계정 1건당 다음 산출물을 수집한다 — `--probe` 는 read-only 자격 환경에서만.

```bash
PYTHONPATH=도서물류관리프로그램/backend \
  python3 debug/diagnose_login_routing.py <login_id> \
    --write-json /tmp/diag_<login_id>.json
```

각 결과 JSON 에서 다음 필드를 본 매트릭스 기대값과 1:1 비교한다.

| 필드 | 출처 | 기대 |
|------|------|------|
| `index_lookup.lookup.status` | `login_id_index` | `single` 또는 `ambiguous(보조 입력 필요)` |
| `single_route.via` | `resolve_login_route` | A 카테고리: `tenant_id` / `account_family` / `index`. B/C: `tenant_id` 우선 |
| `candidates[].remote_id`, `db_name` | `resolve_login_route_candidates` | 표 §1 기대 (remote_id, db_name) 에 1순위 매치 |
| `policy_simulation.would_block_before_probe` | strict 모드 | A/D: false, E1 (default): false, E1 (strict): true |
| (옵션) `probe_results[].result == "password_match"` 행의 `tenant_id` | DB 검증 | 본 매트릭스의 기대 `tenant_id` 와 동일 |

> 자동 회귀 가드는 [test/test_auth_login_cross_tenant_isolation.py](../test/test_auth_login_cross_tenant_isolation.py) 가 동일 매트릭스를 mock 으로 재현해 PR 단계에서 차단한다.

---

## 3. 알려진 시드 충돌 / 정정 후보

[tools/audit_welove_routing_consistency.py](../tools/audit_welove_routing_consistency.py) 가 본 시드와 [analysis/welove_db_route_matrix.json](../analysis/welove_db_route_matrix.json) 를 1:1 비교해 정확히 다음 카테고리로 분류해 출력한다 — 동일 도구가 회귀 가드도 겸한다.

| 코드 | 의미 | 운영 정책 |
|------|------|-----------|
| `SHARED_DB_NO_HCODE_GUARD` | 공유 DB 케이스인데 시드에 `hcode_pattern` 등 격리 키 부재 | 운영자 보강 PR 필수 (DSN-DEC-12 적용 전제) |
| `MATRIX_NOT_IN_SEED` | 레거시 매트릭스에 있으나 시드에 누락 | 시드 추가 PR (T2_DIST/T3 분류 + tenant_id UUIDv5) |
| `SEED_NOT_IN_MATRIX` | 시드에만 있고 매트릭스에 없음 | 신규 운영 테넌트 — 정상. `notes` 에 출처 명시 권장 |
| `PRIMARY_SERVER_MISMATCH` | 동일 라벨인데 시드/매트릭스의 `primary_server` 불일치 | 운영 정본 우선 — 매트릭스 갱신 후 시드 검토 |
| `DB_NAME_LOGICAL_MISMATCH` | 동일 라벨인데 `db_name_logical` 불일치 | 시드 정본 — 매트릭스 갱신 |
| `DB_NAME_LOGICAL_MISSING` | 매트릭스에서 `db_name_logical` 빈 항목 (예: `sky_01`) | 운영자 확인 필요 |

---

## 4. 변경 로그

| 날짜 | 변경 |
|------|------|
| 2026-05-21 | 초안 — 카테고리 A~F + 검증 절차 + 정정 분류 코드 |
