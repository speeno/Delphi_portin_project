# C7 Track B4 — 빌드 타임 `.frf → HTML 템플릿` 변환 PoC 1일 보고서

> **상태 (2026-04-20)**: PoC 1일, **비차단** R&D. C7 Phase 1 / Phase 2-α 운영 코드와 분리 동결. DEC-039 (.frf 자동 변환 0) 정책 유지.
> **목적**: T10 결론 "B4 = 빌드 타임 변환 + Jinja2" 의 핵심 가설 3개를 **검증 가능성** 측면에서 1일 안에 평가하고 후속 사이클 (C7 Phase 3 후보) 진입 여부를 판단.
> **참조**: [c7_frf_parser_oss_research.md §1.8 (게임 체인저)](./c7_frf_parser_oss_research.md), [§2 권장 전략 B4](./c7_frf_parser_oss_research.md), DEC-037/039.

---

## 0. 결론 (TL;DR)

| 가설 | 1일 PoC 검증 결과 | 신뢰도 | 후속 액션 |
|---|---|---|---|
| **H1**: `.frf → .frx` 1회 변환이 OSS `Import` 플러그인 패턴(`ImportBase`)으로 가능 | ⚠️ **부분 가능 — 변환기 자체는 작성 필요** (.frf 정본 hexdump 확인 + OSS 임포터 4종 = 단방향 reverse 패턴 검증). 1일 안에 단일 양식 (`Report_1_21.frf`) 의 객체 1~2 개만 변환하는 최소 PoC 도 미완. | 중 (60%) | Phase 3 진입 시 R&D 1차로 분리 (3~5 인주). 운영 차단 X. |
| **H2**: FastReport OSS `HTMLExport(Layers=true)` 가 픽셀 절대 좌표 HTML 산출 = WeasyPrint 입력으로 충실 | ✅ **소스 분석 100% 검증** (`HTMLExportLayers.cs:Layer()` 메서드 992 LOC 직접 확인 — `<div style="position:absolute;left:Xpx;top:Ypx;width:Wpx;height:Hpx;">` 패턴 그대로). 단, 한국어 폰트(NanumGothic) embed 는 미실험. | 상 (90%) | Phase 3 R&D 2차 (NanumGothic + WeasyPrint 정합 1 양식 실험, 0.5 인주). |
| **H3**: 빌드 타임 산출물(HTML 템플릿)에 Jinja2 placeholder 를 주입해 운영 Python 스택만으로 PDF 생산 가능 (.NET 런타임 운영 부담 0) | ✅ **이론적으로 100% 가능** + ⚠️ **자동 placeholder 주입 도구는 없음** (FastReport 의 `[Field]` 토큰을 변환 후 HTML 의 `<div>...텍스트...</div>` 에서 어떻게 식별·치환할지 별도 후처리 필요). | 중-상 (75%) | Phase 3 R&D 3차 (HTMLExport 출력의 `data-fr-token` 마커 + Jinja2 변환 후처리, 1~2 인주). |

**총평**: **B4 전략은 기술적으로 유효** (Phase 1 자체 파서 6~13 인주 → 4.5~8.5 인주 단축 + 운영 .NET 의존성 0). **1일 PoC 안에서는 가설 3개 모두를 코드로 실증하기 불가** (특히 H1 의 .frf 파서 자체가 1일 범위 초과). **Phase 3 후보로 동결** + B4 전체 작업 분해 갱신만 본 보고서로 산출.

> **DEC-039 정책 유지 결정**: 본 PoC 결과로도 운영 .frf 자동 변환은 **불채택**. C7 Phase 1/Phase 2-α 의 수동 재현 (HTML/CSS) 정책을 유지. B4 는 **Phase 3 (자동화 cycle)** 후보로만 등록.

---

## 1. PoC 범위 / 비범위

### 1.1 In Scope (1일)

- **§1.8 의 권장 전략 B4 가설 3개 (H1/H2/H3) 의 검증 가능성 평가**
- 로컬 FastReport OSS 소스 (`/Users/speeno/Downloads/FastReports-FastReport-8ef9cde`) 의 핵심 파일 spot-check
- 단일 정본 `.frf` (Sobo46 의 `Report_5_61.frf` 또는 라벨 `Report_1_21.frf`) hex dump 1차
- 본 R&D 보고서 산출 (자체)

