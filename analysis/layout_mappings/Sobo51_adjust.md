# 레이아웃 매핑: Sobo51 (원장변경관리) → 모던 `/ledger/adjust/customer`

DEC-028 의무 매핑 노트. 2026-09-12 교문사 요청 — 레거시 자료관리 「원장변경」을 웹 **원장관리** 메뉴에 신설.

> ⚠ **폼 번호 충돌 주의.** `Subu51` 은 빌드마다 다른 화면이다.
> - 유통(정본) 트리 `legacy_delphi_source/legacy_source/Subu51.dfm` = **반품재고(변경)** → 별도 노트 [`Sobo51.md`](Sobo51.md)
> - 출판/총판 트리 `WeLove_FTP/도서유통-출판(총판)/Subu51.dfm` = **원장변경관리** ← 본 노트
>
> 그래서 모던 레지스트리 id 는 `Sobo51` 이 아니라 **`Sobo51_adjust`** 다(`Sobo51` 은 반품재고(변경)가 선점).
> 화면 안의 `data-legacy-id` 접두는 dfm 루트 객체 이름 그대로 **`Sobo51.`** 를 쓴다.

## 0. 입력 산출물

- 원 dfm(정본 — 교문사가 쓰는 빌드): [`WeLove_FTP/도서유통-출판/Subu51.dfm`](../../WeLove_FTP/도서유통-출판/Subu51.dfm) (Caption `원장변경관리`)
- 변형: [`WeLove_FTP/도서유통-총판/Subu51.dfm`](../../WeLove_FTP/도서유통-총판/Subu51.dfm) (Caption `원장변경관리`, Panel002/004 에 `거래처`/`입고처` 캡션 추가 — 그 외 동일)
- pas: [`WeLove_FTP/도서유통-출판/Subu51.pas`](../../WeLove_FTP/도서유통-출판/Subu51.pas)
- ⚠ 배치 변환 산출물 `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu51/` 은 **유통 트리(반품재고(변경))** 를 변환한 것이라 본 화면의 입력이 **아니다**(`Sobo51.meta.json.title == "반품재고(변경)"`). 본 매핑은 위 출판/총판 dfm 을 직접 읽어 작성했다.
- 모던 라우트: `도서물류관리프로그램/frontend/src/app/(app)/ledger/adjust/customer/page.tsx`
- 모던 본체(축 공용): `도서물류관리프로그램/frontend/src/components/ledger/adjustment-ledger-screen.tsx`
- API 클라이언트: `도서물류관리프로그램/frontend/src/lib/adjustment-ledger-api.ts`

## 1. 의미 — 거래처 원장 대조 조정

거래처(`G1_Ggeo`, varchar 5) 축의 **원장 대조 조정 행**을 직접 입력·수정하는 장부다.
저장 대상은 `Sg_Gsum` 의 `Scode='X'` 행이며, `Gcode` 가 거래처코드다.

| 컬럼 | 의미 |
|---|---|
| `Gdate` | 거래일자 |
| `Gcode` | 거래처코드 (`G1_Ggeo`) |
| `Gname` | 거래처명 (조인 표시, 읽기 전용) |
| `Gssum` | 대조금액 |
| `Gosum` | 원장금액 |
| `Gbsum` | 장부차액 — 기본식 `Gssum − Gosum`, **저장값이 식과 다른 행이 실재**하므로 편집 가능 |
| `Gbigo` | 적요 |

「창을 열자마자 입력·저장」하는 조정 장부라 모던도 조회 → 그리드 인라인 편집 → 저장 한 흐름이다.

## 2. dfm 영역 인벤토리

| 영역 | dfm 컨테이너 | TabOrder | 모던 매핑 |
|---|---|---:|---|
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | `PageHeader` 필터 줄 (DEC-268) |
| **상단 그리드** | `Panel002` → `DBGrid101` (TDBGridEh) | 1 / 0 | `SectionHeader` + `DataGrid` |
| 하단 검색 패널 | `Panel003` | 2 | **의도적 제외** (§6) |
| 하단 그리드 | `Panel004` → `DBGrid201` (입고처 축) | 3 / 0 | **의도적 제외** (§6) |
| 진행 패널 | `Panel007` (`ProgressBar0/1`, `Panel008/009/010`) | 4 | React `loading` 상태로 흡수 |
| 액션 코너 | `CornerButton1~4/9` + `Label301~304/309` | n/a | 모던 셸(사이드바/헤더)로 흡수 |

