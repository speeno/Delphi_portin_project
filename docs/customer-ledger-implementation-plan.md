# 거래처원장 / 통합 거래처원장 P2 구현 계획 (Sobo32 · Sobo32_1)

- **ID**: PLAN-LDG-CUSTOMER-2026-04-22
- **상태**: draft (T0 — 계획 동결 직전)
- **owner**: 메인개발자
- **연관 결정**: DEC-028 (DFM 산출물 입력 동결), DEC-033 (mysql3 호환 — 페이저/JOIN 분리), DEC-040 (신규 SQL 0건 정책), DEC-046 (권한 d_select), DEC-055 (useListSession), PHASE1-PROMOTION-GATE
- **연관 계약**: `migration/contracts/customer_book_ledger_phase2.yaml` (이미 `book_*` 2건은 phase1 승격 — `customer_*` 2건이 본 계획 대상)

---

## 0. 한눈 요약

| 항목 | 거래처원장 (Sobo32) | 통합 거래처원장 (Sobo32_1) |
|---|---|---|
| 라우트 | `/ledger/customer` | `/ledger/customer-integrated` |
| 백엔드 | **신규** `GET /api/v1/ledger/customer` | **신규** `GET /api/v1/ledger/customer-integrated` |
| 현 상태 | UI는 `transactionsApi.list` 차용 + `fetchAllPages` (회귀 위험) | 동일 |
| 목표 | 레거시 9 분기 누적(이동/반품/입고/증정/출고/폐기/비품/잔액) 서버 산출 + DEC-033 페이저 | 거래처별 합산 + DEC-033 페이저 |
| 차단 회귀 | mysql3 6컬럼 GROUP BY + JOIN 3개 + ALL pages fetch ⇒ Sobo54/57 와 동일한 read_timeout 회귀 | 동일 |

> **핵심 원칙**(사용자 룰): "결과가 달라지지 않게" = SQL 의 `WHERE` 와 분기 누적 식은 레거시 `Subu32.pas` L380~L660 과 1:1 동등. **SQL 자체는 신설 0건** — 기존 `S1_Ssub`, `Sg_Csum`/`Sb_Csum`, `G1_Ggeo`, `G4_Book`, `G7_Ggeo` 만 재사용.

---

## 1. 레거시 분석 (T1)

### 1.1 출처

| 항목 | 경로 |
|---|---|
| DFM 1 | `legacy_delphi_source/legacy_source/Subu32.dfm` (TSobo32 — 거래처원장) |
| DFM 2 | `legacy_delphi_source/legacy_source/Subu32_1.dfm` (TSobo32_1 — 통합 거래처원장) |
| DFM 3 | `legacy_delphi_source/legacy_source/Subu32_9.dfm` (TSobo32 변형) |
| PAS 1 | `legacy_delphi_source/legacy_source/Subu32.pas` |
| PAS 2 | `legacy_delphi_source/legacy_source/Subu32_1.pas` |
| HTML 산출물 | `tools/.../legacy_source_root/{Subu32,Subu32_1,Subu32_9}/Sobo32*.html` (DEC-028 입력) |
| 화면카드 | `analysis/screen_cards/Sobo32.md`, `analysis/screen_cards/Sobo32_1.md` |

### 1.2 컴포넌트 인벤토리 — Subu32.dfm (대표 폼)

