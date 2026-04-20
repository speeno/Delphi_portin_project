# 레이아웃 매핑: Sobo46 (청구서출력) → 모던 `/settlement/billing/[billingKey]/print` [C5 Phase 2]

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑. 픽셀 좌표·폰트·색상은 가져오지 않음.

> **사용자 결정 (Phase 2)**: 인쇄 = HTML 미리보기까지만(PDF/실인쇄는 C7 이연). 따라서 Sobo46 의 모던 페이지는 "청구 헤더 + 일별 31행 + 67 합계" 를 1매 미리보기로 구성하고 `window.print()` 만 트리거.

## 0. 입력 산출물

- 본 폼: [`tools/.../legacy_source_root/Subu46/Sobo46.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu46/Sobo46.html) + `Sobo46.form.json` + `Sobo46.tree.json` + `Sobo46.pas_analysis.json`
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu46.dfm`](../../legacy_delphi_source/legacy_source/Subu46.dfm)
- 원 pas: [`legacy_delphi_source/legacy_source/Subu46.pas`](../../legacy_delphi_source/legacy_source/Subu46.pas)
  - `FormActivate` (L303 — `nForm:='46'`, `nSqry:=T4_Sub61`, `mSqry:=T4_Sub62`)
  - `Button101Click` (L485~563 — 거래처 검색 + 좌측 그리드 채움 + T2_Ssub 마감 상태 마킹)
  - `Button201Click` (L565~) — 단건 선택 시 67 Edit 값 + 31일 라인 + T3_Ssub 채움
  - `Button016Click` (L418~432 — Bcode='완료' AND Yesno='O' 루프 → `Tong40.print_46_01`)
  - `Button017Click` (L434~448 — 동일 패턴 → `Tong40.print_46_02`)
