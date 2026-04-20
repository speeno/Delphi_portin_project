# 화면 카드: Subu10 (TSubu10) — 환경설정 진입점

_생성: 2026-04-20 — 수동 (C10 T1, 권한 관리 진입점 정의)_

## 0. 한눈 요약
- 시나리오: **C10 권한 관리 (Full)** — Wave D `admin_web_platform` v1.0 가드 미적용 위에 가드 강제 + Id_Logn 매트릭스 UI + d_select 실분기.
- 정본 폼: 레거시 `Subu10` 단일 진입 폼은 **소스 트리에 직접 폼 파일 없음** (`legacy_delphi_source/legacy_source/Subu10.pas/dfm` 부재). 운영 화면은 **메인 메뉴 진입점 (Chul.pas Menu1xx → Base10.Seek_Uses('Fxx'))** 에 분산되어 있고, 사용자/권한 자체 편집은 **DB 직 UPDATE (Chul.pas L1732, Subu45.pas L364)** 로 수행되어 왔음.
- 모던 통합: `/admin/id-logn` 1 페이지에 **사용자 CRUD + F11~F89 매트릭스 + 비번 리셋** 흡수. 권한 캐시·세션 정책은 백엔드 `core/deps.py` 에 일임.

> **중요 (DEC-028 룰 7)**: 본 화면은 신규 모던 통합 화면이지만, 기존 레거시 위젯 ID 가 없으므로 `data-legacy-id` 는 **각 액션의 출처 폼 (Chul.Edit*/Subu40.Edit101/Subu45.Edit*)** 으로 부착한다. 매핑은 [`analysis/layout_mappings/Id_Logn.md`](../layout_mappings/Id_Logn.md) §3 참조.

## 1. 메뉴/진입 경로 (레거시)

| 진입 | 정의 위치 | 근거 |
|---|---|---|
| 로그인 직후 권한 적재 | `Chul.pas` L441~ | `Select Hcode,Hname,Gpass From Id_Logn Where Gcode=:Logn2 and Gname=:Logn1` |
| 메뉴 권한 가드 | `Chul.pas` L2448~ (Menu103Click) | `Base10.Seek_Uses('F17')` → 'X' (불허) / 'O' (R/W) / 'R' (read-only) |
| 비번 변경 | `Chul.pas` L1732 | `UPDATE Id_Logn SET Gcode='@Gcode' ...` (자기 비번) |
| 관리자 비번 리셋 (정산 게이팅) | `Subu45.pas` L364 | `UPDATE Id_Logn SET Gpass='@Gpass' ...` (Gpass 회전 — DEC-032 으로 폐기됨) |
| 권한 부여/회수 | (소스에 직접 UI 없음 — DBA 가 SQL 로 수행한 운영 관행) | 운영 SME 인터뷰 항목 (HA-INT-01 §3.4) |
| 비번 모달 | `Subu40.pas` (TSobo40) | `Edit101.Text` → `Edit101KeyPress(#13) → ModalResult:=mrOK` |

## 2. Id_Logn 컬럼 (정본)

| 컬럼 | 타입(추정) | 의미 | 모던 매핑 |
|---|---|---|---|
| `Hcode` | char(4) | 지점 코드 (`'0000'` = 슈퍼유저) | `branch_id` (JWT claim) |
| `Hname` | varchar | 지점명 | `branch_name` |
| `Gcode` | varchar | 사용자 로그인 ID | `login_id` |
| `Gname` | varchar | 사용자 이름 | `display_name` |
| `Gpass` | varchar | 비번 (평문/MD5+Base64 혼재 — `app/core/security.py::verify_legacy_password`) | `password_hash` (Phase 2 bcrypt — D-ADM-3) |
| `F11`..`F89` | char(1) | 메뉴별 권한 — `'O'`/`'R'`/`'X'`/공백 | `permissions: { code: "<O|R|X>" }` (`legacy_permission_map` 시드) |

> **F11~F89 의 실제 의미**: 메뉴 코드 (`SubXX`/`MenuXXX`) → 권한키 매핑은 `Chul.pas` 의 `Base10.Seek_Uses('Fxx')` 호출 지점에서만 결정됨 (1:1 카탈로그). [`legacy-analysis/permission-keys-catalog.md`](../../legacy-analysis/permission-keys-catalog.md) (T2 신설) 에서 전수 인덱싱.

## 3. 모던 라우트 매핑 (C10 Phase 1)

| 모던 페이지 | 레거시 출처 | 비고 |
|---|---|---|
| `/admin/id-logn` (목록·매트릭스) | Chul.pas L441/L1732 + DBA 운영 관행 | C10 Phase 1 신규 단일 통합 |
| `/admin/id-logn/[hcode]` (상세·비번 리셋) | Subu40.pas + Subu45.pas L364 | 비번 리셋은 `app/services/audit_password_service.py` 100% 재사용 |
| `/admin/permissions` (역할·매트릭스) | Wave D `web_roles`/`web_role_permissions` 위에 `legacy_permission_map` 표 노출 | 이미 [`/admin/rbac`](../../도서물류관리프로그램/frontend/src/app/(app)/admin/rbac/) 1차 가동 |
| `/login?reason=expired` (C13) | (없음 — 새 정책) | `app/lib/api-client.ts` 401 인터셉터 |

## 4. 권한 정책 (C10 Phase 1 결정)

1. **슈퍼유저 보호**: `Hcode='0000'` 사용자의 권한·비번은 **자기 자신만** 변경. 다른 사용자는 422 `ID_LOGN_SUPER_USER_PROTECTED`.
2. **자기권한 박탈 차단**: 자신의 `admin.user.write` 권한을 `O`→`X` 로 떨어뜨리는 변경은 422 `ID_LOGN_SELF_REVOKE`.
3. **Wave D 시드 매핑 (`legacy_permission_map`)**: F18 ↔ `admin.user.write`, F21 ↔ `outbound.write`, F22 ↔ `outbound.cancel`, F26 ↔ `master.write`, ... (T2 카탈로그에서 확장).
4. **세션 만료 (C13)**: access JWT 만료 시 401 `AUTH_TOKEN_EXPIRED` → 클라이언트가 refresh 1회 시도 → 실패 시 `/login?reason=expired`. 권한 부족은 403 `PERMISSION_DENIED`.
5. **동시편집 충돌 (C15)**: Id_Logn UPDATE 시 `If-Match: <revision>` 헤더 필수 → 불일치 시 409 `STALE_VERSION` 반환.

## 5. 산출물 링크

- 레이아웃: [`analysis/layout_mappings/Id_Logn.md`](../layout_mappings/Id_Logn.md), [`analysis/layout_mappings/Subu40.md`](../layout_mappings/Subu40.md)
- 핸들러/SQL: [`analysis/handlers/c10_phase1.md`](../handlers/c10_phase1.md) (T2)
- 권한키 카탈로그: [`legacy-analysis/permission-keys-catalog.md`](../../legacy-analysis/permission-keys-catalog.md) (T2)
- 계약: [`migration/contracts/admin_permissions.yaml`](../../migration/contracts/admin_permissions.yaml) (T3, v1.0.0), [`migration/contracts/admin_web_platform.yaml`](../../migration/contracts/admin_web_platform.yaml) (T3, v1.1.0)
- 테스트: [`test/test_c10_admin_phase1.py`](../../test/test_c10_admin_phase1.py) (T4)
