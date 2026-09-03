# 복원 포인트 — 이메일 기준 북이오웍스 계정 전환 착수 전 (2026-09-03)

| 항목 | 내용 |
|------|------|
| 생성일 | 2026-09-03 (UTC 02:30 DB 캡처) |
| 목적 | 이메일 기준 신규 계정 전환(ACM / DEC-235 후보, [decision-bukioworks-account-migration.md](decision-bukioworks-account-migration.md)) **착수 전** 상태로 되돌릴 수 있는 기준점 |
| 태그 | `restore-pre-email-account-2026-09-03` — 제품·허브 두 저장소 동명 (원격 푸시 완료) |
| DB 기준선 | [`analysis/audit/restore-point-pre-email-account-2026-09-03.json`](../analysis/audit/restore-point-pre-email-account-2026-09-03.json) (비밀 0건) |
| 도구 | `tools/restore_point_db_baseline.py` (캡처 · `--compare` 대조) |
| 비밀 정책 | 본 문서·JSON 에 자격증명·Gpass 0건 (secrets-policy G3) |

## 1. 캡처된 상태

| 대상 | 값 |
|------|----|
| 제품 저장소 `도서물류관리프로그램/` (remote `private` = speeno/books-logistics-web) | `main` = `private/main` = **`6a913d3`** (DEC-233 보강). 태그 `restore-pre-email-account-2026-09-03` → 6a913d3 |
| 제품 저장소 미커밋 | `.run/logs/*.log`(런타임 로그) · `backend/data/login_id_index.json`(로그인 인덱스 자동 갱신) — 복원 대상 아님 |
| 허브 저장소 (remote `origin` = speeno/Delphi_portin_project) | `master` = **`ee04c67`** (DEC-235 후보 보강본). 태그 동명 → ee04c67 |
| 허브 미커밋 | `analysis/audit/*.json`·`docs/delphi-form-screen-equivalence-matrix.md`·`test/_artifacts_c15_*` (자동 생성물) + 미추적 PDF 1건 — 본 작업과 무관, 복원 대상 아님 |
| 프론트 배포 (Vercel, `books-logistics-web`) | 6a913d3 상태 **success** — [deployment](https://vercel.com/mudotmusic-6437s-projects/books-logistics-web/Hntm7ADMdxYxrdC1comFh5o1wkyW) |
| 백엔드 배포 (Render, `books-logistics-web`, autoDeploy main) | 6a913d3 기준 (CLI 워크스페이스가 달라 대시보드로만 확인 가능) |
| DB `remote_138` (MySQL 5.1.73) | Id_Logn 보유 DB **18개**, Id_Logn 합계 **2,117행**. `Web_Account*` 테이블 **0개**. 기존 `Web_*` 사이드테이블은 `book_kb_db`·`chul_09_db` 에만(`Web_Grid_Prefs`·`Web_Print_Assets`·`Web_User_Prefs`) |
| DB `remote_153/154/155` | 미캡처(SSH 터널 필요). 계정 저장소는 remote_138 만 쓰고 Id_Logn 은 어느 서버도 쓰지 않으므로(ACM-INV-1) 변화 대상 아님. 필요 시 `--server remote_153` 으로 추가 캡처 |

## 2. 복원 절차

### 2.1 코드 (제품 저장소)

```bash
cd 도서물류관리프로그램
git fetch private --tags
git checkout -b restore/pre-email-account restore-pre-email-account-2026-09-03   # 검토용 브랜치
# main 을 되돌려 재배포하려면 (팀 합의 후):
git checkout main && git reset --hard restore-pre-email-account-2026-09-03 && git push --force-with-lease private main
```

- `main` 푸시 = Vercel(프론트)·Render(백엔드) 자동 재배포. 강제 푸시 대신 **revert 커밋**(`git revert <전환 커밋 범위>`)이 이력 보존 면에서 우선이다.
- 즉시 롤백만 필요하면 Vercel 대시보드에서 위 deployment 를 **Promote to Production**, Render 는 6a913d3 을 **Manual Deploy → 특정 커밋** 으로 재배포.

### 2.2 코드 (허브 저장소)

```bash
git fetch origin --tags
git checkout -b restore/pre-email-account restore-pre-email-account-2026-09-03
```
테스트(`test/test_acm_*.py`)·도구·계약(`migration/contracts/account_switch.yaml`)이 전환 작업으로 추가된 것들이므로, 되돌릴 때 함께 제거되는지 확인.

### 2.3 환경 변수 (Render / 로컬 `.env`)

전환 작업이 추가하는 변수 — 복원 시 **삭제**: `BLS_EMAIL_PROVIDER` · `BLS_EMAIL_API_KEY` · `BLS_EMAIL_FROM` · `BLS_EMAIL_REPLY_TO` · `BLS_PUBLIC_BASE_URL` · `BLS_ACCOUNT_STORE_SERVER_ID` · `BLS_ACCOUNT_PW_KEY` · `BLS_ACCOUNT_CODE_TTL_MIN` · `BLS_LEGACY_ID_LOGIN`. 기존 변수(`BLS_JWT_SECRET`·`BLS_SERVERS_YAML_B64`·`BLS_CORS_ORIGINS` 등)는 건드리지 않는다.

### 2.4 DB (`remote_138`)

전환 작업이 만드는 것은 사이드테이블 3종뿐이며 **`Id_Logn` 은 쓰지 않는다**(ACM-INV-1). 복원 = 사이드테이블 제거.

```sql
-- 필요 시 먼저 보존: CREATE TABLE Web_Accounts_bak_YYYYMMDD SELECT * FROM Web_Accounts; (비밀 포함 — RED 취급)
DROP TABLE IF EXISTS Web_Account_Codes;
DROP TABLE IF EXISTS Web_Account_Links;
DROP TABLE IF EXISTS Web_Accounts;
```

검증 — 기준선과 대조(차이 0건이면 exit 0):

```bash
python3 tools/restore_point_db_baseline.py --compare analysis/audit/restore-point-pre-email-account-2026-09-03.json
```

`Id_Logn` 행수가 기준선과 다르면 그 차이는 **델파이 쪽 정상 운영(사용자 추가·삭제)** 일 수 있다 — 전환 코드 경로의 쓰기가 아님을 `test_acm_delphi_coexistence.py` 정적 가드와 감사 로그로 확인한다. Id_Logn 전체 내용(비밀 포함) 스냅샷이 별도로 필요하면 [operating-account-credentials-red.md](operating-account-credentials-red.md) 절차대로 `tools/export_id_logn_credentials_red.py` 를 사용하고 산출물은 `WeLove_FTP/`(gitignored) 밖으로 내보내지 않는다.

### 2.5 프론트 사용자 데이터

전환 작업은 브라우저 `localStorage` 에 새 키를 두지 않는다(티켓·이메일은 `sessionStorage` 일회성). 기존 `bls_org_pref:*`·토큰 키는 무변경.

## 3. 복원 후 확인

- [ ] `/login` 이 기존 로그인 ID + 회사 선택 콤보 화면으로 돌아옴, 테스트 계정 로그인 성공.
- [ ] `python -m pytest -q` (허브) PASS, 로그인 회귀 6종 PASS.
- [ ] `tools/restore_point_db_baseline.py --compare …` → `[OK]` 또는 차이가 델파이 운영분으로 설명됨.
- [ ] Render 환경 변수에 `BLS_EMAIL_*`·`BLS_ACCOUNT_*`·`BLS_LEGACY_ID_LOGIN` 없음.
