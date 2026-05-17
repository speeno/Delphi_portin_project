# Design Gap Analysis — 북이오웍스 가이드 vs 현재 구현

> 본 문서는 [`docs/Design.md`](Design.md) (단일 원천) 와 현재 코드 (`globals.css`·앱 셸·로그인 페이지) 의 차이를 **행 단위**로 정리한다.
> 실제 변경은 Phase A → B → C 순으로 별도 PR 로 분리한다 ([`docs/Design.md` §7 / 하단 Phase 섹션](Design.md#7-globalscss-매핑-현재값--목표값)).

조사일 2026-05-11 — 추출/대조 대상 파일은 본문 표에 절대경로로 명기.

---

## 1. globals.css 토큰 대조

대상: [`도서물류관리프로그램/frontend/src/app/globals.css`](../도서물류관리프로그램/frontend/src/app/globals.css)

### 1.1 변경 필요 (Phase A 의 핵심)

| 토큰 | 현재 (oklch) | 가이드 매핑 | 변경 사유 |
|------|--------------|-------------|-----------|
| `--primary` | `oklch(0.38 0.10 258)` Indigo → Phase A 라임 | Bukio Black `#282828` → `oklch(0.275 0 0)` | **가독성 보정**: shadcn `primary` 는 텍스트·아이콘·subtle 배경 전역 시맨틱이라 Vivid Lime 배치 금지 |
| `--primary-foreground` | `oklch(0.99 0 0)` 흰색 → Phase A 검정 | Inverse Text `#F5F5F5` → `oklch(0.965 0 0)` | 다크 필 버튼 위 텍스트 |
| `--link` | (없음) | Info 계열 다크 링크 `oklch(0.46 0.08 245)` | 텍스트 링크/hover 를 `--primary` 와 분리 |
| `--ring` | `oklch(0.55 0.10 258)` Indigo → Phase A 라임 | Info Blue 계열 `oklch(0.62 0.08 245)` | 포커스 링은 라임 대신 차분한 정보색으로 가독성 확보 |
| `--accent` | `oklch(0.74 0.13 38)` Coral | Pale Sky `#F4FFFF` → `oklch(0.99 0.012 200)` | 코랄 누락. 가이드는 페일 스카이가 보조 표면 |
| `--accent-foreground` | `oklch(0.20 0.04 40)` | `#282828` → `oklch(0.275 0 0)` | hue 중립화 |
| `--secondary` | `oklch(0.96 0.012 80)` | Pale Lime `#FCFFE9` → `oklch(0.99 0.04 110)` | 라이트 섹션 배경 톤 |
| `--secondary-foreground` | `oklch(0.28 0.04 258)` | `#282828` → `oklch(0.275 0 0)` | — |
| `--foreground` / `--card-foreground` / `--popover-foreground` | `oklch(0.20 0.025 260)` | `#282828` → `oklch(0.275 0 0)` | hue 제거 |
| `--muted-foreground` | `oklch(0.50 0.02 258)` | `#555555` → `oklch(0.42 0 0)` | Secondary Text 정확값 |
| `--border` | `oklch(0.90 0.012 80)` | Bukio Gray `#E6E6E6` → `oklch(0.92 0 0)` | hue 제거 |
| `--input` | `oklch(0.93 0.010 80)` | `#E6E6E6` 계열 → `oklch(0.93 0 0)` | 동상 |
| `--destructive` | `oklch(0.58 0.22 28)` 진한 빨강 | Error Red `#FFA8A8` → `oklch(0.81 0.10 22)` | 페일톤 ↓ (CMS 전반 차분 톤) |
| `--status-ok` | `oklch(0.62 0.17 155)` | Positive Green `#8EC8CD` → `oklch(0.78 0.045 200)` | 페일톤 ↓ |
| `--status-warn` | `oklch(0.74 0.16 65)` | Warning Orange `#FFC1A0` → `oklch(0.84 0.08 50)` | 페일톤 ↓ |
| `--status-info` | `oklch(0.55 0.13 258)` | Info Blue `#B6D3F5` → `oklch(0.85 0.06 245)` | 페일톤 ↓ |
| `--sidebar` | `oklch(0.975 0.008 258)` | Neutral Gray `#F5F5F7` → `oklch(0.965 0.003 264)` | hue 중립화 |
| `--sidebar-foreground` | `oklch(0.24 0.03 258)` | `#282828` → `oklch(0.275 0 0)` | — |
| `--sidebar-primary` | `oklch(0.38 0.10 258)` → Phase A 라임 | Bukio Black `#282828` → `oklch(0.275 0 0)` | 사이드바 로고/아이콘 강조는 읽기 가능한 다크 톤. active 배경은 `--sidebar-accent` 사용 |
| `--sidebar-primary-foreground` | `oklch(0.99 0 0)` → Phase A 검정 | Inverse Text `#F5F5F5` → `oklch(0.965 0 0)` | 다크 강조 위 텍스트 |
| `--sidebar-accent` | `oklch(0.93 0.03 258)` | Pale Lime → `oklch(0.99 0.04 110)` | hue 변경 |
| `--sidebar-border` | `oklch(0.91 0.015 258)` | `#E6E6E6` → `oklch(0.92 0 0)` | hue 제거 |
| `--sidebar-ring` | `oklch(0.55 0.10 258)` | Lime hover → `oklch(0.88 0.18 122)` | 동상 |

### 1.2 신규 토큰 (가이드에는 있으나 현재 미정의)

| 신규 토큰 | 값 (oklch) | HEX | 용도 |
|-----------|------------|------|------|
| `--vivid-lime` | `oklch(0.95 0.20 122)` | `#E0FF00` | Primary Filled 본색·NOTICE 알림 본색 |
| `--vivid-lime-hover` | `oklch(0.88 0.18 122)` | `#C9E500` | Primary Filled hover |
| `--vivid-sky` | `oklch(0.93 0.10 195)` | `#5EFFFF` | IMPORTANT 알림 한정 |
| `--accent-red` | `oklch(0.93 0.025 25)` | `#FFE3DF` | 중요도 낮은 강조 (서브 라벨 배경) |
| `--radius-pill` | `9999px` | — | Full Pill 버튼 코너 (가이드 §6) |
| `--link` | `oklch(0.46 0.08 245)` | Info Blue 의 텍스트용 다크 변형 | 링크/hover 전용. `--primary` 의 전역 가독성 문제를 방지 |

### 1.3 유지 (가이드와 충돌 없음)

| 토큰 | 값 | 메모 |
|------|------|------|
| `--background` | `oklch(0.985 0.005 80)` | 가이드 White(#FFFFFF) 와 거의 동등. 그대로 두거나 `oklch(1 0 0)` 로 미세 정렬 (선택) |
| `--card` / `--popover` | `oklch(1 0 0)` | 일치 |
| `--muted` | `oklch(0.965 0.008 80)` | Subtle Gray 와 동등 |
| `--radius` | `0.625rem` | 카드/입력 기본 라운드 — Full Pill 은 별도 토큰으로 추가 |
| `--font-sans` | `Pretendard Variable, …` | 가이드 §4 와 일치 (유지) |

### 1.4 폐기 검토

| 토큰 | 사용처 (rg 결과) | 결정 |
|------|------------------|------|
| `--brand-warm` | 2026-05-11 가독성 보정 후 컴포넌트 사용 0건 | Phase A.1 PR 에서 변수 자체 제거 가능. `MascotMotif.tsx` 는 `fill-secondary` / `fill-vivid-lime` 로 이전 완료. |
| `--brand-warm-foreground` | 컴포넌트에서 0회 | 위와 동시 제거 |
| `--font-heading` | 현재 `var(--font-sans)` 와 동일 | 유지 (Outfit 도입 시 분리할 진입점으로 남김) |

> 폐기는 **그레이스 PR** 으로 따로 진행 — 외부에서 className 으로 참조될 가능성 있어 코드 일제 삭제 전에 한 사이클 deprecated 표시 권장.

---

## 2. 앱 셸 컴포넌트 — 브랜드 노출 위치 인벤토리

| 위치 | 파일 | 현재 표현 | Phase B 변경 |
|------|------|-----------|--------------|
| 사이드바 헤더 (대표 로고 + "도서물류관리" + 부제) | [`도서물류관리프로그램/frontend/src/components/app-shell/sidebar.tsx`](../도서물류관리프로그램/frontend/src/components/app-shell/sidebar.tsx) 브랜드 행 | `user.logo_url` 우선 → 없으면 `<Logo variant="symbol" appearance="cms" />` (`bg-muted`·`ring-border`·`BookOpen`). 부제: 「운영 · 관리」+ 계정 라벨(있을 때) | 랜딩과 분리된 CMS 톤 완료. 테넌트 로고 URL 시 `<img>` 유지 |
| 헤더 좌측 ("도서물류관리" + 심볼) | [`도서물류관리프로그램/frontend/src/components/app-shell/header.tsx`](../도서물류관리프로그램/frontend/src/components/app-shell/header.tsx) 좌측 버튼 | `<Logo variant="symbol" appearance="cms" />` + 텍스트「도서물류관리」(대시보드 이동·탭 닫기 동작 유지) | 마케팅 워드마크 PNG 미사용 — 앱 셸은 심볼+텍스트가 정보 밀도에 적합 |
| 사용자 아바타 fallback | 같은 파일 L113–115 | `bg-primary/10 text-primary` | `--primary` 를 Bukio Black 으로 되돌려 읽기 가능. 추후 `bg-secondary text-foreground` 으로 더 완화 가능 |
| 헤더 뱃지 (info / phase / status) | [`도서물류관리프로그램/frontend/src/components/brand/BrandBadge.tsx`](../도서물류관리프로그램/frontend/src/components/brand/BrandBadge.tsx) | `bg-primary/10 / bg-status-ok/15 / bg-status-info/10` | `phase` 는 라임이 아니라 다크 primary subtle 로 표현. 핵심 CTA 만 `brand-primary` |
| BrandHero (로그인·온보딩 등) | [`도서물류관리프로그램/frontend/src/components/brand/BrandHero.tsx`](../도서물류관리프로그램/frontend/src/components/brand/BrandHero.tsx) | `MascotMotif` + 그라데이션 블랍 | 마스코트 → Symbol 로고로 단순화 검토 (Phase B) |
| 마스코트 모티프 | [`도서물류관리프로그램/frontend/src/components/brand/MascotMotif.tsx`](../도서물류관리프로그램/frontend/src/components/brand/MascotMotif.tsx) | 자체 SVG | Logo SVG 가 Symbol 역할을 흡수하면 단계적 폐기 검토 |
| 탭바 / `TabBar` | [`도서물류관리프로그램/frontend/src/components/app-shell/tab-bar.tsx`](../도서물류관리프로그램/frontend/src/components/app-shell/tab-bar.tsx) | shadcn 기본 톤 | 토큰만 회전 (Phase A) |
| 위치권한 부트스트랩 / 글로벌 알림 | `app-shell/location-permission-bootstrap.tsx`, `components/ops/global-alert-banner.tsx` | shadcn `Alert`/`Toast` | 토큰만 회전 (Phase A) |

### 2.1 active sidebar 색상 (DEC 회귀 가드)

`Sidebar` 의 active 행은 `bg-sidebar-accent text-sidebar-accent-foreground` 만 사용 — **토큰만 회전하면 디자인 일치**. 컴포넌트 코드 변경 불필요.

### 2.2 공개 랜딩 적용 (2026-05-11)

| 위치 | 파일 | 적용 |
|------|------|------|
| 공개 메인 루트 | [`도서물류관리프로그램/frontend/src/app/(public)/page.tsx`](../도서물류관리프로그램/frontend/src/app/(public)/page.tsx) | 샘플 `bukioworks-cms-ui-sample` 의 마케팅 헤더·좌우 히어로·일러스트 카드·풋터 패턴 이식. `brand-primary` 는 히어로 CTA 1개만 유지 |
| 로고 단일 진입점 | [`도서물류관리프로그램/frontend/src/components/brand/Logo.tsx`](../도서물류관리프로그램/frontend/src/components/brand/Logo.tsx) | Wordmark PNG / Symbol placeholder 를 한 컴포넌트로 노출. SVG 자산 입수 시 이 파일만 교체 |
| 가이드 캡처 | [`도서물류관리프로그램/frontend/src/components/marketing/LandingGuideShowcase.tsx`](../도서물류관리프로그램/frontend/src/components/marketing/LandingGuideShowcase.tsx) | 운영 기본 노출 제외. `NEXT_PUBLIC_SHOW_DESIGN_GUIDE=1` 일 때만 내부 검수용으로 표시 |

---

## 3. 로그인 화면 (`(public)/login/page.tsx`) 대조

대상: [`도서물류관리프로그램/frontend/src/app/(public)/login/page.tsx`](../도서물류관리프로그램/frontend/src/app/(public)/login/page.tsx)

| 영역 | 현재 | Phase B 변경 |
|------|------|--------------|
| 배경 그라데이션 | `bg-gradient-to-br from-secondary via-background to-accent/20` | 토큰 회전으로 자동 적용 (Phase A) — 현재 코랄/blue 그라데이션 → Pale Sky/White/Pale Lime 톤 |
| 배경 블랍 | `bg-primary/6` + `bg-accent/10` | `--primary` 를 다크 톤으로 되돌린 뒤 과한 네온 블랍 제거. 필요 시 `bg-secondary/70` + `bg-accent/40` 으로 완화 |
| 카드 헤더 | `<MascotMotif size="sm" />` + 텍스트 "도서물류관리프로그램" | `<Logo variant="wordmark" />` 로 치환 + Mascot 제거 검토 (PDF Wordmark 권장 위치) |
| 로그인 버튼 | `<Button>` (shadcn 기본 = 다크 필) | **추가 작업**: 핵심 CTA 이므로 `<Button variant="brand-primary" size="brand">` 로 명시 적용. 라임은 명시 CTA 에만 사용 |
| "고급 — 회사 정보로 라우팅" 토글 텍스트 | `text-muted-foreground` | 토큰 회전 (Phase A) |
| 에러 박스 | `border-destructive/30 bg-destructive/5` | 토큰 회전 (Phase A) |
| 회원가입/계정찾기 링크 | `text-muted-foreground underline` | 토큰 회전 (Phase A) |

### 3.1 버튼 가이드 적용 (Phase B)

PDF §6 의 50px 높이·24px 좌우 패딩·full pill 은 현재 shadcn `Button` 기본 (`h-9 / px-4 / rounded-md`) 와 다름. 두 가지 선택지:

- (a) `Button` 에 `variant="brand-primary"` 신규 추가 → Tailwind 유틸로 `h-[50px] px-6 rounded-full text-[18px] font-semibold` 적용. 호환성 ↑.
- (b) 기존 `--radius` 를 `0.5rem → 9999px` 로 회전. 모든 버튼 영향 → **권장 안 함**.

본 가이드는 **(a) 신규 변형 추가** 를 권장.

---

## 4. 그 외 색상 하드코딩 점검 (rg 결과)

| 파일 | 라인 | 현재 HEX | 분류 | 조치 |
|------|------|-----------|------|------|
| `components/legacy-form/LegacyFormRenderer.tsx` | 74·88·93·128·239·266 | `#ececec`, `#d4d0c8`, `#e8e4dc`, `#c0bcb4` | **Delphi 미리보기 전용** — 레거시 회색 톤 재현 의도 | **유지** (가이드 §8 금지에서 제외 — 미리보기 의도 명시) |
| `components/dashboard/traffic-map-leaflet.tsx` | 53–90 | `#64748b`/`#dc2626`/`#ca8a04`/`#16a34a`/`#3b82f6` | 지도 마커·범례 — Tailwind 표준 컬러 | **차후 검토** (Sub Color 매핑 가능: Error Red/Warning Orange/Positive Green/Info Blue) |
| `components/stats/charts.tsx` | 82·90·125·127·145·189 | `#2563eb` `#16a34a` `#f59e0b` `#dc2626` `#9333ea` | 차트 시리즈 컬러 | Phase C 에서 `--chart-1~5` 토큰화 (Design.md §9 후속) |

---

## 5. Phase 분리 가이드 (요약)

| Phase | 범위 | 영향 |
|-------|------|------|
| **A · 토큰 회전** | `globals.css` 의 §1.1 + §1.2 신규 토큰 5개. 컴포넌트 코드 무변경. | 전 페이지 색상 회전. 회귀는 **시각 차이만**. 단위/계약 테스트 영향 없음. |
| **B · 앱 셸·로그인** | `Logo.tsx` 신설, 헤더/사이드바 SVG 치환, 로그인 카드 워드마크 + brand-primary 버튼 변형 추가. | 자산 (SVG) 입수 후 진행. brand-primary 버튼은 단계적 도입 (기존 Button 유지 가능). |
| **C · 페이지 디테일** | 차트 컬러 토큰화, 대시보드 카드 밀도, 테이블 헤더 페일톤, Vivid 알림 컴포넌트 신설. | 컴포넌트 단위로 PR 분할. |

---

## 6. 자동 회귀 가드 제안

| 가드 | 도구 | 게이트 |
|------|------|--------|
| 하드코딩 HEX 금지 grep | `rg -n '#[0-9a-fA-F]{6}\b' 도서물류관리프로그램/frontend/src --type tsx` | LegacyFormRenderer / charts / traffic-map 외 신규 등장 시 PR 차단 |
| `--brand-warm*` 미사용 확인 | `rg 'brand-warm' 도서물류관리프로그램/frontend/src` | 비어 있어야 폐기 가능 |
| 토큰 동기화 | `docs/Design.md §7` 표 vs `globals.css` 변수값 diff | 수기 체크 (Phase A 머지 시) |

> 위 가드는 [`docs/Design.md`](Design.md) 와 함께 새 규칙 [`design-bookioworks.mdc`](../.cursor/rules/design-bookioworks.mdc) 에 반영한다.

---

## 7. 변경 이력 (요약)

| 일자 | 메모 |
|------|------|
| 2026-05-11 | 공개 랜딩 `(public)/page.tsx`: 샘플 마케팅 패턴 이식 완료. `Logo.tsx` 단일 구현 정리(`BRAND_SVGS_READY`, `/marketing/logo-wordmark.png`). 가이드 PNG·아이콘 그리드는 `NEXT_PUBLIC_SHOW_DESIGN_GUIDE=1` 일 때만 `LandingGuideShowcase` 노출. |
