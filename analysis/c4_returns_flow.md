# C4 (반품 처리) 레거시 흐름 · SQL · 데이터 모델 분석

> 작성: 2026-04-19 (Phase 1 분석 산출물 — `migration/contracts/return_receipt.yaml v1.0.0` 작성 직전)
> 대상 폼: `TSobo23` (메인) + `TSobo23_1` (라인 다이얼로그 — 본/chul_05 + chul_08 자료불러오기) + `TSobo24` (재생) + `TSobo25` (해체) + `TSobo51` (변경) + `TSobo55` (일별 보고서) + `TSobo40` (패스워드 다이얼로그)
> 1차 합격선: 반품 **CRUD + 3분기 처리 (재생/해체/변경) + 일일 보고 + 패스워드 게이트 + 임포트** — 인쇄·바코드·기간 보고서·폐기 원장은 후속

## 0. 한눈 요약

- C2 (출고) 와 동일한 **S1_Ssub 단일 테이블 + 합성키** 모델 — 별도 반품 테이블 없음. **Gubun='반품'** 으로 출고와 구분.
- 라인 단위 트랜잭션은 모두 **`Base01.pas` 의 헬퍼** 에 위임 (T2_Sub31/41/51, T5_Sub11). C4 의 화면 .pas 는 SELECT 와 메모 UPSERT 만 직접 보유.
- **3분기 처리 (재생/해체/변경) 는 Scode 컬럼 값 분기**:
  - **Subu24 재생**: `Gdate` 키 + Scode='2' (정품 환원 후 삭제)
  - **Subu25 해체**: **`Bdate` 키** (반품 입고일!) + Scode='3' (해체 후 삭제)
  - **Subu51 변경**: `Sv_Ghng` (변경 이력) + `Sg_Csum` (집계 재고) 동기 갱신
- **메모 UPSERT 패턴 (Subu23 L1213/1257)** 는 C6 의 S1_Memo 패턴과 동일 — 재사용 가능.
- **임포트 (Subu23_1 chul_08)** 는 외부 자료 → 미리보기 그리드 → 일괄 INSERT 패턴. `_import_*` 별도 트랜잭션.
- **패스워드 다이얼로그 (Subu40)** 는 SQL 호출 0건 — 단순 UI 모달. 검증은 별도 보안 모듈 (호출자가 결과를 받아 본인의 SQL 실행 권한 결정).

## 1. 폼별 이벤트 핸들러 매트릭스

### 1.1 Sobo23 (반품 메인)

| 라인 | 핸들러 | 역할 (1차 매핑) |
|---|---|---|
| L139 | `FormActivate` | 데이터셋 초기화 (`nSqry/mSqry/tSqry`) |
| L147 | `FormShow` | Edit101 = 오늘 날짜 (`yyyy.mm.dd`) |
| L154 | `FormClose` | 데이터셋 OpenExit |
| L372/388 | `Button101Click` / `dxButton1.OnClick` | **조회**: `SELECT * FROM S1_Ssub WHERE D_Select+...+Gubun='반품'` |
| L421 | (lookup) | `SELECT Gname,Gjeja FROM G4_Book WHERE Gcode=? AND Hcode=?` |
| L471~497 | (lookup) | `SELECT Grat1~6 FROM G1_Ggeo / G4_Book` (할인율 자동 채움) |
| L550 | `Button501Click` (메모 로드) | `SELECT Gbigo,Sbigo,Gtel1,Gtel2,Gname,Gpost FROM S1_Memo` |
| L758/776/826/844 | (Idnum 채번) | `SELECT Max(Idnum) FROM S1_Ssub` (라인 번호 자동) |
| L1195 | (메모 존재 검사) | `SELECT Gbigo FROM S1_Memo` |
| L1213 | (메모 UPDATE) | `UPDATE S1_Memo SET Gbigo=?, Sbigo=?, Gtel1=?, ...` |
| L1257 | (메모 INSERT) | `INSERT INTO S1_Memo ...` (UPSERT 패턴) |
| L1305/1328 | (거래처 채움) | `SELECT Gname,Gadd1,Gadd2,Gtel1,Gtel2,Gposa FROM G1_Ggeo` |

라인 단위 INSERT/UPDATE/DELETE 는 본 폼이 **`Base10.T2_Sub31AfterDelete/BeforePost`** 호출로 위임 (Base01.pas L5113~5239).

### 1.2 Sobo23_1 (라인 다이얼로그 — 본/chul_05)