| 영역 | 컨테이너 | 위젯 | 모던 매핑 |
|---|---|---|---|
| 상단 검색 | `Panel001` | Edit101/102 (TFlatMaskEdit, 일자 from/to), Edit103/104 (도서코드 from/to), Edit105 (도서코드 끝, HIDDEN), Edit107 (Hcode), Edit108 (출판사명), Panel101~103 (라벨), Button101 (Hidden 분기), dxButton1 (검색), DateEdit1/2 | `customer/page.tsx` 검색 영역 |
| 모드 토글 | `Panel102` (Caption "도서명/본사도서/창고도서") | TFlatPanel ⇒ St2='B'/A/B (Ocode 분기) | `<select>` 또는 `<RadioGroup>` 신설 (DEC-033 호환) |
| 그리드 1 | `Panel002.DBGrid101` | 일자별 시계열 (Gdate, Gpsum 이동, Gisum 반품, Giqut 입고, Gjqut 증정, Goqut 출고, Gpqut 폐기, Gbqut 비품, Gjsum 비품금, Gbsum 폐기금) | 메인 그리드 |
| 그리드 2 | `Panel003.DBGrid301` (TDBGridEh) | 도서코드 단위 분배 (Bcode/Gname/Ocode/Gubun/Gdang) — 도서별 보기 | sub-그리드 (대시보드 OOS, §6) |
| 진행 패널 | `Panel007` | ProgressBar0/1, StBar101/201 | React `loading` 흡수 |

### 1.3 핵심 SQL 인용 (Subu32.pas, 인용만 — 동등성 매트릭스의 단일 원천)

| line | 종류 | 테이블 | SQL 핵심부 |
|---|---|---|---|
| L293 | SELECT | `G7_Ggeo` | `Select Scode From G7_Ggeo Where ... Gcode='@Gcode'` (거래처 존재 확인) |
| L303 | SELECT | `Sv_Ghng` | `Select Max(Gdate) as Gdate From Sv_Ghng` (이월 기준일) |
| L391 | SELECT (메인 1) | `S1_Ssub` | `Select Gdate,Scode,Gubun,Pubun,Sum(Gsqut)as Gsqut,Sum(Gssum)as Gssum From S1_Ssub Where {DSelect+Gdate>=&<=&Hcode=&Bdate is null&Ocode Like '%St2%'(+Bcode 범위 옵션)} Group By Gdate,Scode,Gubun,Pubun` |
| L426 | SELECT (룩업) | `G4_Book` | `Select Gname,Ocode,Gubun,Gdang From G4_Book Where ... Gcode=&Hcode=` |
| L516 | SELECT (메인 2) | `S1_Ssub` | (L391 동일하되 `Bdate>=&<=` ⇒ 유통반품재고 분기) |
| L654 | SELECT | `S1_Ssub` | `Select Scode,Gdate,Sum(Gbsum)as Gbsum From S1_Ssub Where ... Group By Scode,Gdate` (반품 잔량) |
| L1276 | SELECT | `Sb_Csum` | `Select Gcode,Gubun,Gsqut From Sb_Csum Where ...` (이월 잔량) |
| L1590 | SELECT | `S1_Ssub` | `Select Gdate,Scode,Gubun,Pubun,Bcode,Sum(Gsqut),Sum(Gssum) ... Group By` (DBGrid301 도서별 분배) |
| L1623 | SELECT | `G4_Book` | `Select Grat8 From G4_Book Where Gcode=` (도서 마진) |

### 1.4 클라이언트 누적 분기 (L411~L506) — 결과 보존을 위한 1:1 매핑 표

이 분기 표가 본 계획의 **단일 원천(SSOT)** 입니다. 백엔드 누적 함수(`_accumulate_customer_row`) 가 본 표를 재현해야만 "결과가 달라지지 않음" 이 보장됩니다.

| Yesno (Scode) | Gubun | Pubun | 가산 컬럼 | pas 라인 |
|---|---|---|---|---|
| `Y` | * | `이동` | `Gpsum` += Gsqut | L454 |
| `Y` | * | `반품` | `Gisum` += Gsqut | L457 |
| `Y` | `입고` | * | `Giqut` += Gsqut | L460 |
| `X` | * | `증정` | `Gjqut` += Gsqut | L464 |
| `X` | `출고` | * | `Goqut` += Gsqut | L467 |
| `X` | `폐기` | `비품` | `Gpqut` += Gsqut, `Gjsum` += Gsqut | L471 |
| `X` | `폐기` | (그 외) | `Gpqut` += Gsqut, `Gbsum` += Gsqut | L474 |
| `X` | (그 외) | `비품` | `Gbqut` += Gsqut, `Gjsum` -= Gsqut | L482, L489 |
| `X` | (그 외) | `폐기` | `Gpqut` += Gsqut, (X 모드) / `Gpqut`+`Gjsum` (Z 모드) | L484, L492 |
| `X` | `반품` | * | `Gbsum` -= Gsqut, `Gbqut` += Gsqut | L504 |

