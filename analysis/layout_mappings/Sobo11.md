# 레이아웃 매핑: Sobo11 (거래처 마스터) → 모던 `/master/customer` (목록 + 상세)

DEC-028 — dfm 산출물(`Subu11/Sobo11.*`)을 모던 신규 화면 작성의 영구 입력으로 사용. 본 노트는 "분석 → 모던 위젯 ID 부착(`data-legacy-id`)"의 단일 원천이다. C2(Sobo27.md) / C6(Sobo21.md) 11 섹션 구조 그대로 재사용 (SOLID-S/O).

## 0. 입력 산출물 (참고용)

- DFM HTML/JSON: [`tools/.../legacy_source_root/Subu11/Sobo11.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu11/Sobo11.html), `Sobo11.form.json`, `Sobo11.tree.json`, `Sobo11.meta.json`
- 변형 폴더: **부재** (`Subu11_*` 0건 — §9 참조)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu11.dfm`](../../legacy_delphi_source/legacy_source/Subu11.dfm)
- 화면 카드: [`analysis/screen_cards/Sobo11.md`](../screen_cards/Sobo11.md)
- 모던 라우트:
  - 목록: [`도서물류관리프로그램/frontend/src/app/(app)/master/customer/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/master/customer/page.tsx)
  - 상세: [`도서물류관리프로그램/frontend/src/app/(app)/master/customer/[gcode]/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/master/customer/[gcode]/page.tsx)
- 계약: [`migration/contracts/master_data.yaml`](../../migration/contracts/master_data.yaml) (`/api/v1/masters/customer*`)

## 1. 의미 분기 — 단일 폼(목록+상세 동시) → 목록 / 상세 라우트 2개로 분리

레거시 Sobo11 은 한 화면에 **상단 그리드(Panel001/DBGrid101) + 하단 등록·수정 패널(Panel002, Edit101~129)** 이 동시에 노출되는 윈도우 폼이다. 모던에서는 라우트를 두 개로 분리:

| 영역 | 모던 라우트 |
| --- | --- |
| Panel001 (DBGrid101) | `/master/customer` (목록) |
| Panel002 (상세 등록·수정 폼) | `/master/customer/[gcode]` + `/master/customer/new` |
| Panel003/004 (DBGrid201 + 구분 등록폼) | `/master/customer/[gcode]` · `/master/customer/new` 하위 `CustomerCategoryPanel` (거래처구분 관리) |

→ 위젯 ID 매핑은 **각 영역이 속한 라우트 페이지에 한정해서 부착**한다. 목록 페이지에는 DBGrid101만, 상세/신규에는 Panel002(Edit101~130) + Panel004(구분 CRUD)를 함께 부착. `Edit101` 드롭다운은 구분 CRUD 후 `reloadKey`로 목록 재조회.

## 2. dfm 영역 인벤토리 (tree.json 기준)

- Sobo11 (root)
  - 코너 버튼: `CornerButton2/3/4` (창 닫기·최소화 등 — 모던에서는 OS chrome 으로 대체, §6 참조)
  - 라벨: `Label002/003/309` (정적 텍스트 — `data-legacy-id` 부착 대상 아님)
  - **Panel001** (그리드 영역)
    - `DBGrid101` — 거래처 리스트 (Gcode/Gname/Hcode/Gtel1/Gtel2/Gpost/Gjuso 등)
  - **Panel002** (등록·수정 폼)
    - 라벨: `Label100~111`, `Label130`, `Label300/301`
    - Panel100 액션 버튼: `Button101` (등록/저장), `Button102` (수정/취소), `Button103` (삭제)
    - Panel101~129 (필드 컨테이너)
    - Edit101~129 (입력)
    - `Button104` (조회/검색 보조)
    - `CheckBox1/2`

## 3. 상단 그리드 패널 위젯 매핑 — TabOrder 보존표

목록 페이지 = `master/customer/page.tsx`. 검색 입력은 dfm 의 `Edit*`와 별도(모던 신설) — §7 deltas 참조.

