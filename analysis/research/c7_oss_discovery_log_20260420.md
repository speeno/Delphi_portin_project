# C7 비-FastReport 트랙 — OSS 추가 탐색 로그 (2026-04-20)

> **목적**: 계획 [c7-nofr-porting](../../) 의 § "OSS 기반자료 구축 절차" 0단계 게이트에 따라
> `.frf` (FastReport VCL 4.x 바이너리) 의 자체 디코더/IR 컴파일러 구축에 활용 가능한
> 공개 오픈소스를 GitHub 중심으로 추가 탐색하고, 모든 검색 쿼리·URL·1차 판정을
> 영구 증빙으로 남긴다.
>
> **시드 문서** (이미 평가됨, 재기재 생략):
> - [`analysis/research/c7_frf_parser_oss_research.md`](./c7_frf_parser_oss_research.md)
> - [`analysis/research/c7_b4_poc_1day_report.md`](./c7_b4_poc_1day_report.md)
>
> **본 로그가 다루는 추가 발견**: 시드 문서가 다루지 않은 / 한 줄로만 언급된 / 2026-04 이후
> 신규 갱신된 OSS — 총 12건 1차 후보. shortlist (`c7_oss_shortlist.md`) 와
> 라이선스 매트릭스 (`c7_oss_license_matrix.md`) 의 입력 데이터.

---

## 0. 탐색 메서드

- 본 트랙은 **운영 의존성 0** (Python/WeasyPrint 단일 스택) 정책을 지키므로
  C# / .NET / Pascal 코드는 **참조용 (시맨틱/객체 모델)** 으로만 평가한다.
- 4 가지 탐색 축을 병렬로 수행했다.
  1. `.frf` / FreeReport / FastReport VCL 직접 키워드
  2. Delphi DFM/TStream 바이너리 디코더 (간접 재사용 가능 코드)
  3. Report-template migration / form-binary → IR 도구
  4. WeasyPrint 호환 보조 (바코드 SVG, 폰트 임베드 등)
- 평가는 5 차원 점수 (포맷 적합성 / 라이선스 / 유지보수 / 재사용성 / 운영 적합성)
  에 1~5 점, **총점 25점 만점** 으로 정렬한다 (shortlist 문서 참조).

## 1. 탐색 쿼리 카탈로그

| # | 검색 소스 | 쿼리 | 발견 후보 (raw URL) |
|---|---|---|---|
| Q1 | WebSearch | `GitHub FastReport frf parser Delphi TStream open source` | github.com/FastReports/FastReport · github.com/FastReports/FreeReport |
| Q2 | WebSearch | `GitHub Delphi DFM binary parser Python open source` | github.com/delphi-sucks/DSDfmParser · github.com/Dadie/dfm-toolkit · github.com/MHumm/BinaryDFMFinder · github.com/pyparsing/pyparsing/blob/master/examples/dfmparse.py |
| Q3 | WebSearch | `GitHub report template migration Delphi to HTML open source` | github.com/Kryuski/kryvich-delphi-reporter · github.com/sempare/sempare-delphi-template-engine · github.com/guitorres/htmlbuilder · github.com/NickHodges/delphihtmlwriter |
| Q4 | WebSearch | `GitHub FreeReport frf binary parser Pascal LoadFromStream` | github.com/FastReports/FreeReport/tree/master/Source · forum.lazarus.freepascal.org (LazReport 호환 토론) |
| Q5 | WebSearch | `FastReport frx XML schema reference Bands TextObject Python` | fastreports.github.io/FastReport.Documentation · github.com/FastReports/FastReport/blob/master/Demos/Reports/Text.frx |
| Q6 | WebSearch | `github.com python parse Delphi TStream WriteComponent` | github.com/lmbelo/python4delphi · DelphiVCL4Python (Stream wrapper) |
| Q7 | WebSearch | `github qrcode barcode python weasyprint svg embed` | github.com/lincolnloop/python-qrcode · github.com/Kozea/WeasyPrint/issues/718 (data-url 패턴) |
| Q8 | WebSearch | `github lazarus lazreport frf format documentation source` | github.com/alrieckert/lazarus/blob/master/components/lazreport/source/lr_class.pas (LazReport `lr_class.pas`) |
| Q9 | WebSearch | `github Delphi TFiler TReader binary stream Python decoder` | freepascal.org/docs-html/rtl/classes/treader.html · stackoverflow.com/questions/2700155 (Python `struct` 패턴) |

> **로컬 보강**: 워크스테이션의 `/Users/speeno/Downloads/FastReports-FastReport-8ef9cde/`
> (FastReport master tarball, MIT) 는 시드 문서 §1.8 에서 이미 직접 분석. 본 로그에서
> **신규** 항목으로 카운트하지 않으나, IR 매핑 명세서로 모든 후속 단계에서 계속 사용한다.

