# 레이아웃 매핑: Sobo49 (세금계산서발행) → 모던 `/settlement/tax-invoice` [C5 Phase 2]

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑. 픽셀 좌표·폰트·색상은 가져오지 않음.

> **사용자 결정 (Phase 2)**: 세금계산서 외부 발행 채널(홈택스/이메일 등) 미회신 — `/api/v1/settlement/tax-invoice/{key}/issue` 는 200 + `NOT_INTEGRATED` 응답으로 stub 처리(DEC-035 신설). Chek3 토글 + 내부 보관본(HTML 미리보기) 만 정식 구현.

## 0. 입력 산출물

- 본 폼: [`tools/.../legacy_source_root/Subu49/Sobo49.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu49/Sobo49.html) + `Sobo49.form.json` + `Sobo49.tree.json` + `Sobo49.pas_analysis.json`
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu49.dfm`](../../legacy_delphi_source/legacy_source/Subu49.dfm)
- 원 pas: [`legacy_delphi_source/legacy_source/Subu49.pas`](../../legacy_delphi_source/legacy_source/Subu49.pas)
  - `FormActivate` (L154 — `nForm:='49'`, `nSqry:=T4_Sub91`, `mSqry:=T4_Sub92`)
  - `Button101Click` (L327~420 — 월 SELECT `Hcode,Sum26,Sum27,Sum28,Chek3,Sdate` + Sum27 ≠ 0 인 행만 발행대상)
  - `Button016Click` (L282 — `Tong40.print_49_41(Self)`) / `Button017Click` (L287 — `Tong40.print_49_42`)
  - `Button200Click` (L601~613 — 단건 인쇄 `Tong40.PrinTing00('49','2',...)`)
  - `DBGrid101Columns7UpdateData` (L695~715 — 단건 Chek3 토글: `Code1='1' → Chek3='0'`, 그 외 `'1'`)
  - `RadioButton4Click` (L717~744 — 일괄 Chek3 토글 `'1'`) / `RadioButton5Click` (L746~773 — 일괄 `'0'`)
  - `T4_Sub91BeforePost` (L657~677 — Sdate 변경 시 `UPDATE T2_Ssub SET Sdate=:sdate WHERE Gdate=LEFT(:nGdate,7) AND Hcode=:hcode`)
- 모던 라우트(예정 — T6 신설):
  - 목록: [`도서물류관리프로그램/frontend/src/app/(app)/settlement/tax-invoice/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/settlement/tax-invoice/page.tsx)
  - 미리보기: [`도서물류관리프로그램/frontend/src/app/(app)/settlement/tax-invoice/[billingKey]/print/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/settlement/tax-invoice/[billingKey]/print/page.tsx)
- 백엔드: `GET /api/v1/settlement/tax-invoice` / `POST /api/v1/settlement/tax-invoice/{key}/chek3` / `POST .../issue` / `GET .../print` (T5b 신설)
- 계약: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) v1.1.0

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유

레거시 `Sobo49` 는 **단일 화면 안에서 (a) 월 SELECT → (b) DBGrid101 8컬럼 → (c) Col7 체크박스(저장) 단건 토글 + RadioButton4/5 일괄 토글 → (d) Button200/016/017 인쇄** 흐름을 모달리스로 운영. Chek3 컬럼은 `T2_Ssub` 의 동일 행에 속하므로 단일 진실원이며, dfm 의 `CODE1`/`Code1` 픽 리스트는 표면 표현일 뿐 실제는 `Chek3` 를 UPDATE 한다 (`Subu49.pas` L699/723/752 — 동일 SQL 패턴 3곳).

모던:
- (a)(b) → `/settlement/tax-invoice` 목록 페이지 (DataGrid 8컬럼 + Phase 1 페이지네이션)
- (c) Col7 체크박스 → 단건 토글 호출 `POST /tax-invoice/{key}/chek3` (`bulk:false`)
- (c) RadioButton4/5 → 일괄 토글 호출 (`bulk:true, toggle:'1'|'0'`) — 단일 트랜잭션
- (d) Button200 (단건 인쇄) → 행 우측 "인쇄" 링크 → `/tax-invoice/{key}/print`
- (d) Button016/017 (일괄 인쇄) → Phase 2 미구현 (C7 후속)
- 세금계산서 외부 발행 → `Button{X}Issue` 액션 → `POST .../issue` stub

**핵심 결정** — DEC-036(신설): Chek3 단건/일괄 토글은 동일 백엔드 엔드포인트에서 `bulk:bool` 플래그로 분기, SQL 헬퍼 1개로 흡수 (3곳 중복 패턴 단일화).

