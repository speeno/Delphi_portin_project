# Delphi / 레거시 RBAC 근거 인벤토리 (증거 ID 규칙)

| 항목 | 내용 |
|------|------|
| 목적 | 계정 유형별 메뉴·Fxx 기본값 문서·계약 작성 시 **재조회 가능한 출처** 목록 |
| 추적 ID | `EVID-DELPHI-*` (신규 행마다 증가), `EVID-WEB-*` (웹 매트릭스 행) |

## 1. 증거 ID 규칙

- `EVID-DELPHI-<고객코드>-<파일약칭>-L<라인>` — 예: `EVID-DELPHI-WL-Chul-L2451`
- `EVID-WEB-ACC-MENU-<메뉴ID>` — [docs/onboarding-rbac-menu-matrix.md](onboarding-rbac-menu-matrix.md) 의 `ACC-MENU-*` 행
- `EVID-JSON-<파일명>` — [analysis/welove_chul_menu_matrix.json](analysis/welove_chul_menu_matrix.json), [analysis/welove_chul_menu_handlers.json](analysis/welove_chul_menu_handlers.json) 등

## 2. 고객사·빌드별 Delphi 소스 (인벤토리 — 확장용)

| 고객/빌드 ID | Delphi / 산출물 경로 (워크스페이스 기준) | 웹 매트릭스 정본 |
|--------------|------------------------------------------|------------------|
| `BLD-DIST-STD` / `D-STD` | `docs/welove-chul-build-menu-matrix.md` + `analysis/welove_chul_menu_matrix.json` | `ACC-MENU-*` 의 T2-DIST 열 |
| `BLD-PUB-STD` / `P-STD` | 동상 + `docs/welove-ftp-tongpan-chulpan-chul-menu-diff.md` | T2-PUB / T3 publisher 셸 |
| `BLD-DIST-KBT` / `D-KBT` | 동상 (총판 KBT 확장) | NAV-16, MASTERS-04b 등 D-KBT 단독 행 — `customer_variants` 예시는 `account_family: chul_02` + `F50` 패치 |
| `WH-WL` / `WH-MS` / `WH-BB` | 동상 § T3-LITE / T3-FULL | `T3_WAREHOUSE_*` 열 |
| (추가 고객) | `customer_variants` 에 **바이너리 경로·저장소 루트**를 문자열로 기록 후 본 표에 한 줄 추가 | [migration/contracts/default_id_logn_permissions.yaml](../migration/contracts/default_id_logn_permissions.yaml) |

## 3. 웹·백엔드 정본 (이미 존재)

| 산출물 | 경로 |
|--------|------|
| 메뉴 RBAC (문서) | [docs/onboarding-rbac-menu-matrix.md](onboarding-rbac-menu-matrix.md) |
| 메뉴 RBAC (계약 JSON) | [migration/contracts/rbac_menu_matrix.yaml](../migration/contracts/rbac_menu_matrix.yaml) |
| Fxx ↔ permission_code | [도서물류관리프로그램/backend/app/services/admin_service.py](../도서물류관리프로그램/backend/app/services/admin_service.py) `_DEFAULT_LEGACY_PERMISSION_MAP` |
| 권한 동등성 계획 | [docs/user-permission-management-plan.md](user-permission-management-plan.md) |

## 4. 후속 작업 (SME)

- 고객사별 바이너리/소스가 위 표에 없으면 **1행 추가 + `customer_variants` 패치**로만 반영한다 (코드 하드코딩 분기 금지).
