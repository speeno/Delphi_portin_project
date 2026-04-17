# 레거시 델파이 — 프린트·스캐너(바코드) 연동 조사 기록

**조사 대상:** `legacy_delphi_source/legacy_source/` (대표 분석 루트)  
**조사 방식:** 소스·DFM 문자열 검색 + 핵심 유닛 수동 열람  
**갱신:** 2026-04-21

## 1. 요약

| 구분 | 코드에서 확인된 내용 | 비고 |
|------|----------------------|------|
| 프린터 | VCL `Printers` / `Printer` 캔버스, `TPrintDialog`, QuickReport, (추정) FastReport 계열 사용 | OS 프린터 스풀·드라이버 의존 |
| 바코드 리더(시리얼) | **ComPort(CPort)** 로 수신 후 CR 기준으로 문자열 확정 → 화면 핸들러 호출 | TWAIN/WIA 이미지 스캐너 API는 **미발견** |
| 바코드(인쇄) | `TfrBarCodeObject` 등 리포트용 바코드 컴포넌트 | 인쇄물 생성 |
| 키보드 웨지형 스캐너 | 전용 API 없음; 다수 `KeyPress`는 **가능한 입력 경로**로만 추정 | 현장에서 실제 사용 여부는 OQ-002로 확인 |

## 2. 프린터 — 확인된 유닛·패턴

### 2.1 `Tong04.pas`

- `uses`에 `Printers`, `FR_Chart` 등 포함.
- `Print_11_01`, `Print_12_01` … 다수의 `Print_*` 프로시저 — **화면별 인쇄 진입점**으로 보임.
- **포팅 시:** 각 `Print_*`가 호출하는 리포트 컴포넌트·데이터셋·용지 설정을 웹(PDF/브라우저 인쇄)로 매핑해야 함.

### 2.2 `Seep13.pas`

- `Printer.BeginDoc` / `Printer.Canvas` / `Printer.EndDoc`로 **캔버스 직접 출력**(라벨·명함 형 레이아웃 가능성).
- **포팅 시:** 좌표·폰트·줄바꿈을 HTML/CSS 또는 PDF 생성 라이브러리로 재현·검증 필요.

### 2.3 `Seak05.pas`

- `QuickRpt`, `Printers` 사용; `Printer.SetPrinter` 관련 코드는 **주석 처리**되어 있음.
- **포팅 시:** QuickReport 대체(템플릿·밴드 구조) 범위 산정.

### 2.4 `Tong01.pas`

- `TPrintDialog`, `TPrinterSetupDialog` — 사용자 프린터 선택·설정.

## 3. 스캐너(바코드 입력) — 확인된 유닛·패턴

### 3.1 `Tong08.pas` (시리얼 바코드)

- 라이브러리: **ComPort** (`CPort`, `CPortCtl`) — `TComPort`, `TComTerminal`.
- `ComPortRxChar`에서 `ComPort.Read`로 바이트 수신, `#13`(CR)에서 문자열을 `nBarcode`로 확정.
- `nForm` 값에 따라 `Sobo21` / `Sobo22` / `Sobo23`의 `FTong07.Button104Click(nBarcode)` 호출.

**포팅 시 고려:**

- Web Serial API, 로컬 브리지(네이티브 헬퍼), 또는 **키보드 웨지만 유지**하고 동일 이벤트 체인을 웹에서 재현하는지 현장 결정.

### 3.2 `Tong06.dfm`

- `frBarCodeObject1: TfrBarCodeObject` — **인쇄물·리포트용 바코드 그래픽**(스캐너 하드웨어 제어 아님).

### 3.3 `*KeyPress` (다수 유닛)

- 예: `Subu13`, `Subu44`, `Seak09` 등 — 숫자·길이 제한 등 **입력 검증**.
- **키보드 웨지 스캐너**와 함께 쓰이면 웹에서도 동일 UX(포커스·Enter 처리) 검증 필요. 코드만으로는 “스캐너 전용” 여부 불명.

## 4. 미확인·현장 확인 필요 (OQ-002 연계)

- 실제 매장/창고에서 **COM 바코드 리더 vs USB-HID 웨지** 비중.
- `Tong08`이 항상 띄워지는지, 대체 경로(웨지만)만 쓰는지.
- 라벨 프린터 모델·드라이버(Windows 전용 명령 등) 유무.

→ [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md) **OQ-002**

## 5. 관련 체크리스트

- [`docs/delphi-developer-confirmation-checklist.md`](delphi-developer-confirmation-checklist.md) §4.1 (장비 모델·연결 방식)

---

*본 문서는 레포 내 1차 코드 조사 기록이며, 운영 환경의 최종 확정은 현장 인터뷰·OQ-002 클로저로 보완한다.*