## 2. dfm 영역 인벤토리 (tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수·핵심) | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | Edit100(콤보 월), Edit101/102(시작/종료 일자), Edit103/105(코드), Edit104/106(이름), Panel101/102, Button101/201, RadioButton4/5, dxButton1(검색) | 목록 페이지 검색 영역 |
| 좌측 본 그리드 (`DBGrid101`) | `Panel002` | 1 | 8컬럼 — GCODE/GNAME/SDATE/GOSUM/GBSUM/GSSUM/CODE2(구분)/CODE1(저장체크) | 목록 DataGrid |
| 좌측 푸터 | `Panel007` | 2 | 레코드/검색진행 + ProgressBar | 페이지네이션 카운터 |
| 우측 보조 패널 | `Panel003` | 3 | Edit201/202(보조 일자), Label3d, ProgressBar1 | 미사용 (보조 표시) |
| 데이터셋 | `T4_Sub91`(본), `T4_Sub92`(보조), `DataSource1/2` | n/a | ClientDataSet 2 | 백엔드 응답으로 흡수 |
| Corner 버튼 | `CornerButton1/2/9` | n/a | 디자인 장식(좌측 빨강/파랑/검정 띠) | 무시 (장식) |
| Label301/302/309 | (Label) | n/a | "조회"/"검색자료"/"상태" 좌측 회전 라벨 | 시멘틱 `<aside>` 또는 `aria-label` |

## 3. 검색 패널 위젯 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (`/settlement/tax-invoice`) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit (Visible=false) | 시작일자 (`yyyy.mm.dd`) | (보조 — 월 단위 검색) | `Sobo49.Edit101` |
| 1 | `Edit102` | TFlatMaskEdit (Visible=false) | 종료일자 | (보조) | `Sobo49.Edit102` |
| 2 | `Edit103` | TFlatEdit (Visible=false) | 출판사코드(시작) | `<CustomerSearchInput id="hcodeFrom">` | `Sobo49.Edit103` |
| 3 | `Edit104` | TFlatEdit (Visible=false) | 출판사명(시작) | (lookup 표시) | `Sobo49.Edit104` |
| 4 | `Edit105` | TFlatEdit (Visible=false) | 출판사코드(종료) | `<CustomerSearchInput id="hcodeTo">` | `Sobo49.Edit105` |
| 5 | `Edit106` | TFlatEdit (Visible=false) | 출판사명(종료) | (lookup 표시) | `Sobo49.Edit106` |
| 6 | `Panel101` | TFlatPanel | "조회일자" 라벨 | `<label htmlFor="month">조회일자</label>` | `Sobo49.Panel101` |
| 7 | `Panel102` | TFlatPanel (Visible=false) | "출판사명/입고처명/거 래 처" 토글 | (Phase 2: 단일 출판사명) | `Sobo49.Panel102` |
| 8 | `Button101` (Visible=false) | TFlatButton | 조회(보조) | (`dxButton1` 와 동일 의미) | `Sobo49.Button101` |
| 9 | `Button201` (Visible=false) | TFlatButton | 신규 (Phase 1 패턴) | (out-of-scope) | — |
| 10 | `Edit100` | TFlatComboBox | **조회월** (예 `2010.12`) | `<input type="month" id="month">` | `Sobo49.Edit100` |
| 11 | `dxButton1` | TdxButton | **검색** | `<Button onClick={onSearch}>검색</Button>` | `Sobo49.dxButton1` |
| n/a | `RadioButton4` | TFlatRadioButton | **일괄 발행 ON** | `<Button onClick={onBulkIssueOn}>일괄 발행</Button>` | `Sobo49.RadioButton4` |
| n/a | `RadioButton5` | TFlatRadioButton | **일괄 발행 OFF** | `<Button onClick={onBulkIssueOff}>일괄 해제</Button>` | `Sobo49.RadioButton5` |
| n/a | `Button016` | TFlatButton (인쇄 1) | (Phase 2 out-of-scope — C7) | (미구현) | — |
| n/a | `Button017` | TFlatButton (인쇄 2) | (Phase 2 out-of-scope — C7) | (미구현) | — |
| n/a | `Button200` | TFlatButton (단건 인쇄) | `<Link href="/tax-invoice/{key}/print">인쇄</Link>` | 행 우측 액션 | `Sobo49.Button200` |

## 4. 좌측 본 그리드 매핑 (`DBGrid101`)

