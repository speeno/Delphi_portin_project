# 북이오웍스 계정 전환 설계 — 위러브솔루션 ID → 이메일 계정 (DEC-235 후보, `ACM-*`)

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-09-03 |
| 상태 | **APPROVED · 구현 중 (2026-09-03)** — 사용자 "개발 진행" 지시로 `legacy-analysis/decisions.md` **DEC-235** 기록. 백엔드·프론트·가드 1차 구현 완료(Phase 1 선공개 상태), 잔여 결정 `ACM-Q-1/5/7` 은 기본안으로 진행 |
| 추적 ID | `ACM-DEC-*` (결정) · `ACM-INV-*` (병행 불변식) · `ACM-RISK-*` (위험) · `ACM-Q-*` (사용자 결정 필요) · `WP-*` (구현 워크패키지) |
| 요청 원문 | 2026-09-03 사용자 요구 — §1 |
| **웹 로그인 정책** | **이메일 계정 전용** (2026-09-03 사용자 확정) — 웹은 전환된 계정으로만 로그인, 레거시 ID 웹 로그인은 컷오버 시점에 차단(403 + 전환 유도). 델파이는 그대로. `ACM-Q-2/4/6/8` 종결 |
| **병행 운영 전제** | 전환 이후에도 **레거시 델파이 프로그램은 기존 `Id_Logn` 계정(Gname/Gcode/Gpass)으로 계속 로그인**한다(2026-09-03 사용자 보강). 따라서 전환 = 이전(migration)이 아니라 **연결(overlay)** — §3 · `ACM-DEC-00` |
| 단일 원천 | 본 문서 + (구현 시) `migration/contracts/account_switch.yaml` |
| 비밀 정책 | [`docs/secrets-policy.md`](secrets-policy.md) G3 — 본 문서·계약·테스트 fixture 에 실 자격증명·인증코드 원문 0건 |
| 연관 | DEC-005(Gpass 평문 보존) · DEC-032(bcrypt 회전) · DEC-096(소속 선택 챌린지) · [DSN-DEC-08/09/12](decision-login-db-routing.md)(분산 Id_Logn 라우팅·소유성 가드) · ONB-RISK-04(메일 인프라 부재) · DEC-104/105/113(키보드 흐름) · [`docs/Design.md`](Design.md) · [`.cursor/rules/login-dsn-dec08.mdc`](../.cursor/rules/login-dsn-dec08.mdc) |

---

## 0. 한 줄 요약

**전환 후에도 레거시 델파이는 기존 `Id_Logn` 계정으로 그대로 로그인한다.** 그래서 이 설계는 계정을 옮기지 않는다 — 기존 **위러브솔루션 계정(회사 + 아이디 + 비밀번호)** 을 한 번 검증한 뒤, **이메일 인증코드**로 소유를 확인하고 새 비밀번호를 설정하면 그 이메일을 **기존 `Id_Logn` 행에 연결(overlay)** 해 북이오웍스 로그인 ID 로 쓴다. `Id_Logn` 은 웹이 한 글자도 쓰지 않는다. **웹은 전환된 이메일 계정으로만 로그인**하고(레거시 ID 웹 로그인 차단), 델파이는 기존 방식 그대로다. 이메일 로그인은 **기존 JWT 클레임(sub=Gcode, sid, rdb, hcode …)을 그대로 발급**하므로 도메인 API·hcode 격리·메뉴 권한은 무변경이다. 계정은 Render 비영속 디스크 대신 **로그인 데이터 서버의 사이드테이블 3종**에 저장하고, 레거시 검증은 **현행 `/auth/login` 코어를 함수로 추출해 재사용**한다.

---

## 1. 요구 사항 (사용자 원문 요약)

**북이오웍스 로그인 페이지**
- 아이디/비밀번호 방식 (아이디 = 이메일).
- 로그인 폼 하단에 **[위러브솔루션 → 북이오웍스 계정 전환하기]** 버튼 → 계정 전환 페이지로 이동.

**계정 전환 페이지**
- 기존 위러브솔루션에서 쓰던 **[출판사 / 아이디 / 비밀번호]** 세 필드 입력.
- 북이오웍스 아이디로 쓸 **이메일 주소** 입력.
- 해당 메일함에서 **인증코드** 확인 (복사 버튼).
- 전환 페이지에서 **인증코드 입력 + 비밀번호 설정**. 비밀번호는 **평문 저장** (추후 북이오 계정으로 재사용 목적).
- 비밀번호 설정 완료 시 **북이오웍스 로그인 페이지**로 이동.

**전제 (2026-09-03 보강)**
- 전환(마이그레이션) 이후에도 **기존 로그인 계정과 방식은 레거시 델파이 프로그램에서 병행 사용**한다. 델파이 쪽 코드·데이터는 바꾸지 않는다.
- **웹에서는 신규 포팅된(이메일) 계정으로만 로그인**할 수 있고, 레거시 델파이 프로그램은 그대로 사용하는 상태가 목표다 (2026-09-03 사용자 확정 — 웹의 레거시 ID 병행 로그인 없음).

---

## 2. 현행 구조 조사 결과 — 재사용 자산과 제약

| # | 항목 | 현재 상태 (조사 결과) | 본 설계에서의 의미 |
|---|------|------|------|
| 1 | 로그인 API `POST /api/v1/auth/login` ([auth.py](../도서물류관리프로그램/backend/app/routers/auth.py)) | `userId`(Gcode)+`password`(Gpass) + 힌트 `tenantId`/`hcode`/`dbName`. 4 서버 분산 `Id_Logn` 후보를 순회 검증(DSN-DEC-08/09), 복수 소속 검증 시 **409 `ORG_SELECT_REQUIRED`**(DEC-096), 공유 DB 소유성 fail-closed(DSN-DEC-12). 라우터 본문 약 500줄. | **레거시 검증 엔진으로 그대로 재사용** — 라우터에서 순수 함수로 추출(ACM-DEC-02). |
| 2 | 로그인 UI ([login/page.tsx](../도서물류관리프로그램/frontend/src/app/(public)/login/page.tsx)) | 회사 선택 콤보(`GET /auth/org-options`, tenants_directory 한글 라벨, 기본 "자동 결정") + 로그인 ID + 비밀번호. 소속 선택 카드 UI + `localStorage` 기억. | 전환 페이지의 **"출판사" 필드 = 이 회사 선택 콤보**. 소속 선택 카드도 그대로 재사용. |
| 3 | 레거시 Delphi 로그인 (`Chul.pas` L323) | `Select Hcode,Hname,Gpass From Id_Logn Where Gcode=Logn2 and Gname=Logn1` 후 `Logn3=Gpass` 평문 비교. **출판사(회사)는 EXE 별 `Config.Ini` 로 암묵 결정** — 로그인 창에는 없음. 웹은 이미 Gname 없이 Gcode+Gpass 로 검증(C1 합격선). 델파이 `Sobo10` 은 사용자가 **Gcode/Gname/Gpass 를 직접 변경**할 수 있고(L2122), 운영 관례로 만료 계정은 `Gcode` 를 `_이름_` 으로 바꿔 잠근다(DSN-DEC-09). | **병행 운영 대상** — 델파이는 계속 이 SQL 로 로그인하므로 웹이 `Id_Logn` 행을 바꾸면 델파이 로그인이 깨진다(§3 불변식). "출판사" 는 웹에서 **테넌트(회사) 선택**으로 대응하고, 공유 DB 는 `hcode`/DEC-096 로 단일화. 델파이에서 Gcode 가 바뀌면 링크가 끊길 수 있다 → 재연결 흐름(§3). |
| 4 | 기존 계정 활성화 흐름 `POST /public/activate/lookup` · `/activate/{token}` ([public_lookup.py](../도서물류관리프로그램/backend/app/routers/public_lookup.py)) | 가입 승인 큐(JSON) 기반 토큰 → `id_logn_service.set_password_by_gcode`. **토큰 발송 채널 없음(콘솔만, ONB-RISK-04)**. 비밀번호 규칙 8자+영문+숫자, 열거 방지 동일 메시지(SEC-POL-CITE-04). | 코드 입력/비밀번호 설정 화면 패턴과 보안 문구 재사용. 신설 메일 서비스는 이 흐름에도 연결(부수 효과로 ONB-RISK-04 해소). **단, 이 흐름은 `Gpass` 를 쓰므로 신규 가입 승인 전용으로 한정하고 전환에서는 호출하지 않는다(ACM-INV-7).** |
| 5 | 메일 인프라 | **없음** — `requirements.txt` 에 SMTP/메일 API 의존 없음, `httpx` 는 있음. | 메일 발송 서비스 신설(ACM-DEC-09). |
| 6 | 앱 측 영속 저장소 | `backend/data/*.json` 은 **Render 무료 플랜 비영속** — 재배포 시 이미지 원본으로 리셋 ([DEPLOY.md §3.1](../도서물류관리프로그램/docs/DEPLOY.md)). 정본 패턴 = 로그인 데이터 서버 **사이드테이블** (`Web_User_Prefs`, [user_prefs_db.py](../도서물류관리프로그램/backend/app/services/user_prefs_db.py): `CREATE TABLE IF NOT EXISTS` + `REPLACE INTO`, MySQL 3.23 호환). | 계정·링크·인증코드 = **사이드테이블** (ACM-DEC-01). JSON 파일 저장 금지. |
| 7 | 서버 구성 (`servers.yaml`) | `remote_138`(MySQL 5.1 직결, `BLS_AUTH_SERVER_ID` 기본) · `remote_153`(SSH+MySQL) · `remote_154/155`(SSH+MySQL 3.x raw). | 중앙 계정 테이블 위치 = `remote_138` 기본(env 로 변경 가능). DDL 은 3.23 호환 문법 유지. |
| 8 | 비밀번호 | `Id_Logn.Gpass` 평문(DEC-005). `verify_legacy_password` 는 평문/MD5-b64/MD5-hex 허용. bcrypt 는 `audit_password_service`(passlib·bcrypt 의존 이미 존재). | 신규 계정 비밀번호 해시에 bcrypt 재사용. `Id_Logn` 은 Gpass 뿐 아니라 **행 전체를 변경하지 않음**(ACM-INV-1, 델파이 병행). |
| 9 | JWT ([`_make_token_pair`](../도서물류관리프로그램/backend/app/routers/auth.py)) | `sub`=Gcode, `sid`, `rdb`(테넌트 DB), `hcode`, `account_type`, `tenant_id`, `fxx_caps`, `license_keys` … 모든 도메인 API·hcode 격리가 이 클레임에 의존. `/auth/refresh` 는 클레임+Id_Logn 재도출. | 이메일 로그인도 **동일 클레임** 발급 → 도메인 무변경(ACM-DEC-07). |
| 10 | 프론트 공개 영역 | `(public)` 라우트 그룹, `BrandHero`/`Logo`, 디자인 토큰(hex 금지, `brand-primary` CTA 화면당 1개), `middleware.ts` `PUBLIC_PATHS = ["/", "/login", "/signup"]`(정확 일치). | 신규 공개 라우트는 PUBLIC_PATHS 에 추가. 화면 매트릭스에는 `WEB_ONLY` 로 등록. |
| 11 | 회귀 가드 | 로그인 회귀 6종(`login-dsn-dec08.mdc`) + `test_dec096_org_select_login.py` + `tools/classify_login_audit_logs.py` + `debug/probe_backend_all_servers.py` 스모크 매트릭스. `LoginRequest` 의 `AliasChoices` 이름 변경 금지. | 전부 PASS 유지가 DoD. 새 라우트는 스모크 매트릭스 등록. |

