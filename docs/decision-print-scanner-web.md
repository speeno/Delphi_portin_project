# 인쇄·바코드 웹 대체 방향 결정 메모

레거시 델파이의 **인쇄(VCL/QuickReport/Canvas)**·**바코드 입력(COM 시리얼·키보드 웨지)**을 웹에서 어떻게 대체할지 1차 방향을 정합니다.

- 입력 자료: [`docs/legacy-print-scanner-integration-survey.md`](legacy-print-scanner-integration-survey.md)
- 미해결 질문: [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md) **OQ-002**
- 의사결정 기록: [`legacy-analysis/decisions.md`](../legacy-analysis/decisions.md) **DEC-004**(본 메모로 등록)

> **본 메모는 1차 방향(default)** 입니다. 현장 인터뷰(OQ-002 클로저) 결과로 변경될 수 있으며, 변경 시 본 문서 §4에 기록합니다.

## 1. 1줄 결정 (Default)

> **인쇄는 “브라우저 인쇄(HTML/CSS) + 라벨은 서버 PDF” 하이브리드를 1차로 채택하고, 라벨 프린터 직결은 OQ-002 결과 후 재검토.  
> 바코드는 “키보드 웨지를 1차”로 두고, COM 시리얼 사용처(`Tong08`)는 **로컬 브리지**(또는 Web Serial)를 베타 후 옵션으로 도입.**

| 영역 | 1차 채택 | 2차 옵션 | 비채택(현시점) |
|------|----------|----------|----------------|
| 일반 리포트(거래명세·집계) | 브라우저 인쇄(HTML/CSS) + PDF 다운로드 | 서버 PDF(WeasyPrint/wkhtmltopdf) | 클라이언트 직접 드라이버 호출 |
| 라벨(좁은폭·열전사) | 서버 PDF(라벨 템플릿) → 브라우저 인쇄 | 라벨 프린터 직결(로컬 브리지) | ZPL/EPL 직송(베타 외) |
| 바코드 입력 | 키보드 웨지(USB-HID) | 로컬 브리지(WebSocket) → 시리얼 → 브라우저 | Web Serial(브라우저 정책 의존) |

## 2. 결정 근거

- **레거시 코드 1차 조사**(`legacy-print-scanner-integration-survey.md`):
  - 프린터: VCL `Printers`, `TPrintDialog`, `QuickRpt`, `Printer.Canvas`(좌표 직접 출력) 다수 — **OS 프린터 스풀 의존도 높음**.
  - 시리얼 바코드: `Tong08.pas`에서 `CPort`로 CR 종료 문자열을 받아 `FTong07.Button104Click(nBarcode)` 호출 — **단일 진입점이라 키보드 웨지로 대체하기 비교적 쉬움**.
- **현실 제약**:
  - Web Serial은 일부 브라우저(특히 사내 폐쇄망의 구형 IE/Edge)에서 미지원 가능.
  - 사내 라벨 프린터 모델·드라이버는 OQ-002 미클로저 → 직결 우선 결정은 위험.
- **운영 우선순위**: 베타에서는 “출력물이 종이로 나간다”가 합격선 → **브라우저 인쇄 + PDF**로 충분.

## 3. 후속 작업·게이트 매핑

| 항목 | 담당 | 마감(권장) | 게이트 |
|------|------|-----------|--------|
| OQ-002 클로저(장비 모델·연결 방식) | 메인개발자 + 현장 운영자 | 게이트 #1(2026-07-17) 이전 | #1 분석 산출물 승인 |
| 라벨 폰트·여백·바코드 모듈 폭 합의 | 웹 포팅 + 현장 운영자 | 게이트 #5(2026-09-25) 이전 | #5 인쇄 결과 승인 |
| 키보드 웨지 화면 포커스·Enter 핸들링 표준 | 웹 포팅 | C2(출고 접수) 계약 시점 | #3 API 계약 승인 |
| 로컬 브리지/Web Serial 채택 여부 | 웹 포팅 + 인프라 | 베타 회고 후 | #4 또는 별도 결정 |

## 4. 변경 이력

- 2026-04-21 — 1차 방향 결정(본 메모), [`legacy-analysis/decisions.md`](../legacy-analysis/decisions.md) **DEC-004**로 등록.

---

*관련 산출물: [`docs/legacy-print-scanner-integration-survey.md`](legacy-print-scanner-integration-survey.md), [`docs/core-scenarios-candidates.md`](core-scenarios-candidates.md)(C7·C8), [`docs/eval-axes-and-dod-draft.md`](eval-axes-and-dod-draft.md)(축 “ux” 임계값)*
