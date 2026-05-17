# Design Phase A — globals.css 토큰 회전 회귀 매트릭스

> 본 문서는 [`docs/design-rollout-plan.md`](../../docs/design-rollout-plan.md) §2 Phase A 적용 결과의 자동/수동 회귀 가드 결과를 PR 본문 그대로 붙여 쓰기 위한 매트릭스다.
> 사람 검토 시 §4 체크박스를 직접 채운다.

작업일: 2026-05-11
SSOT: [`docs/Design.md`](../../docs/Design.md) §3·§7  ·  근거: [`docs/design-gap-analysis.md`](../../docs/design-gap-analysis.md) §1

## 1. 변경 파일

| 파일 | 변경 |
|------|------|
| [`도서물류관리프로그램/frontend/src/app/globals.css`](../../도서물류관리프로그램/frontend/src/app/globals.css) | `@theme inline` 에 `--color-vivid-lime/-hover/-sky/--color-accent-red/--radius-pill` 5종 신규 매핑. `:root` 22개 토큰 회전 (Indigo/Coral → Bukio Black + Vivid Lime + Pale Sky/Pale Lime + Neutral Gray). `.dark` 에서 `--primary` 등 라임 동기화 (잠정, A.2 에서 정식). `--brand-warm*` 는 deprecate 주석만 추가하고 실제 제거는 Phase A.1. |

## 2. 자동 회귀 가드 결과

| 가드 | 명령 | 결과 |
|------|------|------|
| Lint (사전 존재 에러는 본 PR 범위 외) | `npm run lint` | 본 변경(globals.css) 신규 lint 에러 0건. 기존 react-hooks 에러는 [`use-sales-statement-pdf-layout.ts`](../../도서물류관리프로그램/frontend/src/hooks/use-sales-statement-pdf-layout.ts), [`use-permissions.ts`](../../도서물류관리프로그램/frontend/src/lib/use-permissions.ts) 등에서 이미 발생 — 별도 PR 사안. |
| Build | `npm run build` | PASS (Next.js App Router 전체 라우트 컴파일 완료) |
| 하드코딩 HEX | `rg -n '#[0-9a-fA-F]{6}\b' 도서물류관리프로그램/frontend/src --type tsx` | 화이트리스트 외 0건 — `LegacyFormRenderer.tsx`(Delphi 회색), `traffic-map-leaflet.tsx`/`charts.tsx`(Phase C 토큰화 예정) 만 잔존 |
| `--brand-warm*` | `rg 'brand-warm' 도서물류관리프로그램/frontend/src` | 1건 — [`MascotMotif.tsx`](../../도서물류관리프로그램/frontend/src/components/brand/MascotMotif.tsx) L28 의 `fill-brand-warm/80`. 본 PR 은 변수값을 Pale Lime 으로 임시 align(시각 회귀 최소). 정식 제거는 Phase B 의 `Logo.tsx` 진입점이 Mascot 을 흡수한 다음 Phase A.1 후속 PR. |
| Pretendard 외 한글 폰트 | `rg "font-(family|sans).*(Apple SD Gothic|Noto Sans KR|Malgun)" 도서물류관리프로그램/frontend/src` | fallback 외 신규 없음 |

## 3. 토큰 매핑 (PR 리뷰어용 압축 표)

> 상세 22개 행은 [`docs/design-gap-analysis.md`](../../docs/design-gap-analysis.md) §1.1 참조. 본 표는 핵심 5축만.

| 축 | 변경 전 | 변경 후 | 출처 |
|----|---------|---------|------|
| Brand · `--primary` | Indigo `oklch(0.38 0.10 258)` | Vivid Lime `oklch(0.95 0.20 122)` (`#E0FF00`) + 검정 텍스트 | Design.md §3.6·§7.1 |
| Surface · `--background` | `oklch(0.985 0.005 80)` | White `oklch(1 0 0)` (`#FFFFFF`) | Design.md §3.3 |
| Text · `--foreground` | `oklch(0.20 0.025 260)` | Bukio Black `oklch(0.275 0 0)` (`#282828`) | Design.md §3.4 |
| Border · `--border` | `oklch(0.90 0.012 80)` | Bukio Gray `oklch(0.92 0 0)` (`#E6E6E6`) | Design.md §3.2 |
| Status · OK/Warn/Info | 기본 채도 톤 | 페일톤 (Sub Color Palette `#8EC8CD/#FFC1A0/#B6D3F5`) | Design.md §3.5 |

신규 토큰 5종: `--vivid-lime`, `--vivid-lime-hover`, `--vivid-sky`, `--accent-red`, `--radius-pill (= 9999px)`.

## 4. 사람 검증 체크리스트 (리뷰어가 직접 체크)

- [ ] 로그인·헤더·사이드바·대시보드 카드의 Primary 색이 라임으로 회전됨 (Indigo/Coral 잔존 없음).
- [ ] **한 화면 라임 Primary 핵심 버튼 1개** 원칙 ([`Design.md`](../../docs/Design.md) §6·§8). 마스터 CRUD 등록 패널의 "신규/저장/삭제" 셋이 함께 라임으로 보이지 않는지 (저장만 라임이어야 — Phase B 의 `brand-primary` 도입 전까지는 임시로 모두 default 라임 표시일 수 있음 → Phase B 에서 분리).
- [ ] 본문/Secondary 텍스트 가독성 (`#282828` / `#555555` 대비) — 사이드바 폼 제목·계정 라벨, 헤더 hcode/계정 뱃지.
- [ ] 사이드바 active 행의 Pale Lime 배경이 흰 사이드바 위에서 인지 가능 (필요 시 `--sidebar-accent` 채도 미세 조정).
- [ ] 다크 모드(.dark) 진입 시 라임 `--primary` 가 가독성을 해치지 않는지 (Phase A.2 정식화 전 잠정).

## 5. 스크린샷 번들 (PR 본문에 채워 넣을 위치)

| 화면 | 변경 전 | 변경 후 |
|------|---------|---------|
| 로그인 (`/login`) | (img) | (img) |
| 대시보드 (`/dashboard`) | (img) | (img) |
| 사이드바 (확장 + 한 메뉴 active) | (img) | (img) |
| 마스터 거래처 목록 (`/master/customer`) | (img) | (img) |
| (선택) 다크 모드 토글 | (img) | (img) |

## 6. PR 본문 템플릿

```text
제목: style(design): phase A — bukioworks token rotation (lime primary + neutral text)

요약:
- globals.css :root / .dark / @theme inline 토큰을 docs/Design.md §3·§7 에 1:1 매핑.
- 신규 토큰 5종(--vivid-lime/-hover/-sky, --accent-red, --radius-pill).
- 컴포넌트 코드 무변경 (OCP, DEC-028).
- --brand-warm* 는 deprecate 주석만 추가 (Phase A.1 에서 변수 자체 제거).

자동 가드:
- npm run lint: 신규 에러 0건 (사전 존재 react-hooks 에러는 범위 외).
- npm run build: PASS.
- rg 화이트리스트 외 신규 HEX 0건.
- brand-warm 사용처 0건 유지.

사람 검증: analysis/regression/design-phase-a-rotation.md §4 체크박스 + §5 스크린샷.
```
