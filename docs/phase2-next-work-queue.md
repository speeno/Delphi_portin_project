# Phase2 후속 작업 큐

## 작성 목적

운영·통계 Phase2 승격 마감 이후 남은 개발 대상을 다음 스프린트 입력으로 분리한다. 이번 승격 대상은 `form-registry.ts`에서 phase1로 전환했으며, 아래 항목은 **아직** 구현 또는 차단 해소가 필요하다(§2 정산·인쇄 잔여는 2026-04-26 재분류로 **완료·아카이브**).

## 1. Sobo16_special 특별관리

우선순위: 높음

현재 상태:

- `dashboard/data/phase2-screen-cards.json::Sobo16_special` 은 `T2=in_progress`, `T3=blocked` 상태다.
- 기준 문서는 `docs/master-special-implementation-plan.md` 다.

다음 작업:

- `BLK-SPC-1`: `Subu16.pas` Button001~009 핸들러와 SQL을 재확인한다.
- `BLK-SPC-2`: `special_class_code` enum을 운영 표본 기반으로 합의한다.
- enum 합의가 지연되면 1차 구현은 `OTHER` 폴백을 허용하고, 실제 enum 확장은 후속 migration contract 변경으로 분리한다.

착수 조건:

- `migration/contracts/special_master.yaml` 의 blocker 해소 방향이 명확해야 한다.
- `analysis/layout_mappings/Sobo16.md` 를 먼저 작성해 DEC-028 widget/data-legacy-id 기준을 고정해야 한다.

## 2. 정산·인쇄 잔여 묶음 — 재분류 완료 (2026-04-26)

다음 4화면(+ `Sobo46_billing_bill` / `Sobo49_tax_bill` 별칭)은 **구현·회귀 근거**에 맞춰 `form-registry.ts` **phase1** + `dashboard/data/phase2-screen-cards.json` **T7/T8 done** 으로 동기화했다.

- **C5(기능·목록·미수 집계)**: `Sobo49_tax` 목록·stub, `Settle_outstanding` `GET /settlement/outstanding`, `Sobo41_slip` 입금 목록 기반 전표 — `test_c5_settlement_phase2.py`(TC-ST-P2_32/33 포함), `test_c5_settlement_optional_filters.py`.
- **C7(PDF 경로)**: `Sobo46`/`Sobo49` 단건 인쇄 PDF — `test_c7_print_phase1.py` (청구/세무 엔드포인트 흡수, C5와 책임 분리).
- **DEC-034/035**: 외부 세금계산서 채널 연동은 범위 밖 — HTML/PDF 미리보기·NOT_INTEGRATED stub 유지.

추가 후속은 없음(본 절은 아카이브 용도).

## 3. 보류 항목

아래 항목은 외부 합의 또는 SQL 미확정이 있어 후순위로 둔다.

- `Sobo48_compare`: 장부대조, 레거시 단일 SQL 미확정
- `Sobo28_delivery`: 출고택배관리, 택배사 API 연동 합의 필요
- `Sobo29_other`: 기타명세서, 비정형 출력 흐름 확정 필요
