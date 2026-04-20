# 레이아웃 매핑: Seep13 (라벨/택배 라벨 인쇄) → 모던 `/print/label/[shipment]` [C7 Phase 1]

DEC-028 의무 — 레거시 위젯 ID 와 모던 컴포넌트 1:1 매핑. 픽셀 좌표·폰트·색상은 가져오지 않으나, **라벨은 물리 인쇄 매체 의존도가 높음** → 용지 사양(A4/80Col/Custom)·여백·라인 간격은 mm 단위 CSS `@page` 로 흡수.

> **사용자 결정 (C7 Phase 1)**: 양식 5종 + 라벨 1종 (DEC-038). 라벨은 Seep13 의 `Tong60.frReport00_01` (Report_1_21~25.frf) 로딩 흐름 중 **단일 양식 (ItemIndex=0 = Report_1_21.frf)** 만 1차 채택. 나머지 4 종 (`Report_1_22~25.frf`) 은 `customer_variants` 로 표시만 — Phase 2 에서 동적 분기.

## 0. 입력 산출물

- 원 dfm: [`legacy_delphi_source/legacy_source/Seep13.dfm`](../../legacy_delphi_source/legacy_source/Seep13.dfm)
- 원 pas: [`legacy_delphi_source/legacy_source/Seep13.pas`](../../legacy_delphi_source/legacy_source/Seep13.pas)
  - `FormShow` (L131 — `ComboBox00Change(Self)` 호출)
  - `ComboBox00Change` (L142 — 5종 Page Columns 분기 + `STPrint00` 전역 상태)
  - `SetTing` (L190 — `Gg_Magn` 테이블에서 좌표/폰트/Style 로드 → SpinEdit*/Edit* 채움)
  - `Button1Click` (L335 — `UPDATE Gg_Magn SET F11..F77, L11..L79` 5번 묶음 — 라벨 디자인 저장)
  - `Button2Click` (L580 — `Tong60.frReport00_01.LoadFromFile('Report\Report_1_21.frf')` + `PrepareReport` + `PrintPreparedReport`)
  - `Button3Click` (L626 — 동일 로드 + `ShowReport` 미리보기)
  - `Button4Click` (L669 — `PrinterSetupDialog1.Execute`)
  - `frDBDataSet00_01Next` (L1232 — RadioButton2/3 필터 + 페이지 범위 + `Memo04` 텍스트 동적 갱신)
  - `PrinTing01/PrinDing01/02/03` (L679~ — Printer.Canvas TextOut 직접 그리기 — 본문 전체 주석처리(`{ ... }`) — **이미 Seep13 가 .frf 채택으로 폐기한 코드**)