---

## 3. 병행 운영 원칙 — 레거시 델파이 공존 (`ACM-DEC-00`, 2026-09-03 보강)

**전제**: 전환 이후에도 레거시 델파이 프로그램은 기존 `Id_Logn` 계정(작업자명 Gname · 아이디 Gcode · 비밀번호 Gpass)으로 계속 로그인한다. 델파이는 웹 계정의 존재를 모르며 델파이 쪽 코드는 한 줄도 바꾸지 않는다. 따라서 **"계정 전환" 은 계정을 옮기는 이전(migration)이 아니라, 이메일 자격을 기존 `Id_Logn` 행에 연결(overlay)하는 것**이다.

| 역할 | 정본 | 비고 |
|------|------|------|
| 신원(누가 어느 회사·출판사 소속인가) · 권한(F11~F89) · 만료/잠금 | `Id_Logn` (테넌트 DB, 델파이가 관리) | 웹은 **읽기만**. 매 로그인·refresh 때 재도출 |
| 웹 로그인 자격(이메일 · 웹 비밀번호) · 링크 | `Web_Accounts` / `Web_Account_Links` (중앙 사이드테이블) | 델파이는 참조하지 않음 |
| 델파이 로그인 자격(Gname/Gcode/Gpass) | `Id_Logn` | 웹이 절대 쓰지 않음 |

### 3.1 불변식 (`ACM-INV-1` ~ `7`) — 테스트로 강제

| ID | 불변식 | 강제 수단 |
|----|--------|----------|
| `ACM-INV-1` | 전환·이메일 로그인·재설정·링크 관리 **어떤 경로도 `Id_Logn` 을 INSERT/UPDATE/DELETE 하지 않는다.** `Gpass` 는 물론 `Gcode`/`Gname`/`Hcode`/`Fxx`/`Gmemo` 도 손대지 않는다. | 정적 가드 `test_acm_delphi_coexistence.py::test_no_id_logn_write_in_account_paths` — 신규 모듈(`account_switch_service`, `web_accounts_db`, `auth_login_core` 이메일 경로)에서 `Id_Logn` 대상 쓰기 SQL 0건 |
| `ACM-INV-2` | **두 비밀번호는 독립**이다. 델파이에서 Gpass 를 바꿔도 웹 비밀번호는 그대로, 웹에서 비밀번호를 바꿔도 델파이 로그인은 그대로다. | 전환 완료 화면·인증 메일·재설정 화면에 "델파이 프로그램은 기존 아이디·비밀번호 그대로 사용" 문구 고정(스냅샷 테스트) |
| `ACM-INV-3` | 이메일 로그인은 매번 링크가 가리키는 `Id_Logn` 행의 **존재를 확인**하고 권한·계정 유형을 그 행에서 재도출한다. 델파이에서 권한을 바꾸면 다음 웹 로그인/refresh 에 반영된다. | `test_acm_delphi_coexistence.py::test_fxx_change_reflected_on_next_login` |
| `ACM-INV-4` | 행이 삭제됐거나, 만료 잠금 관례(`Gcode` → `_이름_`)로 바뀌었거나, `Gcode`/`Hcode` 가 델파이(Sobo10 `UPDATE Id_Logn SET Gcode=…`)에서 변경되면 웹 로그인은 **fail-closed** 로 401 `ACCT_LINK_STALE` 을 낸다. 웹이 임의로 다른 행에 붙지 않는다(첫 매치 금지, DSN-DEC-12 정합). | `::test_stale_link_fails_closed`, `::test_expired_lock_convention_blocks_web` |
| `ACM-INV-5` | 끊어진 링크는 사용자가 **현재 델파이 자격으로 다시 검증**해야만 갱신된다(재연결 모드 `relink`). 관리자가 대신 붙일 때는 감사 로그 필수. | `/account/switch` `mode='relink'` + `test_acm_link_rules.py` |
| `ACM-INV-6` | 델파이에서 **신규로 만든 사용자도 언제든 전환**할 수 있다 — 전환 페이지 상시 운영, 로그인 인덱스 lazy refresh 가 새 행을 찾는다. | 기존 DSN-DEC-09 lazy refresh 테스트 + 스모크 |
| `ACM-INV-7` | 링크 해제는 델파이에 아무 영향이 없다(되돌리기 가능). 기존 `/activate/{token}` 의 `Gpass` 쓰기는 **신규 가입 승인 전용**으로 한정하고 전환 흐름에서는 호출하지 않는다. | 코드 리뷰 체크리스트 + `test_no_id_logn_write_in_account_paths` |

### 3.2 병행 기간의 사용자·관리자 경험

- 사용자는 **델파이는 그대로**, 웹은 이메일로 쓴다. 전환 완료 화면과 인증 메일에 이 사실을 한 문장으로 못 박는다.
- 회사 관리자는 사용자 추가·삭제·권한을 **지금처럼 델파이(또는 웹 `/admin/id-logn`)에서** 관리한다. 웹 계정을 따로 만들 필요가 없고 각 사용자가 스스로 전환한다.
- 사용자가 델파이에서 아이디(Gcode)를 바꾸면 웹 로그인 시 "레거시 계정 정보가 바뀌었습니다 → 다시 연결" 안내를 받고 현재 델파이 자격으로 재연결한다(비밀번호·이메일 유지).
- 관리자 화면 `/admin/id-logn` 에 "웹 계정 연결됨(이메일 마스킹)" 열을 추가해 전환 현황을 회사별로 본다(선택, WP-8).

### 3.3 이 전제가 초안에서 바꾸는 것

| 항목 | 초안 | 보강 |
|------|------|------|
| 전환의 의미 | 계정 이전 | 이메일 자격 → `Id_Logn` 행 **연결(overlay)** |
| 웹 로그인 방식 | 병행(Phase A) 후 차단(Phase B) | **처음부터 이메일 계정 전용** — 레거시 ID 웹 로그인은 컷오버(D-day)에 차단(403 + 전환 유도), 비상 복구 플래그만 유지. 델파이는 무관 — 웹을 안 쓰는 사용자는 델파이만 계속 사용 |
| 북이오 통합 | "북이오 통합 후 정리" | 북이오 통합과 델파이 병행은 별개 — `Id_Logn` 은 델파이가 살아있는 한(그리고 웹 권한 정본으로서 그 이후에도) 남는다 |
| 링크 키 | `(ServerId, DbName, Hcode, Gcode)` 고정 | 같은 키 + **매 로그인 존재 확인** + `ACCT_LINK_STALE` 재연결 |
| 비밀번호 | 웹 비밀번호만 언급 | 두 비밀번호 독립을 불변식으로 승격 |

