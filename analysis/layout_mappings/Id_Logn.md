# 레이아웃 매핑: Id_Logn 사용자·권한 매트릭스

_생성: 2026-04-20 — C10 T1 (DEC-028 룰 7 — 모던 통합 화면, 출처 위젯 ID 부착)_

> **정본**: 레거시 트리에 `Subu10.pas`/`.dfm` 직접 정의는 없으며, 권한 매트릭스 자체는 **DB 직 UPDATE 운영 관행** 으로 수행됨. 모던 통합 (`/admin/id-logn`) 은 **Wave D `admin_web_platform` v1.0** 위에 사용자 CRUD + Fxx 매트릭스 UI 를 추가한 신규 단일 화면.

## 1. 영역 분할

| 영역 | 모던 컴포넌트 | 레거시 출처 (`data-legacy-id`) | 비고 |
|---|---|---|---|
| 헤더 검색 (Hcode/Gcode/Gname q) | `<TextField data-legacy-id="Chul.Edit_Hcode">` | (없음 — 신규) | DataGrid 페이저와 정합 (DEC-024) |
| 사용자 목록 그리드 | `<DataGrid data-legacy-id="Chul.IdLogn">` | (없음 — 신규) | 8 컬럼: Hcode/Hname/Gcode/Gname/last_login/active_perms/super/actions |
| Fxx 매트릭스 그리드 | `<PermissionMatrixGrid data-legacy-id="Chul.SeekUses">` | `Chul.pas` L2448~ (`Base10.Seek_Uses('Fxx')`) | 행=사용자, 열=Fxx (8x10 = 80 권한키), 셀=`O`/`R`/`X`/공백 토글 |
| 비번 리셋 모달 | `<AuditPasswordModal data-legacy-id="Subu40.Edit101">` | `Subu40.pas` L12 (Edit101 — `analysis/layout_mappings/Subu40.md` 참조) | 기존 `audit_password_service` 100% 재사용 |
| 동시편집 충돌 모달 | `<ConcurrencyConflictModal data-legacy-id="Chul.Stale">` | (없음 — 신규 C15) | 409 STALE_VERSION 처리 |

## 2. F11~F89 권한 매트릭스 (8행 × 10열 = 최대 80 키)

```
        F1x  F2x  F3x  F4x  F5x  F6x  F7x  F8x  F9x
F11  F12  F13  F14  F15  F16  F17  F18  F19
F21  F22  F23  ...                         F29
F31  ...                                   F39
F41  ...                                   F49
F51  ...                                   F59
F61  ...                                   F69
F71  ...                                   F79
F81  ...                                   F89
```

| 키 | 화면/메뉴 | 출처 | 모던 permission_code (시드 — `legacy_permission_map`) |
|---|---|---|---|
| F11 | Sobo11 (마스터-거래처 보기) | `Chul.pas` L?? (Menu101Click) | `master.customer.read` |
| F12 | Sobo12 (마스터-도서) | Chul.pas | `master.book.read` |
| F17 | Sobo17 (도서코드) | `Chul.pas` L2452 (Menu103) | `master.book_code.read` |
| F18 | Sobo18 (사용자/권한) | Chul.pas | `admin.user.write` (슈퍼유저 가드) |
| F21 | Sobo21 (거래명세서) → 출고 쓰기 | Chul.pas | `outbound.write` |
| F22 | Sobo22 (출고/입고 취소) | Chul.pas | `outbound.cancel` |
| F26 | Sobo26 (마스터 일괄 수정) | Chul.pas | `master.write` |
| F31 | Sobo31 (재고원장) | Chul.pas | `inventory.read` |
| F43 | Sobo43 (정산 통계) | Chul.pas | `report.read` |
| F45 | Sobo45 (청구) | Chul.pas | `settlement.write` |
| F47 | Sobo47 (월합계) | Chul.pas | `settlement.report.read` |
| ... | ... | ... | (전수: `legacy-analysis/permission-keys-catalog.md` T2) |

> **셀 값**: `'O'` = R/W (full), `'R'` = read-only (`DBGrid.ReadOnly:=True`), `'X'`/공백 = 메뉴 자체 비표시. 모던에서는 토글 칩으로 4상태 순환.

## 3. 모던 통합 페이지 위젯 ID (DEC-028 룰 7)

```tsx
<Page data-legacy-id="Subu10.IdLogn">
  <SearchBar data-legacy-id="Chul.Edit_Hcode" />
  <DataGrid data-legacy-id="Chul.IdLogn">
    <Column data-legacy-id="Id_Logn.Hcode" />
    <Column data-legacy-id="Id_Logn.Hname" />
    <Column data-legacy-id="Id_Logn.Gcode" />
    <Column data-legacy-id="Id_Logn.Gname" />
    <Column data-legacy-id="Id_Logn.active_perms" />
  </DataGrid>
  <PermissionMatrixGrid data-legacy-id="Chul.SeekUses">
    {/* 8x10 셀, 각 셀 data-legacy-id="Id_Logn.F{row}{col}" */}
  </PermissionMatrixGrid>
  <ToolBar>
    <Button data-legacy-id="Chul.Edit_NewUser">신규</Button>
    <Button data-legacy-id="Subu45.Button_GpassReset">비번 리셋</Button>
  </ToolBar>
</Page>
```

## 4. C10 Phase 1 흡수 정책

| 변형 | 정책 | 근거 |
|---|---|---|
| Hcode='0000' (슈퍼유저) 비번/권한 변경 | 자기 자신만, 외부는 422 `ID_LOGN_SUPER_USER_PROTECTED` | DEC-007 슈퍼유저 분기 폐지 → 단일 가드 코드로 흡수 |
| 자기권한 박탈 (`admin.user.write` O→X) | 422 `ID_LOGN_SELF_REVOKE` | 정책: 마지막 admin 잠금 사고 차단 |
| 동시 매트릭스 편집 | If-Match `revision` 헤더 → 409 `STALE_VERSION` | DEC-042 (T8) — 마스터/주문/정산 동일 정책 |
| 세션 만료 | 401 `AUTH_TOKEN_EXPIRED` → refresh 1회 → `/login?reason=expired` | DEC-041 (T8) — 모든 도메인 라우터 동일 |

## 5. 변경 이력

- 2026-04-20 — 초판 (C10 T1)
