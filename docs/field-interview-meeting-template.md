# 현장 인터뷰 진행·기록 템플릿

레거시 델파이 담당자(또는 장기 유지보수 담당자) **1회 인터뷰**용 템플릿입니다.
[`docs/delphi-developer-confirmation-checklist.md`](delphi-developer-confirmation-checklist.md)를 베이스로 하되, **회의 운영(섭외→진행→OQ 클로저)** 까지 한 문서에서 끝내도록 구성했습니다.

> 이 파일은 **운영 산출물**입니다. 실제 회의가 잡히면 §3 진행표·§4 답변·§5 후속작업을 채우고 커밋합니다.

## 1. 회의 개요

| 항목 | 값 |
|------|----|
| 회의 일자 |  |
| 시간/소요 |  |
| 장소/방식 | (대면 / 화상 / 전화) |
| 참석(델파이 측) |  |
| 참석(웹 포팅 팀) |  |
| 사회/기록 |  |

### 사전 공유 자료(메일·메신저로 첨부)

- [`docs/delphi-developer-confirmation-checklist.md`](delphi-developer-confirmation-checklist.md) §1~§6
- [`docs/db-business-logic-inventory.md`](db-business-logic-inventory.md) — DB 측 로직 1차 자동 조사 결과
- [`docs/legacy-print-scanner-integration-survey.md`](legacy-print-scanner-integration-survey.md) — 인쇄·바코드 코드 1차 조사
- [`docs/db-schema-porting-readiness.md`](db-schema-porting-readiness.md) — 서버 간 스키마 diff 요약

## 2. 목표 (Definition of Done)

- 체크리스트 §1~§6의 **모든 행에 한 줄 답변**이 채워진다.
- 아래 OQ가 **클로저 또는 명시적 리스크 수용**으로 정리된다.
  - OQ-001 (고객사 변형 분기)
  - OQ-002 (장비 모델·연결 방식)
  - OQ-003 (DB 정본/서버 구성)
  - OQ-DBL-001 (3.23 DB 측 로직 유무 최종 확인)
  - OQ-DBL-002 (FK·UNIQUE·CHECK 부재 사유)
  - OQ-DBL-003 (런타임 SQL 캡처 필요성·시점)
- **핵심 시나리오 5~10개**(체크리스트 §6.1) 후보가 회의록에 기록된다.
- **베타 노출 범위(라인)** 1차 합의가 회의록에 기록된다.

## 3. 진행표 (90분 기준)

| 시각 | 분 | 안건 | 산출물 |
|------|----|------|--------|
| 0~10 | 10 | 인사·범위 공유(체크리스트 사용법) | 회의록 §4.0 |
| 10~25 | 15 | §1 업무·도메인(분기·암묵 규칙) | §4.1 |
| 25~40 | 15 | §2 DB·데이터(정본/3.23/콜레이션) + §2.5 DB 측 로직 확인 | §4.2 |
| 40~50 | 10 | §3 UI·화면(MDI·단축키·인쇄 대체 가능성) | §4.3 |
| 50~60 | 10 | §4 외부 연동·장비(스캐너·프린터·FTP) | §4.4 |
| 60~70 | 10 | §5 보안·운영·인수(병행 운영) | §4.5 |
| 70~85 | 15 | §6 핵심 시나리오 5~10개 + 베타 라인 합의 | §4.6 |
| 85~90 | 5  | 후속 작업·차주 일정 | §5 |

## 4. 답변 기록 (체크리스트 동기화용)

각 항목은 **한 줄 메모 + 결정/추가 OQ 표시**로 적습니다. 회의 후 그대로 [`docs/delphi-developer-confirmation-checklist.md`](delphi-developer-confirmation-checklist.md) 표에 옮깁니다.

### 4.1 업무·도메인(§1)

- 1.1 (고객사·분기): 
- 1.2 (권한): 
- 1.3 (금액·할인·반올림): 
- 1.4 (배치·야간·외부 EXE): 
- 1.5 (암묵적 사용법): 

### 4.2 DB·데이터(§2)

- 2.1 (DB 정본): 
- 2.2 (서버 간 차이 허용): 
- 2.3 (3.23 유지 계획): 
- 2.4 (문자셋·콜레이션): 
- 2.5 (DB 측 규칙 — 트리거/루틴/뷰): **자동 조사 0건이 맞는가? Y/N**, 메모: 
- 2.6 (동시 수정 관행): 

### 4.3 UI·화면(§3)

- 3.1 (MDI·모달): 
- 3.2 (단축키·F키): 
- 3.3 (인쇄·리포트 — PDF 대체 가능?): 
- 3.4 (숨은 화면): 

### 4.4 외부 연동·장비(§4)

- 4.1 (스캐너/프린터/저울 모델·연결): 
- 4.2 (FTP·공유폴더): 
- 4.3 (이메일·SMS·외부 HTTP): 

### 4.5 보안·운영(§5)

- 5.1 (비밀번호·감사 로그): 
- 5.2 (백업·복구 목표): 
- 5.3 (병행 운영 기간·우선순위 화면): 

### 4.6 검증·인수(§6)

- 6.1 (**핵심 시나리오 5~10개**): 
  1. 
  2. 
  3. 
  4. 
  5. 
- 6.2 (반드시 동일해야 하는 보고서): 
- 6.3 (의도적으로 바꿔도 되는 UX): 

### 4.0 자유 메모·암묵 지식

- 

## 5. 회의 후 작업 (담당자/기한 명시)

- [ ] **체크리스트 갱신** — `docs/delphi-developer-confirmation-checklist.md` (담당: , 기한: )
- [ ] **OQ 클로저** — `legacy-analysis/open-questions.md` OQ-001 / OQ-002 / OQ-003 / OQ-DBL-001~003
- [ ] **DB 정본·스키마 정책** — `docs/db-schema-porting-readiness.md` 또는 별도 메모
- [ ] **DB 로직 갭 리포트** — `docs/db-logic-porting-gap-report.md` 갭 상태 갱신
- [ ] **핵심 시나리오 후보** — `docs/core-scenarios-candidates.md` 5~10개 확정 표시
- [ ] **베타 라인 반영** — `dashboard/data/release-milestones.json` `beta.exitCriteria` 보강
- [ ] **인쇄·바코드 결정** — `docs/decision-print-scanner-web.md` 1줄 결정 + Decision Log
- [ ] **DB 로직 검토 게이트(approvals.json id 2)** 조건 충족 여부 갱신

## 6. 향후 추가 회의(선택)

- 후속 회의가 필요하면 본 템플릿을 복제(`docs/field-interview-YYYY-MM-DD.md`)해 사용합니다. (예시 누적본: [`field-interview-2026-04-23.md`](field-interview-2026-04-23.md))
- 회의록 누적은 `legacy-analysis/decisions.md`에 **DEC**로, 미해결은 `open-questions.md`에 **OQ**로 분리합니다.

---

*최초 작성: 2026-04-21 — 포팅 직전 분석 작업 로드맵 1순위 산출물*