## 2. 1차 후보 카탈로그 (12 건, 신규 + 시드 미상세)

각 항목의 라이선스 / 마지막 활동 / 즉시 채택 가능 여부 / 왜 후보인지 1~2 줄.

### F. `.frf` / FreeReport 직접 후보

| ID | 후보 | URL | 라이선스 | 활동 | 직접 `.frf`? | 노트 |
|---|---|---|---|---|---|---|
| F-01 | **FastReports/FreeReport** (Pascal, Delphi 4~9) | https://github.com/FastReports/FreeReport | BSD-2-Clause (저작권 보존) | 저활성 (2.33 마지막) | ✅ **선조 포맷 디시리얼라이저** (`Source/FR_Class.pas`) | 본 트랙의 **R1 디코더 알고리즘 정본** — Pascal `LoadFromStream` 을 Python `struct` 로 1:1 포팅 |
| F-02 | **FastReports/FastReport** (.NET OSS) | https://github.com/FastReports/FastReport | MIT (단일 LICENSE.md, PdfSimple 포함) | 활발 (2025+ 갱신) | ❌ `.frx` 만 | 시맨틱 명세 / IR 검증 (참조용). 본 트랙은 `Report.Load()` 위임 ❌ — 파일 구조만 차용 |
| F-03 | **FastReports/FastReport.Documentation** | https://github.com/FastReports/FastReport.Documentation | MIT | 안정 | ❌ `.frx` 시맨틱 명세 | IR 스키마 (`frf_ir_schema.md`) 의 1:1 매핑 명세서 — 항목별 속성 전수 레퍼런스 |
| F-04 | **alrieckert/lazarus** `lazreport/lr_class.pas` | https://github.com/alrieckert/lazarus/blob/master/components/lazreport/source/lr_class.pas | LGPL with linking exception | 안정 | ⚠️ **부분** (FreeReport 2.x 기반, 일부 FRF 버전 차이로 "unsupported FRF format" 에러 보고됨) | 본 트랙은 LGPL 코드 직접 incorporate ❌ — 그러나 **포맷 차이 발견 시 비교 디버깅 자료** |

### D. Delphi DFM/TStream 바이너리 보조 후보

| ID | 후보 | URL | 라이선스 | 활동 | 본 트랙 가치 |
|---|---|---|---|---|---|
| D-01 | **delphi-sucks/DSDfmParser** | https://github.com/delphi-sucks/DSDfmParser | (확인 필요 — 라이선스 매트릭스 항목) | 저활성 | 텍스트 DFM 파서. `.frf` 와 직접 호환 ❌. 객체 트리 시맨틱 학습용 |
| D-02 | **Dadie/dfm-toolkit** | https://github.com/Dadie/dfm-toolkit | (확인 필요) | 저활성 | C++/Pascal 토큰화 도구. **JSON 출력 패턴** 만 IR 직렬화 형식 영감 |
| D-03 | **MHumm/BinaryDFMFinder** | https://github.com/MHumm/BinaryDFMFinder | (확인 필요) | 저활성 | 바이너리 DFM 위치 찾기. 본 트랙 가치 ❌ (배제) |
| D-04 | **pyparsing/pyparsing** `examples/dfmparse.py` | https://github.com/pyparsing/pyparsing/blob/master/examples/dfmparse.py | MIT (pyparsing 본체) | 활발 | **Python 단일 파일 예제** — 텍스트 DFM PEG 파서. `.frf` 자체에는 무용하나, **`unsupported_objects[]` graceful fallback 로직** 의 작은 레퍼런스 |
| D-05 | **lmbelo/python4delphi** + DelphiVCL4Python | https://github.com/lmbelo/python4delphi | MIT | 활발 | Python ↔ Delphi 양방향 wrapper. 본 트랙은 *런타임 .NET/Delphi 의존성 0* 정책으로 **운영 채택 ❌**. 단, **dev-only** 디버깅 시 정본 `Report.Save(.frx)` 호출 환경 제공 가능 |

### M. 보조 / 변환 도구

