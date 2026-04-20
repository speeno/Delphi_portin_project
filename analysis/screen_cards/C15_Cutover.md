# 시나리오 카드: C15 — 데이터 마이그레이션/Cut-over

_생성: 2026-04-20 — C10 이후 확장 라인 v0.1 (골격)_

> **사용자 명시 제약**: 본 사이클은 **외부 시스템 연동 제외**. 즉 외부 마이그레이션 SaaS (AWS DMS, Azure Migrate 등), 외부 데이터 변환 서비스 직결은 본 페이즈 out-of-scope. 자체 파이썬 스크립트 + 운영 DBA 수기 절차만.

## 0. 한눈 요약

- **시나리오 ID**: C15 (Cut-over — C10 의 C15 동시편집 흡수 시나리오와 다른 별도 확장 라인)
- **명칭**: 데이터 마이그레이션/Cut-over (레거시 → 모던 전환)
- **상태**: PENDING (스코프 정의 완료, 실행 대기 — 운영 일정 의존)
- **단계 (stages)**: 7 (Cut-over)
- **레거시 등가**: 없음 (전환 자체가 모던 진입)
- **선행 의존**: C1~C10 + C11/C13/C14 모두 안정 + 운영팀 cut-over 윈도우 합의

## 1. 범위

| 영역 | 내용 |
|---|---|
| 데이터 인벤토리 | `Id_Logn` (사용자) + `S1_Ssub`/`S2_Stra` (출고) + `R1_Rsub`/`R2_Rtra` (반품) + `Sv_Ghng` (재고) + 마스터 (G4_Book/G3_Sang/G1/G2_Ggeo) — 각 테이블 row 수 추정 + cut-over 시간 |
| 마이그레이션 절차 | (a) 마지막 영업일 종료 후 운영 lock (b) mysqldump + 신규 환경 import (c) 스키마 어댑터 (DEC-033 t5_ssub_adapt 등) 검증 (d) 1차 검증 (count + checksum) (e) 사용자 검수 (f) 운영 전환 |
| 롤백 시나리오 | 신규 환경에서 24h 이내 critical bug 발생 시 → 레거시 EXE 복구 + 신규 환경 데이터 손실 (read-only 우회) |
| 4 server 동시 cut-over vs 단계적 | 138 파일럿 → 153 → 154/155 (mysql3 폴백) — 점진적 전환 권장 |

## 2. 산출물 (v0.1)

- `migration/contracts/cutover.yaml` v0.1 — cut-over 절차 표준 (timeline + 검증 체크리스트)
- `analysis/handlers/c15_cutover.md` — 인벤토리 + 마이그레이션 매트릭스 (테이블 × 4 server)
- `tools/migration/cutover_validator.py` — count/checksum 검증 자동화 (신규)
- `docs/cutover-runbook.md` — 운영팀용 절차서 (T-호 단위 분단위 일정)

## 3. DoD

1. 4 server 모두 cut-over 검증 자동화 완료 — `tools/migration/cutover_validator.py` 가 100% PASS
2. 24시간 운영 검증 후 0 critical (P0/P1) 결함 — 레거시 EXE 종결
3. 사용자 만족도 검수 (UAT 합격) — 핵심 시나리오 7종 (C2/C3/C4/C5/C6/C7/C8) 모두 운영 시연 PASS
4. 롤백 절차 1회 dry-run 완료 — 실 롤백 발생 시 15분 내 복구 가능 검증

## 4. 결정 게이트 (의존 OQ/DEC)

- **OQ-CUT-1 (신규)**: cut-over 윈도우 — 영업일 외 시간대 (주말/연휴) + 합의된 다운타임 허용 시간 (4h? 8h?)
- **OQ-CUT-2 (신규)**: 4 server 동시 vs 단계 — 운영팀 인력/리스크 trade-off
- **OQ-CUT-3 (신규)**: 레거시 EXE 종결 시점 — 신규 안정화 후 1주? 2주? 1개월?
- **DEC-033 의존**: mysql3 호환 (154/155) cut-over 시 schema_adapter 정합 검증
- **DEC-041/042 의존**: cut-over 후 멀티 사용자 동시 접속 시 If-Match/ETag 부하 검증
- **외부 시스템 연동 제외**: 외부 SaaS 마이그레이션 도구는 별도 사이클

## 5. 변경 이력

- 2026-04-20 — v0.1 골격 (C10 이후 확장 라인)
