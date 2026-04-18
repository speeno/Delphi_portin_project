# C1 로그인·세션 시작 — 4축 동등성 사전 평가 보고서

_생성: 2026-04-22 — `complete-c1-login-t1-t8` 단일 사이클 T7 산출물_
_갱신: 2026-04-22 — 1차 포팅 범위 동결 (DEC-005~008 1차 제외)_

본 보고서는 **레거시 정적 분석 + Migration Contract v1.1.0 + Test Pack v1.1.0-phase1** 만으로 도출 가능한 4축 동등성 사전 분석 결과입니다.
운영 DBA 일정 확정 후 query_capture 1회 + eval_runner 실측이 도착하면 §7 슬롯에 그대로 채워 v1.0 으로 승격합니다.

> **1차 포팅 합격선 (acceptance_goal)**: "기존 사용자가 기존 ID/PW 로 그대로 로그인 가능".
> 멀티테넌시(D-LOGIN-4) / 비밀번호 해시(D-LOGIN-1) / 라이선스 키(D-LOGIN-2) / 슈퍼유저 분기(D-LOGIN-3) 는 모두 후속 작업으로 이관 (DEC-005~008).

> 본 보고서는 [`migration/contracts/login.yaml`](../migration/contracts/login.yaml), [`migration/test-cases/login.json`](../migration/test-cases/login.json), [`analysis/screen_cards/Subu00.md`](../analysis/screen_cards/Subu00.md) 와 1:1 동기화됩니다.

---

## 0. 평가 입력

| 항목 | 값/경로 |
|------|--------|
| Migration Contract | `migration/contracts/login.yaml` (v1.1.0, scope_phase=phase1) |
| Regression Test Pack | `migration/test-cases/login.json` (v1.1.0-phase1, 12 cases — 1차 in_scope 8건 / out_of_scope 4건) |
| 화면 카드 | `analysis/screen_cards/Subu00.md` (자동 생성) |
| DB 교차맵 | `analysis/db_logic_cross_reference.json` (캡처 미포함 정적 1차) |
| 5축 임계값 정의 | `docs/eval-axes-and-dod-draft.md` |
| 캡처 결과 | _대기 — `docs/query-capture-rehearsal-tracker.md` §1 차단_ |

## 1. Functional 축 — 분기·메시지 동등성 (1차 포팅 범위)

| 항목 | 레거시 (Chul.pas) | 웹 contract | TC | 1차 결과 |
|------|------------------|-------------|----|---------|
| 정상 로그인 (일반 사용자) | L441 SELECT + L451 Gpass==Logn3 | `POST /api/auth/login` 200 + body | TC-LOGIN-001 | **동등** |
| 비밀번호 불일치 | L453 ShowMessage | 401 AUTH_BAD_PASSWORD | TC-LOGIN-003 | **동등** |
| 사용자/아이디 불일치 | L457 ShowMessage | 401 AUTH_NO_USER | TC-LOGIN-004 | **동등** |
| Gname 정규화 | 단순 `=` 비교 | (미합의) | TC-LOGIN-005 (`expect_one_of`) | **OQ-001 의존** |
| SQL 인젝션 | #39 결합 (취약) | 파라미터 바인딩 (안전) | TC-LOGIN-006 | **웹 우위** |
| Program Key 미등록 | L477 ShowMessage | 1차 발생 없음 (DEC-006) | (`failure_codes` 스키마 보존) | **1차 미발생 — DEC-006** |
| 슈퍼유저 분기 | L486 `if Hnnnn='0000'` | 1차 미수행 (DEC-007) | TC-LOGIN-002 (`expect_phase1`: is_super=false) | **1차 후속 이관 — DEC-007** |
| 가시성 필터 SQL | L490 SELECT G7_Ggeo Where Chek5='show1' | 1차 미호출 (DEC-007) | TC-LOGIN-011 (out_of_scope) | **1차 후속 이관 — DEC-007** |
| 테넌트 자동 매핑 | (없음) | 1차 단일 테넌트 (DEC-008) | TC-LOGIN-010/012 (out_of_scope) | **1차 후속 이관 — DEC-008** |

