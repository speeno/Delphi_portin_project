# 레이아웃 매핑: Sobo42 (입금현황 — 거래처별) → 모던 `/settlement/cash-status` [C5 Phase 1]

DEC-028 의무. 본 폼은 거래처(Hcode) 키 집계 보고. 변형 [`Sobo42_1_cash.md`](Sobo42_1_cash.md) 는 년월(Sdate) 키 집계 — `customer_variants` 로 분기.

## 0. 입력 산출물

- 본 폼: [`tools/.../legacy_source_root/Subu42/Sobo42.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu42/Sobo42.html) + `.form.json` + `.tree.json` + `.pas_analysis.json`
- 변형: [`Sobo42_1_cash.md`](Sobo42_1_cash.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu42.dfm`](../../legacy_delphi_source/legacy_source/Subu42.dfm)
- 원 pas: [`legacy_delphi_source/legacy_source/Subu42.pas`](../../legacy_delphi_source/legacy_source/Subu42.pas) — `Select Hcode, Sum26..28 From T2_Ssub` (≈278), `Select * From T5_Ssub` (≈324)
- 모던 라우트(예정 — T6 신설): `/settlement/cash-status/page.tsx?variant=hcode`
- 계약: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) `cash_status` 액션

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유

레거시 `Sobo42` = 거래처별 입금/미수 현황 보고. 모던은:

- 검색 영역(거래처·기간) → `<section>`
- 결과 그리드(9컬럼: 코드·출판사명·전월미수·당월금액·세액·합계금액·입금일·입금액·당월미수액)
- 변형 `Sobo42_1` (년월별) 은 **같은 페이지에 `?variant=sdate` 토글** — 컬럼 1개 다름 (`HCODE/HNAME` ↔ `SDATE`)

## 2. dfm 영역 인벤토리 (tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 | `Panel001` (TFlatPanel) | 0 | Edit101/107/108 + Button101/201/700 | `<section>` |
| 결과 영역 | (DBGrid in body) | n/a | 9컬럼 | `<DataGrid>` |
| 데이터셋 | `DataSource1` | n/a | 1 | 백엔드 |

## 3. 검색 패널 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (`/settlement/cash-status`) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| n/a | `Edit101` | TFlatMaskEdit | 기준년월 (mask `!9999.!99`) | `<Input id="month" type="month">` | `Sobo42.Edit101` |
| 1 | `Edit107` | TFlatEdit | 거래처코드 (검색) | `<CustomerSearchInput id="hcode">` | `Sobo42.Edit107` |
| 2 | `Edit108` | TFlatEdit | 거래처명 표시 | (응답 customer_name) | `Sobo42.Edit108` |
| n/a | `Button101` | TFlatButton | 조회 (`Button101Click`) | `<Button onClick=onSearch>조회</Button>` | `Sobo42.Button101` |
| n/a | `Button201` | TFlatButton | 추가 액션 (`Button201Click`) | (Phase 1 미사용) | `Sobo42.Button201` |
| n/a | `Button700` | TFlatButton | 출력/엑셀 (`Button700Click`) | (Phase 2 — C7 인쇄) | `Sobo42.Button700` |

## 4. 결과 그리드 매핑 (DBGrid)

| dfm FieldName | 한글 컬럼 | 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `HCODE` | 코드 | 거래처 코드 | `<th>코드</th>` | `Sobo42.DBGrid.HCODE` |
| `HNAME` | 출판사명 | 거래처명 | `<th>출판사명</th>` | `Sobo42.DBGrid.HNAME` |
| `GSUMX` | 전일미수 | 전월 미수금 | `<th>전월미수</th>` (SUM) | `Sobo42.DBGrid.GSUMX` |
| `GOSUM` | 당월금액 | `Sum(Sum26)` | `<th>당월금액</th>` (SUM) | `Sobo42.DBGrid.GOSUM` |
| `GBSUM` | 세액 | `Sum(Sum27)` | `<th>세액</th>` (SUM) | `Sobo42.DBGrid.GBSUM` |
| `GSSUM` | 합계금액 | `Sum(Sum28)` 또는 `GOSUM+GBSUM` | `<th>합계금액</th>` (SUM) | `Sobo42.DBGrid.GSSUM` |
| `GDATE` | 입금일 | 마지막 입금일 (T5_Ssub join) | `<th>입금일</th>` | `Sobo42.DBGrid.GDATE` |
| `GSUSU` | 입금액 | 당월 입금 누계 | `<th>입금액</th>` (SUM) | `Sobo42.DBGrid.GSUSU` |
| `GSUMY` | 당월미수액 | `GSUMX + GSSUM - GSUSU` | `<th>당월미수</th>` (SUM) | `Sobo42.DBGrid.GSUMY` |

