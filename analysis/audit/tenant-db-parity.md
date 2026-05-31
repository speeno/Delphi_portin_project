# 테넌트 DB 매핑 패리티 — 진단·수정 DoD (DSN-DEC-12 / ACC-DATA-03)

교문사 레거시 엑셀을 첫 Ground Truth 로, "웹이 올바른 DB + 테넌트(hcode 격리) 로
붙는가" 를 **계정 무관 공통 규칙**으로 검증·수정한 결과를 기록한다. 교문사 전용
하드코딩은 두지 않으며, 동일 클래스의 오매핑이 다른 공유 DB 계정에도 함께 해소된다.

## 1. 루트 원인 — 공유 좌표 tenant_id 붕괴

`login_id_index.json` 은 공유 DB 좌표(`remote_153`/`chul_09_db`)의 **모든 로그인을
단일 tenant_id 로 붕괴**시킨다. 실측:

| 로그인 | index hcode | index tenant_id | 라벨 |
|--------|-------------|-----------------|------|
| `교문사` | 5019 | `94455c23-…` | **위러브3** (← 교문사 아님) |
| `교문사 전자책` | 5097 | `94455c23-…` | **위러브3** |

seed 의 교문사 tenant_id 는 `fa6758ea-…` 인데, index 는 좌표 대표값(위러브3)을 부여한다.
이전 auth 는 이 index tenant_id 를 `resolve_unique_tenant` 의 `tenant_id_hint` 로 넘겨,
hcode 격리보다 **먼저** 잘못된 테넌트를 `unique` 로 확정했다 → 교문사 로그인이 위러브3
컨텍스트로 매핑(타사 데이터 노출 위험).

재현(수정 전):

```text
resolve_unique_tenant(remote_153, chul_09_db, hcode=5019, tenant_id_hint=94455c23(위러브3))
  → unique → 위러브3   # 잘못된 매핑
```

## 2. 일반화 수정 (코드 분기 0)

[`auth_service._resolve_account_type`](../../도서물류관리프로그램/backend/app/services/auth_service.py)
의 DSN-DEC-12 가드에 **explicit(UI 입력) tenantId 만** 단일화 힌트로 전달하고,
index 파생 tenant_id 는 더 이상 가드 단일화에 쓰지 않는다. 공유 좌표 단일화는
hcode 격리(`hcode_in`/`hcode_pattern`/`hcode_prefix`)에 위임한다.

수정 후 동작(교문사 로그인, 명시 tenantId 없음):

| 조건 | 결과 |
|------|------|
| 격리 키 부재 | `ambiguous` → `tenant_id=None` (fail-closed, **위러브3 매핑 금지**) |
| `hcode_in` 격리 키 존재 | hcode 로 **교문사** 정확 해석 (잘못된 index tid 무시) |
| 명시 tenantId(UI) | 그대로 신뢰 |

이 규칙은 `if 교문사` 분기 없이 **모든 공유 DB 계정**(B1~B6)에 동일 적용된다.

## 3. 라우팅 패리티 실측 (오프라인, 자격증명 0건)

`PYTHONPATH=도서물류관리프로그램/backend python3 debug/probe_tenant_master_parity.py`

| Case | 테넌트 | 좌표 | owners | ownership(no hint) | 결과 |
|------|--------|------|--------|--------------------|------|
| B1 | 위러브1 | remote_154/chul_09_db | 1 | unique | OK |
| B2 | 위러브2 | remote_155/chul_09_db | 1 | unique | OK |
| B3 | 위러브3 | remote_153/chul_09_db | 2 | ambiguous | OK (격리 대기) |
| B4 | 교문사 | remote_153/chul_09_db | 2 | ambiguous | OK (격리 대기) |
| B5 | 북앤북 | remote_154/book_07_db | 1 | unique | OK |
| B6 | 유앤북 | remote_138/book_07_db | 1 | unique | OK |
| A1~A5 | 단독 DB | — | 1 | unique | OK |