> **이미 검증된 동등 코드**: `backend/app/services/inventory_service.py::_accumulate_row` (Subu31 L386~L466 동일 분기 — 본 화면도 동일 패턴 재사용 가능. SOLID OCP — `_accumulate_*` 의 두 번째 사용처).

### 1.5 변형 차이 (Subu32 vs Subu32_9)

`Subu32_9.dfm`(`TSobo32` 동일 클래스명) 는 폼 클래스 **재정의 없이 변형**된 산출물 — 컴포넌트 수만 차이(31 vs 21). UI/SQL 는 동일하므로 contract 의 `customer_variants` 섹션에 **단언("UI 분기 0건")** 으로 흡수.

---

## 2. 계약 갱신 (T2 → T3)

### 2.1 contract 파일

`migration/contracts/customer_book_ledger_phase2.yaml` 의 `customer_single` / `customer_integrated` 두 섹션을 **v1.0.0 → v1.1.0** 로 보강 (이미 draft 가 있음 — 본 계획에서 추가/구체화):

```yaml
customer_single:
  path: GET /api/v1/ledger/customer
  legacy_id: Sobo32
  legacy_pas:
    - Subu32.pas#L380-L660 (메인 SQL + 누적 분기)
    - Subu32.pas#L411-L506 (분기 표 §1.4 와 1:1)
    - Subu32.pas#L1276 (Sb_Csum 이월)
    - Subu32.pas#L303 (Sv_Ghng 이월 기준일)
  permission: ledger.customer.read
  query_params:
    customer_code: required string  # 레거시 Edit107.Text (Hcode)
    from_date: required ISO date    # Edit101 → 'YYYY.MM.DD' 정규화
    to_date: required ISO date      # Edit102
    bcode_from: optional            # Edit103 (도서 시작)
    bcode_to: optional              # Edit105 (도서 끝)
    scope: enum[A,B,ALL]            # Panel102 토글 (A=본사 B=창고 ALL=전체)
    page:
      limit: 100
      max_limit: 500
      offset: required int
  response:
    opening_date: ISO date          # Sv_Ghng.Max(Gdate) — 이월 기준일
    rows:                           # 일자 단위 — DEC-033(g) 페이저로 잘린 페이지
      - gdate
        gpsum, gisum, giqut, gjqut, goqut, gpqut, gbqut  # 7 수량
        gjsum, gbsum                                     # 2 금액
        balance_qty                                      # 일자 누적 잔량 (opening + Σ(giqut+gisum) - Σ(goqut+gjqut+gpqut+gbqut))
    summary:                        # 페이지 무관 전역 SUM (offset==0 시에만 산출)
      opening_qty: int              # Sb_Csum.Sum(Gsqut) where Gubun='입고' - Σ(반품 누적)
      total_in: int
      total_out: int
      closing_qty: int              # = opening + total_in - total_out
    page: { limit, offset, total, has_more }   # ceiling: offset + visible + (1 if has_more)

customer_integrated:
  path: GET /api/v1/ledger/customer-integrated
  legacy_id: Sobo32_1
  permission: ledger.customer.read
  query_params:
    from_date: required ISO date
    to_date: required ISO date
    customer_pattern: optional string  # 거래처 코드 prefix LIKE
    scope: enum[A,B,ALL]
    page: { limit: 100, max_limit: 500, offset: required }
  response:
    rows:                           # 거래처 단위
      - hcode, hname
        opening_qty, period_in, period_out, closing_qty
    page: { limit, offset, total, has_more }
```

### 2.2 등가성(equivalence) 매트릭스