| dfm 위젯 | TabOrder | 의미 | 모던 위치 | `data-legacy-id` |
| --- | --- | --- | --- | --- |
| `Sobo11.DBGrid101` | (table) | 거래처 그리드 wrapper | `<DataGrid>` `<table>` | `Sobo11.DBGrid101` |
| `Sobo11.DBGrid101.GCODE` | col0 | 거래처 코드 | `<th>` (key=gcode) | `Sobo11.DBGrid101.GCODE` |
| `Sobo11.DBGrid101.GNAME` | col1 | 거래처명 | `<th>` (key=gname) | `Sobo11.DBGrid101.GNAME` |
| `Sobo11.DBGrid101.HCODE` | col2 | 분류 코드 | `<th>` (key=hcode) | `Sobo11.DBGrid101.HCODE` |
| `Sobo11.DBGrid101.GTEL1` | col3 | 전화1 | `<th>` (key=gtel1) | `Sobo11.DBGrid101.GTEL1` |
| `Sobo11.DBGrid101.GTEL2` | col4 | 전화2 | `<th>` (key=gtel2) | `Sobo11.DBGrid101.GTEL2` |
| `Sobo11.DBGrid101.GPOST` | col5 | 우편번호 | `<th>` (key=gpost) | `Sobo11.DBGrid101.GPOST` |
| `Sobo11.DBGrid101.GJUSO` | col6 | 주소 | `<th>` (key=gjuso) | `Sobo11.DBGrid101.GJUSO` |

### 3.1 목록 검색 필터 (모던 신설 — minimal 세트, 2026-05)

dfm 의 검색용 `Edit*` 1:1 대응 위젯이 없어 모던 신설(§7 deltas, `data-legacy-id` 미부착). 서버측 WHERE 확장으로 페이지·total 정합 유지.

| 모던 위젯 | 파라미터 | 동작 | 컬럼 |
| --- | --- | --- | --- |
| 검색 `<Input id="q">` | `q` | 기존 LIKE(양끝 와일드카드) | `Gcode`/`Gname` |
| 거래처구분 `<select id="f-gubun">` | `gubun` | 단일 선택(콤보) — `customerCategoryList`(G1_Gbun)로 로드, 코드 정확 일치 | `G1_Ggeo.Gubun = 선택 Gcode` |
| 지역 `<Input id="f-jubun">` | `jubun` | 부분 일치 LIKE(`_likify`) | `G1_Ggeo.Jubun` |
| 거래종료 제외 `<input id="f-exterm" type=checkbox>` | `excludeTerminated` | 토글(기본 OFF) | `Gname NOT LIKE '[X]%' AND IFNULL(Gubun,'')<>'X 거래종료'` |
| 초기화 `<Button>` | — | 필터 모두 비우고 재조회(`resetFilters`) | — |

세션 보존: `useListSession<Snap>` 키 `master.customer` 재사용 — `Snap = { q, gubun, jubun, excludeTerminated, offset, limit }`(누락 필드 기본값 채움 → 하위호환).

## 4. 상세/등록 패널 위젯 매핑 (Panel002 + Panel004)

상세/신규 페이지 = `master/customer/[gcode]/page.tsx`, `master/customer/new/page.tsx`. Panel004(거래처구분 마스터)는 상세 폼 하단에 통합.

