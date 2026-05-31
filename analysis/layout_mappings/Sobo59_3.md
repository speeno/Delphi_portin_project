# 레이아웃 매핑: Sobo59_3 (출고 검증관리 개별) — 거래관리 출고검증(개별)

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, TabOrder, DBGrid 컬럼, 이벤트) 1:1 매핑.

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu59_3/Sobo59_3.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu59_3/Sobo59_3.html) + `Sobo59_3.form.json`
- PAS 분석: `Subu59_3/Sobo59_3.pas_analysis.json` (sql_calls 17 — **동적 `Sqlen` 연결**, event_handlers 68)
- dfm caption: **「출고 검증관리(개별)」**

## 1. 영역 분할

| 영역 | dfm 컨테이너 | 모던 컴포넌트 | 역할 |
| --- | --- | --- | --- |
| 입력 패널 | `TFlatPanel` 묶음 + `Edit201/501`·`Edit122~124`(SpinEdit) | 개별 입력 폼 | 전표/바코드·수량 개별 입력 |
| 그리드 | `DBGrid201` (TDBGridEh) | `DataGrid` | 개별 검증 라인 |
| 라벨 다수 | `TmyLabel3d` ×18 | 정적 라벨 | 항목 안내 |
| 액션 | `Button102`(검증)·`Button104`(저장)·`btnPrint_label`(라벨 F12) | 버튼 그룹 | 검증·저장·라벨 인쇄 |
| 체크 | `TFlatCheckBox` ×2 | 체크박스 | 검증 옵션 |

## 2. 입력 위젯

| dfm ID | 클래스 | 역할 | 모던 매핑 |
| --- | --- | --- | --- |
| `Edit201`/`Edit501` | TFlatEdit | 전표/바코드 입력 | `<Input data-legacy-id="Sobo59_3.Edit201">` |
| `Edit122~124` | TSpinEdit | 수량 개별 입력 | `<NumberInput>` |
| `Button102` | TdxButton | 검증 | 개별 검증 실행 |
| `Button104` | TdxButton | 저장 | 검증 결과 저장 |
| `btnPrint_label` | TdxButton | 라벨(F12) | 라벨 인쇄 (DEC-018 후속) |

## 3. 이벤트·비즈니스 규칙

- 출고검증(2)과 동일 규칙군(과출고·체크 가드)을 개별 전표/바코드 단위로 수행.
- `Button104` 저장 = 검증 결과 INSERT/UPDATE (쓰기).
- 라벨 인쇄(`btnPrint_label`)는 DEC-018 인쇄 후속 — OOS.

## 4. phase1 게이트 (블록 사유)

- Sobo59_2 와 동일 — 동적 `Sqlen` SQL + 쓰기 워크플로. `Subu59_3.pas` SQL 정본 수기 추출이 phase1 선행 조건.
- 본 노트는 레이아웃·규칙 인벤토리까지 확정. API/서비스는 SQL 정본 확보 후.