---

## 4. 목표 흐름

### 4.1 화면 3개

**A. `/login` (수정)**

```
┌──────────────────────────────────────────────┐
│ 북이오웍스  로그인                           │
│ 이메일        [ name@company.com          ]  │
│ 비밀번호      [ ••••••••                  ]  │
│ [        로그인 (brand-primary)          ]   │
│ ──────────────────────────────────────────── │
│ [ 위러브솔루션 → 북이오웍스 계정 전환하기 ]  │  ← secondary(outline) 버튼, /account/switch
│ 비밀번호 재설정 · 회원 가입 신청 · 공지      │
└──────────────────────────────────────────────┘
```
- 로그인 폼에 **회사 선택 콤보는 없다**(전환 페이지로 이동). 입력값에 `@` 가 없으면(레거시 ID) 서버가 403 `ACCT_SWITCH_REQUIRED` 를 내고, 화면은 "웹은 북이오웍스 계정(이메일)으로만 로그인할 수 있습니다" + 전환 버튼을 강조한다. 비상 시에만 `BLS_LEGACY_ID_LOGIN=on`(break-glass)으로 기존 방식을 임시 복구(기동 시 경고 로그).
- `/login?switched=1` 진입 시 "계정 전환이 완료되었습니다" 배너 + 이메일 자동 채움(sessionStorage 1회).

**B. `/account/switch` (신규 — 한 페이지 3단계 위저드)**

| 단계 | 입력 | 동작 | 결과 |
|------|------|------|------|
| 1 기존 계정 확인 | 출판사(회사 선택 콤보, 기본 "자동 결정") · 아이디 · 비밀번호 | `POST /public/account-switch/verify-legacy` | 성공: 확인 카드(회사 라벨 · 출판사명 Hname · 아이디) + `switchTicket`(15분). 복수 소속: DEC-096 선택 카드 → 선택 후 재검증. 이미 전환됨: "이미 전환된 계정입니다 → 비밀번호 재설정" 안내. |
| 2 이메일 입력 | 이메일 | `POST /public/account-switch/send-code` | "인증코드를 보냈습니다. 메일함을 확인하세요" + 재발송(60초 쿨다운). 이미 북이오웍스 계정이 있는 이메일이면 **연결 모드**(비밀번호 입력 숨김, "기존 계정에 이 회사 계정을 연결합니다"). |
| 3 코드 + 비밀번호 | 인증코드 6자리 · 새 비밀번호 · 확인 | `POST /public/account-switch/complete` | 완료 화면(체크 아이콘) + **"델파이 프로그램은 기존 아이디·비밀번호 그대로 사용하세요"** → 3초 후 또는 버튼으로 `/login?switched=1`. |

- 2·3단계는 **같은 화면에 연속 표시**한다 — 사용자가 메일 탭에 갔다 돌아와도 입력 상태가 남는다(티켓·이메일은 sessionStorage 에 보관, 코드·비밀번호는 보관 안 함).
- 메일의 「인증 계속하기」 딥링크(`/account/switch?ticket=…&code=…`)로 들어오면 3단계가 코드 채워진 채 열린다.

**C. 인증코드 메일**

- 제목 `[북이오웍스] 계정 전환 인증코드`, 본문: 6자리 코드를 큰 글씨(선택·복사가 쉬운 단독 블록)로, 유효 10분, 「인증 계속하기」 버튼(딥링크), "본인이 요청하지 않았다면 무시" 문구.
- 인증 메일에도 같은 문장("델파이 로그인은 바뀌지 않습니다")을 넣는다(ACM-INV-2).
- **메일 클라이언트는 JavaScript 를 실행하지 않으므로 메일 본문 안의 실제 '복사 버튼' 은 만들 수 없다.** 요구의 목적(코드를 손으로 옮기지 않게)은 ① 딥링크로 코드 자동 입력, ② 코드 단독 블록(더블클릭 선택) 두 가지로 충족한다. 웹 페이지의 코드 입력란은 붙여넣기·`autoComplete="one-time-code"` 를 지원한다.

### 4.2 상태 기계

```
[Step1] verify-legacy ──성공──▶ legacy_verified (switchTicket 15분)
   │ 401 동일 메시지 / 409 ORG_SELECT_REQUIRED(선택 후 재시도) / 409 ACCT_ALREADY_SWITCHED
   ▼
[Step2] send-code ──────────▶ code_sent (코드 10분 · 시도 5회 · 재발송 60초)
   │ 429(쿨다운·한도)                        │ 티켓 만료 → Step1 재시작(410)
   ▼                                          ▼
[Step3] complete ──코드 OK + 비밀번호 OK──▶ completed → /login?switched=1
   │ 400 ACCT_CODE_INVALID(불일치/만료 동일) · 423 ACCT_CODE_LOCKED(5회) · 422 ACCT_WEAK_PASSWORD
```

### 4.3 롤아웃 절차 (운영 관점)

| 단계 | 내용 | 게이트 |
|------|------|------|
| **전 Phase 공통** | **델파이 병행** — `Id_Logn` 무변경(ACM-INV-1), 두 비밀번호 독립(ACM-INV-2), 델파이 신규 사용자 상시 전환 가능(ACM-INV-6) | `test_acm_delphi_coexistence.py` PASS |
| Phase 0 준비 | **복원 포인트 생성 완료(2026-09-03)** · **메일 발송 검증 완료(2026-09-03 — 발신자 `newoneseek@buk.io` 실수신 확인)** · **남은 것: Render 환경변수 등록**(등록 전까지 운영 `switchAvailable=false` 로 전환 버튼 숨김) — 태그 `restore-pre-email-account-2026-09-03`(제품 6a913d3 · 허브 ee04c67) + remote_138 DB 기준선, 절차는 [restore-point-pre-email-account-2026-09-03.md](restore-point-pre-email-account-2026-09-03.md). Brevo 발신자 인증 + 도메인 SPF/DKIM 등록, Render env(`BLS_SMTP_*`·`BLS_EMAIL_*`·`BLS_ACCOUNT_*`) 등록, 사이드테이블 생성(첫 호출 시 자동 + 마이그레이션 SQL 문서화), 로그인 공지(platform_portal)에 "계정 전환 안내" 등록 | 테스트 계정 1건 전환 e2e PASS |
| Phase 1 선공개 (선택, 기본 2주) | 전환 페이지 `/account/switch` 만 먼저 공개 + 로그인 화면 배너 "D-day 부터 이메일 로그인만 가능". 로그인 방식은 아직 기존(현행 배포) — 미리 전환한 사용자는 D-day 에 바로 사용 | 사전 전환율 리포트(감사 로그 분류), 헬프데스크 FAQ 준비 |
| Phase 2 컷오버 (D-day, **웹에만**) | 로그인 화면 = **이메일 전용**. 레거시 ID 로그인 403 `ACCT_SWITCH_REQUIRED` + 전환 유도. 관리자 예외 없음(관리자도 전환). 델파이 로그인은 무관. `BLS_LEGACY_ID_LOGIN=on` 은 비상 복구(break-glass)용 | 복원 포인트 대조 `[OK]`, 비밀번호 재설정 화면 배포 완료(ACM-DEC-10), 공지 3회 |
| Phase 3 북이오 통합 | `Web_Accounts` 를 북이오 계정 체계로 이관(평문/복호화 배치, RED 절차) 후 `PwPlain` 컬럼 폐기. **델파이 병행은 계속** — `Id_Logn` 은 남는다 | 북이오 측 이관 완료 확인 |

---

## 5. 결정 사항 (`ACM-DEC-01` ~ `11`)

### `ACM-DEC-01` — 계정 저장소 = 중앙 사이드테이블 3종 (JSON 파일 금지)

