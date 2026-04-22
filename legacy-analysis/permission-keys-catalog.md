# 레거시 권한키 카탈로그 (F11~F89)

_생성: 2026-04-20 — C10 T2 (Wave D `legacy_permission_map` 시드 확장)_
_갱신: 2026-04-22 — DEC-056 (M5 시드 일괄 적용) — `legacy_permission_map` v1.2: §1 30 정본 + §4 7 확장 = **52 정본 키 전체 시드 완료** (web_admin.json + admin_service `_DEFAULT_LEGACY_PERMISSION_MAP`). DEC-058 (M2 사이드바 게이팅) 도 동시 적용._

> 본 카탈로그는 [`analysis/handlers/c10_phase1.md`](../analysis/handlers/c10_phase1.md) §2 의 80개 `Seek_Uses` 호출 지점을 모던 `permission_code` 로 1:1 매핑한 표. 백엔드 `legacy_permission_map` 테이블 시드와 1:1 정합.

## 1. 매핑 표

| Fxx | 모던 permission_code | 레거시 메뉴/폼 | Chul.pas 호출 라인 | Wave D 시드 여부 |
|-----|----------------------|----------------|---------------------|-------------------|
| F11 | `master.customer.read` | Sobo11 (거래처) + 출고 진입 | 2603, 2641, 3678 | seed v1.0 |
| F12 | `master.book.read` | Sobo12 (도서) | 2415 | seed v1.0 |
| F13 | `master.book_code.read` | Sobo13 (코드) | 2378, 2539 | seed v1.0 |
| F14 | `master.alt.read` | Sobo14 (대체) | 2502 | C10 신규 |
| F15 | `master.misc.read` | Sobo15 | 2679 | C10 신규 |
| F16 | `master.magazine.read` | Sobo16 (잡지) | 2576 | C10 신규 |
| F17 | `master.book_code.write` | Sobo17 (메뉴 103/103_1) | 2452, 2477 | seed v1.0 |
| F18 | `admin.user.write` | Sobo18 (사용자/권한) | 2717 | seed v1.0 (슈퍼유저 가드) |
| F18r | `admin.user.read` | Sobo18 (사용자/권한 조회) | (Chul L?? — read-only 변형) | C10 신규 (write 의 read-only 페어) |
| F19 | `master.misc2.read` | Sobo19 | 2698 | C10 신규 |
| F21 | `outbound.write` | Sobo21 (거래명세서) | 2949 | seed v1.0 |
| F22 | `outbound.cancel` | Sobo22 (출고 취소) | 2922, 2967 | seed v1.0 |
| F23 | `return.write` | Sobo23 (반품) | 4002 | seed v1.0 |
| F24 | `outbound.alt` | Sobo24 | 2772, 2872 | C10 신규 |
| F25 | `outbound.misc` | Sobo25 | 2797 | C10 신규 |
| F26 | `master.write` | Sobo26 (마스터 일괄) | 2822 | seed v1.0 |
| F27 | `outbound.export` | Sobo27 (송장/라벨) | (Chul L?? — Phase 2) | C10 신규 |
| F28 | `outbound.adjust` | Sobo28 | 2985 | C10 신규 |
| F29 | `outbound.return` | Sobo29 | 3159, 3177 | C10 신규 |
| F31 | `inventory.read` | Sobo31 | 3015 | seed v1.0 |
| F32 | `inventory.adj` | Sobo32 | 3069 | C10 신규 |
| F33 | `inventory.move` | Sobo33 | 3033 | C10 신규 |
| F34 | `inventory.write` | Sobo34 | 3051, 3330, 3348, 3366, 3384 | seed v1.0 |
| F35 | `inventory.misc` | Sobo35 | 3757, 3804 | C10 신규 |
| F36 | `report.read` | Sobo36 (통계) | 2847, 2897 | seed v1.0 |
| F37 | `report.inventory.read` | Sobo37 (재고 통계) | 3087, 3105 | seed v1.0 |
| F38 | `report.alt.read` | Sobo38 | 3213 | C10 신규 |
| F39 | `report.misc` | Sobo39 | 3231, 3249, 3267, 3285 | C10 신규 |
| F41 | `settlement.deposit` | Sobo41 (입금) | 3501, 3526 | seed v1.0 |
| F42 | `settlement.misc` | Sobo42 | 3123, 3141 | C10 신규 |
| F43 | `settlement.report.read` | Sobo43 (정산 통계) | 3558, 3591 | seed v1.0 |
| F44 | `settlement.bill` | Sobo44 | 3625 | C10 신규 |
| F45 | `settlement.write` | Sobo45 (청구) | 3701 | seed v1.0 |
| F46 | `settlement.adj` | Sobo46 | 3408, 3441, 3474 | C10 신규 |
| F47 | `settlement.report.month` | Sobo47 (월합계) | 3658 | seed v1.0 |
| F48 | `settlement.tax.read` | Sobo48 | 3195 | C10 신규 |
| F49 | `settlement.misc2` | Sobo49 | 3308 | C10 신규 |
| F51 | `report.kpi.read` | Sobo51 | 3831 | C10 신규 |
| F52 | `report.kpi.write` | Sobo52 | 3858 | C10 신규 |
| F53 | `report.delivery.read` | Sobo53 | 3885 | C10 신규 |
| F54 | `report.return.read` | Sobo54 | 3984 | C10 신규 |
| F55 | `report.book.read` | Sobo55 | 3912 | C10 신규 |
| F56 | `report.cust.read` | Sobo56 | 3930 | C10 신규 |
| F57 | `report.month.read` | Sobo57 | 3948 | C10 신규 |
| F58 | `report.year.read` | Sobo58 | 3966 | C10 신규 |
| F59 | `report.year.write` | (Interbase only) | Interbase 3103 | C10 신규 (예약) |
| F61~F89 | (예약) | (Interbase 트리에 일부 정의 — 본 운영 트리에서는 미사용) | Interbase 3126~ | C10 예약 (서버 시드 only) |

