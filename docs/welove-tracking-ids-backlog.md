# Welove 인수인계 추적 ID — 계약·CRUD·OQ 합류 백로그

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-23 (2026-04-24 갱신: BLD-* / MENU-* / OQ-BLD-1~7 / OQ-MENUVIS-* / MENUVIS-DEC-* / DSN-DEC-06~07 / ACC-MULTI-* / OQ-LICENSE-KEY-MAP) |
| 추적 ID | `MAN-*`, `SCH-*`, `DSN-*`, `ONB-*`, `ACC-*`, `PROF-*`, **`BLD-*`**, **`MENU-*`**, **`MENUVIS-DEC-*`**, **`OQ-BLD-*`**, **`OQ-MENUVIS-*`**, **`OQ-LICENSE-KEY-MAP`**, **`ACTR-DEC-*`**, **`WHL-*`**, **`TENDIR-*`** |
| 단일 원천 | 본 문서 — 본 사이클에서 **결정** 된 모든 추적 ID 가 후속 PR 에서 어디에 합류해야 하는지를 1행씩 나열. |
| 정합 | [`docs/manual-catalog.md`](manual-catalog.md), [`docs/welove-publish-schema-dictionary.md`](welove-publish-schema-dictionary.md), [`docs/welove-schema-reconciliation.md`](welove-schema-reconciliation.md), [`docs/decision-login-db-routing.md`](decision-login-db-routing.md), [`docs/onboarding-governance-spec.md`](onboarding-governance-spec.md), [`docs/onboarding-rbac-menu-matrix.md`](onboarding-rbac-menu-matrix.md), [`docs/profile-password-ux-spec.md`](profile-password-ux-spec.md), [`docs/welove-chul-build-menu-matrix.md`](welove-chul-build-menu-matrix.md), [`docs/menu-visibility-runtime-design.md`](menu-visibility-runtime-design.md) |

---

## 1. 한 줄 요약

본 사이클은 **문서·메타** 만 변경했다. 본 표는 다음 사이클에서 **계약·CRUD 백로그·OQ** 에 1줄씩 추가해야 할 항목을 나열한다 — 각 PR 은 본 표의 1 행을 1 commit 으로 처리한다.

---

## 2. `migration/contracts/*.yaml` 합류 항목

| 추적 ID | 대상 contract | 추가/변경 |
|---|---|---|
| `MAN-005` (모바일 거래명세서) | `mobile_uat.yaml` | UAT-OUT-* 단계 본문에 `MAN-005` 1줄 cite. |
| `MAN-008/017/018` (DSN 메타) | `login.yaml` D-LOGIN-4 | `proposed_web_behavior.note` 에 `analysis/welove_db_route_matrix.json` cite. |
| `SCH-WELOVE-출판-Id_Logn` | `login.yaml` D-LOGIN-* | `inputs.gcode/gname.note` 에 `SCH-RECON-01` 링크. |
| `SCH-WELOVE-출판-G7_Ggeo` | `master_data.yaml` (출판사 마스터) | `endpoints[*].columns` 가 본 사전 cite. |
| `SCH-WELOVE-출판-G1_Ggeo` | `master_data.yaml` (거래처 마스터) | 동일 — Size 변경 흔적 inline. |
| `SCH-WELOVE-출판-T2_Ssub` (사전 누락) | `transactions_misc.yaml` (청구) | `OQ-SCH-NEW-1` 링크 + 사전 보강 PR. |
| `SCH-WELOVE-출판-T7_Ssub` (사전 누락) | `return_receipt.yaml` (반품비) | 동일. |
| `DSN-DEC-01..05` | `login.yaml`, `admin_web_platform.yaml` | DSN 결정문 cite. |
| `ACC-T1/T2-DIST/T2-PUB/T3` | `admin_permissions.yaml` | `account_types[*]` 단락 신설. |
| `ACC-MENU-NAV-01..16` | `admin_permissions.yaml` | `menus[*].visible_to` + `menus[*].source_builds[]` + `menus[*].forced_hidden_in_builds[]` + `menus[*].license_key` 컬럼 추가. (확장: NAV-09~16 = warehouse/distributor 셸 신규 메뉴) |
| `ACC-API-01..08` | `admin_permissions.yaml` + 각 도메인 contract | `requires.account_type` 컬럼 추가. |
| `ONB-API-01..06` | `member_signup.yaml` (신설 contract) | 가입 신청·승인 흐름 1차 정의. |
| `PROF-API-01..04`, `PWD-API-01..02` | `profile.yaml` (신설 contract) | 본인·관리자 프로필/비번 흐름 정의. |
| `BLD-DIST-STD/PUB-STD/DIST-KBT/PUB-KBT/PUB-WAREHOUSE-WELOVE/PUB-WAREHOUSE-MS/PUB-WAREHOUSE-BOOKNBOOK-NEW` (7) | `admin_permissions.yaml` + `tenants_directory.yaml`(신설) | `tenants[*].build_id` 매핑 + `builds[*]` 카탈로그 단락 신설. 정본은 [`analysis/welove_chul_builds.json`](../analysis/welove_chul_builds.json). |
| `MENU-* (180 합집합 항목)` | `admin_permissions.yaml::menus[*].menu_id` | 정본은 [`analysis/welove_chul_menu_matrix.json`](../analysis/welove_chul_menu_matrix.json). |
| `MENUVIS-DEC-01..06` | `admin_permissions.yaml`(신규 단락 `runtime_visibility`) + 신규 contract `build_forced_hidden_menus.yaml` + `menu_license_keys.yaml` | [`docs/menu-visibility-runtime-design.md`](menu-visibility-runtime-design.md) cite. |
| `DSN-DEC-06` (`(tenant_id, account_family)` 합성 키) | `login.yaml` D-LOGIN-4 | [`docs/decision-login-db-routing.md`](decision-login-db-routing.md) §보강안 cite. |
| `DSN-DEC-07` (JWT `license_keys[]`) | `login.yaml` D-LOGIN-4 | 동상. |
| `ACC-T3-WAREHOUSE-LITE / -FULL (가설)` | `admin_permissions.yaml::account_types[*]` | 2 sub-type 채택 시 등록. 채택 결정은 `OQ-BLD-2` 닫는 PR. |
| `ACC-MULTI-01..05` | `admin_permissions.yaml::multi_build_policy` (신규 단락) | [`docs/onboarding-rbac-menu-matrix.md::§11`](onboarding-rbac-menu-matrix.md) cite. |

