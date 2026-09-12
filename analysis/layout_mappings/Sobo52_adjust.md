# 레이아웃 매핑: Sobo52 (재고변경관리-(본사)) → 모던 `/ledger/adjust/book`

DEC-028 의무 매핑 노트. 2026-09-12 교문사 요청 — 레거시 자료관리 「재고변경」을 웹 **원장관리** 메뉴에 신설.
상단 창 골격·위젯 id 는 [`Sobo51_adjust.md`](Sobo51_adjust.md)(원장변경)와 **완전히 같고**, 축(코드·컬럼 의미)만 다르다.

> ⚠ **폼 번호 충돌 주의.** `Subu52` 는 빌드마다 다른 화면이다.
> - 유통(정본) 트리 `legacy_delphi_source/legacy_source/Subu52.dfm` = **정품재고(변경)**
> - 출판/총판 트리 `WeLove_FTP/도서유통-출판(총판)/Subu52.dfm` = **재고변경관리-(본사)** ← 본 노트
>
> 모던 레지스트리 id 는 원장변경과 짝을 맞춰 **`Sobo52_adjust`** 다.
> 화면 안의 `data-legacy-id` 접두는 dfm 루트 객체 이름 그대로 **`Sobo52.`** 를 쓴다.

## 0. 입력 산출물

- 원 dfm(정본 — 교문사가 쓰는 빌드): [`WeLove_FTP/도서유통-출판/Subu52.dfm`](../../WeLove_FTP/도서유통-출판/Subu52.dfm) (Caption `재고변경관리-(본사)`)
- 변형: [`WeLove_FTP/도서유통-총판/Subu52.dfm`](../../WeLove_FTP/도서유통-총판/Subu52.dfm) (Caption `재고변경관리`, 그리드 캡션 `도서코드`/`도 서 명` — §7)
- pas: [`WeLove_FTP/도서유통-출판/Subu52.pas`](../../WeLove_FTP/도서유통-출판/Subu52.pas)
- ⚠ 배치 변환 산출물 `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu52/` 는 **유통 트리(정품재고(변경))** 변환본이라 본 화면의 입력이 **아니다**(`Sobo52.meta.json.title == "정품재고(변경)"`).
- 모던 라우트: `도서물류관리프로그램/frontend/src/app/(app)/ledger/adjust/book/page.tsx`
- 모던 본체(축 공용): `도서물류관리프로그램/frontend/src/components/ledger/adjustment-ledger-screen.tsx`
- API 클라이언트: `도서물류관리프로그램/frontend/src/lib/adjustment-ledger-api.ts`

## 1. 의미 — 도서 재고 대조 조정(본사)

도서(`G4_Book`, varchar 10) 축의 **재고 대조 조정 행**을 직접 입력·수정하는 장부다.
저장 대상은 `Sg_Csum` 의 `Scode='A'`(본사) 행이며, `Gcode` 가 도서코드다.

| 컬럼 | 의미 |
|---|---|
| `Gdate` | 거래일자 |
| `Gcode` | 도서코드 (`G4_Book`) |
| `Gname` | 도서명 (조인 표시, 읽기 전용) |
| `Gssum` | 대조재고 |
| `Gosum` | 원장재고 |
| `Gbsum` | 변경수량 — 기본식 `Gssum − Gosum`, **저장값이 식과 다른 행이 실재**하므로 편집 가능 |
| `Gbigo` | 적요 |

`Sg_Csum` 은 도서 재고 산식의 **3소스 중 하나**(스냅샷 + 델타 + `Sg_Csum`)다 — 여기서 입력하는 행이
그대로 재고에 가산된다. 음수 저장 관례도 그대로다(메모리 「도서 재고 산식 정본」 참조).

## 2. dfm 영역 인벤토리

| 영역 | dfm 컨테이너 | TabOrder | 모던 매핑 |
|---|---|---:|---|
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | `PageHeader` 필터 줄 (DEC-268) |
| **상단 그리드** | `Panel002` → `DBGrid101` (TDBGridEh) | 1 / 0 | `SectionHeader` + `DataGrid` |
| 하단 검색 패널 | `Panel003` | 2 | **의도적 제외** (§6) |
| 하단 그리드 | `Panel004` → `DBGrid201` (비품 축) | 3 / 0 | **의도적 제외** (§6) |
| 진행 패널 | `Panel007` (`ProgressBar0/1`, `Panel008/009/010`) | 4 | React `loading` 상태로 흡수 |
| 액션 코너 | `CornerButton1~4/9` + `Label301~304/309` | n/a | 모던 셸(사이드바/헤더)로 흡수 |

