# 사용자 권한관리 동등성 회복 계획 (Legacy ↔ Modern Parity)

- **ID**: PLAN-AUTH-PARITY-2026-04-22
- **상태**: **부분 적용 (M0+M1+M2+M5 APPLIED 2026-04-22)** — M3·M4·M6·M7 은 사용자 SME 확인 대기 (§8)
- **owner**: 메인개발자
- **연관 결정**: DEC-005(비번 평문→해시), DEC-007(슈퍼유저 분기 폐지), DEC-020(legacy_permission_map), DEC-041(RBAC 정공법 / 401·403 인터셉터), DEC-043(IdP/SSO 인터페이스 분리), DEC-046(권한 d_select), DEC-047(시드 폴백 BLS_DEFAULT_ROLE), DEC-051(인증 서버 단일화), DEC-052(사용자별 1:1 데이터 서버), DEC-055(list 화면 상태 보존)
- **연관 산출물**: `legacy-analysis/permission-keys-catalog.md`(F11~F89 30 정본 카탈로그), `analysis/handlers/c10_phase1.md`, `analysis/screen_cards/Subu10.md`, `analysis/layout_mappings/Id_Logn.md`
- **연관 가드레일**: GR-DB-005(병행 운영 기간 테이블 구조 변경 금지) — 본 계획은 **신규 SQL 0건 + 신규 테이블 0건** 정책을 적용해 `Id_Logn` 의 컬럼 그대로 읽고 쓴다(레거시 동등성 보장).

---

## 0. 한눈 요약

| 항목 | 레거시(Delphi) | 현 모던(Web, 2026-04-22 기준) | 본 계획 적용 후 (목표) |
|---|---|---|---|
| 사용자 인증 | `Id_Logn` 비번 비교 (평문 + MD5+Base64 혼재) | ✅ `auth_service.authenticate_user` 100% 동등 | (변경 없음 — 이미 동등) |
| 슈퍼유저 식별 | `Hnnnn = '0000'` (4자리) | ✅ **APPLIED 2026-04-22 (M0)** — 부트스트랩 기본값 `'0000'` 으로 통일 + 슈퍼유저 폴백 3종(hcode/env whitelist/role-admin) 모두 명시 | (완료) |
| 메뉴 단위 가드 | `Base10.Seek_Uses('Fxx')` 80개 호출 | ✅ **APPLIED 2026-04-22 (M5)** — 카탈로그 §1+§4 의 52건 시드 일괄 적용 + R/W 페어 자동 합성 + `test_legacy_permission_map_full_seed` 회귀 가드 | (완료) |
| 'O'/'R'/'X' 3-state | UI 위젯 enable/readonly/disable 토글 | ✅ **부분 APPLIED (M1)** — `_merge_fxx_to_permissions` 가 R 셀을 `*.write` → `*.read` 페어로 자동 변환 (UI 위젯 토글은 페이지별 패턴 일반화는 별도 단계) | UI 위젯 토글은 추가 단계 |
| 메뉴 가시성 (`X` ⇒ 메뉴 비표시) | 메뉴 클릭 시 `if nUse2='X' then ShowMessage` | ✅ **APPLIED 2026-04-22 (M2)** — 사이드바 `usePermissions()` 게이팅 + 그룹 빈 시 자동 hidden | (완료) |
| `D_Select` 행 prefix | `WHERE D_Select+...` SQL 접두사 | ⚠️ `build_d_select_clause` 인터페이스만 존재, 실제 SQL 미삽입 | ⏸️ **M3 보류** — SME 확인 필요 |
| `S_Where0/1/2` 거래처 BL/WL | `Hnnnn` 별 IN/NOT IN 빌드 | ❌ 미포팅 | ⏸️ **M6 보류** — SME 확인 필요 |
| `Hcode` 멀티테넌트 격리 | `Hnnnn=Hcode` 사용자만 자기 데이터 | ⚠️ JWT 에 `hcode` 있으나 도메인 SQL 비강제 (URL 파라미터 신뢰) | ⏸️ **M4 보류** — SME 확인 필요 |
| Id_Logn 권한 변경 | DBA SQL 직수정 (전용 UI 없음) | ✅ **APPLIED 2026-04-22 (M1)** — `LegacyIdLognProvider.fetch_fxx_matrix()` 어댑터 신설 + `_resolve_role_and_permissions_async()` 합류 | (완료) |
| 시드 미완료 사용자 | (해당 없음 — 모든 사용자가 Id_Logn 한 행) | ✅ **APPLIED 2026-04-22 (M1+M5)** — Id_Logn 어댑터 + 52건 시드로 자동 합성 (web_admin.json 시드 폴백 의존도 제거) | (완료) |