| 축 | 기준 | 산출 |
|---|---|---|
| **A. functional** | §1.4 분기 표 10건 모두 PASS | `test/test_c6_ledger_phase2.py::test_branch_table_equivalence` |
| **B. data** | mysql3·5.x·8.x·MariaDB 4서버 동일 raw row | `debug/probe_backend_all_servers.py --endpoint /api/v1/ledger/customer` 산출표 |
| **C. ui** | DBGrid101 9 수량/금액 컬럼 100% 노출 + `data-legacy-id` 부착 | `analysis/layout_mappings/Sobo32.md` |
| **D. audit** | read-only — audit 미적용 (조회만) | (skip — read-only 명시) |
| **E. performance** | mysql3에서 1년치 + 50거래처 P95 < 1.5s | `test/regression_phase2.py` timing |

### 2.3 새 SQL 정책 (DEC-040)

신설 SQL 0건. `customer_single` / `customer_integrated` 모두 다음 **기존 SQL 6건 재사용**:

1. `_opening_sql` (이미 `inventory_service.py` 에 존재) — `Sv_Ghng.Max(Gdate)`.
2. `S1_Ssub Group By Gdate,Scode,Gubun,Pubun` (Subu32.pas L391·L516 동일).
3. `Sb_Csum Select Gcode,Gubun,Gsqut Where ...` (Subu32.pas L1276 — 이월 잔량).
4. `_fetch_publisher_names` / `_fetch_vendor_names` / `_fetch_product_names` (이미 `inbound_service.py` 에 존재 — `in_clause_lookup` 청크).
5. `_dates_count_sql` / `_dates_page_sql` (이미 `inventory_service.py` 에 존재 — Step1·Step2 페이저).
6. `_ledger_rows_sql` (이미 `inventory_service.py` 에 존재 — Step3 사전 집계).

> SOLID DIP — 신규 service 는 위 헬퍼들에 의존 (저수준 SQL 직접 작성 금지).

---

## 3. 백엔드 구현 (T4)

### 3.1 파일 — 신규/수정

| 파일 | 작업 | 비고 |
|---|---|---|
| `backend/app/services/customer_ledger_service.py` | **신규** | `inventory_service.py` 의 페이저/사전 집계 헬퍼를 import 해서 재사용 (DRY · DIP) |
| `backend/app/routers/ledger.py` | **신규 또는 확장** | `/api/v1/ledger/customer`, `/api/v1/ledger/customer-integrated` 라우트 추가. 기존 `/ledger/book*` 와 같은 모듈 |
| `backend/app/models/ledger.py` | **신규** | Pydantic — `CustomerLedgerResponse`, `IntegratedCustomerLedgerResponse` |
| `backend/app/main.py` | 수정 | `include_router(ledger_router)` |

### 3.2 회귀 가드 (이전 케이스에서 학습한 항목 — 사용자 룰 "유사 케이스까지 일반화")

| 회귀 ID | 직전 사례 | 적용 |
|---|---|---|
| **R1: count_grouped 금지** | Sobo54/57 30s timeout (2026-04-22) | `count_grouped` 사용 X. `_dates_count_sql` (단일 컬럼 `COUNT(DISTINCT Gdate)`) 만 허용 |
| **R2: JOIN 분리** | Sobo54/57 mysql3 5분 timeout (v1.2.2) | `S1_Ssub` 메인 쿼리에서 `G4_Book`/`G7_Ggeo`/`G1_Ggeo` JOIN 금지 → 페이지 행에서 distinct hcode/bcode 추출 후 `_fetch_*_names` 청크 룩업 |
| **R3: 페이저 LIMIT+1** | (v1.2.1·v1.2.2 표준) | 모든 메인 쿼리는 `apply_limit_offset_syntax` + `limit_offset_bind` |
| **R4: grand_totals 조건부** | Sobo54/57 v1.2.1 | `summary` 는 `offset==0` 일 때만 산출. 후속 페이지는 0 으로 두고 프론트가 캐싱 |
| **R5: in_clause_lookup 청크** | DEC-033 (e) — POC `_SOBO67_GNAME_CODES_CHUNK` | 이름 룩업은 청크 분할 — 거대 IN(...) 파싱 stall 가드 |
| **R6: 라우터 detail.message** | v1.2.2 — `f"... {type(exc).__name__}"` | 다음 회귀 시 진단 시간 단축 |
| **R7: read-only 권한** | DEC-046 d_select | `ledger.customer.read` 키만 요구. operator=본인 거래처, branch_manager=지사, admin=전체 |

