# 기간별 재고원장(상세) Sobo34_4 P2 완성 + 페이징 속도개선 계획

- **ID**: PLAN-LDG-INV-DETAIL-2026-04-23
- **상태**: ✅ done (2026-04-23 phase1 정식 승격 — 사이드바 초록 체크). T3·T4·T5·T6·T8 완료, 회귀 12 신규 PASS, 인접 226 PASS.
- **owner**: 메인개발자
- **대상 화면**: `Sobo34_4` (기간별 재고원장 상세-폐기) — 모던 라우트 `/returns/ledger`
- **현 단계**: phase2 / T4 in_progress · T7 in_progress · T8 pending (`dashboard/data/phase2-screen-cards.json`)
- **연관 결정**: DEC-024 (페이저 표준), DEC-028 (DFM 산출물 입력 동결), DEC-033 (mysql3 호환 — JOIN 분리/페이저 표준), DEC-040 (신규 SQL 0건), DEC-046 (권한 d_select), DEC-055 (useListSession), PHASE1-PROMOTION-GATE
- **연관 계약**: `migration/contracts/return_receipt.yaml` v1.1.0 — `endpoints[/returns/ledger]`
- **선행 사례**: 거래처원장 P2 계획 [`docs/customer-ledger-implementation-plan.md`](./customer-ledger-implementation-plan.md), 입고내역서 phase1 승격(`inbound_service.daily_report` / `period_report` v1.2.2)

---

## 0. 한눈 요약

| 항목 | 현재 (phase2 — T7 in_progress) | 목표 (phase1 승격 시) |
|---|---|---|
| 라우트 | `/returns/ledger` | (동일) |
| 백엔드 | `returns_service.ledger_query` (`SQL_LEDGER_MASTER` LEFT JOIN G4_Book + G7_Ggeo) | **JOIN 분리** + `LIMIT+1 has_more` + `summary` 캐시 |
| 페이저 | `count_grouped`(GROUP BY 4컬럼) — mysql3 5분+ 타임아웃 위험 | `LIMIT+1` + `_slice_with_has_more` (Sobo54/57 표준) |
| 룩업 | 메인 SQL 인라인 JOIN | `_fetch_publisher_names` / `_fetch_product_names` / `_fetch_vendor_names` 청크 |
| 프론트 | `useState` + `load(detailForBcode)` (페이지 무관 1회 fetch — `limit=100` 고정) | `useListSession` + `DataGridPager` + `useDynamicPageSize` + `totalsCache` |
| KPI | 매 페이지 마다 재계산 (`SQL_LEDGER_KPI` 호출 1회) | `summary` 응답 객체로 통합 — `offset==0` 일 때만 산출 → 후속 페이지 캐시 |
| 권한 | `inventory.write` (오기재 — 조회 전용 화면에 write 키) | `inventory.read` (read-only 권한 키, DEC-046 d_select) |
| 차단 회귀 | mysql3 6컬럼 GROUP BY + JOIN 2개 + count_grouped ⇒ Sobo54/57 (v1.2.0~v1.2.1) 와 동일 read_timeout 회귀 | 7개 가드(R1~R7) 일반화 적용 |

> **핵심 원칙**(사용자 룰): 결과가 달라지지 않게 — 레거시 `Subu34_4.pas` L380~L660 의 8 분기 누적식과 1:1 동등. **신규 SQL 0건** (DEC-040) — 기존 `inbound_service` / `inventory_service` / `returns_service` 의 헬퍼 6건 재사용 + WHERE 만 보강.

---

## 1. 레거시 분석 (T1·T2 — 보강만, 입력 산출은 이미 done)

### 1.1 출처

| 항목 | 경로 |
|---|---|
| DFM | `legacy_delphi_source/legacy_source/Subu34_4.dfm` (TSobo34_4) |
| PAS | `legacy_delphi_source/legacy_source/Subu34_4.pas` (1990 LOC) |
| HTML 산출물 | `tools/.../legacy_source_root/Subu34_4/Sobo34_4.html` (DEC-028 입력) |
| 화면카드 | `analysis/screen_cards/Sobo34_4.md` (T1) |
| 매핑 노트 | `analysis/layout_mappings/Sobo34_4.md` (T1·T5) |
| 계약 | `migration/contracts/return_receipt.yaml` v1.1.0 — `endpoints[/returns/ledger]` (T3) |