대부분의 SQL 은 메인 폼과 공유. 변형별 핵심 차이는 dfm 픽셀 좌표·SQL 의 지점 코드 (DEC-028 §3 "버리는 정보").

### 1.3 Sobo23_1_chul08 (자료불러오기)

별도 폼 — 외부 자료 임포트 다이얼로그. 핵심 흐름:
1. `dxButton1.OnClick` ('불러오기') → 외부 데이터 (CSV/엑셀/타 시스템) 파싱
2. 미리보기 그리드 (DBGrid101 10 컬럼: JUBUN/GCODE/GNAME/BCODE/BNAME/GSQUT/GDANG/GSSUM/CODE1/CODE2) 갱신
3. CODE1 (불능 사유) / CODE2 (완료) 컬럼 표시
4. 일괄 INSERT INTO S1_Ssub (라인별 트랜잭션)

### 1.4 Sobo24 (재생) - T2_Sub41 위임

| 라인 (Subu24.pas) | 핸들러 | 역할 |
|---|---|---|
| L298 | (조회) | `SELECT * FROM S1_Ssub WHERE D_Select+...+Gubun='재생'` |
| L317 | (lookup) | `SELECT Gname,Gjeja FROM G4_Book` |
| L509 | DBGrid101.OnKeyDown (Delete) | `Base10.T2_Sub41AfterDelete(nSqry)` 호출 |

### 1.5 Sobo25 (해체) - T2_Sub51 위임

| 라인 (Subu25.pas) | 핸들러 | 역할 |
|---|---|---|
| L299 | (조회) | `SELECT ID, **Bdate as Gdate**, Hcode, Gcode, Bcode, Gsqut, Gdang, Gssum, Gbigo FROM S1_Ssub WHERE D_Select+...+Gubun='해체'` ⭐ Bdate alias 키 |
| L319 | (lookup) | `SELECT Gname,Gjeja FROM G4_Book` |
| L512 | DBGrid101.OnKeyDown (Delete) | `Base10.T2_Sub51AfterDelete(nSqry)` 호출 |

### 1.6 Sobo51 (변경) - T5_Sub11 위임 + Sv_Ghng

| 라인 (Subu51.pas) | 핸들러 | 역할 |
|---|---|---|
| L299 | (조회) | `SELECT * FROM **Sg_Csum** WHERE D_Select+...` ⭐ S1_Ssub 가 아닌 Sg_Csum 직접 조회 |
| L482/648/718 | (변경 이력 검사) | `SELECT Max(Gdate) as Gdate FROM Sv_Ghng WHERE ...` |
| L539 | DBGrid101.OnKeyDown (Delete) | `Base10.T5_Sub11AfterDelete(nSqry)` 호출 |
| L620 | (lookup) | `SELECT Gcode,Gname FROM G4_Book` |

### 1.7 Sobo55 (일별 보고서)

| 라인 (Subu55.pas) | 핸들러 | 역할 |
|---|---|---|
| L326 | (마스터 그리드) | `SELECT Hcode, Count(Hcode), Sum(Gsqut) as Gsqut, Sum(Gssum) as Gssum FROM S1_Ssub WHERE D_Select+...+Gubun='반품' GROUP BY Hcode LIMIT 0,10000` |
| L353 | (디테일 그리드) | `SELECT * FROM S1_Ssub WHERE D_Select+...+Gubun='반품' AND Hcode=? LIMIT 0,10000` |
| L397/404/411/418/425/433 | (lookup) | `SELECT Gname FROM G7/G1/G5_Ggeo / G4_Book` |

### 1.8 Sobo40 (패스워드)

SQL 호출 0건 — 별도 보안 모듈 (`Base10.VerifyPassword(Edit101.Text)` 추정) 호출. 모던에서는 백엔드 `POST /api/v1/audit/password-verify` 로 분리.

## 2. 핵심 트랜잭션 SQL (Base01.pas 본문 분석)

### 2.1 T2_Sub41AfterDelete (Subu24 재생) — Base01.pas L5251~5294

```pascal
if D_Select='' then begin
  Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and Gdate=''@Gdate''';
end else begin
  Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and Gdate=''@Gdate''';
  Translate(Sqlen, '@Scode', '2');  // soft delete
end;
```

→ **D_Select 비었을 때 (전사 사용자) 물리 삭제, 권한 필터 있을 때 (지점 사용자) Scode='2' soft delete**.

