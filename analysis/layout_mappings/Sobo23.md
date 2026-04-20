# 레이아웃 매핑: Sobo23 (반품명세서 메인) → 모던 `/returns` (목록·상세·CRUD)

DEC-028 의무 — dfm→html 산출물 의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑. 픽셀 좌표·폰트·색상은 가져오지 않음. **본 노트는 C4 Phase 1 신규 매핑** — 모던 라우트는 T6 에서 신설.

## 0. 입력 산출물

- 본 폼: [`tools/.../legacy_source_root/Subu23/Sobo23.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu23/Sobo23.html) + `Sobo23.form.json` + `Sobo23.tree.json` + `Sobo23.pas_analysis.json`
- 변형 폴더 부재 — `Subu23` 단일 (보조 라인 입력 다이얼로그는 별도 `Subu23_1` — `Sobo23_1.md` 참조)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu23.dfm`](../../legacy_delphi_source/legacy_source/Subu23.dfm)
- pas 원본: [`legacy_delphi_source/legacy_source/Subu23.pas`](../../legacy_delphi_source/legacy_source/Subu23.pas) — Button001~024Click + Button101/201/301/401/501Click 다수 핸들러
- 모던 라우트(예정 — T6 신설):
  - `/returns/page.tsx` (목록 + 검색)
  - `/returns/new/page.tsx` (신규 등록)
  - `/returns/[returnKey]/page.tsx` (상세 + 메모 UPSERT, Sobo21 패턴 재사용)
  - `/returns/[returnKey]/edit/page.tsx` (수정)
- 계약: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) (T3 신설)

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유

레거시 `Sobo23` 은 **단일 MDI 자식 폼(top 검색 + mid DBGrid + bot 입력 패널 + 우측 액션 버튼)** 에서 반품 조회·라인 표시·신규/수정·메모(연락처·비고) 편집을 모달리스 동시 수행. 모던 C4 Phase 1 은:

- 검색·그리드 → `/returns/page.tsx` (DataGridPager 신설, Sobo21 패턴 재사용)
- 라인·메모 → `/returns/[returnKey]/page.tsx` (PATCH UPSERT, S1_Memo 동일 테이블)
- 신규 등록 → `/returns/new/page.tsx` (라인 그리드 = `ReturnLineGrid` — Sobo23_1 통합)
- 폐기·변경 분기 → 별도 라우트 (`/returns/dispose/*`, `/returns/change`) — Sobo24/25/51 별도 매핑

**핵심 결정** — Sobo23 의 라인 입력은 본래 모달리스 보조창 `Subu23_1` (반품명세서 라인 다이얼로그) 으로 분리되어 있음. 모던은 본 페이지 안에 `ReturnLineGrid` 로 흡수 (DEC-028: 픽셀 좌표 버리고 의미만 가져감).

## 2. dfm 영역 인벤토리 (tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수·핵심) | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색·메타 패널 | `Panel001` (TFlatPanel) | 0 | 라벨/Edit101~109 + Panel101~105 (거래일자/거래처코드/거래처명/출판사코드/전표구분) + Button101/201 (Visible=false 보조) | `/returns/page.tsx` 검색 영역 |
| 중단 그리드 | `Panel002` (TFlatPanel) | 1 | DBGrid101 + StBar101 | `/returns/page.tsx` `<DataGrid>` |
| 하단 라인·메모 입력 | `Panel003` (TFlatPanel) | 2 | Label103/104, Panel201~204, Edit201~208, StaticText1~4, Button801~803 | `/returns/[returnKey]/page.tsx` 메모 카드 (Sobo21 패턴) |
| 우측 액션 (라벨 코너) | `Label301~309` + `CornerButton1~9` | n/a | "조회/검색자료/참조/상태" — 메뉴 라벨 | 상세/목록 헤더 액션 버튼 (의미만 흡수) |
| 진행/상태 패널 | `Panel007` (TFlatPanel) | 3 | ProgressBar0/1, Panel008/009/010 ("레코드"/"검색진행") | **out-of-scope** — React `loading` boolean |
| 보조 패널 | `Panel401` | n/a | (인쇄 후속 컨테이너) | **out-of-scope** — DEC-017 |
| 데이터셋 | `DataSource1/2` | n/a | 2 | 백엔드/`returns_service` 로 흡수 |