### 3.3 alg 의사코드

```python
# customer_ledger_service.py
async def get_customer_ledger(*, server_id, customer_code, from_date, to_date,
                              bcode_from, bcode_to, scope, limit, offset):
    """Subu32.pas L380~L660 1:1 동등 — DEC-033(e/g) 회귀 가드 적용."""
    # Step 0) 권한 d_select 가드 — DEC-046 (이미 구현된 헬퍼 재사용).
    # Step 1) 이월 — _opening_sql (재사용)
    opening = await execute_query(server_id, _opening_sql(has_hcode=True),
                                  (from_date, customer_code))
    # Step 1.5) 이월 잔량 — Sb_Csum (Subu32.pas L1276)
    seed = await execute_query(server_id, SQL_SB_CSUM_SEED, (customer_code,))

    # Step 2) WHERE — Subu32.pas L380~L388 1:1
    where = _build_filter_where(has_hcode=True, has_bcode=bool(bcode_from), ...)
    params = (from_date, to_date, customer_code, bcode_from, bcode_to, ocode_like)

    # Step 3) DEC-033 페이저 (Sobo33_ledger 와 동일 패턴)
    total = (await execute_query(server_id, _dates_count_sql(where), params))[0]['cnt']
    dates_rows = await execute_query(server_id,
                                     apply_limit_offset_syntax(_dates_page_sql(where), server_id),
                                     params + limit_offset_bind(limit + 1, offset, server_id))
    page_dates, has_more = _slice_with_has_more(dates_rows, limit)

    # Step 4) 사전 집계 fetch — JOIN 0개
    rows = await in_clause_lookup(server_id, _ledger_rows_sql(where),
                                  keys=page_dates, prefix_params=params)

    # Step 5) Python 누적 — _accumulate_customer_row (§1.4 분기 표)
    daily = {d: dict(opening_columns_zero) for d in page_dates}
    running = seed_qty
    for r in rows:
        _accumulate_customer_row(daily[r['Gdate']], r['Scode'], r['Gubun'], r['Pubun'],
                                 r['Gsqut'], r['Gssum'])
    # 누적 잔량 column 추가
    for d in sorted(daily):
        running += daily[d]['giqut'] + daily[d]['gisum'] - daily[d]['goqut'] - daily[d]['gjqut'] \
                 - daily[d]['gpqut'] - daily[d]['gbqut']
        daily[d]['balance_qty'] = running

    # Step 6) 전역 summary — offset==0 일 때만 (R4)
    if offset == 0:
        summary = await _grand_summary(server_id, where, params)
    else:
        summary = {"opening_qty": 0, "total_in": 0, "total_out": 0, "closing_qty": 0}

    return {"opening_date": ..., "rows": [daily[d] for d in page_dates],
            "summary": summary,
            "page": {"limit": limit, "offset": offset,
                     "total": offset + len(page_dates) + (1 if has_more else 0),
                     "has_more": has_more}}
```

`get_integrated_customer_ledger` 는 동일 구조이되:

- Step 1 `Sb_Csum` 을 거래처별 dict 로 누적.
- Step 4 의 `Group By Gdate,Scode,Gubun,Pubun` 을 `Group By Hcode,Scode,Gubun,Pubun` 로 변경(파일 `_integrated_rows_sql`).
- Step 5 누적은 거래처 키.
- 페이저는 distinct `Hcode` 단위.

---

## 4. 프론트 구현 (T5)

### 4.1 파일