- 위치: `BLS_ACCOUNT_STORE_SERVER_ID`(기본 `remote_138`, MySQL 5.1 직결) 의 **전용 DB `BLS_ACCOUNT_STORE_DB`(기본 `bukio_web_db`)** — 테넌트 DB 덤프에 웹 계정(비밀 포함)이 섞이지 않도록 분리하고, 모든 SQL 을 `db.table` 로 명시 한정해 요청 범위 테넌트 DB 컨텍스트(DEC-095)에 끌려가지 않게 한다. 이메일 → 레거시 identity 조회는 **어느 테넌트 DB 인지 모르는 상태**에서 일어나므로 테넌트 DB 가 아닌 중앙 1곳이 필요하다. DSN-DEC-08 이 "장기 옵션"으로 미뤄 둔 `web_users` 중앙 인증 테이블의 최소 실현이다.
- 테이블: `Web_Accounts`(계정) · `Web_Account_Links`(계정 ↔ 레거시 identity, 1:N) · `Web_Account_Codes`(인증코드). DDL 은 §6. 모듈 `app/services/web_accounts_db.py` 가 `user_prefs_db.py` 와 같은 `ensure_tables` + 파라미터 바인딩 패턴을 따른다.
- `backend/data/*.json` 저장 금지 — Render 재배포 시 계정이 사라지는 사고를 원천 차단.

### `ACM-DEC-02` — 레거시 검증 = 현행 로그인 코어 재사용 (함수 추출)

- `auth.py::login` 의 후보 해석 → 순차 검증 → lazy refresh → DEC-096 챌린지 → ownership 결과까지를 `app/services/auth_login_core.py::resolve_and_authenticate(user_id, password, *, tenant_id, hcode, db_name, client_ip) -> LoginOutcome` 로 옮기고, `/auth/login` 과 `/public/account-switch/verify-legacy` 가 **같은 함수**를 호출한다. `LoginOutcome` = `{user, hit_candidate, org_choices | None, audit_fields}`.
- `/auth/login` 의 응답·감사 로그·에러 메시지는 바이트 단위로 무변경 — 로그인 회귀 6종 + `test_dec096_org_select_login.py` 가 게이트.
- 전환 페이지의 **"출판사" = `tenantId` 힌트**(콤보). "자동 결정" 허용. 복수 검증 시 409 `ORG_SELECT_REQUIRED` 를 그대로 전달해 프론트가 기존 선택 카드로 처리한다.

### `ACM-DEC-03` — 전환 티켓 = 서버 무상태 서명 토큰

- `create_access_token` 재사용, `type='switch'`, 만료 15분, `jti` 포함. payload 는 검증된 identity 요약(`sid`, `rdb`, `hcode`, `gcode`, `gname`, `hname`, `tenant_id`, `account_type`, `label`). 비밀번호·Gpass 미포함.
- 응답 본문으로만 전달, 로그 미기록. `complete` 시 `jti` 를 `Web_Account_Codes.TicketId` 와 대조해 **코드가 다른 티켓에 재사용되는 것을 차단**한다.

### `ACM-DEC-04` — 인증코드 정책

| 항목 | 값 |
|------|----|
| 형식 | 6자리 숫자 (`secrets.randbelow`) |
| 유효 | 10분 (`BLS_ACCOUNT_CODE_TTL_MIN`) |
| 시도 | 5회 초과 시 코드 무효화 + 423 (재발송 필요) |
| 재발송 | 60초 쿨다운, 이메일당 시간당 5회, IP 당 시간당 20회 (429) |
| 저장 | salted SHA-256 해시만 (`CodeHash`, `Salt`) — 원문 미저장 |
| 응답 | 전환(`switch`)은 발송 성공/실패·이메일 존재 여부와 무관하게 **동일 메시지** (SEC-POL-CITE-04), 유효한 티켓 보유자에게만 `mode: new|link|relink` 노출(§5 ACM-DEC-08). **재설정(`reset`)은 미등록 이메일에 404 `ACCT_EMAIL_NOT_REGISTERED` 를 즉시 안내** — 사용자 결정(2026-09-03): B2B 폐쇄 환경이라 열거 방지보다 명확한 안내 우선 |
| 로그 | 코드 원문·비밀번호 원문 금지(SEC-POL-CITE-03). 이메일은 `a***@domain` 마스킹 |
| 정규화 | 이메일 `trim` + 소문자, RFC 형식 검사 |

### `ACM-DEC-05` — 비밀번호 저장: 요구(평문) + 해시 병행, 암호화 대안 권장

- **요구 원문대로** `PwPlain` 컬럼에 평문을 보관한다. 동시에 `PwHash`(bcrypt cost 12)를 저장하고 **로그인 검증은 `PwHash` 만** 사용한다. `PwPlain` 은 어떤 API 응답·로그·엑셀·화면에도 노출되지 않으며, 북이오 이관 배치(`tools/export_web_accounts_for_bukio.py`, RED 산출물 절차 = [operating-account-credentials-red.md](operating-account-credentials-red.md))만 읽는다. 이관 완료 후 컬럼을 DROP 한다(Phase 3).
- **권장 대안(`ACM-Q-1`)**: 평문 대신 **AES-256-GCM 봉투 암호화**(`PwEnc`, 키 `BLS_ACCOUNT_PW_KEY` 는 env 만). 북이오 이관 시 같은 키로 복호화하면 "추후 북이오 계정으로 사용" 목적은 동일하게 달성되고, DB 덤프·백업 유출 시 전 계정 비밀번호 노출을 막는다. 코드 차이는 `app/services/account_secret_codec.py` 의 `encode/decode` 1개 모듈뿐이라 결정이 늦어져도 일정에 영향이 없다.
- 규칙: 8자 이상 + 영문 + 숫자(기존 활성화와 동일), 최대 64자. 정책 문서 정합: DEC-005 는 "레거시 Gpass 평문 보존" 이지 신규 저장소의 평문을 허용한 결정이 아니므로, 본 항목은 DEC-235 로 별도 기록한다.

### `ACM-DEC-06` — 웹 로그인 = 이메일 계정 전용 (레거시 ID 웹 로그인 차단, 요청 스키마 무변경)

- `LoginRequest` 필드·`AliasChoices` 는 그대로(login-dsn-dec08 규칙 3). `userId` 값에 `@` 가 있으면 **이메일 계정 경로**: `Web_Accounts` 조회 → 상태(`active`/잠금) → `PwHash` 검증 → `Web_Account_Links` 로 identity 결정 → 해당 서버·DB 의 `Id_Logn` 에서 **행 존재 확인(정확한 Gcode 일치, `_이름_` 만료 관례 그대로)** 후 **권한(Fxx)·계정 유형을 현행 `refresh_user_claims_from_db`/`_resolve_account_type` 로 재도출** → `_make_token_pair`. 비밀번호 불일치는 기존과 동일 401 메시지, 행 부재·변경은 401 `ACCT_LINK_STALE`(ACM-INV-4) + 재연결 안내.
- 링크가 2개 이상이면 409 `ORG_SELECT_REQUIRED`(choices = 링크 목록) → 프론트 기존 선택 카드 → `tenantId`/`dbName` 재제출로 단일화.
- **구현 상태(2026-09-03)**: 코드 기본값 `LEGACY_ID_LOGIN_DEFAULT = "on"`(선공개 기간 — 기존 방식 유지). 컷오버 커밋에서 `"off"` 로 바꾸면 아래 정책이 기본이 되고, 그 뒤 `BLS_LEGACY_ID_LOGIN=on` 은 break-glass(감사 `legacy_login_breakglass=true`). 프론트는 `GET /auth/login-policy` 의 `legacyIdLogin`/`switchAvailable` 로 콤보·전환 버튼을 결정한다.
- `@` 없는 `userId`(레거시 ID)는 **기본적으로 403 `ACCT_SWITCH_REQUIRED`** ("웹은 북이오웍스 계정(이메일)으로만 로그인할 수 있습니다. 계정 전환을 진행하세요"). 관리자 예외 없음 — 관리자도 전환한다. 비상 복구용 `BLS_LEGACY_ID_LOGIN=on`(break-glass) 일 때만 기존 레거시 경로가 열리며, 기동 시 경고 로그와 감사 로그 `legacy_login_breakglass=true` 를 남긴다. 레거시 경로 코드는 전환 페이지 `verify-legacy` 가 같은 코어를 쓰므로 제거하지 않는다. 잠금: 이메일 계정 5회 실패 시 15분 잠금(`FailCount`/`LockedUntil`).

### `ACM-DEC-07` — JWT·세션·도메인 API 무변경

- 이메일 로그인의 JWT 는 기존 클레임 그대로(`sub`=Gcode, `sid`, `rdb`, `hcode`, `account_type`, `tenant_id`, `fxx_caps`, `hname` …) + `acct`(AccountId) + `lvia='email'` 2개만 추가. `/auth/me`·`/auth/refresh`·모든 도메인 라우터·hcode 격리(ACC-DATA-03)·메뉴 권한은 손대지 않는다.
- 세션 만료 시 `/login?reason=expired` 동작도 그대로.

### `ACM-DEC-08` — identity 링크 규칙