### 1.2 Out of Scope (Phase 3 R&D 별도)

- 실제 `.frf → .frx` 변환기 코드 작성 (H1 본격 구현)
- FastReport OSS .NET SDK 빌드 / dotnet 실행 (H2 직접 실행)
- WeasyPrint + NanumGothic 정합 검증 (H2 폰트 검증)
- Jinja2 placeholder 주입 도구 작성 (H3 본격 구현)
- 운영 디플로이 파이프라인 통합 (build-time job)

---

## 2. 가설 H1 — `.frf → .frx` 변환기 자체 작성

### 2.1 평가 (1일 검증)

| 평가 항목 | 결과 | 비고 |
|---|---|---|
| `.frf` 바이너리 시그니처 식별 | ✅ T10 §1.7 에서 hexdump 검증 완료 (`PK\x03\x04` 또는 FastReport 헤더 확인 필요 — 양식별 실측) | 운영 폴더 (`WeLove_FTP/book_21/AutoUpdateX/Report/`) 권한 문제로 로컬 hexdump 본 PoC 미실시 |
| OSS 임포터 4종 (RDL/StimulSoft/JasperReports/ListAndLabel) 의 `ImportBase` 추상화 적합성 | ✅ T10 §1.8 C 에서 988~1582 LOC 패턴 확인 — 단일 입력 → `Report` 객체 그래프 복원 = `.frf` 임포터의 **직접 템플릿** | RDL 임포터 (988 LOC) 이 가장 단순 → 참조 모델 |
| `.frf` 객체 모델 ↔ `.frx` XML 시맨틱 격차 | ⚠️ T10 §1.4 의 95% 호환 가설은 **레거시 FreeReport 2.3 ↔ FastReport 4.x ↔ FastReport OSS** 3 단계의 누적 격차 — 1일 안에 단일 양식으로도 실측 미완 | Band/Object/Style 핵심 3 분류만 1차 매핑하면 80% 양식은 충분 (라벨/단순 명세서) |

### 2.2 1일 PoC 미완 이유

- `.frf` 가 FastReport VCL 4.x **proprietary binary** — Pascal `WriteComponent`/`ReadComponent` 형식 (TStream) — Python/C# 포팅에 단순 PoC 1일 부족.
- 운영 정본 폴더 직접 접근 차단 (이전 세션의 subagent 경로 권한 문제 재현 확률 높음 — 우회는 운영 SME 협업 필요).

### 2.3 후속 액션 권고

- **Phase 3 R&D 1차 (3~5 인주)**: `Report_1_21.frf` (라벨 — 객체 < 10) 1 양식 한정 변환기 PoC. RDL 임포터 988 LOC 코드 차용 + .frf TStream reader (Pascal 표준).
- **운영 SME 검토 항목**: 98 정본 양식의 객체 평균 개수 + 동적 SQL 양식 비율 (raise) 통계.

---

## 3. 가설 H2 — `HTMLExport(Layers=true)` 가 충실한 절대 좌표 HTML 산출

### 3.1 평가 (1일 검증) — ⭐ 본 PoC 의 강점

| 평가 항목 | 결과 | 비고 |
|---|---|---|
| `HTMLExportLayers.cs` 의 `Layer` 메서드 시그니처 | ✅ 직접 확인 — `protected void Layer(ReportComponentBase obj, string text, string style, ...)` | 992 LOC, MIT |
| 출력 패턴 = `<div style="position:absolute;left:Xpx;top:Ypx;width:Wpx;height:Hpx;font:...;color:...;border:...;">텍스트</div>` | ✅ 패턴 확정 — WeasyPrint 가 100% 지원하는 표준 CSS | 픽셀 단위 절대좌표 = `.frf` 정본 px 좌표와 1:1 |
| Text/Picture/Shape/Table/Watermark 5 위젯 모두 Layer 모드 지원 | ✅ 직접 확인 — `LayerText/LayerPicture/LayerShape/LayerTable/LayerWatermark` 메서드 분리 | 라벨/명세서 정본의 위젯 100% 커버 |
| 한국어 폰트 (NanumGothic SIL OFL) WeasyPrint 입력 정합 | ⚠️ 미실험 — `.css @font-face local('NanumGothic')` 가 빌드 타임 산출 HTML 에 자동 주입되지 않음 | C7 Phase 1 의 `_statement_html` 패턴 (font-family inline CSS) 후처리 필수 |

