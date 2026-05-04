# [DEPRECATED] 레이아웃 매핑: Sobo45 (구 「물류비 마스터」 추정 매핑)

> **상태**: ⛔ DEPRECATED (2026-04-23, master_data.yaml v1.2.0 — DEC-060 채택).
> **사유**: 본 문서는 `Subu45.dfm` 의 실제 Caption 인 **'청구서관리'** 가 아닌, `G5_Ggeo.Gposa` 컬럼만 보고 추정한 「물류비 마스터」 의미를 담고 있어 폐기됨.
> **대체 매핑**: 청구서관리는 `Sobo45_billing` (folder=Subu45, route=`/settlement/billing`) 으로 정상 등록되어 있으며, `analysis/layout_mappings/Sobo45_billing.md` 가 단일 원천.
> **G5_Ggeo.Gposa 의 정상 흡수처**: 청구서관리 화면 내부의 inline lookup (레거시 `Subu45.pas:L372` `G5_Ggeo.Locate` 패턴 그대로) — 단독 마스터 화면은 레거시에 부재하므로 모던에도 신설하지 않는다 (DEC-060 옵션 B).
> **재발 방지**: 동일 추정 오류 차단을 위해 새 마스터 화면 추가 시 DFM Caption 1차 검증 의무 (DEC-060 §재발 방지). 본 문서의 이하 본문은 역사 기록으로 보존.

---

DEC-028 — `Subu45/Sobo45.*` 단일 원천. 11 섹션 구조.

## 0. 입력 산출물

- DFM HTML/JSON: [`tools/.../legacy_source_root/Subu45/Sobo45.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu45/Sobo45.html), `.form.json`, `.tree.json`, `.meta.json`
- 변형: `Subu45_1/Sobo45_1.*` (위젯 트리 동일 — §9)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu45.dfm`](../../legacy_delphi_source/legacy_source/Subu45.dfm) — Caption='청구서관리' (DEC-060 정정)
- 화면 카드: [`analysis/screen_cards/Sobo45.md`](../screen_cards/Sobo45.md)
- (DEPRECATED) 모던 라우트: 구 `/master/logistics-cost/page.tsx` — 2026-04-23 삭제됨. 정상 라우트는 `/settlement/billing` (Sobo45_billing).
- (DEPRECATED) 계약: 구 `migration/contracts/master_data.yaml` SQL-MAS-10 — v1.2.0 에서 제거. 정상 계약은 `migration/contracts/settlement_billing.yaml`.

## 1. 의미 분기 — 검색·등록 통합 윈도우 → 1차 단순 3컬럼 그리드

레거시 Sobo45 는 dfm tree 기준 **단일 Panel001** 안에 검색 입력 + 액션 버튼 + 그리드(런타임 동적 — `DBGrid101` tree 미노출, form.json 에 정의됨)가 모여있는 구조. 모던 1차는 `G5_Ggeo.Gposa` 3컬럼(코드/거래처-품목/물류비) READ 만 노출 (DEC-019 — 수정 후속).

## 2. dfm 영역 인벤토리 (tree.json 기준)

- Sobo45 (root)
  - **Panel001** (전체 폼)
    - 라벨: `Label101`
    - Panel: `Panel101, Panel105`
    - 입력: `Edit100, Edit101, Edit102, Edit103, Edit104, Edit105`
    - 일자: `DateEdit1`
    - 액션 버튼: `Button101` (조회), `Button201` (등록), `Button701` (보조1), `Button702` (보조2)

> 그리드(`DBGrid101`)는 본 tree.json 에 직접 노출되지 않음 — form.json 의 DataSource 바인딩으로 런타임 생성. 모던 매핑에는 `Sobo45.DBGrid101` 가상 ID 를 일관 사용.

## 3. 그리드 위젯 매핑