INSERT (T2_Sub41BeforePost L5295~5371):
```sql
INSERT INTO S1_Ssub (Gdate, Scode, Gcode, Hcode, Ocode, Bcode,
  Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang,
  Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa, Time1)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, now())
```

UPDATE (L5373~5423):
```sql
UPDATE S1_Ssub SET
  Gdate=?, Scode=?, Gcode=?, Hcode=?, Ocode=?, Bcode=?,
  Gubun=?, Jubun=?, Pubun=?, Gbigo=?, Gsqut=?, Gdang=?,
  Grat1=?, Gssum=?, Qsqut=?, Jeago=?, Yesno=?, Gjisa=?, Time2=now()
WHERE ID=? AND Gdate=?
```

> **Gsqut/Gssum 부호 반전** (`AfterScroll`): `Gsqut := -T2_Sub41Gsqut.AsFloat;` — 재생은 정품 재고 +N, 반품 재고 -N (이중 기입).

### 2.2 T2_Sub51AfterDelete (Subu25 해체) — Base01.pas L5398~5418

```pascal
if D_Select='' then begin
  Sqlen := 'DELETE FROM S1_Ssub WHERE ID=@ID and **Bdate**=''@Gdate''';
end else begin
  Sqlen := 'UPDATE S1_Ssub SET Scode=''@Scode'' WHERE ID=@ID and **Bdate**=''@Gdate''';
  Translate(Sqlen, '@Scode', '3');  // 해체 soft delete (Subu24 의 '2' 와 다름!)
end;
```

INSERT (T2_Sub51BeforePost L5424~5475):
```sql
INSERT INTO S1_Ssub (**Bdate**, Scode, Gcode, Hcode, Ocode, Bcode,
  Gubun, Jubun, Pubun, Gbigo, Gsqut, Gdang,
  Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa, Time1)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, Time1)  -- ⚠️ Time1 미설정 (버그 추정)
```

UPDATE (L5478~5520):
```sql
UPDATE S1_Ssub SET
  **Bdate**=?, Scode=?, Gcode=?, Hcode=?, Ocode=?, Bcode=?,
  Gubun=?, Jubun=?, Pubun=?, Gbigo=?, Gsqut=?, Gdang=?,
  Grat1=?, Gssum=?, Qsqut=?, Jeago=?, Yesno=?, Gjisa=?, Time2=now()
WHERE ID=? AND **Bdate**=?
```

> **Bdate (반품 입고일) 가 키** — Subu24/51 의 Gdate 와 의미 다름. 모던에서는 `return_key.bdate` 와 `return_key.gdate` 두 종류 존재. → SQ-RT-2.

### 2.3 T5_Sub11AfterDelete (Subu51 변경) — Base01.pas L6805~ + _Sv_Ghng_ L8731~

핵심 위임 — `_Sv_Ghng_(St0, St1, St2, St3, Field1, Field2, Field3: String; Sq1, Sq2: Double)` 헬퍼 호출:

```pascal
// L8760
Sqlen := 'UPDATE Sv_Ghng SET '+ Field1 +'=? , '+ Field2 +'=? , '+ Field3 +'=? WHERE Gdate=? AND ...';
// L8784
Sqlen := 'INSERT INTO Sv_Ghng (Gdate, Hcode, Gcode, Bcode, '+ Field1 +', '+ Field2 +', '+ Field3 +') VALUES (...)';
```

호출 패턴 (L9534~9589):
```pascal
_Sv_Ghng_(St0, St1, St2, St6, 'Gjqut', 'Gsqut', 'Gosum', Sq1, Sq2);  // 변경 (직접)
_Sv_Ghng_(St0, St1, St2, St6, 'Gbqut', 'Gsqut', 'Gbsum', Sq1, Sq2);  // 변경 (간접 - 비품)
```

→ **Sv_Ghng = 재고 변경 이력 테이블** (Field1/2/3 컬럼명을 동적 치환 — 변경 종류 분기). Sg_Csum 도 동기 갱신.

### 2.4 메모 UPSERT (Subu23.pas L1195~1290) — C6 패턴 재사용

```pascal
// L1195: 존재 검사
Sqlen := 'SELECT Gbigo FROM S1_Memo WHERE D_Select+ Gdate=? AND Hcode=? AND Jubun=?';
if Found then begin
  // L1213
  Sqlon := 'UPDATE S1_Memo SET Gbigo=?, Sbigo=?, Gtel1=?, Gtel2=?, Gname=?, Gpost=?, Time2=now() WHERE ...';
end else begin
  // L1257
  Sqlon := 'INSERT INTO S1_Memo (Gdate, Hcode, Jubun, Gbigo, Sbigo, Gtel1, Gtel2, Gname, Gpost, Time1) VALUES (...)';
end;
```