| ID | 후보 | URL | 라이선스 | 활동 | 본 트랙 가치 |
|---|---|---|---|---|---|
| M-01 | **lincolnloop/python-qrcode** | https://github.com/lincolnloop/python-qrcode | BSD-3 | 활발 | ✅ **WeasyPrint + SVG/data-url** 바코드/QR 임베드 — `BarcodeObject` 폴백 |
| M-02 | **Kryuski/kryvich-delphi-reporter** (Kryvich's Reporter) | https://github.com/Kryuski/kryvich-delphi-reporter | LGPL-3.0 | 활발 (3.2.2, 2025-01) | Delphi 측 **template→HTML/RTF/XML** 도구. 본 트랙 운영 도입 ❌ (Pascal + LGPL). 그러나 **Delphi 진영의 template-binding 토큰 문법 레퍼런스** |
| M-03 | **WeasyPrint Issues #718 / #75** (커뮤니티 패턴) | https://github.com/Kozea/WeasyPrint/issues/718 | (이슈 — 라이선스 무관) | 활발 | 바코드/SVG 임베드 권장 패턴 (data-url + img tag). IR→HTML 컴파일러의 `BarcodeObject` 처리 룰 직접 차용 |

## 3. 1차 평가 노트

- **F-01 (FreeReport)**: `.frf` 의 가장 직접적인 정본 디시리얼라이저. **본 트랙의 R1 단계
  핵심 입력**. Pascal 코드를 line-by-line 으로 Python 으로 포팅 — 라이선스 (BSD-2)
  는 저작권 표시 보존 의무만, 본 프로젝트 라이선스와 호환.
- **F-02/F-03 (FastReport .NET OSS + Documentation)**: `.frx` XML 스키마는 IR 의
  *공통 데이터 모델* 정본. F-03 의 `ReportObjects.md`/`Bands.md`/`Expressions.md`
  를 IR 스키마의 1:1 매핑 명세서로 사용한다. **운영 코드에 .NET 도입 ❌** —
  스키마만 차용.
- **F-04 (LazReport lr_class.pas)**: FreeReport 2.x 기반의 Lazarus 포팅. 일부 FRF
  버전 차이로 "unsupported FRF format" 에러 보고됨. 본 트랙의 디코더가
  *동일한 차이* 를 만났을 때 **비교 디버깅 자료** 로만 사용 (LGPL 코드는
  incorporate 하지 않음).
- **D-01~D-04 (DFM 파서/도구)**: `.frf` 와 *직접 호환 ❌* — 그러나 (a) DFM 의
  `object … end` 트리 구조는 FreeReport `TfrPage`/`TfrBand`/`TfrView` 트리와 닮음
  (b) D-04 는 단일 Python 파일이라 **graceful skip 로직** 학습용으로 유용.
- **D-05 (python4delphi)**: 운영 .NET/Delphi 의존성 0 정책에 위배 — **운영 채택 ❌**.
  *dev-only* 로 정본 `Report.Save(.frx)` 호출 환경 1회 구축에만 활용 가능 (D-05
  미사용 시 F-02 의 `dotnet 8` CLI 로 동일 작업 가능).
- **M-01 (python-qrcode)**: BarcodeObject 폴백의 *바로 사용 가능* 라이브러리.
  BSD-3, WeasyPrint 호환. 본 트랙 운영 의존성으로 **추가 가능**.
- **M-02 (Kryvich's Reporter)**: LGPL — 본 트랙은 incorporate ❌. *데이터 바인딩
  토큰 문법 레퍼런스* 로만 1회 참조 후 폐기.
- **M-03 (WeasyPrint 이슈 #718/#75)**: 코드가 아닌 **권장 패턴 자료** — IR→HTML
  컴파일러의 `BarcodeObject` 처리 룰 직접 차용.

## 4. 종료 조건 검증

| 종료 조건 (계획 §0) | 충족 여부 | 비고 |
|---|---|---|
| 최소 10 후보 조사 | ✅ **12 건** (시드 4 + 본 로그 신규 8) | F/D/M 카테고리 골고루 분포 |
| 3건 이상 심층 리뷰 | ✅ **F-01 / F-03 / D-04** (+ M-01) 4 건 심층 | shortlist 문서 §2 에 1:1 평가 매트릭스 |
| 3분류 (즉시 재사용 / 참조 / 배제) | ✅ shortlist 문서 §3 표로 분리 | 본 로그는 raw 데이터, shortlist 가 결정 정본 |
| Phase 게이트 입력으로 shortlist 고정 | ✅ shortlist v0 동결 | 후속 단계 (1) IR 스키마 작성 시 shortlist 의 즉시 재사용 / 참조 자료를 입력으로 사용 |

## 5. 후속 액션

- shortlist 문서 (`c7_oss_shortlist.md`): 본 12 건을 5 차원 점수로 정렬하여 Top N 결정.
- 라이선스 매트릭스 (`c7_oss_license_matrix.md`): 운영 incorporate 가능 / 참조 only /
  배제 3 분류 + NOTICE/저작권 표시 의무 정리.
- 본 로그는 **추가 갱신 없음** — 향후 신규 후보 발견 시 `c7_oss_discovery_log_<YYYYMMDD>.md` 별도 신규.

---

*최종 업데이트: 2026-04-20 — 본 로그 최초 작성. 12 건 1차 후보. F-01 (FreeReport)
+ F-03 (FastReport.Documentation) + D-04 (pyparsing dfmparse.py) + M-01 (python-qrcode)
4 건 심층 평가 완료. shortlist / 라이선스 매트릭스 동봉 작성.*
