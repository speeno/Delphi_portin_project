# 핸들러 카탈로그: C10 Phase 1 — 권한 관리·세션·동시편집

_생성: 2026-04-20 — C10 T2 (Chul.pas 5 SQL + Seek_Uses 인덱싱 + 모던 라우터 매핑)_

> 본 문서는 C10 Phase 1 (Full) 의 **단일 진실 (single source of truth)** 핸들러·SQL 카탈로그. 신규 SQL 0건 — 모두 기존 Chul.pas / Base01.pas / Subu45.pas 의 5 SELECT/UPDATE 를 재사용.

## 1. 레거시 SQL 5건 (정본)

> 출처: [`legacy_delphi_source/legacy_source/docs/phase1-structure/13-db-sql-references.csv`](../../legacy_delphi_source/legacy_source/docs/phase1-structure/13-db-sql-references.csv) L836~854

| # | 위치 | 동사 | SQL (요약) | 모던 매핑 |
|---|---|---|---|---|
| 1 | `Base01.pas` L10168 (`TBase10.Seek_Uses`) | SELECT | `Select @F11 From Id_Logn Where Hcode='@H' and Gname='@N' and Gcode='@C' and Gpass='@P'` (`@F11` 은 매개변수로 들어오는 키 — F11~F89 중 하나) | `app/services/id_logn_service.py::seek_uses(user_ctx, perm_key) -> 'O'\|'R'\|'X'` |
| 2 | `Chul.pas` L441 (로그인 시 사용자 적재) | SELECT | `Select Hcode,Hname,Gpass From Id_Logn Where Gcode='@C' and Gname='@N'` | `app/services/auth_service.py::resolve_user(login_id, display_name)` (이미 가동 — Wave A) |
| 3 | `Chul.pas` L1724 (자기 비번 검증) | SELECT | `Select Gpass From Id_Logn Where '+D_Select+' Hcode='@H'` | `app/services/audit_password_service.py::verify` 100% 재사용 (Wave A) |
| 4 | `Chul.pas` L1732 (자기 비번 변경) | UPDATE | `UPDATE Id_Logn SET Gcode='@C' WHERE ...` (※ 레거시는 Gcode= 로 비번 갱신; 컬럼 의미는 화면 정책상 동치) | `app/services/id_logn_service.py::change_self_password` (인터페이스만 — D-ADM-3 Phase 2) |
| 5 | `Chul.pas` L2451+L2460 (사용자/권한 매트릭스 편집) | SELECT + UPDATE | `Select Hcode,Hname,Gpass From Id_Logn` + `UPDATE Id_Logn SET Gcode='@C',Gname='@N',Gpass='@P' WHERE ...` | `app/services/id_logn_service.py::list_users` + `update_user_with_permissions` |

> **추가 참조** (Phase 2 흡수 후보 — 본 사이클 비차단): `Chul.pas` L3028/L3127/L3160/L3193/L3278/L3345/L3377/L3421/L3457/L3492 (모두 `Select Gname/Gpass From Id_Logn` 의 권한 재검증 호출). 본 사이클은 `Seek_Uses` 단일 통합으로 흡수 — 추가 SQL 0건.
>
> **Subu17·Subu17_1 L1791~1802**: 정산 진입부 비번 재인증 — 이미 [`audit_password_service`](../../도서물류관리프로그램/backend/app/services/audit_password_service.py) 로 흡수됨 (Wave A).
>
> **Subu45.pas L364**: 관리자 비번 리셋 UPDATE — `app/routers/admin.py::reset_user_password` 에 흡수 예정 (T5).

## 2. Seek_Uses 호출 지점 인덱싱 (Chul.pas + Interbase/Chul.pas)

> 핵심 사실: 메뉴 코드 → 권한키 매핑은 `Base10.Seek_Uses('Fxx')` 호출 직전의 핸들러 시그니처에서 1:1 결정. 본 표가 [`legacy-analysis/permission-keys-catalog.md`](../../legacy-analysis/permission-keys-catalog.md) 의 시드.

