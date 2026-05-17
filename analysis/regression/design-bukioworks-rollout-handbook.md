# 북이오웍스 디자인·레이아웃 롤아웃 핸드북

> 플랜「북이오웍스 레이아웃 변경 가능성 및 하네스·스킬」실행 산출물.  
> SSOT: [`docs/Design.md`](../../docs/Design.md) · 규칙: [`.cursor/rules/design-bookioworks.mdc`](../../.cursor/rules/design-bookioworks.mdc) · 스킬: [`.cursor/skills/bookioworks-design/SKILL.md`](../../.cursor/skills/bookioworks-design/SKILL.md)

코드 경로 기준 시점: 저장소 내 `도서물류관리프로그램/frontend` (2026-05-11 확인).

---

## 1. 로그인 전 `(public)` 라우트 인벤토리

Route group 폴더: `도서물류관리프로그램/frontend/src/app/(public)/`

| URL 경로 | 소스 파일 |
|----------|-----------|
| `/` | `(public)/page.tsx` |
| `/login` | `(public)/login/page.tsx` |
| `/signup` | `(public)/signup/page.tsx` |
| `/activate/lookup` | `(public)/activate/lookup/page.tsx` |
| `/activate/{token}` | `(public)/activate/[token]/page.tsx` |

**참고**

- `(public)/layout.tsx` 는 **없음** — 공개 페이지는 루트 [`app/layout.tsx`](../../도서물류관리프로그램/frontend/src/app/layout.tsx) 만 공유.
- [`middleware.ts`](../../도서물류관리프로그램/frontend/src/middleware.ts) 의 `PUBLIC_PATHS` 는 **`/`, `/login`, `/signup`** 만 명시. `/activate/...` 는 목록에 없으나 현재 구현은 대부분의 경로에서 `NextResponse.next()` 로 통과시키므로 라우트 동작은 코드 변경 시 재확인할 것.
- 문서상 `/contact` 등은 저장소 상 `(public)` 에 **미구현** — [`docs/landing-page-design-spec.md`](../../docs/landing-page-design-spec.md) 와 구현을 따로 동기화할 것.

---

## 2. 공개 화면에서 쓰는 공통 컴포넌트 (브랜드·소개)

디렉터리: `도서물류관리프로그램/frontend/src/components/brand/`

| 파일 | `(public)` 사용처 |
|------|-------------------|
| `BrandHero.tsx` | `/`, `/signup`, `/activate/lookup`, `/activate/[token]` |
| `BrandBadge.tsx`, `ProcessStepper.tsx` | `/` (랜딩) |
| `MascotMotif.tsx` | `/login` |
| `Logo.tsx` | (Phase B에서 헤더·로그인 등으로 단일화 예정 — 스킬 참조) |

**선행 디자인 검토 체크리스트 (공개 구간만)**

- [ ] [`docs/Design.md`](../../docs/Design.md) §4 타이포 — 히어로/본문이 Headline_kor·Body_kor 매핑과 충돌하지 않는지
- [ ] §5 레이아웃 — 버튼 높이 50px·pill·아이콘 20/24px·간격 12px
- [ ] §6 버튼 위계 — **한 화면 Primary Filled(lime) 1개** (랜딩 CTA 다중 시 Outline/Dark로 조정)
- [ ] §8 금지 — Vivid 남용·HEX 하드코딩·폰트 추가
- [ ] `npm run lint` / `npm run build` (해당 PR 범위)
- [ ] 선택: 로그인·랜딩 스크린샷 첨부 (스킬 Phase A 회귀와 동일 계열)

---

## 3. `Design.md` §5·§6·§8 및 `design-bookioworks.mdc` 요약

### §5 레이아웃 · 그리드 · 라운드 (발췌)

- 컬러 블록 코너 ≈ 가로의 15%, 여백·가독성
- 버튼: 코너 pill (`999px`), 높이 50px, 좌우 패딩 24px
- 아이콘 20px(버튼 내) / 24px(메뉴·일반), 아이콘↔텍스트 12px
- 8pt 그리드는 PDF 미명시 → Design.md §9 TBD

### §6 컴포넌트 (발췌)

