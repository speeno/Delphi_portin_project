# 거래관리(Menu200) P0 정본 폼 매핑 — Publisher/Distributor 확정

> 산출 근거(단일 원천): `analysis/welove_chul_menu_handlers.json`(메뉴→폼·Fxx),
> `analysis/welove_chul_menu_trees.json`(메뉴 캡션 트리), 가속기 산출물
> `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu*/Sobo*.meta.json`(추출 DFM 캡션).
> 작성 2026-05-31 (P0 `p0-menu-forms`). 거래관리 화면별 포팅(C1~C10) 착수 전 정본·갭 확정.

## 1. 결론 요약 (한 줄)

- **메뉴→폼→Fxx 매핑은 확정됐다** (아래 §2). Publisher·Distributor 표준 빌드의 「거래관리」(Menu200)는
  Menu201~209 → `TSobo21`~`TSobo29`, F21~F29 로 1:1 이다.
- **단, 가속기 추출 DFM(`legacy_source_root`)은 물류(출고관리) 빌드 트리**라서 `Subu23`~`Subu28` 폼은
  Publisher 정본이 **아니다**(§3). Publisher 입고현황·제작명세서·제작현황·원천징수 DFM 은 현재 산출물에 **없음** →
  해당 화면(C2/C6/C7/C8)은 **정본 DFM 재추출이 선행 조건**이다(`dfm-layout-input.mdc`).
- **내역조회(저자)는 표준 빌드 「거래관리」 트리에 존재하지 않는다**(§4). C10 은 정본 미확정 — preview 유지.

## 2. 메뉴 → 폼 → Fxx (확정 · BLD-PUB-STD = BLD-DIST-STD 동일)

`welove_chul_menu_handlers.json`(handlers) + `welove_chul_menu_trees.json`(거래관리 캡션 트리) 교차 확정.

| 메뉴 | 폼(유닛) | Fxx | Publisher 캡션 | 모던 route | registry id |
|------|---------|-----|----------------|-----------|-------------|
| Menu201 | TSobo21 | F21 | 거래명세서 | `/transactions/sales-statement` | `Sobo21` (phase1) |
| Menu202 | TSobo22 | F22 | 입고명세서 | `/transactions/inbound-statement` | `Sobo22_inbound_statement` (stub) |
| Menu203 | TSobo23 | F23 | 기타명세서 | `/transactions/other` | `Sobo29_other` (phase1) ※ id 주의 §5 |
| Menu204 | TSobo24 | F24 | 거래현황 | `/transactions/status` | `Sobo21_status_*` facade (phase1) |
| Menu205 | TSobo25 | F25 | 입고현황 | `/transactions/inbound-status` | `Sobo25_status_*` (stub) |
| Menu206 | TSobo26 | F26 | 제작명세서 | `/transactions/production/statement` | `Sobo26_production_stmt` (stub) |
| Menu207 | TSobo27 | F27 | 제작현황 | `/transactions/production/status` | `Sobo27_production_status` (stub) |
| Menu208 | TSobo28 | F28 | 원천징수 | `/transactions/withholding` | `Sobo28_withholding` (stub) |
| Menu209 | TSobo29 | F29 | 신간발행 | `/transactions/new-release` | `Sobo29_new_release` (stub) |

> registry 의 `licenseFkey`(F21~F29)는 위 handlers `license_keys_checked` 와 일치함을 확인했다.

## 3. 가속기 추출 DFM = 물류(출고관리) 빌드 — Publisher 폼 갭

가속기 `legacy_source_root` 의 `Subu*/Sobo*.meta.json` 캡션은 **물류 출고관리 폼**이다. 같은 유닛명이 빌드마다
다른 폼을 가리키는 델파이 패턴(`multi-db-compat.mdc` 의 빌드 변이와 동형) 때문에, 추출 캡션과 Publisher 캡션이
다음과 같이 어긋난다.

| 유닛 | 가속기 추출 캡션(물류) | Publisher 정본 캡션(Menu20x) | DFM 입력 가용? |
|------|----------------------|------------------------------|----------------|
| Sobo21 | 거래명세서 | 거래명세서 | ✅ 동일 |
| Sobo22 | 입고명세서 | 입고명세서 | ✅ 동일 (C1 착수 가능) |
| Sobo23 | 반품명세서 | 기타명세서 | ⚠️ 다른 폼 |
| Sobo24 | 반품재고(정품입고)-재생 | 거래현황 | ⚠️ 다른 폼 (단 거래현황은 facade 로 이미 phase1) |
| Sobo25 | 반품재고(반품입고)-해체 | **입고현황** | ❌ Publisher DFM 없음 (C2 블록) |
| Sobo26 | 출고접수현황 | **제작명세서** | ❌ Publisher DFM 없음 (C6 블록) |
| Sobo27 | 출고접수관리 | **제작현황** | ❌ Publisher DFM 없음 (C7 블록) |
| Sobo28 | 출고택배관리 | **원천징수** | ❌ Publisher DFM 없음 (C8 블록) |
| Sobo29 | 신간명세서 | 신간발행 | ✅ 사실상 동일 (C9 착수 가능) |

