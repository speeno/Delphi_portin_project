# DB 스키마 메타 분석 — 포팅 준비도 요약

**갱신:** 2026-04-19  
**도구:** `tools/db/extract_server_schema.py`, `tools/db/schema_diff.py`  
**원칙:** 전체 DB dump·데이터 스냅샷 없음. 메타(JSON) 및 구조 diff만.

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

## 3. 권장 다음 액션

1. 업무 우선순위가 높은 테이블(로그인·출고·재고) 위주로 `column_issues` 필터링.  
2. `migration/contracts/*.yaml` + `migration/test-cases/*.json` 최소 1흐름.  
3. OQ-003(운영 DB 대수·스키마 정책)와 diff 결과 정렬.

상세 JSON은 로컬 `debug/output/schema/` 에서 재생성하세요.
