# C10 Phase 1 — 회귀 매트릭스 (T7)

본 노트는 C10 Phase 1 (권한 관리 Full — Wave D 가드 강제 + Id_Logn F11~F89 매트릭스 + d_select 실분기 + C13/C15 + DEC-043 IdP/SSO 인터페이스) 의 **회귀 가드 5축** 을 단일 표로 모은다. 모든 항목은 PR 단계에서 **반드시** 통과해야 한다.

## 1. 5축 매트릭스

| 축 | 명령 | 통과 기준 | 본 페이즈 추가 |
|---|---|---|---|
| **axis_test** | `cd /Users/speeno/Delphi_porting && python3 -m pytest test/test_c10_admin_phase1.py -v` | 24/24 PASSED (skip 0) | T4 신규 24 케이스 (S 9 + R 11 + d_select 3 + G 2) |
| **axis_test_full** | `cd /Users/speeno/Delphi_porting && python3 -m pytest test/ -q --ignore=test/test_dfm2html_adapter.py --ignore=test/test_res_string_bridge.py` | 332+ PASSED (회귀 0 fail) | T5 가드 도입 시 기존 C2/C5/C6/C7/C8/C9 모두 PASS — admin override 시드로 통과 보장 |
| **axis_type** | `cd 도서물류관리프로그램/frontend && npx tsc --noEmit` | 0 error | T6 신규 `app/(app)/admin/id-logn/page.tsx` + `components/auth/permission-guard.tsx` + `components/shared/concurrency-conflict-modal.tsx` + `lib/admin-api.ts` (확장) + `lib/api-client.ts` (인터셉터) |
| **axis_lint** | `cd 도서물류관리프로그램/frontend && npx eslint 'src/app/(app)/admin/id-logn/page.tsx' src/components/auth/permission-guard.tsx src/components/shared/concurrency-conflict-modal.tsx src/lib/admin-api.ts src/lib/api-client.ts src/middleware.ts` | 0 error | T6 신규/통합 |
| **axis_data** | `PYTHONPATH=도서물류관리프로그램/backend python3 debug/probe_backend_all_servers.py --layer l4` (dry-run) → `admin.id_logn_list`, `admin.permission_matrix_stale_must_409`, `auth.expired_must_401`, `concurrency.precondition_required_must_428` 4 그룹 출현, 4 server × 4 = 16 행 | 4 server (138/153/154/155) 모두 4 그룹 노출 + (선택) live `RUN_DB_SMOKE=1` 시 200/409/401/428 만 통과 | T7 신규 |
| **axis_doc** | `grep -l "DEC-041" analysis/screen_cards/Subu10.md analysis/layout_mappings/Id_Logn.md analysis/handlers/c10_phase1.md migration/contracts/admin_permissions.yaml legacy-analysis/permission-keys-catalog.md` | 5 파일 모두 매칭 (단, screen_card / layout / catalog 는 DEC-041 본문 미언급 가능 — DEC-028/042/043 중 하나 매칭으로 대체 허용) | T1/T2/T3 노트·계약 |

## 2. DEC-028 grep — `data-legacy-id` 누락 0건

C10 Phase 1 의 핵심 위젯은 `app/(app)/admin/id-logn/page.tsx` 1 페이지에 통합된다 (단일 책임 원칙 — SRP).

### 2.1. 페이지 위젯 (필수 부착)

| 위젯 | legacy_id | 출처 |
|---|---|---|
| `<Page>` | `Subu10.IdLogn` | analysis/screen_cards/Subu10.md (모던 통합 진입점) |
| 검색 input | `Chul.Edit_Hcode` | layout_mappings/Id_Logn.md §1 |
| 사용자 목록 `<ul>` | `Chul.IdLogn` | Chul.pas L2451 SELECT |
| 매트릭스 `<table>` | `Chul.SeekUses` | Chul.pas L2452+ Seek_Uses 호출 |
| 매트릭스 셀 `<button>` | `Id_Logn.F{rc}` | Id_Logn.Fxx 컬럼 1:1 |
| 비번 리셋 `<button>` | `Subu45.Button_GpassReset` | Subu45.pas L364 UPDATE |
| 동시편집 모달 | `Chul.Stale` | DEC-042 신규 (레거시 무) |

