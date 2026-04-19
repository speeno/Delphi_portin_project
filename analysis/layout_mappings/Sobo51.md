# 레이아웃 매핑: Sobo51 (반품재고-변경) → 모던 `/returns/change`

DEC-028 의무. C4 Phase 1 신규 매핑 — 반품 워크플로우의 **3분기 중 3: 변경** (반품 재고 분류 변경 / 비품재고 이동).

## 0. 입력 산출물

- 본 폼: [`tools/.../Subu51/Sobo51.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu51/Sobo51.html) + `Sobo51.form.json` + `Sobo51.tree.json` + `Sobo51.pas_analysis.json`
- 변형 부재 — `Subu51` 단일
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu51.dfm`](../../legacy_delphi_source/legacy_source/Subu51.dfm)
- pas: [`legacy_delphi_source/legacy_source/Subu51.pas`](../../legacy_delphi_source/legacy_source/Subu51.pas)
- 모던 라우트(예정 — T6): `/returns/change/page.tsx`
- 계약: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) `endpoints[/returns/change/*]` (T3)

## 1. 의미 분기 — 반품 재고 분류 변경

레거시 `Sobo51` 은 반품 재고의 **분류를 변경** (예: 정품→비품, 비품→정품, 또는 수량 조정). Sobo24/25 와 위젯 골격 거의 동일하지만 **그리드 컬럼 의미가 다름** (대조재고/원장재고/변경수량 = 회계 검증 컬럼).

핵심 단서 — Button801/802 캡션 = **"비품재고"** (TO=4/5, Visible=false 기본). 즉 "비품재고로 이동" 액션 토글이 폼에 내장되어 있음.

## 2. dfm 영역 인벤토리 (tree.json) — Sobo24/25 와 동일 골격

| 영역 | dfm 컨테이너 | TabOrder | 핵심 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | Edit101/102 (일자), Edit107/108 (출판사), Panel101/104, DateEdit1/2 | `/returns/change/page.tsx` 검색 영역 |
| 중단 그리드 | `Panel002` (TFlatPanel) | 1 | DBGrid101 (7 컬럼 — **회계 검증 컬럼 포함**) | `<DataGrid>` |
| 진행 패널 | `Panel007` (TFlatPanel) | 2 | ProgressBar0/1, Panel008/009/010 | React `loading` 흡수 |
| 액션 코너 | `Label301~309` + `CornerButton1~9` | n/a | "조회/검색자료/상태" | 헤더 버튼 |
| 보조 액션 | Button700/dxButton1 ('검색') | TO=10/11 | TFlatButton + TdxButton | `<Button>검색`, `<Button>변경 처리` |
| **재분류 액션** | **Button801/802 ('비품재고')** | TO=4/5 (Visible=false) | TFlatButton x 2 | **`<Button>비품재고로 이동` PRIMARY** |

## 3. 상단 검색 패널 위젯 매핑 (Panel001) — Sobo24/25 동일

| dfm TO | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 거래일자 (from) | `<Input id="from" type="date">` | `Sobo51.Edit101` |
| 1 | `Edit102` | TFlatMaskEdit | 거래일자 (to) | `<Input id="to" type="date">` | `Sobo51.Edit102` |
| 4 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">기간</Label>` | `Sobo51.Panel101` |
| 5 | `Panel104` | TFlatPanel | "출판사명" 라벨 | `<Label htmlFor="hcode">출판사</Label>` | `Sobo51.Panel104` |
| 2 | `Edit107` (Visible=false) | TFlatEdit | 출판사코드 보조 | (CustomerSearchInput 통합) | `Sobo51.Edit107` |
| 3 | `Edit108` | TFlatEdit | 출판사명 | `<CustomerSearchInput id="hcode" type="publisher">` | `Sobo51.Edit108` |
| 8 | `DateEdit1` | TDateEdit | 캘린더 (from) | (HTML5 내장) | — |
| 9 | `DateEdit2` | TDateEdit | 캘린더 (to) | (HTML5 내장) | — |
| 11 | `dxButton1` | TdxButton ('검색') | 조회 실행 | `<Button onClick=load>조회` | `Sobo51.dxButton1` |
| 4 | `Button801` (Visible=false) | TFlatButton ('비품재고') | 비품재고로 이동 (행 단위) | (헤더 액션으로 흡수) | `Sobo51.Button801` |
| 5 | `Button802` (Visible=false) | TFlatButton ('비품재고') | 비품재고로 이동 (일괄) | `<Button onClick=onMoveToBipum>비품재고로 이동` | `Sobo51.Button802` |
| 6 | `Button101` (Visible=false) | TFlatButton | 조회 보조 | (dxButton1 통합) | — |
| 7 | `Button201` (Visible=false) | TFlatButton | 처리 보조 | (헤더 통합) | — |
| 10 | `Button700` | TFlatButton | 보조 액션 | **out-of-scope** | — |

## 4. 중단 그리드 매핑 (DBGrid101) — 회계 검증 컬럼 (Sobo24/25 와 다름)

| dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GDATE` | 거래일자 | 반품 라인 일자 | `<th>일자</th>` | `Sobo51.DBGrid101.GDATE` |
| `GCODE` | 코드 | **거래처코드** (Sobo24/25 의 BCODE 와 의미 다름!) | `<th>거래처</th>` | `Sobo51.DBGrid101.GCODE` |
| `GNAME` | 도서명 | 도서명 (의미 혼용 — form.json 한 번 더 확인 필요) | `<th>도서명</th>` | `Sobo51.DBGrid101.GNAME` |
| `GSSUM` | **대조재고** | 회계 검증 — 시스템 기록 재고 | `<th>대조재고</th>` (READ-ONLY) | `Sobo51.DBGrid101.GSSUM` |
| `GOSUM` | **원장재고** | 회계 검증 — 원장 기준 재고 | `<th>원장재고</th>` (READ-ONLY) | `Sobo51.DBGrid101.GOSUM` |
| `GBSUM` | **변경수량** | 변경할 수량 (입력) | `<th>변경수량</th>` (편집 가능) | `Sobo51.DBGrid101.GBSUM` |
| `GBIGO` | 적요 | 변경 사유 | `<th>적요</th>` (편집 가능 — 변경 사유) | `Sobo51.DBGrid101.GBIGO` |

> **회계 검증 패턴**: 대조재고(GSSUM) vs 원장재고(GOSUM) 차이가 있을 때 변경수량(GBSUM) 으로 조정. 모던에서는 GSSUM/GOSUM 가 다르면 행 강조 (warning) + GBSUM 입력 필수.

## 5. out-of-scope (Phase 1 미사용)

Sobo24/25 와 동일 + Button700.

## 6. Deltas — 모던 신설

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | 패스워드 게이트 모달 | `<AuditPasswordModal>` (Sobo40) | 재고 변경 작업 권한 인증 (DEC-029) |
| 모던 신규 | "대조재고 ≠ 원장재고" 행 강조 | DataGrid row className | 회계 불일치 시각적 알림 |
| 모던 신규 | 변경 사유 (GBIGO) 필수 입력 | 처리 버튼 비활성 게이트 | 감사 로그용 |
| 모던 신규 | "비품재고로 이동" 일괄 액션 | 헤더 버튼 (Button802 의미 흡수) | dfm 의 Visible=false 액션 노출 |
| 모던 신규 | DataGridPager | 그리드 푸터 | DEC-024 |

## 7. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → `load()` |
| `dxButton1.OnClick` ('검색') | `load()` → `returnsApi.searchChangeable({from, to, hcode})` |
| `DateEdit1/2.OnChange` / `Edit101/102.OnChange` | `setDateFrom/To` |
| `Edit107.OnChange` | `setHcode` |
| (DBGrid 행 선택 + GBSUM/GBIGO inline edit) | `setRows` (controlled) |
| `Button801Click` ('비품재고') | (행 단위 처리 — 모던은 일괄 처리로 통합) |
| `Button802Click` ('비품재고' 일괄) | `<AuditPasswordModal>` → `returnsApi.changeToBipum({rows, reasons})` |

## 8. 변형 차이

`legacy_source_root/Subu51` 단일 — variant 0건. contract `customer_variants.Sobo51` 에 "variant 0건" 단언 (T3).

## 9. 회귀 가드 체크리스트

- [ ] 본 노트의 부착 대상 `data-legacy-id` (~14개) 가 `/returns/change/page.tsx` DOM 에 존재:
  - 검색: `Sobo51.Edit101/102/107/108`, `Sobo51.Panel101/104`, `Sobo51.dxButton1`
  - 그리드: `Sobo51.DBGrid101.{GDATE,GCODE,GNAME,GSSUM,GOSUM,GBSUM,GBIGO}`
  - 액션: `Sobo51.Button801/802`
- [ ] §5 out-of-scope 항목이 코드에 없음
- [ ] **변경 처리 트랜잭션은 `<AuditPasswordModal>` (Sobo40) 통과 후에만 실행**
- [ ] **GBIGO (변경 사유) 가 비어있으면 처리 버튼 비활성**
- [ ] **GSSUM ≠ GOSUM 행은 warning 색상 강조**
- [ ] DBGrid 헤더 의미가 §4 표와 일치 (특히 "대조재고/원장재고" 의 회계 의미 — 라벨 변경 시 본 노트 동시 갱신)
- [ ] DEC-028 §3 "버리는 정보" 가 코드에 없음

## 10. 참조

- DEC-024: 페이지네이션 표준
- DEC-028: dfm→html 산출물 영구 입력 동결
- DEC-029 (T8 신설): 재고 변경 작업의 패스워드 게이트 정책
- 본 폼 메인: [`Sobo23.md`](Sobo23.md)
- 자매 폼 (재생/해체): [`Sobo24.md`](Sobo24.md), [`Sobo25.md`](Sobo25.md)
- 패스워드 모달: [`Sobo40.md`](Sobo40.md)
- contract: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) (T3)
- 회귀 테스트: [`test/test_c4_returns_phase1.py`](../../test/test_c4_returns_phase1.py) (T4)
