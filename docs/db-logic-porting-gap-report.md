# DB 비즈니스 로직 포팅 — 갭 리포트

**초판:** 2026-04-21  
**갱신 주기:** 스프린트 단위 리뷰 (메인 + 기획)  
**근거 도구:** `tools/db/db_logic_reporter.py`, `tools/db/db_logic_cross_reference.py`

## 관련 문서

- 인벤토리: [`docs/db-business-logic-inventory.md`](db-business-logic-inventory.md)
- 교차맵: [`analysis/db_logic_cross_reference.json`](../analysis/db_logic_cross_reference.json)
- 미해결 질문: [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md) (OQ-DBL 시리즈)
- 체크리스트 §2.5: [`docs/delphi-developer-confirmation-checklist.md`](delphi-developer-confirmation-checklist.md)
- 쿼리 캡처 런북: [`docs/query-capture-runbook.md`](query-capture-runbook.md)

---

## 1. 1차 자동 조사 결과 요약

| 범주 | 조사 결과 | 수집 방법 | 위험도 |
|------|-----------|-----------|--------|
| 저장 루틴(PROCEDURE/FUNCTION) | 4대 모두 **0건** | INFORMATION_SCHEMA + mysql3 probe | 낮음 — 확인 완료 |
| 트리거(TRIGGER) | 4대 모두 **0건** | INFORMATION_SCHEMA + mysql3 probe | 낮음 — 3.23은 미지원 정상 |
| 뷰(VIEW) | 4대 모두 **0건** | INFORMATION_SCHEMA + mysql3 probe | 낮음 — 3.23은 미지원 정상 |
| 외래키(FK) | 모던 2대 **0건** | INFORMATION_SCHEMA | 중간 — 코드 측 참조 무결성 의존 |
| UNIQUE 제약 | 모던 2대 **0건** | INFORMATION_SCHEMA | 중간 — 코드 측 중복 체크 의존 |
| 델파이 내 동적 SQL·CALL | `CALL` 추출 **0건** (query_catalog 기준) | pas_parser | 중간 — 동적 문자열 결합 누락 가능 |
| 운영 SQL 캡처 | 미실시 | query_capture.py | 높음 — 런타임 전용 쿼리 미확인 |

## 2. 누락 후보 & 위험 항목

| ID | 항목 | 위험도 | 현재 상태 | 조치 계획 | OQ 연결 |
|----|------|--------|-----------|-----------|---------|
| GAP-001 | 운영 시 실행되지만 정적 분석에 잡히지 않는 SQL | 높음 | 미조사 | query_capture 리허설 실시 (런북 참고) | OQ-DBL-003 |
| GAP-002 | 3.23 인스턴스 DB 내 로직 존재 여부 확정 | 중간 | probe 완료(0건) | 현장 DBA 확인 후 클로저 | OQ-DBL-001 |
| GAP-003 | FK·CHECK·DEFAULT 등 선언적 규칙의 코드 측 재현 여부 | 중간 | 자동 수집(0건) | 포팅 화면별 테이블 제약 검증 추가 | OQ-DBL-002 |
| GAP-004 | 배치·야간·외부 EXE에서만 실행되는 DB 작업 | 중간 | 미조사 | 체크리스트 §1.4 현장 확인 | — |
| GAP-005 | 동적 SQL 문자열 결합(+, Format, Concat)에 숨은 DB 호출 | 중간 | 1차 추출 완료 | pas_parser 보강 또는 수동 검토 | — |

## 3. 게이트 연결

각 마일스톤 진입 전 아래 기준 충족을 확인:

| 마일스톤 | 기준 |
|----------|------|
| 베타 | GAP 항목 중 **높음** 전부 조사 완료 또는 OQ에 명시적 등록 |
| 내부오픈 | GAP 항목 **높음·중간** 모두 조사 완료, 미해결 시 리스크 수용 기록 |
| 공식오픈 | 전 GAP 항목 클로저 또는 리스크 수용 + 모니터링 합의 |

## 4. 갱신 절차

1. `tools/db/db_logic_reporter.py` 재실행 → 인벤토리 MD/JSON 갱신.
2. `tools/db/db_logic_cross_reference.py` 재실행 → 교차맵 갱신.
3. 본 문서의 §1 표와 §2 항목을 실제 결과와 대조해 갱신.
4. 새 GAP 항목이 있으면 `GAP-XXX`로 추가하고, OQ-DBL 시리즈와 교차 링크.
5. 스프린트 리뷰에서 §2의 **현재 상태** 컬럼을 갱신.

---

*최초 작성: DB 비즈니스 로직 포팅 누락 방지 계획에 따라 자동 조사 결과 + 수동 확인 항목을 통합.*