> **핵심 원칙**(사용자 룰 합의):
> 1. **신규 SQL 0건** — `Id_Logn` 80 컬럼 그대로 SELECT.
> 2. **재귀적 오류 금지** — 기존 `auth_service`/`admin_service`/`d_select` 인터페이스 유지(LSP), 의미만 채운다.
> 3. **유사 코드 우선 확인** — `LegacyIdLognProvider`, `require_permission`, `build_d_select_clause` 가 이미 *DIP 인터페이스로* 마련되어 있다(현 갭 = 구현). 본 계획은 새 클래스가 아니라 **기존 함수 본문을 채우는 작업**이 95%.

---

## 1. 레거시 분석 (T1)

### 1.1 5계층 권한 메커니즘 (출처)

| 계층 | 위치 | 데이터/SQL | 의미 |
|---|---|---|---|
| ① 사용자 컨텍스트 | `Chul.pas` L441-459 | `SELECT * FROM Id_Logn WHERE gcode=@user` → 글로벌 `Hnnnn`/`Hname`/`Gpass` | 부팅 1회 적재 |
| ② 메뉴 권한 (Fxx) | `Base01.pas` L10160-10179 (`Seek_Uses`) + `Chul.pas` L2374~L4002 80개 호출 | `SELECT Fxx FROM Id_Logn WHERE ...` → `'O'` / `'R'` / `'X'` | 메뉴 클릭 시점 가드 |
| ③ `D_Select` 행 prefix | `Base01.pas` L19-27 + 모든 `Open` 호출 | 모든 SELECT 의 WHERE 접두사 (소프트삭제 `Check<>'D'` 등) | 정본 트리는 `''` (회원사 변형이 채움) |
| ④ `S_Where0/1/2` 거래처 BL/WL | `Chul.pas` L486-515 | `Hnnnn` 별로 `IN ('AAA','BBB',...)` 빌드 | 사용자별 화이트/블랙리스트 |
| ⑤ Hcode 멀티테넌트 | `S_Where` 식 안의 `G7_Ggeo.Chek5='Y'` 조건 | 거래처 마스터의 `Hcode` 가 본인 사용자 hcode 와 일치하는 것만 | 본사·지점 격리 |

### 1.2 셀 값 의미 (`legacy-analysis/permission-keys-catalog.md` §2 인용)

| 값 | 의미 | 모던 동작 (목표) |
|----|------|-----------|
| `O` | Read-Write (full) | 라우터 200 OK |
| `R` | Read-Only | GET 200 / POST·PUT·DELETE 403 |
| `X` | Deny | 메뉴 자체 비표시 + 라우터 403 |
| ` ` (공백) | 미지정 (= X) | 동일, UI 는 점선 표시 |

### 1.3 Fxx 카탈로그 정합 (이미 동결)

- 30 정본 키 카탈로그 = `legacy-analysis/permission-keys-catalog.md` §1 (F11~F58 + 예약).
- 본 계획은 카탈로그 갱신 없이 **시드 적재**(현재 3/30 → 30/30)와 **R 페어 분리**(W/R 두 키)만 수행.

---

## 2. 모던 현 상태 진단

### 2.1 슈퍼유저 판정 — 3 폴백 분기

```68:96:도서물류관리프로그램/backend/app/services/auth_service.py
hcode_norm = (hcode or "").strip()
if hcode_norm == "0000":
    return "admin", ["*"]
if user_id in _admin_whitelist_ids():
    return "admin", ["*"]
roles, perms = admin_service.list_user_roles_and_permissions(user_id)
...
default_role = os.environ.get("BLS_DEFAULT_ROLE", "").strip()
...
return "", []
```

### 2.2 admin / admin123 케이스 진단 (현장 디버그용 — §6 Step M2 회귀)

| 시나리오 | hcode | 환경변수 | web_admin.json 매핑 | 결과 |
|---|---|---|---|---|
| (A) 부트스트랩 기본값만 (`bootstrap_admin_id_logn.py --apply`) | `'0000'` (4자리, **APPLIED 2026-04-22 M0**) | 없음 | 무관 (분기 1 슈퍼유저 즉시 인식) | ✅ 슈퍼유저 |
| (B) `BLS_ADMIN_USER_IDS=admin` 추가 | (무관) | 있음 | 무관 | ✅ 슈퍼유저 (분기 2) |
| (C) Id_Logn Fxx 매트릭스가 채워진 일반 사용자 | (사용자별) | 무관 | 무관 | ✅ **APPLIED 2026-04-22 (M1 분기 3)** — Fxx 'O'/'R' 셀이 자동 합성 |
| (D) `web_admin.json` `web_user_roles` 추가 | (무관) | 무관 | admin → `role-admin` (perms=`['*',...]`) | ✅ 슈퍼유저 (분기 4 폴백) |