| dfm 위젯 | 의미 | 모던 위치 | `data-legacy-id` |
| --- | --- | --- | --- |
| `Sobo45.DBGrid101` (form.json) | 그리드 wrapper | `<DataGrid>` `<table>` | `Sobo45.DBGrid101` |
| `Sobo45.DBGrid101.GCODE` | 코드 | `<th>` (key=gcode) | `Sobo45.DBGrid101.GCODE` |
| `Sobo45.DBGrid101.GNAME` | 거래처/품목명 | `<th>` (key=gname) | `Sobo45.DBGrid101.GNAME` |
| `Sobo45.DBGrid101.GPOSA` | 물류비 | `<th>` (key=gposa, align=right) | `Sobo45.DBGrid101.GPOSA` |

## 4. 입력·액션 패널 (1차 미노출)

| dfm 위젯 | 의미 | 모던 처리 |
| --- | --- | --- |
| `Sobo45.Edit100~105`, `DateEdit1` | 검색·등록 입력 시리즈 | 모던 단일 `<Input id="q">` 로 흡수 (§7) |
| `Sobo45.Button101/201/701/702` | 조회·등록·보조 | 1차 미노출 (DEC-019 READ only) |

## 5. 메모/기타

해당 없음.

## 6. out-of-scope 위젯 (1차 미부착)

- 정적 라벨 `Label101`
- `Panel001/101/105` 컨테이너 자체 (래퍼 — 부착 의미 없음)
- 입력 시리즈 `Edit100~105`, `DateEdit1` (검색 박스로 흡수, 등록은 phase2)
- 버튼 `Button101/201/701/702` (등록·보조는 phase2)

## 7. deltas (모던 신설)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` (코드/거래처명 LIKE) | 단일 검색박스 — dfm 다중 입력 흡수 |
| 조회 버튼 | 페이징 트리거 |
| `<DataGridPager>` | 서버 페이징 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `Button101.OnClick` (조회) | `load()` 페이징 트리거 (검색 박스 호출) |
| `Button201/701/702.OnClick` | 미노출 (§6) |
| `DBGrid101.OnCellClick` | (1차 무동작 — READ only) |

## 9. 변형 차이 (`Sobo45` 본 vs `Sobo45_1`)

`Subu45_1/Sobo45_1.tree.json` 인벤토리는 본 폼과 **위젯 트리 1:1 동일** (Panel001 / Edit100~105 / DateEdit1 / Button101/201/701/702). 차이는 form.json 의 SQL/DataSource 바인딩으로 추정 (예: 거래처별 vs 품목별 집계). 모던 단일 라우트 `/master/logistics-cost` 가 두 변형을 흡수 — 추가 부착 대상 없음.

## 10. 회귀 가드 체크리스트

- [ ] `master/logistics-cost/page.tsx` 동작 변화 0
- [ ] tsc/eslint 0 신규
- [ ] `test/test_pagination_contracts.py::C9MastersListPageContract::test_logistics_cost` PASS
- [ ] `test/test_masters_q_search.py` (logistics-cost) PASS

## 11. 참조

- DEC-019, DEC-023, DEC-028
- HA-RET-01
- 화면 카드: `analysis/screen_cards/Sobo45.md`
- 계약: `master_data.yaml` v1.1.0
- 선례: `Sobo27.md`, `Sobo21.md`

## 12. Wave C — 레거시 버튼 → API → 테스트 ID 한 줄 표 (마스터 물류비)

> 본 노트는 **마스터 물류비** (`/master/logistics-cost`, Subu45 마스터 파생). C5 정산 청구의 `Subu45.pas` (Sobo45_billing) 와는 다른 흐름. 정산용은 `Sobo45_billing.md` 참조.

| 레거시 버튼 (Subu45.pas — 마스터 부분) | 의미 | 모던 API | UI 노출 (현 phase1 — R) | 테스트 ID |
| --- | --- | --- | --- | --- |
| `Button101.OnClick` (조회) | SELECT 물류비 마스터 | `GET /api/v1/masters/logistics-cost` | 목록 페이저 | `test_pagination_contracts::C9MastersListPageContract::test_logistics_cost` |
| `Button701.OnClick` (등록/저장) | INSERT/UPDATE | `POST/PATCH /api/v1/masters/logistics-cost` (Wave C 후속) | 미노출 | Wave C 후속 — `test_master_logistics_cost_patch` |
| `Button702.OnClick` (삭제) | DELETE | DEC-019 OFF | **OFF** | (후속) |
