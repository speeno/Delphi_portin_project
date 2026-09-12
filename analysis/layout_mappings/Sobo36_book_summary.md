# 레이아웃 매핑: Sobo36_book_summary (도서별원장총괄) — 원장관리 신설

DEC-028 의무 — dfm→(영역, 위젯 ID, TabOrder, DBGrid 컬럼, 이벤트) 1:1 매핑. 픽셀/폰트/색상 제외.

> **배경(2026-09-12 교문사 요청)** — 「북이오웍스_원장관리(위러브솔루션 기능 복원)_260912」 6항:
> 원장관리 메뉴에 레거시 「도서별원장총괄」을 복원한다. 추가 요구 2가지:
> (a) 도서별 **현재고**를 함께 보여 줄 것 — 레거시에도 `GSUMY`「현재재고」 컬럼이 있어 그대로 유지,
> (b) 조회 일자를 **년월** → **년월일~년월일** 로.

## 0. 입력 산출물 (정본)

- dfm: `WeLove_FTP/도서유통-출판/MySQL/도서유통/한국도서유통출판/출판/Subu36.dfm`
  (L1 `object Sobo36: TSobo36`, L6 `Caption = '도서별원장총괄'`)
- pas: 같은 폴더 `Subu36.pas` (1,341줄)
- 레거시 메뉴: 같은 폴더 `Chul.dfm` L445 `Caption = '도서별원장총괄'` (원장관리 대메뉴)

> **빌드 번호 충돌 주의** — `Subu36` 은 빌드마다 다른 화면이다. 통계 트리의 `Subu36` 은
> 「거래처통계」이고 이미 `Sobo36_stats_route` 가 그 folder 를 쓰고 있다. 그래서 신규 화면의
> 레지스트리 id 는 **`Sobo36_book_summary`** (folder 는 `Subu36` 공용, MULTI_MAP).
> `FORM_REGISTRY` 는 id 로 find 하므로 id 중복은 절대 금지.

### 0-1. 테넌트 분기 (레거시 `Button101Click` L285~293)

```pascal
Sqlen := 'Select Scode From G7_Ggeo Where '+D_Select+'Gcode=''@Gcode'''; // @Gcode = Hnnnn
if Base10.Seek_Name(Sqlen) <> '1' then Button102Click else Button103Click;
```

| G7_Ggeo.Scode | 경로 | 데이터 소스 |
| --- | --- | --- |
| `<> '1'` | `Button102Click` (L295~611) | **Sv_Ghng 스냅샷 + S1_Ssub 델타 + Sg_Csum** |
| `= '1'`   | `Button103Click` (L613~976) | 스냅샷 생략 + `Sb_Csum`(반품재고) 추가 |

**교문사(hcode 5019, remote_153×chul_09_db)의 `G7_Ggeo.Scode` 는 `''`** — 2026-09-12 라이브
확인. 따라서 웹은 `Button102Click`(3소스) 경로만 구현한다. DEC-033 상 서비스 코드 분기 금지이므로
`Scode='1'` 변형이 실제로 필요해지면 contract `customer_variants` 로 주입한다.

## 1. 화면 구조

| 영역 | dfm | 역할 | 웹 |
| --- | --- | --- | --- |
| 검색 패널 `Panel001` (L140) | `Edit101`/`Edit102`(거래일자)·`Edit103~106`(도서 구간)·`CheckBox2`·`dxButton1` | 조회 조건 | `PageHeader` children (DEC-268 필터 줄) |
| 상단 `Panel002` → `DBGrid101` (L516) | 「검색자료」 (`Base10.T3_Sub61`) | 도서별 누계 | `SplitListPanes.top` + `DataGrid` |
| 하단 `Panel003` → `DBGrid201` (L637) | 「상세검색」 (`Base10.T3_Sub62`) | 선택 도서 년월별 | `SplitListPanes.bottom` + `DataGrid` |
| 상태 `Panel007` (L767) | `Panel008`「레코드」/`Panel009` `RecNo/RecordCount`/`ProgressBar1` | 진행·건수 | `SectionHeader` meta (`레코드 n`) |
| 좌측 `CornerButton1/2/3/9` + `Label301/302/303/309` | 「조회」「검색자료」「상세검색」「상태」 구역 라벨 | 장식 | 섹션 제목으로 흡수 |

