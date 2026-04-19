# C4 반품 처리 Phase 2 — 흐름·SQL 카탈로그 추가

> 작성: 2026-04-19 (Phase 2 분석 산출물 — `migration/contracts/return_receipt.yaml v1.1.0` 갱신 직전)
> Phase 1 흐름 문서: [`c4_returns_flow.md`](c4_returns_flow.md) — SQL-RT-1~27 정의
> 본 문서: SQL-RT-28~40 + Phase 2 추가 흐름 (Sobo34_4/58 + 라인 diff PUT + 롤백 + bcrypt + audit DB + FOR UPDATE + D_Select 헬퍼)

## 0. Phase 2 범위 요약

| 그룹 | 추가 항목 | 관련 SQL-RT | 관련 OQ-RT |
| --- | --- | --- | --- |
| A. 신규 화면 | Sobo34_4 (재고원장 폐기), Sobo58 (기간별 반품 내역서) | SQL-RT-28~33 | OQ-RT-8 |
| B. Phase1 누락 | 라인 diff PUT, 부분 재생/해체, 3분기 롤백 | SQL-RT-34~37 | (Phase 1 누락 회귀) |
| C. 보안 강화 | bcrypt 패스워드, Sv_Ghng FOR UPDATE, audit DB | SQL-RT-38~40 | OQ-RT-4, OQ-RT-5, OQ-RT-9 |
| D. 운영팀 의존 | CSV 형식, Bdate/Gdate, Sv_Ghng Field 9종 | (assume_default) | OQ-RT-1, OQ-RT-2, OQ-RT-3 |
| E. 거버넌스 | D_Select 헬퍼, OQ-RT 번호 통일 | (인터페이스만) | OQ-RT-7 |

## 1. SQL 카탈로그 (SQL-RT-28~40)

### A. 신규 화면 — Sobo34_4 (`/returns/ledger`)

#### SQL-RT-28: 재고원장 마스터 — 도서별 누계
```sql
-- Subu34_4.pas L404 패턴 + Phase 2 반품·폐기·재생·해체 축
SELECT s.Bcode, s.Scode, s.Gubun, s.Pubun,
       Sum(s.Gsqut) AS Gsqut, Sum(s.Gssum) AS Gssum,
       b.Gname AS BookName, b.Gjeja AS Jeja
  FROM S1_Ssub s
  LEFT JOIN G4_Book b ON b.Gcode=s.Bcode AND b.Hcode=s.Hcode
 WHERE <D_Select>
   AND s.Gdate BETWEEN :date_from AND :date_to
   AND s.Gubun IN ('반품','재생','해체','변경','폐기')
   AND ( :hcode = '' OR s.Hcode = :hcode )
   AND ( :bcode = '' OR s.Bcode = :bcode )
   AND s.Yesno = '1'
 GROUP BY s.Bcode, s.Scode, s.Gubun, s.Pubun
 ORDER BY s.Bcode
 LIMIT :limit OFFSET :offset
```

#### SQL-RT-29: 재고원장 디테일 — 일자별 트랜잭션
```sql
-- Subu34_4.pas L1041 패턴 (선택된 Bcode 의 line)
SELECT s.Gdate, s.Gubun, s.Gcode, s.Hcode,
       g.Gname AS Gname,
       s.Giqut, s.Gisum, s.Goqut, s.Gosum,
       s.Gjqut, s.Gjsum, s.Gbqut, s.Gbsum,
       s.Gsqut, s.Gssum
  FROM S1_Ssub s
  LEFT JOIN G1_Ggeo g ON g.Gcode=s.Gcode AND g.Hcode=s.Hcode
 WHERE <D_Select>
   AND s.Gdate BETWEEN :date_from AND :date_to
   AND s.Bcode = :bcode
   AND ( :hcode = '' OR s.Hcode = :hcode )
   AND s.Yesno = '1'
 ORDER BY s.Gdate, s.Idnum
```

#### SQL-RT-30: 재고원장 KPI 합계
```sql
SELECT Count(DISTINCT s.Bcode) AS book_count,
       Count(*) AS line_count,
       Sum(s.Gsqut) AS total_qty,
       Sum(s.Gssum) AS total_amount
  FROM S1_Ssub s
 WHERE <D_Select>
   AND s.Gdate BETWEEN :date_from AND :date_to
   AND s.Gubun IN ('반품','재생','해체','변경','폐기')
   AND s.Yesno = '1'
```

