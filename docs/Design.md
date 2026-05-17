# Design.md — 북이오웍스 (Bukioworks) 디자인 단일 원천

> **이 문서가 진실(SSOT) 입니다.** 색상·타이포·로고·컴포넌트 규칙을 변경할 때는 **반드시** 본 문서를 먼저 갱신하고, 이어서 [`globals.css`](../도서물류관리프로그램/frontend/src/app/globals.css)·앱 셸 컴포넌트·로고 자산을 동기화한다.
>
> - 원문: [docs/북이오웍스_디자인_가이드.pdf](북이오웍스_디자인_가이드.pdf) (전체 8 page)
> - 추출본: [docs/design-source/bukioworks-guide-extract.txt](design-source/bukioworks-guide-extract.txt)
> - 색상 데이터: [docs/design-source/color-palette.json](design-source/color-palette.json)
> - 도서물류관리프로그램은 **CMS 컨텍스트** — 운영자용. Vivid 컬러 사용은 알림에 한정.

목차
- [0. 컨텍스트 — 홈페이지 ≠ CMS](#0-컨텍스트--홈페이지--cms)
- [1. 브랜드 톤앤매너](#1-브랜드-톤앤매너)
- [2. 로고 (Symbol · Wordmark)](#2-로고-symbol--wordmark)
- [3. 컬러 시스템](#3-컬러-시스템)
- [4. 타이포그래피](#4-타이포그래피)
- [5. 레이아웃 · 그리드 · 라운드](#5-레이아웃--그리드--라운드)
- [6. 컴포넌트 규칙](#6-컴포넌트-규칙)
- [7. globals.css 매핑 (현재값 → 목표값)](#7-globalscss-매핑-현재값--목표값)
- [8. 금지 사항](#8-금지-사항)
- [9. 미제공 영역 — 추후 보완](#9-미제공-영역--추후-보완)

---

## 0. 컨텍스트 — 홈페이지 ≠ CMS

원문 인용 (PDF 1/8): _"독자가 마주하는 서비스 화면에서는 라임과 스카이 컬러를 통해 북이오만의 선명한 브랜드 인상을 전달하고, 운영자가 사용하는 CMS에서는 눈의 피로를 줄이고 정보 식별과 작업 효율을 높일 수 있는 차분한 색감을 중심으로 구성하였습니다."_

| 컨텍스트 | 시각 언어 | 본 문서 적용 범위 |
|----------|------------|-------------------|
| 홈페이지 (북이오 서비스) | Vivid Lime/Sky 적극 사용 — 브랜드 인상 강조 | 본 문서 범위 외 (참고만) |
| **CMS — 도서물류관리프로그램** | Neutral·Surface·Text 중심, Vivid 는 NOTICE/IMPORTANT 한정 | **본 문서가 다루는 대상** |

따라서 본 문서의 토큰값은 PDF §3 의 Primary Identity (Pale Lime/Sky) 와 Sub Color 를 **표면(Surface) · 보조(Sub) 로 격하**해 차분한 작업 환경에 맞게 재배치한다.

---

## 1. 브랜드 톤앤매너

- **본질**: "책, 기록, 하이라이트, 저장" 의 핵심 경험 (PDF §Symbol 인용).
- **운영자 화면 (CMS)**: 차분 · 가독성 · 작업 효율. 화려한 색상은 강조 알림에만.
- **버튼 위계 한 줄**: _Filled 는 화면당 1개. Outline 은 보조._

---

## 2. 로고 (Symbol · Wordmark)

| 항목 | 사용 위치 | 비고 |
|------|------------|------|
| Symbol | 앱 아이콘 / favicon / 사이드바 헤더 / 프로필 / 메뉴 | 단순한 구조 유지, 제한된 공간에서도 식별 가능 |
| Wordmark "북이오" | 로그인 화면 / CMS 상단(헤더) / 브랜드 안내 페이지 | 심볼보다 공식적·직접적 |

운용 규칙
- **현재 자산 미수신 상태**. 로고 SVG/파비콘은 [§9 미제공 영역](#9-미제공-영역--추후-보완) 항목으로 두고 PR 분리.
- 임시 placeholder: 현재 [`header.tsx`](../도서물류관리프로그램/frontend/src/components/app-shell/header.tsx) 의 책 모양 SVG 와 [`sidebar.tsx`](../도서물류관리프로그램/frontend/src/components/app-shell/sidebar.tsx) 의 `BookOpen` 아이콘을 유지하되, 자산 입수 즉시 교체할 진입점만 한 곳으로 모은다 (`components/brand/Logo.tsx` 신설 제안).

---

## 3. 컬러 시스템

### 3.1 Primary Identity (CMS 에서는 표면·보조로 활용)

| 토큰 | HEX | RGB | CMS 사용 |
|------|------|------|------|
| Pale Lime | `#FCFFE9` | 252 / 255 / 233 | 라이트 섹션·하이라이트 행 배경 (대시보드 카드 등) |
| Pale Sky | `#F4FFFF` | 244 / 255 / 255 | 보조 라이트 섹션 (info 블록 배경) |

### 3.2 Neutral (구조)

| 토큰 | HEX | RGB | CMS 사용 |
|------|------|------|------|
| Bukio Black | `#282828` | 40 / 40 / 40 | 본문 텍스트 / Dark Filled 버튼 / 아이콘 기본색 |
| Bukio Gray | `#E6E6E6` | 230 / 230 / 230 | 외곽선 · 구분선 |

### 3.3 Surface & Background

| 토큰 | HEX | CMS 사용 |
|------|------|------|
| White | `#FFFFFF` | Primary Page Canvas |
| Neutral Gray | `#F5F5F7` | Subtle Gray (사이드바·카드 배경) |
| Neutral Gray_02 | `#F5F5F5` | Zone separator (헤더 하단·섹션 구분) |

### 3.4 Text

| 토큰 | HEX | CMS 사용 |
|------|------|------|
| Primary Text | `#282828` | Body + Heading on Light |
| Secondary Text | `#555555` | Metadata · Secondary Text · placeholder |
| Inverse Text | `#F5F5F5` | Dark 배경 위 헤딩 (Dark Filled 내부 등) |

### 3.5 Sub Color Palette (상태)

| 토큰 | HEX | CMS 사용 |
|------|------|------|
| Info Blue | `#B6D3F5` | 정보 알림 · 링크 · 인포 패널 배경. 텍스트/아이콘은 접근성 보정 파생 토큰(`--status-info`, `--link`) 사용 |
| Positive Green | `#8EC8CD` | 성공 배경·차트 베이스. 텍스트/아이콘은 접근성 보정 파생 토큰(`--status-ok`) 사용 |
| Warning Orange | `#FFC1A0` | 경고 배경·차트 베이스. 텍스트/아이콘은 접근성 보정 파생 토큰(`--status-warn`) 사용 |
| Error Red | `#FFA8A8` | 오류 배경·차트 베이스. 텍스트/아이콘은 접근성 보정 파생 토큰(`--destructive`) 사용 |
| Accent Red | `#FFE3DF` | 중요도 낮은 강조 (서브 라벨) |
| Neutral Gray | `#CCCCCC` | Neutral · disabled border |

### 3.6 Vivid Section (한정 사용)

| 토큰 | HEX | CMS 사용 |
|------|------|------|
| Vivid Lime | `#E0FF00` | **Primary Filled 버튼 본색** · NOTICE / IMPORTANT 알림 |
| Vivid Sky | `#5EFFFF` | Important / Notice 알림 한정 |

> 운용 원칙: Vivid 는 _Warning, Urgent Notice, Important alerts, areas that require immediate attention_ 외에 사용 금지 (PDF §3 인용).

### 3.7 Button-only HEX

| 상태 | HEX | 비고 |
|------|------|------|
| Primary Filled · default | `#E0FF00` | Vivid Lime |
| Primary Filled · hover | `#C9E500` | 클릭 시 밝기 감소 |
| Disabled | `#CCCCCC` | 낮은 대비 |
| Dark Filled | `#282828` | Bukio Black + White text |
| Outline border / text | `#282828` | white 배경 위 |

---

## 4. 타이포그래피

### 4.1 패밀리

| 언어 | 패밀리 | 비고 |
|------|--------|------|
| 영문 | Outfit | Display·Headline 은 Semibold, Body 는 Regular, Detail 은 Light |
| 국문 | Pretendard | 현재 [`globals.css`](../도서물류관리프로그램/frontend/src/app/globals.css) 의 `--font-sans` 가 이미 Pretendard Variable 로딩 중 (유지) |

> 두 서체 모두 정원에 가까운 곡선·직선을 공유 → 혼용 OK (PDF §4 인용).

### 4.2 Hierarchy 표

| Token | Family | Weight | Size | 자간 | 행간 | 사용 |
|-------|--------|--------|------|------|------|------|
| Display | Outfit | Semibold | 48px | 0 | 1.5 | 영문 히어로 디스플레이 |
| Headline_en | Outfit | Semibold | 32px | 0 | 1.5 | 영문 두 줄 이하 타이틀 |
| Body_en | Outfit | Regular | 16px | 0 | 1.5 | 영문 한 줄 이상 본문 |
| Detail_en | Outfit | Light | 14px | 0 | 1.5 | 영문 디테일 텍스트 |
| Headline_kor | Pretendard | Bold | 28px | -2 | 1.5 | 국문 두 줄 이하 타이틀 |
| Body_kor | Pretendard | Medium | 16px | -2 | 1.5 | 국문 한 줄 이상 본문 |
| Detail_kor | Pretendard | Regular | 14px | -2 | 1.5 | 국문 디테일 / 캡션 |

### 4.3 Tailwind 클래스 매핑 제안

| Token | Tailwind utility (잠정) |
|-------|--------------------------|
| Headline_kor | `text-[28px] font-bold leading-[1.5] tracking-[-0.02em]` |
| Body_kor | `text-base font-medium leading-[1.5] tracking-[-0.02em]` |
| Detail_kor | `text-sm font-normal leading-[1.5] tracking-[-0.02em]` |

> 자간 `-2` 는 Figma 단위(per 1000em) 기준 → CSS `letter-spacing: -0.02em` 로 환산.

---

## 5. 레이아웃 · 그리드 · 라운드

| 항목 | 값 / 규칙 | PDF 출처 |
|------|------------|----------|
| 컬러 블록 코너 | 가로 길이의 약 15% | §8 |
| 컬러 블록 여백 | 넉넉한 패딩, 라운드 코너, 높은 가독성 | §8 |
| 버튼 코너 | 999px (full pill) | §6 |
| 버튼 높이 | 50px | §6 |
| 버튼 좌우 패딩 | 24px | §6 |
| 아이콘 크기 | 20px (버튼 내부) / 24px (메뉴·일반) | §6, §7 |
| 아이콘 ↔ 텍스트 간격 | 12px | §6 |

> 그리드·간격 시스템 (8pt grid 등) 은 PDF 에 명시 없음 → [§9](#9-미제공-영역--추후-보완) 으로 둠.

---

## 6. 컴포넌트 규칙

### 6.1 버튼

> _"Primary Filled 버튼을 기본으로 사용하며, 한 화면에서 Primary 스타일은 1개만 사용합니다."_ (PDF §6)

| 변형 | 용도 | 색상 | 라벨 예 |
|------|------|------|---------|
| **Primary Filled (Lime)** | 생성·추가·저장·확인 등 긍정적 핵심 액션 (화면당 1개) | `#E0FF00` 배경 + Black text | "+ 책장 추가하기", "저장" |
| **Dark Filled** | 관리·삭제·설정·편집 완료 등 기능 실행 성격이 강한 액션 | `#282828` 배경 + White text | "관리하기" |
| **Outline** | 상세보기·취소·옵션 확인 등 보조 액션 | Border `#282828` + Text `#282828` | "자세히 보기", "취소" |

상태
- Default → 기본 표시
- Hover → 밝기 감소 (Primary Filled: `#C9E500`)
- Disabled → `#CCCCCC` 로 대비 ↓

### 6.2 아이콘

- 기준 그리드 24×24 px.
- 기본은 **Line Icon**, 선택·강조는 **Solid Icon**.
- 다크 컬러 기본. 버튼/메뉴 안에서도 동일한 크기·간격 규칙.

### 6.3 컬러 블록 (Light · Vivid)

- **Light Section** — 정보 전달·안내·일반 컨텐츠. Pale Lime/Sky 배경 + Primary Text.
- **Vivid Section** — 경고·공지·강조 (NOTICE / IMPORTANT) 한정.
- 두 섹션 모두 코너는 가로 길이의 약 15%, 넉넉한 여백.

### 6.4 폼 (Input · Card · Table) — 최소 규약

PDF 에 직접 명시는 없으나, 위 규칙에서 도출되는 최소 합의:
- 입력 필드 라운드: `radius-md` (≈ 8px) 유지.
- 카드: White Surface + Bukio Gray border (`#E6E6E6`).
- 테이블 헤더: `Neutral Gray (#F5F5F7)` 배경 + Secondary Text.
- 합계 행: Pale Lime 배경 (라이트 섹션과 일관).

> 위 4 항목은 본 문서의 **derivation** 표시 — 가이드 갱신 시 우선 검증.

---

## 7. globals.css 매핑 (현재값 → 목표값)

> 파일: [`도서물류관리프로그램/frontend/src/app/globals.css`](../도서물류관리프로그램/frontend/src/app/globals.css)
> 현재 값은 "buk.io 1단계 잠정값" — Indigo/Coral 톤. 본 가이드 적용 시 **변수값만** 교체하면 컴포넌트 구조 변동 없이 토큰 회전 가능 (OCP, [DEC-028](../legacy-analysis/decisions.md)).
>
> **가독성 보정 원칙 (2026-05-11):** CMS 에서 shadcn/Tailwind 의 `--primary` 는 전역 시맨틱 토큰이다. `text-primary`, `bg-primary/10`, 아이콘, 링크, 포커스 등 본문 주변 UI 에 넓게 퍼지므로 **Vivid Lime 을 `--primary` 에 직접 배치하지 않는다**. Vivid Lime 은 `--vivid-lime` 및 `Button` 의 `brand-primary` 변형처럼 **핵심 CTA / NOTICE / IMPORTANT 전용 토큰**으로만 사용한다.

### 7.1 Light 모드 (`:root`)

| 토큰 | 현재값 (oklch) | 가이드 매핑 (HEX) | 목표 oklch (제안) | 변동 |
|------|----------------|--------------------|-------------------|------|
| `--background` | `oklch(0.985 0.005 80)` | White `#FFFFFF` | `oklch(1 0 0)` | 미세 ↑ |
| `--foreground` | `oklch(0.20 0.025 260)` | Primary Text `#282828` | `oklch(0.275 0 0)` | hue 제거 (중립) |
| `--card` | `oklch(1 0 0)` | White | 유지 | — |
| `--card-foreground` | `oklch(0.20 0.025 260)` | `#282828` | `oklch(0.275 0 0)` | hue 제거 |
| `--popover` / `-foreground` | 위와 동일 | 위와 동일 | 위와 동일 | — |
| `--primary` | `oklch(0.38 0.10 258)` Indigo | Bukio Black `#282828` | `oklch(0.275 0 0)` | **가독성 보정** — 전역 강조/링크/아이콘에 쓰이는 시맨틱 토큰이므로 Vivid Lime 금지 |
| `--primary-foreground` | `oklch(0.99 0 0)` | Inverse Text `#F5F5F5` | `oklch(0.965 0 0)` | 다크 필 버튼 위 텍스트 |
| `--secondary` | `oklch(0.96 0.012 80)` | Pale Lime `#FCFFE9` | `oklch(0.99 0.04 110)` | hue 변경 |
| `--secondary-foreground` | `oklch(0.28 0.04 258)` | `#282828` | `oklch(0.275 0 0)` | 중립 |
| `--muted` | `oklch(0.965 0.008 80)` | Neutral Gray `#F5F5F7` | `oklch(0.965 0.003 264)` | 유지에 가까움 |
| `--muted-foreground` | `oklch(0.50 0.02 258)` | Secondary Text `#555555` | `oklch(0.42 0 0)` | 중립 |
| `--accent` | `oklch(0.74 0.13 38)` Coral | Pale Sky `#F4FFFF` | `oklch(0.99 0.012 200)` | **재정의** |
| `--accent-foreground` | `oklch(0.20 0.04 40)` | `#282828` | `oklch(0.275 0 0)` | — |
| `--destructive` | `oklch(0.58 0.22 28)` | Error Red `#FFA8A8` | `oklch(0.81 0.10 22)` | 페일톤 ↓ |
| `--border` | `oklch(0.90 0.012 80)` | Bukio Gray `#E6E6E6` | `oklch(0.92 0 0)` | hue 제거 |
| `--input` | `oklch(0.93 0.010 80)` | `#E6E6E6` 계열 | `oklch(0.93 0 0)` | hue 제거 |
| `--ring` | `oklch(0.55 0.10 258)` | Info Blue 기반 focus | `oklch(0.62 0.08 245)` | 포커스 링은 라임 대신 차분한 정보색으로 가독성 확보 |
| `--radius` | `0.625rem` (10px) | 기본 카드/입력 — 유지 | 유지 | — |
| `--sidebar` | `oklch(0.975 0.008 258)` | Neutral Gray `#F5F5F7` | `oklch(0.965 0.003 264)` | hue 중성화 |
| `--sidebar-foreground` | `oklch(0.24 0.03 258)` | `#282828` | `oklch(0.275 0 0)` | — |
| `--sidebar-primary` | `oklch(0.38 0.10 258)` | Bukio Black `#282828` | `oklch(0.275 0 0)` | 사이드바 아이콘/텍스트 강조용 — 라임 금지 |
| `--sidebar-primary-foreground` | `oklch(0.99 0 0)` | Inverse Text `#F5F5F5` | `oklch(0.965 0 0)` | 다크 강조 위 텍스트 |
| `--sidebar-accent` | `oklch(0.93 0.03 258)` | Pale Lime `#FCFFE9` | `oklch(0.99 0.04 110)` | hue 변경 |
| `--sidebar-border` | `oklch(0.91 0.015 258)` | `#E6E6E6` | `oklch(0.92 0 0)` | — |
| `--brand-warm` | `oklch(0.93 0.05 60)` | (없음 → 폐기 검토) | — | 가이드에 매칭 컬러 부재 |
| `--brand-warm-foreground` | `oklch(0.35 0.10 40)` | (없음 → 폐기 검토) | — | 동상 |
| `--status-ok` | `oklch(0.62 0.17 155)` | Positive Green `#8EC8CD` | `oklch(0.78 0.045 200)` | 페일톤 ↓ |
| `--status-warn` | `oklch(0.74 0.16 65)` | Warning Orange `#FFC1A0` | `oklch(0.84 0.08 50)` | 페일톤 ↓ |
| `--status-info` | `oklch(0.55 0.13 258)` | Info Blue `#B6D3F5` | `oklch(0.85 0.06 245)` | 페일톤 ↓ |
| `--app-canvas` | — | (파생) 인증 후 본문 스크롤 캔버스 — `muted`·`background` 만 조합 | `color-mix(in oklch, var(--muted) 88%, var(--background))` | 신규 |
| `--app-canvas-edge` | — | (파생) 캔버스 상단 1px 구분선 — `border`·`muted` 만 조합 | `color-mix(in oklch, var(--border) 48%, var(--muted))` | 신규 |

> **신규 토큰 (제안)** — Phase A 에서 추가:
> - `--vivid-lime`: `oklch(0.95 0.20 122)` (= `#E0FF00`)
> - `--vivid-lime-hover`: `oklch(0.88 0.18 122)` (= `#C9E500`)
> - `--vivid-sky`: `oklch(0.93 0.10 195)` (= `#5EFFFF`)
> - `--accent-red`: `oklch(0.93 0.025 25)` (= `#FFE3DF`)
> - `--radius-pill`: `9999px`
> - `--link`: `oklch(0.46 0.08 245)` — 텍스트 링크/hover 전용. `--primary` 와 분리.

### 7.2 Dark 모드 (`.dark`)

PDF 에 다크 변형 명시 없음. 본 가이드 Phase 에서는 **라이트 우선**, 다크는 현재 중립 톤을 유지하되 `--vivid-lime` 은 CTA/NOTICE 전용으로만 동기화한다. 정식 Dark 토큰은 [§9](#9-미제공-영역--추후-보완).

- **본문 캔버스 (파생):** `--app-canvas`, `--app-canvas-edge` 는 `globals.css` 의 `.dark` 에서 동일 변수명으로 정의하며, 값은 **`color-mix(in oklch, …)` 로 `--muted` / `--background` / `--border` 만 조합**한다 (라이트와 동일 정책; 예: 캔버스 `muted` 62% + `background`, 엣지 `border` 55% + `muted`).

---

## 8. 금지 사항

1. **Vivid Lime/Sky 의 무분별한 사용 금지** — 알림·핵심 CTA 외 사용은 PR 차단 사유. 특히 CMS 에서는 `--primary` / `--sidebar-primary` / 텍스트 링크 토큰에 Vivid Lime 을 배치하지 않는다.
2. **하드코딩 HEX 금지** — 컴포넌트는 `var(--primary)` 등 토큰만 참조. (예외: 본 문서·color-palette.json·PR 설명문)
3. **한 화면에 Primary Filled 2개 이상 금지** (PDF §6).
4. **컴포넌트 구조 변경으로 토큰 회피 금지** — 토큰값만 변경해 회귀 범위 통제 (OCP).
5. **Pretendard 외 한글 폰트 추가 금지** — fallback 만 Apple SD Gothic Neo / Noto Sans KR.

---

## 9. 미제공 영역 — 추후 보완

PDF 에 명시되지 않아 본 문서가 **잠정 합의** 또는 **TBD** 로 둔 항목.

| 항목 | 현재 상태 | 후속 액션 |
|------|------------|-----------|
| 8pt 그리드·간격 시스템 | TBD | shadcn 기본(`gap-2/4/6/8`) 유지, 가이드 추가 입수 시 갱신 |
| Dark 모드 정식 팔레트 | TBD | 라이트 안정화 후 별도 PR |
| 로고 SVG (Symbol·Wordmark) | **미수신** | `frontend/public/brand/` 에 자산 입수 후 `Logo.tsx` 신설 |
| favicon.ico / apple-touch-icon | 현재 Next.js 기본값 | 자산 입수 후 [`app/layout.tsx`](../도서물류관리프로그램/frontend/src/app/layout.tsx) 메타 갱신 |
| OG 이미지 / 메타 thumbnail | 미정의 | Phase B 에서 결정 |
| 차트 / 대시보드 시각화 컬러 | `--chart-1~5` 인디고 계열 유지 | Light 적용 후 별도 검토 |
| 모션·애니메이션 | TBD | tw-animate-css 기본값 유지 |

---

## 부록 A — 변경 이력

| 일자 | 버전 | 변경 |
|------|------|------|
| 2026-05-11 | v1.0 | 최초 작성 — PDF 8 page 기반 토큰·매핑·금지 사항 정리 |
