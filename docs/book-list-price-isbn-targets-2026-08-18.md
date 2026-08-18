# 도서명 목록 → 정가·ISBN 컬럼 공통 추가 — 수정 대상 화면 목록 (2026-08-18)

- **요청**: "도서명이 목록에 포함되는 리스트에 대해서 도서가격, ISBN 정보가 필드로
  포함되어 있지 않으면 모두 공통적으로 추가" — 대상 화면 조사·목록화(착수 전 단계).
- **조사 방법**: `frontend/src/{app,components}` 전수 grep — 목록/그리드에 도서명(`도서명`·`도서`·`제목`)
  컬럼을 렌더하는 파일 42개 추출 → 같은 그리드에 **정가/단가**·**ISBN** 컬럼 유무 + 해당
  API 응답 row 타입(`lib/*-api.ts`)의 필드 유무를 대조. 도서 검색 팝업/자동완성(이미 ISBN·정가
  표시)과 상세 폼(도서관리 상세)은 "목록"이 아니라 제외.
- **판정 기준**: 전표 계열의 `단가(GDANG)`는 S1_Ssub.Gdang = 전표 시점 정가(DEC-065 산식
  `금액=정가×수량×비율/100`)이므로 **도서가격 보유**로 간주. ISBN 은 **도서관리(Sobo14) 단 1곳**만
  보유 → 나머지 전부 추가 대상.

## 요약

| 구분 | 화면 수 |
|---|---|
| A. 정가·ISBN 둘 다 없음 (양쪽 추가) | 12 |
| B. 단가/정가는 있고 ISBN 만 없음 | 20 |
| 제외(둘 다 있음) | 1 (도서관리 Sobo14) |

공통 구현 방향(제안): 백엔드에 **G4_Book 메타 청크 lookup 헬퍼**(`Gdang`·`Gisbn`, `in_clause_lookup`
기반 — 기존 `_fetch_product_names`/`_fetch_outbound_book_names` 와 동일 패턴, 목록 JOIN 금지=행증식
방지, MySQL 3.23 호환)를 1개 두고 각 API 응답에 `gdang`/`gisbn` 필드를 채움 → 프론트는 컬럼 정의에
`정가`·`ISBN` 2컬럼 추가(기본 표시, `useGridPrefs` 로 계정별 숨김 가능). XLSX export 가 있는 화면은
헤더도 동기(DEC-148 선례).

## A. 정가·ISBN 모두 추가 (12)

| # | 화면 (formId) | 라우트 · 그리드 | 현재 도서명 키 | API row 타입 | 비고 |
|---|---|---|---|---|---|
| A1 | 재고현황 (Sobo44_inv) | `/inventory/status` 목록 | gname | inquiry `LedgerRow` | 재고금액은 있으나 정가·ISBN 없음 |
| A2 | 도서수불장 (Sobo33_ledger) | `/ledger/book` 목록 | gname | inquiry `LedgerRow` | 메뉴 숨김(DEC-137) — 라우트 보존 화면. 우선순위 낮음 |
| A3 | 통합 도서수불장 (Sobo33_1_ledger) | `/ledger/book-integrated` 목록 | gname | inquiry `BookSalesRow`(gdang 있음) | 메뉴 숨김. row 에 gdang 은 있으나 컬럼 미노출·ISBN 없음 |
| A4 | 거래처판매 (Sobo62) | `/reports/customer-sales` 하단 도서별 상세 | (th) 도서명 | inquiry `CustomerSalesRow` | 상세 패널 sticky(DEC-145) — 컬럼 폭 주의 |
| A5 | 도서별년말집계 (Sobo67_yearbook) | `/reports/year-end-book` 목록 | gname | inquiry `YearEndBookRow` | XLSX 헤더 동기 필요 여부 확인 |
| A6 | 도서통계(목록) (Sobo37_stats_route) | `/stats/book` 목록 | gname | inquiry `BookSalesRow`(gdang 있음) | gdang 컬럼만 노출하면 정가 해결, ISBN 은 API 추가 |
| A7 | 도서 회전율 (Sobo52_stats) | `/stats/book-turnover` 목록 | gname | stats `BookTurnoverItem` | |
| A8 | 반품재고 통합 — 재생/해체/변경 탭 (Sobo23_2/3/4) | `/returns/inventory` 후보 목록 | bname | returns `InventoryCandidateRow` | 3탭 공용 1그리드 |
| A9 | 거래현황 상세 (Sobo24) | `/transactions/status?view=detail` 전표 라인 | (th) 도서명 | inquiry `SalesStatementLine`(gdang 있음) | 라인 row 에 gdang 있음 → 컬럼만 추가, ISBN 은 API |
| A10 | 거래명세서 목록 (Sobo21_shipment_alias) | `/transactions/sales-statement` 목록 하단 라인 표 | (th) 도서명 | inquiry `SalesStatementLine`(gdang 있음) | A9 와 동일 라인 타입 — 한 번에 처리 |
| A11 | 출고검증(1)/(2)/(개별) | `/transactions/verification` 목록 | bcode(도서) | inquiry `VerificationItem`(gdang 있음) | 도서명 자체가 코드만 표시 — 도서명·정가·ISBN 세트로 보강 권장. 총판 전용(DEC-152) |
| A12 | 도서코드 (Sobo38) | `/master/book-code` 목록 | gname(제목) | master `BookCodeListItem` | 메뉴 숨김 화면 — 우선순위 낮음 |

## B. ISBN 만 추가 (20) — 단가/정가 컬럼 이미 존재

