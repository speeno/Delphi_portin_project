# 계정별 메뉴/권한 정합 — fidelity 감사 (Phase C–E)

_갱신: 2026-05-30 — account-menu-fxx-rbac Phase C/D/E 적용_

## 루트 원인 (요약)

| 항목 | 레거시 | 수정 전 모던 | Phase C/D 수정 |
|---|---|---|---|
| Fxx 행 조회 | `Hcode+Gname+Gcode+Gpass` 4-key | `gcode LIMIT 1` | `hcode+gname+gcode` 3-key (인증 행 정합) |
| permissions | O/R/X → 기능별 CRUD | 동일 gcode 잘못된 행 | 4-key fetch + `_merge_fxx_to_permissions` |
| login_profile | 부서별 Fxx 지문 | F11 잔존 시 `publisher_main` 오분류 | F51~55 **우세 카운트** → `department_accounting` |
| UI 버튼 | R=조회+인쇄, O=쓰기 | `master.write` 하드코딩 3화면 | `useScreenCaps` + `WriteGate`/`PrintGate` |
| 사이드바 X | `Seek_Uses='X'` 숨김 | license_keys 만 | `canAccessScreen` (Fxx 파생 read) AND |

## 라이브 수치 (Phase A 정본)

출처: [`account-menu-fxx-all.json`](account-menu-fxx-all.json) · 집중 [`account-menu-fxx-5019.json`](account-menu-fxx-5019.json)

| 계정 | hcode | gname | gcode | login_profile | permissions 건수 |
|---|---|---|---|---:|---:|
| 교문사 | 5019 | 교문사 | 교문사 | `publisher_main` | 10 |
| 경리부 | 5019 | 교문사 | 경리부 | `department_accounting` | 5 |
| 교문사 전자책 | 5097 | (라이브) | 교문사 전자책 | (probe) | (probe) |

**경리부 vs 교문사**: 동일 `hcode=5019`·동일 `gname=교문사` — **`gcode` 로만 분리**. `fetch_fxx_matrix` 는 반드시 인증 성공 3-key 를 사용한다.

## caps 규약

- `O` → read+write+print
- `R` → read+print (write 없음)
- `X` → none (사이드바 숨김 + API 403)
- `print = read-level` — [`screen-caps.ts`](../../도서물류관리프로그램/frontend/src/lib/screen-caps.ts)

## F51~55 vs settlement

- `F51~F55` → `report.*` (통계/KPI). `department_accounting` 은 **부서 라벨**이지 `settlement.*` 가 아님.
- 정산은 `F41~F49` → `settlement.*` ([`permission-keys-catalog.md`](../../legacy-analysis/permission-keys-catalog.md) §4c).

## 구현 체크리스트

- [x] `LegacyIdLognProvider.fetch_fxx_matrix` 3-key, `LIMIT 1` 제거
- [x] `authenticate_user` / `refresh_user_claims_from_db` / inspect overlay 3-key 전달
- [x] `infer_login_profile` F51~55 우세
- [x] JWT `gname`·`rdb` 클레임 + `/auth/refresh` 재도출
- [x] `useScreenCaps` · `WriteGate` · `PrintGate`
- [x] 사이드바 `canAccessScreen` (Fxx X)
- [x] 회귀: `test_auth_fxx_4key_fetch` · `test_screen_caps_static` · `test_account_menu_fidelity_coverage`

## 회귀 실행

```bash
python3 -m pytest test/test_auth_fxx_4key_fetch.py test/test_auth_fxx_license_keys_merge.py \
  test/test_id_logn_fxx_matrix.py test/test_screen_caps_static.py \
  test/test_account_menu_fidelity_coverage.py test/test_sidebar_permission_gating.py -q
```

라이브 재검증 (운영자 수동):

```bash
PYTHONPATH=도서물류관리프로그램/backend python3 debug/probe_account_fxx_caps.py --jwt-probe
```
