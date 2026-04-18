# C2 (출고 접수) 레거시 흐름 · SQL · POC 대조 매트릭스

> 작성: 2026-04-25 (Phase 1 분석 산출물 — `migration/contracts/outbound_order.yaml` 작성 직전)
> 대상 폼: `TSobo27` ([Subu27.pas](../legacy_delphi_source/legacy_source/Subu27.pas), [Subu27.dfm](../legacy_delphi_source/legacy_source/Subu27.dfm))
> 1차 합격선: 출고 주문 **신규 등록 / 수정 / 취소 / 조회 (CRUD)** — 권한키·바코드·인쇄·물리삭제 후속 (DEC-009 ~ DEC-012)

## 0. 한눈 요약

- 본 폼은 **TADOTable + TDataSource + DBGridEh** 기반 — INSERT/DELETE 는 직접 SQL 이 아니라 데이터셋의 `Append/Post/Delete` 로 ADO 가 자동 생성. 정적 분석에서 `query_catalog.json` 에 INSERT/DELETE 가 **0건** 으로 잡히는 이유.
- 직접 SQL 은 **SELECT 30 + UPDATE 2** (취소 플래그 UPDATE 2건이 핵심 쓰기 경로).
- 핵심 테이블은 **`S1_Ssub` (12회 인용)** — 헤더/라인 분리가 **아니라**, **라인 단위 row 다수 + (Gdate, Hcode, Jubun, Gjisa) 합성키로 한 주문 식별** 패턴으로 보인다 (헤더 테이블 별도 없음).
- 보조 테이블: `G7_Ggeo` (거래처 마스터), `G1_Ggeo` (지사 마스터), `G4_Book` (제품 마스터), `T1_Gbun`/`H2_Gbun` (분류/일자), `S4_Ssub`/`T4_Ssub` (가입고/합계).
- `Sg_Csum` (`porting-screens.json` 의 db_impact 추정) 은 **본 폼에서 직접 사용되지 않음** — POC `sobo67_sql.py` 분석 결과 Sg_Csum 은 **Sobo67 (집계 화면) 에서만 사용되는 사전 집계 테이블**. C2 1차 contract 의 데이터 모델은 **S1_Ssub 단일 테이블 중심** 으로 재정의 필요.

## 1. 폼 구조와 이벤트 (Subu27.pas)

| 라인 | 핸들러 | 역할 (1차 매핑) |
|---|---|---|
| L139 | `FormActivate` | 데이터셋 초기화 (`nSqry/mSqry/tSqry` = `T2_Sub71/72`, `T4_Sub81`) |
| L147 | `FormShow` | Edit101 = 오늘 날짜 (`yyyy.mm.dd`) |
| L154 | `FormClose` | 데이터셋 OpenExit (close + free) |
| L327 | `Button101Click` | **조회 (날짜+거래처 범위)** → 거래처 마스터 + S1_Ssub 카운트 (0/1/2 상태별) |
| L553 | `Button201Click` | **명세 채움** — G7/G1/G4 마스터에서 거래처명/제품명 LOOKUP 후 Post |
| L640 | `Button301Click` | **취소** — `UPDATE S1_Ssub SET Yesno='2', Time3=now()` |
| L663 | `Button401Click` | Code5 일괄 ON/OFF (단순 표시 토글) |
| L690 | `Button501Click` | **합계 화면 (tSqry)** — 출고 합계 N개 그리드 (인쇄용 사전 단계) |
| L984 | `Button502Click` | 후속 합계 (변형) |
| L1282 | `Button509Click` | 합계 grand total |
| L1326~ | `Edit10x KeyDown/KeyPress` | 입력 검증 + 다음 필드 포커스 |
| L1431~ | `DBGrid101 KeyDown/KeyPress` | 그리드 행 편집/삭제 단축키 |
| L1534 | `Timer1Timer` | 주기 자동 새로고침 (`Button401` 의 RadioButton6) |
| L1570 | `DateEdit1*` | 일자 picker → Edit101 변환 |
| L1580~ | `Button701/702Click` | 인쇄·바코드 트리거 (1차 비활성 — DEC-010/011) |

## 2. 핵심 SQL 인용 (정적 분석 결과)

### 2.1 SELECT (조회·LOOKUP)