| dfm FieldName | 한글 헤더 | 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GCODE` | 코드 | 거래처 코드 | `<th>코드</th>` | `Sobo49.DBGrid101.GCODE` |
| `GNAME` | 출판사명 | 거래처명 | `<th>출판사명</th>` | `Sobo49.DBGrid101.GNAME` |
| `SDATE` | 발행일자 | 세금계산서 발행 예정일 (`T2_Ssub.Sdate`) | `<th>발행일자</th>` (편집 가능) | `Sobo49.DBGrid101.SDATE` |
| `GOSUM` | 금액 | `T2_Ssub.Sum26` (당월금액) | `<th>금액</th>` (SUM 푸터, fvtSum) | `Sobo49.DBGrid101.GOSUM` |
| `GBSUM` | 세액 | `T2_Ssub.Sum27` | `<th>세액</th>` (SUM 푸터) | `Sobo49.DBGrid101.GBSUM` |
| `GSSUM` | 발행금액 | `Sum26 + Sum27` | `<th>발행금액</th>` (SUM 푸터) | `Sobo49.DBGrid101.GSSUM` |
| `CODE2` | 구분 | 영수/청구 (PickList — 본 Phase 2 는 표시만) | `<th>구분</th>` | `Sobo49.DBGrid101.CODE2` |
| `CODE1` | **저장** | **체크박스 — `T2_Ssub.Chek3` 토글 단일 진실원** | `<th>저장</th>` `<input type="checkbox">` | `Sobo49.DBGrid101.CODE1` |

> 푸터: `GOSUM`, `GBSUM`, `GSSUM` 만 fvtSum (합계) — 모던도 `<tfoot>` 합계 행으로 보존.
>
> `Code1` ↔ `Chek3` 매핑 규약 (DEC-036 단일 진실원):
> - `Code1='1'` (체크 ON) ⇔ `T2_Ssub.Chek3='1'` (영수/발행됨)
> - `Code1='0'` (체크 OFF) ⇔ `T2_Ssub.Chek3='0'` (청구/미발행)
> - 단, 레거시 `DBGrid101Columns7UpdateData` (L704~706) 는 `Code1='1' → '@Chek3','0'` 으로 **반전 토글** 함 — 클릭 시점의 상태가 Code1='1' 이면 새 Chek3='0', 그 외 '1'. 즉, 현재 표시값을 기준으로 토글한다. 모던도 동일하게 "현재값의 부정"을 새 값으로 전송 (백엔드는 `toggle: '1'|'0'` 명시 인자로 받음 — 모던은 클릭 시점에 부정값을 계산해 전달).

## 5. 데이터 흐름 (`Subu49.pas` 인용)

```
조회 (Button101Click L327~420)
  → SELECT Hcode, Sum26, Sum27, Sum28, Chek3, Sdate FROM T2_Ssub WHERE Gdate=:gdate (D_Select)
  → for each row WHERE Sum27<>0:
       T4_Sub91 채움 (Hname=Seek_Name, Gdate=월말, GsumX=Sum26, Gosum=Sum27, Gbsum=Sum28,
                     Gssum=Sum27+Sum28, GsumY=Sum26+Sum27+Sum28, Code1=if Chek3='1' '1' else '0',
                     Code2='청구')

단건 토글 (DBGrid101Columns7UpdateData L695~715)
  → UPDATE T2_Ssub SET Chek3=(if Code1='1' '0' else '1') WHERE Gdate=Copy(nGdate,1,7) AND Hcode=Gcode

일괄 ON  (RadioButton4Click L717~744) → for each row: UPDATE T2_Ssub SET Chek3='1' ...; Code1='1'
일괄 OFF (RadioButton5Click L746~773) → for each row: UPDATE T2_Ssub SET Chek3='0' ...; Code1='0'

발행일자 변경 (T4_Sub91BeforePost L657~677, dsEdit only)
  → UPDATE T2_Ssub SET Sdate=:sdate WHERE Gdate=:gdate AND Hcode=:hcode

