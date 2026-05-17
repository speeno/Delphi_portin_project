# Design Phase B — 자산 입수 전 선스캐폴드 회귀 매트릭스

> 자산 (`/brand/*`) 도착 전 단계에서 **진입점 단일화 + 변형 추가 + 메타 텍스트** 만 미리 두는 PR 의 회귀 가드 결과.
> 자산 도착 시 `Logo.tsx` 의 `ASSETS_PENDING = false` 토글 + `layout.tsx` 의 `metadata.icons` 활성화로 시각이 한 번에 들어온다.

작업일: 2026-05-11
참조: [`docs/design-rollout-plan.md`](../../docs/design-rollout-plan.md) §3, [`docs/Design.md`](../../docs/Design.md) §2·§6

## 1. 변경 파일

| 파일 | 변경 |
|------|------|
| [`도서물류관리프로그램/frontend/src/components/brand/Logo.tsx`](../../도서물류관리프로그램/frontend/src/components/brand/Logo.tsx) | **신설** — `<Logo variant="symbol" \| "wordmark" tone="default" \| "dark" size="sm" \| "md" \| "lg" />`. 자산 부재 시(`ASSETS_PENDING = true`) placeholder 로 헤더의 책 SVG 동등 도형을 그려 시각 회귀 0. 자산 도착 시 한 줄 토글로 `<img src="/brand/...">` 전환. |
| [`도서물류관리프로그램/frontend/src/components/ui/button.tsx`](../../도서물류관리프로그램/frontend/src/components/ui/button.tsx) | `cva variants` 에 `brand-primary` 추가 (Vivid Lime + 검정 텍스트 + 라임 hover). `cva sizes` 에 `brand` 추가 (Full Pill, h-50, px-6, text-18, font-semibold, gap-3, svg-20). 기존 `default` variant 무변경. |
| [`도서물류관리프로그램/frontend/src/app/layout.tsx`](../../도서물류관리프로그램/frontend/src/app/layout.tsx) | `metadata.title` 을 "도서물류관리 · 북이오웍스" 로, `description` 을 가이드 톤으로 갱신. `icons`/`openGraph` 는 자산 입수 후 활성화 (주석으로 명시). |

호출자(`header.tsx`/`sidebar.tsx`/`(public)/login/page.tsx`/`BrandHero.tsx`) 는 **본 PR 에서 수정하지 않음** — 시각 회귀를 0으로 유지하고, 자산 도착 후 별도 작은 PR 로 import 만 교체한다.

## 2. 자동 회귀 가드

| 가드 | 명령 | 결과 |
|------|------|------|
| Type 체크 | `npx tsc --noEmit` | PASS (Exit 0) |
| 신규 컴포넌트 lint | `ReadLints` (Logo / button / layout) | 0건 |
| Build | `npm run build` (Phase A 직후 동일) | PASS |
| 하드코딩 HEX | `rg -n '#[0-9a-fA-F]{6}\b' 도서물류관리프로그램/frontend/src --type tsx` | 화이트리스트 외 0건 (`button.tsx` 의 `oklch(0.83_0_0)` 는 OKLCH 표기로 HEX 검사 대상 아님) |

## 3. 자산 도착 후 활성화 절차 (체크리스트)

자산 ZIP 이 [`docs/design-asset-request.md`](../../docs/design-asset-request.md) §1 표대로 도착하면:

- [ ] `frontend/public/brand/` 에 풀어 배치한다.
- [ ] [`Logo.tsx`](../../도서물류관리프로그램/frontend/src/components/brand/Logo.tsx) 의 `const ASSETS_PENDING = true;` → `false`.
- [ ] [`layout.tsx`](../../도서물류관리프로그램/frontend/src/app/layout.tsx) `metadata.icons` 와 (선택) `openGraph.images` 를 [`design-rollout-plan.md`](../../docs/design-rollout-plan.md) §1.2 표대로 활성화.
- [ ] [`header.tsx`](../../도서물류관리프로그램/frontend/src/components/app-shell/header.tsx) L78–82 인라인 책 SVG → `<Logo variant="wordmark" size="sm" />`.
- [ ] [`sidebar.tsx`](../../도서물류관리프로그램/frontend/src/components/app-shell/sidebar.tsx) L172–193 의 `BookOpen` placeholder → `<Logo variant="symbol" size="sm" />` (단, `user.logo_url` 우선 정책 유지).
- [ ] [`(public)/login/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(public)/login/page.tsx) L83 `<MascotMotif />` → `<Logo variant="wordmark" size="md" />`.
- [ ] [`BrandHero.tsx`](../../도서물류관리프로그램/frontend/src/components/brand/BrandHero.tsx) `<MascotMotif />` → `<Logo variant="symbol" />` 로 옵션 분기.
- [ ] (정리 PR) `MascotMotif.tsx` 와 `--brand-warm*` 토큰 제거 ([`design-gap-analysis.md`](../../docs/design-gap-analysis.md) §1.4).

## 4. 사람 검증 (자산 입수 후 PR 에서)

- [ ] 16 px 파비콘에서 심볼 식별 가능.
- [ ] 다크 배경 위 워드마크(`tone="dark"`) 가독성.
- [ ] 로그인 카드의 워드마크가 한 줄에 안전하게 들어감 (`size="md"` 기준).
- [ ] 한 화면 라임 `brand-primary` 1개 원칙 검증 (등록 패널의 신규/저장/삭제 분리).

## 5. PR 본문 템플릿 (선스캐폴드)

```text
제목: feat(brand): phase B prescaffold — Logo entry point + brand-primary button (assets pending)

요약:
- Logo.tsx 신설 (variant=symbol|wordmark, tone=default|dark, size).
  ASSETS_PENDING=true 동안은 헤더의 책 SVG 동등 placeholder 를 그려 시각 회귀 0.
- button.tsx variants.brand-primary + sizes.brand 추가 (사용처 없음 — 자산 후 PR 에서 로그인 CTA 부터 적용).
- layout.tsx metadata title/description 만 가이드 톤으로 갱신. icons/openGraph 는 자산 후.

자동 가드:
- npx tsc --noEmit PASS
- ReadLints 0건
- npm run build PASS (Phase A 직후 동일)
- rg 화이트리스트 외 신규 HEX 0건

후속: 자산 도착 시 §3 체크리스트 한 번에 진행 (header/sidebar/login/Brand Hero 교체 + ASSETS_PENDING 토글).
```