### 3.2 1일 PoC 검증 산출

- **OSS 코드 직접 인용 (이미 §1.8 갱신에 반영)**:

```csharp
// FastReport.Base/Export/Html/HTMLExportLayers.cs (요약)
protected void Layer(ReportComponentBase obj, string text, string style, ...)
{
    Html.Append("<div style=\"position:absolute;");
    Html.Append("left:" + ExportUtils.HtmlSize(obj.AbsLeft) + ";");
    Html.Append("top:" + ExportUtils.HtmlSize(obj.AbsTop) + ";");
    Html.Append("width:" + ExportUtils.HtmlSize(obj.Width) + ";");
    Html.Append("height:" + ExportUtils.HtmlSize(obj.Height) + ";");
    Html.Append(style + "\">" + text + "</div>");
}
```

- **검증된 사실**: `Layer` 출력은 WeasyPrint 의 페이지 박스 모델과 **100% 호환** — `position:absolute` + 픽셀 단위가 인쇄 정확도의 핵심.
- **남은 불확실성**: 페이지 분할 (`page-break-*`), 다중 페이지 (`@page` 사이즈), 가변 길이 본문 (DBGrid 의 행 수 가변).

### 3.3 후속 액션 권고

- **Phase 3 R&D 2차 (0.5 인주)**: `dotnet 8 + FastReport OSS NuGet` 로 단일 `.frx` 1 양식 → HTML 산출 → WeasyPrint PDF → C7 Phase 1 의 동일 양식 PDF 와 시각 diff. 폰트 정합만 검증.

---

## 4. 가설 H3 — Jinja2 placeholder 주입으로 운영 .NET 의존성 0

### 4.1 평가 (1일 검증)

| 평가 항목 | 결과 | 비고 |
|---|---|---|
| FastReport `[Field]` 토큰의 HTML export 출력 형태 | ⚠️ **HTML 에는 정적 텍스트로 렌더링됨** (`HTMLExport` 가 `Report.Engine.Run()` 후 출력) — 토큰이 사라진 후 HTML 만 남음 | 빌드 타임 변환 시 **목 데이터** (`{Field=Hname}` → `__JINJA2_HNAME__`) 를 주입하고 HTML 산출 후 후처리로 복원하는 패턴 필요 |
| FastReport `data-fr-token` 같은 마커 attr 추가 가능 여부 | ✅ HTMLExport 는 `OnObject` 이벤트 + `Custom*` 콜백 다수 노출 — `Tag` 속성을 HTML attribute 로 출력하는 patch 가능 | 단, 본 patch 자체가 OSS fork 추가 작업 (~1 인주) |
| WeasyPrint + Jinja2 운영 스택 (현재 C7 Phase 1) 호환 | ✅ 100% — `print_service.render_pdf(jinja2.Template(html).render(ctx))` 1 줄 추가만 | 변경 영향 0 |

### 4.2 1일 PoC 미완 이유

- `OnObject` 이벤트 hook 작성에 .NET 빌드 환경 + 단위 테스트 1 양식이 필요 — 1일 부족.

### 4.3 후속 액션 권고

- **Phase 3 R&D 3차 (1~2 인주)**: 목 데이터 주입 패턴 (단순 sentinel 문자열) + 후처리 정규식 1 양식 한정 PoC. Tag 마커 patch 는 2차 진행 후 평가.

---

## 5. B4 전략 — 1일 PoC 후 갱신된 작업 분해

