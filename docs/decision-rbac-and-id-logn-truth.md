# RBAC 단일 원천 + Id_Logn 정본 결정 (`DEC-RBAC-*`)

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-24 |
| 상태 | **DRAFT (사용자 승인 전)** — 본 사이클 구현 일괄 정정의 단일 결정문 |
| 추적 ID | `DEC-RBAC-01` ~ `DEC-RBAC-03` |
| 단일 원천 | 본 문서 + [`docs/onboarding-rbac-menu-matrix.md`](onboarding-rbac-menu-matrix.md) + [`analysis/rbac_menu_matrix.json`](../analysis/rbac_menu_matrix.json) (본 사이클 신설) |
| 비밀 정책 | 자격증명 0건 — [`docs/secrets-policy.md`](secrets-policy.md) G3 준수 |
| 연관 | [`migration/contracts/login.yaml`](../migration/contracts/login.yaml), [`docs/profile-password-ux-spec.md`](profile-password-ux-spec.md), [`docs/welove-publish-schema-dictionary.md`](welove-publish-schema-dictionary.md), [`docs/onboarding-account-type-resolution.md`](onboarding-account-type-resolution.md), [`docs/menu-visibility-runtime-design.md`](menu-visibility-runtime-design.md) |

---

## 0. 배경

지금까지 백엔드 모델·UI 라벨·계약 문서가 추론으로 만들어지면서 두 가지 비정합이 누적되었다.

1. `Id_Logn.gcode` / `Id_Logn.gname` 의 의미가 자료별로 충돌:
   - 스키마 사전(엑셀 추출): `gcode`=「사용자」, `gname`=「아이디」
   - 운영 계약([`migration/contracts/login.yaml`](../migration/contracts/login.yaml)): `gcode`=Logn2 로그인 코드/사번, `gname`=Logn1 작업자 이름
   - 프로필 UX 스펙([`docs/profile-password-ux-spec.md`](profile-password-ux-spec.md)): `gname`=display_name, `gcode`=login_id (불변)
2. 메뉴 권한 매트릭스([`docs/onboarding-rbac-menu-matrix.md`](onboarding-rbac-menu-matrix.md))가 정리돼 있으나, 실제 사이드바([`도서물류관리프로그램/frontend/src/components/app-shell/sidebar.tsx`](../도서물류관리프로그램/frontend/src/components/app-shell/sidebar.tsx))는 `permissions[]` 만 보고 있어 `account_type` / `build_role` / `license_keys` 분기가 미반영.

본 결정문은 위 두 결합 지점을 단일 원천으로 고정해 후속 코드/UI/문서 일괄 정정의 기준을 제공한다.

---

## 1. 핵심 결정

### `DEC-RBAC-01` — Id_Logn 의미 정본 (운영 계약 우선)

| 컬럼 | 정본 의미 | 운영 별칭 | API/UI 키 | 가변 여부 |
|------|-----------|-----------|-----------|-----------|
| `Id_Logn.Gcode` | 로그인 ID (Logn2 / 사번) | login_id | `user_id` | **불변** (계정 폐기 후 재발급) |
| `Id_Logn.Gname` | 표시명 (Logn1 / 작업자 이름) | display_name | `display_name` | 가변 (프로필에서 본인 수정 가능) |
| `Id_Logn.Hcode` | 출판사 / 테넌트 코드 | tenant_hcode | `hcode` | 관리자만 변경 |
| `Id_Logn.Hname` | 출판사명 / 조직명 | organization | `user_name` | 관리자만 변경 |

**근거**: [`migration/contracts/login.yaml`](../migration/contracts/login.yaml) §inputs/outputs (`legacy_field: Id_Logn.Gcode/Gname/Hcode/Hname`) + [`docs/profile-password-ux-spec.md`](profile-password-ux-spec.md) §PROF-FIELD-01/04/07. 스키마 사전의 한글 라벨은 엑셀 원천 그대로 유지하되, 본문에 「운영 의미: 본 결정문 참조」 보조 주석을 추가한다.

**구현 적용 범위**:

- 백엔드 Pydantic: `LoginRequest.username` → `user_id` (Pydantic `Field(alias="username")` + `populate_by_name=True` — 하위호환 유지).
- 백엔드 응답: `LoginResponse.user.username` → `user_name` (= `Id_Logn.Hname` 조직명). 추가로 `display_name` (= `Id_Logn.Gname`) 별도 키.
- 프론트 라벨: 로그인 ID 입력 = "로그인 ID", 헤더/프로필 = "이름" 또는 "표시명", 조직 표시 = "출판사명".