| 라인 | 테이블 | SQL (앞부분) | 1차 매핑 |
|---|---|---|---|
| L351/354 | `G7_Ggeo` | `Select Gcode,Gname,Gtel1,Gtel2 From G7_Ggeo Where ...` | 거래처 마스터 자동완성 → `GET /api/v1/masters/customers?q=` |
| L385/391 | `S1_Ssub` | `Select Hcode,Count(*) From S1_Ssub Where ... Group By Hcode` | 거래처별 라인 수 → `GET /api/v1/outbound/orders?summary=by_customer` |
| L452/464 | `S1_Ssub` | `Select Hcode,Gcode,Jubun,Gjisa,Count(*) From S1_Ssub Where ... Group By Hcode,Gcode,Jubun,Gjisa` | **합성키 단위 카운트** → 한 주문 = (Hcode,Gcode,Jubun,Gjisa) 묶음 |
| L562/577 | `S1_Ssub` | `Select * From S1_Ssub Where ...` | 라인 상세 → `GET /api/v1/outbound/orders/{key}` |
| L586/601 | `G7_Ggeo` | `Select Gname From G7_Ggeo Where ...` | 거래처 이름 lookup |
| L592/607 | `G1_Ggeo` | `Select Gname From G1_Ggeo Where ...` | 지사 이름 lookup |
| L609/624 | `G4_Book` | `Select Gname,Gjeja From G4_Book Where ...` | 제품 이름·저자 lookup |
| L697/713 | `S1_Ssub` | `Select Gcode,Gjisa,Sum(Gsqut) From S1_Ssub Where ... Group By` | 합계 (Button501) |
| L1293/1315 | `S1_Ssub JOIN G4_Book` | `Select S.Hcode,S.Gcode,S.Gjisa,S.Jubun,S.Bcode,Y.Grat8,S.Gsqut From S1_Ssub S, G4_Book Y` | 인쇄용 라인 + 등급 (1차 비활성) |

### 2.2 UPDATE (쓰기)

| 라인 | SQL | 1차 매핑 |
|---|---|---|
| L628 | `UPDATE S1_Ssub SET Yesno='@Yesno', Time3=now() WHERE ...` (Yesno='1' 처리완료) | 1차 미사용 (베타 처리 흐름) |
| L643 | `UPDATE S1_Ssub SET Yesno='@Yesno', Time3=now() WHERE ... Yesno='1'` (→ Yesno='2' 취소) | **`PATCH /api/v1/outbound/orders/{key}/cancel`** |

L643 의 인용 (Subu27.pas):

```
640|procedure TSobo27.Button301Click(Sender: TObject);
641|begin
642|  if RadioButton2.Checked<>True Then begin
643|    Sqlen := 'UPDATE S1_Ssub SET Yesno=''@Yesno'' ,Time3= now()'+
644|    ' WHERE '+D_Select+
645|    ' Gdate=''@Gdate'' and Gubun=''@Gubun'' and '+
646|    ' Scode=''@Scode'' and Yesno=''@Yesoo'' and '+
647|    ' Ocode=''@Ocode'' and Hcode=''@Hcode'' ';
648|
649|    Translate(Sqlen, '@Gdate', mSqry.FieldByName('Gdate').AsString);
650|    Translate(Sqlen, '@Gubun', '출고');
651|    Translate(Sqlen, '@Scode', 'X'   );
652|    Translate(Sqlen, '@Yesoo', '1'   );
653|    Translate(Sqlen, '@Ocode', 'B'   );
654|    Translate(Sqlen, '@Hcode', mSqry.FieldByName('Gcode').AsString);
655|    Translate(Sqlen, '@Yesno', '2'   );
```

→ **취소** = (Gdate, Gubun='출고', Scode='X', Ocode='B', Hcode=거래처) 묶음의 모든 라인 Yesno 를 '1'(처리)→'2'(취소).

### 2.3 INSERT / DELETE (DataSet 자동 생성)

- 정적 SQL 0건. 실제로는 `mSqry.Append; mSqry.FieldByName(...).AsString := ...; mSqry.Post;` 패턴 (예: L365~L373) 으로 ADO 가 `INSERT INTO S1_Ssub (...) VALUES (...)` 자동 생성.
- 1차 contract 에서는 **명시적 INSERT/UPDATE/DELETE SQL 을 작성**(파라미터 바인딩 `%s`) — POC 의 SELECT 패턴을 참조하되 INSERT 는 신규 작성.

## 3. 트랜잭션 경계

- Subu27.pas 에서 `BeginTrans/CommitTrans/RollbackTrans` **직접 호출 없음** — 데이터셋이 row 단위로 commit (default autocommit).
- **포팅 시 강화 (DIP)**: 한 주문(라인 N개) 의 INSERT/UPDATE/DELETE 는 **단일 트랜잭션** 으로 묶음. `outbound_service.create_order` 에서 `connection.begin()` ~ `connection.commit()` 명시. 라인 1개 실패 시 전체 롤백 → TC-OUT-005.

## 4. 도메인 모델 결정 (1차)

### 4.1 한 주문의 식별자 (composite key)

