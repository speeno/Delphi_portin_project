# 레이아웃 매핑: Sobo13 (저자관리·G3 저자 마스터) → 모던 `/masters/authors` (Phase F 신설)

account-menu-fxx-rbac **Phase F-1** — 누락 3화면 정본화. `Subu13/Sobo13.*` 단일 원천 (출판/총판 빌드).

## 0. 입력 산출물 (dfm-layout-input 룰)

- 정본 DFM: [`WeLove_FTP/도서유통-출판/Subu13.dfm`](../../WeLove_FTP/도서유통-출판/Subu13.dfm) + `Subu13.pas` (`TSobo13`).
- accelerator 산출물: [`tools/.../legacy_source_root/Subu13/Sobo13.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu13/Sobo13.html), `.form.json`, `.tree.json`, `.meta.json`(`title=저자관리`), `.pas_analysis.json`.
- 마스터 테이블: **`G3_Gjeo`**(저자 본) + **`G3_Gbun`**(저자 구분/서브). DataSource1=`T1_Sub31`(본), DataSource2=`T1_Sub32`(구분).
- 게이트: `Menu103Click` → `Seek_Uses('F13')` ([`도서유통-출판/Chul.pas`](../../WeLove_FTP/도서유통-출판/Chul.pas) L1909~). 모던 라우트 `/master/author` (form-registry `Sobo13`, 기존 마스터 화면 컨벤션), API `/api/v1/masters/authors` ([`menu_route_crud_map.yaml`](../../migration/contracts/menu_route_crud_map.yaml) `ACC-MENU-MASTERS-06`).
- 빌드 변형: WH 스냅샷의 `Sobo13`=**지역분류(시내+지방)**(G1_Ggeo 참조, 다른 화면)와 혼동 금지. 본 정본은 **출판/총판 저자(G3_Gjeo)**. → `master_data.yaml customer_variants[Sobo13]`.

> ⚠️ WH 빌드 `legacy_delphi_source/legacy_source/Subu13`(`Sobo13`=지역분류) + `Menu103`=`Seek_Uses('F17')` 은 비정본. 본 매핑은 **출판/총판 저자관리 F13** 전용.

## 1. 의미 분기 — 마스터+서브 그리드 + 등록 폼 (Sobo12/Sobo17 동일 패턴)

레거시 Sobo13 = **DBGrid101(저자 목록, G3_Gjeo) + DBGrid201(서브: 저자 구분, G3_Gbun) + Panel002 본 등록·수정 폼 + Panel004 구분 폼 + Panel007 진행률바**. 모던 Phase F: 목록(READ) 우선 + caps 게이트 (`useScreenCaps`/`<WriteGate>`/`<PrintGate>`). 전 위젯 1:1 매핑 기록.

## 2. dfm 영역 인벤토리 (TabOrder)

| 영역 | dfm | TabOrder | 내용 |
| --- | --- | :-: | --- |
| 상단-좌 목록 | `Panel001` | 0 | `DBGrid101` (저자 목록) |
| 상단-우 등록폼 | `Panel002` | 1 | 본 등록·수정 (Edit101~121, Button101~105) |
| 하단-좌 서브목록 | `Panel003` | 2 | `DBGrid201` (저자 구분) |
| 하단-우 서브폼 | `Panel004` | 3 | 구분 등록·수정 (Edit201/202, Button201~203) |
| 상태바 | `Panel007` | 4 | `ProgressBar0/1` + 레코드/검색진행 |
| 검색 | `Button000` | 5 | 저자 검색 |

## 3. 상단 그리드 `DBGrid101` (저자 목록) — 컬럼 매핑

정렬 기본 `Gcode`. 합계 행 없음. **저자명 컬럼 FieldName = `GPOSA`** (Gname 아님 — 레거시 G3_Gjeo 스키마).

| dfm 컬럼 | FieldName | Title.Caption | 정렬 | Width | `data-legacy-id` |
| --- | --- | --- | :-: | :-: | --- |
| col0 | `GCODE` | 코드 | center | 40 | `Sobo13.DBGrid101.GCODE` |
| col1 | `GPOSA` | 저 자 명 | center | 174 | `Sobo13.DBGrid101.GPOSA` |
| col2 | `SCODE` | ^ (런타임 `Sname`=저자구분명) | center | 16 | `Sobo13.DBGrid101.SCODE` |

모던 목록 확장 컬럼(레거시 그리드 보강 필드 대응 — `Subu13.pas` L977~988):

| 모던 컬럼 | G3_Gjeo / 조인 | `data-legacy-id` |
| --- | --- | --- |
| 직장명 | `Gname` | `Sobo13.DBGrid101.GNAME` |
| 전화 | `Gtel1`+`Gtel2` 합성 (`Gtels`) | `Sobo13.DBGrid101.GTELS` |
| 등록일자 | `Date1` | `Sobo13.DBGrid101.DATE1` |
| 직책 | `Gjice` | `Sobo13.DBGrid101.GJICE` |

`gbun_name`은 `G3_Gbun` LEFT JOIN — SCODE 컬럼에 구분명 표시(코드 fallback).

wrapper `data-legacy-id="Sobo13.DBGrid101"`.

### 3.1 목록 검색 필터 (모던 신설 — minimal 세트, 2026-05)

dfm 검색은 `Button000`→`Sobo19` 모달; 모던은 목록 상단 필터 바(§7 deltas, `data-legacy-id` 미부착). 서버 WHERE·COUNT 동일 합성.

| 모던 위젯 | 파라미터 | 동작 | 컬럼 |
| --- | --- | --- | --- |
| 검색 `<Input id="q">` | `q` | LIKE | `Gcode`/`Gposa`/`Gname`(직장) |
| 저자구분 `<select id="f-gubun">` | `gubun` | `author-categories` 로드, 정확 일치 | `G3_Gjeo.Gubun` |
| 직장명 `<Input id="f-workplace">` | `workplace` | LIKE | `G3_Gjeo.Gname` |
| 초기화 `<Button>` | — | `resetFilters` | — |

세션: `useListSession` 키 `master.author` — `Snap = { q, gubun, workplace, offset, limit }`.

## 4. 서브 그리드 `DBGrid201` (저자 구분, G3_Gbun)

| dfm 컬럼 | FieldName | Title.Caption | Width | `data-legacy-id` |
| --- | --- | --- | :-: | --- |
| col0 | `GCODE` | 코드 | 40 | `Sobo13.DBGrid201.GCODE` |
| col1 | `GNAME` | 저자구분 | 191 | `Sobo13.DBGrid201.GNAME` |

## 5. 본 등록·수정 폼 `Panel002` — 입력 위젯 (TabOrder 순)

| TabOrder | dfm | 클래스 | 라벨(캡션) | MaxLen | enabled | `data-legacy-id` |
| :-: | --- | --- | --- | :-: | :-: | --- |
| 0 | `Edit101` | ComboBox | 저자구분 | — | ✓ | `Sobo13.Edit101` |
| 1 | `Edit102` | MaskEdit | 등록일자 | 10 | ✓ | `Sobo13.Edit102` |
| 2 | `Edit103` | Edit | 저자코드 | 5 | ✗(자동) | `Sobo13.Edit103` |
| 3 | `Edit104` | Edit | 저자명 | 20 | ✓ | `Sobo13.Edit104` |
| 4 | `Edit105` | Edit | 직장명 | 24 | ✓ | `Sobo13.Edit105` |
| 5 | `Edit106` | Edit | 직책명 | 20 | ✓ | `Sobo13.Edit106` |
| 6 | `Edit107` | Edit | 사업자번호 | 20 | ✓ | `Sobo13.Edit107` |
| 7 | `Edit108` | Edit | 주민등록 | 20 | ✓ | `Sobo13.Edit108` |
| 8 | `Edit109` | Edit | 출신학교 | 20 | ✓ | `Sobo13.Edit109` |
| 9 | `Edit110` | Edit | 계좌번호 | 20 | ✓ | `Sobo13.Edit110` |
| 10 | `Edit111` | Edit | 전화번호(국번) | 4 | ✓ | `Sobo13.Edit111` |
| 11 | `Edit112` | Edit | 전화번호(번호) | 9 | ✓ | `Sobo13.Edit112` |
| 12 | `Edit113` | Edit | 팩스번호(국번) | 4 | ✓ | `Sobo13.Edit113` |
| 13 | `Edit114` | Edit | 팩스번호(번호) | 9 | ✓ | `Sobo13.Edit114` |
| 14 | `Edit115` | Edit | 우편번호(집) | 7 | ✓ | `Sobo13.Edit115` |
| 15 | `Edit116` | Edit | 우편번호(직장) | 7 | ✓ | `Sobo13.Edit116` |
| 16 | `Edit117` | Edit | 집주소1 | 90 | ✓ | `Sobo13.Edit117` |
| 17 | `Edit118` | Edit | 집주소2 | 90 | ✓ | `Sobo13.Edit118` |
| 18 | `Edit119` | Edit | 직장주소1 | 90 | ✓ | `Sobo13.Edit119` |
| 19 | `Edit120` | Edit | 직장주소2 | 90 | ✓ | `Sobo13.Edit120` |
| 20 | `Edit121` | Edit | 비고 | 40 | ✓ | `Sobo13.Edit121` |

버튼: `Button101`(새화면, tab0) · `Button102`(저장, tab1) · `Button103`(삭제, tab2) · `Button104`(집주소 우편검색 glyph, tab38) · `Button105`(직장주소 우편검색 glyph, tab40). `data-legacy-id="Sobo13.Button101"` 등.

## 6. 서브 등록·수정 폼 `Panel004` (저자 구분)

| TabOrder | dfm | 라벨 | MaxLen | `data-legacy-id` |
| :-: | --- | --- | :-: | --- |
| 0 | `Edit201` | 구분코드 | 5 | `Sobo13.Edit201` |
| 1 | `Edit202` | 구분명 | 20 | `Sobo13.Edit202` |

버튼: `Button201`(새화면)·`Button202`(저장)·`Button203`(삭제).

## 7. 구현 상태 (2026-05-31 — 저자구분 Sobo11/Sobo14 패턴 통합)

본 폼 `Panel002`(Edit101~121) + 구분 폼 `Panel004`(Edit201/202) + CRUD(등록/수정/삭제).
**Edit101** = `MasterGbunSelect` + `authorApi.categoryList` (G3_Gbun 정본만). 구분 CRUD는 상세/신규 `AuthorCategoryCollapsible`(기본 접힘). 목록 탭의 「저자구분」 제거.

| 영역 | 모던 구현 | 비고 |
| --- | --- | --- |
| 목록 | `/master/author` (`page.tsx`) — 필터·주요 컬럼(§3.1) | `AuthorListItem` · `authorApi.list` |
| 상세 | `/master/author/[gcode]` | `AuthorDetailForm` + `AuthorCategoryCollapsible`, `gbunReloadKey` |
| 신규 | `/master/author/new` | 동일 패턴 |
| 구분 | `AuthorCategoryPanel` (G3_Gbun) | 상세/신규 접기만 · `onChanged` → 콤보 재조회 |
| 백엔드 | `get_author` G3_Gbun 이중 조인 + `gbun_orphan` | `gubun`=코드·명칭 lookup, Gubun 고아 시 경고 |

### 컬럼 매핑 (정본 Subu13.pas Button102Click)

`Gposa`=저자명 · `Gname`=직장명 · `Date1`=등록일자 · `Gjice`=직책명 · `Gnumb`=사업자번호 ·
`Gnum1`=주민등록 · `Gscho`=출신학교 · `Gnum2`=계좌번호 · `Gtel1/Gtel2`=전화 · `Gfax1/Gfax2`=팩스 ·
`Gpost/Opost`=우편(집/직장) · `Gadd1/Gadd2`=집주소 · `Oadd1/Oadd2`=직장주소 · `Gbigo`=비고 ·
`Gubun`=저자구분(코드 또는 레거시 명칭 저장) — 상세 `Gcode`+`Gname` 이중 조인→`gbun_name`/`gubun` 해석, 미매칭 시 `gbun_orphan`.

### deltas (모던 신설)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` | `Gcode`/`Gposa` LIKE — 모던 신설(Button000 대체) |
| `<DataGridPager>` | 서버 사이드 페이징 (DEC-024) |
| `<WriteGate>`/`<ReadOnlyBanner>` | Phase D caps 게이트 (F13 O/R/X) |
| `FormClose`(목록 복귀 버튼) | 분리 라우트 네비게이션(레거시 단일 폼 대체) |

## 8. 이벤트 매핑

| dfm 이벤트 | 레거시 동작 | 모던 핸들러 |
| --- | --- | --- |
| `FormActivate`/`FormPaint` | 그리드 리로드 | 페이지 mount fetch |
| `Button000Click` (검색) | `SELECT … FROM G3_Gjeo WHERE Hcode … ORDER BY Gcode` | `GET /api/v1/masters/authors` |
| `Button102Click` (저장) | `INSERT/UPDATE G3_Gjeo` (`G3_GJEO_ID_GEN`) | `POST/PATCH` (caps `canWrite`) |
| `Button103Click` (삭제) | `DELETE FROM G3_Gjeo WHERE Gcode … AND Hcode …` | `DELETE` (caps `canWrite`, DEC-019 확인) |
| `Button202Click` (구분 저장) | `INSERT/UPDATE G3_Gbun` (`G3_GBUN_ID_GEN`) | 구분 `POST/PATCH` |
| `DBGrid101DblClick`/`OnKeyDown` | 행 선택→폼 로드 | onRowClick → 상세 |
| `Edit101Change` (공유 OnChange) | 더티 플래그 | form onChange |

> **O/R/X 게이팅 근거**: `Menu103Click` 의 `'O'`→`Panel002/Panel004.Enabled:=True`+그리드 KeyDown 연결, `'R'`→`Enabled:=False`/이벤트 `nil`(조회·인쇄만), `'X'`→메뉴 미진입. 모던 caps 정합.

## 9. 변형 차이 (build variant)

- **빌드 변형 분기 금지** — 차이는 `master_data.yaml customer_variants[Sobo13]` 에만.
- WH 빌드 `Sobo13`=지역분류(G1_Ggeo, `Menu103`=F17) ↔ 출판/총판 `Sobo13`=저자(G3_Gjeo, `Menu103`=F13). **동일 폼번호·상이 화면**. 모던은 출판/총판 저자 정본만 구현.
- `Subu13_1`(유통 빌드) 존재하나 본 저자 정본과 별개(지역분류 변형) — customer_variants 에 사실만 기록.

## 10. 회귀 가드 체크리스트 (Phase F)

- [x] dfm 위젯 ID 누락 0 — 부착 `data-legacy-id` ↔ 매핑노트 추적성 자동검사 ([`test/test_master_missing_screens_frontend.py`](../../test/test_master_missing_screens_frontend.py)). 본 폼 Panel002 전체 + 구분 CRUD 복원 완료.
- [x] 어댑터 단위 테스트 ([`test/test_g3_gjeo_adapt.py`](../../test/test_g3_gjeo_adapt.py)) + API contract ([`test/test_master_crud_api_contract.py`](../../test/test_master_crud_api_contract.py), [`test/test_master_missing_screens_crud_api_contract.py`](../../test/test_master_missing_screens_crud_api_contract.py)).
- [x] 저자구분 이중 조인·UI 통합 ([`test/test_author_gbun_resolve.py`](../../test/test_author_gbun_resolve.py), [`test/test_sobo13_widget_traceability.py`](../../test/test_sobo13_widget_traceability.py)).
- [x] 목록 검색 필터·컬럼 확장 ([`test/test_author_list_filters.py`](../../test/test_author_list_filters.py)).
- [x] `GET /api/v1/masters/authors`(+`author-categories`) 4서버 스모크 매트릭스 등록 (`masters.authors`/`masters.author_categories`).
- [x] 4서버 "김" 라이브 검증 — [`debug/probe_author_kim_search.py`](../../debug/probe_author_kim_search.py) → [`analysis/audit/sobo13-author-kim-fidelity.md`](../audit/sobo13-author-kim-fidelity.md). remote_138/153 PASS(정렬·표시명·상세 일관), remote_154/155 는 서버측 1129 host-block(코드 무관, flush-hosts 후 재확인).
- [x] `phase1-component-fidelity.md` 갱신 · GAP-P0=0 (DEC-053, 행 39).
- [x] tsc/eslint 0 신규.

## 11. 참조

- DEC-019/023/028/053 · `OQ-LICENSE-KEY-MAP` (F13 정본, 웹 임시값 F19 정정).
- 단일 매핑 정본: [`analysis/audit/account-menu-fxx-mapping.md`](../audit/account-menu-fxx-mapping.md) §2.1/§3.
- 선례 패턴: `Sobo16.md`(특별관리 승격), `Sobo17.md`(master+sub), `Sobo12.md`(입고처).
- 계약: `rbac_menu_matrix.yaml ACC-MENU-MASTERS-06`, `menu_route_crud_map.yaml`, `master_data.yaml customer_variants[Sobo13]`.