## 3. 상단 검색 패널 위젯 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (`/returns/page.tsx`) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 (mask `!9999.!99.99;1; `) | `<Input id="from" type="date">` | `Sobo23.Edit101` |
| 8 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">시작일</Label>` | `Sobo23.Panel101` |
| 13 | `Panel104` | TFlatPanel | "거래처코드" 라벨 | `<Label htmlFor="hcode">거래처</Label>` | `Sobo23.Panel104` |
| 12 | `Panel105` | TFlatPanel | "거래처명" 라벨 | (응답 customer_name 으로 표시 — 별도 입력 없음) | `Sobo23.Panel105` (의미 흡수) |
| 11 | `Panel102` | TFlatPanel | "출판사코드" 라벨 | **out-of-scope (Phase 1)** | — |
| 10 | `Panel103` | TFlatPanel | "전표구분" 라벨 | **out-of-scope (Phase 1)** | — |
| (n/a) | `Edit102` | TFlatComboBox | 검색구분 콤보 | (모던: 단일 hcode 검색) | — |
| (n/a) | `Edit103/104/105` | TFlatEdit | 거래처코드/거래처명/(보조) | `<CustomerSearchInput id="hcode">` (C2 패턴) | `Sobo23.Edit104` |
| (n/a) | `Edit107/108` | TFlatEdit | 출판사코드/명 | **out-of-scope** | — |
| (n/a) | `Edit109` | TFlatEdit | 보조 | **out-of-scope** | — |
| 14 | `Button101` | TFlatButton (Visible=false) | 조회(보조) | (`Button201` 동일 의미 — `dxButton1` 패턴) | — |
| 15 | `Button201` | TFlatButton (Visible=false) | 신규 등록 | `<Link href="/returns/new">신규` | `Sobo23.Button201` |

> **TabOrder 보존**: 모던 검색 영역의 키보드 흐름 = 거래처 → 시작일 → 종료일 → 조회. dfm TabOrder 0(Edit101) → 8(Panel101) → 13(Panel104) 순은 라벨 `htmlFor` 로 묶이며 의미 보존.

## 4. 중단 그리드 매핑 (DBGrid101) — Sobo23.form.json 컬럼

dfm `DBGrid101` 라인 단위 표시 (Sobo23 내부 컬럼 구성은 form.json 기반, **Sobo21 의 9컬럼과 동일 의미**):

| dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 (목록) | data-legacy-id |
| --- | --- | --- | --- | --- |
| `PUBUN` | 품분 | 품목 구분 | (목록 미노출 — 상세) | — |
| `BCODE` | 도서코드 | 키 | (상세 라인) | — |
| `BNAME` | 도서명 | 명칭 | (상세 라인) | — |
| `GSQUT` | 수량 | 라인 수량 | `<th>수량합</th>` (SUM) | `Sobo23.DBGrid101.GSQUT` |
| `GDANG` | 단가 | 단가 | (상세 라인 — Phase 1 미노출) | — |
| `GRAT1` | 할인 | 할인율 | (상세 라인 — Phase 1 미노출) | — |
| `GSSUM` | 금액 | 라인 금액 | `<th>금액합</th>` (SUM) | `Sobo23.DBGrid101.GSSUM` |
| `GBIGO` | 비고 | 라인 메모 | (상세 lineColumns) | `Sobo23.DBGrid101.GBIGO` |
| `YESNO` | 상태 | 정상/취소(=2) | `<th>상태</th>` (배지) — DEC-012 soft cancel | `Sobo23.DBGrid101.YESNO` |

모던 신규 컬럼 (§7 deltas): `<th>일자</th>`, `<th>거래처</th>`, `<th>전표</th>`, `<th>라인</th>`.

> 의미 차이: dfm = "한 거래의 모든 라인 평면 표시", 모던 목록 = "거래 1건당 1행 (group by gdate/hcode/jubun) + 상세 라우트로 라인 노출".

