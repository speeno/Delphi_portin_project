# 레이아웃 매핑: Subu40 비밀번호 입력 모달

_생성: 2026-04-20 — C10 T1 (DEC-028 룰 7)_

> **정본**: [`legacy_delphi_source/legacy_source/Subu40.pas`](../../legacy_delphi_source/legacy_source/Subu40.pas) (TSobo40) — 단일 `Edit101` + Enter (#13) → `ModalResult:=mrOK` 의 단순 비번 입력 모달.

## 1. 레거시 위젯 (Subu40.pas)

| 위젯 | 라인 | 의미 |
|---|---|---|
| `TSobo40` (FormShow) | L63~67 | `Edit101.Text:=''; Edit101.SetFocus;` 초기화 |
| `Edit101` (TFlatEdit) | L12 | 비밀번호 입력 (Echo는 DFM `PasswordChar` 추정) |
| `Button101` (TFlatButton) | L13 | OK 버튼 (보통 `ModalResult=mrOK` 호출자에서 처리) |
| `Button102` (TFlatButton) | L14 | 취소 버튼 |
| `Edit101KeyPress` | L204~208 | `if Key=#13 then ModalResult:=mrOK` |
| `Button001~024` (TButton) | L74~192 | 모두 빈 핸들러 — 사용 안 됨 (UI placeholder) |

## 2. 모던 매핑

이미 [`도서물류관리프로그램/frontend/src/components/shared/audit-password-modal.tsx`](../../도서물류관리프로그램/frontend/src/components/shared/audit-password-modal.tsx) 가 C4/C5 사이클에서 신설되어 가동 중. C10 은 **신규 컴포넌트 0** — 동일 모달을 [`/admin/id-logn`](../../도서물류관리프로그램/frontend/src/app/(app)/admin/id-logn) 비번 리셋 버튼에 100% 재사용.

| 모던 위젯 | data-legacy-id | 동작 |
|---|---|---|
| `<Dialog>` (audit-password-modal) | `Subu40.TSobo40` | FormShow → Edit101.SetFocus 와 동일 |
| `<TextField type="password">` | `Subu40.Edit101` | 평문 입력, Enter 단축키 (KeyPress) |
| `<Button>OK</Button>` | `Subu40.Button101` | `onConfirm()` |
| `<Button>취소</Button>` | `Subu40.Button102` | `onCancel()` |

## 3. C10 Phase 1 사용처

| 트리거 | 백엔드 처리 | 비고 |
|---|---|---|
| 비번 리셋 버튼 (다른 사용자) | `POST /admin/id-logn/{hcode}/password-reset` (require_permission `admin.user.write` + audit_token) | 기존 `audit_password_service.verify_admin` 100% 재사용 |
| 자기 비번 변경 | `POST /auth/change-password` (Phase 2, 본 사이클은 인터페이스만) | D-ADM-3 부분 흡수 |
| 자기권한 박탈 가드 (실수 차단) | 422 `ID_LOGN_SELF_REVOKE` (모달 띄우지 않음) | 정책 강제 |

## 4. 레거시 호환성

- **빈 핸들러 24개 (Button001~024)**: 레거시 GUI 디자인 잔재. 모던에서는 노출 0.
- **Edit101.Text 평문 검증**: 레거시는 평문 비교 (`Subu45.pas L372`) — DEC-032 으로 **폐기**. 본 모달은 audit_password_service (bcrypt + 5회 실패/10분 잠금) 로 통합.

## 5. 변경 이력

- 2026-04-20 — 초판 (C10 T1)
