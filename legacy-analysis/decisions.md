# 의사결정 기록 (Decision Log)

## 형식
각 결정은 아래 형식으로 기록한다:
- **ID**: DEC-XXX
- **일자**: YYYY-MM-DD
- **결정 사항**: 무엇을 결정했는가
- **배경/근거**: 왜 이 결정을 했는가
- **대안**: 검토했지만 선택하지 않은 대안
- **영향**: 이 결정으로 인해 바뀌는 것
- **결정자**: 누가 결정했는가

---

## 결정 목록

### DEC-001: 8계층 하네스 엔지니어링 도입
- **일자**: 2026-04-11
- **결정 사항**: 델파이→웹 포팅에 8계층 하네스 엔지니어링 프레임워크를 핵심 운영 체계로 도입
- **배경/근거**: AI 기반 코드 변환 시 숨겨진 규칙 누락, 이벤트 순서 오류, 트랜잭션 경계 파괴 위험이 높음. 행위 보존을 위해 체계적 분석→분해→검증 루프가 필수
- **대안**: (1) 직접 코드 변환 (2) 4계층 하네스 (3) 외부 마이그레이션 도구
- **영향**: 전체 프로젝트 구조가 하네스 계층 기반으로 설계됨
- **결정자**: 메인개발자

### DEC-002: 프로젝트 대시보드 정적 사이트 구성
- **일자**: 2026-04-11
- **결정 사항**: 프로젝트 관리 대시보드를 HTML+CSS+JS 정적 사이트 + JSON 파일 기반으로 구성, GitHub Pages 배포
- **배경/근거**: DB 없이 파일 기반으로 운영 가능, Git으로 이력 관리, 팀 전원이 JSON 편집→push로 상태 업데이트 가능
- **대안**: (1) React+Vite SPA (2) Next.js Static Export (3) Notion/Confluence
- **영향**: 대시보드 데이터 변경이 JSON 편집→git push 워크플로우로 고정됨
- **결정자**: 메인개발자

### DEC-003: 권장 포팅 순서 확정
- **일자**: 2026-04-11
- **결정 사항**: 기능별 포팅 순서를 위험도 기반으로 확정 - 읽기전용 조회 → 신규등록 → 수정/취소 → 배치/인쇄/장비 → 고객사 커스터마이징
- **배경/근거**: DB 변경이 없는 조회부터 시작하여 위험을 점진적으로 흡수. INSERT만 발생하는 등록이 다음. UPDATE/DELETE는 트랜잭션 경계 검증 후.
- **대안**: 화면 단위 순차 포팅, 고객사별 순차 포팅
- **영향**: Sprint 4 구현 순서에 직접 반영됨
- **결정자**: 메인개발자 + 기획자