## 3. 상단 검색 패널 위젯 매핑 (`Panel001`)

TabOrder 는 출판 빌드 dfm 실측값. Enter=다음 이동 스톱 순서는 `Edit101 → Edit102 → Edit104 → dxButton1`
(`advanceFilterOnEnter`, 숨김 위젯은 스톱에서 제외).

| TabOrder | dfm 위젯 | 클래스 | 역할 | 모던 위젯 | data-legacy-id |
|---:|---|---|---|---|---|
| 0 | `Edit101` | TFlatMaskEdit | 거래일자(시작) | `DateFieldYMD` | `Sobo51.Edit101` |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자(종료) | `DateFieldYMD` | `Sobo51.Edit102` |
| 2 | `Edit103` (Visible=False) | TFlatEdit | 코드 보조 | 미포팅(숨김) | — |
| 3 | `Edit104` | TFlatEdit (w=209) | 거래처명/코드 검색어 | `<Input>` → `q` | `Sobo51.Edit104` |
| 4 | `Edit105` (Visible=False) | TFlatEdit | 코드 보조 | 미포팅(숨김) | — |
| 5 | `Edit106` (Visible=False) | TFlatEdit | 명칭 보조 | 미포팅(숨김) | — |
| 6 | `Panel101` | TFlatPanel | 라벨 `거래일자` | `<Label>거래일자` | `Sobo51.Panel101` |
| 7 | `Panel102` | TFlatPanel | 라벨 `거래처명` | `<Label>거래처명` | `Sobo51.Panel102` |
| 8 | `Button101` (Visible=False) | TFlatButton | 조회 보조 | dxButton1 로 통합 | — |
| 9 | `DateEdit1` | TDateEdit | 달력(시작) | `DateFieldYMD` 내장 달력 | — |
| 10 | `DateEdit2` | TDateEdit | 달력(종료) | `DateFieldYMD` 내장 달력 | — |
| 11 | `Button701` | TFlatButton | 저장/처리 보조 | 「저장」 버튼 | `Sobo51.Button701` |
| 12 | `dxButton1` | TdxButton `검색` | 조회 실행 | 「검색」 버튼 | `Sobo51.dxButton1` |
| — | `Label101` / `Label102` | TmyLabel3d `~` | 기간 구분자 | `~` 텍스트 | `Sobo51.Label101` |

기본 기간은 **올해 1월 1일 ~ 오늘**(사용자 확정 2026-09-12). 필터는 `useListSession("ledger.adjust.customer")` 로 보존한다.

## 4. 상단 그리드 매핑 (`DBGrid101`)

`FooterRowCount = 1`, `SumList.Active = True` — 합계 푸터 1행.

| # | FieldName | Title.Caption | dfm Width | Footer | 모던 컬럼 | 편집 | data-legacy-id |
|---:|---|---|---:|---|---|---|---|
| 1 | `GDATE` | 거래일자 | 80 | `fvtStaticText = '합계'` | 거래일자 | `DateFieldYMD` | `Sobo51.DBGrid101.GDATE` |
| 2 | `GCODE` | 코드 | 50 | — | 코드 | `MasterLookupField` (`lookupKind="customer"`) | `Sobo51.DBGrid101.GCODE` |
| 3 | `GNAME` | 거래처명 | 243 | — | 거래처명 | 읽기 전용 | `Sobo51.DBGrid101.GNAME` |
| 4 | `GSSUM` | 대조금액 | 90 | `fvtSum` | 대조금액 | 숫자 입력 | `Sobo51.DBGrid101.GSSUM` |
| 5 | `GOSUM` | 원장금액 | 90 | `fvtSum` | 원장금액 | 숫자 입력 | `Sobo51.DBGrid101.GOSUM` |
| 6 | `GBSUM` | 장부차액 | 90 | `fvtSum` | 장부차액 | 숫자 입력(자동식 기본) | `Sobo51.DBGrid101.GBSUM` |
| 7 | `GBIGO` | 적요 | 190 | — | 적요 | 텍스트 입력 | `Sobo51.DBGrid101.GBIGO` |
| + | — | — | — | — | 삭제(웹 전용) | 행 삭제 버튼 | `Sobo51.DBGrid101.DELETE` |