## 5. 하단 입력·메모 패널 매핑 (Panel003 → 상세 페이지)

dfm Panel003 의 입력 위젯 → 모던 `/returns/[returnKey]/page.tsx` 메모 카드 (Sobo21 의 S1_Memo UPSERT 패턴 재사용):

| dfm 위젯 ID | 클래스 | dfm 라벨/용도 | S1_Memo 컬럼 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| `Panel201` | TFlatPanel | "전표번호" 라벨 | (key — `return_key.jubun`) | 헤더 텍스트 | `Sobo23.Panel201` |
| `Panel202` | TFlatPanel | "전화번호" 라벨 | Gtel1 | `<Label htmlFor="gtel1">전화1</Label>` | `Sobo23.Panel202` |
| `Panel204` | TFlatPanel | "주소" 라벨 | Gpost | `<Label htmlFor="gpost">우편번호</Label>` | `Sobo23.Panel204` |
| `Panel203` | TFlatPanel | "메모" 라벨 | Gbigo | `<Label htmlFor="gbigo">비고</Label>` | `Sobo23.Panel203` |
| `Edit201` | TFlatEdit | (전표번호 표시) | — | 헤더 텍스트 | (Panel201 흡수) |
| `Edit202/203` | TFlatEdit | 전화번호 1/2 | Gtel1/Gtel2 | `<Input id="gtel1">`, `<Input id="gtel2">` | `Sobo23.Edit202`, `Sobo23.Edit203` |
| `Edit205` | TFlatEdit | 주소 | Gpost | `<Input id="gpost">` | `Sobo23.Edit205` |
| `Edit206` | TFlatEdit | 메모 | Gbigo | `<textarea id="gbigo">` | `Sobo23.Edit206` |
| `Edit207` | TFlatEdit | 소비고 | Sbigo | `<textarea id="sbigo">` | `Sobo23.Edit207` |
| `Edit204/208` | TFlatEdit | 보조 | — | **out-of-scope** | — |
| `StaticText1~4` | TStaticText | 안내 텍스트 | — | (label 텍스트 흡수) | — |
| `Button801` | TFlatButton ('저장') | 저장 (UPDATE) | — | `<Button onClick=onSaveMemo>메모 저장` | `Sobo23.Button801` |
| `Button802/803` | TFlatButton | 보조 | — | **out-of-scope** | — |

## 6. out-of-scope 위젯 (Phase 1 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 검색 | Edit102 (combo), Edit106 (combo, 전표구분), Edit107/108 (출판사 검색), Edit109 (보조) | Phase 1 = hcode/일자 단일 검색 |
| 진행 | Panel007 / ProgressBar0/1 / Panel008~010 | React `loading` boolean 흡수 |
| 인쇄 | Button701/702/901, Panel401 | DEC-017 — C7 인쇄 후속 |
| 라인 보조 | Edit204/208, Button802/803 | Phase 1 메모 핵심 필드만 |
| 라벨 코너 | Label301~309, CornerButton1~9 | 메뉴 진입점 — 모던은 라우트 분리로 흡수 |

