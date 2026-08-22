# 레이아웃 매핑: Sobo34 (기간별재고원장) — 재고현황 화면 정본화

DEC-028 의무 — dfm→(영역, 위젯 ID, DBGrid 컬럼, 이벤트) 1:1 매핑. 픽셀/폰트/색상 제외.

> **배경(2026-08-22 운영 요청)**: "원장관리의 재고현황 화면을 레거시 화면에 맞춰 구성해달라."
> 현행 `/inventory/status`(Sobo44_inv)는 **전용 백엔드가 없어 도서별수불원장(Sobo31) API 를
> 빌려 쓰는 임시 구현**이고, 기간별재고원장(Sobo34)은 커버리지 감사의 `missing_forms` 다.
> 본 문서는 그 포팅을 위한 정본 분석이다.

## 0. 입력 산출물 (출판 빌드 정본)

- dfm: `WeLove_FTP/도서유통-New/도서유통/한국도서유통/출판/MySQL/Subu34.dfm` (caption `기간별재고원장`)
- pas: 같은 폴더 `Subu34.pas` (2,259줄) — `Button102Click`(상단, L298~1221) /
  `Button103Click`(하단, L1222~2063) / `DataSource1DataChange`(L2201, 상단 선택 → 하단 조회)

> **변형 주의**: `도서유통-New/Subu34.dfm` 등 다른 빌드는 컬럼이 8개(전일재고·입고·출고·증정·
> 반품·폐기·현재재고)로 **다르다**. 스크린샷과 일치하는 것은 위 출판 빌드 경로 하나뿐이다.
> `도서유통-New/도서유통/Subu34.dfm` 은 caption 자체가 「정품재고(폐기)」로 다른 화면이다.

## 1. 화면 구조

| 영역 | dfm | 역할 |
| --- | --- | --- |
| 검색 패널 | `Edit101/102`(거래일자 from~to)·`CheckBox1`(전체도서)·`Edit111`(도서명)·`Edit103/105`(도서코드 구간)·`Panel102`(도서명/본사도서/창고도서 토글) | 조회 조건 |
| 상단 `DBGrid101` | **분류 단위** 롤업 | 분류별 재고 |
| 하단 `DBGrid201` | 상단 선택 분류의 **도서 단위** | 도서별 재고 |

> 운영 요청으로 **검색은 「도서명 또는 코드」 단일 칸**(미지정 시 전체)으로 단순화한다 —
> `Edit103/105` 구간 입력 폐지. (2026-08-22 선반영: 제품 커밋 `7b45aeb`)

## 2. 그리드 컬럼 (상·하단 동일, dfm FieldName 기준)

| 표시 | FieldName | 의미 |
| --- | --- | --- |
| 분 류 명 / 도 서 명 | `GNAME` | 상단=분류명(G4_Gbun), 하단=도서명 |
| 전재고 | `GSUMX` | 기간 **시작 직전** 시점 정품재고 |
| 입고 | `GIQUT` | 기간 입고 |
| 반입 | `GISUM` | 기간 반품입고 (※ 스크린샷의 「반납」은 오독, 실제 「반입」) |
| 출고 | `GOQUT` | 기간 출고 |
| 증정 | `GJQUT` | 기간 증정 |
| 반품 | `GBQUT` | 기간 반품 |
| 폐기 | `GPQUT` | 기간 폐기 |
| 변경 | `GPSUM` | 기간 이동/변경 |
| 현재고 | `GSUMY` | 기간 **말** 시점 정품재고 |
| 재고(반) | `GSSUM` | 반품재고 잔량 |

운영 요청 컬럼 순서(상단): `도서코드 · 도서명 · 정가 · 전재고 · 입고 · 출고 · 증정 · 반품 ·
폐기 · 변경 · 현재고 · 재고(반)` — 레거시 대비 **「반입」 제외**, **도서코드·정가 추가**.

## 3. 누적 분기표 (Subu34.pas L415~484, `Scode`=St5 / `Gubun`=St3 / `Pubun`=St4)

