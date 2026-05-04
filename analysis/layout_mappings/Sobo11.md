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
| Panel002 (상세 등록·수정 폼) | `/master/customer/[gcode]` (상세) |

→ 위젯 ID 매핑은 **각 영역이 속한 라우트 페이지에 한정해서 부착**한다. 목록 페이지에는 DBGrid 위젯만, 상세 페이지에는 Panel002 의 Edit/Button 위젯만 부착.

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

## 4. 상세/등록 패널 위젯 매핑 (Panel002)

상세 페이지 = `master/customer/[gcode]/page.tsx`.

| dfm 위젯 | 의미 | 모던 위치 | `data-legacy-id` |
| --- | --- | --- | --- |
| `Sobo11.Panel002` | 상세 폼 wrapper | `<div className="grid ...">` | `Sobo11.Panel002` |
| `Sobo11.Edit101` | 거래처명 (Gname) | `<Input>` 거래처명 | `Sobo11.Edit101` |
| `Sobo11.Edit102` | 분류명 (Gbun_name, read-only) | `<Input disabled>` 분류명 | `Sobo11.Edit102` |
| `Sobo11.Edit103` | 전화1 (Gtel1) | `<Input>` 전화1 | `Sobo11.Edit103` |
| `Sobo11.Edit104` | 전화2 (Gtel2) | `<Input>` 전화2 | `Sobo11.Edit104` |
| `Sobo11.Edit105` | 우편번호 (Gpost) | `<Input>` 우편번호 | `Sobo11.Edit105` |
| `Sobo11.Edit106` | 주소 (Gjuso) | `<Input>` 주소 | `Sobo11.Edit106` |
| `Sobo11.Edit107` | 비고 (Gbigo) | `<Input>` 비고 | `Sobo11.Edit107` |
| `Sobo11.Button101` | 등록(Insert) | — (1차 PATCH 만, §6) | (미부착) |
| `Sobo11.Button102` | 수정/저장 → `<Button>` 저장 | `<Button>저장 (수정)` | `Sobo11.Button102` |
| `Sobo11.Button103` | 삭제 | — (DEC-019 비활성, §6) | (미부착) |
| `Sobo11.FormClose` | 목록 복귀 | `<Button variant="ghost">목록` | `Sobo11.FormClose` |

> Edit108~129 등 추가 필드(연락처 다중·기타 검색 보조)는 1차 모던 폼에 미노출 — §7 deltas 참조.

## 5. 메모/기타 (해당 없음)

Sobo11 은 메모 영역이 없다. (S1_Memo 흐름은 Sobo21/Sobo27 만 해당.)

## 6. out-of-scope 위젯 (1차 미사용 — `data-legacy-id` 미부착)

- `CornerButton2/3/4` — OS chrome 으로 대체
- `Label002/003/309/100~130/300/301` — 정적 텍스트, 시각 라벨만
- `Sobo11.Button101` (Insert), `Sobo11.Button103` (Delete) — DEC-019: 1차 PATCH only
- `Sobo11.Button104` — 보조 검색(Lookup) — 1차 미구현
- `Sobo11.CheckBox1/2` — 활성/사용여부 토글 — 1차 미노출
- `Sobo11.Edit108~129`, `Sobo11.Edit125~129`, `Panel125/126/127/129` — 추가 연락처·메모 슬롯 (phase2)

## 7. deltas (모던 신설 / dfm 미존재)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` | 단일 LIKE 검색박스 — dfm 의 `Sobo11.Edit*` 검색용은 직접 1:1 대응 위젯이 없어 신설(`data-legacy-id` 미부착) |
| 조회 버튼 `<Button>조회` | 페이징 트리거 — dfm 에는 자동 fetch (모던 신설, 미부착) |
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
| `Button101.OnClick` (등록/저장) | INSERT/UPDATE G7_Ggeo | `POST /api/v1/masters/customer` · `PATCH .../{gcode}` | 상세 라우트 폼 액션 | `test_pagination_contracts::C9MastersListPageContract::test_customer` (목록), Wave C 후속에 `test_master_customer_audit` 추가 예정 |
| `Button102.OnClick` (수정/취소) | 폼 모드 토글 (DB 호출 없음) | (UI 전용) | 상세 라우트 폼 헤더 | (UI 전용 — 회귀 미적용) |
| `Button103.OnClick` (삭제) | DELETE | (DEC-019 — UI 미노출) | **OFF** | (Wave C 추가 시 `test_master_customer_delete_blocked` 부정 회귀) |
| `Button104.OnClick` (조회/검색) | 키워드 fetch | `GET /api/v1/masters/customer?q=…` | 목록 검색 입력 | `test_masters_q_search::test_customer` |
