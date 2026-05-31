# 레이아웃 매핑: Sobo14 (도서 마스터) → 모던 `/master/book` (목록 + 상세)

DEC-028 — `Subu14/Sobo14.*` 단일 원천. C2(Sobo27.md) / C6(Sobo21.md) 11 섹션 구조 그대로 재사용.

## 0. 입력 산출물 (참고용)

- DFM HTML/JSON: [`tools/.../legacy_source_root/Subu14/Sobo14.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu14/Sobo14.html), `Sobo14.form.json`, `Sobo14.tree.json`, `Sobo14.meta.json`
- 변형 폴더: `Subu14_1/Sobo14_1.*` (도서 lookup picker — §9)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu14.dfm`](../../legacy_delphi_source/legacy_source/Subu14.dfm)
- 화면 카드: [`analysis/screen_cards/Sobo14.md`](../screen_cards/Sobo14.md), [`analysis/screen_cards/Sobo14_1.md`](../screen_cards/Sobo14_1.md)
- 모던 라우트:
  - 목록: [`도서물류관리프로그램/frontend/src/app/(app)/master/book/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/master/book/page.tsx)
  - 상세/수정: [`도서물류관리프로그램/frontend/src/app/(app)/master/book/[gcode]/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/master/book/[gcode]/page.tsx)
  - 신규: `도서물류관리프로그램/frontend/src/app/(app)/master/book/new/page.tsx`
- 계약: `migration/contracts/master_data.yaml` (`/api/v1/masters/book*`, `/api/v1/masters/book-categories*`)

> **구현 상태(2026-05): 본 폼 전체 복원 완료.** 기존 7필드(제목/저자/ISBN/단가/출판사/구분/분류명)
> → Panel002 전체(도서분류·도서처리·도서구분·비율구분·코드·도서명·저자·ISBN·등록번호·서가위치·
> 판형·단위·묶음·발행/등록일·정지사유·비고·원가·매입가·단가·쪽수/판수·덩이/그램·비율 7종·재고 5종(RO)·
> 체크박스 4종)로 확장. Edit101 `MasterGbunSelect`(G4_Gbun only) + 분류 CRUD를 상세/신규에 접기 통합(목록 탭 제거, 2026-05).
> 카테고리 조인 `Gubun=Gcode`+`Gubun=Gname` 이중 lookup·고아 Sname 경고. NL-ISBN·`matchGname`·DEC-019 보존.

## 1. 의미 분기 — Sobo11 과 동일 패턴 (목록·상세 동시 윈도우 → 라우트 2개)

레거시 Sobo14 도 Sobo11 과 동일하게 **상단 그리드 + 하단 등록·수정 폼** 단일 윈도우. 모던에서는 `/master/book` (목록) + `/master/book/[gcode]` (상세) 로 분리.

| 영역 | 모던 라우트 |
| --- | --- |
| Panel001 / DBGrid101 | `/master/book` |
| Panel002 (Edit101~ + Button) | `/master/book/[gcode]` · `/master/book/new` |
| Panel200 (DBGrid201 + 분류 등록폼) | 상세/신규 `MasterCategoryCollapsible` + `BookCategoryPanel` |

## 2. dfm 영역 인벤토리 (tree.json 기준)

- Sobo14 (root)
  - 코너: `CornerButton2/3/4`
  - 라벨: `Label002/003/309/100~110/300/301`
  - **Panel001** → `DBGrid101` (Gcode/Gname/Gjeja/Gisbn/Gdang/Gpost 등)
  - **Panel002** (등록·수정 폼)
    - Panel100 액션: `Button101` (등록), `Button102` (수정), `Button103` (삭제)
    - Panel101~119 (필드 컨테이너)
    - `Edit101~` (입력 시리즈 — 제목/저자/ISBN/단가/출판사/구분 등)

## 3. 상단 그리드 패널 위젯 매핑

목록 페이지 = `master/book/page.tsx`.