→ C6 의 `transactions_service.upsert_memo` 와 **완전히 동일** — 재사용 가능. 모던에서는 backend `returns_service.upsert_memo` 가 동일 코드를 호출 (DRY).

## 3. SQL 카탈로그 (SQL-RT-1 ~ SQL-RT-N)

| ID | SQL | 위치 (legacy) | 모던 매핑 |
|---|---|---|---|
| **SQL-RT-1-LIST** | `SELECT Gdate, Hcode, Jubun, COUNT(*), SUM(Gsqut), SUM(Gssum) FROM S1_Ssub WHERE Gubun='반품' AND Gdate >= ? AND Gdate <= ? [AND Hcode=?] [AND Yesno != '2'] GROUP BY Gdate, Hcode, Jubun ORDER BY Gdate DESC LIMIT ? OFFSET ?` | Subu23.pas L372 (파생) | `GET /api/v1/returns?from&to&hcode&include_cancelled` |
| **SQL-RT-2-DETAIL** | `SELECT * FROM S1_Ssub WHERE Gdate=? AND Hcode=? AND Jubun=? AND Gubun='반품' ORDER BY Idnum` | Subu23.pas L388 | `GET /api/v1/returns/{return_key}` |
| **SQL-RT-3-INSERT** | `INSERT INTO S1_Ssub (Gdate, Scode, Gcode, Hcode, Ocode, Bcode, Gubun='반품', Jubun, Pubun, Gbigo, Gsqut, Gdang, Grat1, Gssum, Qsqut, Jeago, Yesno, Gjisa, Time1) VALUES (...)` | Base01.pas L4839 (T2_Sub31) | `POST /api/v1/returns` (라인 N개 = 단일 트랜잭션) |
| **SQL-RT-4-UPDATE** | `UPDATE S1_Ssub SET ..., Time2=now() WHERE ID=? AND Gdate=?` | Base01.pas L4897 | `PATCH /api/v1/returns/{return_key}` |
| **SQL-RT-5-CANCEL** | `UPDATE S1_Ssub SET Yesno='2', Time3=now() WHERE Gdate=? AND Hcode=? AND Jubun=? AND Yesno='1'` | (C2 패턴 차용 — Subu27.pas L643 동등) | `PATCH /api/v1/returns/{return_key}/cancel` (DEC-012 soft delete) |
| **SQL-RT-6-MEMO-EXIST** | `SELECT Gbigo FROM S1_Memo WHERE Gdate=? AND Hcode=? AND Jubun=?` | Subu23.pas L1195 | (UPSERT 의 첫 단계) |
| **SQL-RT-7-MEMO-UPDATE** | `UPDATE S1_Memo SET Gbigo=?, Sbigo=?, Gtel1=?, Gtel2=?, Gname=?, Gpost=?, Time2=now() WHERE ...` | Subu23.pas L1213 | `PATCH /api/v1/returns/{return_key}/memo` (action=updated) |
| **SQL-RT-8-MEMO-INSERT** | `INSERT INTO S1_Memo (Gdate, Hcode, Jubun, Gbigo, Sbigo, Gtel1, Gtel2, Gname, Gpost, Time1) VALUES (...)` | Subu23.pas L1257 | `PATCH /api/v1/returns/{return_key}/memo` (action=inserted) |
| **SQL-RT-9-REGEN-LIST** | `SELECT * FROM S1_Ssub WHERE Gubun='재생' AND Gdate >= ? AND Gdate <= ? [AND Hcode=?]` | Subu24.pas L298 | `GET /api/v1/returns/dispose/regenerable?from&to&hcode` |
| **SQL-RT-10-REGEN-INSERT** | `INSERT INTO S1_Ssub (Gdate, ..., Gubun='재생', ..., Time1=now())` (Gsqut/Gssum 부호 반전) | Base01.pas L5295 (T2_Sub41) | `POST /api/v1/returns/dispose/regen` (단일 트랜잭션) |
| **SQL-RT-11-REGEN-DELETE** | `UPDATE S1_Ssub SET Scode='2' WHERE ID=? AND Gdate=?` | Base01.pas L5267 | (롤백 — DELETE 대체) |
| **SQL-RT-12-DISASS-LIST** | `SELECT ID, Bdate as Gdate, Hcode, Gcode, Bcode, Gsqut, Gdang, Gssum, Gbigo FROM S1_Ssub WHERE Gubun='해체' AND Bdate >= ? AND Bdate <= ?` ⭐ Bdate 키 | Subu25.pas L299 | `GET /api/v1/returns/dispose/disassemblable?from&to&hcode` |
| **SQL-RT-13-DISASS-INSERT** | `INSERT INTO S1_Ssub (**Bdate**, ..., Gubun='해체', ...)` | Base01.pas L5424 (T2_Sub51) | `POST /api/v1/returns/dispose/disassemble` (단일 트랜잭션) |
| **SQL-RT-14-DISASS-DELETE** | `UPDATE S1_Ssub SET Scode='3' WHERE ID=? AND Bdate=?` ⭐ Bdate 키 + Scode='3' | Base01.pas L5410 | (롤백 — DELETE 대체) |
| **SQL-RT-15-CHANGE-LIST** | `SELECT * FROM Sg_Csum WHERE D_Select+...` ⭐ Sg_Csum 직접 조회 | Subu51.pas L299 | `GET /api/v1/returns/change/changeable?from&to&hcode` |
| **SQL-RT-16-CHANGE-HIST-MAX** | `SELECT Max(Gdate) as Gdate FROM Sv_Ghng WHERE ...` | Subu51.pas L482/648/718 | (변경 이력 검사 — 동시 변경 충돌 방지) |
| **SQL-RT-17-CHANGE-SVGHNG-UPSERT** | `INSERT INTO Sv_Ghng (...)` / `UPDATE Sv_Ghng SET Field1=?, Field2=?, Field3=? WHERE ...` | Base01.pas L8784 / L8760 (`_Sv_Ghng_`) | `POST /api/v1/returns/change` (단일 트랜잭션 — Sv_Ghng + Sg_Csum 동기) |
| **SQL-RT-18-CHANGE-SGCSUM-SYNC** | `UPDATE Sg_Csum SET Gosum/Gbsum=? WHERE Hcode=? AND Bcode=? AND ...` | Base01.pas L4932 (T2_Sub21 패턴) | (Sv_Ghng 트랜잭션 안에서 동기 호출) |
| **SQL-RT-19-DAILY-MASTER** | `SELECT Hcode, Count(Hcode), Sum(Gsqut), Sum(Gssum) FROM S1_Ssub WHERE Gubun='반품' AND Gdate >= ? AND Gdate <= ? GROUP BY Hcode LIMIT 0,10000` | Subu55.pas L326 | `GET /api/v1/returns/reports/daily?from&to&gcode&hcode` (마스터 응답) |
| **SQL-RT-20-DAILY-DETAIL** | `SELECT * FROM S1_Ssub WHERE Gubun='반품' AND Gdate=? AND Hcode=? LIMIT 0,10000` | Subu55.pas L353 | (마스터 행 클릭 시 디테일 응답 — 같은 endpoint 의 `?detail_for_hcode=` 옵션) |
| **SQL-RT-21-IMPORT-PREVIEW** | (외부 데이터 → 미리보기 그리드 — SQL 없음, 메모리 가공) | Sobo23_1 chul08 | `POST /api/v1/returns/import/preview` (multipart 파일 업로드) |
| **SQL-RT-22-IMPORT-EXEC** | `INSERT INTO S1_Ssub (...) VALUES (...)` × N (라인별, CODE2='완료' 표시) | Sobo23_1 chul08 dxButton1 | `POST /api/v1/returns/import/execute` (preview_id) |
| **SQL-RT-23-AUDIT-VERIFY** | (SQL 없음 — 별도 보안 모듈) | Sobo40 | `POST /api/v1/audit/password-verify` → token 반환 |
| **SQL-RT-24-LOOKUP-CUSTOMER** | `SELECT Gname,Gadd1,Gadd2,Gtel1,Gtel2,Gposa FROM G1_Ggeo WHERE Gcode=? AND Hcode=?` | Subu23.pas L1305/1328 | `GET /api/v1/masters/customers?q=` (C2 재사용) |
| **SQL-RT-25-LOOKUP-BOOK** | `SELECT Gname,Gjeja,Grat1~6 FROM G4_Book WHERE Gcode=? AND Hcode=?` | Subu23.pas L421/497 | `GET /api/v1/masters/products?q=` (C2 재사용) |
| **SQL-RT-26-LOOKUP-DISCOUNT** | `SELECT Grat1,Grat2,Grat3,Grat4,Grat5,Grat6 FROM G1_Ggeo / G4_Book` | Subu23.pas L471~497 | (B-A 자동 채움 — 라인 입력 시 inline) |
| **SQL-RT-27-IDNUM-MAX** | `SELECT Max(Idnum) FROM S1_Ssub WHERE D_Select+...` | Subu23.pas L758/776/826/844 | (라인 채번 — 백엔드 `returns_service._next_idnum`) |