---

## 3. `docs/crud-backlog.md` 합류 항목

| 추적 ID | 추가 항목 |
|---|---|
| `SCH-RECON-03` (23 미사전 테이블) | "사전 누락" 컬럼 신설 + 신규 화면 포팅 시 SME 회의 의제로 격상. |
| `SCH-WELOVE-출판-T2_Ssub` 등 우선 5 | 사전 보강 PR 후보로 등록. |
| `ACC-T2-PUB` `hcode` 격리 (M4 보류) | 데이터 격리 행 강제 미구현 갭 명시. |
| `PROF-GAP-01..04` | 프로필/비번 self-service 미구현 4 갭. |

---

## 4. `legacy-analysis/open-questions.md` 합류 항목

| 신규 OQ | 본문 요지 | 닫는 조건 |
|---|---|---|
| `OQ-LOGIN-2` (`SCH-RECON-01`) | `Id_Logn.gcode/gname` 의 의미가 사전 vs 계약에서 반대 — SME + 운영 DB 1행 조회 후 동결. | DEC ID 발급 + `login.yaml` 정정. |
| `OQ-DBL-NEW-1` (`SCH-RECON-02`) | `S1_Chek` vs `S1_CheK` 대소문자 — 운영 DB `SHOW TABLES LIKE` 확인. | 사전 정정 PR. |
| `OQ-SCH-NEW-1` (`SCH-RECON-03`) | 23 미사전 테이블의 사전 보강. | 우선 5 항목 사전 PR. |
| `OQ-DSN-1` (`DSN-RISK-01`) | 동일 서버·동일 DB 에서 `hcode` 만 다른 출판사의 행 격리 정책 — M4 결정과 묶음. | DEC 발급. |
| `OQ-DSN-2` (`DSN-RISK-02`) | 단일 인증 서버 장애 시 절체 절차 — HA 또는 수동 fallback. | 운영 런북 §3 추가. |
| `OQ-ONB-1` (`ONB-RISK-02`) | 멀티 총판 소속 출판사 (`ACC-T2-PUB-MULTI`) — 본 사이클 비커버. | 별 사이클 spec. |
| `OQ-ONB-2` (`ONB-RISK-03`) | T3 가입 시 신규 DSN 부여 자동화 — R1 단계 후. | DEC-052 R1 승격. |
| `OQ-PROF-1` (`PROF-GAP-04`) | `password_history`, 임시 비번 만료, 세션 무효화 — 보조 인프라 부재. | 인프라 PR 후. |
| `OQ-BLD-1` | `Uses=홍길동` 가 P-STD/P-KBT 의 운영 정본인지 sample placeholder 인지. | SME 인터뷰 + DEC 발급. |
| `OQ-BLD-2` | `ACC-T3-WAREHOUSE-LITE / -FULL` sub-type 분리 채택 여부. WH-MS+WH-BB 2 빌드 일치로 분리 가설 강력 권고. | DEC 발급 → `admin_permissions.yaml::account_types` 행 추가. |
| `OQ-BLD-3` | D-KBT 의 표준 총판 대비 추가 폼군 (`Subu13_1·14_1·22_1·22_2·27_1·32_1·32_9·34_1~4·38_2·42_1·43_1·44_1·45_1·59_1~3·59_9·61~63·71·91·93·96~99` 등) 의 업무 모듈 정체. | SME 검증. |
| `OQ-BLD-4` | WH-MS 의 `TSCLIB.dll` (TSC 라벨 프린터 SDK) 의 운영 필수성 + 호출 메뉴/폼 + 웹 라벨 출력 대안 (브라우저 인쇄 vs 클라이언트 에이전트). App Caption "도서관리프로그램" 의 별도 제품 라인 vs OEM 정체성. | SME 인터뷰 → `admin_permissions.yaml::builds[BLD-PUB-WAREHOUSE-MS].labels` 단락. |
| `OQ-BLD-5` | WH-BB 의 `Uses=한국도서유통` 이 KBT 본사 운영 빌드인지, 북앤북이 KBT 소속 출판사인지, KBT-북앤북 OEM 인지. DB 루트 매트릭스 상 book_07 SKU 는 북앤북·유앤북 2 테넌트 → 독립 가설 우세. | SME 확인 → `tenants_directory.yaml` 의 `parent_tenant` 결정. |
| `OQ-BLD-6` | WH-BB 의 신규 폼군 (`Seak/Seek/Seok/Seep/Base` 28 폼) 가 어떤 업무 모듈인지 (전자세금계산서? 설정마스터? 회계연동?). | 폼 캡션·핸들러 이름 → SME 검증. |
| `OQ-BLD-7` | WH-BB 의 `Interbase/Mysql/Remote` 디렉토리가 (a) Firebird→MySQL 마이그레이션 진행 중 빌드, (b) 본사·로컬 이중 백엔드, (c) 단순 도구/유틸 디렉토리 중 무엇인지. | [`docs/welove-publish-schema-dictionary.md`](welove-publish-schema-dictionary.md) 의 다중 DB 호환 가이드와 직결. |
| `OQ-MENUVIS-1` | `Seek_Uses` 가 'X' 외 다른 코드 ('Y','0','1' 등) 를 반환하는 케이스가 있는지. 현재 모든 핸들러 `<>'X'` 만 검사. | 서버 구현 본문 검사 → DEC 또는 단순화 확정. |
| `OQ-MENUVIS-2` | 라이선스 키 발급/관리 위치 (수기 DB UPDATE vs 별도 콘솔). 웹 이전 시 관리자 화면 신규 필요 여부. | SME → `admin_permissions.yaml::license_management` 단락. |
| `OQ-MENUVIS-3` (= `OQ-LICENSE-KEY-MAP`) | 62 개 F-key 의 의미적 그룹화 + 메뉴 ↔ 키 1:1 매핑 정본화. | 별 사이클 — `migration/contracts/menu_license_keys.yaml` 생성. |
| `OQ-MENUVIS-4` (= `OQ-BLD-MS-1`) | WH-MS FormShow 의 Menu300/400/500/600/700/800/208/308 := False startup hide 의 실효 노출 메뉴 정정. | 운영 화면 캡처 또는 SME 인터뷰 → `build_forced_hidden_menus.yaml`. |
| `OQ-MENUVIS-5` | 사용자별 숨김 메뉴 기능이 레거시에 존재하는지, 신규 도입인지. | SME → `(app)/profile/preferences` 사양에 합류. |

