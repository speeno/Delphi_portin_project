# DB 비즈니스 로직 인벤토리

**자동 생성:** 2026-04-17T17:22:00  
**도구:** `tools/db/db_logic_reporter.py`  
**원칙:** 전체 DB dump·데이터 없음. 메타(INFORMATION_SCHEMA / SHOW)만 사용.

**관련 문서**
- 교차맵: [`analysis/db_logic_cross_reference.json`](../analysis/db_logic_cross_reference.json)
- 갭 리포트: [`docs/db-logic-porting-gap-report.md`](db-logic-porting-gap-report.md)
- 스키마 준비도: [`docs/db-schema-porting-readiness.md`](db-schema-porting-readiness.md)
- 미해결 질문: [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md) (OQ-DBL 시리즈)
- 체크리스트 §2.5: [`docs/delphi-developer-confirmation-checklist.md`](delphi-developer-confirmation-checklist.md)
- 쿼리 캡처 런북: [`docs/query-capture-runbook.md`](query-capture-runbook.md)

## 1차 자동 조사 결과 요약

모던 경로(138·153)에서는 `INFORMATION_SCHEMA.ROUTINES/TRIGGERS/VIEWS`를 완전히 조회했으며, **루틴·트리거·뷰가 0건**으로 확인되었습니다.  
3.23 경로(154·155)에서는 MySQL 3.23 자체가 저장 루틴·트리거·뷰를 지원하지 않으므로, 해당 기능이 존재하지 않는 것이 **정상 결과**입니다.

즉, **현재 운영 DB에서 비즈니스 로직은 DB 객체(루틴·트리거·뷰)가 아닌 전적으로 델파이 클라이언트 코드 내에** 있다고 1차 판단됩니다.  
단, 이 판단을 확정하려면 체크리스트 §2.5의 **현장 확인**이 필요합니다.

## 서버별 요약

| 서버 ID | 추출 모드 | 테이블 | 루틴 | 트리거 | 뷰 | FK | UNIQUE | 비고 |
|---------|-----------|--------|------|--------|-----|-----|--------|------|
| remote_138 | information_schema | 51 | 0 | 0 | 0 | 0 | 0 | — |
| remote_153 | information_schema | 79 | 0 | 0 | 0 | 0 | 0 | — |
| remote_154 | mysql3_show_meta | 65 | 0 | 0 | 0 | 0 | 0 | ⚠ 3.23 미수집 |
| remote_155 | mysql3_show_meta | 78 | 0 | 0 | 0 | 0 | 0 | ⚠ 3.23 미수집 |

## remote_138

이 서버에서는 루틴·트리거·뷰·FK·UNIQUE 객체가 발견되지 않았습니다.

## remote_153

이 서버에서는 루틴·트리거·뷰·FK·UNIQUE 객체가 발견되지 않았습니다.

## remote_154

> **한계:** MySQL 3.23: INFORMATION_SCHEMA 미지원 — routines/triggers/views 자동 수집 불가. DBA 수동 확인 또는 mysql.proc 직접 조회 필요.

DB 로직 객체 자동 수집 불가 (MySQL 3.23). DBA 수동 확인 필요.

## remote_155

> **한계:** MySQL 3.23: INFORMATION_SCHEMA 미지원 — routines/triggers/views 자동 수집 불가. DBA 수동 확인 또는 mysql.proc 직접 조회 필요.

DB 로직 객체 자동 수집 불가 (MySQL 3.23). DBA 수동 확인 필요.

---

## 다음 조치

1. 각 항목의 **포팅 상태**를 검토 후 갱신 (미검토 → 포팅 불필요 / 포팅 필요 / 완료).
2. 3.23 인스턴스는 DBA 수동 확인 후 이 문서에 수기 추가.
3. 교차맵(`analysis/db_logic_cross_reference.json`)과 함께 사용해 화면별 영향 확인.
4. 갭 리포트(`docs/db-logic-porting-gap-report.md`) 주기 갱신.

## 갱신 절차

```bash
# 스키마가 변경되었을 때 재추출 → 인벤토리 재생성
python3 tools/db/extract_server_schema.py --server-id <id>
python3 tools/db/db_logic_reporter.py --schema-dir debug/output/schema
python3 tools/db/db_logic_cross_reference.py
```

주기: **주 1회 + 스키마 변경 시**. 갭 리포트는 스프린트 단위로 리뷰.

## 시나리오 영향 노트 (수동 갱신)

본 섹션은 contract approved 시점에 시나리오 별 DB 영향을 수기 1줄로 기록합니다 (T8 DoD §5 동기화).

| 시나리오 | 테이블 | 영향(베타) | 변경 형태 | 결정 | 출처 |
|---------|--------|-----------|----------|------|------|
| C1 로그인·세션 시작 | `Id_Logn` | **R only** (SELECT × 1) — 베타는 DB 변경 0건 | `tenant_id` 컬럼 신규 추가 (DEC-008, ALTER 1회) | DEC-005 (Gpass 해시 별도 컬럼), DEC-008 (tenant_id) | `migration/contracts/login.yaml` v1.0.0, `docs/c1-login-evaluation-report.md` |
| C1 로그인·세션 시작 | `G7_Ggeo` | **R only** (SELECT × 1, 슈퍼유저 분기) | 변경 없음 | DEC-007 (베타 보존) | `migration/contracts/login.yaml` SQL-LOGIN-2-VISIBILITY |
