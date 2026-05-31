# 레이아웃 매핑: Sobo59_2 (출고 검증관리) — 거래관리 출고검증(2)

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, TabOrder, DBGrid 컬럼, 이벤트) 1:1 매핑. 픽셀/폰트/색상 제외.

## 0. 입력 산출물

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu59_2/Sobo59_2.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu59_2/Sobo59_2.html) + `Sobo59_2.form.json`
- PAS 분석: `Subu59_2/Sobo59_2.pas_analysis.json` (sql_calls 11 — **동적 `Sqlen` 연결이라 리터럴 SQL 미추출**, event_handlers 69)
- dfm caption: **「출고 검증관리」**

> **P0 주의(transactions-menu200-p0-form-mapping.md §5)**: 본 폼은 물류 확장 「출고검증」이며,
> 가속기 `Subu59_1` 은 검증이 아니라 「일별 내역서(요약)」다. 스크린샷의 「출고검증(1)」 매핑은 별도 확인 필요.

## 1. 영역 분할

| 영역 | dfm 컨테이너 | 모던 컴포넌트 | 역할 |
| --- | --- | --- | --- |
| 상단 검색 패널 | `TFlatPanel` 묶음 + `Edit101/102`(기간 마스크)·`DateEdit1/2`·`Edit103~106`·`dxButton1`(검색) | 검색 폼 | 기간·출판사·거래처 검색 |
| 상태 라디오 | `RadioButton1`(접수중)·`RadioButton2`(사용중) | 라디오 그룹 | 검증 대상 상태 필터 |
| 그리드 3종 | `DBGrid101`·`DBGrid201`·`DBGrid301` (TDBGridEh) | 3개 `DataGrid` | 대상/검증/결과 라인 |
| 액션 | `Button102`(검증)·`Button103`(취소)·`Button701/702` | 버튼 그룹 | 검증 실행·취소 |
| 진행 바 | `TFlatProgressBar`·`TProgressBar` | 진행 표시 | 배치 검증 진행 |

## 2. 검색·상태 위젯

| dfm ID | 클래스 | 역할 | 모던 매핑 |
| --- | --- | --- | --- |
| `Edit101`/`Edit102` | TFlatMaskEdit | 기간(시작/끝) 마스크 | `<DateInput data-legacy-id="Sobo59_2.Edit101">` |
| `DateEdit1`/`DateEdit2` | TDateEdit | 기간 캘린더 | 마스크와 동기 |
| `Edit103~106` | TFlatEdit | 출판사/거래처 코드·명 | 자동완성 |
| `dxButton1` | TdxButton | 검색 | `onSubmit` → 검증 대상 조회 |
| `RadioButton1`/`RadioButton2` | TFlatRadioButton | 접수중/사용중 | 상태 토글 |

## 3. 그리드 (3종, 컬럼은 dfm 직접 비교 후 확정)

| 그리드 | 역할 | 비고 |
| --- | --- | --- |
| `DBGrid101` | 검증 대상 전표/라인 | 체크박스 선택(과출고 검증 입력) |
| `DBGrid201` | 검증 결과/대조 | 실물 vs 출고 수량 |
| `DBGrid301` | 요약/오류 | 「과출고」 등 경고 행 |

## 4. 이벤트·비즈니스 규칙 (PAS messages)

| 트리거 | 규칙 메시지 | 의미 |
| --- | --- | --- |
| 검색 | 「검색한 자료가 없습니다」/「검색한 출판사가 없습니다」 | 조회 결과 가드 |
| 검증(`Button102`) | 「과출고입니다. 확인해주세요.」 | 출고수량 > 검증수량 시 차단 (over-shipment) |
| 검증 | 「체크한 도서는 없습니다.」 | 체크박스 미선택 가드 |
| 저장 | `E_Insert`/`E_Update` | 검증 결과 INSERT/UPDATE (쓰기 워크플로) |

## 5. phase1 게이트 (블록 사유)

- 검증 로직은 **동적 SQL(`Sqlen` 문자열 연결)** 로, 가속기가 리터럴 SQL 을 추출하지 못했다.
- 본 화면은 **쓰기 워크플로**(검증 결과 INSERT/UPDATE + 과출고 규칙)라 백엔드 SQL·규칙을 임의로
  합성하면 안 된다(no-fabrication). **`Subu59_2.pas` 의 `Sqlen` 동적 SQL 수기 추출**이 phase1 선행 조건.
- 따라서 본 노트는 레이아웃·규칙 인벤토리까지만 확정하고, API/서비스 구현은 SQL 정본 확보 후 진행한다.