## 2. 위젯 1:1 (TabOrder = dfm Panel001 기준)

| TabOrder | dfm 위젯 | 캡션/마스크 | 웹 `data-legacy-id` | 비고 |
| --- | --- | --- | --- | --- |
| 0 | `Edit101` `TFlatMaskEdit` | `!9999.!99` 시작 년월 | `Sobo36.Edit101` | **년월일**(`DateFieldYMD`) 로 확대 |
| 1 | `Edit102` `TFlatMaskEdit` | `!9999.!99` 종료 년월 | `Sobo36.Edit102` | **년월일**로 확대 |
| 2 | `Edit103` `TFlatEdit` | 시작 도서**코드**(`Visible=False`) | — | `MasterLookupField.value` 로 흡수 |
| 3 | `Edit104` `TFlatEdit` | 시작 도서명 | `Sobo36.Edit104` | `MasterLookupField` 입력칸 |
| 4 | `Edit105` `TFlatEdit` | 끝 도서**코드**(`Visible=False`) | — | `MasterLookupField.value` 로 흡수 |
| 5 | `Edit106` `TFlatEdit` | 끝 도서명 | `Sobo36.Edit106` | `MasterLookupField` 입력칸 |
| 6 | `Panel101` | `거래일자` | — | `<Label>거래일자` |
| 7 | `Panel102` | `도 서 명` / `본사도서` / `창고도서` 토글 | — | 백엔드 `scope` 파라미터(A/B/전체). 1차 UI 미노출 |
| 8 | `Button101` `TFlatButton` | 조회(숨김 트리거) | — | `dxButton1` 과 동일 동작 |
| 9 | `Button201` `TFlatButton` | 하단 조회(숨김) | — | 행 선택으로 대체 |
| 10 | `CheckBox2` `TFlatCheckBox` | `본사출고제외` (`Checked=True`) | `Sobo36.CheckBox2` | **하단에만** 적용 |
| 11/12 | `DateEdit1/2` `TDateEdit` | 달력 버튼 (`Visible=False`) | — | `DateFieldYMD` 내장 달력 |
| 13 | `Button701` `TFlatButton` | 시작 도서 검색 팝업 | `Sobo36.Button701` | `MasterLookupField` 버튼 |
| 14 | `Button702` `TFlatButton` | 끝 도서 검색 팝업 | `Sobo36.Button702` | `MasterLookupField` 버튼 |
| 15 | `dxButton1` `TdxButton` | `검색` | `Sobo36.dxButton1` | 조회 버튼 |
| — | `Label100` `TmyLabel3d` | `(하단을 검색하기 위한 일자)` | `Sobo36.Label100` | 안내문 그대로 노출 |
| — | `Label101`/`Label102` | `~` | `Sobo36.Label102` | 범위 구분자 |
| — | `Panel009` | `RecNo/RecordCount` | `Sobo36.Panel009` | 「레코드 n」 |
| — | `DBGrid101`/`DBGrid201` | 그리드 | `Sobo36.DBGrid101` / `.DBGrid201` | `DataGrid legacyId` |

이벤트 매핑

| dfm 이벤트 | pas 핸들러 | 웹 |
| --- | --- | --- |
| `dxButton1.OnClick` / `Button101.OnClick` | `Button101Click` → `Button102Click` | `GET /api/v1/ledger/book-summary` |
| `DBGrid101.OnDblClick` | `Button007Click` → `T00:=0` → `Button201Click` | 행 클릭/Enter → `GET .../book-summary/months` |
| `DBGrid101/201.OnTitleClick` | `Base10.ColumnS9` (정렬) | `useClientSort` 헤더 정렬 |
| `Edit111KeyPress`/`Edit101Change` | Enter=다음 칸 | `advanceFilterOnEnter` + `FILTER_STOP_IDS` (DEC-104/113) |
| `Button012/013Click` | `ColumnY1/Y2` (컬럼 설정) | `GridColumnSettings` |
| `Button010/011Click` | `DBGridSaveHtml` | `엑셀 다운로드` / `출력` |