인쇄 단건 (Button200Click L601~613) → Tong40.PrinTing00('49','2', mSqry.Gdate, ...)
인쇄 일괄 (Button016/017Click)       → Tong40.print_49_41/42(Self)  (Phase 2 미구현 — C7)
```

## 6. out-of-scope 위젯 (Phase 2 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 일괄 인쇄 | `Button016/017` | C7 후속 |
| Tong40.PrinTing00 (Delphi Canvas) | (런타임) | DEC-034: 모던은 HTML+`window.print()` |
| 외부 채널 발행 (홈택스/이메일) | `Button200` 의 후속 동작 | DEC-035 stub (`/issue` → 200 NOT_INTEGRATED) |
| Glyph 비트맵 / Corner 버튼 | `CornerButton1/2/9`, 모든 Glyph.Data | DEC-028 — 버린다 |
| Code2 PickList (영수/청구) 편집 | `DBGrid101.Col6` | Phase 2 표시만, 편집은 Phase 3 (또는 후속) |
| Excel 저장 | (없음 — Sobo46 와 달리 본 폼은 미제공) | n/a |

## 7. Deltas — 모던 신설 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | `<button>일괄 발행</button>` / `<button>일괄 해제</button>` | 검색 패널 우측 | RadioButton4/5 의미 보존 |
| 모던 신규 | "발행" 배지 (Chek3='1') / "미발행" 배지 (Chek3='0') | DBGrid Code2 옆 | 시각 보강 |
| 모던 신규 | `<a href=/tax-invoice/{key}/print>인쇄</a>` | 행 우측 액션 | Button200 흡수 |
| 모던 신규 | "외부 발행 미연결" 안내 배너 | 페이지 상단 | DEC-035 stub 가시화 |
| dfm out-of-scope | `Button016/017` 일괄 인쇄 | — | C7 이연 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 | 비고 |
| --- | --- | --- |
| `FormActivate` (L154) | `useEffect(mount)` | nForm/nSqry 매핑은 백엔드 책임 |
| `FormShow` (L161) | `useEffect(setDefaults)` | 시작일/종료일 = 오늘 |
| `Button101Click` / `dxButton1.OnClick` (L327) | `onSearch` → `taxInvoiceApi.list({month, hcode?})` | SQL-ST-18 |
| `DBGrid101Columns7UpdateData` (L695) | `onChek3Toggle({key, toggle: !current, bulk:false})` | SQL-ST-20 단건 |
| `RadioButton4Click` (L717) | `onBulkIssueOn` → `chek3Toggle({month, toggle:'1', bulk:true})` | SQL-ST-20 일괄 |
| `RadioButton5Click` (L746) | `onBulkIssueOff` → `chek3Toggle({month, toggle:'0', bulk:true})` | SQL-ST-20 일괄 |
| `T4_Sub91BeforePost` (L657, dsEdit) | `onSdateEdit` → `taxInvoiceApi.updateSdate({key, sdate})` | SQL-ST-21 |
| `Button200Click` (L601) | `<Link>` 라우팅 → 미리보기 페이지 | DEC-034 |
| `Button016/017Click` | (Phase 2 미구현) | C7 |
| `Button{X}Issue` (모던 신설) | `onIssue` → `POST /tax-invoice/{key}/issue` | DEC-035 stub |

## 9. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] §3·§4 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재 (총 ~22개):
  - 검색: `Sobo49.{Edit100..106, Panel101/102, dxButton1, Button101/200, RadioButton4/5}`
  - 그리드: `Sobo49.DBGrid101.{GCODE,GNAME,SDATE,GOSUM,GBSUM,GSSUM,CODE2,CODE1}`
- [ ] §6 out-of-scope (일괄 인쇄·Code2 편집·외부 발행 실연결) 가 코드에 들어가지 않음
- [ ] DEC-031 — 마감(`T2_Ssub.Yesno='1'`) 월에 Chek3 토글/Sdate UPDATE 시도 → 423 + 한글 메시지
- [ ] DEC-035 — `/issue` 응답에 `status:'NOT_INTEGRATED'` + audit 영속화
- [ ] DEC-036 — 단건/일괄 SQL 패턴이 `tax_invoice_service` 단일 헬퍼로 흡수 (3곳 중복 코드 0)
- [ ] DEC-028 §3 "버리는 정보" (픽셀 좌표·폰트·색상·Glyph) 가 코드에 없음

## 10. 참조

- DEC-012: soft cancel (yesno=2)
- DEC-024: 페이지네이션
- DEC-028: dfm→html 산출물 영구 입력 동결
- DEC-029: AuditPasswordModal token gate (본 폼은 단순 토글이라 audit token 불요. 일괄 토글은 audit 옵션화 — Phase 2 OFF)
- DEC-031: 마감 가드 (Phase 1)
- **DEC-034** (T8 신설): C5 Phase 2 인쇄 = HTML 미리보기
- **DEC-035** (T8 신설): 세금계산서 외부 발행 stub 정책 (OQ-ST-1 종결)
- **DEC-036** (T8 신설): Chek3 토글 단일 SQL 헬퍼 흡수
- 화면 카드: [`analysis/screen_cards/c5_settlement.md`](../screen_cards/c5_settlement.md)
- contract: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) v1.1.0
- 핸들러 인덱스: [`analysis/handlers/c5_phase2.md`](../handlers/c5_phase2.md)
- 선례: [`Sobo46_billing.md`](Sobo46_billing.md) (동일 Phase 2 인쇄 패턴), [`Sobo45_billing.md`](Sobo45_billing.md)
