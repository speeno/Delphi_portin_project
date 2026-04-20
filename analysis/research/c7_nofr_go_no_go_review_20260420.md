# C7 비-FastReport (B5) — Go / No-Go 의사결정 회의록 (1차, 2026-04-20)

> **목적**: [c7-nofr-porting](../../) 계획의 § "권장 의사결정" 의 6번째 todo
> ("2주 PoC 결과 기반으로 수동유지/부분자동/전면자동 의사결정 회의록 확정") 산출물.
>
> **본 회의는 1차 회의** — 2주 PoC 트랙 (1주차: IR 사양 + decoder 1양식 / 2주차:
> compiler + runtime 병행) 의 **1일차 결과** 를 기반으로 *방향 동결* 을 한다.
> 후속 2 차 회의 (2주차 종료 후) 에서 본 결정을 재검토하여 최종 의사결정.
>
> **선결 산출물 (모두 완료, 2026-04-20)**:
> - [`c7_oss_discovery_log_20260420.md`](./c7_oss_discovery_log_20260420.md)
> - [`c7_oss_shortlist.md`](./c7_oss_shortlist.md)
> - [`c7_oss_license_matrix.md`](./c7_oss_license_matrix.md)
> - [`../print_specs/frf_ir_schema.md`](../print_specs/frf_ir_schema.md)
> - `debug/frf_decoder_poc.py` (Report_1_21.frf 1 양식 동작 검증)
> - `도서물류관리프로그램/backend/app/services/print_ir_compiler.py` (IR→HTML 컴파일러)
> - `도서물류관리프로그램/backend/app/services/label_service.py` (`PRINT_TEMPLATE_MODE=auto` feature flag 병행)
> - `test/test_c7_frf_decoder_poc.py` + `test/test_c7_print_phase3_auto_template.py` (25 테스트 PASS)

## 0. 회의 메타

| 항목 | 값 |
|---|---|
| 회차 | 1차 (2026-04-20, 방향 동결) |
| 사회 | (담당자 ___) |
| 참석 | (R&D, 운영 SME, 인쇄 SME, 거버넌스 ___) |
| 결정 권한 | 본 회의 = *권고안 동결* / 최종 결정 = 2 차 회의 |
| 다음 회차 | 2주차 종료 시점 (2026-05-04 ± 2d) |

## 1. PoC 1일차 측정치 (2026-04-20)

### 1.1. 정량 지표

| 지표 | 측정값 | 기준 (frf_ir_schema.md §7) | 판정 |
|---|---:|---|:---:|
| 디코더 — 식별 객체 수 (Memo*, Report_1_21.frf) | **19개** | ≥ 5개 | ✅ |
| 디코더 — 토큰 추출 (`expressions_dictionary`) | **5개** ([Gname]/[Gposa]/[Gadd1]/[Gadd2]/[Gpost]) | ≥ 4개 | ✅ |
| 디코더 — 좌표 정확도 | 1/19 (Memo05만 추출 성공) | ≥ 50% | ⚠️ **미달** (휴리스틱 v0 한계) |
| 컴파일러 — 자동 HTML 출력 길이 | 3486 바이트 | ≥ 2500 바이트 | ✅ |
| 컴파일러 — placeholder 치환 누락 | **0건** (`{{ ctx.` 잔존 0) | 0건 | ✅ |
| feature flag — `manual` byte-identical 보존 | ✅ (Phase 1 `Seep13.Label.*` data-legacy-id 그대로) | byte-identical | ✅ |
| feature flag — `auto` 활성 시 자동 HTML 산출 | ✅ (`frf-obj` + `Memo\d+` legacy id) | 동작 | ✅ |
| feature flag — IR 누락 양식 (form=4) graceful fallback | ✅ (manual 경로 자동 복귀) | 5xx 누설 0 | ✅ |
| 정적 회귀 게이트 — 신규 SQL 0 / 외부 SaaS 0 / Jinja2 require 0 / BSD-2 NOTICE | 4/4 | 4/4 | ✅ |
| 회귀 테스트팩 PASS 비율 | **25 / 25** = 100% | 100% | ✅ |
| 운영 의존성 추가 (운영 `requirements.txt`) | **0건** (Jinja2 require 회피) | 0건 | ✅ |

### 1.2. 정성 발견

