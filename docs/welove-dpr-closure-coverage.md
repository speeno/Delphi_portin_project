# WeLove DPR Closure Coverage

이 문서는 `WeLove_FTP` 고객별 Delphi 실행 파일을 포팅 계약에 연결하기 위한 **생성 산출물 요약·운영 원칙**입니다. 원본 자격증명 파일은 읽지 않고, 경로·해시·라우팅 키만 저장합니다.

## 조사 결과 요약

| 항목 | 값 |
|------|-----|
| 활성 테넌트 | 40 |
| `active_build_id` 누락 | 0 (게이트가 차단) |
| DPR 클로저 수 | 468 |
| `layout_mappings` 대비 소스 커버 | 38 / 40 매핑 노트 (`welove_screen_contract_coverage.json`) |
| 미커버 매핑 | `Id_Logn`, `c8_scan_match` — 화면 단위 DPR이 아닌 로그인·스캔 매칭 계약으로 별도 추적 |

**테넌트 라우팅 키 순서:** `tenant_id` → `account_family` → `active_build_id` → `dpr_closure` (상세는 `welove_build_coverage.yaml`의 `tenant_routing_contract`).

## Generated Artifacts

- `analysis/welove_dpr_closures.json`: 468개 `.dpr`의 `uses` 클로저, PAS/DFM 경로, 해시.
- `analysis/welove_build_catalog_extended.json`: 기존 빌드 카탈로그 + 미매핑 실행 파일 유형 + 동치 클로저 그룹.
- `analysis/welove_tenant_build_routing_matrix.json`: `tenant_id -> account_family -> active_build_id -> dpr_closure` 추적.
- `analysis/welove_screen_contract_coverage.json`: `layout_mappings/*.md` 화면별 `build_id` 소스 PAS/DFM 변형.
- `migration/contracts/welove_build_coverage.yaml`: 위 산출물을 포팅 계약의 공통 참조로 고정 (`login_safety_contract` 포함).

생성 스크립트: `tools/extract_welove_dpr_closures.py`, `tools/build_welove_porting_coverage.py`.

## 포팅 적용 순서 (권장)

1. **인벤토리 동기**: 로컬 `WeLove_FTP` 존재 시 스크립트로 JSON 재생성 → 계약 `artifacts` 경로와 불일치 없게 유지.
2. **테넌트·빌드 정합**: `tenants_directory` 시드/런타임과 `welove_tenant_build_routing_matrix.json` 비교; 불일치는 DEC 또는 `customer_variants`에만 기록.
3. **화면 계약**: 신규·수정 화면은 dfm→html 산출물( `.cursor/rules/dfm-layout-input.mdc`)을 공식 입력으로 두고, WeLove 소스 경로는 `welove_screen_contract_coverage.json`과 매핑 노트를 맞춘다.
4. **메뉴·권한**: `rbac_menu_matrix.yaml`, `build_forced_hidden_menus.yaml`, 프런트 `account-menu-matrix.ts`가 `active_build_id`·claim과 일치하는지 확인.
5. **회귀 게이트**: 아래 테스트·probe 실행 또는 CI 동등.

## 로그인 보존 가드 (변경 금지 원칙)

WeLove 메타 확장은 **부가 정보 보존**만 허용한다. 다음은 **변경하지 않는다**.

- DSN-DEC-08 통합 로그인 흐름: `auth.login`, `tenants_directory`, `Id_Logn` 비밀번호 검증, `login_id_index` 해석.
- 활성 테넌트 선택 후 DB 연결 및 JWT 발급 순서.

**허용되는 추가 메타:** `active_build_id`, `account_family`, `build_role`, `warehouse_menu_tier`, 메뉴/권한 claim 등 계약에 명시된 필드의 유지·전달.

**체크리스트 (코드 터치 전 필수):**

- `docs/login-routing-regression-guard.md`
- `migration/contracts/login.yaml`
- `migration/contracts/tenants_directory.yaml`
- `migration/contracts/welove_build_coverage.yaml` → `login_safety_contract`

## 신규 시나리오·화면 입력 규칙

- 레거시 소스 트리만으로 필드가 불명확하면 **`WeLove_FTP` 해당 `build_id` 경로**를 정본으로 삼는다.
- 고객 간 차이는 **서비스/프론트 if/else 분기 금지** — `customer_variants`와 계약 데이터만 사용 (`welove_build_coverage.yaml` `schema_extensions.branch_rule`).
- dfm 변형 폴더(`Subu22`, `Subu22_1` 등) 차이는 **코드 분기 금지**, 계약에 diff 기록 (DEC-028).

## Current Totals

- Tenants: 40
- Missing active_build_id: 0
- DPR closures: 468
- Mapping notes covered by WeLove source: 38 / 40

## Regression Gate

다음이 실패하면 병합·릴리스 전에 원인을 제거한다.

### 필수 (계약 `welove_build_coverage.yaml`·`login_safety_contract`)

- `test/test_welove_porting_coverage.py` — 활성 테넌트 `active_build_id`, 비밀 키 미유출, 소스 추적성, RBAC `source_builds` 정합 등.
- `test/test_auth_login_dynamic_routing.py`
- `test/test_auth_login_500_safety_net.py`
- `test/test_auth_login_fixed_server.py`

### 보조·운영

- `debug/probe_backend_all_servers.py` (4대 서버 매트릭스, 멀티 DB 정책 DEC-033)

`test/test_welove_porting_coverage.py`가 특히 다음을 차단합니다.

- 모든 활성 테넌트는 `active_build_id`를 가져야 합니다.
- 생성 산출물에는 DB 사용자/비밀번호 키가 없어야 합니다.
- `Sobo14` 같은 완료 화면은 `customer_variants[].source_pas_path/source_dfm_path`로 추적 가능해야 합니다.
- `rbac_menu_matrix.yaml`의 `source_builds`와 빌드 카탈로그 alias가 어긋나면 실패합니다.