| dfm 위젯 | 의미 | 모던 위치 | `data-legacy-id` |
| --- | --- | --- | --- |
| `Sobo14.DBGrid101` | 도서 그리드 wrapper | `<DataGrid>` `<table>` | `Sobo14.DBGrid101` |
| `Sobo14.DBGrid101.GCODE` | 도서코드 | `<th>` (key=gcode) | `Sobo14.DBGrid101.GCODE` |
| `Sobo14.DBGrid101.GNAME` | 제목 | `<th>` (key=gname) | `Sobo14.DBGrid101.GNAME` |
| `Sobo14.DBGrid101.GJEJA` | 저자 | `<th>` (key=gjeja) | `Sobo14.DBGrid101.GJEJA` |
| `Sobo14.DBGrid101.GISBN` | ISBN | `<th>` (key=gisbn) | `Sobo14.DBGrid101.GISBN` |
| `Sobo14.DBGrid101.GDANG` | 단가 | `<th>` (key=gdang, align=right) | `Sobo14.DBGrid101.GDANG` |
| `Sobo14.DBGrid101.GPOST` | 출판사 코드 | `<th>` (key=gpost) | `Sobo14.DBGrid101.GPOST` |

### 3.1 목록 검색 필터 (모던 신설 — minimal 세트, 2026-05)

dfm 의 검색용 `Edit*` 1:1 대응 위젯이 없어 모던 신설(§7 deltas, `data-legacy-id` 미부착). 서버측 WHERE 확장으로 페이지·total 정합 유지.

| 모던 위젯 | 파라미터 | 동작 | 컬럼 |
| --- | --- | --- | --- |
| 검색 `<Input id="q">` | `q` | 기존 LIKE(양끝 와일드카드) | `Gcode`/`Gname`/`Gisbn` |
| 도서분류 `<select id="f-gubun">` | `gubun` | 단일 선택 — `bookCategoryList`(G4_Gbun)로 로드, 코드 정확 일치 | `G4_Book.Gubun = 선택 Gcode` |
| 도서처리 `<Input id="f-jubun">` | `jubun` | 부분 일치 LIKE(`_likify`) | `G4_Book.Jubun` |
| 출고정지 제외 `<input id="f-exship" type=checkbox>` | `excludeShippingStop` | 토글(기본 OFF) | `IFNULL(Grat9,'') NOT IN ('1','True','true')` |
| 초기화 `<Button>` | — | 필터 모두 비우고 재조회(`resetFilters`) | — |

세션 보존: `useListSession<Snap>` 키 `master.book` — `Snap = { q, gubun, jubun, excludeShippingStop, offset, limit }`(누락 필드 기본값 채움 → 하위호환).

## 4. 상세/등록 패널 위젯 매핑 (Panel002 — 본 폼 전체)

상세 페이지 = `master/book/[gcode]/page.tsx`, 신규 = `master/book/new/page.tsx`,
폼 컴포넌트 = `components/master/book-detail-form.tsx`.

정본: **WeLove_FTP 위러브(chul_09) 빌드 `Subu14.pas`/`Subu14.dfm`** — 화면 최다 필드 빌드.
라벨↔컬럼은 dfm 좌표(Left/Top)로 1:1 확정. `FieldByName` = 컬럼, dfm Caption = 라벨.