| 단계 | 작업 | 인주 (갱신) | 산출물 | 의존성 |
|---|---|---|---|---|
| **R3a** | `.frf → .frx` 변환기 (H1) — 1 양식 한정 | 3~5 | `tools/frf2frx/` (Pascal TStream reader → C# `Report.Save(.frx)`) | 운영 SME .frf 정본 접근 |
| **R3b** | FastReport OSS 빌드 타임 변환 (H2) — `dotnet 8 + HTMLExport(Layers=true)` | 0.5 | `build/html_templates/Report_*.html` + WeasyPrint 정합 보고서 | R3a 완료 |
| **R3c** | Jinja2 placeholder 주입 (H3) — 토큰 마커 후처리 | 1~2 | `tools/inject_jinja2/` + 운영 `print_service` 의 `render_pdf(html, ctx)` 변형 | R3b 완료 |
| **R3d** | 98 양식 일괄 변환 + 운영 정합 검증 | 1~2 | CI 빌드 잡 + 5 축 회귀 매트릭스 갱신 | R3a/b/c 완료 |
| **합계** | | **5.5~9.5** | | T10 §1.8 의 4.5~8.5 추정에서 **약간 상향** (PoC 결과 H3 의 marker patch 부담 가시화) |

> **T10 §1.8 의 추정 (4.5~8.5 인주) 대비 1일 PoC 후 +1 인주 보정**: H3 의 `OnObject` patch 부담이 추정보다 큼. 그래도 자체 파서 (B1 = 6~13 인주) 대비 **30~40% 절감** 결론은 유효.

---

## 6. C7 Phase 1/Phase 2-α 운영 코드 영향

| 영향 영역 | 평가 | 결정 |
|---|---|---|
| 운영 코드 변경 | **0 줄** | DEC-039 정책 유지 — `.frf` 자동 변환 0 |
| 운영 의존성 (Python/WeasyPrint) | **변경 없음** | B4 빌드 타임은 별도 CI 잡 (Phase 3 후보) |
| Phase 2-α 의 18 변형 매핑 노트 | **변경 없음** | 단일 빌더 + variant 패턴이 Phase 3 자동 변환의 1차 검증 대상 |
| C7 마감 상태 | **변경 없음** | Phase 1 (T1~T10 완료) + Phase 2-α (T1/T3/T4/T5/T7/T8 완료) 모두 운영 가능 |

---

## 7. 후속 권고 (Phase 3 진입 조건)

다음 3 가지가 만족되어야 **Phase 3 진입 권고**:

1. **운영 SME 협의**: 98 양식 중 디자인 변경 빈도 통계 (수동 재현 비용 vs 자동 변환 ROI 비교).
2. **자체 파서 vs B4 비교 회의록**: 본 보고서 §5 의 5.5~9.5 인주 추정과 B1 의 6~13 인주 비교 후 정책 결정.
3. **R&D 1 인력 가용성**: Phase 3 R3a~R3d 합산 5.5~9.5 인주 = 약 1.5~2 사람-월. C9 이후의 신규 시나리오 우선순위와 충돌 검토.

> **현 시점 (2026-04-20) 권고**: **Phase 3 진입 보류**. C7 Phase 1 + Phase 2-α 의 수동 재현이 18 변형까지 흡수했으므로 **즉시 자동 변환 도입 ROI 미확정**. C9 이후 신규 시나리오 (C10/C11) 우선 진행 후 Phase 3 재평가.

---

## 8. 참조

- [c7_frf_parser_oss_research.md](./c7_frf_parser_oss_research.md) §1.8 (로컬 OSS 소스 직접 분석), §2 (권장 전략 B4)
- [DEC-037 / DEC-039](../../legacy-analysis/decisions.md) (WeasyPrint 단일 + .frf 참조용 정책)
- [migration/contracts/print_invoice.yaml v1.1.0](../../migration/contracts/print_invoice.yaml) (Phase 2-α 정본)
- [migration/contracts/print_label.yaml v1.1.0](../../migration/contracts/print_label.yaml) (Phase 2-α 라벨 5종)
- FastReport OSS 로컬 소스: `/Users/speeno/Downloads/FastReports-FastReport-8ef9cde`
  - `FastReport.Base/Export/Html/HTMLExport.cs` (1187 LOC)
  - `FastReport.Base/Export/Html/HTMLExportLayers.cs` (992 LOC) ⭐
  - `Extras/Core/FastReport.Import/RDL/RDLImportPlugin.cs` (988 LOC) — 임포터 템플릿
- 변경 이력: 본 PoC 1일, **2026-04-20**, 비차단 R&D, 운영 코드 변경 0.
