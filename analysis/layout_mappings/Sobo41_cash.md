# 레이아웃 매핑: Sobo41 (입금내역) → 모던 `/settlement/cash` [C5 Phase 1]

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑. 픽셀 좌표·폰트·색상은 가져오지 않음.

## 0. 입력 산출물

- 본 폼: [`tools/.../legacy_source_root/Subu41/Sobo41.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu41/Sobo41.html) + `.form.json` + `.tree.json` + `.pas_analysis.json`
- 변형 폴더 부재 — `Subu41` 단일
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu41.dfm`](../../legacy_delphi_source/legacy_source/Subu41.dfm)
- 원 pas: [`legacy_delphi_source/legacy_source/Subu41.pas`](../../legacy_delphi_source/legacy_source/Subu41.pas) — `Select * From T5_Ssub` 조회, 쓰기는 `Base10.T4_Sub11/12` DataModule 위임 (343/353/563 등)
- 모던 라우트(예정 — T6 신설): `/settlement/cash/page.tsx`
- 계약: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) `list_cash`, `register_cash` 액션

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유

레거시 `Sobo41` = (a) 상단 검색(거래일자·거래처) → (b) 중단 그리드(`DBGrid101` — 입금 내역 7컬럼) → (c) 하단 입력 패널(`Panel003` — 신규/수정 폼) → (d) 진행 패널 모달리스. 모던:

- 검색·그리드 → `/settlement/cash` 단일 페이지 (DataGridPager)
- 신규/수정 → 같은 페이지 우측 슬라이드 패널 또는 모달 (Sobo21 패턴)
- 입금 자체는 `T5_Ssub` 직접 INSERT/UPDATE — 백엔드 `cash_service` 단독 (DataModule 위임 없음)

## 2. dfm 영역 인벤토리 (tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수·핵심) | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색 | `Panel001` (TFlatPanel) | 0 | Edit101/102/107/108 + Button101/201 | `<section>` 검색 영역 |
| 중단 그리드 | `Panel002` (TFlatPanel) | 1 | DBGrid101 + StBar101 | `<DataGrid>` |
| 진행 패널 | `Panel007` (TFlatPanel) | 2 | (있다면 progress) | `loading` boolean 흡수 |
| 하단 입력 | `Panel003` (TFlatPanel) | 3 | Edit301~306, Button700/701 | 우측 슬라이드 패널 (`<form>`) |

## 3. 상단 검색 패널 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (`/settlement/cash`) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Edit101` | TFlatMaskEdit | 입금일자(시작) | `<Input id="from" type="date">` | `Sobo41.Edit101` |
| 1 | `Edit102` | TFlatMaskEdit | 입금일자(종료) | `<Input id="to" type="date">` | `Sobo41.Edit102` |
| 3 | `Edit107` | TFlatEdit | 거래처코드 | `<CustomerSearchInput id="hcode">` | `Sobo41.Edit107` |
| 4 | `Edit108` | TFlatEdit | 거래처명 표시 | (응답 customer_name) | `Sobo41.Edit108` |
| n/a | `Button101` | TFlatButton | 조회 (`Button101Click`) | `<Button onClick=onSearch>조회</Button>` | `Sobo41.Button101` |
| n/a | `Button201` | TFlatButton | 신규 (`Button201Click`) | `<Button onClick=onNew>신규</Button>` | `Sobo41.Button201` |

## 4. 중단 그리드 매핑 (DBGrid101)

| dfm FieldName | 한글 컬럼 | 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GDATE` | 입금일자 | 입금일 | `<th>입금일자</th>` | `Sobo41.DBGrid101.GDATE` |
| `SDATE` | 청구월 | 대응 청구 YYYYMM | `<th>청구월</th>` | `Sobo41.DBGrid101.SDATE` |
| `HCODE` | 출판사코드 | 거래처 코드 | `<th>출판사</th>` | `Sobo41.DBGrid101.HCODE` |
| `HNAME` | 출판사명 | 거래처명 | (HCODE 와 결합 표시) | `Sobo41.DBGrid101.HNAME` |
| `GSSUM` | 금액 | 입금액 | `<th>금액</th>` (SUM 푸터) | `Sobo41.DBGrid101.GSSUM` |
| `PUBUN` | 결재 | 결재구분 코드 (현금/이체/카드 — OQ-ST-4) | `<th>결재</th>` 배지 | `Sobo41.DBGrid101.PUBUN` |
| `GBIGO` | 메모 | 비고 | `<th>메모</th>` | `Sobo41.DBGrid101.GBIGO` |

## 5. 하단 입력 패널 매핑 (Panel003 — TabOrder 보존)

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (입력 폼) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Edit303` | TFlatMaskEdit | 입금일자 | `<Input id="gdate" type="date">` | `Sobo41.Edit303` |
| 1 | `Edit301` | TFlatEdit | 거래처코드 | `<CustomerSearchInput id="hcode_form">` | `Sobo41.Edit301` |
| 2 | `Edit302` | TFlatEdit | 청구월 (SDATE) | `<Input id="sdate" type="month">` | `Sobo41.Edit302` |
| 5 | `Edit306` | TFlatEdit | 입금액 (GSSUM) | `<Input id="gssum" type="number">` | `Sobo41.Edit306` |
| n/a | `Edit304` | TFlatComboBox | 결재구분 (PUBUN) | `<select id="pubun">` (OQ-ST-4 카탈로그) | `Sobo41.Edit304` |
| n/a | `Button700` | TFlatButton | 저장 (`Button700Click`) | `<Button onClick=onSave>저장</Button>` | `Sobo41.Button700` |
| n/a | `Button701` | TFlatButton | 취소/초기화 (`Button701Click`) | `<Button variant="ghost" onClick=onReset>초기화</Button>` | `Sobo41.Button701` |