## 3. 상단 검색 패널 위젯 매핑 (`Panel001`)

Sobo51 과 위젯 id·TabOrder 가 동일하다. 유일한 차이는 `Panel102` 캡션(`거래처명` → **`도서명`**).
Enter=다음 이동 스톱 순서 = `Edit101 → Edit102 → Edit104 → dxButton1`.

| TabOrder | dfm 위젯 | 클래스 | 역할 | 모던 위젯 | data-legacy-id |
|---:|---|---|---|---|---|
| 0 | `Edit101` | TFlatMaskEdit | 거래일자(시작) | `DateFieldYMD` | `Sobo52.Edit101` |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자(종료) | `DateFieldYMD` | `Sobo52.Edit102` |
| 2 | `Edit103` (Visible=False) | TFlatEdit | 코드 보조 | 미포팅(숨김) | — |
| 3 | `Edit104` | TFlatEdit (w=209) | 도서명/코드 검색어 | `<Input>` → `q` | `Sobo52.Edit104` |
| 4 | `Edit105` (Visible=False) | TFlatEdit | 코드 보조 | 미포팅(숨김) | — |
| 5 | `Edit106` (Visible=False) | TFlatEdit | 명칭 보조 | 미포팅(숨김) | — |
| 6 | `Panel101` | TFlatPanel | 라벨 `거래일자` | `<Label>거래일자` | `Sobo52.Panel101` |
| 7 | `Panel102` | TFlatPanel | 라벨 **`도서명`** | `<Label>도서명` | `Sobo52.Panel102` |
| 8 | `Button101` (Visible=False) | TFlatButton | 조회 보조 | dxButton1 로 통합 | — |
| 9 | `DateEdit1` | TDateEdit | 달력(시작) | `DateFieldYMD` 내장 달력 | — |
| 10 | `DateEdit2` | TDateEdit | 달력(종료) | `DateFieldYMD` 내장 달력 | — |
| 11 | `Button701` | TFlatButton | 저장/처리 보조 | 「저장」 버튼 | `Sobo52.Button701` |
| 12 | `dxButton1` | TdxButton `검색` | 조회 실행 | 「검색」 버튼 | `Sobo52.dxButton1` |
| — | `Label101` / `Label102` | TmyLabel3d `~` | 기간 구분자 | `~` 텍스트 | `Sobo52.Label101` |

기본 기간은 **올해 1월 1일 ~ 오늘**. 필터는 `useListSession("ledger.adjust.book")` 로 보존한다.

## 4. 상단 그리드 매핑 (`DBGrid101`)

`FooterRowCount = 1`, `SumList.Active = True` — 합계 푸터 1행.

| # | FieldName | Title.Caption | Footer | 모던 컬럼 | 편집 | data-legacy-id |
|---:|---|---|---|---|---|---|
| 1 | `GDATE` | 거래일자 | `fvtStaticText = '합계'` | 거래일자 | `DateFieldYMD` | `Sobo52.DBGrid101.GDATE` |
| 2 | `GCODE` | 코드 | — | 코드 | `MasterLookupField` (`lookupKind="book"`) | `Sobo52.DBGrid101.GCODE` |
| 3 | `GNAME` | 도서명 | — | 도서명 | 읽기 전용 | `Sobo52.DBGrid101.GNAME` |
| 4 | `GSSUM` | 대조재고 | `fvtSum` | 대조재고 | 숫자 입력 | `Sobo52.DBGrid101.GSSUM` |
| 5 | `GOSUM` | 원장재고 | `fvtSum` | 원장재고 | 숫자 입력(**자동 채움**) | `Sobo52.DBGrid101.GOSUM` |
| 6 | `GBSUM` | 변경수량 | `fvtSum` | 변경수량 | 숫자 입력(자동식 기본) | `Sobo52.DBGrid101.GBSUM` |
| 7 | `GBIGO` | 적요 | — | 적요 | 텍스트 입력 | `Sobo52.DBGrid101.GBIGO` |
| + | — | — | — | 삭제(웹 전용) | 행 삭제 버튼 | `Sobo52.DBGrid101.DELETE` |

