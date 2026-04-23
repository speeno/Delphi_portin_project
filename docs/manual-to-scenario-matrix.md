# 메뉴얼 ↔ 시나리오 ↔ 라우트 ↔ 계약 정합 매트릭스

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-23 |
| 추적 ID | `MAN-*` (인수인계 자산), `C*` (포팅 시나리오), `MIG-*` (계약), `ONB-*` (가입 트랙) |
| 단일 원천 | 본 문서. 신규 메뉴얼·시나리오 추가 시 1 행 추가. |
| 정합 | [`docs/manual-catalog.md`](manual-catalog.md), [`docs/core-scenarios-porting-plan.md`](core-scenarios-porting-plan.md), [`migration/contracts/*.yaml`](../migration/contracts/), [`docs/onboarding-governance-spec.md`](onboarding-governance-spec.md), [`docs/onboarding-rbac-menu-matrix.md`](onboarding-rbac-menu-matrix.md) |

---

## 1. 매트릭스

| `MAN-*` 메뉴얼 | 절(요지) | 시나리오 | 웹 라우트(대표) | Contract | 계정 유형(`ACC-*`) | 비고 |
|---|---|---|---|---|---|---|
| `MAN-001` Chulpan사용법.ppt | 출판 클라이언트 전체 흐름 | C1~C8 전반 | `/(app)/transactions/*`, `/(app)/ledger/*` | 다수 | T2-PUB, T3 | 데스크톱 → 웹 1차 매핑 정본. |
| `MAN-002` 최강물류 매뉴얼.pdf | 총판 운영 흐름 (출고·반품·청구) | C2 출고 / C3 반품 / C4 청구 | `/(app)/transactions/outbound`, `/transactions/returns`, `/settlement/billing` | `outbound_order.yaml`, `return_receipt.yaml`, `settlement_billing.yaml` | T2-DIST | 부속 `최강물류택배폼.xlsx` 도 합류. |
| `MAN-003` 출판메뉴얼.xlsx | 출판 클라이언트 폼별 매뉴얼 | C1~C8 화면별 | `/(app)/*` 전 라우트 | 전 contract | T2-PUB | 폼/필드 단위 매핑 정본. |
| `MAN-004` 모바일 사용법.txt | `m.websend.kr` 접속 + 로그인 | C1 Login (mobile) | `/login` | `login.yaml` D-LOGIN-1 | T2-PUB, T3 | 모바일 vs 웹 SPA 동일 흐름. |
| `MAN-005` 모바일 거래명세서.txt | 거래처 검색 → 도서 추가 → 접수 (10단계) | C2 출고 (mobile UAT) | `/(app)/transactions/outbound` | `mobile_uat.yaml` UAT-OUT-* + `outbound_order.yaml` | T2-PUB, T3 | 단계별 UI flow contract 합류. |
| `MAN-006` 저자 전용 모바일.txt | 저자 페이지 URL 안내 | (P3 별 검토) | `/author/*` (미정) | — | T-AUTHOR (별 트랙) | 본 사이클 비커버. |
| `MAN-007` 지이엠코리아 총판측.txt | 총판 운영 모바일 URL | C* 모바일 보조 | `/(app)/admin/*` (총판 콘솔) | `admin_web_platform.yaml` | T2-DIST | URL 안내 1줄. |
| `MAN-008` DB.txt (비밀) | 서버·DB·계정 매핑 | DSN 라우팅 | (백엔드) | `login.yaml` D-LOGIN-4 | 모두 (DSN 메타) | **메타만** [`analysis/welove_db_route_matrix.json`](../analysis/welove_db_route_matrix.json). 원문 인용 금지. |
| `MAN-010` 출판사 PC 셋팅.pdf | 출판사명/코드 사전 등록 가정 | ONB-TRACK-T2-PUB | `/(public)/signup` (트랙=T2-PUB) | (가입은 contract 신설 후보 — `member_signup.yaml`) | T2-PUB 가입 시 | 회의 메모 FI-01 정합. |
| `MAN-011` DB서버 정보 현황.hwp | 서버·도메인 정보 | 운영 런북 | — | — | 운영 | 마스킹 후 인용. |
| `MAN-012`~`MAN-014` (비밀) | FTP/콘솔 자격증명 | 운영 런북 | — | — | 운영 | vault 이관. |
| `MAN-015` 구버전 설치방법.hwp | 구버전 설치 — 웹 미사용 | — | — | — | — | DEPRECATED 후보. |
| `MAN-016` 더북 별도 설치 안내.hwp | 총판 소속 출판사 별도 클라이언트 | ONB-TRACK-T2-PUB (분기) | `/(public)/signup` 트랙 분기 | `onboarding-governance-spec.md` ONB-API-01/02 | T2-PUB | 가입 분기 직접 근거. |
| `MAN-017`/`MAN-018` (비밀) | 계정→DB 매핑 / FTP 매핑 | DSN 라우팅 | (백엔드) | `login.yaml` D-LOGIN-4 | DSN 메타 | 본 사이클 메타 추출 완료(`welove_db_route_matrix.json`). |
| `MAN-019` 정리 요청 이미지 | (참조) | — | — | — | — | 메타. |
| `MAN-020` 위러브 출판사 연락처.xlsx (개인정보) | 화이트리스트 1차 후보 | ONB-TRACK-T2-PUB whitelist | (백엔드) | `member_signup.yaml` (후속 contract) | T2-PUB | 마스킹 후 사용. |
| `MAN-030` 출판(테이블구조).xls | 33 테이블 사전 | 전 시나리오 (스키마 정본) | (백엔드) | `master_data.yaml` 외 다수 | 모두 | [`analysis/welove_schema_dictionary.json`](../analysis/welove_schema_dictionary.json) 정본. |
| `MAN-031` Project1.exe | 출판 클라이언트 바이너리 | (회귀 비교 보조) | — | — | — | 동등성 비교. |
| `MAN-032` Report(출력물).frf | 인쇄/라벨 양식 | C? 인쇄 | `/(app)/print/*` | `print_label.yaml`, `print_invoice.yaml` | T2-PUB, T2-DIST, T3 | DEC-039/050 정합. |

