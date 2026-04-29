# 특별관리(Sobo16_special) 구현 완료 기록 — `/master/special`

> **목적**: `/master/special` (form-registry `Sobo16_special`, phase1) — 사이드바 「기초관리 · 특별관리」 stub 을 정식 화면으로 승격한 결과를 기록한다. 본 문서는 T1~T8 단계 · blocker 해소 · 코드 변경 단위 · 회귀 가드 · 5축 PASS 조건을 단일 원천으로 유지한다.
>
> **소속**: `legacy-analysis/decisions.md` DEC-019/023(C9 마스터 단일 원천) + DEC-053(phase1 승격 게이트 = 5축 PASS) 적용 대상.

---

## 0. 현황 (2026-04-29 갱신)

| 자산 | 위치 | 상태 |
| --- | --- | --- |
| 레거시 dfm | `legacy_delphi_source/legacy_source/Subu16.dfm` | 보유 (TFlatPanel×4 / TFlatEdit×4 / TCornerButton×3 / TmyLabel3d×3 / TFlatButton×1 / TDBGrid×1, 17 컴포넌트 / 17 이벤트) |
| 레거시 pas | `legacy_delphi_source/legacy_source/Subu16.pas` | 보유 (Button001~009 핸들러 9개 + Form 라이프사이클 3개 + Edit/Grid 핸들러 5개) |
| 화면 카드 | `analysis/screen_cards/Sobo16.md` | done — SQL 3건(SELECT G6_Ggeo / G4_Book / G1_Ggeo), 영향 테이블 G4_Book·G1_Ggeo·G6_Ggeo |
| 매핑 노트 | `analysis/layout_mappings/Sobo16.md` | done — G6_Ggeo 축 기준 |
| Contract | `migration/contracts/special_master.yaml` | active v1.1.0 (`scope_phase: phase1`, blockers 0) |
| Phase2 카드 | `dashboard/data/phase2-screen-cards.json::Sobo16_special` | T1~T8 done |
| 모던 frontend | `app/(app)/master/special/page.tsx` | DataGrid + Grat1/Gssum 편집 패널 구현 |
| 모던 backend | `routers/masters.py` / `services/masters_service.py` | `GET/PATCH /api/v1/masters/special` 구현 |
| 모바일웹(m.websend.kr) | 「특별관리」 메뉴 | 1:1 매핑 대상(layout/SQL 동일성 가정 → T1 검증) |

### Blocker 인벤토리 (단일 원천 = `special_master.yaml` §blockers)

| ID | 상태 | 해소 내용 |
| --- | --- | --- |
| BLK-SPC-1 | closed | 저장 대상이 G1 특수 플래그가 아니라 G6_Ggeo `Grat1`/`Gssum` 임을 계약·구현에 반영 |
| BLK-SPC-2 | closed / out-of-scope | `special_class_code` enum은 이번 화면 범위가 아님. 필요 시 별도 계약으로 분리 |

### 2026-04-29 완료 범위

- `Sobo16_special` 은 `G6_Ggeo` 목록 조회 + `Grat1`/`Gssum` 부분 수정까지 phase1 승격했다.
- 신규 G6 행 INSERT, 물리 DELETE, Gcode/Bcode 변경 저장은 계약의 `out_of_scope` 에 남긴다.
- 다음 큐 문서: `docs/phase2-next-work-queue.md`.

---

## 1. T1~T8 단계 — 단계별 DoD + 산출물

> **소속 룰**: DEC-053 (phase1 승격 게이트 = 5축 PASS · GAP-P0 = 0). 본 단계 DoD 는 phase1-component-fidelity 매트릭스 34행 정식 편입 조건과 동일.

### T1 — 화면 카드 + 매핑 노트 (in_progress→done)