- Primary Filled(Lime) / Dark Filled / Outline 역할 구분, 화면당 Primary Filled 1개
- 아이콘 24×24 기준, Line 기본
- 컬러 블록 Light vs Vivid 구분
- 폼·카드·테이블 최소 규약 (radius-md, 카드 보더, 테이블 헤더·합계 행)

### §8 금지 + 가독성 보정 (§7 메모)

- Vivid Lime/Sky 남용 금지; CMS에서 `--primary` 등에 라임 직접 금지 → `--vivid-lime`·`brand-primary` 등 전용 토큰
- HEX 하드코딩 금지 (화이트리스트 예외는 규칙 §2)
- Primary Filled 2개 이상 금지
- 구조 변경으로 토큰 회피 금지
- Pretendard 외 한글 폰트 추가 금지

### 자동 회귀 가드 (규칙·스킬과 동일)

저장소 루트에서:

```bash
rg -n '#[0-9a-fA-F]{6}\b' 도서물류관리프로그램/frontend/src --type tsx
rg 'brand-warm' 도서물류관리프로그램/frontend/src
```

---

## 4. 레거시(dfm) 포팅 화면 — `layout_mappings` · `data-legacy-id`

공개 `(public)` 구간은 dfm 매핑 대상이 **아님**. `(app)` 이하 레거시 포팅 페이지를 손댈 때만 적용.

| 항목 | 위치 |
|------|------|
| 규칙 | [`.cursor/rules/dfm-layout-input.mdc`](../../.cursor/rules/dfm-layout-input.mdc) |
| 매핑 노트 | `analysis/layout_mappings/<Sobo*>.md` (시나리오별 선행 작성) |
| DOM | 모든 입력·버튼·그리드 헤더에 `data-legacy-id="<원본 ID>"` |
| 회귀 | 매핑 노트의 `legacy_id` 집합과 DOM 일치 자동 검사 (스냅샷/단위 테스트) |

레이아웃을 그리드·반응형으로 바꿔도 **위젯 ID 대응은 유지**한다.

---

## 5. Phase A → B → C 및 PR 분리 (단일 순서)

| Phase | 내용 | 문서 |
|-------|------|------|
| **A** | `globals.css` 토큰 회전, 신규 토큰 5종 | [`docs/design-rollout-plan.md`](../../docs/design-rollout-plan.md) §2, [`analysis/regression/design-phase-a-rotation.md`](design-phase-a-rotation.md) |
| **B** | 앱 셸·로그인·`Logo.tsx`·`brand-primary`·메타 | design-rollout-plan §3·§4, 스킬 Phase B |
| **C** | 차트·지도·테이블 헤더·NOTICE 등 페이지 디테일 | 스킬 Phase C, [`design-phase-c-tokenize.md`](design-phase-c-tokenize.md) |

**의무:** 한 PR에 Phase 전부 섞지 말고 롤아웃 플랜대로 분리.  
**Harness 100:** 디자인 롤아웃에 필수 아님 — 스킬「Harness: N/A」.

---

## 6. 변경 미리보기(Preview) 전략

| 방식 | 이 저장소 메모 |
|------|----------------|
| **Feature 브랜치 + 로컬 `npm run dev`** | 즉시 적용. 백엔드 없이 UI만 볼 때 프론트만 기동. |
| **PR Preview URL** | `.github` 워크플로에 Vercel 등 **전용 Preview 스텝은 미검출**. 호스팅을 연결할 경우 PR마다 URL 공유 방식으로 운영 가능. |
| **스크린샷·시각 회귀** | Playwright 등으로 `/`, `/login` 고정 캡처 — 스킬·Phase A 매트릭스와 합치 가능. |
| **런타임 플래그·쿼리 스킨** | 동일 배포에서 구/신 병존이 필요할 때만; 분기·테스트 비용 증가. |

**권장:** 공개 화면만 먼저 적용할 때는 **브랜치 + 로컬 또는 CI 연동 Preview** 로 충분.

---

## 7. 빠른 링크

- [`docs/design-gap-analysis.md`](../../docs/design-gap-analysis.md)
- [`docs/design-rollout-plan.md`](../../docs/design-rollout-plan.md)
- [`.github/PULL_REQUEST_TEMPLATE/design-bookioworks.md`](../../.github/PULL_REQUEST_TEMPLATE/design-bookioworks.md)