## 7. Deltas — 모던 신설 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | 종료일 입력 | `/returns/page.tsx` | dfm 단일 일자 → 범위 검색 (DEC-019) |
| 모던 신규 | DataGridPager | `/returns/page.tsx` | dfm 모달리스 → 페이지네이션 (DEC-024) |
| 모던 신규 | 상세 라우트 분리 | `/returns/[returnKey]/page.tsx` | dfm 단일 화면 → list/detail 분리 |
| 모던 신규 | "취소 포함" 토글 | `/returns/page.tsx` | DEC-012 soft cancel 정책 — 백엔드 `include_cancelled` 와 짝 |
| 모던 신규 | 신규 등록 라우트 | `/returns/new/page.tsx` | C2/C3 패턴 — `ReturnLineGrid` |
| 모던 신규 | "메모 신규/수정" 안내 + UPSERT action 메시지 | 상세 카드 | C6 패턴 재사용 |
| dfm out-of-scope | 라인 단가/할인 컬럼 (GDANG/GRAT1) | — | Phase 1 라인 합계만 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 | 비고 |
| --- | --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → 자동 사이즈 → `load(0, recommended)` | C6 패턴 재사용 |
| `FormClose` | `<Button variant="ghost" onClick=router.back>목록` | |
| `Button001~024Click` | (메뉴 액션) | 라벨 코너 영역 — 모던은 라우트 분리로 흡수 |
| `Button101Click` / `Button501Click` | `load()` (조회) | dfm 두 버튼 동일 핸들러 |
| `Button201Click` | `<Link href="/returns/new">신규` | 신규 등록 진입 |
| `Button801Click` (메모 저장) | `onSaveMemo` → `returnsApi.upsertMemo` | UPDATE→INSERT 분기는 백엔드 UPSERT |
| `Edit101Change` | `setDateFrom` | |
| `Edit101~114KeyDown` | (autotab/autocomplete) | 모던은 `<CustomerSearchInput>` 의 keyDown 흡수 |
| `DBGrid101TitleClick` | (정렬 — Phase 2 후속) | |
| `DataSource1/2DataChange` | (자동 — React state 갱신) | |

## 9. 변형 차이 (`Sobo23` 본 vs variant)

`legacy_source_root/Subu23` 단일 폴더만 존재 — **본 폼에 variant 없음**. 단, 라인 다이얼로그 `Subu23_1` 의 chul_05/chul_08 변형은 `Sobo23_1.md` 참조.

→ 본 노트 차원의 UI 차이 없음. contract `customer_variants` 에 "Sobo23 variant 0건" 단언 기록 (T3).

## 10. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] 본 노트 §3·§4·§5 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재 (총 ~20개):
  - 목록: `Sobo23.Edit101`, `Sobo23.Panel101`, `Sobo23.Panel104`, `Sobo23.Edit104`, `Sobo23.DBGrid101.GSQUT/GSSUM/GBIGO/YESNO`, `Sobo23.Button201`
  - 상세: `Sobo23.Panel201/202/203/204/105`, `Sobo23.Edit202/203/205/206/207`, `Sobo23.Button801`
- [ ] §6 out-of-scope 항목이 코드에 우연히 들어가지 않았는지 (예: 출판사 검색 input)
- [ ] DBGrid 헤더 의미가 §4 표와 일치 (라벨 변경 시 본 노트 동시 갱신)
- [ ] 메모 저장 흐름이 PATCH UPSERT (action: inserted/updated) 의미 보존 (Sobo21 패턴)
- [ ] DEC-012 soft cancel — 취소된 반품(`yesno=2`) 은 기본 숨김, 토글로 표시
- [ ] DEC-028 §3 "버리는 정보" (픽셀 left/top/width/height/Color) 가 코드에 없음

## 11. PDF 절 (C7 Phase 1 보강 — 반품 영수증)

DEC-017 (인쇄 트리거 → C7) 의 종결.

| 항목 | 값 | 근거 |
| --- | --- | --- |
| 양식 코드 | `P1-D` (반품 영수증) | `print_specs/c7_phase1.md` §1 |
| 용지/여백 | A4 세로 (`210mm 297mm`) / `12mm` | 동 §1 |
| 헤더 | 거래처명 + 반품일자 + 전표번호 | §3 본 노트 (`Edit101`/`Panel101`) |
| 본문 표 | 도서코드/도서명/구분/수량/단가/할인/금액/비고/상태 (9컬럼) | DBGrid101 + 비고/yesno 추가 |
| 합계 | tfoot 2종 (수량합/금액합 — `GSQUT`/`GSSUM`) | DBGrid101 footer |
| 취소행 표시 | `yesno=2` 행에 `text-decoration: line-through` + 회색 | DEC-012 soft cancel 시각화 |
| 엔드포인트 | `GET /api/v1/print/return-receipt/{return_key}.pdf` (T5b — `routers/print.py`) | T5b |
| 빌더 | `returns_service.render_return_receipt_html(return_key)` (기존 `get_return_detail` 재사용) | T5c — SRP, 신규 SQL 0 |
| 데이터 출처 | 기존 SQL-RT-3~5 — 신규 SQL 없음 | C4 자산 재사용 |
| FE 진입점 | 신규 `/print/returns/[returnKey]/page.tsx` (T6b) — 미리보기 + PDF 다운로드 |  |
| FE 트리거 | Sobo23 행 액션 "영수증" 버튼 → 신규 페이지 | T6b |
| 회귀 | `pytest -k test_return_receipt_pdf_signature/text/cancelled_strike` 3 케이스 | T4 |

