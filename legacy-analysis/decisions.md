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
- **2026-04-20 보강 (C7 Phase 1)**: "라벨 = 서버 PDF" 분기는 DEC-037 (WeasyPrint 단일 엔진) + DEC-038 (우편엽서 1종) 으로 동결. 5종 양식 (P1-A ~ P1-E) 도 동일 엔진으로 PDF 다운로드 추가 (HTML 미리보기 = 유지, .pdf = 동시 제공). 라벨 직결·Web Serial 은 여전히 OQ-002 잔여 항목 (Phase 2 이후).
- **배경/근거**: 레거시는 `Printers`/`QuickRpt`/`Printer.Canvas`(OS 스풀 의존), `Tong08.pas`에서 `CPort` 시리얼 바코드 단일 진입점 사용. 베타 합격선("종이로 출력된다 + 바코드가 입력된다")을 가장 적은 리스크로 충족하기 위함.
- **대안**: (1) 라벨 프린터 직결(드라이버·OS 종속 위험) (2) Web Serial 우선(브라우저 호환성 위험) (3) 클라이언트 네이티브 헬퍼(설치·운영 비용)
- **영향**: 핵심 시나리오 C7·C8 계약 형태, 베타·인쇄 결과 게이트(#5) 입력물 형식
- **결정자**: 메인개발자 (현업 OQ-002 클로저로 보강 예정)
- **참조**: [`docs/decision-print-scanner-web.md`](../docs/decision-print-scanner-web.md), [`docs/legacy-print-scanner-integration-survey.md`](../docs/legacy-print-scanner-integration-survey.md)

### DEC-005: 1차 포팅 비밀번호 평문 보존, 해시 마이그레이션은 후속 이관 (D-LOGIN-1)
- **일자**: 2026-04-22 (2026-04-22 1차 동결)
- **결정 사항**: **1차 포팅에서는 `Id_Logn.Gpass` 평문 그대로 사용**. 레거시와 동일한 평문 동등 비교(`Gpass = :gpass`) 유지. bcrypt/argon2id 해시 마이그레이션 및 lazy migration 정책은 **후속 작업으로 분리(post-1차)**.
- **배경/근거**: 1차 포팅의 합격선은 **"기존 사용자가 기존 ID/PW 그대로 로그인"** 이며, 사용자 비밀번호 강제 변경·이관 절차 없이 무중단 전환이 최우선. 해시 도입은 데이터 마이그레이션 + 운영 절차(첫 로그인 시 변환) + 보안 검토 일정이 별도 필요하므로 1차 범위에서 분리.
- **대안**:
  - (A) 1차부터 lazy migration 도입 (이전 검토안) — 운영 절차·보안 검토 비용으로 1차 일정 부담
  - (B) 1차부터 일괄 해시 변환 + 강제 비밀번호 재설정 — 사용자 영향 큼
  - (C) 평문 영구 유지 — 보안 위험 누적 (탈락)
- **영향**:
  - contract `migration/contracts/login.yaml` D-LOGIN-1: **1차 in_scope=false**, `equivalence.data` 에서 Gpass 평문 비교 명시
  - test pack `TC-LOGIN-001/003` 픽스처 평문 그대로 (변경 없음)
  - performance: bcrypt 비용 0 (TC-LOGIN-008 p95 여유)
  - OQ-DBL-002 (평문 비밀번호) **부분 보류** (1차 범위에서 의도적 보존, 후속에서 재개)
- **후속 작업 (post-1차)**: 별도 결정 DEC-XXX 로 해시 정책·마이그레이션 일정 동결. 본 DEC-005 의 (A) 안이 1순위 후보.
- **결정자**: 메인개발자
- **참조**: `migration/contracts/login.yaml` deltas D-LOGIN-1, OQ-DBL-002

### DEC-006: 라이선스 키 검증 서버 측 제어 (설치형 아님) (D-LOGIN-2)
- **일자**: 2026-04-22
- **결정 사항**: 웹은 **설치형 프로그램이 아니므로** 클라이언트 레지스트리 기반 라이선스 키 검증(`ChulpanKey/Chul001~003Key`)을 **완전히 폐지**하고 **서버 측 단일 통제**로 전환. 1차 포팅에서는 라이선스 검증 자체를 비활성(전 사용자 PASS)하여 동작에 영향 없음. 라이선스 운영이 필요해지는 시점에 서버측 정책(요금제·만료·인스턴스 한도 등)을 별도 결정으로 도입.
- **배경/근거**:
  - 레지스트리는 클라이언트 OS 의존 — 웹(SaaS) 모델에서 무의미
  - 사용자가 키를 입력하는 UX 후퇴 회피
  - 단일 출처 원칙(서버 = 라이선스 통제 단일 지점)
- **대안**: (A) 웹에서 키를 사용자 입력 (UX 후퇴) (B) 클라이언트 헬퍼 설치 (DEC-002 정적 사이트 원칙 위배) (C) 영구 폐지 (탈락 — 비즈니스 통제 상실)
- **영향**:
  - contract D-LOGIN-2: **1차 in_scope=false** (서버측 정책은 후속)
  - failure_codes `AUTH_KEY_REGISTER_REQUIRED` **1차 발생 없음** (응답 스키마는 향후 호환을 위해 보존)
  - approvals #1 입력 충족 (라이선스 의존 0)
- **결정자**: 메인개발자 (approvals.json id 1)
- **참조**: `migration/contracts/login.yaml` deltas D-LOGIN-2, OQ-001

### DEC-007: '0000' 슈퍼유저 분기 1차 포팅 제외, 권한 관리 기능에 통합 (D-LOGIN-3)
- **일자**: 2026-04-22
- **결정 사항**: 레거시 `Hnnnn='0000'` 슈퍼유저 특수 분기(가시성 필터 SQL `G7_Ggeo Where Chek5='show1'` 포함)를 **1차 포팅에서 완전 제외**. 슈퍼유저/관리자 권한은 **추후 별도 권한 관리 기능**(역할·권한 매트릭스 화면)이 추가될 때 통합 설계로 도입.
- **배경/근거**:
  - 1차 포팅 합격선은 "기존 사용자 로그인 + 기본 업무 화면 동작" — 슈퍼유저 가시성 필터는 비합격선
  - `Chul.pas` L486~L515 의 슈퍼유저 분기는 메뉴 잠금·가시성 필터 등 다수 화면에 영향 → 부분 도입 시 일관성 위험
  - 권한 모델은 별도 화면(C10 권한 관리)에서 통합 설계가 더 타당
- **대안**: (A) 베타부터 보존 후 단계적 일반화 (이전 검토안) — 1차 일정 부담 (B) 영구 보존 (확장성 상실)
- **영향**:
  - contract D-LOGIN-3: **1차 in_scope=false** (모든 사용자 동등 권한으로 1차 동작)
  - data_access **SQL-LOGIN-2-VISIBILITY 1차 in_scope=false** (G7_Ggeo SELECT 호출 없음)
  - test pack TC-LOGIN-002, TC-LOGIN-011: **1차 out_of_scope** (관리자/0000 동등 분기 검증 미수행)
  - 후속 화면 C10 권한 관리 와 통합 (`M-S1-PORT-C10` 의존 추가)
  - approvals #4 입력 (1차 폐지 합의)
- **결정자**: 메인개발자 (approvals.json id 4)
- **참조**: `migration/contracts/login.yaml` deltas D-LOGIN-3, OQ-001, `dashboard/data/porting-screens.json` C10

### DEC-008: 사용자→테넌트 자동 매핑 1차 포팅 제외, 단일 테넌트 운영 (D-LOGIN-4)
- **일자**: 2026-04-22
- **결정 사항**: **1차 포팅은 단일 테넌트 운영**(레거시와 동일한 "고객사별 별도 인스턴스" 모델 유지)으로 진행. 사용자→테넌트 자동 매핑(`Id_Logn.tenant_id` 컬럼 신설, JWT claim 동봉, RLS-style 필터)은 **후속 작업으로 이관**. 1차 합격선은 **"기존 사용자가 기존 아이디/패스워드로 로그인 가능"** 이며 멀티테넌시는 비합격선.
- **배경/근거**:
  - 1차 합격선("기존 ID/PW 그대로 로그인")은 단일 테넌트 모델로 충분
  - 멀티테넌시 도입 시 (1) `Id_Logn` 스키마 변경 (2) 모든 후속 API의 RLS 필터 (3) 잘못된 매핑 시 데이터 노출 위험 — 모두 1차 일정에 부담
  - 운영 모델 자체가 미합의(OQ-LOGIN-1 미해결) — 별도 합의 사이클 필요
- **대안**:
  - (A) 옵션 A 1차 채택 (이전 검토안 — `Id_Logn.tenant_id`) — 일정·리스크 부담
  - (B) 옵션 B 사용자 선택 UI — UX 후퇴
  - (C) 옵션 C 서브도메인 — 인프라 비용
- **영향**:
  - contract D-LOGIN-4: **1차 in_scope=false** (단일 테넌트 명시)
  - inputs.tenant_hint **삭제** (1차 미사용)
  - test pack TC-LOGIN-010/012: **1차 out_of_scope**
  - fixtures `tenant_id` 컬럼 **삭제** (단일 테넌트 가정)
  - 후속 화면 시나리오 RLS 필터 의무 **해제**(1차)
  - DB 마이그레이션 0건 (1차)
  - OQ-LOGIN-1 **후속 이관** (closure 아님, 1차 범위 외로 보류)
- **후속 작업 (post-1차)**: 멀티테넌시 합의 사이클 → 별도 결정 DEC-XXX 로 옵션 A/B/C 확정 → DB 마이그레이션 + 모든 시나리오 RLS 패치.
- **결정자**: 메인개발자 + 기획자 (approvals.json id 4)
- **참조**: `migration/contracts/login.yaml` deltas D-LOGIN-4, OQ-LOGIN-1, `docs/c1-login-evaluation-report.md` §6

### DEC-009: C2 출고 접수 권한키(F21/F22/F26) 1차 포팅 제외 (D-OUT-1)
- **일자**: 2026-04-25
- **결정 사항**: 레거시 `TSobo27` 의 등록·수정·삭제 권한 분기(`F21`/`F22`/`F26`)를 **C2 1차 포팅에서 제외**. 1차에서는 인증된 사용자(JWT 보유)는 모두 동일 권한으로 신규/수정/취소/조회 가능. 권한 매트릭스는 **DEC-007 과 동일하게 후속 권한 관리 시나리오(C10)** 와 통합 도입.
- **배경/근거**:
  - C2 1차 합격선은 "출고 주문 신규+수정+취소+조회 CRUD 동작" — 권한 분기는 합격선 외
  - DEC-007 슈퍼유저 분기 1차 제외와 일관 (모든 인증 사용자 동등)
  - 권한키별 분기를 1차에 일부만 도입하면 사용자 혼란 + UI 분기 코드가 후속 일반 권한 모델과 충돌
- **대안**: (A) 1차부터 F21/F22/F26 적용 — 일정·UX 후퇴 (B) 권한키 영구 제거 — 비즈니스 통제 상실 (탈락)
- **영향**:
  - contract `migration/contracts/outbound_order.yaml` D-OUT-1: **1차 in_scope=false**
  - test pack TC-OUT-010 (권한 차단): **phase1_in_scope=false** (보류)
  - 후속 시나리오 C10 (권한 관리) 와 통합 (`HA-OUT-PERM` 후속 액션 등록)
- **후속 작업**: C10 권한 관리 사이클에서 F21/F22/F26 매트릭스 + RBAC 통합.
- **결정자**: 메인개발자
- **참조**: `migration/contracts/outbound_order.yaml` deltas D-OUT-1, DEC-007

### DEC-010: C2 바코드 결합(Tong08) 1차 포팅 제외, 별도 시나리오로 분리 (D-OUT-2)
- **상태 (2026-04-20 마감)**: ✅ 후속 작업 **완료**. C8 Phase 1 (바코드 스캔 매칭) 사이클에서 DEC-004 USB-HID 1차 + DEC-040 (서버 매칭/클라이언트 라인 반영 분리) 로 일괄 도입. 출고 (Sobo27) + 입고 (Sobo22) + 반품 (Sobo23) 3 화면에 동일 `ScanInput` 공통 컴포넌트 통합. Web Serial 직결은 OQ-002-R 으로 분리 잔류.
- **일자**: 2026-04-25
- **배경/근거**:
  - 바코드 입력은 USB-HID 키보드 웨지 또는 Web Serial — 디바이스/브라우저 호환성 검증 별도 사이클 필요 (DEC-004)
  - 1차 합격선은 "수기 입력으로 출고 주문 등록 가능" 으로 충분
  - C2 와 바코드 동시 진행 시 디바이스 의존성으로 1차 일정 위험 증가
- **대안**: (A) 1차부터 키보드 웨지 도입 — UX 검증·테스트 비용 (B) Web Serial 1차 — 브라우저 호환성 위험
- **영향**:
  - contract D-OUT-2: **1차 in_scope=false**
  - test pack TC-OUT-011 (바코드 입력): **phase1_in_scope=false**
  - 1차 화면에서 바코드 입력 영역 미노출 (후속 확장 지점만 docstring 메모)
- **후속 작업**: 바코드 시나리오(가칭 C8) 사이클에서 `Tong08.pas` 인용 + DEC-004 방향성으로 통합.
- **결정자**: 메인개발자
- **참조**: `migration/contracts/outbound_order.yaml` deltas D-OUT-2, DEC-004

### DEC-011: C2 인쇄 연계 1차 포팅 제외, C7 인쇄 시나리오로 이관 (D-OUT-3)
- **일자**: 2026-04-25
- **결정 사항**: 출고 주문 등록 후 거래명세서·라벨 인쇄(`Printers`/`QuickRpt` 호출)를 **C2 1차 포팅에서 제외**. 인쇄는 **C7 인쇄 시나리오** 사이클에서 DEC-004 방향성(브라우저 인쇄 + 라벨 PDF 하이브리드)으로 일괄 도입.
- **배경/근거**:
  - 인쇄는 C7 별도 핵심 시나리오로 이미 정의됨 (베타 필수 라인 포함)
  - 출력 양식(거래명세서 vs 라벨) 별로 레이아웃·용지 검토 필요 — C7 사이클에서 통합 처리
  - C2 1차 합격선은 "DB 등록까지" — 인쇄 트리거는 합격선 외
- **대안**: (A) C2 1차에 미니 인쇄 기능 — 양식 중복 작업 (B) 영구 분리 — UX 단절 (탈락, C7 통합 권장)
- **영향**:
  - contract D-OUT-3: **1차 in_scope=false**
  - test pack TC-OUT-012 (인쇄 트리거): **phase1_in_scope=false**
  - 1차 UI 에 "인쇄" 버튼 미노출 (또는 disabled+tooltip "C7 사이클에서 활성화")
- **후속 작업**: C7 인쇄 사이클에서 출고 주문 거래명세서·라벨 양식 정의 + 실제 트리거 연결.
- **결정자**: 메인개발자
- **참조**: `migration/contracts/outbound_order.yaml` deltas D-OUT-3, DEC-004, `dashboard/data/porting-screens.json` C7

### DEC-012: C2 출고 주문 물리 삭제 1차 포팅 제외, 취소 플래그(소프트 삭제)만 1차 포함 (D-OUT-4)
- **일자**: 2026-04-25
- **결정 사항**: `S1_Ssub` 헤더 + `Sg_Csum` 라인의 **물리 삭제(DELETE) 는 1차 포팅에서 제외**. 1차에서는 **취소 플래그 UPDATE(소프트 삭제)** 만 지원. 물리 삭제는 정합성·감사 요건(타 시나리오와의 참조 무결성, 실제 운영 정책) 검토 후 후속 사이클에 별도 결정으로 도입.
- **배경/근거**:
  - 레거시 Subu27 에서도 일반 사용자는 취소(상태 변경) 위주, 관리자만 물리 삭제 사용 패턴 — DEC-009 권한 분기 제외와 정합
  - 물리 삭제 시 다른 시나리오(반품 C4, 정산 등) 의 참조 무결성 일괄 검증 필요 — 1차 범위 외
  - 감사 로그 보존 관점에서도 소프트 삭제가 1차 안전판
- **대안**: (A) 1차에 물리 삭제 포함 — 정합성 검증 부담 (B) 영구 폐지 — 운영 유연성 상실 (탈락)
- **영향**:
  - contract D-OUT-4: **1차 in_scope=false**
  - 1차 endpoint **`PATCH /api/v1/outbound/orders/{id}/cancel` 만 제공**, `DELETE` 메서드 미제공
  - test pack: 물리 삭제 케이스 작성 안 함 (deferred 메모만)
  - 감사 로그: cancel 액션은 기록 (audit_service)
- **후속 작업**: 참조 무결성 매트릭스(다른 시나리오 의존) 작성 후 별도 결정으로 물리 삭제 도입 여부·정책 동결.
- **결정자**: 메인개발자
- **참조**: `migration/contracts/outbound_order.yaml` deltas D-OUT-4, DEC-009

### DEC-019: 환경설정 경계 — Sobo19(레거시) vs Wave D(웹 플랫폼) 분리, 마스터 PATCH 는 «수정 ON · 삭제 OFF»
- **일자**: 2026-04-18
- **결정 사항**: 레거시 Sobo19 의 비즈니스 옵션은 그대로 둔다(별도 화면). 웹 전용 운영/환경설정은 Wave D 의 `application_settings` 로 분리한다. C9 마스터(거래처 Sobo11 / 도서 Sobo14) 의 1차 PATCH 는 **수정 가능 / 삭제는 금지**. 신규 INSERT 와 DELETE 는 후속 사이클에서 결정.
- **배경/근거**:
  - Sobo19 는 인쇄·바코드·기본값 등 화면 전용 옵션 — 사용자 혼동 방지 위해 web 플랫폼 설정과 경계.
  - 마스터 삭제는 다른 시나리오(C2 출고/C6 조회) 와 참조 무결성을 함께 봐야 함 — DEC-012 와 같은 정책으로 1차 보류.
- **영향**:
  - contract `master_data.yaml`: SQL-MAS-3/6 (PATCH) 만 활성, DELETE 미제공.
  - 사이드바 라벨 정정: "환경설정" → "환경설정(레거시)".
  - Wave D `/admin/settings` 페이지에서 application_settings 만 다룸.
- **결정자**: 메인개발자
- **참조**: `migration/contracts/master_data.yaml`, `migration/contracts/admin_web_platform.yaml`

### DEC-020: 웹 RBAC 별도 — 레거시 Id_Logn.Fxx 와 매핑 테이블 1단으로 연결
- **일자**: 2026-04-18
- **결정 사항**: 웹 권한 모델은 `web_roles` / `web_role_permissions` / `web_user_roles` 로 신규 운용한다. 레거시 `Id_Logn.Fxx` 와는 1:1 `legacy_permission_map` 1단으로만 연결한다. 1차 MVP 는 가드 미적용(인증된 사용자 = 모두 가능, DEC-009 패턴) — Phase 2 에서 미들웨어로 강제.
- **배경/근거**:
  - 레거시 권한 키는 화면 단위(`F21/F22/F26` 등) 로 의미가 닫혀있어 웹의 동작 단위 (master.read/write 등) 와 직접 1:1 매칭 불가.
  - 매핑 테이블 1단으로 두면 Phase 2 가드 활성 시점에 양 모델을 동시에 충족 가능.
- **영향**:
  - admin contract `ADMIN-4~7` endpoints, `legacy_permission_map` 시드 3건.
  - `WebAdmRBAC` 페이지에서 시드 역할 + 매핑표 표시.
- **결정자**: 메인개발자
- **참조**: `migration/contracts/admin_web_platform.yaml`, `backend/app/services/admin_service.py`

### DEC-021: 서버 프로필 화이트리스트 — 사용자별 server_id 매핑
- **일자**: 2026-04-18
- **결정 사항**: `web_user_servers` 테이블로 사용자별 허용 `server_id` 화이트리스트를 운용한다. 비어있으면 1차는 "모두 허용" 으로 폴백 (안전 마진). JWT 발급/요청 가드에서 활용.
- **배경/근거**:
  - 운영 환경 분리(테스트/운영) 시 특정 계정만 운영 서버 접근하는 케이스가 발생.
  - 1차에서 강제하면 기존 사용자 모두 차단되므로, 화이트리스트 비어있을 때 폴백 정책 유지.
- **영향**:
  - admin contract `ADMIN-1~3` + `is_server_allowed` helper.
  - 향후 `auth/login` 에서 server_id 가 화이트리스트에 있는지 검증 가능.
- **결정자**: 메인개발자
- **참조**: `backend/app/services/admin_service.py:is_server_allowed`

### DEC-022: 개정별 환경설정 — 모든 변경은 history 강제 적재, 물리 삭제 금지
- **일자**: 2026-04-18
- **결정 사항**: `application_settings` 1행 = (scope, key) 의 현재 revision/value 로 둔다. 모든 변경은 `application_settings_history` 에 새 revision 으로 자동 추가된다. **DELETE 는 금지**, 롤백 = 이전 revision 의 value 를 새 revision 으로 다시 기록. 모든 변경은 audit.admin 로거에 기록되며 `actor` (current user.gcode) 가 비어있으면 400.
- **배경/근거**:
  - 운영 설정은 잘못 변경 시 빠른 롤백이 필요 — history 가 1급 시민이어야 함.
  - 물리 삭제 허용 시 audit 무결성 깨짐 — DEC-022 fail-safe 로 봉쇄.
- **영향**:
  - admin contract `ADMIN-8~11` endpoints, history 강제 적재 invariant.
  - `WebAdmEnv` 페이지에서 history/롤백 UI.
- **결정자**: 메인개발자
- **참조**: `backend/app/services/admin_service.py:upsert_setting,rollback_setting`

### DEC-023: C9 마스터 단일 원천 확정 — Sobo11/14/17/38/39/45 채택, 통계 분리
- **일자**: 2026-04-18
- **결정 사항**: 화면 카드 분석 결과 다음 폼을 「단일 원천」으로 확정한다. Sobo36/37/43 은 통계/조회 화면이므로 마스터에서 분리하고 사이드바 라벨에 "(통계)" 를 표기한다.
  - 거래처 마스터 = **Sobo11** (G1_Ggeo + G1_Gbun, CRUD 11건)
  - 도서 마스터 = **Sobo14** (G4_Book + G4_Gbun, CRUD 13건)
  - 출판사·G7거래처 마스터 = **Sobo17** (G7_Ggeo + G7_Gbun, CRUD 26건, 자동완성과 동일 테이블)
  - 도서코드 = **Sobo38** (G4_Book READ only, SELECT 2건)
  - 할인율 대표 = **Sobo39** (G7_Ggeo.Gpper, 4 변종 중 대표 1폼만 1차)
  - 물류비 = **Sobo45** (G5_Ggeo.Gposa READ)
- **배경/근거**:
  - Sobo36/37 는 T6_Ssub/Sv_Ghng 등 통계 테이블에 접근 — 마스터 CRUD 폼이 아님.
  - 자동완성용 G7_Ggeo (Sobo17) 와 마스터 G1_Ggeo (Sobo11) 는 다른 거래처 종류 — 라벨로 구분.
- **영향**:
  - frontend `form-registry.ts`: Sobo11/14/17/38/39/45 에 `route`/`phase: phase1` 부여, Sobo36/37/43 라벨 정정.
  - backend `masters_service.py`: 자동완성 함수는 보존, 신규 list/get/update 함수 추가.
- **결정자**: 메인개발자
- **참조**: `analysis/screen_cards/Sobo{11,14,17,38,39,45}*.md`, `migration/contracts/master_data.yaml`

### DEC-024: aiomysql 운영 DB 문자셋 — bytes 수신 + EUC-KR replace 디코딩으로 패킷 깨짐 차단
- **일자**: 2026-04-18
- **결정 사항**: 모던 백엔드의 aiomysql 풀은 `use_unicode=False` 로 raw bytes 를 받고, 결과 row 는 `_normalize_aiomysql_row` 가 EUC-KR `errors='replace'` 로 디코딩한다. 동일 정책을 모든 신규 입출력 라우트에 의무화한다.
- **배경/근거**: 운영 G4_Book 의 일부 row 가 `0x8b` 등 비정상 바이트를 포함 — `pymysql` 기본 디코더가 예외를 던지면서 후속 `Packet sequence number wrong` 으로 풀이 오염되어 600건 페이지 후 500 발생.
- **영향**: `app/core/db.py:_normalize_aiomysql_*` 가 단일 원천. 추가 디코더 신설 금지.
- **결정자**: 메인개발자
- **참조**: HOT-MAS-3, `도서물류관리프로그램/backend/app/core/db.py`

### DEC-027: C3 입고 접수 1차 — INSERT/UPDATE ON, 소프트 취소, FTP 자동수신 → 사용자 파일 업로드 우회
- **일자**: 2026-04-19
- **결정 사항**: C3 1차 포팅은 입고 본 폼(TSobo22)의 INSERT/UPDATE 를 활성화하고 물리 DELETE 는 금지(소프트 취소 = `Yesno='2'`, C2 패턴 재사용). FTP 자동수신(TSobo38)은 외부 FTP 서버 의존 없이 **사용자 파일 업로드(EUC-KR CSV/TXT)** 로 우회한다. 일별/기간별 리포트(TSobo54/57)는 READ-only 그대로.
- **배경/근거**:
  - 입고는 신규 INSERT 가 시나리오의 본질 — DEC-019(마스터 INSERT 보류) 와 다른 정책이 필요.
  - FTP 자격증명·스케줄러는 운영 인프라 합의가 선행이라 1차 합격선("입고 등록·수정·취소·조회 가능") 외 — 사용자 업로드 우회로 핵심 기능 보존.
- **영향**:
  - `migration/contracts/inbound_receipt.yaml` SQL-IN-1~6 (READ list/get/sum, INSERT, PATCH, soft-cancel, IMPORT).
  - `POST /api/v1/inbound/import` multipart 라우트 신규.
  - 기존 `outbound_service` 코드는 읽기만, 수정 금지.
- **결정자**: 메인개발자 + 사용자
- **참조**: `analysis/screen_cards/Sobo{22,38,54,57}*.md`, `migration/contracts/inbound_receipt.yaml`, OQ-IN-1

### DEC-028: dfm→html 산출물을 모던 화면 포팅의 공식 입력으로 동결
- **일자**: 2026-04-19
- **결정 사항**: 모든 신규 화면 포팅(C3 이후)은 작업 시작 전 `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/<Subu*>/<Sobo*>.{html,form.json,tree.json}` 의 변형 포함 모든 세트를 인벤토리하고, `analysis/layout_mappings/<Sobo*>.md` 에 (영역 분할, 위젯 ID, **TabOrder**, DBGrid 컬럼명·정렬·합계, 이벤트 매핑) 1:1 매핑표를 선행 작성한다. 모던 페이지의 모든 위젯에는 `data-legacy-id="<원본 ID>"` 부착 필수. 변형 차이는 **코드 분기 금지**·`customer_variants` 섹션에만 기록.
- **배경/근거**:
  - 사람 재설계만으로 페이지를 만들면 필드 누락·탭순서 어긋남·DBGrid 컬럼 빠짐 같은 회귀가 잠재함(C2 outbound 페이지 점검 시 발견).
  - dfm→html 산출물에 픽셀 좌표·TabOrder·DBGrid 컬럼·OnXxx 이벤트 매핑이 이미 추출돼 있어, "모던 위젯에 `data-legacy-id` 부착"만으로 결정적 회귀 가드가 가능.
- **버리는 정보**: 절대 픽셀 좌표(`Left/Top/Width/Height`), 굴림 폰트, 16비트 색상값, Glyph 비트맵.
- **영향**:
  - `docs/core-scenarios-porting-plan.md` §5 운영 룰 7번 신규.
  - `.cursor/rules/dfm-layout-input.mdc` 신규 (alwaysApply: true) — 모든 AI 작업자에 자동 강제.
  - `tools/analysis/screen_card_builder.py` 가 화면 카드 §0/§9 에 dfm 산출물 경로 + layout_mappings 작성 의무를 자동 안내.
  - 기존 done 시나리오(C1·C2·C6·C9 phase1)는 회귀 발견 시 동일 룰로 retrofit.
- **결정자**: 메인개발자 + 사용자
- **참조**: `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/`, `.cursor/rules/dfm-layout-input.mdc`, `analysis/layout_mappings/`

### DEC-029: C4 반품 재고 변경 작업 패스워드 게이트 + audit_token 동결
- **일자**: 2026-04-19
- **결정 사항**: 반품 재고의 재생(Sobo24)/해체(Sobo25)/변경(Sobo51) 처리는 반드시 Sobo40 패스워드 다이얼로그를 통과한 `audit_token`을 `Authorization-Audit: Bearer-Audit {token}` 헤더로 전달해야 실행 가능. 토큰 없거나 잘못된 경우 `401 RT_AUDIT_REQUIRED` 반환. audit 로그(`audit.returns`)에는 `audit_token_hash`(SHA-256 앞 16자) 필수 기록. 비밀번호 평문은 절대 로그 금지.
- **Phase 1 구현**: `application_settings` 테이블 `scope='audit'&key='password'` 또는 기본값 `'1234'` 와 `hmac.compare_digest` 비교. HMAC-SHA256 토큰 발급, TTL 5분.
- **Phase 2 구현 완료 (OQ-RT-4 / OQ-RT-9, 2026-04-19)**: `app/services/audit_password_service.py` 신설 — bcrypt(cost=12) 검증 + 평문 fallback (Phase1 호환) + 5회 실패/10분 윈도/15분 잠금 정책. 신규 테이블 `audit_password_attempts` (시도/잠금 영속화) + `audit_returns` (액션 영속화). `POST /audit/password-rotate` (manager role) 으로 회전. 마이그레이션 `migrations/2026_04_19_c4_phase2.sql`.
- **영향**:
  - `POST /api/v1/audit/password-verify` 신규 엔드포인트.
  - `returns_service.AuditTokenError` + 라우터 401 변환.
  - `AuditPasswordModal` (Sobo40 포팅) 컴포넌트.
  - `audit_service.log_audit_password` 신규.
- **결정자**: 메인개발자 + 사용자
- **참조**: `analysis/layout_mappings/Sobo40.md`, `migration/contracts/return_receipt.yaml` §audit, `test/test_c4_returns_phase1.py` TC-RT-012/013/016

### DEC-030: OQ-RT 번호 정본 통일 — contract 채택, core-scenarios 권고는 OQ-RT-7/8/9 로 재번호
- **일자**: 2026-04-19
- **결정 사항**: C4 후속 보강(Open Question)의 **번호 정본은 `migration/contracts/return_receipt.yaml` 의 OQ-RT-1~6**. `docs/core-scenarios-porting-plan.md §C4 Phase 2 권고` 의 OQ-RT-1/2/3 (D_Select 권한키 / Sobo34_4·Sobo58 신화면 / DB audit 비밀번호) 는 **OQ-RT-7/8/9 로 재번호** 한다. 중복 번호 사용 금지 — 모든 신규/기존 문서·테스트·dashboard 가 단일 카탈로그를 참조.
- **배경/근거**:
  - C4 Phase 2 계획 수립 중 contract 와 core-scenarios 가 같은 OQ-RT-1/2/3 를 다른 의미로 사용하고 있어 추적 불가 (예: OQ-RT-1 이 chul_08 형식 인지 D_Select 인지 모호).
  - 현장 데이터/SQL 분석을 먼저 거친 contract 가 정본으로 적합 (운영팀 의존 항목 모두 contract 측에 정의됨).
- **확정 카탈로그 (OQ-RT-1~9)**:
  | 번호 | 의미 | 처리 |
  |---|---|---|
  | OQ-RT-1 | chul_08 자료불러오기 외부 데이터 형식 | Phase 2: assume_default(CSV EUC-KR) + multipart 형식 확장 인터페이스 |
  | OQ-RT-2 | Bdate vs Gdate 의미 검증 | Phase 2: 분리 유지 + 운영 데이터 1회 검증 스크립트 |
  | OQ-RT-3 | Sv_Ghng Field1/2/3 동적 컬럼명 9종 | Phase 2: 추정 매핑표 작성 + process_change 9종 확장 |
  | OQ-RT-4 | bcrypt 패스워드 마이그레이션 | Phase 2: cost=12 + audit_password_attempts + 5회 잠금 |
  | OQ-RT-5 | Sv_Ghng 동시 변경 충돌 | Phase 2: SELECT FOR UPDATE + 409 강화 |
  | OQ-RT-6 | Subu25 Time1=Time1 자기참조 | Phase 1 NOW() 명시 완료 — 검증만 |
  | OQ-RT-7 (구 core-1) | D_Select 권한키 분기 | Phase 2: 헬퍼 인터페이스만 노출, 실권한 분기는 C10 |
  | OQ-RT-8 (구 core-2) | Sobo34_4 / Sobo58 신화면 | Phase 2: 구현 |
  | OQ-RT-9 (구 core-3) | DB audit 비밀번호 검증 + 실패 추적 | Phase 2: OQ-RT-4 와 동시 구현 |
- **영향**:
  - `docs/core-scenarios-porting-plan.md` §C4 Phase 2 권고 표 OQ-RT-1/2/3 → OQ-RT-7/8/9 일괄 재번호.
  - `dashboard/data/web-porting-progress.json` 등 모든 OQ-RT 참조 위치 통일.
  - 신규 매핑 노트(`Sobo34_4.md`, `Sobo58.md`) 는 OQ-RT-8 만 참조.
- **결정자**: 메인개발자
- **참조**: `migration/contracts/return_receipt.yaml` (정본), `docs/core-scenarios-porting-plan.md §C4 Phase 2`

### DEC-031: C5 정산 마감 가드 — `T2_Ssub.Yesno='1'` 단일 정본 (legacy_yesno 정책)
- **일자**: 2026-04-19
- **결정 사항**: C5 정산(Sobo45/45_1/41/42/42_1/47) 의 "월 마감(Period Close)" 판정은 **레거시 컬럼 `T2_Ssub.Yesno='1'` 단일 정본**을 사용한다. `application_settings.settlement.close_until` 같은 별도 글로벌 키를 도입하지 않는다 (이중 정본 금지). 마감된 월(YYYYMM) 의 청구 집계/확정/취소·입금 등록·입금 취소는 모두 `423 ST_PERIOD_CLOSED` 로 차단되며, 한국어 메시지는 `i18n/messages/c5.ko.json` 의 `c5.errors.period_closed` ("마감된 자료입니다.") 와 byte-equal.
- **배경/근거**:
  - 레거시 `Sobo45.pas` 가 청구서 라인 클릭 시 `Yesno='1'` 인 경우 입력/수정/삭제를 모두 차단 — 운영팀 멘탈모델이 이미 "확정행=마감"으로 정착.
  - 별도 close_until 키를 두면 (a) 운영팀이 "둘 중 어느 게 진짜 마감?" 혼란, (b) 동기화 누락 시 회계와 DB 가 어긋남 — 단일 정본이 안전.
- **구현**: `app/services/settlement_service.assert_period_open(server_id, gdate, hcode)` 가 `T2_Ssub.Yesno='1'` 1행이라도 있으면 `PeriodClosedError` raise → 라우터에서 423 ST_PERIOD_CLOSED 변환. cash 등록도 service layer 에서 `assert_period_open` 호출.
- **영향**:
  - `migration/contracts/settlement_billing.yaml` 의 모든 쓰기 endpoint 에 `423 ST_PERIOD_CLOSED` 응답 명시.
  - `migrations/2026_05_01_c5_phase1.sql` 의 `application_settings` placeholder 에 `settlement.close_policy='legacy_yesno'` 1행으로 정책 문서화 (실제 게이트는 코드 측).
  - `audit_settlement` 신규 테이블에 차단 시도(`reason='period_closed'`) 로그.
- **결정자**: 메인개발자 + 사용자 (옵션 비교 후 사용자 선택: legacy_yesno)
- **참조**: `analysis/layout_mappings/Sobo45_billing.md`, `analysis/handlers/c5_phase1.md`, `migration/contracts/settlement_billing.yaml` §close_policy

### DEC-032: C5 평문 Gpass 폐기 → AuditPasswordModal + bcrypt 회전 (`/audit/gpass-rotate`)
- **일자**: 2026-04-19
- **결정 사항**: 레거시 `Sobo45.pas L372` 의 `InputBox` 평문 Gpass 변경 흐름은 모던에서 폐기. 대체로:
  1. **변경 트리거**: 사용자는 `AuditPasswordModal` 에서 변경 의사 + 신규 비밀번호 입력. (`scope='gpass_change'` audit_token 필수)
  2. **회전 엔드포인트**: `POST /api/v1/audit/gpass-rotate` (DEC-029 의 `/audit/password-rotate` 와 **분리**) — bcrypt(cost=12) 해시 후 `application_settings.scope='gpass'.key='password_hash'` 1행만 보존, 평문 Gpass 컬럼은 단계적 폐기.
  3. **검증**: 청구 확정/취소 등 고위험 액션은 동일 modal 의 `audit_token` 으로 게이팅 (재사용).
  4. **C4 와 경로 분리**: C4 의 `/audit/password-rotate` (scope='audit') 와 의미·권한이 다르므로 라우트도 `/audit/gpass-rotate` 로 분리 — 라우트 충돌·테스트 회귀 방지.
- **배경/근거**:
  - 레거시 평문 비교 `if InputBox(...) <> Sobo01.Gpass.Value then` 는 (a) 평문 노출, (b) 시도 추적 0건, (c) 변경 audit 0건 — 모두 보안 결함. DEC-029 의 audit_password 정책(bcrypt + 5회/10분/15분 잠금)을 그대로 재사용.
  - C4 의 password-rotate 는 audit 운영자(scope='audit') 의 비밀번호용이므로, Gpass(고객/거래처별) 회전과 권한 모델이 다름 — 같은 URL 사용 시 (a) 잘못된 토큰 스코프로 회전 가능, (b) 라우트 등록 순서에 따라 한쪽이 묻힘.
- **구현**:
  - 백엔드: `app/routers/settlement.py::audit_router` 에 `/gpass-rotate` 추가. `app/services/audit_password_service.rotate_password(scope='gpass_change')` 재사용.
  - 프론트: `src/lib/settlement-api.ts::auditApi.rotateGpass`. 호출 UI 는 Phase 2 에서 추가 (현재는 청구 확정/취소 modal 만 사용).
  - 마이그레이션: `migrations/2026_05_01_c5_phase1.sql` 가 `application_settings.scope='gpass'.key='password_hash'` 슬롯 + `audit_settlement` 영속 로그 테이블 추가.
- **영향**:
  - `migration/contracts/settlement_billing.yaml` §audit 섹션에 `/audit/gpass-rotate` 명시 + 401 ST_AUDIT_REQUIRED / 422 ST_VALIDATION 응답 코드.
  - `analysis/layout_mappings/Sobo45_billing.md` 의 "Gpass 변경" 항목이 modal 흐름으로 갱신.
  - 회귀 테스트: `test/test_c5_settlement_phase1.py::test_p1_27/28` 가 audit 헤더 누락→401, 정상→200+audit log 검증.
- **결정자**: 메인개발자 + 사용자
- **참조**: `analysis/layout_mappings/Sobo45_billing.md`, `app/routers/settlement.py::rotate_audit_password`, `migration/contracts/settlement_billing.yaml`

### DEC-034: C5 정산 Phase 2 인쇄 = HTML 미리보기 + `window.print()` (PDF/실인쇄는 C7 이연)
- **일자**: 2026-04-19
- **결정 사항**: C5 Phase 2 의 청구서(`Sobo46`)·세금계산서(`Sobo49`) 인쇄는 **백엔드가 생성한 HTML 미리보기 + 브라우저 `window.print()`** 만 정식 구현한다. PDF 생성, 실프린터 큐, 일괄(N매) 인쇄는 C7 인쇄 모듈로 이연한다.
  - (a) `GET /api/v1/settlement/billing/{key}/print-data` → JSON 응답 (Edit201..Edit315 = 67 합계 + 31 일별 라인). 프런트 미리보기 카드는 `Sobo46.*` `data-legacy-id` 부착(DEC-028).
  - (b) `GET /api/v1/settlement/billing/{key}/print` / `…/tax-invoice/{key}/print` → 백엔드가 표준 string template 으로 1매 HTML 반환 (Jinja2 등 외부 의존 회피, 정합성 우선).
  - (c) 모던 페이지에서는 `window.print()` 또는 iframe `print()` 만 호출. PDF 라이브러리(react-pdf 등) 임포트 금지.
- **배경/근거**: 레거시 `Tong40.print_46_*` / `PrinTing00` 은 Delphi Canvas 직접 그리기. 양식 사이즈/폰트 보존은 인쇄 전용 모듈로 분리하지 않으면 화면 코드를 오염시킨다 — Phase 2 는 데이터·레이아웃 검증이 우선.
- **영향**:
  - `migration/contracts/settlement_billing.yaml` v1.1.0: `print-data` JSON + `print` HTML 두 엔드포인트로 분리.
  - `analysis/layout_mappings/Sobo46_billing.md` §1 / `Sobo49_tax.md` §1: 인쇄 정책 명시.
  - 회귀: `test_p2_03_render_preview_html_*`, `test_p2_15_render_tax_invoice_html_*` 가 HTML 응답에 핵심 ID·banner 포함 검증.
- **결정자**: 사용자 (Phase 2 계획 단계, OQ-ST-2 종결)
- **참조**: `app/services/settlement_print_service.py::render_preview_html`, `app/services/tax_invoice_service.py::render_tax_invoice_html`, `analysis/layout_mappings/Sobo46_billing.md`, `Sobo49_tax.md`

### DEC-035: C5 정산 Phase 2 세금계산서 외부 발행 = NOT_INTEGRATED stub (DEC-034 와 함께 OQ-ST-1 종결)
- **일자**: 2026-04-19
- **결정 사항**: `POST /api/v1/settlement/tax-invoice/{key}/issue` 는 외부 채널(홈택스/이메일/EDI 등) 을 호출하지 **않는다**. 항상 `200 + external.code='NOT_INTEGRATED'` 를 반환하며 내부적으로 `T2_Ssub.Chek3='1'` 만 갱신하고 audit 액션 `tax_issued_stub` 을 영속화한다.
  - 모던 UI 는 응답 banner 로 사용자에게 "외부 채널 미연결" 을 가시화한다 (DEC-028 `data-legacy-id="Sobo49.Banner.NotIntegrated"`).
  - 외부 채널 정식 연동은 후속 마이그레이션 (별도 시나리오) 으로 분리한다.
- **배경/근거**: 레거시 `Sobo49` 는 외부 발행을 별도 모듈에 위임 — 본 시스템은 출판물 물류이며 세무 채널은 비핵심. 채널별 인증·승인·롤백 정책은 본 DEC 범위 밖. Stub 응답으로 흐름은 정합 유지.
- **DoD**: `/issue` 호출이 `409 ALREADY_ISSUED` (이미 Chek3='1') · `423 ST_PERIOD_CLOSED` (마감) 두 상태만 정상 차단; 그 외에는 200 + NOT_INTEGRATED 로 통과한다.
- **영향**: `tax_invoice_service.issue_external_stub` 단일 함수로 흡수, audit 액션 `tax_issued_stub` 등록.
- **결정자**: 사용자 (Phase 2 계획 단계, OQ-ST-1 종결)
- **참조**: `app/services/tax_invoice_service.py::issue_external_stub`, `app/routers/settlement.py::issue_tax_invoice`, `analysis/layout_mappings/Sobo49_tax.md` §6

### DEC-036: C5 정산 Phase 2 Chek3 토글 단일 진실원 (`_update_chek3` 헬퍼) — 단건/일괄 흐름 흡수
- **일자**: 2026-04-19
- **결정 사항**: 레거시 `Subu49.pas` L699/723/752 의 3 곳 중복 SQL (단건 `DBGrid101Columns7UpdateData` + 일괄 ON `RadioButton4Click` + 일괄 OFF `RadioButton5Click`) 은 모던에서 **백엔드 `tax_invoice_service._update_chek3` 단일 헬퍼 + 단일 엔드포인트 `POST /tax-invoice/chek3`** 로 흡수한다 (`hcode` 가 본문에서 누락되면 자동으로 일괄 모드).
  - 단건/일괄 모두 `assert_period_open` (DEC-031) 으로 마감 가드 통과 후 실행한다.
  - audit 액션은 단건 = `tax_chek3_toggled`, 일괄 = `tax_chek3_bulk` 로 분리해 영속화하지만 **헬퍼는 1개**.
  - 모던 UI 는 단건 체크박스 클릭 / 일괄 라디오 버튼 두 흐름 모두 동일 헬퍼를 호출하며, 토글 새 값(`'1'|'0'`) 은 클릭 시점의 부정값을 명시적으로 전달한다 (레거시 inverse-toggle 의미 보존).
- **배경/근거**: 동일 SQL 패턴 3 회 중복은 회귀 위험. 단일 헬퍼로 마감 가드/audit/SQL 호환(`sql_mysql3`) 정책을 한 곳에 집약.
- **DoD**: `tax_invoice_service.py` 의 `_update_chek3` 외에 어떤 함수도 `UPDATE T2_Ssub SET Chek3=…` 를 직접 발행하지 않는다 (코드 grep 0 건).
- **영향**: `analysis/layout_mappings/Sobo49_tax.md` §1·§4 의 1:1 SQL 매핑.
- **결정자**: 메인개발자 (DEC-028 단일 진실원 정책 연장)
- **참조**: `app/services/tax_invoice_service.py::_update_chek3`, `analysis/layout_mappings/Sobo49_tax.md`

### DEC-037: C7 Phase 1 PDF 엔진 = WeasyPrint (Python 백엔드 단일)
- **일자**: 2026-04-20
- **결정 사항**: 5종 인쇄 양식 (P1-A 청구서, P1-B 세금계산서, P1-C 출고 거래명세서, P1-D 반품 영수증, P1-E 거래명세서) + 1종 라벨 (P1-F 우편엽서) 의 PDF 산출은 **WeasyPrint(Python) 단일 엔진** 으로 통일한다.
  - HTML/CSS 입력은 백엔드 Python 빌더 (`render_*_html`) 가 생성하고 `app.services.print_service.render_pdf` 가 PDF 바이트로 변환한다.
  - WeasyPrint 또는 시스템 의존 (`libpango`/`libcairo` 등) 부재 시 `503 PR_ENGINE_UNAVAILABLE` 로 graceful fallback (운영자 안내 토스트는 i18n `c7.engine.unavailable`).
  - 신규 SQL 0건 정책: `print_service.py` 는 SELECT/INSERT/UPDATE/DELETE 0건; 라벨만 SQL-PR-6 (`Sg_Csum` 단건) 1건 신규.
  - 폰트: `NanumGothic` (SIL OFL) 을 `backend/static/fonts/` 에 번들; 미배치 시 시스템 폰트로 폴백.
  - 마감(`T2_Ssub.Yesno='1'`) 자료는 본문 위 "마감" 워터마크 (P1-A/P1-B 한정).
- **배경/근거**: (1) 헤드리스 Chromium/Puppeteer 는 운영 패키지 (1GB+) 와 보안 패치 부담; (2) FastReport (`.frf`) 정본은 바이너리 사유 포맷이라 자동 변환 불가 (DEC-039); (3) HTML/CSS `@page` 는 A4/우편엽서 모두 mm 단위 일관 처리 가능; (4) 단일 엔진/단일 운영 의존이 멀티 운영 노드에서 회귀 비용 최소.
- **DoD**: `test_c7_print_phase1.py` 22 케이스 통과 (PDF byte signature + 마감 워터마크 + 503 fallback + DEC-028 grep + 신규 SQL 0건 정적 검사 포함). `debug/probe_backend_all_servers.py` 의 5 그룹 (`print.*` 4 + `settlement.invoice_pdf` 1) 이 4 서버 전체에 라우팅 등록 확인.
- **영향**: `analysis/print_specs/c7_phase1.md`, `analysis/handlers/c7_phase1.md`, `migration/contracts/print_invoice.yaml`, `migration/contracts/print_label.yaml`, `migration/contracts/settlement_billing.yaml v1.2.0`, 6 모던 미리보기 페이지.
- **결정자**: 사용자 (C7 Phase 1 계획 단계, OQ-002 부분 해소: "라벨 = 서버 PDF" 분기 동결)
- **참조**: `app/services/print_service.py`, `app/services/label_service.py`, `app/routers/print.py`, `analysis/print_specs/c7_phase1.md` §0

### DEC-038: C7 Phase 1 라벨 양식 = 우편엽서 1종 (Seep13 → `Report_1_21.frf` 등가)
- **일자**: 2026-04-20
- **결정 사항**: Seep13 의 `frReport00_01.LoadFromFile(Edits[ItemIndex].Text)` 다중 양식 (5종) 중 **우편엽서 1종 (form=1, `Report_1_21.frf` 등가) 만 1차 채택** 한다.
  - 모던 엔드포인트 `/api/v1/print/label/{shipment_key}.pdf?form=1` 의 `form` 파라미터는 **호환성용** 으로 유지하되 Phase 1 = 1 고정 (라우터에서 `Query(1, ge=1, le=1)`).
  - 디자인 패널 (Edit21~25, SpinEdit71~77 등 78개 위젯) 은 **out-of-scope** — `.frf` 정본을 수동으로 HTML/CSS 재현 (DEC-039 정책의 직접적 산물).
- **배경/근거**: (1) 사용자 운영 통계 — 라벨은 우편엽서가 절대 다수; (2) 5종 자동 변환은 `.frf` 파서 부재 (DEC-039 / T10 R&D 분리); (3) Phase 1 합격선은 "출고/반품/거래처별로 라벨 1매 PDF 다운로드".
- **DoD**: `test_TC_PR_P1_06_label_pdf_signature` + `test_TC_PR_P1_25_label_service_uses_seep13_legacy_ids` 통과 (Seep13.Label.Gname/Gposa/Gjice/Gadds/Gpost 5개 ID).
- **후속 작업**: Phase 2 에서 form 2~5 추가 시 본 DEC 보강 + `print_label.yaml customer_variants` 분리.
- **결정자**: 사용자 (Phase 1 단순화 결정)
- **참조**: `app/services/label_service.py`, `analysis/layout_mappings/Seep13_label.md`, `migration/contracts/print_label.yaml`

### DEC-039: `.frf` (FastReport VCL 4.x) 자산 = 참조용 정본, 자동 변환 0
- **일자**: 2026-04-20
- **결정 사항**: 레거시 98 건의 `.frf` 자산은 **참조용 정본** 으로만 인벤토리하고, **런타임 적재 0 / 자동 HTML 변환 0** 정책을 적용한다.
  - C7 Phase 1 의 5 양식 + 1 라벨 HTML/CSS 는 `.frf` 정본을 **수동으로 재현** 한 결과 (디자인 변경은 별도 Designer 절차 필요).
  - PDF 푸터 또는 운영자 안내에 "본 양식은 참조용 .frf 정본을 수동 재현한 결과" 메시지 부착 (i18n `c7.frf.reference_only`).
  - `analysis/print_specs/frf_catalog.md` (T9) 에 98 건 인벤토리 + 5 양식 ↔ `.frf` 매핑표 보존.
- **배경/근거**: `.frf` 는 FastReport VCL 4.x 의 비공개 바이너리 포맷. 외부 OSS 파서 부재 (T10 별도 R&D 로 검토). 무리한 자동 변환 시도는 Phase 1 일정 위협 + 회귀 폭발.
- **DoD**: T9 카탈로그 100% 인벤토리 (98건 모두 `analysis/print_specs/frf_catalog.md` 등재) + 5 양식별 정본 `.frf` 파일명 명시.
- **후속 작업**: T10 — FastReport OSS 분석 보고서로 자동 변환 가능성 재검토 (비차단 R&D).
- **2026-04-20 R&D 보강 (1)**: T10 보고서에 **`https://github.com/FastReports/FastReport.Documentation` (MIT)** 조사 결과 반영. 핵심: (a) FastReport .NET OSS 본은 `.frx` (XML) 만 지원 — 우리 `.frf` (VCL 4.x 바이너리) 와 직렬화 0% 호환, **그러나 객체 모델/밴드 분류/`[Table.Column]` 데이터 토큰은 95% 시맨틱 호환**. (b) 자체 파서 도입 결정 시 권장 안: 기존 R3 (직접 CSS 변환) → **R3a `.frx` IR 변환 + .NET OSS 적재 검증 + R3b CSS 변환** 2 단계 분리 (총 7~13 인주). IR 검증으로 객체 그래프 충실도가 FastReport.Documentation 명세에 의해 보장. (c) 본 보강은 DEC-039 정책을 변경하지 **않음** (Phase 1 = 자동 변환 0 유지). Phase 2 이후 자체 파서 도입 결정 시 본 R&D 결과를 진입 근거로 사용.
- **2026-04-20 R&D 보강 (2)**: T10 보고서에 **`https://github.com/yusufbal/FastReport.OpenSource.HtmlExporter` (MIT, .NET 8)** 커뮤니티 사례 추가. 핵심: (a) FastReport OSS 진영 자체가 PdfSimple 플러그인 (LGPL, 이미지 PDF, 텍스트 선택 불가) 의 한계를 우회하기 위해 **"HTML 내보내기 → 외부 PDF 엔진 (iText7)" 패턴을 표준 솔루션으로 채택** — 우리 DEC-037 (HTML 빌더 → WeasyPrint) 와 동일한 발상이 .NET OSS 커뮤니티에서도 베스트 프랙티스로 검증됨 → **DEC-037 아키텍처 정당성 강화**. (b) 우리 WeasyPrint (BSD-3 단일) 가 본 사례의 iText7 (Apache 2.0/AGPL 듀얼) 보다 운영 라이선스 부담 면에서 우월. (c) 자체 파서 도입 시 (B3 안) 본 라이브러리의 PDF 출력을 R6 회귀 게이트의 *Ground Truth* 로 사용 가능 (NuGet 1 줄 + 5~10 줄 코드). (d) 본 보강 또한 DEC-039 정책을 변경하지 **않음**.
- **2026-04-20 R&D 보강 (3)**: T10 보고서에 **`https://github.com/atkins126/FastReportExport` (Apache-2.0, antoniojmsjr 본 fork)** 추가 조사. 핵심: (a) 본 라이브러리는 **유료 FastReport VCL 상용 SDK** 의 멀티스레드/서버 환경 안전 호출 래퍼 (Horse/ISAPI/WindowsService 통합 샘플) — 래퍼만 OSS, 핵심 의존성 (`frxClass`/`frxExportPDF` 등) 은 상용. **§4 C 안 (상용 FastReport VCL SDK) 운영 통합 레퍼런스** 가치만 있으며, DEC-037 (Python/WeasyPrint) 와는 라이선스/스택 면에서 정면 비교 시 우리 결정이 우월함을 추가 확인. (b) 샘플 형식이 `.fr3` (FastReport 3+ XML) 인 점에 착안해 **우리 `.frf` 의 실제 시그니처 검증을 5분 실행 → 바이너리 (Pascal TStream + DFM 직렬화) 확증** (`Report_2_11.frf` hexdump: `EPSON Stylus COLOR 1520H` 프린터 헤더 + `Page1`/`Band1` 객체명 발견). 즉 §1.3 의 FreeReport 2.3 LoadFromStream 가설이 100% 유효 → R1 비용 추정 (2~4 인주) 그대로 유지. (c) 본 보강도 DEC-039 정책 변경 없음.
- **⭐ 2026-04-20 R&D 보강 (4) — 게임 체인저**: T10 보고서에 **FastReports/FastReport master tarball (MIT) 의 로컬 소스 직접 분석** 결과 반영. 핵심: (a) **FastReport OSS HTML export 가 코어 내장** (`FastReport.Base/Export/Html/HTMLExport.cs` 1187 LOC + `HTMLExportLayers.cs` 992 LOC + 보조 4 파일, 총 3137 LOC, MIT). Layer 모드는 **`<div style="position:absolute;...">`** 픽셀 절대 좌표 HTML 을 생성 — 우리가 `.frf` 충실 재현에 필요한 출력 형식 그대로. 자체 R3b (CSS 변환) 1.5~3 인주가 **0 인주** 로 대체 가능. (b) **PdfSimple 플러그인 라이선스도 MIT** (단일 LICENSE.md 일관) — 이전 보강 (1)/(2) 의 "LGPL" 표기는 사실관계 오류로 본 보강에서 **교정**. (c) **Import 플러그인 4종** (RDL 988 LOC, StimulSoft 1582 LOC, JasperReports 1165 LOC, ListAndLabel) 의 `ImportBase` 패턴이 자체 `.frf` 임포터의 직접 템플릿. (d) 신규 권장 전략 **B4 (빌드 타임 변환 + Jinja2 템플릿)** 추가 — `.frf → .frx → FastReport OSS HTMLExport.Layers=true → Jinja2 placeholder 후처리 → repo commit` 을 빌드 타임 1회 실행. 운영은 기존 Python/FastAPI/WeasyPrint 그대로 (DEC-037 무변경). 자체 파서 비용 6~13 인주 → **4.5~8.5 인주** (B1 대비 30%, B2 대비 40% 단축). 운영 .NET 런타임 의존성 0. (e) Phase 2 자체 파서 도입 결정 시 **B4 가 1 순위 권장** (B1/B2/B3 대체). 진입 직전 BarcodeObject SVG → WeasyPrint 호환 1 일 PoC 권장. (f) 본 보강도 DEC-039 정책 변경 없음 (Phase 1 = 자동 변환 0). 단, Phase 2 의 R&D 진입 비용/리스크가 본 보강으로 대폭 낮아져 **트리거 조건 만족 시 즉시 도입 결정 가능**.
- **결정자**: 사용자 (C7 Phase 1 계획 단계, "별도 R&D 로 분리" 결정)
- **참조**: `analysis/print_specs/frf_catalog.md` (T9), `analysis/research/c7_frf_parser_oss_research.md` (T10 — 2026-04-20 갱신: FastReport.Documentation MIT OSS 추가 조사 반영)

### DEC-040: C8 바코드 스캔 매칭 = 서버 매칭 + 클라이언트 라인 반영 분리, 신규 SQL 0
- **일자**: 2026-04-20
- **결정 사항**: C8 Phase 1 의 바코드 스캔 (Sobo21/22/23 통합 ─ 레거시 `Tong07.Button100Click` 등가) 은 다음 분리 정책으로 동결한다.
  - (a) **서버 책임**: `POST /api/v1/scan/match` 1 엔드포인트. G4_Book ISBN 매칭 + G1/G2_Ggeo 단가 폴백 (Hcode='' **1순위** → 라인 Hcode 2순위, 레거시 `Tong07.pas` L126-149 와 동일 순서). 응답은 `resolved` 라인 객체 (gcode, gname, gjeja, ocode, gdang, grats, grats_source).
  - (b) **클라이언트 책임**: 라인 추가 / 중복 검출 / 수량 누적은 모두 호출 페이지가 담당. 저장은 **기존 `PUT /orders/{key}` (C2) / `PUT /inbound/receipts/{key}` (C3) / `PUT /returns/receipts/{key}` (C4) desired-state diff** 흐름 그대로 (회귀 0 보장).
  - (c) **신규 SQL 0건**: G4_Book / G1_Ggeo / G2_Ggwo SELECT 재해석. INSERT/UPDATE/DELETE 0 (서버 측 라인 INSERT 금지 — DRY/SRP).
  - (d) **단일 진입 컴포넌트**: 모든 통합 페이지는 `components/shared/scan-input.tsx` 1 컴포넌트만 임포트. 코드 분기 금지 (입력 박스에 `data-legacy-id="FTong07.Edit101"` 부착 — DEC-028 룰 7).
  - (e) **USB-HID 키보드 웨지 1차** (DEC-004 채택): Web Serial 직결은 OQ-002-R 잔류. 사람 입력 vs 웨지 구분은 `lib/scanner.ts` 가 키 간격 임계 (기본 30ms) + Enter(CR) 종결 + 50ms 무입력 디바운스로 처리.
- **배경/근거**:
  - 레거시 `Tong07.Button100Click` 은 단일 SQL 체인 (G4_Book → G1/G2_Ggeo) 으로 라인 객체를 만들고 즉시 `nSqry.Append` 로 라인 그리드에 추가 (서버 INSERT 0). 모던 분리도 동일 정책 유지 시 회귀 면적 최소.
  - 매칭 SQL 은 출고/입고/반품 3 시나리오가 모두 사용 → `pricing_service.resolve_grats(context, gcode, hcode, server_id)` 단일 헬퍼로 추출 (DRY + LSP). `outbound_service` / `inbound_service` / `returns_service` 의 향후 단가 조회도 본 헬퍼로 흡수 가능.
  - `Hcode='' 1순위 → 라인 Hcode 2순위` 폴백은 레거시 정합 (Tong07.pas L138-141). 변경 시 단가 변동 회귀 → 문서·테스트로 동결.
- **DoD**:
  - C8 Phase 1 5축 회귀 (`analysis/regression/c8_phase1.md`) 모두 통과 — `axis_test` 22 케이스 (단가 폴백 우선순위 + nodata + 4 server matrix 포함), `axis_data` `scan.match` 그룹이 4 server probe 매트릭스에 등록.
  - `scan_match_service.py` / `pricing_service.py` 신규 INSERT/UPDATE/DELETE 0건 (정적 검사 자동화).
  - 3 페이지 (`outbound/orders/[orderKey]`, `inbound/receipts/[receiptKey]`, `returns/receipts/[returnKey]`) 모두 `ScanInput` 임포트 + 적절한 hcode/context 주입.
- **결정자**: 메인개발자 + 사용자 (C7 마감 + C8 바코드 스캔 포팅 계획 승인)
- **참조**: `migration/contracts/barcode_scan.yaml` v1.0.0, `analysis/handlers/c8_scan.md`, `analysis/layout_mappings/c8_scan_match.md`, `analysis/screen_cards/Tong08.md`, `analysis/regression/c8_phase1.md`, `i18n/messages/c8.ko.json`, `test/test_c8_scan_phase1.py`, DEC-004 / DEC-010 / DEC-028, OQ-002-R

### DEC-041: 세션·권한 응답 코드 표준 + 글로벌 401/403 인터셉터 (C13 동결)
- **일자**: 2026-04-20
- **결정 사항**: 모든 백엔드 라우터는 **세션·권한 거부 응답을 4 표준 코드** (`AUTH_NO_TOKEN` / `AUTH_TOKEN_EXPIRED` 401, `PERMISSION_DENIED` 403, `PRECONDITION_REQUIRED` 428, `STALE_VERSION` 409) 로 한정한다. 프론트엔드는 단일 글로벌 인터셉터 (`lib/api-client.ts`) 가 다음 정책으로 일관 처리:
  - (a) `AUTH_TOKEN_EXPIRED` → refresh 토큰 1회 시도 (`__noRefresh` 플래그로 무한루프 차단). 성공 시 원 요청 1회 재시도, 실패 시 `/login?reason=expired` 이동.
  - (b) `AUTH_NO_TOKEN` → 즉시 `/login?reason=expired` 이동 (refresh 시도 없음).
  - (c) `PERMISSION_DENIED` → 토스트 + (페이지 진입 시) `<PermissionGuard>` 가 fallback UI 노출. 페이지 강제 이동 없음 (사용자 컨텍스트 보존).
  - (d) `STALE_VERSION` → `<ConcurrencyConflictModal>` (DEC-042) 가 새로고침 옵션 제공.
- **배경/근거**: C10 이전에는 라우터별 401/403 메시지가 흩어져 있어 (예: `detail: "Not authenticated"` / `detail: "Forbidden"` / `detail.code: "USER_DELETED"` 등) FE 가 각각 분기해야 했음 → SRP 위반. 표준 4 코드로 정합 시 글로벌 인터셉터 1개로 흡수 가능.
- **DoD**:
  - `app/core/deps.py::require_permission` 이 401 (no_token/expired) + 403 (PERMISSION_DENIED) 만 반환 (`test_R_01_no_token_401` / `test_R_02_expired_401` / `test_R_03_operator_denied_403`).
  - `lib/api-client.ts` 가 `AUTH_TOKEN_EXPIRED` → `attemptRefresh` → `/login?reason=expired` 단일 분기 (axis_type/axis_lint 0 error).
  - `debug/probe_backend_all_servers.py` 의 `auth.expired_must_401` 그룹이 4 server × 1 = 4 행 등록 (T7).
- **결정자**: 메인개발자 + 사용자 (C10 풀 스코프 승인)
- **참조**: `app/core/deps.py`, `도서물류관리프로그램/frontend/src/lib/api-client.ts`, `analysis/regression/c10_phase1.md` §4, DEC-019 (Wave D 단일 원천)

### DEC-042: 낙관적 동시편집 — If-Match/ETag (C15 동결)
- **일자**: 2026-04-20
- **결정 사항**: PUT/DELETE/PATCH 응답 변경에 대한 동시편집 충돌 방지는 **HTTP If-Match / ETag** 표준으로 통일한다 (서버 락/세션 락 도입 금지 — 분산 환경 SRP).
  - (a) GET 응답에 `ETag: "<sha256(payload)>"` 또는 `ETag: "rev:<n>"` 헤더 부착 (`compute_etag` + `set_etag`).
  - (b) PUT/DELETE 요청은 `If-Match: <etag>` 헤더 필수 — `app/core/concurrency.py::require_if_match()` Depends 가 부재 시 `428 PRECONDITION_REQUIRED`.
  - (c) 서버는 현재 리소스 ETag 와 비교 → 불일치 시 `409 STALE_VERSION` (`check_etag(provided, expected)`).
  - (d) 프론트엔드는 `<ConcurrencyConflictModal data-legacy-id="Chul.Stale">` 1 컴포넌트로 일관 처리 — 새로고침 vs 무시 선택지.
- **배경/근거**: Wave D admin/마스터/주문/정산 라우터에서 동시편집 흔적은 다발 (예: 두 관리자가 같은 사용자 권한 매트릭스 동시 편집). 레거시 Delphi 는 단일 PC 가정으로 락 없음 → 모던 멀티 사용자 환경에서 데이터 손실 위험. ETag/If-Match 는 RFC 9110 표준 + Stateless (라우터 레이어만 도입, DB 스키마 변경 0).
- **DoD**:
  - `app/routers/admin.py` 의 `PUT /id-logn/{hcode}` + `PUT /id-logn/{hcode}/permissions` 가 `Depends(require_if_match)` + `check_etag(...)` 정합 (`test_R_06_if_match_missing_428` / `test_R_07_if_match_stale_409`).
  - `debug/probe_backend_all_servers.py` 의 `admin.permission_matrix_stale_must_409` + `concurrency.precondition_required_must_428` 그룹 4 server × 2 = 8 행 등록 (T7).
  - 후속 사이클에서 마스터/주문/정산 라우터에 점진 도입 — 본 결정 노트의 (a)~(d) 정책을 단일 원천으로 참조.
- **결정자**: 메인개발자 + 사용자 (C10 풀 스코프 승인)
- **참조**: `app/core/concurrency.py`, `도서물류관리프로그램/frontend/src/components/shared/concurrency-conflict-modal.tsx`, `analysis/regression/c10_phase1.md` §4, RFC 9110 §13.1.1

### DEC-043: IdP/SSO 인터페이스 분리 (C10 = 인터페이스만, 외부 연동은 후속)
- **일자**: 2026-04-20
- **결정 사항**: 외부 인증 (SAML/OIDC/LDAP 등) 도입을 위한 **추상 인터페이스만 C10 Phase 1 에 포함**, 실제 외부 IdP 연동은 후속 사이클로 분리한다 (사용자 명시 — 본 사이클 외부 시스템 연동 제외).
  - (a) `app/core/auth_provider.py::AuthProvider` 추상 — `authenticate(hcode, password) -> tuple[user, claims]` + `reset_password(hcode, new_password)` 2 메서드.
  - (b) `LegacyIdLognProvider` 1 구현체 = 기존 `auth_service.authenticate_user` 위임 + Subu45 비번 리셋 (DEC-029 audit token gate 흡수).
  - (c) `SamlProvider` / `OidcProvider` = `NotImplementedError` stub. 후속 사이클 도입 시 본 stub 만 구현체로 교체 (OCP).
  - (d) `select_provider(name="legacy_id_logn")` 디폴트 — 운영 설정에서 `AUTH_PROVIDER=saml` 등 ENV 로 전환 가능하도록 인터페이스 동결.
- **배경/근거**: 사용자 의사 — "외부 시스템 연동 제외, 인터페이스 정의만". 인터페이스만 동결해두면 후속 사이클에서 (a) 운영 IdP 사양 합의 (b) `SamlProvider` 구현 (c) ENV 전환 만으로 흡수 가능. C10 Phase 1 의 회귀 면적 0.
- **DoD**:
  - `app/core/auth_provider.py` 컴파일 + `select_provider("legacy_id_logn")` 동작 + `select_provider("saml")` 호출 시 `NotImplementedError` (`test_S_01_admin_permissions_yaml` 의 `DEC-043` grep).
  - `migration/contracts/admin_permissions.yaml` v1.0.0 의 `decisions:` 섹션에 DEC-043 명시.
- **후속 작업 (별도 사이클)**: (1) 운영 IdP 사양 합의 (Azure AD / Keycloak 등) (2) `SamlProvider` 구현체 도입 (3) 그룹/역할 매핑 정책 (예: AD `Group: 출고관리자` → `permissions: ['*']`) (4) 본 OQ closure (현재 미등록 — 외부 합의 트리거 시 OQ-IDP-* 신규).
- **결정자**: 메인개발자 + 사용자 (C10 풀 스코프 승인 + 외부 시스템 연동 제외 명시)
- **참조**: `app/core/auth_provider.py`, `migration/contracts/admin_permissions.yaml` v1.0.0, DEC-029 (audit_password_service 연계)

### DEC-044: 확장 라인 v0.2 정책 — 신규 SQL 0건 + 권한 카탈로그 단일 등록 + 외부 시스템 연동 제외
- **일자**: 2026-04-20
- **결정 사항**: C10 이후 확장 라인(C11/C13/C14/C15)은 다음 단일 정책으로 동결한다.
  - (a) **신규 SQL 0건 정책 확장**: C13 통계 4 endpoint, C14 audit 통합 뷰, C15 cutover validator 모두 기존 service SELECT 재사용 우선. 신규 SQL 도입 시 본 DEC 보강 + contract 변경 + axis_data 갱신 동시 요구.
  - (b) **확장 권한키 단일 등록**: C13/C14 신규 permission_code (`admin.stats.*` x4, `admin.{audit,metrics,health}.read` x3) 는 `legacy-analysis/permission-keys-catalog.md` §4 가 단일 정본. C10 의 `test_G_05_unknown_permission_code_fails_fast` 가드를 그대로 활용해 fail-fast.
  - (c) **외부 시스템 연동 제외 (사용자 명시)**: BI 도구(Tableau/PowerBI/외부 ETL/DW), APM SaaS(Datadog/NewRelic/Sentry), 알림 채널(Slack/Teams/PagerDuty), 로그 집계(ELK/Splunk), 마이그레이션 SaaS(AWS DMS/Azure Migrate) 모두 본 사이클 out-of-scope. DEC-043(IdP/SSO 인터페이스 분리) 패턴 재사용 — 인터페이스만 유지하고 실 연동은 후속 사이클.
  - (d) **재귀 회귀 차단**: 모든 확장 시나리오 T7 단계에서 기존 C2~C10 전체 회귀(axis_test_full 333+) 동시 PASS 강제.
  - (e) **공수 추정/게이트**: 본 DEC 와 함께 게이트 #6(운영 SLA, C14 종료) + #7(Cut-over, C15 종료) 신규 정의 — 차단 조건은 계획서 v0.2 §6.
- **배경/근거**: 사용자 명시 — "확장 후보 시나리오 구현은 외부 시스템 연동을 제외하고 진행" + "재귀 오류가 발생하지 않도록 기존 코드/유사 케이스 확인 후 일반화 해결". DEC-040 (신규 SQL 0) + DEC-041 (응답 코드 표준) + DEC-042 (If-Match) + DEC-043 (인터페이스 분리) 의 정책 패턴이 그대로 확장 라인에 적용 가능.
- **DoD**:
  - `analysis/handlers/extension_dependencies.md` 의 의존성 그래프 + 선행 자산표가 4 시나리오 모두 충족.
  - `legacy-analysis/permission-keys-catalog.md` §4 등록 + axis_doc grep `DEC-044` PASS.
  - `legacy-analysis/stats_inventory.md` 작성 (C13 진입 게이트).
  - 각 확장 시나리오 contract 의 `constraints:` 절에 외부 연동 제외 명시.
  - 각 시나리오 회귀 매트릭스 (`analysis/regression/cN_phase1.md`) 의 axis_data 가 신규 SQL 0건 grep 가드 포함.
- **결정자**: 메인개발자 + 사용자 (C10 풀 + 확장 후보 시나리오 v0.2 승인)
- **참조**: `analysis/handlers/extension_dependencies.md`, `legacy-analysis/stats_inventory.md`, `legacy-analysis/permission-keys-catalog.md` §4, DEC-040/041/042/043

### DEC-045: Phase1 승격 게이트 = 레거시 동등성 + 자동 회귀 통과 (사이드바 녹색 체크 정의)
- **일자**: 2026-04-21
- **결정 사항**: `frontend/src/lib/form-registry.ts` 의 `phase: "phase1"` (사이드바 녹색 체크) 부여 기준을 다음과 같이 강화·동결한다.
  - (a) **5축 PASS 의무**: `migration/contracts/<flow>.yaml::equivalence` 의 5축(`functional` / `data` / `ui` / `audit` / `performance`) 이 모두 PASS. 단, read-only 화면은 `audit = N/A` 허용.
  - (b) **자동 회귀 통과 의무**: `test/test_regression_phase1.py` 의 해당 그룹이 PASS (단일 server: functional+performance 축 / `--multi-db`: 4대 DB cross-DB invariant data 축 추가).
  - (c) **T-Phase 8단 전부 충족**: `docs/phase1-promotion-gate.md` §3 의 T1(screen_card) → T8(promotion PR) 산출물 모두 PR description 첨부.
  - (d) **승격 PR 단위 분리**: 12개 화면을 묶어서 한 PR 로 승격 금지. 화면 1개 = PR 1개. PR body 에 5축 PASS 표 + 회귀 결과 JSON 링크 첨부.
  - (e) **강등 정책**: 회귀 1회라도 FAIL / 4대 DB probe 1회라도 불일치 / 운영 5xx ≥ 1% (24h) 시 즉시 `phase: "phase2"` 강등 PR 생성. 강등 사유 PR body 기록.
  - (f) **단순 200 응답 = 부족**: "API 가 200 을 반환한다" 만으로 phase1 승격 금지. 본 결정 이전에 임의로 phase1 부여된 화면도 회귀 PASS 증빙 부재 시 phase2 강등 후보.
- **배경/근거**: 사용자 명시 — "테스트 및 동작이 레거시코드 비즈니스로직 및 쿼리 등이 적절하게 동일성을 갖게 적용이 완료되고 테스트가 완료된 이후에 녹색 표시하도록 하는 내용을 계획에 업데이트". 기존 레지스트리는 "UI 가 라우팅된다 = phase1" 수준에서 부여되어 사용자 합격선("기존 사용자가 같은 결과를 얻는다") 과 괴리 발생.
- **DoD**:
  - `docs/phase1-promotion-gate.md` 동결 (T1~T8 + 5축 + 강등 정책).
  - `migration/coverage/phase1-12pages-coverage.md` (12 화면 매트릭스 + 회귀 그룹 정의 + Patch 항목).
  - `test/test_regression_phase1.py` (10 그룹 회귀 러너 + pytest 통합 + CLI `--multi-db`).
  - `migration/test-cases/stats_reports.json` (TC-STATS-MONTHLY-001~005 + alias).
  - `debug/probe_backend_all_servers.py` 에 `inventory.ledger` / `stats.sales_period` / `stats.customer_analysis` / `reports.book_sales` 4 그룹 추가.
  - `frontend/src/lib/form-registry.ts::FormMeta.phase` JSDoc 에 본 게이트 정책 문서화.
- **결정자**: 메인개발자 + 사용자 (Phase 1 12-page 합격선 강화 합의)
- **참조**: `docs/phase1-promotion-gate.md`, `migration/coverage/phase1-12pages-coverage.md`, `test/test_regression_phase1.py`, `migration/test-cases/stats_reports.json`, DEC-040(신규 SQL 0), DEC-041(응답 코드 표준), DEC-033(멀티 DB)

### DEC-007 보강 (2026-04-21): hcode='0000' = 자동 admin 권한 부여 (1차 운영 합격선)
- **일자**: 2026-04-21 (DEC-007 1차 결정 후속 보강)
- **결정 사항**: DEC-007 의 "0000 슈퍼유저 분기 1차 제외" 정책을 다음으로 **부분 회복** 한다 — 단, 레거시 가시성 필터(`Chek5='show1'`) 는 여전히 도입하지 않고, **권한 부여만** 자동화한다.
  - (a) **JWT claim 자동 admin**: `auth_service.authenticate_user` 가 `Id_Logn.Hcode = '0000'` 인 사용자에게 `role="admin"` + `permissions=["*"]` 자동 부여. JWT 의 `role` / `permissions` claim 으로 동봉 (auth.py `_make_token_pair`).
  - (b) **환경변수 화이트리스트**: 운영 긴급 대응을 위해 `BLS_ADMIN_USER_IDS` (콤마 구분) 도 admin 부여 경로로 추가. hcode 값과 무관하게 admin 권한 부여.
  - (c) **가시성 필터 미도입**: G7_Ggeo `Chek5='show1'` SELECT 는 1차에서 여전히 미적용 (DEC-007 (a) 그대로).
  - (d) **명시적 변경 사유**: DEC-007 결정 이후 C10 풀 스코프 (DEC-041~043) 가 도입되면서 `*` 권한 보유자가 필요해짐. admin 페이지 (`/admin/*`) 진입 사용자 0명 상태가 되는 문제 해결.
- **배경/근거**: 사용자 명시 — "admin 계정에 대해서 관리자 권한을 주도록 수정". DEC-007 의 (1차 in_scope=false) 가 "admin UI 진입 불가" 부작용을 발생시켜 본 보강으로 해소. 가시성 필터(데이터 노출 영향) 는 여전히 후속.
- **DoD**:
  - `auth_service._resolve_role_and_permissions(user_id, hcode)` 가 hcode='0000' → `("admin", ["*"])` 반환.
  - `BLS_ADMIN_USER_IDS=user1,user2` 설정 시 동일 결과 (env precedence 동일).
  - JWT decode 시 `role` / `permissions` 클레임이 `get_current_user` 응답에 포함.
  - 프론트 `<PermissionGuard>` 가 admin 사용자에게 모든 화면 진입 허용.
- **결정자**: 메인개발자 + 사용자 (admin 진입 부재 이슈 해결)
- **참조**: `도서물류관리프로그램/backend/app/services/auth_service.py`, `도서물류관리프로그램/backend/app/routers/auth.py`, `도서물류관리프로그램/backend/app/services/admin_service.py::list_user_roles_and_permissions`, DEC-007(원본), DEC-041(응답 코드 표준)

### DEC-CUT-4: C15 Phase 2 — 실 DB 어댑터(Mysql/SqlServer) + cutover_run.py 안전 게이트
- **일자**: 2026-04-20
- **결정 사항**: C15 cut-over 자동화 Phase 2 (T6) 는 다음 단일 정책으로 동결한다.
  - (a) **어댑터 패키지 단일 게이트**: 실 DB 접속은 `scripts/adapters/{base,mysql,sqlserver}.py` 의 `MysqlDataSource`/`SqlServerDataSource` 만 사용한다. 본 어댑터는 **시스템/구조 쿼리만** 허용 — `COUNT(*)`, `INFORMATION_SCHEMA.COLUMNS`, 화이트리스트 컬럼 LIMIT/TOP fetch + Python sha256. 신규 비즈니스 SQL 0건 (DEC-040/044 정합).
  - (b) **식별자 sanitizer 의무**: 동적 식별자(테이블/컬럼) 는 `sanitize_identifier` 화이트리스트 정규식 (`[A-Za-z][A-Za-z0-9_]{0,62}`) 통과만 quoting. 미통과 시 `ValueError` — 어떤 escape 도 시도하지 않는다.
  - (c) **드라이버 lazy import**: `pymysql`/`pyodbc` 는 어댑터 인스턴스의 첫 쿼리 시점에만 import — 미설치 환경(테스트/CI) 에서도 `import scripts.adapters` 만으로는 실패하지 않는다.
  - (d) **자격(credentials) 격리**: 비밀번호는 코드/YAML 평문 ❌. `BLS_C15_PWD__<server_id>` 환경변수 또는 YAML `password_env: VAR_NAME` 만 허용.
  - (e) **운영 자동화 = `scripts/cutover_run.py`**: P1~P6 오케스트레이션 + cutover_validator(P4) 통합 + 단일 JSON 리포트 (`schema_version: "1.0"`). 외부 명령(mysqldump/import/DNS 스위치) 직접 실행 ❌ — 운영 절차 수기.
  - (f) **3단 안전 게이트**:
    1. **OQ 차단** — `cutover.yaml` `cutover_block: true` OQ 미해소 시 live mode 즉시 종료(rc=3). dryrun 은 경고만 기록 (회귀 학습 허용).
    2. **P6 confirm** — `--confirm` 없이 live mode P6 진입 거부(rc=4). dryrun 은 무시.
    3. **rollback 시뮬** — 단계 실패 시 동일 리포트에 `rollback_started_at`/`rollback_elapsed_sec` 기록.
  - (g) **외부 SaaS/네트워크 ❌**: `boto3/azure/sentry/datadog/requests` 등 SDK import 0건 정적 가드 (`test_c15_cutover_phase2_adapter.py::test_S_05`).
- **배경/근거**: 사용자 명시 — "재귀 오류가 발생하지 않도록 기존 케이스/유사 코드 확인 후 일반화 해결". DEC-CUT-1~3 (단계 전환 + 자체 스크립트 + 5종 validator) 위에 *실DB 접속 표면* 만 최소·격리 도입. 임시 우회·우선순위 변경 없이 게이트 위반 시 즉시 종료.
- **DoD**:
  - `scripts/adapters/__init__.py + base.py + mysql.py + sqlserver.py` 존재 + `import` 만으로 드라이버 미설치 환경 통과.
  - `scripts/cutover_run.py --dryrun` rc=0 + GATE/P1~P6 모두 PASS.
  - `scripts/cutover_run.py --legacy ... --modern ...` (live, OQ 미해소) rc=3.
  - `migration/contracts/cutover.yaml` `phase2_runtime` 섹션 + DEC-CUT-4 등록 + `acceptance_criteria` 4건 (Phase 1) 그대로 PASS.
  - `test/test_c15_cutover_phase2_adapter.py` 의 S/R/G 회귀 PASS + Phase 1 회귀 동시 PASS.
  - `dashboard/data/porting-screens.json` `C15.tasks.T6 = completed`.
- **결정자**: 메인개발자 + 사용자 (Phase 2 잔여 — C13/C14/C15 T6 실행 계획 마감)
- **참조**: `scripts/adapters/`, `scripts/cutover_run.py`, `scripts/cutover_validator.py`, `migration/contracts/cutover.yaml`, `test/test_c15_cutover_phase2_adapter.py`, DEC-CUT-1/2/3, DEC-040/044, DEC-033

### DEC-046: Phase 2 32화면 운영체계 — 시나리오 단일 원천 + 사이드바·placeholder·dashboard 동조
- **일자**: 2026-04-21
- **결정 사항**: phase2(32화면) 의 운영 정보(시나리오·진행 단계·blocker)는 다음 단일 원천 체계로 동결한다.
  - (a) **시나리오 단일 원천 = `frontend/src/lib/form-registry.ts::FormMeta.scenario`**: 각 phase2 화면이 `{ input, process, output, eta?, blockers? }` 5필드를 보유. 사이드바 1줄 요약·tooltip·`<ScreenPlaceholder>` 본문이 본 객체만 읽는다 (DRY).
  - (b) **단계 카드 단일 원천 = `dashboard/data/phase2-screen-cards.json`**: 32 화면 × T1~T8 8단 status (`done`/`in_progress`/`pending`/`blocked`). 대시보드 (`dashboard/js/app.js::renderPhase2ScreenCards`) 가 본 JSON 만 렌더 (T1~T8 ✓/◐/○/✕ 색띠 + blocker 강조).
  - (c) **계약 매핑 단일 원천 = `migration/contracts/_phase2_screen_to_contract_map.yaml`**: 32 화면 → 9 yaml(신규 6 + 기존 보강 3) 매핑 + COVERED/COVERED+/NEW 분류. 신규 yaml 추가 시 본 매핑 필수 갱신.
  - (d) **회귀 러너 = `test/test_regression_phase2.py`**: phase2-screen-cards.json 을 자동 로드 → 32 그룹 동적 생성. blocker 보유 화면은 503 NOT_IMPLEMENTED 허용. write-only 화면(POST/PATCH) 은 GET probe SKIP. P95 임계 1200ms (Phase 1 의 800ms 보다 완화 — 신규 SQL 미튜닝 보정). `--multi-db` 로 4대 DB cross-DB invariant 검증.
  - (e) **사이드바 phase2 표시 정책**: phase1 = 녹색 ✓, phase2 = "P2" 배지 + 시나리오 1줄 + tooltip 전체 + ETA, preview = 회색 dot. 사용자 요구("녹색 표시는 5축 PASS 후") 강제.
- **배경/근거**: 사용자 명시 — "각 미구현 화면들에 대해서 항목별로 단순하지만 시나리오로 규정하고 화면과 같은 대시보드 계획까지 업데이트". 시나리오·단계·계약이 4곳(레지스트리/placeholder/사이드바/대시보드) 에 흩뿌려지면 동기 비용 폭증 → 4곳이 동일 단일 원천을 읽도록 통일.
- **DoD**:
  - `form-registry.ts::FormMeta.scenario` 32 phase2 화면 모두 5필드 채움 (`input`/`process`/`output` 필수).
  - `phase2-screen-cards.json` 32 화면 × 8단 status 채움 + `_phase2_screen_to_contract_map.yaml` 9 매핑 등록.
  - `dashboard/js/app.js::renderPhase2ScreenCards` 가 단계 색띠 + blocker 강조 + 진행률 4 카운터 렌더.
  - `<ScreenPlaceholder>` (`screen-placeholder.tsx`) 가 `scenario` 자동 노출 (별도 prop 미주입).
  - `sidebar.tsx` phase2 항목 1줄 요약 + tooltip + ETA 표시.
  - `migration/coverage/phase2-32screens-t1-t2-index.md` 32 화면 분류표 (NEW 15 / REUSE+ 12 / REUSE 5).
  - `test/test_regression_phase2.py` 32 그룹 동적 로드 + dryrun rc=0 + live `--write-json` JSON 산출.
- **결정자**: 메인개발자 + 사용자 (phase2 운영체계 통일 합의)
- **참조**: `frontend/src/lib/form-registry.ts`, `frontend/src/components/screen-placeholder.tsx`, `frontend/src/components/layout/sidebar.tsx`, `dashboard/data/phase2-screen-cards.json`, `dashboard/js/app.js`, `migration/contracts/_phase2_screen_to_contract_map.yaml`, `migration/coverage/phase2-32screens-t1-t2-index.md`, `test/test_regression_phase2.py`, DEC-045(phase1 게이트), DEC-040(신규 SQL 0)

### DEC-047: Phase 2 → Phase 1 승격 = 0건 (1차 baseline) — 4대 DB 환경 등록 + cross-DB PASS 후 재평가
- **일자**: 2026-04-21
- **결정 사항**: 본 PR(F1~F6) 시점에서 phase2 32 화면의 phase1 승격은 **0건** 으로 동결. 사이드바 녹색 ✓ 는 기존 phase1 12 화면만 유지.
  - (a) **승격 0건 근거**: `reports/phase2-regression-2026-04-21.md` 라이브 결과 — 1 PASS / 2 SKIP / 29 FAIL. 단일 PASS(`WebAdmAudit`) 도 data 축(4대 DB cross-DB invariant) 미측정 (`Unknown server id 'mysql8'` 환경 오류). DEC-045 5축 중 data 축 SKIP → 승격 비대상.
  - (b) **승격 게이트 재확인**: phase2 → phase1 승격은 다음 6 항목 모두 충족 시에만 form-registry.ts 의 `phase` 필드 단일 변경 PR 발행 — (1) phase2-screen-cards.json `tasks.T7 == done`, (2) `test_regression_phase2.py --multi-db --servers mysql3 mysql5 mysql8 maria` functional+data+performance PASS, (3) write 화면이면 별도 audit 테스트 PASS, (4) `scenario.blockers == []`, (5) `analysis/screen_cards/<Form>.md` T1 카드 존재, (6) PR description 에 5축 결과 표 + 회귀 JSON 첨부.
  - (c) **차단 화면 명시**: 5 화면(`Sobo48_compare`, `Sobo16_special`, `Sobo29_other`, `Sobo28_delivery`, `Sobo43_stats_route`) 은 `scenario.blockers` 보유 → blocker 해소 전까지 phase1 승격 비대상. `_stub.py` 503 NOT_IMPLEMENTED 응답으로 운영.
  - (d) **승격 후보 분류 (재평가용)**: Tier A 12(T1~T6 done, T7 진행) / Tier B 15(T6 in_progress) / Tier C 5(blocker). 4대 DB 환경 등록 후 Tier A 12 우선 재실행.
  - (e) **재평가 트리거**: backend `BLS_DB_SERVERS` 또는 `app/db/server_registry.py` 에 mysql3/mysql5/mysql8/maria 4 server_id 등록 완료 시 → `test_regression_phase2.py --multi-db` 재실행 → Tier A 12 화면별로 승격 PR 1개씩 분리 발행.
- **배경/근거**: 사용자 명시 — "테스트 및 동작이 레거시코드 비즈니스로직 및 쿼리 등이 적절하게 동일성을 갖게 적용이 완료되고 테스트가 완료된 이후에 녹색 표시" (DEC-045). 라이브 환경 단일 server `mysql8` 만으로 cross-DB invariant 미증명 → 사용자 정책 엄격 적용 결과 0건.
- **DoD**:
  - `form-registry.ts::FormMeta.phase` 32 화면 모두 phase2 유지 (변경 0).
  - `migration/coverage/phase2-promotion-candidates.md` Tier A/B/C 분류 + 승격 진입 체크리스트 6항 + 재평가 명령 동결.
  - `reports/phase2-regression-2026-04-21.json` + `.md` 라이브 baseline 보존.
  - `dashboard/data/phase2-screen-cards.json::tasks.T7` 32 화면 모두 `in_progress`/`pending` (T7 done 0건 정합).
- **결정자**: 메인개발자 + 사용자 (phase1 승격 게이트 엄격 적용 + 환경 미정비 재평가 합의)
- **참조**: `migration/coverage/phase2-promotion-candidates.md`, `reports/phase2-regression-2026-04-21.md`, `reports/phase2-regression-2026-04-21.json`, `frontend/src/lib/form-registry.ts`, `dashboard/data/phase2-screen-cards.json`, DEC-045(승격 게이트), DEC-033(멀티 DB), DEC-046(phase2 운영체계)

### DEC-048: T-B4 트랙 종결 + Phase 3(운영 결합) 별도 게이트로 이관 (.frf→HTML 자동 변환)
- **일자**: 2026-04-21
- **결정 사항**: R&D 트랙 T-B4 (.frf → HTML 자동 변환 PoC) 의 **변환 작업 자체는 100% 완료** 로 동결. 단, **운영 FastAPI 결합(Phase 3) 은 별도 게이트로 이관** 한다.
  - (a) **트랙 status = done**: 저장소 전역 .frf 1744 양식을 `*.template.html` + `*.ir.json` 으로 1:1 자동 변환 완료 (`debug/output/frf_converted_all`). 변환 스크립트 `debug/frf_batch_convert_all.py` + 품질 리포트 `debug/frf_quality_report.py` 동결. PoC 1일 보고서 `analysis/research/c7_b4_poc_1day_report.md` 3 가설 (H1 부분 / H2 ✅ / H3 ⚠️) 정리.
  - (b) **Phase 3 진입 = 별도 게이트**: 운영 FastAPI/WeasyPrint 결합은 **3 조건 게이트** — (1) 운영 SME 협의 (98 양식 변경 빈도 합의), (2) ROI 비교 회의록 (B1 자체 파서 vs B4 빌드타임 변환), (3) R&D 가용성. 3 조건 동시 충족 전까지 운영 제품(`도서물류관리프로그램/`) 에 본 산출물 결합 0줄.
  - (c) **DEC-039 정책 유지**: "운영 .frf 자동 변환 0" (DEC-039) 는 Phase 3 게이트 통과 전까지 계속 유지. 본 산출물은 빌드타임 참조 자산 만으로 분류.
  - (d) **대시보드 정합**: `dashboard/data/tracks.json::T-B4.status = done` + `phase3_followup = deferred_dec048`. `M1c` (트랙 종결) 마감 / `M2`(SME 협의)·`M3`(ROI 회의록)·`M4`(Phase 3 결정) 는 본 결정 별도 추적.
- **배경/근거**: 사용자 확인 (2026-04-21) — ".frf → HTML 자동 변환 (B4 PoC) 변환 처리 완료되었다고 보는데 대시보드 확인하여 업데이트". 변환 작업 자체와 운영 결합을 분리하지 않으면 (1) 본 PoC 의 객관적 산출물 가치(1744 양식 자동화) 가 'Phase 3 미진입' 라벨에 가려지고, (2) Phase 3 운영 결합 비용(SME·ROI·R&D 가용성) 이 무리하게 끌려가는 위험. 두 게이트 분리.
- **DoD**:
  - `dashboard/data/tracks.json::T-B4.status = done` + `phase3_followup = deferred_dec048`.
  - `dashboard/data/web-porting-progress.json::phase` 라벨에 "Track B4 done (DEC-048)" 포함.
  - `dashboard/data/timeline.json` 에 DEC-048 entry 1건.
  - `dashboard/js/app.js` 의 트랙 카드 렌더에서 `phase3_followup` 배지 노출.
  - `legacy-analysis/decisions.md` 에 본 결정 등록.
- **결정자**: 메인개발자 + 사용자 (.frf 변환 작업 종결 + Phase 3 별도 게이트 합의)
- **참조**: `analysis/research/c7_b4_poc_1day_report.md`, `debug/frf_batch_convert_all.py`, `debug/frf_quality_report.py`, `debug/output/frf_converted_all/`, `dashboard/data/tracks.json`, `dashboard/data/timeline.json`, `dashboard/data/web-porting-progress.json`, DEC-037(WeasyPrint), DEC-038(우편엽서 1종), DEC-039(운영 .frf 자동 변환 0)

### DEC-049: 발송비/입금 메뉴 IA 복원 = settlement 라우트 별칭 (billing 그룹은 메뉴 진입점 only)

- **일자**: 2026-04-21
- **결정 사항**: 웹 `MENU_GROUPS` 의 `billing` (발송비/입금) 그룹은 **레거시 「메인 메뉴 / 발송비/입금관리」 트리의 IA 복원 전용** 으로 운영하며, **백엔드 라우트의 정본은 모두 `/settlement/*`** 로 유지한다.
  - (a) **별칭 정책**: `form-registry.ts` 의 `menuGroup: "billing"` 항목은 동일 `route` 를 가리키는 얇은 별칭 (`*_bill` 접미). 라우트·페이지·계약·테스트는 단일 (DEC-046 단일 원천). 별칭 8 행 = 청구서관리(택배 변형 포함) / 청구금액(년월) / 청구서출력 / 입금내역 / 입금현황(거래처/일자) / 세금계산서.
  - (b) **단일 원천 매핑**: 레거시 14행 ↔ 웹 매핑은 [`migration/coverage/billing-deposit-menu-legacy-to-web-map.md`](../migration/coverage/billing-deposit-menu-legacy-to-web-map.md) 1 파일이 정본. 카드 추적은 [`dashboard/data/billing-c5-menu-porting.json`](../dashboard/data/billing-c5-menu-porting.json) 1 파일이 정본 (T1~T8 단계).
  - (c) **wrong_id 가드**: 레거시 `Subu43` (발송비내역) ↔ 웹 `Sobo43_stats_route` (출판사통계, `/stats/publisher`), 레거시 `Subu44` (발송비현황) ↔ 웹 `Sobo44_inv` (재고현황, `/inventory/status`) 두 건은 **동일 폴더·다른 도메인**. 진짜 발송비 도메인은 신규 ID **`Sobo43_shipping_ledger` / `Sobo44_shipping_status`** + 신규 라우트 (`/settlement/shipping-ledger` / `/settlement/shipping-status`) 로 분리한다 (P2 백로그).
  - (d) **이전 (`moved`) 미노출**: 반품수거내역(Sobo36)·반품수거현황(Sobo37)·출고내역서(Sobo39) 는 이미 다른 메뉴(statistics/report) 에 배치되어 있어 `billing` 메뉴에는 노출하지 않는다 (중복 진입점 회피).
  - (e) **신규 SQL 0**: 별칭은 라우트 재사용 only — 백엔드 SQL/계약/테스트 추가 0 (DEC-040 정합).
- **배경/근거**: 사용자 확인 (2026-04-21) — "발송비/입금 메뉴는 아직 준비중... 이라고 메시지가 나오는데 레거시 델파이 소스에는 기존 기능이 없나?". 조사 결과 레거시에는 14화면 (입금/청구/세금/발송비/반품수거/출고내역서/메세지) 이 존재하나, 웹 `billing` 그룹에 등록된 폼이 0건이라 사이드바가 「준비 중...」 만 표시. C5 기능 8개는 이미 `settlement` 그룹으로 포팅 완료 (DEC-031/032/034/035/036) 이므로 라우트를 옮기지 않고 **별칭만 추가** 하는 것이 회귀 비용·DEC-046 단일 원천·DEC-040 신규 SQL 0 정책에 모두 부합.
- **대안**: (1) 정산 화면을 `/billing/*` 로 물리 이동 + 리다이렉트 → DEC-046 단일 원천 충돌, 회귀 비용 큼. (2) 레거시 `Subu43`/`Subu44` 명칭을 그대로 가져와 ID 재사용 → wrong_id 충돌 영구화. (3) 메뉴 노출 안 하고 그대로 두기 → 레거시 사용자 IA 학습 비용 증가.
- **DoD**:
  - `form-registry.ts` 에 `menuGroup: "billing"` 항목 ≥ 1 (실제 8 행) — 사이드바 「준비 중」 메시지 해소.
  - 매핑 문서 행 수 = 대시보드 JSON `screens[]` 수 (현 16 행).
  - wrong_id 2 건 매핑 문서 §3 + 대시보드 `wrong_id_warnings[]` + 본 결정 (c) 에 모두 기록.
  - Subu43/44 진짜 발송비 도메인은 본 결정 시점에는 메뉴 미노출, P2 백로그 (단계 4) 등록.
- **결정자**: 메인개발자 + 사용자 (발송비/입금 하위 메뉴 포팅 작업 계획 합의)
- **참조**: DEC-019 (Sobo42_1/45_1 = variant 단일화), DEC-031/032/034/035/036 (C5 정산), DEC-040 (신규 SQL 0), DEC-046 (단일 원천 패턴), `migration/coverage/billing-deposit-menu-legacy-to-web-map.md`, `migration/coverage/billing-subu43-44-shipping-backlog.md` (P2 백로그), `dashboard/data/billing-c5-menu-porting.json`, `dashboard/js/app.js::renderBillingMenuPorting`

### DEC-050: .frf→HTML 운영 결합 = per-form 화이트리스트 옵트인 (자동 변환 0 영속 + Phase 3 게이트)

- **일자**: 2026-04-21
- **결정 사항**: 1744 변환 자산 (`debug/output/frf_converted_all/`) 의 운영 결합은 **per-form 화이트리스트 PR 단위 옵트인** 으로만 진행하며, **자동 변환 0** (DEC-039) 영속 정책을 유지한다.
  - (a) **레지스트리 단일 원천**: `backend/app/services/print_template_registry.py::_WHITELIST` dict 1개가 화이트리스트 정본. 행 추가는 PR 1건 = 1행 (혼합 금지). 동일 PR 에 IR 파일을 `print_templates/auto/` 로 **수동 복사** 의무. 자동 sync 스크립트 작성·실행 0.
  - (b) **환경변수 게이트**: `PRINT_TEMPLATE_MODE=auto` (기본 `manual`) 인 경우만 화이트리스트 활성화. 운영 기본은 manual 보존 — Phase 1 byte-identical 정본 회귀 0.
  - (c) **Phase 3 게이트 3 조건** (`docs/phase3-print-gate.md`): G1 SME 협의 (`analysis/research/c7_phase3_sme_review.md`) + G2 B1 vs B4 ROI (`analysis/research/c7_b1_vs_b4_roi.md`) + G3 R&D 가용성 (`analysis/research/c7_phase3_capacity.md`) 모두 PASS 시에만 화이트리스트 PR 개시.
  - (d) **품질 점수 게이트**: SOP-A 진입 자격 = `binding_fill ≥ 0.7` AND `coord_recovery ≥ 0.95` (`docs/print-form-add-sop.md` §A4). HIGH 버킷 996/1744 만 자동 대상.
  - (e) **graceful fallback**: IR 파일 누락 / 컴파일 에러 / 화이트리스트 미등록 시 자동으로 manual 빌더로 폴백 + WARNING 로그. 운영 5xx 누설 0.
  - (f) **DEC-046 단일 원천 불변식**: `_WHITELIST` 행 수 = `print_templates/auto/*.ir.json` 파일 수 = `dashboard/data/frf-html-porting.json::screens` 의 `mappingType="ir_in_use"` 행 수 (3 곳 동수). 본 invariant 는 `test_print_template_registry::test_R03_single_source_truth` 가 회귀 가드.
- **배경/근거**: T-B4 PoC 가 1744 자산 변환을 100% 완료 (DEC-048) 했으나 운영 결합 1건만 (`Report_1_21.ir.json`) 인 상태. SME 합의 없이 1744 자산을 모두 결합하면 (1) 양식 변경 추적 불가 (2) 시각 회귀 비용 폭증 (3) DEC-039 정책 충돌. per-form opt-in PR + Phase 3 게이트 + 품질 점수 게이트로 점진 도입이 회귀 비용·DEC-039 정합·DEC-046 단일 원천 모두 만족.
- **대안**: (1) B1 자체 파서 신규 작성 (운영 결합 자동) → DEC-039 충돌 + 파서 RFC 4~6 주 비용. ROI 게이트 G2 에서 비교 검토 (`c7_b1_vs_b4_roi.md`). (2) 1744 전체 자동 결합 → 양식 변경 추적 불가 + 회귀 비용 ∞. (3) 카탈로그 only (운영 결합 0 유지) → P0 라벨 / 청구서 / 세금 정합도 향상 기회 손실.
- **DoD**:
  - `print_template_registry.py` 신설 + `label_service._try_render_label_auto` 위임 (행동 정합) + `test_print_template_registry` 8 PASS + `test_c7_print_phase3_auto_template` 11 PASS 회귀 0.
  - 4 산출물 동결: `migration/coverage/frf-html-form-catalog.md` (1744 카탈로그) + `migration/coverage/frf-to-screen-usage-map.md` (169 직접 호출 + Tong40.PrinTing00 디스패처) + `docs/print-html-status.md` (운영 라우트 6 + IR 결합 1) + `docs/print-form-add-sop.md` (A/B 경로 + 품질 게이트).
  - 게이트 3 산출물 양식 동결 (PENDING 으로 표시): `c7_phase3_sme_review.md` + `c7_b1_vs_b4_roi.md` + `c7_phase3_capacity.md`.
  - 대시보드 단일 원천: `dashboard/data/frf-html-porting.json` (8 카드, P0~P3 백로그 4 분류 등록) + `dashboard/js/app.js::renderFrfHtmlPorting` 노출.
  - DEC-046 단일 원천 invariant: `_WHITELIST` 행 수 = 1 = `print_templates/auto/*.ir.json` 파일 수 = `screens[mappingType=ir_in_use]` 행 수.
- **결정자**: 메인개발자 + 사용자 (.frf→HTML 운영 결합 + 신규 서식 SOP 계획 합의)
- **참조**: DEC-037 (WeasyPrint 단일 엔진), DEC-038 (라벨 1종 → Phase 2-α 5종 확장), DEC-039 (운영 .frf 자동 변환 0), DEC-040 (신규 SQL 0), DEC-046 (단일 원천 패턴), DEC-048 (T-B4 종결 + Phase 3 별도 게이트), `backend/app/services/print_template_registry.py`, `backend/app/services/label_service.py`, `docs/phase3-print-gate.md`, `docs/print-form-add-sop.md`, `dashboard/data/frf-html-porting.json`, `dashboard/js/app.js::renderFrfHtmlPorting`, `test/test_print_template_registry.py`

### DEC-033: 멀티 DB 호환 의무 — mysql3 SQL 헬퍼 + 스키마 어댑터 + 정기 점검 (alwaysApply)
- **일자**: 2026-04-19
- **결정 사항**: 백엔드는 **모든 등록 DB 서버**(`remote_138`, `remote_153`, `remote_154`, `remote_155` 등 `servers.yaml` 프로필)에서 조회·목록이 동일하게 동작해야 한다.
  - (a) **페이지네이션**은 `app.core.sql_mysql3` 의 `apply_limit_offset_syntax` + `limit_offset_bind` 로 `mysql3_protocol` 서버(154/155) 와 표준 서버 모두 지원한다. `LIMIT %s OFFSET %s` 문자열만 두고 헬퍼 없이 호출하지 않는다.
  - (b) **테넌트별 스키마 변이**는 서비스 파일에 `if server_id` 분기로 흩뿌리지 않고, `app/services/<table>_adapt.py` 패턴으로 `SHOW COLUMNS` 등으로 흡수한다 (예: `T5_Ssub` → `t5_ssub_adapt.py`).
  - (c) **신규 라우터 GET** 은 `debug/probe_backend_all_servers.py` 의 `_routes_for` 매트릭스에 그룹을 추가해 4대 스모크에 포함한다.
- **배경/근거**: 2026-04 C5 정산 회귀 — `remote_138` 에서 `T5_Ssub` 에 `Sdate` 등 누락, `remote_154`/`remote_155` 에서 `LIMIT … OFFSET …` 문법·현대 SQL 표현 불가. 동일 종류 재발 방지.
- **DoD**: 4대 서버 각각 L2 `SELECT 1` 성공 + L4 GET 매트릭스 전부 OK(빈 목록 200 허용). 예외는 `migration/contracts/… customer_variants` 또는 본 DEC에 명시된 경우만.
- **운영**: `.cursor/rules/multi-db-compat.mdc` 로 alwaysApply; `docs/db-smoke-runbook.md` 절차 준수; 쓰기 경로 mysql3 호환은 별도 스테이징에서 검증.
- **결정자**: 메인개발자 + 사용자 (멀티 DB API 연동 점검 계획 반영)
- **참조**: `도서물류관리프로그램/backend/app/core/sql_mysql3.py`, `도서물류관리프로그램/backend/app/services/t5_ssub_adapt.py`, `debug/probe_backend_all_servers.py`, `docs/db-smoke-runbook.md`, `.github/workflows/db-smoke.yml`

### DEC-051: 인증 서버 단일화 — `BLS_AUTH_SERVER_ID` 게이트
- **일자**: 2026-04-21
- **결정 사항**: 모든 사용자 비밀번호 검증은 환경변수 `BLS_AUTH_SERVER_ID` (기본 `remote_138`) 한 곳의 `web_users` 에서만 수행한다. 기타 등록된 데이터 서버(`remote_153`, `remote_154`, `remote_155` 등)는 **데이터 전용**이며 자체 자격증명을 노출하지 않는다.
  - (a) 로그인 화면(`(public)/login/page.tsx`) 의 「DB 서버 선택」 콤보·`useEffect(/api/v1/servers)` 호출은 제거된다.
  - (b) `POST /api/v1/auth/login` 의 `serverId` 입력값은 **무시**되며(BC 위해 필드는 deprecated 로 유지), 라우터는 항상 `BLS_AUTH_SERVER_ID` 로 `authenticate_user()` 를 호출한다.
  - (c) JWT `sid` 클레임은 인증 서버가 아니라 **사용자별 primary 데이터 서버**(DEC-052) 로 채워지며, 미설정 시에만 `BLS_AUTH_SERVER_ID` 로 폴백한다.
- **배경/근거**: 운영상 `web_users` 시드는 `remote_138` 한 곳에 통합되어 있고, 기존 다중 콤보 UI 는 (1) 잘못된 서버 선택 시 401, (2) 인증 서버와 데이터 서버 의미를 사용자에게 떠넘기는 혼란을 일으킨다. 레거시 `Sobo10` 도 부팅 환경 1개 DB 만 본다.
- **DoD**: `serverId` 미전송 로그인 200 + JWT `sid` = primary 매핑(없으면 auth 서버) + 회귀 `test_auth_login_fixed_server.py` 전건 PASS + 4대 서버 L4 GET 매트릭스(DEC-033) 무회귀.
- **운영**: `.env`/실행 안내에 `BLS_AUTH_SERVER_ID=remote_138` 를 명시. 인증 서버를 다른 곳으로 옮길 때는 본 키만 변경. 데이터 서버 추가/삭제는 자격증명 동기화 없이 가능.
- **결정자**: 메인개발자 + 사용자 (로그인 서버 선택 UI 제거 합의)
- **참조**: `도서물류관리프로그램/backend/app/routers/auth.py`, `도서물류관리프로그램/backend/app/services/auth_service.py`, `도서물류관리프로그램/frontend/src/app/(public)/login/page.tsx`, `도서물류관리프로그램/frontend/src/contexts/auth-context.tsx`, `test/test_auth_login_fixed_server.py`, DEC-052

### DEC-052: 사용자별 데이터 서버 1:1 (Primary)
- **일자**: 2026-04-21
- **결정 사항**: `web_user_servers` 의 의미를 **다대다 → 1대1(Primary)** 로 좁힌다. 한 사용자(`user_id`) 는 0~1 row 만 가진다.
  - (a) admin UI([(app)/admin/user-servers/page.tsx](../도서물류관리프로그램/frontend/src/app/(app)/admin/user-servers/page.tsx)) 는 다중 토글 → **라디오 1개 선택(Primary)** 으로 교체. `adminApi.setPrimaryServer(userId, serverId|null)` 신설.
  - (b) `admin_service.assign_server(allow=True)` 호출 시 동일 `user_id` 의 기존 row 를 모두 제거 후 1건 INSERT (LSP 보존: 시그니처 유지, 의미만 좁힘). `set_primary_data_server(user_id, server_id, actor)` / `get_primary_data_server(login_id) -> str|None` 신규 함수.
  - (c) `_load_state()` 직후 `_normalize_primary_servers()` 로 **부팅 1회 idempotent 마이그레이션** 실행 — 동일 user_id 가 2건 이상이면 마지막 created 만 유지하고 나머지는 audit `user.server.dedup` 로 기록.
  - (d) 라우터(`/api/v1/auth/login`) 는 `data_server_id = get_primary_data_server(user_id) or BLS_AUTH_SERVER_ID` 로 JWT `sid` 적재.
- **배경/근거**: 다중 매핑은 「로그인 서버 선택 콤보」 와 1:1 대응될 때만 의미 있는데, DEC-051 로 콤보가 사라지면 사용자가 어느 서버로 작업할지 자체적으로 결정할 수 없다. 운영자 1인이 admin 화면에서 명시적으로 1개 서버를 부여하는 정책이 안전하고 단순하다.
- **DoD**: 동일 user 다중 row → 1건 정리 audit 발생 + admin 라디오 UI 단일 선택 강제 + 회귀 `test_admin_primary_server.py` PASS + 사용자 헤더에 미설정 경고 배지 노출.
- **운영**: 데이터 모델 컬럼명은 변경하지 않는다(BC). 기존 자동화 스크립트가 동일 사용자에게 다중 row 를 기록해도 다음 부팅 시 1건으로 정리된다.
- **결정자**: 메인개발자 + 사용자 (1 사용자 1 데이터 서버 정책 합의)
- **참조**: `도서물류관리프로그램/backend/app/services/admin_service.py`, `도서물류관리프로그램/backend/data/web_admin.json`, `도서물류관리프로그램/frontend/src/app/(app)/admin/user-servers/page.tsx`, `도서물류관리프로그램/frontend/src/components/app-shell/header.tsx`, `test/test_admin_primary_server.py`, DEC-051

---
*최종 업데이트: 2026-04-21 — DEC-051/052 신규 추가 (인증 서버 단일화 = `BLS_AUTH_SERVER_ID` 고정 게이트, 로그인 화면 서버 콤보 제거, JWT `sid`=primary 데이터 서버 / 사용자-데이터 서버 1:1(Primary) = `web_user_servers` 다대다→1대1 의미 좁힘 + admin 라디오 UI + 부팅 1회 idempotent 마이그레이션 + 미설정 헤더 경고 배지). DEC-050 등 기존 결정 무변경.*
*이전: 2026-04-21 — DEC-050 신규 추가 (.frf→HTML 운영 결합 = per-form 화이트리스트 옵트인, 자동 변환 0 영속, Phase 3 게이트 G1/G2/G3 + 품질 점수 게이트 binding≥0.7/coord≥0.95, print_template_registry + label_service 위임 + frf-html-porting.json/renderFrfHtmlPorting 단일 원천, 회귀 19 PASS).*
*이전: 2026-04-21 — DEC-049 신규 추가 (발송비/입금 메뉴 IA 복원 = settlement 라우트 별칭, billing 그룹은 진입점 only, wrong_id 2건 가드 + 진짜 발송비 도메인 P2 백로그 분리, 신규 SQL 0).*
*이전: 2026-04-21 — DEC-046/047/048 신규 추가. DEC-046(phase2 32화면 운영체계 = 시나리오/단계카드/계약/회귀 4 단일원천 + 사이드바 1줄 표시 + ScreenPlaceholder DRY). DEC-047(phase2→phase1 승격 = 0건, 4대 DB 환경 등록 + cross-DB PASS 후 재평가, Tier A 12 / Tier B 15 / Tier C 5 분류). DEC-048(T-B4 .frf→HTML 변환 작업 100% 완료 = 트랙 status=done, Phase 3 운영 결합은 SME·ROI·R&D 3 조건 별도 게이트, DEC-039 정책 유지).*
*이전: 2026-04-21 — DEC-045 신규 추가 (Phase1 승격 게이트 = 레거시 동등성 + 자동 회귀 통과, T1~T8 단계, 5축 PASS 의무, 화면 1개=PR 1개, 강등 정책). DEC-007 보강 추가 (hcode='0000' 자동 admin 권한 부여 + BLS_ADMIN_USER_IDS env 화이트리스트). 가시성 필터(G7_Ggeo Chek5='show1') 는 여전히 1차 미도입.*
*이전: 2026-04-20 — DEC-CUT-4 신규 추가 (C15 Phase 2 — 실 DB 어댑터 `MysqlDataSource`/`SqlServerDataSource` + `cutover_run.py` 안전 게이트 3단(OQ 차단·P6 confirm·rollback 시뮬)). 어댑터는 시스템/구조 쿼리만 + sanitize_identifier 화이트리스트 + 드라이버 lazy import + 자격 ENV-only. 외부 SaaS/네트워크 SDK 0건 정적 가드.*
*이전: 2026-04-20 — DEC-041/042/043 신규 추가 (C10 풀 스코프 마감: 세션·권한 응답 코드 표준 + 글로벌 401/403 인터셉터 / If-Match·ETag 낙관적 동시편집 / IdP·SSO 인터페이스 분리). OQ-RT-7 (D_Select 실분기) 마감 — Phase 2 인터페이스 → C10 Phase 1 실분기 도입 (admin/branch_manager/auditor/operator 4 분기). 신규 SQL 0건 (DEC-040 룰 적용).*
*이전: 2026-04-20 — DEC-040 신규 추가 (C8 바코드 스캔 = 서버 매칭 + 클라이언트 라인 반영 분리, 신규 SQL 0). DEC-010 마감 표시 (C8 Phase 1 사이클로 후속 작업 완료). OQ-002 → OQ-002-R 잔류 (Web Serial 직결만).*
*이전: 2026-04-20 — ⭐ DEC-039 R&D 보강 (4) 게임 체인저: FastReports/FastReport 로컬 소스 직접 분석 → (a) HTML export 코어 내장 (1187+992 LOC, MIT, Layer 모드 = 픽셀 절대 좌표) 발견. (b) PdfSimple 라이선스 MIT 로 교정 (이전 LGPL 오기). (c) Import 플러그인 4종 = `.frf` 임포터 템플릿. (d) 신규 권장 전략 B4 (빌드 타임 변환 + Jinja2) — 자체 파서 비용 6~13 → **4.5~8.5 인주** (30~40% 단축), 운영 .NET 의존성 0. Phase 2 자체 파서 도입 시 1 순위 권장. DEC-039 정책 (Phase 1 = 자동 변환 0) 무변경.*
*이전: 2026-04-20 — DEC-039 R&D 보강 (3): atkins126/FastReportExport (Apache-2.0, antoniojmsjr 본 fork) 조사 반영. 부수: `.frf` 시그니처 hexdump 검증 → §1.3 FreeReport 2.3 가설 100% 유효.*
*이전: 2026-04-20 — DEC-039 R&D 보강 (2): yusufbal/FastReport.OpenSource.HtmlExporter (MIT, .NET 8) 커뮤니티 사례 반영 — HTML→PDF 우회 패턴이 .NET OSS 진영의 베스트 프랙티스로 확인되어 DEC-037 (HTML 빌더 → WeasyPrint) 아키텍처 정당성 강화. WeasyPrint (BSD-3) 가 iText7 (Apache 2.0/AGPL) 보다 운영 라이선스 면에서 우월. T10 R&D 안에 B3 안 (HtmlExporter Ground Truth 회귀 게이트) 추가.*
*이전: 2026-04-20 — DEC-037/038/039 신규 추가 (C7 Phase 1 — WeasyPrint 단일 엔진, 라벨 우편엽서 1종, .frf = 참조용 정본). DEC-039 R&D 보강 (1): FastReports/FastReport.Documentation (MIT) 조사 결과 — `.frx` IR 채택 권장. OQ-002 부분 해소. DEC-034 보강 (PDF 다운로드 동시 제공).*
*이전: 2026-04-19 — DEC-034/035/036 신규 추가 (C5 정산 Phase 2 — Sobo46/49 인쇄 = HTML 미리보기, 세금 외부 발행 stub, Chek3 토글 단일 헬퍼). OQ-ST-1/OQ-ST-2 종결.*
*이전: 2026-04-19 — DEC-033 신규 추가 (멀티 DB 호환 alwaysApply 룰 + 점검 매트릭스 동결).*
*이전: 2026-04-19 — DEC-031/032 신규 추가 (C5 정산 Phase 1 마감 가드 + Gpass 폐기/bcrypt 회전 동결).*
*이전: 2026-04-19 — DEC-029 Phase 2 완료 보강 (bcrypt + audit_returns DB 영속화).*
*이전: 2026-04-19 — DEC-030 신규 추가 (C4 OQ-RT 번호 정본 통일).*
*이전: 2026-04-19 — DEC-029 신규 추가 (C4 반품 재고 변경 패스워드 게이트 동결).*
*이전: 2026-04-19 — DEC-024/027/028 신규 추가 (C3 입고 1차 정책 + dfm 레이아웃 산출물 영구 입력 동결).*
*이전: 2026-04-18 — DEC-019~023 신규 추가 (C9 단일 원천 + Wave D 웹 관리 플레인 동결).*
*이전: 2026-04-25 — DEC-009~012 신규 추가 (C2 출고 접수 1차 포팅 범위 동결: 권한키·바코드·인쇄·물리삭제 모두 후속 이관). 1차 합격선은 "출고 주문 신규+수정+취소+조회 CRUD".*
*이전: 2026-04-22 (revised) — DEC-005~008 모두 "1차 포팅 범위 외" 로 동결. 1차 합격선은 "기존 사용자가 기존 ID/PW 그대로 로그인". 멀티테넌시·해시·라이선스·슈퍼유저 분기는 후속 작업으로 이관.*