## 3. 그리드 컬럼

### 3-1. 상단 `DBGrid101` (dfm L559~634) — 「검색자료」

| # | Title.Caption | FieldName | 웹 필드 | Footer |
| --- | --- | --- | --- | --- |
| 1 | `도 서 명` | `GNAME` | `gname` | `fvtStaticText` = 「합계」 |
| 2 | `입고수량` | `GIQUT` | `giqut` | `fvtSum` |
| 3 | `출고수량` | `GOQUT` | `goqut` | `fvtSum` |
| 4 | `증정수량` | `GJQUT` | `gjqut` | `fvtSum` |
| 5 | `반품수량` | `GBQUT` | `gbqut` | `fvtSum` |
| 6 | `폐기수량` | `GPQUT` | `gpqut` | `fvtSum` |
| 7 | `판매금액` | `GSUMX` | `gsumx` | `fvtSum` |
| 8 | `현재재고` | `GSUMY` | `gsumy` | `fvtSum` |

> 웹은 맨 앞에 **`도서코드`** 컬럼을 추가한다(레거시엔 없음 — 웹 원장 화면 공통 관례).
> 컬럼 설정에서 숨길 수 있다.

### 3-2. 하단 `DBGrid201` (dfm L679~764) — 「상세검색」

| # | Title.Caption | FieldName | 웹 필드 | Footer |
| --- | --- | --- | --- | --- |
| 1 | `년월` | `GUBUN` | `ym` | `fvtStaticText` = 「합계」 |
| 2 | `변경수량` | `GSUMX` | `gsumx` | `fvtSum` |
| 3 | `입고수량` | `GIQUT` | `giqut` | `fvtSum` |
| 4 | `출고수량` | `GOQUT` | `goqut` | `fvtSum` |
| 5 | `증정수량` | `GJQUT` | `gjqut` | `fvtSum` |
| 6 | `반품수량` | `GBQUT` | `gbqut` | `fvtSum` |
| 7 | `폐기수량` | `GPQUT` | `gpqut` | `fvtSum` |
| 8 | `판매수량` | `GSQUT` | `gsqut` | `fvtSum` |
| 9 | `판매금액` | `GSUMY` | `gsumy` | `fvtSum` |

> ⚠ **`GSUMX`/`GSUMY` 의 의미가 상·하단에서 뒤바뀐다.**
> 상단 `GSUMX`=판매금액·`GSUMY`=현재재고 / 하단 `GSUMX`=변경수량·`GSUMY`=판매금액.

## 4. 산식

### 4-1. 상단 (`Button102Click`)

```
snap = MAX(Sv_Ghng.Gdate)                                              -- L313~316

① Sv_Ghng (Gdate = snap, Scode LIKE 축, Gcode 구간)                    -- L328~370
     Giqut/Goqut/Gjqut/Gbqut/Gpqut  += 같은 이름 컬럼
     GsumX                          += Gosum + Gbsum
     GsumY                          += Gsusu − Gsqut

② Sg_Csum (Gdate <= snap) GROUP BY Gcode                               -- L382~404
     Gpsum := SUM(Gbsum)      ← **그리드 컬럼이 아니다** (웹 미구현)

③ S1_Ssub (snap < Gdate <= 종료일, Ocode LIKE 축, Bcode 구간)          -- L417~523
     GROUP BY Bcode, Scode, Gubun, Pubun → 아래 분기표

④ Sg_Csum (snap < Gdate <= 종료일, Scode 축)  GROUP BY Scode, Gcode     -- L560~597
     Gpsum += Gbsum ;  Scode ∉ {C,D} 이면 GsumY += Gbsum

⑤ SpaceDel(nSqry,'Gcode','Gname')  ← 도서명이 빈 행 제거 (Base01.pas L2826)  -- L598
⑥ IndexName := 'IDXGCODEDOWN' (Gcode 정렬)                              -- L600
```

③ 분기표 (L457~521, `St3=Gubun / St4=Pubun / St5=Scode`)