- 모던 라우트(예정 — T6b 신설): [`도서물류관리프로그램/frontend/src/app/(app)/print/label/[shipment]/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/print/label/[shipment]/page.tsx)
- 백엔드 데이터: 신설 `GET /api/v1/print/label/{shipment_key}.pdf` (T5b — `label_service.render_label_pdf`)
- 계약: [`migration/contracts/print_label.yaml`](../../migration/contracts/print_label.yaml) v1.0.0 (T3)

## 1. 의미적 분기 — dfm 1:1 복제가 아닌 이유

레거시 `Seep13` 은 **라벨 디자인 GUI(설정 패널)** 와 **인쇄 트리거** 가 한 폼에 공존:

- 디자인 패널 (`SpinEdit*`, `Edit*`, `ComboBox*`, `RadioButton*`) — 5종 양식별 좌표/폰트/Style/용지 사양을 `Gg_Magn` 테이블에 저장 (운영자만 사용, 평소 잠금)
- 인쇄 액션 (`Button2/3/4`) — `Tong60.frReport00_01` 의 `LoadFromFile + PrepareReport + PrintPreparedReport` (FastReport 4 .frf 정본)

모던 C7 Phase 1 은:

- **디자인 패널 = out-of-scope** (DEC-039: `.frf` 자체가 정본, 디자인 변경은 Delphi IDE / FastReport Designer 에서 수동)
- **인쇄 액션 = WeasyPrint HTML/CSS PDF 1매** (단일 양식 `STPrint00='1'` ≡ `Report_1_21.frf` 등가 — 우편엽서/일반 라벨)
- **`frDBDataSet00_01Next` 의 동적 필터 (RadioButton2/3 + SpinEdit1/2 페이지 범위) → 백엔드 query string** (`include_oversea=true` / `from=N&to=M`) 로 흡수

**핵심 결정** — DEC-038 (T8): 라벨 1종 한정. 프린터 직결 (Printer.BeginDoc / `PrinterSetupDialog1`) 은 OQ-002 잔존.

## 2. dfm 영역 인벤토리

| 영역 | dfm 컨테이너 | 자식 위젯 (개수·핵심) | 모던 매핑 |
| --- | --- | --- | --- |
| 라벨 양식 선택 | `FlatPanel1.ComboBox00` | 6 항목 (1=일반/2=우편엽서/3=대형/4=2단 분할/5=2단 大) | URL 쿼리 `?form=1..5` (Phase 1 = `1` 고정) |
| 페이지 범위 | `SpinEdit1`, `SpinEdit2` | 시작/끝 RecNo | `?from=N&to=M` |
| 필터 | `RadioButton1/2/3` | 1=전체 / 2=Scode/Gbigo<>'O' / 3=='O' 만 | `?include_oversea=bool` (RadioButton1=both, 2=only_domestic, 3=only_oversea) |
| 디자인 — 라인 1~5 좌표 | `SpinEdit21~31` | Top/L11/L19 등 좌표 | **out-of-scope** (DEC-039: .frf 정본) |
| 디자인 — 폰트 5종 | `Edit21~25`, `SpeedButton1~5` (`FontDialog1`) | Edit{N}.Font.Name/Size/Style | **out-of-scope** |
| 용지 사양 | `ComboBox1` (A4/80Col/Custom), `SpinEdit61~64` | 페이지 폭/높이/마진/줄간 | **CSS `@page size` mm 단위로 흡수** (Phase 1 = A4 100×148mm 우편엽서 고정) |
| 우편번호 마스크 | `SpinEdit71~77` | 7자리 사이 공백 | 백엔드 `_format_postal_code` 헬퍼 |
| 라벨 후처리 | `Edit28/29` | Posa(직책) / Name(이름) suffix | `?suffix={name}+{posa}` |
| 인쇄 액션 | `Button2/3/4/5` | 인쇄/미리보기/프린터설정/닫기 | `<a href=".pdf" download>` (DEC-038, OQ-002 잔존) |
| 데이터 | `oSqry` (전역 — `Sg_Csum` 또는 호출 폼이 세팅) | 라벨 N건 (Gname/Gposa/Gadds/Gpost/Gjice 등) | 백엔드 `label_service.fetch_label_rows` |

## 3. 라벨 데이터 컬럼 매핑 (`oSqry` 필드 — `Subu23/27/Sobo27` 등 호출 폼이 세팅)

| dfm 필드 (`oSqry.FieldByName`) | 의미 | 모던 응답 키 | data-legacy-id |
| --- | --- | --- | --- |
| `Gadds` | 주소 | `address` | `Seep13.Label.Gadds` |
| `Gpost` | 우편번호 (7자) | `postal_code` | `Seep13.Label.Gpost` |
| `Gname` | 거래처명/수신자명 | `name` | `Seep13.Label.Gname` |
| `Gjice` | 직책/지점 | `branch` | `Seep13.Label.Gjice` |
| `Gposa` | 직책 후행 | `posa` | `Seep13.Label.Gposa` |
| `Scode` | 국내/해외 구분 ('O'=해외) | `is_overseas` (bool) | `Seep13.Label.Scode` |
| `Gbigo` | 비고 (RadioButton3 필터 키) | `memo` | `Seep13.Label.Gbigo` |

> 본 폼은 `oSqry` 가 외부 폼에서 세팅되므로 **호출 컨텍스트별 컬럼 부재 가능성** 존재. 모던은 결측 컬럼은 빈 문자열로 정규화 (레거시 `oSqry.FieldByName('X').AsString` 의 NULL→'' 동작 보존).

## 4. 페이지 / 라벨 1매 사양 (`@page` CSS — Phase 1 우편엽서 고정)

| 속성 | dfm 출처 | 모던 CSS | 비고 |
| --- | --- | --- | --- |
| 용지 크기 | `ComboBox1='A4'` (default) → `SpinEdit61=2100`, `SpinEdit62=2970` (단위 0.1mm) | `@page { size: 210mm 297mm; }` | mm 변환 = ÷10 |
| 80Col | `SpinEdit61=2159, SpinEdit62=2794` | `@page { size: 215.9mm 279.4mm; }` | (Phase 1 미사용) |
| Custom | (사용자 입력) | (Phase 2) | OQ-002 |
| 마진 | `SpinEdit63/64` | `@page { margin: ${SpinEdit63/10}mm ${SpinEdit64/10}mm; }` | Phase 1 = `12mm` 고정 |
| 라인 간격 | `SpinEdit21..31` (5라인) | `<div class='line line-N'>` 의 `margin-top` | Phase 1 = 6mm 고정 |
| 폰트 본문 | `Edit21~25.Font.Name/Size` | `font-family: 'NanumGothic', 'Malgun Gothic'` (서버 번들 — `backend/static/fonts/`) | Phase 1 = 12pt 본문 / 14pt 수신자 |
| Style | Edit{N}.Font.Style → SetTing L240 case | CSS `font-style: italic` / `font-weight: bold` / `text-decoration: underline` | 본 모던은 굵게 1종만 |

> **DEC-039 가시화**: 본 표는 .frf 정본의 **수동 재현 가이드** 일 뿐, 자동 변환 결과 아님. 디자이너는 `Report_1_21.frf` 를 FastReport Designer 로 열어 시각 비교한다.

## 5. 우편번호 분리 매핑 (Mpost1~7 — `PrinDing01` 인용 — 본문 주석화 코드)

레거시 `PrinDing01` (L759~798) 의 `Mpost1..7 := Copy(Mpost0, k, 1)` 는 7자리 우편번호를 1자씩 분리해 SpinEdit71~77 의 `Magin0` (공백 패딩) 으로 출력. 모던:

```python
def _format_postal_code(raw: str, gaps: list[int]) -> str:
    """7자 우편번호를 gaps 패딩으로 분리. gaps=[0,0,0,2,0,0,0] = 'XXX  XXXX'."""
    raw = (raw or "").ljust(7, " ")[:7]
    parts = [(" " * g) + ch for g, ch in zip(gaps, raw)]
    return "".join(parts)
```

Phase 1 = 한국 5자리 우편번호로 단순화 (`gaps=[0,0,0,0,0]`).

## 6. out-of-scope 위젯 (Phase 1 미사용)

| 분류 | dfm 위젯 | 사유 |
| --- | --- | --- |
| 디자인 GUI 전체 | `SpinEdit*`, `Edit21~25`, `SpeedButton1~5`, `Button1` (Gg_Magn 저장) | DEC-039 — `.frf` 정본 / Delphi IDE 수동 |
| 5종 양식 분기 | `ComboBox00` ItemIndex=1~4 | Phase 1 = `0` 고정 (Report_1_21.frf 등가) |
| 프린터 설정 다이얼로그 | `Button4`, `PrinterSetupDialog1` | OQ-002 잔존 (브라우저 인쇄 다이얼로그 위임) |
| 일괄 인쇄 RecNo 범위 | `SpinEdit1/2` | Phase 1 = 단건 호출 (호출자가 N개를 N번 호출) — 후속 사이클 |
| 페이지 컬럼(2단 분할) | `Tong60.frReport00_01.Page.Columns` | Report_1_24/25.frf 전용 — Phase 1 미사용 |
| `PrinDing01/02/03` Canvas 출력 | (런타임) | 이미 Seep13 자체가 폐기 (`{ ... }` 주석화) |
| 폰트 다이얼로그 | `FontDialog1`, `SpeedButton1~5` | 디자인 GUI out-of-scope |

## 7. Deltas — 모던 신설 위젯

| 분류 | 항목 | 위치 | 사유 |
| --- | --- | --- | --- |
| 모던 신규 | `<a href=".pdf" download>PDF 다운로드</a>` | 페이지 우상단 | DEC-004 하이브리드 |
| 모던 신규 | "라벨 1매 미리보기 (CSS @page)" 안내 배너 | 페이지 상단 | DEC-038/039 가시화 |
| 모던 신규 | "프린터 직결 미지원 — 브라우저 인쇄 다이얼로그 사용" 안내 | 인쇄 버튼 옆 | OQ-002 잔존 가시화 |
| dfm out-of-scope | `Button4` 프린터 설정 | — | (브라우저가 처리) |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 | 비고 |
| --- | --- | --- |
| `FormShow` (L131) | (없음 — 라벨 페이지는 URL 파라미터로 즉시 렌더) | |
| `ComboBox00Change` (L142) | (없음 — Phase 1 = form=1 고정) | Phase 2 에서 select 분기 |
| `Button2Click` (L580 — 인쇄) | `<a download>PDF 다운로드</a>` → `GET /api/v1/print/label/{shipment_key}.pdf` | DEC-038 |
| `Button3Click` (L626 — ShowReport 미리보기) | 페이지 자체가 미리보기 | |
| `Button4Click` (L669 — PrinterSetupDialog) | (브라우저 인쇄 다이얼로그) | OQ-002 잔존 |
| `Button5Click` (L674 — Close) | `router.back()` | |
| `frDBDataSet00_01Next` (L1232 — 동적 필터) | `?include_oversea=bool&from=N&to=M` 쿼리 | 백엔드 `label_service.fetch_label_rows` |

## 8.1 Phase 2-α 라벨 5종 양식 표 (form 1~5)

`Tong60.frReport00_01.LoadFromFile('Report\Report_1_2{form+1}.frf')` 의 5 양식을 단일 모던 빌더 `label_service.render_label_html(rows, *, form: int = 1, variant: str = "base")` + 라우터 `?form=1..5` 로 흡수한다 (Phase 1 의 `form=1` 고정 해제).

| form | .frf 정본 | 양식 명 | 페이지 사양 (`@page`) | 컬럼 / 분할 | 주요 차이 (운영 추정) | 우선순위 |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | `Report_1_21.frf` | 일반 라벨 | 100mm × 70mm 기본 | 1단 | Phase 1 정본 — 변경 없음 | Phase 1 (변경 없음) |
| 2 | `Report_1_22.frf` | 우편엽서 | 148mm × 100mm (엽서 표준) | 1단 | 우편번호 박스 + 주소 분할 강조 | Phase 2-α |
| 3 | `Report_1_23.frf` | 대형 라벨 | 148mm × 105mm (A6) | 1단 | 폰트 크기 1.3x | Phase 2-α |
| 4 | `Report_1_24.frf` | 2단 분할 라벨 | A4 가로 (297mm × 210mm) | **2단** (`Page.Columns=2`) | 페이지당 2매 — `column-count: 2` CSS | Phase 2-α |
| 5 | `Report_1_25.frf` | 2단 大 | A4 세로 (210mm × 297mm) | **2단** | 페이지당 4매 (2x2 grid) | Phase 2-α |

> **5 양식 시각 차이의 본질**: form 1~3 = 페이지 크기/폰트만 변동 (단일 라벨/페이지). form 4~5 = `Page.Columns=2` 분할 (CSS `column-count` 또는 grid 흡수 필요). 따라서 `label_service.render_label_html` 은 form 별 `@page` CSS + 컬럼 분할 정책을 데이터 주도로 분기해야 한다 (개별 컴포넌트 5개 금지 — DEC-019/028 룰 7).
>
> **`variant` 보류**: 라벨 5종은 `customer_variants` 가 아니라 **양식 자체의 종류** — `form` 파라미터로 충분. 거래처별 라벨 양식 변형이 발견되면 그때 `variant=` 추가.
>
> **base byte-identical 보장**: `?form=1` 또는 form 미지정 시 Phase 1 산출물과 byte 동일.

## 9. 회귀 가드 체크리스트 (PR 리뷰 시)

- [ ] §3 의 부착 대상 `data-legacy-id` 가 모던 페이지 DOM 에 존재 (총 7개):
  - `Seep13.Label.{Gadds, Gpost, Gname, Gjice, Gposa, Scode, Gbigo}`
- [ ] §6 out-of-scope (디자인 GUI, 5종 분기, 프린터 직결) 가 코드에 들어가지 않음
- [ ] DEC-038 — 라벨 양식 1종 한정 + OQ-002 잔존 안내가 페이지에 가시화
- [ ] DEC-039 — `.frf` 자동 적재 코드 0 (런타임 의존성 0)
- [ ] DEC-028 §3 "버리는 정보" (픽셀 좌표·폰트 굴림·16비트 색상·Glyph) 가 코드에 없음 (CSS `@page` 의 mm 단위는 의미 흡수 — 픽셀 아님)
- [ ] PDF byte signature `%PDF-` + Content-Type `application/pdf` 정상 응답

## 10. 참조

- DEC-004: 하이브리드 (브라우저 인쇄 + 서버 PDF)
- DEC-028: dfm→html 산출물 영구 입력 동결
- **DEC-038** (T8 신설): C7 Phase 1 라벨 양식 1종 한정
- **DEC-039** (T8 신설): `.frf` 자산 정책 (참조용 카탈로그 only)
- 화면 카드: (없음 — 본 노트 자체가 단일 진실원)
- contract: [`migration/contracts/print_label.yaml`](../../migration/contracts/print_label.yaml) v1.0.0
- 핸들러 인덱스: [`analysis/handlers/c7_phase1.md`](../handlers/c7_phase1.md) §SQL-PR-6
- `.frf` 정본 인벤토리: [`analysis/print_specs/frf_catalog.md`](../print_specs/frf_catalog.md) §라벨
- 선례: 본 노트는 C7 신규 — 선례 없음 (Sobo46/Sobo49 의 미리보기 패턴 참고)
