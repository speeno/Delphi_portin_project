# C6 (거래/잔액 조회) 레거시 흐름 · SQL · POC 대조 매트릭스

> 작성: 2026-04-18 (Phase 1 분석 산출물 — `migration/contracts/sales_inquiry.yaml` 작성 직전)
> 대상 폼 4종: `TSobo21`(거래명세서), `TSobo31`(도서별수불원장), `TSobo61`(도서별판매), `TSobo62`(거래처판매)
> 1차 합격선: 4개 화면의 **조회(GET) + 메모 저장(PATCH)** 동등성. **권한키(F24/F31/F61/F62)·인쇄·바코드는 후속 (DEC-016/017/018 신규 등록 예정)**
> 형식 기준: [`analysis/c2_outbound_flow.md`](c2_outbound_flow.md) 와 동일.

---

## 0. 한눈 요약

- 4폼 모두 **TADOQuery + DBGridEh** 기반 — 조회는 동적 SQL 문자열을 `Base10.Socket.RunSQL` 로 보내고 `MakeGrid(SGrid)` / `ClientGrid(nSqry)` 로 받아 클라이언트 임시 데이터셋을 만든다.
- **공통 SELECT 베이스**: `S1_Ssub` (출고/입고/반품 라인 단일 테이블). 합성키 `(Gdate, Hcode, Jubun, Gjisa, Gcode, Scode, Gubun, Ocode)` 로 거래 식별.
- **보조 마스터**: `G1_Ggeo`(거래처), `H2_Gbun`(지점/일자), `G4_Book`(도서), `G7_Ggeo`(거래처 보조), `Sg_Csum`(사전 집계), `Sv_Ghng`(이월 잔액), `Sb_Csum`(누적), `H1_Ssub`(입출금).
- **C6 1차에 포함되는 비-SELECT (사용자 결정 (C))**:
  - `Subu21.pas:1474` — `UPDATE S1_Memo SET Gbigo, Sbigo, Gtel1, Gtel2, Gname, Gpost, Time3=now()` (메모/연락처 갱신)
  - `Subu21.pas:1517` — `INSERT INTO S1_Memo (...) VALUES ...` (메모 신규)
  - 그 외 4폼은 모두 SELECT only (정적 분석 `query_catalog.json` 교차검증).
- **`Sg_Csum` 사용 패턴**: Sobo61(폐기 합계), Sobo62(입출금 합계 sub-query)에서 GROUP BY 합계용으로 SELECT만 사용 — `OQ-OUT-2`(Sg_Csum 트리거 갱신 여부)는 **본 시나리오에서 갱신하지 않으므로** 1차 영향 없음. 기존 트리거가 갱신해 주는 데이터를 단순 읽기.

---

## 1. 폼 ↔ 메뉴 ↔ 라우트 ↔ 엔드포인트 매핑

| 폼 | Delphi 메뉴 (`Chul.dfm`) | 웹 라우트(신규) | 백엔드 엔드포인트(신규) | 주 테이블 |
|---|---|---|---|---|
| **TSobo21** 거래명세서 | 출고관리 > 거래명세서 — `Menu201` ([`Chul.dfm:386-389`](../legacy_delphi_source/legacy_source/Chul.dfm)) | `/transactions/sales-statement` | `GET  /api/v1/transactions/sales-statement`<br>`GET  /api/v1/transactions/sales-statement/{key}`<br>`PATCH /api/v1/transactions/sales-statement/{key}/memo` | `S1_Ssub`, `S1_Memo`, `G1_Ggeo`, `H2_Gbun`, `G4_Book` |
| **TSobo31** 도서별수불원장 | 재고원장 > 도서별수불원장 — `Menu301` ([`Chul.dfm:467-470`](../legacy_delphi_source/legacy_source/Chul.dfm)) | `/inventory/ledger` | `GET /api/v1/inventory/ledger` | `S1_Ssub`, `Sv_Ghng`, `Sb_Csum`, `Sg_Csum`, `G7_Ggeo` |
| **TSobo61** 도서별판매 | 통계관리 > 도서별판매 — `Menu601` ([`Chul.dfm:730-732`](../legacy_delphi_source/legacy_source/Chul.dfm)) | `/reports/book-sales` | `GET /api/v1/reports/book-sales` | `S1_Ssub` GROUP BY, `Sg_Csum` |
| **TSobo62** 거래처판매 | 통계관리 > 거래처판매 — `Menu602` ([`Chul.dfm:734-736`](../legacy_delphi_source/legacy_source/Chul.dfm)) | `/reports/customer-sales` | `GET /api/v1/reports/customer-sales` | `S1_Ssub` GROUP BY, `H1_Ssub`(향후), `Sg_Csum` |

---

## 2. Sobo21 — 거래명세서 (`Subu21.pas`)

### 2.1 핵심 핸들러

