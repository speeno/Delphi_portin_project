# 쿼리 캡처 운영 리허설 런북

**도구:** `tools/db/query_capture.py`  
**목적:** 델파이 클라이언트가 실행하는 SQL을 런타임 캡처하여 정적 분석(query_catalog) 누락을 보완.

## 1. 사전 조건

- [ ] 대상 DB 서버의 **general_log** 활성화(또는 mysql.general_log 테이블 활성)
- [ ] 캡처 실행 장비에서 대상 서버 접속 가능 (SSH 터널 포함)
- [ ] 캡처 기간 중 **델파이 클라이언트가 실제 업무 시나리오를 수행**할 담당자 확보

## 2. 캡처 대상 시나리오 (우선순위)

| # | 시나리오 | 관련 화면 | 예상 SQL 유형 |
|---|----------|----------|--------------|
| 1 | 로그인 | 로그인 폼 | SELECT (Id_Logn) |
| 2 | 입고 등록 | 입고관리(Sobo12) | INSERT/UPDATE |
| 3 | 출고 접수 | 출고접수(Sobo13) | INSERT/UPDATE |
| 4 | 반품 처리 | 반품 폼 | UPDATE/DELETE |
| 5 | 거래처 관리 | 거래처관리(Sobo36) | SELECT/INSERT/UPDATE |
| 6 | 출고 현황 조회 | 출고현황(Sobo67) | SELECT |
| 7 | 정산·집계 | 해당 리포트 폼 | SELECT (집계) |

## 3. 실행 절차

### 3-A. 파일 모드 (general_log 파일 tail)

```bash
# 서버에서 general_log 활성화 (필요 시)
# MariaDB: SET GLOBAL general_log = 'ON';

python3 tools/db/query_capture.py \
    --mode file \
    --log-path /var/log/mysql/general.log \
    --output debug/output/captured_queries_<server-id>_<date>.json
```

### 3-B. 테이블 모드 (mysql.general_log 조회)

```bash
# 서버에서 general_log + log_output='TABLE' 활성화
# SET GLOBAL general_log = 'ON';
# SET GLOBAL log_output = 'TABLE';

python3 tools/db/query_capture.py \
    --mode table \
    --host <host> --port 3306 \
    --user <user> --password <password> \
    --output debug/output/captured_queries_<server-id>_<date>.json
```

### 3-C. 리허설 수행

1. 캡처 시작 후, 델파이 클라이언트에서 **§2 시나리오를 순서대로** 실행.
2. 각 시나리오 실행 전후에 **콘솔에 구분 메모** (예: 파일 모드에서 `echo "=== 시나리오 2: 입고 ===" >> /var/log/mysql/general.log`).
3. 전체 시나리오 완료 후 캡처 중단 (Ctrl+C 또는 테이블 모드는 자동 종료).

## 4. 결과 활용

```bash
# 교차맵에 캡처 결과 합류
python3 tools/db/db_logic_cross_reference.py \
    --capture debug/output/captured_queries_<server-id>_<date>.json

# 인벤토리 재생성 (캡처와 별개, 스키마 변경이 있었을 때)
python3 tools/db/db_logic_reporter.py
```

## 5. 결과 저장 위치

| 파일 | 경로 | 비고 |
|------|------|------|
| 캡처 원본 | `debug/output/captured_queries_*.json` | `.gitignore`에 포함 |
| 교차맵(갱신) | `analysis/db_logic_cross_reference.json` | git 추적 |
| 인벤토리(갱신) | `docs/db-business-logic-inventory.md` | git 추적 |

## 6. 주의사항

- general_log는 **성능 영향**이 있으므로 리허설 완료 후 반드시 비활성화.
- 캡처 파일에 **민감 데이터(비밀번호 등)**가 포함될 수 있으므로 `debug/output/`에만 보관하고 **git에 올리지 않음**.
- MySQL 3.23 인스턴스는 general_log 테이블 모드를 지원하지 않을 수 있음 → 파일 모드만 가능.

## 7. 갭 리포트 연결

캡처 후 `docs/db-logic-porting-gap-report.md`의 **GAP-001** 항목 상태를 갱신하고, 새로 발견된 SQL이 있으면 GAP 항목 추가.

---

*관련: [db-business-logic-inventory.md](db-business-logic-inventory.md) · [db-logic-porting-gap-report.md](db-logic-porting-gap-report.md) · [open-questions.md](../legacy-analysis/open-questions.md) OQ-DBL-003*
