# 레이아웃 매핑: Sobo16 (특별관리) → 모던 `/master/special`

DEC-028 — `Subu16/TSobo16`. 레거시 WRITE 는 `G6_Ggeo` (`Base01.pas` `T1_Sub61BeforePost`). G1 `Special_*` 컬럼과 무관.

> **2026-08-18 갱신 (DEC-155 / DEC-170 / DEC-171)** — 본 노트의 초기본은 **총판 빌드**(`도서유통-총판/Subu16`:
> 비율 1개+단가) 기준이었다. 교문사 등 출판·자체물류 계정의 정본은 **`WeLove_FTP/도서유통-New/Subu16.pas/.dfm`**
> (판매유형별 Grat1~6 + 단가, `Base01.pas` INSERT/UPDATE Grat1~9+Gssum, 출고 적용 `Tong02.pas` `PrinRat1`).
> 두 빌드 차이는 **코드 분기 없이** `migration/contracts/special_master.yaml` `rate_profiles`(single/by_pubun) +
> `customer_variants`(build_role) 데이터로 갈리며(DEC-171), 화면은 서버가 돌려주는 `rate_profile.columns` 로 컬럼을 파생한다.
> 상세 비교: `docs/special-mgmt-legacy-vs-web-2026-08-18.md`.

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

모던 `publisher` 모드는 API 에만 남아 있고(Hcode 전체 조회) **화면에서는 DEC-155 로 제거** — 레거시 New 빌드의
Button301 은 `Bcode=''`(거래처별 기본 특별비율 행) 모드라 의미가 다르며 미이식(DEC-170 D3, 신간 배본 Seek07 폴백과 묶어 후속).

저장 컬럼: **`Grat1`~`Grat6`(프로필 by_pubun) / `Grat1`(single)** + **`Gssum`(단가)** — 레거시 New 빌드 BeforePost 는
Grat1~9+Gssum 전부를 쓴다(Grat7~9 는 웹 미사용=0). 스키마 사전의 `grat5`(특별) 라벨과 혼동 금지.

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
| 위탁 / 비율 | `grat1` | G6.Grat1 — single 프로필은 "비율" 1개 |
| 현매·매절·납품·특별·기타 | `grat2`~`grat6` | G6.Grat2~6 — by_pubun 프로필(출판·자체물류)만 표시/편집 (DEC-171) |
| 단가 | `gssum` | G6.Gssum — 신규 등록 시 도서 정가 자동 채움(레거시 Seek40 확정과 동등, DEC-170) |
| ISBN | `gisbn` | G4_Book.Gisbn 공통 메타(DEC-169, 거래처축 그리드) |
| ID | `id` | G6.ID — PATCH/DELETE 경로 |

## 5. 모던 컴포넌트 · `data-legacy-id` (DEC-155/170/171 현행)

| 모던 UI | `data-legacy-id` |
| --- | --- |
| 거래처축 패널 / 도서축 패널 (상·하 동시 표시) | `Sobo16.PaneCustomer` / `Sobo16.PaneBook` |
| 거래처 검색(자동완성 MLF) / 도서 검색 | `Sobo16.Edit101` / `Sobo16.Edit201` |
| 출판사 코드(관리자만) | `Sobo16.Edit107` |
| 거래처축 그리드 / 도서축 그리드 | `Sobo16.DBGrid101` / `Sobo16.DBGrid201` |
| 그리드 비율 컬럼 | `Sobo16.DBGrid101.GRAT1`~`.GRAT6`(프로필 컬럼만), `.GSSUM`, `.BCODE`, `.BNAME`, `.GCODE`, `.GNAME` |
| 선택 행 편집 블록(선택 해제/Esc) | `Sobo16.DBGrid101.Edit` / `Sobo16.DBGrid201.Edit` — 입력 `…GRATn.edit` |
| 신규 등록 블록(레거시 Append 동등, 거래처축 항상 표시·도서축 접힘) | `Sobo16.DBGrid101.Append` / `Sobo16.DBGrid201.Append` — 입력 `…GRATn.new` |

## 6. out-of-scope (1차)

- `Button001`~`003` 빈 스텁 — 미구현
- `Gcode`/`Bcode` 키 변경 저장 — 후속
- 인쇄/HTML 저장(Button010~017)/진행바 — 미포함(엑셀 export 공통 정책 시 후속)
- 거래처별 기본행(`Bcode=''`, Panel005 모드)·`최근공급율저장하기`(Button401, 숨김) — 미이식(DEC-170 D3/D9)

## 7. deltas

- 서버 페이징 `DataGridPager`, `useListSession` — 레거시 무한 스크롤 아님
- 레거시 상/하 두 축을 `PaneCustomer`/`PaneBook` 두 패널로 동시 표시(DEC-155, 모드 라디오 제거)
- 그리드 내 편집(Enter 셀 이동·마지막 칸 Append) 대신 선택 행 편집 블록 + 항상 표시되는 신규 등록 블록(DEC-170);
  신규 도서 확정 시 단가=정가·비율=거래처 기본 공급율(컬럼별) 자동 채움
- 코드/명칭 검색은 공통 `MasterLookupField`(인라인 자동완성 + 팝업)로 보강, 선택 즉시 조회 후 조회 버튼 포커스
- 비율 컬럼 집합은 서버 `rate_profile`(계약 special_master.yaml customer_variants) 로 계정별 파생(DEC-171)

## 8. 이벤트 → REST

| 레거시 | REST |
| --- | --- |
| `Button101/201Click` | `GET /api/v1/masters/special?mode=customer|book` (응답 `rate_profile` 동봉) |
| 그리드 Append + 코드 Enter(Seek) → BeforePost INSERT | `POST /api/v1/masters/special` (grat1~6·gssum) |
| 그리드 셀 편집 → BeforePost UPDATE | `PATCH /api/v1/masters/special/{id}` (grat1~6·gssum) |
| Delete 키 → AfterDelete | `DELETE /api/v1/masters/special/{id}` |
| 출고 적용(`Subu21` G6 + `PrinRat1`) | `GET /transactions/sales-statement/line-defaults` — 프로필 by_pubun 이면 판매유형 컬럼, 0 이면 Grat1 폴백(DEC-171) |

## 9. 변형

`Subu16_*` accelerator 변형 **0건** 처리. 빌드별 `Base01` SQL 차이는 `migration/contracts` `customer_variants` 에만 기록.

## 10. 회귀 가드

- `test/test_masters_special_g6.py`(CRUD·페이징), `test/test_dec171_special_rate_profile.py`(프로필·pubun 매핑·번들 동기·드리프트),
  `test/test_special_discount_legacy_alignment.py`(§5 legacy-id 정합 — DEC-155 이후 id 로 갱신 필요 시 본 표가 정본)

## 11. 모바일웹

m.websend.kr 「특별관리」 캡처는 후속 첨부.
