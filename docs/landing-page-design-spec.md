# 랜딩 페이지 디자인 스펙 (화이트레벨)

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-24 |
| 대상 파일 | `도서물류관리프로그램/frontend/src/app/(public)/page.tsx` |
| 상태 | DRAFT |

---

## 1. 목표

- 다양한 사용자(총판 직원, 출판사 담당자, 관리자)가 처음 접속했을 때 **서비스 목적을 즉시 파악**하고
  알맞은 진입점(로그인·가입·총판 문의)을 찾을 수 있도록 한다.
- 기존 화이트레벨 디자인 시스템 (`BrandHero`, `Card`, `BrandBadge`, `MascotMotif`) 을 유지하며 보강.

---

## 2. 페이지 섹션 구성

### 2.1 Hero (BrandHero)

| 요소 | 내용 |
|------|------|
| 제목 | 도서물류관리프로그램 |
| 부제 | 도서 유통·재고·발송·통계를 하나로 통합하는 물류 관리 시스템. |
| CTA 1 (Primary) | "로그인" → `/login` |
| CTA 2 (Secondary) | "회원 가입" → `/signup` |
| CTA 3 (Ghost) | "총판 담당자 문의" → `/contact` (또는 mailto 링크, 별 사이클) |
| 트러스트 포인트 | 역할 기반 접근 제어 · 단일 인증 서버 · 감사 로그 |

### 2.2 이용 절차 — 4단계 Stepper

```
① 회원 가입 신청
   총판 소속 출판사 또는 독립 출판사로 가입 신청

② 사전 검증 / 관리자 검토
   총판 소속이면 화이트리스트 자동 확인. 독립 출판사는 관리자 검토.

③ 계정 활성화
   승인 후 안내를 통해 초기 비밀번호를 설정하고 계정을 활성화합니다.

④ 로그인 · 업무 시작
   계정 유형에 맞는 메뉴와 데이터에 즉시 접근합니다.
```

컴포넌트: `ProcessStepper` (4 아이템, 가로 배치 md+, 세로 배치 mobile)

### 2.3 주요 기능 카드 (4 Cards)

| 아이콘 | 제목 | 설명 |
|--------|------|------|
| BookOpen | 기초관리 | 거래처·도서·출판사·할인율 등 기초 마스터 데이터를 통합 관리합니다. |
| Truck | 출고/입고 관리 | 출고 접수, 입고 처리, 출고 현황을 실시간으로 파악합니다. |
| Package | 재고 관리 | 재고 조회, 재고 원장을 통해 정확한 재고 현황을 확인합니다. |
| BarChart3 | 통계/내역서 | 발송비, 입금 관리 및 다양한 통계 리포트를 생성합니다. |

### 2.4 계정 유형 안내 (3 컬럼 카드)

| 유형 | 제목 | 설명 | CTA |
|------|------|------|-----|
| T2-PUB | 총판 소속 출판사 | 소속 총판에 사전 등록된 출판사라면 온라인으로 직접 가입할 수 있습니다. | "소속 출판사로 가입" → `/signup?type=t2pub` |
| T3 | 독립 출판사 | 자체 물류나 도서 관리가 필요한 독립 출판사는 별도 가입 후 이용 가능합니다. | "독립 출판사로 가입" → `/signup?type=t3` |
| T2-DIST | 총판(물류사) | 총판 계정은 별도 개설 절차가 필요합니다. 담당자에게 문의해 주세요. | "총판 문의" → 이메일 링크 |

### 2.5 트러스트 바

아이콘 + 뱃지:
- `Shield` + "역할 기반 접근 제어 (RBAC)"
- `Server` + "단일 인증 서버 (DEC-051)"
- `ClipboardList` + "감사 로그"
- `BrandBadge variant="phase"` → "Phase 1"
- `BrandBadge variant="status"` → "시스템 정상"

### 2.6 Footer

```
© {year} 도서물류관리프로그램. Powered by Next.js + FastAPI.
```

---

## 3. 컴포넌트 추가

### `ProcessStepper`
경로: `frontend/src/components/brand/ProcessStepper.tsx`

Props:
```ts
interface Step {
  number: number;
  title: string;
  desc: string;
  icon?: LucideIcon;
}
interface ProcessStepperProps {
  steps: Step[];
  className?: string;
}
```

### 3분기 CTA 처리
- `signup?type=t2pub` 파라미터를 `SignupWizard` 가 읽어 Step1 선택을 pre-select.
- `signup?type=t3` 도 동일.

---

## 4. 색상 · 타이포 가이드

| 요소 | 값 |
|------|-----|
| Hero 배경 | `bg-gradient-to-b from-secondary via-background to-background` |
| Primary 버튼 | 기존 `shadow-md shadow-primary/20` 유지 |
| Stepper 활성 번호 | `bg-primary text-primary-foreground` |
| 카드 hover | `hover:border-primary/30 hover:shadow-lg hover:shadow-primary/5` |
| Footer | `bg-muted/20` |

---

## 5. 접근성 요건

- 모든 이미지/아이콘에 `aria-hidden="true"` 또는 `aria-label` 설정
- CTA 버튼 focus-visible 링 유지
- Lighthouse 접근성 점수 ≥ 90 목표
- `lang="ko"` root 유지
