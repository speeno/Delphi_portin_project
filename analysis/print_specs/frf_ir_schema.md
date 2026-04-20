# FRF Canonical IR — 스키마 v0 동결 (2026-04-20)

> **목적**: `.frf` (FastReport VCL 4.x 바이너리) 의 자체 디코더가 산출하는
> *중간 표현 (Intermediate Representation, JSON)* 의 형식·의미·허용 오차를 동결한다.
> 본 스키마는 [c7-nofr-porting](../../) 계획의 § "1) Canonical IR 동결" 산출물이며,
> 이후 단계 (Decoder PoC / IR→HTML 컴파일러 / 회귀 게이트) 의 **계약** 이다.
>
> **출처/참조**:
> - [`analysis/research/c7_oss_shortlist.md`](../research/c7_oss_shortlist.md) — F-01/F-03 즉시 재사용
> - [`analysis/research/c7_oss_license_matrix.md`](../research/c7_oss_license_matrix.md) — MIT/BSD-2/BSD-3 인용 의무
> - FastReports/FastReport.Documentation (MIT) — `ReportObjects.md` / `Bands.md` / `Expressions.md` 명세
> - FastReports/FreeReport (BSD-2) — `Source/FR_Class.pas` 의 `LoadFromStream` 알고리즘
> - [`c7_phase1.md`](./c7_phase1.md) — 운영 출력 정본 (P1-A ~ P1-F)
>
> **본 스키마는 `.frf` 와 `.frx` 의 *95% 시맨틱 호환*** 을 활용해 두 포맷의 공통
> 객체 모델로 정의된다. `.frx` 의 검증 가능한 정본을 IR 비교 자료로 사용한다.

## 0. 설계 원칙

1. **JSON 직렬화 가능** — Python `dict` 로 표현 가능한 트리. 외부 라이브러리 무의존.
2. **읽기 가능성 우선** — 키 이름은 풀네임 (`width_mm`, `font_size_pt`).
3. **단위 정규화** — `.frf` TWIPs (1/1440 인치) 와 `.frx` Pt (1/72 인치) 를 **mm 단일 단위** 로 변환.
4. **strict parse + unknown capture** — 모르는 객체/속성은 `unsupported_objects[]` 또는
   `unsupported_props{}` 에 *수집* (실패-허용). 디코더는 빈 IR 보다 **부분 IR** 을 선호.
5. **변형 (variant)** — 거래처별 차이는 코드 분기 ❌, IR 트리에 `variant_profile` 키로 attach.
6. **불변 (immutable)** — IR JSON 은 디코더 산출 후 변경 ❌. 컴파일러는 *읽기 전용* 으로 소비.

## 1. 최상위 구조

```json
{
  "schema_version": "0.1.0",
  "source": {
    "kind": "frf",
    "signature": "FRF15",
    "filename": "Report_1_21.frf",
    "decoded_at": "2026-04-20T00:00:00Z",
    "decoder_version": "0.1.0"
  },
  "report": {
    "name": "Report_1_21",
    "title": "라벨 (우편엽서)",
    "author": "(미상)",
    "creator_version": "FastReport VCL 4.x",
    "page_count_hint": 1
  },
  "pages": [ /* IR.Page 객체 배열 — §2 */ ],
  "data_sources": [ /* IR.DataSource 객체 배열 — §3 */ ],
  "expressions_dictionary": { /* §4 */ },
  "variant_profile": null,
  "unsupported_objects": [ /* §5 */ ],
  "decoder_warnings": [ /* §5 */ ]
}
```

### 키 의미