### DEC-004: 인쇄·바코드 웹 대체 1차 방향
- **일자**: 2026-04-21
- **결정 사항**: 인쇄는 **브라우저 인쇄(HTML/CSS) + 라벨 서버 PDF** 하이브리드, 바코드 입력은 **키보드 웨지(USB-HID)**를 1차 채택. 라벨 직결·Web Serial/로컬 브리지는 베타 후 OQ-002 결과로 재검토.
- **배경/근거**: 레거시는 `Printers`/`QuickRpt`/`Printer.Canvas`(OS 스풀 의존), `Tong08.pas`에서 `CPort` 시리얼 바코드 단일 진입점 사용. 베타 합격선("종이로 출력된다 + 바코드가 입력된다")을 가장 적은 리스크로 충족하기 위함.
- **대안**: (1) 라벨 프린터 직결(드라이버·OS 종속 위험) (2) Web Serial 우선(브라우저 호환성 위험) (3) 클라이언트 네이티브 헬퍼(설치·운영 비용)
- **영향**: 핵심 시나리오 C7·C8 계약 형태, 베타·인쇄 결과 게이트(#5) 입력물 형식
- **결정자**: 메인개발자 (현업 OQ-002 클로저로 보강 예정)
- **참조**: [`docs/decision-print-scanner-web.md`](../docs/decision-print-scanner-web.md), [`docs/legacy-print-scanner-integration-survey.md`](../docs/legacy-print-scanner-integration-survey.md)

### DEC-005: 로그인 비밀번호 평문 → 단방향 해시 마이그레이션 (D-LOGIN-1)
- **일자**: 2026-04-22
- **결정 사항**: `Id_Logn.Gpass` 평문 컬럼을 **bcrypt(work factor 12) 또는 argon2id** 단방향 해시로 전환. 기존 평문은 별도 컬럼에 1회 한정 보관(`Gpass_legacy`)하고 첫 로그인 성공 시 해시로 변환 후 평문 삭제(lazy migration).
- **배경/근거**: 레거시 `Chul.pas` L451 평문 비교는 GDPR/개인정보보호법 위반 + 내부자 위협 노출. 일괄 마이그레이션은 사용자 동시 로그아웃 필요 → lazy migration 으로 베타 무중단 가능. OQ-DBL-002 매칭.
- **대안**: (A) 일괄 변환 후 강제 비밀번호 재설정 (운영 부담) (B) HMAC-SHA256 + salt (해시 함수 강도 부족 우려) (C) 현행 평문 유지 (탈락)
- **영향**: contract `migration/contracts/login.yaml` D-LOGIN-1, test pack `TC-LOGIN-001/003` 픽스처 마이그레이션, performance(bcrypt ~80~120ms 추가 — TC-LOGIN-008 p95<500ms 내 수용 가능)
- **결정자**: 메인개발자 + 보안 검토자 (approvals.json id 3)
- **참조**: `migration/contracts/login.yaml` deltas D-LOGIN-1, OQ-DBL-002

### DEC-006: 라이선스 키 검증 클라이언트 레지스트리 → 서버 측 정책 (D-LOGIN-2)
- **일자**: 2026-04-22
- **결정 사항**: 레거시의 클라이언트 레지스트리 `ChulpanKey/Chul001~003Key` 매칭을 **서버 측 라이선스 테이블(`License_Tenant`) + JWT claim 발급**으로 대체. 베타 단계는 라이선스 검증을 비활성(전 사용자 PASS) 하고 내부오픈 게이트 #3 입력 시점에 활성.
- **배경/근거**: 웹은 클라이언트 레지스트리 접근 불가 + 베타 합격선("로그인이 된다")을 단순화. 라이선스 운영 정책은 D-LOGIN-4(테넌트) 와 묶어 서버 단일 출처로 통합.
- **대안**: (A) 웹에서 키를 사용자 입력 (UX 후퇴) (B) 클라이언트 헬퍼 설치 (DEC-002 정적 사이트 원칙 위배) (C) 키 검증 영구 폐지 (라이선스 통제 상실)
- **영향**: contract D-LOGIN-2, failure_codes `AUTH_KEY_REGISTER_REQUIRED` 베타 비활성, approvals #1 입력 충족
- **결정자**: 메인개발자 (approvals.json id 1)
- **참조**: `migration/contracts/login.yaml` deltas D-LOGIN-2, OQ-001

### DEC-007: '0000' 슈퍼유저 분기 베타 보존, 내부오픈에서 role 일반화 (D-LOGIN-3)
- **일자**: 2026-04-22
- **결정 사항**: 베타 단계는 **`Hcode='0000' = is_super=true`** 동등 동작 보존(가시성 필터 SQL-LOGIN-2-VISIBILITY 포함). 내부오픈 게이트 #4 입력 시점에 `Id_Logn.role` 컬럼 신설로 일반화하고 `'0000' → role='admin'` 마이그레이션.
- **배경/근거**: `Chul.pas` L486~L515 의 슈퍼유저 분기는 가시성 필터 + 메뉴 잠금 등 다수 화면에 영향. 베타에서 즉시 일반화하면 회귀 위험 큼. 단계적 일반화로 위험 분산.
- **대안**: (A) 베타부터 즉시 role 일반화 (회귀 위험) (B) 영구 보존 (확장성 상실)
- **영향**: TC-LOGIN-002/011 베타 통과, 내부오픈 진입 시 추가 마이그레이션 작업, approvals #4 입력
- **결정자**: 메인개발자 (approvals.json id 4)
- **참조**: `migration/contracts/login.yaml` deltas D-LOGIN-3, OQ-001

### DEC-008: 사용자→테넌트 자동 매핑 옵션 A 채택 — `Id_Logn.tenant_id` (D-LOGIN-4)
- **일자**: 2026-04-22
- **결정 사항**: 웹 멀티테넌시 매핑은 **옵션 A** (`Id_Logn` 에 `tenant_id` 컬럼 추가, 로그인 SELECT 결과로 컨텍스트 결정, JWT claim `tenant_id` 동봉, 모든 후속 API 에서 RLS-style 필터) 채택.
- **배경/근거**: 레거시 정적 분석 결과 (`Chul.pas` L376~L427) 사용자→테넌트 매핑 코드 부재(고객사별 EXE/Config.Ini 단일테넌트 모델). 옵션 A 가 (1) 사용자 입력 0 (2) 단일 식별자 (3) 코드 변경 최소 (4) 서브도메인 의존 0 — 4개 기준 모두 만족.
- **대안**:
  - 옵션 B (별도 user_tenant 매핑 테이블 + 선택 UI): 이중 소속 사용자 지원에 유리하나 UI 추가·DB 조인 +1
  - 옵션 C (서브도메인 cust1.app/...): 운영 단순화 강점, 그러나 도메인·SSL·DNS 운영 비용 + 단일 사용자 다중 테넌트 불가
- **영향**: contract D-LOGIN-4, test pack TC-LOGIN-010/012, **모든 후속 시나리오의 RLS 필터 의무**, OQ-LOGIN-1 closure, DB 마이그레이션 1회 (`ALTER TABLE Id_Logn ADD tenant_id`)
- **잔존 위험**: 잘못된 매핑 시 다른 고객사 데이터 노출(data 축 즉시 차단) — TC-LOGIN-012 `must_not` 로 회귀 차단.
- **결정자**: 메인개발자 + 기획자 (approvals.json id 4)
- **참조**: `migration/contracts/login.yaml` deltas D-LOGIN-4, OQ-LOGIN-1, `docs/c1-login-evaluation-report.md` §6

---
*최종 업데이트: 2026-04-22 — DEC-005~008 추가 (C1 로그인 closure). (이전: 2026-04-21 DEC-004)*
