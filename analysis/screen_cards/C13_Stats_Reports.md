# 시나리오 카드: C13 — 통계/리포트 확장

_생성: 2026-04-20 — C10 이후 확장 라인 v0.1 (골격)_

> **사용자 명시 제약**: 본 사이클은 **외부 시스템 연동 제외**. 즉 BI 도구(Tableau/PowerBI) 직결, 외부 ETL 파이프라인 송출, 외부 데이터 웨어하우스 연동은 본 페이즈 out-of-scope.

## 0. 한눈 요약

- **시나리오 ID**: C13 (Stats/Reports — C10 의 C13 세션·권한 흡수 시나리오와 다른 별도 확장 라인)
- **명칭**: 통계/리포트 확장
- **상태**: PENDING (스코프 정의 완료, 실행 대기)
- **단계 (stages)**: 6 (확장 라인)
- **레거시 등가**: Sobo50/51/52/53/54/55 (기간별 매출/매입/거래원장/판매분석 등 — Phase 1 미포팅)
- **선행 의존**: C5 (정산 마감) + C10 (권한 매트릭스) 완료

## 1. 범위

| 항목 | 내용 |
|---|---|
| 신규 화면 | 기간별 매출 분석 / 거래처별 판매 분석 / 도서별 회전율 / 분기·반기·연간 손익 미니 대시보드 (4 화면) |
| 신규 엔드포인트 | `/api/v1/stats/sales-period`, `/stats/customer-analysis`, `/stats/book-turnover`, `/stats/quarterly-summary` |
| 차트 라이브러리 | Recharts (기존 라이센스 무료, React 통합) — 단일 선택 (DEC-019 단일 원천) |
| Export | CSV / Excel (xlsx) / PDF (WeasyPrint, DEC-037 재사용) — 외부 BI 직결 ❌ |
| 권한 | F50/F51/F52/F53 = 통계 가드 (legacy-analysis/permission-keys-catalog.md 등록) |

## 2. 산출물 (v0.1)

- `migration/contracts/stats_reports.yaml` v0.1 — 4 신규 엔드포인트 + customer_variants
- `analysis/handlers/c13_stats.md` — 레거시 Sobo5x 의 SQL 패턴 인덱싱 (통계용 GROUP BY/SUM 쿼리)
- `test/test_c13_stats_phase1.py` — 통계 정확성 + 권한 가드 + 기간 경계 검증

## 3. DoD

1. 4 신규 화면 모두 PermissionGuard (DEC-041) + 표준 에러 응답 정합
2. 신규 SQL 0 정책 검토 — 기존 `s1_ssub_service` / `r2_rsub_service` / `transactions_service` 의 SELECT 재해석 가능 여부 우선 확인 (DEC-040 룰 확장)
3. CSV/Excel/PDF Export 가 모두 동일 데이터 (ETag 정합)
4. 4 server (138/153/154/155) 모두 mysql3 호환 — `axis_data` probe 신규 4 그룹 등록 (DEC-033)

## 4. 결정 게이트 (의존 OQ/DEC)

- **OQ-STAT-1 (신규)**: 통계 데이터 시간 정합 — 일별/주별/월별 마감 시점 (정산 마감 후 즉시 vs T+1)
- **DEC-019 / DEC-040 / DEC-041 의존**: 단일 원천 + 신규 SQL 0 + C13 표준 응답 코드
- **외부 시스템 연동 제외**: BI/ETL/DW 직결은 별도 사이클 (외부 시스템 연동 합의 트리거 시)

## 5. 변경 이력

- 2026-04-20 — v0.1 골격 (C10 이후 확장 라인)