| dfm 위젯 | 라벨 | G4_Book 컬럼 | API 키 | 비고 |
| --- | --- | --- | --- | --- |
| `Sobo14.Panel002` | 본 폼 wrapper | — | — | — |
| `Sobo14.Edit101` | 도서분류 | Gubun/Sname | gbun_name/gubun | `MasterGbunSelect`(G4_Gbun only, `data-legacy-id`=`Sobo14.Edit101`) |
| `Sobo14.Edit102` | 도서처리 | Jubun | jubun | |
| `Sobo14.Edit107` | 도서구분 | Scode | scode | |
| `Sobo14.Edit133` | 비율구분 | Pubun | pubun | |
| `Sobo14.Edit103` | 도서코드 | Gcode | gcode | PK, 신규만 입력 |
| `Sobo14.Edit104` | 도서코드2 | Ocode | ocode | |
| `Sobo14.Edit105` | 도서명 | Gname | gname | 필수 |
| `Sobo14.Edit106` | 저자명 | Gjeja | gjeja | |
| `Sobo14.Edit110` | ISBN번호 | Gisbn | gisbn | NL 조회 버튼 인접 |
| `Sobo14.Edit120` | 등록번호 | Gnumb | gnumb | |
| `Sobo14.Edit134` | 서가위치 | Gpost | gpost | |
| `Sobo14.Edit129` | 판형 | Name2 | name2 | |
| `Sobo14.Edit108` | 단위 | Gdabi | gdabi | |
| `Sobo14.Edit111` | 묶음 | Gbjil | gbjil | |
| `Sobo14.Edit121` | 발행일 | Date1 | date1 | |
| `Sobo14.Edit122` | 등록일 | Date2 | date2 | |
| `Sobo14.Edit123` | 정지사유 | Name1 | name1 | |
| `Sobo14.Edit119` | 비고 | Gbigo | gbigo | |
| `Sobo14.Edit130` | 원가 | Price | price | |
| `Sobo14.Edit131` | 매입가 | Odang | odang | |
| `Sobo14.Edit109` | 단가 | Gdang | gdang | |
| `Sobo14.Edit124` | 쪽수 | Gpage | gpage | |
| `Sobo14.Edit125` | 판수 | Gpan1 | gpan1 | |
| `Sobo14.Edit126` | 덩이 | Gqut1 | gqut1 | |
| `Sobo14.Edit127` | 그램 | Gqut2 | gqut2 | |
| `Sobo14.Edit113~117` | 비율 위탁/현매/매절/납품/특별 | Grat1~Grat5 | grat1~grat5 | |
| `Sobo14.Edit132` | 비율 한도 | Grat7 | grat7 | |
| `Sobo14.Edit118` | 비율 기타 | Grat6 | grat6 | |
| `Sobo14.Edit112` | 재고 | Gsqut | gsqut | **읽기전용**(시스템 산정) |
| `Sobo14.Edit301~302` | 본사재고 정품/비품 | Jego1/Jego2 | jego1/jego2 | **읽기전용** |
| `Sobo14.Edit303~304` | 창고재고 정품/비품 | Jego3/Jego4 | jego3/jego4 | **읽기전용** |
| `Sobo14.CheckBox1` | 세액유무 | Bigo1 | bigo1 | '1'/'' 토글 |
| `Sobo14.CheckBox3` | 재고절판 | Bigo2 | bigo2 | '1'/'' 토글 |
| `Sobo14.CheckBox4` | 전자책 | Bigo3 | bigo3 | '1'/'' 토글 |
| `Sobo14.CheckBox2` | 출고정지 | Grat9 | grat9 | '1'/'' 토글 |
| `Sobo14.Button101` | 등록(새화면) | — | `master/book/new` | DEC-019(신규 폼) |
| `Sobo14.Button102` | 수정/저장 | — | `PATCH .../book/{gcode}` | |
| `Sobo14.Button103` | 삭제 | — | — | **UI 미노출**(DEC-019) |
| `Sobo14.FormClose` | 목록 복귀 | — | — | |

### 4-1. 도서분류 G4_Gbun (상세/신규 접기 통합)

`components/master/book-category-panel.tsx` — 상세/신규 `MasterCategoryCollapsible`(기본 접힘). CRUD 후 `reloadKey`로 Edit101 콤보 재조회.

| dfm 위젯 | 라벨 | G4_Gbun 컬럼 | API | `data-legacy-id` |
| --- | --- | --- | --- | --- |
| `Sobo14.Edit201` | 분류코드 | Gcode | gcode | `Sobo14.Edit201` |
| `Sobo14.Edit202` | 분류명 | Gname | gname | `Sobo14.Edit202` |
| `Sobo14.Button201/202/203` | 등록/저장/삭제 | — | `POST/PATCH/DELETE /api/v1/masters/book-categories` | 동일 ID |
| `Sobo14.DBGrid201` | 분류 그리드 | — | `GET /api/v1/masters/book-categories` | `Sobo14.DBGrid201` |

## 5. 멀티 DB 호환 (multi-db-compat)

`app/services/g4_book_adapt.py` 가 `SHOW COLUMNS FROM G4_Book/G4_Gbun` 로 존재 컬럼만
SELECT(누락 텍스트 `''`, 누락 숫자 `0` fallback)·PATCH 대상에 포함한다. 빌드별 컬럼 차이
(총판: Grat7/Price/Jego/Bigo 없음, New: Grat8 등)는 어댑터가 흡수 — 서비스 분기 0.
회귀 가드: `test/test_g4_book_adapt.py`.

