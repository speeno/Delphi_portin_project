# 계정 유형 자동 결정 규칙 (ACTR-*)

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-24 |
| 상태 | FROZEN — 4대 상위 유형 + `warehouse_menu_tier` 보조 (2026-04-25) |
| 추적 ID | `ACTR-*` (결정 규칙 단위) |
| 단일 원천 | 본 문서 + [`migration/contracts/tenants_directory.yaml`](../migration/contracts/tenants_directory.yaml) + [`migration/contracts/web_publisher_whitelist.yaml`](../migration/contracts/web_publisher_whitelist.yaml) |
| 연관 | [`docs/decision-login-db-routing.md`](decision-login-db-routing.md) DSN-DEC-06/07, [`docs/onboarding-rbac-menu-matrix.md`](onboarding-rbac-menu-matrix.md), [`docs/menu-visibility-runtime-design.md`](menu-visibility-runtime-design.md) MENUVIS-DEC-04 |

---

## 1. 계정 유형 코드표

| 코드 | 의미 | 대상 | 빌드 계열 |
|------|------|------|----------|
| `T1` | 수퍼관리자 | 시스템 관리자 | 특수 계정 |
| `T2_DIST` | 총판(물류사) | 물류센터 운영사 | `BLD-DIST-*`, `chul_*`, `book_kb` |
| `T2_PUB` | 총판 소속 출판사 | 총판에 등록된 출판사 | `BLD-PUB-*` |
| `T3` | 독립 출판사 | 단독 운영 출판사 또는 자체 물류 보유 출판사 | `book_*` / `chul_09` / `book_21` / `book_07` 등 |
| *(레거시 입력)* `T3_WAREHOUSE_*` | *(접힘)* | JWT·로그인 응답에서는 **`T3`** 만 노출 | 시드·구버전 JWT 호환 입력 → 내부에서 `T3` + `warehouse_menu_tier` 로 복원 |
| `warehouse_menu_tier` | *(JWT·메뉴 보조)* | `lite` (WH-WL / chul_09) \| `full` (WH-MS·WH-BB / book_21·book_07·book_kb) \| 빈 문자열 | `auth_service` + `account_type_policy` |

---

## 2. 결정 우선순위 (`ACTR-DEC-01..05`)

> **운영 함수 정합 (DEC-RBAC-03 정합)**: 실제 ``app.services.auth_service._resolve_account_type``
> 의 분기 순서는 **수퍼유저(DEC-02) → web_users(DEC-01) → whitelist(DEC-03) → tenants(DEC-04) → 폴백(DEC-05)** 이다.
> 종단에서 상위 ``account_type`` 은 **T1/T2_DIST/T2_PUB/T3** 네 값으로 접으며, 자체 물류 LITE/FULL 구분은 ``warehouse_menu_tier`` 로만 노출한다.
> DEC-01 이 "명시 우선순위" 라는 의미는 *비-슈퍼* 사용자에 한해 가장 강한 출처가 web_users 라는 뜻이며,
> 운영자 락아웃 방지를 위해 슈퍼유저(`hcode='0000'` / `BLS_ADMIN_USER_IDS` / role 매핑) 는 모든 출처에 우선한다.
> 회귀 잠금: ``backend/tests/test_actr_priority.py`` (6 케이스).

### `ACTR-DEC-02` — 수퍼유저 신호 (런타임 최우선)

`_has_admin_role_mapping(user_id)` 또는 `hcode == '0000'` 또는 `BLS_ADMIN_USER_IDS` 화이트리스트 → `T1` + `build_role='super'`.
**운영자 락아웃 방지를 위해 모든 출처(web_users 포함) 보다 우선 적용된다.**

```python
if is_admin(user_id, hcode):
    return "T1"
```

### `ACTR-DEC-01` — web_users 명시값 (비-슈퍼 사용자 최우선)

관리자가 승인 시 직접 지정한 `web_users.account_type` 이 존재하면 그 값 사용.
1차 구현: ``member_signup_service.list_requests(status="approved")`` 의
``login_id == user_id`` 행을 임시 정본으로 사용 (TODO: 정식 ``web_users`` 저장소 도입 시 교체).

```python
if web_users.account_type:
    # 구현: auth_service 종단에서 account_type_policy.canonicalize_account_type 로 T3 로 접고
    # warehouse_menu_tier 를 채운다.
    return resolved.account_type
```

### `ACTR-DEC-03` — web_publisher_whitelist 매핑

로그인한 사용자의 `hcode` 가 `web_publisher_whitelist` 에 `status=active` 인 행으로 존재하면 `expected_account_type` 사용.
단, **동일 hcode 다중 총판** 가능성을 고려해 런타임 판정은 반드시 `dist_hcode + publisher_hcode(hcode)` 복합 조건을 우선 사용한다.
`hcode` 단독 조회 결과만으로 `T2_PUB` 를 확정하지 않는다.