### 1.2 핵심 SQL 인용 (`Subu34_4.pas`)

| line | 종류 | 테이블 | SQL 핵심부 |
|---|---|---|---|
| L388~L406 | SELECT (메인 1) | `S1_Ssub` | `Select Bcode,Scode,Gubun,Pubun, Sum(Gsqut), Sum(Gssum) From S1_Ssub Where {D_Select + Gdate>=&<= + Bdate is null + Ocode Like '%St2%' + Bcode 범위 옵션 + Hcode=@}` Group By Bcode,Scode,Gubun,Pubun |
| L429 / L437 | SELECT (룩업) | `G4_Book` | `Select Gname,Ocode,Gubun,Gdang From G4_Book Where Gcode=@ and Hcode=@` |
| L566~L583 | SELECT (메인 2) | `S1_Ssub` | (L388 동일하되 `Bdate>=&<=` ⇒ "유통반품재고" 분기 — Bdate 키) |
| L654 (변형) | SELECT | `S1_Ssub` | `Select Scode, Gdate, Sum(Gbsum) From S1_Ssub Where ... Group By Scode, Gdate` (반품 잔량 — 후속 P3) |

> **계약 SQL-RT-28~30** 매핑: `SQL_LEDGER_MASTER` (메인) + `SQL_LEDGER_DETAIL` (디테일 — `Bcode=@` 단건) + `SQL_LEDGER_KPI` (전역 SUM). 본 계획은 **SQL 자체는 신설 0건** — 다음 5건 재사용:
>
> 1. `_fetch_publisher_names` (`inbound_service.py` — G7_Ggeo IN 청크 룩업)
> 2. `_fetch_product_names` (`inbound_service.py` — G4_Book IN 청크 룩업)
> 3. `_fetch_vendor_names` (`inbound_service.py` — G1_Ggeo IN 청크 룩업)
> 4. `_slice_with_has_more` (`inbound_service.py` — LIMIT+1 페이저)
> 5. `apply_limit_offset_syntax` / `limit_offset_bind` (`core.sql_mysql3` — 4서버 호환)

### 1.3 클라이언트 누적 분기 (L487~L562) — 결과 보존을 위한 1:1 매핑 표

> 본 표가 본 계획의 **단일 원천(SSOT)**. P2 의 `master` 응답은 `(Bcode,Scode,Gubun,Pubun)` 분할만 표시(레거시 동등) — **누적 합산은 P3 으로 이연** (DBGrid301 도서별 분배). 백엔드는 분할 행 그대로 반환, 프론트는 4컬럼 합성 키로 표시.

| Yesno (Scode) | Gubun (St3) | Pubun (St4) | 가산 컬럼 | pas 라인 |
|---|---|---|---|---|
| `Y` | * | `이동` | `Gpsum` += T01 | L489 |
| `Y` | * | `반품` | `Gisum` += T01 | L492 |
| `Y` | `입고` | * | `Giqut` += T01 | L495 |
| `X` | * | `증정` | `Gjqut` += T01 | L499 |
| `X` | `출고` | * | `Goqut` += T01 | L502 |
| `X` | `폐기` | `비품` | `Gpqut` += T01, `Gjsum` += T01, `bPQUT` += T01 | L506~L509 |
| `X` | `폐기` | (그 외) | `Gpqut` += T01, `Gbsum` += T01, `aPQUT` += T01 | L511~L514 |
| `X` | (그 외) | `비품` | `Gbqut` += T01, `Gjsum` -= T01, `bBQUT` += T01 | L520~L535 |
| `X` | (그 외) | `폐기` | `Gpqut` += T01, `Gjsum` += T01 / `bPQUT` += T01 | L542~L546 |
| `X` | `반품` | * | `Gbsum` -= T01, `Gbqut` += T01, `aBQUT` += T01 | L555~L559 |