→ **2026-04-22 적용 후**: M0 정정으로 (A) 경로 자체가 슈퍼유저로 인식된다. 추가로 M1 분기 3 (`Id_Logn Fxx`) 이 일반 사용자에 대한 자동 권한 합성을 제공한다.

### 2.3 갭 분류 (P0/P1/P2)

| 갭 | 코드 위치 | 우선순위 | 영향 | 상태 |
|---|---|---|---|---|
| G1. `BLS_ADMIN_HCODE='00000'` 자릿수 불일치 | `debug/bootstrap_admin_id_logn.py` L122 | **P0** | admin 부트스트랩 결과 슈퍼유저 미인식 | ✅ **APPLIED 2026-04-22 (M0)** |
| G2. Id_Logn 실 DB 어댑터 부재 | `auth_provider.py::LegacyIdLognProvider` (메서드 없음) | **P0** | 시드 외 모든 사용자 403 | ✅ **APPLIED 2026-04-22 (M1)** |
| G3. 사이드바 권한 게이팅 부재 | `frontend/src/components/app-shell/sidebar.tsx` | **P1** | 권한 없는 메뉴 노출 → 클릭 시 403 토스트 | ✅ **APPLIED 2026-04-22 (M2)** |
| G4. d_select 결과 SQL 미삽입 | 모든 도메인 service (`returns_service.py` L1178 등) 로깅만 | **P1** | 멀티테넌트 격리 미작동 | ⏸️ M3 보류 (SME) |
| G5. Hcode 격리 라우터 가드 부재 | `routers/ledger.py` 등 | **P1** | URL `customer_code=` 변조 시 타테넌트 노출 | ⏸️ M4 보류 (SME) |
| G6. 'R' read-only 의미 손실 | `core/deps.py::require_permission` | **P2** | DBGrid readonly UX 미회복 | ✅ **부분 APPLIED 2026-04-22 (M5)** — 시드 + 페어 합성 완료, 페이지별 UI 토글은 별도 |
| G7. `S_Where0/1/2` 미포팅 | (없음) | **P2** | 거래처 BL/WL 운영 시나리오 차단 (SME 확인 필요) | ⏸️ M6 보류 (SME) |
| G8. 변형사 D_Select 채움 값 미정 | `core/d_select.py` L63 | **P2** | 회원사 트리 소프트삭제 의미 누락 (SME 확인 필요) | ⏸️ M7 보류 (SME) |

---

## 3. 갭 매트릭스 (계획 적용 후 매핑)

| 갭 | 해소 단계 | 산출물 | 회귀 가드 |
|---|---|---|---|
| G1 | M0 | `bootstrap_admin_id_logn.py` 기본값 `'0000'` 정정 + docstring 갱신 | `test_bootstrap_admin_default_hcode_4digit` |
| G2 | M1 | `LegacyIdLognProvider.fetch_fxx_matrix()` 신설 + `_resolve_role_and_permissions` 합류 | `test_id_logn_fxx_matrix_resolves_perms` |
| G3 | M2 | `usePermissions()` 훅 + `Sidebar` `requiredPermission` 비교 | `test_sidebar_hides_X_permission_menu` |
| G4 | M3 | 도메인 service `<D_Select>` 자리 삽입 + ctx 전파 | `test_d_select_injected_in_domain_sql`(정적 검사) |
| G5 | M4 | 라우터 가드 `enforce_hcode_isolation(ctx, input_hcode)` 헬퍼 | `test_hcode_param_tampering_returns_403` |
| G6 | M5 | `*.read` / `*.write` 페어 시드 (카탈로그 §1 의 R 표기 반영) + 페이지별 `disabled` 패턴 일반화 | `test_read_only_role_blocks_post` |
| G7 | M6 | SME 확인 후 `S_Where_service.build_user_filter(login_id)` 신설 (조건부 단계) | `test_s_where_blacklist_excludes_codes` |
| G8 | M7 | SME 확인 후 `build_d_select_clause` 변형 분기 추가 | `test_variant_d_select_appends_check_filter` |

---

## 4. 영향 컴포넌트 인벤토리

### 4.1 백엔드

