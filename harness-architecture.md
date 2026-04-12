# 8계층 하네스 엔지니어링 아키텍처 설계서

## 1. 개요

### 1.1 왜 하네스 엔지니어링인가

델파이 시스템의 핵심 난이도는 "UI 이벤트와 비즈니스 로직의 강결합, 고객사별 분기, 숨겨진 규칙, 장비 연동"이 한 프로세스에 섞여 있다는 점이다. 하네스 엔지니어링은 **"AI가 레거시를 오해하지 않고, 작은 단위로 바꾸고, 자동 검증을 거쳐, 안전하게 이전하게 만드는 운영체계 설계"**이다.

### 1.2 5대 설계 원칙

| # | 원칙 | 설명 |
|---|------|------|
| 1 | 행위 보존 우선 | 코드 변환이 아니라 업무 행위(behavior) 보존이 목표. 버튼 클릭 후 어느 테이블이 갱신되는가, 유효성 검사 순서, 에러 메시지 시점, 저장 후 후처리가 기준 |
| 2 | 유스케이스 단위 분해 | 폼 단위가 아니라 탭/버튼/이벤트/업무 시나리오 단위로 분해 |
| 3 | AI가 읽기 쉬운 중간 표현 | 이벤트 흐름 표, SQL 카탈로그, 테이블 영향도 맵, 필드 사전, 고객사 분기표 등 구조화된 중간 산출물을 먼저 생성 |
| 4 | 항상 trace 남기기 | 근거 소스, 변환 규칙, 검증 테스트, diff, 불확실 영역을 모두 기록 |
| 5 | 평가 없는 자동화 금지 | 동일 입력 → 동일 결과를 정량 검증. eval 없이 "느낌상 좋아졌다" 금지 |

---

## 2. 8계층 아키텍처 상세

```
┌─────────────────────────────────────────────────┐
│                8-Layer Harness                   │
├─────────────────────────────────────────────────┤
│  L1  Asset Collection      (자산 수집)           │
│  L2  Static Analysis       (정적 분석)           │
│  L3  Task Decomposition    (작업 분해)           │
│  L4  Execution Tools       (실행 도구)           │
│  L5  Guardrails            (가드레일)            │
│  L6  State Tracking        (상태 추적)           │
│  L7  Evaluation            (평가)                │
│  L8  Approval / Deploy     (승인 / 배포)          │
└─────────────────────────────────────────────────┘

흐름: L1 → L2 → L3 → L4 (← L5 제약) → L6 → L7 → L8
                                         ↑ 회귀 시 L3으로 복귀
```

### L1 - 자산 수집 (Asset Collection)

**목적**: AI가 추론 가능한 구조화 입력으로 레거시 자산을 변환

**수집 대상**:
| 자산 유형 | 설명 | 파일 확장자/위치 |
|-----------|------|-----------------|
| 프로젝트 파일 | 전체 구조, uses 절 | .dpr |
| 유닛 소스 | 비즈니스 로직, 이벤트 핸들러 | .pas |
| 폼 정의 | UI 컴포넌트 구조 | .dfm |
| 공통 유닛 | 공유 라이브러리/유틸리티 | .pas (공통) |
| DB 접근 유닛 | TDataModule, 쿼리 컴포넌트 | .pas (DB) |
| 리포트/출력 유닛 | 인쇄 양식, 라벨 | .pas/.dfm (출력) |
| 배치/스케줄러 | 자동 실행 작업 | .pas (배치) |
| 장비 연동 코드 | 스캐너, 프린터, 저울 | .pas (장비) |
| 설정 파일 | INI, Registry, Config | .ini/.cfg |
| SQL 스크립트 | DDL, 프로시저, 뷰 | .sql |
| DB 스키마 | 테이블/인덱스/FK/트리거 | INFORMATION_SCHEMA |
| 운영 매뉴얼 | 사용자 가이드, 교육자료 | .doc/.pdf |

**표준화 출력**:
- `inventory/dpr_files.json` - 프로젝트 파일 목록
- `inventory/pas_files.json` - 유닛 파일 목록 (경로, 라인수, 유형)
- `inventory/dfm_files.json` - 폼 정의 파일 목록
- `inventory/sql_files.json` - SQL 스크립트 목록
- `inventory/db_schema.json` - DB 스키마 정보

### L2 - 정적 분석 (Static Analysis)

**목적**: 코드에서 지식을 추출하여 구조화

**추출 대상**:
1. **화면→기능→유닛→쿼리 맵**: 폼에서 어떤 유닛을 호출하고, 어떤 SQL을 실행하는가
2. **버튼→서비스→SQL→테이블 영향도**: 사용자 액션이 DB에 미치는 최종 영향
3. **전역 변수/싱글턴 의존성**: 글로벌 상태에 의존하는 로직
4. **예외 처리 패턴**: try/except, raise, ShowMessage 패턴
5. **메시지 박스/검증 로직**: 사용자에게 노출되는 경고, 에러
6. **숨겨진 비즈니스 규칙**: 코드 내부에만 존재하는 조건문 로직

