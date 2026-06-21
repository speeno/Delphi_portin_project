# 레이아웃 매핑: Sobo12 (입고처관리·G2 입고처 마스터) → 모던 `/masters/inbound-vendors` (Phase F 신설)

account-menu-fxx-rbac **Phase F-1** — 누락 3화면 정본화. `Subu12/Sobo12.*` 단일 원천 (출판/총판 빌드).

## 0. 입력 산출물 (dfm-layout-input 룰)

- 정본 DFM: [`WeLove_FTP/도서유통-출판/Subu12.dfm`](../../WeLove_FTP/도서유통-출판/Subu12.dfm) + `Subu12.pas` (`TSobo12`).
- accelerator 산출물: [`tools/.../legacy_source_root/Subu12/Sobo12.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu12/Sobo12.html), `.form.json`, `.tree.json`, `.meta.json`(`title=입고처관리`), `.pas_analysis.json`.
- 마스터 테이블: **`G2_Ggwo`**(입고처 본) + **`G2_Gbun`**(입고처 구분/서브). DataSource1=`T1_Sub21`(본), DataSource2=`T1_Sub22`(구분).
- 게이트: `Menu102Click` → `Seek_Uses('F12')` ([`도서유통-출판/Chul.pas`](../../WeLove_FTP/도서유통-출판/Chul.pas) L1872~). 모던 라우트 `/master/inbound-vendor` (form-registry `Sobo12`, 기존 마스터 화면 컨벤션), API `/api/v1/masters/inbound-vendors` ([`menu_route_crud_map.yaml`](../../migration/contracts/menu_route_crud_map.yaml) `ACC-MENU-MASTERS-02`).
- 빌드 변형: WH 스냅샷의 `Sobo12`=도서(다른 화면)와 혼동 금지. 본 정본은 **출판/총판 입고처**. → `master_data.yaml customer_variants[Sobo12]`.

> ⚠️ WH 빌드(`legacy_delphi_source/legacy_source/Subu12`)는 `Sobo12`=도서 의미라 비정본. 본 매핑은 **출판/총판 G2_Ggwo** 입고처 전용.

## 1. 의미 분기 — 마스터+서브 그리드 + 등록 폼 (Sobo17/Sobo14 동일 패턴)

레거시 Sobo12 = **DBGrid101(입고처 목록, G2_Ggwo) + DBGrid201(서브: 입고처 구분, G2_Gbun) + Panel002 본 등록·수정 폼 + Panel004 구분 등록·수정 폼 + Panel007 진행률바**. 모던은 `useScreenCaps`/`<WriteGate>`/`<PrintGate>` (Phase D) 게이트를 유지하면서 **본 폼/구분 폼 전체 필드 CRUD** 를 복원한다. 위젯 ID 누락 0 가드를 위해 **전 위젯 1:1 매핑**을 본 노트에 기록한다.

## 2. dfm 영역 인벤토리 (tree.json 기준 · TabOrder)

| 영역 | dfm | TabOrder | 내용 |
| --- | --- | :-: | --- |
| 상단-좌 목록 | `Panel001` | 0 | `DBGrid101` (입고처 목록) |
| 상단-우 등록폼 | `Panel002` | 1 | 본 등록·수정 (Edit101~132, Button101~104, CheckBox1/2) |
| 하단-좌 서브목록 | `Panel003` | 2 | `DBGrid201` (입고처 구분) |
| 하단-우 서브폼 | `Panel004` | 3 | 구분 등록·수정 (Edit201/202, Button201~203) |
| 상태바 | `Panel007` | 4 | `ProgressBar0/1` + 레코드/검색진행 라벨 |
| 검색 | `Button000` | 5 | 입고처 검색 트리거 |
| 코너 | `CornerButton2/3/4` | — | 장식 (모던 미부착) |

## 3. 상단 그리드 `DBGrid101` (입고처 목록) — 컬럼 매핑

목록 = `/master/inbound-vendor` (목록 전용). 정렬 기본 `Gcode`. 모던 목록은 레거시 3컬럼보다 **구분·지역·연락처·주소** 를 추가 노출(거래처 Sobo11 목록 패턴).

| dfm 컬럼 | FieldName | Title.Caption | 모던 목록 컬럼 | `data-legacy-id` |
| --- | --- | --- | --- | --- |
| col0 | `GCODE` | 코드 | 코드 | `Sobo12.DBGrid101.GCODE` |
| col1 | `GNAME` | 입고처명 | 입고처명 | `Sobo12.DBGrid101.GNAME` |
| col2 | `SCODE` | ^ (펼침 토글) | 입고처구분(`gbun_name`/`gubun`) | `Sobo12.DBGrid101.SCODE` |
| — | `Jubun` | 입고처지역 | 지역 | `Sobo12.Edit102` |
| — | `Gposa` | 대표자 | 대표자 | `Sobo12.Edit106` |
| — | `Gtel1`/`Gtel2` | 전화 | 전화(합침) | `Sobo12.Edit112` |
| — | `Gpost` | 우편번호 | 우편번호 | `Sobo12.Edit111` |
| — | `Gadd1`/`Gadd2` | 주소 | 주소(`gjuso`) | `Sobo12.Edit116` |

검색 필터(모던): `q`(코드·입고처명·대표자·전화·사업자번호 LIKE), `gubun`(G2_Gbun 코드), `jubun`(지역 LIKE). API `GET /api/v1/masters/inbound-vendors?gubun=&jubun=`.

그리드 wrapper `data-legacy-id="Sobo12.DBGrid101"`.

## 4. 서브 그리드 `DBGrid201` (입고처 구분, G2_Gbun)

| dfm 컬럼 | FieldName | Title.Caption | Width | `data-legacy-id` |
| --- | --- | --- | :-: | --- |
| col0 | `GCODE` | 코드 | 40 | `Sobo12.DBGrid201.GCODE` |
| col1 | `GNAME` | 입고처구분 | 191 | `Sobo12.DBGrid201.GNAME` |

wrapper `data-legacy-id="Sobo12.DBGrid201"`.

## 5. 본 등록·수정 폼 `Panel002` — 입력 위젯 (TabOrder 순)

label 패널(`Panel101`~)은 캡션, 입력은 `Edit*`. 모던 입력에 `data-legacy-id="Sobo12.<EditName>"` 부착, 라벨은 캡션 텍스트로.

| TabOrder | dfm | 클래스 | 라벨(캡션) | MaxLen | enabled | `data-legacy-id` |
| :-: | --- | --- | --- | :-: | :-: | --- |
| 0 | `Edit101` | ComboBox | 입고처구분 | — | ✓ | `Sobo12.Edit101` |
| 1 | `Edit102` | Edit | 입고처지역 | 6 | ✓ | `Sobo12.Edit102` |
| 2 | `Edit103` | Edit | 입고처코드 | 5 | ✗(자동) | `Sobo12.Edit103` |
| 3 | `Edit104` | Edit | (지역코드 보조) | 5 | ✓ | `Sobo12.Edit104` |
| 4 | `Edit105` | Edit | 입고처명 | 50 | ✓ | `Sobo12.Edit105` |
| 5 | `Edit106` | Edit | 대표자 | 30 | ✓ | `Sobo12.Edit106` |
| 6 | `Edit107` | Edit | 사업자번호 | 12 | ✓ | `Sobo12.Edit107` |
| 7 | `Edit108` | Edit | 업태 | 30 | ✓ | `Sobo12.Edit108` |
| 8 | `Edit109` | Edit | 종목 | 30 | ✓ | `Sobo12.Edit109` |
| 9 | `Edit110` | Edit | 담당자 | 20 | ✓ | `Sobo12.Edit110` |
| 10 | `Edit132` | Edit | 핸드폰번호 | 20 | ✓ | `Sobo12.Edit132` |
| 11 | `Edit131` | Number | 한도액 | 8 | ✗ | `Sobo12.Edit131` |
| 12 | `Edit111` | Edit | 우편번호 | 7 | ✓ | `Sobo12.Edit111` |
| 13 | `Edit112` | Edit | 전화번호(국번) | 4 | ✓ | `Sobo12.Edit112` |
| 14 | `Edit113` | Edit | 전화번호(번호) | 20 | ✓ | `Sobo12.Edit113` |
| 15 | `Edit114` | Edit | 팩스번호(국번) | 4 | ✓ | `Sobo12.Edit114` |
| 16 | `Edit115` | Edit | 팩스번호(번호) | 20 | ✓ | `Sobo12.Edit115` |
| 17 | `Edit116` | Edit | 주소1 | 90 | ✓ | `Sobo12.Edit116` |
| 18 | `Edit117` | Edit | 주소2 | 90 | ✓ | `Sobo12.Edit117` |
| 19~24 | `Edit118~122`,`Edit130` | Number | 비율(위탁/현매/매절/납품/특별/한도) | 3 | ✓ | `Sobo12.Edit118`…`Sobo12.Edit122`,`Sobo12.Edit130` |
| 25 | `Edit123` | Number | 비율(기타) | 3 | ✓ | `Sobo12.Edit123` |
| 26 | `Edit124` | Number | 신간수량 | 5 | ✓ | `Sobo12.Edit124` |
| 27 | `CheckBox1` | CheckBox | 발행유무(계산서) | — | ✗ | `Sobo12.CheckBox1` |
| 28 | `Edit127` | Edit | 계산서 | 50 | ✓ | `Sobo12.Edit127` |
| 29 | `CheckBox2` | CheckBox | 정지유무(출고정지) | — | ✗ | `Sobo12.CheckBox2` |
| 30 | `Edit129` | Edit | 정지사유 | 50 | ✗ | `Sobo12.Edit129` |
| 31 | `Edit125` | Edit | 비고1 | 50 | ✓ | `Sobo12.Edit125` |
| 32 | `Edit126` | Edit | 비고2 | 50 | ✓ | `Sobo12.Edit126` |

버튼: `Button101`(새화면, tab0) · `Button102`(저장, tab1) · `Button103`(삭제, tab2, 초기 disabled) · `Button104`(우편번호 검색 glyph, tab50). `data-legacy-id="Sobo12.Button101"` 등.

## 6. 서브 등록·수정 폼 `Panel004` (입고처 구분)

| TabOrder | dfm | 라벨 | MaxLen | `data-legacy-id` |
| :-: | --- | --- | :-: | --- |
| 0 | `Edit201` | 구분코드 | 5 | `Sobo12.Edit201` |
| 1 | `Edit202` | 구분명 | 20 | `Sobo12.Edit202` |

버튼: `Button201`(새화면)·`Button202`(저장)·`Button203`(삭제). `data-legacy-id="Sobo12.Button201~203"`.

## 7. deltas (모던 신설)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` | `Gcode`/`Gname` LIKE — 모던 신설(레거시 Button000 대체) |
| `<DataGridPager>` | 서버 사이드 페이징 (DEC-024) |
| `<WriteGate>`/`<PrintGate>` | Phase D caps 게이트 (F12 O/R/X) |

## 8. 이벤트 매핑

| dfm 이벤트 | 레거시 동작 | 모던 핸들러 |
| --- | --- | --- |
| `FormActivate`/`FormPaint` | 그리드 리로드·그리기 | 페이지 mount fetch |
| `Button000Click` (검색) | `SELECT … FROM G2_Ggwo WHERE Hcode … ORDER BY Gcode` | `GET /api/v1/masters/inbound-vendors` |
| `Button102Click` (저장) | `INSERT/UPDATE G2_Ggwo` | `POST/PATCH` (caps `canWrite`) |
| `Button103Click` (삭제) | `DELETE FROM G2_Ggwo` | `DELETE` (caps `canWrite`, DEC-019 정책 확인) |
| `Button202Click` (구분 저장) | `INSERT/UPDATE G2_Gbun` | 구분 `POST/PATCH` |
| `DBGrid101DblClick`/`OnKeyDown` | 행 선택→폼 로드 | onRowClick → `/master/inbound-vendor/{gcode}` 상세 |
| `Button101` (새화면) | 신규 등록 폼 | `/master/inbound-vendor/new` |
| 입고처구분 `Panel004` | G2_Gbun CRUD | 상세/신규 `InboundVendorCategoryCollapsible` (목록 탭 없음) |
| `Edit101Change` (공유 OnChange) | 더티 플래그 | form onChange |

> **O/R/X 게이팅 근거**: `Menu102Click` 은 `nUse2='O'` 일 때 `Panel002.Enabled:=True`/`Panel004.Enabled:=True` + 그리드 KeyDown 연결, `'R'` 이면 `Enabled:=False`/이벤트 `nil`(조회·인쇄만), `'X'` 면 메뉴 미진입(`ShowMessage(E_Connect)`). → 모던 `canWrite`(O)·read-only(R)·hidden/403(X) 정합 (account-menu-fxx-mapping §1).

## 9. 변형 차이 (build variant)

- **빌드 변형 분기 금지** — 차이는 `migration/contracts/master_data.yaml customer_variants[Sobo12]` 에만 기록.
- WH 빌드 `Sobo12`=도서(상이 화면) → 본 정본(출판/총판 G2_Ggwo 입고처)과 코드 분기 없음. 모던은 출판/총판 정본만 구현.
- `Subu12_*` 별도 변형 폴더: 출판/총판 빌드에 없음(단일 폼).

## 10. 회귀 가드 체크리스트 (Phase F)

- [x] dfm 위젯 ID 누락 0 — 부착 `data-legacy-id` ↔ 매핑노트 추적성 자동검사 ([`test/test_master_missing_screens_frontend.py`](../../test/test_master_missing_screens_frontend.py) `WidgetIdTraceability`). 본/구분 폼 필드(Edit101~132, Edit201~202) CRUD 포함.
- [x] `GET /api/v1/masters/inbound-vendors` 4서버 스모크 매트릭스 등록 ([`probe_backend_all_servers.py`](../../debug/probe_backend_all_servers.py) `masters.inbound_vendors`).
- [x] `phase1-component-fidelity.md` 갱신 · GAP-P0=0 (DEC-053, 행 37).
- [x] tsc/eslint 0 신규.

## 11. 참조

- DEC-019/023/028/053 · `OQ-LICENSE-KEY-MAP` (F12 정본).
- 단일 매핑 정본: [`analysis/audit/account-menu-fxx-mapping.md`](../audit/account-menu-fxx-mapping.md) §2.1/§3.
- 선례 패턴: `Sobo17.md`(출판사 master+sub), `Sobo14.md`(도서), `Sobo11.md`(거래처).
- 계약: `rbac_menu_matrix.yaml ACC-MENU-MASTERS-02`, `menu_route_crud_map.yaml`, `master_data.yaml customer_variants[Sobo12]`.
