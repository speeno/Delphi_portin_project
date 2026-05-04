## 요약

<!-- 무엇을 왜 바꿨는지 한두 문단 -->

## 모델 티어 (계획 수립 시)

| 서브태스크 | 권장 티어 | 실행 시 모델 |
|------------|-----------|----------------|
| 계약 YAML·라우터·서비스·pytest·`data-legacy-id`·스모크 매트릭스 | 표준 | Cursor 기본·빠른 모델 |
| pas 이벤트/SQL/인쇄 레이아웃 동등 판단, 다테넌트 분기·DEC 문구, 다화면 갭 우선순위 | 고급 권장 | **Claude Opus 4.7 (Thinking)** — 해당 단계만 Chat/Agent에서 수동 전환 |

**모델 선택:** 표준 행은 기본 모델로 진행. 고급 권장 행만 사용자가 모델을 바꾼 뒤 그 단계를 재실행하면 된다. (저장소 규칙 `.cursor/rules/planning-model-tiers.mdc` 와 동일)

## 체크리스트

- [ ] 의도한 테스트·스모크(dry-run) 실행
- [ ] 신규 API 는 `debug/probe_backend_all_servers.py` 매트릭스 등록(해당 시)
- [ ] 멀티 DB: `sql_mysql3`·`<table>_adapt` 패턴 준수(해당 시)