**1차 사전 평가**: 레거시 분기 중 1차 합격선 분기 5건(정상/비밀번호불일치/NODATA/정규화/인젝션) 정적 매칭 ✓ + 1건(정규화) OQ-001 의존. 슈퍼유저·라이선스·테넌트 4건은 1차 범위 외(decisions.md DEC-005~008).

## 2. Data 축 — DB 영향 동등성

화면 카드 §4 (`db_impact_matrix.json` 발췌):

| table | C | R | U | D | total | 1차 본 흐름 | 비고 |
|-------|---|---|---|---|-------|-------------|------|
| Id_Logn | 0 | 9 | 4 | 0 | 13 | **R only (Gpass 평문 비교)** | UPDATE 4건은 비밀번호 변경 흐름(별도 계약). 1차 tenant_id 컬럼 추가 없음 (DEC-008). |
| G7_Ggeo | 3 | 97 | 11 | 3 | 114 | **호출 없음** | 가시성 필터 SELECT 1건은 1차 제외 (DEC-007). 후속 작업에서 재도입. |
| Gg_Magn | 1 | 7 | 4 | 0 | 12 | **무관** | 환경설정 흐름 |
| Me_Sage | 2 | 13 | 2 | 2 | 19 | **무관** | 메시지 흐름 |

**1차 사전 평가**: C1 1차 범위는 Id_Logn SELECT only (delta 0 보장). TC-LOGIN-007 이 데이터 무변경 검증. DB 마이그레이션 0건 (DEC-005/008).

**골든마스터 명령 (캡처 도착 후 즉시)**:
```bash
python3 tools/harness/golden_master.py \
    --tables Id_Logn \
    --before debug/output/before_<server>.json \
    --after  debug/output/after_<server>.json \
    --report debug/output/c1-data-delta.md
```
> 1차에서는 `--tables Id_Logn` 만 (G7_Ggeo 는 호출 없음). 후속 작업에서 G7_Ggeo 재추가.

## 3. UX 축 — 메시지·상태 동등성

| 메시지 키 | 레거시 한글 | 웹 응답 코드 | 1차 동등성 |
|-----------|------------|-------------|-----------|
| AUTH_BAD_PASSWORD | "비밀번호가 틀립니다." | 401 + `{code:AUTH_BAD_PASSWORD}` | 의미 보존 ✓ |
| AUTH_NO_USER | "사용자 또는 아이디가 틀립니다." | 401 + `{code:AUTH_NO_USER}` | 의미 보존 ✓ |
| AUTH_KEY_REGISTER_REQUIRED | "Program Key를 등록해 주세요." | 1차 미발생 (DEC-006) | 1차 후속 이관 |
| 헤더 hname 표시 | `Subu00.Caption` 추가 표시 | 응답 `hname` + 클라이언트 헤더 렌더 | TC-LOGIN-001 검증 |

**1차 사전 평가**: 1차 합격선 메시지 의미 동등성 충족.

## 4. Performance 축 — 응답 시간

| 임계값 | 베타 | 내부오픈 | 정식오픈 |
|--------|------|----------|----------|
| p95 (네트워크 포함) | < 1.0 s | < 500 ms | < 300 ms |
| 에러율 | < 1% | < 0.5% | < 0.1% |

contract `equivalence.performance: p95 < 500 ms` (내부오픈 기준).
TC-LOGIN-008: rps=5, duration=60s, warmup=10s, expect p95<500ms, error_rate<0.005.

**1차 사전 평가**: 단일 SELECT + 평문 비교 (bcrypt 비용 0 — DEC-005 1차 평문 보존) 가정 시 p95 < 500ms 충분 달성 가능.

**eval_runner 명령 (웹 가동 후)**:
```bash
python3 tools/harness/eval_runner.py migration/test-cases /api/v1 \
    --filter C1 --output debug/output/c1-eval-report.json
```

## 5. Audit 축 — 감사 로그

| 요구 | 레거시 | 웹 | 1차 결정 |
|------|-------|----|---------|
| 성공 로그 | 미흡 | 필수 (timestamp/gcode/result/client_ip) | TC-LOGIN-009 |
| 실패 로그 | 미흡 | 필수 (동일 필드 + reason) | TC-LOGIN-009 |
| 테넌트 격리 위반 | n/a | 1차 미적용 (DEC-008) | 후속 작업에서 D-LOGIN-4 + TC-LOGIN-012 도입 시 추가 |