```
Scode='Y' (입고계열)
  Pubun='이동'                 → Gpsum += q     (변경)
  Gubun='반품' and Pubun='반품' → Giqut += q     (입고)
  Pubun='반품'                 → Gisum += q     (반입)
  Gubun='입고'                 → Giqut += q     (입고)
그 외(출고계열)
  Pubun='증정'                 → Gjqut += q     (증정)
  Gubun='출고'                 → Goqut += q     (출고)
  Gubun='폐기'                 → Gpqut += q, 그리고 Pubun='비품'? Gjsum += q : Gbsum += q
  Pubun in ('비품','폐기')      → 비품: Gbqut += q, Gjsum -= q / 폐기: Gpqut += q (+테넌트 분기)
  Gubun='반품'                 → Gbsum -= q, Gbqut += q   (반품)
```

> ⚠ L463 에 `Base10.Database.Database='chul_09_db'` 테넌트 분기가 있다(폐기 시 Gbsum vs Gjsum).
> DEC-033 규약상 **서비스 코드 분기 금지** — `migration/contracts/` 의 `customer_variants` 로 옮긴다.

## 4. 마감 산식 (L1111~1159)

```
GsumX  = Σ 스냅샷 전재고                       (기간 시작 직전)
GsumY  = GsumX + Giqut − Goqut − Gjqut + Gisum + Gbsum + Gpsum
         − (Gosum ≠ 0 이면 Gosum)
Gssum  = Σ스냅샷 Gbqut − Gisum + Gjsum + Gosum   (재고(반))
```

## 5. 포팅 전략 — **재구현이 아니라 조립** (핵심)

전·현재고 산식은 **DEC-138 에서 이미 1:1 포팅되고 라이브 대사까지 끝났다**
(`Tong04.pas` TTong40 `_Sv_Ghng_`/`_Sv_GhngX` → `reports_service._fetch_stock_asof`,
검증 앵커 도서 3411 asof 07.09=981 / 07.16=960 이 레거시 현재고와 정확 일치).

| 컬럼 | 조달 방법 | 상태 |
| --- | --- | --- |
| 전재고 | `_fetch_stock_asof(asof=시작일−1일, axis_like=None)` | **재사용 가능** |
| 현재고 | `_fetch_stock_asof(asof=기준일, axis_like=None)` | **재사용 가능** |
| 입고·반입·출고·증정·반품·폐기·변경 | S1_Ssub 기간 집계 §3 분기표 (`reports_service` `_BOOK_SALES_MEASURE_KEYS` 와 동일 버킷) | **재사용 가능** |
| 재고(반) | §4 `Gssum` — 스냅샷 `Sv_Ghng.Gbqut` 가 추가로 필요 | **미구현** (DEC-138 이 "반품재고 버킷 1차 미표시"로 유보) |
| 분류 롤업 | `G4_Book.Ocode` 로 묶고 이름은 `G4_Gbun.Gname` (L1171) | **미구현** |

즉 **10개 중 9개는 기존 검증 로직 조합으로 얻고**, 신규 작업은 (a) 재고(반) 스냅샷 버킷,
(b) 분류(Ocode) 롤업 축 두 가지다. 900줄 누적 로직을 다시 옮길 필요는 없다.

## 6. 남은 결정

1. **재고(반)** 를 1차에 포함할지 — 포함 시 `_fetch_stock_asof` 에 `Gbqut` 버킷 확장 필요.
2. 상단 축 — 레거시는 **분류(Ocode)**, 운영 요청 컬럼에는 도서코드·도서명이 있어 축이 상충.
   레거시 준수 시 상단=분류(도서코드·정가 열 없음) / 하단=도서(도서코드·정가 표시).

## 7. 참조

- DEC-138(재고 산식 정본 + 라이브 대사), DEC-033(테넌트 분기는 contract 로), DEC-028
- 현행 임시 화면: `도서물류관리프로그램/frontend/src/app/(app)/inventory/status/page.tsx`
- 재사용 지점: `backend/app/services/reports_service.py` `_fetch_stock_asof` / `attach_period_end_stock`