- **F-01 (FreeReport BSD-2)** 의 알고리즘 *line-by-line Python 포팅* 은 본 PoC 에서
  *완전 구현 ❌* — 실제 디코더는 **휴리스틱 스캐너** (WORD-prefixed string 트리 인식)
  로 작성. 이는 v0 PoC 의 의도된 한계 (계획 §리스크 "decoder 를 strict parse +
  unknown capture 로 설계").
- 그러나 휴리스틱만으로도 **객체명 + binding 토큰 + 페이지/밴드 트리 구조** 까지는
  100% 식별 — IR→HTML 컴파일러가 최소한의 자동 템플릿 (placeholder 형태) 을
  생성하는 데 충분.
- **좌표 정확도 (1/19)** 가 가장 큰 리스크. 본 휴리스틱은 객체명 직후 4×int32 LE
  를 *맹목적으로* 좌표로 가설 — FreeReport 직렬화 규칙은 객체명 직후 *클래스 마커
  + 가변 길이 props* 가 먼저 오므로, 실제 좌표는 더 뒷쪽에 있다. v1 에서는
  F-01 의 `LoadFromStream` 을 정확히 포팅 필요.
- **데이터 매핑 미스매치 발견** — `.frf` 의 `[Gadd1]`/`[Gadd2]` 두 줄은 운영 `Sg_Csum`
  의 `Gadds` 단일 컬럼과 직접 호환 ❌. v1 에 *컬럼 매핑 어댑터* (`.frf` 토큰명 →
  운영 row 컬럼명) 가 별도 항목으로 필요.
- 라이선스 검증 (BSD-2 / MIT / BSD-3) 은 모두 운영 incorporate 가능. 추가 NOTICE
  의무도 자동 회귀 테스트로 가드 (S_04 BSD-2 NOTICE 보존).

### 1.3. 비용/일정 재추정 (1일차 데이터 반영)

| 단계 | 시드 추정 (계획) | 1일차 후 재추정 |
|---|---|---|
| OSS 게이트 + IR 동결 (R0~R1) | 1주 | 1일 (완료) ✅ |
| Decoder PoC 1양식 (R2) | 1주 | **2주 추가** (정밀 디시리얼라이저 = F-01 line-by-line 포팅) |
| 컴파일러 (R3) | (계획 외) | **0.5주** (PoC 완료, v1 안정화만) |
| Runtime 통합 + feature flag (R4) | 0.5주 | 0.2일 (완료) ✅ |
| 회귀 게이트 (R5) | 0.5주 | 0.5일 (완료, 시각 픽셀 diff 만 운영 도입 시 추가) |
| 컬럼 매핑 어댑터 (v1 신규 발견) | (없음) | **1주** |
| 1 양식 → 5 양식 확장 검증 | 1주 | **2~3주** |
| 1 양식 → 98 양식 확장 검증 | 2~3주 | **6~10주** (추정 폭 ↑, 변형 폭발 위험) |

**→ 부분 자동 (B 안) 의 인주 비용**: 5~6 인주 (라벨류 5건 + 단순 명세서)
**→ 전면 자동 (C 안) 의 인주 비용**: 12~18 인주 (98건, 변형 30건 포함)

## 2. 3 안 비교 매트릭스

| 안 | 정의 | 인주 비용 (재추정) | 운영 위험 | 디자인 변경 대응 | 결정 근거 |
|---|---|---:|---|---|---|
| **A 수동 유지** | DEC-039 그대로 — 양식별 빌더 함수 수동 작성, `.frf` 정본 참조용 | 0 (현 상태) | 매우 낮음 | 양식별 함수 수정 | Phase 1 5+1 양식 이미 운영, 회귀 0 |
| **B 부분 자동** | 라벨/단순 명세서만 IR→HTML 자동 컴파일, 복잡 양식은 수동 유지 | 5~6 인주 | 낮음 (auto 실패 시 manual fallback) | shared compiler 자동 흡수 | PoC 1일차로 라벨 1건 동작 검증 ✅ |
| **C 전면 자동** | 98 양식 모두 IR→HTML 컴파일, 수동 빌더 폐기 | 12~18 인주 | 중상 (변형 폭발 + 좌표 정확도) | shared compiler | PoC 단일 양식 결과로는 *조기 결정 위험* |

### 2.1. 평가 차원 (각 1~5 점)

| 차원 | A 수동 | B 부분 자동 | C 전면 자동 |
|---|---:|---:|---:|
| 단기 ROI (3개월 내) | 5 | 4 | 1 |
| 중기 ROI (1년 내) | 3 | 4 | 4 |
| 장기 ROI (3년 내) | 2 | 4 | 5 |
| 운영 안정성 | 5 | 4 | 2 |
| 디자인 변경 대응 속도 | 2 | 4 | 5 |
| 라이선스/거버넌스 위험 | 5 | 5 | 4 |
| 인력 수급 (Python only) | 5 | 5 | 4 |
| **합계 (35점 만점)** | **27** | **30** | **25** |

## 3. 1차 권고안 (회의 후 동결, 2 차 회의에서 재검토)

### 3.1. 결정

- **방향 권고: B 안 (부분 자동) 으로 *2주차 PoC 진입***. C 안 (전면 자동) 은
  2주차 결과로 별도 재평가.
- **단기 운영 (Phase 1+2-α): A 안 유지** — DEC-039 정책 깨지 않음. `auto` feature
  flag 는 *기본 비활성* (`PRINT_TEMPLATE_MODE` env 미설정 = manual).
- **2주차 PoC 범위**:
  1. Decoder 정밀화 — F-01 의 `LoadFromStream` 을 line-by-line Python 포팅 (좌표
     정확도 ≥ 90% 목표).
  2. 컬럼 매핑 어댑터 — `.frf` 토큰명 ↔ 운영 row 컬럼명 mapping table 도입
     (예: `Gadd1`/`Gadd2` → split(`Gadds`)).
  3. 라벨 5종 (`Report_1_21` ~ `Report_1_25`) 자동 템플릿 생성 + form=1~5 모두
     auto 모드 통과.
  4. 시각 픽셀 diff 게이트 추가 (pdftoppm + Pillow / `dssim` 등) — 수동 정본
     vs 자동 산출 ≤ 5% 픽셀 diff.

### 3.2. 후속 결정 (2 차 회의 진입 전)

| 트리거 | 다음 결정 |
|---|---|
| 2주차 — 좌표 정확도 ≥ 90% + 라벨 5종 모두 auto 모드 회귀 PASS | **B 안 운영 도입 결정** (라벨류만 PRINT_TEMPLATE_MODE=auto 운영 적용, 1주 모니터링 후 확장) |
| 2주차 — 좌표 정확도 < 90% / 라벨 5종 중 1건이라도 회귀 FAIL | **A 안 유지** (DEC-039 그대로, R&D 트랙 종결 또는 1주 추가 연장) |
| 2주차 — 라벨 5종 모두 PASS + 단순 명세서 (P1-C/E) 도 자동 변환 가능 | **C 안 부분 진입 검토** (단순 양식 ~ 30건만 자동 확장) |

### 3.3. 비-결정 사항 (회의에서 명시적으로 *결정 보류*)

- 본 회의는 **C 안 (전면 자동) 의 가부 결정 ❌** — 1 양식 결과로는 변형 폭발
  리스크 평가 불가능. C 안은 라벨 5종 + 단순 명세서 8종 (= 13종) 결과 누적 후
  3 차 회의에서 재논의.
- DEC-037 (PDF 엔진 = WeasyPrint) 변경 ❌. PoC 트랙은 항상 WeasyPrint 호환 HTML
  만 산출.
- 외부 SaaS / 상용 SDK 도입 ❌ (DEC-044 / 라이선스 매트릭스 §3).

## 4. 이행 책임자 / 일정

| 항목 | 책임 | 마감 |
|---|---|---|
| 2주차 PoC — F-01 정밀 포팅 | (R&D ___) | 2026-04-27 |
| 2주차 PoC — 컬럼 매핑 어댑터 | (R&D ___) | 2026-04-29 |
| 2주차 PoC — 라벨 5종 IR + 자동 템플릿 검증 | (R&D + 인쇄 SME ___) | 2026-05-02 |
| 시각 픽셀 diff 게이트 신설 | (R&D ___) | 2026-05-04 |
| 2 차 회의록 작성 | (사회 ___) | 2026-05-04 |

## 5. 거버넌스 동기화

- **DEC 신규 후보 (2 차 회의 후 확정)**: `DEC-044` (R&D 트랙 — PRINT_TEMPLATE_MODE
  feature flag 정책, manual 기본 / auto 옵트인) — 본 회의에서는 *예약* 만, 등록 ❌.
- **OQ 신규 후보**: `OQ-PR-3` (라벨 5종 + 단순 명세서 자동 템플릿 정확도 게이트
  통과 여부) — 2 차 회의 결과로 close.
- **계획 동기화**:
  - [`c7-nofr-porting`](../../) plan: 본 1 차 회의로 todo 6 = `completed` 처리.
  - 2 차 회의록 작성 시 별도 plan re-enable 권장.

## 6. 변경 이력

| 일자 | 회차 | 결정 |
|---|---|---|
| 2026-04-20 | 1 차 | B 안 권고 + 2주차 PoC 진입. 단기 운영은 A 안 (manual) 유지. C 안은 2 차 회의에서 재평가. |
| (예정) 2026-05-04 | 2 차 | 좌표 정확도 / 라벨 5종 회귀 결과 기반 최종 결정. |