**분석 도구**:
- 정규식 기반 .pas 파서 (SQL 추출, 이벤트 핸들러 추출)
- .dfm 텍스트 파서 (컴포넌트 트리, 이벤트 바인딩)
- uses 절 파서 (유닛 의존 관계 그래프)

**표준화 출력**:
- `analysis/event_flow.json` - 이벤트 흐름 맵 (산출물 #2)
- `analysis/query_catalog.json` - SQL 카탈로그 (산출물 #3)
- `analysis/db_impact_matrix.json` - DB 영향도 매트릭스 (산출물 #4)
- `analysis/validation_rules.json` - 검증 규칙 카탈로그 (산출물 #5)
- `analysis/dependency_graph.json` - 유닛 의존 관계

### L3 - 작업 분해 (Task Decomposition)

**목적**: AI에게 큰 단위로 주지 않고 검증 가능한 작은 단위로 분해

**분해 원칙**:
- ❌ "전체 WMS를 바꿔라"
- ✅ "frmInboundRegister의 신규등록 흐름만 분석해라"
  → "등록 버튼 클릭 시 SQL과 검증 규칙 추출"
  → "해당 기능을 REST API 계약으로 변환"
  → "기존 동작과 동일한 테스트 케이스 생성"

**분해 단위**: 기능 단위 입력 템플릿 (feature_input_template.yaml 참조)

**산출물**:
- Migration Contract (계약) - `migration/contracts/*.yaml`
- Eval Case (평가 케이스) - `migration/test-cases/*.json`

### L4 - 실행 도구 (Execution Tools)

**목적**: AI가 사용할 도구를 제한적으로 제공

**허용 도구 목록**:
| 도구 | 용도 | 위험도 |
|------|------|--------|
| 코드 검색기 (grep/rg) | .pas/.dfm 내 패턴 검색 | 낮음 |
| AST/파서 | 델파이 소스 구조 분석 | 낮음 |
| DB schema reader | INFORMATION_SCHEMA 읽기 | 낮음 |
| 샘플 데이터 loader | 테스트용 데이터 로딩 | 중간 |
| UI 스크린 캡처 비교 | 기존 화면 vs 신규 화면 비교 | 낮음 |
| HTTP API 테스트 도구 | REST API 호출 및 검증 | 중간 |
| SQL 실행 시뮬레이터 | SELECT 전용 읽기 쿼리 | 중간 |
| 로그 diff 도구 | 실행 로그 비교 | 낮음 |
| Git 브랜치 생성기 | 기능별 브랜치 관리 | 낮음 |
| test runner | 테스트 실행 및 결과 수집 | 낮음 |

### L5 - 가드레일 (Guardrails)

> 별도 문서: `guardrails.md` 참조

### L6 - 상태 추적 (State Tracking)

**목적**: 에이전트가 중간에 멈춰도 이어서 할 수 있게 기록 체계 유지

**파일 구조**:
```
legacy-analysis/
  progress.md           - 분석 진행 상태
  open-questions.md     - 미해결 질문
  decisions.md          - 의사결정 기록
  known-risks.md        - 알려진 위험
migration/
  contracts/*.yaml      - API 계약서
  test-cases/*.json     - 테스트 케이스 (Eval Cases)
```

**업데이트 규칙**:
1. 모든 분석 작업 완료 후 `progress.md` 업데이트
2. 불확실한 항목 발견 시 `open-questions.md`에 즉시 기록
3. 의사결정 발생 시 `decisions.md`에 배경/대안/영향 기록
4. 새로운 위험 식별 시 `known-risks.md`에 추가
5. API 계약 생성/변경 시 `contracts/` 하위에 YAML 파일 생성
6. 테스트 케이스 생성 시 `test-cases/` 하위에 JSON 파일 생성

### L7 - 평가 (Evaluation)

**5축 평가 체계**:

| 축 | 검증 대상 | 예시 |
|----|-----------|------|
| Outcome | 저장 결과, 계산 결과, 상태 변화 | 전표번호 생성 규칙 일치, 재고 수량 정확 |
| Process | 필수 validation, 트랜잭션, audit log | 필수 검증 수행 여부, 커밋/롤백 경계 준수 |
| UI/UX | 버튼 활성/비활성, 경고 문구, 포커스 이동 | 입력 focus 순서, 목록 갱신 타이밍 |
| Efficiency | 불필요 API 호출, DB round-trip | N+1 쿼리 없음, 불필요 조회 없음 |
| Variant | 고객사별 분기 유지 | A고객 저장규칙, B고객 라벨규칙 |

**합격 기준 (초안)**:
- Outcome: 동일 입력 → DB delta 100% 일치
- Process: 필수 validation 100% 수행, 트랜잭션 경계 일치
- UI/UX: 핵심 상호작용 90% 이상 동일 (사소한 시각적 차이 허용)
- Efficiency: 기존 대비 응답시간 150% 이내
- Variant: 고객사별 분기 100% 유지

### L8 - 승인/배포 (Approval/Deploy)

**6개 승인 게이트**:

| # | 게이트 | 시점 | 승인 주체 |
|---|--------|------|-----------|
| 1 | 분석 산출물 승인 | Sprint 1 완료 | M + P |
| 2 | API 계약 승인 | Sprint 2 완료 | M + P + 현업 |
| 3 | 고객사별 차이 승인 | Sprint 3 완료 | P + 현업 |
| 4 | 인쇄 결과 승인 | Sprint 4 중반 | P + 현업 |
| 5 | UAT 승인 | Sprint 5 완료 | P + 현업 + 관리자 |
| 6 | Cut-over 승인 | Sprint 6 시작 | 전원 + 경영진 |

---

## 3. 핵심 데이터 모델

### Legacy Object Catalog

```json
{
  "object_id": "frmInboundRegister.btnSaveClick",
  "type": "event_handler",
  "form": "frmInboundRegister",
  "unit": "uInboundForm.pas",
  "depends_on": [
    "uInboundService.SaveInbound",
    "uCommonValidation.RequireItemCode"
  ],
  "touches_tables": ["tb_inbound", "tb_stock", "tb_audit"],
  "customer_variants": ["A", "B"],
  "risk_level": "high"
}
```

### Migration Contract

```json
{
  "contract_id": "api.inbound.create",
  "legacy_source": ["frmInboundRegister.btnSaveClick"],
  "request_schema": {},
  "response_schema": {},
  "validation_rules": [],
  "side_effects": ["insert tb_inbound", "update tb_stock", "insert tb_audit"],
  "equivalence_tests": ["inbound-create-basic-001"]
}
```

### Eval Case

```json
{
  "eval_id": "inbound-create-basic-001",
  "input": { "item_code": "A100", "qty": 10 },
  "expected_db_delta": {
    "tb_inbound": "+1 row",
    "tb_stock.qty_change": "+10"
  },
  "expected_messages": [],
  "variant": "default"
}
```

---

## 4. 10대 표준 산출물

| # | 산출물 | 파일 | 생성 시점 |
|---|--------|------|-----------|
| 1 | Form Inventory | inventory/form_inventory.json | Sprint 1 |
| 2 | Event Flow Map | analysis/event_flow.json | Sprint 1 |
| 3 | SQL Catalog | analysis/query_catalog.json | Sprint 1 |
| 4 | DB Impact Matrix | analysis/db_impact_matrix.json | Sprint 1 |
| 5 | Validation Rule Catalog | analysis/validation_rules.json | Sprint 1 |
| 6 | Customer Variant Matrix | analysis/customer_variants.json | Sprint 1 |
| 7 | API Contract Spec | migration/contracts/*.yaml | Sprint 2 |
| 8 | Regression Test Pack | migration/test-cases/*.json | Sprint 2 |
| 9 | Migration Decision Log | legacy-analysis/decisions.md | Sprint 0~ |
| 10 | Known Unknowns List | legacy-analysis/open-questions.md | Sprint 0~ |

---

## 5. 권장 포팅 순서 (위험도 기반)

1. **1차 - 읽기 전용 조회 기능**: DB 변경 없이 결과 동일성만 검증
2. **2차 - 신규 등록 기능**: INSERT만 발생
3. **3차 - 수정/취소 기능**: UPDATE/DELETE, 트랜잭션 경계 검증 필수
4. **4차 - 배치/인쇄/장비 연동**: 현장 의존성 높음, 별도 승인 필요
5. **5차 - 고객사 커스터마이징**: 코드 분기 → 설정 기반 전환

---

## 6. 하네스 성숙도 로드맵

| 계층 | Sprint 0 | Sprint 1 | Sprint 2 | Sprint 3 | Sprint 4 | Sprint 5 | Sprint 6 |
|------|----------|----------|----------|----------|----------|----------|----------|
| L1 자산수집 | **구축** | **운영** | 운영 | 운영 | 운영 | 운영 | 완료 |
| L2 정적분석 | 설계 | **실행** | 운영 | 운영 | 운영 | 운영 | 완료 |
| L3 작업분해 | 설계 | 설계 | **실행** | 운영 | 운영 | 운영 | 완료 |
| L4 실행도구 | 조사 | **세팅** | 운영 | 운영 | 운영 | 운영 | → CI/CD |
| L5 가드레일 | **확정** | 운영 | 운영 | 운영 | 운영 | 운영 | 운영 |
| L6 상태추적 | **구축** | 운영 | 운영 | 운영 | 운영 | 운영 | → Audit Log |
| L7 평가 | 초안 | 초안 | **PoC** | **구현** | **운영** | 운영 | → 회귀테스트 |
| L8 승인배포 | 정의 | **게이트#1** | 게이트#2 | 게이트#3 | 게이트#4 | **게이트#5** | **게이트#6** |

---

*문서 버전: v1.0*
*작성일: 2026-04-11*
*작성자: 하네스 아키텍트 (메인개발자)*