## 2. 셀 값 의미

| 값 | 의미 | 모던 동작 |
|----|------|-----------|
| `O` | Read-Write (full) | 라우터 200 OK |
| `R` | Read-Only | GET 200 / POST·PUT·DELETE 403 |
| `X` | Deny | 메뉴 자체 비표시 + 라우터 403 |
| ` ` (공백) | 미지정 (= X) | 동일 동작, UI 는 점선 |

## 3. C10 신규 가드 매트릭스

- 신규 80개 키 = 7개 (seed v1.0 — 그대로) + 22개 (C10 신규 정의) + 1개 (예약, F59) = 30 키 정본 + 50 키 예약/Interbase only
- 본 사이클 정본 30 키 만 `legacy_permission_map` v1.1 시드에 추가
- **2026-04-22 (DEC-056 M5 적용 완료)**: §1 30 정본 + §4 7 확장 = **52 키 전체** 가 `legacy_permission_map` v1.2 시드 (`web_admin.json` + `admin_service._DEFAULT_LEGACY_PERMISSION_MAP`) 에 일괄 적재. `Id_Logn` Fxx 매트릭스 → 모던 `permission_code` 합성에 사용. R 페어(F18r) 는 `_merge_fxx_to_permissions` 가 `*.write` → `*.read` 자동 변환으로 흡수(별도 행 시드 불필요).
- 라우터 가드는 `app/core/deps.py::require_permission(code)` 1 의존으로 통합

## 4. 확장 라인 신규 권한키 (C13/C14)

본 카탈로그는 `C10 풀 + 확장 후보` 의 **신규 permission_code** 를 등록하는 단일 정본이다. C10 의 fail-fast 가드 (`test_G_05_unknown_permission_code_fails_fast`) 가 미등록 키 사용을 차단하므로, 신규 라우터 작성 시 본 §4 갱신을 선행해야 한다.

| 확장 키 | 모던 permission_code | 출처 시나리오 | 용도 | 등록 사이클 |
|---|---|---|---|---|
| F50 | `admin.stats.sales` | C13 통계 | 기간별 매출 분석 (`/api/v1/stats/sales-period`) | 확장 라인 v0.2 |
| F51e | `admin.stats.customer` | C13 통계 | 거래처별 판매 분석 (`/api/v1/stats/customer-analysis`) | 확장 라인 v0.2 |
| F52e | `admin.stats.book` | C13 통계 | 도서 회전율 (`/api/v1/stats/book-turnover`) | 확장 라인 v0.2 |
| F53e | `admin.stats.quarterly` | C13 통계 | 분기/반기 손익 (`/api/v1/stats/quarterly-summary`) | 확장 라인 v0.2 |
| F90 | `admin.audit.read` | C14 운영 | audit 통합 뷰 (`/api/v1/admin/audit`) | 확장 라인 v0.2 |
| F91 | `admin.metrics.read` | C14 운영 | Prometheus exposition (`/metrics`) | 확장 라인 v0.2 |
| F92 | `admin.health.read` | C14 운영 | `/health` 확장 dependency 상세 | 확장 라인 v0.2 |

> **명명 규약**: F51/F52/F53 은 §1 의 Sobo51/52/53 (`report.kpi.*` / `report.delivery.read`) 와 의미가 다르므로 카탈로그 키 자체는 `F51e`/`F52e`/`F53e` (extension 접미) 로 표기하고 `permission_code` 만 `admin.stats.*` 단일 정본으로 등록한다 (라우터 grep 가드는 `permission_code` 로 검사).

## 5. 결정 (DEC) 트레이서

- DEC-028 — 본 카탈로그의 모든 30 정본 키는 `data-legacy-id` 부착 시 출처 폼/메뉴 ID (Chul.MenuItem* 등) 와 1:1 일치
- DEC-040 — 본 카탈로그는 `Chul.pas`/`Subu45.pas`/`Base01.pas` 등 레거시 SQL 5종 패턴을 100% 재사용한 `permission_code` 만 등록 (신규 SQL 도입 0)
- DEC-041 — 미정의 `permission_code` 가 라우터에서 사용될 경우 `test_G_05_unknown_permission_code_fails_fast` 정적 가드로 차단 → 표준 401/403 응답 트리(C13)에서 fail-fast
- DEC-044 — 확장 라인(C13/C14) 의 신규 키는 본 §4 단일 등록. 등록 후 contract `*.yaml` 의 `permission_keys_new` 와 1:1 일치 강제 (axis_doc grep)

## 6. 변경 이력

- 2026-04-20 — 초판 (C10 T2 — Chul.pas 80개 호출 지점 인덱싱 + 30 정본 매핑 확정)
- 2026-04-20 — admin.user.read (F18r) 신규 추가
- 2026-04-20 — §4 결정 트레이서 추가 (C10 T7)
- 2026-04-20 — §4 확장 라인 신규 키 7종 등록 (C13/C14 진입 게이트). `admin.stats.{sales,customer,book,quarterly}` + `admin.{audit,metrics,health}.read` + DEC-044 신규.
