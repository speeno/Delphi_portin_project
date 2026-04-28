# 레거시 바코드·출력 vs 모던 포팅 매트릭스

**ID**: AUDIT-BARCODE-PRINT-2026-04-27  
**근거 계획**: 레거시 바코드·출력 vs 모던 포팅 점검 (참조: `docs/legacy-print-scanner-integration-survey.md`, DEC-004/010/040)

본 문서는 레거시 델파이에서 **바코드가 등장하는 경로**를 구분하고, 모던 코드·계약·문서와 **1:1 여부**를 표로 정리한다. (픽셀·폰트 회귀는 범위 외.)

---

## 1. 레거시 인벤토리 (역할별)

| ID | 레거시 위치 | 역할 | “출력”과의 관계 |
|----|----------------|------|------------------|
| L1 | [`legacy_delphi_source/legacy_source/Tong08.pas`](../../legacy_delphi_source/legacy_source/Tong08.pas) `ComPortRxChar` | COM 포트로 바이트 수신, `#13`(CR)에서 문자열 확정 후 `Sobo21/22/23.FTong07.Button104Click(nBarcode)` | **입력** — 인쇄 파이프라인이 아님 |
| L2 | [`legacy_delphi_source/legacy_source/Tong07.pas`](../../legacy_delphi_source/legacy_source/Tong07.pas) / `Tong70` — `Button104Click(nBarcode)` | 스캔 문자열을 `Edit101` 등에 반영 (생성기 `examples/.../Tong70.pas_analysis.json` 에 시그니처 기록) | 입력 UI |
| L3 | [`legacy_delphi_source/legacy_source/Tong06.dfm`](../../legacy_delphi_source/legacy_source/Tong06.dfm) `frBarCodeObject1: TfrBarCodeObject` | FastReport 디자이너 **리포트용 바코드 그래픽** 컴포넌트 | **인쇄/PDF**에 막대 심볼로 그려질 수 있음 |
| L4 | [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Tong06/Tong60.form.json`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Tong06/Tong60.form.json) `frBarCodeObject1` / `TfrBarCodeObject` | 동일 컴포넌트의 구조화 산출물 | L3 과 동일 |
| L5 | [`legacy_delphi_source/legacy_source/Subu59_4.pas`](../../legacy_delphi_source/legacy_source/Subu59_4.pas) `tsclib.dll` — `barcode(...)`, `printlabel`, `windowsfont` | TSC 라벨 프린터 **물리 라벨** (단위 주석: 물표출력) | **하드웨어 라벨** — 웹 PDF 경로와 별개 |
| L6 | [`legacy_delphi_source/legacy_source/Subu21.pas`](../../legacy_delphi_source/legacy_source/Subu21.pas) `Tong20.Print_00_00('21-01'/'21-02')`, `Tong40.Print_21_02` | 거래명세 등 **리포트 인쇄 진입** | 템플릿에 바코드 객체가 있으면 L3 과 결합 가능 |

---

## 2. 모던 매핑·충실도

| 레거시 ID | 모던 대응 | 충실도 | 비고 |
|-----------|-----------|--------|------|
| L1, L2 | **C8** — `POST /api/v1/scan/match` [`scan.py`](../../도서물류관리프로그램/backend/app/routers/scan.py), [`scan_match_service.py`](../../도서물류관리프로그램/backend/app/services/scan_match_service.py); 프론트 [`scan-input.tsx`](../../도서물류관리프로그램/frontend/src/components/shared/scan-input.tsx), [`scanner.ts`](../../도서물류관리프로그램/frontend/src/lib/scanner.ts); 계약 [`migration/contracts/barcode_scan.yaml`](../../migration/contracts/barcode_scan.yaml) | **의도적 대체** | DEC-004 USB-HID 1차, DEC-010/040. COM 포트 동일 구현 아님 |
| L3 | **IR HTML 컴파일** — [`print_ir_compiler.py`](../../도서물류관리프로그램/backend/app/services/print_ir_compiler.py) `_compile_barcode` → `div.frf-barcode` + 바인딩 또는 `[barcode]` | **플레이스홀더** | Delphi `TfrBarCodeObject` 수준의 **스캔 가능 1D/2D 심볼** 재현은 미보장 |
| L4 | (L3 과 동일 파이프라인) | 동일 | |
| L5 | **미포팅** (OQ-002-R 잔류) | N/A | Web Serial·로컬 브리지·TSC 드라이버는 별 시나리오 |
| L6 거래명세 | **수동 HTML** [`transactions_service.render_sales_statement_html`](../../도서물류관리프로그램/backend/app/services/transactions_service.py) — 라인 `bcode`/도서명은 **텍스트 `<td>`**; IR 경로는 `print_template_registry` 정책에 따름 | **텍스트 코드 표기** | 바코드 **막대 그래픽** 필드 없음 |
| Sobo21 UI | [`analysis/layout_mappings/Sobo21.md`](../layout_mappings/Sobo21.md) — 바코드·일부 인쇄 **out-of-scope** | **1차 제외** | DEC-028 매핑 노트와 일치 |

---

## 3. FRF / IR 산출물 스캔 결과 (2026-04-27 레포 기준)

### 3.1 `*.ir.json` 내 `type: Barcode` (또는 `"Barcode"`)

- 워크스페이스 전역 `rg '"type": "Barcode"' **/*.ir.json'`: **0건**.
- 샘플 [`Report_2_11-.ir.json`](../../debug/output/frf_converted_all/legacy_delphi_source/legacy_source/Report/Report_2_11-.ir.json): 객체 타입은 `MasterData` / `Text` 만 확인 (거래명세 IR).

**해석**: 현재 보관된 IR 변환 샘플에는 **Barcode 객체가 직렬화되지 않았거나**, 해당 리포트에 바코드 객체가 없다. `Tong06` 디자이너 폼의 `TfrBarCodeObject`는 **런타임 리포트(.frf) 쪽**과 별 트리일 수 있음.

### 3.2 `*.template.html` 의 `frf-barcode` CSS

- [`debug/output/frf_converted_all/.../Report/*.template.html`](../../debug/output/frf_converted_all/legacy_delphi_source/legacy_source/Report/) 다수에 **공통 스타일 블록** `.frf-barcode` 존재 (컴파일러 [`print_ir_compiler.py`](../../도서물류관리프로그램/backend/app/services/print_ir_compiler.py) 와 정합).
- 이는 **바코드 객체가 IR 단계에서 HTML로 펼쳐질 때** 사용할 CSS 일반 규칙이며, 개별 템플릿에 실제 `<div class='frf-barcode'>` 노드가 있는지는 템플릿별 추가 확인이 필요하다.

### 3.3 원본 `.frf` 텍스트 검색

- `legacy_delphi_source/legacy_source/Report/*.frf` 에 대해 `Barcode`/`BarCode` 문자열 grep: **0건** (포맷이 바이너리이거나 문자열 미포함 가능 — 한계 명시).

---

## 4. 갭(GAP) 및 후속 결정안 (gap-decision)

| GAP-ID | 내용 | 권장 후속 |
|--------|------|-----------|
| G1 | IR `_compile_barcode` 가 **실제 바코드 인코딩**이 아닌 영역·플레이스홀더 | WeasyPrint 호환 **SVG** (예: Code128) 생성 또는 **서버에서 PNG data-URL** 생성 후 `img` 삽입; `_compile_barcode` 에서만 분기해 DEC-037 print 파이프와 정합 문서화 |
| G2 | 거래명세 PDF는 **ISBN/도서코드 텍스트**만 | 스캔 요구 시 G1 과 동일하되 `sales_statement_base` 또는 수동 HTML **한 화면만** 범위 한정 |
| G3 | TSC `tsclib` 라벨 | OQ-002-R — 웹과 무관한 **현장 라벨** 정책 유지 또는 별도 마이크로서비스 |

**DEC 갱신 시 제안 문구(초안)**: “FRF `Barcode` 타입은 Phase1에서 HTML 플레이스홀더로만 동등; 스캔 가능 심볼이 계약 필수인 템플릿은 DEC-037 부록에 템플릿 ID 명시 후 G1 구현.”

---

## 5. 한 줄 결론

- **스캐너 → 화면**: 레거시 COM(Tong08) 대신 **C8 서버 매칭 + 웨지**로 **의도적으로** 포팅됨.  
- **인쇄물에 바코드 막대**: **Tong06 `TfrBarCodeObject` 수준의 1:1은 아님**; IR은 플레이스홀더, 거래명세 수동 HTML은 **텍스트 bcode**; TSC 라벨은 **웹 범위 밖**.

---

## 6. 검증 체크리스트 (운영/QA)

- [ ] 실제 운영 `.frf` 중 바코드가 **필수**인 템플릿 ID 목록 확정 (Delphi 디자이너 또는 인쇄 샘플 PDF).  
- [ ] 해당 템플릿에 대해 모던 PDF에서 **사람이 스캔 가능한지** 현장 검증.  
- [ ] 불가 시 G1 범위에 템플릿 화이트리스트 추가 후 구현 스프린트 착수.