```
order_key = (Gdate, Hcode, Jubun)
```
- `Gdate`: 'YYYY.MM.DD' 문자열 (Subu27 도 문자열로 저장).
- `Hcode`: 거래처 코드 (`Subu27.mSqry.Gcode` 가 Hcode 매핑됨 — L654 인용).
- `Jubun`: 주문 단위 코드 (전표 번호 추정).
- (선택) `Gjisa`: 지사 코드. 1차에서는 합성키 일부로만 사용, URL path 외부 노출 없음.

REST 식별자는 합성키를 단일 문자열로 직렬화: `{Gdate}|{Hcode}|{Jubun}` 또는 별도 surrogate id 도입. **1차는 합성키 직렬화** 채택 (DB 스키마 변경 없음, OCP).

### 4.2 라인 row (`S1_Ssub` 단일 테이블)

| 컬럼 | 타입(추정) | 용도 |
|---|---|---|
| Gdate | varchar(10) | 일자 (키) |
| Hcode | varchar | 거래처 (키) |
| Jubun | varchar | 전표 (키) |
| Gjisa | varchar | 지사 (옵션) |
| Gcode | varchar | 제품 코드 (라인) |
| Bcode | varchar | 책 코드 (라인) |
| Gubun | varchar | '출고' 고정 (1차) |
| Ocode | char(1) | 본사/지사 ('B' 지사 1차 가정) |
| Scode | char(1) | 'X' 입고 1차 가정 |
| Yesno | char(1) | 상태: '0' 미처리 / '1' 처리완료 / '2' 취소 |
| Pubun | varchar | 신간/구간 등 |
| Gsqut | int | 수량 |
| Gssum | decimal | 금액 |
| Time3 | datetime | 마지막 수정 시각 (`now()`) |

→ **헤더 정보 (거래처명·일자·합계 등) 는 라인 row 의 메타에서 추출** + 마스터 lookup. 별도 `S1_Header` 테이블 생성 안 함.

### 4.3 1차 acceptance_goal 매핑

| 동작 | SQL | 트랜잭션 |
|---|---|---|
| 신규 등록 | `INSERT INTO S1_Ssub (Gdate, Hcode, Jubun, Gjisa, Gcode, Bcode, Gubun, Ocode, Scode, Yesno, Pubun, Gsqut, Gssum, Time3) VALUES ...` × N (라인) | BEGIN → N×INSERT → COMMIT |
| 수정 | (라인 추가) INSERT × M / (라인 수정) UPDATE × U / (라인 삭제) DELETE × D — diff 기반 | BEGIN → 모두 → COMMIT |
| 취소 | `UPDATE S1_Ssub SET Yesno='2', Time3=now() WHERE Gdate=%s AND Hcode=%s AND Jubun=%s` | 단일 UPDATE (autocommit OK) |
| 조회 (목록) | `SELECT Gdate, Hcode, Jubun, COUNT(*) AS lines, SUM(Gsqut) AS qty, SUM(Gssum) AS amount FROM S1_Ssub WHERE Gdate >= %s AND Gdate <= %s [AND Hcode = %s] [AND Yesno != '2'] GROUP BY Gdate, Hcode, Jubun ORDER BY Gdate DESC, Hcode LIMIT %s OFFSET %s` | 읽기 |
| 조회 (상세) | `SELECT * FROM S1_Ssub WHERE Gdate=%s AND Hcode=%s AND Jubun=%s ORDER BY Gcode` | 읽기 |

## 5. POC 대조 매트릭스 (`POC/web/seak80-sample/backend/`)

