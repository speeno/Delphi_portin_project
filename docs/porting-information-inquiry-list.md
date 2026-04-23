# 포팅 시 필요한 정보 — 문의 사항 목록

웹 포팅을 진행하기 위해 **레거시 지식 보유자·운영 담당·DBA** 등에게 확인해야 하는 정보를 한눈에 모은 목록입니다.  
항목별 상세 질문문·표 형식 답변란은 [`docs/delphi-developer-confirmation-checklist.md`](delphi-developer-confirmation-checklist.md)를 사용하고, 미해결 이슈 추적은 [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md)를 따릅니다.

| 구분 | 문서/템플릿 |
|------|-------------|
| 인터뷰 진행·90분 안건표 | [`field-interview-meeting-template.md`](field-interview-meeting-template.md) |
| 현장 회의록(누적) | 예: [`field-interview-2026-04-23.md`](field-interview-2026-04-23.md) |

---

## 1. 업무·도메인·설치 맥락

| # | 문의 내용 | 연결 |
|---|-----------|------|
| D-01 | 운영 **고객사(설치) 수**, 고객사별 **화면·로직·DB 분기** 조건(회사코드·INI·레지스트리·하드코딩 등) | 체크 §1.1 · **OQ-001** |
| D-02 | 레거시 설치 시 **출판사명·출판사코드** 등 식별 정보 수집 순서·필수 여부(회의에서 부분 확인됨) | [`field-interview-2026-04-23.md`](field-interview-2026-04-23.md) FI-2026-04-23-01 |
| D-03 | `Id_Logn` **f11~f89 외** 별도 권한(PC명·IP·특정 gcode 등) | 체크 §1.2 |
| D-04 | **금액·할인·세금·반올림** 순서와 레거시와 맞춰야 할 **경계 케이스** | 체크 §1.3 |
| D-05 | 화면에 없는 **배치·야간 작업·외부 EXE** 유무 | 체크 §1.4 |
| D-06 | 알려진 버그에 대한 **현장 우회 사용법** | 체크 §1.5 |
| D-07 | **멀티테넌시**(한 웹 인스턴스·사용자→테넌트 매핑) 요구 시점과 정책 — 1차는 단일 테넌트 모델 전제 가능 | **OQ-LOGIN-1** · DEC-008 |
| D-08 | **회의 확정** 계정 유형 **3종**(수퍼관리자 / 물류·총판 및 소속 출판사 / 독립 출판사) — 권한·데이터 범위·기능 분기 | [`meeting-account-types-rbac-context.md`](meeting-account-types-rbac-context.md) |

---

## 2. DB·데이터·스키마

| # | 문의 내용 | 연결 |
|---|-----------|------|
| DB-01 | 운영 **정본 DB** 호스트·인스턴스, 서버가 여러 대인 이유 | 체크 §2.1 · **OQ-003** |
| DB-02 | 서버 간 **테이블·컬럼 차이** 허용 여부·용도 | 체크 §2.2 · [`db-schema-porting-readiness.md`](db-schema-porting-readiness.md) |
| DB-03 | **MySQL 3.23** 유지 기간·웹 읽기 전용 여부 | 체크 §2.3 · [`mysql-3.23-legacy-connection-notes.md`](mysql-3.23-legacy-connection-notes.md) |
| DB-04 | 한글·메모 필드 **문자셋·콜레이션** 합의 | 체크 §2.4 |
| DB-05 | DB **트리거·루틴·뷰** 실제 유무·중요도(자동조사 0건 후 현장 확인) | 체크 §2.5 · **OQ-DBL-001~003** · [`db-business-logic-inventory.md`](db-business-logic-inventory.md) |
| DB-06 | 동일 레코드 **동시 수정** 관행 | 체크 §2.6 |
| DB-07 | **FK·CHECK·UNIQUE 부재**가 의도인지·앱 레벨 무결성 범위 | **OQ-DBL-002** |
| DB-08 | **런타임 SQL 캡처**(리허설) 필요 시점·범위 | **OQ-DBL-003** · [`query-capture-runbook.md`](query-capture-runbook.md) |

---

## 3. UI·화면·인쇄

| # | 문의 내용 | 연결 |
|---|-----------|------|
| U-01 | **MDI·모달**이 업무 규칙인지 | 체크 §3.1 |
| U-02 | **단축키·F키·그리드** 의존도·웹 우선 재현 화면 | 체크 §3.2 |
| U-03 | 인쇄·리포트 엔진·**PDF 단독 대체** 가능 여부 | 체크 §3.3 · [`decision-print-scanner-web.md`](decision-print-scanner-web.md) |
| U-04 | 메뉴에 없는 **숨은 화면·디버그** 운영 사용 여부 | 체크 §3.4 |

---

## 4. 외부 연동·장비

| # | 문의 내용 | 연결 |
|---|-----------|------|
| E-01 | 스캐너·라벨 프린터·저울 **모델·연결 방식**(HID/COM/네트워크) | 체크 §4.1 · **OQ-002** · **OQ-002-R**(잔여 직결) · [`legacy-print-scanner-integration-survey.md`](legacy-print-scanner-integration-survey.md) |
| E-02 | **FTP·공유폴더·파일 경로**·계정·방화벽 | 체크 §4.2 · **OQ-IN-1** 등 |
| E-03 | 이메일·SMS·HTTP 등 **코드상 연동 중 현재 사용** 항목 | 체크 §4.3 |

---

## 5. 보안·운영·인수

| # | 문의 내용 | 연결 |
|---|-----------|------|
| O-01 | 비밀번호 정책·**감사 로그** 요구 | 체크 §5.1 |
| O-02 | 백업·**복구 목표**(RPO 등) | 체크 §5.2 |
| O-03 | 델파이와 **병행 기간**·웹 우선 화면 | 체크 §5.3 |

---

## 6. 검증·핵심 시나리오(UAT 연계)

| # | 문의 내용 | 연결 |
|---|-----------|------|
| V-01 | “**돌아가야 하는**” **핵심 시나리오 5~10개**(화면·버튼 단위) | 체크 §6.1 · [`core-scenarios-candidates.md`](core-scenarios-candidates.md) |
| V-02 | 숫자·집계 **동일해야 할 보고서** 목록 | 체크 §6.2 |
| V-03 | **의도적으로 바꿔도 되는** UX 범위 | 체크 §6.3 |

---

## 7. 도메인별 미해결(OQ) — 빠른 색인

포팅 중 발생한 **세부 도메인 질문**은 `open-questions.md`에 누적됩니다. 대표 예:

| ID | 한 줄 요약 |
|----|------------|
| OQ-001 | 고객사 수·커스터마이징 분기 |
| OQ-002 / OQ-002-R | 장비 연동·라벨/Web Serial/저울 잔여 |
| OQ-003 | DB 서버 대수·스키마 차이 |
| OQ-DBL-001~003 | DB 내 로직·제약·캡처 |
| OQ-LOGIN-1 | 멀티테넌시 매핑(후속) |
| OQ-OUT-1~4 | 출고(S1_Ssub 등) 운영 분기·집계·동시성 |
| OQ-IN-1 | FTP 전송 자격증명·인프라 |

전체 목록·상태는 **반드시** 원본 [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md)를 확인합니다.

---

*본 문서는 문의 항목의 **색인·우선순위 논의용**입니다. 답변 기록의 정본은 체크리스트 표와 OQ입니다.*