- **이메일 1개 = 계정 1개.** identity `(ServerId, DbName, Hcode, Gcode)` 는 **최대 1개 계정**에만 연결(PK). 이미 전환된 identity 로 다시 전환하면 409 `ACCT_ALREADY_SWITCHED` + "비밀번호 재설정" 안내.
- **한 계정에 여러 identity 허용**(같은 담당자가 여러 회사 계정을 가진 경우, DEC-096 실측 672건 패턴). 이미 계정이 있는 이메일로 전환하면 `mode='link'`: 코드 인증 후 링크만 추가하고 비밀번호는 유지. 로그인 시 링크가 여럿이면 소속 선택(ACM-DEC-06).
- `Id_Logn` 은 변경하지 않는다(ACM-INV-1·DEC-005). 레거시 비밀번호가 바뀌어도 링크는 유지된다(링크는 identity 기반, 비밀번호 기반이 아님).
- **링크 drift**: 델파이 Sobo10 에서 `Gcode`(또는 `Hcode`)가 바뀌면 링크가 가리키는 행이 사라진다 → 로그인 401 `ACCT_LINK_STALE` → `/account/switch` **재연결 모드**(`mode='relink'`): 이메일 계정에 로그인된 상태 또는 코드 인증 후, 현재 델파이 자격으로 `verify-legacy` → 옛 링크 행 삭제 + 새 identity 행 삽입(유니크 재검사). 이메일·웹 비밀번호는 유지.

### `ACM-DEC-09` — 메일 발송 서비스 = **Brevo SMTP 무료 티어** (ONB-RISK-04 동시 해소, ACM-Q-3 종결 2026-09-03)

- **구현 완료(2026-09-03, WP-2)**: `app/services/email_dispatch_service.py` — `send_email(to, subject, html, text)` 1개 진입점 + `verify_smtp_connection()`(접속·STARTTLS·로그인만) + `startup_warnings()`(기동 로그). 회귀 `test/test_acm_email_dispatch.py`. 점검 `debug/send_test_email.py --check | --to`.
- provider (`BLS_EMAIL_PROVIDER`):
  - `console` (개발 기본): 로그에 마스킹 주소·제목만. `BLS_EMAIL_DEBUG_ECHO=1` 이면 응답에 코드 포함 — **로컬 전용**, 다른 provider 와 함께 켜지면 기동 경고. 운영(Render)에서 console 이면 기동 경고.
  - `smtp` (**운영 정본 = Brevo**): `smtp-relay.brevo.com:587` STARTTLS, 로그인 = Brevo SMTP 로그인, 비밀번호 = Brevo SMTP 키. `aiosmtplib` 의존 추가. 발송 실패는 예외 없이 `SendResult(ok=False, error=<예외명>)` — 호출자는 열거 방지 동일 메시지 유지.
- env: `BLS_EMAIL_PROVIDER=smtp` · `BLS_SMTP_HOST` · `BLS_SMTP_PORT`(587) · `BLS_SMTP_USER` · **`BLS_SMTP_PASSWORD`(비밀 — 로컬 `.env`·Render 대시보드만)** · `BLS_EMAIL_FROM`(**Brevo 에서 인증된 발신자** 주소 필수) · `BLS_EMAIL_FROM_NAME` · `BLS_EMAIL_REPLY_TO` · `BLS_PUBLIC_BASE_URL`(딥링크). `render.yaml` 에 키는 `sync: false`, 호스트·포트는 값으로 등록.
- Brevo 무료 티어 한도 **일 300통** — 컷오버 전후 전환 폭주 시 초과 가능(ACM-RISK-14). 발신자/도메인 인증(DKIM)은 Phase 0.
- 대안(미채택): Resend HTTP API, 네이버웍스/구글워크스페이스 SMTP.
- 템플릿 `app/services/email_templates/account_switch_code.html` — 메일은 CSS 변수를 못 쓰므로 `Design.md` 의 색 값을 인라인 hex 로 쓰되, **hex 가드 대상은 TSX 뿐**이라 충돌 없음(파일 상단에 사유 코멘트).
- 발송 주체는 Render 백엔드이므로 키는 **Render env** 에 둔다(Vercel 무관). 기존 활성화 안내(`/activate/lookup`)도 같은 서비스로 발송한다(ACM-DEC-11).

### `ACM-DEC-10` — 비밀번호 재설정(컷오버 전 필수)·계정 관리(선택)

- `/account/reset`: 이메일 → 코드(`purpose='reset'`) → 새 비밀번호. 전환 흐름과 코드 인프라·화면 컴포넌트 90% 공유. **컷오버 이후 비밀번호 분실의 유일한 복구 경로**이므로 Phase 2 이전 배포가 필수(ACM-Q-4 종결).
- `/settings/my-profile` 에 "연결된 회사 계정" 섹션(링크 목록·추가 연결·해제) — 로그인 상태에서 추가 연결은 코드 없이 레거시 검증만으로 허용.
- `/admin/accounts`(수퍼): 계정 목록(이메일 마스킹 해제 권한)·잠금 해제·링크 해제·재설정 강제. 감사 로그 필수.

### `ACM-DEC-11` — 신규 가입·활성화 흐름을 전환 흐름에 흡수 (웹 = 이메일 계정 전용의 귀결) — **이연**

> **2026-09-03 구현 시 보류**: 가입 승인이 만드는 `Id_Logn` 행은 아직 C10 Phase 1 **인메모리 상태**(`id_logn_service`)라 실 DB 에 없다. 이메일 로그인은 실 `Id_Logn` 행 존재를 요구하므로(INV-3) 활성화 토큰 → 전환 티켓 교환은 DSN-DEC-10 프로비저닝(실 DB 행 생성) 이후 착수한다. 그때까지 기존 `/activate/*` 는 그대로 두고, 신규 가입자는 승인 후 델파이 임시 비밀번호로 **전환 페이지**를 직접 사용한다.

- 웹 로그인이 이메일 전용이므로 **신규 가입자도 이메일 계정으로만 웹에 들어온다.** 관리자 승인이 `Id_Logn` 행을 만든 뒤 발급하는 활성화 토큰은 더 이상 `Gpass` 를 쓰지 않고, `/activate/{token}` 이 토큰을 **switchTicket 으로 교환**해 전환 흐름 Step 2(이메일·코드·비밀번호)로 보낸다(identity = 승인 시 만든 행).
- 델파이용 초기 비밀번호는 승인 시 시드(DSN-DEC-10 `임시 평문`)로 관리자가 별도 전달 — 웹과 무관(ACM-INV-2).
- 「기 등록 계정 찾기」(`/activate/lookup`)는 결과 안내를 전환 페이지로 연결하고, 메일 발송은 신설 서비스(ACM-DEC-09)를 쓴다. `id_logn_service.set_password_by_gcode` 의 공개 경로 호출은 제거(ACM-INV-7 강화). ACM-Q-6 종결.

---

## 6. 데이터 모델 (DDL — MySQL 3.23 호환 문법, 기본 서버 `remote_138` · 전용 DB `bukio_web_db`)

> 구현 정본은 `app/services/web_accounts_db.py::ddl_statements()` — 아래와 동일하되 `CREATE DATABASE IF NOT EXISTS \`bukio_web_db\`` 가 앞에 오고 테이블은 `\`bukio_web_db\`.\`Web_Accounts\`` 로 한정된다. `PwPlain` 은 VARCHAR(255)(aesgcm 모드의 봉투 길이 수용).