| 파일 | 작업 |
|---|---|
| `frontend/src/lib/ledger-api.ts` | **신규** — `customerLedgerApi.{single, integrated}` (timeout 60s — 리포트 표준) |
| `frontend/src/app/(app)/ledger/customer/page.tsx` | **재작성** — `transactionsApi.list` + `fetchAllPages` 제거, 신규 API 호출 |
| `frontend/src/app/(app)/ledger/customer-integrated/page.tsx` | **재작성** — 동일 |
| `analysis/layout_mappings/Sobo32.md` | **신규** — DEC-028 매핑 노트 (`Sobo31.md` 와 동일 형식) |
| `analysis/layout_mappings/Sobo32_1.md` | **신규** — 동일 |
| `frontend/src/lib/form-registry.ts` | T8 시 `phase: "phase2" → "phase1"` |

### 4.2 UI 동등성 — 레거시 DBGrid101 9컬럼 노출

| dfm 컬럼 | 한글 라벨 | 데이터 키 | data-legacy-id |
|---|---|---|---|
| `GDATE` | 일자 | `gdate` | `Sobo32.DBGrid101.GDATE` |
| `GPSUM` | 이동 | `gpsum` | `Sobo32.DBGrid101.GPSUM` |
| `GISUM` | 반품 | `gisum` | `Sobo32.DBGrid101.GISUM` |
| `GIQUT` | 입고 | `giqut` | `Sobo32.DBGrid101.GIQUT` |
| `GJQUT` | 증정 | `gjqut` | `Sobo32.DBGrid101.GJQUT` |
| `GOQUT` | 출고 | `goqut` | `Sobo32.DBGrid101.GOQUT` |
| `GPQUT` | 폐기수 | `gpqut` | `Sobo32.DBGrid101.GPQUT` |
| `GBQUT` | 비품수 | `gbqut` | `Sobo32.DBGrid101.GBQUT` |
| `GJSUM` | 비품금 | `gjsum` | `Sobo32.DBGrid101.GJSUM` |
| `GBSUM` | 폐기금 | `gbsum` | `Sobo32.DBGrid101.GBSUM` |
| (모던 신설) | 잔량 | `balance_qty` | `Sobo32.DBGrid101.BALANCE` (deltas 표기) |

> 검색 패널은 `Sobo31.md` 의 표 §3 컨벤션 그대로(Edit101/102/103/105/107 + Panel101~103 + dxButton1) 매핑 — `data-legacy-id` 11~13개 부착.

### 4.3 React 패턴 (이미 검증된 7화면 표준)

- `useListSession<Snap>("ledger.customer", ...)` (DEC-055).
- `DataGridPager` (`DEC-033(g)`) + `useDynamicPageSize`.
- `totalsCache` (Sobo54/57 v1.2.1 패턴) — `summary` 가 `offset==0` 만 채워지므로 후속 페이지에서 캐시 보존.
- `ApiErrorBanner` 표준 에러 표시.
- 60s timeout — `inboundApi.daily` / `period` 와 동일 옵션.
- `fetchAllPages` 제거 (회귀 차단).

---

## 5. 테스트 팩 (T6)

### 5.1 파일

| 파일 | 작업 |
|---|---|
| `migration/test-cases/customer_book_ledger_phase2.json` | 보강 — 분기 표 §1.4 의 10케이스 모두 추가 |
| `test/test_c6_customer_ledger_phase2.py` | **신규** — 위 fixtures 로 단위·통합 테스트 (16~20케이스 목표) |

### 5.2 필수 케이스 (회귀 가드 + 분기 표)

