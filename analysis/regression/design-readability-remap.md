# Design Readability Remap — 북이오웍스 CMS 가독성 보정

작업일: 2026-05-11

## 배경

Phase A 에서 `--primary` 를 Vivid Lime 으로 회전한 뒤, shadcn/Tailwind 의 전역 시맨틱 사용처(`text-primary`, `bg-primary/10`, 아이콘, 링크, subtle badge) 전반에 라임이 번져 실제 화면의 가독성이 떨어졌다. `docs/Design.md` §0 과 §8 은 CMS 를 차분한 작업 환경으로 정의하고 Vivid 사용을 CTA/알림에 한정하므로, `--primary` 와 `--vivid-lime` 의 의미를 분리했다.

## 변경 요약

| 축 | 보정 |
|----|------|
| SSOT | `docs/Design.md` §7·§8: CMS 에서 `--primary` 에 Vivid Lime 을 배치하지 않는다고 명시. |
| 토큰 | `globals.css`: `--primary` / `--sidebar-primary` 를 Bukio Black 계열로 재매핑, `--link` 신설, `--ring` 을 Info 계열로 조정. |
| CTA | 로그인/랜딩 핵심 CTA 만 `variant="brand-primary" size="brand"` 사용. |
| 상태 텍스트 | `--status-ok/warn/info` 는 PDF 페일톤을 그대로 텍스트에 쓰지 않고 접근성 보정 파생값으로 사용. |
| 타이포 | `@layer base` 에 국문 기본 `line-height: 1.5`, `letter-spacing: -0.02em`, h1/h2/h3 계층을 반영. |
| 레이아웃 | 앱 셸 본문 `p-4`, 헤더 `h-16`, 사이드바 `w-60` / 여백 증가. DOM 구조는 유지. |
| 테이블 | 공통 `DataGrid` 헤더를 `bg-muted`, `text-muted-foreground`, `text-[13px] font-semibold tracking-[-0.02em]` 으로 정리. |

## 사용처 감사 결과

1. 고위험 `text-primary` 링크/상태:
   - 활성화 성공/조건 충족 텍스트는 `text-status-ok` 로 이전.
   - 링크성 텍스트는 `text-link` 로 이전.
2. CTA:
   - 로그인/랜딩 시작하기는 `brand-primary` 로 명시.
   - 일반 `Button` default 는 다크 필 역할로 유지.
3. 장식/브랜드 모티프:
   - `MascotMotif` 는 `fill-brand-warm` 제거, `secondary` + `vivid-lime` 조합으로 이동.
4. 잔여 `primary`:
   - `bg-primary`, `text-primary`, `fill-primary` 잔여는 이제 Bukio Black 계열이므로 가독성 문제를 만들지 않는다.
   - 핵심 CTA 라임은 `--vivid-lime` / `brand-primary` 를 통해서만 노출한다.

## 자동 회귀 가드

| 가드 | 기대값 |
|------|--------|
| `ReadLints` | 변경 파일 0건 |
| `npx tsc --noEmit` | PASS |
| `npm run build` | PASS |
| 하드코딩 HEX | `LegacyFormRenderer.tsx` 의 Delphi 미리보기 회색 외 신규 없음 |
| `brand-warm` | TSX 사용 0건. globals 의 deprecated 변수만 남김 |

## 사람 검증 체크리스트

- [ ] 로그인 카드: 버튼은 라임 CTA 1개만 보이고, 설명/보조 텍스트가 충분히 진하다.
- [ ] 헤더/사이드바: 아이콘·아바타·active 행이 라임 텍스트로 보이지 않고 읽기 가능하다.
- [ ] 대시보드/랜딩: 카드 아이콘이 라임 글자처럼 튀지 않고, hover 경계가 차분하다.
- [ ] DataGrid: 헤더와 셀 간 구분이 명확하고, 작은 텍스트가 회색 배경에서 읽힌다.
- [ ] 다크 모드: `--primary` 가 라임이 아니라 밝은 중립색으로 보이고, CTA 만 라임이다.

## 후속

- `--brand-warm*` 변수는 Phase A.1 에서 제거 가능.
- 페이지별 `text-xs` / `text-[10px]` 는 많으므로, 실제 화면 스크린샷 기준으로 너무 작은 보조 텍스트만 선택 보정한다.
- PDF 에 8pt grid 수치가 없으므로 전체 레이아웃은 앱 셸 → DataGrid → 페이지 카드 순으로 단계 적용한다.
