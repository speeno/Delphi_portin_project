# 레이아웃 매핑: Sobo34_1 (재고 및 재고금액) — 재고금액 화면 신설

DEC-028 의무 — dfm→(영역, 위젯 ID, DBGrid 컬럼, 이벤트) 1:1 매핑. 픽셀/폰트/색상 제외.

> **배경(2026-08-23 운영 요청)**: "원장관리-재고현황 메뉴 다음에 재고금액 메뉴를 신설해라.
> 재고현황 화면과 거의 동일한데 수량보다는 **금액 관점**으로 정보를 제공한다."
> 해당 레거시 화면은 포팅 누락(`analysis/audit/delphi-form-screen-matrix.json` 의 orphan
> legacy stem `Subu34_1`)이었다. 본 문서는 그 포팅을 위한 정본 분석이다.

## 0. 입력 산출물 (정본)

- dfm: `WeLove_FTP/도서유통-New/도서유통/한국도서유통/출판/MySQL/Subu34_1.dfm` (caption `재고 및 재고금액`)
- pas: 같은 폴더 `Subu34_1.pas` (2,404줄) — `Button101Click`(L336, 거래처/출판사 분기) /
  `Button102Click`(L347~1290, 본 조회) / `Button103Click`(L1292~, 거래처 축)
- 레거시 메뉴: `한국도서유통/유통/Chul.dfm` `Menu300`(재고원장) → `Menu304_1` = `재고 및 재고금액`
  → `Menu304_1Click` 이 `TSobo34_1` 생성. **재고현황(Sobo34/Menu303 기간별재고원장) 과 같은 대메뉴.**

> **변형 주의**: `도서유통-New/Subu34_1.{pas,dfm}`(= `legacy_delphi_source/legacy_source/`)
> 는 필터 패널이 다르다(출판사명 `Edit108`·반품재고 제로 `CheckBox3` 추가, `Edit102`/`Panel102`
> 숨김). **DBGrid 9컬럼은 두 빌드가 완전히 동일**하다. 분류 롤업에는 New 빌드에만
> `mSqry.Gjqut` 이중 가산 버그가 있고(출판 빌드는 해당 줄이 주석 처리), 본 포팅은
> **출판 빌드(= Sobo34 포팅과 같은 정본 경로)** 를 따른다 — 재고합계 단일 가산.

## 1. 화면 구조

| 영역 | dfm | 역할 |
| --- | --- | --- |
| 검색 패널 `Panel001` | `Edit101`(거래일자)·`Edit103/105`(도서코드 구간)·`Panel102`(도서명/본사도서/창고도서 토글)·`Edit109`(기준율 %)·`dxButton1`(검색) | 조회 조건 |
| 상단 `DBGrid101` (`Panel002`) | **분류 단위** 롤업 (`mSqry`) | 분류별 재고·재고금액 |
| 하단 `DBGrid201` (`Panel003`) | 상단 선택 분류의 **도서 단위** (`nSqry`) | 도서별 재고·재고금액 |

- **거래일자는 1일**이다. `Edit102` 는 `Visible=False` 이고 SQL 은 출판 빌드 기준
  `Gdate >= Edit101 and Gdate <= Edit101` (L369~370) — 기간이 아니라 **그 날 마감 시점** 재고.
- 도서 검색은 재고현황 선례대로 **「도서명 또는 코드」 한 칸**으로 단순화(`Edit103/105` 구간 폐지).
- `Edit109`(기준율, 기본 100)는 금액에 곱하는 계수다. `Button703Click`/`CheckBox3Click` 은
  조회 없이 금액만 재계산하는 핸들러 — 웹은 상태 변경 후 재조회로 대체한다.

## 2. 그리드 컬럼 (상·하단 동일 9컬럼, dfm FieldName 기준)

| 표시 | FieldName | 의미 | 웹 필드 |
| --- | --- | --- | --- |
| 분류코드 / 도서코드 | `GCODE` | 상단=`G4_Book.Gubun`, 하단=도서코드 | `class_code` / `bcode` |
| 분 류 명 / 도 서 명 | `GNAME` | 상단=`G4_Gbun.Gname`, 하단=도서명 | `gname` |
| 정가 | `GSQUT` | `G4_Book.Gdang` | `gdang` |
| 정품재고 | `GSUMY` | 거래일자 마감 정품재고 (= Sobo34 「현재고」) | `stock_qty` |
| 재고금액 | `GOSUM` | 정가 × 정품재고 × 기준율 | `stock_amt` |
| 반품재고 | `GSSUM` | 반품재고 잔량 (= Sobo34 「재고(반)」) | `return_qty` |
| 재고금액 | `GBSUM` | 정가 × 반품재고 × 기준율 | `return_amt` |
| 재고합계 | `GJQUT` | 정품재고 + 반품재고 | `total_qty` |
| 금액합계 | `GJSUM` | 재고금액 + 반품 재고금액 | `total_amt` |

