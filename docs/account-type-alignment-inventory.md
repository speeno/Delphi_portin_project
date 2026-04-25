# 계정 유형(account_type) 정합 — 코드·데이터 인벤토리

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-25 |
| 상태 | 운영 정본 — 4대 상위 유형 + 보조 속성 |
| 추적 | 계정 유형 정합 재정의 플랜 `acct-*` |

## 1. 상위 유형 정본 (런타임 노출)

| 코드 | 의미 | 보조 속성 |
|------|------|-----------|
| `T1` | 수퍼관리자 | `build_role=super` |
| `T2_DIST` | 총판(물류) | `build_role=distributor` |
| `T2_PUB` | 총판 소속 출판사 | `build_role=publisher`, `dist_hcode` 필수 |
| `T3` | 독립 출판사 | 일반: `build_role=publisher` / 자체 물류: `build_role=warehouse_publisher` + `warehouse_menu_tier` |

레거시 값 `T3_WAREHOUSE_LITE` / `T3_WAREHOUSE_FULL` 은 **시드·승인 row·JWT 구버전 입력** 으로만 남을 수 있으며,
`app.services.auth_service._resolve_account_type` 종단에서 **`T3` 로 접고** `warehouse_menu_tier` 로만 LITE/FULL 메뉴 셸을 구분한다.

## 2. 단일 원천 (판정)

- **로그인/JWT**: `auth_service._resolve_account_type` → `account_type_policy.canonicalize_account_type` + `infer_warehouse_menu_tier`
- **Id_Logn Fxx 기본값**: `default_id_logn_permissions_service.resolve_default_permissions` — `T3` 베이스 + `customer_variants` 의 `match.build_role: warehouse_publisher` 패치
- **메뉴 가시성**: `docs/onboarding-rbac-menu-matrix.md` → `tools/extract_rbac_matrix.py` → `warehouse_menu_tiers` + 프론트 `isMenuVisible`

## 3. 정적 계약 분포 (시드)

| 출처 | 비고 |
|------|------|
| `migration/contracts/tenants_directory.yaml` | `default_account_type` 는 `T3` 로 통일, 자체 물류는 `build_role=warehouse_publisher` + `account_family` (chul_09·book_21·book_07·book_kb 등) |
| `migration/contracts/web_publisher_whitelist.yaml` | `expected_account_type` enum: `T2_PUB` \| `T3` |
| `migration/contracts/default_id_logn_permissions.yaml` | `base_templates` 키: `T2_DIST` / `T2_PUB` / `T3` + `customer_variants` |

## 4. 오분류 후보 (T2_PUB 누락)

| 패턴 | 기대 | 조치 |
|------|------|------|
| `dist_hcode` 가 채워진 비-총판 가입/승인 row 인데 `account_type` 이 `T2_DIST` 또는 `T3` | `T2_PUB` | `member_signup_service.approve_request` 에서 **dist 보유 시 `T2_PUB` 강제** |
| 총판 하위인데 tenants 시드가 `T2_DIST` 로만 표기 | 화이트리스트 `expected_account_type=T2_PUB` 로 ACTR-DEC-03 보정 | 계약·시드 유지 |

## 5. 자동 점검

- `python3 tools/check_account_type_consistency.py` — YAML/JSON 내 비정본 `account_type` 문자열 탐지
- `pytest 도서물류관리프로그램/backend/tests/test_account_type_normalization.py` — 정규화 단위
- `pytest 도서물류관리프로그램/backend/tests/test_actr_priority.py` — ACTR 우선순위 + 정본화
- `python3 debug/check_affiliation_integrity.py` — `dist_hcode`/`dist_tenant_id`/`parent_tenant_id` 불일치와 cross-DB 소속 전환 위험 탐지
