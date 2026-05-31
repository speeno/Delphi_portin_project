# 계정 무관 단일 정본 매핑 — Fxx → permission_code → menuId → 화면 → 버튼 caps

_생성: 2026-05-30 — account-menu-fxx-rbac **Phase B** (단일 정본 매핑 정리 / `OQ-LICENSE-KEY-MAP` 정본화)_

> **목적**: 레거시 `Id_Logn.Fxx`(O/R/X) 1셀 → 모던 권한·메뉴·화면 버튼까지 **빌드/계정 무관 단일 테이블**로 고정한다.
> 이 문서는 *결정·근거*의 단일 원천이며, 기계 소비 원천은 그대로
> [`permission-keys-catalog.md`](../../legacy-analysis/permission-keys-catalog.md)(Fxx→permission_code),
> [`rbac_menu_matrix.yaml`](../../migration/contracts/rbac_menu_matrix.yaml)(menuId→route/license_keys),
> [`menu_route_crud_map.yaml`](../../migration/contracts/menu_route_crud_map.yaml)(menuId↔API↔Fxx),
> [`form-registry.ts`](../../도서물류관리프로그램/frontend/src/lib/form-registry.ts)(화면 id/route/requiredPermission/menuId) 다.

## 입력 (정본)
- 라이브 전수: [`account-menu-fxx-all.json`](account-menu-fxx-all.json) · 집중 diff [`account-menu-fxx-5019.json`](account-menu-fxx-5019.json) (Phase A).
- 레거시 게이트 진실: 정본 빌드 `Chul.pas` `Menu…Click` 의 `Seek_Uses('F##')` (출판/총판/`chul_09(위러브)` 일치).
- 7 빌드 메뉴 합집합: [`welove_chul_menu_handlers.json`](../welove_chul_menu_handlers.json)(menu→form) · [`welove_chul_menu_matrix.json`](../welove_chul_menu_matrix.json).

## 결정 참조
- DEC-RBAC-02 (rbac 매트릭스 단일 원천) · DEC-056 (Id_Logn Fxx 어댑터) · DEC-058 (사이드바 권한 게이팅) · `OQ-LICENSE-KEY-MAP`.

---

## 1. caps 파생 규약 (O/R/X → read / write / print)

| Fxx 셀 | read | write | print | 비고 |
|---|:-:|:-:|:-:|---|
| `O` (Read-Write) | ✓ | ✓ | ✓ | 전체 CRUD + 인쇄 |
| `R` (Read-Only) | ✓ | ✗ | ✓ | 조회 + **인쇄**(레거시 R 패널만 비활성, 인쇄 버튼 유지) |
| `X` / 공백 (Deny) | ✗ | ✗ | ✗ | 메뉴 비표시 + 라우터 403 |

- **`print = read-level`**: 레거시는 별도 인쇄 Fxx 가 없다(§5). `read==true ⇒ print==true`. 별도 `*.write` 키가 `R` 이면 `*.read` 페어로 강등([`_merge_fxx_to_permissions`](../../도서물류관리프로그램/backend/app/services/auth_service.py)).
- 단일 구현 정본: [`debug/probe_account_fxx_caps.py`](../../debug/probe_account_fxx_caps.py) `derive_fkey_caps`.

---

## 2. 단일 매핑 테이블

`caps(R/W/P)` 칸은 셀 값별 산출(§1)을 요약: **O→RWP / R→R·P / X→없음**. `menuId` 는 메뉴 가시성(사이드바), `requiredPermission`(form-registry)·`fxx_keys`(라우터) 는 화면·API 게이트.

### 2.1 기초관리 (`ACC-MENU-MASTERS-*`) — 게이트 키 = Fxx 라이선스

| Fxx | permission_code (정본) | menuId | 라우트 | 화면(form-registry) | 비고 |
|---|---|---|---|---|---|
| F11 | `master.customer.read` | `ACC-MENU-MASTERS-01` | `/master/customer` | `Sobo11` | 거래처관리 |
| **F12** | `master.book.read` | `ACC-MENU-MASTERS-02` | `/(app)/masters/inbound-vendors` | (Phase F) | **입고처관리** — `Menu102`→`TSobo12` |
| **F13** | `master.book_code.read` | `ACC-MENU-MASTERS-06` | `/(app)/masters/authors` | (Phase F) | **저자관리** — `Menu103`→`TSobo13` (웹 F19 → **정정 F13**) |
| F14 | `master.alt.read` | `ACC-MENU-MASTERS-05` | `/master/book` | `Sobo14` | 도서관리 |
| **F15** | `master.misc.read` | `ACC-MENU-MASTERS-03` | `/(app)/masters/etc-customers` | (Phase F) | **기타거래처** — `Menu105`→`TSobo15` (웹 F13 → **정정 F15**) |
| F16 | `master.magazine.read` | `ACC-MENU-MASTERS-11`(특별) | `/master/special` | `Sobo16_special` | 잡지/특별 |
| F17 | `master.book_code.write` | `ACC-MENU-MASTERS-04` | `/master/publisher` | `Sobo17` | 출판사관리 |
| F18 | `admin.user.write` | `ACC-MENU-MASTERS-11` | `/master/special` | `Sobo18` | 사용자/권한 (R 페어 `F18r`=`admin.user.read`) |
| F19 | `master.misc2.read` | — | `/master/discount` | `Sobo19` | (저자=F13 정정 후 미참조) |

