# 북이오웍스 — CMS 디자인 자산 요청서 (Phase B 차단 해제용)

> 본 문서는 도서물류관리프로그램 CMS 적용을 위한 **로고·파비콘 자산 패키지** 요청 양식이다.
> 디자인/브랜드 담당에게 그대로 전달해 사용한다. 코드 적용 후 자산 파일은
> [`도서물류관리프로그램/frontend/public/brand/`](../도서물류관리프로그램/frontend/public/brand/) 에 동일 파일명으로 배치된다.
>
> 근거: [`docs/Design.md`](Design.md) §2 로고 · [`docs/design-rollout-plan.md`](design-rollout-plan.md) §1.1 디렉터리 구조.

## 0. 회신 마감 / 전달 방식

| 항목 | 값 |
|------|------|
| 마감 | (요청일 + 10영업일 내 권장) |
| 전달 | 압축 ZIP 1개. 폴더 구조는 §1 표와 동일 |
| 라이선스 | 사용 범위 명기 (CMS 한정 vs 마케팅 공용) — 미명기 시 CMS 한정으로 간주 |
| 소스 파일 | (선택) Figma / AI / Sketch 원본 링크 — 후속 보정용 |

## 1. 파일 목록 (필수)

| 분류 | 파일명 (필수) | 포맷 / 크기 | 용도 |
|------|------------------|-------------|------|
| Symbol | `bukioworks-symbol.svg` | SVG, viewBox 1:1 | 사이드바 헤더, 메뉴, 프로필 fallback |
| Symbol (다중 PNG) | `bukioworks-symbol-32.png` `-96.png` `-192.png` | PNG, 32 / 96 / 192 px | SVG 미지원 환경, 앱 아이콘 |
| Wordmark | `bukioworks-wordmark.svg` | SVG, viewBox 가로 길이 명시 | 로그인 카드, CMS 헤더 |
| Wordmark (다크용) | `bukioworks-wordmark-dark.svg` | SVG, 흰색·라임 위에서도 가독 | Dark Filled 영역 / 다크 모드 |
| favicon | `favicon.svg` | SVG, 16 / 32 px 모두에서 식별 가능 | 모던 브라우저 탭 |
| favicon (래스터) | `favicon-16.png`, `favicon-32.png` | PNG | 레거시 브라우저 fallback |
| iOS 홈 화면 | `apple-touch-icon-180.png` | PNG, 180 × 180 px, 모서리 여백 12 % | iOS Add to Home |

## 2. 파일 목록 (선택)

| 파일명 | 포맷 / 크기 | 용도 |
|--------|-------------|------|
| `og-default.png` | PNG, 1200 × 630 px | OpenGraph 기본 썸네일 (마케팅 공유) |
| `bukioworks-symbol-mono-dark.svg` | SVG | 단색 다크 변형 (옵션 컴포넌트용) |
| `bukioworks-symbol-mono-light.svg` | SVG | 단색 라이트 변형 |

## 3. 디자인·기술 조건

- **색**: 가이드 §3 기준. Symbol 단색은 Bukio Black `#282828` 권장. 라임 배경(`#E0FF00`) 또는 다크 배경(`#282828`) 위에서도 식별되는 별도 변형을 다크용으로 별도 제출.
- **여백**: PDF에 “최소 여백” 수치가 있으면 동일 비율 적용. 없을 경우 사이드바 32 px·파비콘 16 px에서 윤곽이 깨지지 않도록 보수적으로.
- **SVG 작성 규칙**:
  - `viewBox` 명시 / 절대 좌표 금지.
  - `<style>` 인라인이 아닌 `fill`/`stroke` 속성 권장 (Tailwind `currentColor` 호환을 위해 단색 변형은 `fill="currentColor"` 옵션도 고려).
  - 텍스트는 **아웃라인** (path 변환)으로 제출 — 폰트 누락 방지.
- **접근성**: alt 텍스트 권장 문구 (예: “북이오웍스 도서물류 CMS”) 함께 명기.
- **상표·라이선스**: 외부 노출 가능 여부와 사용 가이드(축소 한계, 색 변형 허용 여부) 1줄 명시.

## 4. 검수 기준 (수령 후 개발 측 확인)

- [ ] 16 px 파비콘에서 심볼 식별 가능 (식별 어려우면 simplified 마크 별도 요청).
- [ ] 다크 배경 위 워드마크 가독성 확인 (Dark Filled 영역).
- [ ] 192 / 180 px PNG에서 픽셀 어긋남 없음 (앱 아이콘·iOS 홈).
- [ ] SVG 파일 단독 미리보기 시 색상·여백 PDF 가이드와 일치.
- [ ] 라이선스·사용 범위 회신 명기 확인.

## 5. 코드 적용 후 진입점 (참고)

자산 수령 후 단일 진입점은 다음 모듈에서만 import 한다 — 헤더/사이드바/로그인은 직접 SVG 인라인을 추가하지 않는다.

```text
도서물류관리프로그램/frontend/src/components/brand/Logo.tsx   ← 신설 (자산 입수 후)
도서물류관리프로그램/frontend/src/app/layout.tsx              ← metadata.icons 갱신
```

## 6. 회신 양식 (브랜드 담당 → 개발)

```text
[북이오웍스 디자인 자산 회신]
- ZIP 첨부: bukioworks-cms-brand-vYYYY-MM-DD.zip
- 사용 범위: (CMS 한정 / 마케팅 공용)
- 소스 파일 링크: (Figma 등 / 없음)
- 특이사항: (16 px simplified 별도 / 다크 변형 미포함 등)
```