1. `test_branch_Y_iko_입고` — `Scode=Y, Gubun=입고` ⇒ giqut.
2. `test_branch_Y_pubun_이동` — Gpsum.
3. `test_branch_Y_pubun_반품` — Gisum.
4. `test_branch_X_pubun_증정` — Gjqut + Gosum.
5. `test_branch_X_gubun_출고` — Goqut + Gosum.
6. `test_branch_X_gubun_폐기_pubun_비품` — Gpqut + Gjsum.
7. `test_branch_X_gubun_폐기_else` — Gpqut + Gbsum.
8. `test_branch_X_pubun_비품` — Gbqut + Gbsum + Gjsum-=.
9. `test_branch_X_pubun_폐기_X_mode` — Gpqut.
10. `test_branch_X_gubun_반품` — Gbsum-= + Gbqut+=.
11. `test_self_consistent` — opening + Σin - Σout == closing (AC-LDG-1).
12. `test_pager_LIMIT+1_has_more` — limit=2, fixture=3일 ⇒ has_more=True.
13. `test_pager_offset_skips_summary` — offset=2 응답에 `summary.opening_qty == 0`.
14. `test_join_separation_no_g4_book_in_main_sql` — captured SQL 에 `JOIN G4_Book` 등 미포함 (정적 검사).
15. `test_in_clause_lookup_chunked` — names 룩업이 청크 분할(monkeypatch).
16. `test_integrated_equals_sum_of_singles` — 통합 응답의 hcode 합 == single 호출 closing 합 (AC-LDG-3).
17. `test_dselect_operator_only_self` — operator 토큰으로 hcode 비교환 (AC-LDG-5).
18. `test_limit_over_500_returns_422` — limit=1000 (AC-LDG-6).
19. `test_router_500_includes_exception_class_name` — R6 회귀 가드.
20. `test_period_30_days_completes_under_2s_with_mocked_db` — R1 회귀 가드.

### 5.3 4서버 DB 등가 (T7 의 입력)

```bash
debug/probe_backend_all_servers.py \
  --endpoint /api/v1/ledger/customer \
  --query "customer_code=C001&from_date=2026-04-01&to_date=2026-04-30&offset=0&limit=20" \
  --servers mysql3,mysql5,mysql8,mariadb \
  --diff
```

> 이전 케이스 학습(사용자 룰): EUC-KR/UTF-8 인코딩 분기는 `_decode_upload` 와 무관(read-only 이므로). DECIMAL/float→int 변환은 `_safe_int` 표준 헬퍼 사용 의무 (Sobo54/57 회귀 가드 잔여 항목).

---

## 6. T-Phase 단계 (Phase1 승격 게이트 §3 정확 매핑)

| 단계 | 산출 | 통과 기준 |
|---|---|---|
| **T1** screen_card | `analysis/screen_cards/Sobo32{,_1}.md` (이미 자동 생성) + 본 계획 §1 보강 | 컴포넌트·이벤트·SQL 인벤토리 100% (이미 충족) |
| **T2** event_sql_extract | 본 계획 §1.3 SQL 6건 + §1.4 분기 표 10건 | 모든 SQL 이 contract `data_access` 와 1:1 매핑 |
| **T3** contract_yaml | `customer_book_ledger_phase2.yaml` v1.0.0 → v1.1.0 동결 | `customer_*` 2개 endpoints/inputs/outputs/equivalence 완비 |
| **T4** api_impl | `customer_ledger_service.py` + `routers/ledger.py` 확장 | 라우트 스키마가 contract 와 1:1 |
| **T5** ui_impl | `ledger/customer{,-integrated}/page.tsx` 재작성 + `Sobo32{,_1}.md` 매핑 노트 | DBGrid101 9컬럼 표시 + `data-legacy-id` 부착 + ApiErrorBanner |
| **T6** test_pack | `test/test_c6_customer_ledger_phase2.py` 20케이스 PASS | §5.2 항목 모두 PASS |
| **T7** equivalence_run | `regression_phase2.py` + `probe_backend_all_servers.py` | 5축 모두 PASS, 회귀 0건 |
| **T8** promotion | `form-registry.ts` `Sobo32_ledger` / `Sobo32_1_ledger` `phase: "phase2" → "phase1"` + `phase2-screen-cards.json` 2건 제거 (32 → 28) + `porting-screens.json` 동기 | 사이드바 초록 체크 노출 + dashboard 카드 수 갱신 |

