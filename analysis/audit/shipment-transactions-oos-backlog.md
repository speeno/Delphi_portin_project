# 출고·거래관리 OOS 백로그 (2026-06)

공통 검색창 rollout 이후에도 남아 있는 출고·거래관리 범위 외 항목을 별도 트랙으로 분리한다.

| ID | 항목 | 현재 상태 | 후속 트랙 |
| --- | --- | --- | --- |
| OOS-OUT-PRINT | Sobo27 출고증 인쇄 라디오/인쇄 워크플로 | 미구현 | C7 인쇄 |
| OOS-OUT-PANEL | Sobo27 Panel004/005/007(자동알람·신간필터·진행바) | 미구현 | Phase 2 |
| OOS-INQ-PUB | Sobo21 출판사 검색 Edit107/108 | 미구현 | C6 후속 |
| OOS-S67-PRINT | Sobo67 인쇄/전표편집 | 미구현 | C7 인쇄 |
| C8-BARCODE | 스캔 장치 연동 고도화(출고/입고 라인 매칭) | 부분 구현 | C8 바코드 |

## 운영 원칙

- 공통 검색창 rollout(PR 범위)과 OOS 기능 구현을 혼합하지 않는다.
- OOS 구현 시에도 `data-legacy-id`·`customer_variants`·멀티 DB 룰(DEC-033)을 유지한다.