핵심: **런타임 공유 좌표는 `remote_153`/`chul_09_db`(B3·B4) 단 하나**다. B1/B2/B5/B6 은
같은 논리 DB 라도 `server_id` 가 달라 좌표 단위로는 단일화된다(`logical_shared_db`).

## 4. 라이브 도출 결과 — **해소(resolved)** (2026-05-30, remote_153 read-only)

엑셀에는 `Hcode` 컬럼이 없어 소관 hcode 를 라이브로 결정적 역산했다 (추정 0건).

### 4-a. 소관 hcode 결정적 도출 (엑셀 = Ground Truth)

`debug/probe_master_hcode_scope.py --server remote_153 --family chul_09 --baseline-xref gyomunsa`
(엑셀 gcode 를 `G4_Book`/`G1_Ggeo` 와 이름 일치 교차조회 → 소유 Hcode 역산)

| 신호 | 결과 |
|------|------|
| 엑셀 name-match Hcode 분포 | **100% → Hcode 5019** (books 2668·customers 654, 타 hcode 누출 0) |
| `G4_Book` Hcode=5019 행수 | **3437** = 엑셀 books 3437 (정확 일치) |
| `G1_Ggeo` Hcode=5019 행수 | **1289** = 엑셀 customers 1289 (정확 일치) |
| `Id_Logn` `교문사`/`경리부` | hname=`(주)교문사`, **hcode=5019** (배타적) |

→ 교문사 = **Hcode 5019** (이전 가정 `5056` 은 오류: 5056 은 books 3213/customers 7003 로 불일치). `Gcode` 는 테넌트별 순번이라 좌표 전역에서 비유일 → **이름 일치만이 결정적 신호**.

### 4-b. 소유권 분할 (교문사 vs 위러브3, 증거 기반)

| 테넌트 | tenant_id | `hcode_in` | 근거 |
|--------|-----------|-----------|------|
| 교문사 | `fa6758ea-…` | `["5019"]` | 4-a (엑셀·로그인·마스터 3중 일치) |
| 서버3(위러브3) | `94455c23-…` | `["0000","5000"]` | `Id_Logn`: `위러브`(0000)·`위러브출판사`(5000) 배타적. 자체 데이터 미미(4·13건). 좌표의 125k 행 대부분은 ~200개 타 입주 출판사 hcode 로 위러브3 식별과 무관 |

두 집합 교집합 = ∅ → 로그인 hcode→테넌트 결정적. 근거는 [`welove_shared_db_hcode_candidates.json`](../welove_shared_db_hcode_candidates.json) `partition_evidence` 에 보존.

### 4-c. 마스터 스코프 루트 원인 — **로그인 hcode 가 JWT 에 누락** (추가 발견·수정)

라이브 검증 중, `chul_09` T3 로그인의 **JWT `hcode` 가 빈 값**이라 `resolve_scope_hcode` 가
`None` → 교문사가 **창고 전체(books 125,870 / customers 68,036)** 를 보던 격리 결함을 발견했다.
근본 원인: `servers.yaml` `auth.query` 가 표준 컬럼 `hcode AS hcode` 를 누락(드리프트)하고
hcode 를 `auth_flags = CONCAT(hcode,':',gname)` 합성 문자열에만 노출 → `row.get('hcode')` 공백.

일반화 수정(계정·서버 무관):
- 코드: [`auth_service._row_hcode`](../../도서물류관리프로그램/backend/app/services/auth_service.py) — 표준 hcode 컬럼이 비면 `auth_flags` 접두에서 hcode 복원(방어선). `CONCAT` 만 유지한 모든 쿼리 변형에 동작.
- 설정: `servers.yaml` `auth.query` 를 표준 `DEFAULT_AUTH_QUERY` 와 정합(`hcode AS hcode`·`gname AS display_name` 복원).