## 4. 트랜잭션 경계 — 모던 강화 (DIP)

레거시는 `Base10.Socket.RunSQL(Sqlon+Sqlen)` 직접 실행 (autocommit, BEGIN/COMMIT 명시 없음).

모던 포팅 시 각 endpoint 의 트랜잭션 경계:

| Endpoint | 트랜잭션 | 이유 |
|---|---|---|
| `POST /returns` | BEGIN → `next_jubun` lock → INSERT 라인 N개 → COMMIT | 라인 1개 실패 시 전체 롤백 (TC-RT-005) |
| `PATCH /returns/{key}` | BEGIN → diff 계산 → 추가/수정/삭제 → COMMIT | 라인 diff 의 원자성 |
| `PATCH /returns/{key}/cancel` | 단일 UPDATE (autocommit OK) | DEC-012 soft cancel |
| `PATCH /returns/{key}/memo` | BEGIN → SELECT 검사 → INSERT/UPDATE → COMMIT | UPSERT 원자성 |
| `POST /returns/dispose/regen` | **AuditPasswordModal token 검증** → BEGIN → INSERT 라인 N개 → COMMIT | 권한 + 원자성 |
| `POST /returns/dispose/disassemble` | **token 검증 + ConfirmDialog** → BEGIN → INSERT 라인 N개 → COMMIT | 권한 + 확인 + 원자성 |
| `POST /returns/change` | **token 검증** → BEGIN → INSERT/UPDATE Sv_Ghng + UPDATE Sg_Csum → COMMIT | 권한 + 변경 이력 + 집계 동기성 |
| `POST /returns/import/execute` | BEGIN → INSERT 라인 N개 → COMMIT (CODE2='완료' 표시) | 임포트 원자성 |
| `POST /audit/password-verify` | (트랜잭션 없음) → bcrypt 비교 → token 발급 + audit_log INSERT | 검증 |