| 파일 | 변경 종류 | 단계 |
|---|---|---|
| `app/core/auth_provider.py` | **메서드 추가** `fetch_fxx_matrix()` (LegacyIdLognProvider) | M1 |
| `app/services/auth_service.py` | `_resolve_role_and_permissions` 분기 ②③ 사이에 어댑터 합류 | M1 |
| `app/services/admin_service.py` | `list_legacy_permission_map` 시드 30건 확장 (web_admin.json) | M5 |
| `app/core/d_select.py` | 변형 분기 추가 (M7, SME 후) | M7 |
| `app/core/deps.py` | `enforce_hcode_isolation()` 헬퍼 추가 | M4 |
| `app/routers/ledger.py`, `inventory.py`, `transactions.py`, `returns.py` | 도메인 SQL 의 `WHERE` 시작점에 `{d_select}` placeholder 삽입 + ctx 인자 전파 | M3 |
| `app/services/id_logn_service.py` | `_load_from_db()` / `_save_to_db()` 실 구현 (현재 NotImplemented) | M1 후속 |
| `data/web_admin.json` | `legacy_permission_map` 30건 + `web_roles.role-admin.permissions` 정합 | M5 |
| `debug/bootstrap_admin_id_logn.py` | 기본값 `'00000' → '0000'` + docstring 갱신 | M0 |

### 4.2 프론트

| 파일 | 변경 |
|---|---|
| `frontend/src/contexts/auth-context.tsx` | JWT `permissions` 필드 노출 + `hasPermission(code)` 헬퍼 |
| `frontend/src/lib/use-permissions.ts` | **신규** — `hasPermission` / `hasAnyPermission` 훅 |
| `frontend/src/components/app-shell/sidebar.tsx` | `requiredPermission` 비교 → 메뉴 hidden/disabled |
| `frontend/src/lib/form-registry.ts` | 각 `FormMeta` 에 `requiredPermission?: string` 필드 추가 (미지정 = 노출) |
| 도메인 페이지 (예: `app/(app)/outbound/page.tsx`) | `*.read` 권한 사용자 = `disabled` 토글 패턴 일반화 (write 버튼만) |

### 4.3 계약·문서

| 파일 | 변경 |
|---|---|
| `legacy-analysis/permission-keys-catalog.md` | §1 표 의 R 셀에 `*.read` 페어 표기 보강 (M5) |
| `migration/contracts/auth_permission_parity.yaml` | **신규** — 본 계획의 acceptance criteria 동결 |
| `legacy-analysis/decisions.md` | DEC-056(권한 어댑터 신설), DEC-057(d_select 정식 활성화), DEC-058(사이드바 권한 게이팅) 신규 항목 추가 |

---

## 5. 단계별 실행 계획 (M0~M7)

### M0. 부트스트랩 기본값 정정 (P0, 0.5d) — *G1* — **APPLIED 2026-04-22**

```diff
- ap.add_argument("--hcode", default=os.environ.get("BLS_ADMIN_HCODE", "00000"))
+ ap.add_argument("--hcode", default=os.environ.get("BLS_ADMIN_HCODE", "0000"))
```

- docstring L21: `BLS_ADMIN_HCODE   소속 코드           (기본 0000)` 으로 수정.
- 회귀: `test/test_bootstrap_admin_default_hcode_4digit.py` (argparse 호출 → default=='0000' 단정).
- *기존 운영* 데이터 영향: 본 변경은 *기본값* 만 바꾸며 이미 INSERT 된 hcode 행은 변경하지 않는다(GR-DB-001). 운영 admin 행 고치려면 사용자가 `--hcode 0000` 명시 또는 별도 `UPDATE Id_Logn SET hcode='0000' WHERE gcode='admin'` 수동 실행.

### M1. Id_Logn 실 DB 어댑터 (P0, 2d) — *G2* — **APPLIED 2026-04-22**

#### M1-a. `LegacyIdLognProvider.fetch_fxx_matrix(server_id, user_id) -> dict[str,str]`

```python
async def fetch_fxx_matrix(self, server_id: str, user_id: str) -> dict[str, str]:
    """Id_Logn 의 F11~F89 80셀을 dict 로 반환. 없는 셀/행 = 빈 dict."""
    from app.db.async_pool import execute_query
    sql = "SELECT * FROM Id_Logn WHERE gcode = %s LIMIT 1"
    rows = await execute_query(server_id, sql, (user_id,))
    if not rows:
        return {}
    row = rows[0]
    return {
        f"F{i}{j}": _safe_str(row.get(f"F{i}{j}", "")).strip().upper()
        for i in range(1, 9) for j in range(1, 10)
        if f"F{i}{j}" in row
    }
```

#### M1-b. `_resolve_role_and_permissions` 합류

기존 분기 ②③ **사이**에 ②.5 추가 (LSP 보존, 시그니처 변경 없음):

