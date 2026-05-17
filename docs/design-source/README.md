# docs/design-source/

북이오웍스(Bukioworks) 디자인 가이드의 **추출 원문 + 보관본**.
편집·해석한 단일 원천(SSOT) 은 [`docs/Design.md`](../Design.md) 이며, 본 폴더는 그 출처와 diff 추적용 원자료를 둔다.

## 파일

| 파일 | 출처 | 용도 |
|------|------|------|
| `bukioworks-guide-extract.txt` | [docs/북이오웍스_디자인_가이드.pdf](../북이오웍스_디자인_가이드.pdf) (8 page PDF) — 2026-05-11 추출 | Design.md 작성·검증 시 원문 대조 |
| `color-palette.json` | 위 PDF §Color System 표 | 색상 토큰 자동 매핑·테스트용 구조 데이터 |

## 정책

- 본 폴더 자료는 **내부용** 보관본이다. 외부 유포 금지.
- PDF 가 갱신되면 새 추출본을 `bukioworks-guide-extract-YYYYMMDD.txt` 형식으로 추가하고 README 표를 갱신한다.
- Design.md 의 토큰 값과 본 폴더 색상이 어긋나면 **PDF → Design.md → globals.css** 순으로 진실 우선순위를 따른다.