### 4-d. 적용 + 라이브 패리티 (green)

1. overlay: `python3 tools/apply_hcode_isolation_overlay.py --filled analysis/welove_shared_db_hcode_candidates.json --apply` → [`tenants_directory_overlay.json`](../../도서물류관리프로그램/backend/data/tenants_directory_overlay.json).
2. `python3 tools/audit_welove_routing_consistency.py --strict` → critical `SHARED_COORD_NO_HCODE_GUARD` **2건 → 0건** (exit 0). 감사도 런타임처럼 seed+overlay 유효 뷰를 평가하도록 보강.
3. 라이브 마스터 diff (교문사):

| 항목 | web_total | baseline | key diff | match |
|------|-----------|----------|----------|-------|
| books | **3437** | 3437 | 0/0 | ✅ |
| customers | **1289** | 1289 | 0/0 | ✅ |

   JWT: `tenant_id=fa6758ea`, **`hcode=5019`**. (gcode zero-pad `00001`↔엑셀 `1` 정규화로 키셋 0 diff.)
4. **원 버그 종결**: 교문사 로그인(명시 tenantId 없이) → `tenant_id=fa6758ea`(교문사)·`hcode=5019`·warnings 0. 이전엔 위러브3 로 매핑되던 케이스가 hcode 격리로 단일화.

### 4-e. 마스터 스코프 결정 (axis 4) — resolved

교문사 데이터가 **단일 Hcode 5019 에 정확히 정합**(3437/1289)하므로 단일-hcode scope 가
올바르며, `hcode_in` set 확장(다수 hcode)이나 별도 DEC 가 **불필요**하다. `master_data.yaml`
`tenant_data_scope` → `resolved`. (스코프 결함은 4-c 의 hcode 전파 수정으로 해소.)

## 5. 산출물

- 코드: [`auth_service._resolve_account_type`](../../도서물류관리프로그램/backend/app/services/auth_service.py) (index tid → 가드 미전달), [`auth_service._row_hcode`](../../도서물류관리프로그램/backend/app/services/auth_service.py) (hcode auth_flags 폴백)
- 설정: `도서물류관리프로그램/backend/servers.yaml` `auth.query` 표준 정합(hcode/display_name 복원, gitignored)
- 도구: [`tools/audit_welove_routing_consistency.py`](../../tools/audit_welove_routing_consistency.py) (seed+overlay 유효 뷰 병합 평가), [`tools/apply_hcode_isolation_overlay.py`](../../tools/apply_hcode_isolation_overlay.py)
- 격리 키: [`tenants_directory_overlay.json`](../../도서물류관리프로그램/backend/data/tenants_directory_overlay.json) (교문사 `5019` / 위러브3 `0000,5000`)
- 계약: [`migration/contracts/tenant_master_parity_manifest.yaml`](../../migration/contracts/tenant_master_parity_manifest.yaml) (B4 `canonical_hq_hcode=5019`), [`master_data.yaml`](../../migration/contracts/master_data.yaml) `tenant_data_scope=resolved`
- 진단: [`debug/probe_tenant_master_parity.py`](../../debug/probe_tenant_master_parity.py) (gcode 정규화), [`debug/probe_master_hcode_scope.py`](../../debug/probe_master_hcode_scope.py) (`--baseline-xref`), [`debug/import_legacy_master_baseline.py`](../../debug/import_legacy_master_baseline.py)
- 라이브 산출물(운영자 수동, CI 자동 X): [`analysis/audit/master-hcode-scope-remote153-chul09.json`](master-hcode-scope-remote153-chul09.json), [`analysis/audit/tenant-master-parity-B4.json`](tenant-master-parity-B4.json)
- baseline: `debug/baselines/gyomunsa_books.json` (3437), `gyomunsa_customers.json` (1289)
- 테스트: [`test/test_tenant_master_parity.py`](../../test/test_tenant_master_parity.py)