```sql
CREATE TABLE IF NOT EXISTS Web_Accounts (
  AccountId        VARCHAR(32)  NOT NULL,              -- uuid4 hex
  Email            VARCHAR(120) NOT NULL,              -- 정규화(소문자)
  PwHash           VARCHAR(80)  NOT NULL DEFAULT '',   -- bcrypt (로그인 검증 전용)
  PwPlain          VARCHAR(64)  NOT NULL DEFAULT '',   -- ACM-DEC-05 요구안 (대안: PwEnc TEXT)
  Status           VARCHAR(12)  NOT NULL DEFAULT 'active',  -- active|locked|disabled
  EmailVerifiedAt  VARCHAR(19)  NOT NULL DEFAULT '',   -- 'YYYY-MM-DD HH:MM:SS' UTC
  CreatedAt        VARCHAR(19)  NOT NULL DEFAULT '',
  LastLoginAt      VARCHAR(19)  NOT NULL DEFAULT '',
  FailCount        INT          NOT NULL DEFAULT 0,
  LockedUntil      VARCHAR(19)  NOT NULL DEFAULT '',
  PRIMARY KEY (AccountId),
  UNIQUE ux_web_accounts_email (Email)
);

CREATE TABLE IF NOT EXISTS Web_Account_Links (
  AccountId  VARCHAR(32) NOT NULL,
  ServerId   VARCHAR(32) NOT NULL,                     -- servers.yaml id (remote_138 …)
  DbName     VARCHAR(64) NOT NULL DEFAULT '',          -- 논리 DB (chul_09_db …)
  Hcode      VARCHAR(20) NOT NULL DEFAULT '',
  Gcode      VARCHAR(50) NOT NULL,                     -- 레거시 로그인 ID
  Gname      VARCHAR(50) NOT NULL DEFAULT '',
  Hname      VARCHAR(50) NOT NULL DEFAULT '',          -- 출판사명(표시)
  TenantId   VARCHAR(64) NOT NULL DEFAULT '',
  Label      VARCHAR(80) NOT NULL DEFAULT '',          -- 회사 한글 라벨(소속 선택 표시)
  LinkedAt   VARCHAR(19) NOT NULL DEFAULT '',
  LastSeenAt VARCHAR(19) NOT NULL DEFAULT '',          -- 마지막으로 Id_Logn 행 존재 확인된 로그인
  StaleAt    VARCHAR(19) NOT NULL DEFAULT '',          -- ACCT_LINK_STALE 최초 감지(재연결 시 초기화)
  PRIMARY KEY (ServerId, DbName, Hcode, Gcode),        -- identity 1 = 계정 최대 1 (ACM-DEC-08)
  INDEX ix_web_account_links_acct (AccountId)
);

CREATE TABLE IF NOT EXISTS Web_Account_Codes (
  CodeId     VARCHAR(32)  NOT NULL,
  Email      VARCHAR(120) NOT NULL,
  Purpose    VARCHAR(12)  NOT NULL,                    -- switch|link|reset
  CodeHash   VARCHAR(64)  NOT NULL,                    -- sha256(Salt + code)
  Salt       VARCHAR(32)  NOT NULL,
  TicketId   VARCHAR(32)  NOT NULL DEFAULT '',         -- switch 티켓 jti 바인딩
  ExpiresAt  VARCHAR(19)  NOT NULL,
  Attempts   INT          NOT NULL DEFAULT 0,
  UsedAt     VARCHAR(19)  NOT NULL DEFAULT '',
  SentAt     VARCHAR(19)  NOT NULL,
  ClientIp   VARCHAR(45)  NOT NULL DEFAULT '',
  PRIMARY KEY (CodeId),
  INDEX ix_web_account_codes_email (Email)
);
```

- 시각은 UTC 문자열 — mysql3 raw 프로토콜 경로가 문자열을 돌려주므로 드라이버 무관하게 동일 처리. 문자셋은 서버 기본(`euckr`) — 이메일은 ASCII, 라벨·Hname 은 한글 OK.
- 생성: 첫 호출 시 `ensure_tables()` + 문서화용 `backend/migrations/2026_09_xx_web_accounts.sql`. 서브쿼리·`ON DUPLICATE KEY`·JSON 타입·`CASE WHEN` 미사용(DEC-033).
- 만료 코드 정리: `complete`/`send-code` 시 같은 이메일의 `ExpiresAt < now` 행 DELETE (배치 불필요).

---

## 7. API 설계

### 7.1 공개 엔드포인트 — 라우터 `app/routers/public_account_switch.py` (prefix `/api/v1/public/account-switch`, 인증 없음, `# noqa: hcode-router-coalesce` 사유 주석 — `public_lookup.py` 와 동일)

| Method | Path | 요청 | 200 응답 | 오류 |
|--------|------|------|----------|------|
| POST | `/verify-legacy` | `{tenantId?, hcode?, dbName?, userId, password}` | `{switchTicket, legacy:{label, hname, userId, hcode, serverLabel}}` | 401 동일 메시지 · 409 `ORG_SELECT_REQUIRED{choices}` · 409 `ACCT_ALREADY_SWITCHED` · 429 |
| POST | `/lookup` | `{tenantId?, hcode?, dbName?, userId, password}` | `{found, legacy, account?:{email, linkedAt, lastLoginAt, linkedCount, stale, locked}, switchTicket?}` — **내 계정 찾기**(2026-09-03 사용자 요청): 로그인과 같은 검증만으로 전환된 이메일 계정을 보여주고, 없으면 티켓을 줘 바로 전환으로 잇는다. 기존 `/activate/lookup`(화이트리스트 매칭) 화면을 대체 | 401 · 409 `ORG_SELECT_REQUIRED` · 429 |
| POST | `/send-code` | `{switchTicket, email}` | `{message, mode:"new"\|"link"\|"relink", resendAfterSec:60}` | 410 `ACCT_TICKET_EXPIRED` · 422 `ACCT_EMAIL_INVALID` · 429 `ACCT_CODE_RATE_LIMITED` |
| POST | `/complete` | `{switchTicket, email, code, newPassword?}` (`link`/`relink` 모드는 `newPassword` 생략; `relink` 는 끊어진 링크를 새 identity 로 교체) | `{message, email, linkedCount}` | 400 `ACCT_CODE_INVALID`(불일치·만료 동일) · 423 `ACCT_CODE_LOCKED` · 422 `ACCT_WEAK_PASSWORD` · 409 `ACCT_ALREADY_SWITCHED` · 410 `ACCT_TICKET_EXPIRED` |

### 7.2 로그인 확장 — `POST /api/v1/auth/login` (ACM-DEC-06)

- 요청 스키마 무변경. `userId` 에 `@` → 이메일 경로. 응답 `TokenResponse` 무변경(`user.login_via='email'` 정보 필드 1개 추가).
- 401 `ACCT_LINK_STALE` — 링크가 가리키는 `Id_Logn` 행이 없거나 바뀜(ACM-INV-4). 프론트는 "레거시 계정 정보가 바뀌었습니다" + 재연결 버튼.
- 403 `ACCT_SWITCH_REQUIRED` — `@` 없는 로그인 ID(기본 정책, 웹에만). 프론트는 전환 버튼 강조. `BLS_LEGACY_ID_LOGIN=on`(break-glass) 일 때만 레거시 경로.

### 7.3 선택 엔드포인트 (ACM-DEC-10)

| Method | Path | 용도 |
|--------|------|------|
| POST | `/api/v1/public/account-reset/send-code` · `/complete` | 비밀번호 재설정 (`purpose='reset'`). 미등록 이메일 → 404 `ACCT_EMAIL_NOT_REGISTERED` |
| GET | `/api/v1/me/account` | 내 이메일·링크 목록 |
| POST | `/api/v1/me/account/links` | 로그인 상태에서 추가 연결(레거시 검증만) |
| DELETE | `/api/v1/me/account/links/{linkKey}` | 링크 해제(마지막 1개는 불가) |
| GET/POST | `/api/v1/admin/accounts…` | 수퍼 관리(`admin.user.write`) |

### 7.4 감사 로그

- `audit.auth` 에 action `account_switch.verify` / `.send_code` / `.complete` / `login.email` 을 구조화 JSON 으로 기록: `result`, `reason`(`link_stale`·`relinked` 포함), `email_masked`, `gcode`, `server_id`, `resolved_db`, `client_ip`, `mode`, `linked_count`. `tools/classify_login_audit_logs.py` 에 카테고리 `ACCOUNT_SWITCH_OK/FAIL`, `EMAIL_LOGIN_OK/FAIL`, `SWITCH_REQUIRED` 추가 → 전환율 리포트의 원천.

### 7.5 프론트 API 클라이언트

- `lib/account-switch-api.ts` 신설. `api-client.ts` 의 `ApiErrorCode` 에 `ACCT_*` 코드 추가.
- `auth-context.tsx` 의 `login(userId, password, hints)` 시그니처 무변경 — 로그인 페이지가 이메일을 `userId` 로 넘긴다.

---

## 8. 프론트 설계

| 파일 | 변경 |
|------|------|
| `(public)/login/page.tsx` | 라벨 "이메일", placeholder, 전환 버튼(secondary), `?switched=1` 배너, 회사 선택 콤보 제거(전환 페이지로 이동), 401 `ACCT_LINK_STALE`(재연결 유도) · 403 `ACCT_SWITCH_REQUIRED` 처리 |
| `(public)/account/switch/page.tsx` + `components/account/SwitchWizard.tsx` | 3단계 위저드(§4.1 B), DEC-096 선택 카드 재사용(`OrgChoice` 타입을 `lib/login-org-select.ts` 로 추출해 공유), 딥링크 파라미터 처리, `?mode=relink` 재연결, 완료 화면 "델파이는 그대로" 문구 |
| `(public)/account/reset/page.tsx` (선택) | 재설정 |
| `src/middleware.ts` | `PUBLIC_PATHS` 에 `/account/switch`, `/account/reset` 추가 |
| `lib/account-switch-api.ts`, `lib/api-client.ts` | API·에러 코드 |
| `(app)/settings/my-profile` (선택) | 연결된 회사 계정 섹션 |
| `(app)/admin/id-logn` (선택) | "웹 계정 연결됨" 열(이메일 마스킹) — 회사별 전환 현황 |