## 5. 도메인 모델 결정 (1차)

### 5.1 한 반품의 식별자 (composite key)

```
return_key = (gdate | bdate, hcode, jubun)
```

- **gdate/bdate 분리**: 일반 반품은 `gdate` 키, 해체(Subu25) 는 `bdate` 키 (반품 입고일). 모던 URL 은 `/returns/{return_key}` 의 `return_key` 가 `{gdate}|{hcode}|{jubun}` 또는 `B|{bdate}|{hcode}|{jubun}` 형태.
- **Hcode**: 거래처 코드.
- **Jubun**: 전표 번호 (서버 자동 채번 또는 클라이언트 제공).

### 5.2 라인 row (`S1_Ssub` — C2 와 동일 + Gubun 분기)

| 컬럼 | 타입 (추정) | C2 (출고) | C4 (반품) |
|---|---|---|---|
| `Gdate` | varchar(10) | 일자 | 일반 반품 일자 |
| `Bdate` | varchar(10) | (미사용) | **해체 일자 (반품 입고일)** ⭐ |
| `Hcode` | varchar | 거래처 (키) | 거래처 (키) |
| `Jubun` | varchar | 전표 (키) | 전표 (키) |
| `Gjisa` | varchar | 지사 (옵션) | 지사 (옵션) |
| `Gcode` | varchar | 제품 코드 (라인) | 제품 코드 (라인) |
| `Bcode` | varchar | 책 코드 (라인) | 책 코드 (라인) |
| `Gubun` | varchar | '출고' 고정 | **'반품' / '재생' / '해체' 분기** ⭐ |
| `Ocode` | char(1) | 'B' (지사) | 'B' (지사) |
| `Scode` | char(1) | 'X' | 'X' / '2' (재생 후 삭제) / '3' (해체 후 삭제) |
| `Yesno` | char(1) | '0'/'1'/'2' | '0'/'1'/'2' (DEC-012) |
| `Pubun` | varchar | 신간/구간 | 동일 |
| `Idnum` | int | 라인 번호 | 라인 번호 (max+1 채번) |
| `Gsqut` | decimal | 수량 | 수량 (재생/해체 시 부호 반전) |
| `Gdang` | decimal | 단가 | 단가 |
| `Grat1` | decimal | 할인율 | 할인율 |
| `Gssum` | decimal | 금액 | 금액 |
| `Qsqut` | int | (보조 수량) | (보조 수량) |
| `Jeago` | int | (재고 표시) | (재고 표시) |
| `Time1` | datetime | INSERT 시각 | 동일 |
| `Time2` | datetime | UPDATE 시각 | 동일 |
| `Time3` | datetime | (취소 시각) | 동일 |

