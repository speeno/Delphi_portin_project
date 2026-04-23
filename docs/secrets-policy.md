# 인수인계·운영 자격증명 취급 정책 (`SECRETS-POLICY`)

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-23 |
| 추적 ID | `SEC-POL-*` (정책 행), `SEC-AUD-*` (감사 항목) |
| 단일 원천 | 본 문서. `G3 — 민감 정보 금지` 의 운영 절차서 본문. |
| 정합 | [`docs/manual-catalog.md`](manual-catalog.md) §6, [`docs/decision-login-db-routing.md`](decision-login-db-routing.md), [`harness-architecture.md`](../harness-architecture.md) L1 |
| 강제 시점 | 본 정책은 **즉시 발효** — 미준수 PR 은 머지 차단. |

---

## 1. 한 줄 요약

- **레포에는 자격증명 평문이 0건.** 자격증명·root 토큰·실 계정 비번을 포함한 자산은 메타만 카탈로그하고 원본은 작업자 PC 한정 보존.
- **환경 변수 + 외부 vault** 가 운영 단일 주입 채널.
- **회의·PR·이슈·로그** 의 본문에서도 평문 인용 금지 — 마스킹된 메타만 허용.
- 위반 발견 시 **즉시 git history 재작성 + 자격증명 회전** 절차(§6)를 따른다.

---

## 2. 자산 분류 (`SEC-POL-CLASS-*`)

| 등급 | 정의 | 예시 자산 | 본 카탈로그 표기 |
|------|------|---|:-:|
| `SEC-POL-CLASS-RED` | DB 비번 / root / API 토큰 / 외부 콘솔 자격증명 — **유출 시 즉시 회전 필요** | `MAN-008` DB.txt, `MAN-012/013/014` (FTP·콘솔), `MAN-017/018` 엑셀의 user/password 컬럼 | **○** |
| `SEC-POL-CLASS-AMBER` | 개인정보(연락처·실명·주소) — **마스킹 후 인용 가능** | `MAN-020` 위러브 출판사 연락처 | **△** |
| `SEC-POL-CLASS-GREEN` | 일반 매뉴얼·스크린샷 비주얼·정책 문서 | `MAN-001`~`MAN-007`, `MAN-010`, `MAN-015`, `MAN-016`, `MAN-030`~`MAN-032` | **×** |

---

## 3. 저장·이동 정책 (`SEC-POL-STORAGE-*`)

| ID | 자산 등급 | 허용 저장 위치 | 금지 저장 위치 |
|----|---|---|---|
| `SEC-POL-STORAGE-01` | RED | (1) 작업자 PC `WeLove_FTP/...` (gitignored), (2) 운영 vault, (3) CI/CD secret store | git 추적 파일·이슈·PR·로그·캡처·대시보드·테스트 fixture |
| `SEC-POL-STORAGE-02` | AMBER | git 추적 가능하되 **평문 인용 금지** — 이름·번호 마스킹 후 사용 | 평문 인용된 PR/이슈 |
| `SEC-POL-STORAGE-03` | GREEN | 자유 — 단, 화면 캡처에 RED/AMBER 데이터가 보이지 않도록 사전 검토 | — |
| `SEC-POL-STORAGE-04` | 모든 등급 | 백업/이메일 첨부 시 사내 정책에 따른 보관 기간 | 외부 클라우드 (개인 Google Drive·Dropbox 등) |

`.gitignore` 강제 패턴(권장):

```
# 자격증명 포함 자산 (RED)
WeLove_FTP/Welove_인수인계/메뉴얼/DB.txt
WeLove_FTP/Welove_인수인계/셋팅방법/DB_ftp.txt
WeLove_FTP/Welove_인수인계/셋팅방법/로그인정보.txt
WeLove_FTP/Welove_인수인계/셋팅방법/스마일서브 리부팅.txt
WeLove_FTP/Welove_인수인계/셋팅방법/DB정보, DB_FTP 엑셀/DB정보 엑셀정리.xlsx
WeLove_FTP/Welove_인수인계/셋팅방법/DB정보, DB_FTP 엑셀/DB_FTP 엑셀정리.xlsx
```

> 본 사이클은 정책 정의에 한한다. 실 `.gitignore` 갱신은 별 PR — 기존 커밋에 포함되어 있을 가능성이 있으므로 §6 회전 절차와 병행 검토.

---

## 4. 환경별 주입 (`SEC-POL-INJECT-*`)

