# 레이아웃 매핑: Sobo54 (일별 입고내역서) — 모던 일별 리포트

DEC-028 의무 — DBGrid 컬럼·정렬·합계와 위젯 ID·TabOrder 를 1:1 보존.

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu54/Sobo54.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu54/Sobo54.html) + `Sobo54.form.json` + `Sobo54.tree.json`
- 화면 카드: [`analysis/screen_cards/Sobo54.md`](../screen_cards/Sobo54.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu54.dfm`](../../legacy_delphi_source/legacy_source/Subu54.dfm) — 40 위젯, DBGrid 2개

## 1. 영역 분할

| 영역 | dfm 컨테이너 | 모던 컴포넌트 | 역할 |
| --- | --- | --- | --- |
| 상단 검색 패널 | (Panel001 류) | `<section data-legacy-id="Panel001">` | 거래일자(시작/종료) 단일일자 + 출판사/입고처 |
| 좌측 그리드 | `DBGrid101` | `<DataGrid data-legacy-id="DBGrid101">` | 출판사 단위 집계 (11 컬럼) |
| 우측 그리드 | `DBGrid201` | `<DataGrid data-legacy-id="DBGrid201">` | 입고처 단위 집계 (10 컬럼) |
| 액션 버튼 | (Button 류) | `<Toolbar>` | 조회 / 출력 (인쇄는 DEC-004 — 1차는 화면만) |

## 2. DBGrid101 (출판사 단위 집계) 컬럼

| 순서 | FieldName | 한글 라벨 | 모던 column | 정렬·합계 |
| --- | --- | --- | --- | --- |
| 1 | `GDATE` | 거래일자 | `gdate` (date) | 좌, 그룹 키 |
| 2 | `HCODE` | 출판사코드 | `hcode` (string) | 좌, 그룹 키 |
| 3 | `HNAME` | 출판사명 | `hname` (string) | 좌 |
| 4 | `GCODE` | 코드 (입고처) | `gcode` | 좌 |
| 5 | `GNAME` | 입고처명 | `gname` | 좌 |
| 6 | `IDNUM` | No | `idnum` | 우 |
| 7 | `PUBUN` | 구분 | `pubun` | 중앙 |
| 8 | `BCODE` | 도서코드 | `bcode` | 좌 |
| 9 | `BNAME` | 도서명 | `bname` | 좌 |
| 10 | `GSQUT` | 수량 | `gsqut` (number) | 우, **합계** |
| 11 | `GDANG` | 단가 | `gdang` (number) | 우 |

## 3. DBGrid201 (입고처 단위 집계) 컬럼

| 순서 | FieldName | 한글 라벨 | 모던 column | 정렬·합계 |
| --- | --- | --- | --- | --- |
| 1 | `GCODE` | 코드 | `gcode` | 좌, 그룹 키 |
| 2 | `GNAME` | 입고처명 | `gname` | 좌 |
| 3 | `IDNUM` | No | `idnum` | 우 |
| 4 | `PUBUN` | 구분 | `pubun` | 중앙 |
| 5 | `BCODE` | 도서코드 | `bcode` | 좌 |
| 6 | `BNAME` | 도서명 | `bname` | 좌 |
| 7 | `GSQUT` | 수량 | `gsqut` | 우, **합계** |
| 8 | `GDANG` | 단가 | `gdang` | 우 |
| 9 | `GRAT1` | 비율 | `grat1` | 우 |
| 10 | `GSSUM` | 금액 | `gssum` | 우, **합계** |

> **합계** = `gsqut`, `gssum` footer 합계. 컬럼 순서·라벨 dfm 그대로 보존.

## 4. 이벤트 매핑

| dfm | 모던 핸들러 | 역할 |
| --- | --- | --- |
| `FormActivate` | useEffect mount | 오늘 일자 디폴트 |
| 검색 일자 변경 | `onChange` | 그리드 양쪽 동기 새로 fetch |
| 조회 버튼 | `onClick` | GET `/api/v1/inbound/reports/daily?gdate=...` |
| 출력 버튼 | `onClick` (Phase 2) | DEC-004 인쇄 — 1차는 disabled 또는 브라우저 인쇄 |

## 5. 회귀 가드 체크리스트

- [ ] DBGrid101 11 컬럼 + DBGrid201 10 컬럼 모두 모던 grid 정의에 존재.
- [ ] 합계 행: `gsqut`/`gssum` footer 합계 표시.
- [ ] `data-legacy-id="DBGrid101"`, `data-legacy-id="DBGrid201"` 부착.
- [ ] 검색 일자 변경 시 두 그리드 동시 새로고침.

## 6. 참조

- DEC-028 (dfm 영구 입력), DEC-004 (인쇄 1차 보류).
- contract: `migration/contracts/inbound_receipt.yaml` SQL-IN-3 (READ daily report).