| 라인 | 핸들러 | 역할 (1차 매핑) |
|---|---|---|
| L177 | `FormShow` | Edit101 = 오늘 (`yyyy.mm.dd`) → 기본 기간 |
| L460 | `Button101Click` | **조회**: 거래처 출고정지/지점 정지 검사 → `Select * From S1_Ssub Where Gdate, Gubun, Jubun, Gcode, Scode, Gjisa, Ocode='B', Hcode` 동등 조건 |
| L571 | `Button201Click` | **명세 채움**: G7/G1/G4 마스터에서 거래처명/제품명 LOOKUP 후 nSqry.Append (1차 미포함 — 신규 등록 흐름) |
| L1452 | (메모 SELECT/UPDATE/INSERT 진입점) | `S1_Memo` 메모/비고/연락처 저장 (PATCH 매핑) |

### 2.2 SELECT (조회·LOOKUP)

| 출처 | SQL 발췌 | 1차 매핑 |
|---|---|---|
| L467 | `Select Grat9 From G1_Ggeo Where Hcode=? and Gcode=?` | 거래처 출고정지 검사 (서비스에서 그대로 호출) |
| L476 | `Select Gbigo From H2_Gbun Where Hcode=? and Gcode=? and Gname=? and Jubun=?` | 지점 정지 검사 |
| L503 | `Select * From S1_Ssub Where Gdate=? and Gubun=? and Jubun=? and Gcode=? and Scode='X' and Gjisa=? and Ocode='B' and Hcode=?` | 메인 명세서 조회 (목록·상세 공통 베이스) |
| L536 | `Select Gname,Gjeja From G4_Book Where Gcode=? and Hcode=?` | 도서명 보강 |
| L669 | `Select Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost From S1_Memo Where Gdate=? and Gubun=? and Jubun=? and Gcode=? and Scode=? and Gjisa=? ...` | 상세 모달 메모 LOAD |

### 2.3 비-SELECT (1차 포팅 포함)

| 출처 | SQL 발췌 | 1차 매핑 |
|---|---|---|
| L1455 | `Select Gbigo From S1_Memo Where ...` (존재 검사) | PATCH 분기 결정 (UPSERT) |
| L1474 | `UPDATE S1_Memo SET Gbigo=?, Sbigo=?, Gtel1=?, Gtel2=?, Gname=?, Gpost=?, Time3=now() WHERE Gdate=? and Gubun=? ...` | `PATCH /transactions/sales-statement/{key}/memo` (존재 시 UPDATE) |
| L1517 | `INSERT INTO S1_Memo (Gdate, Gubun, Jubun, Gcode, Scode, Gjisa, Hcode, Ocode, Gbigo, Sbigo, Gtel1, Gtel2, Gname, Gpost, Time1) VALUES (...)` | `PATCH /transactions/sales-statement/{key}/memo` (없으면 INSERT) |

> **트랜잭션**: 메모 UPSERT 단건은 `app/core/db.py::execute_in_transaction` 으로 BEGIN→SELECT→UPDATE/INSERT→COMMIT 1 트랜잭션. 동시성은 `Time3=now()` 이외 잠금 없음(레거시와 동일).

---

## 3. Sobo31 — 도서별수불원장 (`Subu31.pas`)

### 3.1 핵심 핸들러

| 라인 | 핸들러 | 역할 |
|---|---|---|
| L135 | `FormShow` | 기본 기간 (오늘/월초) |
| L280 | `Button101Click` | **분기 라우터**: `Select Scode From G7_Ggeo Where Gcode=?` → '1'이면 `Button103Click`(고객사용), 아니면 `Button102Click`(일반) |
| L290 | `Button102Click` | 일반 수불 — `Sv_Ghng` 이월 잔액 + `S1_Ssub` 기간 명세 + `Sb_Csum` 누적 |
| (Button103Click) | 고객사 변형 | 1차에서는 동일 응답 스키마 사용 (분기는 서비스 내부 처리) |

### 3.2 SELECT 베이스

| 출처 | SQL 발췌 | 비고 |
|---|---|---|
| L282 | `Select Scode From G7_Ggeo Where Gcode=?` | 분기 결정 |
| L336 | `Select Max(Gdate) as Gdate From Sv_Ghng Where Gdate < ? and Hcode=?` | **이월 기준일** 산출 |
| L366 | `Select Gdate, Scode, Gubun, Pubun, Bcode, Gbigo, Gsqut, Gssum From S1_Ssub Where Gdate>=? and Gdate<=? and (Bdate is null) and (Bcode=? [or 도서묶음]) and Ocode Like '%B%' Order By Gdate, Jubun, Id` | **메인 수불 명세** |
| (102 후반) | `Select ... From Sg_Csum Where ...`, `Select ... From Sb_Csum Where ...` | 누적/사전집계 합산 |

### 3.3 1차 응답 모델

각 행 = `(Gdate, Gcode, Gname, Giqut[입고], Gbqut[비품], Gpqut[폐기], Gjqut[증정], Goqut[출고], Gisum, Gosum, Gbsum, Gjsum, Gpsum)` 의 누적 컬럼. 레거시 클라이언트 측 누적 로직(L383~)을 서버에서 GROUP BY + Python 집계로 재현 (n+1 호출 제거).

---

