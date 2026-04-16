# Delphi → Web Porting Accelerator

이 프로젝트는 두 가지를 함께 제공합니다.

1. **Next.js + FastAPI 기반의 포팅 예시 앱**
   - `Seak04` 우편번호 검색 화면 → `frontend/app/postcodes`
   - `Subu36` 반품수거내역 화면 → `frontend/app/pickups`
2. **DFM/PAS를 읽어 기본 HTML 레이아웃을 생성하는 Python 변환기**
   - `dfm2web`
   - 표준/커스텀 VCL 컨트롤을 웹용 기본 레이아웃으로 정규화

## 폴더 구성

- `frontend/` : Next.js App Router 기반 화면
- `backend/` : FastAPI CRUD API 예시
- `dfm2web/` : DFM/PAS → HTML/JSON 변환기
- `examples/source/` : 실제 입력 예시(`Seak04`, `Subu36`)
- `examples/generated/` : 변환 결과물

## 빠른 시작

### 1) 프런트엔드

```bash
cd frontend
npm install
npm run dev
```

환경 변수 예시:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### 2) 백엔드

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 3) DFM 변환기 실행

단일 변환:

```bash
python -m dfm2web.cli convert \
  --dfm examples/source/Seak04.dfm \
  --pas examples/source/Seak04.pas \
  --out examples/generated/seak04
```

일괄 변환:

```bash
python -m dfm2web.cli batch \
  --src examples/source \
  --out examples/generated/batch
```

소스 **루트에만** 있는 `.dfm`만 변환(하위 `Data/` 등 제외):

```bash
python -m dfm2web.cli batch \
  --src /path/to/legacy_source \
  --out examples/generated/legacy_root \
  --root-only
```

리소스 문자열(`.rc` STRINGTABLE)을 적용해 숫자 ID 대신 실제 문자열로 치환:

```bash
python -m dfm2web.cli convert \
  --dfm Subu36.dfm --pas Subu36.pas \
  --rc strings1.rc --rc strings2.rc \
  --out output/Subu36

python -m dfm2web.cli batch \
  --src /path/to/legacy_source \
  --out examples/generated/batch \
  --rc /path/to/strings.rc
```

`--rc`를 생략하면 기존과 동일하게 동작합니다(회귀 안전). 바이너리 `.res`는 `brcc32` 등으로 `.rc`로 변환 후 같은 파이프라인을 사용합니다.

배치가 끝나면 출력 루트에 `reports/`가 생성됩니다.

- `reports/unsupported_component_ratio.json` — 폼별·클래스별 미지원 비율
- `reports/event_binding_coverage.json` — 이벤트/바인딩 노드 수·핸들러 수 요약
- `reports/porting_summary.md` — 사람이 읽기 쉬운 요약

## 설계 포인트

- **UI 재현**: DFM의 `Left/Top/Width/Height`, `Align`, `Caption`, `Font`, `Visible`, `Enabled`를 중심으로 HTML/CSS를 생성
- **소스 참조**: 같은 이름의 `.pas`가 있으면 이벤트 핸들러, `resourcestring`, 런타임 속성 변경 패턴을 함께 분석
- **누락 최소화**: 정규화 JSON(`*.form.json`)에 원본 `rawProps`와 데이터 바인딩(`DataSource`, `DataField` 등)을 유지해 1차 포팅에서 비즈니스 로직/DB 연결 단서를 보존
- **미지원 컴포넌트 근사**: `visualType=unsupported`라도 `renderType`(button/panel/input 등)로 최대한 유사한 골격을 렌더링하여 추후 디자인 교체를 쉽게 함
- **실무 전략**: DFM은 “기본 틀 자동 생성”, 비즈니스 로직과 복잡한 커스텀 컨트롤은 “후처리/수동 포팅”으로 분리

## 현재 지원 범위

- 레이아웃 컨테이너: `TForm`, `TPanel`, `TFlatPanel`
- 입력: `TEdit`, `TFlatEdit`, `TFlatMaskEdit`, `TFlatNumber`, `TDateEdit`, `TMemo`
- 버튼: `TButton`, `TFlatButton`, `TFlatSpeedButton`, `TBitBtn`, `TdxButton`
- 표시: `TLabel`, `TmyLabel3d`
- 그리드: `TDBGrid`, `TDBGridEh`, `TStringGrid`
- 기타: `TProgressBar`, `TFlatProgressBar`, `TCheckBox`, `TRadioButton`, `TGroupBox`

지원하지 않는 컨트롤은 리포트에 기록되고, 화면에는 placeholder로 렌더링됩니다.