```python
# ②.5 — Id_Logn Fxx 매트릭스 합성 (DEC-056 — Wave A 어댑터)
provider = select_provider()
if hasattr(provider, "fetch_fxx_matrix"):
    fxx = await provider.fetch_fxx_matrix(server_id, user_id)
    catalog = _load_legacy_permission_index()  # {Fxx → permission_code}
    perms_w = {catalog[k] for k, v in fxx.items() if v == "O" and k in catalog}
    perms_r = {f"{catalog[k].rsplit('.',1)[0]}.read"
               for k, v in fxx.items() if v == "R" and k in catalog}
    if perms_w or perms_r:
        return "operator", sorted(perms_w | perms_r)  # role 기본값 = operator (M5 에서 read_only 분리)
```

> **`_resolve_role_and_permissions` 가 동기 함수**인 점에 주의 — `auth_service.authenticate_user` 가 이미 async 이므로 `_resolve_role_and_permissions` 도 함께 async 로 시그니처 확장(인접 호출 1곳만 수정). DEC-007 비번 분기 폐지와 무관.

#### M1-c. server_id 인자 전파

`_resolve_role_and_permissions(user_id, hcode, server_id)` 시그니처로 확장 → `authenticate_user` 가 자체 `server_id` 인자 전달.

### M2. 사이드바 권한 게이팅 (P1, 1d) — *G3* — **APPLIED 2026-04-22**

- `auth-context.tsx` 의 JWT decode 시 `permissions: string[]` 노출.
- `use-permissions.ts` 신규:

```ts
export const usePermissions = () => {
  const { user } = useAuth();
  const set = useMemo(() => new Set(user?.permissions ?? []), [user]);
  const isSuper = set.has("*") || user?.role === "admin" || user?.hcode === "0000";
  return {
    has: (code: string) => isSuper || set.has(code),
    hasAny: (codes: string[]) => isSuper || codes.some((c) => set.has(c)),
  };
};
```

- `form-registry.ts::FormMeta` 에 `requiredPermission?: string` 추가 (33 phase1 + 30 phase2 폼 모두 카탈로그 §1 의 매핑으로 일괄 등록 — `permission-keys-catalog.md` §1 `permission_code` 컬럼 그대로).
- `sidebar.tsx` 의 메뉴 렌더 루프에 `if (form.requiredPermission && !perms.has(form.requiredPermission)) continue;` 추가.

### M3. d_select SQL 삽입 (P1, 2d) — *G4*

- 모든 도메인 SQL 헬퍼(`_dates_count_sql`, `_ledger_rows_sql`, `inventory_service`, `transactions_service`, `returns_service`)에 placeholder `<D_Select>` 마련.
- 라우터에서 `ctx = await get_user_context(...)` → `d_select = await build_d_select_clause(ctx)` → service 인자로 전달.
- service 내부에서 SQL 포맷 시 `WHERE {d_select} AND ...` 로 합성.
- **회귀 가드**: `test/test_d_select_injection.py` — 모든 service의 export 된 SQL 문자열에 `<D_Select>` placeholder 또는 그 결과(`1=1` 또는 `Server_id=...`)가 등장하는지 정적 검사.

### M4. Hcode 격리 라우터 가드 (P1, 1d) — *G5*

```python
# app/core/deps.py
def enforce_hcode_isolation(ctx: dict[str, Any], input_hcode: str | None) -> None:
    if not input_hcode or is_super_user(ctx):
        return
    if (ctx.get("hcode") or "").strip() != input_hcode.strip():
        raise HTTPException(status_code=403, detail={
            "code": "HCODE_FORBIDDEN",
            "message": "본인 hcode 외 데이터 접근 불가",
        })
```

- `routers/ledger.py` 의 `get_customer_ledger(hcode, ...)` 진입부에 1줄 호출.
- 회귀 가드: `test/test_hcode_isolation.py` — operator 토큰 + 다른 hcode → 403.

### M5. R 페어 시드 + 카탈로그 정합 (P2, 1d) — *G6* — **APPLIED 2026-04-22**

- `web_admin.json` `legacy_permission_map` 을 30건으로 확장 (현재 3건).
- 카탈로그 `legacy-analysis/permission-keys-catalog.md` §1 의 `permission_code` 가 `*.read` / `*.write` 명명을 그대로 따르도록 보강.
- `web_roles` 에 `role-read-only` (모든 `*.read` 만) 추가.
- 페이지별 write 버튼: `if (!perms.has('outbound.write')) buttonProps.disabled = true;` 패턴 일반화.

### M6. S_Where0/1/2 BL/WL (조건부, P2, SME 확인 후 2d) — *G7*