---

## 7. 작업 순서 (TODO 단위 — 체크포인트별 회귀 실행)

| # | 작업 | 산출 | 회귀 |
|---|---|---|---|
| 1 | T2/T3 — contract v1.1.0 보강 + 매핑 노트 2건 | `.yaml` + `Sobo32{,_1}.md` | yamllint |
| 2 | T4 — `customer_ledger_service` + 라우트 + Pydantic 모델 | 백엔드 코드 | smoke import + 신규 라우트 OPTIONS 200 |
| 3 | T6 — 단위 테스트 20케이스 (mock DB) | `test_c6_customer_ledger_phase2.py` | `pytest` PASS |
| 4 | T5 — 프론트 재작성 + `data-legacy-id` 부착 | `page.tsx` x2 + `ledger-api.ts` | `tsc --noEmit` 0, `eslint` 0 신규 warn |
| 5 | T7-A — 4서버 probe (실 DB 환경) | `reports/probe-ldg-customer-2026-MM-DD.json` | 4서버 동등 |
| 6 | T7-B — `regression_phase2.py` 추가 + 5축 체크 | `reports/regression-2026-MM-DD.json` | 5축 PASS |
| 7 | T8 — `form-registry.ts` phase 승격 + dashboard 동기 | PR | Sobo54/57 승격과 동일 표준 |

---

## 8. 위험 및 보완

| 위험 | 영향 | 보완 |
|---|---|---|
| **Sb_Csum 이월 잔량 부재 서버** | opening_qty=0 으로 계산되어 closing 오차 | contract 에 `opening_qty_source: optional` 명시 + 테스트에서 fixture 표시 |
| **`Bdate is null` 분기 (L383)** 가 모던 응답에 빠짐 | "유통 반품 재고" 분기 누락 | Step 4 메인 쿼리에 `(Bdate is null OR Bdate=' ')` 그대로 부착 (SQL 신설 0건 — WHERE 만 추가) |
| **거래처별 그리드(DBGrid301) 미구현** | 레거시는 도서별 분배도 동시 표시 | 1차 P2 = DBGrid101 만. DBGrid301 은 §6 out-of-scope, 후속 P3 으로 별 카드 분리 |
| **권한 d_select 회귀** | operator 가 다른 hcode 조회 가능 | `test_dselect_operator_only_self` (AC-LDG-5) 필수 |
| **mysql3 BETWEEN 22일 timeout** | Sobo54/57 동일 회귀 | §3.2 회귀 가드 R1~R6 모두 필수 적용 |
| **SUM/AVG → Decimal Pydantic 검증 실패** | 500 (검증 시점) | 모든 응답 정수 필드는 `_safe_int(grand.get(...))` 통과 |

---

## 9. 산출물 인덱스 (PR 첨부 표준)

승격 PR 에는 다음 7개 링크를 본문에 첨부 (T1~T7 산출):

1. `analysis/screen_cards/Sobo32.md`, `analysis/screen_cards/Sobo32_1.md`
2. 본 계획 §1.3 / §1.4 (T2 SQL/이벤트 추출)
3. `migration/contracts/customer_book_ledger_phase2.yaml` v1.1.0
4. `backend/app/services/customer_ledger_service.py`, `backend/app/routers/ledger.py`
5. `frontend/src/app/(app)/ledger/{customer,customer-integrated}/page.tsx` + `analysis/layout_mappings/Sobo32{,_1}.md`
6. `test/test_c6_customer_ledger_phase2.py` PASS 결과
7. `reports/probe-ldg-customer-...json` + `reports/regression-...json`

---

## 10. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-22 | 최초 draft. Sobo32/Sobo32_1 phase2 → phase1 승격을 위한 T1~T8 전체 계획. Sobo54/57 회귀(v1.2.2) 의 "JOIN 분리 + LIMIT+1 + grand_totals 조건부" 표준을 본 계획에 7개 회귀 가드(R1~R7) 로 일반화. |