- **키보드 흐름**: Enter = 다음 필드(`advanceFocusOnEnter`), 각 단계 마지막 필드 Enter = 제출, 코드 6자리 입력 완료 시 자동 제출, 한글 IME 조합 중 Enter 무시(DEC-097 패턴).
- **디자인**: 토큰만 사용(hex 0건), 화면당 `brand-primary` CTA 1개(전환 페이지는 현재 단계의 주 버튼만), `BrandHero` 재사용, 비밀번호 표시 토글은 활성화 페이지 패턴 복사. 모바일 1열.
- **화면 매트릭스**: 대응 dfm 없음 → `tools/delphi_form_screen_matrix.py` 레지스트리에 `_WebAcct`(WEB_ONLY) 등록, `data-legacy-id` 는 `WebAcct.*` 접두로 부착(테스트 셀렉터 용).
- **검증**: 커밋 전 로컬 dev + Chrome 실화면으로 전환 e2e(콘솔 provider + DEBUG_ECHO)와 이메일 로그인을 확인하고 커밋 메시지에 명기(verify-ui 규칙).

---

## 9. 구현 워크패키지 · 티어 · 테스트

### 9.1 워크패키지 (의존 순서)

| WP | 내용 | 산출물 | 권장 티어 | 사용자 모델 선택 메모 |
|----|------|--------|-----------|------------------------|
| WP-0 | 설계 동결 — `ACM-Q-*` 응답 반영, DEC-235 기록, `migration/contracts/account_switch.yaml`, `login.yaml` 합격선 개정(v2 "웹 = 이메일 계정 로그인", 레거시 ID 웹 로그인 out) | 본 문서 승인본, decisions.md | **고급 권장** (다의성·트레이드오프) | 실행 전 고급 모델 지정 권장 |
| WP-1 | 저장소·코덱 — `web_accounts_db.py`(ensure/CRUD/잠금), `account_secret_codec.py` **구현 완료** (migrations SQL 은 `ddl_statements()` 가 정본) | 백엔드 2 모듈 | 표준 | 기본 |
| WP-2 | 메일 발송 — `email_dispatch_service.py`(console/smtp=Brevo) **구현 완료 2026-09-03** + env·`render.yaml`·점검 스크립트·테스트. 남은 것: 인증코드 템플릿(WP-4 에서), 활성화 안내 연결(ACM-DEC-11) | 서비스 + 템플릿 | 표준 | 기본 |
| WP-3 | 로그인 코어 추출 — `auth_login_core.py`, `/auth/login` 무회귀 리팩터 **구현 완료**(로그인 회귀 70건 PASS) | 서비스 1 + auth.py 축소 | **고급 권장** | 완료 |
| WP-4 | 전환 API — `public_account_switch.py`, `account_switch_service.py`(티켓·코드·링크·재연결), 감사 로그, `Id_Logn` 무쓰기 정적 가드 **구현 완료** | 라우터 + 서비스 | 표준 | 완료 |
| WP-5 | 이메일 로그인 경로 — `/auth/login` 분기, 링크 → `Id_Logn` 행 존재 확인(`load_user_by_identity`) → 클레임 재도출, `ACCT_LINK_STALE`, 잠금, 레거시 ID 플래그 + `login-policy` **구현 완료** | auth.py + auth_service | 표준 | 완료 |
| WP-6 | 프론트 — 로그인 개편, 전환 위저드(`SwitchWizard`), 재설정 페이지, API 클라이언트, DEC-096 공용화(`login-org-select`), middleware **구현 완료**(tsc·build PASS) | 페이지 2 + 컴포넌트 | 표준 | 완료 |
| WP-7 | 회귀·가드 — `test_acm_*` 4파일 46건, 스모크 매트릭스 3건 등록, 계약 `account_switch.yaml`, 트래커 C1 **완료**. 남은 것: 감사 분류기 카테고리(`classify_login_audit_logs`) | test/ + tools/ | 표준 | 대부분 완료 |
| WP-8 | 재설정 **완료**(`/account/reset`). (선택) 내 계정·관리자 화면·`/admin/id-logn` 연결 현황 열 | 페이지 3 + API | 표준 | 기본 |
| WP-9 | 운영 — DKIM, Render env, 공지, 컷오버 D-day 런북(체크리스트·공지·헬프데스크 FAQ), 전환율 리포트 스크립트 | docs 런북 + tools | 표준 | 기본 |

**모델 선택:** 표준 행은 기본·빠른 모델로 진행 가능. 고급 권장 행(WP-0, WP-3)만 사용자가 실행 전에 모델을 바꾸면 된다. 고급 모델을 고르지 않아도 WP-1·2·4·6·7 은 독립적으로 완료 가능하며, WP-3 은 표준 모델로도 진행할 수 있으나 회귀 6종을 반드시 돌린다.

예상 규모(참고): 백엔드 신규 약 1,200줄 · 프론트 신규 약 900줄 · 테스트 약 700줄. 순차 진행 시 표준 티어 기준 3~5 작업일.

### 9.2 회귀 테스트 (hub `test/`, 모두 PASS 가 DoD)

| 파일 | 검증 |
|------|------|
| `test_acm_verify_legacy_reuses_login_core.py` | `/auth/login` 과 `verify-legacy` 가 동일 코어 호출(모킹), 409 챌린지 전달, `ACCT_ALREADY_SWITCHED` |
| `test_acm_code_policy.py` | 해시 저장·TTL·5회 잠금·쿨다운·동일 메시지·이메일 정규화 |
| `test_acm_complete_and_email_login.py` | complete → 계정·링크 행, `PwHash` 검증, 이메일 로그인 JWT 클레임이 레거시 로그인과 동일(`sub`=Gcode, `sid`, `rdb`, `hcode`) |
| `test_acm_link_rules.py` | identity 유니크, `link` 모드, 다중 링크 → `ORG_SELECT_REQUIRED` |
| `test_acm_legacy_login_switch_required.py` | 기본 설정에서 레거시 ID 로그인 403 `ACCT_SWITCH_REQUIRED`(관리자 포함), `BLS_LEGACY_ID_LOGIN=on` 이면 기존 경로 + 감사 `legacy_login_breakglass` |
| `test_acm_activation_absorbed.py` | 활성화 토큰 → switchTicket 교환, 공개 경로에서 `Gpass` 쓰기 0건(ACM-DEC-11) |
| `test_acm_no_secret_in_logs_or_responses.py` | 응답·감사 로그에 코드·비밀번호·`PwPlain` 0건 (secrets-policy) |
| `test_acm_email_dispatch.py` | **구현됨** — provider 선택, smtp 설정 누락 무예외, aiosmtplib.send STARTTLS·자격 호출, 실패 결과화, 로그에 비밀·수신 주소 원문 0건, 기동 경고 |
| `test_acm_delphi_coexistence.py` | **병행 불변식** — 계정 경로에서 `Id_Logn` 쓰기 SQL 0건(정적), stale 링크 fail-closed, `_이름_` 만료 관례 차단, Fxx 변경 다음 로그인 반영, 재연결 후 옛 링크 제거 |
| 기존 | 로그인 회귀 6종(`login-dsn-dec08.mdc`) + `test_dec096_org_select_login.py` + `test_classify_login_audit_logs.py` — 레거시 경로 검증이므로 **`BLS_LEGACY_ID_LOGIN=on` 픽스처**로 실행(코어 무회귀 보존) |

### 9.3 정적 가드·등록

- `debug/probe_backend_all_servers.py` `_routes_for` 에 `public.account_switch.verify_bad_body`(422)·`send_code_bad_ticket`(410) 무인증 스모크 등록.
- `python3 tools/audit_router_hcode_coalesce.py` — 공개 라우터 noqa 사유 주석.
- `python3 tools/delphi_form_screen_matrix.py --check` — `_WebAcct` WEB_ONLY 등록 후 PASS.
- `rg '#[0-9a-fA-F]{6}\b' 도서물류관리프로그램/frontend/src` — 신규 TSX 0건.
- `tsc --noEmit` + `next build` PASS.

---

## 10. 위험 · 사용자 결정 필요 항목

### 10.1 위험 (`ACM-RISK-*`)

