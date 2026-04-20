# 시나리오 카드: C11 — 모바일/태블릿 UAT

_생성: 2026-04-20 — C10 이후 확장 라인 v0.1 (골격)_

## 0. 한눈 요약

- **시나리오 ID**: C11
- **명칭**: 모바일/태블릿 UAT (User Acceptance Testing)
- **상태**: PENDING (스코프 정의 완료, 실행 대기)
- **단계 (stages)**: 6 (확장 라인)
- **레거시 등가**: 없음 (모던 신규 — Delphi VCL 은 데스크톱 전용)
- **선행 의존**: C1~C10 (전체 백엔드 + 프론트엔드 1차 포팅 완료)

## 1. 범위

| 항목 | 내용 |
|---|---|
| 디바이스 매트릭스 | iOS Safari (iPad Pro/iPhone) + Android Chrome (Galaxy Tab/Pixel) — 각 2 모델, 2 OS 버전 |
| 화면 매트릭스 | C2 출고 + C3 입고 + C4 반품 + C8 스캔 = 4 핵심 시나리오 (현장 운영 시 모바일/태블릿 활용도 고) |
| 비포함 | C5 정산 / C7 인쇄 (PDF 다운로드) — 데스크톱 우선 사용처로 간주 |
| 검증 축 | (a) viewport ≤ 768px 반응형 (b) USB-OTG 바코드 스캐너 키보드 웨지 호환 (c) 터치 입력 (스와이프/롱탭) (d) 오프라인 큐 (선택) |

## 2. 산출물 (v0.1 — 페이즈 진입 시 본격화)

- `migration/contracts/mobile_uat.yaml` v0.1 — 디바이스/시나리오 매트릭스 + 합격 기준 정의
- `analysis/research/c11_mobile_responsive_audit.md` — Tailwind breakpoint 가이드 + 실측 스크린샷
- `test/test_c11_mobile_responsive.py` — Playwright/Cypress UAT 스위트 (디바이스 emulation)

## 3. DoD (Definition of Done)

1. 4 핵심 시나리오 (C2/C3/C8 + 일부 C4) 가 iPad/Galaxy Tab 에서 데스크톱 동등 워크플로우 실행 가능
2. USB-OTG 바코드 스캐너 (DEC-004 USB-HID 웨지) 가 모바일에서도 동작 — `lib/scanner.ts` 의 keydown 버퍼링이 모바일 가상 키보드와 충돌하지 않음
3. 터치 영역 ≥ 44×44 pt (Apple HIG) — 버튼/그리드 셀 모두 충족
4. 모바일 회귀 매트릭스 5 디바이스 × 4 시나리오 = 20 테스트 PASS

## 4. 결정 게이트 (의존 OQ/DEC)

- **OQ-MOB-1 (신규)**: USB-OTG 어댑터 호환 모델 매트릭스 — 운영 디바이스 인벤토리 합의 필요
- **DEC-004 / DEC-040 의존**: 스캐너 분기는 USB-HID 웨지 1차 (모바일에서도 동일 정책)
- **DEC-019 의존**: 단일 빌드 산출물 (반응형 CSS 분기, 별도 모바일 앱 미생성)

## 5. 변경 이력

- 2026-04-20 — v0.1 골격 (C10 이후 확장 라인)