### 2.1 본 트리 (`Chul.pas`) — 80개 호출 지점

| 권한키 | Chul.pas 라인 | 메뉴/액션 | 모던 permission_code |
|---|---|---|---|
| F11 | 2603, 2641, 3678 | Sobo11 (거래처 마스터) + Outbound 진입 | `master.customer.read` |
| F12 | 2415 | Sobo12 (도서 마스터) | `master.book.read` |
| F13 | 2378, 2539 | Sobo13 (입고/조회) | `master.book_code.read` |
| F14 | 2502 | Sobo14 (대체) | `master.alt.read` |
| F15 | 2679 | Sobo15 | `master.misc.read` |
| F16 | 2576 | Sobo16 (잡지) | `master.magazine.read` |
| F17 | 2452, 2477 | Sobo17 (도서코드 — 메뉴 103/103_1) | `master.book_code.write` |
| F18 | 2717 | Sobo18 (사용자/권한) | `admin.user.write` |
| F19 | 2698 | Sobo19 | `master.misc2.read` |
| F21 | 2949 | Sobo21 (출고 거래명세서) | `outbound.write` |
| F22 | 2922, 2967 | Sobo22 (출고 취소) | `outbound.cancel` |
| F23 | 4002 | Sobo23 (반품) | `return.write` |
| F24 | 2772, 2872 | Sobo24 | `outbound.alt` |
| F25 | 2797 | Sobo25 | `outbound.misc` |
| F26 | 2822 | Sobo26 (마스터 일괄) | `master.write` |
| F28 | 2985 | Sobo28 | `outbound.adjust` |
| F29 | 3159, 3177 | Sobo29 | `outbound.return` |
| F31 | 3015 | Sobo31 (재고원장) | `inventory.read` |
| F32 | 3069 | Sobo32 | `inventory.adj` |
| F33 | 3033 | Sobo33 | `inventory.move` |
| F34 | 3051, 3330, 3348, 3366, 3384 | Sobo34 (재고 진입 다수) | `inventory.write` |
| F35 | 3757, 3804 | Sobo35 | `inventory.misc` |
| F36 | 2847, 2897 | Sobo36 (통계) | `report.read` |
| F37 | 3087, 3105 | Sobo37 (재고 통계) | `report.inventory.read` |
| F38 | 3213 | Sobo38 | `report.alt.read` |
| F39 | 3231, 3249, 3267, 3285 | Sobo39 (보고서) | `report.misc` |
| F41 | 3501, 3526 | Sobo41 (정산-입금) | `settlement.deposit` |
| F42 | 3123, 3141 | Sobo42 | `settlement.misc` |
| F43 | 3558, 3591 | Sobo43 (정산 통계) | `settlement.report.read` |
| F44 | 3625 | Sobo44 | `settlement.bill` |
| F45 | 3701 | Sobo45 (청구) | `settlement.write` |
| F46 | 3408, 3441, 3474 | Sobo46 | `settlement.adj` |
| F47 | 3658 | Sobo47 (월합계) | `settlement.report.month` |
| F48 | 3195 | Sobo48 | `settlement.tax.read` |
| F49 | 3308 | Sobo49 | `settlement.misc2` |
| F51 | 3831 | Sobo51 | `report.kpi.read` |
| F52 | 3858 | Sobo52 | `report.kpi.write` |
| F53 | 3885 | Sobo53 | `report.delivery.read` |
| F54 | 3984 | Sobo54 | `report.return.read` |
| F55 | 3912 | Sobo55 | `report.book.read` |
| F56 | 3930 | Sobo56 | `report.cust.read` |
| F57 | 3948 | Sobo57 | `report.month.read` |
| F58 | 3966 | Sobo58 | `report.year.read` |

### 2.2 Interbase 변형 (`Interbase/Chul.pas`) — 64개 호출 지점

> 동일 키 매핑 (`Seek_Uses('Fxx')`) — 라인 번호만 다름. 변형은 본 사이클 회귀 테스트에서 동일 권한 모델을 통과하는지만 확인 (회귀 가드, T7).