| 키 | 타입 | 필수 | 의미 |
|---|---|:---:|---|
| `schema_version` | string (semver) | ✅ | 본 스키마 버전. 호환성 깨질 때 메이저 증가. |
| `source.kind` | enum {`frf`, `frx`} | ✅ | 디코더 입력 포맷. 본 트랙은 `frf` 만. |
| `source.signature` | string | ✅ | 바이너리 첫 5 바이트 (`FRF15` / `FRF20`). |
| `source.filename` | string | ✅ | 원본 파일명 (디버깅). |
| `report.creator_version` | string | ⚠️ | 추정값. 헤더에서 추출 불가 시 `"unknown"`. |
| `pages[]` | array | ✅ | 페이지 트리. 최소 1. |
| `data_sources[]` | array | ❌ | 데이터셋 메타. PoC 단계는 빈 배열 허용. |
| `expressions_dictionary` | object | ❌ | 페이지/객체에서 참조되는 표현식 토큰. |
| `variant_profile` | object/null | ❌ | 거래처/지점별 차이 메타. PoC 는 `null`. |
| `unsupported_objects[]` | array | ✅ | 디코더가 skip 한 객체 (실패-허용). |
| `decoder_warnings[]` | array | ✅ | 경고 메시지 (정확도 ⇩ 가능성 신호). |

## 2. Page / Band / Object 트리

### 2.1. IR.Page

```json
{
  "name": "Page1",
  "size_mm": { "width": 100.0, "height": 148.0 },
  "margin_mm": { "top": 8.0, "right": 8.0, "bottom": 8.0, "left": 8.0 },
  "orientation": "portrait",
  "columns": 1,
  "background": null,
  "bands": [ /* IR.Band 배열 */ ]
}
```

| 키 | 의미 |
|---|---|
| `size_mm` | 페이지 크기 (mm). `.frf` paper code → mm 변환 (`A4`/`Letter`/`Custom`). |
| `margin_mm` | 4 방향 여백. 디코더 누락 시 8mm 기본. |
| `orientation` | `portrait` / `landscape`. `width > height` 면 `landscape` 강제. |
| `columns` | 다단 인쇄 (라벨류 = 1). |
| `background` | 색상 또는 이미지. 미사용 시 `null`. |

### 2.2. IR.Band

```json
{
  "name": "Band1",
  "type": "MasterData",
  "y_mm": 0.0,
  "height_mm": 30.0,
  "data_source_ref": null,
  "objects": [ /* IR.Object 배열 */ ]
}
```

`type` 허용 enum (FastReport.Documentation `Bands.md` 와 1:1 매핑):

| IR `type` | `.frf` Pascal 클래스 | `.frx` 클래스 |
|---|---|---|
| `ReportTitle` | `frBandReportTitle` | `ReportTitleBand` |
| `ReportSummary` | `frBandReportSummary` | `ReportSummaryBand` |
| `PageHeader` | `frBandPageHeader` | `PageHeaderBand` |
| `PageFooter` | `frBandPageFooter` | `PageFooterBand` |
| `ColumnHeader` | `frBandColumnHeader` | `ColumnHeaderBand` |
| `ColumnFooter` | `frBandColumnFooter` | `ColumnFooterBand` |
| `MasterHeader` | `frBandMasterHeader` | `GroupHeaderBand` (단일 그룹 시) |
| `MasterData` | `frBandMasterData` | `DataBand` |
| `MasterFooter` | `frBandMasterFooter` | `GroupFooterBand` |
| `Child` | `frBandChild` | `ChildBand` |
| `Overlay` | `frBandOverlay` | `OverlayBand` |

### 2.3. IR.Object

공통 속성 (모든 객체 종류):

```json
{
  "name": "Memo1",
  "type": "Text",
  "rect_mm": { "x": 5.0, "y": 5.0, "w": 80.0, "h": 6.0 },
  "z_order": 0,
  "visible": true,
  "rotation_deg": 0,
  "border": { "left": true, "top": true, "right": true, "bottom": true,
              "color": "#888888", "width_pt": 1.0, "style": "solid" },
  "fill": { "color": "#FFFFFF", "transparent": true },
  "style": { /* type 별 §2.4~§2.9 */ },
  "binding": { /* §2.10 */ },
  "unsupported_props": {}
}
```

`type` 허용 enum:

| IR `type` | `.frf` Pascal | `.frx` |
|---|---|---|
| `Text` | `frTextView` / `TfrMemoView` | `TextObject` |
| `Picture` | `frPictureView` | `PictureObject` |
| `Line` | `frLineView` | `LineObject` |
| `Rect` | `frRectView` | `ShapeObject` (kind=rectangle) |
| `Shape` | `frShapeView` | `ShapeObject` |
| `Barcode` | `frBarCodeObject` | `BarcodeObject` |
| `SubReport` | `frSubReportView` | `SubreportObject` |
| `Cross` | `frCrossView` | (n/a — 본 트랙 PoC 미지원) |
| `Chart` | `frChartView` | `ChartObject` (본 트랙 PoC 미지원) |

