# 레이아웃 매핑: Sobo16 (특별관리) → 모던 `/master/special`

DEC-028 — `Subu16/TSobo16`. 레거시 WRITE 는 `G6_Ggeo` (`Base01.pas` `T1_Sub61BeforePost`). G1 `Special_*` 컬럼과 무관.

## 0. 입력 산출물

- 원 dfm/pas: [`legacy_delphi_source/legacy_source/Subu16.dfm`](../../legacy_delphi_source/legacy_source/Subu16.dfm), [`Subu16.pas`](../../legacy_delphi_source/legacy_source/Subu16.pas)
- 대안 트리: [`legacy_delphi_source/도서유통-New/.../Subu16.pas`](../../legacy_delphi_source/도서유통-New/도서유통/한국도서유통/출판/Subu16.pas) (동작 동등)
- WRITE 근거: [`도서유통-New/.../Base01.pas`](../../legacy_delphi_source/도서유통-New/도서유통/한국도서유통/출판/Base01.pas) `T1_Sub61BeforePost` / `T1_Sub62BeforePost`
- 화면 카드: [`analysis/screen_cards/Sobo16.md`](../screen_cards/Sobo16.md)
- 모던 라우트: [`도서물류관리프로그램/frontend/src/app/(app)/master/special/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/master/special/page.tsx)
- 계약: [`migration/contracts/special_master.yaml`](../../migration/contracts/special_master.yaml)
- accelerator HTML: **미생성** — dfm 직접을 T1 입력으로 사용 (dfm-layout-input 룰: 후속 생성 시 본 노트 갱신)

## 1. 의미 분기

레거시 3 검색 축 → 모던 **mode** 쿼리 파라미터:

| 레거시 | 조건(요지) | mode |
| --- | --- | --- |
| `Button101Click` | G6 `Gcode`+`Hcode`, Order `Bcode` | `customer` |
| `Button201Click` | G6 `Bcode`+`Hcode`, Order `Gcode` | `book` |
| `Button301Click` | `Hcode` 전체(레거시는 `Bcode=''` 필터; 모던 API 는 동일 출판사 전체 행) | `publisher` |

모던 `publisher` 모드는 운영 편의상 **`Hcode` 만으로 G6 전체** 조회 (레거시 Button301 의 빈 도서코드 필터와 완전 일치하지 않을 수 있음 — 계약 notes).

저장 컬럼: **`Grat1`**, **`Gssum`** (레거시 BeforePost). 스키마 사전의 `grat5`(특별) 라벨과 혼동 금지.

## 2. dfm 영역 인벤토리 (요약)

- **Panel001 / Panel002**: 거래처 조회 — `Edit101`(거래처코드), `Edit102`(거래처명), `Edit107`(출판사), `Button101`
- **Panel003 / Panel004**: 도서 조회 — `Edit201`~`208`, `Button201`
- **Panel005**: 토글 패널 (`Button004Click`)
- **Panel006 / Panel301**: 출판사 단독 조회 — `Edit307`~`308`, `Button301`
- **DBGrid101 / DBGrid201 / DBGrid301**: 그리드 3종 (동일 G6 데이터셋 축)
- 코너·라벨·상태바: 장식

## 3. TabOrder (dfm 발췌 — 주요 입력)

검색 패널별 `TabOrder` 는 dfm 내 `Edit101`(2), `Edit102`(3), `Button101`(6) 등. 모던에서는 **모드별 필드 그룹**으로 재배치하되 동일 위젯 의미를 유지.

## 4. DBGrid 컬럼 ↔ API 필드

| 표시 | API / DB | 비고 |
| --- | --- | --- |
| 출판사 | `hcode` | G6.Hcode |
| 거래처코드 | `gcode` | G6.Gcode |
| 도서코드 | `bcode` | G6.Bcode |
| 도서명 | `bname` | G4_Book.Gname 조인 |
| 거래처명 | `gname` | G1_Ggeo.Gname 조인 |
| 비율1(위탁) | `grat1` | G6.Grat1 — 레거시 저장 |
| 금액/한도 | `gssum` | G6.Gssum |
| ID | `id` | G6.ID — PATCH 경로 |

## 5. 모던 컴포넌트 · `data-legacy-id`

| 모던 UI | `data-legacy-id` |
| --- | --- |
| 검색 패널 래퍼 | `Sobo16.searchPanel` |
| 모드 라디오 그룹 | `Sobo16.mode` / `Sobo16.mode.publisher` 등 |
| 조회 버튼 | `Sobo16.ButtonSearch` |
| 출판사 코드 입력 | `Sobo16.Edit107` (customer 패널 기준; 공용 시 `Sobo16.EditHcode`) |
| 거래처 코드 | `Sobo16.Edit101` |
| 도서 코드 | `Sobo16.Edit201` |
| 데이터 그리드 테이블 | `Sobo16.DBGrid101` |
| 그리드 컬럼 헤더 | `Sobo16.DBGrid101.HCODE`, `.GCODE`, `.BCODE`, `.BNAME`, `.GNAME`, `.GRAT1`, `.GSSUM` |
| 편집 패널 래퍼 | `Sobo16.editPanel` |
| 편집 Grat1 | `Sobo16.EditGrat1` |
| 편집 Gssum | `Sobo16.EditGssum` |
| 저장 PATCH | `Sobo16.ButtonSave` |

## 6. out-of-scope (1차)

- `Button001`~`003` 빈 스텁 — 미구현
- 물리 DELETE (`T1_Sub61AfterDelete`) — DEC-019 1차 미제공
- INSERT 신규 G6 행 — phase 2
- 인쇄/CSV/진행바 — 미포함

## 7. deltas

- 서버 페이징 `DataGridPager`, `useListSession` — 레거시 무한 스크롤 아님

## 8. 이벤트 → REST

| 레거시 | REST |
| --- | --- |
| `Button101/201/301Click` | `GET /api/v1/masters/special` |
| 그리드에서 행 편집 후 저장 | `PATCH /api/v1/masters/special/{id}` |

## 9. 변형

`Subu16_*` accelerator 변형 **0건** 처리. 빌드별 `Base01` SQL 차이는 `migration/contracts` `customer_variants` 에만 기록.

## 10. 회귀 가드

- 매핑 표 §5 의 `data-legacy-id` 집합과 DOM 일치 검사 (T7)

## 11. 모바일웹

m.websend.kr 「특별관리」 캡처는 후속 첨부.
