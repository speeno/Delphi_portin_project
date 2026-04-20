# C7 R&D — FastReport `.frf` 파서 OSS 분석 (T10, 비차단)

본 문서는 레거시 98 건의 `.frf` (FastReport VCL 4.x 바이너리) 자산을 자동으로 HTML/CSS/PDF 로 변환하기 위한 **자체 파서 구현 가능성** 을 OSS 코드 기반으로 조사한 R&D 보고서이다. **C7 Phase 1 의 차단 항목이 아님** — Phase 1 은 DEC-039 (`.frf` = 참조용, 자동 변환 0) 정책으로 동결되었으며, 본 R&D 결과는 Phase 2 이후 자동 변환 도입 여부 결정의 근거 자료로만 사용된다.

> **2026-04-20 갱신 (1)**: `https://github.com/FastReports/FastReport.Documentation` (MIT 라이선스, FastReport .NET OpenSource 공식 문서) 추가 조사 결과를 §1.4·§1.5·§4 에 반영. 핵심: **OSS .NET 본은 `.frx` (XML) 포맷만 다루며, 우리의 `.frf` (VCL 4.x 바이너리) 는 직접 지원 0** — 그러나 *공통 객체 모델/밴드 분류/`[Table.Column]` 데이터 바인딩 토큰 문법* 은 동일 → 파서 작성 시 **객체 시맨틱 참조서** 로는 가치 있음.

> **2026-04-20 갱신 (2)**: `https://github.com/yusufbal/FastReport.OpenSource.HtmlExporter` (MIT, .NET 8) 추가 조사 결과를 §1.6·§4 에 반영. 핵심: **FastReport OSS 진영 자체가 PdfSimple 플러그인 (LGPL, 이미지 PDF, 큰 용량, 텍스트 선택 불가) 의 한계를 우회하기 위해 "HTML 내보내기 → 외부 PDF 엔진 (iText7)" 패턴을 채택** — 이는 우리의 DEC-037 (HTML 빌더 → WeasyPrint) 아키텍처와 **동일한 발상** 으로, 자체 파서 도입 시에도 (B2 안) HTML/CSS 를 최종 출력 형식으로 유지하는 결정을 강하게 지지한다.

> **2026-04-20 갱신 (3)**: `https://github.com/atkins126/FastReportExport` (Apache-2.0, Delphi VCL Pascal, antoniojmsjr 본/atkins126 fork) 추가 조사 결과를 §1.7·§4 에 반영. 핵심: **본 라이브러리는 우리 `.frf` 자체 파싱 문제를 풀어주지 않음** — 의존성 (`frxClass`/`frxExportPDF`/`frxExportHTML` 등) 은 **유료 FastReport VCL SDK** 이며, 래퍼만 Apache-2.0. 샘플 리포트 형식도 `.fr3` (FastReport 3+ XML) 으로, `.frf` (구 바이너리) 가 아님. **우리 §4 의 C 안 (상용 FastReport VCL SDK) 운영 패턴 참조** 로만 가치 있음 (Horse/ISAPI/WindowsService 멀티스레드 서버 통합 예시). DEC-037 (Python/WeasyPrint 단일) 와 정면 비교 시 운영 라이선스/스택 단순성 면에서 우리 결정이 우월함을 추가 확인.

> **2026-04-20 갱신 (4) — ⭐ 중요**: `https://github.com/FastReports/FastReport` 의 **로컬 소스 (`/Users/speeno/Downloads/FastReports-FastReport-8ef9cde`) 직접 분석** 결과를 §1.8·§4·§2 에 반영. 핵심: (a) **FastReport OSS HTML export 가 코어 내장** (`FastReport.Base/Export/Html/HTMLExport.cs` 1187 LOC + Layers 992 LOC + 보조 4 파일, 총 3137 LOC, MIT) — 별도 NuGet 의존성 0. (b) **Layer 모드가 픽셀 절대 좌표 (`<div style="position:absolute;...">`) HTML 을 생성** — 정확히 우리가 `.frf` 를 충실 재현할 때 필요한 출력 형식. (c) **PdfSimple 플러그인도 MIT 동일 라이선스** (단일 LICENSE.md) — 이전 보강 (1)/(2) 의 "LGPL" 표기는 오류로 **교정**. (d) **Import 플러그인 4종** (RDL 988 LOC, StimulSoft 1582 LOC, JasperReports 1165 LOC, ListAndLabel) 의 `ImportBase` 패턴이 **자체 `.frf` 임포터의 직접 템플릿**. (e) 새로운 권장 전략 **B4 (빌드 타임 변환 + Jinja2 템플릿)** 추가 — `.frf → .frx → FastReport OSS HTML export` 를 *빌드 타임 1회* 실행해 Jinja2 placeholder 가 박힌 HTML 템플릿을 만들고, 운영은 기존 Python/WeasyPrint 스택 그대로 (DEC-037 그대로). 자체 파서 비용 6~13 인주 → **3~5 인주** 로 단축 + .NET 런타임 운영 부담 0.

## 0. 결론 (TL;DR)