#### 2.4. IR.Object — Text style

```json
"style": {
  "font_family": "NanumGothic",
  "font_size_pt": 12.0,
  "font_weight": "bold",
  "font_italic": false,
  "font_underline": false,
  "color": "#222222",
  "halign": "left",
  "valign": "top",
  "wordwrap": true,
  "padding_pt": { "top": 1.0, "right": 1.0, "bottom": 1.0, "left": 1.0 },
  "format": null
}
```

#### 2.5. IR.Object — Picture style

```json
"style": { "stretched": true, "keep_aspect": false, "image_blob_ref": "Image001" }
```

> `image_blob_ref` 는 `pages[].embedded_blobs{}` (별도 §) 에서 base64 로 보관.

#### 2.6. IR.Object — Line / Rect / Shape style

(`border` 공통 + `style.kind` 만 추가) — `kind` ∈ {`rect`, `roundrect`, `ellipse`, `triangle`, `diamond`}.

#### 2.7. IR.Object — Barcode style

```json
"style": {
  "symbology": "Code128",
  "show_text": true,
  "rotation_deg": 0,
  "module_width_mm": 0.33,
  "module_height_mm": 10.0
}
```

> `symbology` 허용 enum: `Code39` / `Code128` / `EAN13` / `EAN8` / `QR` / `DataMatrix` / `PostNet`.
> 본 트랙 PoC v0 = `Code128` + `QR` 만 (M-01 python-qrcode + python-barcode 폴백).
> 미지원 symbology 는 `unsupported_objects[]` 로 수집.

### 2.10. IR.Object.binding (데이터 바인딩 / 표현식)

모든 `Text` / `Picture` / `Barcode` 가 공유:

```json
"binding": {
  "kind": "literal",
  "value": "EMPLOYEES",
  "raw": "EMPLOYEES"
}
```

또는

```json
"binding": {
  "kind": "expression",
  "value": null,
  "raw": "[Employees.LastName]",
  "tokens": [
    { "type": "field", "table": "Employees", "column": "LastName",
      "format": null, "format_spec": null }
  ]
}
```

또는 (혼합 / 함수 호출 / Pascal 표현식):

```json
"binding": {
  "kind": "expression",
  "value": null,
  "raw": "Today is [Date]",
  "tokens": [
    { "type": "literal", "value": "Today is " },
    { "type": "function", "name": "Date", "args": [], "format": null }
  ]
}
```

> `kind` enum: `literal` / `expression` / `picture_blob` / `picture_field`.
> 표현식 토큰화는 PoC 단계 = **단순 `[A.B]` / `[A.B "fmt"]` 패턴만** (FastReport.Documentation
> `Expressions.md` 의 다단계 평가는 v0 미지원, `unsupported_props.complex_expression = true`
> 로 marker 후 raw 보존).

## 3. DataSource 메타

```json
{
  "name": "Employees",
  "reference_name": "NorthWind.Employees",
  "columns": [
    { "name": "EmployeeID", "data_type": "int" },
    { "name": "LastName", "data_type": "string" }
  ]
}
```

> PoC 단계 — `.frf` 는 데이터셋 메타를 self-describing 하지 않음. 빈 배열 + 디코더 경고만.
> 실제 데이터는 운영 시 기존 C7/C5/C2/C4 조회 서비스의 결과 dict 가 주입됨.

## 4. Expressions Dictionary

```json
{
  "[Employees.LastName]": { "table": "Employees", "column": "LastName" },
  "[PageN]": { "function": "PageN" },
  "[Date]": { "function": "Date" }
}
```

> 페이지/객체에서 발견된 모든 토큰의 *유일 (uniqued)* 색인. 컴파일러가 Jinja2
> 변수명 정규화 (`{{ employees__last_name }}`) 시 사용.

## 5. unsupported_objects[] / decoder_warnings[]