**결론**: C2/C6/C7/C8 은 **Publisher 소스(`WeLove_FTP/도서유통-출판`)에서 Sobo25/26/27/28 DFM 재추출**이
선행돼야 한다(가속기 입력 트리를 출판 빌드로 교체 후 재생성). 재추출 전에는 layout_mappings 정본을 만들 수 없으므로
phase1 승격 불가 — 해당 C 항목은 본 갭 해소까지 **STUB 유지**한다.

## 4. 내역조회(저자) — 표준 빌드 부재

- 7개 빌드 handlers 어디에도 「거래관리」 하위 저자 내역 메뉴가 없다. `TSobo13`(저자) 참조는 모두
  **Menu103**(기초관리 「저자관리」, F13/F17)뿐이다.
- 가속기 산출물에 저자 내역 폼 후보: `Subu13`=저자관리(master), `Seek30`=저자검색현황(검색 다이얼로그).
  `Subu13_1`=출고증정렬(무관).
- 스크린샷의 「내역조회(저자)」는 표준 출판/총판 빌드 「거래관리」에 없는 **물류 확장/비표준 메뉴**다.
- **C10**: 정본 미확정. 레거시 실행 환경에서 실제 메뉴 핸들러·Subu·SQL 을 확보하기 전까지 **preview 유지**.

## 5. 식별된 정합 메모 (후속 결정 필요)

1. **기타명세서 id**: handlers 는 Menu203→TSobo23(F23)이나 모던 registry 는 기타명세서를 `Sobo29_other`(Subu29,
   F29)로 매핑해 운영 중(phase1). 신간발행(Menu209→Sobo29)과 유닛이 겹쳐 보이는데, 이는 기존 결정으로
   본 P0 범위 밖. → A2 `sobo29-other-split-doc` 에서 `customer_variants` 로 정리한다.
2. **출고검증 폼**: 가속기 캡션은 `Subu59_2`=「출고 검증관리」, `Subu59_3`=「출고 검증관리(개별)」 이며
   `Subu59_1`=「일별 내역서(요약)」(검증 아님). 스크린샷의 「출고검증(1)/(2)/개별」 3분류 중 (1)은 표준 추출과
   불일치 → C3~C5 는 **Subu59_2/Subu59_3 을 정본**으로 하고, 「출고검증(1)」은 비표준/물류확장으로 별도 확인 필요.
   registry 의 `Sobo59_1` folder(`Subu59_1`)는 실제 「일별 내역서(요약)」를 가리키므로 검증 화면 착수 시 폴더 재지정 검토.

## 6. C 항목 착수 게이트 (P0 산출)

| 화면 | 정본 DFM | 착수 가능 | 비고 |
|------|----------|-----------|------|
| C1 입고명세서 | `Subu22`(입고명세서) | ✅ | 입고접수(Sobo22 /inbound/receipts)와 분리 — `Sobo22.md §7.1` |
| C2 입고현황 | (없음 — 재추출 필요) | ❌ 블록 | Publisher Sobo25 DFM 재추출 선행 |
| C3~C5 출고검증 | `Subu59_2`,`Subu59_3` | ⚠️ 부분 | (1) 정본 불명, (2)/(개별) 가용 |
| C6 제작명세서 | (없음 — 재추출 필요) | ❌ 블록 | Publisher Sobo26 DFM 재추출 선행 |
| C7 제작현황 | (없음 — 재추출 필요) | ❌ 블록 | Publisher Sobo27 DFM 재추출 선행 |
| C8 원천징수 | (없음 — 재추출 필요) | ❌ 블록 | Publisher Sobo28 DFM 재추출 선행 |
| C9 신간발행 | `Subu29`(신간명세서) | ✅ | 기타명세서와 variant 분리 |
| C10 내역조회(저자) | (없음 — 메뉴 부재) | ❌ 블록 | 표준 빌드 미존재 §4 |

> 본 게이트는 `dfm-layout-input.mdc`(정본 DFM=공식 입력) 의 직접 적용이다. 블록 항목은 정본 확보 전
> phase1 승격을 금지하고 STUB/preview 로 유지한다.
