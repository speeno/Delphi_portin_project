# Phase2 후속 작업 큐

## 작성 목적

운영·통계 Phase2 승격 마감 이후 남은 개발 대상을 다음 스프린트 입력으로 분리한다. 이번 승격 대상은 `form-registry.ts`에서 phase1로 전환했으며, 아래 항목은 **아직** 구현 또는 차단 해소가 필요하다(§2 정산·인쇄 잔여는 2026-04-26 재분류로 **완료·아카이브**).

## 모델·피드백 운영 (초안)

이 큐를 실행할 때는 [`.cursor/rules/planning-model-tiers.mdc`](../.cursor/rules/planning-model-tiers.mdc) 에 맞춘다.

- **다양한 모델**: 서브태스크(화면·단계·PR 단위)마다 Cursor Chat/Agent의 **모델 드롭다운**에서 사용자가 선택한다. 에이전트는 특정 상용 모델명을 강제하지 않고, 플랜·표에 **표준 vs 고급 권장**만 적는다.
- **실행 전 합의**: 이번 세션에서 다룰 우선순위 범위와, 항목별 표준 티어로 진행할지 고급 권장 구간이 있는지 짧게 맞춘 뒤 착수한다.
- **피드백 후 진행**: 화면 단위 또는 T1~T8 단계 단위로 산출을 사용자에게 확인받고, 승인·수정 요청에 따라 다음 항목으로 넘어가거나 동일 항목을 **다른 모델로 재실행**할 수 있다.
- **한계**: IDE가 모델을 자동 전환하지 않으므로, 고급 권장 구간은 실행 직전 **드롭다운에서 모델을 바꿀지** 사용자에게 안내한다.

## 1. Sobo16_special 특별관리 — 완료 (2026-04-29)

우선순위: 높음

완료 상태:

- `Sobo16_special` 은 `G6_Ggeo` 목록 조회 + `Grat1`/`Gssum` 부분 수정 범위로 phase1 승격했다.
- 기준 문서는 `docs/master-special-implementation-plan.md`, 매핑은 `analysis/layout_mappings/Sobo16.md`, 계약은 `migration/contracts/special_master.yaml` 이다.
- 후속 범위는 신규 G6 행 INSERT, 물리 DELETE, Gcode/Bcode 변경이며 phase1 범위 밖으로 둔다.

## 2. 정산·인쇄 잔여 묶음 — 재분류 완료 (2026-04-26)

다음 4화면(+ `Sobo46_billing_bill` / `Sobo49_tax_bill` 별칭)은 **구현·회귀 근거**에 맞춰 `form-registry.ts` **phase1** + `dashboard/data/phase2-screen-cards.json` **T7/T8 done** 으로 동기화했다.

- **C5(기능·목록·미수 집계)**: `Sobo49_tax` 목록·stub, `Settle_outstanding` `GET /settlement/outstanding`, `Sobo41_slip` 입금 목록 기반 전표 — `test_c5_settlement_phase2.py`(TC-ST-P2_32/33 포함), `test_c5_settlement_optional_filters.py`.
- **C7(PDF 경로)**: `Sobo46`/`Sobo49` 단건 인쇄 PDF — `test_c7_print_phase1.py` (청구/세무 엔드포인트 흡수, C5와 책임 분리).
- **DEC-034/035**: 외부 세금계산서 채널 연동은 범위 밖 — HTML/PDF 미리보기·NOT_INTEGRATED stub 유지.

추가 후속은 없음(본 절은 아카이브 용도).

## 3. 보류 항목

아래 항목은 외부 합의 또는 SQL 미확정이 있어 후순위로 둔다. 상세·다음 단계는 [`migration/contracts/phase2_screen_blockers.yaml`](../migration/contracts/phase2_screen_blockers.yaml) 및 [`migration/contracts/courier_management.yaml`](../migration/contracts/courier_management.yaml) 의 `implementation_schedule` 를 단일 원천으로 한다.

- `Sobo48_compare`: 장부대조, 레거시 단일 SQL 미확정
- `Sobo28_delivery`: 출고택배관리 — **내부** 라인/메모 구현은 완료, **외부** 택배사 API는 계약서상 별도 후속 (`courier_management.yaml`)
- `Sobo29_other`: 기타명세서, 비정형 출력 흐름 확정 필요