> **이미 검증된 동등 코드**: `inventory_service.py::_accumulate_row` 가 (Subu31 L386~L466 + Subu32 L411~L506) 동일 분기 표를 PASS. P3 에서 `_accumulate_inv_detail_row` 로 확장 시 동일 함수 재사용 가능 (SOLID OCP).

---

## 2. 계약 갱신 (T3 보강)

### 2.1 contract `endpoints[/returns/ledger]` 변경점 — `return_receipt.yaml` v1.1.0 → v1.2.0

```yaml
endpoints:
  /returns/ledger:
    method: GET
    legacy_id: Sobo34_4
    legacy_pas:
      - Subu34_4.pas#L380-L660 (메인 SQL + 누적 분기)
      - Subu34_4.pas#L487-L562 (분기 표 §1.3 와 1:1)
    permission: inventory.read   # ← inventory.write (현재 오기재) 에서 교정
    query_params:
      from_date: required ISO date
      to_date: required ISO date
      hcode: optional               # 출판사 코드 (Edit107)
      bcode: optional               # 도서 코드 (Edit103/105 범위 → 동일 코드 단건)
      gubun: optional enum[반품,재생,해체,변경,폐기,all]
      detail_for_bcode: optional    # 마스터 행 클릭 시
      page:
        limit: 100
        max_limit: 500
        offset: required int
    response:
      master:                       # 도서×구분×Pubun 분할 — 페이지로 잘림
        - bcode, scode, gubun, pubun
          book_name, gname          # in_clause_lookup 청크 룩업
          total_qty, total_amount   # SUM(Gsqut), SUM(Gssum)
      detail:                       # detail_for_bcode 지정 시 단건 조회
        - gdate, gubun, gcode, gname
          giqut, gisum, goqut, gosum
          gjqut, gjsum, gbqut, gbsum
          gsqut, gssum              # 14 컬럼 (DBGrid201 핵심 12종 + 매출 2종)
      summary:                      # 페이지 무관 전역 SUM (offset==0 일 때만 산출)
        book_count: int
        line_count: int
        total_qty: int
        total_amount: int
      page: { limit, offset, total, has_more }   # ceiling: offset + visible + (1 if has_more)
```

### 2.2 등가성 매트릭스 (5축)

| 축 | 기준 | 산출 |
|---|---|---|
| **A. functional** | §1.3 분기 표 10건 — 마스터 분할 행 합 == `summary.total_qty` | `test/test_c4_returns_phase2.py::test_master_split_sum_equals_summary` |
| **B. data** | mysql3·5.x·8.x·MariaDB 4서버 동일 raw row | `debug/probe_backend_all_servers.py --endpoint /api/v1/returns/ledger` |
| **C. ui** | DBGrid101 7컬럼 + DBGrid201 14컬럼 모두 노출 + `data-legacy-id` 부착 | `analysis/layout_mappings/Sobo34_4.md` (이미 done — 회귀 가드만 보강) |
| **D. audit** | read-only — audit 미적용 | (skip) |
| **E. performance** | mysql3 1년치 + 50권 P95 < 1.5s | `test/regression_phase2.py` timing 추가 |

### 2.3 신규 SQL 정책 (DEC-040)

신설 SQL 0건. 본 화면은 다음 **기존 SQL 5건 재사용**:

1. `SQL_LEDGER_MASTER` 의 GROUP BY 본문 — JOIN 부분만 제거 (WHERE/GROUP BY 동일).
2. `SQL_LEDGER_DETAIL` 그대로 — 디테일은 `Bcode=@` 단건이라 JOIN 1개(G1_Ggeo) 잔존 허용 (단건 조회는 회귀 위험 없음).
3. `SQL_LEDGER_KPI` 그대로 — 그러나 `summary` 응답으로 컨테이너 변경 (offset==0 캐시).
4. `_fetch_publisher_names` / `_fetch_product_names` (`inbound_service`) 청크 룩업.
5. `_slice_with_has_more` + `apply_limit_offset_syntax` + `limit_offset_bind` 페이저 헬퍼.

> SOLID DIP — 신규 service 코드 0건. 기존 `returns_service.ledger_query` 만 리팩토링.

---

## 3. 백엔드 구현 (T5 — 리팩토링)

### 3.1 파일 — 수정만