---

## 5. `legacy-analysis/decisions.md` (DEC) 후보

| 신규 DEC | 본문 후보 | 정합 |
|---|---|---|
| `DEC-XXX (DSN-DEC-01..05)` | DSN 라우팅 5 결정 — 단일 인증 서버 + 사용자별 primary 데이터 서버, JWT 클레임 표준, `pool_for(...)` 헬퍼, R0/R1/R2 단계, 메타 단일 원천. | [`docs/decision-login-db-routing.md`](decision-login-db-routing.md). |
| `DEC ONB-001` | 소속 출판사 가입 게이트 = "A AND B (사전등록 + 총판 승인)" + 운영자 토글 (A only). | [`docs/onboarding-governance-spec.md`](onboarding-governance-spec.md) §3. |
| `DEC-XXX (ACC-MATRIX)` | 4 가지 계정 유형의 메뉴/API 노출 매트릭스 본문화. | [`docs/onboarding-rbac-menu-matrix.md`](onboarding-rbac-menu-matrix.md). |
| `DEC-XXX (PROF-PWD)` | 본인 변경 vs 관리자 reset 정책 + 비번 정책(`PWD-RULE-01..06`). | [`docs/profile-password-ux-spec.md`](profile-password-ux-spec.md). |
| `DEC-XXX (BUILD-CATALOG)` | 7 빌드 카탈로그 (`BLD-*`) 정본화 + binary-identical 그룹 (`BLD-PUB-STD ≡ BLD-PUB-KBT`) 처리 규칙. | [`analysis/welove_chul_builds.json`](../analysis/welove_chul_builds.json), [`docs/welove-chul-build-menu-matrix.md`](welove-chul-build-menu-matrix.md). |
| `DEC-XXX (MENUVIS-DEC)` | 메뉴 가시성 2 레이어 (PermissionGuard 강제 + 사용자 환경설정 소프트), 라이선스 키 매핑, ToolBar 토글 분리. | [`docs/menu-visibility-runtime-design.md`](menu-visibility-runtime-design.md). |
| `DEC-XXX (DSN-DEC-06/07)` | DSN 라우팅 합성 키 + JWT license_keys[] 클레임. | [`docs/decision-login-db-routing.md`](decision-login-db-routing.md) §보강안. |
| `DEC-XXX (ACC-MULTI)` | 동일 테넌트 다중 빌드 / 동일 SKU 다중 테넌트 5 정책. | [`docs/onboarding-rbac-menu-matrix.md::§11`](onboarding-rbac-menu-matrix.md). |

