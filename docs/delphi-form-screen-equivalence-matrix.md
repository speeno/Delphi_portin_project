# 델파이 폼 ↔ 모던 화면 동등성 매트릭스

> **자동 생성** — `python3 tools/delphi_form_screen_matrix.py` 로 갱신. 직접 편집하지 마세요.
> **생성 시각 (UTC)**: 2026-08-25T03:24:47Z

## 목적

- 레거시 `Subu*.dfm` 루트 **Caption** 과 모던 `form-registry.ts` 의 **caption** 을 나란히 두어,
  포팅 시 **제목 불일치·폴더 오매칭**(예: DEC-060 사례) 재발을 방지한다.
- **동등성**: 문자열이 완전히 같으면 `MATCH`. 의도적 표기 차이는 코드 내 allowlist + 본 표 `note` 로 관리한다.

## 파이프라인에서의 위치

1. 화면 포팅/계약 수정 전: `python3 tools/delphi_form_screen_matrix.py` 실행 → 본 문서·JSON 갱신.
2. `status` 가 `CAPTION_DIFF` 인 행을 우선 검토 — DFM Caption 재확인 (`iconv -f EUC-KR -t UTF-8 Subu*.dfm`).
3. CI/로컬 체크: `python3 tools/delphi_form_screen_matrix.py --check` — 등록된 **`Subu*`** 폴더에 대응 `Subu*.dfm` 이 없으면 실패. 제목 불일치까지 게이트하려면 `--strict` (단일 매핑 `CAPTION_DIFF` 포함). `WEB_ONLY`(`_WebAdm`) 는 제외.

## 표 — form-registry 등록 화면 (폴더 = DFM 스템)

