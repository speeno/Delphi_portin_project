# 레이아웃 매핑: Sobo39 (할인율 대표 마스터) → 모던 `/master/discount` (READ only, 1차)

DEC-028 — `Subu39/Sobo39.*` 단일 원천. DEC-023 (단일 원천 6폼 — Sobo39 4 변종 중 대표 1폼만 1차 노출). 11 섹션 구조.

## 0. 입력 산출물

- DFM HTML/JSON: [`tools/.../legacy_source_root/Subu39/Sobo39.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu39/Sobo39.html), `.form.json`, `.tree.json`, `.meta.json`
- 변형 폴더: **accelerator 산출물 미생성** (`Subu39_*` 0건). `form-registry.ts` 메타에는 `Subu39_1/_2/_5` 가 있음 — accelerator backlog (OOS-MAS-5)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu39.dfm`](../../legacy_delphi_source/legacy_source/Subu39.dfm)
- 화면 카드: [`analysis/screen_cards/Sobo39.md`](../screen_cards/Sobo39.md)
- 모던 라우트: [`도서물류관리프로그램/frontend/src/app/(app)/master/discount/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/master/discount/page.tsx)
- 계약: `migration/contracts/master_data.yaml` (`/api/v1/masters/discount`)

## 1. 의미 분기 — 복합 조건 폼·서브 그리드 → 1차 단순 4컬럼 그리드

레거시 Sobo39 는 dfm 위젯 수 최대(13개의 RadioButton, 16개의 Edit, 3개의 DataSet T3_Sub91~93). 4 변종(`Sobo39_1/_2/_5`) 의 차이는 검색 조건 조합·집계 단위 차이로 추정. 모던 1차는 DEC-023 단일 원천 정책에 따라 **대표 1폼**만 노출하고, 그 안에서도 `G7_Ggeo.Gpper` 4컬럼(코드/거래처명/할인율/Ocode) READ 만 보여준다(검색 라디오·기간 필터·집계 그리드는 phase2). → 위젯 매핑은 DBGrid101 4컬럼 + wrapper 만 부착.

## 2. dfm 영역 인벤토리 (tree.json 기준)

- Sobo39 (root)
  - **Panel001** (검색 폼)
    - `Label101, Panel101, Edit101, Button101, Button201, Panel105, Edit102~105, DateEdit1, Button701/702, dxButton1`
  - **Panel002** → `DBGrid101`
  - **Panel003** → `DBGrid201` (서브 그리드)
  - **Panel004** (라디오 4개): `RadioButton4~7`
  - **Panel005** (라디오 3개): `RadioButton1~3`
  - **Panel006** (라디오 3개): `RadioButton8/9/0`
  - **Panel011** (라디오 3개): `RadioButton11/12/13`
  - **Panel012** (집계 라벨·입력): `myLabel3d1~4, Label300, Panel013/014/015, Edit201~204/301~304/401~404`
  - **Panel007** (진행률)
  - DataSource1/2 + **T3_Sub91/92/93** (DataSet 3종 — 일자별/거래처별/도서별 집계)

## 3. 상단 그리드 패널 위젯 매핑 (1차 모던에 노출되는 부분)

| dfm 위젯 | 의미 | 모던 위치 | `data-legacy-id` |
| --- | --- | --- | --- |
| `Sobo39.DBGrid101` | wrapper | `<DataGrid>` `<table>` | `Sobo39.DBGrid101` |
| `Sobo39.DBGrid101.GCODE` | 거래처/출판사 코드 | `<th>` (key=gcode) | `Sobo39.DBGrid101.GCODE` |
| `Sobo39.DBGrid101.GNAME` | 거래처/출판사명 | `<th>` (key=gname) | `Sobo39.DBGrid101.GNAME` |
| `Sobo39.DBGrid101.GPPER` | 할인율(%) | `<th>` (key=gpper, align=right) | `Sobo39.DBGrid101.GPPER` |
| `Sobo39.DBGrid101.OCODE` | Ocode | `<th>` (key=ocode) | `Sobo39.DBGrid101.OCODE` |

## 4. 입력·라디오·집계 패널 (1차 미노출)

`Panel001/004/005/006/011/012` 일체 — 1차 미노출 (§6).

## 5. 메모/기타

해당 없음.

## 6. out-of-scope 위젯 (1차 미부착)

- 정적 라벨, 코너 위젯
- **Panel001 검색 입력** (Edit101~105, DateEdit1, Button101/201/701/702, dxButton1) — phase2
- **Panel003 (DBGrid201) 서브 그리드** — phase2
- **Panel004/005/006/011** 라디오버튼 13개 (집계 단위·기간 단위 옵션) — phase2
- **Panel012** 집계 라벨·합계 입력 (`Edit201~204`, `Edit301~304`, `Edit401~404`) — phase2
- T3_Sub91/92/93 (전체 컬럼 — phase2 집계)
- `Panel007/ProgressBar0/1` — 진행률
- 변형 `Sobo39_1/_2/_5` — accelerator 산출물 미생성 (OOS-MAS-5)

## 7. deltas (모던 신설)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` (코드/거래처명 LIKE) | 단일 검색박스 — dfm 의 라디오·기간 필터 흡수 (1차) |
| 조회 버튼 | 페이징 트리거 |
| `<DataGridPager>` | 서버 페이징 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `dxButton1.OnClick` (조회) | `load()` 페이징 트리거 (검색 박스 호출) |
| `RadioButton*.OnClick` | 미노출 (§6) |
| `DBGrid101.OnCellClick` | (1차 무동작 — READ only) |

## 9. 변형 차이 (`Sobo39` 본 vs `Sobo39_1/_2/_5`)

**accelerator 산출물 0건** — `legacy_source_root/Subu39_*` 폴더가 미생성. `form-registry.ts` 메타에 `Subu39_1/_2/_5` 가 등록되어 있고 화면 카드 분석에서 4 변종이 식별되었으나, dfm 산출물 생성기가 아직 처리하지 못함. → DEC-023 단일 원천 정책에 따라 phase1 은 본 폼(`Sobo39`) 4컬럼만 노출. 변형 산출물 생성은 [`master_data.yaml`](../../migration/contracts/master_data.yaml) `out_of_scope.OOS-MAS-5` 백로그에 등재.

## 10. 회귀 가드 체크리스트

- [ ] `master/discount/page.tsx` 동작 변화 0
- [ ] tsc/eslint 0 신규
- [ ] `test/test_pagination_contracts.py::C9MastersListPageContract::test_discount` PASS
- [ ] `test/test_masters_q_search.py` (discount) PASS
- [ ] phase2 변형 산출물 생성 후 §3/§4/§9 보강

## 11. 참조

- DEC-019, DEC-023, DEC-028
- HA-RET-01, OOS-MAS-5
- 화면 카드: `analysis/screen_cards/Sobo39.md`
- 계약: `master_data.yaml` v1.1.0
- 선례: `Sobo27.md`, `Sobo21.md`