- [x] `analysis/screen_cards/Sobo16.md` (자동 생성 done)
- [ ] **`analysis/layout_mappings/Sobo16.md` 신설** — 11 섹션 구조(DEC-028 표준).
  - §0 입력 산출물 (dfm/pas/screen_card/모바일웹 캡처)
  - §1 의미 분기 — 1차 노출 범위(읽기 그리드 + 플래그 토글 1개) vs phase3 분류 카탈로그 등록 폼
  - §2 dfm 영역 인벤토리 — Panel001~004 / Edit101~114 / Button001~009 매핑 표
  - §3 TabOrder 보존 표
  - §4 DBGrid101 컬럼 매핑 (`G1_Ggeo.{Gcode, Gname, Special_flag, Special_class, Memo}` 5컬럼 가정 — T2 검증)
  - §5 위젯 → 모던 컴포넌트 매핑 + `data-legacy-id` 부착 표
  - §6 **out-of-scope** 항목 (인쇄·바코드·고객사 분기 4건)
  - §7 deltas (모던 신설 컬럼: `updated_at`, `audit_id`)
  - §8 이벤트 핸들러 매핑 (Button001~009 → REST endpoint 매핑)
  - §9 변형 폴더(`Subu16_*` 산출물) 검토 — 변형 0건 가정
  - §10 회귀 가드 체크리스트 (T7 입력)
  - §11 모바일웹 캡처 vs 모던 비교 1행

DoD: 매핑 노트 §1~§11 채움 + 모바일웹 「특별관리」 화면 캡처 1건 첨부.

### T2 — 레거시 SQL/이벤트 추출 (in_progress) ← BLK-SPC-1 해소 단계

#### T2.1 — SQL 추출 (BLK-SPC-1)

- [ ] `tools/db/query_capture.py --tag sobo16` 실행 → `/dump/queries/sobo16/*.sql`
- [ ] `Subu16.pas` Button001~009 핸들러 분기별 SQL 라벨링:
  - Button001 = 등록(INSERT G1_Ggeo Special_*) — 미확정
  - Button002 = 수정(UPDATE G1_Ggeo Special_*) — 미확정
  - Button003 = 삭제 / 플래그 OFF — 미확정
  - Button004 = 분류 변경 — 미확정
  - Button005~009 = 검색·인쇄·CSV — 1차 OOS
- [ ] `pas_analysis/Sobo16.json` 보강 — Button00xClick → SQL 라인 매핑 표
- [ ] `migration/coverage/placeholder-t1-t2-index.md::§1 #1` 항목 close

DoD: SQL 인벤토리 ≥ 5건(SELECT 3 + INSERT/UPDATE 추정 2) + Button00x 분기 표 작성 → BLK-SPC-1 close 라벨.

#### T2.2 — 분류 카탈로그 합의 (BLK-SPC-2)

- [ ] 운영 DB 표본 추출: `SELECT DISTINCT Special_class FROM G1_Ggeo WHERE Special_flag='Y' GROUP BY Special_class ORDER BY COUNT(*) DESC LIMIT 50`
- [ ] 비즈니스 미팅 1회 → 카탈로그 enum 4~8개 후보 합의
- [ ] `migration/contracts/special_master.yaml::scope.upsert.request_body.special_class_code` enum 확정 + AC-SPC-4 활성화

DoD: enum 카탈로그 합의 + 운영 표본 100% 매핑 가능(미매핑은 `OTHER` 폴백) → BLK-SPC-2 close.

### T3 — Contract 0.9.0 → 1.0.0

- [ ] `migration/contracts/special_master.yaml`:
  - version 0.9.0 → 1.0.0
  - status draft → active
  - `blockers: []` (T2 해소 후)
  - `scope.upsert.request_body.special_class_code` enum 확정
  - `acceptance_criteria` AC-SPC-1~4 모두 활성 + `pending_blocker` 제거
- [ ] DEC-019/023 「PATCH 수정 ON · 삭제 OFF」 정책 준수 — DELETE endpoint 미제공(`special_flag=false` 로 OFF 갈음) 명시
- [ ] `migration/contracts/master_data.yaml::sub_contracts` 에 reference 추가

DoD: contract 1.0.0 active + 회귀 testpack T4 입력 fixture 동결.

### T4 — TestPack 작성

- [ ] `test/test_c9_master_special.py` 신설:
  - `test_upsert_visible_in_list` (AC-SPC-1)
  - `test_permission_guard` (AC-SPC-2 — `master.special.write` 미보유 → 403)
  - `test_audit_diff_recorded` (AC-SPC-3 — `audit_master` 테이블에 before/after JSON 기록)
  - `test_invalid_class_code_rejected` (AC-SPC-4 — enum 외 → 422)
  - `test_in_clause_lookup_chunk_applied` — list 응답에서 거래처명 join 시 `in_clause_lookup` 헬퍼 사용 검증 (DEC-033 e)
  - `test_count_grouped_total` — list 의 `total` 산출이 `count_grouped` 헬퍼 사용 검증 (DEC-033 d, mysql3 안전)
