# DFM → HTML 레이아웃 미리보기 한계

HTML 미리보기(`tools/dfm_layout_to_html.py`)는 **포팅 참고용 근사치**이며, 델파이 VCL과 1:1로 일치하지 않는다. 단일 진실은 가능한 한 **레이아웃 JSON + `layout_ir`**(파서·`dfm_layout_ir` 출력)에 두는 것을 권장한다.

## 레이아웃 엔진 선택 (`legacy` vs `dfm2html`)

- **legacy**([`dfm_parser.parse_dfm_layout`](../tools/parsers/dfm_parser.py)): 줄 병합(`dfm_merge_blocks`) + 인벤토리/분석 파이프라인과 동일한 구현. 기본값.
- **dfm2html**([`dfm2html_layout_adapter.parse_dfm_layout_via_dfm2html`](../tools/dfm2html_layout_adapter.py)): [`tools/dfm2html_project`](../tools/dfm2html_project) 의 `DfmParser` AST로 동일 스키마의 레이아웃 JSON 을 만든다. `Columns = < … >` 등은 파서 내부에서 구조화되므로 그리드 열이 더 잘 채워질 수 있다. 인코딩은 `read_delphi_source` 로 통일한다.
- **보내기**: [`dfm_layout_export.py`](../tools/dfm_layout_export.py) 에 `--engine legacy|dfm2html` 과 선택 `--pas`(또는 stem 동명 `.pas` 자동)로 `pas_resourcestrings` 를 JSON에 붙일 수 있다.
- **HTML/CSS 전용 변환기**: `dfm2html_project` CLI(`python -m dfm2html.cli.main`)는 별도 산출물(폼별 `.html`/`.css`/메타)을 만든다. 레이아웃 JSON 경로와 혼동하지 말 것.

## 파서

- **이진 DFM**(TPF0 헤더): 텍스트 파서가 처리하지 않으며, `parse_error`와 `root: null` 형태로 반환된다. 텍스트 DFM으로 변환한 뒤 분석한다.
- **좌표 식**: `Width = ClientWidth - 8` 등은 숫자 리터럴만 `px`로 쓰이며 식은 평가하지 않는다.
- **괄호/중괄호 블록**: `Items.Strings`, `Glyph.Data` 등은 줄 병합으로 대부분 수집하지만, 문자열 안의 괄호·중괄호가 깊이 계산을 교란하는 변형 포맷은 여전히 취약할 수 있다.
- **컬렉션 `< … >`**: `Columns = < item … end … >` 는 줄 병합 후 `grid_columns`(FieldName·Title.Caption)로 요약된다. 파싱은 정규식 기반이라 비표준 `item` 블록은 누락될 수 있다.

## 문자열·리소스 ID

- **DFM 문자열**: `Caption`/`Text`/`Hint`는 `#13#10`·인접 `'…'` 리터럴 결합을 [`delphi_string_normalize.py`](../tools/parsers/delphi_string_normalize.py) 규칙으로 정규화해 JSON·HTML에 반영한다.
- **리소스 전용 문자열**: 숫자 ID만 있고 DFM에 문구가 없으면 파서가 알 수 없다. 텍스트 `.rc`의 `STRINGTABLE` 줄을 [`tools/res_string_bridge.py`](../tools/res_string_bridge.py)로 읽어 ID→문자열 dict 를 만든 뒤, PAS/별도 단계에서 조인하는 설계를 쓴다(바이너리 `.res`는 변환 후 동일). 동일 모듈의 `extract_resourcestrings_from_pas` 는 `dfm2html_project` 의 `resourcestring` 스캔을 `.pas` 에 적용한다.
- **라벨 폴백(HTML)**: `Caption` → `Text` → `Hint` → (버튼·라벨·체크박스) 컴포넌트 **이름** → 타입명 순이다. 글리프만 있는 버튼은 이름이 있으면 그 이름을 쓴다.

## 레이아웃 IR·CSS

- **Align / Anchors**: 일부 값만 규칙 테이블로 매핑한다(`alClient`, 좌우/상하 앵커 조합 등). `alNone`, 스플리터, MDI, 스크롤 영역은 근사 또는 미반영이다.
- **TabOrder → z-index**: 같은 부모 자식 사이에서만 순서를 매기며, 델파이의 실제 포커스 순서·탭 스톱과 다를 수 있다.
- **DPI / PixelsPerInch**: JSON에는 남기지만 HTML 단계에서는 스케일을 완전히 반영하지 않는다.

## 컴포넌트·그리드

- **레지스트리**(`tools/dfm_component_registry.json`): 프로젝트에만 있는 3rd-party 타입은 목록에 추가해야 한다.
- **TPageControl**: 탭 스트립 + 패널 스택 형태의 **정적 근사**이며, 런타임 탭 전환·테마는 없다.
- **그리드**: 레이아웃 JSON에 `grid_columns`가 있으면 `Title.Caption`(없으면 FieldName)으로 헤더 행을 그린다. 없을 때만 A/B/C 플레이스홀더를 쓴다.

## 시각 회귀

- `tools/dfm_layout_visual_regression.py`는 Playwright·Chromium 및 `debug/dfm_layout_html_to_png.py`에 의존한다. OS·폰트·렌더링 차이로 **픽셀 단위 비교는 flaky**할 수 있으므로 CI에서는 `workflow_dispatch` 등 선택 실행을 권장한다.
- 기준 PNG 갱신: `DFM_VISUAL_UPDATE=1` 환경 변수와 함께 실행한다.

## 관련 문서·스크립트

- 분석 절차 내 레이아웃 도구 안내: [`delphi-source-analysis-procedure.md`](delphi-source-analysis-procedure.md) §3.1
- 포괄적 위험 목록: [`../legacy-analysis/known-risks.md`](../legacy-analysis/known-risks.md)
- Subu36 감사(JSON): `python3 debug/dfm_layout_audit_subu36.py` → [`debug/subu36_layout_audit.json`](../debug/subu36_layout_audit.json)