- 「재고금액」 라벨이 **두 번** 나오는 것은 레거시 그대로다(정품/반품 각각). 웹도 같은 라벨을
  쓰되 `headerHint` 로 구분한다.
- 하단 「합계」 = `Footer.ValueType = fvtSum` 인 6컬럼(`GSUMY/GOSUM/GSSUM/GBSUM/GJQUT/GJSUM`).
  `GSQUT`(정가)는 합계 대상이 **아니다**.
- **상단 그리드의 「정가」는 항상 공란**이다 — 롤업 루프(L1219~1252)가 `mSqry.Gsqut` 를
  누적하지 않는다. 웹도 `gdang: null` 로 두고 빈 칸으로 렌더한다(임의 합산 금지).

## 3. 산식 (Subu34_1.pas L1189~1213)

```
정품재고(GSUMY) = Sobo34 현재고와 동일 산식
                = 전재고 + Giqut − Goqut − Gjqut + Gisum + Gbsum + Gpsum
                  − (Gosum ≠ 0 이면 Gosum)
반품재고(GSSUM) = Σ스냅샷 Gbqut − Gisum + Gjsum + Gosum

재고금액(GOSUM) = GSQUT(정가) × GSUMY × (Edit109/100)
재고금액(GBSUM) = GSQUT(정가) × GSSUM × (Edit109/100)
   ※ CheckBox3(반품재고 제로) 체크 시 → GSSUM := 0, GBSUM := 0  (금액 산출 **후** 덮어쓰기)
재고합계(GJQUT) = GSUMY + GSSUM
금액합계(GJSUM) = GOSUM + GBSUM
```

누적 분기표(L451~633)와 스냅샷 시드는 **Sobo34 와 같은 코드**다 —
`analysis/layout_mappings/Sobo34_inventory_ledger.md` §3/§4 참조.

## 4. 포팅 전략 — **재구현이 아니라 재사용**

수량 축이 Sobo34 와 동일하므로 `inventory_service.get_stock_value_ledger` 는
`get_stock_ledger(date_from=date_to=거래일자)` 를 호출하고 금액만 얹는다.
DEC-138(전·현재고 라이브 대사) / DEC-182(합계 행) / DEC-183(행 집합 = 기간 거래 ∪ 재고 스냅샷)
의 검증 자산을 그대로 승계한다 — 900줄 누적 로직 재이식 없음.

| 컬럼 | 조달 |
| --- | --- |
| 정품재고 / 반품재고 / 정가 | `get_stock_ledger` 의 `gsumy` / `gssum` / `gdang` |
| 재고금액 · 반품 재고금액 · 재고합계 · 금액합계 | 위 값의 파생(§3) |
| 분류코드·분류명 | `get_stock_ledger` 의 `by_class` 가 이미 해석한 `G4_Gbun.Gname` 재사용 |

## 5. 위젯 ID 매핑 (`data-legacy-id`)

| dfm id | 웹 위치 |
| --- | --- |
| `Edit101` | 거래일자 `DateFieldYMD` |
| `Edit103` | 도서명 또는 코드 `MasterLookupField` (Edit105 구간 폐지) |
| `Edit109` | 기준율(%) `Input[type=number]` |
| `Panel102` | 도서구분 토글(전체/본사도서/창고도서) |
| `CheckBox3` | 반품재고 제로 체크박스 (New 빌드 기능, 웹 기본 **해제** — 출판 정본 동작과 일치) |
| `dxButton1` | 조회 버튼 |
| `DBGrid101` / `DBGrid201` | 상·하단 `DataGrid` (+ 컬럼별 `Sobo34_1.<grid>.<FieldName>`) |

## 6. 남은 결정

1. **라이브 대사 미완** — 수량 축은 Sobo34 검증 자산 승계지만, 금액 4컬럼을 교문사(5019,
   remote_153/chul_09) 실화면과 대조하지 않았다. `RUN_DB_SMOKE` 로 확인 필요.
2. `CheckBox3`(반품재고 제로) 기본값 — New 빌드는 `Checked=True`(반품 0 표시), 출판 정본은
   컨트롤 자체가 없다. 운영이 New 빌드 기본값을 원하면 기본 체크로 전환한다.
3. 기준율 ≠ 100 일 때 금액은 소수가 될 수 있다. 백엔드는 반올림 없이 float 로 반환하고
   화면에서만 원 단위로 표시한다(합계 = Σ원값, 표시 오차 누적 없음).

## 7. 참조

- DEC-028(레이아웃 매핑 의무), DEC-138(재고 산식 정본 + 라이브 대사), DEC-182/183(합계·행 집합)
- 형제 화면: `analysis/layout_mappings/Sobo34_inventory_ledger.md` (재고현황 = Sobo34)
- 구현: `backend/app/services/inventory_service.py` `get_stock_value_ledger`,
  `backend/app/routers/inventory.py` `GET /api/v1/inventory/stock-value`,
  `frontend/src/app/(app)/inventory/value/page.tsx`