| 영역 | 본 분석 (Subu27.pas) | POC | 차이 / 결정 |
|---|---|---|---|
| **출고 라인 SELECT** | `Select * From S1_Ssub Where ... Order By Gcode` (L562) | `sobo67_sql.py: build_sobo67_detail_pymysql` — `SELECT Bcode,Gdate,Scode,Gubun,Pubun,Hcode, SUM(Gsqut), SUM(Gssum), MAX(b.Gname) FROM S1_Ssub s LEFT JOIN G4_Book b ON ... WHERE ... GROUP BY ...` | POC 는 **집계 화면용** (Sobo67) — C2 의 상세는 GROUP BY 없이 라인 단위 그대로. POC 의 G4_Book LEFT JOIN 패턴은 **마스터 자동 채움** 에 차용. |
| **거래처 마스터** | `Select Gcode,Gname,Gtel1,Gtel2 From G7_Ggeo Where ...` (L351) | (POC 미수록 — `phase2_masters_sql.py` 도 G7 직접 없음) | POC 미참조. Subu27 SELECT 그대로 파라미터화. |
| **WHERE 전치 prefix** | `D_Select` 변수 (Delphi) — 거래처별 추가 필터 | `servers.yaml: d_select_sql` 필드 → `D_Select` 동등 (예: `` `Check`=0 and ``) | **본 포팅은 1차에서 D_Select 채택 안 함**. 모든 사용자 동등(DEC-009) 이므로 추가 필터 불필요. (후속 권한 사이클에서 화이트리스트 DSL 로 재설계 — plan §4 위험 메모) |
| **Ocode/Scode 분기** | `Ocode='B' and Scode='X'` 고정 (1차 출고만) | `sobo67: ocode_like_for_mode('hq'→'%A%','지사'→'%B%')` | 1차 contract 는 **Ocode='B' (지사 출고) 고정**, hq/지사 모드 분기는 후속 (DEC-009 권한 일반화 시) |
| **취소 (Yesno)** | `UPDATE S1_Ssub SET Yesno='2', Time3=now() WHERE ...` (L643) | (POC 미구현 — read-only POC) | POC 차용 불가. Subu27 인용을 **파라미터 바인딩 `%s` 로 재작성** 후 contract `SQL-OUT-5-CANCEL` 으로 등록. |
| **PyMySQL 호환** | (정적 분석 N/A) | `pymysql_compat.py`: CP949↔UTF-8 디코더, MySQL 3.x compat | 1차에서는 도서물류관리프로그램의 기존 connection (auth_service `get_connection_for_server`) 재사용. 한글 깨짐 발견 시 POC 의 디코더 헬퍼만 발췌. |
| **다중 서버** | (Subu27 단일 서버) | `ssh_tunnels.py` + `servers.yaml` (4 서버 + SSH 터널) | 도서물류관리프로그램의 server selector 가 동일 모델 — **추가 의존 없이 그대로 사용**. |
| **컬럼 라벨** | (없음) | `frontend/seak80-column-labels.js` (델파이 컬럼 한글 라벨 사전) | T6 에서 `frontend/src/lib/column-labels.ts` 로 그대로 이식 (TS 객체화). S1_Ssub 컬럼 라벨 즉시 차용. |

## 6. 후속 보강 (Open Questions — `legacy-analysis/open-questions.md` 등록 예정)

| ID | 질문 | C2 1차 처리 |
|---|---|---|
| OQ-OUT-1 | `S1_Ssub.Yesno` 의 정확한 enum (`'0'/'1'/'2'/...`) — 운영 데이터 검증 | 1차는 발견된 3종(`0`/`1`/`2`) 만 사용, 그 외 row 는 조회에 포함하되 cancel 로 간주 안 함 |
| OQ-OUT-2 | `Sg_Csum` 이 Sobo27 출고 등록 시점에 자동 갱신되는 트리거가 DB 에 존재하는가 (정적 분석 미감지) | 1차는 `Sg_Csum` 갱신 로직 미구현. 운영 검증 후 후속에서 트리거/배치 둘 중 결정 |
| OQ-OUT-3 | 동일 (Gdate, Hcode, Jubun) 합성키의 동시성 — Delphi 는 단일 클라이언트 가정 | 1차는 RDB 단일 트랜잭션만, 분산 락 없음. 동시 등록 충돌 시 INSERT 중복 키로 오류 (UI 재시도) |
| OQ-OUT-4 | `Gjisa` 가 합성키 일부인지 메타인지 (Subu27 L452/464 GROUP BY 에 포함) | 1차는 메타로 처리 (URL key 미포함). 후속 운영 검증 후 합성키 승격 가능 |

## 7. Contract 입력 사양 (T3 작성 직전 메모)

- `inputs.order_header`:
  - `gdate: str` (YYYY-MM-DD, 입력 시 'YYYY.MM.DD' 변환 후 저장)
  - `hcode: str` (거래처 코드, 필수)
  - `jubun: str` (전표 번호, 신규 시 서버에서 자동 채번 또는 클라이언트 제공)
  - `gjisa?: str`
  - `gubun: '출고'` (고정)
  - `ocode: 'B'` (1차 고정)
  - `scode: 'X'` (1차 고정)
- `inputs.order_lines[]`:
  - `gcode: str`, `bcode: str`, `pubun?: str`, `gsqut: int`, `gssum: int`
- `output (POST)`:
  - `order_key: { gdate, hcode, jubun }`, `lines: int`, `qty: int`, `amount: int`, `created_at`
- `output (GET 목록)`:
  - 페이지 + 행: `[{ order_key, customer_name, lines, qty, amount, status }]` (status = `active`/`cancelled` ← Yesno 매핑)

---

*다음 단계*: 본 매트릭스를 입력으로 **`migration/contracts/outbound_order.yaml` v1.0.0** 작성 (T3) → **`migration/test-cases/outbound_order.json`** (T4).