### 5.3 보조 테이블

- **S1_Memo**: 메모 UPSERT (C6 와 동일 — 재사용)
- **Sg_Csum**: 집계 재고 (Subu51 변경 시 동기 갱신)
- **Sv_Ghng**: 변경 이력 (Subu51 의 핵심 — Field1/2/3 동적 컬럼명)
- **G1_Ggeo / G4_Book / G5_Ggeo / G7_Ggeo**: 마스터 lookup (C2 재사용)

## 6. 1차 acceptance_goal 매핑

| 동작 | SQL ID | 트랜잭션 | 게이트 |
|---|---|---|---|
| 반품 신규 등록 | SQL-RT-3 × N (라인) | BEGIN → N×INSERT → COMMIT | (없음 — 일반 사용자 가능) |
| 반품 수정 | SQL-RT-3/4 (diff) | BEGIN → diff → COMMIT | (없음) |
| 반품 취소 | SQL-RT-5 | 단일 UPDATE | (없음 — DEC-012 soft) |
| 반품 조회 (목록) | SQL-RT-1 | 읽기 | (없음) |
| 반품 조회 (상세) | SQL-RT-2 | 읽기 | (없음) |
| 메모 UPSERT | SQL-RT-6 + 7/8 | BEGIN → SELECT + INSERT/UPDATE → COMMIT | (없음) |
| **재생 처리** | SQL-RT-9 + 10 × N | **AuditPasswordModal** → BEGIN → N×INSERT → COMMIT | ⭐ 패스워드 |
| **해체 처리** | SQL-RT-12 + 13 × N | **AuditPasswordModal + ConfirmDialog** → BEGIN → N×INSERT → COMMIT | ⭐ 패스워드 + 확인 |
| **변경 처리** | SQL-RT-15 + 17 + 18 × N | **AuditPasswordModal** → BEGIN → Sv_Ghng + Sg_Csum 동기 → COMMIT | ⭐ 패스워드 |
| 일별 보고서 | SQL-RT-19 + 20 | 읽기 (master + detail) | (없음) |
| 임포트 미리보기 | SQL-RT-21 | (메모리) | (없음) |
| 임포트 실행 | SQL-RT-22 × N | BEGIN → N×INSERT → COMMIT | (없음 — chul_08 한정) |
| 패스워드 검증 | SQL-RT-23 | (트랜잭션 없음) → bcrypt + audit_log | (자체 — 검증 후 token 발급) |

## 7. 후속 보강 (Open Questions — `legacy-analysis/open-questions.md` 등록 예정)

| ID | 질문 | C4 1차 처리 |
|---|---|---|
| **OQ-RT-1** | chul_08 (임프린트) 의 "자료불러오기" 다이얼로그 — 외부 데이터 형식 (CSV/엑셀/타 시스템 API) 미상. 운영팀 확인 필요 | 1차는 **CSV 업로드** 가정 + multipart 엔드포인트 노출. 운영팀 확인 후 형식 추가 |
| **OQ-RT-2** | `S1_Ssub.Bdate` (해체 키) vs `Gdate` (재생 키) 의 정확한 의미 — 운영 데이터 검증 | 1차는 분석 가정대로 (Bdate = 반품 입고일, Gdate = 거래일자) 분리 처리. 검증 결과에 따라 통합 가능성 있음 |
| **OQ-RT-3** | `Sv_Ghng` 의 Field1/2/3 동적 컬럼명 9종 (Giqut/Gsusu/Gosum/Gjqut/Gsqut/Goqut/Gbqut/Gbsum/...) — 각각 의미 카탈로그 필요 | 1차는 변경(Sobo51) 의 핵심 5종만 사용 (Gjqut/Gsqut/Gosum/Gbqut/Gbsum). 나머지는 후속 변경 화면 추가 시 |
| **OQ-RT-4** | Sobo40 패스워드 검증 알고리즘 — 레거시는 평문 비교 추정. 운영 마이그레이션 시점 결정 | 1차는 환경변수 평문 비교 (임시 — DEC-029) → Phase 2 에서 bcrypt + audit_log 정식 구현 |
| **OQ-RT-5** | 동시 변경 (Subu51 의 Sv_Ghng 동시 INSERT) 충돌 처리 — Delphi 는 Max(Gdate) 검사로 회피 | 1차는 DB 유니크 제약 + 충돌 시 409 응답. Sv_Ghng 의 Gdate < 현재 검사를 백엔드에서 강화 |
| **OQ-RT-6** | Subu25 의 INSERT 에서 Time1=Time1 (자기 자신 참조 — Base01.pas L5440 추정 버그) — 정상 동작 확인 필요 | 1차는 `Time1=now()` 로 수정 (모던 백엔드는 명시) |

