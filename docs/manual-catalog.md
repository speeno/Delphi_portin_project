# Welove 인수인계 매뉴얼·자산 메타 카탈로그 (`MAN-*`)

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-23 |
| 추적 ID 접두사 | `MAN-*` (메뉴얼/자산 단위), `MAN-CH-*` (채널), `MAN-TPC-*` (주제) |
| 대상 폴더 | [`WeLove_FTP/Welove_인수인계/`](../WeLove_FTP/Welove_인수인계) 직속 텍스트·문서 자산 |
| 단일 원천 | 본 문서. 채널/주제 분류는 §2~§4, 자산별 추적표는 §5. |
| 비밀 처리 | §6 — DB.txt·로그인정보.txt 등 **계정·암호 포함 자산은 본 카탈로그에 메타만 보존**, 원본 텍스트는 인용 금지(SECRETS-POLICY 준수). |

본 카탈로그는 [`harness-architecture.md`](../harness-architecture.md) **L1(자산 수집)** 의 표준 입력으로 합류한다.
포팅 검증은 5축([`docs/eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md)) 중 **기능·UX·감사**에 영향 — 「레거시 사용자가 어떤 절차로 어떤 화면을 썼는지」 정본 근거.

---

## 1. 채널·주제 태깅 정의

### 1.1 채널 (`MAN-CH-*`)

| 채널 ID | 정의 | 동등성 대상 |
|---------|------|-------------|
| `MAN-CH-DESKTOP` | 데스크톱 델파이 클라이언트 (Chulpan/Project1.exe 류) | 웹 SPA(Next.js) `(app)/...` 라우트 |
| `MAN-CH-MOBILE-WEB` | 모바일 웹 (`m.websend.kr/*`) | 웹 SPA 모바일 뷰 + 동일 API |
| `MAN-CH-MOBILE-AUTHOR` | 저자 전용 모바일 (`m.websend.kr/author`) | 미정(P3 — 저자 페이지 별도 검토) |
| `MAN-CH-DISTRIBUTOR-WEB` | 총판 측 모바일/웹 (`m.websend.kr/one`) | 총판 운영 콘솔 (T2 권한) |
| `MAN-CH-INFRA` | DB·서버 셋팅 / 호스팅 / 리부팅 | 운영 런북·인프라(IAC) — 포팅 직접 대상 아님 |

### 1.2 주제 (`MAN-TPC-*`)

| 주제 ID | 의미 | 5축 1차 영향 |
|--------|------|---------------|
| `MAN-TPC-LOGIN` | 로그인·계정·암호 안내 | 기능·감사 |
| `MAN-TPC-ONBOARDING` | 신규 출판사·총판 가입·셋팅 | 기능·UX·감사 |
| `MAN-TPC-OPS` | 일상 업무 절차(거래명세서·출고·반품 등) | 기능·UX |
| `MAN-TPC-PRINT` | 인쇄·라벨·송장 | 기능·UX·성능 |
| `MAN-TPC-INFRA` | 서버·DB·FTP·리부팅 | 운영(포팅 외) |
| `MAN-TPC-PRICING` | 요금·플랜 | 기능 외(영업 정책) |
| `MAN-TPC-SCHEMA` | 테이블 구조·필드 정의 | 데이터 — `SCH-*` 와 합류 |

---

## 2. 메뉴얼 폴더 (`Welove_인수인계/메뉴얼`)

| 추적 ID | 자산 | 채널 | 주제 | 비밀? | 비고 |
|---|---|---|---|:-:|---|
| `MAN-001` | [`Chulpan사용법.ppt`](../WeLove_FTP/Welove_인수인계/메뉴얼/Chulpan사용법.ppt) | `MAN-CH-DESKTOP` | `MAN-TPC-OPS` | × | 출판 클라이언트 데스크톱 사용 흐름. 변환 필요(텍스트 추출은 다음 사이클). |
| `MAN-002` | [`최강물류 프로그램 매뉴얼.pdf`](../WeLove_FTP/Welove_인수인계/메뉴얼/최강물류%20프로그램%20매뉴얼.pdf) (+ [매뉴얼 폴더](../WeLove_FTP/Welove_인수인계/메뉴얼/최강물류%20프로그램%20매뉴얼/)) | `MAN-CH-DESKTOP` | `MAN-TPC-OPS` | × | 총판(물류) 데스크톱. 부속 `최강물류택배폼.xlsx`·`프로그램 모바일 사용법.xlsx` 동봉. |
| `MAN-003` | [`출판메뉴얼.xlsx`](../WeLove_FTP/Welove_인수인계/메뉴얼/출판메뉴얼.xlsx) | `MAN-CH-DESKTOP` | `MAN-TPC-OPS` | × | 출판 클라이언트 폼별 화면 메뉴얼(엑셀 표 형식). |
| `MAN-004` | [`모바일 사용법.txt`](../WeLove_FTP/Welove_인수인계/메뉴얼/모바일%20사용법.txt) | `MAN-CH-MOBILE-WEB` | `MAN-TPC-LOGIN` | × | `m.websend.kr` 접속·로그인(출판사·ID·PW). |
| `MAN-005` | [`모바일 거래명세서 사용법.txt`](../WeLove_FTP/Welove_인수인계/메뉴얼/모바일%20거래명세서%20사용법.txt) | `MAN-CH-MOBILE-WEB` | `MAN-TPC-OPS` | × | 거래처 검색 → 도서 추가 → 접수 흐름(10단계). |
| `MAN-006` | [`저자 전용 모바일 페이지..txt`](../WeLove_FTP/Welove_인수인계/메뉴얼/저자%20전용%20모바일%20페이지..txt) | `MAN-CH-MOBILE-AUTHOR` | `MAN-TPC-OPS` | × | URL 안내 1줄 (`m.websend.kr/author`). |
| `MAN-007` | [`지이엠코리아 총판측 이용사이트.txt`](../WeLove_FTP/Welove_인수인계/메뉴얼/지이엠코리아%20총판측%20이용사이트.txt) | `MAN-CH-DISTRIBUTOR-WEB` | `MAN-TPC-OPS` | × | URL 안내 1줄 (`m.websend.kr/one/`). |
| `MAN-008` | [`DB.txt`](../WeLove_FTP/Welove_인수인계/메뉴얼/DB.txt) | `MAN-CH-INFRA` | `MAN-TPC-INFRA` | **○** | **계정·암호·root 비밀번호 포함**. 본 카탈로그에는 「서버 4개·계정 약 30~40 row」 메타만 기록, 원문 인용·재배포 금지. DSN 메타 추출은 [`analysis/welove_db_route_matrix.json`](../analysis/welove_db_route_matrix.json) 가 정본. |

## 3. 셋팅방법 (`Welove_인수인계/셋팅방법`)

| 추적 ID | 자산 | 채널 | 주제 | 비밀? | 비고 |
|---|---|---|---|:-:|---|
| `MAN-010` | [`출판사프로그램 PC 셋팅.pdf`](../WeLove_FTP/Welove_인수인계/셋팅방법/출판사프로그램%20PC%20셋팅.pdf) (+ `.hwp`) | `MAN-CH-DESKTOP` | `MAN-TPC-ONBOARDING` | × | 출판사 PC 셋팅 절차 — **레거시 「출판사명/코드 사전 등록」 가정의 1차 출처**. `field-interview-2026-04-23.md` FI-01 과 정합. |
| `MAN-011` | [`DB서버 정보 현황 및 모바일 서비스.hwp`](../WeLove_FTP/Welove_인수인계/셋팅방법/DB서버%20정보%20현황%20및%20모바일%20서비스.hwp) | `MAN-CH-INFRA` | `MAN-TPC-INFRA` | △ | 서버·도메인 정보 포함 가능 — 본문 인용 시 마스킹 필요. |
| `MAN-012` | [`DB_ftp.txt`](../WeLove_FTP/Welove_인수인계/셋팅방법/DB_ftp.txt) | `MAN-CH-INFRA` | `MAN-TPC-INFRA` | **○** | FTP 계정·고객사별 디렉토리 매핑. 메타만 추출 → DSN 라우팅에 합류. |
| `MAN-013` | [`로그인정보.txt`](../WeLove_FTP/Welove_인수인계/셋팅방법/로그인정보.txt) | `MAN-CH-INFRA` | `MAN-TPC-INFRA` | **○** | 가비아·스마일서브·헬프유 등 외부 콘솔 자격증명. 운영 vault 이전 후 본 파일은 폐기 후보. |
| `MAN-014` | [`스마일서브 리부팅.txt`](../WeLove_FTP/Welove_인수인계/셋팅방법/스마일서브%20리부팅.txt) | `MAN-CH-INFRA` | `MAN-TPC-INFRA` | **○** | 호스팅 콘솔 ID/PW. 운영 런북 이전. |
| `MAN-015` | [`※구버젼 설치방법.hwp`](../WeLove_FTP/Welove_인수인계/셋팅방법/※구버젼%20설치방법.hwp) | `MAN-CH-DESKTOP` | `MAN-TPC-ONBOARDING` | × | 구버전 설치 — 웹 전환 시 미사용. |
| `MAN-016` | [`※더북 물류사를 이용하는 출판사는 물류프로그램을 따로 설치.hwp`](../WeLove_FTP/Welove_인수인계/셋팅방법/※더북%20물류사를%20이용하는%20출판사는%20물류프로그램을%20따로%20설치.hwp) | `MAN-CH-DESKTOP` | `MAN-TPC-ONBOARDING` | × | **총판 소속 출판사**가 별도 클라이언트를 설치하던 정책 — 웹 가입 분기(ONB-SUBPUB) 의 직접 근거. |
| `MAN-017` | [`DB정보 엑셀정리.xlsx`](../WeLove_FTP/Welove_인수인계/셋팅방법/DB정보,%20DB_FTP%20엑셀/DB정보%20엑셀정리.xlsx) | `MAN-CH-INFRA` | `MAN-TPC-INFRA` | **○** | 계정 → 서버/DB 매핑 표. 메타만 [`analysis/welove_db_route_matrix.json`](../analysis/welove_db_route_matrix.json) 으로 분리. |
| `MAN-018` | [`DB_FTP 엑셀정리.xlsx`](../WeLove_FTP/Welove_인수인계/셋팅방법/DB정보,%20DB_FTP%20엑셀/DB_FTP%20엑셀정리.xlsx) | `MAN-CH-INFRA` | `MAN-TPC-INFRA` | **○** | FTP 메타 — 동일 정책. |
| `MAN-019` | [`DB, DB_FTP 엑셀 정리요청.(김효빈).png`](../WeLove_FTP/Welove_인수인계/셋팅방법/DB정보,%20DB_FTP%20엑셀/DB,%20DB_FTP%20엑셀%20정리요청.(김효빈).png) | `MAN-CH-INFRA` | `MAN-TPC-INFRA` | × | 정리 요청 이미지(메타). |
| `MAN-020` | [`위러브 물류, 출판사 연락처(신).xlsx`](../WeLove_FTP/Welove_인수인계/출판setting/위러브%20물류,%20출판사%20연락처(신).xlsx) | `MAN-CH-DISTRIBUTOR-WEB` | `MAN-TPC-ONBOARDING` | △ | 총판·출판사 연락처(개인정보) — 가입 화이트리스트 정합 검토용, 인용 시 마스킹. |

## 4. 출판 셋팅 (`Welove_인수인계/출판setting`)

| 추적 ID | 자산 | 채널 | 주제 | 비밀? | 비고 |
|---|---|---|---|:-:|---|
| `MAN-030` | [`출판(테이블구조).xls`](../WeLove_FTP/Welove_인수인계/출판setting/weelove/출판(테이블구조).xls) | — | `MAN-TPC-SCHEMA` | × | **스키마 사전 단일 원천** — [`analysis/welove_schema_dictionary.json`](../analysis/welove_schema_dictionary.json) + [`docs/welove-publish-schema-dictionary.md`](welove-publish-schema-dictionary.md) 로 추출. 추적 ID `SCH-WELOVE-출판-*`. |
| `MAN-031` | [`Project1.exe`](../WeLove_FTP/Welove_인수인계/출판setting/weelove/) (+ `Login.zip`, `AutoUpdate/`, `Report(출력물-변경)/`) | `MAN-CH-DESKTOP` | `MAN-TPC-OPS` | × | 출판 클라이언트 바이너리 — 동등성 검증 보조 자산. 본 카탈로그는 "존재" 만 메타 기록. |
| `MAN-032` | [`Report(출력물-변경)/*.frf`](../WeLove_FTP/Welove_인수인계/출판setting/weelove/Report(출력물-변경)/) | `MAN-CH-DESKTOP` | `MAN-TPC-PRINT` | × | 인쇄/라벨 양식 — 운영 결합은 DEC-039/DEC-050 정책에 따름. |

---

## 5. 자산별 추적 매핑 (포팅 산출물 합류)

| `MAN-*` | 산출물 매핑 | 시나리오/계약 매핑 |
|---|---|---|
| `MAN-001`, `MAN-002`, `MAN-003` | [`docs/manual-to-scenario-matrix.md`](manual-to-scenario-matrix.md) | C1~C8 핵심 시나리오, `migration/contracts/*.yaml` |
| `MAN-004`, `MAN-005`, `MAN-006`, `MAN-007` | [`migration/contracts/mobile_uat.yaml`](../migration/contracts/mobile_uat.yaml) | 모바일 UAT 계약 |
| `MAN-008`, `MAN-012`, `MAN-013`, `MAN-014`, `MAN-017`, `MAN-018` | [`analysis/welove_db_route_matrix.json`](../analysis/welove_db_route_matrix.json) (메타만) + [`docs/decision-login-db-routing.md`](decision-login-db-routing.md) | `migration/contracts/login.yaml` D-LOGIN-4 (멀티테넌시) |
| `MAN-010`, `MAN-016`, `MAN-020` | [`docs/onboarding-rbac-menu-matrix.md`](onboarding-rbac-menu-matrix.md) | `migration/contracts/admin_permissions.yaml`, ONB-001 |
| `MAN-030` | [`analysis/welove_schema_dictionary.json`](../analysis/welove_schema_dictionary.json) | `migration/contracts/master_data.yaml`, `db_impact_matrix.json` |
| `MAN-031`, `MAN-032` | (보조 자산 — 회귀 비교 시 참조) | DEC-037/DEC-039/DEC-050 |

---

## 6. 비밀 처리 정책 (요약)

| 자산 군 | 본 카탈로그 표기 | 원본 보존 | 인용 정책 |
|---|---|---|---|
| 계정·암호·root 토큰 (`MAN-008/012-014/017/018`) | "○" 표시 + 메타(필드명·테이블명·서버 ID) 만 | 작업자 PC `WeLove_FTP/` 한정. **레포 커밋 금지**. | 본문/PR/이슈에 원문 평문 인용 금지. |
| 개인정보(연락처) (`MAN-020`) | "△" 표시 | 보존하되 마스킹 후 인용 | `010-****-1234` 형식. |
| 일반 매뉴얼 (텍스트/PPT/PDF) | "×" | 보존 + 인용 가능 | 절·단계만 인용, 화면 캡처는 별도 PR. |

상세는 [`docs/secrets-policy.md`](secrets-policy.md) 참조. 본 카탈로그는 그 정책의 **첫 적용 사례**.

---

## 7. 갱신 절차

1. 신규 자산이 `WeLove_인수인계/` 에 도착하면 §2~§4 표에 행 추가.
2. 비밀 포함 여부를 §1.2/§6 기준으로 분류해 "○/△/×" 표기.
3. 자산이 산출물(스키마 사전·DSN 메타·시나리오)에 합류하면 §5 매핑 1행 추가.
4. 본 문서 변경 시 추적 ID 는 **재사용 금지**(폐기 자산은 `[DEPRECATED]` 표기 후 행 보존).

---

## 8. 자동 재현 (다음 사이클 후보)

- 폴더 스캔 + 채널·주제 휴리스틱 자동 분류 스크립트(`tools/manual_inventory.py`) 도입 검토 — 본 사이클은 수기.
- `analysis/manual_inventory.json` 자동 export(파일명·해시·크기·확장자만) — 비밀 자산은 `secret: true` 메타만.
