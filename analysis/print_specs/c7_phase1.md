# C7 Phase 1 — 인쇄 양식 5종 + 라벨 1종 사양표

DEC-004 (하이브리드 — 브라우저 인쇄 + 서버 PDF) / DEC-028 (dfm 산출물 영구 입력) / DEC-037 (PDF 엔진 = WeasyPrint 단일) / DEC-038 (라벨 1종 한정) / DEC-039 (.frf 참조용) 의 운영 단일 사양표.

> **본 노트는 5종 양식 + 1 라벨의 용지·여백·폰트·표 컬럼·합계 라인을 한 곳에 정의한다.** 양식별 매핑 노트(`Sobo46_billing.md` 등)는 위젯 ID·이벤트·SQL 매핑 책임. 본 노트는 **출력 조판** 단일 진실원.

## 0. 공통 사양

| 항목 | 값 | 근거 |
| --- | --- | --- |
| PDF 엔진 | WeasyPrint (Python) | DEC-037 |
| 폰트 본문 | `NanumGothic` | 서버 번들 — `backend/static/fonts/NanumGothic.ttf` (라이선스 SIL OFL) |
| 폰트 제목 | `NanumGothicBold` | 동일 번들 |
| 본문 색상 | `#222` | 흑백 인쇄 호환 |
| 표 테두리 | `1px solid #888` | 회색 (모니터·인쇄 양립) |
| 라벨 본문 | 12pt / 라인 간격 6mm | Seep13_label.md §4 |
| 페이지 번호 | `<span class='pageno'>` (CSS `@page :left` 적용 — Phase 2) | Phase 1 = 단일 페이지 가정 |
| 시스템 패키지 | libpango1.0-0 / libcairo2 / libgdk-pixbuf-2.0-0 / libffi8 | Dockerfile 메모 |

## 1. 양식별 사양 (P1-A ~ P1-F)

| # | 양식 | 용지 (`@page size`) | 여백 | 헤더 | 본문 표 컬럼 | 합계 라인 |
| --- | --- | --- | --- | --- | --- | --- |
| **P1-A** | 청구서 (Sobo46) | A4 세로 (`210mm 297mm`) | `12mm` | 거래처명 + 청구월 + 마감 배지 | 일자/시내/지방/박스/보호/반품총/반품시내/반품지방/지역/화물명/서점명/코드/건수/발송비/상태 (총 15컬럼) | 당월금액/세액/합계금액/입금액 (4종, `<tfoot>` SUM) |
| **P1-B** | 세금계산서 (Sobo49) | A4 가로 (`297mm 210mm`) | `15mm` | 거래처명 + 발행일자 + 발행/미발행 배지 | 공급가액/세액/합계금액 (3종) — 단건 카드 형식 (표 미사용) | (없음 — 단건) |
| **P1-C** | 출고 거래명세서 (Sobo27) | A4 세로 (`210mm 297mm`) | `12mm` | 거래처명 + 출고일자 + 전표번호 | 도서코드/도서명/구분/수량/단가/금액 (총 6컬럼) | 수량합/금액합 (2종, `<tfoot>` SUM) |
| **P1-D** | 반품 영수증 (Sobo23) | A4 세로 (`210mm 297mm`) | `12mm` | 거래처명 + 반품일자 + 전표번호 | 도서코드/도서명/구분/수량/단가/할인/금액/비고/상태 (총 9컬럼) | 수량합/금액합 (2종) |
| **P1-E** | 거래명세서 (Sobo21) | A4 세로 (`210mm 297mm`) | `12mm` | 거래처명 + 출고일자 + 전표번호 + 지사 | 도서코드/도서명/구분/수량/금액/비고 (총 6컬럼) | 수량합/금액합 (2종) |
| **P1-F** | 라벨 (Seep13) | 우편엽서 (`100mm 148mm`) | `8mm` | (없음 — 본문이 곧 헤더) | 수신자명 / 직책+이름 / 주소 (3라인) | (없음 — 1매 1수신자) |

> Phase 1 모든 양식은 **단일 페이지 가정**. 라인이 페이지를 초과하면 WeasyPrint 가 자동 페이지네이션. 페이지 번호는 Phase 2.

## 2. 5종 양식 공통 HTML 골격

```html
<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <title>{{ form_name }} — {{ key }}</title>
  <style>
    @page { size: 210mm 297mm; margin: 12mm; }
    body { font-family: 'NanumGothic'; font-size: 11pt; color: #222; }
    header { display: flex; justify-content: space-between; border-bottom: 2px solid #333; padding-bottom: 6mm; }
    h1 { font-family: 'NanumGothicBold'; font-size: 16pt; margin: 0; }
    table { border-collapse: collapse; width: 100%; margin-top: 4mm; }
    th, td { border: 1px solid #888; padding: 1.5mm 2mm; }
    thead th { background: #eee; }
    tfoot td { font-family: 'NanumGothicBold'; background: #f3f3f3; }
    .badge { display: inline-block; padding: 0.5mm 2mm; border-radius: 1mm; font-size: 9pt; }
    .badge.closed { background: #fdecc8; color: #7a4d00; }
  </style>
</head>
<body>
  <header>...</header>
  <table>...</table>
</body>
</html>
```

> 본 골격은 `print_service.render_pdf` 의 입력 HTML 이 따라야 할 **계약**. 양식별 빌더는 본 골격을 채우는 책임.

## 3. 라벨 (P1-F) 1매 사양