> **DEC-017 종결**: C4 의 SQL/서비스는 그대로, 빌더 + 신규 페이지/엔드포인트만.

### 11.1 Phase 2-α 거래처별 변형 표 (4 변형)

`Report_2_13-{1,2,3,5}.frf` 4 변형 (※ 4 누락 — 운영 SME 확인 필요) 의 시각 차이를 단일 모던 빌더 `render_return_receipt_html(detail, *, variant: str = "base")` 의 데이터 주도 분기로 흡수한다.

| variant | .frf 정본 | 헤더 로고/회사명 차이 | 컬럼 구성 차이 | 합계 행 차이 | 우선순위 |
| --- | --- | --- | --- | --- | --- |
| `base` | `Report_2_13.frf` | 기본 (반품 영수증 표준) | 6 컬럼 (Phase 1 기준) | 수량합/금액합 | Phase 1 (변경 없음) |
| `v1` | `Report_2_13-1.frf` | 거래처 1 — 헤더 텍스트 변형 | 동일 | 동일 | Phase 2-α |
| `v2` | `Report_2_13-2.frf` | 거래처 2 — 헤더 텍스트 변형 | 동일 | 동일 | Phase 2-α |
| `v3` | `Report_2_13-3.frf` | 거래처 3 — 헤더 텍스트 변형 | 동일 | 동일 | Phase 2-α |
| `v5` | `Report_2_13-5.frf` | 거래처 5 — 헤더 텍스트 변형 (`-4` 결번) | 동일 | 동일 | Phase 2-α |

> **`-4` 결번 추정**: 거래처 4 가 폐업/해지 또는 `-3` 양식 공유 가능성. 운영 SME 확인 후 contract 의 `customer_variants` 에 `note: "거래처 4 결번 — `-3` 공유 또는 미사용"` 기록 필요. variant 매핑 시 `v4` 는 미정의 키로 유지.
>
> **단일 모던 컴포넌트 + 데이터 주도 분기 (DEC-019/028 룰 7)**: Sobo27 과 동일 정책. `?variant=` 쿼리 수동 지정만 Phase 2-α 범위.
>
> **base variant byte-identical 보장**: variant 미지정 시 또는 `variant=base` 시 Phase 1 산출물과 byte 동일.

## 12. 참조

- DEC-012: 취소는 soft delete (yesno=2)
- DEC-017: 인쇄 트리거 → C7 (본 노트에서 종결)
- DEC-019: customer_variants 정책 (variant 0건 단언)
- DEC-024: 페이지네이션 표준 (DataGridPager)
- DEC-028: dfm→html 산출물 영구 입력 동결
- **DEC-037/038/039** (C7 T8): WeasyPrint / 라벨 1종 / .frf 참조용
- 화면 카드: [`analysis/screen_cards/Sobo23.md`](../screen_cards/Sobo23.md) (있으면)
- contract: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) (T3), [`migration/contracts/print_invoice.yaml`](../../migration/contracts/print_invoice.yaml) v1.0.0 (C7)
- 인쇄 사양: [`analysis/print_specs/c7_phase1.md`](../print_specs/c7_phase1.md) §P1-D
- 보조 라인 입력: [`Sobo23_1.md`](Sobo23_1.md)
- 회귀 테스트: [`test/test_c4_returns_phase1.py`](../../test/test_c4_returns_phase1.py) (T4), [`test/test_c7_print_phase1.py`](../../test/test_c7_print_phase1.py)
- 선례: `Sobo21.md` (S1_Memo UPSERT, list/detail 분리), `Sobo22.md` (입고 — 같은 거래 메인 패턴)