| 파일 | 작업 | 비고 |
|---|---|---|
| `backend/app/services/returns_service.py` | **수정** — `ledger_query` 본문만 (SQL 상수는 유지) | JOIN 제거 + LIMIT+1 + summary 분기 |
| `backend/app/routers/returns.py` | **수정** — `get_returns_ledger` 응답 모델/권한 키 보강 | DEC-046 read 권한 |
| `backend/app/models/ledger.py` | **확장** | `LedgerSummary` Pydantic 추가 |

### 3.2 회귀 가드 (이전 케이스에서 학습 — 사용자 룰 "유사 케이스까지 일반화")

| 회귀 ID | 직전 사례 | 적용 |
|---|---|---|
| **R1: count_grouped 위험** | Sobo54/57 30s timeout (v1.2.1) | `count_grouped` 제거 → `_slice_with_has_more` 로 대체 (단, 후방호환을 위해 `count_grouped` 호출 자체는 1차에 유지하고 `total` 산출만 ceiling 으로 교체 → R1.1: 두 단계 마이그레이션) |
| **R2: JOIN 분리** | Sobo54/57 mysql3 5분 timeout | `SQL_LEDGER_MASTER` 에서 `LEFT JOIN G4_Book/G7_Ggeo` 제거 → 페이지 행에서 distinct hcode/bcode 추출 후 `_fetch_*_names` 청크 룩업 |
| **R3: 페이저 LIMIT+1** | (v1.2.1·v1.2.2 표준) | `apply_limit_offset_syntax` + `limit_offset_bind` + `_slice_with_has_more` |
| **R4: summary 조건부** | Sobo54/57 v1.2.1 | `summary` 는 `offset==0` 일 때만 SUM 쿼리 호출. 후속 페이지는 `book_count=0` 등 placeholder 반환, 프론트가 `totalsCache` 보존 |
| **R5: in_clause_lookup 청크** | DEC-033 (e) — POC `_SOBO67_GNAME_CODES_CHUNK` | 이름 룩업은 청크 분할 — 거대 IN(...) 파싱 stall 가드 |
| **R6: 라우터 detail.message** | v1.2.2 — `f"... {type(exc).__name__}"` | 다음 회귀 시 진단 시간 단축 (`returns.py` `get_returns_ledger` try/except 보강) |
| **R7: read-only 권한** | DEC-046 d_select | `inventory.read` 키로 교정. operator=본인 거래처(D_Select 적용), branch_manager=지사, admin=전체 |

### 3.3 알고리즘 의사코드

