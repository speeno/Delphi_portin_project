# 레이아웃 매핑: Sobo45 (청구서관리) → 모던 `/settlement/billing` [C5 Phase 1]

> **[2026-04-19 분리 안내]** 같은 이름의 [`Sobo45.md`](Sobo45.md) 는 C9 단계의 "물류비 마스터" 변환 노트(DEC-023). 본 노트는 C5 청구·정산용 **별도 매핑**이며 접미어 `_billing` 으로 분리한다 (`Sobo38_inbound.md` 선례).

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, **TabOrder**, DBGrid 컬럼, 이벤트) 를 모던 컴포넌트로 1:1 매핑. 픽셀 좌표·폰트·색상은 가져오지 않음.

## 0. 입력 산출물

- 본 폼: [`tools/.../legacy_source_root/Subu45/Sobo45.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu45/Sobo45.html) + `Sobo45.form.json` + `Sobo45.tree.json` + `Sobo45.pas_analysis.json`
- 변형: [`Sobo45_1_billing.md`](Sobo45_1_billing.md) (택배 전용, 로컬 `T4_Sub51/52` 데이터셋)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu45.dfm`](../../legacy_delphi_source/legacy_source/Subu45.dfm)
- 원 pas: [`legacy_delphi_source/legacy_source/Subu45.pas`](../../legacy_delphi_source/legacy_source/Subu45.pas) — `INSERT/UPDATE T2_Ssub` (≈2644~2971), `T2_Ssub.Yesno` 마감 분기 (840·979·1051), `Tong40._Sv_Ghng_` 트리거 (3282~3304, 4523), 평문 Gpass 변경(372~381)
- 모던 라우트(예정 — T6 신설): `/settlement/billing/page.tsx`
- 계약: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) (T3 신설)

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유

레거시 `Sobo45` 는 단일 MDI 자식 폼에서 (a) 거래일자/거래처 검색 → (b) 좌측 거래처 그리드 → (c) 우측 거래 라인 그리드(출고·반품·발송비) → (d) 푸터 인쇄/마감/Gpass 변경을 모달리스 동시 수행. 모던 C5 Phase 1 은:

- 검색·헤더 영역 → `/settlement/billing` 상단 검색 필터 + customer 드롭다운
- 좌측 거래처 그리드 → 출판사 리스트(`<DataGrid>` Sobo21 패턴)
- 우측 라인 그리드(`DBGrid201`) → 월합계 행 + 라인 라이프사이클 (집계·확정·취소)
- Gpass 변경 → DEC-029 `AuditPasswordModal` 의 `rotatePassword` 액션으로 흡수 (평문 InputBox 폐기)
- 인쇄·세금계산서 → C5 Phase 2 후속 (Sobo46/49)

**핵심 결정** — `T2_Ssub.Yesno='1'` 분기를 그대로 보존하여 마감 후 쓰기를 423 으로 차단(레거시 메시지 보존). `application_settings.settlement.close_until` 키는 **도입하지 않음**(DEC-031).

## 2. dfm 영역 인벤토리 (tree.json 기준)

| 영역 | dfm 컨테이너 | TabOrder | 자식 위젯 (개수·핵심) | 모던 매핑 |
| --- | --- | --- | --- | --- |
| 상단 검색·메타 패널 | `Panel001` (TFlatPanel) | 0 | Edit100~105, Panel101~105, Button101/201, Label101 | `/settlement/billing` 검색 영역 |
| 좌측 출판사 그리드 | (DBGrid in Panel002, dfm Width≈525) | 1 | DBGrid + 컬럼 `HCODE/HNAME` | `<DataGrid>` 좌측 |
| 우측 거래 라인 그리드 | `DBGrid201` (dfm `Title.Caption='저장'` 컬럼 포함) | 2 | 14컬럼 — GDATE/GQUT1~7/NAME1/NAME2/GNAME/GSQUT/GSSUM/YESNO | `<DataGrid>` 우측 (Sobo23 패턴) |
| 푸터 액션 | Button701/702 (`OnClick=Button70xClick`) | n/a | 인쇄·마감 트리거 | 헤더 액션 버튼(Phase 1: 마감만) |
| 데이터셋 | `DataSource1/2` | n/a | 2 | 백엔드/`settlement_service` 로 흡수 |
| Gpass 변경 (`Button004Click`, `Subu45.pas` 372~381) | (런타임 호출 — dfm 없음) | n/a | InputBox + `UPDATE Id_Logn` | `AuditPasswordModal` rotate 액션 |

## 3. 상단 검색 패널 위젯 매핑 (Panel001) — TabOrder 보존

