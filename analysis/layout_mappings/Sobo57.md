# 레이아웃 매핑: Sobo57 (기간별 입고내역서) — 모던 기간 리포트

DEC-028 의무 — DBGrid 컬럼·정렬·합계와 위젯 ID 를 1:1 보존.

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu57/Sobo57.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu57/Sobo57.html) + `Sobo57.form.json` + `Sobo57.tree.json`
- 화면 카드: [`analysis/screen_cards/Sobo57.md`](../screen_cards/Sobo57.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu57.dfm`](../../legacy_delphi_source/legacy_source/Subu57.dfm) — 41 위젯, DBGrid 2개

## 1. 영역 분할

| 영역 | dfm 컨테이너 | 모던 컴포넌트 | 역할 |
| --- | --- | --- | --- |
| 상단 검색 패널 | (Panel001 류) | `<section data-legacy-id="Panel001">` | **시작일~종료일** + 출판사·입고처 필터 |
| 좌측 그리드 | `DBGrid101` | `<DataGrid data-legacy-id="DBGrid101">` | 출판사 단위 기간 집계 (11 컬럼) |
| 우측 그리드 | `DBGrid201` | `<DataGrid data-legacy-id="DBGrid201">` | 입고처 단위 기간 집계 (10 컬럼) |
| 액션 버튼 | (Button 류) | `<Toolbar>` | 조회 / 출력 (DEC-004 — 1차는 화면만) |

## 2. DBGrid101 (출판사 단위 기간 집계) 컬럼

| 순서 | FieldName | 한글 라벨 | 모던 column | 정렬·합계 |
| --- | --- | --- | --- | --- |
| 1 | `HCODE` | 출판사코드 | `hcode` | 좌, 그룹 키 |
| 2 | `HNAME` | 출판사명 | `hname` | 좌 |
| 3 | `GDATE` | 거래일자 | `gdate` (date) | 좌 |
| 4 | `GCODE` | 코드 | `gcode` | 좌 |
| 5 | `GNAME` | 입고처명 | `gname` | 좌 |
| 6 | `IDNUM` | No | `idnum` | 우 |
| 7 | `PUBUN` | 구분 | `pubun` | 중앙 |
| 8 | `BCODE` | 도서코드 | `bcode` | 좌 |
| 9 | `BNAME` | 도서명 | `bname` | 좌 |
| 10 | `GSQUT` | 수량 | `gsqut` (number) | 우, **합계** |
| 11 | `GDANG` | 단가 | `gdang` (number) | 우 |

## 3. DBGrid201 (입고처 단위 기간 집계) 컬럼

| 순서 | FieldName | 한글 라벨 | 모던 column | 정렬·합계 |
| --- | --- | --- | --- | --- |
| 1 | `GDATE` | 거래일자 | `gdate` | 좌, 그룹 키 |
| 2 | `GCODE` | 코드 | `gcode` | 좌 |
| 3 | `GNAME` | 입고처명 | `gname` | 좌 |
| 4 | `IDNUM` | No | `idnum` | 우 |
| 5 | `PUBUN` | 구분 | `pubun` | 중앙 |
| 6 | `BCODE` | 도서코드 | `bcode` | 좌 |
| 7 | `BNAME` | 도서명 | `bname` | 좌 |
| 8 | `GSQUT` | 수량 | `gsqut` | 우, **합계** |
| 9 | `GDANG` | 단가 | `gdang` | 우 |
| 10 | `GRAT1` | 비율 | `grat1` | 우 |
| 11 | `GSSUM` | 금액 | `gssum` | 우, **합계** |

> Sobo54 와 동일 컬럼 패턴이지만 그룹 키가 출판사(HCODE)+거래일자(GDATE) 또는 거래일자(GDATE) — Sobo54 (일별) 와 차이는 **검색 시작일~종료일 범위** 뿐. SQL 은 BETWEEN 으로 변경.

## 4. 이벤트 매핑

| dfm | 모던 핸들러 | 역할 |
| --- | --- | --- |
| `FormActivate` | useEffect mount | 시작일=이번달1일, 종료일=오늘 디폴트 |
| 시작/종료 일자 변경 | `onChange` | 그리드 양쪽 동기 새로 fetch |
| 조회 버튼 | `onClick` | GET `/api/v1/inbound/reports/period?from=...&to=...` |

## 5. 회귀 가드 체크리스트

- [ ] DBGrid101 11 컬럼 + DBGrid201 11 컬럼(합계 포함) 모두 모던 grid 정의.
- [ ] 합계 행: `gsqut`/`gssum`.
- [ ] `data-legacy-id` 부착.
- [ ] 시작/종료 일자 양방향 검증 (시작 ≤ 종료).

## 6. 참조

- DEC-028, DEC-004.
- contract: `migration/contracts/inbound_receipt.yaml` SQL-IN-4 (READ period report).
