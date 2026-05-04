# DFM 기반 화면 포팅 — 실행 큐 (다음 사이클)

**전제:** DB 스모크 L4 DoD는 DEC-062(슈퍼유저 probe)로 정의됨. 멀티 DB에서 남는 5xx·스키마 차이는 런북·`customer_variants`·DEC로만 “허용”한다.

## 단일 원천

1. `docs/core-scenarios-porting-plan.md` — 시나리오·게이트·T1–T8 파이프라인.
2. `dashboard/data/porting-screens.json` — 화면별 `not_started` / `in_progress` / `review` / `done` 트래커 (`planDoc` 필드와 동기화).

## 권장 순서

1. **인벤토리** — `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/` 변형 폴더 포함 세트 목록 (`.cursor/rules/dfm-layout-input.mdc`).
2. **매핑 노트** — `analysis/layout_mappings/<Sobo*>.md` (TabOrder·그리드·이벤트 1:1).
3. **DFM↔registry** — 변경 전후 `tools/delphi_form_screen_matrix.py` + `docs/delphi-form-screen-equivalence-matrix.md` (DEC-060/061).
4. **구현** — 모던 페이지에 `data-legacy-id` 전부 부착.
5. **회귀** — 레거시 ID 누락 0건 테스트·`analysis/audit/phase1-component-fidelity.md` (phase1 승격 시).

## “큐”에서 고를 때

`porting-screens.json` 의 `lines` / 시나리오별 화면 객체에서 **`done` 이 아닌 항목**을 우선한다. 동일 우선순위가 여러 개면 `core-scenarios-porting-plan.md` 의 웨이브·게이트 순서를 따른다.

## 관련

- DEC-062: 스모크 probe  
- DEC-063: 위치 권한 목적·재요청 (운영 완결)  
- `docs/location-permission-runbook.md`