## 6. 데이터 흐름 (`Subu41.pas` 인용)

```
조회 → SELECT * FROM T5_Ssub
       LEFT JOIN G7_Ggeo ON T5_Ssub.Hcode = G7_Ggeo.Hcode
       WHERE Gdate BETWEEN ? AND ? AND Hcode LIKE ?
신규 → INSERT INTO T5_Ssub (Gdate, Hcode, Sdate, Gssum, Pubun, Gbigo) VALUES (...)
수정 → UPDATE T5_Ssub SET Gssum=?, Pubun=?, Gbigo=? WHERE Gdate=? AND Hcode=? AND Jubun=?
삭제 → DEC-012 soft cancel (Yesno='2' 권장 — OQ-ST-3 확정)
```

> 레거시는 쓰기를 `Base10.T4_Sub11/12` DataModule 에 위임하지만 모던은 백엔드 `cash_service` 직접 SQL 로 단순화 (DEC-024 단일 디코딩 정책).

## 7. out-of-scope 위젯

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 진행 패널 | Panel007 + ProgressBar | React `loading` boolean 흡수 |
| 인쇄 | (있다면 Button702/901) | C7 인쇄 후속 |
| 보조 입력 | Edit304 외 추가 라벨 패널 | 핵심 5필드만 |

## 8. Deltas — 모던 신설 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | DataGridPager | 그리드 | DEC-024 페이지네이션 표준 |
| 모던 신규 | 결재구분 enum 검증 | `<select id="pubun">` | OQ-ST-4 카탈로그 적용 시 enum 화 |
| 모던 신규 | "취소 포함" 토글 | 검색 영역 | DEC-012 soft cancel 기본 숨김 |

## 9. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 | 비고 |
| --- | --- | --- |
| `FormActivate` | `useEffect` mount → `load()` | C6 패턴 |
| `Button101Click` | `onSearch` → `cashApi.list()` | |
| `Button201Click` | `onNew` → 입력 패널 open | |
| `Button700Click` | `onSave` → `cashApi.upsert()` | INSERT/UPDATE 분기는 백엔드 |
| `Button701Click` | `onReset` → 입력 폼 초기화 | |
| `DBGrid101DblClick` | (행 더블클릭 → 수정) | Phase 1 클릭 → 입력 패널 prefill |

## 10. 변형 차이

본 폼에 variant 없음. (입금현황 변형은 [`Sobo42_cash.md`](Sobo42_cash.md) / [`Sobo42_1_cash.md`](Sobo42_1_cash.md) 참조 — 별 폼이며 본 입금내역과 다른 시나리오)

## 11. 회귀 가드 체크리스트

- [ ] 본 노트 §3·§4·§5 의 모든 `data-legacy-id` 가 모던 페이지에 존재 (총 ~17개):
  - 검색: `Sobo41.Edit101/102/107/108`, `Button101/201`
  - 그리드: `Sobo41.DBGrid101.{GDATE,SDATE,HCODE,HNAME,GSSUM,PUBUN,GBIGO}`
  - 입력: `Sobo41.Edit303/301/302/306/304`, `Button700/701`
- [ ] DEC-012 — 취소된 입금(`Yesno='2'`) 기본 숨김, 토글로 표시
- [ ] DEC-024 — DataGridPager + EUC-KR 단일 디코딩 정책
- [ ] DEC-028 §3 "버리는 정보" 미존재

## 12. 참조

- DEC-012: soft cancel
- DEC-024: 페이지네이션 표준
- DEC-028: dfm 산출물 영구 입력
- OQ-ST-4: PUBUN 결재구분 코드 카탈로그
- contract: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml)
- 화면 카드: [`analysis/screen_cards/Sobo45.md`](../screen_cards/Sobo45.md) (C5 통합 카드)
- 선례: `Sobo23.md` (목록·라인 패턴), `Sobo21.md` (S1_Memo UPSERT)