셀 입력 위젯에는 `.EDIT` 접미 id 를 더 붙인다(`Sobo51.DBGrid101.GSSUM.EDIT` 등).
`GNAME` 컬럼의 `ButtonStyle = cbsEllipsis` + `OnEditButtonClick`(거래처 검색 팝업) → 모던은 코드 칸의
`MasterLookupField` 검색 버튼(`Sobo51.DBGrid101.GNAME.ELLIPSIS`)으로 흡수했다. 인라인 자동완성은 켜지 않는다
(컴포넌트 기본값 유지 — DEC-193 의 「쓰기 화면 인라인 금지」 관례).

### 합계 (레거시 SumList)

- 합계 대상 = `GSSUM` · `GOSUM` · `GBSUM` 3컬럼. 첫 컬럼(`GDATE`)에는 정적 문자열 `합계`.
- 모던은 `DataGrid` 의 `totals` prop(sticky `tfoot`). 서버 `totals`(**전체 검색 결과** 합계)에
  화면의 미저장 변경분 델타(수정·추가·삭제)를 더해 레거시 SumList 처럼 입력 즉시 움직인다.

### 차액 자동식

`Gbsum = Gssum − Gosum` 을 기본으로 자동 계산하되, 사용자가 차액 칸을 직접 고치면 그 행은 자동 재계산을
멈춘다(`bsumTouched`). 서버에서 읽어온 행도 저장값이 식과 다르면 「직접 입력됨」으로 간주해 값을 보존한다.

## 5. 이벤트 / 데이터 매핑

| 레거시 | 모던 |
|---|---|
| `dxButton1Click` (검색) | `GET /api/v1/ledger/adjustments?axis=customer&dateFrom=&dateTo=&q=` |
| 그리드 삽입행 Post | `POST /api/v1/ledger/adjustments` (`axis=customer`) |
| 그리드 편집행 Post | `PATCH /api/v1/ledger/adjustments/{id}` |
| 그리드 행 Delete | `DELETE /api/v1/ledger/adjustments/{id}?axis=customer` |
| (없음 — 사용자가 원장금액 직접 입력) | `GET …/ledger-value?axis=customer` → `{supported:false}` 라 호출하지 않는다 |

저장은 **삭제 → 수정 → 신규** 순으로 행 단위 진행하며, 일부만 실패해도 성공분은 그대로 반영하고
실패한 행의 입력은 화면에 남긴다(오류 배너에 `n행(코드) — 사유` 나열, `formatApiError`).

## 6. 의도적 제외 — 하단 창(입고처)

사용자 확정(2026-09-12 교문사): **상단 창만 필요**. 아래는 포팅하지 않았다.

| dfm | 내용 | 사유 |
|---|---|---|
| `Panel003` (TabOrder 2) | 하단 검색 패널 — `Edit201/202`(기간), `Edit204`(입고처명), `Panel201/202`, `DateEdit3/4`, `Button201` | 요구 제외 |
| `Panel004` → `DBGrid201` (TabOrder 3) | 입고처 축 조정 그리드(같은 7 컬럼, `GNAME` = 입고처명) | 요구 제외 |
| `Panel007` | 진행률 패널 | React `loading` 으로 대체 |
| `CornerButton*` / `Label30*` | 델파이 폼 코너 액션 | 모던 셸이 담당 |

필요해지면 이 문서의 §4 표를 그대로 재사용해 같은 컴포넌트에 **입고처 축**(`AdjustmentAxis`) 하나를
더 추가하면 된다 — 코드 분기 없이 축 객체만 늘어난다.

## 7. 고객 변형

출판/총판 두 빌드의 상단 창은 위젯 id·TabOrder·컬럼 7종이 동일하고 캡션만 미세하게 다르다
(총판은 `Panel002` 에 `거래처` 캡션 추가). 코드 분기 없이 동일 화면으로 처리한다.
차이를 굳이 데이터로 남겨야 할 일이 생기면 `migration/contracts/<flow>.yaml` 의 `customer_variants` 로 간다.