> **§4b 정본화**: F12/F13/F15 는 정본 빌드 `Seek_Uses` 로 확정(§3). permission_code 명은 WH 빌드 의미라 출판 화면 의미와 어긋나지만 **1 Fxx = 1 permission_code**(no build-branch) 원칙으로 유지. 3 누락 화면(입고처/기타거래처/저자) 전용 신규 permission_code 여부는 **Phase F** 결정.

### 2.2 거래·출고 (`ACC-MENU-NAV-02` 거래관리 / `NAV-09~13` 출고·재고) — 계정유형·프로파일 게이트

| Fxx | permission_code | 화면(form-registry) | 비고 |
|---|---|---|---|
| F21 | `outbound.write` | 출고 명세 | 거래명세서 |
| F22 | `outbound.cancel` | 출고 취소 | |
| F23 | `return.write` | 반품 | |
| F24 | `outbound.alt` | `Sobo24` | |
| F25 | `outbound.misc` | `Sobo25` | |
| F26 | `master.write` | 마스터 일괄 | |
| F27 | `outbound.export` | 송장/라벨 | |
| F28 | `outbound.adjust` | | |
| F29 | `outbound.return` | | |
| F31~F39 | `inventory.*` / `report.*` | 재고·통계 | warehouse 프로파일 지문 |

### 2.3 회계/정산 (`ACC-MENU-NAV-04` 회계관리) — `settlement.*`

| Fxx | permission_code | 화면 | menuId |
|---|---|---|---|
| F41 | `settlement.deposit` | 입금 | `ACC-MENU-NAV-04` |
| F42 | `settlement.misc` | | `ACC-MENU-NAV-04` |
| F43 | `settlement.report.read` | 정산 통계 | `ACC-MENU-NAV-04` |
| F44 | `settlement.bill` | | `ACC-MENU-NAV-04` |
| F45 | `settlement.write` | 청구 | `ACC-MENU-NAV-04` |
| F46 | `settlement.adj` | | `ACC-MENU-NAV-04` |
| F47 | `settlement.report.month` | 월합계 | `ACC-MENU-NAV-04` |
| F48 | `settlement.tax.read` | 세금계산서 | `ACC-MENU-NAV-04` |
| F49 | `settlement.misc2` | | `ACC-MENU-NAV-04` |

### 2.4 자료/통계 (`ACC-MENU-NAV-05`/`NAV-06`) — `report.*` (부서계정 풋프린트, §4)

| Fxx | permission_code | 화면(form-registry) | menuId |
|---|---|---|---|
| F51 | `report.kpi.read` | `Sobo51` | 자료/통계 |
| F52 | `report.kpi.write` | `Sobo52` | 자료/통계 |
| F53 | `report.delivery.read` | `Sobo53` | 자료/통계 |
| F54 | `report.return.read` | `Sobo54` | 자료/통계 |
| F55 | `report.book.read` | `Sobo55` | 자료/통계 |
| F56 | `report.cust.read` | | |
| F57 | `report.month.read` | | |
| F58 | `report.year.read` | | |
| F59 | `report.year.write` | (Interbase only) | |

`admin.stats.*` 별칭 정책 (2026-05-30)
- C13 API 라우터는 `admin.stats.*` 를 유지한다.
- Id_Logn 원본 컬럼은 `F51e/F52e/F53e`가 없으므로, 런타임 가드에서
  `admin.stats.*` 를 `report.*` read 코드 집합으로 alias 해석한다.
- 단일 원천: `backend/app/core/permission_aliases.py` /
  `frontend/src/lib/permission-aliases.ts`.

---

## 3. 기초관리 Fxx 정본화 — 레거시 근거 (Phase B step 6b)

동일 `Sobo##` 번호가 빌드마다 다른 화면을 가리킨다(빌드 변형). 정본은 **출판/총판/`chul_09(위러브)`** 빌드 `Chul.pas` `Menu10xClick` 의 실제 `Seek_Uses` 인자다. 3 정본 빌드가 **모두 일치**한다.

| 모던 메뉴 | 정본 핸들러 → 폼 | `Seek_Uses` | 웹 임시값 | 정본 | 근거 라인 ([`도서유통-출판/Chul.pas`](../../WeLove_FTP/도서유통-출판/Chul.pas)) |
|---|---|:-:|:-:|:-:|---|
| `ACC-MENU-MASTERS-02` 입고처 | `Menu102Click`→`TSobo12` | `F12` | F12 | **F12** ✓ | L1872~ `Seek_Uses('F12')` |
| `ACC-MENU-MASTERS-03` 기타거래처 | `Menu105Click`→`TSobo15` | `F15` | F13 ✗ | **F15** | L1983~ `Seek_Uses('F15')` |
| `ACC-MENU-MASTERS-06` 저자 | `Menu103Click`→`TSobo13` | `F13` | F19 ✗ | **F13** | L1909~ `Seek_Uses('F13')` |

