---
name: bookioworks-design
description: 북이오웍스 디자인 가이드(`docs/Design.md`)를 단일 원천으로 도서물류관리프로그램의 토큰·앱 셸·로고를 회귀 없이 변경합니다. UI/디자인/색상/로고/타이포 변경 또는 검수 요청 시 사용합니다.
---

# bookioworks-design — 디자인 단일 원천 적용 스킬

## 언제 사용

- "디자인을 가이드대로 바꿔줘 / 토큰 회전 / 컬러 회전 / 로고 적용 / 워드마크 적용" 류 요청.
- 색상·타이포·버튼·라운드·로고·favicon 변경 또는 검수.
- `globals.css` / `app-shell/*` / `(public)/login/*` / `components/brand/*` 수정.

## 단일 원천 (반드시 먼저 읽는다)

1. [`docs/Design.md`](docs/Design.md) — SSOT.
2. [`docs/design-gap-analysis.md`](docs/design-gap-analysis.md) — 변경 행 단위 표.
3. [`docs/design-source/`](docs/design-source/) — PDF 추출 원문 + 색상 데이터.

## 단계 (Phase A → B → C)

### Phase A · 토큰 회전 (Risk 낮음)

1. `docs/Design.md` §7.1 표를 펼치고 각 행을 `globals.css` 의 `:root` 블록에 1:1 매핑.
2. 신규 토큰 5개 (`--vivid-lime`, `--vivid-lime-hover`, `--vivid-sky`, `--accent-red`, `--radius-pill`) 추가.
3. 폐기 검토: `rg 'brand-warm' 도서물류관리프로그램/frontend/src` 가 0건이면 `--brand-warm*` 제거 (그레이스 PR 권장).
4. 회귀 가드:
   - `npm run lint` / `npm run build` 통과.
   - 시각 회귀: 로그인 / 대시보드 / 테이블 페이지 스크린샷 (browser-use MCP 활용 가능).
5. PR 제목: `style(design): phase A — bukioworks token rotation (lime primary + neutral text)`

### Phase B · 앱 셸 · 로그인 · 로고

1. **자산 입수 확인** — `frontend/public/brand/` 에 `bukioworks-symbol.svg`, `bukioworks-wordmark.svg`, `favicon-32.png`, `apple-touch-icon-180.png` 존재 여부 확인.
2. **로고 진입점 단일화**:
   - `components/brand/Logo.tsx` 신설 (props: `variant: "symbol" | "wordmark"`, `size`).
   - `header.tsx` / `sidebar.tsx` / `login/page.tsx` / `BrandHero.tsx` 의 인라인 SVG·`MascotMotif` 를 `<Logo />` 로 교체.
3. **brand-primary 버튼 변형 추가**:
   - `components/ui/button.tsx` 의 `cva` variants 에 `"brand-primary"` 추가:
     `h-[50px] px-6 rounded-full text-[18px] font-semibold bg-[var(--vivid-lime)] hover:bg-[var(--vivid-lime-hover)] text-foreground`.
   - 로그인 페이지·메인 CTA 부터 단계적으로 적용. **한 화면에 1개 원칙** 검수.
4. **`app/layout.tsx` 메타 갱신**: `metadata.title` / `metadata.icons` / `metadata.openGraph` 자산 경로 동기화.
5. PR 제목: `feat(brand): phase B — logo & login wordmark + brand-primary button`

### Phase C · 페이지 디테일

1. `components/stats/charts.tsx` 의 `#2563eb` 등 하드코딩 → `--chart-1~5` 토큰 (`docs/Design.md` §9 미제공 보완: 라임/스카이 톤 베이스로 신규 정의).
2. `components/dashboard/traffic-map-leaflet.tsx` 의 신호 컬러 → `--status-ok/--status-warn/--status-info` 토큰 매핑.
3. 테이블 헤더 / 합계 행: Pale Lime 배경 토큰 적용 (DataGrid 컴포넌트만).
4. NOTICE / IMPORTANT 컬러 블록 컴포넌트 신설 (`components/ui/color-block.tsx`).

## 의무 체크리스트 (PR 머지 전)

- [ ] `docs/Design.md` 의 §3·§6·§7 표와 PR 변경이 1:1 일치한다.
- [ ] `rg -n '#[0-9a-fA-F]{6}\b' 도서물류관리프로그램/frontend/src --type tsx` 결과가
      [`design-bookioworks.mdc`](.cursor/rules/design-bookioworks.mdc) §2 화이트리스트 외 0건.
- [ ] `rg 'brand-warm' 도서물류관리프로그램/frontend/src` 가 0건 (Phase A 후).
- [ ] 한 화면에 Primary Filled 가 2개 이상인지 수동 검수 (로그인·대시보드·등록 패널).
- [ ] `npm run lint && npm run build` PASS.
- [ ] 시각 회귀: 로그인 / 대시보드 / 테이블 / 사이드바 active 행 스크린샷 첨부.

## Harness 100 정책

- **Harness:** N/A — 본 작업은 단일 디자인 가이드 적용으로, Harness 100 케이스 이식 없이 본 스킬 단독 운용으로 충분함.
- 추후 디자인 시스템 자동 검증 도구가 필요해지면 Phase C 후 재평가.

## 모델 선택 (planning-model-tiers)

| 서브태스크 | 권장 티어 |
|------------|-----------|
| Phase A 토큰 회전 (oklch 환산·매핑) | 표준 |
| Phase B brand-primary 버튼 cva 변형 추가 | 표준 |
| Phase C 차트 토큰화·시각 회귀 평가 | 표준 |
| 가이드 모호 영역 (Vivid 사용 경계 등) 해석 | 고급 권장 |

## 금지 사항 (가이드 §8 인용)

1. Vivid Lime/Sky 의 무분별한 사용 금지.
2. 하드코딩 HEX 금지 (예외는 본 스킬 §의무 체크리스트의 화이트리스트만).
3. 한 화면에 Primary Filled 2개 이상 금지.
4. 컴포넌트 구조 변경으로 토큰 회피 금지.
5. Pretendard 외 한글 폰트 추가 금지.

## 참조

- 단일 원천: [`docs/Design.md`](docs/Design.md)
- 갭 분석: [`docs/design-gap-analysis.md`](docs/design-gap-analysis.md)
- 규칙: [`.cursor/rules/design-bookioworks.mdc`](.cursor/rules/design-bookioworks.mdc)
- 자산 / 롤아웃 노트: [`docs/design-rollout-plan.md`](docs/design-rollout-plan.md)
