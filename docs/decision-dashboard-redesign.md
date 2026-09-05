# 대시보드 재구성 설계 (DEC-236)

- 작성 2026-09-05 · 상태 **설계안(미승인)** · 관련 DEC-236, DEC-033, DEC-093, DEC-138
- 시각 산출물(목업 포함): https://claude.ai/code/artifact/72a30116-0ea3-4b23-ae34-361375b4b0e0

## 1. 문제

현행 대시보드(`components/dashboard/role-dashboard-view.tsx`)에서 시각적 비중이 가장 큰
카드 두 개가 실측이 아니다. `backend/app/services/stats_service.py` 기준:

| 카드 | 실제 계산 | 문제 |
|---|---|---|
| 물류 플로우 퍼널 | 6단계 전부 `in_total`·`out_total`·`ret_total` 의 뺄셈. `배송완료 = max(out-ret-(ret//2),0)` | 레거시 DB 에 배송 상태·시각이 없음 |
| 리드타임 분해 | `avg_days = (건수/건수) × 0.8` 또는 `× 1.2` | 일 단위와 무관한 비율 |
| 미처리건 KPI | `max(out_total - ret_total, 0)` | 미처리 건수가 아님 |
| 창고 IoT | `_iot_demo_snapshot()` — 서버명 해시 | 연결된 센서 없음 |

운영자가 이 숫자를 근거로 판단하면 잘못된 결론에 이른다. **없는 데이터를 표시하지 않는 것**이
이 설계의 첫 번째 원칙이다.

## 2. 화면 구성 — 한 화면 세 구역

위에서 아래로 **① 지금 처리해야 할 일 → ② 오늘 실적 → ③ 돈과 재고**.
모든 숫자는 클릭하면 그 상태로 걸러진 목록 화면으로 이동한다(숫자 → 일감).

### ① 지금 처리해야 할 일 (Action Queue)
| 카드 | 정의 | 이동 |
|---|---|---|
| 미완료 출고 전표 | 전표 `MAX(Yesno)` 가 대기('')·접수('0') | `/outbound/orders` |
| 접수 후 미완료 반품 | 반품 `Yesno='1'`(접수), DEC-093 | `/returns/status` |
| 오늘 입고 접수 | 당일 입고 전표 건수 | `/inbound/receipts` |
| 명세서 미출력 | 완료 전표 중 인쇄 이력 없음 (3단계) | `/transactions/sales-statement` |

0건 카드는 배경을 가라앉혀 남은 일만 눈에 띄게 한다. 카드 왼쪽 3px 띠로 상태를 표시한다.

### ② 오늘 실적 (한 줄)
출고 건수 · 출고 금액 · 입고 건수 · 반품 건수 · 반품률. 기간 토글(오늘/이번 주/이번 달).

### ③ 돈과 재고 (2열)
- 미수 상위 5 거래처 + 합계 → `/settlement/outstanding` (`compute_outstanding_by_customer`)
- 재고 경고: 음수 재고 우선, 그다음 저회전 → `/inventory/status`, `/stats/book-turnover`

## 3. 카드별 데이터 출처

| 카드 | 출처 | 지금 가능 |
|---|---|---|
| 미완료 출고 전표 | `S1_Ssub` 상태 집계 | 신규 집계 |
| 접수 후 미완료 반품 | `S1_Ssub` (DEC-093) | 신규 집계 |
| 오늘 입고 접수 | `inbound_service.list_receipts` | 가능 |
| 출고 건수·금액 | `outbound_service.list_orders` | 건수 가능 |
| 반품률 | 위 두 값의 나눗셈 | 가능 |
| 미수 상위 거래처 | `settlement_service.compute_outstanding_by_customer` | 가능 |
| 저회전 도서 | `reports_service.get_book_sales` (scope B) | 가능 |
| 음수 재고 | Tong04 3소스 합 (DEC-138) | 신규 집계 |
| 명세서 미출력 | 인쇄 이력 저장 필요 | 3단계 |

신규 집계는 **파생 테이블 금지**(MySQL 3.23, DEC-033)에 따라 `count_grouped()` 로 작성한다.

## 4. 역할별 구성

컴포넌트는 하나, 역할 매트릭스(`lib/dashboard-role-matrix.ts`) 데이터만 다르게 한다.
고객사별 차이는 코드 분기 없이 `migration/contracts/*.yaml` 의 `customer_variants` 로 처리한다.

- **총판(T2_DIST)** — 미완료 출고·반품·입고 / 출고 건수·금액·반품률 / 미수 상위 / 재고 경고(음수 우선)
- **출판사(T2_PUB)** — 미완료 출고·반품 / 출고 금액·반품률 / 미수 상위 / 저회전 도서
- **일반(T3)** — 미완료 출고·오늘 입고 / 출고 건수 / 미수·재고 패널 없음 / 자주 쓰는 화면 바로가기
- **수퍼관리자(T1)** — 테넌트별 미완료 합계 / 로그인·계정 전환 현황 / 미수 합계 / 관리·감사 바로가기

## 5. 구현 단계

**1단계 — 지어낸 지표 제거·재배치 (프론트만)**
- 퍼널·리드타임 카드 제거(백엔드 라우트는 잠시 유지)
- 외부 위젯 9종 기본 레이아웃 해제 → 「위젯 추가」로 이동
- 미수 상위·저회전 도서 패널을 하단 2열로 재배치, 기간 토글·이동 링크 배선

**2단계 — 상태별 집계 신설 (설계의 핵심)**
- `GET /stats/dashboard/worklist` 신설: 출고 대기·접수·완료, 반품 접수 건수
- `count_grouped()` 로 전표 단위 집계 (파생 테이블 금지)
- `test/` 회귀 테스트 + `debug/probe_backend_all_servers.py` 스모크 행렬 등록
- 출고 금액 합계·반품률 추가

**3단계 — 남은 두 카드**
- 명세서 인쇄 이력 저장 → 「명세서 미출력」 카드
- 재고 음수 도서 집계 → 재고 경고 상단 고정
- 역할별 기본 레이아웃 확정 후 서버 저장 레이아웃 마이그레이션

## 6. 결정 필요

1. **명세서 미출력 카드** — 인쇄 이력을 새로 저장해야 한다. 포함할지.
2. **외부 위젯** — 기본 해제만 할지, 카탈로그에서도 감출지.
3. **기간 기본값** — 오늘 / 이번 주 / 이번 달.
4. **수퍼관리자 화면** — 위 안대로 갈지, 현행 감사 중심 구성을 유지할지.

## 7. 이미 반영된 것 (2026-09-05)

창고 IoT 감추기만 선반영했다(사용자 지시 "우선 감추기"). 삭제는 하지 않았다.
- `frontend/src/app/(app)/dashboard/layout.tsx` — `SHOW_IOT_TAB=false`
- `frontend/src/lib/dashboard-role-matrix.ts` — 총판·t3 `embeddedWidgets: []`
- `frontend/src/lib/dashboard-widget-registry.ts` — `hidden:true` + `DASHBOARD_WIDGET_PICKER_CATALOG`
- 라우트 `/dashboard/iot`·화면·백엔드 엔드포인트·SSE 스트림은 그대로
