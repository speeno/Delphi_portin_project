# DB 스키마 메타 분석 — 포팅 준비도 요약

**갱신:** 2026-04-23  
**도구:** `tools/db/extract_server_schema.py`, `tools/db/schema_diff.py`, `tools/extract_welove_schema.py`(스키마 사전), `tools/extract_welove_db_routes.py`(DSN 메타)  
**원칙:** 전체 DB dump·데이터 스냅샷 없음. 메타(JSON) 및 구조 diff만. **스키마 사전 정본은 `MAN-030`** ([`analysis/welove_schema_dictionary.json`](../analysis/welove_schema_dictionary.json)). **DSN 라우팅 정본은** [`analysis/welove_db_route_matrix.json`](../analysis/welove_db_route_matrix.json) — 본 가이드는 두 정본을 1차 입력으로 한다.

## 1. 포팅에 필요한 정보가 생겼는가?

| 항목 | 상태 |
|------|------|
| 서버별 테이블·컬럼·인덱스·제약 메타 | 생성됨 (`debug/output/schema/<server-id>/`, 로컬) |
| 서버 간 스키마 차이 정량 | 생성됨 (`diff-*.json` / `.md`) |
| MySQL 3.23 전용 메타 경로 | `mysql3_show_meta`로 154·155 반영 |
| Migration Contract / Eval JSON | 아직 없음 — 다음 게이트 |

즉 **「DB가 무엇을 갖고 있고 서버끼리 어디가 다른가」**에 대한 재현 가능한 근거는 마련되었고, **계약·자동 회귀**까지는 추가 작업이 필요합니다.

## 2. 결과 한눈에 (숫자)

| 서버 ID | 추출 모드 | 테이블 수 |
|---------|------------|-----------|
| remote_138 | information_schema | 51 |
| remote_153 | information_schema | 79 |
| remote_154 | mysql3_show_meta | 65 |
| remote_155 | mysql3_show_meta | 78 |

**138 vs 153:** 153에만 있는 테이블 28개 · 공통 51 · 컬럼 정의 차이 576건(표현 차 포함 가능).  
**154 vs 155:** 155에만 14테이블 · 154에만 `S1_Logn` · 공통 64 · 컬럼 이슈 160 · DDL 길이 불일치 8.

## 3. DB 내 비즈니스 로직 검토

| 객체 유형 | 138 | 153 | 154 (3.23) | 155 (3.23) | 비고 |
|-----------|-----|-----|-----------|-----------|------|
| 저장 루틴 (PROCEDURE/FUNCTION) | 0 | 0 | 미지원 | 미지원 | INFORMATION_SCHEMA + mysql3 probe |
| 트리거 (TRIGGER) | 0 | 0 | 미지원 | 미지원 | 3.23은 트리거 기능 없음 |
| 뷰 (VIEW) | 0 | 0 | 미지원 | 미지원 | 3.23은 뷰 기능 없음 |
| 외래키 (FK) | 0 | 0 | — | — | 코드 측 참조 무결성 의존 |
| UNIQUE 제약 | 0 | 0 | — | — | 코드 측 중복 체크 의존 |

**1차 판단:** DB 측 비즈니스 로직 객체는 전 서버에서 **0건**. 비즈니스 로직은 델파이 클라이언트 코드에 집중.

**확정을 위한 조건:**
- [ ] 체크리스트 §2.5 현장 확인 완료
- [ ] query_capture 운영 리허설 1회 이상 실시
- [ ] OQ-DBL-001~003 클로저

**상세:** [`docs/db-business-logic-inventory.md`](db-business-logic-inventory.md), [`docs/db-logic-porting-gap-report.md`](db-logic-porting-gap-report.md)

## 4. 권장 다음 액션

1. 업무 우선순위가 높은 테이블(로그인·출고·재고) 위주로 `column_issues` 필터링.  
2. `migration/contracts/*.yaml` + `migration/test-cases/*.json` 최소 1흐름.  
3. OQ-003(운영 DB 대수·스키마 정책)와 diff 결과 정렬.
4. **DB 로직 인벤토리·갭 리포트** 갱신 후 OQ-DBL 시리즈 클로저.

상세 JSON은 로컬 `debug/output/schema/` 에서 재생성하세요.

## 5. SCH-WELOVE-출판 사전 우선순위 (`G5` 적용)

[`analysis/welove_schema_dictionary.json`](../analysis/welove_schema_dictionary.json) 가 단일 원천이다 — `Size(전)→Size(후)` 흔적은 멀티 DB 호환 어댑터(DEC-033)의 1차 후보를 제공하고, [`docs/welove-schema-reconciliation.md`](welove-schema-reconciliation.md) 의 `SCH-RECON-01..04` 4 항목이 본 가이드의 진단 게이트다.

| 게이트 | 통과 조건 |
|---|---|
| **G5-Gate-A** | 신규 컬럼 어댑터 PR 시 사전(JSON) 의 해당 행을 인용 + diff 보고. |
| **G5-Gate-B** | 사전과 운영 DB 의 컬럼 size 가 다르면 `OQ-SCH-NEW-*` 등록. |
| **G5-Gate-C** | 사전 미수록(§3.1 23 테이블) 의 화면 포팅 시 SME 회의 의제로 격상. |

## 6. 로그인 기반 DSN 라우팅 (`G6` 적용 — 신설)

본 가이드의 DB 결정 흐름은 [`docs/decision-login-db-routing.md`](decision-login-db-routing.md) 에 위임한다 — 본 절은 **DB 포팅 단계에서 지켜야 할 항목**만 요약한다.

| 항목 | 결정 |
|---|---|
| 인증 서버 | 단일 (`BLS_AUTH_SERVER_ID`) — DEC-051. |
| 데이터 서버 | 사용자별 1:1 (DEC-052) → JWT `primary_server` 적재. |
| 풀 선택 헬퍼 | `pool_for(jwt)` 1 개 — 도메인 서비스 신설 시 본 헬퍼만 사용. |
| 메타 단일 원천 | [`analysis/welove_db_route_matrix.json`](../analysis/welove_db_route_matrix.json). 자격증명은 본 JSON 에 **0건** — vault 분리. |
| 신규 테넌트 추가 | 메타 1행 추가 + admin 화면 드롭다운 갱신 + 운영 vault 비번 적재 — 3 단계 PR. |

> **DB 포팅 게이트:** 신규 SQL/마이그레이션 작성 시 (1) 사전(`MAN-030`) 의 컬럼 정의 + (2) 본 라우팅 표의 `server_id` 매칭 두 가지를 함께 인용해야 한다.

## 7. 자동 재현 스니펫

```bash
python3 tools/extract_welove_schema.py            # 사전 갱신 (UTF-8)
python3 tools/extract_welove_db_routes.py         # DSN 메타 갱신 (자격증명 0건)
python3 tools/db/extract_server_schema.py --server <id>   # 운영 DB 메타 갱신 (메타만)
```