**1차 사전 평가**: 1차 — 성공/실패 감사 로그 신규 도입(레거시 미흡 보강). 테넌트 격리 위반 항목은 후속.

## 6. 결정 의존도 정리 (1차 포팅 범위 동결 후)

| Delta | 1차 in_scope | 결정 (DEC-) | 1차 동작 | 후속 작업 |
|-------|-------------|-------------|---------|----------|
| D-LOGIN-1 (평문 → 해시) | **false** | DEC-005 | 평문 동등 비교 그대로 (Performance bcrypt 비용 0) | 후속 사이클: 별도 결정 DEC-XXX → 해시 + lazy migration |
| D-LOGIN-2 (라이선스 키) | **false** | DEC-006 | 라이선스 검증 비활성 (전 사용자 PASS, 설치형 아님) | 후속: 서버측 License_Tenant + JWT claim |
| D-LOGIN-3 (슈퍼유저 일반화) | **false** | DEC-007 | 슈퍼유저 분기 자체 폐지, 가시성 필터 SQL 미호출 | 후속: C10 권한 관리 통합 설계 시 role 일반화 |
| D-LOGIN-4 (테넌트 자동 매핑) | **false** | DEC-008 | 단일 테넌트 운영 (레거시 동일 모델 유지) | 후속 사이클: 옵션 A/B/C 합의 → DB 마이그레이션 + 모든 시나리오 RLS 패치 |

→ DEC-005~008 모두 **1차 포팅 범위 외** (`legacy-analysis/decisions.md` 참조).
→ 1차 합격선은 D-LOGIN-1~4 의존도 **0** — "기존 ID/PW 로그인" 단일 항목으로 단순화.

## 7. 최종 4축 결과 슬롯 (캡처·실측 도착 후 채움)

| 축 | 1차 임계값 | 측정값 | 결과 |
|----|-----------|--------|------|
| Functional | 1차 in_scope 분기 5건 일치 (TC-LOGIN-001/003/004/005/006) | _대기_ | _대기_ |
| Data | Id_Logn delta = 0 (TC-LOGIN-007) | _대기_ | _대기_ |
| UX | 메시지 의미 보존 (AUTH_BAD_PASSWORD/AUTH_NO_USER) | _대기_ | _대기_ |
| Performance | p95 < 1.0s, error_rate < 1% (TC-LOGIN-008) | _대기_ | _대기_ |
| Audit | 성공/실패 모두 기록 (TC-LOGIN-009) | _대기_ | _대기_ |

> 1차 in_scope 8건 (TC-LOGIN-001/003/004/005/006/007/008/009) 만 채점 대상. TC-LOGIN-002/010/011/012 는 후속 사이클에서 채점.

## 8. 잔존 위험

- **OQ-DBL-003** (런타임 SQL 캡처 미실시) — 정적 분석으로 식별된 SQL 11건 외 동적 SQL 가능성 잔존. 캡처 1회 후 closure.
- **OQ-LOGIN-1** (멀티테넌시 매핑) — DEC-008 으로 1차 포팅 범위 외 결정. 후속 사이클에서 옵션 A/B/C 합의 후 closure.
- **GAP-001** (DB 비즈니스 로직 1차 자동 조사 한계) — 캡처 1회 + cross_reference 갱신으로 완화 → 해결 예정.

## 9. 변경 이력

- 2026-04-22 — 초안 작성. 정적 4축 사전 평가 + 캡처 도착 슬롯.
- 2026-04-22 (revised) — 1차 포팅 범위 동결 반영. DEC-005~008 모두 1차 범위 외로 갱신:
  - §1 Functional: 슈퍼유저/라이선스/테넌트 분기 4건 1차 후속 이관 표기
  - §2 Data: tenant_id 컬럼 추가 없음, G7_Ggeo 호출 없음 명시
  - §3 UX: AUTH_KEY_REGISTER_REQUIRED 1차 미발생 표기
  - §4 Performance: bcrypt 비용 0 (평문 보존)
  - §5 Audit: 테넌트 격리 항목 후속 이관
  - §6 결정 의존도: 1차 in_scope=false 일괄 표기 + 후속 작업 명시
  - §7 4축 결과 슬롯: 1차 in_scope 8건만 채점 대상으로 한정
