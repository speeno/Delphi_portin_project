# 레이아웃 매핑: Sobo28 (출고택배관리) — NAV-16 `/shipping/courier`

DEC-028 의무 — dfm→html 산출물 기준 영역·위젯 ID·**TabOrder**·DBGrid·이벤트 1:1. 픽셀·폰트·색상 미사용.

## 0. 입력 산출물

- [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu28/Sobo28.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu28/Sobo28.html)
- `Sobo28.form.json`, `Sobo28.tree.json`, `Sobo28.pas_analysis.json`
- 원본: [`legacy_delphi_source/legacy_source/Subu28.pas`](../../legacy_delphi_source/legacy_source/Subu28.pas) (`Button101Click` L326~)
- 모던 라우트(정본): [`도서물류관리프로그램/frontend/src/app/(app)/shipping/courier/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/shipping/courier/page.tsx)
- 레거시 별칭: `/delivery/management` → `/shipping/courier` 리다이렉트
- 계약: [`migration/contracts/courier_management.yaml`](../../migration/contracts/courier_management.yaml)

## 1. 의미적 분기

- 레거시는 MDI·클라이언트 데이터셋·엑셀(`ColumnX1`)·인쇄 루프·진행 바가 혼재. 모던 1차는 **조회 + 그리드 + 메모 편집**까지만. 엑셀/라벨·인쇄·이중클릭→Sobo21 연동은 §7 out-of-scope.
- `Panel007`·`ProgressBar*`·`StBar101` 세부 셀: 로딩/레코드 카운트는 React state 로 흡수, **data-legacy-id** 는 그리드·입력·라디오·검색에 집중.

## 2. 영역

| 영역 | dfm | TabOrder | 모던 |
| --- | --- | --- | --- |
| 상단 검색 | `Panel001` | 0 | 검색 카드 |
| 중단 그리드 | `Panel002` + `DBGrid101` | 1 | `DataGrid` |
| 우측 필터 라디오 | `Panel003`~`Panel005` | 3~5 | 라디오 그룹 3열만 |
| 하단 메모 | `FlatPanel1` | 6 | 메모 카드 |
| 하단 진행/레코드 | `Panel007` | 2 | (간이) 로딩 텍스트만 — legacy-id 선택 |

## 3. 상단 Panel001 — TabOrder (form.json)

| TabOrder | 위젯 ID | 용도 | data-legacy-id |
| --- | --- | --- | --- |
| 0 | `Edit101` | 거래일자 | `Edit101` |
| 1 | `Edit102` | 출판사코드(시작) | `Edit102` |
| 2 | `Edit103` | 출판사명(시작) | `Edit103` |
| 3 | `Edit104` | 출판사코드(끝) | `Edit104` |
| 4 | `Edit105` | 출판사명(끝) | `Edit105` |
| 5 | `Panel101` | 라벨 거래일자 | `Panel101` |
| 6 | `Panel102` | 라벨 출판사명 | `Panel102` |
| 7 | `Button101` | (숨김 보조) | `Button101` |
| 8 | `Button201` | (숨김) | `Button201` |
| 9 | `DateEdit1` | 캘린더 | `DateEdit1` |
| 10 | `Button701` | 출판사 찾기 | `Button701` |
| 11 | `Button702` | 출판사(끝) 찾기 | `Button702` |
| 12 | `dxButton1` | 검색 실행 | `dxButton1` |

## 4. DBGrid101 컬럼 (dfm FieldName 순)

| 순서 | FieldName | 한글 | data-legacy-id (헤더) |
| --- | --- | --- | --- |
| 1 | `HCODE` | 코드 | `DBGrid101.HCODE` |
| 2 | `HNAME` | 출판사명 | `DBGrid101.HNAME` |
| 3 | `CODE5` | 선택 | `DBGrid101.CODE5` |
| 4 | `GNAME` | 거래처명 | `DBGrid101.GNAME` |
| 5 | `GPOSA` | 받는사람 | `DBGrid101.GPOSA` |
| 6 | `GTELS` | 전화번호 | `DBGrid101.GTELS` |
| 7 | `JUBUN` | 전표 | `DBGrid101.JUBUN` |
| 8 | `GQUT1` | 수량 | `DBGrid101.GQUT1` |
| 9 | `GQUT2` | 건수 | `DBGrid101.GQUT2` |

## 5. 우측 라디오

| ID | 캡션( dfm ) | data-legacy-id |
| --- | --- | --- |
| `RadioButton1` | 접수 | `RadioButton1` |
| `RadioButton2` | 완료 | `RadioButton2` |
| `RadioButton3` | 전체 | `RadioButton3` |
| `RadioButton4` | 전체선택 | `RadioButton4` |
| `RadioButton5` | 전체해제 | `RadioButton5` |
| `RadioButton6` | 자동알람 | `RadioButton6` |
| `RadioButton7` | 자동해체 | `RadioButton7` |
| `RadioButton8` | 구간 | `RadioButton8` |
| `RadioButton9` | 신간 | `RadioButton9` |
| `RadioButton0` | 전체 | `RadioButton0` |

## 6. 하단 메모 FlatPanel1

| ID | 용도 | data-legacy-id |
| --- | --- | --- |
| `Panel203` | 메모 라벨 | `Panel203` |
| `Edit203` | 메모1 | `Edit203` |
| `Edit204` | 메모2 | `Edit204` |
| `Edit205` | 전화1 | `Edit205` |
| `Edit206` | 전화2 | `Edit206` |
| `Edit207` | 수신자명 | `Edit207` |

## 7. §7 deltas (모던 전용·legacy-id 없음)

- 페이지네이션 UI, API 오류 배너, `Button701/702` 모달 대체 시각적 플레이스홀더, Excel/인쇄.

## 8. 회귀 검사용 legacy_id 목록 (부분 — 전량 grep)

```
Sobo28.Page Edit101 Edit102 Edit103 Edit104 Edit105 dxButton1 Button701 Button702
Sobo28.DBGrid101 DBGrid101.HCODE DBGrid101.HNAME DBGrid101.CODE5 DBGrid101.GNAME DBGrid101.GPOSA
DBGrid101.GTELS DBGrid101.JUBUN DBGrid101.GQUT1 DBGrid101.GQUT2
RadioButton1 RadioButton2 RadioButton3 RadioButton4 RadioButton5 RadioButton8 RadioButton9 RadioButton0
Panel203 Edit203 Edit204 Edit205 Edit206 Edit207
```
