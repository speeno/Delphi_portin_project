# 프로필·비밀번호 수정 UX·API 스펙 (`PROF-*` / `PWD-*`)

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-23 |
| 추적 ID | `PROF-*` (프로필 필드/액션), `PWD-*` (비밀번호 액션) |
| 단일 원천 | 본 문서. UI/API/감사 정합은 본 문서를 기준으로 PR 진행. |
| 정합 | [`docs/onboarding-rbac-menu-matrix.md`](onboarding-rbac-menu-matrix.md) (`ACC-MENU-ADMIN-06`, `ACC-API-06/07`), [`docs/onboarding-governance-spec.md`](onboarding-governance-spec.md), DEC-005 (비번 정책), [`backend/app/services/id_logn_service.py`](../도서물류관리프로그램/backend/app/services/id_logn_service.py) (`reset_password`) |

---

## 1. 한 줄 요약

- **본인 변경**(self-service): 프로필 4 필드 + 비밀번호. 모든 활성 유형 허용.
- **관리자 대리 변경**: T1 전체 / T2-DIST 본인 총판 사용자만 — 비밀번호 reset + 프로필 일부 필드.
- **신규 발급(가입 직후)**: 자동 임시 비번 메일 발송 후 첫 로그인 시 변경 강제 — `PWD-FLOW-01`.
- 감사 4 종(`profile.update_self`, `profile.update_admin`, `password.change_self`, `password.reset_admin`) 모두 admin_audit 로 적재.

---

## 2. 프로필 필드 표 (`PROF-FIELD-*`)

| ID | 필드 | 자가 변경 | 관리자 변경 (T1) | 관리자 변경 (T2-DIST) | 검증 |
|----|---|:-:|:-:|:-:|---|
| `PROF-FIELD-01` | display_name (`gname`) | ✓ | ✓ | ✓ (본인 총판 hcode 사용자) | 1~80자, 한글/영문/숫자/공백 허용 |
| `PROF-FIELD-02` | contact_email | ✓ | ✓ | ✓ | RFC 5322 lite, 120자 이내 |
| `PROF-FIELD-03` | contact_phone | ✓ | ✓ | ✓ | E.164 또는 한국 형식 (010-XXXX-XXXX) |
| `PROF-FIELD-04` | organization (`hname`) | — | ✓ | ✓ | 80자, 변경 시 admin audit 필수 |
| `PROF-FIELD-05` | account_type (`ACC-T*`) | — | ✓ | — | T1 only, ENUM, 변경 시 DSN 재계산 트리거 |
| `PROF-FIELD-06` | primary_server | — | ✓ | — | DEC-052 admin 화면과 동일 컴포넌트 |
| `PROF-FIELD-07` | login_id (`gcode`) | — | — | — | **불변** — 변경 필요 시 새 계정 발급 + 폐기 |

---

## 3. UX 흐름

### 3.1 본인 (`PROF-UX-SELF`)

```mermaid
flowchart LR
    Login --> Nav[Nav 우상단 사용자 메뉴]
    Nav --> ProfilePage[/profile]
    ProfilePage --> EditProfile[프로필 4 필드 편집]
    ProfilePage --> ChangePassword[비밀번호 변경]
    EditProfile -->|PUT /api/v1/profile/me| API
    ChangePassword -->|POST /api/v1/profile/me/password| API
    API --> Audit[admin_audit]
    API --> SuccessToast
```

- 라우트: `/(app)/profile/page.tsx` — 본인 모든 유형 접근 가능.
- 비밀번호 변경 시 **현재 비밀번호 재확인** 필수 (`PWD-RULE-01`).

### 3.2 관리자 (`PROF-UX-ADMIN`)

- T1: `/(app)/admin/users/[hcode]/edit` 에서 §2 의 모든 ✓ 필드 편집.
- T2-DIST: 동일 화면에 본인 총판 hcode 필터 적용 — UI 는 동일, 결과 셋만 좁힘.
- 비번 reset 은 별 버튼 — 즉시 임시 비번 발급 + 본인 메일/SMS 발송 (`PWD-FLOW-02`).

---

## 4. API 표 (`PROF-API-*` / `PWD-API-*`)

| ID | 메서드 + 경로 | 입력 | 응답 | 권한 |
|----|---|---|---|---|
| `PROF-API-01` | `GET /api/v1/profile/me` | — | 본인 프로필 + ETag | 본인(모든 유형) |
| `PROF-API-02` | `PUT /api/v1/profile/me` | `display_name?, contact_email?, contact_phone?` + `If-Match` | 갱신 결과 + ETag | 본인 |
| `PWD-API-01` | `POST /api/v1/profile/me/password` | `current_password, new_password` | 200 + 새 ETag | 본인 |
| `PROF-API-03` | `GET /api/v1/admin/users/{hcode}` | — | 사용자 + ETag | T1, T2-DIST(소속) |
| `PROF-API-04` | `PUT /api/v1/admin/users/{hcode}` | §2 의 모든 admin 변경 가능 필드 + `If-Match` + `X-Audit-Token` | 갱신 결과 + ETag | T1, T2-DIST(소속) |
| `PWD-API-02` | `POST /api/v1/admin/users/{hcode}/password-reset` | `newPassword?` (없으면 임시 자동 생성) + `X-Audit-Token` | `{ temp_password, must_change_on_next_login: true, etag }` | T1, T2-DIST(소속) |

