# 승인 게이트 정합성 점검 (6+1 = 7건)

[`dashboard/data/approvals.json`](../dashboard/data/approvals.json)에 등록된 승인 게이트 일정·승인 주체·산출물 매핑 정합성을 1차 점검합니다.

> 본 문서는 **검토 메모**입니다. 일정/주체 변경이 필요하면 PR로 `approvals.json`을 갱신하고 본 문서 §5에 변경 이력을 남깁니다.

## 1. 현재 등록 현황

| id | 이름 | 스프린트 | 일자(예정) | 승인자 | 비고 |
|----|------|----------|------------|--------|------|
| 1 | 분석 산출물 승인 | 1 | 2026-07-17 | M, P | 산출물 #1~#6 + Legacy Object Catalog |
| 2 | DB 로직 검토 게이트 | 1 | 2026-07-10 | M, P | 인벤토리·갭 리포트·query_capture 1회 |
| 3 | API 계약 승인 | 2 | 2026-07-31 | M, P, 현업 | Migration Contract + Eval Case |
| 4 | 고객사별 차이 승인 | 3 | 2026-08-14 | P, 현업 | Customer Variant Matrix 최종 |
| 5 | 인쇄 결과 승인 | 4 | 2026-09-25 | P, 현업 | 라벨/송장/리포트 동일성 |
| 6 | UAT 승인 | 5 | 2026-10-23 | P, 현업, 관리자 | 5축 eval 기반 |
| 7 | Cut-over 승인 | 6 | 2026-11-06 | 전원, 경영진 | Routing 100% |

## 2. 정합성 점검 결과

### 2.1 일정 — 스프린트 종료일과의 정합성

| id | 게이트 일자 | 스프린트 종료 | 정합성 | 비고 |
|----|-------------|---------------|--------|------|
| 1 | 2026-07-17 | Sprint 1 = 2026-07-17 | ✅ 일치 |  |
| 2 | 2026-07-10 | Sprint 1 = 2026-07-17 | ✅ 1주 선행 | 베타 직전 DB 로직 1차 차단·릴리스 |
| 3 | 2026-07-31 | Sprint 2 = 2026-07-31 | ✅ 일치 |  |
| 4 | 2026-08-14 | Sprint 3 = 2026-08-14 | ✅ 일치 |  |
| 5 | 2026-09-25 | Sprint 4 = 2026-09-25 | ✅ 일치 |  |
| 6 | 2026-10-23 | Sprint 5 = 2026-10-23 | ✅ 일치 |  |
| 7 | 2026-11-06 | Sprint 6 = 2026-11-06 | ✅ 일치 |  |

→ **결론: 일정 정합성 OK.**

### 2.2 승인 주체 — 역할 정의 정합성

- M(메인개발자), P(프로젝트 매니저/기획자), 현업, 관리자, 경영진.
- 게이트 #2(DB 로직 검토)는 현재 **M, P**만 지정. **DB 운영 측(DBA 또는 운영 책임)** 추가가 필요 — §3 권고.
- 게이트 #5(인쇄 결과)는 현장 운영자(라벨/배송 담당)가 사실상 핵심 — “현업”에 **현장 운영자 1명 명시**가 운영 시점에서 필요.

### 2.3 산출물 — 게이트별 입력물 정합성

| id | 필요한 산출물 | 현재 상태 | 갭 |
|----|--------------|-----------|----|
| 1 | 분석 산출물 #1~#6 + Legacy Object Catalog | #1~#6 완료, Catalog 진행 | OK |
| 2 | DB 로직 인벤토리·갭 리포트·query_capture 1회 | 인벤토리/갭 리포트 ✅, **캡처 0회** | ⚠ query_capture 리허설 1회 필요 |
| 3 | Migration Contract + Eval Case | 1건 초안(login) | 2~3건 추가 필요(C2, C7) |
| 4 | Customer Variant Matrix 최종 | 산출물 #6 완료 | 회의 후 분기 합의 결과 반영 필요 |
| 5 | 라벨/송장/리포트 동등성 | 코드 1차 조사 ✅ | 인쇄 결정 메모 + 실측 필요 |
| 6 | 5축 eval 결과 | [`docs/eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md) 초안 | 정식 채택 + 회귀 팩 N개 통과 필요 |
| 7 | Routing 100% + 안정 1주 | 미시작 | Sprint 5 결과 의존 |

## 3. 권고 액션

- **A1.** 게이트 #2 승인자에 **DBA(또는 운영 측 1명)** 추가.  
  → `approvals.json` `id:2` `approvers`에 `"DBA"` 추가 권고.
- **A2.** 게이트 #2 조건에 **query_capture 1회 실시 여부**가 명시되어 있으므로,  
  [`docs/query-capture-rehearsal-tracker.md`](query-capture-rehearsal-tracker.md) 결과를 직접 링크하도록 description에 트래커 경로 추가 권고.
- **A3.** 게이트 #3은 Migration Contract **N건 합의** 임계값이 모호 — 본 문서에 명시:  
  → 권고: **베타 라인 핵심 시나리오(C1, C2, C7) 3건 이상 `approved`**.
- **A4.** 게이트 #5 승인자 “현업”에 **현장 운영자(라벨/배송 담당) 1명 명시** 권고.
- **A5.** 게이트 #6 `description`에 **5축 임계값 출처**([`docs/eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md))를 추가.

## 4. 적용(승인 시 갱신)

- 위 권고 중 합의된 항목만 `dashboard/data/approvals.json`에 반영.
- 변경은 PR 단위로 진행하고, 본 문서 §5에 한 줄씩 기록.

## 5. 변경 이력

- 2026-04-21 — 정합성 점검 1차 작성. 일정 정합성 OK 확인. 승인자/산출물 갭 5건 권고(A1~A5).

---

*관련 문서: [`docs/eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md), [`docs/query-capture-rehearsal-tracker.md`](query-capture-rehearsal-tracker.md), [`migration/contracts/login.yaml`](../migration/contracts/login.yaml)*
