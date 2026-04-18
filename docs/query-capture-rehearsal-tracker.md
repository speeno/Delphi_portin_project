# 쿼리 캡처 리허설 트래커

런북 [`docs/query-capture-runbook.md`](query-capture-runbook.md)을 **운영 환경에서 1회 이상 실시**한 결과를 추적합니다.
**GAP-001 / OQ-DBL-003** 클로저의 단일 출처(single source of truth)로 사용합니다.

> 본 문서는 **체크리스트형 트래커**입니다. 실제 캡처는 운영 DBA·델파이 담당자와 일정을 잡아 수행합니다.
> 자동화 가능한 부분(분석/교차맵 갱신)은 모두 도구화되어 있어 캡처 파일만 들어오면 즉시 반영 가능합니다.

## 1. 일정·승인

| 항목 | 값 |
|------|----|
| 1차 리허설 일자(예정) | (운영 DBA 일정 조율 중 — 2026-04-22 기준 미확정) |
| 1차 리허설 일자(실시) | _대기_ |
| 대상 서버 | `legacy-153` 1대 (시범) |
| 운영 영향 윈도 | 야간 21:00~22:00 (저부하) |
| DBA 승인자 | _대기_ |
| 델파이 시나리오 수행자 | _대기_ |
| 캡처 실행(웹 포팅) | _대기_ |
| C1 상태(2026-04-22) | **외부 의존(blocked by DBA schedule)** — 캡처 파일 도착 즉시 §5 자동 갱신. 본 차단은 D-LOGIN-1~4 결정 진행을 막지 않음(static analysis 기반 최선 계약 동결). |

## 2. 사전 체크 (런북 §1)

- [ ] general_log 활성 가능 확인 (성능 영향·디스크 여유)
- [ ] 접속 경로(SSH 터널 포함) 검증 — `tools/db/db_probe.py` 1회 통과
- [ ] 시나리오 수행자 일정 확정
- [ ] 캡처 파일 보관 경로 확인 — `debug/output/` (git 미추적)

## 3. 캡처 시나리오 진행표

[`docs/core-scenarios-candidates.md`](core-scenarios-candidates.md)와 런북 §2의 교집합으로 사용. 베타 라인을 먼저 채웁니다.

| # | 시나리오 | 수행 시각 | 메모/이슈 | 관련 contract/test-pack |
|---|----------|-----------|-----------|--------------------------|
| 1 | 로그인(C1) | _대기_ | screen_card §3 SQL 11건(SELECT9/UPDATE2)이 정적 분석으로 식별됨. 캡처 시 (1) 일반 로그인 1회 + (2) 슈퍼유저(0000) 로그인 1회 만 수행하면 SQL-LOGIN-1 / SQL-LOGIN-2-VISIBILITY 양쪽 커버. | `migration/contracts/login.yaml`, `migration/test-cases/login.json` |
| 2 | 출고 접수(C2) |  |  | (작성 예정) |
| 3 | 라벨/송장 인쇄(C7) |  |  | (작성 예정) |
| 4 | 거래/잔액 조회(C6) |  |  | (선택) |
| 5 | 바코드 스캔→매칭(C8) |  |  | (선택) |

## 4. 캡처 산출물 (실시 후)

| 항목 | 경로/값 |
|------|----------|
| 캡처 원본(JSON) | `debug/output/captured_queries_<server>_<date>.json` |
| 캡처 라인 수 |  |
| 신규 발견 SQL 수 |  |
| 누락 가능성 분류 | (동적 SQL / 배치 / 외부 EXE / 기타) |

## 5. 결과 활용 — 명령

```bash
python3 tools/db/db_logic_cross_reference.py \
    --capture debug/output/captured_queries_<server>_<date>.json
```

실행 후 갱신되는 산출물:

- `analysis/db_logic_cross_reference.json` (orphan SQL·미커버 테이블 등)
- 후속: [`docs/db-business-logic-inventory.md`](db-business-logic-inventory.md) §관련 표·노트 갱신
- 갭: [`docs/db-logic-porting-gap-report.md`](db-logic-porting-gap-report.md) **GAP-001** 상태(미해결→완화/해결) 업데이트

## 6. OQ·게이트 클로저

- [ ] [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md) **OQ-DBL-003** 상태/해결 방법 기록
- [ ] [`docs/db-logic-porting-gap-report.md`](db-logic-porting-gap-report.md) **GAP-001** 상태·잔존 위험 기록
- [ ] `dashboard/data/approvals.json` **id 2 「DB 로직 검토 게이트」** 충족 여부 갱신
- [ ] `dashboard/data/timeline.json`에 마일스톤(또는 결정) 1줄 추가

## 7. 잔존 위험 (회의용 요약 칸)

회의나 게이트 심의에서 사용할 1~3줄 요약을 채웁니다.

> (예) 동적 SQL 0건 추가 발견. 단, 야간 배치는 미수행 → GAP-004와 함께 잔존.

---

*최초 작성: 2026-04-21 — 포팅 직전 분석 작업 로드맵 2순위 산출물*
