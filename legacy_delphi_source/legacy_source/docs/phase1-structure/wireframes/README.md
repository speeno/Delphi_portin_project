# Wireframes (DFM-based SVG)

텍스트 `.dfm`의 `Left` / `Top` / `Width` / `Height`를 이용한 **대략적인 배치 스케치**입니다. Delphi 실제 화면과 픽셀 단위로 일치하지 않으며, **전체 레이아웃 파악**용입니다.

## 재생성

저장소 루트 `도서유통-New`에서:

```bash
# 먼저 12-screen-specification.csv 필요
python3 debug/generate_screen_specification.py

# 우선순위 화면(메뉴 연결·시작 CreateForm·TDBGrid 다수 등)
python3 debug/generate_wireframes.py

# 스펙에 있는 Form/Frame 전부
python3 debug/generate_wireframes.py --all

# 개수 제한(스모크 테스트)
python3 debug/generate_wireframes.py --max 15
```

## 파일

- 행마다 `{instance}.svg` 한 개(예: `Sobo21.svg`).
- **바이너리 DFM**(예: `Base01`): CSV만 있는 경우 **placeholder** 레이아웃(컴포넌트 수).

## 관련

- [12-screen-specification.md](../12-screen-specification.md)
- [11-screen-business-flows.md](../11-screen-business-flows.md)
- [00-wireframe-coverage-gap.md](../00-wireframe-coverage-gap.md)
- [`debug/generate_wireframes.py`](../../../debug/generate_wireframes.py)