| # | 화면 (formId) | 라우트 · 그리드 | 정가/단가 현재 | API row 타입 |
|---|---|---|---|---|
| B1 | 도서별수불원장 (Sobo31) | `/inventory/ledger` — 도서 단위 화면(정가는 헤더 표시). 목록 컬럼은 거래처별 상세 | 헤더 `정가` | 상세 `DetailRow` — 도서 1종 화면이라 ISBN 은 헤더에 표기 권장 |
| B2 | 거래처원장 (Sobo32_ledger) | `/ledger/customer` 전표별 상세 | th `정가` | (page 내 타입) |
| B3 | 배본처관리 (Sobo16_baebon, 숨김) | `/master/baebon` 목록 | 없음(gssum=단가 미노출) | master `SpecialListItem` |
| B4 | 특별관리 (Sobo16_special) | `/master/special` 이중 패널 | `단가`(gssum) | master `SpecialListItem` |
| B5 | 도서별판매 (Sobo61) | `/reports/book-sales` 목록 | `정가`(gdang) | inquiry `BookSalesRow` — XLSX 헤더 동기 |
| B6 | 기간별반품내역서 (Sobo58) | `/returns/period-report` 상세 | `단가`(gdang) | returns `PeriodDetailItem` |
| B7 | 일별반품내역서 (Sobo55) | `/returns/reports` 상세 | `단가`(gdang) | returns `DailyDetailItem` |
| B8 | 기간별재고원장(상세) (Sobo34_4) | `/returns/ledger` 상세 | gssum(금액)만 — 단가 컬럼 없음 → **정가도 추가** | returns `LedgerDetailItem` |
| B9 | 반품명세서 상세 (Sobo23) | `/returns/receipts/[returnKey]` 라인 | `단가` | returns `UpdateLine` |
| B10 | 입고접수 상세 (Sobo22) | `/inbound/receipts/[receiptKey]` 라인 + `inbound-line-grid` | `단가` | inbound `ReceiptLine` |
| B11 | 일별 입고내역서 (Sobo54) | `/inbound/reports/daily` 2그리드 | `단가`(gdang) | inbound `PublisherRow`/`VendorRow` |
| B12 | 기간별 입고내역서 (Sobo57) | `/inbound/reports/period` 2그리드 | `단가`(gdang) | inbound 동일 |
| B13 | 입고명세서 (Sobo22_inbound_statement) | `/transactions/inbound-statement` 라인 | `단가` | inbound `ReceiptLine` |
| B14 | 입고현황 (Sobo25_status_list) | `/transactions/inbound-status` 목록+라인 | `단가` | inbound `ReceiptLine` |
| B15 | 출고현황 (Sobo67_status) | `/transactions/outbound-status` 라인 목록 + 상세 | `단가`(gdang) | inquiry `OutboundStatusLineItem` |
| B16 | 거래명세서 상세 (Sobo21) | `/transactions/sales-statement/[orderKey]` 라인 | `단가` | inquiry `SalesStatementLine` |
| B17 | 신규 거래명세서 (Sobo21 new) | `/transactions/sales-statement/new` 입력 그리드 | `단가`(gdang) | 입력 그리드 — 읽기전용 ISBN 컬럼(도서 확정 시 채움) |
| B18 | 제작명세서 (Sobo26_production_stmt) | `/transactions/production/statement` | `단가`(gdang) | inquiry `ProductionItem` |
| B19 | 제작현황 (Sobo27_production_status) | `/transactions/production/status` | `단가` | inquiry `ProductionItem` |
| B20 | 내역조회(저자) (Sobo_author_history) | `/transactions/author-history` | gdang 있음(컬럼 여부 확인) | inquiry `AuthorHistoryItem` |

### 공유 컴포넌트(화면 아님, 함께 수정)
- `components/transactions/sales-statement-edit-dialog.tsx` — 명세서 수정 팝업 라인 표(단가 있음/ISBN 없음)
- `components/transactions/sales-statement-search-dialog.tsx` — 거래현황(상세) 검색 다이얼로그(단가 있음/ISBN 없음)
- `components/returns/data-import-modal.tsx` — 반품 자료 가져오기 미리보기(단가 있음/ISBN 없음)
- `components/returns/return-line-grid.tsx`, `components/inbound/inbound-line-grid.tsx` — 입력 라인 그리드(단가 있음/ISBN 없음)

## 제외
- 도서관리 (Sobo14, `/master/book`) — 정가·ISBN 모두 이미 목록 컬럼(DEC-148).
- 도서 검색 팝업/자동완성(`MasterLookupField` 도서 모드) — ISBN·단가 이미 표시.
- 신규도서 등록·도서 상세 폼 — 목록이 아님.

## 결정 (2026-08-18 사용자) → DEC-169 착수

1. 도서가격 = **전표 단가(GDANG)로 충분** (마스터 정가는 단가가 없는 화면의 폴백으로만 사용).
2. **메뉴 숨김 화면 제외** — A2 도서수불장, A3 통합 도서수불장, A12 도서코드, B3 배본처관리.
3. 새 컬럼 **기본 표시**.

## (참고) 착수 전 확인했던 질문
1. "도서가격" = 전표 단가(GDANG, 전표 시점 정가)로 충분한지, 아니면 **현재 마스터 정가(G4_Book.Gdang)** 를
   별도 컬럼으로 원하는지(둘이 다를 수 있음 — 정가 변경 이력).
2. 메뉴 숨김 화면(A2·A3·A12·B3)까지 포함할지.
3. 새 컬럼 기본 표시 vs 컬럼 설정에서 선택 표시(기본 숨김) — 폭이 좁은 상세 패널(A4·B1) 고려.