```python
# returns_service.py — ledger_query 리팩토링
async def ledger_query(*, server_id, date_from, date_to, hcode, bcode,
                       detail_for_bcode, gubun, limit=100, offset=0,
                       user_context=None):
    """Sobo34_4 재고원장 — 마스터 + (선택) 디테일 + summary 캐시."""
    # Step 0) DEC-046 권한 d_select
    _d_clause = await build_d_select_clause(user_context)
    gs, ph = _build_gubun_list(gubun)
    hcode_p = _safe_str(hcode) or ""
    bcode_p = _safe_str(bcode) or ""

    # Step 1) 메인 SQL — JOIN 0개 (R2). LIMIT+1 (R3).
    master_sql = apply_limit_offset_syntax(
        SQL_LEDGER_MASTER_NOJOIN.format(gubun_list=ph), server_id,
    )
    lim_b, off_b = limit_offset_bind(limit + 1, offset, server_id)
    master_params = (date_from, date_to, *gs,
                     hcode_p, hcode_p, bcode_p, bcode_p, lim_b, off_b)
    raw = await execute_query(server_id, master_sql, master_params)
    master_rows, has_more = _slice_with_has_more(raw, limit)

    # Step 2) 이름 룩업 — 청크 (R5)
    bcodes = sorted({_safe_str(r.get("Bcode")) for r in master_rows if r.get("Bcode")})
    hcodes_in_page = sorted({hcode_p}) if hcode_p else \
                     sorted({_safe_str(r.get("Hcode")) for r in master_rows if r.get("Hcode")})
    book_names = await _fetch_product_names(server_id, bcodes) if bcodes else {}
    publisher_names = await _fetch_publisher_names(server_id, hcodes_in_page) if hcodes_in_page else {}

    # Step 3) summary — offset==0 일 때만 (R4)
    if offset == 0:
        kpi_rows = await execute_query(server_id, SQL_LEDGER_KPI.format(gubun_list=ph),
                                       (date_from, date_to, *gs, hcode_p, hcode_p))
        kpi = kpi_rows[0] if kpi_rows else {"book_count": 0, "line_count": 0,
                                            "total_qty": 0, "total_amount": 0}
        summary = {
            "book_count": _safe_int(kpi.get("book_count")),
            "line_count": _safe_int(kpi.get("line_count")),
            "total_qty": _safe_int(kpi.get("total_qty")),
            "total_amount": _safe_int(kpi.get("total_amount")),
        }
    else:
        summary = {"book_count": 0, "line_count": 0, "total_qty": 0, "total_amount": 0}

    # Step 4) 디테일 — 단건 (변경 없음)
    detail = []
    if detail_for_bcode:
        detail = await execute_query(server_id, SQL_LEDGER_DETAIL,
                                     (date_from, date_to, detail_for_bcode, hcode_p, hcode_p))

    # Step 5) page meta — ceiling pagination (Sobo54/57 v1.2.2 와 동일)
    visible = len(master_rows)
    total = offset + visible + (1 if has_more else 0)

    return {
        "master": [_row_to_master(r, book_names, publisher_names) for r in master_rows],
        "detail": [_row_to_detail(r) for r in detail],
        "summary": summary,                  # ← kpi 가 summary 로 이름 변경 (응답 호환 유지)
        "kpi": summary,                      # ← (deprecation 윈도우) 1 사이클 유지 후 제거
        "page": {"limit": limit, "offset": offset, "total": total, "has_more": has_more},
    }
```

> **호환성**: `kpi` 키는 1 사이클 동안 `summary` 와 동일 객체로 중복 송신. 프론트 마이그레이션 완료 후 다음 사이클에서 제거. (사용자 룰 "이전 케이스 고려" — 외부 의존을 깨지 않는 점진 마이그레이션).

### 3.4 SQL 상수 변경 — JOIN 제거

```python
# returns_service.py — SQL_LEDGER_MASTER (현재) → SQL_LEDGER_MASTER_NOJOIN (목표)
SQL_LEDGER_MASTER_NOJOIN = (
    "SELECT s.Bcode, s.Scode, s.Gubun, s.Pubun, s.Hcode, "
    "  COALESCE(SUM(s.Gsqut),0) AS total_qty, "
    "  COALESCE(SUM(s.Gssum),0) AS total_amount "
    "FROM S1_Ssub s "
    "WHERE s.Gdate BETWEEN %s AND %s "
    "  AND s.Gubun IN {gubun_list} "
    "  AND (%s='' OR s.Hcode=%s) "
    "  AND (%s='' OR s.Bcode=%s) "
    "  AND s.Yesno='1' "
    "GROUP BY s.Bcode, s.Scode, s.Gubun, s.Pubun, s.Hcode "
    "ORDER BY s.Bcode "
    "LIMIT %s OFFSET %s"
)
# 변경: LEFT JOIN G4_Book b / LEFT JOIN G7_Ggeo g 제거. SELECT 에 s.Hcode 추가
#       (룩업 청크용 distinct 추출). GROUP BY 에 s.Hcode 추가 (의미 보존 — 동일
#       Bcode 라도 Hcode 가 다르면 다른 도서로 식별하는 레거시 동등성).
# 기존 SQL_LEDGER_MASTER 는 회귀 가드용 상수로 1 사이클 유지 후 제거.
```

> 주의 — 기존 회귀 가드 (`test_returns_period_ledger_regression.py::LedgerQueryUsesCountGroupedTests`) 의 fake_execute 매처가 `"GROUP BY s.Bcode" in sql and "ORDER BY s.Bcode" in sql` 를 검사. 변경 후에도 두 토큰 모두 SQL 본문에 존재하므로 기존 테스트 PASS 유지.

---

## 4. 프론트 구현 (T6 — 재작성)

### 4.1 파일

