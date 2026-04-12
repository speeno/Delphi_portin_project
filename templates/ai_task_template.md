# AI 작업 지시 템플릿

## 사용법
아래 템플릿을 복사하여 각 기능 포팅 시 AI에게 제공한다.
`{placeholder}`를 실제 값으로 대체한다.

---

## 템플릿

```
목표: {기존 Delphi 기능}의 {동작}을 동일하게 웹 API로 구현한다.

대상 기능:
  - Legacy Form: {폼명}
  - Legacy Event: {이벤트 핸들러명}
  - 관련 유닛: {유닛 파일 목록}
  - 관련 SQL: {SQL 식별자 목록}

제약:
  - 운영 DB 스키마 변경 금지
  - 기존 컬럼명 유지
  - 고객사 분기 삭제 금지
  - 미확실한 로직은 TODO로 남기고 추측 구현 금지

참조 자료:
  - Legacy Object Catalog: {object_id}
  - Event Flow Map: {해당 이벤트 흐름}
  - SQL Catalog: {관련 쿼리 목록}
  - Customer Variant Matrix: {관련 고객사 분기}

산출물:
  1. 분석 요약 (legacy-analysis/progress.md에 기록)
  2. API 계약 (migration/contracts/{contract_id}.yaml)
  3. 서비스 코드 (해당 모듈)
  4. 통합 테스트 (migration/test-cases/{eval_id}.json)
  5. 남은 리스크 목록 (legacy-analysis/known-risks.md에 기록)

검증:
  - 동일 입력 데이터로 DB delta 비교
  - 필수 validation 메시지 일치
  - 실패 케이스 3개 이상 테스트
  - 고객사 분기 테스트 ({variant 목록})
```

---

*문서 버전: v1.0*
*작성일: 2026-04-11*
