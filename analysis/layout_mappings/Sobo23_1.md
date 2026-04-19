# 레이아웃 매핑: Sobo23_1 (반품 라인 다이얼로그) → 모던 `ReturnLineGrid` (+ chul_08 자료불러오기)

DEC-028 의무. **본 노트는 3 변형의 결정적 차이 기록** — 본 + chul_05 + chul_08 모두 동일 파일명 `Subu23_1.dfm` 이지만 chul_08 은 의미 자체가 다른 폼임.

## 0. 입력 산출물 (3 변형 모두 변환 완료)

| 변형 | 출력 폴더 | 폼 제목 | dfm 크기 | 의미 |
| --- | --- | --- | --- | --- |
| 본 (book_kb) | [`Subu23_1/`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu23_1/) | "반품명세서" | 38,674 B | Sobo23 의 라인 입력 보조 다이얼로그 |
| chul_05 (한강북-중앙라인) | [`Subu23_1_chul05/`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu23_1_chul05/) | "반품명세서" | 37,842 B | 본과 미세 차이 (위젯 트리 1:1 동일) |
| chul_08 (임프린트) | [`Subu23_1_chul08/`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu23_1_chul08/) | **"자료불러오기"** | 13,818 B | ⚠️ **완전히 다른 폼** — 데이터 임포트 다이얼로그 |

원 dfm 위치 (변형별 트리):

- 본: `WeLove_FTP/도서유통-New/도서유통/book_kb(반품과)/Subu23_1.dfm`
- chul_05: `WeLove_FTP/도서유통-New/도서유통/chul_05(한강북-중앙라인)/Subu23_1.dfm`
- chul_08: `WeLove_FTP/도서유통-출판/MySQL/도서유통/chul_08(임프린트)/Subu23_1.dfm`

모던 라우트(예정 — T6):
- 본/chul_05 → `ReturnLineGrid` 컴포넌트 (`/returns/new` + `/returns/[returnKey]/edit` 내부)
- chul_08 → `DataImportModal` 컴포넌트 + 트리거 버튼 (`/returns/page.tsx` 우상단)

## 1. 의미적 분기 — 같은 파일명, 다른 폼

`Subu23_1.dfm` 이라는 같은 파일명이지만:

- **본/chul_05** = "반품명세서" 라인 입력 다이얼로그 (Sobo23 의 보조 모달리스 창). 거래처별 반품 라인 수기 입력.
- **chul_08** = "자료불러오기" — 임프린트 지점 전용. 외부 자료 (CSV/엑셀/타 시스템) 를 일괄 임포트해 반품으로 등록하는 데이터 임포트 다이얼로그.

DEC-019 (customer_variants 통합 정책) 위배 케이스 — 같은 파일명이지만 의미가 달라 단순 diff 항목으로 처리 불가. **별도 모던 컴포넌트 2개로 분리** (DEC-029 신설 권고 — T8).

## 2. 본/chul_05 — Sobo23_1 라인 입력 다이얼로그

### 2.1 영역 인벤토리 (tree.json)

| 영역 | dfm 컨테이너 | TabOrder | 핵심 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 메타 헤더 패널 | `Panel001` (TFlatPanel) | 2 | Panel105 ("거래처명"), Panel103 ("전표구분"), Edit102 (combo), Label100 ("지점명") | `ReturnLineGrid` 헤더 — 라인 그리드 위 메타 표시 |
| 라인 그리드 | (Sobo23 본 폼의 DBGrid101 과 통합) | n/a | (다이얼로그 형태로 메인 그리드 공유) | `<DataGrid>` editable mode |
| 액션 버튼 | Button101 (TO=8, Visible=false) / Button201 (TO=9, Visible=false) | n/a | 저장/취소 보조 | 모던: `<Button>저장`, `<Button variant=ghost>취소` |

> 본 폼의 라인 그리드는 **별도 DBGrid 가 아니라 Sobo23 의 DBGrid101 을 공유** — `Sobo23.md` 의 §4 그리드 매핑이 그대로 적용됨.

### 2.2 위젯 매핑

| dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `Sobo23_1.Panel105` | TFlatPanel | "거래처명" 라벨 | `<Label>거래처</Label>` (그리드 헤더 위) | `Sobo23_1.Panel105` |
| `Sobo23_1.Panel103` | TFlatPanel | "전표구분" 라벨 | `<Label>전표</Label>` | `Sobo23_1.Panel103` |
| `Sobo23_1.Label100` | TmyLabel3d (Visible=false) | "지점명" 라벨 (가변) | (모던: `userContext.gjisa` 표시) | `Sobo23_1.Label100` |
| `Sobo23_1.Edit102` | TFlatComboBox | 전표구분 콤보 | `<Select id="jubun_kind">` | `Sobo23_1.Edit102` |
| `Sobo23_1.Button101` | TFlatButton (Visible=false) | 저장 보조 | (의미 흡수 — 모던 `<Button>저장`) | — |
| `Sobo23_1.Button201` | TFlatButton (Visible=false) | 취소 보조 | (의미 흡수 — 모던 `<Button variant=ghost>취소`) | — |

### 2.3 chul_05 변형 차이

위젯 트리 **1:1 동일** (위 §2.2 표 그대로 적용). 차이는 form.json 의 picksel 좌표·DataSource 바인딩 SQL 의 지점 코드 정도 (DEC-028 §3 "버리는 정보" 범주).

→ contract `customer_variants.chul_05` 에 "위젯 트리 동일, SQL 바인딩 chul_05 지점 코드만 차이 — 코드 분기 없음" 단언 기록 (T3).

## 3. chul_08 — Sobo23_1 자료불러오기 다이얼로그

### 3.1 영역 인벤토리 (tree.json — `Subu23_1_chul08/Sobo23_1.tree.json`)

| 영역 | dfm 컨테이너 | TabOrder | 핵심 위젯 | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 패널 | `Panel001` (TFlatPanel) | 0 | Panel101 ("거래처구분"), Edit101 (TFlatComboBox), Label100~309 | `DataImportModal` 상단 폼 |
| 중단 그리드 | `Panel002` (TFlatPanel) | 1 | DBGrid101 (10 컬럼 — JUBUN/GCODE/GNAME/BCODE/BNAME/GSQUT/GDANG/GSSUM/CODE1/CODE2) | `DataImportModal` 미리보기 그리드 |
| 진행 패널 | `Panel007` (TFlatPanel) | 2 | ProgressBar0/1, Panel008/009/010 | React `loading` boolean 흡수 |
| 액션 | dxButton1 ('불러오기') | TO=1 | TdxButton | `<Button>불러오기` (PRIMARY) |
| 보조 | Button101 (Visible=false) | TO=0 | TFlatButton | (의미 흡수 — 모던 `<Button>닫기`) |

### 3.2 DBGrid101 컬럼 매핑 — 임포트 미리보기

| dfm FieldName | 한글 컬럼 | 데이터 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `JUBUN` | 거래일자 | 외부 자료의 거래일자 | `<th>일자</th>` | `Sobo23_1_import.DBGrid101.JUBUN` |
| `GCODE` | 코드 | 거래처코드 | `<th>거래처</th>` | `Sobo23_1_import.DBGrid101.GCODE` |
| `GNAME` | 거래처명 | (조인 결과) | (GCODE 와 통합 표시) | `Sobo23_1_import.DBGrid101.GNAME` |
| `BCODE` | 도서코드 | 키 | `<th>도서</th>` | `Sobo23_1_import.DBGrid101.BCODE` |
| `BNAME` | 도서명 | (조인 결과) | (BCODE 와 통합 표시) | `Sobo23_1_import.DBGrid101.BNAME` |
| `GSQUT` | 수량 | 라인 수량 | `<th>수량</th>` | `Sobo23_1_import.DBGrid101.GSQUT` |
| `GDANG` | 단가 | 단가 | `<th>단가</th>` | `Sobo23_1_import.DBGrid101.GDANG` |
| `GSSUM` | 금액 | 라인 금액 | `<th>금액</th>` | `Sobo23_1_import.DBGrid101.GSSUM` |
| `CODE1` | 불능 | 임포트 불능 사유 (배지) | `<th>불능</th>` | `Sobo23_1_import.DBGrid101.CODE1` |
| `CODE2` | 완료 | 임포트 완료 표시 (체크) | `<th>완료</th>` | `Sobo23_1_import.DBGrid101.CODE2` |

> **CODE1/CODE2** 는 임포트 결과 라인별 상태 (불능 사유 / 완료 여부) — 모던 `DataImportModal` 의 미리보기 행 상태 표시에 그대로 흡수.

### 3.3 위젯 매핑

| dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `Sobo23_1_import.Panel101` | TFlatPanel | "거래처구분" 라벨 | `<Label htmlFor="customer_kind">거래처 구분</Label>` | `Sobo23_1_import.Panel101` |
| `Sobo23_1_import.Edit101` | TFlatComboBox | 거래처구분 콤보 | `<Select id="customer_kind">` | `Sobo23_1_import.Edit101` |
| `Sobo23_1_import.dxButton1` | TdxButton ('불러오기') | 임포트 실행 | `<Button onClick=onImport>불러오기` | `Sobo23_1_import.dxButton1` |
| `Sobo23_1_import.Label301~309` | TmyLabel3d | "조회/검색자료/상태" 라벨 코너 | (모던: 진행 텍스트 흡수) | — |

> 모던 컴포넌트명에 `_import` suffix 부착 — 본 폼과 충돌 회피. data-legacy-id 충돌 정책 (DEC-029 후속 — T8).

## 4. 이벤트 매핑

### 4.1 본/chul_05 (Sobo23_1)

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `FormShow` | `useEffect` mount → 라인 그리드 초기화 |
| `Edit102.OnChange` | `setJubunKind` |
| `Button101Click` (저장 보조) | `onSaveLine` → `returnsApi.upsertLine` |

### 4.2 chul_08 (자료불러오기)

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `dxButton1.OnClick` ('불러오기') | `onImport` → `returnsApi.importExternal({customer_kind})` → 미리보기 그리드 갱신 |
| `Edit101.OnChange` | `setCustomerKind` |
| (자동) DataSource binding | `useEffect` 폴링 — 진행률 업데이트 |

## 5. out-of-scope (Phase 1 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 진행 (본/chul_05) | (없음 — 본 폼은 진행 패널 자체 없음) | — |
| 진행 (chul_08) | Panel007 / ProgressBar0/1 | React `loading` 흡수 |
| 코너 라벨 | Label301~309, CornerButton1~9 (chul_08) | 모던 흡수 |

## 6. Deltas — 모던 신설

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | 라인 그리드 inline edit | `ReturnLineGrid` | dfm 모달리스 → 모던 inline (Sobo23 페이지 내 통합) |
| 모던 신규 | 임포트 결과 통계 | `DataImportModal` 푸터 | "성공 N건 / 불능 M건" 요약 |
| 모던 신규 | 임포트 후 자동 등록 옵션 | `DataImportModal` 토글 | 미리보기 → 일괄 등록 (DEC-029 후속) |
| dfm 흡수 | 본 폼의 별도 다이얼로그 | — | 모던은 페이지 내부 inline (UX 개선) |

## 7. 회귀 가드 체크리스트

- [ ] **본/chul_05** 의 `data-legacy-id` (~6개) 가 `ReturnLineGrid` DOM 에 존재: `Sobo23_1.Panel105`, `Sobo23_1.Panel103`, `Sobo23_1.Label100`, `Sobo23_1.Edit102`
- [ ] **chul_08** 의 `data-legacy-id` (~12개) 가 `DataImportModal` DOM 에 존재: `Sobo23_1_import.Panel101/Edit101/dxButton1`, `Sobo23_1_import.DBGrid101.{JUBUN,GCODE,GNAME,BCODE,BNAME,GSQUT,GDANG,GSSUM,CODE1,CODE2}`
- [ ] chul_05 변형 차이는 `customer_variants` 에만 기록, 컴포넌트 코드에 if/switch 분기 0건
- [ ] chul_08 은 별도 모던 컴포넌트로 분리됨 (`DataImportModal` ≠ `ReturnLineGrid`)
- [ ] DBGrid101 컬럼 10 개의 한글 헤더 (chul_08) 가 §3.2 표와 일치

## 8. 참조

- DEC-019: customer_variants 통합 정책 (chul_05 = 동일 위젯, chul_08 = 의미 분기 — 별도 컴포넌트)
- DEC-028: dfm→html 산출물 영구 입력 동결 (본 노트 = 3 변형 결정적 차이)
- DEC-029 (T8 신설 예정): "동일 파일명, 의미 다른 폼" 의 `data-legacy-id` 네임스페이스 분리 정책
- 본 폼: [`Sobo23.md`](Sobo23.md)
- contract: [`migration/contracts/return_receipt.yaml`](../../migration/contracts/return_receipt.yaml) `customer_variants` (T3)
- 회귀 테스트: [`test/test_c4_returns_phase1.py`](../../test/test_c4_returns_phase1.py) (T4)
- 선례: 동일 파일명 의미 분기 케이스는 본 노트가 첫 선례 — DEC-029 의 모범 사례로 등록 예정 (T8)