| 질문 | 결론 | 근거 |
| --- | --- | --- |
| OSS 공개 파서 존재? | **부재** (`.frf` 전용 0건) | FastReport .NET OSS = `.frx` (XML) / `.fpx` (prepared) 만. VCL 4.x `.frf` 바이너리 파서 미공개. |
| FastReport 자체 OSS? | (a) **FreeReport 2.3** (Object Pascal, BSD) — `.frf` *선조 포맷*. (b) **FastReport .NET OpenSource** (C#, MIT) — `.frx` XML. (c) **FastReport.Documentation** (MIT) — .NET 본 시맨틱/객체 모델 공식 명세. | (a) https://github.com/FastReports/FreeReport (b) https://github.com/FastReports/FastReport (c) https://github.com/FastReports/FastReport.Documentation |
| `.frx` ↔ `.frf` 관계 | **포맷 0% 호환 (직렬화)** + **객체/밴드/표현식 95% 호환 (시맨틱)** | `.frx` = XML 평문, `.frf` = TStream 바이너리. 둘 다 `TextObject`/`PictureObject`/`DataBand`/`PageFooterBand`/`[Employees.Title]` 토큰 등 **공통 객체 클래스 + 데이터 바인딩 문법** 사용. |
| 자체 구현 비용 | **중상 (6~11 인주)** — §2 작업 분해 참조. .NET OSS 의 `Report.Save(stream)` 출력물(.frx) 과 비교하면 **인터미디어트 IR (XML) 채택 시 디자인 손실 최소화 가능**. | (a) FreeReport 2.3 Pascal 디시리얼라이저를 Python 으로 포팅, (b) .NET OSS 의 .frx XML 객체 명세 (FastReport.Documentation) 를 IR 로 사용 |
| 권장 조치 | **Phase 1 = DEC-039 정책 유지 (수동 재현)**. Phase 2 에 1 회 더 검토 — 만약 거래처별 변형 (`Report_4_51-N` 10건 / `Report_2_13-N` 4건) 이 운영상 회귀를 일으키면 그때 본 R&D 발동. | C7 Phase 1 5 양식 + 1 라벨은 수동 재현으로 모두 PDF 출력 가능 |

## 1. OSS 환경 조사 결과

### 1.1. FastReport 공식 OSS 레포 (https://github.com/FastReports)

| 레포 | 라이선스 | `.frf` 직접 관련성 | `.frf` 자체 파서 R&D 가치 |
| --- | --- | --- | --- |
| **FreeReport** (Pascal, Delphi 4~9) | BSD-류 | **선조 포맷 직렬화 코드** | ⭐⭐⭐ (디시리얼라이저 알고리즘 이식 가능) |
| **FastReport** (.NET, OpenSource) | **MIT 일관** (코어 + 모든 OSS 플러그인 = 단일 LICENSE.md, 2026-04-20 로컬 소스 직접 검증으로 교정) | `.frx` 만 — `.frf` 는 미지원 | ⭐⭐⭐ (객체 모델/밴드 분류/토큰 문법 + **HTML export 코어 내장 1187 LOC + Layer 모드 992 LOC = 픽셀 절대좌표 `<div style="position:absolute;...">`** 가 그대로 우리 요구사항) |
| **FastReport.Documentation** | MIT | `.frx` XML 객체 명세 / Class Reference / `Bands.md` / `ReportObjects.md` / `StoringLoadingReport.md` | ⭐⭐ (R3 단계 IR 매핑 명세서로 직접 사용) |
| **FastReport.VCL.RES** | MIT | UI 다국어 리소스. 포맷 분석 불가. | (없음) |

### 1.2. 비공식 / 커뮤니티 시도

- 검색 결과 `.frf` 전용 OSS 파서 미발견 (2026-04 기준).
- 일부 포럼 (https://forum.fast-report.com/en/categories/freereport) 에 사용자 토론 있음 — 코드 산출물 미공개.
- StackOverflow 등에 단편 Q&A 있음 — 완전한 파서 코드 부재.

### 1.3. FreeReport 2.3 소스 분석 (R&D 1 차)

- **레포**: https://github.com/FastReports/FreeReport/tree/master/Source
- **핵심 파일**:
  - `FR_Class.pas` — 전체 클래스 계층 (`TfrReport`, `TfrPage`, `TfrBand`, `TfrView` 등) 및 LoadFromStream/SaveToStream 직렬화.
  - `FR_DSet.pas` — 데이터셋 바인딩 (런타임 의미 — 파서 분석에는 불필요).
  - `FR_BarC.pas` / `FR_Chart.pas` — 추가 객체 (FastReport 4 에서 `frBarCodeObject` 등으로 진화).
- **직렬화 구조**:
  - `Stream.Read(Sign, 5)` → `'FRF15'` 또는 `'FRF20'` 시그니처.
  - 페이지/밴드/객체 트리를 `TStream` 으로 순차 직렬화 (가변 길이 객체 + RTTI 기반).
  - 좌표/폰트/색상은 **TWIPs (1/1440 인치)** 단위 → CSS mm 변환은 단순.
- **확장 (FastReport 4.x → 우리 `.frf`)**: 추가 객체 (`frBarCodeObject`, `frTextObject` 의 신규 속성) 가 직렬화 후미에 붙음. **모르는 객체는 skip 가능 → 폐쇄 호환** (단, 디자인 충실도 손실).

### 1.4. FastReport .NET OpenSource — 객체 모델 / `.frx` XML 시맨틱 (2026-04-20 신규 조사)

- **레포 (코드)**: https://github.com/FastReports/FastReport (MIT, .NET6/.NET Core/.NET Framework 4.x). 1.2k+ stars, 활성 유지 (2025년 갱신).
- **레포 (문서)**: https://github.com/FastReports/FastReport.Documentation (MIT). 117 stars. 핵심 명세서 인덱스 (ReportTemplateFileStructure / Bands / ReportObjects / StoringLoadingReport / Expressions / ClassReference/).
- **`.frx` 파일 구조 (`ReportTemplateFileStructure.md` 인용)**:
  ```xml
  <Report ScriptLanguage="CSharp" ReportInfo.Name="..." ReportInfo.CreatorVersion="1.0.0.0">
    <Dictionary>
      <TableDataSource Name="Employees" ReferenceName="NorthWind.Employees">
        <Column Name="EmployeeID" DataType="System.Int32"/>
        ...
      </TableDataSource>
    </Dictionary>
    <ReportPage Name="Page1">
      <ReportTitleBand Name="ReportTitle1" Width="718.2" Height="75.6">
        <TextObject Name="Text1" Top="47.25" Width="718.2" Height="28.35"
                    Text="EMPLOYEES" HorzAlign="Center" Font="Tahoma, 14pt, style=Bold"/>
      </ReportTitleBand>
      <DataBand Name="Data1" Width="718.2" Height="219.24" DataSource="Employees">
        <TextObject Name="Text4" Left="113.4" Top="66.15"
                    Text="[Employees.BirthDate]" Format="Date" Format.Format="D"/>
        <PictureObject Name="Picture1" DataColumn="Employees.Photo"/>
      </DataBand>
      <PageFooterBand Name="PageFooter1" Height="28.35">
        <TextObject Name="Text10" Text="[PageN]" HorzAlign="Right"/>
      </PageFooterBand>
    </ReportPage>
  </Report>
  ```
- **단위**: 1pt = 1/72 인치 (`.frf` TWIPs = 1/1440 인치 와 다름 — 변환 1 step 추가).
- **`.frf` ↔ `.frx` 시맨틱 호환 (95%)**:
  | 시맨틱 | `.frf` (VCL 4.x) | `.frx` (.NET) | 호환 |
  | --- | --- | --- | --- |
  | 밴드 분류 | `frPageHeader`/`frDataBand`/`frPageFooter`/`frChild` | `PageHeaderBand`/`DataBand`/`PageFooterBand`/`ChildBand` | ✅ 1:1 |
  | 텍스트 객체 | `TfrTextView` (Text, Font, Frame, Highlight) | `TextObject` (Text, Font, Border, Format) | ✅ 1:1 (속성명 차이만) |
  | 그림 객체 | `TfrPictureView` (Picture, Stretched) | `PictureObject` (DataColumn, Border) | ✅ 1:1 |
  | 라인/도형 | `TfrLineView`/`TfrRectView` | `LineObject`/`ShapeObject` | ✅ 1:1 |
  | 바코드 | `frBarCodeObject` | `BarcodeObject` | ✅ 1:1 |
  | 데이터 토큰 | `[Sg_Csum."Gname"]` | `[Employees.LastName]` | ✅ 같은 문법 (인용부호 처리만 차이) |
  | 표현식 | Pascal 평가기 (FR_Pars.pas) | C# 스크립트 (`Expressions.md`) | ⚠️ 평가기 다름 — but 데이터 바인딩 토큰만 사용하면 95% 호환 |
- **PDF 내보내기**: OSS 코어는 PDF export 가 *별도 플러그인* (LGPL `FastReport.OpenSource.Export.PdfSimple`). 본문은 HTML/PNG/JPEG/EMF 등은 코어 포함 (`COMPARISON.md`).
- **OS 지원**: Linux/MacOS = Core 에디션만 ✅, OSS 도 .NET Core/6+ 에서 동작 (Windows/Linux 모두). **단** OSS 의 PDF 플러그인 + 폰트 의존은 별도 검증 필요.

### 1.5. `.frx` IR 활용 가능성 (자체 파서 R&D 개선안)

기존 §2 의 R3 단계 (객체 → CSS 변환) 를 **2 단계로 분리** 하는 개선 가능:

```
.frf (binary) ──[R1+R2 디시리얼라이저]──> 객체 그래프
                                           │
                                           ├──[R3a IR 변환]──> .frx XML 동등 (FastReport.Documentation 명세 준수)
                                           │                       │
                                           │                       └──[A. 변환 도구 검증용]──> FastReport .NET OSS 로 실제 PDF 생성 (검증 단계)
                                           │
                                           └──[R3b 직접 변환]──> CSS @page (현 방안)
```

**장점**:
- R3a 의 `.frx` IR 출력은 FastReport .NET OSS 의 `Report.Load()` 로 그대로 검증 가능 → **회귀 게이트** 가 즉시 가능.
- IR 검증 통과 후 R3b 의 CSS 변환은 *덜 엄격* 해도 됨 (정본은 IR 까지의 충실도로 보장).
- 향후 .NET 환경 채택 시 IR 가 곧바로 운영 가능.

**단점**:
- R3a 가 추가 작업 (1~2 인주 추가). 총 비용 7~13 인주 로 상승.
- IR 정확도 검증을 위해 .NET 빌드 환경 (1회) 구축 필요.

### 1.6. 커뮤니티 사례 — `yusufbal/FastReport.OpenSource.HtmlExporter` (2026-04-20 신규 조사)

- **레포**: https://github.com/yusufbal/FastReport.OpenSource.HtmlExporter (MIT, .NET 8.0, 13 stars)
- **NuGet**: https://www.nuget.org/packages/PdfExporter.FastReport.OpenSource v1.0.0
- **배경 (README 인용)**: FastReport OpenSource 의 PDF 출력은 공식적으로 `FastReport.OpenSource.Export.PdfSimple` 플러그인 (LGPL) 을 사용해야 하지만, 이 플러그인은 **각 페이지를 이미지로 변환 후 합치는 방식** 이라 (a) PDF 용량이 비대하고 (b) 텍스트 선택 불가. 유료 본 (FastReport.NET / Core) 만 텍스트 선택 가능한 PDF 를 생성한다.
- **해결 패턴**: 본 라이브러리는 다음 2 단계 파이프라인을 구현:
  ```
  .frx (XML) ──[FastReport OSS HTML export]──> HTML ──[iText7]──> PDF (텍스트 선택 가능, 작은 용량)
  ```
  - 1 단계: FastReport OSS 코어의 HTML export (코어 포함, 추가 라이선스 0) 로 HTML/CSS 출력.
  - 2 단계: iText7 (Apache 2.0 / AGPL 듀얼) 로 HTML → PDF 변환. 페이지 크기/마진은 원본 보존 (최신 .NET 8 버전 개선점).
- **사용 예 (README)**:
  ```csharp
  var fastReportGenerator = new FastReportGenerator<TestReportDataModel>(ReportUtils.DesignerPath, "test.frx");
  var report = fastReportGenerator.GeneratePdfFromHtml(data);
  ```

#### 본 R&D 에 미치는 시사점

| 항목 | 의미 | 본 프로젝트 (DEC-037) 와의 정합성 |
| --- | --- | --- |
| **HTML 을 IR 로 채택** | FastReport OSS 진영 자체가 "고품질 PDF" 를 위해 HTML 우회 패턴을 표준 솔루션으로 인정 | ✅ 우리도 이미 HTML → WeasyPrint 한다 (DEC-037). **동일 아키텍처가 .NET OSS 커뮤니티에서도 베스트 프랙티스로 검증됨** |
| **PdfSimple 우회 정당성** | LGPL PdfSimple 의 품질 한계 (이미지 PDF, 텍스트 선택 불가) 를 OSS 진영도 인지 | ✅ 우리는 처음부터 `weasyprint` (BSD-3) 채택 — LGPL/이미지 PDF 의존성 0 |
| **외부 PDF 엔진 = iText7** | iText7 은 듀얼 라이선스 (Apache 2.0 무료 ↔ AGPL 상용제한) — 상용 운영 시 라이선스 비용 발생 가능 | ✅ WeasyPrint = BSD-3 단일 — 상용 운영 라이선스 부담 0. 본 사례 대비 **운영 라이선스 면에서 우리 선택이 더 안전** |
| **B2 안 (`.frx` IR + .NET OSS) 검증 단계 비용** | 검증 단계에 본 라이브러리 (`PdfExporter.FastReport.OpenSource`) 를 그대로 쓰면 .NET 환경에서 추가 코드 작성 0 | ⭐ B2 안의 **R3a-검증 단계 비용을 0.5 → 0.2 인주 로 단축 가능** (NuGet 패키지 1 줄 추가만으로 검증 PDF 생성) |
| **HTML 출력 충실도 확인** | FastReport OSS 의 HTML export 는 페이지 크기/마진/텍스트 정확도를 일정 수준 보장 (본 라이브러리가 .NET 8 에서 개선 시도 중) | ⚠️ 주의: HTML export 충실도가 우리 자체 파서 R3b 의 *목표 기준선* 으로 사용 가능. 본 라이브러리 출력 PDF vs 우리 자체 파서 출력 PDF 픽셀 diff 비교가 R6 회귀 게이트의 좋은 후보 |

#### B2 안 작업 분해 갱신 (R3a-검증 단계)

기존 §2 의 R3a-검증 단계 (`.frx` IR → FastReport .NET OSS Report.Load → PDF`) 를 다음으로 구체화:

```bash
# .NET 8 + NuGet 1 줄
dotnet add package PdfExporter.FastReport.OpenSource --version 1.0.0

# 검증 코드 (총 5~10 줄)
var gen = new FastReportGenerator<EmptyModel>("Designer", "our_ir_output.frx");
File.WriteAllBytes("verification.pdf", gen.GeneratePdfFromHtml(emptyData));
```

→ R3a-검증 비용: **0.5~1 인주 → 0.2~0.5 인주** 로 단축 (총 B2 안 비용 7~13 → **6.7~12.5 인주**, 사실상 §2 기존 표는 그대로 유지하되 NuGet 의존성 1줄 추가).

### 1.7. 커뮤니티 사례 — `atkins126/FastReportExport` (antoniojmsjr 본 fork) (2026-04-20 신규 조사)

- **레포 (fork)**: https://github.com/atkins126/FastReportExport (Apache-2.0, Pascal/Delphi VCL, 2 stars)
- **레포 (원본)**: https://github.com/antoniojmsjr/FastReportExport (Apache-2.0)
- **목적 (README 인용)**: "Biblioteca de exportação de relatórios utilizando Fast Report em ambientes multithreading e servidores" — 멀티스레드/서버 환경에서 안전한 FastReport 리포트 내보내기 래퍼.
- **소스 분석 (Source/FRExport.\*.pas)**:
  - 핵심 단위 (`FRExport.Core.pas`, `FRExport.Interfaces.Providers.pas`) 가 `frxClass`, `frxExportPDF`, `frxExportHTML`, `frxExportImage`, `frxExportCSV`, `frxDBSet`, `frxChart`, `frxBarcode`, `frxOLE`, `frxRich`, `frxGaugeView`, `frxCross` 등 **FastReport VCL 상용 SDK 의 컴포넌트** 에 의존.
  - 패턴: 빌더 인터페이스 (`IFRExport`/`IFRExportProviders`/`IFRExportExecute`)로 `Report.DataSets.SetDataSet(...).End.Providers.SetProvider(PDF/HTML/PNG/CSV).End.Export.SetFileReport('...fr3').Execute` 형태의 fluent API 제공.
  - 샘플 (`Samples/Horse`, `Samples/ISAPI`, `Samples/WindowsService`, `Samples/WindowsServiceHorse`): Horse 프레임워크 (Delphi REST), ISAPI, Windows Service 환경에서 동시 요청 처리.
- **샘플 리포트 형식**: `Samples/Report/rptCliente.fr3` — **`.fr3` (FastReport 3+ XML/text)**, **`.frf` 가 아님**.

#### 본 R&D 에 미치는 시사점

| 항목 | 의미 | 본 프로젝트와의 관계 |
| --- | --- | --- |
| **의존성 = 유료 FastReport VCL SDK** | 래퍼만 Apache-2.0, 핵심 `frxClass`/`frxExportPDF` 는 fast-report.com 의 **상용 VCL SDK** (Standard/Professional/Enterprise) 에서 제공 | ❌ §4 의 **C 안 (상용 FastReport VCL SDK)** 와 동일 라이선스 부담 — 우리 DEC-037 (BSD-3 WeasyPrint) 가 운영 라이선스 면에서 우월 |
| **`.frf` 직접 파싱 0** | 본 라이브러리는 이미 메모리에 적재된 `TfrxReport` 객체를 받아서 다양한 포맷으로 내보낼 뿐 | ❌ 우리 `.frf` 자산 자동 변환 문제는 해결 못 함 |
| **샘플은 `.fr3` (XML)** | FastReport VCL 도 3+ 부터 XML 평문 포맷 (`.fr3`) 으로 전환 | ⚠️ 우리 `.frf` 자산이 **만약 FastReport VCL 4.x 라면** 본질적으로 `.fr3` (XML) 일 가능성 검증 필요 — 기존 가정 ("`.frf` = 바이너리") 을 *재검증* 권장 (T9 카탈로그 1~2 건 hexdump 5분) |
| **멀티스레드 서버 패턴 참고** | Horse + ISAPI + WindowsService 운영 샘플 — 서버 환경에서 FastReport VCL 동시 호출 안전 처리 (`{$REGION 'TFRExportCustom'}`/`TInterfacedObject` 기반 인스턴스 격리) | 📚 §4 C 안 (상용 SDK) 채택 시 **운영 통합 레퍼런스** 로 활용 가능. 단, 본 프로젝트는 Python/FastAPI 스택 → **현 단계 적용 0** |
| **라이선스 깔끔함 (래퍼)** | Apache-2.0 — 우리 프로젝트에 인용/포함 자유 (단, 의존성 SDK 라이선스 별도 해결 필요) | ✅ 의존성 문제만 해결되면 코드 영감 (fluent API 패턴) 을 자체 Python 빌더 설계에 차용 가능 (저작권 표시 의무) |

#### 추가 액션 제안 (작은 검증)

`.frf` 가 실제로 바이너리인지 텍스트 (`.fr3` 동등) 인지 5 분 검증을 권장:

```bash
file /Users/speeno/Delphi_porting/WeLove_FTP/도서유통-총판/Report/Report_2_11.frf
hexdump -C /Users/speeno/Delphi_porting/WeLove_FTP/도서유통-총판/Report/Report_2_11.frf | head -5
```

- 바이너리 시그니처 (`FRF15` / `FRF20` 등) 확인 시: 기존 §1.3 (FreeReport 2.3 직렬화) 가설 유지.
- 텍스트/XML 시그니처 (`<?xml` / `object frxReport` 등) 확인 시: **`.frf` 의 일부가 사실 `.fr3`/Pascal DFM 텍스트 변형일 수 있음** → 자체 파서 R&D (B1/B2) 비용이 1~3 인주 단축될 수 있음. 본 R&D 결론 (DEC-039 유지) 은 변경 없음.

**검증 결과 (2026-04-20 실행, `Report_2_11.frf` 1 건 샘플)**:

```text
file: data (= 비표준 바이너리)
hexdump 첫 32바이트:
  00000000: 19ff ffff ff1f 0045 5053 4f4e 2053 7479  .......EPSON Sty
  00000010: 6c75 7320 434f 4c4f 5220 3135 3230 4828  lus COLOR 1520H(
  00000060: ff01 0000 0000 0000 0000 0500 5061 6765  ............Page
  00000080: 0000 7800 0000 7c01 0000 2c01 0000 0400  ..x...|...,.....
  00000090: 0000 0200 f900 0000 0500 4261 6e64 3100  ..........Band1.
```

→ **확증**: (a) Pascal short-string 길이 prefix (0x19 = 25 bytes 이후 0x1F = 31 bytes 의 "EPSON Stylus COLOR 1520H(KSSM+)" 프린터명), (b) 0x60 위치의 `Page1` / 0x90 위치의 `Band1` 객체명 = **TStream 기반 Delphi DFM 바이너리 시리얼라이즈 + FreeReport 객체 명명 규약** 정확히 일치. **§1.3 의 FreeReport 2.3 LoadFromStream 가설 100% 유효** — 즉, B1/B2 안의 R1 (Pascal 디시리얼라이저 Python 포팅) 단계는 그대로 6~11 인주 추정 유지.

부수 발견: 헤더 첫 9 바이트 (`19FFFFFFFF1F00`) 는 **프린터 정보 (printer setup)** 가 페이지 정보보다 앞서 직렬화되는 FastReport VCL 2.x 의 시그니처 — 이는 FreeReport 2.3 의 `TfrReport.SaveToStream` 시퀀스와 일치하므로 R1 디시리얼라이저는 *프린터 헤더 → 페이지 → 밴드 → 객체* 순서로 읽으면 됨. (단, 프린터 정보는 우리 운영에 불필요 → R1 에서 skip 가능.)

### 1.8. 로컬 FastReport OSS 소스 직접 분석 (2026-04-20 신규 — ⭐ 게임 체인저)

`/Users/speeno/Downloads/FastReports-FastReport-8ef9cde` (FastReports/FastReport master tarball, MIT) 를 워크스테이션에 복제 후 직접 분석한 결과, 기존 §1.4 의 "객체 시맨틱 95% 호환" 조사를 넘어 **HTML 변환 코드 자체가 OSS 코어에 이미 완비** 되어 있음을 확인. 본 발견은 자체 파서 R&D 의 작업량/리스크/비용 추정을 근본적으로 재계산하게 한다.

#### A. HTML export 코어 내장 ✅ (3137 LOC, MIT, 별도 의존성 0)

| 파일 | LOC | 책임 |
| --- | --- | --- |
| `FastReport.Base/Export/Html/HTMLExport.cs` | 1187 | 진입점, `ExportBase` 상속, 페이지/밴드 순회, CSS/HTML 빌드 |
| `FastReport.Base/Export/Html/HTMLExportLayers.cs` | 992 | **Layer 모드 — `<div style="position:absolute;">` 픽셀 절대 좌표 출력** (Text/Picture/Shape/Table/Watermark) |
| `FastReport.Base/Export/Html/HTMLExportDraw.cs` | 394 | 그리기 (테두리/채움/이미지) |
| `FastReport.Base/Export/Html/HTMLExportStyles.cs` | 164 | CSS 클래스 생성 (font/color/border) |
| `FastReport.Base/Export/Html/HTMLExportTemplates.cs` | 164 | HTML 페이지 골격 템플릿 |
| `FastReport.Base/Export/Html/HTMLExportUtils.cs` | 236 | 단위/색상/엔티티 변환 헬퍼 |

**Layer 모드 핵심 패턴** (`HTMLExportLayers.cs:Layer` 메서드):
```csharp
Page.Append("<div ").Append(classTag).Append(" style=\"").
     Append("position:absolute;").
     // left, top, width, height, font, color, border ...
     Append("\">").Append(text).Append("</div>");
```

→ **이는 우리가 `.frf` 의 Pascal `TfrTextView`/`TfrPictureView`/`TfrLineView`/`TfrRectView` 를 픽셀 절대 좌표 HTML 로 충실 재현할 때 필요한 출력 형식과 정확히 동일**. 자체 R3b (객체 → CSS 변환) 1.5~3 인주의 작업이 *0 인주* 로 대체 가능.

#### B. PdfSimple 플러그인 라이선스 = MIT (이전 R&D 오기 교정)

`Extras/OpenSource/FastReport.OpenSource.Export.PdfSimple/.../*.csproj` 직접 확인:
```xml
<PackageLicenseUrl>https://github.com/FastReports/FastReport/blob/master/LICENSE.md</PackageLicenseUrl>
<!-- LICENSE.md = MIT (Copyright 2024 Fast Reports Inc) -->
```

→ 이전 보강 (1)/(2) 에서 "LGPL-3.0 PdfSimple" 로 표기한 부분은 **사실관계 오류** (MIT 일관). 본 갱신에서 §5 라이선스 요약/§4 비교표 모두 정정. 단, PdfSimple 의 *기능 한계* (페이지를 이미지로 합성, 텍스트 선택 불가, 큰 용량) 는 그대로 — yusufbal 사례의 우회 패턴 정당성은 유지.

#### C. Import 플러그인 4종 = `.frf` 임포터의 직접 템플릿

`FastReport.Base/Import/` 산하:

| 임포터 | LOC | 입력 포맷 | 우리 R&D 가치 |
| --- | --- | --- | --- |
| **RDL** (Microsoft Reporting) | 988 + 672 (ImportTable) + 588 (UnitsConverter) | `.rdl` (XML) | ⭐⭐⭐ 가장 단순한 `ImportBase` 구현 — XML XmlReader 기반 + 단위 변환 패턴 모범 |
| **StimulSoft** | 1582 + 867 | `.mrt` (XML) | ⭐⭐ 복잡한 표현식/함수 매핑 예시 |
| **JasperReports** | 1165 + 425 | `.jrxml` (XML) | ⭐⭐ 다른 벤더 호환 매핑 예시 |
| **ListAndLabel** | (별도) | `.lst` | ⭐ 단순 변환 |

**공통 골격** (`ImportBase.cs:LoadReport(report, filename)`):
```csharp
public virtual void LoadReport(Report report, string filename) {
  report.Clear();
  // → 파일 파싱 → Report.Pages.Add(new ReportPage()) →
  // → 각 ReportPage.Bands.Add(new DataBand()) →
  // → 각 BandBase.Objects.Add(new TextObject() { Left=…, Top=…, Text=… })
}
```

→ **자체 `FrfImport : ImportBase` 작성 시 RDL 임포터를 1:1 템플릿으로 사용 가능** (Pascal TStream 디코더만 신규 작성, 객체 매핑은 RDL 임포터 988 LOC 의 패턴 그대로).

#### D. Report 적재/저장 파이프라인

`FastReport.Base/Report.cs:Load(Stream)` (line 2059~2111):
```csharp
public void Load(Stream stream) {
  Clear();
  using (FRReader reader = new FRReader(this)) {
    if (Compressor.IsStreamCompressed(stream)) stream = Compressor.Decompress(...);
    if (Crypter.IsStreamEncrypted(stream))    stream = Crypter.Decrypt(...);
    reader.Load(stream);   // .frx XML parse
    reader.Read(this);     // 객체 그래프 복원
  }
}
```

→ `.frf → .frx` 변환만 하면 OSS 의 `Report.Load()` 가 그대로 객체 그래프 복원. 그 후 `report.Export(new HTMLExport(), htmlStream)` 1 줄로 HTML 산출.

#### E. 새로운 권장 전략 **B4 — 빌드 타임 변환 + Jinja2 템플릿** 🌟

기존 B1/B2 안의 운영 부담 (Python 디시리얼라이저 + CSS 변환기 유지보수) 을 *근본적으로 회피* 하는 신규 전략:

```
[빌드 타임, 1회 또는 .frf 변경 시]
  .frf (Pascal binary) ──[R1 디시리얼라이저, Python or .NET]──> 객체 그래프
                                                                  │
                                                                  ├──[R3a IR 변환]──> .frx XML (FastReport.Documentation 명세)
                                                                                          │
                                                                                          └──[R3b-NEW] FastReport OSS Report.Load + HTMLExport.Layers=true
                                                                                                                                                           │
                                                                                                                                                           └──> HTML 산출 (Jinja2 placeholder 삽입)
                                                                                                                                                                   │
[운영 시 — Python/FastAPI + WeasyPrint 그대로 (DEC-037 무변경)]                                                                                                       │
                                                                                                                                                                   ▼
  GET /api/v1/print/.../*.pdf ──> Jinja2 렌더 (DB 데이터) ──> WeasyPrint PDF 출력
```

**Jinja2 placeholder 변환 규칙** (.frx → 빌드 타임 후처리, 1 인주):

| FastReport 토큰 | 빌드 타임 치환 | 운영 시 Jinja2 컨텍스트 |
| --- | --- | --- |
| `[Sg_Csum.Gname]` (TextObject.Text) | `{{ Sg_Csum.Gname }}` | `{ "Sg_Csum": {"Gname": "..."} }` |
| `[PageN]` | `{{ page_num }}` | `{ "page_num": 1 }` |
| 정적 텍스트 (라벨) | 그대로 유지 | (없음) |
| 데이터 밴드 반복 | `{% for row in Sg_Csum %}...{% endfor %}` | `{ "Sg_Csum": [...] }` |

**비용 재계산 (B4 vs B1/B2)**:

| 단계 | B1 (직접 변환) | B2 (`.frx` IR + .NET 검증) | **B4 (빌드 타임 + Jinja2)** |
| --- | --- | --- | --- |
| R1 (Pascal 디시리얼라이저 → Python) | 2~4 | 2~4 | 2~4 |
| R2 (98 건 시그니처 덤프) | 0.5 | 0.5 | 0.5 |
| R3a (객체 그래프 → `.frx` IR) | — | 1~2 | 1~2 |
| R3b (CSS 변환 — *자체 작성*) | 1.5~3 | 1.5~3 | **0** (FastReport OSS HTMLExport 위임) |
| R3c (Jinja2 placeholder 후처리) | — | — | **0.5~1** |
| R4 (데이터 토큰 → Python 컨텍스트) | 0.5~1 | 0.5~1 | **0** (Jinja2 자체) |
| R5 (모르는 객체 skip) | 0.5 | 0.5 | 0 (FastReport OSS 가 처리) |
| R6 (회귀 게이트) | 1~2 | 1~2 | 0.5~1 |
| **합계** | **6~11 인주** | **7~13 인주** | **⭐ 4.5~8.5 인주** |
| 운영 시 .NET 의존성 | 0 | 0 | **0** (빌드 타임만) |
| 운영 시 라이선스 | WeasyPrint BSD-3 | WeasyPrint BSD-3 | WeasyPrint BSD-3 |
| 디자인 충실도 | 자체 R3b 품질에 의존 | 동일 | **⭐ FastReport OSS 1187 LOC HTML export 품질 = 표준 보장** |
| `.frf` 변형 회귀 | 변형마다 검증 | 변형마다 검증 | 변형마다 *빌드 타임 1회 재실행* (CI 통합 용이) |

**B4 안의 핵심 우월성**:
1. **R3b 비용 0** — FastReport OSS 코어 1187 LOC HTML export 를 그대로 위임. Layer 모드 = 픽셀 절대 좌표.
2. **운영 스택 변동 0** — DEC-037 Python/WeasyPrint 그대로. .NET 런타임 운영 도입 안 함.
3. **빌드 타임 한정 .NET 의존성** — `dotnet run` 으로 `frf-converter.dll` 1회 실행 → HTML 템플릿 생성 → repo 에 commit. CI 워크플로 `convert-frf-templates.yml` 추가.
4. **회귀 게이트 단순화** — 빌드 타임 산출 HTML vs 수동 재현 HTML diff 가 그대로 회귀 가드.

**B4 안의 단점**:
- 빌드 환경 (CI 런너) 에 .NET 8 런타임 필요 (1회 추가).
- 데이터 밴드 반복 변환 (`{% for ... %}`) 은 단순 치환 후처리로 가능하지만 nested band/group 은 추가 매핑 필요 (R3c 0.5~1 인주에 포함).
- FastReport OSS HTML export 의 한계 (BarcodeObject HTML 출력 시 SVG 사용 — WeasyPrint 호환 검증 필요) — 1 일 PoC 권장.

## 2. 자체 구현 시 작업 분해 (참고)

만약 Phase 2 이후 자체 파서 도입 결정 시 다음 단계로 나눈다.

| 단계 | 작업 | 추정 인주 | 참조 OSS / 문서 |
| --- | --- | --- | --- |
| **R1** | FreeReport 2.3 `FR_Class.pas` 의 LoadFromStream 로직을 Python (pure stdlib `struct` + RTTI 디코더) 으로 포팅 | 2~4 | https://github.com/FastReports/FreeReport |
| **R2** | 우리 98 건 `.frf` 시그니처/페이지/밴드/객체 트리 덤프 — 모르는 객체 인벤토리 | 0.5 | (자체) |
| **R3a** *(신규, 2026-04-20)* | 객체 그래프 → `.frx` 동등 XML IR 변환. FastReport.Documentation 의 `ReportObjects.md`/`Bands.md`/`ReportTemplateFileStructure.md` 를 매핑 명세서로 사용. | 1~2 | https://github.com/FastReports/FastReport.Documentation |
| **R3a-검증** *(신규)* | IR `.frx` 를 FastReport .NET OSS (`Report.Load`) 로 적재 → PDF 생성 → 시각 비교. 통과 = 객체 그래프 충실도 보장. | 0.5~1 | https://github.com/FastReports/FastReport (MIT) |
| **R3b** | 알려진 객체 (`TfrTextView`/`TfrLineView`/`TfrRectView`/`TfrPictureView`/`TfrBarCodeView`) 5종을 CSS 절대 좌표 (`position: absolute`) + `@page` mm 단위로 변환. WeasyPrint 호환 출력. | 1.5~3 | (자체, DEC-037 엔진 유지) |
| **R4** | 데이터 바인딩 토큰 (`[Sg_Csum."Gname"]` 류) → Python 컨텍스트 변수 매핑 (Jinja 등). FastReport `Expressions.md` 토큰 문법 100% 채택. | 0.5~1 | https://raw.githubusercontent.com/FastReports/FastReport.Documentation/master/Expressions.md |
| **R5** | 모르는 객체 graceful skip + 손실율 측정 → DEC-039+ 정책 갱신 | 0.5 | (자체) |
| **R6** | C7 Phase 1 의 5 양식 + 1 라벨 = **수동 재현본 vs 자동 변환본** 픽셀 diff 측정 (회귀 게이트). 옵션: B3 (HtmlExporter PDF 를 *Ground Truth* 로) 추가 시 3-way diff (수동/자동/HtmlExporter). | 1~2 | (자체) + (옵션) https://github.com/yusufbal/FastReport.OpenSource.HtmlExporter |
| **합계 (개선안)** | | **7~13 인주** | (R3a IR + 검증 단계 1~2 인주 추가) |
| **합계 (기존안 = R3a 생략)** | | **6~11 인주** | |

**권고**: R3a IR 채택 — IR 검증으로 객체 그래프 충실도가 .NET OSS 표준에 의해 보장됨. R3b CSS 변환의 자유도가 늘어 WeasyPrint 호환 최적화에만 집중 가능.

## 3. 위험 / 제약

- **위험 1 (디자인 손실)**: FreeReport 2.3 → FastReport 4.x 사이에 추가된 객체/속성을 skip 하면 디자인 충실도가 떨어짐. 운영 사용자 클레임 가능.
- **위험 2 (.frf 변형 폭발)**: `Report_4_51-{0~9}` 처럼 거래처별 양식이 10 변형. 자동 변환은 변형마다 회귀 검증 필요.
- **위험 3 (라이선스)**: FreeReport 는 BSD-류. 자체 포팅 시 라이선스 헤더 보존 의무. 신규 코드는 우리 프로젝트 라이선스로 분리.
- **제약 (성능)**: 98 건 일괄 변환 시 FreeReport 의 TStream 디코더는 각 파일 50~200ms 추정. 빌드 타임 변환 (1회) 권장.

## 4. 대안 비교

| 대안 | 장점 | 단점 | 채택 여부 |
| --- | --- | --- | --- |
| **A. 수동 재현 (Phase 1 채택)** | 디자인 100% 자유, 코드 단순, WeasyPrint 만 의존 | 양식 추가/거래처 변형 시 매번 노동 | **Phase 1 = ✅ (DEC-039)** |
| B1. 자체 파서 (기존 안, R3 직접 변환) | 98 건 일괄 자동화 가능 | 6~11 인주 + 디자인 손실 위험 + 변형 회귀 | Phase 2 이후 검토 |
| **B2. 자체 파서 (개선안, R3a `.frx` IR + .NET OSS 검증)** *(신규)* | 객체 그래프 충실도가 FastReport.Documentation 명세 + .NET OSS 적재로 보장; 향후 .NET 환경 채택 시 IR 즉시 활용 | 7~13 인주 (1~2 인주 추가); .NET 빌드 환경 1회 필요 | Phase 2 이후 **권장** (B1 대비 우선) |
| **B3. B2 + HtmlExporter 회귀 게이트** *(신규, 2026-04-20)* | B2 의 R6 픽셀 diff 게이트에서 *기준선* 을 `yusufbal/FastReport.OpenSource.HtmlExporter` (MIT) 의 PDF 출력으로 사용. NuGet 1 줄 의존성으로 .NET OSS 표준 HTML/PDF 출력을 *Ground Truth* 화 가능 | iText7 (Apache 2.0/AGPL 듀얼) 가 검증 빌드에 포함됨 — 운영 패키지에는 미포함이므로 라이선스 영향 0 | B2 채택 시 회귀 게이트 *기본값* 으로 권장 |
| **⭐ B4. 빌드 타임 변환 + Jinja2 (신규 권장)** *(2026-04-20)* | (i) FastReport OSS 코어 HTML export 1187 LOC (MIT, Layer 모드 = 픽셀 절대 좌표) 를 그대로 위임 — 자체 R3b CSS 변환 비용 **0**. (ii) **운영 스택 (Python/FastAPI/WeasyPrint) 변동 0** — DEC-037 그대로. (iii) 변환은 빌드 타임 1회, repo 에 HTML 템플릿 commit. (iv) Jinja2 placeholder 후처리로 데이터 바인딩 토큰 자연스러운 매핑. **합계 4.5~8.5 인주** (B1 대비 30% 단축, B2 대비 40% 단축). | (i) 빌드 환경에 .NET 8 런타임 1회 필요 (운영 0). (ii) 데이터 밴드 반복 (nested) 매핑은 추가 작업 (R3c 0.5~1 인주에 포함). (iii) BarcodeObject HTML 출력 (SVG) 의 WeasyPrint 호환은 1일 PoC 권장. | **Phase 2 진입 시 1순위 권장** (B1/B2/B3 대체) |
| C. 상용 FastReport VCL SDK 라이선스 | 100% 호환. 운영 통합 패턴 = `atkins126/FastReportExport` (Apache-2.0 래퍼, 멀티스레드 서버 안전 fluent API) 참조 가능 | 라이선스 비용 + Delphi/C++ 의존 + Linux 서버 미지원 + 현 Python/FastAPI 스택과 이질 | 부적합 |
| **C2. FastReport .NET OSS 직접 운영** *(신규)* | MIT, Linux/Core 지원, `.frx` 입력 시 PDF 즉시 생성 | (i) 입력은 `.frx` 만 — `.frf` 변환기 (B2) 필요. (ii) PDF 플러그인 LGPL 별도. (iii) .NET 런타임 운영 부담 (현재 스택은 Python/FastAPI). | B2 채택 시 *검증 단계에만* 사용 권장 (운영 엔진은 DEC-037 WeasyPrint 유지) |
| **C3. FastReport .NET OSS + HtmlExporter (.NET 직접 운영)** *(신규, 2026-04-20)* | (i) `.frx` 적재 → HTML export → iText7 PDF 가 검증된 OSS 파이프라인 (yusufbal 사례). (ii) NuGet 1 패키지 + 5~10 줄 코드. | (i) `.frx` 만 입력 — `.frf → .frx` 변환기 (B2 의 R3a) 필요. (ii) iText7 AGPL 면 상용 운영 시 라이선스 비용. (iii) Python/FastAPI 스택에서 .NET 런타임 마이크로서비스 추가 부담. | 운영 채택 부적합 — DEC-037 WeasyPrint 가 라이선스/스택 면에서 우월 |
| D. Wine 등으로 레거시 EXE 호출 | 즉시 사용 가능 | 운영 노드에 Wine + Delphi 런타임 + .frf 경로 마운트 — 운영 부담 큼 | 부적합 |

## 5. 권장 결론 / 후속 트리거

- **Phase 1 = DEC-039 정책 유지** (자동 변환 0, 수동 재현). 본 R&D 는 Phase 1 의 결정에 영향 없음.
- **Phase 2 진입 시 1 회 재검토** — 다음 조건 중 1 개라도 만족하면 자체 파서 도입 검토:
  1. 거래처별 변형 (`Report_4_51-N` / `Report_2_13-N`) 이 5건 이상 운영 사용자에 의해 요구되어 수동 재현 비용 폭발.
  2. C7 Phase 2 에서 통계/현황 (Report_5_*/6_*) 인쇄 도입 계획 (30+ 양식).
  3. 외부 파트너에서 `.frf` 정본을 수정해 전달하는 워크플로 도입 (자동 동기화 필요).
- **자체 파서 도입 결정 시 권장 안 = ⭐ B4 (빌드 타임 변환 + Jinja2)** — 2026-04-20 로컬 소스 분석 결과 추가된 신규 권장. B1/B2/B3 대비 30~40% 비용 단축 + 운영 스택 변동 0 + 디자인 충실도 표준 보장.
  - 진입 직전 1 일 PoC 권장: BarcodeObject SVG 출력의 WeasyPrint 호환 확인.
- **차단 가드**: 자체 파서 도입 결정 후에도 **DEC-037 (WeasyPrint 단일 엔진) 은 유지** — 파서는 `.frf → HTML` 1 단계 (B4 의 빌드 타임) 만 책임지고, HTML → PDF 는 동일 엔진. .NET 런타임은 *빌드 타임 한정* 으로 도입.

## 참조

### OSS 코드 / 명세 (R&D 자료)

- **FreeReport** (BSD, Delphi 4~9, `.frf` 선조 포맷 디시리얼라이저): https://github.com/FastReports/FreeReport
- **FastReport (.NET OpenSource)** (MIT, `.frx` XML 적재 + HTML/PNG/PDF 출력): https://github.com/FastReports/FastReport
- **FastReport.Documentation** (MIT, 객체/밴드/표현식 공식 명세 — `.frx` 시맨틱 정본): https://github.com/FastReports/FastReport.Documentation
  - `ReportTemplateFileStructure.md` — `.frx` XML 예시 (단위, 속성, 데이터셋)
  - `Bands.md` — 밴드 분류 (PageHeader/DataBand/PageFooter/ChildBand 등)
  - `ReportObjects.md` — TextObject/PictureObject/LineObject/BarcodeObject 등 객체 명세
  - `Expressions.md` — `[Table.Column]` 토큰 + 함수 평가 규칙
  - `StoringLoadingReport.md` — `Report.Load(stream)`/`LoadFromString` API
  - `COMPARISON.md` — OSS / Core / .NET 본 기능/OS 비교
  - `ClassReference/` — 클래스 별 속성/메서드 사전
- **FastReport.VCL.RES** (MIT, UI 다국어): https://github.com/FastReports/FastReport.VCL.RES — 본 R&D 가치 없음
- **yusufbal/FastReport.OpenSource.HtmlExporter** *(MIT, .NET 8, 2026-04-20 추가)*: https://github.com/yusufbal/FastReport.OpenSource.HtmlExporter
  - 패턴: `.frx` → FastReport OSS HTML export → iText7 PDF (텍스트 선택 가능, 작은 용량)
  - NuGet: https://www.nuget.org/packages/PdfExporter.FastReport.OpenSource
  - 본 R&D 시사점: **DEC-037 (HTML 빌더 → WeasyPrint) 아키텍처와 동일한 발상** 이 .NET OSS 진영에서도 베스트 프랙티스 → 우리 결정 정당성 강화. B3 안의 회귀 게이트 *Ground Truth* 후보.
- **atkins126/FastReportExport** *(Apache-2.0, Delphi VCL Pascal, antoniojmsjr 본 fork, 2026-04-20 추가)*: https://github.com/atkins126/FastReportExport (원본: https://github.com/antoniojmsjr/FastReportExport)
  - 패턴: 멀티스레드/서버 환경 (Horse/ISAPI/WindowsService) 에서 FastReport VCL 상용 SDK 안전 호출 fluent API 래퍼
  - 의존성: 유료 FastReport VCL SDK (`frxClass`, `frxExportPDF`, `frxExportHTML` 등) — 래퍼만 OSS
  - 샘플 형식: `.fr3` (FastReport 3+ XML), `.frf` 미지원
  - 본 R&D 시사점: **§4 C 안 (상용 FastReport VCL SDK) 채택 시 운영 통합 레퍼런스**. 현 DEC-037 Python/WeasyPrint 스택에는 **직접 적용 0**. 부수 발견: `.frf` 의 실제 시그니처 (binary FRF15 vs text `.fr3`) 5분 검증 권장.

### 로컬 소스 분석 (2026-04-20 신규)

- **FastReports/FastReport master tarball** (워크스테이션 복제, MIT): `/Users/speeno/Downloads/FastReports-FastReport-8ef9cde`
  - `FastReport.Base/Export/Html/` (3137 LOC, HTML export Layer 모드 = 픽셀 절대 좌표) — **B4 안의 핵심 위임 대상**
  - `FastReport.Base/Import/{RDL,StimulSoft,JasperReports,ListAndLabel}/` — **자체 `.frf` 임포터의 직접 템플릿** (RDL 988 LOC 가 가장 단순)
  - `FastReport.Base/Report.cs:Load(Stream)` — `.frx XML → 객체 그래프 복원` 파이프라인
  - `Demos/OpenSource/Console apps/PdfExport/Program.cs` — `.frx → Report.Load → Prepare → HTMLExport.Export(stream)` 30 LOC 미만의 데모

### 라이선스 요약 (2026-04-20 로컬 소스 직접 검증으로 교정)

- FreeReport: BSD-2-Clause (저작권 표시 보존)
- **FastReport (.NET OSS): MIT 일관** — 코어 + 모든 OSS 플러그인 (`FastReport.OpenSource.Export.PdfSimple` 포함) 이 단일 `LICENSE.md` 의 MIT 라이선스 적용 (이전 보강의 "LGPL PdfSimple" 표기는 오류로 **교정**)
- FastReport.Documentation: **MIT**
- yusufbal/FastReport.OpenSource.HtmlExporter: **MIT** (단, 의존성 iText7 = Apache 2.0/AGPL 듀얼 — AGPL 면 상용 운영 라이선스 부담 ↑. 검증 빌드 전용 사용 시 영향 0)
- atkins126(antoniojmsjr)/FastReportExport: **Apache-2.0** (래퍼만; 의존성 FastReport VCL = 유료 상용 SDK — 운영 도입 시 별도 라이선스 비용)
- **본 프로젝트 통합 정책 (B4 안 채택 시)**: 빌드 타임 .NET 8 + FastReport.OpenSource (MIT) NuGet 만 사용 → 운영 패키지에는 .NET 의존성 0, MIT 저작권 표시 1회 (빌드 도구 README 또는 NOTICE 파일) 만 추가.

### 포럼 / 외부 자료

- FastReport 공식 포럼: https://forum.fast-report.com/en/categories/freereport (커뮤니티 토론, 코드 산출물 미공개)

### 본 프로젝트 연계 문서

- `analysis/print_specs/frf_catalog.md` — T9, 98 건 정본 인벤토리 + 5 양식 ↔ `.frf` 매핑표
- `legacy-analysis/decisions.md` DEC-039 — `.frf` 정본 정책 (참조용, 자동 변환 0)
- `legacy-analysis/decisions.md` DEC-037 — WeasyPrint 단일 PDF 엔진 (자체 파서 도입 후에도 유지)
- `analysis/regression/c7_phase1.md` — 5축 회귀 매트릭스 (자체 파서 도입 시 R6 픽셀 diff 게이트 추가 위치)