- **선결**: 운영 SME 인터뷰로 4대 변형사(remote_138/153/154/155) 의 `Chul.pas` L486-515 분기가 활성화되어 있는지 확인.
- 활성 시: `app/services/s_where_service.py` 신설 — `Id_Logn` 의 `S_Where0/1/2` 컬럼 또는 별도 `Id_Hbod/Id_Hbsv` 테이블에서 `IN (...)` / `NOT IN (...)` 빌드.
- 비활성 시: `decisions.md` 에 "정본 트리 미사용" 기록 후 단계 종결.

### M7. 변형사 D_Select 채움 (조건부, P2, SME 확인 후 1d) — *G8*

- **선결**: 4대 DB 의 주요 도메인 테이블(`G4_Book`, `S1_Ssub` 등)에 `Check` 컬럼이 존재하는지 + 회원사별로 `Check<>'D'` 사용 여부 SME 확인.
- 활성 시: `build_d_select_clause` 의 `role == 'admin'` 분기 *후* 에 `_variant_check_clause(server_id)` 합류:

```python
if role == "admin" or hcode == "0000":
    base = " 1=1 "
else:
    ...
variant = _variant_check_clause(server_id)  # 예: "(Check is null or Check<>'D') and "
return f" {variant}{base} " if variant else base
```

---

## 6. 테스트 / 회귀 (T6)

### 6.1 신규 테스트 파일 (test/ 폴더 — 사용자 룰 준수)

| 파일 | 단계 | 케이스 |
|---|---|---|
| `test/test_bootstrap_admin_default_hcode_4digit.py` | M0 | 1 (default=='0000') |
| `test/test_id_logn_fxx_matrix.py` | M1 | 5 (mock DB → fxx_matrix → perms 합성) |
| `test/test_auth_resolve_with_id_logn.py` | M1 | 4 (시드 미완료 + Id_Logn 'O'/'R' 셀 → perms 정상) |
| `test/test_sidebar_permission_gating.spec.tsx` | M2 | 3 (admin/operator/viewer → 메뉴 가시성) |
| `test/test_d_select_injection.py` | M3 | 1 + 도메인 service 갯수만큼 (정적 grep) |
| `test/test_hcode_isolation.py` | M4 | 3 (super/own/other) |
| `test/test_role_read_only_blocks_write.py` | M5 | 4 (read 200, write 403) |
| `test/test_s_where_filter.py` | M6 (조건부) | 2 |
| `test/test_d_select_variant_check.py` | M7 (조건부) | 2 |

### 6.2 회귀 가드 (필수)

| ID | 가드 | 검증 단계 |
|---|---|---|
| **A1** | hcode 비교는 항상 4자리 영(`'0000'`) | M0/M1 |
| **A2** | `_resolve_role_and_permissions` 가 server_id 없이 호출되면 폴백(시드만) | M1 |
| **A3** | `auth_provider` 가 NotImplemented (Saml/Oidc) 일 때 `_resolve_role_and_permissions` 가 *선험적 hasattr 체크* 로 폴백 | M1 |
| **A4** | 사이드바 게이팅이 슈퍼유저에 대해 모든 메뉴를 노출 | M2 |
| **A5** | d_select placeholder 가 모든 도메인 service SQL 에 *정확히 1회* 등장 | M3 |
| **A6** | 라우터 500 detail.message 에 `type(exc).__name__` 포함 (DEC-046 R6 일관성) | M1~M4 |
| **A7** | `web_admin.json` `legacy_permission_map` 의 키가 카탈로그 §1 의 30 정본 중 하나(미등록 키 fail-fast) | M5 |
| **A8** | 본인 권한 박탈 차단 (`ID_LOGN_SELF_REVOKE`) — 기존 가드 회귀 검증 | M5 |

### 6.3 4서버 동등성 (T7 — 라이브)

```bash
debug/probe_backend_all_servers.py \
  --endpoint /api/v1/admin/id-logn/me \
  --servers mysql3,mysql5,mysql8,maria \
  --user-fixture admin/admin123 \
  --diff
```

- 4서버 모두 동일 `permissions` 셋 반환(슈퍼유저).
- operator 토큰: 4서버 모두 본인 `hcode` 데이터만 노출 + 다른 hcode 입력 시 403.

---

## 7. 위험 및 보완

