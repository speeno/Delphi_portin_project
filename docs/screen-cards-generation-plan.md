# 화면 카드 자동 생성 계획 (analysis/screen_cards/) — 선택 산출물

화면(폼) 단위 포팅 직전에 “이 화면을 짜려면 어떤 자료가 필요한가”를 1장에 모은 카드.
포팅 작업자가 매번 여러 JSON·PAS 파일을 뒤지지 않게 하기 위한 **개발자 가이드 카드**입니다.

> 본 문서는 **계획 + 도구 사양**입니다. 실제 자동 생성 스크립트(`tools/analysis/screen_card_builder.py`)는 후속 작업으로 분리합니다 — 화면 단위 포팅이 시작될 때 즉시 활용할 수 있도록 설계만 미리 동결합니다.

## 1. 산출물 위치·명명

- 디렉터리: `analysis/screen_cards/`
- 파일명: `<form_name>.md`  (예: `Subu00.md`, `Sobo13.md`)
- 인덱스: `analysis/screen_cards/INDEX.md` (자동 생성)

## 2. 카드 1장 — 표준 구성

```markdown
# 화면 카드: <form_name> (<form_class>)

## 0. 한눈 요약
- 파일: <dfm 경로>, <pas 경로>
- 컴포넌트 수 / 이벤트 수 / 주요 컴포넌트 종류
- 핵심 SQL 수 / 영향 테이블 수 / 검증 규칙 수
- 매핑 시나리오: C? (있다면)

## 1. UI 구성
- 컴포넌트 트리(요약: TButton/TEdit/TStringGrid 개수)
- 화면 레이아웃 메모(가능하면 form_layouts/<form>.json 활용)

## 2. 이벤트 흐름
- 핸들러 목록(OnClick/OnShow/OnClose 등)
- 호출 체인 요약(unit_dependency_graph.json 기반)

## 3. 데이터 액세스 (SQL)
- query_catalog.json에서 같은 unit/form의 SQL 발췌
- 영향 테이블(테이블 단위 작업 빈도)

## 4. DB 영향
- db_impact_matrix.json 표 발췌
- 트랜잭션 경계(추정)·INSERT/UPDATE/DELETE 분포

## 5. 검증 규칙
- validation_rules.json에서 form 키로 발췌

## 6. 고객사 분기
- customer_variants.json에서 관련 항목

## 7. 관련 OQ·GAP·DEC
- open-questions.md / db-logic-porting-gap-report.md / decisions.md 링크

## 8. 인쇄·바코드 연관
- legacy-print-scanner-integration-survey.md 매칭

## 9. 포팅 체크리스트(자동 생성)
- [ ] 본 화면을 다루는 Migration Contract가 있는가?
- [ ] 5축 임계값(eval-axes-and-dod-draft.md)이 정해졌는가?
- [ ] 본 화면 SQL이 query_capture로 보강되었는가?
```

## 3. 자동 생성 스크립트 사양 (`tools/analysis/screen_card_builder.py`)

### 3.1 입력

| 입력 | 경로 |
|------|------|
| 폼 인벤토리 | `analysis/form_inventory.json` |
| 이벤트 흐름 | `analysis/event_flow.json` |
| SQL 카탈로그 | `analysis/query_catalog.json` |
| DB 영향도 | `analysis/db_impact_matrix.json` |
| 검증 규칙 | `analysis/validation_rules.json` |
| 고객사 분기 | `analysis/customer_variants.json` |
| 의존성 그래프 | `analysis/unit_dependency_graph.json` |
| (선택) 폼 레이아웃 | `analysis/form_layouts/<form>.json` |
| (선택) 캡처 결과 | `debug/output/captured_queries_*.json` |

### 3.2 인터페이스

```bash
python3 tools/analysis/screen_card_builder.py \
    [--form Subu00] \           # 미지정 시 전체 폼 대상
    [--out analysis/screen_cards/] \
    [--with-capture debug/output/captured_queries_<server>_<date>.json] \
    [--rebuild-index]
```

### 3.3 출력

- 카드: `analysis/screen_cards/<form>.md` (위 §2 표준 구성)
- 인덱스: `analysis/screen_cards/INDEX.md`
- 통계 JSON(선택): `analysis/screen_cards/_stats.json` — 카드별 SQL 수, 검증 수, 캡처 매칭률

### 3.4 키 매칭 규칙

- 폼 ↔ unit/PAS 파일 매칭: `form_inventory.json`의 `file` → 디렉터리 같은 PAS 파일.
- 같은 form_class(예: `TSubu00`)가 여러 파일에 등장할 경우 모두 묶어 표기.
- query_catalog는 `unit` 키 기준으로 묶고, “form ↔ unit” 매핑이 없으면 `<unmapped>` 섹션에 분류.

## 4. 우선 생성 대상 (착수 시)

[`docs/core-scenarios-candidates.md`](core-scenarios-candidates.md)의 베타 라인부터:

1. `Subu00` (로그인·메인 MDI, C1)
2. 출고 접수(`Sobo13` 등 — 회의 후 최종 폼 확정)
3. 인쇄 진입점(`Tong04`의 `Print_*` 그룹, C7)
4. 바코드 진입점(`Tong08` + 호출 대상 폼, C8)
5. 거래/잔액 조회(C6)

## 5. 운영 워크플로

- 화면 단위 포팅 직전:
  1. `screen_card_builder.py --form <form>` 실행 → 카드 갱신
  2. 카드 §3·§4를 보고 `migration/contracts/<flow>.yaml` 보강
  3. 카드 §9 체크리스트 충족 후 구현 착수
- 캡처 결과 갱신 시: `--with-capture` 옵션으로 카드의 §3 “캡처에서 추가 발견된 SQL” 섹션 자동 업데이트.

## 6. 후속 작업

- [ ] `tools/analysis/screen_card_builder.py` 스크립트 구현 (Sprint 1 후반 또는 Sprint 2 초)
- [ ] 첫 5장 자동 생성 → 작업자 피드백 수렴 → 표준 §2 보강
- [ ] CI에 “스키마/이벤트/SQL 변경 시 자동 재빌드” 훅 추가(선택)

## 7. 변경 이력

- 2026-04-21 — 계획·도구 사양 1차 작성 (포팅 직전 분석 작업 로드맵 5순위 산출물).

---

*관련: [`docs/core-scenarios-candidates.md`](core-scenarios-candidates.md), [`docs/eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md), `analysis/*.json`*