## 6. out-of-scope 위젯 (미부착)

- `CornerButton2/3/4`, 정적 라벨 전체
- `Sobo14.Button103`(Delete) — DEC-019 (UI 미노출, 백엔드 라우트는 유지)
- 검색 lookup 보조 폼(`Sobo14_1`) — §9

## 7. deltas (모던 신설)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` (코드/제목/ISBN LIKE) | 단일 검색박스 — dfm 의 lookup 헬퍼 패턴과 다름, 신설 |
| 필터 바 `구분 select·처리 input·출고정지 제외 체크` (§3.1) | 검색 편의 minimal 세트 — 서버 WHERE 확장, 미부착 |
| 조회/초기화 버튼 | 페이징 트리거 / 필터 리셋 (모던 신설) |
| `<DataGridPager>` | 서버 사이드 페이징 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `DBGrid101.OnDblClick` | `onRowClick={r => router.push("/master/book/{gcode}")}` |
| `Button102.OnClick` (수정) | `save()` → `masterApi.bookUpdate(gcode, body)` |
| `FormClose` | `router.push("/master/book")` |

## 9. 변형 차이 (`Sobo14` 본 vs `Sobo14_1`)

`Subu14_1/Sobo14_1.tree.json` 인벤토리:

```
Sobo14_1
  CornerButton1/2/9
  Label301/302/309
  Panel001
    Label100, Panel101, Edit201
```

→ Sobo14_1 은 **위젯이 사실상 Edit201 1개**인 lookup picker 미니 폼이다(도서 코드 입력 + 즉시 lookup 후 모폼 닫기). 모던에서는 별도 라우트로 노출하지 않고 자동완성/검색 박스 안에 흡수 (`master/book/page.tsx` 의 `<Input id="q">`). UI variant 0건(기능 차이만 — `data-legacy-id` 추가 부착 대상 없음).

## 10. 회귀 가드 체크리스트

- [x] `master/book/page.tsx`(목록) / `[gcode]`(상세+분류 접기) / `new`(신규) — tsc/eslint 경고 0 신규
- [x] `test/test_book_gbun_resolve.py` · `test/test_sobo14_widget_traceability.py`
- [x] `test/test_g4_book_adapt.py` PASS (어댑터 fallback·patch 제외)
- [x] `test/test_master_crud_api_contract.py` PASS (book-categories 라우트·클라이언트 노출)
- [ ] `test/test_pagination_contracts.py::C9MastersListPageContract::test_book` PASS
- [ ] `test/test_masters_q_search.py` PASS
- [ ] (옵션) 4대 서버 live 스모크 — `debug/probe_backend_all_servers.py` (`masters.book_categories`)

## 11. 참조

- DEC-019, DEC-023, DEC-028, DEC-016/017/018
- HA-RET-01
- 화면 카드: `analysis/screen_cards/Sobo14.md`, `Sobo14_1.md`
- 계약: `migration/contracts/master_data.yaml` v1.1.0
- 테스트: 위 §10
- 선례: `Sobo27.md` (C2), `Sobo21.md` (C6)

## 12. Wave C — 레거시 버튼 → API → 테스트 ID 한 줄 표

| 레거시 버튼 (Subu14.pas) | 의미 | 모던 API (master_data.yaml) | UI 노출 (현 phase1) | 테스트 ID |
| --- | --- | --- | --- | --- |
| `Button101.OnClick` (등록/저장) | INSERT/UPDATE T1_Sub11 (도서) | `POST /api/v1/masters/book` · `PATCH .../{bcode}` | 상세 라우트 폼 액션 | `test_pagination_contracts::C9MastersListPageContract::test_book` |
| `Button102.OnClick` (수정/취소) | 폼 모드 토글 | (UI 전용) | 상세 라우트 헤더 | — |
| `Button103.OnClick` (삭제) | DELETE | (DEC-019 — UI 미노출) | **OFF** | Wave C 후속 `test_master_book_delete_blocked` |
| `Button104.OnClick` (검색) | 키워드 fetch | `GET /api/v1/masters/book?q=…` | 목록 검색 | `test_masters_q_search::test_book` |
