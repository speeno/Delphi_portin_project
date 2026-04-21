# C7 Phase 3 — SME 협의 양식 (G1)

**ID**: C7-PHASE3-SME-REVIEW
**일자**: 2026-04-21 (양식 동결, 인터뷰 미실시)
**상태**: 게이트 G1 — **PENDING (미실시)**
**연관**: [`docs/phase3-print-gate.md`](../../docs/phase3-print-gate.md), [`migration/coverage/frf-html-form-catalog.md`](../../migration/coverage/frf-html-form-catalog.md), [`migration/coverage/frf-to-screen-usage-map.md`](../../migration/coverage/frf-to-screen-usage-map.md)

---

## 0. 인터뷰 목적

운영 SME(고객/내부 운영팀) 와 합의해 1744 자산 중 **운영 결합 후보 form_id (≤ 5건/sprint)** 의 우선순위와 양식 변경 빈도를 동결한다. 본 양식이 채워져야 게이트 G1 PASS.

---

## 1. 인터뷰 메타

| 항목 | 값 |
|---|---|
| 인터뷰 대상자 | (TBD — 예: 운영팀 / 사업본부 / 키 거래처 SME) |
| 인터뷰 일시 | (TBD) |
| 진행자 | (TBD) |
| 소요 시간 | ≥ 60 분 (필수) |
| 회의록 작성자 | (TBD) |
| 합의 방식 | 라이브 합의 + 24h 내 e-mail 확인 |

---

## 2. 인터뷰 어젠다

1. (10 분) 매핑 표 [`migration/coverage/frf-to-screen-usage-map.md`](../../migration/coverage/frf-to-screen-usage-map.md) §1 의 P0~P3 우선순위 검토.
2. (15 분) 1744 자산 중 **고객 복제본 1646건** (WeLove_FTP/도서유통-*) 의 정본 지정 정책 합의.
3. (15 분) **양식 변경 빈도** 합의 — Report_4_51(청구서) 137 복제 / Report_2_13(거래명세) 123 복제 등이 거래처별로 얼마나 자주 바뀌는가? 운영 결합이 의미 있는가?
4. (10 분) **form_id 후보 ≤ 5건/sprint** 합의 — 이번 sprint 결합 대상 1차 동결.
5. (10 분) 위험·정합 합의 — DEC-039 (자동 변환 0) 영속, opt-in 만 추가.

---

## 3. 합의 결과 표 (PENDING)

| form_id (.frf) | SME 정본 합의 | 양식 변경 빈도 (분기당) | 우선순위 (P0~P3) | 결합 sprint | 비고 |
|---|---|---|---|---|---|
| `Report_4_51.frf` (Sobo46 청구서) | (TBD ✓/✗) | (TBD) | P0 | (TBD) | 137 복제, 운영 사용 중 |
| `Report_2_11.frf` (Sobo49 세금) | (TBD) | (TBD) | P0 | (TBD) | 67 복제, 운영 사용 중 |
| `Report_2_13.frf` (거래명세) | (TBD) | (TBD) | P0 | (TBD) | 123 복제, 운영 사용 중 |
| `Report_2_19.frf` (세금 변형) | (TBD) | (TBD) | P0 | (TBD) | 20 복제 |
| `Report_1_22.frf`~`1_25` (라벨 4종) | (TBD) | (TBD) | P1 | (TBD) | 라벨, label_service 옵트인 |

---

## 4. 게이트 PASS 기준 (DoD)

- [ ] §3 표의 form_id 후보 ≥ 1 행 SME 합의 ✓
- [ ] 변경 빈도 합의 (`분기당 변경 ≤ 1회` 인 form 만 P0/P1)
- [ ] 다음 sprint 결합 대상 1건 이상 동결
- [ ] 회의록 e-mail 1차 회신 받음 (24h 내)

3 조건 모두 만족 → [`docs/phase3-print-gate.md`](../../docs/phase3-print-gate.md) §1 G1 = PASS 표기 + G2 단계로 진행.

---

## 5. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-21 | 양식 신설 (인터뷰 미실시, PENDING). |