### A. 신규 화면 — Sobo58 (`/returns/period-report`)

#### SQL-RT-31: 기간별 반품 마스터 — 출판사별 누계
```sql
-- Subu58.pas L1xx 패턴
SELECT s.Hcode,
       g.Gname AS Hname,
       Count(*) AS line_count,
       Sum(s.Gsqut) AS sum_qty,
       Sum(s.Gssum) AS sum_amount
  FROM S1_Ssub s
  LEFT JOIN G1_Ggeo g ON g.Gcode=s.Hcode AND g.Hcode=''
 WHERE <D_Select>
   AND s.Gdate BETWEEN :date_from AND :date_to
   AND s.Gubun = '반품'
   AND ( :hcode = '' OR s.Hcode = :hcode )
   AND s.Yesno = '1'
 GROUP BY s.Hcode
 ORDER BY s.Hcode
 LIMIT :limit OFFSET :offset
```

#### SQL-RT-32: 기간별 반품 디테일 — 라인
```sql
SELECT s.Gdate, s.Gcode, s.Hcode, s.Idnum, s.Pubun,
       s.Bcode, b.Gname AS Bname,
       s.Gsqut, s.Gdang, s.Grat1, s.Gssum,
       g.Gname AS Gname
  FROM S1_Ssub s
  LEFT JOIN G4_Book b ON b.Gcode=s.Bcode AND b.Hcode=s.Hcode
  LEFT JOIN G1_Ggeo g ON g.Gcode=s.Gcode AND g.Hcode=s.Hcode
 WHERE <D_Select>
   AND s.Gdate BETWEEN :date_from AND :date_to
   AND s.Hcode = :hcode
   AND s.Gubun = '반품'
   AND s.Yesno = '1'
 ORDER BY s.Gdate, s.Idnum
```

#### SQL-RT-33: 기간별 반품 KPI 합계 (Sobo58 Edit201~204)
```sql
SELECT Count(DISTINCT s.Hcode) AS publisher_count,
       Count(*) AS line_count,
       Sum(s.Gsqut) AS total_qty,
       Sum(s.Gssum) AS total_amount
  FROM S1_Ssub s
 WHERE <D_Select>
   AND s.Gdate BETWEEN :date_from AND :date_to
   AND s.Gubun = '반품'
   AND s.Yesno = '1'
```

### B. Phase 1 누락 보강

#### SQL-RT-34: 라인 diff 수정 (PUT /returns/{key})

레거시는 `Base01.pas` 의 `T2_Sub31AfterDelete/BeforePost` 가 라인별 INSERT/UPDATE/DELETE 위임. Phase 2 는 단일 트랜잭션으로 diff 적용:

```python
# pseudocode
async def update_return_lines(server_id, return_key, lines_new):
    lines_old = await fetch_lines(return_key)  # Idnum keyed dict
    to_insert = [l for l in lines_new if l.idnum not in lines_old]
    to_update = [l for l in lines_new if l.idnum in lines_old and changed(l, lines_old[l.idnum])]
    to_delete = [idnum for idnum in lines_old if idnum not in {l.idnum for l in lines_new}]

    async with begin_transaction(server_id) as tx:
        for ln in to_insert:
            await tx.exec("INSERT INTO S1_Ssub (...) VALUES (...)")
        for ln in to_update:
            await tx.exec("UPDATE S1_Ssub SET ... WHERE Gdate=:gdate AND Hcode=:hcode AND Jubun=:jubun AND Idnum=:idnum")
        for idnum in to_delete:
            await tx.exec("UPDATE S1_Ssub SET Yesno='2' WHERE ... AND Idnum=:idnum")  # 소프트 삭제 (DEC-012)
```

#### SQL-RT-35: 부분 재생/해체 (lines 옵션)

Phase 1 의 `process_regen/disassemble` 는 `rows: list[ProcessRow]` 전체 일괄. Phase 2 는 `lines: list[int] | None` 추가 — None 이면 전체, list 면 해당 Idnum 만:

```sql
-- Phase 2 부분 재생 (선택 라인만)
UPDATE S1_Ssub SET Scode='2', Time2=NOW()
 WHERE <D_Select>
   AND Gdate=:gdate AND Hcode=:hcode AND Jubun=:jubun
   AND Idnum IN (:idnum_list)
   AND Yesno='1' AND Gubun='반품'
```