```json
"unsupported_objects": [
  { "name": "Chart1", "type": "Chart",
    "reason": "ChartObject 디코더 v0 미지원",
    "raw_size_bytes": 256,
    "raw_offset": 1024 }
],
"decoder_warnings": [
  { "code": "FRF_W_001", "message": "TfrCheckBoxView 미지원 — skip", "object_name": "Check1" }
]
```

> `reason` 은 인간 가독 메시지. `code` 는 회귀 게이트가 *허용 임계값* 으로 사용.

## 6. 단위 변환 표 (mm 정규화)

| 원본 단위 | 출처 | 변환식 | 정밀도 |
|---|---|---|---|
| TWIPs (1/1440 인치) | `.frf` | `mm = twips * 25.4 / 1440` | 0.0001 mm |
| Pixel (1/72 인치) | `.frx` Pt | `mm = pt * 25.4 / 72` | 0.0001 mm |
| Pixel (96 dpi) | 일부 PNG 임베드 | `mm = px * 25.4 / 96` | 0.0001 mm |

## 7. 허용 오차 기준 (회귀 게이트 입력)

본 IR 의 회귀 검증 시 **수동 정본 (DEC-039 Phase 1 5+1 양식) vs 자동 IR→HTML→PDF**
의 비교에서 다음 오차를 허용한다:

### 7.1. 렌더링 오차

| 항목 | 임계값 | 비고 |
|---|---|---|
| 객체 좌표 (x,y,w,h) | ±0.5 mm | 단위 변환 round-trip 손실 허용 |
| 텍스트 baseline | ±1.0 mm | 폰트 메트릭 차이 (NanumGothic vs 원본) |
| 라인 굵기 | ±0.2 pt | `border.width_pt` |
| 색상 차이 | ΔE < 5 (Lab) | sRGB 가정 |

### 7.2. 텍스트 오차

| 항목 | 임계값 | 비고 |
|---|---|---|
| 텍스트 일치율 (수동 정본 ↔ 자동) | ≥ **99.0%** | `pdftotext` 후 정규화 비교 |
| 줄바꿈 위치 | ±1 줄 | wordwrap 알고리즘 차이 허용 |
| 페이지 수 | ±0 (정확 일치) | 본 트랙 PoC = 단일 페이지 양식만 |

### 7.3. 페이지 오차

| 항목 | 임계값 | 비고 |
|---|---|---|
| 페이지 크기 (`@page size`) | 정확 일치 | 100mm 148mm / 210mm 297mm 등 |
| 여백 | ±0.0 mm (정확) | margin 은 단위 round-trip 없이 직접 매핑 |
| 시각 픽셀 diff | < **5%** 픽셀 | `pdftoppm` 후 픽셀 단위 비교 (회귀 게이트) |

## 8. 본 스키마와 운영 출력 (P1-A~P1-F) 의 관계

| Phase 1 양식 | 본 IR 적용 가능? | 노트 |
|---|:---:|---|
| P1-A 청구서 (Sobo46) | ⚠️ 부분 | 표 컬럼 15개 → 본 IR 의 Text 객체 트리로 매핑 가능. PoC 후 v1 로 미룸. |
| P1-B 세금계산서 (Sobo49) | ⚠️ 부분 | 단건 카드 형식. v1 로 미룸. |
| P1-C 출고 거래명세서 | ⚠️ 부분 | 6컬럼 표. v1 로 미룸. |
| P1-D 반품 영수증 | ⚠️ 부분 | 9컬럼 표. v1 로 미룸. |
| P1-E 거래명세서 | ⚠️ 부분 | 6컬럼 표. v1 로 미룸. |
| **P1-F 라벨 (Seep13)** | ✅ **PoC v0 우선** | `Report_1_21.frf` — 단순 텍스트 4 객체. PoC 1양식 = 본 양식. |

## 9. 변경 이력

| 일자 | 버전 | 변경 |
|---|---|---|
| 2026-04-20 | 0.1.0 | 초기 동결. PoC 1 양식 (P1-F = Report_1_21.frf) 대상으로 Page/Band/Text 객체 + Binding 까지 정의. Barcode/Chart/SubReport 는 v0 미지원 (`unsupported_objects[]` 로 수집). 허용 오차 (렌더링/텍스트/페이지 3 차원) 동결. |
