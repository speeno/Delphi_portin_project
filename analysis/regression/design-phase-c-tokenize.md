# Design Phase C — 차트·지도·테이블 토큰화 회귀 매트릭스

> [`docs/design-rollout-plan.md`](../../docs/design-rollout-plan.md) §4 의 Phase C 1차 적용 (차트·지도). 테이블 헤더·합계 행과 NOTICE/IMPORTANT 컬러 블록 컴포넌트는 별도 후속 PR.

작업일: 2026-05-11

## 1. 변경 파일

| 파일 | 변경 |
|------|------|
| [`도서물류관리프로그램/frontend/src/lib/design-tokens.ts`](../../도서물류관리프로그램/frontend/src/lib/design-tokens.ts) | **신설** — 런타임 토큰 헬퍼. recharts/leaflet 처럼 CSS 변수를 직접 받지 못하는 라이브러리에 색을 주입할 때 본 모듈만 통과한다. SSR fallback 은 가이드 §3 HEX 와 동일. |
| [`도서물류관리프로그램/frontend/src/components/stats/charts.tsx`](../../도서물류관리프로그램/frontend/src/components/stats/charts.tsx) | `#2563eb`, `#16a34a`, `#f59e0b`, `#dc2626`, `#9333ea` 6 곳 → `readToken("chart-1")` 등 토큰 헬퍼. `PIE_COLORS` 상수 → `readChartPalette()`. 컴포넌트 본체에서 호출해 다크 모드 토글 시 stale 회피. |
| [`도서물류관리프로그램/frontend/src/components/dashboard/traffic-map-leaflet.tsx`](../../도서물류관리프로그램/frontend/src/components/dashboard/traffic-map-leaflet.tsx) | `#64748b/#dc2626/#ca8a04/#16a34a/#3b82f6` 5 곳 → `readStatusColor("neutral|crit|warn|ok")`/`readToken("status-info")`. 신호 단계 (속도 < 20 / < 40 / >= 40) 가 가이드 §3.5 status-* 토큰과 1:1. |

## 2. 자동 회귀 가드

| 가드 | 명령 | 결과 |
|------|------|------|
| 하드코딩 HEX | `rg -n '#[0-9a-fA-F]{6}\b' 도서물류관리프로그램/frontend/src --type tsx` | LegacyFormRenderer.tsx (Delphi 의도된 회색 톤) **만** 잔존 — 화이트리스트와 일치 |
| Type 체크 | `npx tsc --noEmit` | PASS (Exit 0) |
| Build | `npm run build` | PASS |
| Lint (신규) | `ReadLints` charts/leaflet/design-tokens | 0건 |

## 3. 토큰 매핑 (PR 리뷰어용)

| 위치 | 변경 전 (HEX) | 변경 후 (토큰) | 가이드 매핑 |
|------|---------------|----------------|-------------|
| Line / Bar 시리즈 1 (수량·primary) | `#2563eb` | `readToken("chart-1")` → Info Blue 페일톤 | §3.5 |
| Line / Bar 시리즈 2 (금액·secondary) | `#16a34a` | `readToken("chart-2")` → Positive Green 페일톤 | §3.5 |
| Pie 시리즈 5종 | `#2563eb / #16a34a / #f59e0b / #dc2626 / #9333ea` | `readChartPalette()` (Info / Positive / Warning / Error / Vivid Lime) | §3.5·§3.6 |
| 지도 신호 — 정보 없음 | `#64748b` | `readStatusColor("neutral")` → muted-foreground | §3.4 |
| 지도 신호 — 정체 (<20 km/h) | `#dc2626` | `readStatusColor("crit")` → destructive | §3.5 |
| 지도 신호 — 서행 (<40 km/h) | `#ca8a04` | `readStatusColor("warn")` → status-warn | §3.5 |
| 지도 신호 — 원활 (>=40) | `#16a34a` | `readStatusColor("ok")` → status-ok | §3.5 |
| 지도 BBOX 외곽 | `#3b82f6` | `readToken("status-info")` → Info Blue | §3.5 |

## 4. 사람 검증 체크리스트

- [ ] 통계 페이지 (`/stats/*`) 의 라인·바·파이 차트 색이 가이드 §3.5 페일톤으로 바뀜.
- [ ] 대시보드 ITS 트래픽 맵의 폴리라인 신호색 (정체/서행/원활) 인지 가능.
- [ ] BBOX 사각형이 라이트 배경에서 너무 옅지 않은지 (필요 시 `--status-info` 채도 조정).
- [ ] 다크 모드에서 차트 색상이 `--chart-*` 다크 변형으로 자연 회전.
- [ ] LegacyFormRenderer 의 `#ececec/#d4d0c8` 등은 **의도** — 본 PR 에서 변경하지 않았는지 확인.

## 5. 후속 작업 (Phase C 잔여)

- 테이블 헤더·합계 행: DataGrid 컴포넌트 한 곳에 Pale Lime 배경 적용 — 별도 작은 PR.
- NOTICE / IMPORTANT 컬러 블록: `components/ui/color-block.tsx` 신설 — 별도 작은 PR.
- `--chart-*` 토큰 자체의 OKLCH 미세 조정 (실 데이터 시연 후 디자인 검수).

## 6. PR 본문 템플릿

```text
제목: refactor(design): phase C — chart/map color tokens via design-tokens helper

요약:
- lib/design-tokens.ts 신설 — recharts/leaflet 등 CSS 변수 미수용 라이브러리용 토큰 헬퍼.
- charts.tsx / traffic-map-leaflet.tsx 의 하드코딩 HEX 11곳 → 토큰 헬퍼.
- LegacyFormRenderer 의 회색 톤은 의도 — 변경 없음 (rules §2 화이트리스트).

자동 가드:
- npx tsc --noEmit PASS / npm run build PASS / ReadLints 0건
- rg 화이트리스트 외 신규 HEX 0건

후속: DataGrid 헤더·합계 / color-block 컴포넌트는 별도 PR.
```