| 위험 | 영향 | 보완 |
|---|---|---|
| **Id_Logn SELECT 가 도메인 라우터마다 호출되면 N+1 쿼리** | 응답 지연 | (a) JWT 발급 시점 1회만 합성(현 구조 유지) (b) `_resolve_role_and_permissions` 결과는 토큰 lifetime(15분) 동안 캐시 |
| **카탈로그 미등록 Fxx 셀 발견 (예: Interbase F61~F89)** | 권한 누락 | 무시 + 로그 (`logger.info("unmapped Fxx %s for user %s", k, user_id)`) — 카탈로그 §1 마지막 행 정책 그대로 |
| **role 결정 로직이 admin 계정에서 'operator' 로 강등** | UX 회귀 | hcode='0000' 또는 BLS_ADMIN_USER_IDS 분기를 **항상 우선** 두어 (M1-b 의 ②.5 는 *그 이후* 합류) |
| **d_select 합성 시 SQL Injection** | 보안 | `_escape()` 단일 인용 + JWT 출처 값만 허용(`get_user_context` 가 이미 검증) |
| **기존 사용자 권한 변경이 즉시 반영 안 됨** | 운영 혼선 | 토큰 만료(15분) 까지 대기 또는 `/api/v1/auth/refresh` 강제. `decisions.md` 에 명시 |
| **변형사 SME 확인 지연 (M6/M7)** | 일정 슬립 | M6/M7 은 *선택 단계* 로 분리. M0~M5 만으로 사이드바 노출·전권/멀티테넌트 격리 확보 (`open-questions.md` 등록) |
| **자릿수 마이그레이션 이슈** (기존 운영 admin 이 `'00000'` 5자리로 저장됨) | M0 적용 후에도 슈퍼유저 미인식 | 운영 안내: `UPDATE Id_Logn SET hcode='0000' WHERE gcode='admin' AND hcode='00000'` 1건 수동 실행 (운영자 승인) |

---

## 8. 의사결정 사항 (DEC 후보 — 사용자 확인 필요)

| ID | 결정 사항 | 사용자 확인 요청 |
|---|---|---|
| **DEC-056 (안)** | `LegacyIdLognProvider.fetch_fxx_matrix()` 신설 + `_resolve_role_and_permissions` 합류 (M1) | 신규 SQL 0건 정책 유지(`SELECT *` 만 사용) — 동의? |
| **DEC-057 (안)** | `build_d_select_clause` 결과를 **모든 도메인 service** SQL 에 일괄 삽입 (M3) | 일괄 적용 vs 화면별 단계적 적용? |
| **DEC-058 (안)** | 사이드바 권한 게이팅(`requiredPermission`) 도입 — 권한 없는 메뉴 = **hidden** (vs disabled tooltip) | hidden / disabled / 둘 다(슈퍼유저만 disabled 노출) 중 선택 |
| **DEC-059 (안)** | M6 (`S_Where0/1/2`) — 4대 변형사 중 활성화 여부 | SME 확인 결과에 따라 진행/종결 |
| **DEC-060 (안)** | M7 (`D_Select` 변형 채움 `Check<>'D'`) — 4대 변형사 운영 여부 | SME 확인 결과에 따라 진행/종결 |
| **DEC-061 (안)** | 토큰 lifetime 동안 권한 캐시 — 권한 변경 즉시 반영 정책 | 15분 대기 OK / refresh 강제 / 둘 다 |

> 위 6건은 의사결정 후 `legacy-analysis/decisions.md` 에 정식 등록.

---

## 9. 작업 순서 (TODO 단위 — 체크포인트별 회귀 실행)