> `PWD-API-02` 는 현 코드 [`/id-logn/{hcode}/password-reset`](../도서물류관리프로그램/backend/app/routers/admin.py) 와 동일 핸들러 — 본 스펙은 응답 본문에 `must_change_on_next_login` 플래그 추가만 권고.

---

## 5. 비밀번호 정책 (`PWD-RULE-*`)

| ID | 규칙 | 비고 |
|----|---|---|
| `PWD-RULE-01` | 본인 변경 시 현재 비번 재확인 필수 | 세션 토큰 탈취 시나리오 가드 |
| `PWD-RULE-02` | 길이 ≥ 10, 영문 + 숫자 + 특수 중 2 종 이상 | DEC-005 정합 — 레거시 4 자리 PIN 대비 강화 |
| `PWD-RULE-03` | 최근 3 개 재사용 금지 | `password_history` 보조 테이블 (후속 PR) |
| `PWD-RULE-04` | 임시 비번은 12 시간 내 변경하지 않으면 자동 만료 | 만료 후 재 reset 요청 |
| `PWD-RULE-05` | 5 회 연속 실패 시 30 분 잠금 | DEC-005 강화 |
| `PWD-RULE-06` | 자가 변경 후 모든 기존 세션 무효화(자기 1 세션 제외) | jti rotation |

---

## 6. 감사 로그 (`PROF-AUD-*` / `PWD-AUD-*`)

| ID | 액션 | 페이로드(예) |
|----|---|---|
| `PROF-AUD-01` | `profile.update_self` | `{ "actor": "<self>", "fields": ["display_name","contact_email"] }` |
| `PROF-AUD-02` | `profile.update_admin` | `{ "actor": "<admin>", "target": "<hcode>", "fields": [...], "before": {...}, "after": {...} }` |
| `PWD-AUD-01` | `password.change_self` | `{ "actor": "<self>", "result": "ok" }` |
| `PWD-AUD-02` | `password.reset_admin` | `{ "actor": "<admin>", "target": "<hcode>", "temp_issued": true }` (비번 평문 절대 미적재) |

비밀번호 평문은 **어디에도** 적재되지 않는다 — 로그·DB·메모리 dump 모두. 임시 비번은 메일/SMS 채널로만 1회 전달.

---

## 7. 5 축 정합

| 축 | 강제 |
|---|---|
| **기능** | §4 표의 8 API 가 200/422/409 케이스 별 happy/edge 회귀 테스트 보유. |
| **데이터** | T2-DIST 가 본인 총판 외 hcode 의 PROF-API-03/04 호출 시 403. |
| **UX** | §3 의 두 흐름이 폼 유효성 + 토스트 + ETag 충돌 메시지 일관. |
| **성능** | self-service P95 < 200ms (DB rt 제외), admin reset P95 < 500ms. |
| **감사** | §6 4 종이 모두 admin_audit 에 1 row + 1초 내 적재. |

---

## 8. 구현 갭 (현 코드 vs 본 스펙)

| 갭 ID | 현 코드 | 본 스펙 차이 | 처리 |
|----|---|---|---|
| `PROF-GAP-01` | `/api/v1/profile/me` 미구현 | `PROF-API-01/02/PWD-API-01` 신설 필요 | 다음 PR — `routers/profile.py` |
| `PROF-GAP-02` | `id_logn_service.reset_password` 응답에 `must_change_on_next_login` 없음 | 응답 본문 확장 + `id_logn` 행에 `temp_password_at` 컬럼 추가 (in-memory) | 동일 PR |
| `PROF-GAP-03` | T2-DIST 의 admin 화면 hcode 필터 부재 | `require_permission("admin.user.write")` 에 `tenant_scope("self_dist")` 보강 | 다음 PR |
| `PROF-GAP-04` | `password_history`, 임시 비번 만료, 세션 무효화 미구현 | 별 사이클 백로그 | OQ 등록 |

---

## 9. 수용 기준

- ✅ §4 의 8 API 가 contract 화 (`migration/contracts/profile.yaml` 신설 후보) 후 라우터 가드와 일치.
- ✅ `(app)/profile/page.tsx` + `(app)/admin/users/[hcode]/edit` 두 화면이 §2 표를 코드 상수로 사용.
- ✅ 본인 변경 후 admin_audit 에 `profile.update_self` 1행이 1초 내 출현.
- ✅ T2-DIST 가 다른 총판 사용자에게 reset 시도 시 403.
