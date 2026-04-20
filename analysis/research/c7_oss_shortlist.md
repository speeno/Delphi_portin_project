# C7 비-FastReport 트랙 — OSS Shortlist v0 (2026-04-20)

> **목적**: [`c7_oss_discovery_log_20260420.md`](./c7_oss_discovery_log_20260420.md)
> 의 raw 후보를 5 차원 점수로 정렬해 본 트랙의 *즉시 재사용 / 참조 / 배제* 3 분류를
> 동결한다. 본 문서는 [c7-nofr-porting](../../) 계획 §0 (OSS 게이트) 의 **결정 정본**.
>
> **시드 문서** ([`c7_frf_parser_oss_research.md`](./c7_frf_parser_oss_research.md),
> [`c7_b4_poc_1day_report.md`](./c7_b4_poc_1day_report.md)) 의 항목은 본 shortlist 의
> 점수 산정에 *비교 기준* 으로만 인용 — 재기재 ❌.

## 0. 평가 기준 (각 1~5 점, 총점 25 점 만점)

| 차원 | 정의 | 5 점 정의 | 1 점 정의 |
|---|---|---|---|
| FMT | 포맷 적합성 (직접 `.frf` 지원) | `.frf` 바이너리 100% 디시리얼라이저 보유 | `.frf` 와 무관, 영감만 |
| LIC | 라이선스 적합성 (운영 incorporate 가능성) | MIT/BSD/Apache, 저작권 표시만 | AGPL/상용, 사실상 incorporate ❌ |
| MNT | 유지보수성 | 2025+ 활발 + 테스트 + 이슈 응답 | 2015 이전 + 이슈 폐쇄 |
| RUS | 재사용성 (파서 코어 분리 가능 여부) | 단일 파일 / 명확 API | 거대 모놀리스, 추출 어려움 |
| OPS | 운영 적합성 (런타임 의존성 0 유지) | Python 순수 + 표준 라이브러리만 | .NET/Pascal/Delphi 런타임 강요 |

### 0.1. 결정 임계치

- **즉시 재사용** (run 0 ~ run N 직접 incorporate): 총점 ≥ 18, **OPS ≥ 4** 필수.
- **참조** (코드 incorporate 안 함, 시맨틱/명세만 차용): 12 ≤ 총점 < 18, OPS 와 무관.
- **배제** (본 트랙 사용 ❌): 총점 < 12, 또는 OPS = 1 + LIC ≤ 2.

## 1. Top 후보 점수표 (전체 12 건)

| 순위 | ID | 후보 | FMT | LIC | MNT | RUS | OPS | 총점 | 분류 |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 1 | F-01 | FastReports/FreeReport (Pascal) | **5** | 4 | 2 | 4 | 3 | **18** | 즉시 재사용 (알고리즘만 Python 포팅) |
| 2 | F-03 | FastReports/FastReport.Documentation | 4 | 5 | 5 | 5 | 5 | **24** | 즉시 재사용 (스키마 명세) |
| 3 | M-01 | lincolnloop/python-qrcode | 1 | 5 | 5 | 5 | 5 | **21** | 즉시 재사용 (BarcodeObject 폴백) |
| 4 | F-02 | FastReports/FastReport (.NET OSS) | 4 | 5 | 5 | 3 | 1 | **18** | 참조 (운영 .NET 도입 ❌, 시맨틱만) |
| 5 | D-04 | pyparsing/pyparsing dfmparse.py | 1 | 5 | 5 | 5 | 5 | **21** | 참조 (graceful skip 패턴만) |
| 6 | M-03 | WeasyPrint Issue #718/#75 패턴 | 2 | — | 5 | 5 | 5 | (스코어 N/A — 코드 아닌 가이드) | 참조 (BarcodeObject 임베드 룰) |
| 7 | F-04 | LazReport `lr_class.pas` (LGPL) | **5** | 2 | 3 | 2 | 2 | **14** | 참조 (디버깅 비교 자료만) |
| 8 | M-02 | Kryvich's Delphi Reporter (LGPL) | 2 | 2 | 5 | 2 | 1 | **12** | 참조 (token 문법 1회 비교) |
| 9 | D-05 | lmbelo/python4delphi | 1 | 5 | 5 | 3 | 1 | **15** | 참조 (dev-only 정본 추출) |
| 10 | D-01 | delphi-sucks/DSDfmParser | 1 | (조사 필요) | 2 | 3 | 3 | **~10** | 배제 (DFM 텍스트, `.frf` 무관) |
| 11 | D-02 | Dadie/dfm-toolkit | 1 | (조사 필요) | 2 | 2 | 1 | **~8** | 배제 |
| 12 | D-03 | MHumm/BinaryDFMFinder | 1 | (조사 필요) | 1 | 1 | 1 | **~5** | 배제 |

> **주**: 시드 문서에서 이미 평가된 (a) FastReport master tarball (정본, 본 문서 = F-02 와 동일 코드) /
> (b) Demo `.frx` 자산은 본 점수표에서 *별도 카운트 없이* F-02 + F-03 의 평가에 흡수.

## 2. 심층 리뷰 (4 건)

### 2.1. F-01 — FastReports/FreeReport (BSD-2-Clause, Pascal)

- **본 트랙 가치**: `.frf` 의 **유일한 정본 디시리얼라이저** (`Source/FR_Class.pas` 의
  `LoadFromStream` / `LoadFromFile`). FreeReport 2.3 = `.frf` 1.x ~ 2.x 의 정본.