| dfm TabOrder | dfm 위젯 ID | 클래스 | 라벨/용도 | 모던 위치 (`/settlement/billing`) | data-legacy-id |
| --- | --- | --- | --- | --- | --- |
| 0 | `Panel001` | TFlatPanel | 검색 패널 컨테이너 | `<section>` | `Sobo45.Panel001` |
| 4 | `Panel101` | TFlatPanel | "거래일자" 라벨 | `<Label htmlFor="from">거래일자</Label>` | `Sobo45.Panel101` |
| n/a | `Edit101` | TFlatMaskEdit | 거래일자(시작) | `<Input id="from" type="date">` | `Sobo45.Edit101` |
| 1 | `Edit100` | TFlatMaskEdit | 거래일자(종료) — `Label101="~"` | `<Input id="to" type="date">` | `Sobo45.Edit100` |
| 2 | `Edit102` | TFlatComboBox | 검색구분 | `<select id="searchKind">` | `Sobo45.Edit102` |
| 3 | `Edit103` | TFlatEdit | 출판사코드 | `<CustomerSearchInput id="hcode">` | `Sobo45.Edit103` |
| 8 | `Edit104` | TFlatEdit | 출판사명 표시 | (응답 customer_name) | `Sobo45.Edit104` |
| 9 | `Edit105` | TFlatEdit | 보조 검색어 | `<Input id="qfree">` | `Sobo45.Edit105` |
| 6 | `Button101` | TFlatButton (Visible=false) | 조회(보조) | (`Button201` 동일 의미로 흡수) | — |
| 7 | `Button201` | TFlatButton (Visible=false) | 신규 등록 | `<Button onClick=onSearch>조회</Button>` | `Sobo45.Button201` |

> dfm Panel101~105 은 라벨 컨테이너 — 모던에서는 `<label htmlFor>` 로 의미 흡수. Panel102~105 은 `data-legacy-id` 만 빈 `<span>` 으로 가드 부착.

## 4. 우측 거래 라인 그리드 매핑 (`DBGrid201`)

| dfm FieldName | 한글 컬럼 (헤더 그룹) | 의미 | 모던 컬럼 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GDATE` | 일자 | 거래일자 | `<th>일자</th>` | `Sobo45.DBGrid201.GDATE` |
| `GQUT1` | 출고내역\|시내부수 | 시내 출고 부수 | `<th>시내부수</th>` (출고내역 그룹) | `Sobo45.DBGrid201.GQUT1` |
| `GQUT2` | 출고내역\|지방부수 | 지방 출고 부수 | `<th>지방부수</th>` | `Sobo45.DBGrid201.GQUT2` |
| `GQUT4` | 출고내역\|보호대 | 보호대 부수 | `<th>보호대</th>` | `Sobo45.DBGrid201.GQUT4` |
| `GQUT3` | 출고내역\|박스대 | 박스대 부수 | `<th>박스대</th>` | `Sobo45.DBGrid201.GQUT3` |
| `GQUT6` | 반품수거\|시내 | 시내 반품 수거 | `<th>시내(반품)</th>` | `Sobo45.DBGrid201.GQUT6` |
| `GQUT7` | 반품수거\|지방 | 지방 반품 수거 | `<th>지방(반품)</th>` | `Sobo45.DBGrid201.GQUT7` |
| `GQUT5` | 반품내역\|총부수 | 반품 합계 | `<th>총부수</th>` | `Sobo45.DBGrid201.GQUT5` |
| `NAME1` | 발송비내역\|지역 | 지역명 | `<th>지역</th>` | `Sobo45.DBGrid201.NAME1` |
| `NAME2` | 발송비내역\|화물명 | 화물명 | `<th>화물명</th>` | `Sobo45.DBGrid201.NAME2` |
| `GNAME` | 발송비내역\|서점명 | 서점명 | `<th>서점명</th>` | `Sobo45.DBGrid201.GNAME` |
| `GSQUT` | 발송비내역\|건수 | 건수 | `<th>건수</th>` | `Sobo45.DBGrid201.GSQUT` |
| `GSSUM` | 발송비내역\|발송비 | 발송 금액 | `<th>발송비</th>` (SUM 푸터) | `Sobo45.DBGrid201.GSSUM` |
| `YESNO` | 저장 | 확정 플래그 (`'1'`=마감) | `<th>상태</th>` 배지 — DEC-031 마감 가드 | `Sobo45.DBGrid201.YESNO` |

좌측 출판사 그리드 (별도 DataSource, `DBGrid202` 추정):

| dfm FieldName | 한글 | 의미 | 모던 | data-legacy-id |
| --- | --- | --- | --- | --- |
| `HCODE` | 코드 | 출판사 코드 | 좌측 그리드 1열 | `Sobo45.DBGrid202.HCODE` |
| `HNAME` | 출판사명 | 출판사명 | 좌측 그리드 2열 | `Sobo45.DBGrid202.HNAME` |

## 5. 데이터 흐름 (`Subu45.pas` 인용)

```
검색 → SELECT * FROM T2_Ssub WHERE Hcode = ? AND Gdate BETWEEN ?
     → 좌측 그리드: 거래처 선택
     → 우측 그리드: 라인 단위 GQUT1~7 / 발송비 NAME1/NAME2/GSSUM
신규/수정 → DBGrid201Columns10UpdateData → INSERT/UPDATE T2_Ssub (≈2644~2971)
                                       → INSERT/UPDATE T3_Ssub (라인)