#### SQL-RT-36: 3분기 롤백 (POST /returns/{key}/rollback)

24h 이내 + audit_token 필수. Scode 를 다시 '1' 로 되돌림. 단, 변경(Sobo51)은 reverse INSERT (DELETE 금지):

```sql
-- 재생/해체 롤백
UPDATE S1_Ssub SET Scode='1', Time2=NOW()
 WHERE <D_Select>
   AND ((Gdate=:gdate) OR (Bdate=:bdate))
   AND Hcode=:hcode AND Jubun=:jubun
   AND Scode IN ('2','3')
   AND Time2 >= NOW() - INTERVAL 24 HOUR

-- 변경(Sobo51) 롤백 = reverse INSERT into Sv_Ghng
INSERT INTO Sv_Ghng (Gdate, Hcode, Gcode, Bcode, <Field1>, <Field2>, <Field3>, Time1, Reason)
 VALUES (NOW(), :hcode, :gcode, :bcode, -:val1, -:val2, -:val3, NOW(), 'rollback')
```

#### SQL-RT-37: 부분 처리 사전 검증 (FOR UPDATE)
```sql
SELECT Gdate, Hcode, Jubun, Idnum, Scode, Yesno, Gsqut, Gssum
  FROM S1_Ssub
 WHERE <D_Select>
   AND ((Gdate=:gdate) OR (Bdate=:bdate))
   AND Hcode=:hcode AND Jubun=:jubun
   AND Idnum IN (:idnum_list)
 FOR UPDATE
```

### C. 보안 강화

#### SQL-RT-38: bcrypt 패스워드 검증 (OQ-RT-4 / OQ-RT-9)

```sql
-- 신규 application_settings.audit_password_hash 컬럼
-- Phase 2 마이그레이션:
ALTER TABLE application_settings
  ADD COLUMN audit_password_hash VARCHAR(255) NULL AFTER value;

-- 패스워드 검증
SELECT audit_password_hash AS hash
  FROM application_settings
 WHERE scope='audit' AND `key`='password'
 LIMIT 1;
-- 백엔드: bcrypt.checkpw(password.encode(), hash.encode())
```

#### SQL-RT-38b: 실패 잠금 (audit_password_attempts)
```sql
CREATE TABLE IF NOT EXISTS audit_password_attempts (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  gcode VARCHAR(64) NOT NULL,
  client_ip VARCHAR(64) NOT NULL,
  scope VARCHAR(64) NOT NULL,
  result ENUM('success','failure','locked') NOT NULL,
  attempted_at DATETIME NOT NULL,
  reason VARCHAR(255) NULL,
  INDEX idx_gcode_ip_time (gcode, client_ip, attempted_at)
) ENGINE=InnoDB CHARSET=utf8mb4;

-- 5회 실패 시 10분 잠금 검사
SELECT COUNT(*) AS failures
  FROM audit_password_attempts
 WHERE gcode=:gcode AND client_ip=:ip
   AND result='failure'
   AND attempted_at >= NOW() - INTERVAL 10 MINUTE;
```

#### SQL-RT-39: Sv_Ghng FOR UPDATE (OQ-RT-5)

Phase 1 의 `process_change` Max(Gdate) 검사 race condition 해결:

```sql
-- 기존 (Phase 1):
SELECT Max(Gdate) AS Gdate FROM Sv_Ghng WHERE <D_Select> AND Hcode=:hcode AND Gcode=:gcode AND Bcode=:bcode;
-- → Phase 2:
SELECT Max(Gdate) AS Gdate
  FROM Sv_Ghng
 WHERE <D_Select>
   AND Hcode=:hcode AND Gcode=:gcode AND Bcode=:bcode
 FOR UPDATE;  -- 동일 Gcode/Bcode 의 동시 변경 lock
```

#### SQL-RT-40: audit DB 영속화 (OQ-RT-9)

```sql
CREATE TABLE IF NOT EXISTS audit_returns (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  action ENUM('created','updated','cancelled','regenerated','disassembled','changed','rolled_back','imported') NOT NULL,
  result ENUM('success','failure') NOT NULL,
  gcode VARCHAR(64) NOT NULL,
  return_key_gdate VARCHAR(10) NULL,
  return_key_bdate VARCHAR(10) NULL,
  return_key_hcode VARCHAR(64) NULL,
  return_key_jubun VARCHAR(32) NULL,
  client_ip VARCHAR(64) NOT NULL,
  server_id VARCHAR(64) NOT NULL,
  audit_token_hash VARCHAR(16) NULL,
  reason VARCHAR(255) NULL,
  extra JSON NULL,
  recorded_at DATETIME NOT NULL,
  INDEX idx_gcode_time (gcode, recorded_at),
  INDEX idx_action_result (action, result),
  INDEX idx_return_key (return_key_hcode, return_key_jubun)
) ENGINE=InnoDB CHARSET=utf8mb4;
```