- 총판 [`도서유통-총판/Chul.pas`](../../WeLove_FTP/도서유통-총판/Chul.pas) · 라이브 테넌트 [`chul_09(위러브)/Chul.pas`](../../WeLove_FTP/도서유통-출판/MySQL/도서유통/chul_09(위러브)/Chul.pas) **동일**.
- ⚠️ **WH 스냅샷 제외**: [`legacy_delphi_source/legacy_source/Chul.pas`](../../legacy_delphi_source/legacy_source/Chul.pas) 는 물류 빌드라 `Menu103`=`Seek_Uses('F17')`·`Menu105`=`Seek_Uses('F13')` 로 어긋난다(Sobo13/15 의미가 다름). 정본 아님.
- 정합 반영처: [`onboarding-rbac-menu-matrix.md`](../../docs/onboarding-rbac-menu-matrix.md) §3, [`rbac_menu_matrix.yaml`](../../migration/contracts/rbac_menu_matrix.yaml), [`menu_route_crud_map.yaml`](../../migration/contracts/menu_route_crud_map.yaml), [`permission-keys-catalog.md`](../../legacy-analysis/permission-keys-catalog.md) §4b.

---

## 4. F51~F55 vs settlement(F41~F49) 충돌 해소 — 라이브 근거 (Phase B step 5)

**충돌**: 카탈로그는 `F51~F55 → report.*`, `F41~F49 → settlement.*`. 그러나 `infer_login_profile` 은 `F51~F55` 만 가진 부서계정을 `department_accounting`("회계") 로 분류 → 정산을 쓰는 것처럼 오인 소지.

**라이브 실측** ([`account-menu-fxx-5019.json`](account-menu-fxx-5019.json), `remote_153`/`chul_09_db`):

| 계정 | hcode | 부여 Fxx | settlement (F41~F49) | report (F51~F55) |
|---|---|---|:-:|:-:|
| `경리부` | 5019 | F51~F55 = `O` | **전부 미부여 (X)** | **전부 `O`** |
| `교문사 전자책` | 5097 | F51~F55 = `O` | **전부 미부여 (X)** | **전부 `O`** |
| `교문사`(본계정) | 5019 | F11/F14/F17/F18/F19/F24/F25… | 미부여 | 미부여 |

**결론**:
1. `F51~F55 → report.*`, `F41~F49 → settlement.*` 매핑은 **라이브로 확정**(재매핑 없음). 부서계정은 정산을 **전혀 쓰지 않는다**.
2. `department_accounting` 은 **레거시 부서 명칭(경리부)** 라벨일 뿐, 권한 풋프린트는 **`report.*`(통계)** 다. 동작 변경 없음 — 근거를 카탈로그 §4c + `infer_login_profile` 주석에 고정.
3. **Phase C/D 시사점**: 현재 `ACC-MENU-NAV-04`(회계=settlement) 가 `login_profiles:[department_accounting]` 로 노출되나(회귀 가드 [`test_account_menu_matrix_visibility.py`](../../test/test_account_menu_matrix_visibility.py)), 부서계정은 `settlement.*` 권한 0 → 진입 후 화면이 빈다. 부서계정의 실제 화면(F51~F55 통계/자료) 노출 정합은 **Phase C/D 에서 테스트 동반 변경**으로 처리(본 Phase B 는 근거 기록까지).

---

## 5. print 모델 (Phase B step 6)

레거시는 별도 인쇄 Fxx 가 없다. 인쇄는 폼 메서드(`Sobo##.Print`)이며, 메뉴 핸들러의 `R` 분기는 입력 패널·그리드 편집만 비활성화하고 **인쇄 버튼은 유지**한다. → **`print = read-level`** (O·R 모두 인쇄 가능). 별도 `*.print` 코드는 신설하지 않고, 인쇄가 read 와 다른 화면이 식별될 때만 예외 파생.

---

## 6. 다음 단계 인계
- **Phase C**: `fetch_fxx_matrix` 4-key 정합, `_merge_fxx_to_permissions`(§1 규약), `infer_login_profile` 임계값(§4 근거).
- **Phase D**: `useScreenCaps(screenId) → {canRead,canWrite,canPrint}` 가 본 §1 규약을 그대로 구현.
- **Phase E**: 본 테이블 + [`account-menu-fxx-all.json`](account-menu-fxx-all.json) 로 **전 계정 미매핑 f-컬럼 0 / ungated 0 / 계정 하드코딩 0** 커버리지 가드.
- **Phase F**: 입고처(F12)/기타거래처(F15)/저자(F13) 화면 포팅 + 신규 permission_code 결정.