| # | 작업 | 단계 | 산출 | 회귀 | 상태 |
|---|---|---|---|---|---|
| 1 | M0 — bootstrap 기본값 + docstring | 0.5d | `bootstrap_admin_id_logn.py` | `test_bootstrap_admin_default_hcode_4digit` | ✅ DONE 2026-04-22 |
| 2 | M1-a — `fetch_fxx_matrix()` 신설 (mock DB 단위 테스트) | 1d | `auth_provider.py` | `test_id_logn_fxx_matrix` | ✅ DONE 2026-04-22 |
| 3 | M1-b/c — `_resolve_role_and_permissions_async` + 어댑터 합류 | 1d | `auth_service.py` | `test_auth_resolve_async_with_id_logn` | ✅ DONE 2026-04-22 |
| 4 | M5 (선행) — `legacy_permission_map` 52건 시드 (카탈로그 §1+§4) | 0.5d | `web_admin.json`, `admin_service.py` | `test_legacy_permission_map_full_seed` | ✅ DONE 2026-04-22 |
| 5 | M2 — `usePermissions` + `Sidebar` 게이팅 + `form-registry.ts` 매핑 | 1d | `use-permissions.ts`, `sidebar.tsx`, `form-registry.ts` | `test_sidebar_permission_gating.py` | ✅ DONE 2026-04-22 |
| 6 | M3 — d_select SQL 삽입 (도메인별 PR 분리 — ledger / inventory / transactions / returns) | 2d | service 4건 | `test_d_select_injection` | ⏸️ SME 대기 |
| 7 | M4 — Hcode 격리 가드 | 1d | `core/deps.py` + 라우터 5건 | `test_hcode_isolation` | ⏸️ SME 대기 |
| 8 | M5 (마무리) — `*.read` / `*.write` 페어 + role-read-only | 0.5d | `web_admin.json` | `test_role_read_only_blocks_write` | ✅ 페어 합성 DONE 2026-04-22, role-read-only 분리는 별도 |
| 9 | T7-A — 4서버 probe (실 DB 환경) | 0.5d | `reports/probe-auth-parity-2026-MM-DD.json` | 4서버 동등 | ⏸️ 라이브 환경 필요 |
| 10 | T7-B — `regression_phase2.py` 권한 축 추가 + 5축 체크 | 0.5d | `reports/regression-2026-MM-DD.json` | 5축 PASS | ⏸️ 후속 |
| 11 | (조건부) M6 + M7 — SME 확인 후 결정 | 3d | `s_where_service.py`, `d_select.py` 변형 분기 | 해당 테스트 | ⏸️ SME 대기 |
| 12 | DEC-056·DEC-058 정식 등록 + 잔여 `auth_permission_parity.yaml` v1.0.0 동결 | 0.5d | `decisions.md`, contract | yamllint | ✅ DEC-056·058 등록 DONE 2026-04-22, contract 동결은 잔여 단계 후 |

**총 일정**: M0~M5 + 회귀 = 약 **8.5d** (조건부 M6/M7 제외).

---

## 10. 산출물 인덱스 (PR 첨부 표준)

승격 PR 에는 다음 8개 링크를 본문에 첨부:

1. 본 계획 (`docs/user-permission-management-plan.md`) — 동결 버전
2. `migration/contracts/auth_permission_parity.yaml` v1.0.0
3. `legacy-analysis/permission-keys-catalog.md` (시드 30/30 정합 표기)
4. `backend/app/core/auth_provider.py` + `auth_service.py` 변경분
5. `backend/app/core/d_select.py` + `core/deps.py` (`enforce_hcode_isolation`)
6. `frontend/src/lib/use-permissions.ts` + `sidebar.tsx` + `form-registry.ts`
7. `test/test_*` 9개 파일 PASS 결과
8. `reports/probe-auth-parity-...json` + `reports/regression-...json`

---

## 11. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-22 | 최초 draft. 5계층 레거시 권한 메커니즘(Id_Logn/Seek_Uses/D_Select/S_Where/DBA 직수정)과 모던 8 갭(G1~G8) 매트릭스 작성. M0~M7 단계별 실행 계획 + admin/admin123 케이스 (A)~(D) 4 시나리오 진단 표 포함. DEC-056~061 6건 의사결정 후보 제시. 사용자 룰(신규 SQL 0건·재귀 오류 금지·기존 인터페이스 LSP 보존) 준수. |
| 2026-04-22 (적용) | **M0 + M1 + M2 + M5 일괄 적용 완료**. ① M0: `bootstrap_admin_id_logn.py` 기본값 `'00000'` → `'0000'`. ② M1-a: `LegacyIdLognProvider.fetch_fxx_matrix()` 신설 (`Id_Logn` SELECT, F11~F89 80셀 정규화). ③ M1-b/c: `_resolve_role_and_permissions_async()` + `_load_legacy_permission_index()` + `_merge_fxx_to_permissions()` 신설, `authenticate_user` 라우팅 1줄 변경 (LSP 보존 — 기존 동기 함수 유지). ④ M5: `legacy_permission_map` 시드를 카탈로그 §1+§4 의 **52건 정본 키** 전체로 일괄 확장 (`web_admin.json` + `admin_service._DEFAULT_LEGACY_PERMISSION_MAP`). ⑤ M2: `use-permissions.ts` 신설(`isSuperUser` = `*` ∨ `role==admin` ∨ `hcode==0000`) + `FormMeta.requiredPermission` 필드 추가 + 52 폼 매핑 일괄 + `sidebar.tsx` 게이팅 (그룹 빈 시 자동 hidden). 신규 테스트 5종 (bootstrap·seed·fxx_matrix·resolve_async·sidebar) 모두 PASS. 기존 `test_c10_admin_phase1.py::test_P_01..05` 등 인접 회귀 모두 PASS (LSP 보존 확인). DEC-056·DEC-058 정식 등록. M3·M4·M6·M7 은 SME 확인 대기. |