## 2. 트랜잭션 경계 — Phase 2 강화 (DIP)

| 작업 | Phase 1 | Phase 2 |
| --- | --- | --- |
| 라인 diff PUT | (없음) | 단일 트랜잭션 (insert/update/soft-delete 묶음) |
| 부분 재생/해체 | 전체 일괄 | `FOR UPDATE` + Idnum 필터 + 단일 트랜잭션 |
| 3분기 롤백 | (없음) | 24h 윈도우 검증 → reverse 트랜잭션 |
| 변경 (Sobo51) | Sv_Ghng+Sg_Csum 단일 tx | `SELECT ... FOR UPDATE` 추가 |
| audit 로그 | 파일 logger | DB INSERT 병행 (fail-safe — DB 실패해도 작업 성공) |

## 3. D_Select 헬퍼 인터페이스 (OQ-RT-7)

Phase 2 는 헬퍼만 노출, 실제 권한 분기는 C10:

```python
# app/core/d_select.py
from typing import Any

async def build_d_select_clause(user_context: dict[str, Any]) -> str:
    """
    Phase 2: 항상 빈 문자열 반환 (DEC-009 유지).
    C10 (RBAC): user_context.role/branch_id 기반 WHERE 조각 반환.
    호출 형식: f"WHERE {await build_d_select_clause(ctx)} AND ..."
    빈 절 반환 시 자동으로 ' 1=1 ' 로 패딩 (앞뒤 'AND' 결합 안전).
    """
    return " 1=1 "  # Phase 2: D_Select=='' 와 동등
```

요청 헤더 `Authorization-Context: {"branch_id":"BR01","role":"manager"}` 파싱 → `user_context`. Phase 2 는 헤더 없으면 `{}` 사용.

## 4. 외부 의존 가정 (assume_default — OQ-RT-1/2/3)

| OQ-RT | 가정 | 코드 위치 |
| --- | --- | --- |
| OQ-RT-1 | CSV EUC-KR 유지, `format=csv` 만 200, `format=xls` 는 501 | `import_preview` 라우터 |
| OQ-RT-2 | Bdate=Gdate 동일 가정, 검증 스크립트 1회 실행 후 결정 | `analysis/data-validation-reports/` |
| OQ-RT-3 | 9종 카탈로그 = `analysis/sv_ghng_field_catalog.md` | `process_change` 확장 |

## 5. 합격선 매핑

| 합격선 | Phase 2 매핑 |
| --- | --- |
| Sobo34_4 폐기 원장 조회 | SQL-RT-28~30 + DBGrid101/201 표 |
| Sobo58 기간별 반품 보고 | SQL-RT-31~33 + KPI |
| 라인 단위 수정 | SQL-RT-34 (PUT /returns/{key}) |
| 부분 재생/해체 | SQL-RT-35 + Idnum 필터 |
| 24h 롤백 | SQL-RT-36 + 24h 윈도우 |
| bcrypt 패스워드 | SQL-RT-38 + audit_password_attempts |
| 동시 변경 충돌 | SQL-RT-39 (FOR UPDATE) → 409 |
| audit 영속화 | SQL-RT-40 (audit_returns) |
| D_Select 인터페이스 | `app/core/d_select.py` 헬퍼 |

## 6. 참조

- DEC-029: 패스워드 게이트
- DEC-030: OQ-RT 번호 통일
- Phase 1 흐름: [`c4_returns_flow.md`](c4_returns_flow.md)
- Sv_Ghng 카탈로그: [`sv_ghng_field_catalog.md`](sv_ghng_field_catalog.md)
- contract: [`migration/contracts/return_receipt.yaml`](../migration/contracts/return_receipt.yaml) v1.1.0 (T3)
- 매핑 노트: [`layout_mappings/Sobo34_4.md`](layout_mappings/Sobo34_4.md), [`layout_mappings/Sobo58.md`](layout_mappings/Sobo58.md)