```python
whl = publisher_whitelist_service.lookup(hcode)
if whl and whl["status"] == "active":
    return whl["expected_account_type"]
```

### `ACTR-DEC-04` — tenants_directory 매핑

`tenants_directory` 에서 `default_account_type` / `build_role` 을 읽는다. **동일 `hcode` 가 복수 테넌트에 걸쳐 있을 수 있어** `hcode` 단독 역매핑은 신뢰할 수 없다.

운영 구현 (`app.services.auth_service._resolve_account_type`) 은 다음 순서로 테넌트 row 를 해석한다.

1. **DSN-DEC-09** `login_id_index` 조회: 서버 전체 `SHOW DATABASES` + `Id_Logn` 보유 DB 스캔으로 만든 `(Gcode, Hcode, 논리 db_name, remote_id)` 힌트를 소비해 `tenant_id` / `account_family` 를 복원한다. `ambiguous` 이면 `resolved_db`(인증에 사용한 논리 DB명)로 후보를 좁혀 단일화한다.
2. `tenant_id` 가 있으면 `tenants_directory_service.lookup_by_tenant_id` 로 시드 row 를 로드한다.
3. 아니면 `account_family` + `server_id` 로 `lookup_by_account_family` 를 호출한다. (`server_id` 는 `remote_*` 형태이며, 시드의 `primary_server` 한글 라벨과 동등 비교된다.)
4. 그래도 없으면 `lookup_by_hcode_hint` 로 폴백한다(레거시·테스트 호환).

```python
# 의사코드 — 실제는 auth_service._resolve_account_type 참고
idx = login_id_index_service.lookup(login_id=user_id, hcode=hcode)
tenant = resolve_tenant_from_index_and_tenants_directory(idx, resolved_db, server_id)
if tenant:
    return tenant["default_account_type"]
```

### `ACTR-DEC-05` — 미결정 폴백

매핑 실패 시 `""` (빈 문자열) 반환 → JWT 에 `account_type=""` 포함 → 프론트 헤더에 노란 배지 표시 → 관리자가 `(app)/admin/id-logn` 에서 수동 지정.

### `DEC-RBAC-03` — license_keys 합집합(union)

``account_type`` 결정 결과와 **무관하게**, license_keys 는 다음 3 소스의 합집합으로 산출된다 (정렬·중복 제거).
JWT 60키 한도(DSN-DEC-07) 는 ``app/routers/auth.py`` 에서 적용한다.

  1. ``tenants_directory(.overlay).features`` 또는 ``.license_keys``
  2. ``publisher_whitelist[hcode].license_keys``
  3. ``web_users(=approved signup row).license_keys``

회귀 잠금: ``backend/tests/test_license_keys_union.py`` (7 케이스).

---

## 3. 결정 흐름도

```
로그인(user_id, hcode)
  │
  ├─ [ACTR-DEC-01] web_users.account_type set?
  │       YES → 해당 값 반환
  │       NO ↓
  │
  ├─ [ACTR-DEC-02] admin 신호?
  │       YES → T1
  │       NO ↓
  │
  ├─ [ACTR-DEC-03] whitelist[hcode] hit?
  │       YES → whitelist.expected_account_type
  │       NO ↓
  │
  ├─ [ACTR-DEC-04] tenants_directory 조회 성공?
  │       YES → tenant.default_account_type
  │       NO ↓
  │
  └─ [ACTR-DEC-05] "" → 관리자 매핑 대기 배지
```

---

## 4. JWT 클레임 (DSN-DEC-07 정합)

로그인 성공 시 JWT payload:

```json
{
  "sub": "<user_id>",
  "sid": "<primary_server_id>",
  "hcode": "<출판사코드>",
  "role": "admin|operator|...",
  "permissions": ["outbound.read", "..."],
  "pset": true,
  "account_type": "T2_PUB",
  "tenant_id": "tendir-chul05-jungang-001",
  "account_family": "chul_05",
  "build_role": "publisher",
  "license_keys": ["F11", "F12", "F17", "F18"]
}
```

- `license_keys[]` 1차: `analysis/welove_chul_menu_handlers.json::handlers[*].license_keys_checked` 합집합 중 `tenant_features.granted=true` 인 것만 포함. 1차 운영은 모든 테넌트에 합집합 풀 부여 후 점진 폐지 (DSN-DEC-07 §5).
- JWT 크기 가드: `license_keys` 60키, `permissions` 30키 한도.

---

## 5. 회원가입 → 계정 유형 결정 흐름

### T2-PUB (총판 소속 출판사)

```
가입 위저드 Step1 → T2-PUB 선택
    → Step2: 총판 드롭다운 선택 + 출판사 hcode 검색
    → web_publisher_whitelist lookup
    → matched: Step3 제출 가능, requested_account_type=T2_PUB, whitelist_match=matched
    → not_matched: "총판 관리자에게 등록 요청" 안내 (ONB-REJ-NOT_IN_WHITELIST)
    
관리자 승인 시:
    → approve_request(account_type=T2_PUB, tenant_id=..., dist_hcode=...)
    → activation_token 발급
    → 사용자에게 활성화 링크 안내
```