확정    → UPDATE T2_Ssub SET Yesno='1' WHERE 월키 + audit_token(scope=settlement_confirm)
취소    → UPDATE T2_Ssub SET Yesno='2' (DEC-012 soft cancel)
집계 후 → Tong40._Sv_Ghng_ → Sv_Ghng (3282~3304, 4523)
Gpass    → InputBox + UPDATE Id_Logn ... → AuditPasswordModal rotate (DEC-032)
```

## 6. out-of-scope 위젯 (Phase 1 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 인쇄 | Button701/702, Panel401(있다면) | C5 Phase 2 = Sobo46 청구서출력 |
| 진행/상태바 | (있다면) | React `loading` boolean 흡수 |
| Gpass 평문 변경 (`Subu45.pas` 372~381) | InputBox 호출 | DEC-032: Audit 모달 rotate 액션으로 이관 |

## 7. Deltas — 모던 신설 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | 마감 토글 / 마감 후 차단 배지 | 그리드 헤더 | DEC-031 (`T2_Ssub.Yesno='1'` ⇒ 423) |
| 모던 신규 | DataGridPager | `/settlement/billing` | dfm 모달리스 → 페이지네이션 (DEC-024) |
| 모던 신규 | 변형 토글 (택배/일반) | URL `?variant=takbae` | Sobo45_1 통합 (`customer_variants`) |
| 모던 신규 | 확정/취소 액션 → AuditPasswordModal | 우측 그리드 푸터 | DEC-029 패스워드 게이팅 (scope=`settlement_confirm`) |
| dfm out-of-scope | 인쇄 콜아웃 | — | Phase 2 — Sobo46 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 | 비고 |
| --- | --- | --- |
| `FormActivate` / `FormShow` | `useEffect` mount → `useDynamicPageSize` → `load()` | C6 패턴 |
| `FormClose` | `<Button>목록</Button>` (대시보드 복귀) | |
| `Button101Click` / `Button201Click` | `onSearch` → `settlementApi.list()` | `Visible=false` 였으나 모던은 명시 노출 |
| `Button701Click` (인쇄) | (Phase 2) | C5 Phase 2 — Sobo46 |
| `Button702Click` (마감/Gpass) | (Phase 1) `onConfirmClose` → AuditPasswordModal | DEC-029/032 |
| `DBGrid201Columns10UpdateData` | 라인 셀 편집 → `settlementApi.upsertLine()` | 백엔드 UPSERT |
| `DBGrid201CellClick` (`YESNO`) | 마감 후 클릭 시 423 메시지 | DEC-031 |
| `DataSource1/2DataChange` | (자동 — React state) | |

## 9. 변형 차이 (`Sobo45` 본 vs `Sobo45_1`)

`Sobo45_1` (택배 전용): 컬럼 5~7번이 출고내역에서 **택배비\|大/中/小** 로 치환 (필드 `GQUT5/6/7` 의미만 다름). 데이터셋이 폼 로컬 `T4_Sub51/52` 로 이동. **차이는 [`Sobo45_1_billing.md`](Sobo45_1_billing.md) + contract `customer_variants.takbae`** 에만 기록 (코드 분기 금지).

## 10. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] 본 노트 §3·§4 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재 (총 ~22개):
  - 검색: `Sobo45.Panel001/101`, `Edit100/101/102/103/104/105`, `Button201`
  - 좌측 그리드: `Sobo45.DBGrid202.HCODE/HNAME`
  - 우측 그리드: `Sobo45.DBGrid201.{GDATE,GQUT1..7,NAME1,NAME2,GNAME,GSQUT,GSSUM,YESNO}`
- [ ] §6 out-of-scope (인쇄 버튼·평문 Gpass 입력) 가 코드에 들어가지 않음
- [ ] DEC-031 — `T2_Ssub.Yesno='1'` 인 월에 쓰기 시 423 + 레거시 한글 메시지(`i18n/messages/c5.ko.json`)
- [ ] DEC-029 — 확정·취소·Gpass 변경 액션이 `Authorization-Audit` 헤더 검증
- [ ] DEC-028 §3 "버리는 정보" (픽셀 좌표·폰트·색상·Glyph) 가 코드에 없음

## 11. 참조

- DEC-009: 1차 권한키 미적용
- DEC-012: soft cancel (yesno=2)
- DEC-024: 페이지네이션 표준 (DataGridPager)
- DEC-028: dfm→html 산출물 영구 입력 동결
- DEC-029: Sobo40 패스워드 토큰 게이팅
- DEC-031 (T8 신설): C5 마감 정책 — `T2_Ssub.Yesno` 보존
- DEC-032 (T8 신설): 평문 Gpass → AuditPasswordModal rotate 이관
- 화면 카드: [`analysis/screen_cards/Sobo45.md`](../screen_cards/Sobo45.md) (T1 신설)
- contract: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) (T3)
- 변형: [`Sobo45_1_billing.md`](Sobo45_1_billing.md)
- 선례: `Sobo23.md` (목록·라인 패턴), `Sobo38_inbound.md` (이름 충돌 회피 접미어)