| 파일 | 작업 |
|---|---|
| `frontend/src/lib/returns-api.ts` | **수정** — `LedgerResponse` 에 `summary` 추가. `kpi` 는 deprecated 주석. |
| `frontend/src/app/(app)/returns/ledger/page.tsx` | **재작성** — `useListSession` + `DataGridPager` + `useDynamicPageSize` + `totalsCache` |
| `analysis/layout_mappings/Sobo34_4.md` | **수정** — §9 회귀 체크리스트에 페이저 항목 추가 |

### 4.2 React 패턴 (이미 검증된 7화면 표준 — `customer/page.tsx`, `inbound/reports/period/page.tsx` 등)

```tsx
// returns/ledger/page.tsx — 핵심 hooks
const { snap, replace } = useListSession<Snap>("returns.ledger", { ... });
const { recommended, isAuto } = useDynamicPageSize({ rowHeight: 36 });

useEffect(() => {
  if (!user?.server_id) return;
  load(snap.limit, snap.offset);   // pagination 변경 시 재호출
}, [snap.limit, snap.offset, user?.server_id]);

async function load(limit: number, offset: number, detailForBcode?: string) {
  const res = await returnsPhase2Api.ledger({
    serverId: user.server_id,
    dateFrom, dateTo, hcode, bcode, gubun: gubun || undefined,
    detailForBcode, limit, offset,
  });
  setMaster(res.master);
  if (offset === 0) setSummary(res.summary);  // R4 — totalsCache 보존
  setDetail(res.detail);
  setPage(res.page);
}

return (
  <>
    {/* 검색 패널 (현행 유지) */}
    <DataGridPager
      page={page}
      onChange={({ limit, offset }) => replace({ limit, offset })}
      recommended={recommended}
      isAuto={isAuto}
    />
    {/* 마스터/디테일 (현행 유지) */}
  </>
);
```

### 4.3 UI 동등성 — 현행 보존 + 권한 키 교정

- DBGrid101 7컬럼 / DBGrid201 14컬럼 — 현행 그대로 유지 (T1 layout 매핑 done).
- `requiredPermission: "inventory.write"` → `"inventory.read"` 교정 (`form-registry.ts` L368).
- `crudNotes: "조회 전용 — 5축 회귀 미완 (T7 in_progress)"` → `"조회 전용 — 페이저/JOIN 분리 적용 (DEC-033 표준)"` 갱신.

---

## 5. 테스트 팩 (T6 보강)

### 5.1 파일

| 파일 | 작업 |
|---|---|
| `test/test_returns_period_ledger_regression.py` | **보강** — R2/R3/R4 가드 5건 추가 |
| `test/test_c4_returns_phase2.py` | **보강** — 분기 표 §1.3 의 10건 + 페이저 시나리오 |
| `migration/test-cases/customer_book_ledger_phase2.json` | (out-of-scope — 본 화면 별도 fixture 미생성, 기존 mock 으로 충분) |

### 5.2 필수 케이스 (회귀 가드)

1. `test_no_g4_book_join_in_main_sql` — `SQL_LEDGER_MASTER_NOJOIN` 본문에 `JOIN G4_Book` / `JOIN G7_Ggeo` 미포함 (정적 검사) — **R2**.
2. `test_pager_limit_plus_one_has_more` — `limit=2, fixture=3 rows` ⇒ `has_more=True, master.length==2` — **R3**.
3. `test_summary_only_offset_zero` — `offset=2` 응답에 `summary.total_qty == 0` — **R4**.
4. `test_master_response_includes_book_name_after_lookup` — `_fetch_product_names` mock → `master[0].book_name` 채워짐 — **R2 보강**.
5. `test_in_clause_lookup_chunked_for_lookup` — `_fetch_product_names` 가 청크 분할로 호출 (monkeypatch) — **R5**.
6. `test_router_500_includes_exception_class_name` — `get_returns_ledger` 의 detail message 에 `type(exc).__name__` 포함 — **R6**.
7. `test_permission_inventory_read_required` — operator 토큰으로 D_Select 자기 거래처만 — **R7**.
8. `test_summary_kpi_compatibility_dual_emission` — `summary` 와 `kpi` 동일 값 (호환 윈도우) — 호환성 가드.
9. `test_period_30_days_p95_under_1_5s_with_mocked_db` — **R1** 회귀 가드 (P5 timing).
10. `test_master_split_sum_equals_summary_total_qty` — 마스터 분할 행 SUM == `summary.total_qty` — 결과 동등성.