**적용 제외**: DB 컬럼명(`Gcode`/`Gname`/`Hcode`/`Hname`)은 그대로 — 레거시 SQL 호환을 위해 변경하지 않는다.

### `DEC-RBAC-02` — 메뉴 RBAC 단일 원천 (matrix → JSON → import)

[`docs/onboarding-rbac-menu-matrix.md`](onboarding-rbac-menu-matrix.md) 의 메뉴 표를 정본으로 삼고, 추출 도구 `tools/extract_rbac_matrix.py` 가 `analysis/rbac_menu_matrix.json` 을 산출한다. 이 JSON 을 **단일 원천**으로 다음이 모두 import 한다.

- 백엔드: `_resolve_account_type` 결과와 매트릭스 lookup 의 일관성 회귀 테스트
- 프론트엔드 `account-menu-matrix.ts`: `isMenuVisible({menuId, accountType, buildRole, licenseKeys, isSuperUser})` 순수 함수
- 사이드바 `app-shell/sidebar.tsx`: 폼 메타의 `menuId` 로 가시성 게이트
- 관리자 화면(권한 미리보기) — 후속 사이클

산출 schema 예:

```json
{
  "version": "2026-04-24",
  "menus": [
    {
      "id": "ACC-MENU-NAV-07",
      "route": "/(app)/year-month-stats",
      "caption": "년/월(통계)",
      "account_types": ["T1", "T2_PUB", "T3"],
      "build_roles": ["publisher"],
      "license_keys": [],
      "source_builds": ["P-STD", "P-KBT"]
    }
  ]
}
```

### `DEC-RBAC-03` — 게이트 키 (3중 키 + 슈퍼 우회 + 라이선스)

메뉴 노출 가시성 평가 함수의 우선순위:

1. **슈퍼 우회**: `permissions[]` 에 `*` 또는 `role=admin` 또는 `hcode=0000` → 모두 노출 (운영자 락아웃 방지, 기존 동작 유지).
2. **`account_types[]`**: 매트릭스의 허용 계정 유형 집합에 사용자 `account_type` 포함 여부.
3. **`build_roles[]`**: (있을 때만) 사용자 `build_role` 이 매트릭스 허용 집합에 포함되어야 함.
4. **`license_keys[]`**: (있을 때만) 매트릭스가 요구하는 모든 키가 사용자 `license_keys` 에 존재해야 함 (AND).
5. **레거시 `permissions[]` (Seek_Uses 'F##')**: 폼 단위 `requiredPermission` 은 매트릭스와 **AND** 결합 — 둘 다 통과해야 노출.

비고:

- `account_type`/`build_role`/`license_keys` 산출은 [`docs/onboarding-account-type-resolution.md`](onboarding-account-type-resolution.md) 의 ACTR-DEC-01~05 우선순위에 따른다 (본 사이클에서 ACTR-DEC-01 가산 구현).
- `license_keys` 출처: `tenants_directory(.overlay).features` ∪ `publisher_whitelist[*].license_keys` (있는 경우) ∪ matrix 기본값. JWT 60키 한도(DSN-DEC-07)는 그대로.
- 매트릭스에 `account_types`/`build_roles`/`license_keys` 가 비어 있으면 **해당 차원은 통과** (제약 없음) 으로 해석한다.

---

## 2. 비파괴 / 안전 원칙

- 필드 rename 은 모두 alias 동반(파괴 변경 금지). 기존 `username` 요청도 그대로 수용.
- 사이드바 게이트는 매트릭스 + 기존 `permissions` 의 **AND** — 더 엄격해질 뿐, 기존 노출 항목이 임의로 늘어나지 않는다.
- 슈퍼유저 우회는 그대로 유지 — 운영자 락아웃 회피.
- 토큰/비번/첨부 본문 미적재 정책(SEC-POL-CITE-03/04, G3) 그대로.
- 신설 메뉴 라우트는 placeholder + RBAC 가드 — 본 구현은 별 사이클로 분리.

---

## 3. 추적 / 후속

- 본 결정문 등록 후 [`docs/welove-tracking-ids-backlog.md`](welove-tracking-ids-backlog.md) 에 `DEC-RBAC-01~03`, `MAN-009`, `ACC-MENU-NEW-*`, `MENU-MATRIX-EXPORT-*` 신규 ID 등록.
- 후속 사이클: 관리자 권한 미리보기 화면, license_keys 의 features.json 정식 매핑, 매트릭스 변경 시 CI 회귀 가드.