| dfm 위젯 | 의미 | 모던 위치 | `data-legacy-id` |
| --- | --- | --- | --- |
| `Sobo11.Panel002` | 상세 폼 wrapper | `<div className="grid ...">` | `Sobo11.Panel002` |
| `Sobo11.Edit101` | 거래처구분(`gbun_name`/`gubun`) — 레거시 `TFlatComboBox` | `MasterGbunSelect`: **G1_Gbun 목록만** 선택, 표시=`Gubun`→Gname 조인(코드·명칭 이중 lookup); 고아 `Sname`은 경고만 | `Sobo11.Edit101` |
| `Sobo11.Edit102` | 거래처지역(`jubun`) | `<Input>` 거래처지역 | `Sobo11.Edit102` |
| `Sobo11.Edit103` | 거래처코드(`gcode`) | `<Input>` 거래처코드 | `Sobo11.Edit103` |
| `Sobo11.Edit104` | 보조코드(`ocode`) | `<Input>` 거래처코드2 | `Sobo11.Edit104` |
| `Sobo11.Edit105~130` | 상세 필드군 (`gname`/`gposa`/`gnumb`/`guper`/`gjomo`/`gpost`/`gtel*`/`gfax*`/`gadd*`/`grat*`/`gqut1`/`gbigo`/`name*`/`pubun`/`email`/`gnum1`) | 상세 입력 폼 | 동일 ID |
| `Sobo11.CheckBox1` | 계산서 발행유무(`yesno`) | 상세 입력 폼 | `Sobo11.CheckBox1` |
| `Sobo11.CheckBox2` | 출고정지(`grat9`) | 상세 입력 폼 | `Sobo11.CheckBox2` |
| `Sobo11.Button101` | 신규 등록 | `/master/customer/new` + 등록 버튼 | `Sobo11.Button101` |
| `Sobo11.Button102` | 저장 | 상세 저장 버튼 | `Sobo11.Button102` |
| `Sobo11.Button103` | 삭제 | 상세 삭제 버튼 | `Sobo11.Button103` |
| `Sobo11.FormClose` | 목록 복귀 | `<Button variant="ghost">목록` | `Sobo11.FormClose` |
| `Sobo11.DBGrid201` | 거래처구분 그리드 | 상세/신규 `CustomerCategoryCollapsible` (기본 접힘) | `Sobo11.DBGrid201` |
| `(독립메뉴)` | 거래처구분 | `/master/customer-category` 단독 진입(동일 G1_Gbun CRUD 패널 재사용) | 동일 `data-legacy-id` 집합 |
| `Sobo11.Edit201/202` | 거래처구분 코드/명 | 상세/신규 구분 관리 패널 | 동일 ID |
| `Sobo11.Button201/202/203` | 거래처구분 등록/저장/삭제 | 상세/신규 구분 관리 패널 | 동일 ID |

### 4.1 지사 마스터 (Seok10 / H2_Gbun) — Panel003 과 별개

레거시 `Sobo11.Button007Click` → `Seok10` 모달(`H2_Gbun` CRUD). **Panel003/004 는 G1_Gbun(거래처구분) 전용** — 혼동 금지.

| 레거시 | 의미 | 모던 | `data-legacy-id` |
| --- | --- | --- | --- |
| `Button007` | 지사 관리 열기 | 상세/신규 `CustomerBranchCollapsible` | `Seok10.Seok10` |
| `Seok10.DBGrid101` | 지사 그리드 | `CustomerBranchPanel` DataGrid | `Seok10.DBGrid101` |
| `Seok10.BitBtn101/102` | 등록/저장 | 지사 패널 버튼 | 동일 ID |
| API | `H2_Gbun` CRUD | `GET/POST/PATCH/DELETE /api/v1/masters/customer/{gcode}/branches` | `master_data.yaml` SQL-MAS-3H-* |

> 상세 필드 매핑 정본은 `Sobo11.pas_analysis.json runtime_assignments` 기준으로 유지한다.

## 5. 메모/기타 (해당 없음)

Sobo11 은 메모 영역이 없다. (S1_Memo 흐름은 Sobo21/Sobo27 만 해당.)

## 6. out-of-scope 위젯 (1차 미사용 — `data-legacy-id` 미부착)

- `CornerButton2/3/4` — OS chrome 으로 대체
- `Label002/003/309/100~130/300/301` — 정적 텍스트, 시각 라벨만
- `Sobo11.Button104` — 우편번호 보조 검색(Seak40) 2차
- `Panel125/126/127/129` 고정 위치 패널 라벨 — 모던 섹션으로 흡수