### 5.3 4서버 DB 등가 (T7 입력)

```bash
debug/probe_backend_all_servers.py \
  --endpoint /api/v1/returns/ledger \
  --query "dateFrom=2026-04-01&dateTo=2026-04-30&offset=0&limit=100" \
  --servers mysql3,mysql5,mysql8,mariadb \
  --diff
```

> 사용자 룰 학습: EUC-KR/UTF-8 인코딩 분기는 read-only 이므로 무관. DECIMAL/float→int 변환은 `_safe_int` 표준 헬퍼 사용 의무 (현재 이미 적용 — 회귀 잔여 없음).

---

## 6. T-Phase 단계 (Phase1 승격 게이트 §3 매핑)

| 단계 | 산출 | 통과 기준 | 현 상태 |
|---|---|---|---|
| **T1** screen_card | `analysis/screen_cards/Sobo34_4.md` | 컴포넌트·이벤트·SQL 인벤토리 100% | ✅ done |
| **T2** event_sql_extract | §1.2 SQL 4건 + §1.3 분기 표 10건 | 모든 SQL 이 contract `data_access` 와 1:1 | ✅ done |
| **T3** contract_yaml | `return_receipt.yaml` v1.1.0 → v1.2.0 동결 | `summary` / `permission` 보강 | 🟡 in_progress (본 계획 산출) |
| **T4** test_pack 골격 | `test/test_returns_period_ledger_regression.py` 7건 | §5.2 항목 PASS | 🟡 in_progress (3/10) |
| **T5** 백엔드 리팩토링 | `returns_service.ledger_query` JOIN 분리 + 페이저 | smoke import + 라우트 OPTIONS 200 | ⏳ pending |
| **T6** 프론트 재작성 | `page.tsx` + `returns-api.ts` | `tsc --noEmit` 0, `eslint` 0 신규 warn | ⏳ pending |
| **T7** equivalence_run | `regression_phase2.py` + `probe_backend_all_servers.py` | 5축 모두 PASS, 회귀 0건 | ⏳ pending |
| **T8** promotion | `form-registry.ts` Sobo34_4 `phase: "phase2" → "phase1"` + `phase2-screen-cards.json` 1건 제거 + `porting-screens.json` 동기 + `web-porting-progress.json` 갱신 | 사이드바 초록 체크 노출 + dashboard 카드 수 갱신 | ⏳ pending — **본 계획 최종 단계** |

---

## 7. 작업 순서 (TODO 단위 — 체크포인트별 회귀 실행)

| # | 작업 | 산출 | 회귀 |
|---|---|---|---|
| 1 | T3 — contract v1.2.0 보강 (summary 키 추가, 권한 키 교정) | `return_receipt.yaml` diff | yamllint |
| 2 | T5-A — `SQL_LEDGER_MASTER_NOJOIN` 신설 + 기존 상수 alias | `returns_service.py` diff | mypy |
| 3 | T5-B — `ledger_query` 본문 LIMIT+1 + summary 분기 + 청크 룩업 | `returns_service.py` diff | unit test 7건 PASS |
| 4 | T5-C — 라우터 detail.message 회귀 가드 추가 | `routers/returns.py` diff | smoke import |
| 5 | T6-A — `LedgerResponse` 에 `summary` 추가 (`kpi` deprecated 주석) | `returns-api.ts` diff | `tsc --noEmit` |
| 6 | T6-B — `page.tsx` `useListSession` + `DataGridPager` 마이그레이션 | `page.tsx` diff | `tsc` 0, `eslint` 0 |
| 7 | T4 — 회귀 테스트 10건 작성/보강 | `test_returns_period_ledger_regression.py` diff | `pytest` PASS |
| 8 | T7-A — 4서버 probe (실 DB 환경) | `reports/probe-ldg-inv-detail-2026-MM-DD.json` | 4서버 동등 |
| 9 | T7-B — `regression_phase2.py` 5축 체크 추가 | `reports/regression-2026-MM-DD.json` | 5축 PASS |
| 10 | **T8 — 승격** | `form-registry.ts` phase1 + `phase2-screen-cards.json` 제거 + 대시보드 동기 | 사이드바 초록 ✅ |