---

## 6. 온보딩 RBAC 사이클 신규 ID (2026-04-24)

### 계정 유형 결정 (ACTR-DEC-*)

| ID | 내용 | 출처 |
|----|------|------|
| `ACTR-DEC-01` | web_users.account_type 명시값 최우선 | [`docs/onboarding-account-type-resolution.md`](onboarding-account-type-resolution.md) |
| `ACTR-DEC-02` | hcode=0000 / BLS_ADMIN_USER_IDS → T1 | 동 문서 |
| `ACTR-DEC-03` | web_publisher_whitelist 매칭 → expected_account_type | 동 문서 |
| `ACTR-DEC-04` | tenants_directory 조회 → default_account_type | 동 문서 |
| `ACTR-DEC-05` | 미결정 폴백 → "" (관리자 수동 지정 대기) | 동 문서 |
| `ACTR-RISK-01..04` | 계정 유형 결정 위험 요인 4건 | 동 문서 §7 |

### 화이트리스트 (WHL-*)

| ID | 내용 | 출처 |
|----|------|------|
| `WHL-VAL-DIST_UNKNOWN` | T2-PUB 가입 시 dist_hcode 없으면 422 | [`migration/contracts/web_publisher_whitelist.yaml`](../migration/contracts/web_publisher_whitelist.yaml) |
| `WHL-VAL-NOT_IN_WHITELIST` | (dist_hcode, publisher_hcode) 미등록 → 422 | 동 파일 |
| `WHL-VAL-ALREADY_REGISTERED` | 이미 활성 web_users 행 존재 → 409 | 동 파일 |
| `WHL-VAL-STATUS_CHECK` | whitelist.status==disabled → 가입 불가 | 동 파일 |
| `ONB-REJ-NOT_IN_WHITELIST` | 응답 코드 (백엔드 HTTPException detail) | `publisher_whitelist_service.py` |

### 테넌트 디렉토리 (TENDIR-*)

| ID | 내용 | 출처 |
|----|------|------|
| `TENDIR-v1` | 테넌트 디렉토리 계약 초안 | [`migration/contracts/tenants_directory.yaml`](../migration/contracts/tenants_directory.yaml) |
| `OQ-TENDIR-1..3` | chul_09_db 공유·한국도서유통 다중빌드·시드 불완전 미결 | 동 파일 open_questions |

---

## 7. `dashboard/data/todos.json` 등 대시보드 합류 (선택)

본 문서 §2~§5 의 ID 들은 다음 사이클에서 대시보드 todo 카드 1장씩 매핑한다 — 본 사이클은 **문서 결정만**, 카드 등록은 별 PR.

---

## 7. 갱신 절차

1. 본 표의 한 행을 PR 로 옮기면 `done`/`PR-#` 컬럼을 본문에 추가.
2. 본 사이클의 신규 ID 가 더 발생하면 (§1 출처 문서 갱신 + 본 표 1행 추가) 동시 PR.
3. 모든 행이 `done` 표시되면 본 문서는 [DEPRECATED] 표기 후 보존.
