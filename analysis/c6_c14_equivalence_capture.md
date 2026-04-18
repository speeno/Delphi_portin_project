# C6 ↔ C14 보고서 동등성 캡처 (1차)

> Contract: `migration/contracts/sales_inquiry.yaml` v1.0.0 — `equivalence.report`.
> 본 캡처는 1차 합격선 검증을 위한 *서비스 레이어* 동등성 (mock fixture 비교).
> 실 DB 기반 회귀는 T7 후속(통합 환경) 으로 이관(OQ-OUT-2 추적).

C6 가 C14(레거시 보고서 통합) 를 흡수하므로, 4개 화면 중
**판매 보고서 2건(Sobo61 도서별판매 / Sobo62 거래처판매)** 의 *수치 동등성*을
다음 두 케이스로 캡처한다.

---

## 캡처 1 — Sobo61 도서별 판매: 단일 도서 / 30일 범위

| 항목 | 레거시 (Subu61.qry1) | 신규 (`/api/v1/reports/book-sales`) | Δ |
|------|----------------------|--------------------------------------|----|
| Hcode 필터 | `WHERE Hcode='A0001'` | `?hcode=A0001` | 0 |
| 기간 | `Gdate BETWEEN '2026.04.01' AND '2026.04.30'` | `?dateFrom=2026-04-01&dateTo=2026-04-30` (서비스 normalize) | 0 |
| GROUP BY | `Gcode` | `Gcode` | 0 |
| 행 수(예시) | 1 | 1 | 0 |
| `giqut` (입고수) | 10 | 10 | 0 |
| `goqut` (출고수) | 5 | 5 | 0 |
| `gosum` (출고액) | 50,000 | 50,000 | 0 |
| `gpsum` (파지액 — Sg_Csum 보강) | 0 | 0 | 0 |

**결론**: GROUP BY 결과 + Sg_Csum 파지 보강 모두 동일 (mock fixture 기준).

검증 코드: `test/test_c6_inquiry_phase1.py::C6ReportsTests::test_tc_inq_006_book_sales_returns_rows` PASS.

---

## 캡처 2 — Sobo62 거래처별 판매: 다(多)거래처 / 30일 범위

| 항목 | 레거시 (Subu62.qry1) | 신규 (`/api/v1/reports/customer-sales`) | Δ |
|------|----------------------|--------------------------------------|----|
| 거래처 필터 | (없음 — 전체) | `?hcode=` 미지정 → 전체 | 0 |
| 기간 | 동일 | 동일 | 0 |
| GROUP BY | `Hcode, Gcode` | `Hcode, Gcode` | 0 |
| 행 수(예시) | 1 | 1 | 0 |
| `goqut` (출고수) | 5 | 5 | 0 |
| `gosum` (출고액) | 50,000 | 50,000 | 0 |
| `gjqut` (재고수) | 4 | 4 | 0 |
| `gjsum` (재고액) | 40,000 | 40,000 | 0 |

**결론**: hcode×gcode 단위 집계 동일 (mock fixture 기준).

검증 코드: `test/test_c6_inquiry_phase1.py::C6ReportsTests::test_tc_inq_007_customer_sales_returns_rows` PASS.

---

## OQ-OUT-2 (Sg_Csum 트리거 / 업데이트 시점) 추적

- 본 캡처는 `Sg_Csum` 가 *조회 시점에 이미 갱신되어 있다*는 가정 하에 검증.
- 갱신 시점/트리거(레거시 측) 의 정확한 경로는 1차 범위 외 — `legacy-analysis/open-questions.md::OQ-OUT-2` 로 이관.
- 통합 회귀 시점에 두 보고서를 *동일 시점 스냅샷* 으로 비교하면 본 캡처와 동등성 유지 가능.

## 캡처 한계 (1차 동결)

- 실 MySQL 인덱스 영향(정렬 안정성), `Ocode='A'/'B'` 분기, 다(多) 지사 합산 등은
  T7 후속(실 데이터 회귀) 에서 보강.
- 5축 검증 중 *부수효과(write side effect)* 는 본 보고서 화면들이 read-only 이므로
  S1_Memo UPSERT 만 별도 캡처(test_tc_inq_003/004) 하여 충족.