```html
<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><style>
  @page { size: 100mm 148mm; margin: 8mm; }
  body { font-family: 'NanumGothic'; font-size: 12pt; }
  .name { font-family: 'NanumGothicBold'; font-size: 14pt; margin-bottom: 4mm; }
  .branch { font-size: 11pt; color: #444; margin-bottom: 4mm; }
  .address { font-size: 12pt; line-height: 1.4; }
  .postal { letter-spacing: 0.4em; font-family: monospace; margin-top: 4mm; font-size: 13pt; }
</style></head>
<body>
  <div class="name" data-legacy-id="Seep13.Label.Gname">{{ name }}</div>
  <div class="branch" data-legacy-id="Seep13.Label.Gjice">{{ branch }} {{ posa }}</div>
  <div class="address" data-legacy-id="Seep13.Label.Gadds">{{ address }}</div>
  <div class="postal" data-legacy-id="Seep13.Label.Gpost">{{ postal_formatted }}</div>
</body>
</html>
```

## 4. 마감 워터마크 (Sobo46/Sobo49 한정)

`T2_Ssub.Yesno='1'` 인 자료의 PDF 는 본문 위에 **반투명 회색 "마감"** 워터마크.

```html
<style>
.watermark { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%) rotate(-30deg);
             font-family: 'NanumGothicBold'; font-size: 80pt; color: rgba(0,0,0,0.10); pointer-events: none; }
</style>
<div class="watermark">마감</div>
```

DEC-031 가시화 — 데이터는 읽기 전용이므로 PDF 응답 자체는 200, 다만 **시각적으로 "이 자료는 마감되어 수정 불가"** 임을 인쇄물에서도 인지하도록.

## 5. 폰트 번들 정책

- 서버 번들: `backend/static/fonts/NanumGothic.ttf`, `NanumGothicBold.ttf` (SIL OFL, 무료 재배포 OK)
- WeasyPrint 는 시스템 폰트도 사용하나, 컨테이너/클라우드 환경 일관성을 위해 **번들 우선**.
- @font-face 는 매 빌더가 인라인 정의 (외부 URL 의존 0):

```css
@font-face { font-family: 'NanumGothic'; src: url('file:///app/backend/static/fonts/NanumGothic.ttf'); }
@font-face { font-family: 'NanumGothicBold'; src: url('file:///app/backend/static/fonts/NanumGothicBold.ttf'); }
```

> 폰트 파일 누락 시 graceful fallback (시스템 sans-serif). 단 한국어 글리프가 있는 폰트가 없으면 □ (tofu) → DoD 회귀에 폰트 임베드 byte 검사 1건 포함.

## 6. PDF 응답 표준

| 항목 | 값 |
| --- | --- |
| Content-Type | `application/pdf` |
| Content-Disposition | `inline; filename="{form}_{key}.pdf"` (브라우저 미리보기 우선, 다운로드는 `<a download>` 가 강제) |
| Cache-Control | `private, no-store` (자료 변동 가능) |
| 인증 | DEC-004 — 호출 화면의 권한 위임. 별도 audit 토큰 미요구 (Phase 2 마감 자료 워터마크는 시각만, 차단은 별도 정책) |

## 7. 빌더 ↔ 데이터 출처 (수직 매핑)

| 양식 | 빌더 함수 | 데이터 함수 | SQL ID |
| --- | --- | --- | --- |
| P1-A | `settlement_print_service.render_invoice_pdf_html` (T5c — `render_preview_html` 재사용) | `get_print_data` | SQL-ST-13~17 (기존) |
| P1-B | `tax_invoice_service.render_tax_invoice_pdf_html` (T5c — `render_tax_invoice_html` 재사용) | (인라인) | SQL-ST-18~22 (기존) |
| P1-C | `outbound_service.render_outbound_statement_html` (T5c 신설) | `get_order_detail` | SQL-OUT-6 (기존) |
| P1-D | `returns_service.render_return_receipt_html` (T5c 신설) | `get_return_detail` (기존) | SQL-RT-3~5 (기존) |
| P1-E | `transactions_service.render_sales_statement_html` (T5c 신설) | `get_sales_statement_detail` (기존) | SQL-INQ-2~3 (기존) |
| P1-F | `label_service.render_label_html` (T5b 신설) | `label_service.fetch_label_rows` (T5b 신설) | SQL-PR-6 (T2 신설) |

> **모든 빌더는 신규 SQL 생성 금지**. 기존 list/detail 헬퍼를 재사용하고 출력 변환만 담당 (SRP).

## 8. 회귀 게이트 (T7)

- 양식 5종 × `pytest -k pdf_signature` (10케이스 — `%PDF-` 시그니처 + Content-Type)
- 5종 × `pytest -k pdf_text` (5케이스 — pypdf 로 헤더 텍스트 추출 → 거래처명/일자 등가)
- 5종 × `pytest -k pdf_empty` (5케이스 — 빈 데이터 양식이라도 200 + placeholder)
- 마감 워터마크 (P1-A/B 한정) 2케이스
- WeasyPrint 미설치 fallback 1케이스
- DEC-028 grep — `data-legacy-id` ↔ 빌더 입력 키 1:1 정적 검사 1건

## 9. 참조

- DEC-004: 하이브리드 인쇄
- DEC-028: dfm→html 산출물 영구 입력
- **DEC-037** (T8 신설): PDF 엔진 = WeasyPrint 단일
- **DEC-038** (T8 신설): Phase 1 라벨 양식 1종 한정
- **DEC-039** (T8 신설): `.frf` 참조용 카탈로그 정책
- 양식별 매핑: `Sobo46_billing.md`, `Sobo49_tax.md`, `Sobo27.md`, `Sobo23.md`, `Sobo21.md`, `Seep13_label.md`
- contract: `print_invoice.yaml` v1.0.0, `print_label.yaml` v1.0.0, `settlement_billing.yaml` v1.2.0
- `.frf` 인벤토리: `frf_catalog.md`
