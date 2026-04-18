# C1 로그인·세션 시작 — 4축 동등성 사전 평가 보고서

_생성: 2026-04-22 — `complete-c1-login-t1-t8` 단일 사이클 T7 산출물_

본 보고서는 **레거시 정적 분석 + Migration Contract v0.2.0-review + Test Pack v0.2.0-review** 만으로 도출 가능한 4축 동등성 사전 분석 결과입니다.
운영 DBA 일정 확정 후 query_capture 1회 + eval_runner 실측이 도착하면 §5 슬롯에 그대로 채워 v1.0 으로 승격합니다.

> 본 보고서는 [`migration/contracts/login.yaml`](../migration/contracts/login.yaml), [`migration/test-cases/login.json`](../migration/test-cases/login.json), [`analysis/screen_cards/Subu00.md`](../analysis/screen_cards/Subu00.md) 와 1:1 동기화됩니다.

---

## 0. 평가 입력

| 항목 | 값/경로 |
|------|--------|
| Migration Contract | `migration/contracts/login.yaml` (v0.2.0-review) |
| Regression Test Pack | `migration/test-cases/login.json` (v0.2.0-review, 12 cases) |
| 화면 카드 | `analysis/screen_cards/Subu00.md` (자동 생성) |
| DB 교차맵 | `analysis/db_logic_cross_reference.json` (캡처 미포함 정적 1차) |
| 5축 임계값 정의 | `docs/eval-axes-and-dod-draft.md` |
| 캡처 결과 | _대기 — `docs/query-capture-rehearsal-tracker.md` §1 차단_ |

## 1. Functional 축 — 분기·메시지 동등성

| 항목 | 레거시 (Chul.pas) | 웹 contract | TC | 결과 |
|------|------------------|-------------|----|------|
| 정상 로그인 | L441 SELECT + L451 Gpass==Logn3 | `POST /api/auth/login` 200 + body | TC-LOGIN-001/002 | **동등** |
| 비밀번호 불일치 | L453 ShowMessage | 401 AUTH_BAD_PASSWORD | TC-LOGIN-003 | **동등** |
| 사용자/아이디 불일치 | L457 ShowMessage | 401 AUTH_NO_USER | TC-LOGIN-004 | **동등** |
| Program Key 미등록 | L477 ShowMessage | 403 AUTH_KEY_REGISTER_REQUIRED | (`failure_codes` 정의됨) | **동등** (D-LOGIN-2 결정 후 확정) |
| 슈퍼유저 분기 | L486 `if Hnnnn='0000'` | `is_super=true` + visibility_filter | TC-LOGIN-002/011 | **동등** |
| 가시성 필터 SQL | L490 SELECT G7_Ggeo Where Chek5='show1' | `SQL-LOGIN-2-VISIBILITY` | TC-LOGIN-011 | **동등** |
| Gname 정규화 | 단순 `=` 비교 | (미합의) | TC-LOGIN-005 (`expect_one_of`) | **OQ-001 의존** |
| SQL 인젝션 | #39 결합 (취약) | 파라미터 바인딩 (안전) | TC-LOGIN-006 | **웹 우위** |
| 테넌트 자동 매핑 | (없음) | D-LOGIN-4 옵션 A 신규 | TC-LOGIN-010/012 | **웹 신규 — OQ-LOGIN-1 의존** |

**사전 평가**: 레거시 9개 분기 중 7개 정적 매칭 ✓ / 2개 OQ 의존(OQ-001, OQ-LOGIN-1).

## 2. Data 축 — DB 영향 동등성

화면 카드 §4 (`db_impact_matrix.json` 발췌):

| table | C | R | U | D | total | 본 흐름 | 비고 |
|-------|---|---|---|---|-------|---------|------|
| Id_Logn | 0 | 9 | 4 | 0 | 13 | **R only** | UPDATE 4건은 비밀번호 변경 흐름(별도 계약, out_of_scope) |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | **R only** | 가시성 필터 SELECT 1건 (Hnnnn='0000' 조건) |
| Gg_Magn | 1 | 7 | 4 | 0 | 12 | **무관** | 환경설정 흐름 |
| Me_Sage | 2 | 13 | 2 | 2 | 19 | **무관** | 메시지 흐름 |

**사전 평가**: C1 베타 범위는 SELECT only (delta 0 보장 가능). TC-LOGIN-007 이 데이터 무변경 검증.

**골든마스터 명령 (캡처 도착 후 즉시)**:
```bash
python3 tools/harness/golden_master.py \
    --tables Id_Logn,G7_Ggeo \
    --before debug/output/before_<server>.json \
    --after  debug/output/after_<server>.json \
    --report debug/output/c1-data-delta.md
```

## 3. UX 축 — 메시지·상태 동등성

