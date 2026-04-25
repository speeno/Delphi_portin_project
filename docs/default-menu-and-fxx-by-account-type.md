# 계정 유형별 기본 메뉴·Id_Logn Fxx (Delphi 근거 + 자동 적용)

| 항목 | 내용 |
|------|------|
| 목적 | **총판(T2_DIST)**, **총판 소속 출판사(T2_PUB)**, **독립 출판사(T3)** (+ 자체 물류는 `build_role`·`warehouse_menu_tier`) 에 대해 웹 메뉴·API 권한(Fxx) 기본값을 한곳에서 설명하고, [migration/contracts/default_id_logn_permissions.yaml](../migration/contracts/default_id_logn_permissions.yaml) 과 동기 유지한다. |
| 인덱스 | [docs/inventory-delphi-rbac-sources.md](inventory-delphi-rbac-sources.md) |
| 메뉴 정본 | [docs/onboarding-rbac-menu-matrix.md](onboarding-rbac-menu-matrix.md) (`ACC-MENU-*`) |
| Fxx 정본 키 | `legacy-analysis/permission-keys-catalog.md` + [admin_service 시드](../도서물류관리프로그램/backend/app/services/admin_service.py) `legacy_permission_map` |

## 1. 메뉴(웹) — 계정 유형별 요약

| 계정 유형 | 레거시 셸 | 최상위 NAV 요약 (상세는 onboarding 문서 §2) |
|-----------|-----------|-----------------------------------------------|
| `T2_DIST` | distributor / 자체 물류 총판 | 기초·거래·원장·회계·자료·통계 + **출고·재고·발송비·내역서** (NAV-09~15), 총판 전용(NAV-16 등) 가능 |
| `T2_PUB` | publisher (소속) | 기초·거래·원장·회계·자료·통계 + **년/월 통계(NAV-07)** — **출판사관리(MASTERS-04) 비표시** |
| `T3` | publisher (독립) | T2-PUB 과 동일 셸에 가깝게 운영 (단독 DB) |
| `T3` + `warehouse_publisher` + `warehouse_menu_tier=lite` | 위러브형 자체 물류 | distributor 셸에서 LITE 전용 메뉴(반품재고 통합 등) — onboarding §2·§4 |
| `T3` + `warehouse_publisher` + `warehouse_menu_tier=full` | MS북스·북앤북형 | distributor 셸 8메뉴·재고/반품 분리 — onboarding §2 |

> **중요**: 위 표는 **가시성(RBAC 메뉴 매트릭스)** 이다. **API 쓰기 허용**은 별도로 `Id_Logn` Fxx `O`/`R`/`X` 로 결정되며, 기본값은 [default_id_logn_permissions.yaml](../migration/contracts/default_id_logn_permissions.yaml) 에서 관리한다.

## 2. Fxx 기본값 — 설계 원칙

1. **과잉 권한 방지**: 명시되지 않은 F 키는 계약에서 **`X`(차단)** 로 둔다.
2. **읽기 우선**: 업무에 필요한 마스터·조회는 **`R`** 로 시작하고, 운영에서 `O` 로 승격.
3. **총판 vs 출판사**: `F17`(출판사관리)은 **T2_DIST·물류형**에서 `R` 이상, **T2_PUB·T3** 에서는 **`X`** (onboarding MASTERS-04 열과 정합).
4. **관리자 콘솔**: 일반 업계 사용자 기본에서 `F18`(admin.user.write) 은 **`X`** — 슈퍼/별도 부여만 `O`.
5. **고객사 차이**: Delphi 바이너리/빌드 차이는 **YAML `customer_variants`** 만 수정 ([inventory](inventory-delphi-rbac-sources.md) §2).

## 3. 자동 적용 경로 (런타임)

| 단계 | 구성 요소 |
|------|-----------|
| 계약 로드 | `default_id_logn_permissions_service` → `migration/contracts/default_id_logn_permissions.yaml` |
| 회원 승인 | `member_signup_service.approve_request` 가 `resolve_default_permissions(...)` 결과를 `id_logn_service.create_user` 에 전달 |
| 관리 UI | `GET /api/v1/admin/id-logn/permission-defaults` + Id_Logn 페이지 **「기본 권한 적용」** |

## 4. 변경 절차

1. Delphi 또는 운영 요구 변경 → **본 문서** 요약 수정 + **YAML** `base_templates` 또는 `customer_variants` 수정.
2. PR 에 **근거 ID**(`EVID-*`) 를 본 문서 또는 인벤토리에 추가.
3. `pytest` `tests/test_default_id_logn_permissions.py` 스냅샷 갱신.
