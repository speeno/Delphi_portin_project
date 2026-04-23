# 계정 유형 자동 결정 규칙 (ACTR-*)

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-24 |
| 상태 | DRAFT — 온보딩 사이클 1차 |
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
| `T3` | 독립 출판사 | 단독 운영 출판사 | `book_*` |
| `T3_WAREHOUSE_LITE` | 독립 출판사 + 자체 물류(경량) | 출판사관리 부재, 7 메뉴 | `chul_09` (위러브) |
| `T3_WAREHOUSE_FULL` | 독립 출판사 + 자체 물류(완전) | 출판사관리 보유, 8 메뉴 | `book_21` (MS북스), `book_07` (북앤북) |

---

## 2. 결정 우선순위 (`ACTR-DEC-01..05`)

### `ACTR-DEC-01` — web_users 명시값 최우선

관리자가 승인 시 직접 지정한 `web_users.account_type` 이 존재하면 그 값 사용.

```python
if web_users.account_type:
    return web_users.account_type  # 정본
```

### `ACTR-DEC-02` — 수퍼유저 신호

`_has_admin_role_mapping(user_id)` 또는 `hcode == '0000'` 또는 `BLS_ADMIN_USER_IDS` 화이트리스트 → `T1`.

```python
if is_admin(user_id, hcode):
    return "T1"
```

### `ACTR-DEC-03` — web_publisher_whitelist 매핑

로그인한 사용자의 `hcode` 가 `web_publisher_whitelist` 에 `status=active` 인 행으로 존재하면 `expected_account_type` 사용.

```python
whl = publisher_whitelist_service.lookup(hcode)
if whl and whl["status"] == "active":
    return whl["expected_account_type"]
```

### `ACTR-DEC-04` — tenants_directory 매핑

`tenants_directory` 에서 `account_family` 또는 `tenant_label_kor` 로 조회해 `default_account_type` 사용.

```python
tenant = tenants_directory_service.lookup_by_hcode_hint(hcode, server_id)
if tenant:
    return tenant["default_account_type"]
```

`hcode_hint` 조회 전략:
- `hcode` prefix (앞 4~6자) 로 `account_family` 패턴 매칭
- 또는 `web_users.account_family` (승인 시 적재된 캐시) 직접 사용
- `(account_family, server_id)` → `tenants_directory` 조회

### `ACTR-DEC-05` — 미결정 폴백

매핑 실패 시 `""` (빈 문자열) 반환 → JWT 에 `account_type=""` 포함 → 프론트 헤더에 노란 배지 표시 → 관리자가 `(app)/admin/id-logn` 에서 수동 지정.

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