- 모던 라우트(예정 — T6 신설): [`도서물류관리프로그램/frontend/src/app/(app)/settlement/billing/[billingKey]/print/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/settlement/billing/[billingKey]/print/page.tsx)
- 백엔드 데이터: `GET /api/v1/settlement/billing/{billing_key}/print-data` (T5a 신설)
- 계약: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) v1.1.0 (Phase 2)

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유

레거시 `Sobo46` 은 거래처별 1매 청구서를 **사전 미리보기 + Tong40.print_46_01/02 인쇄** 두 단계로 운영. Edit201~Edit315 67개 Edit 는 모두 표시 전용(`SetVal`) — 사용자가 편집하지 않음. 따라서 모던에서는:

- 67 Edit → 백엔드 응답 JSON 으로 묶어 1매 인쇄 카드의 **합계 행** 으로 흡수
- 좌측 출판사 그리드 (`DBGrid101`) → 청구서 목록 페이지(`/settlement/billing`)로 이전, **본 페이지는 단건 미리보기**
- 우측 일별 그리드 (`DBGrid201`) → 1매 미리보기의 본문 표 (31행 × 16컬럼)
- `Button016/017` 일괄 인쇄 → 모던은 목록 페이지의 "선택 인쇄" 액션 (Phase 2 단순화: 단건 미리보기만 — 일괄은 브라우저 새 창 N개 또는 후속)
- `Button701/702` (인쇄/마감) → 본 페이지에는 `window.print()` 버튼만. 마감은 Phase 1 `/settlement/billing` 에서 이미 구현됨.

**핵심 결정** — DEC-034(신설): Phase 2 인쇄 = HTML 미리보기. PDF/실인쇄/일괄/세무 양식 사이즈 보존은 C7 인쇄 모듈로 이연.

## 2. dfm 영역 인벤토리 (tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수·핵심) | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색·메타 패널 | `Panel001` (TFlatPanel) | 0 | Edit100~105, Edit101 콤보, Button101/201, Label101, RadioButton4/5 | (목록 페이지 `/settlement/billing` 책임 — 본 페이지는 검색 미사용) |
| 좌측 출판사 그리드 (`DBGrid101`) | (Panel002) | 1 | 거래처 1건/행 (HCODE/HNAME/BNAME/GBIGO/GMEMO/BCODE/YESNO) | 목록 페이지에 이미 구현 (Phase 1) |
| 좌측 푸터 (`StBar101`) | (StatusBar) | n/a | 레코드/검색진행 | 무시 |
| **본 미리보기: 67 합계 패널 (Panel003 → Edit201~Edit315)** | `Panel003` | 2 | 67개 TFlatNumber/TFlatEdit (출고·반품·발송비 합계) | **`<table>` 푸터 합계 + 좌측 카드 합계 영역** |
| **본 미리보기: 우측 일별 그리드 (`DBGrid201`)** | (DBGrid in Panel) | 3 | 16컬럼 — GDATE/GQUT1~7/NAME1/NAME2/GNAME/GCODE/GSQUT/GSSUM/YESNO | **`<table>` 본문 31행** |
| 푸터 액션 (`StBar201`) | StatusBar | n/a | 인쇄 진행 | 무시 |
| 데이터셋 | `T4_Sub61` (좌측), `T4_Sub62` (우측), `DataSource1/2` | n/a | ClientDataSet 2 | 백엔드 `settlement_print_service` 가 단일 응답에 묶음 |

## 3. 백엔드 응답 (`GET /settlement/billing/{billing_key}/print-data`) 매핑

| 응답 키 | 출처 (`Subu46.pas`) | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- |
| `header.gdate` | `mSqry.Gdate` (월키, 6자) | 카드 머리글 (월) | `Sobo46.Header.Gdate` |
| `header.hcode` / `header.hname` | `mSqry.Hcode` + `Seek_Ggeo` | 카드 머리글 (거래처) | `Sobo46.Header.Hcode` / `Sobo46.Header.Hname` |
| `header.bname` (출판사명/주소 보조) | `mSqry.Bname` | 카드 머리글 보조 | `Sobo46.Header.Bname` |
| `lines[]` (31행) | `nSqry` (T4_Sub61) — 일별 31행 | 표 본문 | `Sobo46.DBGrid201.Row{N}` |
| `lines[].gdate` (DD) | `nSqry.Gdate` | 일자 셀 | `Sobo46.DBGrid201.GDATE` |
| `lines[].gqut1~7` | `nSqry.Gqut1~7` | 출고·반품 수치 | `Sobo46.DBGrid201.GQUT{1..7}` |
| `lines[].name1/name2/gname/gcode/gsqut/gssum` | T3_Ssub 라인 | 발송비·금액 셀 | `Sobo46.DBGrid201.{NAME1,NAME2,GNAME,GCODE,GSQUT,GSSUM}` |
| `lines[].yesno` | `nSqry.Yesno` | 상태 배지 | `Sobo46.DBGrid201.YESNO` |
| `summary.sum01..sum69` (67개 — 매핑) | `Edit201..Edit315` (T2_Ssub Sum01~Sum69) | 좌측 합계 카드 + 표 푸터 | `Sobo46.Summary.Sum{NN}` (각 Edit 의 dfm Name 보존) |
| `summary.sum26 / sum27 / sum28` | Edit226/227/228 (당월/세액/합계) | 우측 큰 합계 (Phase 1 contract `summary`) | `Sobo46.Summary.Sum26..28` |
| `summary.gsusu / vdate / bigo1 / bigo2` | Edit310/Edit238/Edit239/Edit901 | 보조 메모 영역 | `Sobo46.Summary.Gsusu`, `Vdate`, `Bigo1`, `Bigo2` |

> 67개 Sum 필드는 백엔드가 `T2_Ssub` 의 Sum01~Sum69 컬럼을 그대로 묶어 응답 — 모던은 일부만 표시(주요 5종) + `<details>` 로 나머지를 토글. Sobo46 와 동일한 모든 dfm 위젯 ID 를 `data-legacy-id` 로 부착해 회귀 가드는 보존.

## 4. 우측 일별 그리드 매핑 (`DBGrid201`)

| dfm FieldName | 한글 헤더 | 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GDATE` | 일자 | 일자(DD) | `<th>일자</th>` | `Sobo46.DBGrid201.GDATE` |
| `GQUT1` | 출고\|시내 | 시내 출고 부수 | `<th>시내</th>` | `Sobo46.DBGrid201.GQUT1` |
| `GQUT2` | 출고\|지방 | 지방 출고 부수 | `<th>지방</th>` | `Sobo46.DBGrid201.GQUT2` |
| `GQUT3` | 출고\|박스 | 박스대 부수 | `<th>박스</th>` | `Sobo46.DBGrid201.GQUT3` |
| `GQUT4` | 출고\|보호 | 보호대 부수 | `<th>보호</th>` | `Sobo46.DBGrid201.GQUT4` |
| `GQUT5` | 반품\|총부수 | 반품 합계 | `<th>반품총</th>` | `Sobo46.DBGrid201.GQUT5` |
| `GQUT6` | 반품\|시내 | 시내 반품 | `<th>반품시내</th>` | `Sobo46.DBGrid201.GQUT6` |
| `GQUT7` | 반품\|지방 | 지방 반품 | `<th>반품지방</th>` | `Sobo46.DBGrid201.GQUT7` |
| `NAME1` | 발송\|지역 | 지역명 | `<th>지역</th>` | `Sobo46.DBGrid201.NAME1` |
| `NAME2` | 발송\|화물명 | 화물명 | `<th>화물명</th>` | `Sobo46.DBGrid201.NAME2` |
| `GNAME` | 발송\|서점명 | 서점명 | `<th>서점명</th>` | `Sobo46.DBGrid201.GNAME` |
| `GCODE` | 발송\|코드 | 코드 | `<th>코드</th>` | `Sobo46.DBGrid201.GCODE` |
| `GSQUT` | 발송\|건수 | 건수 | `<th>건수</th>` | `Sobo46.DBGrid201.GSQUT` |
| `GSSUM` | 발송\|발송비 | 발송 금액 | `<th>발송비</th>` (SUM 푸터) | `Sobo46.DBGrid201.GSSUM` |
| `YESNO` | 상태 | 마감 플래그 | `<th>상태</th>` 배지 | `Sobo46.DBGrid201.YESNO` |

## 5. 67 합계 영역 매핑 (Edit201~Edit315 → `summary.sum*`)

레거시 (`Subu46.pas` L668~736) 가 `Edit{NNN}.Value := SGrid.Cells[k]` 로 채우는 67개 Edit 를 모던 응답 키 `summary.sumNN` 으로 1:1 흡수. 모던 미리보기 카드 좌측에 펼침. 핵심 5종은 큰 글자, 나머지는 `<details>` 토글:

| dfm Edit | T2_Ssub 컬럼 | 한글 라벨 (출력 시) | 분류 |
| --- | --- | --- | --- |
| Edit226 | Sum26 | **당월금액** | 핵심 |
| Edit227 | Sum27 | **세액** | 핵심 |
| Edit228 | Sum28 | **합계금액** | 핵심 |
| Edit310 | Gsusu | **입금액** | 핵심 |
| Edit315 | (반영합계) | **반영합계** | 핵심 |
| Edit201~Edit248 | Sum01~Sum48 | 일자별/항목별 합계 | 보조 |
| Edit261~Edit266 | Sum61~Sum66 | 보조 합계 | 보조 |
| Edit301~Edit309 | Sum51~Sum59 | 운임/세무 보조 | 보조 |
| Edit238/239/901 | Bigo1/Bigo2/Memo | 메모 | 보조 |

> 모든 Edit 는 `data-legacy-id="Sobo46.{EditID}"` 부착. dfm 의 `Visible=false` Edit 도 Phase 2 회귀 가드를 위해 hidden `<span>` 으로 보존(시각 표시는 안 함, ID 만 남김).

## 6. out-of-scope 위젯 (Phase 2 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 일괄 인쇄 (Bcode='완료' 루프) | `Button016`, `Button017` | Phase 2 단건 미리보기만, 일괄은 C7 후속 |
| Tong40.print_46_01/02 (Delphi Canvas) | (런타임) | 모던은 HTML+`window.print()` 로 흡수 (DEC-034) |
| Glyph 비트맵 / 폰트 (굴림) | 모든 위젯 | DEC-028 — 버린다 |
| Excel 저장 (Button010/011) | `DBGridSaveHtml` | C7 Reports 모듈로 이연 |
| Zoom_Int_01/Out_01 (확대/축소) | `Button008/009` | 브라우저 zoom 으로 흡수 |
| ColumnX1/X9 (열 너비 자동) | `Button012/013` | CSS 그리드 자동 |

## 7. Deltas — 모던 신설 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | `<button>인쇄</button>` (`window.print`) | 카드 우상단 | DEC-034 HTML preview only |
| 모던 신규 | `<a href=/settlement/billing>목록</a>` | 카드 좌상단 | 라우팅 보조 |
| 모던 신규 | "마감됨" 배지 | 카드 머리글 | DEC-031 시각화 |
| dfm out-of-scope | `Button016/017` 일괄 인쇄 | — | C7 이연 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 | 비고 |
| --- | --- | --- |
| `FormActivate` (L303) | (없음) | 모던 페이지는 URL 파라미터 `[billingKey]` 가 활성화 |
| `FormShow` (L310) | `useEffect(load)` | `print-data` API 호출 |
| `Button101Click` (L485) | (없음 — 목록 페이지로 이전) | Phase 1 `list_billing` 재사용 |
| `Button201Click` (L565) | `useEffect(load)` 의 일부 | `print-data` 응답에 67 합계 + 31 라인 모두 포함 |
| `Button016/017Click` | (Phase 2 미구현) | C7 후속 |
| `Button701/702Click` | (Phase 1 `/settlement/billing` 책임) | 마감은 Phase 1 |
| `T4_Sub61/62*` 이벤트 | (없음) | 응답 JSON 으로 흡수 |
| 인쇄 트리거 | `<button onClick={() => window.print()}>인쇄</button>` | 브라우저 인쇄 다이얼로그 |

## 9. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] §3·§4·§5 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재 (총 ~95개 — 31행 × 일부 + 67 sum + 헤더):
  - 핵심: `Sobo46.Header.{Gdate,Hcode,Hname,Bname}`, `Sobo46.Summary.{Sum26,Sum27,Sum28,Gsusu,Sum_Total}`
  - 표 헤더: `Sobo46.DBGrid201.{GDATE,GQUT1..7,NAME1,NAME2,GNAME,GCODE,GSQUT,GSSUM,YESNO}`
- [ ] §6 out-of-scope (일괄 인쇄·확대축소·Excel저장) 가 코드에 들어가지 않음
- [ ] DEC-034 — 미리보기 HTML 만 (PDF 라이브러리 임포트 없음)
- [ ] DEC-031 — 마감(`T2_Ssub.Yesno='1'`) 행이라도 미리보기는 200(읽기 전용 — 마감 가드는 쓰기 한정)
- [ ] DEC-028 §3 "버리는 정보" (픽셀 좌표·폰트·색상·Glyph) 가 코드에 없음

## 10. PDF 절 (C7 Phase 1 보강)

C7 (DEC-037 — WeasyPrint) 에서 본 페이지의 미리보기 HTML 을 **그대로** 입력으로 받아 PDF 1매를 산출.

| 항목 | 값 | 근거 |
| --- | --- | --- |
| 양식 코드 | `P1-A` (청구서) | `print_specs/c7_phase1.md` §1 |
| 용지/여백 | A4 세로 (`210mm 297mm`) / `12mm` | 동 §1 |
| 본문 표 | 15컬럼 (DBGrid201 그대로) | §3 본 노트 |
| 합계 | tfoot 4종 (Sum26/27/28/Gsusu/Sum_Total) | §5 |
| 마감 워터마크 | `T2_Ssub.Yesno='1'` 일 때 "마감" 반투명 | `print_specs/c7_phase1.md` §4 |
| 엔드포인트 | `GET /api/v1/settlement/billing/{billing_key}/print.pdf` | T5b |
| 빌더 | `settlement_print_service.render_invoice_pdf_html(billing_key)` (기존 `render_preview_html` 재사용) | T5c — SRP |
| FE 트리거 | 기존 미리보기 페이지 우상단 "PDF 다운로드" `<a download>` 추가 | T6a |
| 회귀 | `pytest -k test_invoice_pdf_signature/text/empty/closed_watermark` 4 케이스 | T4 |

> **변경 0**: 본 화면 자체 HTML/SQL/Backend 함수는 그대로. C7 추가는 신규 빌더 + 신규 엔드포인트 + FE 다운로드 버튼만.

## 11. 참조

- DEC-024: 페이지네이션 (목록 페이지 책임 — 본 페이지는 단건)
- DEC-028: dfm→html 산출물 영구 입력 동결
- DEC-031: 마감 가드 (Phase 1)
- **DEC-034** (T8 신설): C5 Phase 2 인쇄 = HTML 미리보기
- **DEC-037/038/039** (C7 T8): WeasyPrint / 라벨 1종 / .frf 참조용
- 화면 카드: [`analysis/screen_cards/c5_settlement.md`](../screen_cards/c5_settlement.md) §10 Phase 2 체크리스트
- contract: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) v1.2.0 (C7 PDF 절 포함)
- 인쇄 사양: [`analysis/print_specs/c7_phase1.md`](../print_specs/c7_phase1.md) §P1-A
- 핸들러 인덱스: [`analysis/handlers/c5_phase2.md`](../handlers/c5_phase2.md), [`analysis/handlers/c7_phase1.md`](../handlers/c7_phase1.md)
- 선례: [`Sobo45_billing.md`](Sobo45_billing.md) (Phase 1)
