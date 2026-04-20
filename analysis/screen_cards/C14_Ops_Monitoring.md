# 시나리오 카드: C14 — 운영 모니터링

_생성: 2026-04-20 — C10 이후 확장 라인 v0.1 (골격)_

> **사용자 명시 제약**: 본 사이클은 **외부 시스템 연동 제외**. 즉 외부 SaaS APM (Datadog/NewRelic/Sentry 호스티드), 외부 알림 채널 (Slack/Teams/PagerDuty), 외부 로그 집계 (ELK 호스티드/Splunk) 직결은 본 페이즈 out-of-scope.

## 0. 한눈 요약

- **시나리오 ID**: C14
- **명칭**: 운영 모니터링 (Self-hosted 인스트루먼테이션)
- **상태**: PENDING (스코프 정의 완료, 실행 대기)
- **단계 (stages)**: 6 (확장 라인)
- **레거시 등가**: 없음 (모던 신규 — Delphi 는 운영 모니터링 인프라 부재)
- **선행 의존**: C1~C10 전체 + Cut-over (C15) 일정 동기화

## 1. 범위

| 영역 | 내용 |
|---|---|
| 헬스체크 | `/api/v1/health` 확장 — DB 연결성 + 디스크 공간 + 응답 시간 (현재는 단순 200 OK) |
| 메트릭 | Prometheus exposition (`/metrics`) — 요청 수/지연/에러율/DB 풀 사용률 (self-hosted Prometheus 가정) |
| 로그 | 구조화 JSON 로그 + 로컬 파일 회전 (외부 ELK 직결 ❌) |
| 알림 | 임계 초과 시 운영 화면 (`/admin/ops`) 알림 배너 (외부 채널 ❌) |
| 감사 (audit) | 기존 `audit_settlement` / `audit_returns` / `audit_password_attempts` 통합 뷰 + admin 가드 (admin.audit.read 신규) |

## 2. 산출물 (v0.1)

- `migration/contracts/ops_monitoring.yaml` v0.1 — `/health` 확장 + `/metrics` + `/admin/ops` UI 계약
- `analysis/handlers/c14_ops.md` — 메트릭 카탈로그 (모던 정의, 레거시 무) + 임계값 정책
- `test/test_c14_ops_phase1.py` — 헬스체크 분기 + Prometheus exposition 포맷 + audit 뷰 권한 가드

## 3. DoD

1. `/health` 가 dependency 별 분리 응답 (DB/디스크/외부 서비스(없음)) — 503 부분 실패 시 정상 분리
2. Prometheus `/metrics` exposition 표준 포맷 (text-based, version 0.0.4) — `prometheus_client` Python 라이브러리 (Apache-2.0) 도입
3. 운영 알림 배너가 LocalStorage 가 아니라 서버 권위 (DB persisted 또는 in-memory 큐) — 다중 관리자 동시성 고려 (DEC-042 If-Match 정책 점검)
4. audit 통합 뷰가 admin.audit.read 가드 + d_select 본 사용자 데이터만 (DEC-041)

## 4. 결정 게이트 (의존 OQ/DEC)

- **OQ-OPS-1 (신규)**: 메트릭 보존 정책 — Prometheus retention (15d 디폴트) + DB audit 테이블 archival (월별 partition?)
- **OQ-OPS-2 (신규)**: 알림 임계값 — DB 연결 실패 0초 vs 30초, 응답 지연 P99 임계 (1s? 5s?)
- **DEC-033 의존**: 4 server (138/153/154/155) 모두 메트릭 노출
- **DEC-041 의존**: 운영 알림 배너 = 표준 응답 코드 (PERMISSION_DENIED 등) 와 별도 채널
- **외부 시스템 연동 제외**: 외부 APM/알림/로그 집계는 별도 사이클

## 5. 변경 이력

- 2026-04-20 — v0.1 골격 (C10 이후 확장 라인)