## 7. deltas (모던 신설 / dfm 미존재)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` | 단일 LIKE 검색박스 — dfm 의 `Sobo11.Edit*` 검색용은 직접 1:1 대응 위젯이 없어 신설(`data-legacy-id` 미부착) |
| 필터 바 `구분 select·지역 input·거래종료 제외 체크` (§3.1) | 사용자 검색 편의 필터(minimal 세트) — dfm 미존재, 서버 WHERE 확장(`gubun`/`jubun`/`excludeTerminated`), 미부착 |
| 조회 버튼 `<Button>조회` / 초기화 `<Button>초기화` | 페이징 트리거 / 필터 리셋 — dfm 에는 자동 fetch (모던 신설, 미부착) |
| `<DataGridPager>` | 서버 사이드 페이징 — dfm 미존재 (전체 메모리 로드) |
| `Wave A` 배지(허브 카드) | 정보성 — dfm 미존재 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `DBGrid101.OnDblClick` | `<DataGrid onRowClick={r => router.push(...)}>` (단일 클릭으로 상세 진입) |
| `Button102.OnClick` (수정/저장) | `save()` → `masterApi.customerUpdate(gcode, body)` |
| `FormClose` | `router.push("/master/customer")` |

## 9. 변형 차이 (variant 폴더)

**`Subu11_*` 변형 폴더 0건** — accelerator 산출물 트리에 변형 폴더가 존재하지 않음. 즉 거래처 마스터는 1버전만 운영되어 왔고 UI/로직 variant 가 없음. 향후 변형이 발견되면 본 §9 와 [`master_data.yaml`](../../migration/contracts/master_data.yaml) `customer_variants` 섹션에 추가.

## 10. 회귀 가드 체크리스트

- [ ] `data-legacy-id` 부착 후에도 `master/customer/page.tsx` / `[gcode]/page.tsx` 의 검색·조회·행클릭·저장 동작 변화 0
- [ ] tsc/eslint 경고 0 신규
- [ ] `test/test_pagination_contracts.py::C9MastersListPageContract::test_customer` PASS
- [ ] `test/test_masters_q_search.py` PASS
- [ ] §6 미부착 위젯은 모던에 신규 도입 시 §3/§4 표 보강 후 부착

## 11. 참조

- DEC-019 (마스터 PATCH only / Delete OFF), DEC-023 (단일 원천 6폼), DEC-028 (dfm 산출물 영구 입력), DEC-016/017/018
- HA-RET-01 (C9 retrofit 묶음)
- 화면 카드: `analysis/screen_cards/Sobo11.md`
- 계약: `migration/contracts/master_data.yaml` v1.1.0
- 테스트: `test/test_pagination_contracts.py::C9MastersListPageContract`, `test/test_masters_q_search.py`
- 동일 패턴 선례: `analysis/layout_mappings/Sobo27.md` (C2), `analysis/layout_mappings/Sobo21.md` (C6)

## 12. Wave C — 레거시 버튼 → API → 테스트 ID 한 줄 표 (CRUD 잔여 추적)

DEC-019 정책(마스터 = PATCH only / Delete OFF) 하에서 **UI 버튼·가드·audit** 의 레거시 1:1 매핑을 행 단위로 고정한다 (`docs/crud-backlog.md` Wave C).

| 레거시 버튼 (Subu11.pas) | 의미 | 모던 API (master_data.yaml) | UI 노출 (현 phase1) | 테스트 ID (회귀 PASS 시 표기) |
| --- | --- | --- | --- | --- |
| `Button101.OnClick` (등록/저장) | INSERT/UPDATE G1_Ggeo | `POST /api/v1/masters/customer` · `PATCH .../{gcode}` | 상세/신규 폼 액션 | `test_master_crud_api_contract.py` |
| `Button102.OnClick` (수정/취소) | 폼 모드 토글 (DB 호출 없음) | (UI 전용) | 상세 라우트 폼 헤더 | (UI 전용 — 회귀 미적용) |
| `Button103.OnClick` (삭제) | DELETE | `DELETE /api/v1/masters/customer/{gcode}` | ON | `test_master_crud_api_contract.py` |
| `Button201/202/203` | 구분 CRUD (`G1_Gbun`) | `/api/v1/masters/customer-categories` CRUD | 목록 탭 ON | `test_master_crud_api_contract.py` |
| `Button104.OnClick` (조회/검색) | 키워드 fetch | `GET /api/v1/masters/customer?q=…` | 목록 검색 입력 | `test_masters_q_search::test_customer` |