---

## 8. 위험 및 보완

| 위험 | 영향 | 보완 |
|---|---|---|
| **GROUP BY 에 Hcode 추가로 행수 증가** | 동일 Bcode 라도 Hcode 별 분리되어 마스터 행 수 증가 가능성 | 레거시는 항상 `Hcode=Edit107.Text` 단일 필터(L396) 가정 → Hcode 추가는 멀티-출판사 케이스에서만 영향. 테스트 fixture 로 단일/복수 출판사 양쪽 PASS |
| **Sb_Csum 이월 잔량 미반영** | "유통반품재고" 분기 (L566) 가 아직 누락 | P3 (`_accumulate_inv_detail_row`) 에서 처리. P2 는 BETWEEN 단순 SUM 만 (스코프 명확화) |
| **`Bdate is null` 분기 (L390)** 가 모던 응답에 빠짐 | 입출고 전체가 아닌 "정상 출고" 만 표시되어 결과 차이 가능 | Step 1 메인 쿼리 WHERE 에 `(s.Bdate IS NULL OR s.Bdate=' ')` 옵션 추가 — `gubun='반품'` 일 때만. (DEC-033 새 SQL 0건 정책 — WHERE 절 보강만) |
| **`kpi`/`summary` 중복 송신 페이로드 증가** | 응답 크기 ~10% 증가 (페이지 무관) | 1 사이클 후 `kpi` 키 제거 (deprecation 윈도우). 응답 크기 영향 미미 (수치 4개) |
| **권한 키 교정으로 기존 사용자 접근 차단** | `inventory.write` 보유자만 접근하던 사용자가 `inventory.read` 미보유 시 403 | RBAC seed 재검증 — `inventory.write` 보유자는 자동 `inventory.read` 도 보유 (계층 권한). `test_permission_inventory_read_inherited` 가드 추가 |
| **mysql3 LIMIT+1 페이저로도 timeout** | Sobo54/57 v1.2.2 와 동일 회귀 | §3.2 R1~R6 모두 적용. 추가로 `s.Yesno='1'` 인덱스 활용 EXPLAIN 검증 (T7-A 추가 항목) |
| **`SUM/AVG → Decimal` Pydantic 검증 실패** | 500 (검증 시점) | 모든 응답 정수 필드는 `_safe_int(grand.get(...))` 통과 (현재 이미 적용) |

---

## 9. 산출물 인덱스 (PR 첨부 표준)

승격 PR 에는 다음 7개 링크를 본문에 첨부 (T1~T8 산출):

1. `analysis/screen_cards/Sobo34_4.md`
2. 본 계획 §1.2 / §1.3 (T2 SQL/이벤트 추출)
3. `migration/contracts/return_receipt.yaml` v1.2.0 (`endpoints[/returns/ledger]`)
4. `backend/app/services/returns_service.py` (`ledger_query` + `SQL_LEDGER_MASTER_NOJOIN`) + `backend/app/routers/returns.py`
5. `frontend/src/app/(app)/returns/ledger/page.tsx` + `frontend/src/lib/returns-api.ts` + `analysis/layout_mappings/Sobo34_4.md`
6. `test/test_returns_period_ledger_regression.py` 10건 PASS 결과
7. `reports/probe-ldg-inv-detail-...json` + `reports/regression-...json`

---

## 10. 변경 이력

| 일자 | 변경 |
|---|---|
| 2026-04-23 | 최초 draft. Sobo34_4 phase2 → phase1 승격 + 페이징 속도개선 T1~T8 전체 계획. Sobo54/57 v1.2.2 / 거래처원장 P2 (PLAN-LDG-CUSTOMER-2026-04-22) 의 7개 회귀 가드(R1~R7) 를 본 화면에 일반화 적용. 기존 회귀 가드 테스트 호환을 위한 SQL 토큰 보존 전략 명시. |
