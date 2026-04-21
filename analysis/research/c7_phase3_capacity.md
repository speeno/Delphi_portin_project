# C7 Phase 3 — R&D 가용성 점검표 (G3)

**ID**: C7-PHASE3-CAPACITY
**일자**: 2026-04-21 (양식 동결, 점검 미실시)
**상태**: 게이트 G3 — **PENDING (미실시)**
**연관**: [`docs/phase3-print-gate.md`](../../docs/phase3-print-gate.md), [`dashboard/data/tracks.json`](../../dashboard/data/tracks.json) `T-B4` M2/M3/M4

---

## 0. 점검 목적

게이트 G1 (SME 합의) + G2 (B1 vs B4 ROI) 통과 직후 **다음 sprint 의 인력·시간이 화이트리스트 PR 1~5건을 흡수할 수 있는지** 점검. 가용성 부족 시 sprint 1회 이상 deferral.

---

## 1. 마일스톤 점검표

| 마일스톤 | 정의 | 산출물 | 담당 | 시작일 | 종료일 | 상태 |
|---|---|---|---|---|---|---|
| **M1 게이트 통과 확인** | G1+G2 PASS 문서화 | `phase3-print-gate.md §1` 체크 | 메인개발자 | (TBD) | (TBD) | PENDING |
| **M2 화이트리스트 인프라** | `print_template_registry.py` 신설 + label_service 일반화 | 본 계획 `registry` todo | 메인개발자 | 2026-04-21 | 2026-04-21 | DONE (DEC-050 시행 전 인프라 선행) |
| **M3 1차 화이트리스트 PR** | SME 합의 form 1건 결합 (Sobo46 또는 라벨 변형) | `print_templates/auto/Report_*.ir.json` + 화이트리스트 1행 | 메인개발자 | (TBD) | (TBD) | PENDING |
| **M4 5축 회귀 + 시각 회귀** | 결합 form 의 PDF 시각 회귀 + `test_regression_phase2.py` 그룹 추가 | 회귀 리포트 + 5축 PASS | 메인개발자 | (TBD) | (TBD) | PENDING |

---

## 2. 인력 가용성 (PENDING)

| 역할 | 담당 | 가용 시간 (sprint 당) | 결합 form 수용량 |
|---|---|---|---|
| 메인개발자 | (TBD) | (TBD) | (TBD) |
| 운영 SME | (TBD) | (TBD) | (TBD — 합의/검토 시간) |
| QA | (TBD) | (TBD) | (TBD — 시각 회귀 검토) |

**합산 가용 form 수용량**: (TBD) / sprint — 본 게이트 PASS 의 임계값 = `≥ 1 form/sprint`.

---

## 3. 위험·차단 요인

| 위험 | 영향 | 완화책 |
|---|---|---|
| SME 가용성 < 1 회/sprint | G1 미통과 → 모든 결합 deferral | 비동기 인터뷰 (e-mail 합의) 허용 |
| WeasyPrint 시스템 의존성 누락 | 회귀 테스트 불가 | `503 PR_ENGINE_UNAVAILABLE` 폴백 + Docker 환경 통일 |
| MID/LOW 버킷 form 합의 | 시각 회귀 비용 증가 | SOP-B (manual) 강제, 자동 결합 거부 |

---

## 4. 게이트 PASS 기준 (DoD)

- [ ] §1 M1, M2 = DONE
- [ ] §2 합산 가용 form 수용량 ≥ 1 form/sprint
- [ ] §3 모든 위험에 완화책 합의 ✓
- [ ] sprint 1회 일정 합의 (시작일/종료일 동결)

3 조건 만족 → [`docs/phase3-print-gate.md`](../../docs/phase3-print-gate.md) §1 G3 = PASS + 첫 화이트리스트 PR 개시.

---

## 5. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 양식 신설 (점검 미실시, PENDING). M2 만 인프라 선행으로 DONE 처리. |
