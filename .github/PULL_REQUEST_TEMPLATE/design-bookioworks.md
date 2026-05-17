# 디자인 PR — 북이오웍스 가이드 적용 (Phase ___)

> 본 템플릿은 [`docs/Design.md`](../../docs/Design.md) 적용 PR 전용. 디자인 변경이 아닌 PR 은 기본 템플릿 사용.

## 1. Phase 분리 합의 (체크 1개만 표시)

- [ ] **Phase A — 토큰 회전** (`globals.css` 만 수정. 컴포넌트 코드 무변경. 자산 불필요)
- [ ] **Phase B — 앱 셸·로고·로그인** (`frontend/public/brand/` 자산 수령 후. `Logo.tsx` 진입점, `layout.tsx` 메타, `brand-primary` 버튼)
- [ ] **Phase C — 페이지 디테일** (차트·지도·DataGrid·알림 컬러 블록 등 — 페이지 단위 소단위 PR)

## 2. 모델 티어

| 서브태스크 | 권장 티어 | 실제 모델 |
|------------|-----------|-----------|
| 토큰 매핑 (oklch 환산) / `cva` 변형 / 컴포넌트 교체 | 표준 | Cursor 기본 |
| Vivid 사용 경계 / `Design.md` §9 미제공 영역 해석 | 고급 권장 | (해당 시 Claude Opus Thinking 등) |

## 3. 변경 요약

<!-- 무엇을 / 왜 / 어떤 토큰·파일 -->

- 토큰 회전 (Phase A 한정): __개 토큰 회전 + __개 신규.
- 컴포넌트 교체 (Phase B/C 한정): _____ 파일 _____ 곳.

## 4. 자동 회귀 가드 (모두 체크)

- [ ] `npm run lint` PASS — `frontend/` 기준
- [ ] `npm run build` PASS
- [ ] 하드코딩 HEX 점검: `rg -n '#[0-9a-fA-F]{6}\b' 도서물류관리프로그램/frontend/src --type tsx` 결과가 화이트리스트 외 0건
   - 화이트리스트: `LegacyFormRenderer.tsx` (Delphi 회색 톤 의도), `traffic-map-leaflet.tsx`/`charts.tsx` (Phase C 토큰화 예정 — 본 PR이 Phase C 면 제거)
- [ ] `--brand-warm*` 미사용: `rg 'brand-warm' 도서물류관리프로그램/frontend/src` = 0건 (Phase A 후)

## 5. 사람 검증 체크리스트 (리뷰어·디자인 승인)

> 자동화로 잡기 어려운 항목만 사람이 본다.

- [ ] 로그인·헤더·사이드바에 브랜드 노출이 [`docs/Design.md`](../../docs/Design.md) §2 의도 위치와 일치
- [ ] **한 화면에 라임 Primary 핵심 버튼 1개** 원칙 ([`docs/Design.md`](../../docs/Design.md) §6·§8)
- [ ] 본문·보조 텍스트 대비 (라이트 배경에서 `#282828` / `#555555` 가독성)
- [ ] 파비콘·탭 제목·OG (적용 시) 가 [`layout.tsx`](../../도서물류관리프로그램/frontend/src/app/layout.tsx) 메타와 일치
- [ ] 사이드바 active 행 / 포커스 링 (`--ring`) 시각 회귀 없음

## 6. 스크린샷 번들 (붙여넣기)

| 화면 | 변경 전 | 변경 후 |
|------|---------|---------|
| 로그인 | (img) | (img) |
| 대시보드 | (img) | (img) |
| 사이드바 (확장 + active) | (img) | (img) |
| 마스터 테이블 (예: customer) | (img) | (img) |
| (선택) 설정 / 다크 모드 | (img) | (img) |

## 7. 참조

- 단일 원천: [`docs/Design.md`](../../docs/Design.md)
- 갭 분석: [`docs/design-gap-analysis.md`](../../docs/design-gap-analysis.md)
- 롤아웃 노트: [`docs/design-rollout-plan.md`](../../docs/design-rollout-plan.md)
- 규칙: [`.cursor/rules/design-bookioworks.mdc`](../../.cursor/rules/design-bookioworks.mdc)
- 스킬: [`.cursor/skills/bookioworks-design/SKILL.md`](../../.cursor/skills/bookioworks-design/SKILL.md)
- 자산 요청: [`docs/design-asset-request.md`](../../docs/design-asset-request.md)