| ID | 환경 | 주입 채널 | 비고 |
|----|---|---|---|
| `SEC-POL-INJECT-01` | 개발자 로컬 | `.env.local` (git 미추적) + `direnv` | 템플릿 `.env.example` 만 git 추적, **값 없음**. |
| `SEC-POL-INJECT-02` | CI/CD | repo secret (예: GitHub Actions encrypted secrets) | secret 이름은 `BLS_*_USER`, `BLS_*_PASSWORD` 표준화. |
| `SEC-POL-INJECT-03` | 스테이징/프로덕션 | 외부 vault (예: HashiCorp Vault, AWS Secrets Manager) → 컨테이너 startup 시 환경변수 주입 | 비번 회전 ≤ 90일 권장. |
| `SEC-POL-INJECT-04` | DB 마이그레이션 도구 | 일회성 운영자 세션에서 vault → 도구 stdin / env | 스크립트 인자 `--password=...` 금지. |

표준 환경변수 (DSN 라우팅과 정합):

| 환경변수 | 의미 |
|---|---|
| `BLS_AUTH_SERVER_ID` | 인증 서버 식별자 (DEC-051) |
| `BLS_DB__<server_id>__USER` | 서버별 DB 사용자 |
| `BLS_DB__<server_id>__PASSWORD` | 서버별 DB 비번 |
| `BLS_VAULT_ENDPOINT` | (옵션) vault 엔드포인트 |

---

## 5. 인용·로깅 정책 (`SEC-POL-CITE-*`)

| ID | 항목 | 허용 | 금지 |
|----|---|---|---|
| `SEC-POL-CITE-01` | RED 자산을 PR/이슈 본문에서 다루기 | 메타(서버 ID, 컬럼명, 영향 범위) | 사용자명·비번·토큰의 평문 |
| `SEC-POL-CITE-02` | AMBER 자산을 인용 | 마스킹된 형태 (`010-****-1234`, `홍**`) | 원문 |
| `SEC-POL-CITE-03` | 로깅 (애플리케이션·하네스·CI) | 사용자 ID, 액션, 결과 코드 | 비번, 토큰, 임시 비번, 이메일 본문 |
| `SEC-POL-CITE-04` | 비번 reset 결과 응답 | `temp_password` 1회 반환 후 즉시 폐기, 로그 미적재 | 로그/audit 본문에 평문 적재 |
| `SEC-POL-CITE-05` | 화면 캡처/녹화 | RED/AMBER 영역 마스킹 후 첨부 | 그대로 첨부 |

---

## 6. 위반 대응 (`SEC-POL-INC-*`)

위반(평문 자격증명 git 커밋, 로그 평문 적재, PR 본문 인용 등) 발견 시:

1. **즉시 보고** — Slack `#sec-incidents` 또는 운영 책임자에게 1회.
2. **자격증명 회전** — 노출된 모든 자격증명을 24시간 내 회전. vault 갱신 + 재배포.
3. **git history 재작성** — `git filter-repo --replace-text` 또는 `git filter-branch` 로 평문 제거 후 force push (모든 작업자 재 clone 안내).
4. **사후 분석** — 본 정책 §3~§5 위반 원인 + 재발 방지 가드(`pre-commit hook`·`gitleaks` 등) 도입.
5. **추적** — 본 사고를 `legacy-analysis/decisions.md` 의 보안 사고 로그에 1행 추가.

---

## 7. 자동 가드 (다음 사이클 후보)

| 도구 | 역할 |
|------|------|
| `gitleaks` (pre-commit) | DB.txt / 로그인정보.txt 패턴 + 정규식(`(?i)(password|passwd|root|user)\\s*[:=]`) 차단. |
| `tools/secrets/scan.py` | 본 카탈로그(`manual-catalog.md`)에 ○ 표기된 파일이 git index 에 추가되면 차단. |
| CI step `secret-scan` | PR diff 에서 비번 패턴 검출 시 fail. |

본 사이클은 **정책 동결만**, 자동 가드 도입은 별 PR.

---

## 8. 수용 기준

- ✅ 본 문서가 [`docs/manual-catalog.md`](manual-catalog.md) §6, [`docs/decision-login-db-routing.md`](decision-login-db-routing.md), [`harness-architecture.md`](../harness-architecture.md) L1, [`harness_runbook.md`](harness_runbook.md) §6 에서 인용됨.
- ✅ §3 의 `.gitignore` 패턴이 다음 사이클에 실제 `.gitignore` 로 반영.
- ✅ §4 의 환경변수 표준이 [`backend/app/core/config.py`](../도서물류관리프로그램/backend/app/core/config.py) 와 정합.
- ✅ 운영 vault 가 구축되면 §6 의 회전 절차가 1회 dry-run 으로 검증됨.