- [ ] fixture: `test/fixtures/G1_Ggeo_special.csv` (10행 — 플래그 ON/OFF 혼합 + 카탈로그 4종)

DoD: 테스트 6/6 RED 상태로 PASS 게이트 정의(T5 구현 후 GREEN).

### T5 — Backend 구현

- [ ] `backend/app/services/masters_service.py`:
  - `async def list_special(server_id, *, class_code=None, page=1, limit=100) -> tuple[list[dict], int]`
    - WHERE: `Special_flag='Y'` (+ class_code 옵셔널)
    - JOIN 거래처명: `in_clause_lookup` 헬퍼로 G1_Ggeo.Gname 청크 룩업
    - total: `count_grouped(server_id, "G1_Ggeo", where_sql, group_by="Gcode", params=...)` (mysql3 안전)
  - `async def upsert_special(server_id, customer_code, *, special_flag, special_class_code, memo, actor_id) -> dict`
    - read-after-write: 동일 트랜잭션에서 SELECT 1 회 보강
    - audit_master INSERT: before/after JSON diff
  - **DELETE 미구현** (DEC-019 정책 준수)
- [ ] `backend/app/routers/masters.py`:
  - `GET /api/v1/masters/special` (`special.read` 권한)
  - `PUT /api/v1/masters/special/{customer_code}` (`special.write` 권한 + `If-Match` ETag — DEC-042)
- [ ] `backend/app/core/permissions.py`:
  - `master.special.{read,write}` 키 추가
  - `seed/web_admin.json::role-admin.permissions` + `role-branch_manager.permissions` 동기화
  - `permission-keys-catalog.md` 갱신
- [ ] BLS_IN_CHUNK_SIZE 환경변수 그대로 적용(추가 0건)

DoD: T4 회귀 6/6 GREEN + 인접 회귀(`test_list_count_grouped_mysql3.py`, `test_in_clause_lookup_chunked.py`, `test_c10_phase1_perms.py`) 무회귀 + tsc 0.

### T6 — Frontend 구현

- [ ] `app/(app)/master/special/page.tsx` 교체:
  - `<ScreenPlaceholder>` 제거
  - `DataGridPager` + `recommend-page-size` 적용 (DEC-024/025)
  - 컬럼: 거래처코드 / 거래처명 / 분류 / 비고 / 수정시각 (5컬럼)
  - 행 클릭 → 우측 슬라이드 입력 폼 (`Sobo45_billing` 패턴 재사용)
  - `master.special.write` 미보유 시 입력 폼 read-only + 「권한 없음」 배지
  - `data-legacy-id` 부착 — Sobo16 매핑 노트 §5 정본 준수(DEC-028)
- [ ] `lib/masters-api.ts`:
  - `specialApi.list({classCode?, page?, limit?})` (GET)
  - `specialApi.upsert(customerCode, payload, etag)` (PUT + `If-Match` 헤더 — DEC-042)
- [ ] form-registry.ts: `Sobo16_special.phase` `phase2` → `phase1` (T8 단계에서 수행 — 본 단계는 코드만 준비)
- [ ] i18n: `i18n/master-special.ko.json` (라벨 5건)
- [ ] tsc 0 / eslint 0 / 인접 페이지 회귀 0

DoD: 화면 진입 → list 100건 표시 → 행 선택 → 슬라이드 입력 → 저장 → 즉시 반영 + audit 영속.

### T7 — 5축 회귀 (DEC-053 §1 5축)

- [ ] `analysis/audit/phase1-component-fidelity.md` §3 에 §AH(Sobo16_special) 신설:
  - W (Widget) — 매핑 노트 §5 위젯 17개 부착 PASS / OOS 4건 명시
  - B (Business) — Button001~009 → REST endpoint 매핑 PASS (insert/update 만 노출, delete 는 OOS DEC-019)
  - U (User flow) — TabOrder Edit101→102→103→104→Button001 보존 + 분류 콤보 단축키
  - D (Data) — DBGrid101 5컬럼 1:1 매핑 + audit 보강(deltas)
  - O (Out-of-scope) — 인쇄·바코드·물리삭제·고객사 분기 4건 §6 명시
- [ ] §2 매트릭스 34행 정식 편입(33→34)
- [ ] GAP-P0 / P1 / P2 한 단어 평가 + P0 = 0 가드

DoD: §AH PASS / OOS 합계 5축 모두 정의 + GAP-P0 = 0.

### T8 — 동결 + phase1 정식 승격

