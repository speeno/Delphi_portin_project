# 레이아웃 매핑: Sobo47 (청구금액 년월) → 모던 `/settlement/period` [C5 Phase 1]

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, 컬럼) 을 모던 컴포넌트로 1:1 매핑.

## 0. 입력 산출물

- 본 폼: [`tools/.../legacy_source_root/Subu47/Sobo47.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu47/Sobo47.html) + `.form.json` + `.tree.json` + `.pas_analysis.json`
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu47.dfm`](../../legacy_delphi_source/legacy_source/Subu47.dfm)
- 원 pas: [`legacy_delphi_source/legacy_source/Subu47.pas`](../../legacy_delphi_source/legacy_source/Subu47.pas) — `Select Gdate, Sum(Sum26..28) From T2_Ssub Group By Gdate` (271~316), `Tong20.Srart_47_01` 보고 호출
- 모던 라우트(예정 — T6 신설): `/settlement/period/page.tsx`
- 계약: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) `list_period_summary` 액션

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유

레거시 `Sobo47` = 단일 검색 폼 → "거래처(`Edit105`)" + "년월 시작·종료" 입력 → `T2_Ssub` 월별 합계 → 보고 모듈(`Tong20.Srart_47_01`) 로 캐스케이드. 모던은:

- 검색 영역 → 거래처 + 시작년월·종료년월 입력
- 결과 → `<DataGrid>` 4컬럼(년월·당월금액·세액·합계금액) + `<th>비고</th>`
- 보고 모듈은 모던에서 화면 결과 그 자체 (인쇄 후속은 C7)

## 2. dfm 영역 인벤토리 (tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | Edit103/104/105, Button101 | `<section>` |
| 결과 영역 | (DBGrid in body) | n/a | 5컬럼 | `<DataGrid>` |
| 데이터셋 | `DataSource1` | n/a | 1 | 백엔드 |

## 3. 검색 패널 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (`/settlement/period`) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Panel001` | TFlatPanel | 검색 패널 컨테이너 | `<section>` | `Sobo47.Panel001` |
| n/a | `Edit103` | TFlatEdit | 거래처코드 | `<CustomerSearchInput id="hcode">` | `Sobo47.Edit103` |
| 5 | `Edit104` | TFlatMaskEdit | 시작년월 (mask `!9999.!99`) | `<Input id="from" type="month">` | `Sobo47.Edit104` |
| 6 | `Edit105` | TFlatMaskEdit | 종료년월 | `<Input id="to" type="month">` | `Sobo47.Edit105` |
| n/a | `Button101` | TFlatButton | 조회 (`Button101Click`) | `<Button onClick=onSearch>조회</Button>` | `Sobo47.Button101` |

## 4. 결과 그리드 매핑 (DBGrid)

| dfm FieldName | 한글 컬럼 | 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GDATE` | 일자(년월) | YYYYMM 키 | `<th>년월</th>` | `Sobo47.DBGrid.GDATE` |
| `GSUMX` | 당월금액 | `Sum(Sum26)` | `<th>당월금액</th>` (SUM 푸터) | `Sobo47.DBGrid.GSUMX` |
| `GSUMY` | 세액 | `Sum(Sum27)` | `<th>세액</th>` (SUM 푸터) | `Sobo47.DBGrid.GSUMY` |
| `GSSUM` | 합계금액 | `Sum(Sum28)` 또는 `GSUMX+GSUMY` | `<th>합계금액</th>` (SUM 푸터) | `Sobo47.DBGrid.GSSUM` |
| `NAME1` | 비고 | 거래처/특이사항 | `<th>비고</th>` | `Sobo47.DBGrid.NAME1` |

## 5. 데이터 흐름 (`Subu47.pas` 271~316 인용)

```
SELECT Gdate, Sum(Sum26) AS GSUMX, Sum(Sum27) AS GSUMY, Sum(Sum28) AS GSSUM
  FROM T2_Ssub
 WHERE Hcode = ? AND Gdate BETWEEN ? AND ?
 GROUP BY Gdate
 ORDER BY Gdate
→ ClientDataSet `nSqry` 누적
→ Tong20.Srart_47_01 (레거시 보고 — 모던은 화면 결과 자체)
```

## 6. out-of-scope 위젯

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 보고 호출 | `Tong20.Srart_47_01` (런타임) | 모던 화면 표시로 흡수 (C7 인쇄 후속) |
| 추가 검색 콤보 | (있다면 Edit106~) | Phase 1 = 거래처+년월 단일 |

## 7. Deltas — 모던 신설 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | DataGridPager | `/settlement/period` | DEC-024 페이지네이션 표준 |
| 모던 신규 | 합계 푸터 (당월·세액·합계 SUM) | DataGrid `<tfoot>` | 레거시 보고서가 합산 출력하던 의미 흡수 |
| 모던 신규 | 마감 후 행 readonly 배지 | 결과 그리드 | DEC-031 (`Yesno='1'` 행은 편집 불가 표시) |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 | 비고 |
| --- | --- | --- |
| `FormActivate` | `useEffect` mount | C6 패턴 |
| `Button101Click` | `onSearch` → `settlementApi.listPeriodSummary()` | |
| `Edit104Change` / `Edit105Change` | `setFromMonth` / `setToMonth` | |

## 9. 변형 차이

`Subu47` 단일 폴더 — 본 폼에 variant 없음. contract `customer_variants` 에 "Sobo47 variant 0건" 단언 기록.

## 10. 회귀 가드 체크리스트

- [ ] 본 노트 §3·§4 의 모든 `data-legacy-id` 가 모던 페이지에 존재 (총 ~10개):
  - 검색: `Sobo47.Panel001`, `Edit103/104/105`, `Button101`
  - 그리드: `Sobo47.DBGrid.{GDATE,GSUMX,GSUMY,GSSUM,NAME1}`
- [ ] 합계 SUM 푸터가 SQL 합계 결과와 일치 (레거시 캡처 1~2건과 ±0 차이)
- [ ] DEC-028 §3 "버리는 정보" (픽셀 left/top/width/height/Color) 미존재

## 11. 참조

- DEC-024: 페이지네이션 표준
- DEC-028: dfm 산출물 영구 입력
- contract: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml)
- 본 폼 카드: [`analysis/screen_cards/Sobo45.md`](../screen_cards/Sobo45.md) — C5 화면군 통합 카드
- 선례: `Sobo61.md`, `Sobo62.md` (보고서 패턴)