## 8. C2/C6 와의 재사용 매트릭스

| 영역 | C2 (출고) 재사용 | C6 (조회) 재사용 | C4 (반품) 신규 |
|---|---|---|---|
| `S1_Ssub` 라인 row 모델 | ✅ 그대로 | ✅ 그대로 | + Bdate/Gubun 분기 |
| `S1_Memo` UPSERT 패턴 | — | ✅ 그대로 | ✅ 동일 (returns_service.upsert_memo) |
| 합성키 직렬화 | ✅ 그대로 | ✅ 그대로 | + B 접두사 (해체 키) |
| `next_jubun` 채번 | ✅ 그대로 | — | ✅ 그대로 |
| `CustomerSearchInput` (자동완성) | ✅ 그대로 | — | ✅ 그대로 |
| 마스터 lookup (G1/G4/G7_Ggeo, G4_Book) | ✅ 그대로 | ✅ 그대로 | ✅ 그대로 |
| `DataGridPager` | ✅ 그대로 | ✅ 그대로 | ✅ 그대로 |
| `DataGrid` + legacyId | ✅ 그대로 | ✅ 그대로 | ✅ 그대로 |
| `inboundLineGrid` 패턴 | (C3 신규) | — | ✅ ReturnLineGrid 로 모방 |
| Sg_Csum 동기 갱신 | (출고는 미사용) | — | ⭐ 신규 (변경 트랜잭션) |
| Sv_Ghng 변경 이력 | — | — | ⭐ 신규 (변경 트랜잭션) |
| AuditPasswordModal | — | — | ⭐ 신규 (Sobo40 — 향후 다른 시나리오 재사용 가능) |
| DataImportModal | — | — | ⭐ 신규 (chul_08 — 향후 다른 임포트 화면 재사용 가능) |

## 9. Contract 입력 사양 (T3 작성 직전 메모)

- `inputs.return_header`:
  - `gdate: str` (YYYY-MM-DD, 일반 반품/변경)
  - `bdate?: str` (YYYY-MM-DD, 해체 시)
  - `hcode: str` (거래처 코드, 필수)
  - `jubun?: str` (전표 번호, 신규 시 서버 자동 채번)
  - `gjisa?: str`
  - `gubun: '반품' | '재생' | '해체'` (Phase 1)
  - `ocode: 'B'` (1차 고정)
  - `scode: 'X'` (1차 정상)
- `inputs.return_lines[]`:
  - `gcode: str`, `bcode: str`, `pubun?: str`, `gsqut: int`, `gdang: int`, `grat1?: float`, `gssum: int`
- `inputs.dispose_password_token`:
  - `token: str` (Sobo40 검증 후 발급, 5분 수명, HMAC-SHA256)
- `output (POST/PATCH)`:
  - `return_key: { gdate?: str, bdate?: str, hcode, jubun }`, `lines: int`, `qty: int`, `amount: int`, `created_at`
- `output (GET 목록)`:
  - 페이지 + 행: `[{ return_key, customer_name, lines, qty, amount, status }]` (status = `active`/`cancelled`/`regenerated`/`disassembled`/`changed`)
- `output (일별 보고서)`:
  - `master: [{ gdate, hcode, hname, line_count, total_qty, total_amount }]`
  - `detail: [{ ...all S1_Ssub columns }]` (선택된 master 행의 라인)
  - `kpi: { total_publishers, total_count, total_qty, total_amount }`

---

*다음 단계*: 본 매트릭스를 입력으로 **`migration/contracts/return_receipt.yaml v1.0.0`** 작성 (T3) → **`test/test_c4_returns_phase1.py`** (T4).