| 상태 | 모던 ID | 폴더(DFM) | 모던 caption | 레거시 Caption (DFM) | 레거시 폼 객체 | 라우트 | 비고 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MULTI_MAP | `Sobo11` | `Subu11` | 거래처관리(마스터) | 거래처관리-통합 | `Sobo11` | `/master/customer` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo11_gbun` | `Subu11` | 거래처구분 | 거래처관리-통합 | `Sobo11` | `/master/customer-category` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| CAPTION_DIFF | `Sobo12` | `Subu12` | 입고처관리(마스터) | 입고처관리 | `Sobo12` | `/master/inbound-vendor` | 포함 관계·수동검토: DFM「입고처관리」↔「입고처관리(마스터)」 (r=0.67) |
| CAPTION_DIFF | `Sobo13` | `Subu13` | 저자관리(마스터) | 지역분류(시내+지방) | `Sobo13` | `/master/author` | DFM「지역분류(시내+지방)」↔모던「저자관리(마스터)」 (r=0.20) |
| MULTI_MAP | `Sobo14` | `Subu14` | 도서관리(마스터) | 도서관리 | `Sobo14` | `/master/book` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo14_gbun` | `Subu14` | 도서분류 | 도서관리 | `Sobo14` | `/master/book-category` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| CAPTION_DIFF | `Sobo15` | `Subu15` | 기타거래처관리(마스터) | 거래처관리-개별 | `Sobo15` | `/master/etc-customer` | DFM「거래처관리-개별」↔모던「기타거래처관리(마스터)」 (r=0.50) |
| MULTI_MAP | `Sobo16_baebon` | `Subu16` | 배본처관리 | 특별관리 | `Sobo16` | `/master/baebon` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo16_special` | `Subu16` | 특별관리 | 특별관리 | `Sobo16` | `/master/special` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| OK_EXEMPT | `Sobo17` | `Subu17` | 출판사·출고거래처(마스터) | 출판사관리 | `Sobo17` | `/master/publisher` | DEC-023 표기 통일(allowlist) |
| MULTI_MAP | `Sobo21` | `Subu21` | 거래 명세서 | 거래명세서 | `Sobo21` | `/transactions/sales-statement` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo21_shipment_alias` | `Subu21` | 거래 명세서 | 거래명세서 | `Sobo21` | `/transactions/sales-statement` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo21_status_list` | `Subu21` | 거래 현황(LIST) | 거래명세서 | `Sobo21` | `/transactions/status?view=list` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo21_status_memo` | `Subu21` | 거래 현황(메모) | 거래명세서 | `Sobo21` | `/transactions/status?view=memo` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo21_status_summary` | `Subu21` | 거래 현황(요약) | 거래명세서 | `Sobo21` | `/transactions/status?view=summary` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo22` | `Subu22` | 입고 접수 | 입고명세서 | `Sobo22` | `/inbound/receipts` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo22_inbound_statement` | `Subu22` | 입고명세서 | 입고명세서 | `Sobo22` | `/transactions/inbound-statement` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo23` | `Subu23` | 반품 접수 | 반품명세서 | `Sobo23` | `/returns/receipts` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo23_scrap` | `Subu23` | 폐기 접수 | 반품명세서 | `Sobo23` | `/returns/scrap/new` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo23_scrap_status` | `Subu23` | 폐기 현황 | 반품명세서 | `Sobo23` | `/returns/scrap/status` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo23_status` | `Subu23` | 반품 현황 | 반품명세서 | `Sobo23` | `/returns/status` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo21_status_detail` | `Subu24` | 거래 현황(상세) | 반품재고(정품입고)-재생 | `Sobo24` | `/transactions/status?view=detail` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo24` | `Subu24` | 반품재고(재생) | 반품재고(정품입고)-재생 | `Sobo24` | `/returns/inventory?tab=regen` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo25` | `Subu25` | 반품재고(해체) | 반품재고(반품입고)-해체 | `Sobo25` | `/returns/inventory?tab=disassemble` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo25_status_detail` | `Subu25` | 입고 현황(상세) | 반품재고(반품입고)-해체 | `Sobo25` | `/transactions/inbound-status?view=detail` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo25_status_list` | `Subu25` | 입고 현황 | 반품재고(반품입고)-해체 | `Sobo25` | `/transactions/inbound-status` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo25_status_summary` | `Subu25` | 입고 현황(요약) | 반품재고(반품입고)-해체 | `Sobo25` | `/transactions/inbound-status?view=summary` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| CAPTION_DIFF | `Sobo26_production_stmt` | `Subu26` | 제작명세서 | 출고접수현황 | `Sobo26` | `/transactions/production/statement` | DFM「출고접수현황」↔모던「제작명세서」 (r=0.00) |
| CAPTION_DIFF | `Sobo_author_history` | `Subu26_1` | 내역조회(저자) | 내역조회(저자)-거래현황 | `Sobo26_1` | `/transactions/author-history` | 포함 관계·수동검토: DFM「내역조회(저자)-거래현황」↔「내역조회(저자)」 (r=0.76) |
| MULTI_MAP | `Sobo27` | `Subu27` | 출고 접수 | 출고접수관리 | `Sobo27` | `/outbound/orders` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo27_production_status` | `Subu27` | 제작현황 | 출고접수관리 | `Sobo27` | `/transactions/production/status` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo28_delivery` | `Subu28` | 택배관리 | 출고택배관리 | `Sobo28` | `/shipping/courier` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo28_withholding` | `Subu28` | 원천징수 | 출고택배관리 | `Sobo28` | `/transactions/withholding` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo29_new_release` | `Subu29` | 신간발행 | 신간명세서 | `Sobo29` | `/transactions/new-release` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo29_new_release_shipment_alias` | `Subu29` | 신간발행 | 신간명세서 | `Sobo29` | `/transactions/new-release` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo29_other` | `Subu29` | 기타명세서 | 신간명세서 | `Sobo29` | `/transactions/other` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MATCH | `Sobo31` | `Subu31` | 도서별수불원장 | 도서별수불원장 | `Sobo31` | `/inventory/ledger` |  |
| CAPTION_DIFF | `Sobo32_ledger` | `Subu32` | 거래처원장 | 기간별평균재고 | `Sobo32` | `/ledger/customer` | DFM「기간별평균재고」↔모던「거래처원장」 (r=0.00) |
| CAPTION_DIFF | `Sobo32_1_ledger` | `Subu32_1` | 통합 거래처원장 | 출판사별 재고 현황 | `Sobo32_1` | `/ledger/customer-integrated` | DFM「출판사별 재고 현황」↔모던「통합 거래처원장」 (r=0.00) |
| MULTI_MAP | `Sobo33_1_ledger` | `Subu33` | 통합 도서수불장 | 기간별재고원장 | `Sobo33` | `/ledger/book-integrated` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo33_ledger` | `Subu33` | 도서수불장 | 기간별재고원장 | `Sobo33` | `/ledger/book` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| OK_EXEMPT | `Sobo34_1_value` | `Subu34_1` | 재고금액 | 재고 및 재고금액 | `Sobo34_1` | `/inventory/value` | DEC-023 표기 통일(allowlist) |
| NEAR_MATCH | `Sobo34_4` | `Subu34_4` | 기간별재고원장(상세) | 기간별재고원장(상세)-폐기 | `Sobo34_4` | `/returns/ledger` | 유사도 0.88 (≥0.78) |
| CAPTION_DIFF | `Sobo36_stats_route` | `Subu36` | 거래처통계(목록) | 도서별원장총괄 | `Sobo36` | `/stats/customer` | DFM「도서별원장총괄」↔모던「거래처통계(목록)」 (r=0.00) |
| CAPTION_DIFF | `Sobo37_stats_route` | `Subu37` | 도서통계(목록) | 담당자판매원장 | `Sobo37` | `/stats/book` | DFM「담당자판매원장」↔모던「도서통계(목록)」 (r=0.00) |
| MULTI_MAP | `Sobo22_import` | `Subu38` | 입고 파일 업로드 | Sobo38 | `Sobo38` | `/inbound/import` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo38` | `Subu38` | 도서코드(마스터) | Sobo38 | `Sobo38` | `/master/book-code` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo39` | `Subu39` | 할인율(대표) | 출고내역서 | `Sobo39` | `/master/discount` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo39` | `Subu39` | 출고내역서 | 출고내역서 | `Sobo39` | `/outbound/statement` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo41_cash` | `Subu41` | 입금내역 | 입금내역 | `Sobo41` | `/settlement/cash` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo41_cash_bill` | `Subu41` | 입금내역 | 입금내역 | `Sobo41` | `/settlement/cash` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo41_slip` | `Subu41` | 입금전표 | 입금내역 | `Sobo41` | `/settlement/payment-slip` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo42_cash` | `Subu41` | 입출금전표 거래처 | 입금내역 | `Sobo41` | `/settlement/cash-status` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Settle_outstanding` | `Subu42` | 미수현황 | 입금현황(1) | `Sobo42` | `/settlement/outstanding` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo42_cash_bill` | `Subu42` | 입금현황(거래처별) | 입금현황(1) | `Sobo42` | `/settlement/cash-status?variant=hcode` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| CAPTION_DIFF | `Sobo42_1_cash_bill` | `Subu42_1` | 입금현황(일자별) | 입금현황(2) | `Sobo42_1` | `/settlement/cash-status?variant=sdate` | DFM「입금현황(2)」↔모던「입금현황(일자별)」 (r=0.75) |
| MULTI_MAP | `Sobo43_shipping_ledger` | `Subu43` | 발송비내역 | 발송비내역 | `Sobo43` | `/settlement/shipping-ledger` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo43_stats_route` | `Subu43` | 출판사통계 | 발송비내역 | `Sobo43` | `/stats/publisher` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo44_inv` | `Subu44` | 재고현황 | 발송비현황 | `Sobo44` | `/inventory/status` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo44_shipping_status` | `Subu44` | 발송비현황 | 발송비현황 | `Sobo44` | `/settlement/shipping-status` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo45_billing` | `Subu45` | 청구서관리 | 청구서관리 | `Sobo45` | `/settlement/billing` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo45_billing_bill` | `Subu45` | 청구서관리 | 청구서관리 | `Sobo45` | `/settlement/billing` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MATCH | `Sobo45_1_billing_bill` | `Subu45_1` | 청구서관리-택배 | 청구서관리-택배 | `Sobo45_1` | `/settlement/billing?variant=takbae` |  |
| MULTI_MAP | `Sobo46_billing` | `Subu46` | 청구서 인쇄(미리보기) | 청구서출력 | `Sobo46` | `/settlement/billing?view=print` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo46_billing_bill` | `Subu46` | 청구서출력 | 청구서출력 | `Sobo46` | `/settlement/billing?view=print` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo47_billing` | `Subu47` | 청구금액(년월) | 청구금액(년월) | `Sobo47` | `/settlement/period` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo47_billing_bill` | `Subu47` | 청구금액(년월) | 청구금액(년월) | `Sobo47` | `/settlement/period` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo48_compare` | `Subu48` | 출판사관리(설정) | 출판사관리(설정) | `Sobo48` | `/ledger/comparison` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Stats_monthly` | `Subu48` | 월별통계 | 출판사관리(설정) | `Sobo48` | `/stats/monthly` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo49_tax` | `Subu49` | 세금계산서 발행 | 세금계산서발행 | `Sobo49` | `/settlement/tax-invoice` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo49_tax_bill` | `Subu49` | 세금계산서 | 세금계산서발행 | `Sobo49` | `/settlement/tax-invoice` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| DFM_PLACEHOLDER | `Sobo50_stats` | `Subu50` | 기간별 매출 분석 | Sobo50 | `Sobo50` | `/stats/sales-period` | 루트 Caption 이 식별자 수준「Sobo50」— 실제 화면은 변형 폴더·주 폼 참조 |
| MULTI_MAP | `Sobo51` | `Subu51` | 반품재고(변경) | 반품재고(변경) | `Sobo51` | `/returns/inventory?tab=change` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo51_stats` | `Subu51` | 거래처별 판매 분석 | 반품재고(변경) | `Sobo51` | `/stats/customer-analysis` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| CAPTION_DIFF | `Sobo52_stats` | `Subu52` | 도서 회전율 | 정품재고(변경) | `Sobo52` | `/stats/book-turnover` | DFM「정품재고(변경)」↔모던「도서 회전율」 (r=0.00) |
| CAPTION_DIFF | `Sobo53_stats` | `Subu53` | 분기/반기 손익 | 일별 출고내역서 | `Sobo53` | `/stats/quarterly-summary` | DFM「일별 출고내역서」↔모던「분기/반기 손익」 (r=0.00) |
| MATCH | `Sobo54` | `Subu54` | 일별 입고내역서 | 일별 입고내역서 | `Sobo54` | `/inbound/reports/daily` |  |
| MATCH | `Sobo55` | `Subu55` | 일별반품내역서 | 일별 반품내역서 | `Sobo55` | `/returns/reports` |  |
| MATCH | `Sobo57` | `Subu57` | 기간별 입고내역서 | 기간별입고내역서 | `Sobo57` | `/inbound/reports/period` |  |
| MATCH | `Sobo58` | `Subu58` | 기간별반품내역서 | 기간별반품내역서 | `Sobo58` | `/returns/period-report` |  |
| MULTI_MAP | `Sobo59_1` | `Subu59_1` | 출고검증(1) | 일별 내역서(요약) | `Sobo59_1` | `/transactions/verification?v=1` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo59_verification_shipment_alias` | `Subu59_1` | 출고검증 | 일별 내역서(요약) | `Sobo59_1` | `/transactions/verification?v=1` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| CAPTION_DIFF | `Sobo59_2` | `Subu59_2` | 출고검증(2) | 출고 검증관리 | `Sobo59_2` | `/transactions/verification?v=2` | DFM「출고 검증관리」↔모던「출고검증(2)」 (r=0.62) |
| NEAR_MATCH | `Sobo59_3` | `Subu59_3` | 출고검증(개별) | 출고 검증관리(개별) | `Sobo59_3` | `/transactions/verification?v=individual` | 유사도 0.89 (≥0.78) |
| MATCH | `Sobo61` | `Subu61` | 도서별판매 | 도서별판매 | `Sobo61` | `/reports/book-sales` |  |
| OK_EXEMPT | `Sobo62` | `Subu62` | 거래처별판매 | 거래처판매 | `Sobo62` | `/reports/customer-sales` | DEC-023 표기 통일(allowlist) |
| MULTI_MAP | `Sobo67_status` | `Subu67` | 출고 현황 | 도서별년말집계 | `Sobo67` | `/transactions/outbound-status` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| MULTI_MAP | `Sobo67_yearbook` | `Subu67` | 도서별년말집계 | 도서별년말집계 | `Sobo67` | `/reports/year-end-book` | 동일 레거시 폴더에 복수 모던 라우트 — 루트 Caption 은 주 폼 기준 (파생 화면은 §DEC-019) |
| WEB_ONLY | `MenuBillingStatements` | `_Matrix` | 내역서관리 | — | `—` | `/billing/statements` | Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1) |
| WEB_ONLY | `MenuShippingReturnsInventory` | `_Matrix` | 반품재고관리(통합) | — | `—` | `/shipping/returns-inventory` | Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1) |
| WEB_ONLY | `MenuYearMonthStats` | `_Matrix` | 년/월(통계) | — | `—` | `/year-month-stats` | Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1) |
| WEB_ONLY | `Subu10_id_logn` | `_WebAdm` | 사용자·권한 (F11~F89) | — | `—` | `/admin/id-logn` | Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1) |
| WEB_ONLY | `WebAdmAudit` | `_WebAdm` | 감사 통합 뷰 | — | `—` | `/admin/audit` | Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1) |
| WEB_ONLY | `WebAdmAuditRotate` | `_WebAdm` | 감사 비밀번호 회전 | — | `—` | `/admin/audit-rotate` | Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1) |
| WEB_ONLY | `WebAdmEnv` | `_WebAdm` | 환경설정(개정) | — | `—` | `/admin/settings` | Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1) |
| WEB_ONLY | `WebAdmHome` | `_WebAdm` | 관리자 콘솔(서버/DB·계정·권한) | — | `—` | `/admin` | Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1) |
| WEB_ONLY | `WebAdmOps` | `_WebAdm` | 운영 모니터링 | — | `—` | `/admin/ops` | Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1) |
| WEB_ONLY | `WebAdmRBAC` | `_WebAdm` | 역할/권한 | — | `—` | `/admin/rbac` | Wave D 웹 전용 — 레거시 DFM 대응 없음 (OOS-MAS-1) |

## 참고 — 레지스트리 미등록 DFM (주 트리만)

아래는 `legacy_source` 에 존재하나 현재 `FORM_REGISTRY` 에 `folder` 가 없는 스템입니다.
신규 포팅 후보이거나 통계/분기 전용일 수 있습니다.

| DFM 스템 | 레거시 Caption | 경로 |
| --- | --- | --- |
| `Subu10` | 로그인 | `legacy_delphi_source/legacy_source/Subu10.dfm` |
| `Subu13_1` | 출고증정렬 | `legacy_delphi_source/legacy_source/Subu13_1.dfm` |
| `Subu14_1` | 도서관리(위치) | `legacy_delphi_source/legacy_source/Subu14_1.dfm` |
| `Subu17_1` | 출판사관리-택배 | `legacy_delphi_source/legacy_source/Subu17_1.dfm` |
| `Subu18` | 종당관리 | `legacy_delphi_source/legacy_source/Subu18.dfm` |
| `Subu19` | Sobo19 | `legacy_delphi_source/legacy_source/Subu19.dfm` |
| `Subu19_1` | Sobo19_1 | `legacy_delphi_source/legacy_source/Subu19_1.dfm` |
| `Subu1A` | 환경설정 | `legacy_delphi_source/legacy_source/Subu1A.dfm` |
| `Subu20` | 거래내역변경 | `legacy_delphi_source/legacy_source/Subu20.dfm` |
| `Subu22_1` | 가입고 요청서 | `legacy_delphi_source/legacy_source/Subu22_1.dfm` |
| `Subu22_2` | 가입고 현황 | `legacy_delphi_source/legacy_source/Subu22_2.dfm` |
| `Subu27_1` | 출고접수관리 | `legacy_delphi_source/legacy_source/Subu27_1.dfm` |
| `Subu30` | Sobo30 | `legacy_delphi_source/legacy_source/Subu30.dfm` |
| `Subu32_9` | 도서별수불원장 | `legacy_delphi_source/legacy_source/Subu32_9.dfm` |
| `Subu34` | 기간별재고원장 | `legacy_delphi_source/legacy_source/Subu34.dfm` |
| `Subu34_2` | 기간별재고원장(상세)-정품 | `legacy_delphi_source/legacy_source/Subu34_2.dfm` |
| `Subu34_3` | 기간별재고원장(상세)-비품 | `legacy_delphi_source/legacy_source/Subu34_3.dfm` |
| `Subu35` | 거래처원장총괄 | `legacy_delphi_source/legacy_source/Subu35.dfm` |
| `Subu38_1` | 운임관리-택배 | `legacy_delphi_source/legacy_source/Subu38_1.dfm` |
| `Subu38_2` | 운송비-입력(1) | `legacy_delphi_source/legacy_source/Subu38_2.dfm` |
| `Subu40` | 패스워드: | `legacy_delphi_source/legacy_source/Subu40.dfm` |
| `Subu43_1` | 반품비내역 | `legacy_delphi_source/legacy_source/Subu43_1.dfm` |
| `Subu44_1` | 반품비현황 | `legacy_delphi_source/legacy_source/Subu44_1.dfm` |
| `Subu56` | 기간별출고내역서 | `legacy_delphi_source/legacy_source/Subu56.dfm` |
| `Subu59` | 기간별택배내역서 | `legacy_delphi_source/legacy_source/Subu59.dfm` |
| `Subu59_9` | 자료삭제 | `legacy_delphi_source/legacy_source/Subu59_9.dfm` |
| `Subu60` | Sobo60 | `legacy_delphi_source/legacy_source/Subu60.dfm` |
| `Subu63` | 도서별집계 | `legacy_delphi_source/legacy_source/Subu63.dfm` |
| `Subu64` | 거래처집계 | `legacy_delphi_source/legacy_source/Subu64.dfm` |
| `Subu65` | 도서별출고현황 | `legacy_delphi_source/legacy_source/Subu65.dfm` |
| `Subu66` | 거래처출고현황 | `legacy_delphi_source/legacy_source/Subu66.dfm` |
| `Subu68` | 거래처년말집계 | `legacy_delphi_source/legacy_source/Subu68.dfm` |
| `Subu69` | Sobo69 | `legacy_delphi_source/legacy_source/Subu69.dfm` |
| `Subu71` |  | `legacy_delphi_source/legacy_source/Subu71.dfm` |
| `Subu91` | 기타명세서 | `legacy_delphi_source/legacy_source/Subu91.dfm` |
| `Subu93` | 일별 출고내역서-(택배) | `legacy_delphi_source/legacy_source/Subu93.dfm` |
| `Subu96` | 출고접수현황-(택배) | `legacy_delphi_source/legacy_source/Subu96.dfm` |
| `Subu97` | 출고접수관리-(택배) | `legacy_delphi_source/legacy_source/Subu97.dfm` |
| `Subu98` | 출고택배관리-(택배) | `legacy_delphi_source/legacy_source/Subu98.dfm` |
| `Subu99` | 출고내역서-(택배) | `legacy_delphi_source/legacy_source/Subu99.dfm` |

## 관련 결정·규칙

- **DEC-060**: DFM Caption 대조 게이트 — 테이블 컬럼만으로 폼 의미 추정 금지.
- **DEC-023**: 마스터 단일 원천 — 모던 caption 의 `(마스터)` 등 접미는 레거시와 다를 수 있음 (allowlist).

- 소스: `도서물류관리프로그램/frontend/src/lib/form-registry.ts`
- DFM 루트: `legacy_delphi_source/legacy_source/Subu*.dfm`