- **incorporate 방식**: Pascal 코드를 *직접 컴파일/링크 ❌* — 알고리즘을 line-by-line
  으로 Python `frf_decoder.py` 로 포팅 (BSD-2 의 저작권 표시 의무는 헤더 주석으로
  충족). 데이터 구조 (`TfrPage`, `TfrBand`, `TfrView` 계층) 는 IR 스키마 §2 의
  객체 모델 그대로 매핑.
- **위험**: 2026 활성도 낮음 — 그러나 *포맷이 동결됨* 이라 활성도 영향 ≤ low.
- **결론**: **즉시 재사용 / 알고리즘 정본**.

### 2.2. F-03 — FastReports/FastReport.Documentation (MIT)

- **본 트랙 가치**: `.frx` 의 모든 객체/속성 시맨틱을 정리한 **단일 정본 명세서**.
  `.frf` 는 같은 객체 모델의 바이너리 직렬화 형태이므로 IR 스키마는 본 명세서를
  1:1 매핑.
- **incorporate 방식**: 코드 incorporate ❌ — IR 스키마 (`frf_ir_schema.md`) 작성 시
  표 / 정의 / 속성명을 *그대로 reference 인용*. MIT 으로 인용/배포 자유.
- **위험**: 없음 — 문서이며 활발히 갱신.
- **결론**: **즉시 재사용 / 스키마 정본**.

### 2.3. M-01 — lincolnloop/python-qrcode (BSD-3)

- **본 트랙 가치**: `.frf` 의 BarcodeObject (Code39/Code128/EAN/QR 등) 를 IR →
  HTML 컴파일러가 SVG/data-url 로 임베드할 때 **즉시 사용 가능** 한 Python 라이브러리.
- **incorporate 방식**: `requirements.txt` 에 추가. 본 트랙은 1차 PoC 에서 QR 만
  지원, 1D 바코드는 fallback 이미지로 대체 (계획 §리스크 부합).
- **위험**: 1D 바코드는 별도 라이브러리 (`python-barcode`) 필요할 수 있음 — 별도 평가 후
  v1 에서 추가.
- **결론**: **즉시 재사용** (BarcodeObject 폴백).

### 2.4. D-04 — pyparsing/pyparsing examples/dfmparse.py (MIT)

- **본 트랙 가치**: 단일 파일 Python PEG 파서 — `.frf` 자체에는 무용 (텍스트 DFM 만
  지원). 그러나 *`unsupported_objects[]` graceful skip 로직* 의 작은 레퍼런스로 매우 적합.
- **incorporate 방식**: 코드 incorporate ❌ — 패턴 (try/except 후 skip + warning log)
  만 차용.
- **결론**: **참조** (배제 ❌, 즉시 재사용 ❌).

## 3. 3 분류 결정 동결 (Top → Down)

### 3.1. 즉시 재사용 (3 건)

| ID | 후보 | 사용 위치 | incorporate 형태 |
|---|---|---|---|
| F-01 | FreeReport `FR_Class.pas` | `frf_decoder` (R1) | **알고리즘 Python 포팅** + 헤더 주석에 BSD-2 저작권 표시 |
| F-03 | FastReport.Documentation | IR 스키마 (`frf_ir_schema.md`) | **표 / 정의 인용** + MIT 출처 표시 |
| M-01 | python-qrcode | `ir_to_html` (R3) BarcodeObject 폴백 | **`requirements.txt` 의존성 추가** + BSD-3 NOTICE |

### 3.2. 참조 only (5 건)

| ID | 후보 | 참조 목적 | 사용 후 |
|---|---|---|---|
| F-02 | FastReport (.NET OSS) | `.frx` 시맨틱 검증 | 1회 IR 스키마 작성 시 참조 |
| D-04 | pyparsing dfmparse.py | graceful skip 패턴 | `frf_decoder` 의 `unsupported_objects[]` 로직 모방 |
| M-03 | WeasyPrint Issue #718/#75 | BarcodeObject SVG/data-url 패턴 | `ir_to_html` 의 BarcodeObject 임베드 룰 |
| F-04 | LazReport `lr_class.pas` | 디버깅 비교 자료 | "unsupported FRF format" 에러 발생 시 비교 분석 |
| M-02 | Kryvich's Reporter | Delphi-진영 token 문법 | 1회 비교, 본 트랙은 자체 token 문법 정의 |

### 3.3. 배제 (4 건)

| ID | 후보 | 배제 사유 |
|---|---|---|
| D-01 | DSDfmParser | DFM 텍스트만, `.frf` 무관, 활성도 ↓ |
| D-02 | dfm-toolkit | C++/Pascal 의존, OPS = 1 |
| D-03 | BinaryDFMFinder | 위치 찾기 도구, 본 트랙 가치 ❌ |
| D-05 | python4delphi | 운영 .NET/Delphi 의존성 도입, OPS = 1 (단, dev-only 시 *참조* 로 격하 가능) |

## 4. 후속 단계 입력 동결

- **R1 (FRF Decoder PoC)**: 입력 = F-01 (알고리즘) + D-04 (graceful skip 패턴).
- **IR 스키마 동결**: 입력 = F-03 (정본 명세) + F-02 (.frx 검증).
- **R3 (IR → HTML 컴파일러) BarcodeObject 처리**: 입력 = M-01 + M-03.
- **회귀 디버깅 시**: 보조 = F-04 (포맷 차이 비교).

## 5. 변경 이력

| 일자 | 버전 | 변경 |
|---|---|---|
| 2026-04-20 | v0 | 초기 12 건 후보, 3 분류 동결, Top 3 즉시 재사용 확정 |