### T3 (독립 출판사)

```
가입 위저드 Step1 → T3 선택
    → Step2: 출판사명/사업자번호/대표자 자유 입력
    → web_publisher_whitelist 검증 없음 (독립)
    
관리자 승인 시:
    → account_type=T3 (또는 T3_WAREHOUSE_LITE/FULL) 수동 지정
    → activation_token 발급
```

### T2_DIST (총판 / 물류센터) — 온라인 가입 + 계약 승인 워크플로우 (`ACTR-DEC-01` 우선)

T1(수퍼관리자)만 차단하고, T2_DIST 도 공개 가입 신청을 허용한다. 단 출판사 목록 엑셀 첨부와 계약 PDF 활성화가 강제된다.

```
가입 위저드 Step1 → T2_DIST 선택
    → Step2: 회사 기본 정보(11 필드) + tenant_label_kor + primary_server_hint?
        + 출판사 목록 엑셀(.xlsx, ≤5MB) 다운로드 → 작성 → 업로드 (ONB-DIST-SUBMIT)
    → POST /api/v1/public/signup-requests/distributor (multipart)
        → attachment_service.save (ATT-VAL-*)
        → distributor_publishers_excel.parse_publisher_rows (parsed_publisher_count + parse_warnings)
        → status=contract_review (다른 유형은 pending)

관리자 검토 (T1 또는 dist_hcode 범위 T2_DIST):
    → GET /api/v1/admin/signup-requests/{id}/attachment (엑셀 다운로드)
    → POST /api/v1/admin/signup-requests/{id}/contract (PDF, ≤10MB)
        → contract_pdf_id, contract_signed_at 기록 (ONB-DIST-CONTRACT)
    → POST /api/v1/admin/signup-requests/{id}/approve
        → 계약 PDF 미첨부 시 422 SIGNUP_APPROVE_CONTRACT_REQUIRED
        → tenants_directory.upsert_tenant (overlay 파일에만 기록 — 시드 무손상, TENDIR-UPSERT-*)
        → publisher_whitelist.bulk_upsert(dist_hcode, rows) (부분 실패 허용, WHL-BULK-*)
        → Id_Logn 생성 + activation_token 발급 (ONB-DIST-APPROVE)
```

- ACTR 적용: 승인 시 `web_users.account_type=T2_DIST` 가 직접 적재되므로 이후 로그인은 ACTR-DEC-01 로 즉시 결정.
- 계약 PDF / 첨부 엑셀의 본문은 `attachments_index.json` 에 적재 금지(SEC-POL-CITE-03). 인덱스에는 `id, original_filename, content_type, size_bytes, sha256, related_*` 만 기록.

---

## 6. 사전등록(레거시) 사용자 활성화 흐름

레거시 Id_Logn 에 이미 gcode/hcode 가 존재하는 사용자가 웹에서 로그인하려면 비밀번호 재설정이 필요.

```
(public)/activate/lookup
    → hcode + 출판사명 (+ 이메일 last4) 입력
    → POST /api/v1/public/activate/lookup
    → 매칭 성공: activation_token 발급 + 안내 (이메일·화면)
    
(public)/activate/{token}
    → 새 비밀번호 설정
    → POST /api/v1/public/activate/{token}
    → OK → 로그인 페이지 리다이렉트
```

---

## 7. 위험 / 미결

| ID | 내용 |
|----|------|
| `ACTR-RISK-01` | `ACTR-DEC-03` 화이트리스트 조회 시 동일 hcode 가 복수 총판에 등록될 수 있음 — `dist_hcode` 와 함께 복합 조회 필수 |
| `ACTR-RISK-02` | `ACTR-DEC-04` hcode_hint 매칭이 실패하면 account_type="" — admin 주의 배지가 출력되지 않을 경우 권한 과부여 위험. 프론트 가드 추가 필요 |
| `ACTR-RISK-03` | T1 가입은 공개 경로 차단 (HTTP 403) — 비상 부트스트랩은 `BLS_ADMIN_USER_IDS` 환경변수로만 |
| `ACTR-RISK-04` | 레거시 사용자 `account_type` 자동 결정이 틀릴 경우 (ACTR-DEC-04 오탐) 잘못된 메뉴 노출 — admin 재지정 플로우로 수정 가능 (ACTR-DEC-01 우선) |
| `ACTR-RISK-05` | 동일 DB(`same_db`)는 총판 소속의 강한 후보 신호지만 확정 신호가 아님 — `Hcode`/관계키(`dist_hcode`,`parent_tenant_id`) 불일치 시 소속 확정 금지 |
| `ACTR-RISK-06` | 미소속 출판사 사후 전환은 총판(T2_DIST) 전용 + 동일DB 제약으로만 허용해야 함 — cross-DB 전환은 `AFFILIATION_CROSS_DB_FORBIDDEN` 로 차단 |