## 4. Sobo61 — 도서별판매 (`Subu61.pas`)

### 4.1 핵심 핸들러

| 라인 | 핸들러 | 역할 |
|---|---|---|
| L133 | `FormShow` | 기본 기간 |
| L288 | `Button101Click` | **메인 조회** — `S1_Ssub` GROUP BY 후 `Sg_Csum` 합계 후처리 |
| L452 | `Button201Click` | 상세 (도서별 → 거래처별) — 1차 별도 엔드포인트로 분리 가능 (생략 가능) |

### 4.2 SELECT 베이스

| 출처 | SQL 발췌 |
|---|---|
| L323 | `Select Bcode, Scode, Gubun, Pubun, Sum(Gsqut) as Gsqut, Sum(Gssum) as Gssum From S1_Ssub Where Gdate>=? and Gdate<=? and Hcode=? and Ocode Like '%B%' [+ Bcode 구간] [+ S_Where1] [+ Scode 필터] Group By Bcode, Scode, Gubun, Pubun` |
| L404 | `Select Gcode, Sum(Gbsum) as Gbsum From Sg_Csum Where Gdate>=? and Gdate<=? and Hcode=? and Scode Like '%B%' [+ Gcode 구간] Group By Gcode` |

### 4.3 1차 응답 모델

행 = `(Gcode 도서코드, Gname 도서명, Giqut, Gbqut, Gpqut, Gjqut, Goqut, Gisum, Gosum, Gbsum, Gpsum)`. C14 동등성 캡처 대상.

---

## 5. Sobo62 — 거래처판매 (`Subu62.pas`)

### 5.1 핵심 핸들러

| 라인 | 핸들러 | 역할 |
|---|---|---|
| L133 | `FormShow` | 기본 기간 |
| L288 | `Button101Click` | **메인 조회** — `S1_Ssub` GROUP BY (거래처+지사+분류) |

### 5.2 SELECT 베이스

| 출처 | SQL 발췌 |
|---|---|
| L329 | `Select Hcode, Gcode, Scode, Gubun, Pubun, Gjisa, Sum(Gsqut) as Gsqut, Sum(Gssum) as Gssum From S1_Ssub Where Gdate>=? and Gdate<=? and Ocode='B' and Scode=? [X/Y/Z] [+ Hcode] [+ Gcode 구간] [+ S_Where1] Group By Hcode, Gcode, Scode, Gubun, Pubun, Gjisa` |
| L421~ | `H1_Ssub` 입출금 sub-query (정산 결합 — 1차에서는 합계 미반환, 후속 C5) | (필드만 0 으로 채워 응답 스키마 유지) |

### 5.3 1차 응답 모델

행 = `(Hcode 본사, Gcode 거래처, Gname 거래처명, Gjisa 지사코드, Goqut, Gosum, Gbqut, Gbsum, Gjqut, Gjsum, Gsusu, Gssum)`. C14 동등성 캡처 대상.

---

## 6. POC 대조

| 패턴 | POC 참조 | C6 재사용 위치 |
|---|---|---|
| `S1_Ssub` GROUP BY 2패스 집계 (메인 + Sg_Csum 합) | [`POC/web/seak80-sample/backend/sobo67_sql.py`](../POC/web/seak80-sample/backend/sobo67_sql.py), [`sobo67_aggregate.py`](../POC/web/seak80-sample/backend/sobo67_aggregate.py) | Sobo61/62 서비스 — 동일 GROUP BY + Python merge |
| EUC-KR 헤더 처리 + `D_Select` (서버 시드) | [`sobo_phase1_sql.py`](../POC/web/seak80-sample/backend/sobo_phase1_sql.py) | C2 `outbound_service.py` 가 이미 같은 패턴 사용 → 그대로 재사용 |
| 컬럼 라벨 한글 매핑 | [`POC/web/seak80-sample/frontend/seak80-column-labels.js`](../POC/web/seak80-sample/frontend/seak80-column-labels.js) | C6 4페이지 모두 `frontend/src/lib/column-labels.ts` 에 추가 |
| 가상 스크롤 그리드 | (POC 없음) | TanStack Table 신설 — `frontend/src/components/data-grid/` |

---

## 7. 1차 컷오프 (Deferral 후보 → DEC 신설)

| 후속 ID(예정) | 항목 | 후속 시나리오 |
|---|---|---|
| DEC-016 | F24/F31/F61/F62 권한키 차단 | C10 |
| DEC-017 | 거래명세서·라벨 인쇄 (Tong20.Srart_21_01 등) | C7 |
| DEC-018 | Tong40 진입점 (장시간 작업 표시 다이얼로그) → 프론트 스피너로 대체. 바코드 진입은 별도 (C8) | C7/C8 |
| (참고) | Sobo62 의 `H1_Ssub` 입출금 합계 — 1차에서는 응답에 0 으로 채움 | C5 (정산) |

---

## 8. 변경 이력

- 2026-04-18 — 최초 작성. 4폼 SELECT 베이스 인용 동결, S1_Memo UPSERT 1차 포함 결정 반영.