## 5. 데이터 흐름 (`Subu42.pas` 인용)

```
SELECT Hcode, Sum(Sum26) AS GOSUM, Sum(Sum27) AS GBSUM, Sum(Sum28) AS GSSUM
  FROM T2_Ssub
 WHERE Sdate = ?
 GROUP BY Hcode

LEFT JOIN T5_Ssub
       ON Hcode = ?
      AND Gdate BETWEEN ?  AND ?

→ 클라이언트에서 GSUMY = GSUMX + GSSUM - GSUSU 계산
```

## 6. out-of-scope 위젯

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 출력/엑셀 | Button700 | C7 인쇄 후속 |
| 추가 액션 | Button201 | Phase 1 미사용 |

## 7. Deltas — 모던 신설 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | DataGridPager | 결과 영역 | DEC-024 페이지네이션 표준 |
| 모던 신규 | 변형 토글 (거래처/년월) | URL `?variant=hcode\|sdate` | Sobo42_1 통합 (`customer_variants`) |
| 모던 신규 | 9컬럼 SUM 푸터 | DataGrid `<tfoot>` | 보고서 의미 흡수 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 | 비고 |
| --- | --- | --- |
| `FormActivate` | `useEffect` mount | C6 패턴 |
| `Button101Click` | `onSearch` → `settlementApi.cashStatus({variant:'hcode'})` | |
| `Edit101Change` | `setMonth` | |

## 9. 변형 차이 — Sobo42 본 vs Sobo42_1

| 항목 | Sobo42 (본) | Sobo42_1 (변형) |
| --- | --- | --- |
| 집계 키 | `Hcode` (거래처별) | `Sdate` (년월별) |
| 첫 컬럼 | `HCODE/HNAME` | `SDATE` (년월) |
| 추가 컬럼 | (없음) | `GPSUM` 당월합계 (전월미수+당월금액+세액 누계 — 변형 추가) |
| 데이터셋 | `Base10.T4_Sub21/22` | 폼 로컬 `T4_Sub21` ClientDataSet (주석된 mSqry) |

> 모던은 단일 컴포넌트 + `variant` query param 으로 분기. 컬럼 헤더만 데이터 주도로 변경.

## 10. 회귀 가드 체크리스트

- [ ] 본 노트 §3·§4 의 모든 `data-legacy-id` 가 모던 페이지에 존재 (총 ~15개):
  - 검색: `Sobo42.Edit101/107/108`, `Button101`
  - 그리드: `Sobo42.DBGrid.{HCODE,HNAME,GSUMX,GOSUM,GBSUM,GSSUM,GDATE,GSUSU,GSUMY}`
- [ ] 변형 토글 시 `data-legacy-id` 가 `Sobo42_1.*` 로 정확히 변경 — `Sobo42_1_cash.md` 와 짝
- [ ] SUM 푸터 결과가 SQL 합계와 일치 (소수점·EUC-KR 디코딩 후 ±0)
- [ ] DEC-028 §3 "버리는 정보" 미존재

## 11. 참조

- DEC-019: customer_variants — 코드 분기 금지
- DEC-024: 페이지네이션 표준
- DEC-028: dfm 산출물 영구 입력
- 변형: [`Sobo42_1_cash.md`](Sobo42_1_cash.md)
- contract: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml)
- 선례: `Sobo61.md`, `Sobo62.md` (집계 보고서 패턴)