셀 입력 위젯에는 `.EDIT` 접미 id 를 더 붙인다. `GNAME` 컬럼의 `ButtonStyle = cbsEllipsis` +
`OnEditButtonClick`(도서 검색 팝업) → 코드 칸의 `MasterLookupField` 검색 버튼
(`Sobo52.DBGrid101.GNAME.ELLIPSIS`)으로 흡수. 인라인 자동완성은 켜지 않는다(컴포넌트 기본값).

### 합계 (레거시 SumList)

- 합계 대상 = `GSSUM` · `GOSUM` · `GBSUM`. 첫 컬럼(`GDATE`)에는 정적 문자열 `합계`.
- 모던은 `DataGrid` 의 `totals` prop. 서버 `totals`(전체 검색 결과 합계) + 화면의 미저장 변경분 델타.

### 원장재고 자동 채움 (모던 보강)

코드를 고르거나 직접 입력해 확정하면 `GET …/ledger-value?axis=book&gcode=&asof=<거래일자>` 로
**기준일 원장재고**(정본 재고 산식)를 받아 `GOSUM` 을 채우고, 이어서 `GBSUM = GSSUM − GOSUM` 을 재계산한다.
응답 `supported:false` 이거나 호출이 실패하면 조용히 넘어가 레거시처럼 사용자가 직접 입력한다.
사용자가 변경수량을 직접 고친 행은 자동 재계산을 멈춘다(`bsumTouched`).

## 5. 이벤트 / 데이터 매핑

| 레거시 | 모던 |
|---|---|
| `dxButton1Click` (검색) | `GET /api/v1/ledger/adjustments?axis=book&dateFrom=&dateTo=&q=` |
| 그리드 삽입행 Post | `POST /api/v1/ledger/adjustments` (`axis=book`) |
| 그리드 편집행 Post | `PATCH /api/v1/ledger/adjustments/{id}` |
| 그리드 행 Delete | `DELETE /api/v1/ledger/adjustments/{id}?axis=book` |
| (레거시 수기 입력) | `GET /api/v1/ledger/adjustments/ledger-value?axis=book&gcode=&asof=` → `GOSUM` 자동 채움 |

저장은 **삭제 → 수정 → 신규** 순으로 행 단위 진행하며, 일부만 실패해도 성공분은 그대로 반영하고
실패한 행의 입력은 화면에 남긴다(오류 배너에 `n행(코드) — 사유` 나열, `formatApiError`).

## 6. 의도적 제외 — 하단 창(비품)

사용자 확정(2026-09-12 교문사): **상단 창만 필요**. 아래는 포팅하지 않았다.

| dfm | 내용 | 사유 |
|---|---|---|
| `Panel003` (TabOrder 2) | 하단 검색 패널 — `Edit201/202`(기간), `Edit204`(도서명), `Panel201/202`, `DateEdit3/4`, `Button201` | 요구 제외 |
| `Panel004` → `DBGrid201` (TabOrder 3) | 비품 축 조정 그리드(상단과 같은 7 컬럼) | 요구 제외 |
| `Panel007` | 진행률 패널 | React `loading` 으로 대체 |
| `CornerButton*` / `Label30*` | 델파이 폼 코너 액션 | 모던 셸이 담당 |

필요해지면 `AdjustmentAxis` 객체를 하나 더 추가하는 것으로 끝난다 — 코드 분기 0.

## 7. 고객 변형

| 항목 | 출판 빌드(정본) | 총판 빌드 |
|---|---|---|
| 폼 Caption | `재고변경관리-(본사)` | `재고변경관리` |
| `GCODE` Title | `코드` | `도서코드` |
| `GNAME` Title | `도서명` | `도 서 명` |
| `Panel002`/`Panel004` 캡션 | 없음 | 있음 |

위젯 id·TabOrder·컬럼 7종·Footer 구성은 동일하다. 캡션 차이는 화면 코드가 아니라 축 객체
(`BOOK_ADJUSTMENT_AXIS` 의 `codeLabel`/`nameLabel`)의 값이며, 계정·hcode 별 코드 분기는 두지 않는다.
고객별로 갈라야 할 일이 생기면 `migration/contracts/<flow>.yaml` 의 `customer_variants` 로 간다.
