# C7 Phase 3 — B1(자체 파서) vs B4(빌드타임 변환 + IR) ROI (G2)

**ID**: C7-B1-VS-B4-ROI
**일자**: 2026-04-21 (양식 동결, 회의 미실시)
**상태**: 게이트 G2 — **PENDING (미실시)**
**연관**: [`docs/phase3-print-gate.md`](../../docs/phase3-print-gate.md), [`analysis/research/c7_b4_poc_1day_report.md`](./c7_b4_poc_1day_report.md), [`analysis/research/c7_oss_shortlist.md`](./c7_oss_shortlist.md), [`analysis/research/c7_nofr_go_no_go_review_20260420.md`](./c7_nofr_go_no_go_review_20260420.md)

---

## 0. 배경

B4 PoC ([`c7_b4_poc_1day_report.md`](./c7_b4_poc_1day_report.md)) 가 1744 자산 변환을 완료했으나, **운영 결합 1건만** ([`Report_1_21.ir.json`](../../도서물류관리프로그램/backend/app/services/print_templates/auto/Report_1_21.ir.json)). DEC-048 의 Phase 3 게이트 통과 여부는 본 ROI 비교에 의존.

| 옵션 | 정의 |
|---|---|
| **B1 자체 파서** | 운영 코드에 .frf → HTML 자체 파서 신설 (트랙 신설 = `T-B5`). 운영 결합 = 모든 form 자동. |
| **B4 빌드타임 + IR** | 현 PoC 그대로. 1744 IR 산출은 빌드타임 1회. 운영 결합은 per-form 화이트리스트 PR(opt-in). |

---

## 1. 회의 메타

| 항목 | 값 |
|---|---|
| 참석자 | (TBD — 메인개발자 + 사용자 + 운영 SME) |
| 일시 | (TBD) |
| 진행자 | (TBD) |
| 회의록 | (TBD) |

---

## 2. ROI 비교 표 (양식)

비용·이득은 운영 결합 form **5건 (P0/P1 합산)** 기준.

| 축 | B1 자체 파서 | B4 빌드타임 + IR (현행) |
|---|---|---|
| 초기 개발 비용 | High (파서 RFC 4 ~ 6 주, fastrep_decoder 0.6.x 의 1408 경고 흡수) | None (PoC 완료 산출물 그대로 활용) |
| Form 1건 결합 비용 | Low (자동 — 모든 form 즉시 사용) | Low (화이트리스트 PR 1행 + IR 복사) |
| 회귀 위험 | High (DEC-039 정책 충돌, 자동 변환이 운영 영역 침투) | Low (opt-in, 폴백 보장, DEC-039 정합) |
| 양식 변경 시 추적 | (TBD) | per-form PR 단위 (감사 추적 ✓) |
| 정합도 (legacy 1:1) | (TBD) | quality 점수 평균 binding 0.57 / coord 0.99 — HIGH 996/1744 |
| Phase 4 확장성 | High (모든 form 자동 결합) | Mid (화이트리스트 누적 필요) |
| 권장 시나리오 | 양식 변경 빈도 ≥ 분기 1회 + 결합 form ≥ 50건 | 양식 변경 빈도 ≤ 분기 1회 + 결합 form ≤ 20건 |

---

## 3. 결정 (PENDING)

```text
□ B1 채택 → T-B5 트랙 신설 + DEC-051 등록 + DEC-039 갱신
□ B4 채택 → 본 게이트 G2 PASS + DEC-050 (per-form 화이트리스트 옵트인) 시행
□ 보류 → 다음 sprint 재검토
```

**잠정 권고 (PoC 결과 기반)**: §2 의 "양식 변경 빈도 ≤ 분기 1회 + 결합 form ≤ 20건" 가정이 [`c7_phase3_sme_review.md`](./c7_phase3_sme_review.md) 의 G1 결과로 확인되면 **B4 채택** 이 회귀 비용·DEC-039 정합 측면에서 우월. 가정이 깨지면 **B1 채택** 재검토.

---

## 4. 게이트 PASS 기준 (DoD)

- [ ] §2 비교 표 모든 행 채움
- [ ] §3 결정 1개 체크 (B1/B4/보류)
- [ ] B4 채택 시 → DEC-050 등록 + 본 게이트 G2 = PASS 표기
- [ ] B1 채택 시 → DEC-051 등록 + T-B5 트랙 신설

---

## 5. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 양식 신설 (회의 미실시, PENDING). |
