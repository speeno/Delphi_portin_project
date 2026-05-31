# 레이아웃 매핑: Sobo15 (기타거래처관리·G5 마스터) → 모던 `/masters/etc-customers` (Phase F 신설)

account-menu-fxx-rbac **Phase F-1** — 누락 3화면 정본화. `Subu15/Sobo15.*` 단일 원천 (출판/**총판** 빌드).

## 0. 입력 산출물 (dfm-layout-input 룰)

- 정본 DFM: [`WeLove_FTP/도서유통-총판/Subu15.dfm`](../../WeLove_FTP/도서유통-총판/Subu15.dfm) + `Subu15.pas` (`TSobo15`, Caption=`기타거래처관리`). 출판 빌드 [`도서유통-출판/Subu15.dfm`](../../WeLove_FTP/도서유통-출판/Subu15.dfm) 도 G5_Ggeo 동일.
- accelerator 산출물: [`tools/.../legacy_source_root/Subu15/Sobo15.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu15/Sobo15.html), `.form.json`, `.tree.json`, `.meta.json`(`title=기타거래처관리`), `.pas_analysis.json`.
- 마스터 테이블: **`G5_Ggeo`**(기타거래처 본) + **`G5_Gbun`**(거래처 구분/서브). DataSource1=`T1_Sub51`(본), DataSource2=`T1_Sub52`(구분).
- 게이트: `Menu105Click` → `Seek_Uses('F15')` ([`도서유통-출판/Chul.pas`](../../WeLove_FTP/도서유통-출판/Chul.pas) L1983~). 모던 라우트 `/master/etc-customer` (form-registry `Sobo15`, 기존 마스터 화면 컨벤션), API `/api/v1/masters/etc-customers` ([`menu_route_crud_map.yaml`](../../migration/contracts/menu_route_crud_map.yaml) `ACC-MENU-MASTERS-03`).
- 빌드 변형(**핵심**): WH 빌드는 `Sobo15`=**거래처관리-개별(G1_Ggeo/G1_Gbun)**, 출판/총판은 `Sobo15`=**기타거래처(G5_Ggeo/G5_Gbun)**. → `master_data.yaml customer_variants[Sobo15]` 에 G1↔G5 diff 기록.

> ⚠️ WH 빌드 `legacy_delphi_source/legacy_source/Subu15`(`Sobo15`=거래처-개별, INSERT `G1_Ggeo`) 비정본. 본 매핑은 **출판/총판 G5_Ggeo 기타거래처 F15** 전용.

## 1. 의미 분기 — 마스터+서브 그리드 + 등록 폼 (Sobo11/Sobo12 동일 패턴)

레거시 Sobo15 = **DBGrid101(기타거래처 목록, G5_Ggeo) + DBGrid201(서브: 거래처 구분, G5_Gbun) + Panel002 본 등록·수정 폼 + Panel004 구분 폼 + Panel007 진행률바**.

**구현 상태(2026-05-30 — 거래처 Sobo11 패턴으로 상세 복원 완료)**: 거래처(Sobo11)와 동형 Ggeo 마스터로,
본 폼 `Panel002` 전체 입력(Edit101~127·비율·발행유무) + 구분 폼 `Panel004`(G5_Gbun) 전체 CRUD 를
**분리 라우트**로 복원. 단일 SimpleMasterPage(목록만) → 목록/상세/신규 3 라우트로 승격.
- 목록(검색·확장 컬럼): `/master/etc-customer`
- 상세(보기/수정/삭제): `/master/etc-customer/[gcode]` (`EtcCustomerDetailForm` + `EtcCustomerCategoryCollapsible`)
- 신규 등록: `/master/etc-customer/new` (`EtcCustomerDetailForm` createMode + 구분 접기 패널)
- API: `GET/POST/PATCH/DELETE /api/v1/masters/etc-customers`(+`/{gcode}`), `/api/v1/masters/etc-customer-categories`(+`/{gcode}`)
- 스키마 어댑터: [`g5_ggeo_adapt.py`](../../도서물류관리프로그램/backend/app/services/g5_ggeo_adapt.py) — `SHOW COLUMNS` 기반 존재 컬럼만 SELECT/PATCH (멀티 DB).

## 2. dfm 영역 인벤토리 (TabOrder)

| 영역 | dfm | TabOrder | 내용 |
| --- | --- | :-: | --- |
| 상단-좌 목록 | `Panel001` | 0 | `DBGrid101` (기타거래처 목록) |
| 상단-우 등록폼 | `Panel002` | 1 | 본 등록·수정 (Edit101~127, CheckBox1, Button101~104) |
| 하단-좌 서브목록 | `Panel003` | 2 | `DBGrid201` (거래처 구분) |
| 하단-우 서브폼 | `Panel004` | 3 | 구분 등록·수정 (Edit201/202, Button201~203) |
| 상태바 | `Panel007` | 4 | `ProgressBar0/1` + 레코드/검색진행 |
| 검색 | `Button000` | 5 | 거래처 검색 (`OnClick=FormShow`) |

## 3. 상단 그리드 `DBGrid101` (기타거래처 목록) — 컬럼 매핑

목록 = `/master/etc-customer` (목록 전용). 정렬 기본 `Gcode`. 모던 목록은 레거시 3컬럼보다 **구분·지역·연락처·주소** 를 추가 노출(입고처 Sobo12·거래처 Sobo11 패턴).

| dfm 컬럼 | FieldName | Title.Caption | 모던 목록 컬럼 | `data-legacy-id` |
| --- | --- | --- | --- | --- |
| col0 | `GCODE` | 코드 | 코드 | `Sobo15.DBGrid101.GCODE` |
| col1 | `GNAME` | 거래처명 | 거래처명 | `Sobo15.DBGrid101.GNAME` |
| col2 | `SCODE` | ^ | 거래처구분(`gbun_name`/`gubun`) | `Sobo15.DBGrid101.SCODE` |
| — | `Jubun` | 거래처지역 | 지역 | `Sobo15.Edit102` |
| — | `Guper` | 대표자 | 대표자 | `Sobo15.Edit108` |
| — | `Gtel1`/`Gtel2` | 전화 | 전화(합침) | `Sobo15.Edit112` |
| — | `Gpost` | 우편번호 | 우편번호 | `Sobo15.Edit111` |
| — | `Gadd1`/`Gadd2` | 주소 | 주소(`gjuso`) | `Sobo15.Edit116` |

검색 필터(모던): `q`(코드·거래처명·대표자·전화·사업자번호 LIKE), `gubun`(G5_Gbun 코드), `jubun`(지역 LIKE). API `GET /api/v1/masters/etc-customers?gubun=&jubun=`.

wrapper `data-legacy-id="Sobo15.DBGrid101"`.

## 4. 서브 그리드 `DBGrid201` (거래처 구분, G5_Gbun)

| dfm 컬럼 | FieldName | Title.Caption | Width | `data-legacy-id` |
| --- | --- | --- | :-: | --- |
| col0 | `GCODE` | 코드 | 40 | `Sobo15.DBGrid201.GCODE` |
| col1 | `GNAME` | 거래처구분 | 159 | `Sobo15.DBGrid201.GNAME` |

## 5. 본 등록·수정 폼 `Panel002` — 입력 위젯 (TabOrder 순)

> **정정(2026-05-30)**: 아래 라벨/필드 바인딩은 **정본 `Subu15.pas`** `nSqry.FieldByName(...)` 로드(L336~365) 와
> `INSERT INTO G5_Ggeo`(L393~) 기준으로 확정. (Phase F-1 초안의 라벨 추정치를 .pas 실제 바인딩으로 교정.)

| TabOrder | dfm | 클래스 | 라벨(캡션) | G5_Ggeo 필드 | API 키 | `data-legacy-id` |
| :-: | --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | ComboBox | 거래처구분 | `Gubun`(→`G5_Gbun.Gname`) | `gbun_name` | `Sobo15.Edit101` |
| 1 | `Edit102` | Edit | 거래처지역 | `Jubun` | `jubun` | `Sobo15.Edit102` |
| 2 | `Edit103` | Edit | 거래처코드 | `Gcode` | `gcode` | `Sobo15.Edit103` |
| 3 | `Edit104` | Edit | 거래처코드2 | `Ocode` | `ocode` | `Sobo15.Edit104` |
| 4 | `Edit105` | Edit | 거래처명 | `Gname` | `gname` | `Sobo15.Edit105` |
| 5 | `Edit106` | Edit | 출고증구분 | `Gposa` | `gposa` | `Sobo15.Edit106` |
| 6 | `Edit107` | Edit | 사업자번호 | `Gnumb` | `gnumb` | `Sobo15.Edit107` |
| 7 | `Edit108` | Edit | 대표자 | `Guper` | `guper` | `Sobo15.Edit108` |
| 8 | `Edit109` | Edit | 업태/종목 | `Gjomo` | `gjomo` | `Sobo15.Edit109` |
| 9 | `Edit110` | Number | 한도액 | `Gpper` | `gpper` | `Sobo15.Edit110` |
| 10 | `Edit111` | Edit | 우편번호 | `Gpost` | `gpost` | `Sobo15.Edit111` |
| 11 | `Edit112` | Edit | 전화번호1 | `Gtel1` | `gtel1` | `Sobo15.Edit112` |
| 12 | `Edit113` | Edit | 전화번호2 | `Gtel2` | `gtel2` | `Sobo15.Edit113` |
| 13 | `Edit114` | Edit | 팩스번호1 | `Gfax1` | `gfax1` | `Sobo15.Edit114` |
| 14 | `Edit115` | Edit | 팩스번호2 | `Gfax2` | `gfax2` | `Sobo15.Edit115` |
| 15 | `Edit116` | Edit | 주소1 | `Gadd1` | `gadd1` | `Sobo15.Edit116` |
| 16 | `Edit117` | Edit | 주소2 | `Gadd2` | `gadd2` | `Sobo15.Edit117` |
| 17~22 | `Edit118~123` | Number | 비율(위탁/현매/매절/납품/특별/기타) | `Grat1`~`Grat6` | `grat1`~`grat6` | `Sobo15.Edit118`…`Sobo15.Edit123` |
| 23 | `Edit124` | Number | 신간수량 | `Gqut1` | `gqut1` | `Sobo15.Edit124` |
| 24 | `CheckBox1` | CheckBox | 발행유무(계산서) | `Yesno` | `yesno` | `Sobo15.CheckBox1` |
| 25 | `Edit125` | Edit | 비고1 | `Gbigo` | `gbigo` | `Sobo15.Edit125` |
| 26 | `Edit126` | Edit | 계산서 거래처명 | `Name1` | `name1` | `Sobo15.Edit126` |
| 27 | `Edit127` | Edit | 정지사유 | `Name2` | `name2` | `Sobo15.Edit127` |

> 레거시 INSERT 는 `Grat7/Grat8/Grat9` 를 항상 0 으로 채우며 본 폼 입력 위젯이 없음 → 모던 폼/모델에서 제외(어댑터는 존재 컬럼만 patch).

버튼(캡션 변형 주의 — **추가/등록/삭제**): `Button101`(추가/신규, tab0) · `Button102`(등록/저장, tab1) · `Button103`(삭제, tab2) · `Button104`(우편번호 검색 glyph, tab45). `data-legacy-id="Sobo15.Button101"` 등. 모던은 신규=`Button101`(목록 헤더), 상세 저장=`Button102`, 삭제=`Button103`.

## 6. 서브 등록·수정 폼 `Panel004` (거래처 구분)

| TabOrder | dfm | 라벨 | MaxLen | `data-legacy-id` |
| :-: | --- | --- | :-: | --- |
| 0 | `Edit201` | 구분코드 | 5 | `Sobo15.Edit201` |
| 1 | `Edit202` | 구분명 | 20 | `Sobo15.Edit202` |

버튼: `Button201`(추가)·`Button202`(등록)·`Button203`(삭제).

## 7. deltas (모던 신설)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` | `Gcode`/`Gname` LIKE — 모던 신설(Button000 대체) |
| `<DataGridPager>` | 서버 사이드 페이징 (DEC-024) |
| `<WriteGate>`/`<PrintGate>` | Phase D caps 게이트 (F15 O/R/X) |

## 8. 이벤트 매핑

| dfm 이벤트 | 레거시 동작 | 모던 핸들러 |
| --- | --- | --- |
| `FormActivate`/`FormShow` | 그리드 리로드 | 페이지 mount fetch |
| `Button000Click` (검색) | `SELECT … FROM G5_Ggeo WHERE Hcode … ORDER BY Gcode` | `GET /api/v1/masters/etc-customers` |
| `Button102Click` (등록) | `INSERT/UPDATE G5_Ggeo` (`G5_GGEO_ID_GEN`) | `POST/PATCH` (caps `canWrite`) |
| `Button103Click` (삭제) | `DELETE FROM G5_Ggeo WHERE Gcode … AND Hcode …` | `DELETE` (caps `canWrite`, DEC-019 확인) |
| `Button202Click` (구분 등록) | `INSERT/UPDATE G5_Gbun` (`G5_GBUN_ID_GEN`) | 구분 `POST/PATCH` |
| `DBGrid101DblClick`/`OnKeyDown` | 행 선택→폼 로드 | onRowClick → `/master/etc-customer/{gcode}` 상세 |
| `Button101` (새화면) | 신규 등록 폼 | `/master/etc-customer/new` |
| 거래처구분 `Panel004` | G5_Gbun CRUD | 상세/신규 `EtcCustomerCategoryCollapsible` (목록 탭 없음) |
| `Edit101Change` (공유 OnChange) | 더티 플래그 | form onChange |

> **O/R/X 게이팅 근거**: `Menu105Click` 의 `'O'`→`Panel002/Panel004.Enabled:=True`+그리드 KeyDown 연결, `'R'`→`Enabled:=False`/이벤트 `nil`(조회·인쇄만), `'X'`→메뉴 미진입. 모던 caps 정합.

## 9. 변형 차이 (build variant) — **G1 vs G5**

- **빌드 변형 분기 금지** — 차이는 `master_data.yaml customer_variants[Sobo15]` 에만.
- **WH 빌드**: `Sobo15`=거래처관리-개별, 테이블 `G1_Ggeo`/`G1_Gbun`, INSERT `G1_Ggeo`.
- **출판/총판 빌드(정본)**: `Sobo15`=기타거래처, 테이블 `G5_Ggeo`/`G5_Gbun`, `Menu105`=F15. 모던은 출판/총판 정본만 구현(G5).
- 위젯 트리·TabOrder 는 두 빌드 거의 동일(거래처 마스터 폼 공통). 차이는 **테이블 prefix(G1↔G5)·캡션(거래처관리-개별↔기타거래처관리)** 뿐 → 데이터/계약 변이로만 흡수.

## 10. 회귀 가드 체크리스트 (Phase F)

- [x] dfm 위젯 ID 누락 0 — 부착 `data-legacy-id` ↔ 매핑노트 추적성 자동검사 ([`test/test_master_missing_screens_frontend.py`](../../test/test_master_missing_screens_frontend.py)). **본 폼 Panel002 전체 필드 + 구분 Panel004 CRUD 복원 완료**(잔여 P2 없음).
- [x] `GET/POST/PATCH/DELETE /api/v1/masters/etc-customers`(+`/{gcode}`) · `/api/v1/masters/etc-customer-categories`(+`/{gcode}`) 등록.
- [x] CRUD 계약/권한 가드 회귀 ([`test/test_master_missing_screens_crud_api_contract.py`](../../test/test_master_missing_screens_crud_api_contract.py)) · 어댑터 단위 ([`test/test_g5_ggeo_adapt.py`](../../test/test_g5_ggeo_adapt.py)).
- [x] `GET /api/v1/masters/etc-customers`/`etc-customer-categories` 4서버 스모크 매트릭스 등록 ([`debug/probe_backend_all_servers.py`](../../debug/probe_backend_all_servers.py)).
- [x] `phase1-component-fidelity.md` 갱신 · GAP-P0=0 (DEC-053, 행 38).
- [x] tsc/eslint 0 신규.

## 11. 참조

- DEC-019/023/028/053 · `OQ-LICENSE-KEY-MAP` (F15 정본, 웹 임시값 F13 정정).
- 단일 매핑 정본: [`analysis/audit/account-menu-fxx-mapping.md`](../audit/account-menu-fxx-mapping.md) §2.1/§3.
- 선례 패턴: `Sobo11.md`(거래처 G1), `Sobo12.md`(입고처 G2), `Sobo17.md`(master+sub).
- 계약: `rbac_menu_matrix.yaml ACC-MENU-MASTERS-03`, `menu_route_crud_map.yaml`, `master_data.yaml customer_variants[Sobo15]`.