| 조건 | 누적 |
| --- | --- |
| `Scode='Y'` & `Gubun=반품` & `Pubun=반품` | `Giqut += q`, `GsumY += q` |
| `Scode='Y'` & `Gubun=입고` | `Giqut += q`, `GsumY += q` |
| `Pubun=증정` | `Gjqut += q`, `GsumX += amt`, `GsumY −= q` |
| `Gubun=출고` | `Goqut += q`, `GsumX += amt`, `GsumY −= q` |
| `Gubun=폐기` & `Pubun=비품` | `Gpqut += q`, `GsumX += amt` |
| `Gubun=폐기` & 그 외 | `Gpqut += q`, `GsumX += amt`, `GsumY += q` |
| `Pubun∈{비품,폐기}` & `Pubun=비품` | `Gbqut += q`, `GsumX += amt` |
| `Pubun∈{비품,폐기}` & `Pubun=폐기` | `Gpqut += q`, `GsumX += amt` (+ `mChek`&`chul_09_db` 면 `GsumY += q`) |
| `Gubun=반품` | `Gbqut += q`, `GsumX += amt`, `GsumY −= q` |

- **표시 측정치(`Giqut/Goqut/Gjqut/Gbqut/Gpqut/GsumX`)** 는 웹 서비스
  `book_summary_ledger_service._apply_subu36_branch` 가 그대로 구현한다.
- **`GsumY`(현재재고)** 는 재구현하지 않고 `reports_service._fetch_stock_asof` 를 재사용한다.
  같은 3소스(Sv_Ghng 스냅샷 `Gsusu−Gsqut` + S1_Ssub 델타 + Sg_Csum `Scode∉{C,D}`)이고
  DEC-138/283 에서 라이브 대사까지 끝낸 함수다. 레거시 `mChek`&`chul_09_db` 분기는 그 함수의
  `_apply_stock_branch` 가 이미 공통 경로(`Pubun=폐기` & `Scode='Z'` → `+q`)로 흡수했다.
- **부호 정규화 금지** — 반품·폐기는 음수 저장 관례(DEC-138)라 합계가 음수로 보이는 것이 정상.

### 4-2. 하단 (`Button201Click`, T00=0 = 상단 선택 도서)

```
S1_Ssub (시작일 <= Gdate <= 종료일, Bcode = 선택도서, Ocode LIKE 축)     -- L1021~1025
  [본사출고제외 체크 시] AND ((Scode='X' AND Gcode<>'00001') OR Scode='Y' OR Scode='Z')  -- L1017~1019
  GROUP BY Gdate, Scode, Gubun, Pubun  →  버킷 키 = Copy(Gdate,1,7) (년월)  -- L1042

Sg_Csum (기간, Gcode = 선택도서, Scode LIKE 축)                          -- L1124~1127
  GsumX(변경수량) += Gbsum
```

분기표 (L1053~1091)

| 조건 | 누적 |
| --- | --- |
| `Scode='Y'` & `Gubun∈{입고,반품}` | `Giqut += q` |
| `Pubun=증정` | `Gjqut += q`, `GsumY += amt` |
| `Gubun=출고` | `Goqut += q`, `Gsqut += q`, `GsumY += amt` |
| `Gubun=폐기` | `Gpqut += q` (판매수량/금액 **제외**) |
| `Pubun∈{비품,폐기}` & `Scode='X'` | `Gbqut += q`, `Gsqut += q`, `GsumY += amt` |
| `Pubun∈{비품,폐기}` & 그 외 | `Gpqut += q`, `Gsqut += q`, `GsumY += amt` |
| `Gubun=반품` | `Gbqut += q`, `Gsqut += q`, `GsumY += amt` |

## 5. 레거시와 의도적으로 다른 점

