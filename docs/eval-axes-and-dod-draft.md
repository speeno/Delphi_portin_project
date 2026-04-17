# 5축 평가 기준 + DoD/UAT 합격 조건 (초안)

웹 포팅의 “**레거시와 동등**”을 정의하는 5축 평가 기준과, 각 단계(베타 → 내부오픈 → 공식오픈/UAT)의 합격 조건(DoD)을 정리합니다.
- 산출물 #7 [`migration/contracts/*.yaml`](../migration/contracts/) 의 `equivalence` 항목에 대응.
- 산출물 #8 [`migration/test-cases/*.json`](../migration/test-cases/) 의 `axes` 항목에 대응.
- 승인 게이트 [`dashboard/data/approvals.json`](../dashboard/data/approvals.json)의 검증 기준으로 사용.

> 본 문서는 **초안(draft)** 입니다. 게이트 1·3·6 심의 시 정식 채택합니다.

## 1. 5축 평가 기준

| 축 | 영문 | 정의 | 측정 방법 | 자동화 도구 |
|----|------|------|-----------|-------------|
| 기능 | functional | 동일 입력에 대해 **동일 분기·동일 결과 코드** | API 응답 비교, UI 분기 비교 | Test Harness PoC, Comparison Harness |
| 데이터 | data | DB **before/after delta**가 동일(또는 정의된 차이 내) | 트랜잭션 단위 스냅샷 비교 | DB Diff Tool, capture-and-replay |
| UX | ux | 화면 흐름·메시지·핵심 단축키가 의미 보존 | UI 스크린·라우팅 비교, 휴리스틱 체크 | screen_cards 휴리스틱, 수동 |
| 성능 | performance | p95 응답 시간·처리량이 합의 SLA 이내 | k6/Locust, APM | (Sprint 4~5에 도입) |
| 감사 | audit | 보안·감사 로그·권한 검증이 신규 요구를 충족 | 로그 검증, 보안 점검 | 별도 audit checklist |

### 1.1 축별 합격 임계값(베타 기본값, 시나리오별 가감)

| 축 | 베타 임계값 | 내부오픈 임계값 | 공식오픈/UAT 임계값 |
|----|------------|------------------|----------------------|
| 기능 | 핵심 케이스 100% pass, 차단급 결함 0 | 회귀 팩 95% pass | 회귀 팩 100% pass(또는 명시적 면책) |
| 데이터 | INSERT/UPDATE/DELETE 키 불일치 0건(베타 흐름) | 모든 변경 흐름에서 delta 일치 | 100% 일치(또는 명시 차이) |
| UX | 핵심 메시지·분기 의미 보존 | 단축키 재현 50% 이상 | 단축키 재현 80% 이상 |
| 성능 | p95 < 1.0s (warm) | p95 < 0.7s | p95 < 0.5s, error_rate < 0.5% |
| 감사 | 로그인/권한 변경 로그 기록 | 모든 INSERT/UPDATE 감사 | SLA에 가까운 응답 + 감사 보존 정책 |

(시나리오 단위 임계값은 각 `migration/test-cases/<flow>.json`의 `expect`로 덮어씀)

## 2. Definition of Done (DoD) — 단계별

### 2.1 시나리오 DoD (Migration Contract 1건 단위)

해당 시나리오가 “끝났다”고 부를 수 있는 최소 조건:

- [ ] `migration/contracts/<flow>.yaml` 작성 + `status: approved`
- [ ] `migration/test-cases/<flow>.json` 작성 + 회귀 팩 통과(베타 임계값)
- [ ] 5축 모두 결과 기록(미적용 축은 `n/a` + 사유)
- [ ] 차이점(deltas) 항목이 [`legacy-analysis/decisions.md`](../legacy-analysis/decisions.md)에 DEC로 등록되었거나 OQ로 추적 중
- [ ] DB 영향이 있는 경우 [`docs/db-business-logic-inventory.md`](db-business-logic-inventory.md) §관련 표·노트에 반영
- [ ] 캡처 결과(있다면) [`docs/db-logic-porting-gap-report.md`](db-logic-porting-gap-report.md) 갱신

### 2.2 베타 DoD (게이트 #1, #2)

- [ ] 핵심 시나리오(C1, C2, C7) 시나리오 DoD 충족
- [ ] 차단급(데이터 손실·안전·법규) 결함 0건 또는 명시적 완화 합의
- [ ] [`dashboard/data/release-milestones.json`](../dashboard/data/release-milestones.json) `beta.exitCriteria` 충족
- [ ] DB 로직 검토 게이트(approvals id 2) — query_capture 1회 실시 + 갭 리포트 갱신

### 2.3 내부오픈 DoD (게이트 #3, #4, #5)

- [ ] 모든 베타 결함의 백로그 정리(중대 이상 클로저)
- [ ] Customer Variant Matrix 최종 반영 + 고객사 분기 분기점 동작 확인
- [ ] 인쇄·라벨·세무 보고서 5축 동등 입증
- [ ] Routing shadow 모드로 1주 이상 비교 결과 0% 불일치(또는 합의 임계값)

### 2.4 UAT 합격 (게이트 #6)

- [ ] 5축 모두 “공식오픈 임계값” 충족
- [ ] 운영 측(현업·관리자) 사인오프
- [ ] 롤백 절차 1회 실연 통과
- [ ] 감사 로그 보존 정책 시행 확인

## 3. 평가 운영 규칙

- **회귀 팩 실패 = 즉시 차단**: 베타 단계라도 `data` 축 실패는 차단급으로 간주.
- **OQ 미해결**: 시나리오의 `outstanding.blocked_by_open_questions`가 비어 있어야 베타 진입.
- **수동 케이스**: 자동화 불가 케이스는 `manual: true` 표기 + 별도 체크리스트로 운영.
- **임계값 변경**: 본 문서를 PR로 갱신 + 게이트 심의 의결을 거친다(임시 변경 금지).

## 4. 산출물 연결

| 항목 | 위치 |
|------|------|
| 5축 정의(축별) | 본 문서 §1 |
| 시나리오별 임계값 | `migration/test-cases/<flow>.json` `expect` |
| 시나리오별 동등성 항목 | `migration/contracts/<flow>.yaml` `equivalence` |
| 게이트 일정·승인자 | `dashboard/data/approvals.json` |
| 베타·내부·공식 출구 기준 | `dashboard/data/release-milestones.json` |

## 5. 변경 이력

- 2026-04-21 — 초안 작성 (포팅 직전 분석 작업 로드맵 4순위 산출물).

---

*다음 단계: 게이트 #1 심의 시 본 초안 정식 채택 → `migration/contracts/login.yaml` `equivalence` 검증으로 베타 첫 사이클 적용.*