| ID | 위험 | 완화 |
|----|------|------|
| `ACM-RISK-01` | **평문 비밀번호 보관** — DB 덤프·백업·SSH 계정 유출 시 전 계정 노출, 사용자가 타 서비스와 같은 비밀번호를 쓸 가능성 | `ACM-Q-1` 암호화 대안, 접근 최소화(전용 DB 계정 권장), 응답·로그 0건 가드, Phase 3 컬럼 폐기 |
| `ACM-RISK-02` | 계정 저장소(remote_138) 단일 지점 장애 시 이메일 로그인 불가 | 비상 시 `BLS_LEGACY_ID_LOGIN=on`(break-glass)으로 임시 복구 + 복원 포인트, 야간 덤프 백업(RED 절차), 저장소 서버 env 로 이동 가능 |
| `ACM-RISK-03` | 메일 미도달(스팸·DKIM 미설정) | 발신 도메인 인증 필수, 운영에서 `console` provider 금지(기동 경고), 재발송 + 관리자 코드 조회(감사 기록) |
| `ACM-RISK-04` | Render 무료 플랜 콜드스타트(첫 요청 50초+) | 프론트 대기 문구·타임아웃 60초, 코드 TTL 10분은 여유 |
| `ACM-RISK-05` | 공용 ID 관행(총무부·영업부 등, 인덱스 동명 27%) — 한 이메일을 여러 사람이 공유 | "이메일 1개 = 계정 1개" 안내, 공용 메일이면 다중 링크로 흡수, 향후 개인 이메일 전환 유도 |
| `ACM-RISK-06` | 델파이 병행 사용자가 `Id_Logn.Gpass` 를 바꿔도 웹 비밀번호는 별개 | 전환 완료 화면·메일에 "웹 비밀번호는 별도" 명시, Phase 3 까지 공존 |
| `ACM-RISK-07` | 저장소를 MySQL 3.23 서버로 옮길 때 DDL 호환 | 서브쿼리·JSON·CASE 미사용, VARCHAR 시각, `sql_mysql3` 헬퍼 준수 |
| `ACM-RISK-08` | 이메일 열거 | `send-code` 응답 동일화, `mode` 는 유효 티켓 보유자(레거시 검증 통과자)에게만 |
| `ACM-RISK-09` | 로그인 코어 추출 중 회귀 | WP-3 를 별 커밋으로 분리, 회귀 6종 + DEC-096 테스트 게이트, `/auth/login` 응답 스냅샷 비교 |
| `ACM-RISK-10` | **링크 drift** — 델파이 Sobo10 에서 Gcode 변경·만료 잠금(`_이름_`)·행 삭제로 링크가 끊김 | 매 로그인 존재 확인 + fail-closed `ACCT_LINK_STALE`(ACM-INV-4), 재연결 모드(ACM-INV-5), 관리자 현황 열 |
| `ACM-RISK-11` | 두 비밀번호(델파이·웹) 혼동 — 사용자가 한쪽을 바꾸고 다른 쪽이 안 바뀐다고 문의 | 완료 화면·메일·재설정 화면 문구 고정(ACM-INV-2), 로그인 공지, 헬프데스크 FAQ |
| `ACM-RISK-16` | **미인증 발신 도메인 → 조용한 전달 실패** — Brevo 는 미인증 발신자 메일도 SMTP 250 `queued as ...` 로 접수한 뒤 차단한다. 실제 발생(2026-09-03): `newoneseek@buk.io` 는 NXDOMAIN, `bukio.com` 은 타인 소유 파킹 도메인 | 발신 도메인은 보유·DNS 관리 가능한 것만 사용(`newoneseek@buk.io`). `debug/send_test_email.py --check` 가 발신 도메인 NS/A·MX·SPF 를 검사해 NXDOMAIN 이면 종료 코드 1. Brevo 발신자/도메인 인증 완료를 Phase 0 게이트로 |
| `ACM-RISK-15` | **회사 미선택 시 후보 스윕 지연** — 운영 실측 89초(후보 39개 순차 조회)로 프론트 30초 타임아웃 초과 → "서버 응답 초과" 오류 | `BLS_LOGIN_SWEEP_BUDGET_SEC`(기본 20초) 예산 — 추측 후보만 대상, 인덱스/테넌트 유래 고신뢰 후보는 무제한. 예산 소진 시 409 `ACCT_ORG_HINT_REQUIRED` 로 회사 선택 요청. 계정 계열 프론트 타임아웃 150초 + 진행 안내 |
| `ACM-RISK-14` | **Brevo 무료 티어 일 300통** — 컷오버 주간 전환·재발송 폭주 시 한도 초과 → 발송 거부 | 선공개 기간으로 분산, 재발송 쿨다운(ACM-DEC-04), 발송 실패 시 "잠시 후 재시도" 안내 + 감사 로그 카운트 알람, 초과 지속 시 Brevo 유료 플랜 또는 2차 provider |
| `ACM-RISK-13` | **컷오버 D-day 웹 잠금** — 미전환 사용자는 전환 전까지 웹 사용 불가(델파이는 가능) | Phase 1 선공개 기간, 공지 3회(로그인 배너·메일·헬프데스크), 전환 페이지 상시 운영, 관리자 초대 메일(선택) |
| `ACM-RISK-12` | 웹 관리 화면(`/admin/id-logn`·가입 승인)이 `Id_Logn` 을 쓰는 기존 경로와 본 기능의 무쓰기 원칙 혼재 | 무쓰기 원칙은 **계정 전환·이메일 로그인 경로에 한정**(ACM-INV-1 범위 명시). 기존 관리 경로는 C10 정책(델파이 호환 UPDATE 패턴) 그대로 |

### 10.2 사용자 결정 필요 (`ACM-Q-*`) — 답이 없으면 괄호의 기본안으로 진행

| ID | 질문 | 선택지 (기본안) |
|----|------|------|
| `ACM-Q-1` | 비밀번호 보관 방식 | (a) 요구 원문대로 평문 `PwPlain` + `PwHash` 병행 **(기본안)** / (b) AES-GCM 암호화 `PwEnc` + `PwHash` — 권장 |
| `ACM-Q-2` | ~~웹의 레거시 ID 로그인 병행 기간~~ → **결정(2026-09-03)**: 웹은 이메일 계정 전용, 병행 없음. 남은 결정: 선공개 기간 길이 | 기본안: Phase 1 선공개 2주 후 컷오버 |
| `ACM-Q-3` | 메일 제공자·발신 주소 | **결정(2026-09-03)**: Brevo SMTP 무료 티어(`smtp-relay.brevo.com:587`). 발신 주소 = `newoneseek@buk.io`(2026-09-03 확정 — Brevo 발신자/도메인 인증 필요). **발신 도메인은 실제 보유·DNS 관리 가능한 도메인이어야 한다**: 미등록 도메인(`bukio.works` NXDOMAIN)이나 타인 소유 파킹 도메인(`bukio.com`)은 Brevo 가 SMTP 접수(250 queued)만 하고 전달을 차단한다 — `ACM-RISK-16` |
| `ACM-Q-4` | 비밀번호 재설정 화면 | **결정**: 포함, 컷오버 전 필수(ACM-DEC-10) |
| `ACM-Q-5` | 한 이메일에 여러 회사 계정 연결 허용 | 기본안: 허용(로그인 시 소속 선택) |
| `ACM-Q-6` | 기존 「기 등록 계정 찾기」(활성화) 링크 | **결정**: 전환 흐름에 흡수(ACM-DEC-11) |
| `ACM-Q-7` | 계정 저장소 서버 | 기본안: `remote_138` (MySQL 5.1 직결) |
| `ACM-Q-8` | 웹에서 레거시 ID 로그인 영구 병행 여부 | **결정(2026-09-03)**: 병행 없음 — 웹은 이메일 계정 전용, 비상 복구 플래그만 |

---

## 11. 수용 기준 (DoD)

- [ ] 테스트 계정 1건이 `/account/switch` 3단계를 실메일로 완주하고 `/login` 에서 이메일로 로그인해 기존 화면(거래명세서 등)을 동일 권한으로 조회한다.
- [ ] 이메일 로그인 JWT 의 `sub`/`sid`/`rdb`/`hcode`/`fxx_caps` 가 같은 계정의 레거시 ID 로그인과 동일하다(테스트 `test_acm_complete_and_email_login.py`).
- [ ] `/auth/login` 레거시 경로 응답·감사 로그가 리팩터 전과 동일(로그인 회귀 6종 + DEC-096 PASS).
- [ ] 응답·로그·엑셀 어디에도 인증코드·비밀번호·`PwPlain` 이 나타나지 않는다(테스트 + `rg` 가드).
- [ ] Render 재배포 후에도 전환된 계정으로 로그인된다(사이드테이블 영속 확인).
- [ ] 기본 설정(`BLS_LEGACY_ID_LOGIN` 미설정)에서 레거시 ID 로 웹 로그인 시 403 `ACCT_SWITCH_REQUIRED`, 활성화 토큰 경로에서 `Gpass` 쓰기 0건.
- [ ] **병행**: 전환 전후 해당 `Id_Logn` 행 diff 0건, 델파이와 동일한 SQL(`Gcode+Gname+Gpass`)로 로그인이 계속 성공한다. 델파이에서 Fxx 를 바꾸면 다음 웹 로그인에 반영되고, Gcode 를 바꾸면 웹은 `ACCT_LINK_STALE` 후 재연결로 복구된다.
- [ ] `tsc --noEmit`, `next build`, hub `pytest -q`, `audit_router_hcode_coalesce`, `delphi_form_screen_matrix --check`, hex 가드 모두 PASS.
- [ ] `dashboard/data/porting-screens.json` C1 의 `web.routes/endpoints` 에 신규 라우트·API 반영, `analysis/audit/incomplete-features-inventory` 갱신.
- [ ] DEC-235 기록 + `migration/contracts/account_switch.yaml` approved.