---

## 2. 시나리오별 메뉴얼 풀(역인덱스)

| 시나리오 | 메뉴얼 |
|---|---|
| **C1 Login** | `MAN-001`, `MAN-003`, `MAN-004`, `MAN-008`, `MAN-017` |
| **C2 출고** | `MAN-001`, `MAN-002`, `MAN-003`, `MAN-005` |
| **C3 반품** | `MAN-001`, `MAN-002`, `MAN-003` |
| **C4 청구·정산** | `MAN-001`, `MAN-002`, `MAN-003` |
| **C5 결제·정산** | `MAN-001`, `MAN-003` |
| **C6 원장** | `MAN-001`, `MAN-003` |
| **C7 통계** | `MAN-001`, `MAN-003` |
| **C8 자료/리포트** | `MAN-001`, `MAN-003`, `MAN-032` |
| **C10 권한 관리** | (메뉴얼 없음 — 회의 메모 + 본 사이클 신설) |
| **C13~C15 (Phase2)** | `MAN-001`~`MAN-003` |
| **ONB-TRACK-T2-PUB 가입** | `MAN-010`, `MAN-016`, `MAN-020` |
| **ONB-TRACK-T3 가입** | (본 사이클 신설) |
| **DSN 라우팅** | `MAN-008`, `MAN-017`, `MAN-018` (메타만) |

---

## 3. 계정 유형별 최소 happy-path 시나리오 (`SCN-MIN-*`)

| ID | 유형 | 시퀀스 | 통과 조건 |
|----|---|---|---|
| `SCN-MIN-T1-01` | T1 수퍼관리자 | 로그인 → admin 콘솔 → 신규 사용자 발급 → 본 사용자 로그인 가능 | admin_audit 4 행 + JWT 발급 |
| `SCN-MIN-T2-DIST-01` | T2-DIST | 로그인 → 출판사 가입 신청 승인 → 소속 출판사 활성 | ONB E2E |
| `SCN-MIN-T2-PUB-01` | T2-PUB | 공개 가입(트랙=T2-PUB, dist_hcode 입력) → 총판 승인 → 첫 로그인 → 출고 1건 등록 | DSN 정합 + outbound 1행 |
| `SCN-MIN-T3-01` | T3 독립 출판사 | 공개 가입(트랙=T3) → 운영자 승인 → DSN 부여 → 첫 로그인 → 도서 마스터 등록 | DSN 부여 + master 등록 |

위 4 시나리오는 phase1 회귀에 포함되어야 한다 — `test/test_onboarding_*.py` 신설 (백로그).

---

## 4. 갱신 절차

1. 신규 메뉴얼 도착 → `manual-catalog.md` 행 추가 → 본 §1 표 1행 추가.
2. 신규 시나리오 또는 contract 신설 → §2 역인덱스 갱신.
3. 새 계정 유형 추가 → §3 의 `SCN-MIN-*` 행 추가.