| # | 레거시 | 웹 | 근거 |
| --- | --- | --- | --- |
| 1 | 조회 일자 `년월`(`!9999.!99`), SQL 은 `Edit101+'.00' ~ Edit102+'.99'` | `년월일 ~ 년월일` (`DateFieldYMD`) | 사용자 확정 2026-09-12 (요청 6항 b) |
| 2 | 상단 상한 = `Edit102 + '.99'`(종료월 말) | 상한 = **종료일** | 1의 자연 확장 |
| 3 | 스냅샷 = `MAX(Sv_Ghng.Gdate)` (상한 없음) | `MAX(Gdate) WHERE Gdate <= 종료일` | `_fetch_stock_asof` 와 **같은 스냅샷**을 보게 해 두 소스 불일치 방지 |
| 4 | 도서 구간은 `Edit105`(끝 코드)가 비면 **둘 다 무시** | from/to 각각 독립 적용 | 한쪽만 지정하는 사용을 허용 (상위집합) |
| 5 | `Gpsum`(Sg_Csum 누계)을 계산하지만 그리드에 없음 | 미구현 | 표시되지 않는 값 |
| 6 | 「본사도서/창고도서」 토글(`Panel102` 더블클릭) | 백엔드 `scope` 파라미터만 제공, UI 미노출 | 1차 범위 — 필요 시 토글 추가 |
| 7 | 페이지네이션 없음 | 동일(전 행 반환) | 합계가 「전 검색 결과」 기준이어야 함 |
| 8 | — | `도서코드` 컬럼 추가 | 웹 원장 화면 공통 관례 (숨김 가능) |

## 6. API

| Method | Path | 설명 |
| --- | --- | --- |
| GET | `/api/v1/ledger/book-summary` | 상단 — `serverId`·`dateFrom`·`dateTo`·`bcodeFrom`·`bcodeTo`·`scope`·`hcode` |
| GET | `/api/v1/ledger/book-summary/months` | 하단 — `serverId`·`bcode`·`dateFrom`·`dateTo`·`scope`·`excludeHqOut`·`hcode` |

- 서비스: `backend/app/services/book_summary_ledger_service.py`
- 라우터: `backend/app/routers/ledger.py` (`enforce_hcode_isolation` — 비-슈퍼는 로그인 출판사 Hcode 강제)
- 프런트: `frontend/src/app/(app)/ledger/book-summary/page.tsx`
- 레지스트리: `Sobo36_book_summary` (menuGroup `inventory`, menuId `ACC-MENU-NAV-03`, `report.inventory.read`)
- 스모크: `debug/probe_backend_all_servers.py` `ledger.book_summary` / `ledger.book_summary_months`

## 7. 라이브 대사 (remote_153 × chul_09_db, hcode 5019, 2026-09-12)

고객 스크린샷(거래일자 `2026.09 ~ 2026.09`, 레코드 42/**3020**) 대비:

| 컬럼 | 웹 계산 | 레거시 화면 | 판정 |
| --- | --- | --- | --- |
| 입고수량 | 5,571,222 | 5,571,222 | ✅ |
| 출고수량 | 5,889,678 | 5,889,678 | ✅ |
| 증정수량 | 263,794 | 263,794 | ✅ |
| 반품수량 | −1,370,884 | −1,370,884 | ✅ |
| 폐기수량 | −26,644 | −26,644 | ✅ |
| 판매금액 | 73,**491,213,362** | (칸 폭에 잘려) 491,213,362 | ✅ 하위 9자리 일치 |
| 현재재고 | 473,579 | 473,579 | ✅ |
| 레코드 수 | 3,020 | 3,020 | ✅ |

- 스냅샷 기준일 `2009.12.31`, `SpaceDel` 제거 행 **69건**(3,089 → 3,020).
  이 69건을 빼기 전에는 출고 5,889,829 / 증정 263,798 / 반품 −1,370,932 로 어긋난다 —
  **`SpaceDel` 은 선택이 아니라 필수**다(DEC-274 와 같은 이유).
- 하단 교차검증(도서 `91764`, 2026.01~09, 본사출고제외 해제):
  원시 `X/출고/위탁 2,047 (89,417,000)` · `X/출고/증정 80 (0)` · `X/반품/정품 −286 (−12,584,000)` ·
  `Y/입고/재생 1,025` → 출고 2,047 / 증정 80 / 반품 −286 / 입고 1,025 /
  판매수량 1,761 / 판매금액 76,833,000 — 전부 일치.
  본사출고제외 **체크**(기본) 시 출고 1,617 / 판매금액 62,007,000 (Scode='X' & Gcode='00001' 제외분 차이).