| 메시지 키 | 레거시 한글 | 웹 응답 코드 | 동등성 |
|-----------|------------|-------------|--------|
| AUTH_BAD_PASSWORD | "비밀번호가 틀립니다." | 401 + `{code:AUTH_BAD_PASSWORD}` | 의미 보존 ✓ |
| AUTH_NO_USER | "사용자 또는 아이디가 틀립니다." | 401 + `{code:AUTH_NO_USER}` | 의미 보존 ✓ |
| AUTH_KEY_REGISTER_REQUIRED | "Program Key를 등록해 주세요." | 403 + `{code:AUTH_KEY_REGISTER_REQUIRED}` | D-LOGIN-2 결정 후 확정 |
| 헤더 hname 표시 | `Subu00.Caption` 추가 표시 | 응답 `hname` + 클라이언트 헤더 렌더 | TC-LOGIN-001 검증 |

**사전 평가**: 베타 임계값(메시지 의미 동등성) 충족.

## 4. Performance 축 — 응답 시간

| 임계값 | 베타 | 내부오픈 | 정식오픈 |
|--------|------|----------|----------|
| p95 (네트워크 포함) | < 1.0 s | < 500 ms | < 300 ms |
| 에러율 | < 1% | < 0.5% | < 0.1% |

contract `equivalence.performance: p95 < 500 ms` (내부오픈 기준).
TC-LOGIN-008: rps=5, duration=60s, warmup=10s, expect p95<500ms, error_rate<0.005.

**사전 평가**: SQL 1~2 회 + bcrypt 1회 (해시 도입 후) 가정 시 p95 < 500ms 달성 가능 (단일 SELECT + 인덱스 가정).

**eval_runner 명령 (웹 가동 후)**:
```bash
python3 tools/harness/eval_runner.py migration/test-cases /api/v1 \
    --filter C1 --output debug/output/c1-eval-report.json
```

## 5. Audit 축 — 감사 로그

| 요구 | 레거시 | 웹 | 결정 |
|------|-------|----|------|
| 성공 로그 | 미흡 | 필수 (timestamp/gcode/result/client_ip) | TC-LOGIN-009 |
| 실패 로그 | 미흡 | 필수 (동일 필드 + reason) | TC-LOGIN-009 |
| 테넌트 격리 위반 | n/a | 필수 (TC-LOGIN-012 must_not) | D-LOGIN-4 |

**사전 평가**: 레거시 미흡 → 웹 신규 요구사항으로 전환. 베타에서 Audit 스키마 동결 필요.

## 6. 결정 의존도 정리

| Delta | 결정 게이트 | 본 보고서 영향 |
|-------|-------------|---------------|
| D-LOGIN-1 (평문 → 해시) | approvals #3 (API 계약 승인) | Performance(bcrypt 비용), Data(병행 운영 컬럼) |
| D-LOGIN-2 (라이선스 키 정책) | approvals #1 (베타 게이트) | Functional(403 분기), Audit(키 검증 로그) |
| D-LOGIN-3 (슈퍼유저 일반화) | approvals #4 (고객사별 차이) | Functional(visibility_filter), UX(권한 표시) |
| D-LOGIN-4 (테넌트 자동 매핑) | approvals #4 | **모든 축**, 특히 Data(격리)·Audit(위반 차단) |

→ T8 에서 DEC-005~008 로 등록(§5 §5.1).

## 7. 최종 4축 결과 슬롯 (캡처·실측 도착 후 채움)

| 축 | 임계값(베타) | 측정값 | 결과 |
|----|--------------|--------|------|
| Functional | 9 분기 모두 일치 | _대기_ | _대기_ |
| Data | Id_Logn delta = 0 | _대기_ | _대기_ |
| UX | 메시지 의미 보존 | _대기_ | _대기_ |
| Performance | p95 < 1.0s | _대기_ | _대기_ |
| Audit | 성공/실패 모두 기록 | _대기_ | _대기_ |

## 8. 잔존 위험

- **OQ-DBL-003** (런타임 SQL 캡처 미실시) — 정적 분석으로 식별된 SQL 11건 외 동적 SQL 가능성 잔존. 캡처 1회 후 closure.
- **OQ-LOGIN-1** (멀티테넌시 매핑) — D-LOGIN-4 옵션 A/B/C 미선택. 옵션 A 추천 사유: 사용자 입력 0 + 단일 식별자 + 코드 변경 최소.
- **GAP-001** (DB 비즈니스 로직 1차 자동 조사 한계) — 캡처 1회 + cross_reference 갱신으로 완화 → 해결 예정.

## 9. 변경 이력

- 2026-04-22 — 초안 작성. 정적 4축 사전 평가 + 캡처 도착 슬롯.