- [ ] `form-registry.ts::Sobo16_special.phase` `phase2` → `phase1` + `scenario` 필드 제거
- [ ] `dashboard/data/phase2-screen-cards.json::Sobo16_special` T8=done + 다음 사이클 카드 제거 예정 메모
- [ ] `legacy-analysis/decisions.md` DEC-053 §운영 보강 (phase1 정식 승격 사례 1건)
- [ ] `dashboard/data/timeline.json` improvement 항목 추가
- [ ] `dashboard/data/web-porting-progress.json` frontend 블록 항목 추가
- [ ] 사이드바 P2 amber 배지 → CheckCircle2 초록 체크 자동 전환 검증

DoD: 본 plan §1 T1~T7 모두 done + 사이드바 표기 자동 전환 + 회귀 0.

---

## 2. 위험 요소 + 완화

| 위험 | 영향 | 완화 |
| --- | --- | --- |
| BLK-SPC-1 SQL 추출 지연 → T2 stalled | T3~T8 전체 stall | query_capture 실행을 T1 매핑 노트와 병행 → 양 작업 dependency 단방향 해제 |
| BLK-SPC-2 분류 카탈로그 합의 지연 | T3 contract 1.0.0 미달 | 단계적 enum: 1차 `OTHER` 만 + 2차 비즈니스 합의 후 enum 추가 (Backwards compatible) |
| `master.special.{read,write}` 권한 신규 → C10 시드 회귀 | RBAC 시드/감사 회귀 | T5 작업에 시드 동기화 항목 명시 + `test_c10_phase1_perms.py` 보강 |
| mysql3 raw socket 에서 list 응답 stall | T5 백엔드 회귀 | T5 구현 의무: `count_grouped` + `in_clause_lookup` 헬퍼 사용 + T4 가드(`test_count_grouped_total`, `test_in_clause_lookup_chunk_applied`) |
| 모바일웹 「특별관리」 화면과 캡션·컬럼 불일치 | UX 회귀 | T1 §11 모바일웹 캡처 비교 + T7 §AH U 축에 단축키/탭 순서 PASS 가드 |

---

## 3. 인접 변경 (작업 외부 영향 0 검증)

- DEC-019/023 — 정책 무변경. PATCH ON / DELETE OFF 그대로 적용.
- DEC-033 (d/e) — `count_grouped` + `in_clause_lookup` 헬퍼 의무 사용 (T5 코드 변경 0 — 헬퍼 호출만).
- DEC-042 — PUT 의 If-Match/ETag 표준 그대로 적용.
- DEC-053 — phase1 승격 게이트 GAP-P0 = 0. T7 에서 가드.
- DEC-051/052 — 인증 서버 단일화 / Primary 데이터 서버. 본 화면 영향 0 (단일 서버 호출).

---

## 4. 일정 (제안)

| 단계 | 기간 | 의존 | 비고 |
| --- | --- | --- | --- |
| T1 | 0.5d | — | 매핑 노트 신설 |
| T2 | 1d | BLK-SPC-1 / BLK-SPC-2 | 외부 의존 (담당자/비즈니스) |
| T3 | 0.5d | T2 done | contract 1.0.0 |
| T4 | 1d | T3 | 회귀 6건 RED |
| T5 | 1.5d | T4 | backend + 권한 시드 |
| T6 | 1.5d | T5 | frontend + i18n |
| T7 | 0.5d | T6 | 5축 audit §AH |
| T8 | 0.5d | T7 | phase1 정식 승격 + 동기화 |
| **합계** | **7d** | (외부 blocker 해소 시점에 종속) | T2 외부 대기 시간 별도 |

---

## 5. 참조

- `analysis/screen_cards/Sobo16.md`
- `migration/contracts/special_master.yaml`
- `migration/contracts/master_data.yaml`
- `legacy-analysis/decisions.md` DEC-019, DEC-023, DEC-028, DEC-033(d/e), DEC-042, DEC-053
- `analysis/audit/phase1-component-fidelity.md`
- `dashboard/data/phase2-screen-cards.json::Sobo16_special`
- `migration/coverage/placeholder-t1-t2-index.md` §1 #1 (BLK-SPC-1 출처)
- `legacy_delphi_source/legacy_source/Subu16.{dfm,pas}`

---

*최초 작성: 2026-04-21 — 사이드바 「기초관리」 정합화 사이클(Sobo39_1/_2/_5/Sobo19 stub 제거)과 함께 본 plan 신설.*
