# 레이아웃 매핑: Sobo42_1 (입금현황 — 년월별 변형) → 모던 `/settlement/cash-status?variant=sdate` [C5 Phase 1]

> 본 노트는 [`Sobo42_cash.md`](Sobo42_cash.md) 의 **년월별 변형 diff 만** 기록한다. 위젯/이벤트는 본 폼과 동일.

DEC-019 — 변형 차이는 코드 분기 금지, 단일 모던 컴포넌트 + `?variant=sdate` 데이터 주도 분기.

## 0. 입력 산출물

- 변형 본 폼: [`tools/.../legacy_source_root/Subu42_1/Sobo42_1.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu42_1/Sobo42_1.html) + `.form.json` + `.tree.json` + `.pas_analysis.json`
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu42_1.dfm`](../../legacy_delphi_source/legacy_source/Subu42_1.dfm)
- 원 pas: [`legacy_delphi_source/legacy_source/Subu42_1.pas`](../../legacy_delphi_source/legacy_source/Subu42_1.pas) — `Select Gdate, Sum26..28 From T2_Ssub` (≈297), `Select Sdate,Gdate,Gssum From T5_Ssub` (≈349)
- 본 폼 매핑: [`Sobo42_cash.md`](Sobo42_cash.md)

## 1. 핵심 차이 (Sobo42 vs Sobo42_1)

| 분류 | Sobo42 본 (거래처별) | Sobo42_1 (년월별) |
| --- | --- | --- |
| 집계 키 (GROUP BY) | `Hcode` | `Gdate` (또는 `Sdate`) |
| 첫 컬럼 | `HCODE` 코드 + `HNAME` 출판사명 | `SDATE` 년월 (단일) |
| 추가 컬럼 | (없음) | `GPSUM` 당월합계 (전월미수+당월금액+세액 누계) |
| 데이터셋 | `Base10.T4_Sub21/22` (전역 DataModule) | 폼 로컬 `T4_Sub21` ClientDataSet (`mSqry := nil`) |
| 검색 콤보 위치 | Panel001 TabOrder 2 | Panel001 TabOrder 3 (`Edit108`) — 콤보 한 칸 추가 |

## 2. 컬럼 매핑 (DBGrid — 차이 부분만)

| dfm FieldName | Sobo42 본 | Sobo42_1 (변형) | 모던 컬럼 (variant=sdate) | data-legacy-id |
| --- | --- | --- | --- | --- |
| `SDATE` | (없음) | 년월 | `<th>년월</th>` (1열로 이동) | `Sobo42_1.DBGrid.SDATE` |
| `HCODE/HNAME` | 코드/출판사명 | (없음) | (variant=sdate 시 미노출) | — |
| `GSUMX` | 전일미수 | 전일미수 | `<th>전월미수</th>` (SUM) | `Sobo42_1.DBGrid.GSUMX` |
| `GOSUM` | 당월금액 | 당월금액 | `<th>당월금액</th>` (SUM) | `Sobo42_1.DBGrid.GOSUM` |
| `GBSUM` | 세액 | 세액 | `<th>세액</th>` (SUM) | `Sobo42_1.DBGrid.GBSUM` |
| `GPSUM` | (없음) | 당월합계 | `<th>당월합계</th>` (SUM, 변형 전용) | `Sobo42_1.DBGrid.GPSUM` |
| `GSSUM` | 합계금액 | 합계금액 | `<th>합계금액</th>` (SUM) | `Sobo42_1.DBGrid.GSSUM` |
| `GDATE` | 입금일 | 입금일 | `<th>입금일</th>` | `Sobo42_1.DBGrid.GDATE` |
| `GSUSU` | 입금액 | 입금액 | `<th>입금액</th>` (SUM) | `Sobo42_1.DBGrid.GSUSU` |
| `GSUMY` | 당월미수액 | 당월미수액 | `<th>당월미수</th>` (SUM) | `Sobo42_1.DBGrid.GSUMY` |

## 3. 데이터 흐름 (`Subu42_1.pas` 인용)

```
SELECT Gdate, Sum(Sum26) AS GOSUM, Sum(Sum27) AS GBSUM, Sum(Sum28) AS GSSUM
  FROM T2_Ssub
 WHERE Hcode = ?              -- 거래처는 검색 입력
 GROUP BY Gdate
 ORDER BY Gdate

LEFT JOIN T5_Ssub
       ON Hcode = ?
   GROUP BY Gdate
```

## 4. 데이터 주도 분기 — contract `customer_variants` 항목

```yaml
# settlement_billing.yaml (T3 발췌)
customer_variants:
  cash_status_sdate:
    description: "년월별 입금현황 변형 (Sobo42_1)"
    columns_diff:
      first_column: { from: "HCODE/HNAME", to: "SDATE" }
      additional:
        - { field: "GPSUM", title: "당월합계" }
    dataset_scope: "form_local"   # T4_Sub21
    nForm: "42_1"
    group_by: "Gdate"
```

## 5. 회귀 가드 체크리스트

- [ ] 단일 컴포넌트 — `if (variant === 'sdate') ...` 의 분기는 컬럼 헤더/SUM 푸터에만 한정
- [ ] DOM 의 `data-legacy-id` 가 본 폼은 `Sobo42.*`, 변형은 `Sobo42_1.*` 로 정확히 분리
- [ ] `GPSUM` 컬럼은 variant=sdate 일 때만 노출 — `?variant=hcode` 시 숨김
- [ ] 집계 결과(SUM 푸터) 가 SQL 결과와 일치

## 6. 참조

- DEC-019: customer_variants — 코드 분기 금지
- DEC-028: dfm 산출물 영구 입력
- 본 폼: [`Sobo42_cash.md`](Sobo42_cash.md)
- contract: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml)
- 선례: `Sobo23_1.md` (반품 라인 다이얼로그 변형 패턴)