## 3. 모던 라우터 매핑 (T5 신설/갱신)

| 라우터 | 메서드 | 가드 | 백엔드 함수 |
|---|---|---|---|
| `/admin/id-logn` | GET | `require_permission("admin.user.read")` | `id_logn_service.list_users(role, branch_id, q)` |
| `/admin/id-logn` | POST | `require_permission("admin.user.write")` + If-Match (None: 신규) | `id_logn_service.create_user(payload)` |
| `/admin/id-logn/{hcode}` | PUT | `require_permission("admin.user.write")` + If-Match | `id_logn_service.update_user_with_permissions(hcode, payload, etag)` |
| `/admin/id-logn/{hcode}/permissions` | PUT | `require_permission("admin.user.write")` + If-Match | `id_logn_service.update_permission_matrix(hcode, matrix, etag)` |
| `/admin/id-logn/{hcode}/password-reset` | POST | `require_permission("admin.user.write")` + audit_token | `id_logn_service.reset_password(hcode, audit_token)` (audit_password_service 100% 재사용) |

## 4. 가드 매트릭스 (T4 시드)

| 라우터 그룹 | 토큰 무 | 토큰 만료 | 권한 부족 | If-Match 누락 | If-Match 불일치 |
|---|---|---|---|---|---|
| `/admin/*` | 401 `AUTH_NO_TOKEN` | 401 `AUTH_TOKEN_EXPIRED` | 403 `PERMISSION_DENIED` | 428 `PRECONDITION_REQUIRED` (PUT/DELETE) | 409 `STALE_VERSION` |
| `/master/*` | 401 | 401 | 403 | 428 | 409 |
| `/outbound/*` | 401 | 401 | 403 | 428 | 409 |
| `/return/*` | 401 | 401 | 403 | 428 | 409 |
| `/inventory/*` | 401 | 401 | 403 | 428 | 409 |
| `/settlement/*` | 401 | 401 | 403 | 428 | 409 |
| `/report/*` | 401 | 401 | 403 | (R/O) | (R/O) |
| `/scan/*` (C8) | 401 | 401 | 403 | (idempotent) | (idempotent) |
| `/auth/*` | (해당 없음 — 발급) | (refresh 자체) | (해당 없음) | - | - |

## 5. d_select 실분기 (T5)

| 역할 | WHERE clause | 비고 |
|---|---|---|
| `admin` (Hcode='0000') | `1=1` | 슈퍼유저 — 전 데이터 |
| `branch_manager` | `Server_id = :server_id` | 본 지점 + 산하 |
| `operator` (`Hcode != '0000'`) | `Branch_id = :branch_id AND Hcode = :hcode` | 본 사용자 데이터만 |
| `auditor` | `Server_id = :server_id` (R/O 강제) | F36/F37/F43 read-only |

## 6. 결정 (DEC) 트레이서

본 핸들러 노트는 다음 결정 항목과 1:1 트레이서 관계에 있다 (T8 결정 노트 참조).

| 결정 ID | 본 노트 적용 위치 | 요약 |
|---|---|---|
| DEC-028 | §2 (Subu10/Id_Logn `data-legacy-id` 부착) | 모던 통합 화면도 출처 위젯 ID 부착 — 룰 7 |
| DEC-040 | §1 (5 SQL 100% 재사용) | C10 신규 SQL 0건 정책 |
| DEC-041 | §4 (가드 매트릭스 — 401/403 표준 코드) | C13 흐름 (세션·권한 응답 코드 표준화) |
| DEC-042 | §4 (If-Match/ETag 428/409) | C15 흐름 (낙관적 동시편집) |
| DEC-043 | (T3 admin_permissions.yaml 참조) | IdP/SSO 인터페이스 분리 — C10 인터페이스만 |

## 7. 변경 이력

- 2026-04-20 — 초판 (C10 T2)
- 2026-04-20 — §6 DEC 트레이서 추가 (C10 T7)