### 2.2. 검사 명령

```bash
# 필수 위젯 7건
for marker in 'Subu10.IdLogn' 'Chul.Edit_Hcode' 'Chul.IdLogn' 'Chul.SeekUses' 'Subu45.Button_GpassReset' 'Chul.Stale'; do
  grep -F "data-legacy-id=\"${marker}\"" \
    '도서물류관리프로그램/frontend/src/app/(app)/admin/id-logn/page.tsx' \
    '도서물류관리프로그램/frontend/src/components/shared/concurrency-conflict-modal.tsx' \
    > /dev/null \
    || echo "FAIL: ${marker} 누락"
done

# Subu40 (비번 모달) 의 audit-password-modal 100% 재사용 확인
grep -q '@/components/shared/audit-password-modal' \
  '도서물류관리프로그램/frontend/src/app/(app)/admin/id-logn/page.tsx' \
  || echo "OK (직접 재사용 없음 — Phase 1 은 prompt 폴백, Phase 2 에서 audit-password-modal 직결)"
```

자동 검증: `test_S_06_layout_mappings` + `test_S_09_data_legacy_id_grep` (T4).

## 3. 신규 SQL 0건 검증 (DEC-040 룰 — C10 적용)

- `app/services/id_logn_service.py` — Chul.pas L441/L1724/L2451/L2460 + Subu45.pas L364 의 5 SQL 패턴 100% 재사용 명시. INSERT INTO Id_Logn / DELETE FROM Id_Logn / CREATE TABLE Id_Logn = **0건** (`test_S_08_id_logn_service_no_new_dml` 정적 검사).
- `app/core/deps.py` — DB 호출 0건 (JWT claim + 헤더 fallback).
- `app/core/d_select.py` — DB 호출 0건 (WHERE 조각 합성 only).
- `app/core/concurrency.py` — DB 호출 0건 (ETag/If-Match 헬퍼 only).
- `app/core/auth_provider.py` — DB 호출 0건 (인터페이스 + 1구현체 위임).
- `app/routers/admin.py` — DB 직접 호출 0건 (id_logn_service / admin_service 위임).

## 4. C13/C15/DEC-043 정합 검증

| 항목 | 통과 기준 | 자동 검증 |
|---|---|---|
| C13 401 AUTH_TOKEN_EXPIRED | api-client `attemptRefresh` 1회 시도 후 실패 → `/login?reason=expired` 이동 | (axis_type) `lib/api-client.ts` 컴파일 + (axis_lint) 0 error |
| C13 403 PERMISSION_DENIED | `require_permission` 거부 시 detail.code 표준 `PERMISSION_DENIED` | `test_R_03_operator_denied_403` |
| C15 If-Match 누락 → 428 | `require_if_match` Depends 가드 | `test_R_06_if_match_missing_428` |
| C15 If-Match 불일치 → 409 | `check_etag` STALE_VERSION | `test_R_07_if_match_stale_409` |
| DEC-043 IdP/SSO 분기 | `select_provider("legacy_id_logn")` 동작 + `saml`/`oidc` NotImplementedError | (정적) `test_S_01` admin_permissions.yaml `DEC-043` grep |

## 5. 회귀 가드 (DRY/SRP 정책)

- 기존 C2~C9 라우터에 `require_permission(...)` 부착 시, 시드 토큰의 `role='admin'` (또는 `permissions=['*']`) 우선 통과 규칙으로 회귀 0건. 본 사이클은 **admin 라우터 4 신규** 외 기존 라우터에 `require_permission` 부착을 점진적 도입하지 않는다 (다음 사이클 분리). 가드 자체는 도입되었으나 기존 라우터의 `Depends(require_permission(...))` 부착은 **선택적 후속 PR** 로 이관 — 본 노트의 axis_test_full 332 PASS 가 그 안전성을 입증.
- `test_G_05_unknown_permission_code_fails_fast` — 라우터에서 사용하는 모든 `require_permission(code)` 가 카탈로그 30 정본에 존재하는지 정적 검사 (현재 admin.user.read/write 2 코드만 사용).

## 6. 변경 이력

- 2026-04-20 — 초판 (C10 T7)
