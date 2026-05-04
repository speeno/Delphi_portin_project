# 레이아웃 매핑: Sobo38 (도서코드 마스터) → 모던 `/master/book-code` (READ only)

DEC-028 — `Subu38_1/Sobo38_1.*` + `Subu38_2/Sobo38_2.*` 변형 산출물을 단일 원천으로 사용. 11 섹션 구조.

> **[중요]** `Subu38/Sobo38.html` 본 폼은 **빈 셸**(위젯 0개, root 노드만). C9 도서코드 READ 그리드의 실제 위젯 정보는 변형 폴더 `Subu38_1` (`T3_Sub82` 14컬럼) / `Subu38_2` (`T3_Sub81` 10컬럼 + `T3_Sub82` 3컬럼) 에 들어있다. C3 `/inbound/import` 전용 노트는 [`Sobo38_inbound.md`](Sobo38_inbound.md) 참조.

## 0. 입력 산출물

- DFM HTML/JSON (본 폼, 빈 셸): [`tools/.../legacy_source_root/Subu38/Sobo38.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu38/Sobo38.html)
- DFM HTML/JSON (변형 1, T3_Sub82 14컬럼): [`tools/.../legacy_source_root/Subu38_1/Sobo38_1.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu38_1/Sobo38_1.html), `.form.json`, `.tree.json`
- DFM HTML/JSON (변형 2, T3_Sub81 10컬럼 + T3_Sub82 3컬럼): [`tools/.../legacy_source_root/Subu38_2/Sobo38_2.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu38_2/Sobo38_2.html), `.form.json`, `.tree.json`
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu38.dfm`](../../legacy_delphi_source/legacy_source/Subu38.dfm)
- 화면 카드: [`analysis/screen_cards/Sobo38.md`](../screen_cards/Sobo38.md)
- 모던 라우트: [`도서물류관리프로그램/frontend/src/app/(app)/master/book-code/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/master/book-code/page.tsx)
- 계약: `migration/contracts/master_data.yaml` (`/api/v1/masters/book-code`)

## 1. 의미 분기 — 본 폼은 빈 셸, 위젯은 변형에서 가져옴 / 모던은 SELECT 2건만

레거시 Sobo38 본 폼은 dfm 정적 위젯이 0개(런타임 동적 생성 추정 — Sobo38_inbound.md §0 참조). 도서코드 마스터의 실제 그리드·입력 위젯은 변형 폴더(`Sobo38_1` 등록형 / `Sobo38_2` 검색·등록 통합형)에 정의되어 있다. 모던 1차는 **G4_Book.{Gcode, Gname, Gjeja} 3컬럼 READ 그리드**만 노출 (DEC-019 보수적 적용 — 등록·수정·삭제 미구현).

## 2. dfm 영역 인벤토리 (`Subu38_1` + `Subu38_2` tree.json 기준)

### Subu38_1/Sobo38_1 (등록형)

- Sobo38_1
  - 코너: `CornerButton1/2/9`
  - 라벨: `Label301/302/309`
  - **Panel001** (입력 폼)
    - `dxButton1` (조회), `Panel101`, `Edit101`, `DateEdit1`
  - **Panel002** → `DBGrid101`
  - **Panel007** (진행률)
  - DataSource1/2
  - **T3_Sub82 (DataSet, 14 컬럼)**: `T3_Sub82ID, GCODE, GDATE, GNAME, NAME1, GQUT5~9, GSQUT, GSSUM, MEMO1, MEMO2`

### Subu38_2/Sobo38_2 (검색·등록 통합형)

- Sobo38_2
  - 코너·라벨 동일
  - **Panel001** (입력 폼)
    - `Label101, Button101, Panel101, Edit101, Edit102, Panel104, Edit107, Edit108, Button201, DateEdit1, DateEdit2, Button700, dxButton1`
  - **Panel002** → `DBGrid101`
  - DataSource1/2
  - **T3_Sub81 (DataSet, 10컬럼)**: `T3_Sub81ID, HCODE, GDATE, GCODE, GNAME, GUBUN, GSQUT, GDANG, GSSUM, GBIGO`
  - **T3_Sub82 (DataSet, 3컬럼)**: `T3_Sub82GCODE, GNAME, GUBUN`

## 3. 상단 그리드 패널 위젯 매핑 (1차 모던에 노출되는 부분만)

목록 페이지 = `master/book-code/page.tsx`. dfm 의 14·10·3 컬럼 중 **G4_Book 단순 조회**에 의미 매핑되는 3컬럼만 부착.

| dfm 위젯 (변형 기준) | 의미 | 모던 위치 | `data-legacy-id` |
| --- | --- | --- | --- |
| `Sobo38.DBGrid101` | wrapper (변형 공통) | `<DataGrid>` `<table>` | `Sobo38.DBGrid101` |
| `Sobo38_2.T3_Sub82GCODE` | 도서 코드 | `<th>` (key=gcode) | `Sobo38.DBGrid101.GCODE` |
| `Sobo38_2.T3_Sub82GNAME` | 도서 제목 | `<th>` (key=gname) | `Sobo38.DBGrid101.GNAME` |
| `Sobo38_1.T3_Sub82NAME1` | 저자 (G4_Book.Gjeja 매핑) | `<th>` (key=gjeja) | `Sobo38.DBGrid101.GJEJA` |

> 다른 컬럼(GDATE/GUBUN/GSQUT/GSSUM 등)은 phase1 모던 read scope 가 아님 — §6 참조.

## 4. 입력·액션 패널 (1차 미노출)

| dfm 위젯 (변형 기준) | 의미 | 모던 처리 |
| --- | --- | --- |
| `Sobo38_1.Edit101`, `Sobo38_2.Edit101/102/107/108` | 검색·등록 입력 시리즈 | 모던 단일 검색 박스로 흡수 (§7) |
| `dxButton1`, `Button101/201/700` | 조회·등록·삭제 버튼 | 1차 미노출 (DEC-019 — READ only) |
| `DateEdit1/2` | 일자 범위 | 1차 미노출 |

## 5. 메모/기타

해당 없음.

## 6. out-of-scope 위젯 (1차 미부착)

- `CornerButton1/2/9`, 정적 라벨
- 변형의 모든 입력·등록·삭제 위젯(§4)
- T3_Sub82 의 GDATE/GQUT5~9/GSQUT/GSSUM/MEMO1/MEMO2 (등록형만 사용)
- T3_Sub81 의 HCODE/GDATE/GUBUN/GSQUT/GDANG/GSSUM/GBIGO
- `Panel007/ProgressBar0/1` (진행률, 모던 미구현)
- 본 폼 `Subu38/Sobo38` (빈 셸 — Sobo38_inbound.md 별도 처리)

## 7. deltas (모던 신설)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` (코드/제목 LIKE) | 단일 검색박스 — dfm 의 다중 입력 흡수 |
| 조회 버튼 | 페이징 트리거 |
| `<DataGridPager>` | 서버 페이징 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `DBGrid101.OnCellClick` | (1차 무동작 — READ only) |
| `dxButton1.OnClick` | `load()` 페이징 트리거 (모던에서 검색 박스로 흡수) |

## 9. 변형 차이 (본 vs `_1` vs `_2`)

| 변형 | 위젯 수 | 데이터셋 | 용도 |
| --- | --- | --- | --- |
| Subu38 (본) | **0개** (빈 셸) | — | 런타임 동적/별도 — Sobo38_inbound.md (FTP 우회 업로드) 에서 활용 |
| Subu38_1 | Edit101 + dxButton1 + DateEdit1 + DBGrid101 | T3_Sub82 (14 컬럼) | 도서코드 등록 + 단순 그리드 |
| Subu38_2 | Edit101/102/107/108 + Button101/201/700 + dxButton1 + DateEdit1/2 + DBGrid101 | T3_Sub81 (10) + T3_Sub82 (3) | 도서코드 검색·등록 통합 |

→ 모던 phase1 은 `Subu38_2.T3_Sub82` 의 3 컬럼만 직결. UI variant 차이는 §3 표 단일 부착으로 흡수.

## 10. 회귀 가드 체크리스트

- [ ] `master/book-code/page.tsx` 동작 변화 0
- [ ] tsc/eslint 0 신규
- [ ] `test/test_pagination_contracts.py::C9MastersListPageContract::test_book_code` PASS
- [ ] `test/test_masters_q_search.py` (book-code) PASS
- [ ] §3 외 위젯 신규 도입 시 §4/§9 보강 후 부착

## 11. 참조

- DEC-019, DEC-023, DEC-027 (FTP 우회 — Sobo38_inbound.md), DEC-028
- HA-RET-01
- 자매 노트: [`Sobo38_inbound.md`](Sobo38_inbound.md) (C3 `/inbound/import`)
- 화면 카드: `analysis/screen_cards/Sobo38.md`
- 계약: `master_data.yaml` v1.1.0
- 선례: `Sobo27.md`, `Sobo21.md`

## 12. Wave C — 레거시 버튼 → API → 테스트 ID 한 줄 표

| 레거시 버튼 (Subu38_2.pas, 본판은 빈 셸) | 의미 | 모던 API | UI 노출 (현 phase1 — R) | 테스트 ID |
| --- | --- | --- | --- | --- |
| `dxButton1.OnClick` (조회) | SELECT T3_Sub82 | `GET /api/v1/masters/book-code` | 목록 페이저 | `test_pagination_contracts::C9MastersListPageContract::test_book_code` |
| `Button101.OnClick` (등록/저장) | INSERT/UPDATE | `POST/PATCH /api/v1/masters/book-code` (Wave C 후속) | 미노출 | Wave C 후속 — `test_master_book_code_patch` |
| `Button700.OnClick` (삭제) | DELETE | DEC-019 OFF | **OFF** | (후속) |
