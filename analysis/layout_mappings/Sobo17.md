# 레이아웃 매핑: Sobo17 (출판사·G7거래처 마스터) → 모던 `/master/publisher` (목록 only, 1차)

DEC-028 — `Subu17/Sobo17.*` 단일 원천. 11 섹션 구조.

## 0. 입력 산출물

- DFM: [`tools/.../legacy_source_root/Subu17/Sobo17.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu17/Sobo17.html), `.form.json`, `.tree.json`, `.meta.json`
- 변형: `Subu17_1/Sobo17_1.*` (위젯 동일, §9 미세 차이만)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu17.dfm`](../../legacy_delphi_source/legacy_source/Subu17.dfm)
- 화면 카드: [`analysis/screen_cards/Sobo17.md`](../screen_cards/Sobo17.md)
- 모던 라우트: [`도서물류관리프로그램/frontend/src/app/(app)/master/publisher/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/master/publisher/page.tsx)
- 계약: `migration/contracts/master_data.yaml` (`/api/v1/masters/publisher`)

## 1. 의미 분기 — 마스터·서브 그리드 + 등록 폼 → 1차 단순 목록

레거시 Sobo17 은 Sobo11/14 보다 한 단계 복잡: **DBGrid101(출판사 목록) + DBGrid201(서브: 출판사별 도서 등) + Panel002 등록 폼 + Panel004 보조 패널(상태바 StBar101 포함)**. 모던 1차는 `READ only 단순 목록`만 노출(상세/수정은 후속, DEC-019 보수적 적용). → 위젯 매핑은 DBGrid101 컬럼만 부착하고, 나머지는 §6 out-of-scope 로 명시.

## 2. dfm 영역 인벤토리 (tree.json 기준)

- Sobo17 (root)
  - 코너: `CornerButton2/3/4`
  - **Panel001** → `DBGrid101` + `StBar101` (상태바)
  - **Panel003** → `DBGrid201` (서브 그리드 — 후속)
  - **Panel004** (서브 등록·수정 폼)
    - Panel200 → `Button201/202/203`, Panel201/202, Edit201/202
  - **Panel007** (진행률 바 — `ProgressBar0/1`, Panel008/009/010)
  - **Panel002** (메인 등록·수정 폼)
    - 라벨/Panel100~119
    - `Button101/102/103/104`, `Edit101~124`, `CheckBox1`

## 3. 상단 그리드 패널 위젯 매핑

목록 페이지 = `master/publisher/page.tsx`.

| dfm 위젯 | 의미 | 모던 위치 | `data-legacy-id` |
| --- | --- | --- | --- |
| `Sobo17.DBGrid101` | 출판사 그리드 wrapper | `<DataGrid>` `<table>` | `Sobo17.DBGrid101` |
| `Sobo17.DBGrid101.GCODE` | 코드 | `<th>` (key=gcode) | `Sobo17.DBGrid101.GCODE` |
| `Sobo17.DBGrid101.GNAME` | 출판사명 | `<th>` (key=gname) | `Sobo17.DBGrid101.GNAME` |
| `Sobo17.DBGrid101.HCODE` | 분류 | `<th>` (key=hcode) | `Sobo17.DBGrid101.HCODE` |
| `Sobo17.DBGrid101.CHEK1` | Chek1 | `<th>` (key=chek1) | `Sobo17.DBGrid101.CHEK1` |
| `Sobo17.DBGrid101.CHEK2` | Chek2 | `<th>` (key=chek2) | `Sobo17.DBGrid101.CHEK2` |

## 4. 등록·수정 패널 (1차 미노출)

상세/수정 폼 (Panel002 의 Edit101~124, Button101~104) 은 1차 미노출 — §6 out-of-scope. 후속 라우트(`master/publisher/[gcode]`) 신설 시 본 §4 표를 기준으로 부착할 것.

## 5. 메모/기타

해당 없음.

## 6. out-of-scope 위젯 (1차 미부착)

- `CornerButton2/3/4`, 정적 라벨
- **Panel002 전체** (등록·수정 폼) — 1차 READ only, 후속 사이클에서 부착
- **Panel003/Panel004** (서브 그리드·서브 폼 — phase2)
- `StBar101` — 상태바 (모던 미구현)
- `Panel007/ProgressBar0/1` — 진행률 (모던 미구현)
- `Sobo17.CheckBox1` — 활성 토글

## 7. deltas (모던 신설)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` | 단일 LIKE 검색 — 모던 신설 |
| 조회 버튼 | 페이징 트리거 |
| `<DataGridPager>` | 서버 사이드 페이징 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `DBGrid101.OnCellClick` | (1차 무동작 — onRowClick 미사용, 후속 detail 라우트 신설 시 활성) |
| `Button101~104.OnClick` | 미노출 (§6) |

## 9. 변형 차이 (`Sobo17` 본 vs `Sobo17_1`)

`Subu17_1/Sobo17_1.tree.json` 인벤토리: **Sobo17 과 위젯 트리가 1:1 동일** — 동일 위젯명 (CornerButton2/3/4, Panel001/DBGrid101/StBar101, Panel002/Edit101~124 등 동일). 차이는 form.json 의 텍스트·캡션·SQL 바인딩 정도. 모던에서는 두 변형이 같은 라우트(`/master/publisher`)를 공유하므로 추가 부착 대상 없음.

## 10. 회귀 가드 체크리스트

- [ ] `master/publisher/page.tsx` 동작 변화 0
- [ ] tsc/eslint 0 신규
- [ ] `test/test_pagination_contracts.py::C9MastersListPageContract::test_publisher` PASS
- [ ] `test/test_masters_q_search.py` PASS

## 11. 참조

- DEC-019, DEC-023, DEC-028
- HA-RET-01
- 화면 카드: `analysis/screen_cards/Sobo17.md`
- 계약: `master_data.yaml` v1.1.0
- 선례: `Sobo27.md`, `Sobo21.md`
