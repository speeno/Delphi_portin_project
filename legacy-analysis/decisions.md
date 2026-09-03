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
  - **(2026-04-21 보강 — 사이드바 정합화)** Sobo19 는 `Subu14/12/11/15.pas` 에서 `ShowModal` 로 호출되는 InputBox 류 다이얼로그(폼 크기 306x137)로 정식 메뉴가 아님. 모바일웹(m.websend.kr)·델파이 정식 메뉴 어디에도 단독 노출 사례 없음 → form-registry.ts 의 `Sobo19` stub 항목을 사이드바에서 제거(Wave D `/admin/settings` `WebAdmEnv` 만 단일 원천 노출). 레거시 dfm/pas 보존은 변동 없음.
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
  - **(2026-04-21 보강 — 사이드바 정합화)** 「대표 1폼만 1차 노출」 원칙에 따라 사이드바에서 `Sobo39_1`(할인율 2)·`Sobo39_2`(할인율 기타)·`Sobo39_5`(할인율 물류) stub 3건 제거. 변형 차이는 `migration/contracts/master_data.yaml` 의 `customer_variants` 단일 원천에만 보유하고, `/master/discount/[type]` 동적 라우트는 직접 URL 진입 시에만 placeholder 노출(메뉴 비노출). 사이드바 master 그룹은 정식 6폼(Sobo11/14/17/38/39/45) + phase2 1폼(Sobo16_special) = 7행으로 정합. **Sobo16_special(특별관리)** phase1 정식 승격 절차는 `docs/master-special-implementation-plan.md` 단일 원천에 T1~T8 계획·blocker(BLK-SPC-1/2)·DoD 정리.
- **결정자**: 메인개발자
- **참조**: `analysis/screen_cards/Sobo{11,14,17,38,39,45}*.md`, `migration/contracts/master_data.yaml`, `docs/master-special-implementation-plan.md`

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
  - **(2026-04-21 보강)** phase1 승격 시 `analysis/audit/phase1-component-fidelity.md` 매트릭스 GAP-P0 = 0 가드 (DEC-053).
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
  - **(d) 보관본 출력 경로 분리 (2026-05-04 보강)**: 레거시와 동등한 **보관용 HTML·PDF 미리보기** (`GET …/tax-invoice/{key}/print`, `…/print.pdf`) 는 동일 `T2_Ssub` 행을 **목록 API 과 같은 컬럼 어댑터**(`SHOW COLUMNS` 기반 동적 SELECT, DEC-058)로 읽으며, **DEC-035 stub 와 무관하게 완결된 사용자 가치**를 제공한다. Stub 은 `/issue` 의 외부 채널 호출 부재만 의미한다.
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

### MENUVIS-DEC-07: 메뉴 가시성 show-first + 사용자별 메뉴 감추기
- **일자**: 2026-05-30
- **결정 사항**: 메뉴 가시성을 **show-first** 로 전환한다.
  - (a) **RBAC 축은 숨기지 않음**: `account_types`/`build_roles`/`warehouse_menu_tiers` 는 「대상 빌드 힌트」로만 남고 메뉴를 숨기는 데 쓰지 않는다. `is_menu_visible_rbac` / `isMenuVisible` 는 알려진 메뉴면 항상 노출(슈퍼유저 우회 유지, 미정의 menuId 만 비공개).
  - (b) **숨김 축은 3가지만**: ① 빌드 `forced_hidden`(MENUVIS-DEC-03) ② 사용자별 `hidden_menu_ids`(L2, 관리자 설정) ③ 계정유형 오버레이 `visibility=deny`. 라이선스(Fxx) 미보유는 숨기지 않고 `disabled`(MENUVIS-DEC-06)만 적용.
  - (c) **사용자별 감추기 저장소**: `backend/data/user_menu_visibility.json` — 키 `(server_id, hcode, gcode)` 4-key(`gname` 은 표시·감사용). 빈 목록이면 행 제거(전체 노출 복귀). GR-DB-005 준수(신규 SQL 0건). 단일 원천: `app/services/user_menu_visibility_service.py`.
  - (d) **클레임 전달**: `auth._enrich_user_profile` 가 로그인/`/me` 시 `hidden_menu_ids` 를 신선하게 로드 → `UserInfo.hidden_menu_ids` → 프론트 `use-permissions` → `navUiState`. JWT 미적재(크기·신선도 이유).
  - (e) **관리자 UI**: `/admin/id-logn` 우측에 「메뉴 노출」 체크리스트(기본 전체 체크=보임). 관리 API `GET/PUT /api/v1/admin/users/menu-visibility`(4-key, super-admin 게이트).
- **배경/근거**: 사용자 요구 — "기본적으로 모든 메뉴가 보이도록 하고, 관리자에서 사용자별·메뉴항목별 보이기/감추기". 또한 `account_type` 미매핑 계정에서 사이드바가 0건이 되고 신규 기초관리 3화면(입고처/기타거래처/저자)이 미노출되던 회귀를 근본 제거. API·라우터 403(권한) 모델은 유지 — URL 직접 입력은 여전히 권한으로 차단(비파괴).
- **대안**: (1) 매트릭스 기반 hide 유지(미매핑 0건 회귀 지속) (2) account_type 보정만(신규 화면·운영 변경마다 재발).
- **영향**: `backend/app/core/menu_policy.py`(`is_menu_visible_rbac`/`nav_ui_state_for_menu`/`MenuPolicyContext.hidden_menu_ids`), 프론트 `account-menu-matrix.ts`(`isMenuVisible`/`navUiState`/`hiddenMenuIds`), `use-permissions.ts`, `auth-context.tsx`/`models/auth.py`(`hidden_menu_ids`), `routers/auth.py`·`routers/admin.py`, 신규 `user_menu_visibility_service.py`. 회귀: `test/test_menu_visibility_show_first.py`, `test_account_menu_matrix_visibility.py`(show-first), `test_menu_policy_overrides.py`.
- **결정자**: 메인개발자 + 사용자 (`show_first` 명시 선택)
- **참조**: `docs/menu-visibility-runtime-design.md` MENUVIS-DEC-07, `analysis/audit/menu-visibility-show-first-baseline.json`, MENUVIS-DEC-03/06, DEC-RBAC-01/03

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
  - (d) **(2026-04-21 보강 — HOTFIX)** LIST 엔드포인트의 `total` 산출은 **반드시** `app.core.sql_mysql3.count_grouped(server_id, table, where_sql, group_by, having, params)` 헬퍼만 사용한다. `SELECT COUNT(*) FROM (subquery) t` 형태의 파생 테이블 직접 작성을 금지한다 — MySQL 3.23 호환 서버에서 1064 → HTTP 500 재발 차단(C2 출고/C3 입고/C4 반품/C6 거래명세서 4화면 동시 회귀 사례). 회귀 가드: `test/test_list_count_grouped_mysql3.py`.
  - (d++) **(2026-04-23 보강 — 기간별 재고원장 500 + 기간별 반품 거래처명 누락 동시 핫픽스)** (d) 의 derived-table 금지 정책 + 출판사명 lookup 단일 진실 원천 정책을 반품 화면 2종에도 일반화. 사례: ① `returns_service.SQL_LEDGER_MASTER_COUNT` 가 ``SELECT COUNT(*) AS total FROM (… GROUP BY s.Bcode, s.Scode, s.Gubun, s.Pubun) AS sub`` 파생 테이블 패턴을 잔존시켜 mysql3 서버(예: `remote_155`)에서 1064 → HTTP 500 회귀(사용자 보고 "기간별 재고원장 화면은 500 오류"). ② `returns_service.SQL_PERIOD_MASTER` 가 ``LEFT JOIN G1_Ggeo g ON g.Gcode=s.Hcode AND g.Hcode=''`` 로 출판사명을 (복합키 거래처 마스터 G1_Ggeo)에서 빈 Hcode row 매칭 시도 — 거의 매칭이 없어 hname 항상 빈 값(사용자 보고 "기간별 반품 내역서 화면에 거래처명이 출력되지 않는다"). 채택: ① `SQL_LEDGER_MASTER_COUNT` 상수를 `SQL_LEDGER_MASTER_COUNT_WHERE` + `SQL_LEDGER_MASTER_GROUP_BY` 절(節) 분해 + `ledger_query` 본체에서 `count_grouped(server_id, table="S1_Ssub s", where_sql=…, group_by=…)` 1회 호출(파생 테이블 0). ② `SQL_PERIOD_MASTER` 의 join 을 ``LEFT JOIN G7_Ggeo g ON g.Gcode=s.Hcode`` 로 교체 — 레거시 `Subu58.pas:376` `Base10.G7_Ggeo.Locate('Gcode', Hcode)` 패턴 + 형제 화면 `SQL_LEDGER_MASTER`/`list_returns` in_clause_lookup 패턴과 1:1 (SOLID-D, SOLID-O — 단일 진실 원천 G7_Ggeo, 신규 패턴 0). 회귀 가드: `test/test_returns_period_ledger_regression.py` 4/4 PASS — 4축(G7_Ggeo join + g.Hcode='' 정적 부재 + count_grouped 호출 + execute_query derived 0 + period_report_query hname 채워짐). 인접 가드 `test_list_count_grouped_mysql3.py` 11/11 + `test_in_clause_lookup_chunked.py` 17/17 무회귀 = 32/32. 신규 회귀 가드 일반화 정신 — 형제 LIST 함수에 derived 패턴 잔존 시 동일 가드 추가.
  - (d+) **(2026-04-22 보강 — 청구서관리 500 핫픽스)** LIST/상세 SELECT 절에 **인라인 스칼라/상관 서브쿼리** ``(SELECT … FROM …) AS X`` 를 작성하는 것도 동일하게 금지한다. MySQL 3.23 은 4.1 이전이라 SELECT 절 서브쿼리(스칼라/상관/IN/EXISTS) 자체를 파싱 단계에서 거절하여 1064 → HTTP 500 이 동일 재발한다. 사례: `settlement_service._SQL_LIST_BILLING` SELECT 에 인라인된 ``(SELECT COUNT(*) FROM T3_Ssub d WHERE d.Hcode=t.Hcode AND LEFT(d.Gdate,6)=t.Gdate) AS LineCnt`` 가 mysql3 서버(예: `remote_154`/`remote_155`) 에서 청구서관리 화면 빈손 「조회」 시 500 발생. 채택: 인라인 서브쿼리를 별도 함수(`_fetch_billing_line_counts`) + (e) 의 `in_clause_lookup` 청크 기반 GROUP BY 일괄 lookup 으로 분리하고 Python 측에서 `(gdate(YYYYMM), hcode) → LineCnt` 머지(SOLID-O — 신규 패턴 도입 0, 기존 transactions/reports 의 fetch+merge 컨벤션 1:1 재사용). 신규 SQL `_SQL_BILLING_LINE_COUNTS = "SELECT Hcode, LEFT(Gdate, 6) AS Gdm, COUNT(*) AS LineCnt FROM T3_Ssub WHERE Hcode IN ({placeholders}) GROUP BY Hcode, LEFT(Gdate, 6)"` 는 mysql3 호환 함수(LEFT/COUNT/GROUP BY) 만 사용. 회귀 가드: `test/test_c5_settlement_optional_filters.py::BillingMysql3CompatTests` 3축 — (i) `_SQL_LIST_BILLING` 문자열에 ``(SELECT`` 부재 보장, (ii) `list_billing` 이 헬퍼 결과를 `total_lines` 로 정확히 머지, (iii) 라우터 200 round-trip. 동일 가드는 settlement 외 모든 서비스 `_SQL_LIST_*` 에도 적용 — 신규 LIST SQL 추가 시 review 체크리스트.
  - (e) **(2026-04-21 보강 — POC 효율성 일반화)** 마스터 lookup(거래처/출판사/도서/벤더 — `G1_Ggeo`/`G7_Ggeo`/`G4_Book`/`G2_Ggwo`)에서 `WHERE Gcode IN (…)` 단발 거대 쿼리는 **금지**한다. POC `seak80-sample` 의 `_SOBO67_GNAME_CODES_CHUNK = 400` 정책을 일반화한 `app.core.sql_mysql3.in_clause_lookup(server_id, sql_template, keys, prefix_params, chunk_size)` 헬퍼만 사용해 자동 청크 분할 + dedupe + prefix_params 처리한다 (mysql3 raw socket SQL 파싱 stall / read_timeout 회귀 차단). 적용 9곳: `transactions_service._fetch_customer_names/_fetch_product_names`, `inbound_service._fetch_publisher_names/_fetch_vendor_names/_fetch_product_names`, `outbound_service._fetch_customer_names/_fetch_product_names`, `inventory_service.get_inventory_ledger` 인라인 lookup, `reports_service.get_book_sales/get_customer_sales` 인라인 lookup, `returns_service.list_returns/get_daily_summary` publisher lookup. 회귀 가드: `test/test_in_clause_lookup_chunked.py`.
  - (g) **(2026-04-21 보강 — 재고관리 메뉴 표준 페이지네이션 + 사이드바 phase1 승격)** (f) 의 hcode/bcode 옵셔널화 + truncated 가드를 마무리한 동일 메뉴 3종(`Sobo44_inv` 재고현황 / `Sobo33_ledger` 도서수불장 / `Sobo33_1_ledger` 통합 도서수불장) 에 **DEC-024 표준 페이지네이션** 을 일관 적용한다. 백엔드 `inventory_service.get_inventory_ledger` 시그니처에 `limit/offset` 추가 — 일자(by_date) 누적 결과에 대해 `clamp_limit(default=100, ceil=2000)` + `clamp_offset` + `build_page` 를 적용해 `{rows, total, page:{limit,offset,total,has_more}, truncated}` 반환. 라우터 `routers/inventory.py` 에 `limit: int = Query(100, ge=1, le=2000)` / `offset: int = Query(0, ge=0)` 추가, `LedgerResponse` 모델에 `total: int = 0` + `page: PageMeta` 필드 추가(default factory 로 BC 보장). 통합 도서수불장은 동일 메뉴 일관성을 위해 백엔드 변경 없이 프런트만 `book_sales` API 의 기존 페이지 메타를 `DataGridPager` 로 노출(기존 `fetchAllPages` 자동 누적 → 사용자 요구 「순차적 쿼리」 로 교체). 가드 직교 원칙 — `truncated`(raw 행 LIMIT_MAX 가드) 와 `page.has_more`(누적 결과 페이지) 는 의미가 독립이므로 동시 노출 가능. 적용 백엔드: `app/routers/inventory.py`, `app/services/inventory_service.py` (+ `clamp_limit` / `clamp_offset` / `build_page` 임포트), `app/models/inquiry.py` (`LedgerResponse` 확장). 적용 프런트: `lib/inquiry-api.ts` (`inventoryApi.ledger` params + `LedgerResponse.page/total` 타입), `(app)/inventory/status/page.tsx`, `(app)/ledger/book/page.tsx`, `(app)/ledger/book-integrated/page.tsx` (모두 `DataGridPager` + `useEffect` 자동 첫 페이지 로드 + 「조회」 버튼은 페이지 0 으로 리셋, 동일한 7화면 표준 패턴 — DEC-024). 사이드바 동기화 — `lib/form-registry.ts` 의 `Sobo44_inv` / `Sobo33_ledger` / `Sobo33_1_ledger` 모두 `phase: "phase2"` → `"phase1"` 정식 승격(P2 amber 배지 → 초록 `CheckCircle2` 체크 자동 전환). 회귀 가드: `test/test_inventory_ledger_paging.py` 7/7 신규(page 메타 보장, limit/offset 슬라이싱, has_more 정확성, ceil 상한, truncated 직교성) + 기존 `test_inventory_ledger_optional.py` 9/9 + `test_book_sales_optional_hcode.py` 4/4 무회귀 = 20/20 PASS, 전체 스위트 601 PASS(이전 594 + 신규 7), 사전 환경 dfm2html 2건 외 무회귀, tsc 0 errors, YAML/JSON 무결성 OK.
  - (f+) **(2026-04-22 확장 — 발송비/입금 7화면 422/500 핫픽스로 (f) 패턴 settlement 4함수 일반화)** 사용자 보고(발송비/입금 메뉴 하위 화면 빈손 진입 시 422/500) 를 (f) 의 "필터 옵셔널화 + 경계 필수 유지" 정책으로 일반화 적용. 적용 4함수: `settlement_service.list_period_summary`(Sobo47 — hcode 옵셔널, monthFrom/monthTo 경계 필수), `settlement_service.cash_status` variant=sdate 분기(Sobo42_1 — hcode 옵셔널 fallback, month 경계 필수), `tax_invoice_service.list_tax_invoices`(Sobo49 — hcode 옵셔널, gdate(YYYYMM) 경계 필수 + 422 메시지 명확화), 신규 `settlement_service.compute_outstanding_by_customer`(미수현황 — fetchAllPages 클라이언트 누적 → 서버측 단일 집계 + truncated 가드 + `transactions_service.summarize_sales_statements_by_customer` 의 fetch+Python merge 컨벤션 1:1 재사용). mysql3 호환은 동일 패턴 `(%s = '' OR Hcode = %s)` SQL 분기 + `LIMIT %s OFFSET %s` 표준 페이저(DEC-033 (g)) 합류로 흡수 — 신규 SQL/패턴 도입 0(SOLID-O). 신규 endpoint = `GET /api/v1/settlement/outstanding` (`OutstandingItem`/`OutstandingResponse` 모델). 회귀 가드: `test/test_c5_settlement_optional_filters.py` 14/14 PASS — 5 클래스(Period/CashStatusSdate/TaxInvoice 옵셔널 + Outstanding 집계 + 5화면 페이저 round-trip) + `test/test_c5_settlement_phase1.py::test_p1_12_period_summary_validation` 정책 동기화(hcode 누락 200, 경계 누락 422). 계약: `migration/contracts/settlement_billing.yaml` v1.2.0 → v1.3.0(hcode optional + outstanding endpoint + truncated 응답), `migration/test-cases/settlement_billing.json` 5 케이스. 프런트: 5 list 화면(billing/cash/cash-status/tax-invoice/outstanding) `useListSession`(DEC-055) + `DataGridPager` + `useDynamicPageSize` 합류, period/payment-slip 은 useListSession 만(소량 의도 유지). probe 매트릭스 `settlement.outstanding` 그룹 추가.
  - (f) **(2026-04-21 보강 — 조회형 화면 필수값 옵셔널화 + 풀스캔 가드)** 조회형 화면(재고관리 메뉴 3종 — `Sobo44_inv` 재고현황 / `Sobo33_ledger` 도서수불장 / `Sobo33_1_ledger` 통합 도서수불장 — 및 모바일웹 「재고현황」 통합 카드) 의 `hcode`/`bcode` 입력은 **옵셔널**로 한다. 백엔드는 빈/None/`'%'` 입력을 `_normalize_filter` 로 None 정규화한 뒤 해당 `WHERE` 절을 SQL 본문에서 동적으로 제거해 "전체 대상" 조회를 허용한다. 풀스캔 회귀 차단을 위해 다음 가드를 의무화한다: (i) **일자 범위(`date_from`/`date_to`) 는 라우터에서 `Query(...)` 필수 유지**(mysql3 stall 회피 1차 방벽), (ii) **서버측 결과 상한 LIMIT** — `inventory_service.LEDGER_MAX`(env `BLS_INVENTORY_LEDGER_MAX`, 기본 5,000행) + 1 로 SELECT 후 `truncated` 플래그 동봉, `LedgerResponse.truncated: bool` 응답 필드로 클라이언트에 노출, (iii) **도서명 lookup 은 (e) 의 `in_clause_lookup` 청크를 그대로 사용**하되 hcode 미입력 케이스에서는 lookup SQL 의 `Hcode=%s` 도 동적으로 제거(`prefix_params=()`). 적용 백엔드: `routers/inventory.py::get_inventory_ledger`, `services/inventory_service.py::get_inventory_ledger` (+ `_opening_sql` / `_ledger_main_sql` / `_normalize_filter` / `LEDGER_MAX`), `routers/reports.py::get_book_sales`, `services/reports_service.py::get_book_sales` (SQL-INQ-7/8 양쪽 절 동적 제거). 적용 프런트: `(app)/inventory/status/page.tsx`, `(app)/ledger/book/page.tsx`(기존 `hcode='%'` 트릭 제거 — 정확 일치 SQL 에서 사실상 0행이던 잠재 버그 동시 정리), `(app)/ledger/book-integrated/page.tsx`, `lib/inquiry-api.ts` (`inventoryApi.ledger` / `reportsApi.bookSales` params 옵셔널 + `LedgerResponse.truncated`). 계약: `migration/contracts/sales_inquiry.yaml` `ledger_filter` / `reports_filter` / endpoint 시그니처 + `ledger_rows.flags.truncated` 동기화. 회귀 가드: `test/test_inventory_ledger_optional.py`(9/9), `test/test_book_sales_optional_hcode.py`(4/4) + 기존 `test/test_in_clause_lookup_chunked.py`(17/17) / `test/test_list_count_grouped_mysql3.py`(11/11) 무회귀. 부산물 — `test/conftest.py` 신설(autouse 픽스처 `_ensure_default_event_loop`): `IsolatedAsyncioTestCase` 가 알파벳 순으로 더 앞쪽 파일에 등장하기 시작하면(신규 `test_book_sales_*.py` 등) 후속 일반 테스트의 `asyncio.get_event_loop().run_until_complete(...)` 호출(`test_c2/c3/c4` 서비스 단위 회귀)이 `RuntimeError: There is no current event loop` 로 무더기 깨지는 격리 회귀를 일반 정책으로 차단(향후 모든 `IsolatedAsyncioTestCase` 추가 시 동일 가드 자동 적용 — DEC-033 §회귀 가드 일반화 정신을 테스트 인프라로 확장).
- **배경/근거**: 2026-04 C5 정산 회귀 — `remote_138` 에서 `T5_Ssub` 에 `Sdate` 등 누락, `remote_154`/`remote_155` 에서 `LIMIT … OFFSET …` 문법·현대 SQL 표현 불가. 동일 종류 재발 방지.
- **DoD**: 4대 서버 각각 L2 `SELECT 1` 성공 + L4 GET 매트릭스 전부 OK(빈 목록 200 허용). 예외는 `migration/contracts/… customer_variants` 또는 본 DEC에 명시된 경우만.
- **운영**: `.cursor/rules/multi-db-compat.mdc` 로 alwaysApply; `docs/db-smoke-runbook.md` 절차 준수; 쓰기 경로 mysql3 호환은 별도 스테이징에서 검증.
- **결정자**: 메인개발자 + 사용자 (멀티 DB API 연동 점검 계획 반영)
- **참조**: `도서물류관리프로그램/backend/app/core/sql_mysql3.py`, `도서물류관리프로그램/backend/app/services/t5_ssub_adapt.py`, `debug/probe_backend_all_servers.py`, `docs/db-smoke-runbook.md`, `.github/workflows/db-smoke.yml`

### DEC-051: 인증 서버 단일화 — `BLS_AUTH_SERVER_ID` 게이트
- **일자**: 2026-04-21 — **(2026-04-26 DSN-DEC-08 정합)** 본문 (b)(c) 및 비밀 검증 위치 서술 갱신.
- **결정 사항**: 로그인 **엔드포인트·게이트**는 단일(`POST /api/v1/auth/login`)이며, 사용자가 UI에서 데이터 서버를 고르지 않는다. **비밀번호 검증(DSN-DEC-08)** 은 `tenants_directory_service.resolve_login_route_candidates` 가 만든 `(remote_id, db_name)` 후보를 순서대로 시도할 때, 각 후보에 대해 `authenticate_user(server_id, …, db_name=…)` 가 해당 서버의 ``Id_Logn``(레거시 자격)에서 수행된다. 환경변수 `BLS_AUTH_SERVER_ID`(기본 `remote_138`)는 **감사 로그·폴백 후보** 등 보조 용도이며, “모든 사용자 비밀을 `BLS_AUTH_SERVER_ID` 의 `web_users` 한 곳에서만 검증”한다는 초기 서술은 **폐기**한다(운영 코드·`docs/login-routing-regression-guard.md` 기준).
  - (a) 로그인 화면(`(public)/login/page.tsx`) 의 「DB 서버 선택」 콤보·`useEffect(/api/v1/servers)` 호출은 제거된다.
  - (b) `POST /api/v1/auth/login` 의 `serverId` 입력값은 **무시**되며(BC 위해 필드는 deprecated 로 유지). 라우터는 메타·인덱스가 고른 **후보별** `authenticate_user(sid, …)` 를 호출한다 — `sid` 를 항상 `BLS_AUTH_SERVER_ID` 로 고정 호출하지 않는다.
  - (c) JWT `sid` 클레임은 **비밀 검증에 성공한 후보의 데이터 서버**(`remote_id`)로 채워진다. DEC-052 의 Primary(`web_user_servers`)는 admin·소속 정책용이며, 로그인 성공 시점의 `sid` 와 항상 동일하다고 가정하지 않는다.
- **배경/근거**: 운영상 `web_users` 시드는 `remote_138` 한 곳에 통합되어 있고, 기존 다중 콤보 UI 는 (1) 잘못된 서버 선택 시 401, (2) 인증 서버와 데이터 서버 의미를 사용자에게 떠넘기는 혼란을 일으킨다. 레거시 `Sobo10` 도 부팅 환경 1개 DB 만 본다. 이후 통합 로그인(DSN-DEC-08)으로 멀티 테넌트·`Id_Logn` 검증 경로가 추가되었다.
- **DoD**: `serverId` 미전송 로그인 200 + JWT `sid` = **검증 성공 데이터 서버** + 회귀 `test_auth_login_fixed_server.py` 전건 PASS + 4대 서버 L4 GET 매트릭스(DEC-033) 무회귀.
- **운영**: `.env`/실행 안내에 `BLS_AUTH_SERVER_ID=remote_138` 를 명시. 인증 서버를 다른 곳으로 옮길 때는 본 키만 변경. 데이터 서버 추가/삭제는 자격증명 동기화 없이 가능.
- **결정자**: 메인개발자 + 사용자 (로그인 서버 선택 UI 제거 합의)
- **참조**: `도서물류관리프로그램/backend/app/routers/auth.py`, `도서물류관리프로그램/backend/app/services/auth_service.py`, `docs/login-routing-regression-guard.md`, `도서물류관리프로그램/frontend/src/app/(public)/login/page.tsx`, `도서물류관리프로그램/frontend/src/contexts/auth-context.tsx`, `test/test_auth_login_fixed_server.py`, DEC-052

### DEC-052: 사용자별 데이터 서버 1:1 (Primary)
- **일자**: 2026-04-21
- **결정 사항**: `web_user_servers` 의 의미를 **다대다 → 1대1(Primary)** 로 좁힌다. 한 사용자(`user_id`) 는 0~1 row 만 가진다.
  - (a) admin UI([(app)/admin/user-servers/page.tsx](../도서물류관리프로그램/frontend/src/app/(app)/admin/user-servers/page.tsx)) 는 다중 토글 → **라디오 1개 선택(Primary)** 으로 교체. `adminApi.setPrimaryServer(userId, serverId|null)` 신설.
  - (b) `admin_service.assign_server(allow=True)` 호출 시 동일 `user_id` 의 기존 row 를 모두 제거 후 1건 INSERT (LSP 보존: 시그니처 유지, 의미만 좁힘). `set_primary_data_server(user_id, server_id, actor)` / `get_primary_data_server(login_id) -> str|None` 신규 함수.
  - (c) `_load_state()` 직후 `_normalize_primary_servers()` 로 **부팅 1회 idempotent 마이그레이션** 실행 — 동일 user_id 가 2건 이상이면 마지막 created 만 유지하고 나머지는 audit `user.server.dedup` 로 기록.
  - (d) **(2026-04-26 DSN-DEC-08 정합)** `/api/v1/auth/login` 성공 시 JWT `sid` 는 `get_primary_data_server(user_id)` 가 아니라 **비밀 검증에 성공한 후보의 `remote_id`** 로 설정된다(`auth.py` — 후보 순회·`hit_candidate`). Primary 매핑은 admin UI·헤더 경고 등 **소속/운영 정책**에 계속 사용된다.
- **배경/근거**: 다중 매핑은 「로그인 서버 선택 콤보」 와 1:1 대응될 때만 의미 있는데, DEC-051 로 콤보가 사라지면 사용자가 어느 서버로 작업할지 자체적으로 결정할 수 없다. 운영자 1인이 admin 화면에서 명시적으로 1개 서버를 부여하는 정책이 안전하고 단순하다.
- **DoD**: 동일 user 다중 row → 1건 정리 audit 발생 + admin 라디오 UI 단일 선택 강제 + 회귀 `test_admin_primary_server.py` PASS + 사용자 헤더에 미설정 경고 배지 노출.
- **운영**: 데이터 모델 컬럼명은 변경하지 않는다(BC). 기존 자동화 스크립트가 동일 사용자에게 다중 row 를 기록해도 다음 부팅 시 1건으로 정리된다.
- **결정자**: 메인개발자 + 사용자 (1 사용자 1 데이터 서버 정책 합의)
- **참조**: `도서물류관리프로그램/backend/app/services/admin_service.py`, `도서물류관리프로그램/backend/data/web_admin.json`, `도서물류관리프로그램/frontend/src/app/(app)/admin/user-servers/page.tsx`, `도서물류관리프로그램/frontend/src/components/app-shell/header.tsx`, `test/test_admin_primary_server.py`, DEC-051

### DEC-053: 1차 포팅 화면 컴포넌트 동등성 정기 재점검 (Phase 1 Component Fidelity Audit)
- **일자**: 2026-04-21
- **결정 사항**: `form-registry.ts` 의 모든 `phase: "phase1"` 폼(현 33행) 은 `analysis/audit/phase1-component-fidelity.md` 단일 매트릭스에 5 축(W/B/U/D/O) PASS/OOS 평가를 보유한다. **phase1 승격 게이트** (DEC-045) 는 본 매트릭스의 `GAP-P0 = 0` 을 의무화한다 — P0 1건이라도 있으면 phase1 승격을 차단한다.
  - (a) **5 축**: W(Widget — dfm 위젯 누락) / B(Business logic — OnXxx·SQL) / U(User flow — TabOrder·단축키·토글·라디오) / D(Data — 컬럼·집계·필터 기본값) / O(Out-of-scope — 의식적 비포함). 각 축은 한 단어: PASS / GAP-P0 / GAP-P1 / GAP-P2 / OOS.
  - (b) **P0 정의**: 사용자 작업이 차단되는 항목 (예: 본사/창고 토글 부재로 데이터가 비어 보임 — 본 사이클 직전 Sobo67 핫픽스 사례).
  - (c) **단일 원천**: 위젯 표·이벤트 매핑·인쇄 절은 `analysis/layout_mappings/<Sobo*>.md` 단일 원천 — 본 매트릭스는 5축 한 단어 + 매핑 노트 링크만 보유. 매핑 노트 변경 시 본 매트릭스를 동시 갱신한다.
  - (d) **재실행 트리거**: 신규 DEC, 백엔드/프런트 변경, 사용자 보고로 인한 5축 의미 변경 시 audit_only 사이클로 매트릭스 재실행.
  - (e) **HA-RET-02**: P0/P1 발견 시 `dashboard/data/human-action-items.json::HA-RET-02` 에 항목 등록 후 별 사이클(retrofit) 로 처리. 본 사이클 자체는 코드 변경 0.
- **배경/근거**: Sobo67 본사/창고 토글 부재로 출고현황 화면이 비어 보이는 P0 가 phase2 포팅 후 사용자 보고로 발견됨 → DEC-019 변형 통합 정책과 dfm 의 의식적 OOS 구분 가이드가 부족했음. 폼 단위 5축 평가를 phase1 승격 게이트에 묶어 동일 회귀 재발을 결정적으로 차단한다.
- **DoD**: `analysis/audit/phase1-component-fidelity.md` 매트릭스 33 행 GAP-P0 합계 = 0 + DEC-028 §결정 1줄 보강 + `.cursor/rules/dfm-layout-input.mdc` §회귀 가드 1줄 추가. 코드 변경 0.
- **운영**: 본 사이클 결과 P0 = 0 / P1 = 0 / P2 = 15(모두 의식적 deltas). HA-RET-02 ID 예약 + 항목 = 0.
  - **(2026-04-21 보강 — phase1 정식 승격 1건)** `Sobo67_status`(출고현황, `/outbound/status`) 가 본사/창고/전체 토글 복원(DEC-051/052) + `count_grouped` 서버 집계(DEC-033 d) + `in_clause_lookup` 청크 마스터 룩업(DEC-033 e) 5축 모두 PASS 로 phase1 정식 승격(`form-registry.ts::Sobo67_status.phase = "phase1"`). 사이드바 P2 amber 배지 → `CheckCircle2` 초록 체크로 마무리. 매트릭스 §2.1 합계는 본 사이클 동결(33행) 유지 — **34행 정식 편입은 다음 audit 사이클에서 처리** (사례는 §2.3 phase1 정식 승격 1건 기록). `dashboard/data/phase2-screen-cards.json` Sobo67_status 카드 T8=done(다음 사이클 phase2 카드에서 제거 예정).
- **결정자**: 메인개발자 + 사용자 (1차 폼 컴포넌트 누락 0 가드 합의)
- **참조**: `analysis/audit/phase1-component-fidelity.md`, `.cursor/rules/dfm-layout-input.mdc`, DEC-028(공식 입력) + DEC-045(phase1 승격 게이트) + GR-CODE-001 (고객사 분기 보존) + GR-PROC-004 (capture 없는 동등성 주장 금지)

### DEC-054: 레거시 포팅 누락 자동 탐지 (Legacy Coverage Audit)
- **일자**: 2026-04-21
- **결정 사항**: `legacy_source/*.dfm` 의 root form Caption 인벤토리(=사용자 진입 가능 화면 후보의 단일 진실 원천) 와 프런트 `form-registry.ts` (`FORM_REGISTRY`) 의 정합을 매 사이클 자동 검증한다. `tools/audit_legacy_coverage.py` 가 4 카테고리(missing/caption_mismatch/allowed/ok) 로 분류하여 `analysis/audit/legacy-coverage-report.json` 을 산출하며, `--check` CLI 가 신규 위반 시 non-zero exit 한다. `test/test_legacy_coverage_audit.py` 가 pytest 게이트로 매 회귀 사이클에서 신규 위반 0 을 의무화한다.
  - (a) **단일 진실 원천**: `legacy_source/<name>.dfm` 직속 (서브디렉토리 Interbase/Data/version 등은 백업·대체 구현이라 후보에서 자동 제외 → 동일 form_name 다중 caption 충돌 회피).
  - (b) **registry ↔ DFM 매핑 우선순위**: ① `scenario.legacy_form` 명시 ② `id` 정확 일치 ③ `id` 의 base prefix(`Sobo67_status` → `Sobo67`). DFM ↔ registry 양방향 surface 로 Sobo67 사례(DFM Caption='도서별년말집계' vs registry caption='출고현황') 같은 라벨 붕괴를 자동 검출.
  - (c) **baseline 부채 명시화**: 도입 시점 `missing_forms` 75건 + `caption_mismatches` 34건 을 `legacy-analysis/coverage-allowlist.yaml` 에 `reason`+`until` 필수로 등록. 신규 위반(allowlist 외) 만 pytest FAIL — 의도된 부채 vs 신규 회귀 분리 (사용자 룰: 임시방편 금지 / 근본 원인 명시).
  - (d) **의도된 신규 포팅 deferral**: `Sobo67_yearbook` 같이 registry id 만 존재하고 DFM form_name 으로는 미존재하는 신규 포팅 화면은 별도 `intentional_new_forms` 섹션에 surface (audit 카테고리 영향 0, 문서화 목적).
  - (e) **운영 룰**:
    - 신규 포팅 화면 등록 시 — `python3 tools/audit_legacy_coverage.py --check` 로컬 실행 → MISSING 자동 제거 확인.
    - 신규 위반 발생 시 — pytest FAIL → (i) 진짜 누락이면 포팅 plan 수립, (ii) 의도된 deferral 이면 `coverage-allowlist.yaml` 에 reason+until 필수 추가 + PR 리뷰.
    - 분기 정기 점검 — `until` 만료 항목 일괄 재분류.
  - (f) **DFM 파서 보강**: `tools/parsers/dfm_parser.py::parse_dfm_file` 가 root form 의 `Caption` 속성을 `form_inventory.json` 의 옵셔널 `caption` 필드로 surface (기존 `LAYOUT_EXPORT_KEYS` 가 이미 추출, 1줄 보강 — 기존 사용자 영향 0). 173 폼 → caption 보유 163 폼 (10 폼은 TDataModule/Base 류 = 사용자 진입 불가 → 자동 제외).
- **배경/근거**: 사용자 보고 — "레거시 도서별년말집계 화면이 포팅되어 있나?" 직접 원인 추적 결과 `Subu67.dfm Caption='도서별년말집계'` 를 `form-registry::Sobo67_status` 가 잘못된 의미("출고현황") 로 라벨링하고 있었음(DEC-033 (k+1)). 단순 사례 핫픽스가 아닌 회귀 가드로 일반화하지 않으면 동일 라벨 붕괴가 다른 175 폼에서 재발할 수 있음 → 영구 회귀 가드(plan §6 P2/P3/P4 후속 별도) 도입.
- **DoD**: ① `python3 tools/audit_legacy_coverage.py --check` exit 0 ② `pytest test/test_legacy_coverage_audit.py` 13/13 PASS ③ ReadLints 0 ④ baseline allowlist 109건 등록 ⑤ 의도적 위반 주입 시 FAIL 재현 검증.
- **운영**: 본 사이클 결과 missing=0 mismatch=0 ok=23 allowed=109 (baseline). Sobo67_status 가 baseline allowed (category=caption_mismatch) 에 surface 되어 가드 살아있음 스모크 통과.
- **결정자**: 메인개발자 + 사용자 (레거시 화면 누락 회귀 가드 도입 합의)
- **참조**: `tools/audit_legacy_coverage.py`, `tools/parsers/dfm_parser.py`, `legacy-analysis/coverage-allowlist.yaml`, `analysis/audit/legacy-coverage-report.json`, `test/test_legacy_coverage_audit.py`, DEC-033 (k+1) (사례 발단), DEC-053 (5축 audit 와 직교 — 본 가드는 IA 정합 / DEC-053 은 컴포넌트 동등성)

### DEC-055: list 화면 상태 보존 — sessionStorage 일반화 + 회귀 가드
- **일자**: 2026-04-22
- **결정 사항**: `DataGridPager` 를 사용하는 모든 list 화면(17건) 의 검색조건·페이지·offset 을 단일 hook(`useListSession`, `frontend/src/lib/use-list-session.ts`) 으로 sessionStorage 영속화하여 detail 진입 후 복귀 시 직전 위치 복원을 보장한다. 신규 list 화면 누락은 `tools/audit_list_state_persistence.py` 정적 grep 가드 + `test/test_list_state_persistence_audit.py` pytest 게이트로 매 사이클 자동 차단한다 (DEC-054 패턴 재사용 — discover/allowlist/`--check` CLI/JSON report 동일 골격).
  - (a) **단일 hook**: `useListSession<T>(key, defaults, opts?)` — SSR-safe(첫 render defaults 반환 → `useEffect` 에서 storage 읽고 `setState`+`hydrated=true`) + TTL 30분(cross-day 누적 방지) + JSON 직렬화 + `listSessionKeyFromPathname` 헬퍼(라우트 path 기준 키 자동 생성, 충돌 방지). 저장 매체 = sessionStorage 단일(URL 깨끗 + 새로고침 OK + 새 탭 휘발 — 사용자 선택).
  - (b) **page.tsx 통합 패턴**: 각 화면별 `Snap` 인터페이스 정의(filters + offset/limit) → `snap.value` 로 `useState` 초기값 시드 → `load`/`fetchData` 에 `LoadOverrides`/`FetchOverrides` 옵셔널 파라미터 추가 → hydration `useEffect` 가 (i) 복원된 값으로 개별 state 세팅 (ii) `overrides` 로 즉시 load 호출 (iii) `bootDone=true` (iv) `dyn.recommended` reload `useEffect` 는 `!bootDone || snap.limit > 0` 가드. `useCallback` 묶인 `fetchData` 는 dep 배열에 `setSnap` 포함 — 복원된 페이지 위치를 자동 reset 으로 덮어쓰지 않도록 사용자 의도 우선.
  - (c) **회귀 가드**: `tools/audit_list_state_persistence.py` 가 `frontend/src/app/(app)/**/page.tsx` 73건을 스캔 → `DataGridPager` 사용 + `@/lib/use-list-session` import 둘 다 있어야 covered. 위반 시 `legacy-analysis/list-state-allowlist.yaml::deferred_pages` 에 `route_key`+`reason`+`until` 필수 등록(의도적 deferral 분리). `--check` exit code + pytest 9 케이스(violations 0 / 17쪽 baseline 커버리지 / CLI smoke / stale allowlist 0 등) 로 매 사이클 강제.
  - (d) **detail→back 일원화 미필요**: `<Link>`/`router.push`/`router.back()` 어떤 복귀 방식이든 sessionStorage 키 기반 복원이 동작 — 기존 detail 페이지 무접촉(SOLID-O — 신규 패턴 0).
  - (e) **운영 룰**:
    - 신규 list 화면 추가 시 — `DataGridPager` 도입과 동시에 `useListSession` 의무. `python3 tools/audit_list_state_persistence.py --check` 로 자동 검출.
    - sessionStorage 키 = `listSessionKeyFromPathname(usePathname())` 또는 명시적 dot-키("master.customer", "outbound.orders" …) — 수동 명명 시 `bls.list.` prefix 자동 부여(충돌 방지).
    - TTL 30분 — 더 길게 보존이 필요한 화면(예: 정산 마감) 은 caller 가 `opts.ttlMs` 명시.
    - 의도적 비적용(예: 단발 dialog 류) 발견 시 — `list-state-allowlist.yaml` 에 reason+until 등록 + PR 리뷰.
- **배경/근거**: 사용자 보고 — "모든 화면에 대해서 상세 화면으로 진입한 후 다시 이전 화면으로 돌아올때 이전 위치를 캐싱하지 않아서 재검색하거나 페이징 위치를 다시 검색이후 다시 이동해야 한다." 탐사 결과 17개 list 화면(`DataGridPager` 사용) 모두 검색조건·page·offset 을 부모 `useState` 만으로 관리 → detail 복귀 시 휘발. `useDynamicPageSize` 가 page 사이즈만 `localStorage` 보관 — page offset/필터 보존 없음. detail→back 처리 혼재(`<Link>`/`router.push`/`router.back()`) 도 sessionStorage 복원으로 통일 가능. `useFormStore` (MDI 탭 전용, persist 미적용) 는 list 상태에 부적합 → 신규 단일 hook 도입(SOLID-S/O).
- **DoD**: ① `cd 도서물류관리프로그램/frontend && npm run typecheck` exit 0 ② `python3 tools/audit_list_state_persistence.py --check` exit 0 (17/17 covered, violations 0) ③ `python3 -m pytest test/test_list_state_persistence_audit.py` 9/9 PASS ④ ReadLints 0 ⑤ 전체 `pytest test/` 회귀 0(2 사전 환경 dfm2html/res_string 무관) ⑥ 수동 3축 시나리오 검증(master/customer + outbound/orders + reports/year-end-book — 검색조건·페이지·드릴다운 모두 복원).
- **운영**: 본 사이클 결과 — pages=73 covered=17 violations=0 allowed=0 skipped=56(detail/dialog/CRUD 등 list 가 아닌 페이지). list-state-allowlist.yaml `deferred_pages: []` (전 화면 도입 완료 — 부채 0).
- **결정자**: 메인개발자 + 사용자 (list 상태 보존 일반화 + 회귀 가드 도입 합의)
- **참조**: `frontend/src/lib/use-list-session.ts`, `tools/audit_list_state_persistence.py`, `legacy-analysis/list-state-allowlist.yaml`, `analysis/audit/list-state-coverage-report.json`, `test/test_list_state_persistence_audit.py`, DEC-054 (정적 audit 패턴 reuse 원천)

### DEC-056: Id_Logn Fxx 어댑터 — 레거시 권한 매트릭스 → 모던 RBAC 합류

- **결정 사항**: 레거시 `Id_Logn` 의 `F11~F89` 80셀(`'O'`/`'R'`/`'X'`/`' '`) 매트릭스를 **신규 SQL 0건** 정책으로 그대로 SELECT 한 뒤 `legacy_permission_map` 카탈로그(52건 정본)와 합성해 `(role, permissions)` 를 산출한다(Wave A 어댑터). 구현 산출:
  - (a) `LegacyIdLognProvider.fetch_fxx_matrix(server_id, user_id) -> dict[str,str]` 신설 — 기존 Chul.pas L441 `SELECT * FROM Id_Logn WHERE gcode = %s LIMIT 1` 패턴 재사용, F11~F89 80셀을 `_safe_str` + `.strip().upper()` 정규화 + Euc-KR bytes 디코딩 폴백.
  - (b) `auth_service._resolve_role_and_permissions_async(user_id, hcode, server_id)` 신설 — *기존 동기* `_resolve_role_and_permissions(user_id, hcode)` 시그니처는 그대로 유지(LSP 보존, `test_c10_admin_phase1::test_P_01..05` 무회귀). 신규 비동기 함수가 분기 1·2(슈퍼유저/whitelist) → **분기 3 = Id_Logn Fxx 합성** → 분기 4·5·6(기존 동기 함수 위임) 으로 합류.
  - (c) `_load_legacy_permission_index()` 캐시 — `admin_service.list_legacy_permission_map()` 1회 호출로 `{Fxx: permission_code}` 인덱스 캐시.
  - (d) `_merge_fxx_to_permissions(fxx, catalog)` — `'O'` 셀은 카탈로그 매핑된 권한 그대로, `'R'` 셀 + `*.write` 매핑은 `*.read` 페어로 자동 변환(레거시 read-only 의미 회복).
  - (e) `authenticate_user` 라우팅 1줄 변경: `_resolve_role_and_permissions(...)` → `await _resolve_role_and_permissions_async(..., server_id)`. 그 외 호출부 무변동.
  - (f) `web_admin.json::legacy_permission_map` + `admin_service._DEFAULT_LEGACY_PERMISSION_MAP` 시드를 카탈로그 §1+§4 의 **52 정본 키 전체**로 일괄 확장 (이전 3건 → 52건). `_empty_state()` 가 신규 환경에 동일 시드 보장.
  - (g) `bootstrap_admin_id_logn.py` 의 `--hcode` argparse 기본값 `'00000'`(5자리) → `'0000'`(4자리, `auth_service` 슈퍼유저 분기와 정합) — `BLS_ADMIN_HCODE` env 폴백도 동일.
- **배경/근거**: (1) 레거시 `Base10.Seek_Uses('Fxx')` 80개 호출의 SSOT 인 `Id_Logn` Fxx 셀이 모던 시드(3/30 → 0건 활용) 와 분리되어 있어 admin/admin123 부트스트랩 결과가 *전 도메인 403* 회귀를 일으킴(diagnostic 표 시나리오 (A)). (2) 다중 분기를 동기 함수에 일괄 추가하면 `_resolve_role_and_permissions` 동기 시그니처를 깨뜨려 `test_P_01..05` 5건 + `admin_service` 인접 호출 회귀 → SOLID-L 위반. → 신규 *비동기* 함수를 옆에 두고 동기 함수는 폴백 위임으로만 사용해 LSP 보존. (3) 카탈로그 R 페어(예: `outbound.write` 의 read 페어) 는 `*.write` 명명 규약 위에서 자동 합성 가능 → 카탈로그 행 추가 0(SOLID-O).
- **수용 기준 (DoD)**:
  - ① `python3 -m pytest test/test_id_logn_fxx_matrix.py` 7/7 PASS (빈 행/단일 행/blank·None drop/소문자 정규화/EucKR bytes 디코딩/Saml·Oidc fallback/예외 전파).
  - ② `python3 -m pytest test/test_auth_resolve_async_with_id_logn.py` 7/7 PASS (분기 1~6 + R/W 페어 합성 + LSP 동기 시그니처 무변동 정적 가드).
  - ③ `python3 -m pytest test/test_bootstrap_admin_default_hcode_4digit.py` 1/1 PASS.
  - ④ `python3 -m pytest test/test_legacy_permission_map_full_seed.py` 3/3 PASS (web_admin.json ↔ catalog 52건 일치, admin_service ↔ web_admin.json 정합, fkey/permission_code 중복 0).
  - ⑤ 인접 회귀: `test_c10_admin_phase1.py` PASS(LSP 보존), `test_admin_primary_server.py` PASS, `test_auth_login_fixed_server.py` PASS, `test_c1_login_phase1.py` PASS.
  - ⑥ tsc 0 + ReadLints 0 (changed files only).
- **위험 / 보완**:
  - (i) 운영 admin 행 hcode 가 5자리(`'00000'`) 로 저장된 환경 → M0 적용 후에도 분기 1 미인식. 안내: `UPDATE Id_Logn SET hcode='0000' WHERE gcode='admin' AND hcode='00000';` 또는 `BLS_ADMIN_USER_IDS=admin` env 우회.
  - (ii) Saml/Oidc provider 가 `fetch_fxx_matrix` 미구현 → `hasattr` 체크로 안전 폴백, NotImplementedError 미발생.
  - (iii) `Id_Logn` SELECT 의 mysql3 unicode 디코딩 실패 → 기존 `_safe_str` + Euc-KR bytes 폴백 패턴 재사용으로 흡수.
  - (iv) 카탈로그 미등록 Fxx 셀(예: Interbase F61~F89 일부) → drop + `logger.info` (catalog §1 마지막 행 정책 그대로).
- **결정자**: 메인개발자 + 사용자 (DEC-056·DEC-058 즉시 적용 명시 합의 2026-04-22)
- **참조**: `도서물류관리프로그램/backend/app/core/auth_provider.py` (`fetch_fxx_matrix`), `도서물류관리프로그램/backend/app/services/auth_service.py` (`_resolve_role_and_permissions_async`/`_load_legacy_permission_index`/`_merge_fxx_to_permissions`), `도서물류관리프로그램/backend/app/services/admin_service.py` (`_DEFAULT_LEGACY_PERMISSION_MAP`), `도서물류관리프로그램/backend/data/web_admin.json` (`legacy_permission_map` 52), `debug/bootstrap_admin_id_logn.py`, `legacy-analysis/permission-keys-catalog.md` §1+§4, `docs/user-permission-management-plan.md` §5 M0/M1/M5, `test/test_id_logn_fxx_matrix.py`, `test/test_auth_resolve_async_with_id_logn.py`, `test/test_bootstrap_admin_default_hcode_4digit.py`, `test/test_legacy_permission_map_full_seed.py`, DEC-007(슈퍼유저 분기 폐지 — 본 결정으로 부분 회복), DEC-020(legacy_permission_map), DEC-041(RBAC 정공법), DEC-043(IdP/SSO 인터페이스 분리), DEC-047(BLS_DEFAULT_ROLE 폴백), DEC-058(사이드바 게이팅 — 본 결정의 클라이언트 사이드 짝)

### DEC-056 보강 (2026-04-22 두 번째 사이클): admin 슈퍼유저 3중 안전망

- **결정 사항**: `admin` / `admin123` 계정이 *어떤 환경에서도* 슈퍼유저(`role=admin` + `permissions=['*']`) 로 인식되도록 **3중 안전망** 적용. 어느 한 경로가 실패해도 다른 경로로 자동 폴백.
  - **#1 (기존 — DEC-056 본문)**: `Id_Logn.hcode == '0000'` 4자리 정합 (M0 부트스트랩 + 분기 1).
  - **#2 (신규)**: `auth_service._admin_whitelist_ids()` 의 정책 보강 — `BLS_ADMIN_USER_IDS` 환경변수가 *미설정*(`os.environ` 에 키 자체 없음) 이면 기본 폴백 `{'admin'}` 반환. 명시적 빈 문자열(`""`) 시 폴백 비활성(보안 격리 의도 존중), 명시 콤마 ID(`"admin,root"`) 시 그 값만 사용(운영자 의도 우선). 모듈 레벨 `_DEFAULT_ADMIN_USER_IDS: frozenset[str] = frozenset({"admin"})` 단일 정본.
  - **#3 (신규)**: `admin_service._empty_state()` 가 신규 환경 부팅 시 admin 사용자(`u-admin-default`) + `role-admin` 매핑을 자동 시드. `_ensure_admin_role_mapping()` 헬퍼가 *기존* 환경에서도 admin 사용자만 있고 매핑이 누락된 경우 idempotent 보정 (`_load_state` 의 부팅 1회 정규화 사이클에 합류). 운영자가 admin 사용자를 *의도적으로 제거* 한 환경은 자동 시드를 건너뜀(의사 존중 — `_DEFAULT_ADMIN_LOGIN_ID` 가 `web_users` 에 없으면 무동작).
  - **#3 데이터 적재**: `web_admin.json::web_user_roles` 에 기존 admin 사용자(`u-1776757269230`) → `role-admin` 매핑 1건 추가.
- **배경/근거**: 사용자 보고 — "admin 계정에는 모든 superadmin 권한을 주도록 설정해주세요". 기존 DEC-056 본문은 분기 1 (`hcode='0000'`) 에 의존했으나, 운영 admin 행이 *legacy 5자리*(`'00000'`) 로 저장된 환경 + `web_user_roles` 매핑 누락 + `BLS_ADMIN_USER_IDS` 환경변수 미설정의 3중 누적 미스 케이스에서 admin 이 빈 권한으로 폴백되는 회귀를 발견. 단일 경로 해결(예: hcode 정정 SQL) 은 운영 환경 수동 작업 필요 → 다중 방어로 *out-of-the-box* 보장.
- **수용 기준 (DoD)**:
  - ① `python3 -m pytest test/test_admin_superuser_safety_net.py` 11/11 PASS (3 클래스 — 화이트리스트 정책 3 / async 분기 2 폴백 3 / admin_service 자동 시드·보정 4 / 현재 web_admin.json 검증 1).
  - ② 기존 회귀 무영향: `test_c10_admin_phase1::test_P_01..05` PASS, `test_auth_resolve_async_with_id_logn` 7/7 PASS, `test_legacy_permission_map_full_seed` 3/3 PASS.
  - ③ ReadLints 0 (changed files only).
- **위험 / 보완**:
  - (i) 보안 우려 — admin 으로 로그인 시도가 비밀번호 검증을 *반드시* 통과해야 분기 2 에 도달. admin user_id 자체가 등록되지 않은 환경에서는 분기 2 무력화. 추가 보안 격리는 `BLS_ADMIN_USER_IDS=""` env 로 사용자가 *명시적* 비활성화 가능.
  - (ii) `_empty_state()` 의 자동 시드는 *신규 환경* 만 영향. 기존 운영 `web_admin.json` 은 `_ensure_admin_role_mapping()` 의 *idempotent 보정* 이 처리 (admin 사용자가 있으면 매핑만 추가, 없으면 무동작).
  - (iii) 다중 안전망이 admin 권한 박탈을 *불가능* 하게 만들 수 있음 → 운영자가 의도적으로 박탈하려면 (a) `BLS_ADMIN_USER_IDS=""` env 설정 + (b) Id_Logn admin 행 hcode 변경 + (c) web_admin.json 매핑 제거 *3 단계 모두* 수행. 다른 사용자가 admin 사용자 자체를 제거(`web_users` 에서 삭제)하면 (c) 는 자동 만족.
- **결정자**: 메인개발자 + 사용자 (2026-04-22 두 번째 사이클 — "admin 계정에는 모든 superadmin 권한을 주도록 설정해주세요" 명시 합의)
- **참조**: `도서물류관리프로그램/backend/app/services/auth_service.py` (`_DEFAULT_ADMIN_USER_IDS`/`_admin_whitelist_ids`), `도서물류관리프로그램/backend/app/services/admin_service.py` (`_DEFAULT_ADMIN_USER_ID`/`_DEFAULT_ADMIN_LOGIN_ID`/`_empty_state`/`_ensure_admin_role_mapping`/`_load_state`), `도서물류관리프로그램/backend/data/web_admin.json` (`web_user_roles` admin → role-admin), `test/test_admin_superuser_safety_net.py`, `README.md` (운영 가이드 3중 안전망 표), DEC-056 (본문 — 분기 1·3·4 정의), DEC-007 (슈퍼유저 분기 폐지 — 본 보강으로 admin 한정 회복)

### DEC-056 보강 (2026-04-22 세 번째 사이클): 분기 0 — admin role 매핑 즉시 채택 (Wave B)

- **결정 사항**: 3중 안전망 위에 **4중째 안전망 = 분기 0** 신설. `admin_service.list_user_roles_and_permissions(user_id)` 가 `'admin'` 또는 `'role-admin'` role 을 반환하는 사용자에 대해 *분기 1·2·3 모두 우회* 하여 즉시 `admin / ['*']` 반환.
  - **위치**: `auth_service._has_admin_role_mapping(user_id)` 신규 헬퍼 + 동기 `_resolve_role_and_permissions` / 비동기 `_resolve_role_and_permissions_async` 양쪽 첫 분기에 호출 (LSP — sync/async 일관 정책).
  - **순서 변경**: `0. admin role 매핑` → `1. hcode='0000'` → `2. BLS_ADMIN_USER_IDS` → `3. Id_Logn Fxx` → `4. admin_service` → `5. BLS_DEFAULT_ROLE` → `6. ('', [])`.
  - **Fail-safe**: `admin_service` 임포트/조회 실패 시 False 반환 → 기존 분기 1 부터 자연 폴백. 일반 사용자(role-admin 미매핑) 미영향.
- **배경/근거**: 사용자 보고 — "admin 계정인데도 보이지 않는 메뉴가 존재한다 / 통계 화면 403". 진단: Id_Logn 의 admin 행 일부 Fxx 셀이 `'O'`/`'R'` 로 박혀있으면 분기 3 가 admin 을 *operator* role 로 합성하여 분기 4(`web_admin.json` admin 매핑) 가 평가되지 않는 lacuna 발견. 분기 0 은 admin role 매핑이 *어떤 분기보다도 우선* 임을 단일 정책으로 해결 — admin 한정 패치가 아니라 `role='admin'` 매핑된 *모든* 사용자가 동일 보장(SOLID-O 일반화).
  - 통계(stats) 403 도 동일 원인 — admin JWT 에 `admin.stats.*` 권한이 합성되지 않음. 분기 0 적용 시 `permissions=['*']` → `_has_permission` 의 `'*' in perms` 분기로 모든 require_permission 통과.
- **수용 기준 (DoD)**:
  - ① `python3 -m pytest test/test_admin_resolver_branch0_priority.py` 5/5 PASS (분기 0 우선순위 / async 분기 3 우회 / 일반 사용자 미영향 / role 코드 'admin'·'role-admin' 양 인정).
  - ② `python3 -m pytest test/test_admin_settlement_full_access.py` 4/4 PASS (정산 7개 + 통계 4개 권한 전수 통과 / 일반 사용자 차단).
  - ③ 기존 회귀: `test_admin_superuser_safety_net` 11/11 PASS (3중 안전망 무영향), `test_c10_admin_phase1::test_P_01..05` 5/5 PASS (LSP).
  - ④ 정산 7화면 라이브 probe (`debug/probe_settlement_endpoints.py`) 4 서버 × 7 endpoint = 28/28 OK.
  - ⑤ ReadLints 0 (changed files only).
- **위험 / 보완**:
  - (i) 기존 admin 토큰 보유자는 *재로그인* 필요 (분기 0 은 토큰 발급 시점에 발효). README 운영 가이드 §재로그인 섹션 추가, `debug/show_jwt_claims.py` 로 즉시 진단 가능.
  - (ii) admin role 매핑된 사용자의 *권한 박탈* 은 (a) `web_admin.json::web_user_roles` 에서 매핑 제거 + (b) admin user 자체 제거 또는 비밀번호 변경 후 가능 — 분기 0 은 매핑 존재 ↔ admin 동치 정책.
- **결정자**: 메인개발자 + 사용자 (2026-04-22 세 번째 사이클 — "admin 에서는 모든 메뉴와 데이터가 접근가능하고, 검색 가능하도록 수정해라" + "통계 화면도 권한 해결" 명시 합의)
- **참조**: `도서물류관리프로그램/backend/app/services/auth_service.py` (`_has_admin_role_mapping`/`_resolve_role_and_permissions{,_async}`), `test/test_admin_resolver_branch0_priority.py`, `test/test_admin_settlement_full_access.py`, `test/test_settlement_billing_no_inline_correlated_subquery.py`, `test/test_settlement_tax_invoice_chek3_optional.py`, `test/test_settlement_cash_status_sdate_response_shape.py`, `debug/probe_settlement_endpoints.py`, `debug/show_jwt_claims.py`, DEC-056 본문 + 보강(2026-04-22 두 번째 사이클), DEC-007, DEC-041, DEC-058

### DEC-058 보강 (2026-04-22 세 번째 사이클): 정산 변형사 DB 컬럼 어댑터 (Wave B 동반)

- **결정 사항**: `tax_invoice_service` 에 `_t2_columns(server_id)` 캐시 헬퍼 + `_build_sql_list_tax(cols)` / `_build_sql_count_tax(cols)` 동적 SELECT 빌더 신설. `T2_Ssub` 의 `Chek3` / `Sdate` / `Yesno` 선택 컬럼이 변형사 DB(예: remote_152) 에 부재할 때 정적 리터럴(`'0' AS Chek3`) 로 대체하여 1054(Unknown column) → HTTP 500 회귀 차단.
  - 패턴: `t5_ssub_adapt.t5_column_names` + `t5_month_key_expr` 의 컬럼 어댑터 1:1 재사용(SOLID-O — 신규 패턴 0).
  - alias 순서 보존(`Chek3` → `Sdate` → `Yesno`) — 응답 모델 호환.
  - WHERE 절의 `COALESCE(t.Yesno,'0') <> '2'` 마감 가드도 `Yesno` 부재 시 자동 제거.
- **수용 기준 (DoD)**:
  - ① `python3 -m pytest test/test_settlement_tax_invoice_chek3_optional.py` 6/6 PASS (전수 컬럼 / 각 컬럼 부재 / WHERE Yesno 자동 제거 / alias 순서 보존).
  - ② 정산 7화면 라이브 probe 4 서버 × 7 endpoint = 28/28 OK.
- **참조**: `도서물류관리프로그램/backend/app/services/tax_invoice_service.py` (`_t2_columns`/`_build_sql_list_tax`/`_build_sql_count_tax`/`clear_t2_column_cache_for_tests`), `t5_ssub_adapt.py` (재사용 패턴 원본), `test/test_settlement_tax_invoice_chek3_optional.py`, DEC-033 (f) (변형사 DB 호환 일반화)

### DEC-059: 메뉴 메타 3축 분리 — `phase` (품질) ∥ `roadmapWave` (P2/P3/P4) ∥ `crudParity` (R/RU/CRUD/STUB)

- **결정 사항**: `FormMeta` 단일 필드 `phase` 가 *품질 게이트*(DEC-053) 와 *로드맵 우선순위*(P2/P3/P4) 두 개념을 동시에 떠안던 모호함을 직교 3축으로 분리. 사이드바 표기 정책도 동일하게 분리한다.
  - (a) `phase: "phase1" | "phase2" | "preview"` — 기존 5축 PASS·회귀 통과 여부(불변).
  - (b) `roadmapWave?: "p2" | "p3" | "p4"` — 신설. 백로그 우선순위(현 사이클 / 차기 / 장기). 사이드바는 `p3`/`p4` 일 때만 회색 보조 라벨 `W3`/`W4` 노출(`p2` = 기본값 가정 → 비표시, 소음 방지).
  - (c) `crudParity?: "R" | "RU" | "CRUD" | "STUB"` — 신설. 레거시 델파이 화면 대비 지원 연산 집합(R=조회만 / RU=조회+부분쓰기 / CRUD=동등 / STUB=라우트만 placeholder). 사이드바는 `R`/`RU`/`STUB` 일 때만 보조 배지 노출(`CRUD` = 기본값 → 비표시).
  - (d) `crudNotes?: string` — `crudParity ≠ CRUD` 인 행의 차이 사유 한 줄(사이드바 tooltip 본문, `docs/crud-backlog.md` 의 “갭” 칸과 1:1).
  - (e) tooltip 정책 — `caption` + 품질·CRUD·웨이브 줄을 *적용된 축만* 한 줄씩 추가(기본값과 일치하면 침묵). `phase1` + `R` 조합은 “녹색 체크 + 회색 R” 로 표시되어 “녹색 = 레거시 동일” 오해 차단(예: `master/publisher` `1차 READ only`).
  - (f) **동기화 정책** — 본 메타의 단일 원천은 `form-registry.ts`. `dashboard/data/phase2-screen-cards.json` 은 거울이며 `$comment` 에 동기화 의무 명시(다음 사이클에 `wave`/`crud` 키 일괄 채움 예정).
- **배경/근거**: 사용자 보고 — *"현재 메뉴별로 P2 단계에 대해서만 표기되어 있는데 P3/P4 단계로 진행해야할 부분이 있으면 표기하고자 한다"*. 분석 결과:
  - 기존 사이드바의 노란 `P2` 배지는 *품질 phase2* 의미였으나 사용자의 "P3/P4" 표현은 *로드맵 우선순위* 의미여서 같은 라벨을 재사용하면 혼란 가중.
  - `phase: phase1` 화면(예: 출판사 마스터) 일부가 페이지 주석에 *"1차 READ only · 수정은 후속"* 으로 박혀 있어 사이드바 녹색 체크가 *"레거시와 완전 동일"* 로 오인됨 — CRUD 동등성 축이 보이지 않은 결과.
  - 두 개념을 같은 필드/라벨로 묶을 때 SOLID-S(단일 책임) 위반. 직교 3축 분리 + 시각 라벨 분리(`P2` 노랑 = 품질 / `W3`/`W4` 회색 = 로드맵 / `R`/`RU`/`STUB` 회색 outline = CRUD) 로 일반화.
- **수용 기준 (DoD)**:
  - ① `python3 -m pytest test/test_form_registry_metadata.py` PASS — 허용값 검증 + `phase1` 인데 `crudParity ∈ {R, RU, STUB}` 행은 `crudNotes` (또는 `scenario.blockers`) 에 한 줄 이상 사유 보유.
  - ② `cd 도서물류관리프로그램/frontend && npx tsc --noEmit` exit 0 (`FormMeta` 확장 타입 정합).
  - ③ ReadLints 0 (`form-registry.ts` + `sidebar.tsx`).
  - ④ 사이드바 렌더 — `master/publisher` 행에 `R` 보조 배지 + `master/customer` 행에 `RU` + `Sobo16_special` 행에 `STUB` + `W2` 가 어디에도 없음(p2 = 기본값) + `Sobo16_special` 에 `W2` 미표시(p2) / `Sobo50_stats` 에 `W3` 표시.
- **위험 / 보완**:
  - (i) `phase1` 화면 다수가 인벤토리 1차 단계라 `crudParity` 미설정 — 정적 가드 §5.4 (인벤토리 완성도) 는 1차에 *경고*, 다음 사이클에 *에러* 로 점진 도입(폭발 회귀 방지).
  - (ii) `phase2-screen-cards.json` 은 본 사이클에 `$comment` 만 갱신, 화면별 `wave`/`crud` 키는 다음 사이클(스키마 추가 + 검증 가드 동시 도입). drift 방지를 위해 `form-registry.ts` 단일 원천 정책 명시.
  - (iii) `roadmapWave` 미설정 = `p2` 가정 — 명시적 빈 값과 `p2` 의 의도 차이는 `crudNotes` 로 보충(예: “현 사이클 범위, 인벤토리 보류”).
- **결정자**: 메인개발자 + 사용자 (2026-04-23 — "P3/P4 단계로 진행해야할 부분이 있으면 표기하고자 한다" + "CRUD 동등성도 같이 보고싶다" 합의)
- **참조**: `docs/menu-roadmap-waves.md`(신규 정책 단일 원천), `docs/crud-backlog.md`(신규 — CRUD gap matrix + G0~G4 보강 절차 + P2/P3/P4 우선순위), `도서물류관리프로그램/frontend/src/lib/form-registry.ts`(`FormMeta` 확장 + 식별 행 채움), `도서물류관리프로그램/frontend/src/components/app-shell/sidebar.tsx`(보조 배지 + tooltip 한 줄 자막), `dashboard/data/phase2-screen-cards.json`($comment 동기화 의무), `test/test_form_registry_metadata.py`(허용값·일관성 정적 가드), DEC-053(품질 phase 게이트 — 본 결정의 짝), DEC-058(사이드바 권한 게이팅 — 필터링 책임은 분리), DEC-019(마스터 PATCH «수정 ON · 삭제 OFF» 정책 — `crudParity: RU` 인 마스터 화면의 백엔드 짝)

### DEC-060: 레거시 매핑 추정 오류 사전 차단 — DFM Caption 대조 게이트 (DEC-019/023/028 보강)

- **일자**: 2026-04-23
- **결정 사항**: 모든 모던 화면(`form-registry.ts::FormMeta` 항목)은 `folder` (예: `Subu45`) 가 가리키는 레거시 DFM 의 `Caption` 과 의미적으로 일치해야 한다. 단일 `folder` 에 두 개 이상의 `FormMeta` 가 매핑되는 경우(접미 `_billing`/`_cash` 등 DEC-019 변형 통합 정책 예외) 는 모두 동일한 본 화면(Caption)에서 파생된 단일 의미여야 하며, 「테이블 컬럼만 보고 마스터 카탈로그를 추정해 새로운 ID 를 부여하는 행위」를 금지한다. master_data.yaml v1.0.0 (Wave A/B/C) 가 `G5_Ggeo.Gposa` 컬럼만 보고 「Sobo45 = 물류비 마스터」 로 추정했으나 실제 `Subu45.dfm Caption='청구서관리'` (Sobo45_billing) 와 어긋났던 사례를 일반화 차단한다.
- **배경/근거**:
  1. **사용자 보고 (2026-04-23)**: "이 화면이 레거시 델파이 프로그램에서는 청구서관리 화면이고 검색 필터를 위한 입력 항목도 다른데?" — `/master/logistics-cost` 화면 헤더가 "Sobo45 · G5_Ggeo · 1차 READ only" 였으나 사용자가 즉시 잘못된 매핑을 식별.
  2. **사실 검증**: `Subu45.dfm` Caption (EUC-KR 디코딩) = `'청구서관리'`. `Subu45_1.dfm` = `'청구서관리-택배'`. 청구서관리는 이미 `Sobo45_billing` (folder=Subu45, route=/settlement/billing) 으로 정상 등록되어 있어 동일 folder 에 모순된 두 ID 가 공존.
  3. **근본 원인**: master_data.yaml v1.0.0 작성 시 G5_Ggeo.Gposa 컬럼이 "물류비" 의미였기 때문에 Subu45 폴더의 폼 1개를 그 마스터 화면이라고 추정 — DFM Caption 1차 검증을 누락. 동일 패턴이 다른 G*_* 마스터 테이블에도 잠복 가능.
  4. **대안 검토**:
     - (A) 화면 자체는 G5_Ggeo CRUD 카탈로그로 의미 보존, ID/부제만 정정 (예: `WebMasterLogisticsCost`).
     - **(B) 화면 제거 + 청구서관리(Sobo45_billing) 로 통합** ← 채택. G5_Ggeo.Gposa 는 Subu45.pas L372 의 `G5_Ggeo.Locate` 패턴대로 청구서관리 화면 내부 lookup 으로 흡수되며, 단독 마스터 화면이 레거시에 존재하지 않으므로 「레거시에 없는 화면을 신설하지 않는다 = 5축 동등성 보존」 원칙에 부합.
     - (C) 별도 신규 카탈로그로 보존 — 사용자 가치가 모호하고 청구서관리와 데이터 영역 중복.
- **영향**:
  - **백엔드**: `routers/masters.py` 의 `GET /api/v1/masters/logistics-cost` 엔드포인트 + `services/masters_service.list_logistics_costs` + `models/master.LogisticsCost*` 제거.
  - **프론트**: `(app)/master/logistics-cost/page.tsx` 삭제, `lib/form-registry.ts` 의 `Sobo45 (caption='물류비', menuGroup='master')` 항목 제거 (단일 folder 중복 매핑 차단), `lib/master-api.ts` `logisticsCostList` + `LogisticsCost*` 인터페이스 제거, `(app)/master/page.tsx` 카드 1건 제거.
  - **계약**: `migration/contracts/master_data.yaml` v1.1.0→**v1.2.0**, catalog 행 `Sobo45 → 물류비` + endpoints[SQL-MAS-10] + customer_variants[Sobo45] 제거. 6 종 → 5 종 마스터 표기 일괄 정정 (DEC-024/025/026 본문 내 라인).
  - **테스트**: `test/test_masters_q_search.py` LIST_FUNCS 6→5, 18 케이스→15 케이스 + `LogisticsCostMappingRemovedTests` 5축 부재 단언 신규(서비스/모델/라우트/프론트 페이지/계약 catalog). `test/test_pagination_contracts.py::test_logistics_cost_list` 제거. `test/test_list_state_persistence_audit.py` baseline 6→5.
  - **감사/대시보드**: `analysis/audit/list-state-coverage-report.json` 자동 재생성 필요. `analysis/audit/phase1-component-fidelity.md` Sobo45 행 DEPRECATED 마킹. `analysis/layout_mappings/Sobo45.md` 헤더에 DEPRECATED 마킹 + 대체 참조 추가. `dashboard/data/porting-screens.json` 라우트/엔드포인트/요약 항목 정정.
- **DoD (수용 기준)**:
  - ① `pytest test/test_masters_q_search.py test/test_pagination_contracts.py test/test_list_state_persistence_audit.py` 전부 PASS — 신규 부재 단언(`LogisticsCostMappingRemovedTests` 5/5) 포함.
  - ② `cd 도서물류관리프로그램/frontend && npx tsc --noEmit` exit 0.
  - ③ `master_data.yaml` 에 `path: /api/v1/masters/logistics-cost` 라인 0건, `LogisticsCostListResponse` 참조 0건.
  - ④ `form-registry.ts` 에서 `id: "Sobo45"` (caption=물류비 매핑) 0건, `id: "Sobo45_billing"` 단일 매핑만 보존.
- **재발 방지 (일반화)**:
  - 새 마스터 화면 추가 시 「DFM Caption 1차 검증」 절차 의무: `iconv -f EUC-KR -t UTF-8 legacy_delphi_source/legacy_source/Subu*.dfm | grep -E '^  Caption'` 으로 폼 단위 Caption 을 확인하고 카탈로그 추정 대신 사실 매핑.
  - 동일 `folder` 에 두 개 이상의 `FormMeta` 가 등록되는 경우, 각 항목의 의미가 본 폼 Caption 에서 파생된 단일 의미인지 (DEC-019 변형 통합 또는 다른 화면 카탈로그 위치 분리) 매핑 노트 §0 에 명시.
  - 신규 카탈로그 항목 도입 전 DEC-019 (수정 ON·삭제 OFF) + DEC-023 (단일 원천) + DEC-028 (DFM 산출물 동결) 3 결정 본문을 1차 점검 가드로 사용.
- **결정자**: 메인개발자 + 사용자 (2026-04-23 매핑 검증 사이클)
- **참조**: `migration/contracts/master_data.yaml` v1.2.0, `legacy_delphi_source/legacy_source/Subu45.dfm` (Caption='청구서관리'), `migration/contracts/settlement_billing.yaml` (Sobo45_billing 정상 매핑), `analysis/layout_mappings/Sobo45.md` (DEPRECATED), `test/test_masters_q_search.py::LogisticsCostMappingRemovedTests`, DEC-019(마스터 정책), DEC-023(단일 원천), DEC-028(DFM 동결), DEC-053(Phase 1 component fidelity)

### DEC-061: DFM↔form-registry 동등성 매트릭스 — 자동 생성 문서 + 파이프라인 훅 (DEC-060 운영화)

- **일자**: 2026-04-23
- **결정 사항**:
  1. **`tools/delphi_form_screen_matrix.py`** — `legacy_source/Subu*.dfm` 루트 `object Sobo*:` + `Caption` (EUC-KR/CP949 디코딩) 을 수집하고, `form-registry.ts` 의 `id`·`folder`·`caption`·`route` 와 병합하여 **동등성 표**를 만든다.
  2. **인간용 산출물** — `docs/delphi-form-screen-equivalence-matrix.md` (항상 갱신, Git 추적). **기계용** — `analysis/audit/delphi-form-screen-matrix.json`.
  3. **상태 분류**: `MATCH` · `NEAR_MATCH` · `MULTI_MAP`(동일 폴더 복수 라우트) · `DFM_PLACEHOLDER`(루트 Caption 이 `Sobo38` 등 식별자 수준) · `WEB_ONLY`(`_WebAdm`) · `CAPTION_DIFF` 등 — 표와 JSON 에 명시.
  4. **`--check`** — 등록된 **`Subu*`** 폴더마다 대응 `dfm` 파일 존재 여부만 게이트(종료 코드 1). **`--strict`** — 단일 매핑 행의 `CAPTION_DIFF` 까지 게이트(선택, 초기 레거시는 라벨 차이 많아 기본 미사용).
  5. **회귀**: `test/test_delphi_form_screen_matrix.py` — Subu45 청구서관리 문구·`Sobo45_billing` 존재·구 잘못 ID 부재·CLI `--check` exit 0.
- **배경/근거**: 사용자 요청 — 델파이 폼 이름·제목과 포팅 화면을 표로 비교해 재발 방지 및 파이프라인에 포함. DEC-060 의 「DFM Caption 대조」를 매 사이클 실행 가능한 산출물로 고정.
- **포팅 파이프라인**: `docs/core-scenarios-porting-plan.md` 연관 산출물에 본 문서 링크 추가 — 화면 계약·레지스트리 수정 **전후**에 스크립트 1회 실행 권장.
- **결정자**: 메인개발자 + 사용자
- **참조**: `tools/delphi_form_screen_matrix.py`, `docs/delphi-form-screen-equivalence-matrix.md`, DEC-060

### DEC-058: 사이드바 권한 게이팅 — `usePermissions()` + `requiredPermission` (legacy 'X' 동등 = hidden)

- **결정 사항**: 모던 사이드바를 레거시 `if nUse2='X' then ShowMessage` 클릭 시점 거부와 동등한 **메뉴 비표시** 정책으로 게이팅한다. 채택 패턴:
  - (a) `frontend/src/lib/use-permissions.ts` 신규 — `usePermissions()` 훅 = `{ isLoading, isSuperUser, has, hasAny }`. `isSuperUser = perms.has('*') || user.role === 'admin' || user.hcode === '0000'` 3-OR (분기 1·2·4 슈퍼유저 폴백 모두 흡수).
  - (b) `frontend/src/lib/form-registry.ts::FormMeta` 에 옵셔널 `requiredPermission?: string` 필드 추가 — 미지정 = 모든 사용자 노출(기존 행동 보존). 52 폼 매핑은 카탈로그 §1+§4 의 `permission_code` 1:1 적용.
  - (c) `frontend/src/components/app-shell/sidebar.tsx` 게이팅 — `isVisibleForm(form) = !form.requiredPermission || perms.has(form.requiredPermission)`, `useMemo` 로 그룹별 visibleForms 캐시, **그룹 내 가시 폼이 0건이면 그룹 헤더 자체를 hidden** (legacy 사이드바와 동일한 빈 그룹 제거 시각 효과).
  - (d) **선택 정책 = hidden** (vs disabled tooltip) — legacy `'X'` 가 클릭 시점 거부였으므로 의미 동등. 의사결정 단일화로 추가 분기 0(SOLID-S).
- **배경/근거**: (1) 사용자 보고: "권한 없는 메뉴가 노출되어 클릭 시 403 토스트 → 운영 혼선". (2) 레거시 메커니즘이 메뉴 클릭 시점 가드(`Seek_Uses('Fxx')`) 인데 모던은 사이드바가 권한 무관(`phase` 만) 이라 UX 회귀. (3) 백엔드 권한 변경 즉시 반영은 토큰 만료(15분) 까지 대기 — 본 결정은 *클라이언트 사이드* 가시성만 다루고, 라우터 가드(`require_permission`) 는 그대로 두어 *URL 직접 입력 우회 = 403* 의 보안 모델 무변동(이중 방어).
- **수용 기준 (DoD)**:
  - ① `python3 -m pytest test/test_sidebar_permission_gating.py` 4/4 PASS (정적 분석: `requiredPermission` 값이 카탈로그 §1+§4 부분집합 / `FormMeta` 매핑 ≥ 50건 / `sidebar.tsx` 가 `usePermissions()` 호출 / `usePermissions` 의 3-OR 슈퍼유저 분기 보존).
  - ② `cd 도서물류관리프로그램/frontend && npx tsc --noEmit` exit 0.
  - ③ `cd 도서물류관리프로그램/frontend && npx eslint src/lib/use-permissions.ts src/lib/form-registry.ts src/components/app-shell/sidebar.tsx` 0 error/warning.
  - ④ 슈퍼유저(role=admin / `*` / hcode=0000) 로그인 시 모든 메뉴 노출(회귀 가드 — `usePermissions` 3-OR).
- **위험 / 보완**:
  - (i) 권한 부여 직후 사이드바가 즉시 안 보임 → 토큰 만료(15분) 또는 `/api/v1/auth/refresh` 강제. `decisions.md` 에 명시(DEC-061 후속 검토).
  - (ii) `requiredPermission` 미지정 폼은 노출 — 신규 폼 추가 시 카탈로그 매핑 누락 차단 가드는 별도 audit 단계(M5 마무리 후속).
  - (iii) `isSuperUser` 가 user 미로드 시 false → 첫 렌더 빈 사이드바 깜빡임 가능. `loading` 플래그 노출로 호출자가 skeleton 처리 가능(현재는 그대로 통과 — UX 미세).
- **결정자**: 메인개발자 + 사용자 (DEC-056·DEC-058 즉시 적용 명시 합의 2026-04-22)
- **참조**: `도서물류관리프로그램/frontend/src/lib/use-permissions.ts`(신규), `도서물류관리프로그램/frontend/src/lib/form-registry.ts`(`FormMeta.requiredPermission` 추가 + 52 매핑), `도서물류관리프로그램/frontend/src/components/app-shell/sidebar.tsx`(`isVisibleForm` 게이팅 + 빈 그룹 hidden), `legacy-analysis/permission-keys-catalog.md` §1+§4, `docs/user-permission-management-plan.md` §5 M2, `test/test_sidebar_permission_gating.py`, DEC-041(RBAC 401·403 인터셉터 — 라우터 게이트 무변동), DEC-046(권한 d_select), DEC-056(Id_Logn Fxx 어댑터 — 본 결정의 백엔드 짝)

### DEC-062: DB 스모크 probe — L4 TestClient 슈퍼유저 dependency_overrides

- **일자**: 2026-05-04
- **결정 사항**: `debug/probe_backend_all_servers.py` 의 L4 점검은 실제 JWT 없이 **슈퍼유저 클레임**으로 `app.routers.auth.get_current_user` 와 `app.core.deps.get_user_context` 를 함께 override 한다. JWT 형태 dict 는 `permissions=['*']`, `role='admin'` (`deps._resolve_permissions` 단일 규칙과 정합). 요청별 데이터 소속 `server_id` 는 쿼리 `serverId`/`server_id`, 헤더 `X-Smoke-Ownership-Server`, path 파라미터에서 해석한다. 음성 검증 그룹 ``auth.expired_must_401`` 등은 해당 호출에서만 override 를 제거해 무토큰 경로를 검증한다.
- **배경/근거**: 다수 라우트가 핸들러 시그니처에 `Depends(get_current_user)` 만 두어 `get_user_context` 만 우회할 경우 401 로 SQL·스키마 회귀 검증에 도달하지 못함. 멀티 DB 스모크의 1차 목적은 DEC-033 계열 **데이터/SQL 호환** 이지 실운영 RBAC 재현이 아님. 분석: `analysis/audit/db-smoke-permission-mapping.md`.
- **대안**: (B) L4 매트릭스를 데이터 회귀만 남기고 인증은 별도 단위 테스트로 분리 — DoD·문서 이중화 필요.
- **영향**: live 스모크에서 도메인 라우트까지 도달 가능. 테넌트별 스키마 차이·미배포 테이블 등으로 인한 5xx 는 기존 정책대로 런북·`customer_variants`/DEC 에 예외 기록.
- **결정자**: 메인개발자
- **참조**: `analysis/포팅_완결_우선_계획_672e6c6a.plan.md`, `docs/db-smoke-runbook.md`, DEC-033, DEC-041

### DEC-063: 브라우저 위치 권한 — 목적 고지·로컬 플래그·재요청 UX

- **일자**: 2026-05-04
- **결정 사항**: (1) **목적** — HTML5 Geolocation 으로 얻은 좌표는 기상청 격자 변환(`weather-grid-from-point` 등 기존 대시보드 API)과 헤더 날씨·위치 연동 위젯에만 사용한다. 원시 좌표를 프로필·감사 로그 등 다른 용도로 저장·전송하지 않는다(배너·플래그는 `localStorage` 키 `portal_location_permission_v1` 만). (2) **재요청** — 내정보 설정에 「위치 안내 다시 요청(저장값 초기화)」으로 `dismissed`/`denied` 등 로컬 플래그를 제거해 배너를 다시 띄울 수 있게 한다. (3) **계약** — 한 줄 요약은 `migration/contracts/portal_location.yaml` 의 `intent.location_data_purpose_ko` 로 고정한다.
- **배경/근거**: 포팅 완결 계획의 위치 권한 운영 마감; 법무 검토 전이라도 운영·DEC·계약에 목적을 한 줄 명시해 혼선을 줄인다.
- **참조**: `docs/location-permission-runbook.md`, `도서물류관리프로그램/frontend/src/lib/location-permission-storage.ts`, `.../settings/my-profile/page.tsx`

### DEC-064: C6 거래명세서(Sobo21) 재고 Label104 — Phase 1 placeholder, Phase 2 PrinJing

- **일자**: 2026-06-01
- **결정 사항**: (1) **Phase 1** — `customer-preview`·`detail` 의 `stock_qty` 는 `compute_sales_statement_stock_qty` placeholder(`SUM(Gsqut)` on S1_Ssub, 동일 검색 맥락 + `gjisa_lookup_variants IN`) 로 유지한다. 레거시 `Label104` 가 표시하는 **694** 는 `Tong02.pas` `PrinJing` → `Sv_Ghng` 창고 재고(`SUM(GsumX)` by `Bcode`) 이므로 Phase 1 DoD 에서 수치 동등을 요구하지 않는다. (2) **Phase 2** — `PrinJing`/`Sv_Ghng` 포팅으로 `stock_qty` 정의를 교체하고, `migration/contracts/sales_inquiry.yaml` `sales_statement_detail.stock_qty`·`barcode_scan.yaml` 교차 참조로 회귀 가드 추가. (3) **동시 완료(본 사이클)** — `Gjisa` `gjisa_lookup_variants IN`(pipe·dot·공백), `customer-preview` `memo_preview`(Subu21 Button301), 참고 패널 G1+메모 read-only — 목록 0건·참고 비표시 P0 해소.
- **배경/근거**: 레거시 스크린샷(교보문고 00001·2026-05-14) 대비 모던 목록 0건의 1순위 원인은 `Gjisa` 정확 일치; 재고 694 불일치는 별도 비즈니스 정의. `gcode_lookup_variants` 패턴을 `gjisa_lookup_variants` 로 일반화(SOLID-O).
- **영향**: `h2_gbun_adapt.gjisa_lookup_variants`, `transactions_service._append_gjisa_filter`, `load_sales_statement_memo_preview`, FE `SalesStatementReferencePanel`·`page.tsx` `refError`/`memoPreview`. 진단: `debug/probe_sales_statement_list_gjisa.py`. 회귀: `test/test_sales_statement_gjisa_variants.py`, `test/test_sales_statement_list_reference_panel.py`.
- **2026-06-02 보강**: LIST `Scode='X'`·`jubun_lookup_variants`·`gjisa_search_variants`(H2 gname-only); GET `/sales-statement` 는 쿼리 `hcode` 없을 때 JWT scope 미주입(Subu21 Edit107 `''`). 전표번호 FE `formatJubunInput`. RTF `rtf_convert` pandoc optional + `\u`/`\fs` 파서.
- **2026-06-04 보강 (교문사·chul_09_db)**: WeLove `chul_09(위러브)/Subu21.pas` 정본 — `Hcode=Hnnnn`(JWT 5019), `Ocode='A'`(창고 캡션), H2 도 `Hnnnn`. `resolve_h2_hcode_for_customer`·`sales_statement_ocode_sql`·T3·`chul_09` LIST JWT hcode 주입·취소 라인 HAVING 미적용. `customer_variants` §8 `chul_09_warehouse_subu21`. 회귀 `test/test_sales_statement_chul09_hcode_scope.py`.
- **2026-06-04 보강 (전표번호 중심 UX)**: Jubun 비고유 — FE 전표+일자 우선 조회·단건 자동 detail·다건 후보 그리드·라인(Bcode) 클릭 시 `customer-preview` 로 Label104(PrinJing) 재고 갱신. `formatJubunInput` 2자리 패딩 금지. 회귀 `test/test_sales_statement_jubun_primary_search.py`.
- **2026-06-05 보강 (§Idnum 상세수정 — row key + detail WHERE 정합)**: 재시작 후에도 전표번호가 Jubun `11` 로 보이고 상세 라인이 비는 회귀 — 원인 ① LIST 가 SQL row dict 의 `Idnum`/`stmt_gcode` 대소문자 키를 읽지 못해 `order_key.idnum=0` surface, ② 상세 `_build_stmt_line_where` 가 LIST 대비 `Ocode`·`jubun_lookup_variants` 누락. 수정: `transactions_service._row_get`/`_stmt_list_fields_from_row`, `s1_ssub_adapt.s1_idnum_{group,select}_expr`(Idnum 컬럼 부재 테넌트 `0 AS Idnum`), detail WHERE `server_id` 시 `sales_statement_ocode_sql` + Jubun IN variants, `detail_lines_select_sql` Idnum/Gjisa/Ocode 추가. FE 참조 패널 `slipNo` Jubun 폴백 제거·거래처 단건 자동 `selectStatementRow`·상세 실패 배너. 진단 `debug/probe_sales_statement_idnum_detail.py`. 회귀 `test/test_stmt_line_where_ocode.py`, `test/test_sales_statement_detail_idnum_lines.py`.
- **2026-06-05 보강 (§Idnum 정합 + 좌·우 한 화면 + 도서 lookup + 키보드 네비)**: 레거시 정본 재대조 결과 사용자 노출 "전표번호" 의 진짜 정체는 `Subu21.pas` `Edit109`(=`Idnum`) 5자리 zero-pad(`Format('%05s', FormatFloat('00000', St2))`, L961·L2349·L2365 동등) 이며, `Edit103`(=`Jubun`) 은 `MaxLength=2`·`Visible=False` 인 거래구분 차수(출고 11/12·반품 21/22). 기존 모던 LIST `_GROUP_BY_STMT_KEYS = (Gdate, Hcode, Jubun, Gjisa)` 4축은 `Gcode` 가 다른 두 슬립이 동일 Jubun(예: 출고 11) 일 때 한 행으로 합쳐져 교문서-경리부 등 다중 거래처 테넌트에서 LIST 누락이 발생하므로 6축(`Gdate, Hcode, Idnum, Gubun, Jubun, Gjisa, Gcode`) 으로 확장하고 `ORDER BY Gdate DESC, Hcode, Idnum DESC, Gcode` 로 안정화. 백엔드 신규 `_append_idnum_filter`(정수 매칭, `Subu21.pas` Button901Click L924 `Idnum= @Idnum` 동등) + LIST/customer-preview/detail 라우터 `idnum?: int` 쿼리 + `inquiry_order_key` 7세그먼트(`gdate|hcode|jubun|gjisa|idnum|gubun|gcode`) 확장(4세그먼트 backward-compat). 응답 `order_key`/Pydantic `StatementKey` 에 `idnum`, `gubun`, `gcode` 필드 surface, `slip_no` 는 `idnum` 5자리 zero-pad. FE `formatIdnumInput`(1~5자리 zero-pad, `formatJubunInput` 별칭 보존), `transactionsApi.list({idnum})`, `serializeStatementKey` 7세그먼트, 거래명세서 페이지 좌(목록·라인) / 우-상(거래처참조)·우-하(배송메모) 한 화면(`lg:grid-cols-[2fr,1fr]` + sticky), 라인 그리드 도서코드 셀 `MasterLookupButton(book)` 미리보기, `DataGrid` opt-in 키보드 네비(↑/↓/Home/End/Enter, 기존 화면 회귀 0). 회귀 `test/test_sales_statement_idnum_groupby.py`, `test/test_routers_sales_statement_idnum.py`, `test/test_data_grid_keyboard_nav.tsx`, `test/test_layout_mappings_sobo21.py`.
- **참조**: `analysis/layout_mappings/Sobo21.md`, `migration/contracts/sales_inquiry.yaml`, Subu21.pas Button101/Button301, Tong02.pas PrinJing

### DEC-065: 거래명세서(Sobo21) 화면 내 신규추가 — outbound create_order 재사용 + 라인 패리티 + 키보드 전용

- **일자**: 2026-06-14
- **결정 사항**: 거래명세서(Sobo21) 화면에 **신규추가**를 복원한다(기존 `Button201 = out-of-scope, "거래명세서 신규는 C2 outbound 와 분리"` 결정 **부분 번복**). (1) **생성 동선** — Sobo21 화면 내 신규(레거시 충실), 전용 라우트 `/transactions/sales-statement/new` 의 in-grid 키보드 입력. (2) **거래구분** — 1차 **출고 고정**(Gubun, 서버 강제); 반품/파지 후속(D2). (3) **라인 충실도** — 풀 패리티: 도서코드→단가·비율 자동조회, 수량→금액 자동계산, 비고 포함. (4) **백엔드** — 생성은 `outbound_service.create_order`(동일 S1_Ssub INSERT·트랜잭션·전표 자동채번·audit) 재사용, `OrderLineInput`+`SQL_INSERT_LINE` 에 `Gdang/Grat1/Gbigo` 추가(기본값으로 기존 출고 호출부 BC 유지). 신규 엔드포인트 `POST /sales-statement`, `GET /sales-statement/line-defaults`(신규 SQL 표면 최소화, DEC-040 정합). (5) **자동조회 규격(레거시 정본)** — 단가·비율 4단 override(last-wins): `G1_Ggeo`(거래처 비율, Pubun 선택) → `G4_Book`(도서마스터 단가/비율) → `G6_Ggeo`(거래처×도서 특가) → `S1_Ssub` 직전거래가(`PrinRat1`, `G7_Ggeo.Chek3='grat1'`=단가+비율 / `'grat2'`=비율만 게이트, 특정 고객 DB 는 `Chek2≠'True'` 시 지사 키 추가). 비율은 품목구분(Pubun)으로 `Grat1~Grat7` 중 택1(`PrinZing`). 금액 = `round(Gdang*Gsqut*Grat1/100)`(`PrinYing`, 비율 0 → 0). (6) **키보드 전용** — 도서코드 Enter→자동조회·수량 이동, 수량 Enter→다음 행 자동추가, ↑/↓ 행 이동, Ctrl+S/F2 저장, Ctrl+Del 행삭제, Esc 목록, 목록에서 `N` 키 신규 진입(레거시가 마우스 없이 키보드로 운용된 흐름 보존).
- **배경/근거**: 레거시 시연 영상 `거래명세서 신규추가 및 검색.mp4` + `WeLove_FTP/도서유통-출판/{Subu21,Tong02,Base01}.pas` 정본 분석. 모던 포팅이 Sobo21 을 읽기 전용(목록·상세·메모)으로만 구현해 사용자가 신규추가를 못 하던 P0 격차. 생성 로직은 outbound 와 동일 테이블이므로 재사용으로 신규 SQL·중복 최소화.
- **영향**: BE `models/outbound.OrderLineInput`(+gdang/grat1/gbigo), `services/outbound_service.SQL_INSERT_LINE`/`create_order`(+`_safe_num`), 신규 `services/sales_statement_create_service.py`, `models/inquiry`(+`SalesStatementLineCreate`/`SalesStatementCreateRequest`/`SalesStatementCreateResponse`/`LineDefaultsResponse`), `routers/transactions`(+POST·line-defaults, line-defaults 는 `{order_key}` 보다 먼저 선언). FE `lib/inquiry-api`(+`lineDefaults`/`createSalesStatement`), 신규 `app/(app)/transactions/sales-statement/new/page.tsx`, 목록 페이지 `신규(N)` 버튼·단축키. 회귀 `test/test_sales_statement_create_phase1.py`(15). 계약 `migration/contracts/sales_inquiry.yaml`, 매핑 `analysis/layout_mappings/Sobo21.md`.
- **잔여(verify-at-impl)**: ① 직전거래가(PrinRat1) 와 G6 특가의 정확한 선후(레거시 OnChange 호출 순서로 P1 확정 — 현재 직전거래가를 최상위 override 로 둠). ② `Hnnnn`(회사/지점) vs `S1_Ssub.Hcode`(거래처) 의미 — line-defaults 는 회사=JWT scope, customer=거래처코드로 분리 전달, G4_Book 은 Hcode 무관 폴백으로 빌드 차이 흡수. ③ 금액 반올림 규칙(round 가정) 은 실 데이터로 절삭/반올림 확정.
- **2026-06-14 보강 (P4 거래현황(상세) 검색 다이얼로그)**: 레거시 `Subu24/Subu24_2`(`거래현황(상세)`, Sobo21 검색버튼 ShowModal) 동등 — 거래일자(범위)·거래구분·전표구분·거래처명·**도서구분(Pubun)**·**도서코드(Bcode)**·취소포함 필터 + 듀얼그리드(좌 전표목록 / 우 선택전표 라인상세). BE: `list_sales_statements`/`_build_sales_statement_list_where`/라우터 LIST 에 `bcode`/`pubun` 라인 동등 필터 추가(S1_Ssub 행=라인, 파생테이블 불요·mysql3 호환, count·select 동일 WHERE 공유). FE: 신규 모달 `components/transactions/sales-statement-search-dialog.tsx`(키보드 전용 — 필터 Enter 검색·결과 ↑/↓/Home/End·Enter 상세이동·Esc 닫기), 목록 페이지 `검색(F)` 버튼·`F`/`Ctrl+F` 단축키. data-legacy-id `Sobo20.*`(검색폼)/`Sobo20.DBGrid101·DBGrid201`. 회귀 `test/test_sales_statement_search_dialog_filters.py`(3).
- **2026-06-15 보강 (지점명/도서코드 검색 + 컬럼 레거시 정렬 + 수정기능)**: ① **지점명(Gjisa)** — 신규 페이지에서 plain input → 거래처 지점 드롭다운(`masterApi.customerBranchList`, 목록 페이지와 동일 H2_Gbun 패턴). ② **도서코드** — plain input → 기존 `MasterLookupField`(인라인 자동완성 + 검색 팝업) 재사용; 키워드 입력 후 Enter → 정확코드면 자동조회·수량 이동, 미일치면 키워드로 **시드된 검색 팝업** 오픈. 공용 컴포넌트 가산 강화: `MasterLookupDialog/Button`에 `initialQuery`(시드)·제어형 open, `MasterLookupField`에 `inputRef`·`dialogOpen` 추가(기존 호출부 BC). ③ **라인 컬럼을 레거시 `Subu21.dfm DBGrid101` 순서로 정렬** — 구분·도서코드·도서명·수량·단가·비율·금액·비고·**배송**(YESNO 추가). 거래현황 검색 다이얼로그 라인 패널도 비고·배송 추가(Subu24 동등). ④ **수정(EDIT) 기능** — 거래현황(상세) 검색 → 결과 선택 → 거래명세서 폼 로드(`?edit=<order_key>` 수정 모드, 거래일자·거래처 잠금) → 라인 수정/추가/삭제 → 저장(같은 전표). BE 신규 `PUT /api/v1/transactions/sales-statement/{order_key}` + `sales_statement_create_service.update_sales_statement`(desired-state diff, 금액 서버 재계산, **mysql3 IFNULL 게이트**, Gdang/Grat1/Gbigo 컬럼 존재 시만 SELECT/INSERT/UPDATE — **레거시 DB 구조 무변경**, DDL 0, audit 'updated'). FE 상세 페이지 `수정` 버튼. 회귀 `test/test_sales_statement_update_phase1.py`(6).
- **2026-06-14 적대적 리뷰 반영 (6축×검증, 확정 3건)**: ① **mysql3 COALESCE 회귀(critical, 선재결함)** — `outbound_service.list_orders`/`inbound_service.list_receipts` 가 mysql3_protocol 서버에서 raw `COALESCE`(1064→500) 방출. `_shipment_status_order_level_sql` 패턴(mysql3 시 `IFNULL`)으로 SELECT/GROUP BY/ORDER BY/count_grouped 일괄 치환. 회귀 가드 `test/test_outbound_inbound_list_mysql3_coalesce.py`(SQL 문자열 캡처 검증). ② **키보드(high)** — `MasterLookupField` 인라인 자동완성 키보드 미지원(blur 무조건 닫힘+방향키 없음) → focus-aware blur(relatedTarget)+roving nav(↑/↓/Enter/Esc, role=listbox/option/aria-activedescendant)+`onKeyDown` prop 추가(가산적, 마우스 동작 보존). ③ **키보드(medium)** — 신규 페이지 헤더(거래일자/거래처/지점) Enter→첫 도서코드 칸 이동(`onHeaderEnter`). 잔여(미수정·선재): `_SQL_OUTBOUND_ORDER_HDR_WHERE`/입고 `_RECEIPT_KEY` 상수의 COALESCE(update/cancel/detail 경로) — 본 P4 범위 밖, 별도 정리 권장.
- **참조**: `docs/sobo21-new-add-plan.md`(적용계획), `analysis/layout_mappings/Sobo21.md`, Subu21.pas Button201Click, Subu24.{pas,dfm}(거래현황 상세), Tong02.pas PrinYing/PrinZing/PrinRat1, Base01.pas L12200(Chek2/Chek3)
- **결정자**: 메인개발자

### DEC-066: 부서계정(경리부) 전(全) 화면 CRUD + MENUVIS-DEC-06 사이드바 가시성 환원

- **일자**: 2026-06-20
- **결정 사항**: (A) **사이드바 가시성 환원** — DEC-058 의 "Fxx 'X' = 메뉴 hidden" 정책을 부분 환원한다. 사이드바 `isVisibleForm` 은 **매트릭스(`getMenuState().visible`) 기준만** 사용하고, Fxx read 게이트(`perms.canAccessScreen`)로 메뉴를 숨기지 *않는다*. 근거: 레거시 Delphi `Chul.pas` 의 `Menu1xxClick` 은 `Seek_Uses('Fxx')` 결과가 `'X'` 여도 메뉴 항목 자체는 항상 노출하고(클릭 시 `ShowMessage(E_Connect)` 접속불가 안내), `'O'/'R'` 일 때만 폼을 열되 `Panel.Enabled`/`DBGrid.ReadOnly` 로 **편집 가능 여부**만 토글했다. 직전 세션에서 추가한 `canAccessScreen` 2차 게이트가 경리부(부서계정)에서 "관리자 외 모든 메뉴"가 보이던 원본 구성을 깨뜨려(스크린샷 회귀) 환원한다. (B) **경리부 full-CRUD** — `Id_Logn.Gcode == '경리부'` 계정은 (관리자 플랫폼 화면 제외) 모든 업무 화면에서 등록/수정/삭제가 가능해야 한다. 로그인·리프레시 시 권한/캡 산출 *직전* 에 업무 Fxx 셀을 전부 `O` 로 승격한 **효과(effective) 매트릭스**를 사용한다:
  - (a) `auth_service.full_crud_effective_fxx(user_id, fxx)` — 대상 계정이면 `_FULL_CRUD_BUSINESS_FXX`(F11~F19/21~29/31~39/41~49/51~62, **관리자 F18/F18r/F50/F5xe/F90~F92 제외**) 전부 `O` 로 승격한 새 dict 반환(원본 비파괴). 비대상 계정은 원본 그대로.
  - (b) 이 효과 매트릭스를 `_resolve_role_and_permissions_async`(→ permissions) 와 `build_fxx_caps_from_matrix`(→ fxx_caps) 에 주입. **`login_profile`·`license_keys` 는 *원본* 매트릭스로 산출** → `navUiState`(메뉴 가시성)는 permissions·fxx_caps 를 보지 않으므로 **메뉴 구성 무변경**(관리자 메뉴 계속 숨김, 부서계정 셸=accounting 유지).
  - (c) **불변식**: 슈퍼유저가 아니다(`role=operator`, `permissions` 에 `'*'` 없음) → `hcode` 행 격리(DSN-DEC-12) 유지 = 자기 테넌트 데이터에 한해 CRUD. 관리자 플랫폼 Fxx 제외 → 유저 생성/감사 등 관리자 행위로 권한 상승 없음.
  - (d) 대상 계정은 `BLS_FULL_CRUD_LOGIN_IDS`(쉼표 구분, `_admin_whitelist_ids` 와 동일 env 정책: 미설정→`{'경리부'}` / 빈문자열→비활성 / 콤마→그 값) 로 운영 조정 가능.
  - (e) `auth.py _make_token_pair` 의 JWT `permissions` 절단 한도 **30→64** (상수 `_MAX_PERMISSIONS`). 업무 write 코드(`return.write`·`settlement.*` 등 ~44키)가 `[:30]` 절단에 떨어져 프론트 `deriveScreenCaps` permissions 폴백에서 `canWrite=false` 회귀 내는 것을 차단(일반 계정은 30키 미만이라 무영향, fxx_caps 가 이미 토큰 주 크기 요인).
- **배경/근거**: 백엔드 업무 라우터 대부분(outbound/inbound/returns/settlement/inventory/transactions)은 라우터 레벨 `require_server_ownership` 만 있고 쓰기 권한 가드가 없어 인증 사용자에게 이미 열려 있다. 실제 편집 차단은 (1) 프론트 버튼 상태(`useScreenCaps().canWrite`) 와 (2) masters.py 의 `require_fxx_write(F11~F17)`/`require_permission("master.write")` 뿐. 따라서 경리부에 **fxx_caps(업무 셀 write=true) + permissions(업무 write 코드)** 를 동시 부여하면 양 가드와 프론트 캡을 모두 통과한다. `deriveScreenCaps` 우선순위 2(`fxxCaps[licenseFkey]`)는 셀 존재 시에만 적용되므로 fxx_caps 를 **전 업무 키 포함**으로 만드는 것이 핵심.
- **부수 수정(form-registry licenseFkey 정합)**: Delphi `Menu5xxClick` 의 `DBGrid.ReadOnly` O/R 토글 = 편집 가능 그리드인 `Sobo51`(F51 반품재고변경)·`Sobo54`(F54 일별입고내역서)·`Sobo55`(F55 일별반품내역서) 에 `licenseFkey` 부착(O→canWrite). `Sobo61`(도서별판매)은 Delphi `Menu601` 이 ReadOnly 토글 없는 읽기전용 리포트(키 F61)이므로 부착하지 않음.
- **수용 기준 (DoD)**: ① `test/test_auth_full_crud_accounting.py`(10) PASS — 효과 매트릭스 승격/관리자 키 제외/원본 비파괴/permissions·fxx_caps 정합/env 정책/login_profile 보존. ② `test/test_screen_caps_static.py`(6) PASS — `test_sidebar_visibility_is_matrix_driven`(매트릭스 visible 사용 + `canAccessScreen` 재유입 가드). ③ `test/test_fxx_caps_jwt_merge.py`·`test_master_fxx_write_guards.py`·`test_auth_fxx_*`·`test_account_menu_matrix_visibility.py`·`test_menu_visibility_show_first.py` 무회귀(총 79 PASS). ④ `cd 도서물류관리프로그램/frontend && npx tsc --noEmit` exit 0.
- **위험 / 보완**: (i) 권한 변경은 JWT 재발급(재로그인 또는 `/api/v1/auth/refresh`) 후 반영 — 리프레시 경로도 동일 승격 적용. (ii) 동일 `Gcode='경리부'` 가 여러 테넌트에 존재해도 hcode 격리로 각 테넌트 자기 데이터에 한정 — over-broad 아님. (iii) 관리자 화면 추가 시 해당 Fxx 가 `_FULL_CRUD_BUSINESS_FXX` 에 들지 않도록 유지(권한 상승 차단).
- **결정자**: 메인개발자 + 사용자 (2026-06-20 "경리부 CRUD 전면 활성화" 명시 요청)
- **참조**: `도서물류관리프로그램/backend/app/services/auth_service.py`(`full_crud_effective_fxx`/`_FULL_CRUD_BUSINESS_FXX`/`_full_crud_login_ids`/`is_full_crud_account` + 로그인·리프레시 경로), `.../backend/app/routers/auth.py`(`_MAX_PERMISSIONS=64`), `.../frontend/src/components/app-shell/sidebar.tsx`(`isVisibleForm` 환원), `.../frontend/src/lib/form-registry.ts`(Sobo51/54/55 licenseFkey), `WeLove_FTP/도서유통-New/도서유통/chul_09(위러브)/Chul.pas`(Menu1xx/5xxClick + Base01.pas `Seek_Uses`), DEC-058(부분 환원), DEC-056(Id_Logn Fxx 어댑터), DEC-RBAC-04(fxx_caps 정본)

### DEC-067: CJ대한통운 택배 표준 API 연동 — 서버사이드 프록시 + 목업 1차

- **일자**: 2026-06-21
- **결정 사항**: 택배관리(`/shipping/courier`)에 CJ대한통운 택배 표준 API(Developer Guide V3.9.4)를 붙인다. (A) **모든 CJ 호출은 서버사이드 전용** — `CJ-Gateway-APIKey`·계약 식별자(`CUST_ID`/`BIZ_REG_NUM`)는 `BLS_CJ_*` env 로만 두고 프론트에 절대 노출하지 않는다(프론트는 우리 백엔드 `/api/v1/courier/cj/*` 만 호출). 근거: 브라우저 직호출은 키 탈취·CORS 문제 → JS SDK 대신 Python 서버 클라이언트 채택. (B) **인증 2단계** — 헤더 API Key + `ReqOneDayToken`(24h) 토큰을 `cj_client` 가 모듈 캐시(만료 1분 전 갱신, 1초 2회 금지 정책 준수)로 관리하고 토큰발행 외 전 API 의 `DATA.TOKEN_NUM` 에 동봉. (C) **목업 1차** — 키 미설정(또는 `BLS_CJ_API_ENABLED=0`)이면 `cj_client.is_enabled()=False` → **HTTP 0건, 가이드 스키마 정합 결정적 mock 응답**(운송장번호=`'65'`+seed해시 8자리, 화물상태코드 1.2.1 매핑). 키 확보 후 `=1` 로 켜면 동일 인터페이스로 실연동. (D) **캐리어 추상화** — 기존 `delivery_dispatch_service.refresh_dispatch` 의 한진 분기와 동형으로 `carrier=='cj'` 분기 추가, 운송장/상태는 동일 dispatch state(JSON)에 저장(provider 무관 단일 모델). (E) **합성키 정합** — 예약 `CUST_USE_NO`(취소 기준 PK) = 우리 dispatch_id(`gdate|hcode|gcode|jubun|gjisa`). 자가출력 흐름(`ReqInvcNo`→`RegBook` `PRT_ST='02'`).
- **범위(1차, 일반업체 패키지)**: `ReqOneDayToken`·`RegBook`(예약접수)·`CnclBook`(예약취소)·`ReqOneGdsTrc`(운송장 상품추적)·`ReqInvcNo`(운송장발번)·`ReqAddrRfnSm`(주소정제). 중개(Brkr*)·예약기준 대량추적(`ReqMssGdsTrc`/`RcvMssGdsTrcCnfrm`)은 후속.
- **업무규칙 반영**: 예약취소 불가 조건(운송장 스캔/출력 후)·예약 직후 추적불가(실물 스캔 이후)·단건 접수(대량도 단건 반복) — 화면 버튼 상태·후속 구현에 반영.
- **수용 기준 (DoD)**: ① `test/test_courier_cj_mock.py`(6) PASS — mock 모드 HTTP 0건·예약/취소/추적/주소정제·dispatch 상태(`carrier='cj'`,`booked`/`cancelled`)·전화 3분할. ② `npx tsc --noEmit` exit 0. ③ `app.main` import OK(라우터 등록). ④ probe 매트릭스에 `courier.cj_status` 등록.
- **위험/보완**: (i) dispatch state 는 로컬 JSON(단일 인스턴스 가정) — 멀티 인스턴스 운영 시 DB 백킹 후속. (ii) 토큰 401 시 1분 후 재발급 정책은 캐시 만료로 처리, DDoS 차단 회피 위해 동시요청 락. (iii) RegBook 보내는분(SENDR)·정확한 수취인 주소는 회사 설정/마스터 보강 후속(목업은 메모·라인값으로 best-effort).
- **결정자**: 메인개발자 + 사용자 (2026-06-21 "1차 API Key 미확보 → 목업 우선 구현" 요청)
- **참조**: `도서물류관리프로그램/backend/app/services/carriers/cj_client.py`, `.../app/services/cj_booking_service.py`, `.../app/routers/courier_cj.py`, `.../app/services/delivery_dispatch_service.py`(`carrier=='cj'`·`set_dispatch_status`), `.../app/core/config.py`(`CJ_*`), `.../frontend/src/lib/courier-cj-api.ts`, `.../frontend/src/app/(app)/shipping/courier/page.tsx`(CJ 패널), `CJLAPI-택배 표준 API Developer Guide-V3.9.4.pdf`, `debug/probe_backend_all_servers.py`(`courier.cj_status`)

### DEC-068: 기초관리(거래처/입고처/저자/도서) 엑셀 입출력 + 헤더정렬 + 도서 전자책/발행일

- **일자**: 2026-06-27
- **결정 사항**: 4개 기초관리 목록 화면(Sobo11/12/13/14)에 다음을 추가/수정한다.
  - **(A) 엑셀 저장(export)** — 공용 `masters_excel.py`(openpyxl) + `GET /api/v1/masters/exports/{customer,inbound-vendors,authors,book}.xlsx`. hcode 격리는 기존 `list_*` 서비스 재사용, `collect_all_rows` 가 `page.has_more` 로 ceil=500 페이지를 끝까지 모음(`EXPORT_MAX_ROWS=100000` 안전상한). **저장 대상 = 현재 화면 검색 필터 결과**(프론트가 필터+정렬 동봉). 파일명은 클라이언트가 `거래처목록_YYYYMMDD.xlsx` 로 날짜 접미.
  - **(B) 거래처 필드선택** — 거래처만 상세 전체 32필드를 체크박스로 선택 저장(`GET /exports/customer-fields` 단일 카탈로그 + `?fields=` CSV). 라벨 정본 = `customer-detail-form.tsx`(DFM 캡션 정정: **Gposa=대표자/Guper=업태/Gjomo=종목**, Grat1~6=위탁/현매/매절/납품/특별/기타). 팝업은 `resize` 가능. **PK(거래처코드)는 항상 강제 포함**(프론트 disabled 체크 + 백엔드 `select_customer_columns` 가 `gcode` 무조건 주입) — 업로드 역반영 시 행 식별 필수.
  - **(C) 엑셀 업로드(역반영)** — 다운로드 서식 그대로 재업로드 → PK(코드)로 행 식별, 수정분을 기존 `update_*` 서비스로 반영(업서트 아님, 존재 행만). `POST /api/v1/masters/imports/{...}.xlsx`(multipart), **PATCH 와 동일 Fxx 가드(F11~F14)+audit**. 전화/주소 **합본 컬럼은 역분해 불가 → import 제외**(거래처는 전화1/2·주소1/2 개별이라 거의 전 필드 역반영). 행별 부분실패 허용 + 요약 리포트(updated/unchanged/not_found/error).
  - **(D) 헤더 클릭 정렬** — `DataGrid` 에 opt-in `sort`/`onSortChange`/컬럼 `sortable` 추가(LSP, 기존 호출자 무변경). 백엔드 `list_*` 에 `sortBy`/`sortDir` + **화이트리스트 `_order_by_clause`**(허용 key만, 그 외 default — SQL 주입 차단, 동률 시 PK 보조정렬). 정렬은 export 에도 동봉.
  - **(E) 도서 발행일 필터 버그 수정** — `Date1` 이 `YYYY-MM-DD`/`YYYY.MM.DD`/`YYYYMMDD` 혼재 저장이라 입력의 `-` 만 제거해 비교하면 `'2026-01-01' >= '20260101'` 이 거짓이 되어 범위 행 누락. **양쪽 모두 구분자 제거(중첩 REPLACE, 3.23 호환) 후 숫자 비교** + 빈 Date1 제외.
  - **(F) 거래처 export 중복행 버그 수정** — `list_customer_master_full` 의 G1_Gbun 이중 LEFT JOIN 이 멀티테넌트 Gcode 충돌로 행을 2배 증식(상세 단건은 rows[0] 라 은폐). **JOIN 제거 + G1_Gbun 1회 조회 후 Python 맵으로 구분명 1:1 해석**(목록 JOIN 금지 원칙 = inbound 와 동일).
  - **(G) 신규 도서 전자책 카드** — 레거시 `G4_Book` 은 전 컬럼이 용도 확정(bigo3=전자책 플래그)이라 전자책 전용 ISBN/가격을 둘 빈 컬럼이 없음 → **신규 사이드 테이블 `G4_Book_Ebook`(Hcode,Gcode,Eisbn,Eprice)** 으로 분리(레거시 스키마 무변경). `book_ebook_service`(CREATE IF NOT EXISTS + REPLACE INTO, 3.23 호환, scope_hcode 격리). 책 create/detail/update 에 wiring, 폼에 「전자책」 카드(전자책 여부+ISBN+가격).
- **배경/근거**: (B)/(C)/(F)/(G) 모두 멀티테넌트 hcode 격리·MySQL 3.23 무파괴·레거시 DDL 회피 제약을 우선. JOIN 행증식·날짜 표기 혼재·합본 컬럼 비가역성은 레거시 데이터 특성상 실측 버그. 전자책 저장은 **사용자 선택(별도 사이드 테이블)**.
- **대안**: 전자책 — (1)G4_Book 신규 컬럼 ALTER (2)기존 여유 컬럼 재사용 → 사용자가 (3)사이드 테이블 선택. 정렬 — DataGrid 클라이언트 정렬(전 페이지 미반영) 대신 서버 ORDER BY.
- **영향**: `masters.py`(+exports/imports/ebook), 신규 `masters_excel.py`·`book_ebook_service.py`, `masters_service.py`(sort_by/sort_dir·list_customer_master_full·발행일), `data-grid.tsx`(sort opt-in), 4 목록 페이지 + book 폼/new/[gcode] + `master-api.ts` + `download.ts`/`focus-advance.ts`. requirements 에 `openpyxl` 고정. 회귀 `test/test_masters_excel_export.py`(17). probe 에 export GET 등록. **별도: 신규 입력폼 Enter=다음칸 이동**(`focus-advance.ts`, 4 마스터 폼 + 출고접수 헤더, 콤보/그리드는 가드/제외).
- **결정자**: 메인개발자 + 사용자 (2026-06-27 일련 요청)
- **참조**: `도서물류관리프로그램/backend/app/services/{masters_excel,book_ebook_service}.py`, `.../app/services/masters_service.py`(`list_customer_master_full`·`_order_by_clause`·발행일 REPLACE), `.../app/routers/masters.py`(exports/imports/ebook), `.../frontend/src/components/data-grid/data-grid.tsx`, `.../src/lib/{download,focus-advance,master-api}.ts`, `.../src/components/master/{master-import-button,book-detail-form}.tsx`, `test/test_masters_excel_export.py`

### DEC-069: 배포-안전 저장소 상대 경로 탐색 (parents[N] 고정 인덱스 금지 + 계약 yaml 번들 사본)

- **일자**: 2026-07-03
- **결정 사항**: 백엔드에서 저장소 상대 리소스(허브 계약 yaml, 허브 산출물 IR 등)를 찾을 때 `Path(__file__).parents[N]` **고정 인덱스 접근을 금지**하고, 신규 공용 헬퍼 `app/core/repo_paths.find_repo_file(relpath, start=)` (상위 디렉토리 순차 탐색, 미발견 시 `None`) 만 사용한다. 아울러 런타임 필수 계약인 `migration/contracts/print_sales_statement.yaml` 은 **백엔드 번들 사본** `backend/data/contracts/print_sales_statement.yaml` 을 두고, 탐색 우선순위 = 허브 정본(개발 중첩 배치) → 번들 사본(단독 배포) → 내장 기본 프로필(graceful) 로 한다. 편집은 반드시 허브 정본에서 하고 사본에 복사 — 두 파일의 파싱 내용 동기화는 회귀 테스트가 강제한다. Dockerfile 에는 `fonts-nanum` 을 추가해 한글 글리프 tofu 를 차단한다(폰트 README 의 apt 경로 채택).
- **배경/근거**: 거래명세서 PDF 인쇄가 로컬은 정상, Render 배포에서 500. 원인 = Render Docker 는 `backend/` 만 빌드해 모듈 경로가 `/app/app/services/...` (조상 4개)가 되고, `sales_statement_print_profile.py` 의 모듈 레벨 `parents[4]` 가 **IndexError** → 모듈 임포트 자체가 실패 → 삼련/일괄/자동출력 전부 500. `print_template_registry._resolve_ir_path` 의 동일 패턴도 잠재 500 (try 블록 밖 호출). WeasyPrint 미설치 503 graceful 경로는 이미 있었으나 경로 깊이 크래시는 커버하지 못했다.
- **대안**: (1) Docker 에 허브 전체 포함 — 이미지 비대 + 제품 단독 배포 원칙 위배. (2) env 로 계약 경로 주입 — 운영 설정 누락 시 재발, 기본값이 안전해야 함. (3) 계약 yaml 정본을 제품 레포로 이동 — CLAUDE.md 상 customer_variants 정본은 허브 `migration/contracts` 이므로 사본+동기화 가드 채택.
- **영향**: `backend/app/core/repo_paths.py` 신규, `backend/app/services/sales_statement_print_profile.py`(_contract_path 탐색), `backend/app/services/print_template_registry.py`(_resolve_ir_path → find_repo_file, 미발견 None = manual 빌더 fallback), `backend/data/contracts/print_sales_statement.yaml` 번들 사본, `backend/Dockerfile`(+fonts-nanum). 회귀 가드 `test/test_print_repo_paths_deploy.py` — 얕은 경로 무예외 / yaml 미발견 기본 프로필 / 번들↔허브 파싱 동기화 / `parents[4-9]` 재유입 금지 스캔 4종. 잔여 알려진 제약: `.dockerignore` 가 `data/tenant_print/` 를 제외하므로 Render 에서 도장 오버레이는 미출력(코드는 graceful None) — 운영 디스크/외부 저장소 이관은 별도 운영 작업.
- **보강 (2026-07-03, 같은 날 2차)**: 경로 수정 배포 후 500 → **503 PR_ENGINE_UNAVAILABLE** 로 전환 확인(설계된 graceful). 잔여 원인 = Dockerfile apt 목록이 구세대 WeasyPrint(<53) 기준(libcairo2/libgdk-pixbuf)이라 **>=53 이 dlopen 하는 `libpangoft2-1.0-0`(+fontconfig)/`libharfbuzz0b`/`libharfbuzz-subset0` 누락**. apt 목록 보완 + **빌드 타임 엔진 검증**(`RUN python -c "from weasyprint import HTML; ...write_pdf()"` — 실패 시 빌드 자체가 죽어 Render 가 직전 Live 유지, 런타임 503 조기 차단) 추가. 가드: `test_print_repo_paths_deploy.py::DockerfileEngineGuardTests` (apt 필수 5종 + 빌드 검증 존재).
- **결정자**: 메인개발자 + 사용자 (2026-07-03 운영 500 보고)
- **참조**: `도서물류관리프로그램/backend/app/core/repo_paths.py`, `.../app/services/{sales_statement_print_profile,print_template_registry}.py`, `.../backend/data/contracts/print_sales_statement.yaml`, `.../backend/Dockerfile`, `test/test_print_repo_paths_deploy.py`, DEC-037(WeasyPrint 단일 엔진)

### DEC-070: 내정보 preferences DB 정본화 (Web_User_Prefs 사이드 테이블)

- **일자**: 2026-07-03
- **결정 사항**: 내정보(preferences — 자동출력/테두리/테마/공급자정보 등)의 정본을 파일(`backend/data/user_profiles.json`)에서 **로그인 데이터 서버의 신규 사이드 테이블 `Web_User_Prefs`** (PK=(Hcode,UserId), Prefs TEXT, 3.23 호환 CREATE IF NOT EXISTS + REPLACE INTO — `grid_prefs_service`/DEC-068 G4_Book_Ebook 과 동일 패턴)로 옮긴다. 파일은 동기 렌더 경로(`user_profile_service.get_profile` — 인쇄 HTML 빌더가 사용)를 위한 **캐시**로 유지: GET /me/profile 이 DB 정본 → 파일 캐시 동기화, PATCH 는 파일+DB 이중 기록, DB 무행 + 파일 저장분 존재 시 1회 back-fill 승격. DB 실패는 전부 graceful(파일 fallback, 200 유지).
- **배경/근거**: Render Docker 의 컨테이너 파일시스템은 임시라 재배포/재시작마다 파일이 이미지 원본으로 리셋 — 사용자가 내정보에서 자동출력을 켜고 저장해도 다음 배포에 소실("저장이 안 됨" 2026-07-03 보고, 당일 배포 4회로 증폭). 격리: 모든 SQL Hcode+UserId 동시 필터(hcode 감사 info 등급 통과).
- **대안**: (1) Render Persistent Disk — 유료 + zero-downtime 배포 상실. (2) 파일을 git 에 주기 커밋 — 운영 데이터의 레포 유입, 부적절. (3) 채택: 기존 사이드 테이블 패턴 재사용(추가 인프라 0).
- **영향**: `backend/app/services/user_prefs_db.py` 신규, `backend/app/routers/me.py`(GET 동기화/back-fill + PATCH 이중 기록). 회귀 `test/test_user_prefs_db_persistence.py` 9종. **잔여**: 업로드 로고(`data/uploads/`)·테넌트 도장(`data/tenant_print/`)은 여전히 임시 FS/이미지 제외 — 영속화 별도 과제.
- **결정자**: 메인개발자 + 사용자 (2026-07-03 저장 유실 보고)
- **참조**: `도서물류관리프로그램/backend/app/services/{user_prefs_db,grid_prefs_service,user_profile_service}.py`, `.../app/routers/me.py`, DEC-068(사이드 테이블 선례), DEC-069(임시 FS 배포 함정)

### DEC-071: 일괄 출고요청 (거래명세서·출고현황 화면 — 대기 전표 선택 접수 전이)

- **일자**: 2026-07-03
- **결정 사항**: 신규 생성 화면에서 출고요청 없이 **신청만 한(대기, Yesno='') 전표**를 거래명세서(Sobo21)·출고현황(Sobo24) 화면에서 **선택 일괄 출고요청(접수 '0' 전이)** 할 수 있게 한다(레거시 기능 동등 — 사용자 확인). 백엔드는 신규 `PATCH /api/v1/outbound/orders/batch/request` (keys ≤200, 기존 `outbound_service.request_dispatch` 재사용, bounded gather 동시 3, keys 순서 보존, 항목 단위 부분 실패 not_found/error 보고, 건별 audit). **단건 라우트보다 먼저 등록**해 `batch` 가 order_key 로 매칭되지 않게 한다. 프론트: 거래명세서 = 기존 다중선택 재사용 + 「대기 N건 출고요청」 버튼(`Sobo21.BulkRequestDispatch`), 출고현황 상세 뷰 = 체크박스 선택열 신설 + 툴바 버튼(`Sobo24.BulkRequestDispatch`) — 두 화면 모두 **대기(pending) 상태만 집계/전송**.
- **배경/근거**: 상태기계(DEC-009~012/065): 저장=대기('') → 출고요청=접수('0') → 완료('1') / 취소('2'). 단건 전이 API 는 기존 존재 — 화면 단위 일괄 실행 UI 와 배치 API 가 공백이었다. Render↔한국DB RTT 때문에 클라이언트 단건 반복 대신 서버 배치 + 병렬(동시 3, batch.pdf 와 동일 보수치).
- **영향**: `backend/app/routers/outbound.py`(+BatchRequestBody/Response·request_dispatch_batch), `frontend/src/lib/outbound-api.ts`(+requestDispatchBatch), 거래명세서/출고현황 page.tsx. 회귀 `test/test_outbound_batch_request.py`(라우터 4 + 화면 정적 2). 신규 SQL 0(기존 서비스 재사용).
- **결정자**: 메인개발자 + 사용자 (2026-07-03 레거시 기능 요청)
- **참조**: `도서물류관리프로그램/backend/app/routers/outbound.py`, `.../frontend/src/app/(app)/transactions/{sales-statement,outbound-status}/page.tsx`, DEC-065(화면 내 신규추가), DEC-033(다중 DB)

### DEC-072: 출력 결과 추적 — 출력된 건만 완료 전이 + Web_Print_Log 이력 + 자동출력 조회창

- **일자**: 2026-07-03
- **결정 사항**: ① **출력이 실제 완료된 건만 접수→완료 전이** — 거래명세서 단건/일괄 PDF 응답에 `X-Printed-Keys` 헤더(PDF 에 실제 포함된 전표 키의 base64 UTF-8 JSON — Gjisa 한글 대비)를 실어, 프론트(수동 인쇄·자동출력 모니터)는 이 목록에 대해서만 `completeSalesStatement` 를 호출한다(헤더 부재 구버전만 기존 동작 fallback). ② **상세 출력 이력** — 신규 사이드 테이블 `Web_Print_Log`(Seq AUTO_INCREMENT PK, Hcode/UserId/PrintedAt/Kind(single|batch|auto)/Gdate/Jubun/Gjisa/Gcode/CustomerName/LineCount/Amount, 3.23 호환 append 전용, 기록 실패는 인쇄 비차단). PDF 생성 성공 시 전표당 1행 기록, `GET /api/v1/print/sales-statement/print-log`(hcode 격리·최신순) + 자동출력 모니터 「서버 출력 이력」 패널·세션 로그 전표번호 표기. PDF 요청에 `source=auto|manual` 로 kind 구분. ③ **자동출력 조회창** — `received-today` 에 `days`(1~30, 기본 1) 파라미터: 일괄 출고요청(DEC-071)은 과거 거래일자 전표도 접수 전이하므로 Gdate=당일 필터로는 자동출력이 놓친다 → 모니터는 `days=7` 로 폴링(완료 전이 후 목록에서 빠지므로 중복 인쇄 없음, 세션 dedup 병행). ④ 출고현황 목록 뷰 라인에 거래처명 컬럼 추가(G1_Ggeo 런타임 lookup — 목록 JOIN 금지 유지).
- **배경/근거**: 2026-07-03 보고 — "접수요청 후 출력이 완료된 건만 완료로", "어떤 건이 출력되었는지 자세한 기록", "다건 접수요청 시 출력 검증", "출고현황 거래처 필드 누락". 기존 흐름은 인쇄 트리거 직후 선택 전체를 완료 전이해 PDF 미포함(자료 없음) 건도 완료 처리될 수 있었다.
- **영향**: `backend/app/routers/print.py`(+헤더/이력/print-log GET/source), `backend/app/services/print_log_db.py` 신규, `backend/app/routers/transactions.py`(received-today days), `backend/app/services/transactions_service.py`+`models/inquiry.py`(라인 customer_name), 프론트 `print-api.ts`(+decodePrintedKeysHeader·printPdfFromUrl 반환·getSalesStatementPrintLog), `inquiry-api.ts`(days), 거래명세서/자동출력 모니터/출고현황 page.tsx. probe 매트릭스 `print.sales_statement_print_log` 등록. 회귀 `test/test_print_result_tracking.py`(11 — 멀티키 헤더/누락 제외/kind/이력 SQL/days 창/모니터 정적).
- **결정자**: 메인개발자 + 사용자 (2026-07-03 연속 요청)
- **참조**: DEC-071(일괄 출고요청), DEC-070(사이드 테이블 패턴), `도서물류관리프로그램/backend/app/services/print_log_db.py`

### DEC-073: 로고·도장 이미지 DB 영속화 (Web_Print_Assets — DEC-070 패턴 확장)

- **일자**: 2026-07-04
- **결정 사항**: 업로드 로고(`data/uploads/`, StaticFiles 서빙)와 테넌트 도장(`data/tenant_print/`)의 정본을 신규 사이드 테이블 **`Web_Print_Assets`**(PK=(Hcode,UserId,Kind), `DataB64` MEDIUMTEXT base64 — 바이너리 charset 이슈 회피, 3.23 호환, 상한 768KB)로 옮긴다. 로고 = (hcode, user_id, 'logo'), 도장 = ('', '', 'sales_statement_seal') — **도장의 서버(테넌트) 단위 시맨틱은 파일 모델 그대로 보존**(hcode 단위 분리는 필요 시 후속). 파일은 캐시: 업로드/삭제 시 파일+DB 이중 기록, 조회 경로에서 히드레이션 — 로고는 `GET /me/profile` 에서 파일 부재 시 DB 복원 + 구버전 파일 보유 시 1회 back-fill, 도장은 `hydrate_seal_from_db`(프로세스당 서버별 1회 — RTT 절약)를 seal-status/미리보기/거래명세서 단건·일괄 PDF 렌더 직전에 호출. 모든 DB 실패는 graceful(자산 없는 표시/출력으로 저하).
- **배경/근거**: Render 임시 FS + `.dockerignore` 제외로 재배포 시 로고 소실, 도장은 운영 이미지에 아예 미포함(DEC-069 잔여 과제). 이로써 **Render 에서도 도장 오버레이가 인쇄에 복원**된다.
- **대안**: Render Persistent Disk(유료·zero-downtime 상실) / 이미지에 자산 포함(git 에 운영 바이너리 유입) → 기존 사이드 테이블 패턴 재사용 채택.
- **영향**: `backend/app/services/web_assets_db.py` 신규, `tenant_print_assets.py`(+persist/delete/hydrate), `user_profile_service.py`(+read_logo_bytes — 경로 이탈 가드), `routers/me.py`(로고·도장 이중 기록 + 히드레이션, 도장 업로드 응답 `persisted_db`), `routers/print.py`(렌더 전 도장 히드레이션). 회귀 `test/test_web_assets_persistence.py`(11 — base64 왕복/상한/graceful/히드레이션 실복원·1회성/이중 기록/렌더 훅). hcode 감사 strict exit 0 유지.
- **결정자**: 메인개발자 + 사용자 (2026-07-04 후속 과제 지시)
- **참조**: DEC-070(Web_User_Prefs), DEC-069(임시 FS 함정), `도서물류관리프로그램/backend/app/services/web_assets_db.py`

### DEC-074: 양식지 인쇄 위치 보정 (preprinted_calibration — 계약 yaml 실측 캘리브레이션)

- **일자**: 2026-07-04
- **결정 사항**: 미리 인쇄된 A4 양식지 위에 텍스트만 출력할 때(테두리 OFF) 물리 용지와 텍스트 위치가 어긋나는 문제의 보정을 **계약 yaml 데이터**로만 제어한다(코드 분기 0). `print_sales_statement.yaml profiles.<key>.preprinted_calibration = { offset_top_mm, offset_left_mm, line_row_height_mm }` — offset 양수=아래/오른쪽(body transform: translate), `line_row_height_mm > 0` 이면 표 행 높이 고정(0=폰트 자동). 삼련(.tri-lines)·A4 이련(.a4-lines) 두 빌더 공통 헬퍼 `_preprinted_calibration_css` 로 적용하며, **borders ON/OFF 지오메트리를 단일화** — 테두리 ON 시험 인쇄로 측정한 어긋남(mm)이 양식지 모드에 그대로 유효하다. 서버(회원사)별 용지 차이는 `profiles.<key>` 오버라이드 + `server_profile_map` (customer_variants 원칙 동일).
- **배경/근거**: 2026-07-04 보고. 현 지오메트리는 CSS mm 근사 구현이며 **물리 양식지의 실측 좌표 스펙은 리포에 없음** — 원본 입력(용지 사진/샘플)은 세션 첨부로 소실. 전체 재입력 대신 "시험 인쇄 → 상/좌 어긋남 실측 → yaml 보정" 루프로 수렴시킨다.
- **대안**: (1) CSS 상수 직접 수정 — 회원사별 용지 차이에 코드 분기 유발. (2) .frf 레거시 좌표 재추출 — 물리 용지가 레거시 인쇄본이라는 보장이 없고 프린터 여백 오차는 어차피 실측 필요.
- **영향**: `backend/app/services/transactions_service.py`(+_preprinted_calibration_css, 두 css 조립), `migration/contracts/print_sales_statement.yaml` + 백엔드 번들 사본(동기). 회귀 `test/test_preprinted_calibration.py`(6 — 오프셋/행높이 반영, ON/OFF 동일 지오메트리, 0=무배출, 불량값 graceful, yaml 블록).
- **보강 (2026-07-04, 실측 반영)**: 사용자 제공 양식지 사진을 픽셀 계측(괘선 검출, 스케일 앵커 = 3련 섹션 주기 582.3px=99mm → 5.882px/mm, 원근오차 0.6%)해 **실측 정본** `analysis/print_specs/sales_statement_triplicate_form.md`(+사진 사본 assets/)로 영구 기록. 종전 렌더와의 주요 편차: 표 폭 194→**172.6mm**, 데이터 행 4.0→**4.45mm**, 표 헤더 4.7→**6.0mm**, 섹션 피치 93→**99mm**(2·3련 누적 -6/-12mm 어긋남의 주범). 캘리브레이션 노브 확장: `table_width_mm`(중앙 배치+flex 스트레치 해제)/`line_col_widths_mm`(7열, 도서명 auto — **yaml `no:` 는 boolean 이라 반드시 `"no":` 인용**)/`line_header_height_mm`/`field_row_height_mm`/`section_pitch_mm`+`section_gap_mm`/`page_margin_v_mm`(3×99=297 충족 위해 상하 0). 기본 프로필에 실측값 기입, 잔여 미확정(페이지 좌우 절대 위치·섹션 상단 오프셋 — 사진 크롭으로 미상)은 테두리 ON 시험 인쇄 후 offset 으로 확정.
- **결정자**: 메인개발자 + 사용자 (2026-07-04 위치 불일치 보고 + 양식지 사진 제공)
- **참조**: DEC-037(WeasyPrint), DEC-065(삼련), `analysis/print_specs/{c7_phase1,sales_statement_triplicate_form}.md`

### DEC-075: 삼련 마지막 련 auto-height (3×section_pitch_mm > A4 297mm 2페이지 분리 수정)

- **일자**: 2026-07-04
- **결정 사항**: `legacy_triplicate` 렌더러의 `.triplicate-section:last-child`(3번째 련)에
  `height: auto; padding-bottom: 0; border-bottom-width: 0;`를 추가한다
  (`backend/app/services/transactions_service.py`
  `_render_sales_statement_legacy_triplicate_html`). 앞의 2개 련은 다음 련의 시작 위치를
  맞추기 위해 `section_pitch_mm` 고정 높이 박스가 필요하지만, 마지막 련은 뒤에 아무것도
  없으므로 고정 높이가 불필요 — 실제 내용 높이만 차지하게 하고, 물리 양식지에 대응하는
  기준선이 없는 하단 padding/border 여백도 제거한다.
- **배경/근거**: DEC-074 보강(2026-07-04, PDF 검증)에서 스캔 실측 기반 `section_pitch_mm`을
  99→**99.7mm**로 갱신했으나, `page_margin_v_mm=0`에서도 `3 × 99.7mm = 299.1mm >
  297mm`(A4)가 되어 3련 인쇄 시 3번째 련이 2페이지로 밀려나는 회귀가 발생(사용자 보고:
  "3륜 출력하면 2페이지로 출력된다"). **1차 수정(`height: auto`만)은 불충분했다** —
  WeasyPrint 로 실제 렌더링해 박스 트리를 실측한 결과, 3번째 련의 실제 필요 높이는
  border-box 기준 **98.43mm**(content 94.38 + padding 3.2 + border 0.85)인데 앞 2련이
  `2 × 99.7mm = 199.4mm`를 차지해 잔여 공간은 **97.6mm**뿐 — **0.83mm 초과**로
  `page-break-inside: avoid` 가 3번째 련 전체를 다음 페이지로 밀어(스크린샷: 1페이지 하단에
  큰 공백 후 2페이지에 인수증 단독 출력) 여전히 2페이지였다. 하단 padding(1.6mm)+
  border(0.42mm)는 물리 양식지의 어떤 기준선과도 대응하지 않는 순수 렌더링 여백이라
  안전하게 제거 가능 — 제거 시 실측 필요 높이가 96.83mm(또는 padding+border 모두 제거 시
  96.4mm)로 줄어 97.6mm 안에 들어간다. 1·2련의 피치 앵커(0mm, 99.7mm 시작)와 실측
  지오메트리(DEC-074)는 그대로 유지된다.
- **대안**: (1) `section_pitch_mm`을 99mm로 되돌림 — 실측 정본(DEC-074 PDF 검증, ±0.35mm 오차)을
  폐기하게 되어 2·3련 정렬이 다시 어긋남. (2) `page_margin_v_mm`을 음수로 — `@page` 음수 마진은
  프린터/브라우저 호환성이 불확실. 마지막 련의 하단 padding/border 만 제거하는 편이 실측값을
  보존하면서(1·2련·3련의 상단 정렬 기준은 전혀 건드리지 않음) 가장 안전하다.
- **검증 방법**: HTML 문자열 검사만으로는 실제 페이지 분할 여부를 알 수 없다는 것 자체가
  1차 수정이 불충분한 채로 통과했던 원인 — WeasyPrint 로 직접 렌더링해 `len(doc.pages)`와
  박스 트리(`position_y`/`height`)를 실측해 검증했다(로컬 확인 시
  `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:/usr/local/lib` 필요, Homebrew pango/cairo).
- **영향**: `backend/app/services/transactions_service.py`(last-child CSS 규칙 확장).
  회귀: `test/test_preprinted_calibration.py`(last-child 규칙 문자열 갱신 + 계약 yaml
  `section_pitch_mm × 2 ≤ 297mm - 2×page_margin_v_mm` 산술 가드), `test/test_sales_statement_triplicate.py`
  신규 `test_legacy_triplicate_renders_single_pdf_page`(WeasyPrint 실렌더 후 `len(doc.pages) == 1`
  실측 검증, borders on/off 모두 — 네이티브 의존성 없는 환경에서는 graceful skip).
- **결정자**: 메인개발자 (2026-07-04 사용자의 "3륜 2페이지 출력" 버그 보고 + 재현 스크린샷 확인 후)
- **참조**: DEC-074(양식지 캘리브레이션), `analysis/print_specs/sales_statement_triplicate_form.md`

### DEC-076: 삼련 반품처 세로문구 — WeasyPrint writing-mode 미지원 대체(글자별 줄바꿈)

- **일자**: 2026-07-04
- **결정 사항**: 삼련(`legacy_triplicate`) 반품처 안내문구(`.vert-note`, 예: "※반품처 천일화물
  파주광탄")를 CSS `writing-mode: vertical-rl` 대신 **글자 단위 `<br>` 줄바꿈**으로 렌더한다
  (`transactions_service._vertical_note_html`). 공백 문자는 빈 줄로 남겨 의미 단위 사이 여백을
  살린다. `.vert-note` CSS 에서 `writing-mode`/`text-orientation` 선언은 제거.
- **배경/근거**: 사용자 보고 — 반품처 문구가 "※반품/처 천/일화물/파주광/탄" 처럼 여러 짧은
  줄로 뒤섞여 보임(스크린샷). 백엔드 로그(`WARNING weasyprint: Ignored 'writing-mode:
  vertical-rl' ... unknown property`)로 확인한 결과 **WeasyPrint 는 writing-mode/
  text-orientation 을 아예 지원하지 않아 조용히 무시**한다 — 실제로는 좁은 7mm 폭 열 안에서
  가로쓰기가 줄바꿈되어 여러 줄로 쪼개진 것이었다(DEC-037 이후 처음부터 있던 결함으로 추정 —
  브라우저 미리보기는 `writing-mode` 를 지원해 정상으로 보였을 것이나, 실제 인쇄 PDF 엔진은
  WeasyPrint 단일이라 미리보기-출력 간 불일치가 있었다). CSS 세로쓰기에 의존하지 않는 방식으로
  바꾸면 브라우저 미리보기와 PDF 출력이 동일해지는 부수 효과도 있다.
- **영향**: `backend/app/services/transactions_service.py`(`_vertical_note_html` 신설,
  `.vert-note` CSS 단순화). 회귀: `test/test_sales_statement_triplicate.py`
  (`test_legacy_triplicate_contains_three_sections_and_columns` /
  `test_supplier_fields_from_user_preferences_over_yaml` — 글자별 `<br>` 조인 문자열로 갱신 +
  `writing-mode`/`text-orientation` 미사용 assertNotIn 추가).
- **보강(2026-07-05, 겹침 수정)**: 세로문구가 표 오른쪽 컬럼(비고)과 겹쳐 보이는 후속 보고.
  원인: 표는 캘리브레이션으로 고정폭(182.9mm)인데 `.vert-note` 를 flex 컬럼(7mm)으로 두어
  표를 왼쪽으로 밀지 못하고 표가 세로문구 영역으로 오버플로우(표 우단 196.2mm > 문구 시작
  193.0mm). 수정: `.vert-note` 를 flex 흐름에서 빼 `.body-flex`(position:relative) 기준
  `position:absolute; right:0; width:3.4mm` 로 표 우측 잔여 폭(≈197~200mm)에 얹음 — 표는
  전폭 확보, 문구 글리프(197.2~199.3mm)가 표 우단(196.2mm)을 넘지 않아 겹침 제거(WeasyPrint 실측).
- **보강(2026-07-05, 스캔 기준 재검증·도장/세로문구 정밀 정렬)**: 사용자 A4 스캔
  (`Scan2026-07-04`, 2457×3484px=11.7px/mm)을 실측해 현 렌더와 대조(에이전트 픽셀 계측).
  **결론: 표는 이미 스캔과 ≤0.3mm 일치**(좌 14.2, 우 197.1, 폭 182.9, 행 4.52, 피치 99.7 모두
  DEC-074 값 그대로 유효 — 세로문구 수정이 표를 변형시키지 않았음을 확인). 실제 어긋남 2건만 보정:
  (1) **세로문구**: 렌더 중심 198.8mm vs 스캔 199.7mm → `.vert-note right: -0.9mm` 로 우측 이동
  (렌더 중심 199.83mm). (2) **도장**: 이전 값(top2/right2/width22)이 스캔 대비 8mm 아래·2mm 큼
  (업태/전화 위) → `seal_overlay { offset_top_mm:-4.5, offset_right_mm:-1.5, width_mm:18.5 }`
  (공급자블록 우상단 음수 오프셋) 로 등록번호/성명 상단(중심 y≈12mm, 지름 18.5mm)에 정렬
  (렌더 중심 192.9/11.9 — y·크기 스캔 일치, x 는 섹션 우측 클립 경계 200.6mm 때문에 5mm 좌측).
  추가로 **양식지(borders=off) 모드에서도 도장이 찍히도록** `.preprinted .seal-overlay
  { visibility: visible }` 예외(공급자 블록은 양식지 인쇄분이라 숨기되 도장은 문서별 오버레이).
  yaml 소스+번들 사본 동기 갱신. 회귀: `test_sales_statement_triplicate.py` 도장 테스트에 신값·
  양식지 가시성·세로문구 이동 assert 추가.
- **보강(2026-07-05, 외곽 테두리 제거 — 세로문구를 테두리 바깥으로)**: 사용자 보고 — 세로문구가
  전체 페이지 외곽 테두리 안에 갇히고 표가 그 폭에 안 맞음. 스캔 재확인 결과 **삼련엔 내용
  블록(표/공급자/거래처/푸터) 각자의 테두리만 있고 이들을 감싸는 바깥 사각형이 없다**. 렌더는
  `.triplicate-section` 이 외곽 사각형(우 202mm)을 그려 표 우측(197mm)을 지나 세로문구(199.7mm)를
  안에 가뒀다. 수정: `.triplicate-section { border: ...transparent; overflow: visible }` — 테두리
  폭 유지(box-sizing/피치 불변)로 색만 투명해 바깥 사각형 제거, overflow:visible 로 우측 여백의
  세로문구·도장이 안 잘림. 결과: 표 우측 테두리가 최외곽, 세로문구는 그 바깥 여백(스캔 동형).
  실제 인쇄(borders=off 양식지)에선 외곽선·세로문구가 원래 숨김이라 무영향 — borders=on
  미리보기/빈용지 정합용. 3련 1페이지 유지 확인.
  - **주의**: 섹션은 인라인 `style='border-color:{련색}'` 이 있어 CSS 투명을 덮어써 처음엔 외곽선이
    안 지워졌다. 인라인에서 `border-color` 제거(‑‑ink 만 유지)해야 실제로 투명 적용됨.
- **보강(2026-07-05, 헤더·푸터 좌우 정렬 — 3블록 좌단 14.2mm 일치)**: 사용자 보고 — 표가
  거래처코드 블록(위)·국민은행 푸터(아래) 보다 3.5mm 안쪽으로 들어가 좌단이 안 맞음. 스캔 실측:
  거래처코드 블록·표·푸터 좌단이 **모두 14.2mm**, 공급자 블록 우단은 표와 같은 197.1mm. 원인:
  DEC-074 의 `table_margin_left_mm=3.5` 를 **표에만** 적용해 헤더(hdr3)·푸터(foot3)가 섹션 좌단
  (10.7mm)에 남아 어긋남. 수정: `_preprinted_calibration_css` 에서 삼련일 때 `.hdr3`/`.foot3` 에도
  표와 동일한 `width=182.9mm; margin-left=3.5mm; align-self:flex-start`(flex 컬럼 stretch 방지)
  적용 → 헤더(거래처코드 좌 14.2 / 공급자 우 197.1)·표·푸터 모두 14.2~197.1 정렬. borders on/off
  공통(양식지 모드에서도 거래처코드 값이 인쇄 셀에 맞음). 회귀: `test_preprinted_calibration.py`
  에 hdr3/foot3 정렬 assert 추가.
- **결정자**: 메인개발자 (2026-07-04 세로문구 / 2026-07-05 스캔 기준 재캘리브레이션 사용자 보고 확인 후)
- **참조**: DEC-037(WeasyPrint 단일 PDF 엔진), DEC-074(양식지 캘리브레이션 정본),
  DEC-073(도장 DB 영속화), DEC-075(같은 삼련 렌더러의 페이지 분리 수정)

### DEC-077: 거래명세서 수정 저장 시 거래처(Gcode)·전표번호(Idnum) 소실 버그 수정

- **일자**: 2026-07-05
- **결정 사항**: `sales_statement_create_service.update_sales_statement` 의 desired-state diff 에서
  라인 식별키의 거래처코드(Gcode)를 **hcode(테넌트)로 잘못 채우던 버그**를 수정한다. 슬립의
  실제 거래처 Gcode 는 payload 라인에 없으므로, 현재 라인(cur_rows[0])의 Gcode 를 슬립 공통값
  `s_gcode` 로 취해 desired 키·INSERT 값에 사용한다(한 전표=한 거래처 불변식). 아울러 재삽입
  라인이 전표번호(Idnum)를 잃지 않도록 SELECT 에 Idnum 을 추가하고(`has_idnum`), 슬립 공통
  `s_idnum` 을 `_build_insert_line_sql(has_idnum=True)` 경로로 INSERT 에 함께 넣는다.
- **배경/근거**: 사용자 보고(2026-07-05) — 상세 편집 팝업(더블클릭)이나 수정 폼에서 라인
  수정/도서 추가 후 저장하면 목록의 거래처가 `거래처명 (코드)` → **`5019 (5019)`**(=hcode)로,
  전표번호가 **`–`**(빈값)로 바뀌는 회귀. 원인: `desired[(hcode, bcode)]` + `"gcode": hcode`
  로 키잉했는데 `current` 는 `(실제 Gcode, Bcode)` 로 키잉 → 키가 **절대 일치하지 않아** 전
  라인이 DELETE + `gcode=hcode` 로 재INSERT(=거래처 소실) + INSERT 경로가 `has_idnum` 미지정
  이라 Idnum 누락(=전표번호 소실). 같은 값(hcode==Gcode)만 쓰던 기존 테스트가 이를 못 잡았다.
- **영향**: `backend/app/services/sales_statement_create_service.py`(update_sales_statement:
  SELECT+Idnum, s_gcode/s_idnum, desired 키, INSERT mid_vals). 회귀:
  `test/test_sales_statement_update_phase1.py::test_update_preserves_customer_gcode_and_idnum`
  (hcode≠Gcode 슬립에서 기존 라인 UPDATE·삭제 0 + 신규 라인 INSERT 의 Gcode=거래처/Idnum 보존
  검증). 프론트 무변경(저장 payload 형태 동일).
- **결정자**: 메인개발자 (2026-07-05 사용자 재현 스크린샷 확인 후)
- **참조**: DEC-065(거래명세서 수정 desired-state diff), 멀티테넌트 hcode 격리(hcode=테넌트 vs Gcode=거래처 구분)

### DEC-078: 거래명세서 상세 수정 — 거래일자(Gdate) 변경 허용(정밀 스코프 이동)

- **일자**: 2026-07-05
- **결정 사항**: 거래명세서 편집 팝업에서 거래일자를 편집 가능하게 하고, 저장 시 새 일자가 다르면
  슬립을 새 일자로 이동한다. 이동은 **이 슬립의 거래처(Gcode)로 스코프**한
  `UPDATE S1_Ssub SET Gdate=<new> WHERE Gdate=<old> AND Hcode=<h> AND IFNULL(Jubun,'')=<j> AND Gcode=<gc>`
  를 라인 diff 보다 **먼저** 실행하고, 이후 라인 diff(UPDATE/INSERT/DELETE)는 새 일자 키로 수행한다.
  전표번호(Idnum)는 **유지**(재부여 안 함). `update_sales_statement(new_gdate=...)` +
  `SalesStatementUpdateRequest.newGdate` + 프론트 편집 다이얼로그 날짜 input.
- **배경/근거**: 사용자 요청(2026-07-05). 조사 결과 거래명세서 슬립의 실제 식별은 7축
  (Gdate, Hcode, Idnum, Gubun, Jubun, Gjisa, Gcode)이고 전표번호(Idnum)는 **날짜별 일련번호**라,
  날짜 이동 시 새 일자에 같은 Idnum 이 이미 있으면 중복이 생긴다. 사용자는 이 중복을 **인지하고
  레거시에서 그렇게 사용해왔다며 그대로 진행**을 승인(중복 표시 허용). 다만 "키로 쓰는 경우 의견을
  달라"는 요청에 따라, **다른 거래처/슬립 훼손 방지**를 위해 이동을 Gcode 로 스코프해 같은
  (일자,회사,전표)를 공유할 수 있는 타 거래처 슬립을 건드리지 않도록 했다(정밀 스코프).
- **알려진 한계(사용자 합의)**: 같은 거래처가 대상 일자에 동일 (Jubun,Idnum) 슬립을 이미 가진
  드문 경우엔 목록 GROUP BY(7축)에서 병합되어 보일 수 있다. 사용자 합의 하에 허용(레거시 동작).
  필요 시 후속으로 이동 시 Idnum 재부여/충돌 차단 옵션 추가 가능(open).
- **영향**: `backend/app/services/sales_statement_create_service.py`(update_sales_statement:
  new_gdate/ng/write_hkey/이동 UPDATE, INSERT·라인 diff 를 새 일자 키로), `app/models/inquiry.py`
  (newGdate), `app/routers/transactions.py`(전달). 프론트: `sales-statement-edit-dialog.tsx`
  (날짜 input+dirty), `inquiry-api.ts`(newGdate). 회귀: `test_sales_statement_update_phase1.py`
  (이동 UPDATE 선행+Gcode 스코프+새 일자 라인 diff+응답 order_key 새 일자 / 동일 일자 미이동).
- **결정자**: 메인개발자 + 사용자 (2026-07-05 — 중복 전표번호 인지·승인, 정밀 스코프는 개발자 판단)
- **참조**: DEC-077(같은 update 경로 Gcode/Idnum 보존), DEC-065

### DEC-079: 거래처(Sobo11) 구분별 코드 접두 채번 + 검색 Enter 네비 + 목록 선택 컬럼 13종

- **결정**: 사용자 제공 스킴(2026-07-05)을 신규 기능으로 구현. 레거시/기존 앱엔 **접두 스킴이
  전무**(기존 채번은 숫자 `MAX(Gcode)+1`, 거래처구분은 G1_Gbun 자유 카테고리)했으므로 신규 도입.
  1) **구분별 접두 채번**: 거래처구분명→접두문자 맵(구내서점 A·인터넷서점 B·일반서점 C·총판 D·
     현매거래처 E·eBook거래처 F·교과서 G·본보기도서 H·납품거래처 **J**·기타거래처 **K** — **I 건너뜀**).
     코드=`<접두><6자리>`, 같은 접두 코드 중 `MAX(Gcode)+1`(`LIKE '<P>%'`+`LENGTH=7`, 6자리 0패딩이라
     문자 MAX=숫자 MAX → CAST 불필요 mysql3 호환). `masters_service.customer_type_prefix` +
     `next_customer_code_by_prefix`, `/masters/next-code` 에 `gubunName` 파라미터 추가(매칭 안 되면
     숫자 폴백). 신규 등록 화면은 거래처구분 select/변경 시 재발급(접두 매칭 시 덮어씀, 미매칭 시
     빈 경우만 숫자 채움).
  2) **검색 Enter 네비**: 코드+Enter→결과 1건이면 거래처구분으로 포커스 이동, 거래구분+Enter→지역.
  3) **목록 선택 컬럼 13종**: 구분(sname)·지역(jubun)·코드·명·대표자(gposa)·사업자번호(gnumb)·
     업태(guper)·종목(gjomo)·주소·이메일(email)·전화·팩스(gfax1)·비고1(gbigo). 추가 컬럼은
     `g1_geo_column_meta`(SHOW COLUMNS)로 DDL 차이 흡수(없으면 '' 리터럴). **신규 컬럼은 정렬 비활성**
     — 테넌트별 컬럼 누락 시 ORDER BY 500 위험(4서버 무500 불변식), 코드/명/전화만 정렬 유지.
- **주의**: 접두 매칭은 거래처구분 **명(sname)** 기준(공백·대소문자 무시). 테넌트 G1_Gbun 카테고리명이
  스킴과 다르면 폴백(숫자). 목록 구분 표시는 저장된 sname(생성/수정 시 기록) 사용 — 필요 시 G1_Gbun
  재해석은 `list_customer_master_full` 방식(파이썬 맵) 참조.
- **테스트**: `test_customer_code_prefix.py`(맵 10종·I 제외·접두 채번·mysql3 SQL). 기존
  `test_customer_list_filters.py`·`test_masters_q_search.py` 는 `list_customer_master` 신규 SHOW
  COLUMNS 호출을 `g1_geo_column_meta` 모킹으로 흡수(실 DB 미연결 유지).
- **보강(2026-07-05, 사용자 재검토 피드백)**:
  - **거래처구분 컬럼 데이터 미표시 수정**: 상당수 테넌트에 `Sname` 컬럼이 **아예 없음**
    (remote_153 실측) → `_txt_col("sname")` 이 `'' AS sname` 로 항상 빈값. `Gubun` 코드를 뽑아
    `_gbun_code_name_map`(G1_Gbun 1회 조회, JOIN 금지) 로 명 해석해 채운다. 나머지 신규 컬럼
    (gposa/gnumb/guper/gjomo/email 등)은 존재하나 레코드에 값이 없으면 정상적으로 빈값.
  - **목록 신규 컬럼이 화면에서 빈값(response_model strip)**: 서비스는 sname 등을 채웠으나
    라우터 `response_model=CustomerListResponse`(Pydantic `CustomerListItem`)에 신규 필드가
    없어 FastAPI 가 응답에서 잘라냄 → 컬럼은 뜨는데 값이 전부 빔(상세는 정상). `CustomerListItem`
    에 sname/jubun/gposa/gnumb/guper/gjomo/gfax1/gbigo/email 추가. 회귀:
    `CustomerListResponseModelTests`(모델 필드 선언 + 값 라운드트립). **교훈: 서비스 dict 에 필드를
    더하면 response_model 에도 반드시 선언**(안 그러면 조용히 잘림).
  - **미등록 구분값 추가·자동 채번**(사용자 "등록 안 된 구분값도 추가"): 신규 거래처 화면
    거래처구분 선택지에 접두 스킴 10종을 미등록이어도 노출(`/masters/customer-type-prefixes` +
    `MasterGbunSelect includeTypePrefixes`). 선택 시 gubun 코드는 비워 보내고(구분명만) 백엔드
    `_resolve_gubun_code` 가 구분명→코드 조회 실패 시 **접두 스킴이면 카테고리 자동 등록**
    (G1_Gbun 코드=접두문자 A~K, 숫자 카테고리 코드와 무충돌·거래처코드 접두와 의미일치).
    거래처코드도 해당 접두로 채번. 회귀: `test_customer_code_prefix.py::ResolveGubunAutoRegisterTests`.
- **결정자**: 메인개발자 + 사용자 (2026-07-05 — 스킴·접두표·컬럼 목록 사용자 제공, 재검토 피드백 2건)
- **참조**: DEC-068(목록 JOIN 금지 행증식), G1_Ggeo 컬럼 의미 메모(Gposa=대표/Guper=업태/Gjomo=종목)

### DEC-080: 거래명세표 대량 소실 사고(2026-07-04) — binlog 복원 + 전표 키 스코프 강제(fail-closed)

- **일자**: 2026-07-06
- **사고**: h=5019(remote_153) 사용자가 7/4 23:43·23:44 / 7/5 02:37 웹 거래명세서 **수정 저장** 시
  타 거래처 라인이 일괄 삭제됨. 피해: **7/2 jubun=11 46라인·12거래처 2,048,225원**,
  7/2 jubun=12 3라인·138,140원, **6/30 jubun=21 반품 32라인·5거래처 −899,415원**,
  7/3 소전표(교문사 80028·교보 00001) 12라인 — 반복 재수정 churn 중 소실. 잔존물은
  `Gcode='5019'(=hcode)`·`Idnum=NULL` 손상 행 15개("오류가 발생된 거래처 2곳"의 정체).
  과거 동일 유형 1건: 6/20 22:09 jubun=23(2행, 원본 불명·미복원).
- **근본 원인 (2중)**:
  1) **키 결함(설계)**: `update_sales_statement` 가 전표를 (Gdate, Hcode, Jubun) 3키로 식별.
     레거시 Jubun 은 (Gdate,Hcode) 내 **거래처별** 시퀀스라 거래처 간 공유 키 — desired-state
     diff 의 `current` 에 같은 날짜·같은 Jubun 의 **전 거래처 라인**이 로드되어
     `current − desired` 가 전부 DELETE 됨. DEC-077(로컬 수정)로도 이 폭은 안 닫혔음.
  2) **배포 격차**: 운영(Render)은 DEC-077 이전 빌드 — 재삽입 라인 Gcode←hcode, Idnum 누락
     (사고 잔존물 시그니처와 일치. 같은 세션의 신규 작성은 정상 시그니처 → create 정상, update 만 결함).
- **포렌식/복구**: remote_153 은 `log_bin=ON`(STATEMENT)·`expire_logs_days=0` —
  `SHOW BINLOG EVENTS`(읽기 전용 SQL, SSH 불필요)로 mysql-bin.000025 후미 ~17MB 스캔
  (secant + id↔일자 브래킷). 사고 DELETE 문(거래처·도서쌍 전수)과 원본 INSERT/UPDATE 전량 확보 →
  이벤트 재생 시뮬레이션(최종 상태가 실 DB 잔존 4행과 **정확 일치**로 검증) → 삭제 시점 상태 재구성.
  **90라인 복원**(원본 id/Idnum/Yesno/Gubun 보존, 존재확인 idempotent, 7/6 레거시 수동 재입력 9라인
  자동 제외) + **손상 행 15개 삭제**(id 4중 일치 검증). 오류 0. 실행 로그/재구성 산출물은
  세션 스크래치(`restore_run_log.json`/`restore_inventory.json`) — 사고 SQL 원문은 binlog 에 영구 잔존.
  기본 제외(사용자 승인): 6/27 13라인(744,900원)·6/17~6/29 개별 삭제 8건·7/2 ju12 '00003' 추가분·6/20 ju23.
- **재발 방지 (fail-closed)**:
  1) `update_sales_statement(gcode=, idnum=)` — 7세그 order_key 의 거래처/전표번호로 SELECT·쓰기
     (UPDATE/DELETE/일자이동) 스코프. 스코프 없이 **여러 거래처 매칭 시
     `ValueError("SLIP_KEY_AMBIGUOUS")` → 422, 아무 것도 쓰지 않음** (단일 거래처면 4세그 호환).
  2) PUT 라우터 `_parse_order_key`(4세그, gcode/idnum 폐기) → `_parse_order_key_extended`(7세그).
     프론트는 전 구간 7세그 전송 중이었음 — 라우터가 버리던 것이 약한 고리.
  3) `outbound_service.update_order` — gcode 미지정+다중 거래처 매칭 시 `ORDER_KEY_AMBIGUOUS` 거부,
     INSERT `has_idnum` 누락 수정(전표번호 보존) + SELECT 에 Gjisa/Gubun/Ocode/Scode 추가
     (재삽입 라인 지사 소실·Ocode='B' 고정 회귀 동시 수정).
- **영향**: `backend/app/services/sales_statement_create_service.py`, `outbound_service.py`,
  `app/routers/transactions.py`, `outbound.py`. 회귀:
  `test/test_sales_statement_update_slip_scope.py`(11건 — 사고 재현·fail-closed 무기록·스코프
  SQL/params·7세그 전달·422 메시지·Idnum 보존) + `test_sales_statement_update_phase1.py` fake 시그니처
  갱신. 정적 감사 3종 critical=0. 전체 스위트 신규 실패 0(기존 실패 94건은 패치 전 103건의 부분집합).
- **운영 조치 필요**: ① **Render 재배포**(이 패치 + DEC-077/078 포함 최신 빌드) — 배포 전까지
  웹 '수정' 기능 사용 금지 안내. ② 사용자 데이터 검증(7/2·6/30·7/3 화면 대조, 6/20·6/27 항목 판단).
  ③ remote_154/155 'Host blocked'(1129) — `mysqladmin flush-hosts` 필요(별건).
- **결정자**: 메인개발자 + 사용자 (2026-07-06 — 복원 범위·손상 행 삭제·패치 승인)
- **참조**: DEC-077(부분 대응 — 배포 격차로 사고 미차단), DEC-078(일자 이동 Gcode 스코프),
  DEC-064(7세그 합성키), DEC-065(desired-state diff), DEC-033(IFNULL/COALESCE 게이트)

### DEC-081: 출고접수 목록 — Yesno='2'는 완료(취소 아님)이며 항상 표시(HAVING 제외 제거)

- **문제**(사용자 보고 2026-07-06): 출고접수관리에서 기간(예 7/1~7/6) 지정해도 7/2 데이터만
  나옴. 라이브 실측(remote_153/hcode 5019): 7/1(39)·7/3(49)·7/6(82) 라인이 **전부 Yesno='2'**,
  7/2 만 '0'(45)/'1'(4). `list_orders` 의 `HAVING MAX(Yesno)<>'2'`(취소 포함 미체크 시)가 그 날들을
  통째로 숨김.
- **근본 원인 = 코드 내 '2' 의미 충돌**: 상태표시 `_line_status_from_yesno_max`+레거시 Subu21 정본은
  **'1'·'2' 모두 완료(done)**(취소는 행 DELETE), 그러나 목록 HAVING 과 웹 취소(TC-OUT-003
  soft-delete `UPDATE Yesno='2'`)는 **'2'=취소**로 취급. 데이터 패턴(하루 전체 '2')상 취소가 아니라
  **완료(출고끝)**가 타당.
- **결정**(사용자 확정): **'2'=완료, 항상 표시.** `list_orders` 의 `having=""` 로 고정(SELECT·
  count_grouped 공통) — Yesno 기반 취소 제외 없음. status 표시는 그대로 done. `include_cancelled`
  는 이제 HAVING 무영향(취소=행 DELETE 정본).
- **잔여 이슈(후속 결정 필요)**: (a) 웹 취소가 soft-delete 로 '2' 를 써 이제 '완료'로 노출됨 —
  실제 취소 숨김을 원하면 별도 취소 표식/행 DELETE 필요. (b) 프론트 "취소 포함" 체크박스가
  no-op 이 됨(정리/재정의 대상).
- **회귀**: `test_outbound_list_server_sort.py::OutboundListShowsCompletedTest`(HAVING '2' 제외 없음
  + count_having='' + '2'행 done 포함). 라이브 검증: 42건(7/1:12·7/2:14·7/3:7·7/6:9) 정상 표시.
- **결정자**: 메인개발자 + 사용자 (2026-07-06 — '2'=완료 항상표시 선택)
- **참조**: DEC-033(list_orders mysql3 count_grouped), 상태어휘 메모(status-vocab-yesno-3state)

### DEC-082: 재고관리·재고원장 7화면 공통 그리드 정비 — 서버 정렬 아키텍처 + 룩업 + book-sales 상한

- **배경**(사용자 요청 2026-07-07): 재고관리(재고현황 Sobo44_inv/도서수불장 Sobo33/통합
  도서수불장 Sobo33_1) + 재고원장(도서별수불원장 Sobo31/거래처원장 Sobo32/통합 Sobo32_1/
  출판사관리설정 Sobo48) 목록 화면에 공통 요소(헤더 클릭 서버 정렬·컬럼 선택/순서/너비·
  검색 입력 자동완성+팝업)가 미반영 상태였음(전 화면 중 최하위 준수, stats 와 동급).
- **정렬 아키텍처 결정** — DEC-068 (D) 를 페이지네이션 축이 있는 조회 화면으로 확장:
  - **축 컬럼은 SQL 전역 정렬**: inventory/ledger 의 `gdate`(dates-page ORDER BY 방향),
    customer-integrated 의 `hcode`(hcodes-page), comparison 의 `gcode/gname`(단순 목록 ORDER BY).
  - **비축 컬럼은 누적 완료 후 "페이지 내" Python 정렬**: 일자/거래처 단위 사전 집계 구조
    (DEC-033 (g/h/j))와 전역 수량 정렬이 상충하므로 페이지 구성은 유지.
  - **Sobo32(거래처원장)는 페이지 구성 오름차순 고정**: 잔량(balance_qty) 누적·R4 totalsCache 가
    "오름차순 일자 + 순차 페이지" 를 전제하므로 gdate desc 포함 모든 정렬은 표시 정렬만
    (페이지 내 재정렬). 회귀: `test_ledger_sort_params.py::test_single_pagination_axis_stays_ascending`.
  - **book-sales(통합 도서수불장)는 전체 정렬 후 페이징**(이미 전량 메모리 집계라 비용 0).
  - 화이트리스트 밖 sortBy 는 방향까지 무시(masters `_order_by_clause` 동일 정책, 주입 차단).
- **book-sales 풀스캔 상한 신설**: 서버측 LIMIT 없는 유일한 재고 계열 API 였음 —
  `BLS_BOOK_SALES_MAX`(기본 20000) 상한 + `truncated` 응답/배너 (LEDGER_MAX 정책 미러).
- **검색 입력 룩업 결정**: 이들 화면의 거래처 입력(S1_Ssub.Hcode = 거래처코드, 레거시
  Subu32 Edit107 근거)은 `MasterLookupField lookupKind="customer"` + `applyCustomerToHcode`
  (G1_Ggeo.Gcode 채움 — selection.hcode 는 소유계정이므로 금지), 도서코드 시작/끝은
  `lookupKind="book"` + `applyBookToBcode`, Sobo48 검색어는 `publisher` 룩업.
- **컬럼 설정**: 7화면 모두 `useGridPrefs`(서버 저장, hcode 계정 종속) + `GridColumnSettings`
  + 헤더 드래그 순서/너비. Sobo32/32_1 은 원시 `<table>` → `DataGrid` 전환(기존
  data-legacy-id 전량 컬럼 `legacyId` 로 보존). 재고현황(Sobo44_inv)은 표가 클라이언트 파생
  집계(현재 페이지 도서별 재집계)라 정렬만 `useClientSort`(서버 표현 없음).
- **부수 정비**: `ledger.comparison` 에 `useListSession` 도입(DEC-055 위반 16→15),
  transactions/verification 동적 WHERE 오탐 2건 noqa 주석(hcode strict 감사 exit 0 복구).
- **회귀**: `test/test_ledger_sort_params.py` 15건(5 엔드포인트 × 축/비축/주입/상한) + 기존
  인접 스위트 106건 PASS, tsc/eslint/next build PASS.
- **결정자**: 메인개발자 + 사용자 (2026-07-07 — 공통요소 반영 지시)
- **참조**: DEC-068 (D) 헤더 정렬 표준, DEC-033 (f/g/h/j), DEC-055, DEC-024, Sobo32.md/Sobo32_1.md

### DEC-083: 통계관리 12화면 전면 정비 — 계정코드 "기본 검색 조건" 정책 + 검색 시맨틱 교정

- **배경**(사용자 요청 2026-07-07~08): 통계관리 하위 12화면(도서별판매 Sobo61/거래처판매
  Sobo62/도서별년말집계 Sobo67_yearbook + stats 8종 + 년/월 허브)의 검색이 계정 코드
  기반으로 바르게 동작하지 않았고, 검색창에 룩업·정렬·컬럼설정 등 공통 요소가 전무했다.
- **계정코드(=로그인 hcode) 정책 (사용자 확정)**: "입력창이 존재하면 다른 계정 정보 접근이
  가능해져 문제" — **계정코드 입력창은 admin(수퍼) 전용으로만 노출**하고, 일반 계정은
  로그인 계정 코드가 **기본 검색 조건**으로 자동 적용된다(프론트 hcode 미전송 → 서버
  `enforce_hcode_isolation` 이 JWT 코드 주입, 타 코드 403 기존 유지). 프론트 판정은
  `user.role === "admin"`. 동일 정책을 재고관리·재고원장 화면(재고현황/도서수불장/통합
  도서수불장/도서별수불원장)의 거래처/지사 입력에도 소급 적용.
- **검색 시맨틱 교정 (S1_Ssub 축 정본: Hcode=계정(출판사, G7_Ggeo.Gcode 동일 키) /
  Gcode=거래처(G1_Ggeo) / Bcode=도서(G4_Book))**:
  - 거래처판매(Sobo62): `gcodeFrom/To` 가 "도서코드" 로 오표기 — 실제 바인딩은 거래처코드
    범위. 라벨·룩업(거래처)·그리드 컬럼(hcode=계정코드/gcode=거래처코드/gname=거래처명/
    gjqut=증정수) 교정.
  - 거래처별 판매 분석·거래처통계: "코드" 컬럼이 `hcode`(계정, 격리 계정에선 상수) 표시
    → `gcode`(거래처) 로 교정.
  - **출판사통계(Sobo43) 근본 수정**: 기존 구현은 get_book_sales 행에 없는 `pcode` 를 읽어
    전량 "미분류" 1행으로 붕괴 — 출판사 축은 `S1_Ssub.Hcode` GROUP 이 정본. 신규
    `reports_service.get_publisher_sales_summary`(SQL-INQ-7 의 Hcode GROUP 트리비얼 변형,
    stats_service "신규 SQL 0건" 가드 준수 위해 reports 층에 배치) + `_fetch_publisher_names`
    (G7_Ggeo) 재사용. metadata.publisher_source="s1_ssub_hcode".
- **조회 대상별 룩업**: 계정코드(admin)=거래처/출판사 룩업, 거래처코드 범위=customer 룩업
  (`applyCustomerToGcode`), 도서코드 범위=book 룩업 — `MasterLookupField` 자동완성+Enter
  확정+검색 팝업. 공용 `StatsFilterBar` 에 `showGcodeRange`/`showBcodeRange` 신설.
- **필터·정렬 확장 (DEC-082 패턴)**: customer-sales/year-end-book/sales-period/
  customer-analysis/book-turnover/publisher 에 `sortBy/sortDir`(화이트리스트, 전체 정렬 후
  페이징) + customer-analysis `gcodeFrom/To`, sales-period·book-turnover `bcodeFrom/To` 신설.
  customer-sales/year-end-book 에 `BOOK_SALES_MAX` 상한+`truncated` 부여. 분기/반기 손익은
  정렬 미지원(월 시계열 고정).
- **공통 그리드**: 12화면 전부(허브 제외 11) DataGrid + useGridPrefs + GridColumnSettings +
  useListSession — stats 8화면의 DEC-055 위반 해소(전체 위반 15→7, 잔여는 transactions 계열).
- **회귀**: `test_stats_reports_sort_params.py` 11건(정렬/필터 전달/주입/상한) +
  `test_stats_optional_paging.py` 출판사 축 테스트 재작성(구 버그 고정 테스트 폐기) +
  기존 인접 스위트 170건 PASS, tsc/eslint/next build PASS. hcode strict 감사 exit 0.
- **잔여 이슈(후속)**: (a) 기간별 매출의 구간별 get_book_sales 반복 호출(일 단위 1년 ≈ 365회)
  성능 — SQL 레벨 버킷 집계로 개선 여지. (b) 도서 회전율의 기반 조회 상한(2000행) — 대형
  카탈로그에서 절단. (c) `/stats/publisher` 권한 키가 `admin.stats.customer` 재사용.
- **결정자**: 메인개발자 + 사용자 (2026-07-08 — 계정코드 입력창 금지·기본 조건화 지시)
- **참조**: DEC-082(공통 그리드·정렬 아키텍처), DEC-033 (f), DEC-055, hcode_isolation.py

### DEC-084: 통계·원장 "완료 거래 미조회" 사고 — 도서구분(Ocode) 스코프 기본값 교정

- **증상**(사용자 보고 2026-07-08): 출고관리·입고관리에는 완료 거래가 대량인데 통계관리
  화면들은 거의 0건. (원장·재고 화면도 동일 계열 영향.)
- **근본 원인 — Ocode 값 불일치**: 운영 4서버(remote_138/153/154/155)는 전부
  `chul_09_db`(창고 계열)이고, 이 계열의 출고·입고·거래명세서 라인은
  ``Ocode='A'``(레거시 일부 입고는 ``''``/NULL) 로 기록된다
  (`_default_outbound_ocode`/`_inbound_ocode`/`sales_statement_ocode_sql` — 같은 원인의
  입고 LIST 0건 회귀를 2026-06-21 에 이미 해결한 전례). 그런데 통계·원장 조회는
  ``Ocode LIKE '%B%'``(scope 기본 'B') / 하드코딩 ``Ocode='B'``(거래처판매) 로
  필터링해 'A' 행을 전부 제외했다.
- **레거시 정본 확인**(WeLove_FTP Subu61/62/67 cp949 원문 대조):
  - Subu61(도서별판매)/Subu67(년말집계) 기본값 = Panel102 '도 서 명' → ``Ocode LIKE '%%'``
    (**전체**). 'A'/'B' 는 본사도서/창고도서 명시 선택 시에만.
  - **Subu62(거래처판매)는 Ocode 필터 자체가 없음** (Scode='X' + Hcode 만).
  - 즉 포팅 시 'B' 하드 기본은 레거시에 없던 축소 — 회귀였다.
- **수정**:
  - `get_book_sales`/`get_publisher_sales_summary`/`get_inventory_ledger`/
    customer ledger(단일·통합): **scope 미지정/ALL = Ocode 절 제거(전체, ''/NULL 포함)**,
    'A'/'B' 명시 시에만 LIKE. 라우터 기본 Query("B")→Query(None).
  - `get_customer_sales`: 하드코딩 ``Ocode='B'`` 제거 (Subu62 원본 동등 — Scode 로만 스코프).
  - `get_year_end_book_aggregate`: 기본 전체 + ``IFNULL(s.Ocode,'') LIKE`` NULL 안전화
    (Sg_Csum pass 도 동일). 프론트 년말집계 bookMode 초기값 'B'→'ALL'.
  - stats 위임 경로(`_sum_book_sales_outbound`/도서회전율/출판사통계) scope='B'→None.
  - 거래처원장/통합 원장 프론트 범위 select 초기값 '창고도서(B)'→'전체(ALL)'.
- **부수 발견·수정 — 통합 거래처원장 파라미터 순서 버그**: ocode 파라미터를 마지막에
  append 해 위치 바인딩이 ``Ocode LIKE <hcode>`` / ``Hcode = '%B%'`` 로 어긋나 있었음
  (격리 계정 통합원장 상시 0건). 절 순서(Gdate,Gdate,Bdate,Ocode,Hcode)에 맞게 재배치.
- **잔여 이슈(후속)**: (a) `returns_service` 가 반품 라인을 ``Ocode='B'`` 리터럴로 쓰고
  같은 값으로 읽음 — chul_09 에서 레거시('A') 반품 행이 반품 화면에 안 보일 가능성,
  쓰기 경로 포함이라 별도 검증 후 서버 가변화 필요. (b) `verification_service`(출고검증)
  의 ``Ocode='B'`` 하드코딩 + S1_Chek 키 — 동일 계열, 검증 키에 얽혀 있어 별도 이관.
  (c) `transactions_service` S1_Memo 헤더 INSERT 의 Ocode 'B' 리터럴 — 명세서 라인('A')과
  불일치 가능성 점검. (d) Subu61 원본의 ``(Scode='Y' AND Pubun<>'이동') OR X OR Z`` 상시
  절은 미이식 — 분기 로직상 이동 행이 계상되지 않아 실효 차이 없다고 판단, 관찰 대상.
- **회귀**: `test/test_dec084_ocode_scope.py` 9건(기본=절 제거/명시 LIKE/Subu62 무필터/
  파라미터 순서/위임 scope=None) + 인접 스위트 179건 PASS, tsc/eslint/next build PASS,
  hcode strict 감사 exit 0. 라이브 검증은 배포 후 통계 화면 실측 권장.
- **결정자**: 메인개발자 (레거시 원문 대조 — Subu61 L297-323, Subu62 L285-325, Subu20 L561)
- **참조**: DEC-083(통계 정비), DEC-033 (f), 입고 LIST 0건 회귀(2026-06-21,
  inbound_service._inbound_ocode), h2_gbun_adapt.sales_statement_ocode_sql

### DEC-085: 분기/반기 손익 0건 사고 — T2_Ssub.Gdate 월키 정규화

- **증상**(사용자 보고 2026-07-08): 분기/반기 손익(Sobo53) 화면 데이터 전무.
- **근본 원인 — 월키 포맷 불일치**: 레거시 Subu45(정산 입력)는 T2_Ssub.Gdate 에
  ``FormatDateTime('yyyy"."mm"')`` = **점 구분 월('2026.07')** 을 기록
  (legacy_delphi_source Subu45.pas L170/L657). 그런데 `_SQL_PERIOD_SUMMARY` 는
  ``Gdate BETWEEN '202601' AND '202603'``(YYYYMM 6자리) 직접 비교 — 문자열
  정렬상 ``'.'(0x2E) < '0'(0x30)`` 이라 점 표기 전 행이 하한 탈락 → **항상 0건**.
- **수정**: 숫자만 남긴 6자리 월키
  ``LEFT(REPLACE(REPLACE(REPLACE(TRIM(Gdate),'-',''),'.',''),'/',''),6)`` 로
  WHERE/GROUP/ORDER/COUNT 통일 — '2026.07'/'202607' 표기 모두 일치
  (t5_ssub_adapt._trim_gdate·T5 입금 sql_deposit_sdate 와 동일한 mysql3 검증 패턴).
  Sobo47 청구금액(년월) 도 같은 SQL 공유로 함께 복구.
- **잔여 이슈(후속) — 정산 모듈 전반의 'YYYYMM' 가정**: settlement_service 의
  다른 T2/T3/S1 비교(`Gdate = %s` 마감 키, `LEFT(Gdate,6)` — 점 표기에선
  '2026.0' 이 됨, Sobo42 입금현황 `t.Gdate = %s` 등 _norm_month 사용 12곳)가
  동일 가정 위에 있음. **마감 UPDATE/DELETE 키에 얽혀 있어 별도 검증 후 일괄
  월키화 필요** — 이번에는 사용자 보고 화면(분기 손익 + 년월 청구) 조회만 수정.
- **회귀**: `test/test_dec085_t2_month_key.py` 3건(월키 SQL 강제/원컬럼 BETWEEN
  회귀 금지/분기→월 경계 위임) + 정산·통계 인접 52건 PASS.
- **결정자**: 메인개발자 (레거시 Subu45 원문 대조)
- **참조**: DEC-084(Ocode 스코프 사고 — 같은 "포맷/값 가정 vs 실데이터" 계열),
  t5_ssub_adapt(월키 어댑터 선례), DEC-031(마감 가드 — 후속 수정 시 주의)

### DEC-086: 기간별 매입·매출(월/분기/년) + 엑셀 export — 통계 그룹 R/W3 배지 완료 처리

- **배경**(사용자 요청 2026-07-08): 통계관리 사이드바의 R/W3 배지 항목 완료 + "월별,
  년별, 분기별 매입·매출 조회 및 엑셀로 모든 정보 저장" 기능 요청.
- **매입·매출 기간 통계**: `_apply_book_sales_branch` 에 ``gisum``(매입액 — Scode='Y'
  입고/반품 행 Gssum) 누적 추가(BookSalesRow 추가 필드, 하위 호환). `get_sales_period`
  groupBy quarterly/yearly 신설(버킷 라벨 YYYY-Qn/YYYY) + 매입 축
  ``buy_qut_total/buy_sum_total`` 동시 집계(기존 매출 키 유지). 화면(Sobo50)은
  「기간별 매입·매출 분석」 으로 확장 — 매입/매출 4컬럼 + 5장 요약 카드.
- **엑셀 export**: ``GET /api/v1/stats/sales-period/export.xlsx`` — 전체 버킷+합계 행,
  화면과 동일 필터·정렬 부착(DEC-068 "정렬은 export 에도 동봉"),
  `masters_excel.build_list_workbook` 재사용(표현만 책임 — SRP), guard
  admin.stats.sales + enforce_hcode_isolation. 프론트 「엑셀 저장」 버튼
  (`downloadBlobAs` + 날짜 접미 파일명). probe 매트릭스 등록(stats.sales_period_export).
- **R/W3 배지 완료 처리**: 통계 그룹 9항목(Sobo50~53_stats/Stats_monthly/
  Sobo36·37_stats_route/MenuYearMonthStats/Sobo43_stats_route)의
  ``roadmapWave``/``crudParity``/``crudNotes`` 제거 — DEC-082~086 으로 공통그리드·
  서버정렬·룩업·계정코드 정책·조회 복구·매입매출·엑셀이 반영되어 p3 백로그 소진.
  통계는 조회 화면이 정본(쓰기 없음 = R 배지 불필요). docs/crud-backlog.md 해당 행
  완료 표기. (주의: 사이드바 캡션은 「기간별 매출 분석」 유지 — 매트릭스 캡션 드리프트 회피.)
- **회귀**: `test/test_dec086_buy_sell_period.py` 5건(gisum 누적/분기·년 버킷/매입 축/
  groupBy 폴백/export 라우트 OpenAPI) + 통계·리포트 인접 151건 PASS,
  form-registry 메타 가드 17건 PASS, tsc/eslint/next build PASS.
- **결정자**: 메인개발자 + 사용자 (2026-07-08 — 스크린샷 R/W3 완료 + 매입매출·엑셀 지시)
- **참조**: DEC-082~085, DEC-068(export 정렬 동봉), masters_excel(DEC-068 엑셀 선례),
  docs/crud-backlog.md §2.5/§P3

### DEC-087: 통계 목록 최종거래일 필드 — 집계 행 날짜 정렬

- **배경**(사용자 요청 2026-07-08): 통계 목록들이 기간으로 조회하면서도 행에 날짜
  필드가 없어 날짜 정렬이 불가.
- **결정**: 집계 행은 단일 날짜가 없으므로 **그룹별 ``MAX(Gdate)`` = 최종거래일** 을
  표시·정렬 필드로 채택. SQL-INQ-7/9·출판사 축 집계에 ``MAX(Gdate) AS Gdate``
  (+Sg_Csum pass) 한 컬럼씩 추가(mysql3 안전, 집계 수치 불변). 응답 필드
  ``gdate``(도서별판매/거래처판매/거래처통계/도서통계/도서회전율) /
  ``last_date``(출판사통계) — 모델·타입 추가 필드(하위 호환), 정렬 화이트리스트 편입.
  7개 화면 그리드에 「최종거래일」 sortable 컬럼 부착. (구간 축 화면 — 기간별/월별/
  분기손익/년말집계 — 는 이미 날짜 축 보유로 제외.)

### DEC-088: 분기/반기 손익 — 최대 N개(1~12, UI 1~8) 분기 비교 고도화

- **배경**(사용자 요청 2026-07-08): 분기 화면에서 여러 분기를 비교하고 싶다.
- **설계**: ``quarters`` 파라미터 — (year, quarter) 를 **기준(마지막) 분기**로 과거
  방향 N개 분기를 함께 집계. 응답: ``comparison``[{label 'YYYY-Qn', 청구/입금/잔액/
  손익, month_from/to}] (과거→기준 순) + ``items`` = N개 분기 월별 행 병합(월 오름차순,
  기존 페이지네이션 유지) + ``totals`` = N개 분기 합산. quarters=1 은 기존과 동등
  (신규 SQL 0건 — 분기당 list_period_summary 1회 재사용, N≤12 클램프).
- **화면**: 필터에 「비교 분기 수」(단일/최근 N개, 1~8) 선택 — 2개 이상이면 분기 비교
  막대 차트 + 분기별 비교 표(손익 음수 적색), 요약 카드 라벨에 분기 수 표기.
- **부수 수정**: 월별 그리드/차트가 ``ymonth`` 키를 읽어 월 컬럼이 비어 있던 잠복
  버그 → 백엔드 정본 ``gdate``(DEC-085 'YYYYMM' 월키)로 교정.
- **회귀**: `test_dec085_t2_month_key.py::test_quarterly_summary_n_quarter_comparison`
  (분기 시퀀스/비교 배열/합산/월 병합 정렬) + DEC-087 gdate 가드
  (`test_dec086_buy_sell_period.py`) + 통계 스위트 PASS, tsc/eslint/next build PASS.
- **결정자**: 메인개발자 + 사용자 (2026-07-08)
- **참조**: DEC-085(월키 정본), DEC-086(기간 통계), settlement_service.list_period_summary

### DEC-089: 분기손익 0원 2차 원인(Yesno) + 통계 차트 보강 + 엑셀 export 전면화

- **분기손익 모두 0원 — 2차 원인**(사용자 보고 2026-07-08, DEC-085 월키 수정 후에도
  지속): 레거시 Subu47 L282 원문 WHERE 는 ``Gdate 범위 [+Hcode]`` 뿐인데, 웹 포팅이
  임의로 추가한 ``COALESCE(Yesno,'0') <> '2'`` 가 실데이터(마감 상태 값)를 전부 제외.
  DEC-081 (Yesno '2'=완료) 과 동일 계열 — **레거시에 없는 Yesno 제외 금지**.
  `_SQL_PERIOD_SUMMARY`(+COUNT) 에서 Yesno 절 제거, 회귀 가드에 "Yesno 미포함" 강제.
- **차트 전수 점검**: 기간별 매입·매출 라인차트에 매입 시리즈 2종(점선, chart-3/4
  토큰) 추가(`StatsLineChart` buyQut/buySum 옵션 — 하위 호환). 분기 월별 차트/그리드의
  ``ymonth`` 키 참조는 DEC-088 에서 ``gdate`` 로 교정 완료. 거래처별/회전율/출판사
  막대차트 매핑은 실키 대조 결과 정상.
- **엑셀 export 전면화**: 통계관리 전 화면(11 — 허브 제외) 「엑셀 저장」.
  신규 라우트 7종(도서별판매/거래처별판매/년말집계/거래처별분석/도서회전율/출판사/
  분기손익 — 분기는 시트1 분기비교+시트2 월별 2시트, `build_multi_sheet_workbook`
  신설) + 기존 기간별 1종. 전 행 수집은 `collect_all_rows`(has_more 루프,
  EXPORT_MAX_ROWS 상한 + X-Export-Truncated 헤더), 컬럼은 화면 그리드 1:1,
  조회와 동일 필터·정렬 부착(DEC-068 정책). 각 라우트 GET 가드는 조회와 동일
  (admin.stats.* / enforce_hcode_isolation). probe 매트릭스 7건 등록.
  월별통계/거래처통계/도서통계는 각각 기간별(monthly)/거래처별분석/도서별판매
  export 를 재사용.
- **회귀**: export 라우트 8종 OpenAPI 가드 + Yesno 미포함 가드 + 기존 스위트 106건
  PASS, tsc/eslint/next build PASS.
- **결정자**: 메인개발자 + 사용자 (2026-07-08 — 분기 0원·차트·엑셀 전면화 지시)
- **참조**: DEC-081(Yesno 교훈), DEC-085(월키), DEC-086(기간별 엑셀 선례),
  masters_excel(collect_all_rows/build_list_workbook)

### DEC-090: 분기손익 0원 3차 원인 — T2 정산 도메인의 hcode 주입 부적합

- **증상**(사용자 보고 2026-07-08): DEC-085(월키)·DEC-089(Yesno) 수정 후에도 모두 0원.
- **근본 원인 — 도메인별 Hcode 의미 차이**: ``T2_Ssub.Hcode`` 는 **정산 대상
  출판사 코드**(= G7_Ggeo.Gcode — cash-status JOIN·Subu45 거래처별 정산 행 구조)로,
  S1 계열(Hcode=계정)과 다르다. 그런데 분기손익/청구금액(년월) 라우터가 S1 용
  ``enforce_hcode_isolation`` 으로 **물류/총판 운영 계정의 로그인 코드를 강제 주입**
  → 운영 코드는 T2 행에 존재하지 않아 항상 0. 레거시 Subu47 의 Hcode(Edit107)는
  **선택 필터, 기본 = 전체 합산**.
- **수정**: `hcode_isolation.resolve_publisher_row_scope(request_hcode, ctx)` 신설 —
  격리 계정(T2_PUB / T3+chul_09)은 본인 출판사 코드 강제(요청값 무시), 물류/총판
  (T1·T2_DIST)·슈퍼는 요청 필터 그대로(미지정=전체). `resolve_g7_ggeo_list_scope`
  (Seak80/ACC-DATA-03 G7 정본) 재사용. 적용: stats 분기손익 GET/export +
  settlement 청구금액(년월) 라우트. 감사 도구 `_ALLOWED_HELPERS` 에 등록.
- **잔여(후속)**: settlement 의 다른 T2/T5 라우트(cash-status·billing·마감 등)도
  동일 주입을 쓰므로 운영 계정에서 같은 증상 가능성 — 화면별 검증 후 일괄 전환 대상.
  배포 후에도 0 이면 다음 진단 순서: ① 해당 계정 account_type(T3+chul_09 로 분류되면
  격리 강제 — 광역 재분류 필요) ② T2_Ssub 에 실데이터 존재 여부(정산 모듈 미사용 계정).
- **회귀**: `test_dec085_t2_month_key.py::PublisherRowScopeTests` 3건(운영=전체/선택
  필터 통과/출판사 강제) + 정산·통계 스위트 83건 PASS, 라우터 hcode 감사 critical 0.
- **결정자**: 메인개발자 (레거시 Subu47/45 + Seak80 G7 스코프 정본 대조)
- **참조**: DEC-085/089(선행 2개 원인), resolve_g7_ggeo_list_scope, ACC-DATA-03

### DEC-091: 정산관리 9화면 전면 정비 — 도메인 데이터복구(월키·Yesno·출판사스코프) + 공통그리드 + 발송비(T1_Ssub) 이식

- **배경**(사용자 요청 2026-07-08): DEC-090 §잔여(후속) 이 예고한 대로, 정산관리 하위
  9화면(청구서관리/청구금액년월/입금내역/입금현황/미수현황/입금전표/세금계산서/발송비내역/
  발송비현황)에 통계·재고 사이클(DEC-082/083/089)의 "이전 최적화·개선 방식"을 그대로 적용.
- **레거시 정본 대조**(WeLove_FTP/도서유통-New Subu41/42/42_1/43/44/45/47/49 cp949 원문):
  모든 정산 `*_Ssub` 테이블에서 **`Hcode`=출판사(=G7_Ggeo.Gcode)**, `Gcode`=거래처.
  Ocode/Scode/Gubun 리터럴은 청구 집계의 S1_Ssub 원천 읽기에만 있고 요약 테이블(T1/T2/T5)엔
  없음. `D_Select`/`S_Where1` 은 빈 값(Base01.pas). **Yesno 필터는 정산 조회 어디에도 없음**.
- **데이터 복구 3종 (조회 0건/오격리 근본 원인)**:
  1. **월키 정규화(DEC-085 확대)**: 레거시 T2_Ssub.Gdate 는 점 표기 월('2026.07'). 조회
     SQL 이 `Gdate=%s`/`BETWEEN`/`LEFT(Gdate,6)` 로 6자리('202607')와 직접 비교해 점 표기
     행이 전량 탈락하던 잠복 버그를 `settlement_service._t2_month_key()`
     (`LEFT(REPLACE(REPLACE(REPLACE(TRIM(Gdate),'-',''),'.',''),'/',''),6)`)로 통일 —
     목록/상세/라인/라인수/입금현황(T2 4종)/미수 청구측/세금계산서 목록·카운트·인쇄.
     **쓰기 키(_SQL_CHECK_YESNO/confirm/cancel/upsert/recalc/chek3·sdate UPDATE)는 원시
     'YYYYMM' 유지** — 웹이 만든 헤더만 정확 겨냥, 레거시 행 오매칭 방지(DEC-085 주의 준수).
  2. **Yesno 제외 제거(DEC-089/081 계열)**: 입금현황(T2·T5 양측)·미수(T2·T5)·세금계산서
     조회의 웹 임의 추가 `COALESCE(Yesno,'0')<>'2'` 제거(레거시 무 Yesno). 청구서/입금
     목록의 `includeCancelled` 토글(DEC-012 소프트취소, UI escape-hatch)은 유지.
  3. **출판사 행 스코프(DEC-090 확대)**: billing/cash/cash-status/outstanding/tax-invoice
     목록·export 라우터를 `enforce_hcode_isolation`(S1용 로그인코드 강제주입) →
     `resolve_publisher_row_scope`(격리 계정만 본인 출판사 강제, 물류/총판·슈퍼는 선택
     필터·기본 전체)로 전환. 상세/인쇄의 `enforce_hcode_identity`(식별자 tamper 가드)는 유지.
- **발송비 실 이식(Subu43/44 → T1_Ssub)**: W2 scaffold(빈 목록)였던 발송비내역/현황을
  레거시 T1_Ssub(Gdate 전체일자/Hcode 출판사/Gcode·Gname 거래처/Name1·2/Gssum) 실 쿼리로
  구현. `shipping_ledger_service` — SHOW COLUMNS 캐시 어댑터(t5_ssub_adapt 패턴, 미보유
  테넌트는 빈 목록+scaffold 격하로 500 방지), 일자키 정규화, 출판사 스코프, 거래처 선택,
  정렬 화이트리스트, 페이지네이션. 현황은 출판사(Hcode)별 합계. 모델 필드 보강(gcode/gname/
  line_count/totals/truncated). form-registry phase2/STUB → **phase1**.
- **공통 그리드(DEC-082/083 그대로)**: 9화면 `DataGrid`+`useGridPrefs`+`GridColumnSettings`+
  `useListSession`, 계정코드(hcode) 입력창 **admin 전용**(일반 계정은 서버 스코프 강제),
  검색 입력 `MasterLookupField`(출판사=publisher·거래처=customer 룩업). 정렬은 서버
  (outstanding/shipping — sortBy/sortDir 화이트리스트) 또는 클라이언트(billing/cash/
  cash-status/period/tax — 소량 결과셋, `useClientSort`, DEC-082 재고현황 선례). write 흐름
  (등록/수정/취소/확정/발행/토글/인쇄/전표카드)·data-legacy-id 보존.
- **엑셀 export 전면화(DEC-089 미러)**: 8개 목록에 `export.xlsx` 라우트 신설(조회와 동일
  필터·정렬, `masters_excel.collect_all_rows`+`build_list_workbook` 재사용) + 프론트 「엑셀
  저장」 버튼. `/billing/export.xlsx` 는 `/billing/{billing_key}` 보다 먼저 등록(path 충돌 회피).
  probe 매트릭스 9건(period 목록 + 8 export) 등록.
- **회귀**: `test_dec091_settlement_normalization.py` 9건(월키/Yesno/쓰기키 원시 유지/미수 SQL
  캡처/정렬 주입 차단/라우터 스코프) + `test_shipping_ledger_scaffold.py` 6건 재작성(T1_Ssub
  실쿼리+미보유 격하+정렬) + `test_settlement_tax_invoice_chek3_optional.py` 3건 DEC-091
  반영 + 기존 정산 스위트(phase1/optional/dec085/dec086) 무회귀 → 정산 인접 82+건 PASS.
  라우터 hcode 감사 critical 0, ruff/py_compile OK.
- **잔여 이슈(후속)**: (a) 청구서/입금 목록의 `includeCancelled` 기본 숨김 — 운영 T2 Yesno
  의미가 '취소'가 아닐 경우 기본 숨김이 실데이터를 가릴 소지(별도 실측 후 기본값 재검토).
  (b) 정산 마감 UPDATE/DELETE·recalc S1_Ssub 읽기의 월키는 미정규화(쓰기 키 안전 — 별도
  검증 후 일괄 월키화 대상, DEC-085 잔여와 동일). (c) 발송비현황의 Scode 차원 집계는 출판사
  합계로 단순화(레거시 Subu44 (Hcode,Scode) GROUP 대비 축소 — 필요 시 후속 확장).
- **결정자**: 메인개발자 + 사용자 (2026-07-08 — 정산관리 하위 화면 정상화 지시)
- **참조**: DEC-082/083(공통그리드·계정코드 정책), DEC-084(Ocode 스코프 계열),
  DEC-085(월키), DEC-089(Yesno·엑셀 전면화), DEC-090(출판사 스코프 헬퍼),
  Subu41/42/43/44/45/47/49(레거시 정본), masters_excel, t5_ssub_adapt

#### DEC-091 보강 (같은 날 사용자 후속 2건)

- **도서별년말집계(Sobo67) 월단위 0건**: 레거시 Subu67 Button201Click 은 `T00` 플래그로
  **T00=1=전체 도서 월별 집계**(단일 도서 필터 없음)와 **T00=0=단일 도서 드릴다운**
  (`Bcode=St3`) 두 모드를 갖는데, 포팅이 드릴다운만 구현하고 **부모 미지정 월 조회를
  `1=0`으로 하드 차단**해 "월" 토글이 항상 0건이었다. `get_year_end_book_aggregate`
  Pass1/2 의 `1=0` 제거 → 월+부모미지정 = 전체 도서 월별(Bcode 범위 존중), 드릴다운은
  행 클릭 유지. 프론트 "월" 라디오가 `parentBcode` 를 비우도록 수정. `test_year_end_book`
  22 PASS.
- **분기/반기 손익(STAT-4) 값 미조회 — T2_Ssub 미집계 근본원인**(사용자 지적):
  `get_quarterly_summary → list_period_summary → T2_Ssub`(사전 집계 테이블)만 읽는데,
  T2 는 청구서 집계/재집계(recalc_billing)로만 채워지는 on-demand 테이블이라 **주기적
  사전계산(크론·범위 recalc)이 없음** → 운영자가 해당 분기를 집계 안 했으면 S1 실거래가
  있어도 0건. 사용자 선택 = **A(온디맨드 폴백) + C(손익 정본)**, 크론(B)은 후속:
  - **A**: `list_period_summary` 가 T2 0행이면 출고(S1_Ssub)−반품(R3_Ssub) 월별 실시간
    파생(`_period_summary_from_source`, recalc 공식). **읽기 전용**, 응답 `source`
    ('t2_ssub'|'s1_ssub_live'). 파생 SQL 은 **월키 정규화(DEC-085) + Yesno 무필터
    (DEC-081 — S1 Yesno='2'=완료)** — recalc 의 두 함정 회피.
  - **C**: 손익 정본화 — 기존 화면은 `gsumx-gsumy`(금액−**세액**)를 "청구−입금"으로 오표기
    하고 실입금(T5)을 안 읽었다. `deposits_by_month`(T5_Ssub 월합, cash_status/outstanding
    T5 패턴 재사용) 신설 → `get_quarterly_summary` 축을 **청구=T2 Sum28 / 입금=T5 /
    잔액=손익=청구−입금** 으로 재매핑. 프론트에 `source='s1_ssub_live'` 시 "마감 전 추정치"
    앰버 배지.
  - 회귀: `test_dec091_quarterly_source_fallback.py` 4 + `test_dec085`(분기 비교 재작성) +
    stats/settlement 인접 150 PASS, tsc 0, hcode 감사 critical 0.
  - **500 핫픽스**: A/C 도입 직후 quarterly-summary 500(STAT_INTERNAL_ERROR) 보고 —
    신규 원천 쿼리(S1/R3/T5)가 미존재 테이블·변형사 스키마에서 예외 → 500. `_period_
    summary_from_source`/`deposits_by_month` 를 **fail-safe**(예외 시 빈/0 격하 + warning
    로그, year-end-book Sg_Csum 패턴)로 강화. 500 → 200(값 없으면 0 표시, 로그로 원인 추적).
  - **실시간 진행률 UX**(사용자 요청): 분기별 원격 조회가 느릴 수 있어 **원형 프로그래스**로
    진행률(%) 표시. `get_quarterly_summary` 를 `_compute_quarter`/`_assemble_quarterly`
    로 분해(단일 진실원). 1차 SSE 스트림은 **버퍼링/React 배치로 0%에 고착** 보고(빠른/
    빈 데이터에서 이벤트가 한 청크로 도착) → **클라이언트 분기별 팬아웃**으로 전환:
    화면이 각 분기를 `quarterly-summary?quarters=1` 개별 요청으로 순차 호출하며 매 왕복마다
    `CircularProgress`(SVG, 토큰만) 갱신 후 합산(백엔드 축과 동일). 왕복 지연이 단계별
    진행을 보장(스트림/프록시 무관). SSE 라우트·제너레이터·구독 클라이언트는 제거.
  - **차트 Y축 단위 축약**(사용자 요청): 큰 금액이 왼쪽 축에서 앞자리째 잘림 → 금액 축은
    **천원(÷1000)** tick 포매터 + 축 라벨 "천원"(`StatsBarChart valueUnit`/`StatsLineChart
    sumUnit="thousand"` — 분기손익·기간별 매출). 수량/혼합 축은 콤마+축 폭 확대(가독성).
    툴팁은 항상 원 단위 정확값. 출판사통계는 출고수(수량)+금액 혼합축이라 천원 미적용(콤마만).
  - **발송비 500 핫픽스**(사용자 보고 2026-07-10, 라이브 재현): ① `_txt_sel` 무접두
    참조가 G7_Ggeo JOIN 에서 1052(Gcode/Gname ambiguous — 양 테이블 공존) → alias
    한정(`COALESCE(t.Gcode,…)`). ② mysql3(remote_155) 현황 정렬 1111(ORDER BY 집계식)
    → SELECT alias(`Total_Gssum`) 정렬. 수정 후 4서버 라이브 확인 — chul_05 25,763건/
    book_kb 207,778건/chul_01 131,577건/book_bs 34,871건 유입.
  - **입금(T5) 데이터 실측**(사용자 질문 2026-07-10): chul_09_db=0건(정산 모듈 미사용),
    타 테넌트는 존재하나 대부분 2011~2014 과거 데이터(book_bs 만 2026.06 까지) —
    기본 90일 조회범위에서는 0건이 정상. 화면 문제 아님(범위 확대 시 표시).
  - **입금내역 UI 보강**(사용자 요청 2026-07-10): 필터·등록폼의 자유 텍스트 날짜
    (YYYY.MM.DD/YYYYMM 수기)를 브라우저 date/month 컨트롤로 교체 — **상태·세션·API 는
    점 표기 유지**(하위호환), 입력 경계에서만 변환(dotToDateInput 등). 검색 패널
    6열 그리드 → 표준 flex items-end(조회=secondary, 신규=primary 우측 ml-auto),
    날짜 Enter=조회, 등록폼 거래처코드에 publisher 룩업. 정산 9화면 전부
    date/month 컨트롤 완비(자유 텍스트 잔존 0).
  - **잔여(B, 후속)**: `POST /billing/recalc-range` + 크론 야간 재집계로 T2 영속화(조회 성능
    + 청구/입금현황/미수 등 전체 T2 화면 일괄 정상화). 폴백(A)의 청구 공식이 recalc 와
    동일하므로, B 도입 시 배지가 자동으로 't2_ssub'(확정)로 전환.

### DEC-092: 전자책 판매분석 신규 화면 — 외부 채널 판매 요약 사이드 테이블 + 서식 2종 엑셀

- **배경**(사용자 요청 2026-07-08): 교문사 「전자책 매출분석.xlsx」 서식을 저장할 수 있는
  화면 요청 — 워크북 분석 결과 요약 서식 2종(① 연간: 연도 × 판매처[아카디피아/교보/
  북이오/노팅/스콘] × [1팀|2팀|계|전년대비], 부수·금액 2블록 ② 동일 피벗의 월범위 연도
  비교) + 채널별 원본 정산 시트(교보 47컬럼~스콘 55컬럼 이기종, 요약 수식은 대부분
  0/#REF!). **기존 화면 없음 확인**(기존 전자책 코드는 G4_Book_Ebook 마스터 부가필드
  DEC-068 뿐, 통계 화면은 전부 S1_Ssub 기반) → 통계 메뉴 하위 신규 화면.
- **저장 모델**: 전자책 판매는 외부 채널 정산 파일 데이터라 레거시 DB 에 없음 →
  ``Web_Ebook_Sales`` 사이드 테이블 신설(G4_Book_Ebook 패턴 1:1 — CREATE TABLE IF NOT
  EXISTS + REPLACE INTO, mysql3-safe). PK (Hcode, Ym, Channel, Team) — **월 단위가 두
  서식을 모두 파생 가능한 최소 granularity**. Hcode = 로그인 계정 스코프
  (enforce_hcode_isolation — 계정 소유 데이터, S1 계열과 동일 주입이 올바름).
- **입력 경로**: ① 화면 인라인 폼(년월/판매처/팀/부수/금액, 같은 키 덮어쓰기, 0/0=행
  정리) ② 롱 포맷 입력 서식(년월|판매처|팀|부수|금액) 다운로드 + 업로드(동일 키 합산,
  행 단위 부분 실패 허용 — masters import 컨벤션). 채널 원본 시트(교보/스콘 등) 직접
  파싱은 이기종 5+ 서식이라 후속 분리(워크북 요약 수식이 깨져 있어 원본 파싱도 불가).
- **출력**: ``GET /stats/ebook-sales/export.xlsx`` — 서식 2종 워크북(시트1 연간 1~12월,
  시트2 M월~N월 연도비교). 피벗 재현: 채널 순서 = 원본 표기 우선
  [아카디피아,교보,북이오,노팅,스콘]+신규 가나다(데이터 주도), 채널당 [1팀|2팀|계|
  전년대비] 4컬럼 병합 헤더, 부수/금액 2블록, 연도 desc + 계 행 + 전체 계 열.
  **전년대비 = 당년 계 − 전년 계**(원본 수식 확인 불가 — 차이값 채택, 전년 데이터
  없으면 공란).
- **적용**: backend ``ebook_sales_service.py`` + stats 라우터 6종(list/upsert/DELETE/
  import.xlsx/template.xlsx/export.xlsx, admin.stats.sales 가드), frontend
  ``/stats/ebook-sales``(DataGrid+useGridPrefs+GridColumnSettings+useListSession+클라
  정렬 — DEC-082/083 공통그리드 준수, 계정코드 admin 전용), form-registry
  ``Stats_ebook_sales``(folder ``_WebStats`` → 매트릭스 WEB_ONLY), probe 2건.
- **회귀**: `test_dec092_ebook_sales.py` 11건(SQL 스코프/REPLACE·0/0 정리/검증/파서
  합산·헤더·불량행/서식 2종 피벗 값·전년대비·연간 vs 월범위/라우트 등록) PASS,
  form-registry 가드·stats 인접·list-state(신규 페이지 covered) 무회귀, tsc/eslint/
  next build PASS. (legacy-coverage mismatch 20건·list-state 위반 7건은 기존 미커밋
  transactions/production 계열 — 본 건 무접촉 확인.)
- **잔여(후속)**: (a) 채널 원본 정산 파일(교보/아카디피아/북이오/스콘) 직접 업로드
  파싱 — 채널별 어댑터로 월 요약 자동 산출. (b) 팀 구분이 1/2 고정 — 조직 개편 시
  코드값 확장. (c) 전년대비 정의(차이 vs 증감률) 사용자 확인.
- **결정자**: 메인개발자 + 사용자 (2026-07-08 — 서식 확인 후 신규 화면 지시)
- **참조**: DEC-068(G4_Book_Ebook 사이드테이블·masters 엑셀 입출력 선례), DEC-082/083
  (공통그리드·계정코드 정책), DEC-089(엑셀 export 전면화), masters_excel

### DEC-093: 반품관리 전면 정비 — 데이터 정상화(Ocode/Yesno/날짜/스코프) + 공통그리드·키보드

- **배경**(사용자 요청 2026-07-08): 반품관리 하위 화면들을 다른 메뉴(DEC-082/083/091)와
  동일하게 정비 + 로그인 계정 데이터 기반 정상화 + 목록 표준 기능(정렬/컬럼이동/편집)·
  검색어 입력·키보드 인터페이싱. 매핑 결과: 반품 전 화면 공통그리드 0/9,
  **inventory(재생/해체/변경) 조회는 스텁(`setRows([])`)이라 3개 기능 도달 불가**,
  reports 상세는 stale-closure(한 클릭 지연) 버그.
- **레거시 정본 대조**(WeLove_FTP Subu23/24/25/51/55/58/34_4 + Base01 NewRecord,
  도서유통-출판 빌드 교차): 반품 테이블은 전부 **S1_Ssub**(R3 없음, 변경만 Sg_Csum).
  **운영 chul_09 계열 빌드에는 반품 폼이 없고** Subu21 거래명세서 경유 입력 —
  Ocode 'A'/''/혼재, Yesno='O'(문자 O) 등. 레거시 반품 조회에 **Yesno 필터 전무**,
  쓰기는 접수='1'/완료='2'(Base01 L7883~).
- **데이터 정상화 4종**:
  1. **Ocode**: 조회 3곳(`list_returns`/일별 마스터·상세)의 `='B'` 리터럴 제거(DEC-084
     잔여 (a) 해소 — Gubun='반품'+Scode='X' 만으로 판별, ledger/period 무 Ocode 선례).
     INSERT 는 `_default_outbound_ocode(server_id)` 서버 가변(chul_09='A' — 출고/입고
     INSERT 동일 컨벤션, 양방향 불일치 차단).
  2. **Yesno**: INSERT '0'→**'1'(레거시 접수)**. 읽기측 `s.Yesno='1'` 필터 9곳 전부
     제거(웹 등록 반품이 원장/기간 화면에서 안 보이던 이중 버그 + 운영 혼재값 제외).
     목록 기본 `HAVING MAX(Yesno)<>'2'` 제거(DEC-081 미러 — '2'=완료, 취소 아님) +
     **3-state status**(pending/received/done, 구 active/cancelled 하위호환 Literal).
     처리 경로(부분 재생/해체 FOR UPDATE 가드)의 Yesno='1' 은 유지(쓰기 가드).
  3. **날짜 정규화**: ledger/period 가 대시(`YYYY-MM-DD`) 입력을 무정규화로 점 표기
     Gdate 와 BETWEEN 비교하던 0건 갭 → `_normalize_gdate` 적용.
  4. **스코프(크로스테넌트 차단)**: 일별 상세 무필터 → 로그인 스코프 폴백 +
     `detail_for_hcode` 에 `enforce_hcode_identity` tamper 가드(일별·기간 공통),
     기간 KPI 에 hcode 필터 추가(종전 전 테넌트 합산 노출).
- **inventory 목록 신설**: `GET /returns/inventory-candidates` — 미처리 반품 라인
  (Gubun='반품', Scode='X', 행 id 포함) 목록. 모던 처리 축(재생/해체=행 id, 변경=
  Gdate/Hcode/Bcode)에 맞춰 3개 탭 단일 소스. 스텁이던 화면 조회 실동작화.
- **엑셀 export 4종**: 목록/재고원장/기간별/일별 `export.xlsx`(masters_excel 재사용,
  조회 동일 필터). probe 5건(candidates+export 4) 등록.
- **공통 그리드 + 키보드**(프론트 5화면): DataGrid+useGridPrefs+GridColumnSettings+
  useListSession(+기간/일별 신규)+클라 정렬, 계정코드 admin 전용(publisher 룩업),
  도서 book 룩업, 날짜 Enter=조회, `enableKeyboardNav`+`onRowEnter`(Enter=상세/선택),
  「엑셀 저장」. 목록의 취소포함 체크박스 제거(항상 표시+상태 배지). write 흐름
  (등록/수정/취소/재생/해체/변경/롤백/가져오기, AuditPasswordModal 게이트) 전부 보존.
  reports stale-closure 상세 지연 버그 수정.
- **회귀**: `test_dec093_returns_normalization.py` 12건(INSERT 파라미터화/Yesno 어휘/
  읽기필터 부재/KPI 스코프/일별 상세 폴백/후보 목록/날짜 정규화/라우트 등록) +
  기존 반품 스위트 71 PASS·3 skip 무회귀, 라우터 hcode 감사 critical 0.
- **잔여(후속)**: (a) 모던 소프트취소(PATCH cancel=Yesno '2')가 레거시 완료와 동치 —
  '취소' UI 라벨 재검토(완료 처리로 개명 여부 사용자 확인). (b) 라인 편집 후 요약
  재계산의 Yesno='1' 읽기 — 레거시 혼재값 슬립 편집 시 저계상 가능(별도 검증).
  (c) 반품 INSERT 에 거래처(Gcode) 미기록 — 레거시는 기록(스키마 확장 별도 사이클).
- **결정자**: 메인개발자 + 사용자 (2026-07-08 — 반품관리 정상화 지시)
- **참조**: DEC-084 잔여 (a), DEC-081(Yesno='2'=완료), DEC-082/083/091(공통그리드),
  _default_outbound_ocode/h2_gbun_adapt, Base01.pas NewRecord 정본

### DEC-094: 청구서 인쇄(미리보기, Sobo46) 복구 — Sum38/39 유령 컬럼 + 월키 3종 사고

- **증상**(사용자 보고 2026-07-09): 정산관리 청구서 인쇄(미리보기) 작동 안 함.
- **근본 원인 3종** (레거시 Subu46.pas L648-655/L781-787 원문 대조 —
  `settlement_print_service` 가 DEC-085/091(월키)·DEC-058(컬럼 어댑터) 사이클에서
  누락된 모듈이었음):
  1. **유령 컬럼**: 정적 헤더 SELECT 가 `range(1,49)` 로 Sum38/Sum39 포함 — 레거시
     원문은 Sum01~37 + **Sum40**~48 로 38/39 를 건너뜀(컬럼 부재) → 1054 (Unknown
     column) → **전 서버 HTTP 500**. 변형사 T2 는 Sdate/Chek3 등도 부재(DEC-058 계열).
  2. `WHERE Gdate=%s` 원시 비교 — 레거시 T2.Gdate 점 표기('2026.07') → 404.
  3. 라인 `LEFT(Gdate,6)` — 점 표기 전체일자('2026.07.15')에서 '2026.0' → 라인 0건.
- **수정**: `_build_sql_print_header(cols)` 동적 SELECT (`tax_invoice_service._t2_columns`
  SHOW COLUMNS 캐시 재사용 — 존재 컬럼 IFNULL/COALESCE, 부재 컬럼 정적 리터럴 alias,
  67개 sum 응답 스키마 보존) + 헤더/라인 WHERE `_t2_month_key()` 정규화 + gdate 입력
  방어 정규화(`_norm_month`). HTML/PDF 빌더는 동일 데이터 재사용이라 무수정 복구.
- **회귀**: `test_dec094_billing_print.py` 5건(부재 컬럼 리터럴/월키/라인 정규화/
  레거시 형태 200+스키마/404) + 정산 인접 72 PASS. TestClient E2E(레거시 형태 mock)
  print-data·print(html) 200 + 마감 배지·라인 렌더 확인.
- **결정자**: 메인개발자 (레거시 Subu46 원문 대조)
- **참조**: DEC-034(인쇄 미리보기 정책), DEC-058(_t2_columns), DEC-085/091(월키),
  DEC-090(스코프 — 인쇄는 enforce_hcode_identity 키 가드 유지)

### DEC-095: 비-기본 DB 테넌트 전 화면 0건 — 테넌트 DB 요청 컨텍스트 신설

- **증상**(사용자 보고 2026-07-09): 「도서출판 배움」 로그인 시 아무 데이터도 조회·출력
  안 됨.
- **근본 원인 — 멀티 DB 라우팅 구조 갭**: 배움 = remote_153 / **chul_05_db** / hcode
  1002. 로그인은 메타 인덱스가 고른 chul_05_db 의 Id_Logn 으로 검증되고 JWT 에
  ``rdb=chul_05_db`` 클레임까지 실리지만, 데이터 API 의 ``_effective_database`` 는
  **inspect 오버레이 또는 서버 프로필 기본 DB(chul_09_db)** 만 반환 — rdb 를 적용하는
  코드가 없어 모든 조회가 엉뚱한 DB 로 감. 라이브 검증: chul_09_db 의 S1_Ssub
  (Hcode=1002) **0건** vs chul_05_db **444,262건**. 지금까지 chul_09 계열 계정만
  테스트되어 잠복(DEC-084 의 "운영 4서버=전부 chul_09_db" 가정도 같은 뿌리).
- **수정**: `app/core/tenant_db_context.py` 신설 — 요청 범위 ContextVar
  ``(server_id, db_name)`` (inspect_context 동일 패턴, app 의존 0).
  `get_current_user` 가 JWT ``rdb`` 를 바인딩, `_effective_database` 우선순위 =
  **inspect > 테넌트(요청 서버 일치 시) > 프로필 기본**. mysql3/트랜잭션 경로 포함
  전 쿼리 자동 적용. chul_09 계정(rdb=기본값)·수퍼(rdb='')는 동작 무변화.
- **회귀**: `test_dec095_tenant_db_context.py` 7건(기본/오버라이드/서버 불일치 미적용/
  inspect 우선/빈값 미바인딩/JWT 바인딩→유효 DB/무 rdb 기본 유지) + 인증·정산·반품
  인접 87 PASS. 라이브: 컨텍스트 바인딩 후 화면 동일 쿼리 444,262건 반환 확인.
- **잔여(후속)**: (a) `user_prefs`/`grid_prefs` 등 Web_* 사이드테이블도 이제 테넌트 DB
  에 생성됨 — 기존 기본 DB 에 저장된 프리퍼런스의 이관 여부 검토. (b) 배움 외
  비-기본 DB 계정(book_11_db 등) 광역 실측.
- **결정자**: 메인개발자 (라이브 교차 검증 — chul_09 0건 vs chul_05 444,262건)
- **참조**: DSN-DEC-08/12(로그인 라우팅·rdb 해석), inspect_context(패턴 선례),
  DEC-084(chul_09 단일 가정)

### DEC-096: 로그인 조직(소속) 선택 챌린지 — 동일 ID+비밀번호 크로스 DB 672건 해소

- **배경**(사용자 제안 2026-07-09): 동일 아이디+비밀번호가 복수 테넌트 DB 에 등재된
  계정 실측 **672건**(다중 후보 716 의 94% — DSN-DEC-09 v2 의 "매우 드물다" 가정과
  정반대). first-match 로 항상 같은 DB 에 고정 진입해 다른 소속 데이터 접근 불가.
  사용자 제안 = 로그인 시 조직명 선택 → Slack 워크스페이스 선택 패턴으로 채택.
- **설계 (2단계 로그인)**:
  1. ID+비밀번호 제출 → **인덱스 유래 고신뢰 후보**(candidate_via ∈ index_single/
     index_ambiguous — 사용자가 실제 등재된 DB, 716건의 근원)가 복수이고 힌트가
     없으면 전 후보 비밀번호 검증(probe 2~5개; directory_sweep 등 추측 후보는 제외 —
     39개 probe 폭주·오염 방지).
  2. **복수 검증 성공 시 토큰 미발급** + `409 ORG_SELECT_REQUIRED` + choices
     [{serverId, dbName, tenantId, hcode, label}] — 라벨은 tenants_directory
     `tenant_label_kor`, 폴백 account_family/db_name. **선택지는 비밀번호가 실제
     검증된 후보만**(자격 증명 보유자 한정 공개 — 정보 누출 없음). 감사 로그
     reason='org_select_required'.
  3. 프론트 선택 UI → `tenantId`(우선)/`dbName`(신규 LoginRequest 필드) 재제출 →
     후보 단일화 → 정상 발급. 단일 검증/단일 후보는 기존 흐름 그대로(무회귀).
- **적용**: backend `auth.py`(후보 내로잉 + 챌린지) + `models/auth.py`(`db_name`
  필드 추가 — 기존 userId/tenantId/hcode AliasChoices 무변경), frontend
  `auth-context.tsx`(LoginHints.dbName) + `login/page.tsx`(선택 카드 UI, 입력 변경
  시 초기화). DEC-095 테넌트 DB 컨텍스트와 합쳐져 선택한 소속의 DB 로 전 화면 조회.
- **회귀**: `test_dec096_org_select_login.py` 5건(복수 검증 409+선택지 2건+스윕 제외/
  tenantId·dbName 재제출 200/단일 검증 통과/단일 후보 무챌린지) + 로그인 인접
  23 PASS(스윕 mock 이 챌린지를 오발화하던 1차 구현을 테스트가 검출 → 우주를
  인덱스 후보로 한정). tsc/next build PASS. (auth-context L168 eslint 는 기존 이슈.)
- **보강 (같은 날 사용자 지시 — 한글 계열명 + 로그인 기본 처리)**:
  ① 라벨 해석기 강화 — tenant_id 직결 → `resolve_unique_tenant`(공유 DB hcode
  격리, 예: chul_09 의 교문사/위러브3 구분) → `find_owning_tenants` 첫 라벨 →
  계열/DB 폴백. 충돌 라우트 21곳 실측 18곳 한글 라벨(고려물류/중앙라인(한강북)/
  한국도서유통/한강물류 등), 미등록 3곳(book_gs/book_js/remote_138 chul_09)은
  디렉터리 라벨 보강 대상. ② **기억된 소속 자동 적용** — 최초 1회 선택을
  localStorage(`bls_org_pref:<userId>`)에 저장, 이후 로그인은 챌린지 발생 시
  자동 재제출(=로그인 기본 처리, 선택 UI 생략). ID 입력란 아래 「기본 소속:
  {라벨} (자동 적용) · 변경」 으로 초기화 수단 제공, 자동 적용 실패(소속 제거
  등) 시 기억 초기화 후 선택 UI 폴백.
- **보강 2 (같은 날 — 회사 선택 콤보 상시 노출)**: 사용자 지시로 로그인 폼
  「고급 옵션(회사 코드 Hcode/테넌트 ID 수기 입력)」 블록 **제거**, ID 위에
  **회사 선택 콤보**(기본 = 「자동 결정 (통합 로그인)」) 상시 노출. 옵션은 신규
  공개 엔드포인트 `GET /api/v1/auth/org-options`(tenants_directory 활성 테넌트의
  한글 라벨+tenant_id 만 — 서버/DB 좌표·비밀 무노출, 40건) 로 로드, 선택 시
  `tenantId` 힌트로 후보 단일화. DSN-DEC-12 모호(fail-closed) 안내문도 콤보
  기준으로 갱신. 챌린지(409)·기억된 소속 자동 적용은 콤보 '자동' 경로의
  폴백으로 유지.
- **잔여(후속)**: (a) 디렉터리 한글 라벨 미등록 3계열 보강 + '(테스트용)' 류
  테넌트 is_active=false 정리(콤보 노출 대상 제외). (b) DSN-DEC-09 v2
  문서의 "드물다" 서술 갱신.
- **결정자**: 메인개발자 + 사용자 (2026-07-09 — 조직명 선택 제안)
- **참조**: DSN-DEC-08/09 v2(후보 probe·narrowing), DEC-095(테넌트 DB 컨텍스트),
  account-hcode-groups.md(672건 실측)

### DEC-097: 거래명세서(Sobo21) Enter=저장·선택·진행 정합 — 고객 수정요청 5건 대응

- **배경**(고객 수정요청 2026-07-16, 위러브솔루션 레거시 사용자): ① 신규 등록 시
  거래처명/도서명 자동완성 팝업이 "떴다 안 떴다" ② Enter 로 옆 칸 이동이 안 되는
  곳이 있음 ③ 도서 선택 후 공급율·수량으로 포커스가 안 넘어가는 경우 다수
  ④ 빈 줄에서 Enter 시 줄이 계속 늘어남 ⑤ 거래명세서 목록에서 줄 클릭 팝업이
  도서명 변경 불가. 총론 = "레거시(Enter=저장·선택 기능) 그대로".
- **원인 진단**: ① `MasterLookupField` 가 디바운스 200ms 완료 + 결과≥1건일 때만
  드롭다운을 열고(대기 중/0건 무표시), 디바운스 완료 전 Enter 는 별도 즉시조회
  경로로 분기(단일건 자동선택/다건 다이얼로그) — 사용자에겐 비결정적으로 보임.
  추가 발견 2건: Enter 자동확정 후 `onKeyDown(e)` 위임 → 소비자가 stale state 의
  bcode 로 재조회해 "책을 골랐는데 또 팝업"; Escape 가 stopPropagation 없이 페이지
  Esc(목록 이탈)와 동시 발화. ③ 마우스/다이얼로그 선택 경로(`onInlineSelect`/
  `onSelect`)에 포커스 이동 코드 부재(Enter 경로만 이동). ④ `addLine()` 무조건
  append(저장 시 필터만). ⑤ 한줄 팝업이 도서를 정적 텍스트로 렌더 + `saveLineEdit`
  가 항상 원본 bcode 재전송(백엔드는 (gcode,bcode) diff 로 이미 변경 지원).
- **채택**(레거시 Subu21.pas Enter 체인 재현 — Edit111/114KeyPress·DBGrid101KeyPress
  L1189·KeyDown L1306):
  1. **자동완성 결정화**: 4상태 패널(idle/loading "검색 중…"/results/empty "결과
     없음")로 입력 즉시 표시, 응답 순서 가드(seq), Enter 는 디바운스 flush 후 단일
     경로 — 정확일치/1건 자동확정+다음 칸(레거시 Seek 1건 자동선택), 0건/다건 검색
     팝업(`handleDialogOpenChange` — 제어형 다이얼로그도 열림). 자동확정 후
     `onKeyDown` 위임 제거(항상 `focusNextFrom`), Escape `stopPropagation`, 한글
     IME 조합 중 Enter 무시. props 무변경 — 인라인 사용 45개 화면 공통 수혜,
     `onKeyDown` 직접 전달처는 신규 페이지 2곳뿐이라 파급 최소.
  2. **신규 페이지 Enter 체인**: 헤더 거래일자→거래처→지점→그리드(레거시 SetFocus
     체인), 그리드 `EDIT_COLS` = 구분→도서코드→수량→단가→비율→비고(레거시 컬럼
     걷기 — 기존 "수량 Enter→바로 새 줄" 단축 제거, 사용자 확정), 비고 Enter→새 행
     (직전 행 구분 승계, 새 행 구분 열 복귀), 그리드 Esc→헤더(레거시 Edit101),
     구분 Enter 시 비율 재조회(레거시 SIndexs=0 Grat1 재조회). 저장 후 연속 입력
     포커스는 거래처로.
  3. **선택 후 수량 포커스**: 도서 선택 3경로(인라인 클릭/다이얼로그/Enter 자동확정)
     모두 수량으로 이동. 거래처 선택 시 지점으로 이동.
  4. **빈 행 가드**: 현재 행 도서코드가 비어 있으면 비고 Enter/"라인 추가" 버튼
     모두 행을 늘리지 않고 그 행 도서코드로 유도(신규 페이지 + 전체 수정 팝업
     `addLineFromMemo`/`addLine` 동일). 수량≤0 은 입력 중 차단하지 않음(저장 시
     validate 가 행 번호로 안내).
  5. **한줄 팝업 도서 변경**: `sales-statement-line-edit-dialog` 에 도서
     MasterLookupField 신설(line-defaults 로 도서명·단가·비율 채움+수량 포커스),
     `saveLineEdit` 이 draft.bcode 전송 — 서버 (gcode,bcode) diff 가 DELETE+INSERT
     처리(신규 라인 Yesno='0' 접수 초기화). **같은 전표 내 중복 bcode 는 서버
     desired dict 가 무언 병합(마지막 승리)해 라인이 유실되므로 클라이언트에서
     차단**(에러 안내). Enter 체인 수량→단가→비율→비고→저장&닫기 + 열릴 때 수량
     autoFocus.
- **범위 제외(사용자 확정)**: 라인 입력순서 정렬(현재 `ORDER BY Gcode, Bcode` 로
  입력순 소실 — 레거시는 auto-increment `ID` 표시 순) — 추후 백엔드 ORDER BY 변경
  으로 대응 예정. outbound `order-line-grid`/inbound `BookBcodeCell`(동일 결함 보유)
  개별 수정은 후속 — 공통 컴포넌트 수정 혜택은 자동 적용.
- **적용**: frontend `master-lookup-field.tsx`(상태기계 재작성),
  `transactions/sales-statement/new/page.tsx`, `sales-statement/page.tsx`
  (saveLineEdit draft.bcode + 팝업 props), `sales-statement-line-edit-dialog.tsx`
  (도서 변경), `sales-statement-edit-dialog.tsx`(빈 행 가드). 백엔드 무변경.
- **검증**: tsc 0 / eslint 신규 이슈 0(기존 이슈 4건 잔존) / dev 라우트 컴파일 200 /
  hub pytest `-k sales_statement` 148 PASS·2 FAIL(백엔드 무변경이라 기존 실패).
  수동 E2E(운영 DB 라 자동 기입 미수행): 팝업 3상태·빠른 Enter 자동확정·빈 행
  연타·3경로 수량 포커스·한줄 팝업 도서 변경/중복 차단.
- **보강 (같은 날 사용자 지시 — "모든 검색창에서 결과 선택+Enter=즉시 반영" 전수 점검)**:
  검색 UI 전수 인벤토리 결과 이미 정상 = `SalesStatementSearchDialog`(↑↓/Enter 확정),
  `DataGrid enableKeyboardNav` 사용 화면(~11곳), `order-line-grid`(공용 필드).
  처리 4건: ① **공용 검색 팝업 `MasterLookupDialog` 키보드 흐름 완성** — 검색 입력
  autoFocus, Enter=검색(결과 1건이면 즉시 확정 — 레거시 Seek 1건 자동선택, 같은
  키워드 재-Enter 면 강조 행 확정), 검색 직후 **첫 행 자동 선택**, ↓ 로 결과
  그리드 진입(기존 DataGrid ↑↓/Enter/더블클릭 확정과 연결), IME 조합 가드.
  ② **입고 수정 그리드 `BookBcodeCell`(마우스 전용 구식 자동완성) 제거** →
  공용 `MasterLookupField(book)` 교체(키보드 선택·4상태 패널·검색 팝업 자동 획득;
  `InboundLineGrid` 의 serverId prop 은 인터페이스 유지·내부 미사용). ③ 회원가입
  `WhitelistPicker` 키보드 선택 추가(↑↓/Enter/Esc + blur 닫힘 + 활성 행 강조).
  ④ 고아 컴포넌트 `outbound/customer-search.tsx`(CustomerSearchInput, 사용처 0)
  삭제 — 마우스 전용 구식 패턴 재사용 방지. 잔여(후속): `return-line-grid` 도서코드는
  결과 목록 자체가 없음(정확 코드 입력만) — 검색 UI 도입은 별도 결정.
- **보강 2 (같은 날 사용자 지시 — 거래현황(상세) 검색 팝업 필터 순차 입력)**:
  스크린샷 지목 화면 `sales-statement-search-dialog.tsx`(Sobo20). 기존 "필터 아무
  칸에서나 Enter=검색"을 레거시 순차 입력 흐름으로 교체 — **Enter=다음 필터 칸**
  (거래일자 시작→종료→거래구분→전표구분→거래처명→도서구분→도서코드→취소포함,
  `focusNextFilter` 가 패널 내 input/select 를 DOM 순으로 걷기), **마지막 칸(취소포함)
  Enter=검색 실행**, **Ctrl(⌘)+Enter=어느 칸에서든 즉시 검색**(버튼 라벨도
  "검색 (Ctrl+Enter)"). 필터 패널에 `data-enter-scope` 부여 — 거래처명/도서코드
  자동완성 확정 후 다음 포커스가 패널 안(도서구분/취소포함)으로 이동. 전역 Esc
  (capture) 리스너는 자동완성 패널이 열린 입력(`[role="combobox"][aria-expanded]`)
  이면 양보 — Esc 1회=패널 닫기, 2회=팝업 닫기. IME 조합 Enter 가드. 푸터 힌트 갱신.
- **보강 7 (2026-07-17 사용자 리포트 — 신규 출고명세서 그리드 컬럼 너비 조절 부재)**:
  신규 거래명세서 라인 그리드(수제 `<table>`)가 다른 표준 목록(DataGrid)처럼 컬럼
  너비 드래그 조절이 안 됨 — 고정 `widthPercent` + 순서 드래그만 있었음. DataGrid
  의 리사이즈 패턴을 이식: `<th>` 오른쪽 경계에 `cursor-col-resize` 핸들 + `startColResize`
  (min 40px, `gridPrefs.onColumnResize` → 계정별 서버 저장), 저장된 px 너비 우선 적용
  (없으면 % 기본). 너비 조절 제스처 중에는 `suppressColDragRef` 로 순서변경 드래그
  억제(공통 DataGrid 와 동일). 헤더 title 을 "순서변경 · 오른쪽 경계 드래그: 너비
  조절"로 갱신.
- **보강 9 (2026-07-17 사용자 리포트 — 거래명세서 수정 팝업 구분 select Enter 이동 부재)**:
  전체수정 팝업(`sales-statement-edit-dialog`, multi-row) 구분(pubun) `<select>` 에서
  Enter 로 다음 칸(도서코드) 이동 안 됨. 원인 2중: ① select 에 `onKeyDown` 미부여,
  ② `focusNextFrom` 이 `input` 만 조회(select 제외)라 시작 노드가 select 면 index -1
  → 첫 행으로 튐. **수정**: `focusNextFrom` 쿼리에 `select:not([disabled])` 추가(다음
  포커스는 `HTMLInputElement` 일 때만 `.select()`), `focusNextCell` 타입 `HTMLElement`
  로 확장 + 한글 조합 Enter 가드, 구분 select 에 `onKeyDown={focusNextCell}` 부여.
  (한줄수정 팝업은 이미 `enterTo(qtyRef)` 보유 — 무변경.)
- **보강 8 (2026-07-17 — 검색 첫 ↓ 가 둘째 항목 선택 = 한글 IME 이중 keydown)**:
  결정적 단서 "검색 직후 첫 ↓ → 둘째, 좌/우 키 먼저 누르면 그 다음 ↓ → 첫째"로
  원인 확정 — **한글 IME 조합 중 물리적 ↓ 1회가 keydown 2회(IME keyCode 229 +
  실제 키) 발생**하는데, 화살표 핸들러에 `isComposing` 가드가 없어 `activeIdx`
  -1→0→1 로 두 칸 이동(둘째 선택). 좌/우 키는 조합을 커밋시켜 다음 ↓ 는 1회만
  발생(첫째). **격리 재현으로 확증**: (1) 순수 로직 복제본은 정상(-1→0), (2) IME
  이중 keydown(isComposing true→false) 시뮬레이션 시 가드 없음=1(둘째)·가드 있음=0
  (첫째). **수정**: `MasterLookupField` 인라인 ArrowDown/ArrowUp, `MasterLookupDialog`
  검색 입력 ArrowDown, `DataGrid` 키보드 네비 ArrowDown/ArrowUp 에 `isComposing`
  가드 추가(조합 keydown 무시). (보강 6·7 의 첫-항목 관련 조치는 IME 아닌 경로의
  보강으로 함께 유지.)
- **보강 6 (2026-07-17 사용자 리포트 — 검색 팝업 첫 ↓ 가 둘째 항목 선택)**:
  인라인 결과 상태에서 Enter → 검색 팝업(MasterLookupDialog) → 첫 ↓ 가 **첫 행을
  건너뛰고 둘째 행**을 선택. **원인 2중**: ① `DataGrid.handleKeyDown` 의 ArrowDown 이
  `cur = focusedIndex>=0 ? focusedIndex : 0; moveTo(cur+1)` 라, 미선택(focusedIndex=-1,
  자동선택 async 미반영/타이밍) 상태에서 첫 ↓ 가 `moveTo(0+1)=1` → 둘째 행. ② 검색
  입력 ↓ 는 그리드에 포커스만 주고 첫 행 선택을 명시하지 않음. **채택**: ① DataGrid
  ArrowDown/ArrowUp 을 `moveTo(focusedIndex<0 ? 0 : focusedIndex±1)` 로 — 미선택 첫 ↓ =
  첫 행(전 키보드네비 그리드 공통 개선, 표준 동작). ② 검색 입력 ↓ 에서 첫 행
  (`config.rowKey(rows[0],0)`) 명시 선택 후 그리드 진입 — 자동선택 타이밍과 무관하게
  결정적. 이후 ↓ 는 둘째 행으로 정상 진행.
- **보강 5 (2026-07-17 사용자 리포트 — 검색창 브라우저 자동완성 차단)**:
  거래처 MasterLookupField 에서 앱 자동완성 드롭다운(00001…) 위에 브라우저 자체
  입력기록 자동완성("교보"/"교")이 겹쳐 표시됨. 공용 검색 입력에 브라우저 자동완성/
  자동수정/비밀번호매니저 오버레이 차단 속성 부여 — `MasterLookupField` 입력 +
  `MasterLookupDialog` 검색 입력 모두: `autoComplete="off"`, `autoCorrect="off"`,
  `autoCapitalize="off"`, `spellCheck={false}`, `data-1p-ignore`,
  `data-lpignore="true"`. 공용 컴포넌트라 인라인 사용 45+ 화면 + 검색 팝업 일괄 적용.
  로그인/회원가입 등 자동완성이 유용한 폼은 공용 `Input` 기본값 미변경으로 영향 없음.
- **보강 4 (2026-07-17 사용자 리포트 — 신규 명세서 거래처→지점 포커스 누락)**:
  거래처 확정 시 지점명(지사) 드롭다운이 자동 생성되는데 포커스가 이를 건너뛰고
  그리드로 넘어감 — 사용자가 지점 선택 불가. 지점 목록은 거래처 선택 시
  `customerBranchList` 로 **비동기 로드**되어, 확정 직후 동기 포커스는 로딩
  자리표시자만 렌더된 상태라 그리드로 샜다.
  - **1차 시도(nonce+effect) 실패**: 확정과 같은 render 에서 nonce 가 effect 를 즉시
    실행시키는데, 이 render 의 `branchLoading` 은 아직 false(branch 로드 effect 의
    setBranchLoading(true)는 다음 render 반영)라 "로딩 아니면 즉시 포커스"가 premature
    하게 그리드로 폴백 — 여전히 건너뜀(사용자 재리포트).
  - **2차 rAF 시도 기각**: rAF 는 React passive effect 보다 먼저 실행돼 로딩 상태 미반영
    → 부분입력→선택 경로를 오히려 깨뜨림.
  - **확정 채택(순수 state/effect, 경합 제거)**: 지점 로드 완료된 hcode 를
    `branchesForHcodeRef` 로 추적. 확정 시 플래그+nonce 만 올리고, effect 가:
    ① 로딩 중이면 대기, ② 지점이 **현재 거래처 기준으로 이미 로드**면 즉시(전체코드
    입력 후 확정·동일거래처 재확정 경로), ③ **방금 로드 완료(true→false)** 면 반영
    (부분입력→드롭다운 선택 경로 — hcode 변경으로 새 로드), ④ 새 로드 예정이면 대기
    (premature 그리드 폴백 방지). rAF/타이머 없음. 지점 있으면 드롭다운 포커스(선택
    가능)·없으면 그리드. `selectItem` 이 `onValueChange(hcode)` 로 거래처를 바꾸므로
    부분입력→선택 시 새 로드가 트리거됨을 확인. MasterLookupField 내부 `focusNextFrom`
    은 헤더 `data-enter-scope` 스코프라 로딩 중 그리드로 새지 않음(공존).
- **보강 3 (2026-07-17 사용자 지시 — 거래명세서 인라인 필터 패널 순차 입력)**:
  스크린샷 지목 = 거래명세서 목록 화면 본문 필터 패널(Sobo21.Panel001, 검색 팝업이
  아니라 `sales-statement/page.tsx` 인라인). 보강 2(Sobo20 팝업)와 동형 패턴 이식 —
  패널에 `data-enter-scope`+`filterPanelRef`, `focusNextFilter`(input/select DOM 순,
  읽기전용 거래처명·숨김·비활성 종료일(당일만 시) 스킵) + `onFilterKeyDown`:
  **Enter=다음 칸**(거래구분→거래차수→거래처코드→[지사]→취소포함→[전표번호]→시작일→
  종료일→당일만), **마지막 칸 Enter=검색**, **Ctrl(⌘)+Enter=즉시 검색**. 종료 검색은
  조회 버튼과 동일 분기(`runFilterSearch`: 전표번호/거래차수 있으면 commitPrimaryAndSearch,
  아니면 load). **예외**: 전표번호(Edit109)는 힌트 문구("입력하고 Enter 또는 조회")대로
  자체 Enter=즉시 조회 유지. 거래처코드 MasterLookupField 는 자동완성 확정 후
  `focusNextFrom`(data-enter-scope)으로 패널 안 다음 칸 이동, 빈값 Enter 는 onKeyDown
  위임으로 다음 칸. IME 조합 Enter 가드. **전수 확인**: 인라인 필터 순차 Enter 미적용
  화면은 이 페이지가 유일(나머지 조회 화면은 단일 필드/DataGrid).
- **결정자**: 사용자 (2026-07-16 — 고객 수정요청 전달 + 3택 확정: 입력순서 스킵/
  한줄 팝업 도서 변경/레거시 Enter 순서; 2026-07-17 — 보강 3 인라인 필터)
- **참조**: DEC-028/053(레거시 정합), DEC-065(화면 내 신규), Subu21.pas
  DBGrid101KeyPress·KeyDown, `sales_statement_create_service.update_sales_statement`
  (gcode,bcode) diff

### DEC-098: 교문사(출판사 테넌트) 통계 권한 정합 — 사이드바 별칭 인식 + /stats/publisher 게이트 키 통일

- **배경**(2026-07-16, 교문사 = remote_153/chul_09 공유 DB의 출판사 테넌트): 통계
  메뉴가 안 보이거나, 보이는 메뉴(출판사 통계)를 열면 403. 조사 결과 권한 체계의
  두 비대칭이 원인:
  1. 페이지 `PermissionGuard` 는 `hasAliasedPermission`(별칭 브리지
     `admin.stats.* ⇐ report.*`)을 쓰는데 **사이드바 `has()` 는 정확 일치만** 판정 —
     report 권한만 있는 계정은 "페이지는 통과인데 메뉴는 숨김".
  2. `/stats/publisher` 는 DEC-083 이 **사이드바 키를 `settlement.report.read` 로
     완화**했으나 페이지 가드/백엔드 `require_permission` 은 `admin.stats.customer`
     로 남아 — "메뉴는 보이는데 열면 403"(교문사가 본 화면).
- **채택**:
  1. `use-permissions.ts` 의 `has`/`hasAny`/화면 caps 리졸버가 `hasAliasedPermission`
     을 함께 보도록 통일 — 사이드바/페이지/백엔드 3곳이 같은 판정 규칙.
  2. `/stats/publisher` 본조회 + `export.xlsx` 의 `require_permission` 과 페이지
     가드를 `settlement.report.read` 로 통일(DEC-083 사이드바 키와 정합). 행 스코프는
     `resolve_publisher_row_scope` 가 별도 강제(테넌트=자기 출판사 고정)라 hcode
     격리 무영향 — admin.stats 는 데이터 격리 장치가 아니라 메뉴 게이트.
- **데이터 조치 완료(사용자 승인 2026-07-17 — "통계관리 하위 전 화면 read 접근")**:
  교문사 실계정 `Id_Logn`(remote_153/chul_09_db, hcode=5019·gname=교문사·gcode=교문사
  단일 행) Fxx 실측 후 통계 8셀을 **'R'(Read-Only)** 부여 —
  **F36**(report.read) **F37**(report.inventory.read) **F43**(settlement.report.read)
  **F51**(report.kpi.read → admin.stats.* 4종 별칭) **F55**(report.book.read)
  **F56**(report.cust.read) **F57**(report.month.read) **F58**(report.year.read).
  근거: 통계 메뉴 requiredPermission 전수 매핑(form-registry ↔ web_admin
  legacy_permission_map) — **F51 단독은 admin.stats.* 4종만 커버**하고 report.* 계열
  화면(도서별판매·거래처판매·년말집계·월별·거래처통계·도서통계·출판사통계·전자책판매
  분석)은 각 report 코드 셀이 별도 필요. `_merge_fxx_to_permissions` 시뮬레이션으로
  화면 요구 코드 11종 전부 충족 확인(role=operator 유지 → 테넌트 hcode 격리 무영향,
  전부 read 라 쓰기 미발생). 스크립트 `/tmp/grant_gyomun_stats.py`(단일 행 가드 +
  셀별 before/after + 재조회 검증 + 멱등). **적용 반영은 재로그인 필요**(권한은 JWT
  발급 시 합성). 롤백: F36/F37 은 NULL, 나머지는 'X' 로 되돌림.
- **검증**: `test_c13_stats_phase1.py::test_S_05` 갱신 — stats 라우터 허용 코드
  집합에 `settlement.report.read` 포함 + `/publisher` 본조회·export 2곳에만 부착
  가드. 관련 서브셋 pre/post 비교 신규 회귀 0건.
- **결정자**: 메인개발자 (2026-07-16 — 교문사 사용자 리포트 기반) + 사용자
  (2026-07-17 — 통계관리 전 화면 read 데이터 조치 승인·실행)
- **참조**: DEC-083(사이드바 키 완화), DEC-044(admin.stats 권한 4종),
  `frontend/src/lib/permission-aliases.ts`, `resolve_publisher_row_scope`

### DEC-099: 전표번호 표기 정본(Idnum) 통일 + 거래현황 컬럼 정렬 + 창 닫기 시 목록 검색세션 초기화 — 고객 리포트(2026-07-16) 대응

- **배경**(고객 리포트 2026-07-16 오후, 위러브솔루션): ① 거래현황(LIST/상세/요약)
  전표 번호가 화면마다 안 맞음 ② 카테고리(컬럼) 오름차순/내림차순 정렬 요청
  ③ 거래현황·출고현황 등 창을 닫고 다시 열면 이전 검색 데이터가 그대로 남음
  ④ 출고접수관리 "전표" 번호 확인 요청.
- **원인 진단**(①④): `Jubun`(거래처별 차수=키)과 `Idnum`(일자별 전표번호=표시 정본,
  DEC-064 5자리 zero-pad) 혼용으로 4가지 표기 공존 — 거래현황=raw Jubun,
  출고접수=Jubun 5-pad(정본 오용), 거래명세서=Idnum 5-pad(정본), 출고현황=raw Idnum.
  출고접수는 백엔드가 Idnum 을 아예 반환하지 않았음.
- **채택**:
  1. **백엔드 order_key.idnum 신설**(표시 전용, 키 불변): `outbound_service.list_orders`
     슬립 그룹에 `MAX(Idnum+0) AS idnum` SELECT(전 서버 기조회 무가드 패턴),
     `get_order_detail` 은 라인 Idnum 대표값(MAX, 컬럼 부재 서버 0 폴백). `OrderKey`
     모델에 `idnum: int | None` 추가. 거래현황 쪽은 `list_sales_statements` 가 이미
     반환 — 파사드 `/transactions/status` 에 `sortBy/sortDir` 패스스루만 추가.
  2. **표기 A(Idnum 5-pad) 통일**: 거래현황 LIST/상세, 출고접수 목록/상세,
     출고현황 슬립/요약, 거래명세서 상세 헤더 — 전부
     `formatIdnumDisplay(order_key.idnum) || jubun`(Idnum 미반환 서버 폴백),
     컬럼 라벨 "전표"→"전표번호".
  3. **거래현황 컬럼 정렬**: 서버 화이트리스트 `_SALES_STATEMENT_SORTS`
     (gdate/idnum/customer_name/gubun/gjisa/row_count/qty/amount/status) 기반
     헤더 클릭 토글(오름↔내림, aria-sort) — list/상세/메모=서버 재조회,
     요약=클라이언트 정렬(정렬 컬럼: 거래처/전표수/수량합/금액합).
  4. **창 닫기 시 목록 검색세션 초기화**: `clearAllListSessions()` 신설 —
     워크스페이스 `closeWindow`/`closeAll` 에서 목록 세션 스냅샷(KEY_PREFIX 전체)
     제거. 닫힌 창을 다시 열면 새 창처럼 시작(사용자 요청). 상세↔목록 왕복(창
     유지) 복원(DEC-055)은 창이 닫히지 않으므로 영향 없음.
  5. **부수 정비**(같은 배치): 신규 거래명세서 라인 그리드 컬럼 헤더 드래그 순서
     변경(`useGridPrefs`, 계정별 서버 저장 — 다른 목록과 동일 UX), 로그인 화면
     DSN-DEC-08 내부 문구 노출 제거.
- **보강(2026-07-17, 사용자 지시)**: 거래현황 정렬 헤더에 **비활성 컬럼 인디케이터
  부재** — 활성 컬럼만 ▲/▼ 표시되어 정렬 가능 여부가 안 보임. 공용 DataGrid 헤더와
  동일 표기(버튼 + 상시 인디케이터: 활성 ▲/▼, 비활성 ↕, text-[10px] opacity-70,
  우측 정렬 flex-row-reverse)로 `sortTh` 교체 — 4개 뷰(list/상세/요약/메모) 공통.
  전수 검색 결과 수제 정렬 헤더는 이 페이지가 유일(나머지 목록은 전부 DataGrid 로
  이미 ↕ 표시) — 신규 수제 정렬 테이블 도입 시 DataGrid 표기 규약을 따를 것.
- **범위 제외**: 거래명세서 라인 "입력순서" 정렬(레거시 auto-increment ID 순)은
  DEC-097 에서 사용자 확정으로 스킵 — 추후 백엔드 ORDER BY 변경으로 별도 대응.
- **검증**: `test_dec099_slip_number_display.py` 신설(list_orders MAX(Idnum+0)
  SELECT+반환, get_order_detail 라인 MAX, status 파사드 sortBy/sortDir 패스스루)
  — 3건 PASS. 프론트 tsc 0, eslint 신규 이슈 0(기존 6건 잔존, stash 비교 동일).
  관련 서브셋(outbound/sales_statement/stats/permission) pre/post 비교 —
  **post-only 실패 0건**(33건 전부 기존 실패), pre-only 3건=신규 테스트.
  정적 감사 4종(routing/hcode/coalesce/login-audit) critical 0.
- **결정자**: 사용자 (2026-07-16 — 고객 리포트 전달)
- **참조**: DEC-064(Idnum 표기 정본·5자리 zero-pad), DEC-055(목록 세션 복원),
  DEC-082(서버 정렬 화이트리스트 패턴), `sales-statement-jubun.ts`
  `formatIdnumDisplay`

### DEC-181: 출고 현황 — 선택분 「이 PC 프린터」 출력 (2026-08-22)

- **요청**: "바로재출고(지정된 자동 출력용) 버튼과 유사하게 **현재 사용자 PC 출력** 가능하도록
  거래 명세서 출력 기능·버튼 추가."
- **배경(무엇이 없었나)**: 기존 「바로출고」/「바로재출고」는 *지정된 자동출력 PC* 의 인쇄 큐로
  보내는 **원격 지시**(`transactionsApi.urgentPrint`, DEC-111 SSE 자가폴 프린터 탭)다.
  지금 앉아 있는 PC 에서 뽑을 수단이 출고 현황에는 **전혀 없었다**.
- **결정**: 선택분을 브라우저 인쇄 대화상자로 출력하는 버튼 추가.
  - 거래 명세서 목록의 단건/일괄 인쇄와 **같은 엔드포인트·같은 양식** —
    `salesStatementPdfUrl` / `salesStatementBatchPdfUrl`, `layout=legacy_triplicate`,
    테두리는 사용자 설정 `sales_statement_print_borders` 를 그대로 따른다(양식지/빈 용지).
  - 2건 이상은 **batch PDF 1개**로 묶어 인쇄 대화상자가 1회만 뜬다.
  - **상태 전이 없음** — 바로재출고와 동일하게 "출력 수단"만 추가. (거래 명세서 목록의
    인쇄는 접수→완료 전이를 하지만, 여기서는 하지 않는다. 필요해지면 별도 결정.)
  - 선택 상태 무관하게 노출(대기/접수/완료 전부) — 재출력 목적이므로.
- **키 주의**: 인쇄 API 키는 `serializeStatementKey`. 화면의 선택키 `slipKey`
  (`gdate|hcode|jubun|gjisa|gcode`) 와 **다른 형식**이라 혼용하면 전표가 어긋난다.
- **회귀 가드**: `test/test_outbound_status_print_on_this_pc.py` 8건 — 버튼/라벨, 선택 1건
  이상 노출, `printPdfFromUrl` 사용·`urgentPrint` 미사용, 단건/일괄 엔드포인트 분기,
  동일 양식·테두리 설정, statement 키 사용, **상태 전이 호출 부재**, 기존 원격 큐 버튼 잔존.
- **보강(2026-08-22 2차, 사용자 흐름 확인 요청)**:
  - 좌측 전표 목록 기본 순서 = 선택 · **전표번호 · 거래일자** · 거래처 · 수량 · 금액 · 접수
    (전표번호를 거래일자 앞으로 — 입고 현황·출고 접수 목록과 동일하게 선두).
  - **"개별 선택 → 상세 → 수정 → 저장 → 출력" 흐름 점검 결과**: 상세 표시·수정·저장은
    이미 정합(행 클릭 → 우측 라인 지연 조회, 「수정」 → `OrderDetailDialog` → `라인 저장`
    → `onChanged` 로 목록·선택 라인 재조회)이었으나, **출력만 끊겨 있었다** —
    상단 「거래 명세서 출력」은 *체크박스*(`checkedKeys`) 기반이라 행을 클릭만 한 전표는
    대상이 아니었다(`selectedKey` 와 `checkedKeys` 는 별개).
    → 우측 상세 액션 줄에 「출력」 버튼 추가, `doPrintOnThisPc(targets?)` 로 명시 대상
    1건을 넘긴다. 이제 한 자리에서 흐름이 끝난다.
- **결정자**: 사용자 (2026-08-22)
- **참조**: DEC-111(자동출력 = 브라우저 탭 드라이버), DEC-179(출고 접수 개별 출력), print-api

### DEC-180: 메뉴 진입점 분리 — `menuRoute` (출고 접수 → 신규 주문 직행) (2026-08-22)

- **요청**: "출고 접수 메뉴를 누르면 목록 말고 **바로 신규 주문 화면**이 뜨도록."
- **함정(왜 `route` 를 바꾸면 안 되나)**: `getFormByRoute` 는 **접두 매칭**이다
  (`path === routePath || path.startsWith(routePath + "/")`, 가장 긴 매치 우선).
  `Sobo27.route` 를 `/outbound/orders/new` 로 바꾸면
  `/outbound/orders`(목록)·`/outbound/orders/{key}`(상세) 가 **어떤 폼에도 매칭되지 않아
  권한 caps 매핑에서 빠진다.**
- **결정**: `FormMeta.menuRoute?: string` 신설 — `route` 는 화면의 대표 경로(접두 매칭 기준)로
  두고, **메뉴 클릭 시 열 라우트만** 덮어쓴다. 사이드바는 `openRouteOf(form) = menuRoute || route`
  로 **열기와 활성 표시 두 곳 모두** 같은 값을 쓴다(한쪽만 바꾸면 메뉴 하이라이트가 죽는다).
  Sobo27 에 `menuRoute: "/outbound/orders/new"` 부여. 목록은 신규 화면의 「목록」 버튼으로 유지.
- **총판 회귀 차단**: `/outbound/orders` 는 총판이면 `DistributorOutboundBoard`, 그 외는 목록을
  렌더한다. 메뉴가 `/outbound/orders/new` 를 직접 열게 되면서 **총판도 이 경로로 들어오므로**
  신규 화면에도 같은 분기를 뒀다 — 총판 화면은 진입 경로와 무관하게 동일.
- **회귀 가드**: `test/test_outbound_menu_opens_new_order.py` 9건 — `menuRoute` 필드 선언,
  Sobo27 의 route/menuRoute 값, **접두 매칭 미러**(목록·상세가 여전히 해석되는지 + route 를
  `/new` 로 바꿨다면 빠진다는 반증), `getFormByRoute` 가 접두 매칭이라는 전제 검증,
  사이드바가 열기·활성 두 곳에서 같은 resolver 를 쓰는지, 총판 분기 2페이지, 목록 복귀 링크.
- **결정자**: 사용자 (2026-08-22)
- **참조**: DEC-179(출고 접수 성격·컬럼), `form-registry.getFormByRoute`

### DEC-179: 화면 표기 띄어쓰기 규칙 + 출고 접수 목록 컬럼·개별 출력 (2026-08-22)

- **표기 규칙(확정)**: 「<도메인><기능>」 합성어는 **띄어 쓰고 「관리」 접미는 뗀다.**
  - 적용 완료: 입고접수관리→`입고 접수`, 입고현황→`입고 현황`, 출고접수관리→`출고 접수`,
    출고현황→`출고 현황`, 거래명세서→`거래 명세서`, 거래현황→`거래 현황`(LIST/상세/요약/메모
    변형 및 사이드바 서브그룹 라벨 포함).
  - 코드 **주석**의 옛 표기는 추적성 유지를 위해 그대로 둔다(사용자 노출 문자열만 변경).
  - **미적용(남은 후보)**: 입고명세서·반품명세서·기타명세서·제작명세서·출고내역서·
    일별/기간별반품내역서·재고현황·미수현황·입금현황·제작현황·발송비현황·내역서관리.
    일괄 적용 여부는 사용자 확인 후.
  - 캡션 감사 영향: 단일 map 폼은 legacy DFM 캡션과 어긋나므로
    `coverage-allowlist.yaml` `caption_mismatches` 에 사유와 함께 등재한다
    (Sobo27, Sobo67_status). MULTI_MAP 폼(Sobo22/Sobo25/Sobo21 계열)은 감사 무영향.
- **출고 접수(`/outbound/orders`) 성격 확인**: 신규 출고 **거래 명세서 입력** 화면이 맞다
  (신규 → `/outbound/orders/new`, 저장 후 목록·상세).
- **목록 기본 컬럼**: 전표번호 · 거래일자 · 거래처 · 라인 · 수량 · 금액 · 상태.
  (종전 일자·거래처·전표번호 순, 「수량합/금액합」 라벨 → 「수량/금액」.)
- **개별 바로 출력(신규)**: 종전에는 목록에서 인쇄가 **불가**했고 상세로 들어가 「거래 명세서
  PDF」를 **다운로드**해야 했다. 목록 행에 인쇄 버튼을 추가 —
  상세와 **같은 엔드포인트**(`outboundStatementPdfUrl`)를 쓰되 다운로드가 아니라
  `printPdfFromUrl`(거래 명세서 목록의 단건 인쇄와 동일 헬퍼)로 인쇄 창을 띄운다.
  키는 `serializeOrderKey(order_key)` 그대로라 전표 식별이 어긋나지 않는다
  (거래명세서 목록은 `serializeStatementKey`(gjisa 축)라 키 형태가 다르다 — 혼용 금지).
  행별 `printingKeys` 로 누른 행만 비활성화하고, 실패는 「인쇄 실패」 배너로 노출.
- **미반영**: 거래 명세서 목록의 **일괄 인쇄**(선택 N건 batch.pdf)·양식지 테두리 토글·
  X-Printed-Keys 완료 처리는 출고 접수에 이식하지 않았다 — 필요 시 별도 작업.
- **결정자**: 사용자 (2026-08-22)
- **참조**: DEC-099/108(전표번호=Idnum), DEC-054(캡션 감사 allowlist), print-api

### DEC-178: 콤보(픽 필드) 키 규약 — Enter=목록, 방향키=입력 컨트롤 이동 (2026-08-22)

- **보고**: 사용자(스크린샷 — 신규 출고 주문 라인의 「구분」 콤보) — "콤보 입력은 Enter 를
  치면 목록이 나와서 선택하게 하고, 그렇지 않으면 상하좌우 키가 입력 컨트롤 이동이 되도록
  **모든 화면에서** 수정 필요."
- **원인**: `LocalComboField` 닫힘 상태 핸들러가 `Enter || ArrowDown` 을 **둘 다 "팝업 열기"**
  로 처리하고 `stopPropagation()` 까지 했다(DEC-119 규약). 그래서 라인 그리드에서 ↓ 로 다음
  행에 가려 하면 표의 `handleGridArrowKey` 가 이벤트를 **아예 보지 못하고** 콤보 목록이
  펼쳐졌다.
- **결정(DEC-119 의 "닫힘 ↓=열기" 철회)**:
  1. 닫힘 상태에서 목록을 여는 키는 **Enter(및 클릭) 뿐**.
  2. 닫힘 상태 ↑↓←→ — 표 안(`closest("td")`)이면 `preventDefault`/`stopPropagation` 없이
     **버블링만** 시켜 `grid-arrow-nav` 의 열 기준 셀 이동에 양보. 표 밖(검색 필터 바·상세
     폼)이면 신설 `focus-advance.moveFocusBy(el, ±1)` 로 이전/다음 컨트롤 이동.
  3. `moveFocusBy` 의 이동 대상 셀렉터에는 **픽 필드**(readOnly + `role="combobox"`)를 포함
     — 그렇지 않으면 콤보로 되돌아올 수 없다(`grid-arrow-nav.isNavTarget` 과 같은 기준).
  4. 네이티브 `<select>` 도 동일 규약 — `grid-arrow-nav` 가 이동할 행이 없는 첫/마지막 행에서
     `HTMLSelectElement` 의 기본 동작(항목 변경)을 막는다(number 스피너와 같은 처리).
- **적용 범위**: `LocalComboField` 는 **16개 화면이 공유**하므로 이 한 곳 수정으로 전 화면에
  적용된다(신규 출고 주문 라인 그리드 포함).
- **회귀 가드**: `test/test_combo_arrow_moves_not_opens.py` 7건 — 닫힘 상태 Enter만 열기,
  표 안 양보, 표 밖 `moveFocusBy`, 방향키 분기 `stopPropagation` 금지, 픽 필드가 이동 대상에
  포함, 사용처 breadth. jsdom 8항목(닫힌 콤보 ↓ 가 목록을 열지 않고 다음 행 콤보로 이동,
  ←/→ 행 내 이동, 수량↔콤보 왕복, Enter 는 그리드로 전파 안 됨). ↓=열기로 되돌리면 실제로
  실패하는 것(red)까지 확인.
- **부수**: 표기 「출고접수관리」 → **「출고 접수」**(입고 접수/입고 현황과 동일 규칙).
  단일 map 폼이라 legacy-coverage 캡션 감사에 걸려 `coverage-allowlist.yaml`
  `caption_mismatches` 에 사유·기한과 함께 등재(Sobo22/Sobo25 는 MULTI_MAP 이라 무영향).
- **결정자**: 사용자 (2026-08-22)
- **참조**: DEC-119(픽 필드 도입), DEC-168(그리드 방향키), DEC-054(캡션 감사 allowlist)

### DEC-177: 출고현황 상세 — 응답 모델이 ISBN 을 잘라내던 결함 + 좌측 전표 목록 기본 컬럼 (2026-08-22)

- **보고**: 사용자 — "출고현황 상세 우측 목록에 ISBN 값이 나타나지 않는다" + 좌측 목록
  기본 필드 순서 지정(선택·거래일자·전표번호·거래처·수량·금액·접수).
- **원인(ISBN)**: `outbound_service.get_order_detail` 은 `product_name` 과 **같은 G4_Book
  lookup**(`IFNULL(Gisbn,'') AS gisbn`)에서 `gisbn` 을 이미 채워 반환하고 있었다. 그런데
  라우터가 `response_model=OrderDetailResponse` 로 검증하는데 `OrderLineDetail` 모델에
  `gisbn` 필드가 없어 **Pydantic 이 응답에서 조용히 잘라냈다**(FastAPI response_model 은
  모델에 없는 키를 버린다). 목록(view=list)은 다른 엔드포인트(`OutboundStatusLineItem`,
  inquiry 모델)를 써서 정상이었기 때문에 "목록엔 나오는데 상세엔 안 나오는" 형태였다.
  → DEC-169 대상 목록 B15(출고현황 라인 목록 **+ 상세**) 중 상세 쪽 누락 해소.
- **교훈(재발 방지)**: 서비스가 값을 채워도 **응답 모델에 필드가 없으면 화면에 안 나온다.**
  DEC-169 계열로 컬럼을 추가할 때는 (서비스 SELECT/채움) → (**응답 모델 필드**) →
  (프론트 타입/렌더) 3계층을 모두 확인해야 한다.
- **좌측 전표 목록 기본 컬럼**: 선택 → 거래일자 → 전표번호 → 거래처 → 수량 → 금액 → 접수.
  「선택」은 체크박스 열(`requestSelectCol`)이라 prefs reorder 밖에서 항상 맨 앞.
  `qty`/`amount` 는 요약 뷰에만 있던 것을 상세 뷰에도 노출(같은 `OutboundStatusSlipItem`).
  「거래처명」 라벨은 「거래처」로. 「항목수」(DEC-162)는 요청 목록에 없어 **뒤로 밀되 유지**
  — 컬럼 설정에서 숨기거나 앞으로 옮길 수 있다.
- **회귀 가드**: `test/test_outbound_detail_gisbn_response_model.py` 6건 — 모델 필드 존재,
  서비스 dict → 모델 → dump 왕복에서 `gisbn` 생존(도서명과 함께), 구서버(키 부재) 시 빈 문자열
  폴백, 우측 표 렌더, 좌측 기본 컬럼 순서, 선택 열 선두 고정.
  모델에서 `gisbn` 을 빼면 3건이 실제로 실패하는 것(red)까지 확인.
- **결정자**: 사용자 (2026-08-22)
- **참조**: DEC-169(도서 메타 공통 컬럼 · 대상 B15), DEC-162(항목수), DEC-099/108(전표번호)

### DEC-176: 검색 팝업 자동 선택 제거 — 무심코 친 Enter 가 1번째 결과를 입력하던 오입력 (2026-08-22)

- **보고**: 사용자 — "검색 팝업이 뜰 때 사용자가 명시적으로 선택하지 않았는데 첫 항목이 자동
  선택돼 있어, 무의식적으로 Enter 를 치면 무조건 1번째 검색 항목이 입력된다."
- **원인**: `master-lookup-dialog.tsx` 가 검색 직후 `initIdx = exactIdx >= 0 ? exactIdx : 0`
  으로 **항상 첫 행을 강조**했고, 검색창에서 같은 키워드로 Enter 를 다시 치면
  (`term === lastTermRef.current && selectedRow`) 그 강조 행을 확정했다. 즉 "검색하려고 친
  Enter" 가 "1번째 결과 확정" 이 됐다.
- **결정**: 자동 강조는 **정확 코드 일치 행에만** 남긴다.
  - 유지: 전체 코드를 입력한 경우의 Enter 1회 확정(DEC-134) — 사용자 표현의
    "값을 입력해서 항목 선택" 에 해당하는 명시적 행동.
  - 제거: 그 외 미일치 시 `setSelectedKey("")` — 어떤 행도 강조하지 않는다.
  - 선택은 **↓ / 클릭 / 정확 코드 입력** 같은 명시적 행동에서만 생긴다. `↓` 가 첫 행을
    선택하고 그리드로 진입하는 흐름은 그대로.
- **점검 결과(무변경)**: 인라인 자동완성(`master-lookup-field` `activeIdx=-1`), 거래명세서
  검색 팝업(`selectedIdx=-1`), 공용 `DataGrid`(`selectedRowKey` 비면 -1) 는 원래부터
  미선택 시작이라 손대지 않았다 — 회귀 가드로만 고정.
- **회귀 가드**: `test/test_lookup_dialog_no_auto_select.py` 7건.
- **결정자**: 사용자 (2026-08-22)
- **참조**: DEC-134(Enter 자동확정 조건), DEC-097(팝업 폴백)

### DEC-175: 입고 상세/수정/취소 SQL 행 스코프(`Scode='Y'`) 누락 — 전표번호 오표시·출고 전표 오염 (2026-08-22)

- **보고**: 사용자 — "입고 접수 상세 화면의 전표 번호 이상하여 확인 필요".
- **근본 원인(백엔드)**: 입고 상세/수정/취소 SQL 이 헤더키
  `(Gdate, Hcode, Gcode, Jubun)` 만 조건으로 썼다. 이 좌표는 **거래처 간 공유 키**라
  (DEC-080 SLIP_KEY_AMBIGUOUS) 같은 키에 출고(`Scode='X'`) 행이 함께 존재할 수 있다.
  목록은 `Scode='Y'` 로 입고만 집계하는데 상세 계열은 이 조건이 없어서:
  1. 상세 `MAX(Idnum+0)` 가 **출고 전표의 Idnum** 을 집어 목록과 다른 전표번호 표시,
  2. 상세 라인에 출고 라인이 섞이고,
  3. **소프트 취소(`Yesno='2'`)·라인 UPDATE/DELETE 가 출고 전표를 함께 건드릴 수** 있었다
     (데이터 훼손 위험 — 실제 사고 보고는 없으나 경로가 열려 있었다).
- **수정**: `_SQL_INBOUND_ROW_WHERE = 헤더키 + " AND Scode='Y'"` 신설, `S1_Ssub` 를 건드리는
  6개 SQL(상세 라인 / MAX(Idnum) / 취소 전 Yesno 조회 / 취소 UPDATE / 라인 UPDATE·DELETE)
  전부 교체. **`S1_Memo` 는 Scode 컬럼이 없어 헤더키 그대로** 둔다(붙이면 1054).
  `Gubun` 은 넣지 않는다 — 입고현황은 반품입고 전표도 함께 보여준다(DEC-174).
  목록에 보이는 행은 정의상 `Scode='Y'` 이므로 이 조건은 결과를 좁히기만 한다.
- **증상 증폭(프론트)**: 상세가 `formatIdnumDisplay(idnum) || receipt_key.jubun` 으로
  폴백해 Idnum 이 0 이면 12자리 **Jubun(거래처별 차수)** 을 전표번호 자리에 노출했다.
  이는 **DEC-108 이 감사 대상으로 남긴 "`inbound/receipts/[receiptKey]:271`
  (입고 체계 확인 요)" 미해결 항목**이다. 레거시 정본 Sobo22 는
  `Edit109 = Format('%05s', Idnum)` 이므로 Idnum 이 정본 — 없으면 목록과 동일하게 `—`.
  신규 화면 저장 배너의 `savedKey.jubun` 노출도 같은 결함이라 서버 채번 `idnum` 으로 교체.
  → **DEC-108 감사 항목 중 입고 건 종결.**
- **회귀 가드**: `test/test_inbound_detail_slip_number_scope.py` 7건
  (S1_Ssub 6종 SQL 의 Scode 스코프 / S1_Memo 는 Scode 금지 / 상세 Idnum·라인 조회 스코프 /
  취소가 출고 행 미접촉 / 프론트 Jubun 폴백 제거).
- **결정자**: 사용자 리포트 (2026-08-22)
- **참조**: DEC-080(공유키 fail-closed), DEC-099/108(전표번호=Idnum), DEC-174

### DEC-174: 입고현황 교문사 정합 — 입고처명 정본 G2_Ggwo·요약 hcode 격리·Gubun 무필터 + 입고접수 6컬럼 (2026-08-22)

- **보고**: 사용자 — "교문사 계정에서 조회되는 입고처 데이터가 기존 프로그램 입고현황 화면과 다르다"
  (레거시 스크린샷: 2026.07.01~08.22, 중원아트(랩핑)·태성제책사·(주)디북 등 13행 / 상세 2행 합계 1,792).
- **정본**: `WeLove_FTP/도서유통-New/도서유통/한국도서유통/출판/MySQL/도서유통/chul_09(위러브)/Subu25_2.pas`
  (교문사 = chul_09 공유 DB, `BLD-PUB-WAREHOUSE-WELOVE` 빌드). `Button101Click` L396~L427.
- **원인 4건 / 수정**:
  1. **요약 뷰 hcode 미전달(보안)** — `/transactions/inbound-status?view=summary` facade 가
     `period_report(hcode=...)` 를 넘기지 않아 `chul_09_db` 공유 4테넌트(교문사·위러브1·2·3)
     입고가 합산됐다. `_effective_hcode` 전달로 격리(OQ-TENDIR-1 계열, DEC-136 fail-closed 동형).
  2. **입고처명 테이블 오선택** — `inbound_service._fetch_vendor_names` 가 거래처 마스터
     `G1_Ggeo` 를 무스코프 조회. 입고처 마스터 정본은 **`G2_Ggwo`** 이고, 레거시는 행별
     `G2_Ggwo.Locate('Hcode;Gcode', [로그인hcode, Gcode])` → 실패 시 `Hcode=''` 폴백(L455~L475).
     → `Hcode IN (<scope>, '')` 청크 lookup + **정확 일치 행 우선** 병합으로 재현.
     입고처 자동완성(`/masters/inbound-vendors-search`) 도 동일 스코프 적용.
  3. **`Gubun='입고'` 하드필터** — 레거시 입고현황 고정 조건은 `Scode='Y'` + `Gcode<>''` 뿐이고
     Gubun(입고/반품)은 검색 콤보(Edit103)다. `list_receipts(gubun=None, require_vendor=True)`
     로 입고현황 facade 만 무필터 전환(입고접수/입고명세서는 `Gubun='입고'` 기본 유지).
  4. **`Yesno='2'` 전표 기본 제외** — 프론트 `includeCancelled` 기본 false → `HAVING MAX(Yesno)<>'2'`.
     레거시 입고현황은 Yesno 를 **전혀 필터하지 않는다**. 입고현황(조회 전용) 만 기본 true·라벨
     "완료·취소 포함" 으로 전환. 입고접수(Sobo22, CRUD)의 기본 false 는 **무변경** — 웹 소프트취소
     전표는 계속 숨긴다.
     - ⚠ **`Yesno='2'` 는 이중 의미다(알려진 위험).** 레거시 기록에서는 **완료/확정**
       (`_line_status_from_yesno_max` — Subu21.pas L1395/L1444 삭제 잠금 조건 `Yesno<>'1' and <>'2'`,
       레거시의 취소는 행 DELETE), 모던 웹에서는 **소프트취소** 마커(`SQL_CANCEL_RECEIPT`, DEC-012).
       같은 컬럼 값이라 **행만 보고는 구분 불가** — 이것이 "레거시엔 보이는데 웹엔 없다" 의 직접 원인이다.
       구분이 필요해지면 별도 취소 마커(Time3/Time4 또는 전용 컬럼) 도입이 선행돼야 한다.
- **부수 정합(회귀 차단)**: `_fetch_vendor_names` 는 원장(`customer_ledger_service._fetch_customer_names`)
  과 공유 중이었다. 원장 축의 `Gcode` 는 **거래처(G1_Ggeo)** 라(DEC-137) 테이블이 다르므로,
  원장 폴백을 G1_Ggeo 인라인 조회로 되돌리고 공유 import 를 끊었다. **두 도메인의 `Gcode` 동음이의
  (입고=입고처/원장=거래처)가 공용 헬퍼로 묶이면 안 된다.**
- **입고접수 화면(운영 요청 동시 반영)**: 메뉴/제목 표기 `입고접수관리` → **`입고접수`**,
  목록 컬럼 = **전표번호·거래일자·입고처·라인·수량·금액** 6종 고정(출판사·상태 제외 —
  출판사 필터는 이미 UI 제거됨, 접수 잠금은 상세에서 확인). 전표번호는 공용
  `formatIdnumDisplay`(5-pad, DEC-099/108) 로 통일. Sobo22 는 MULTI_MAP 이라 캡션 매트릭스 무영향.
- **회귀 가드**: `test/test_inbound_status_gyomunsa_parity.py` 10건 신규(요약 hcode 전달 / facade
  레거시 스코프 / WHERE 조립·파라미터 순서 / G2_Ggwo+Hcode 폴백·정확일치 우선 / 자동완성 스코프 /
  프론트 기본값). `test_inbound_ocode_detail_robust.py` 의 `Gubun='입고'` 리터럴 단언은
  바인딩 파라미터 형태로 갱신(의도 보존). 전체 `test/` **2141 passed / 0 failed / 48 skipped**, tsc 0.
- **미해결**: 레거시 화면의 본사/창고 토글(Edit107 → `Ocode A/B`) 은 여전히 미노출(현행 NULL/A/B 전부 허용).
  교문사 실데이터 대조는 라이브 DB 스모크(`RUN_DB_SMOKE`) 로 별도 확인 필요.
- **결정자**: 사용자 (2026-08-22 리포트 + 입고접수 컬럼 지정)
- **참조**: DEC-136(공유좌표 hcode 격리), DEC-137(원장 도메인 축), DEC-172(G2_Ggwo 컬럼 의미),
  DEC-099/108(Idnum 표기), `analysis/layout_mappings/Sobo25_inbound_status.md`

### DEC-173: 허브 회귀 스위트 부채 청산 — 128 실패 → 0 (2026-08-19)

- **배경**: 전체 스위트가 126~128건 기존 실패를 안고 있어 CI 신호가 죽어 있었음(DEC-169 검증 시 "격리 재실행"으로 우회).
- **원인 3계층**: ① 21개 파일이 모듈 import 시 `app.dependency_overrides` 인증 오버라이드를 설치 → 먼저 실행된
  테스트의 pop/clear 로 401(순서 의존) → 각 `setUp` 에서 재설치(기존 `test_c4_returns_phase2` 패턴). ② 서비스
  `execute_query` 만 패치하고 어댑터(`t5_ssub/s1_ssub/h2_gbun/g1_ggeo/g4_book_adapt`) 는 실 DB 로 나가던 9건
  (라이브 SSH/MySQL 접속!) → 어댑터 모킹, `test_sales_statement_jubun_primary_search` 의 라이브 remote_153 질의는
  모킹 테스트로 전환. ③ `sys.modules`/monkeypatch 누수(`h2_gbun_column_meta` 미복원, `app` 패키지 pop, 허브
  프로토타입 `backend/` 의 `test_nav_api` 가 제품 app 로드) → finally 복원/격리.
- **낡은 가드 갱신(결정 인용)**: Sobo39 숨김(DEC-155/124), 특별관리 legacy-id(DEC-155/170/171), 출고현황
  ORDER BY idnum(DEC-099/108/118), 필터 픽필드 `LocalComboField`(DEC-119), 도서별수불원장 재작성(DEC-164),
  인쇄 base 레이아웃 재사용·DEC-158, admin inspect(DEC-056), 로그인 org-select(DEC-096), 등. `test_screen_caps_static`
  는 `distributorOnly+menuId:null` 블록만 면제(판단 — 대안은 registry 에 requiredPermission 부여).
  `test_dfm2html_adapter`/`test_res_string_bridge` 는 외부 프로젝트 부재 시 skip.
- **정적 감사 3종**: `delphi_form_screen_matrix.py` 에 보조 DFM 루트(출판 MySQL/New) — 레지스트리가 참조하는 스템만
  보충(고아 집계 불변 41), `coverage-allowlist.yaml` 캡션 불일치 20건 사유·기한 등재(서브폼/별칭·빌드 변형·웹 캡션
  정책), `list-state-allowlist.yaml` 7화면 deferred(후속 일괄 도입, 2026-09).
- **결과**: 2131 passed / 0 failed / 48 skipped, 순서 무관(정·역·셔플 동일), 라이브 DB 접속 0.
- **결정자**: 사용자 (2026-08-19 "1,2,3,7 순서로 진행")
- **참조**: `test/` 63파일, `tools/delphi_form_screen_matrix.py`, 두 allowlist

### DEC-172: 입고처관리 = 거래처관리 동형 + 기타거래처 상세폼 정본 라벨 (2026-08-19)

- **보고**: 영업팀 기초관리 요청서(260813) "[입고처 관리] 거래처관리와 동일하게 작업 요청" + DEC-149 잔여(기타거래처·
  입고처 상세폼 `gpper` 를 "한도액" 숫자로 취급 → 담당자 텍스트 소실 위험).
- **정본(레거시 New/출판 빌드 Subu12/Subu15 + DB 스키마 G1/G2/G5 동일)**: Edit110 '담 당 자'→Gpper(TEXT),
  한도액→Gssum, 핸드폰→Gphon, 한도(율)→Grat7, 비고2→Name1, 계산서 거래처명→Name2, 정지사유→Email,
  발행유무→Yesno, 정지유무→Grat9; Sobo15 는 계산서구분→Pubun(Edit128). `gjomo1` 은 실컬럼 아님(제거).
- **구현(제품 259a2d3)**: g2_ggwo/g5_ggeo 어댑터 타입 정정, 입고처 목록=세부내역 전면(요청 순서, G2_Gbun 1회 조회
  맵), 필드 카탈로그/선택 export(33열)+역반영, 상세폼 정본 라벨(입고처·기타거래처), 프로브 매트릭스 등록.
- **참고(라이브)**: 교문사 5019 입고처 82행, `80014 센게이지러닝코리아` 담당자 '박현수' — 구 매핑이면 0 으로 소실됐을 값.
  잔여: `list_etc_customers` G5_Gbun LEFT JOIN 행 증식(04641 3배, 숨김 화면) · `get_inbound_vendor` gbun_name 스칼라
  서브쿼리(3.23 미지원) — 후속.
- **결정자**: 사용자/영업팀 (2026-08-19)
- **참조**: [[DEC-149]], `docs/masters-request-260813-reconciliation.md`

### DEC-171: 특별관리 계정(빌드)별 비율 프로필 — 총판 비율 1개 / 출판 판매유형별 Grat1~6 (2026-08-18)

- **보고**: 사용자 — "총판 계정과 (수정요청을 반영하는) 교문사 독립 출판사 계정들 별로 계정별 적용이
  가능하면 그렇게 수정" (DEC-170 분석의 A안을 계정 변형으로 채택).
- **결정**: 코드 분기 없이 **계약 데이터**로 분기 — `migration/contracts/special_master.yaml` v1.3.0
  `rate_profiles`(single: 총판 빌드 원형 Grat1+단가 / by_pubun: 출판·자체물류 빌드 Grat1~6+단가) +
  `customer_variants`(match `build_role` ∈ {publisher, warehouse_publisher} → by_pubun, 그 외 기본 single).
  런타임은 허브 정본 → 백엔드 번들 사본(`backend/data/contracts/special_master.yaml`) 순(DEC-069 패턴,
  동기화 가드 테스트).
- **적용 규칙(by_pubun)**: `Tong20.PrinRat1` 동등 — 위탁·신간·반품→Grat1, 현매→Grat2, 매절→Grat3, 납품→Grat4,
  특별→Grat5, 한도→Grat6, 증정→0, 단가=Gssum. 명시 이탈 2건: ① '기타'는 레거시 분기 부재(Grat1 잔존) 대신
  그리드 라벨(기타=Grat6)대로 Grat6, ② 판매유형 컬럼이 0(미입력)이면 **Grat1 폴백** — 웹 기존 특가 행은
  Grat1 만 채워져 있어 현매 전표가 0% 로 계산되는 사고 방지(레거시는 0 그대로).
- **구현(제품 323733e)**: `services/special_rate_profile.py`(프로필 해석·pubun→컬럼), `services/g6_ggeo_adapt.py`
  (SHOW COLUMNS 캐시로 Grat2~9 드리프트 대응, IFNULL), 목록 응답 `rate_profile`+행 `grat2~6`, POST/PATCH
  grat2~6, line-defaults 라우터가 로그인 컨텍스트로 프로필 해석 후 `resolve_line_defaults(special_profile=)`.
  화면은 프로필 컬럼에서 그리드/편집/신규 입력 파생(총판 계정 = 기존 "비율" 1칸 그대로), 거래처 기본 공급율
  컬럼별 자동 채움. 출고접수(`resolveSpecial`)는 같은 line-defaults 경로라 자동 반영.
- **검증**: `test_dec171_special_rate_profile.py` 9 PASS(프로필 해석·pubun 매핑·번들 동기·드리프트 조각·
  create/update 컬럼·by_pubun/single/0-폴백) + 인접 30 PASS, tsc 0, hcode 감사 신규 0, 라이브(remote_153,
  G6 Grat1~9 존재 확인) create(grat2/4)→patch(grat3)→delete 라운드트립 정상(잔여 0), line-defaults 실측
  위탁 75 / 현매(미입력)→폴백 75 / 증정 0 / 총판 프로필 현매 75, 화면 6컬럼(위탁~기타)+단가 렌더.
- **잔여**: 거래처별 기본행(Bcode='') 모드·신간 배본 폴백(Seek07)은 신간발행 이식과 묶어 별도(DEC-170 D3),
  `analysis/layout_mappings/Sobo16.md` 총판 기준 서술 갱신 필요.
- **결정자**: 사용자 (2026-08-18)
- **참조**: [[DEC-170]], [[DEC-155]], [[DEC-069]](번들 사본), `docs/special-mgmt-legacy-vs-web-2026-08-18.md`

### DEC-170: 특별관리 — 행 선택 후 신규 등록 유지 + 정가/기본비율 자동 채움 + 레거시 절차 재검토 (2026-08-18)

- **보고**: 영업팀 스크린샷 4건 — ① 기존 도서 클릭 시 추가 방법 소실 ② 신규 도서 추가 시 비율/단가 수기
  ("정가 자동 계산 안 됨") ③ 도서기준 패널 용도 불명(빈 결과 문구 혼동) ④ 신규 거래처 등록 불필요.
  사용자: "레거시 처리절차 재검토 후 현행과 차이 확인" + "검증해서 수정안".
- **검증**: `page.tsx` 하단 블록이 `selected ? 편집 : 신규` 삼항이라 행 클릭 순간 신규 등록 UI 가 사라짐(재현).
  레거시(New/출판 빌드 `Subu16`) 는 그리드 마지막 칸 Enter → Append, 코드 Enter → Seek40 → 도서명+**단가=정가**
  자동. 3411 은 G6 특가 거래처 0건 → 도서기준 0건은 정상이나 문구가 "도서를 선택하면…" 공용이라 오인.
- **구현(제품 5ded482)**: 편집 블록(선택 시, `선택 해제`/Esc)과 신규 등록 블록(거래처축 항상 표시) 분리,
  등록 후 신규 코드 입력 포커스 복귀, 신규 도서 확정 시 단가=도서 정가·비율=거래처 기본 위탁율(G1 Grat1,
  customerDetail) 자동 채움(수정 가능), 도서축 신규 거래처는 접힘 기본('이 도서에 특가 거래처 추가'),
  0건 문구 "○○에 등록된 특가 도서/거래처가 없습니다 — 신규 등록에서 추가" + 패널 부제(용도).
- **레거시 대비 잔여 차이(분석 문서 `docs/special-mgmt-legacy-vs-web-2026-08-18.md`)**: 웹은 총판 빌드 기준
  **비율 1개(Grat1)+단가**만 다루나 교문사 빌드(New/출판)는 판매유형별 **Grat1~6(+7~9 저장)** 을 등록·표시하고
  출고(`Subu21`+`Tong20.PrinRat1`)에서 pubun 별 컬럼(현매→Grat2 … 한도→Grat6, 증정→0)+단가=Gssum 을 적용,
  거래처별 기본행(Bcode='') 모드·신간 배본 폴백(Seek07)도 있음 → **A안(판매유형별 컬럼 복원+적용) 권장, 결정 대기**.
- **검증**: tsc 0, eslint 신규 오류 0(기존 useEffect setState 1건), 로컬 Chrome — 00001 조회 → 3392 클릭 시
  편집+신규 블록 동시, 3411 확정 시 단가 30,000 자동, 도서축 접힘 버튼 표시.
- **결정자**: 사용자/영업팀 (2026-08-18)
- **참조**: [[DEC-155]], [[DEC-065]](G6 적용 산식), `analysis/layout_mappings/Sobo16.md`(총판 기준 — 갱신 필요)

### DEC-169: 도서명 목록 전 화면 정가·ISBN 공통 컬럼 + 거래처원장 상세 합계 (2026-08-18)

- **보고**: "도서명이 목록에 포함되는 리스트에 도서가격·ISBN 이 없으면 모두 공통 추가" →
  대상 조사(`docs/book-list-price-isbn-targets-2026-08-18.md`, A 정가·ISBN 둘 다 12 / B ISBN 만 20)
  → 사용자 결정 "정가는 전표 단가로 충분, 숨김 화면 제외, 기본 표시로 A/B 전부 진행".
  같은 요청에서 거래처원장(Sobo32_ledger) 하단 상세 합계행(수량/출고금액/반품금액) 추가.
- **원칙**: ① ISBN 정본 = G4_Book.Gisbn, 정가 = 전표 단가(GDANG=전표 시점 정가, DEC-065)이며
  단가 컬럼이 없는 화면(재고현황·년말집계·회전율·반품후보·재고원장 등)만 마스터 정가(G4_Book.Gdang)
  로 채움. ② **목록 SQL JOIN 금지** — 행 완성 후 bcode 집합으로 공통 헬퍼
  `services/book_meta_lookup.py`(`fetch_book_meta`/`attach_book_meta`/`attach_book_meta_by_row_hcode`)
  청크 lookup(DEC-033 in_clause_lookup), Hcode 일치 → Hcode='' 공용 폴백(Subu24 2단계 동등),
  Gdang/Gisbn 컬럼 드리프트는 `g4_book_adapt` 메타로 SQL 조각만 분기, IFNULL, fail-soft(실패 시
  gisbn='' 로 표시만 비움). ③ 프론트는 도서명 바로 뒤 ISBN(font-mono) → 정가 순, 기본 표시,
  useGridPrefs 로 계정별 숨김 가능. 서버 정렬 화이트리스트에는 미추가.
- **제외(숨김 화면)**: 도서수불장·통합 도서수불장(DEC-137 숨김), 도서코드(Sobo38), 배본처관리.
- **구현(제품 3bb3f59)**: 백엔드 12 서비스 + 4 모델 + 3 라우터(XLSX 카탈로그), 프론트 29 페이지 +
  5 공유 컴포넌트(신규 명세서·입고·반품 입력 그리드는 읽기전용 ISBN 셀 — Enter/화살표 흐름 불변,
  DEC-104/156/168). 출고검증(A11)은 도서코드만 있던 컬럼을 도서명(코드)+ISBN+단가로 보강.
  거래처원장 slip-detail 은 관리자 무-hcode 조회 시 공용 마스터만 조회돼 ISBN 공란 가능(테넌트
  로그인은 정상 — 후속 시 행별 hcode 그룹 lookup 으로 보강 가능).
- **검증**: tsc 0 · eslint 신규 오류 0(기존 2건: special useEffect setState, [orderKey] hooks 순서)
  · 신규 가드 `test_book_meta_lookup.py` + `test_dec169_book_meta_group1~4.py` 17 PASS ·
  전체 스위트 126 실패는 기존/순서의존(격리 재실행 시 관련 파일 전부 PASS, outbound_status ORDER BY
  ·special legacy_alignment 은 DEC-099/155 이후 기존 실패) · hcode 감사 critical 신규 0 ·
  라이브(remote_153/5019) 재고현황·도서별판매·년말집계·반품후보·입고일별·명세서상세·특별관리
  gisbn 실값, 거래처원장 상세 합계 3/73,525/0/306,985.
- **결정자**: 사용자 (2026-08-18)
- **참조**: [[DEC-148]](도서 목록 컬럼), [[DEC-065]](단가=정가 산식), [[DEC-033]], `book_meta_lookup.py`

### DEC-168: 라인 그리드 공통 ↑/↓/←/→ 셀 이동 — 신규 출고 주문·입고·반품 라인표 (2026-08-18)

- **보고**: 신규 출고 주문(`/outbound/orders/new`, `order-line-grid`) 스크린샷 — "키보드 상하좌우로
  입력창 이동을 수정했던 것 같은데 원복됐으면 다시". **확인 결과 원복이 아님**: 화살표 셀 이동은
  DEC-156(2026-08-13)에서 **신규 거래명세서**(`sales-statement/new`) 그리드에만 구현됐고, 출고 주문
  라인표·입고 라인표·반품 라인표에는 애초에 없었다(git -S 이력 0건). 수량 ↑/↓=±1(`handleQtyArrowKey`)만 있었음.
- **구현(제품)**: 공통 헬퍼 `lib/grid-arrow-nav.ts` `handleGridArrowKey` — `<tbody onKeyDown>` 1곳 부착,
  DOM(tr/td)만으로 동작해 컬럼 순서·숨김(useGridPrefs)과 무관.
  ①↑/↓ = 같은 열(td index) 이웃 행 입력(입력 없는 열이면 다음 행 계속 탐색) ②←/→ = 같은 행 이웃 입력,
  DEC-156 규약대로 **캐럿이 값 처음/끝일 때만**(전체 선택·빈값·number 입력은 항상 이동)
  ③이미 소비된 이벤트(`defaultPrevented`: 자동완성 목록 ↑↓, 수량 ±1, 구분 픽필드 ↓=팝업 열기)와
  IME 조합 중은 불간섭 ④픽 필드(readOnly+role=combobox)도 이동 대상. 부착: `order-line-grid`,
  `inbound-line-grid`, `return-line-grid`.
- **검증(로컬 dev, Chrome, /outbound/orders/new 3행)**: 공급율 r0 →↓ r1 →↓ r2 →↑ r1 →→ 수량 →→ 금액(단가
  읽기전용 건너뜀) →→ 비고 →← 금액 →← 수량 →← 공급율 →← 도서코드 →← 구분 →↑ r0 구분; 구분 ↓ = 팝업
  열기 유지. tsc 0.
- **결정자**: 사용자 (2026-08-18)
- **참조**: [[DEC-156]], [[DEC-104]]/[[DEC-105]](Enter 흐름), `lib/grid-arrow-nav.ts`

### DEC-167: 도서별수불원장 하단 상세 합계행 — 입고/출고/반품/금액 합계 표기 (2026-08-18)

- **보고**: 스크린샷(3411, 2026.03.05 상세) — 하단 거래처별 상세의 합계 행이 현재고(256)만
  표기하고 입고·출고·반품·금액 칸이 비어 있음 → "하단에 관련 합계 정보를 출력" 요청.
- **구현(제품)**: `app/(app)/inventory/ledger/page.tsx` — `detailSums` useMemo 로 상세
  items 의 in_qty/out_qty/rtn_qty/amount 를 클라이언트 합산(일자 상세 API
  `/inventory/book-ledger/day-detail` 는 비페이징 전체 행이라 서버 변경 불필요), 합계
  tfoot 을 `colSpan=3`(거래일자·거래처명·%) + 4 합계 셀 + 현재고(=기말 `closing`) 로 재배치.
  상단 일자 그리드 합계 행(DEC-164 서버 totals)은 불변.
- **검증(로컬 dev, Chrome 실화면, 교문사 remote_153/5019)**: 3411 검색 → 03.05 클릭 →
  합계 행 `입고 0 · 출고 111 · 반품 0 · 금액 2,847,000 · 현재고 256`; DOM 재합산과 일치,
  상단 03.05 출고 109+증정 2=111 정합(상세 출고=출고+증정). tsc 0.
- **결정자**: 사용자 (2026-08-18)
- **참조**: [[DEC-164]] (도서별수불원장 정본 재작성)

### DEC-166: 통합 거래처원장 — 전 거래처 미수 요약 + 전표별 드릴다운 (2026-08-14)

- **보고**: "통합 거래처원장 화면도 동일하게 수정" (DEC-165 후속).
- **전제**: 레거시에 통합 거래처원장 전용 폼은 없음 — form-registry 의 folder
  `Subu32_1` 실물 캡션은 '출판사별 재고 현황'(다른 화면)이라 매핑이 어긋나
  있고, 기존 웹 화면은 수량 축(이동/입고/출고/잔량) 합산 뷰였음. 통합 화면의
  산식·컬럼 정본을 [[DEC-165]](Subu31 거래처거래원장)와 단일 공유하는 웹
  확장으로 재정의.
- **구현(제품 b0ad7c9)**: `customer_txn_ledger_service.customer_ledger_summary`
  — `_opening_receivable_map`(전일미수 GROUP BY Gcode set 판: Sv_Chng 스냅샷
  Σ(Gssum−Gsusu) + 기간전 S1 Σ Gssum − H1 입금 + H1 출금 + Sg_Gsum, 모두
  GROUP BY Gcode 4쿼리) + 기간 S1(GROUP BY Gcode,Gubun,Pubun → 출고/반품
  버킷)·H1(입금−출금=수금) 집계, 행 미수 = 전일미수+출고금액+반품금액(음수)
  −수금액(DEC-165 running 기말값과 동치), **'-전자책' 거래처 미수 0 고정
  특례**, G1 거래처명 300 청크 lookup + 이름/코드 부분일치 필터, 전부 0 행
  제외. 라우터 `/inventory/customer-ledger/summary`. 프론트
  `/ledger/customer-integrated` 전면 재작성 — 상단 거래처별 요약(전일미수·
  출고수량/금액·반품수량/금액·수금액·미수+합계 tfoot) + 거래처 클릭 시 하단
  전표별 목록(거래처원장 상단 동형, daily API 재사용, 지사 라벨·수금 청색).
- **검증**: remote_153/5019 실데이터 571 거래처(4.6s) — 1015 행이 DEC-165
  단일 화면 수치와 완전 일치(2,227,265/189/6,496,910/−120/−3,773,700/
  4,950,475/0), 임의 2곳(00437 밀알서적·3255 한남대) summary↔daily 교차
  대사 MATCH, 로컬 브라우저 실화면(검색→교보문고 드릴다운 전일미수
  94,231,895 + running 일치) 확인. 회귀 가드
  `test_dec166_customer_ledger_integrated.py` 2 PASS(미수 산식·전자책 특례·
  필터), probe 매트릭스 `inventory.customer_ledger_summary` 등록.
- **참조**: [[DEC-165]](산식 정본), Subu31.pas, Tong04.pas _Sv_Chng_

### DEC-165: 거래처거래원장 레거시(Subu31) 동형 재작성 + 데이터 대사 (2026-08-14)

- **보고**: 거래처원장 화면을 레거시(거래처거래원장)와 동일 구성 + 검색 데이터 검증.
- **정본(Subu31.pas 출판 빌드 — L500~640 판독 완료)**:
  - 상단(일자별): 전일미수 행 + 일자 행(거래내역=첫 도서명(+비고)+지사, 외종=같은
    전표(Gcode,Gdate,Jubun,Gjisa,출고반품구분)의 추가 종수 카운트, 출고수량/출고금액
    (출고·입고 합산), 반품수량/반품금액(반품·폐기), 수금액=H1_Ssub(라벨
    Gubun-Oname-Gbigo 예 '현금--…'), 미수금 running) + 합계.
  - 하단(상세): 선택 전표의 도서 라인 — 단가·%(Grat1)·판매수량·출고금액·반품금액·
    수금액·미수금 running + 전일미수 행.
  - 전일미수 = Tong40._Sv_Chng_(_S1_Ssub,_H1_Ssub,_Sg_Gsum,_Sv_Chng) — Sv_Chng
    스냅샷 + 기간전 델타 (도서원장 _Sv_Ghng_ 와 평행 구조, 웹 미이식 — 신규 필요).
  - S1 정렬: Gdate,Jubun,Gjisa,Gubun DESC,Id.
  - **미수 running 확정(L705~720)**: 미수 = 전일미수 + Gosum(출고금액) +
    Gbsum(반품금액, 음수 저장) − Gsusu(수금액). 전일미수 = Tong40._Sv_Chng_
    결과 GsumX 합 (다음 배치: Tong04.pas _Sv_Chng_ 판독 → 서비스 이식).
    '-전자책' 거래처는 미수 0 고정 특례.
- **검증 앵커(실물 스크린샷 — 홍익대[서울]대학서적 1015, 2026.01.01~08.13)**:
  전일미수 2,227,265 · 2.20 출고 112(외7종)/3,793,020 → 미수 6,020,285 ·
  3.16 수금 2,326,625 → 6,217,730 · 3.26 반품 -34/-1,003,740 → 5,213,990 ·
  합계 189/6,496,910/-120/-3,773,700/4,950,475. 상세(2.20): 리빙토픽 22,000·85%·
  20·374,000 부터 8라인.
- **구현(제품 dc13d6e)**: `customer_txn_ledger_service` 신설 —
  `_opening_receivable`(Tong04._Sv_Chng_ (+)경로: Sv_Chng 최근 스냅샷
  Σ(Gssum−Gsusu) + 스냅샷~시작일 S1 Σ Gssum − H1 입금 + H1 출금 + Sg_Gsum
  Σ Gbsum, Scode='X'), `customer_ledger_daily`(전표 그룹 key=(Gdate,Jubun,
  Gjisa,출고성1/반품성2) — 라벨=첫 도서명(비고)-지사, 외N, H1 수금 행
  kind=3(입금+/출금−, 라벨 Pubun-Oname-Gbigo), running=전일미수+출고금액
  +반품금액(음수)−수금액, 합계), `customer_ledger_slip_detail`(kind 필터
  + G4 정가·Grat1% + 라인 running). 라우터 `/inventory/customer-ledger/
  daily·slip-detail`(enforce_hcode_isolation, opening 쿼리 전달). 프론트
  `/ledger/customer` 전면 재작성 — 구 수량원장 페이지를 Subu31 마스터-
  디테일로 교체(전일미수 행 + 합계 tfoot + 수금 행 청색 + 전표 클릭 상세,
  MLF onSelect/onInlineSelect(거래처 인라인 코드=hcode 필드)).
- **검증**: 위 앵커 전 수치 실데이터 일치(전일미수 2,227,265 · 2.20
  112(외7)/3,793,020→6,020,285 · 3.16 수금 2,326,625→6,217,730 · 3.26
  −34/−1,003,740→5,213,990 · 합계 189/6,496,910/−120/−3,773,700/수금
  4,950,475 · 최종 미수 0) + 상세 8라인(리빙토픽 22,000·85%·20·374,000→
  closing 6,020,285) + 로컬 브라우저 실화면 확인(자동완성→조회→전표 클릭).
  회귀 가드 `test_dec165_customer_txn_ledger.py` 3 PASS, probe 매트릭스에
  book/customer-ledger daily 2종 등록(DEC-164 누락분 소급 포함).
- **참조**: [[DEC-164]](동형 구현 패턴), Subu31.pas, Tong04.pas _Sv_Chng_

### DEC-164: 도서별수불원장 레거시(Subu32) 동형 재작성 + 데이터 대사 (2026-08-14)

- **보고**: 화면 항목이 레거시와 동일해야 하고, 날짜 검색 후 날짜 클릭 시
  상세가 나와야 함 + 데이터 확인 요청(실물 스크린샷).
- **정본**: Subu32.pas L330~640 — 일자 버킷(Y입고=입고·Y반품=반입·출고·증정·
  반품·폐기·변경=Sg_Csum), 전일재고=Tong40._Sv_Ghng_, 현재고 running.
  running 확정식(3226 대사): +입고+반입 −출고 −증정 **−반품(음수 저장→실질
  가산)** +변경 −Y폐기 (출판 빌드 주석과 달리 반품 반영 — 합계 257 재현 근거).
- **구현**: book_ledger_service(daily+day_detail, _fetch_stock_asof 재사용) +
  inventory 라우터 2종 + 프론트 마스터-디테일 재작성(전일재고 행·합계 tfoot·
  일자 클릭 상세·거래처명-지사·%).
- **검증(실데이터 3226)**: 전일재고 716 · 1.02 증정1→715 · 1.29 출고15→688 ·
  합계 100/0/706/14/−161/0/0/257 · 상세 703→파주10(85%,187,000)→693→대구5→688
  — 레거시 스크린샷과 전 수치 일치(로컬 화면 검증). tsc 0.
- **참조**: [[book-stock-formula]](Tong40 산식), [[DEC-138]](_fetch_stock_asof)

### DEC-163: 라인 그리드 금액 입력 천단위 콤마 (2026-08-14)

- **보고**: 거래명세서 상세 화면 금액 숫자에 콤마 요청.
- **구현**: OrderLineGrid gssum 셀 number→text(inputMode=numeric) — 표시
  toLocaleString·파싱 콤마 제거. 공유 그리드(신규 출고/상세 팝업/입고) 일괄.
- **검증**: 로컬 화면 — 팝업 금액란 9,600/16,000/38,400 콤마 확인.

### DEC-162: 출고현황 상세 — 전표 목록에 세부 항목(라인) 갯수 컬럼 (2026-08-14)

- **보고**: 거래명세서 내 세부 항목 갯수 표시 요청(출고현황 상세 좌측 전표 목록).
- **구현**: 기존 API 필드 item_count(COUNT(*) 라인수)를 "항목수" 컬럼으로 노출.
- **검증**: 로컬 화면 — 헤더에 항목수 추가·쿠팡 전표 17(접수목록 라인수 일치).

### DEC-161: 거래현황(상세)·출고현황 상세 — 선택 전표 라인 합계 행 (2026-08-14)

- **보고**: 레거시 거래현황(상세) 스크린샷 — 우측 라인 하단 합계(수량·금액)가
  웹에 없음. 거래현황 통합(transactions/status view=detail)의 전표 확장 라인
  테이블 + 출고현황(outbound-status) 상세 라인 테이블 두 곳에 tfoot 합계 추가.
- **검증**: 로컬 화면 — 전표(수량3/103,550) 확장 → 합계 3/103,550 일치. tsc 0.
- **참조**: 레거시 Subu24 거래현황(상세) 합계 행

### DEC-160: 신규 출고 주문 — 추가 내용(G1) 참조 최상단 배치 (2026-08-14)

- **보고**: 사용자 — G1 메모(공급률·택배주소·담당자)를 라인 입력 중 한눈에
  봐야 함 → 거래처 참조 항목 바로 위로 이동.
- **구현**: 공유 SalesStatementReferencePanel 에 `memoOnTop` prop — 신규 출고
  주문에서만 G1 을 전표번호 위 최상단 배치(거래명세서 화면들 종전 유지).
- **검증**: 로컬 화면 — 패널 라벨 순서 추가내용(G1)→전표번호→거래구분→거래처명.

### DEC-159: 삼련 양식지 인쇄 위치 이탈 — 행번호 이중 인쇄 수리 + 배율 진단 (2026-08-14)

- **보고**: 양식지(미리 인쇄 용지) 출력 시 칸 이탈(실물 사진 IMG_9855).
- **사진 분석**: ① 행번호 1~10 이중 인쇄(양식지에 이미 있는데 우리도 인쇄 —
  빈 행 포함 전부) → `.preprinted` 에서 LineNo(첫 td) 숨김 수리. ② 헤더 필드
  (거래처코드/발행일/거래처명) 값이 칸 좌하단으로 이탈(~5mm↓) — field_margin_top
  과보정 의심. ③ 하단 련일수록 위로 당김(누적) — **브라우저 인쇄 배율 <100%**
  (Chrome PDF '맞춤') 시그니처. ②③은 배율 100% 확정 후 재촬영 기반으로
  YAML 캘리브레이션(preprinted_calibration) 정밀 보정 예정 — 배율 섞인 상태의
  오프셋 튜닝은 무의미.
- **참조**: [[DEC-158]], print_sales_statement.yaml(preprinted_calibration),
  analysis/print_specs/sales_statement_triplicate_form.md(2026-07-04 실측)

### DEC-158: 자동출력 미동작 — 일괄 인쇄 타임아웃 + 선마킹 영구 스킵 (2026-08-13)

- **보고**: 경리부가 접수(출력 큐) 생성 → 자동출력 켜진 교문사 계정에서 미출력.
- **실측 진단**:
  - SSE 스트림(received-stream)은 로컬·프로덕션 모두 정상(하트비트 TTFB 0.5s —
    초기 "무응답" 관측은 curl 파이프 버퍼링 착시).
  - **일괄 PDF 3건 = 80초에도 무응답**(장당 ~20s 렌더 × N, DEC-157 CPU 병목) →
    프록시/브라우저 한계 초과로 통째 실패.
  - 모니터 결함: 인쇄 **성공 전에** printedRef 선마킹 → 실패 건이 탭 리로드
    전까지 영구 스킵. 실패가 반복되며 "자동출력 안 됨"으로 관측.
  - (부가) DEC-157 이전엔 렌더가 이벤트 루프를 블록해 SSE tick/하트비트도
    20s+ 정지 — 재연결 루프 유발. 스레드풀 오프로딩으로 해소됨.
- **수정**: 모니터 printFreshKeys — 일괄 1요청 → **1건씩 순차 인쇄**(각 요청
  한계 내) + 건별 실패 격리, 실패 키 printedRef **롤백**(다음 3분 폴/SSE 재시도)
  + 실패 배너. 근본 소요(장당 20s)는 DEC-157 인스턴스 업그레이드로 해소 예정.
- **결정자**: 진행 (2026-08-13)
- **참조**: [[DEC-157]](렌더 CPU 병목), DEC-111(자동출력 SSE), `auto-print/page.tsx`

### DEC-157: 거래명세서 PDF 20초 병목 실측 — weasyprint CPU(렌더 인스턴스) (2026-08-13)

- **보고**: 영업팀 — 신규 명세서 출력 미작동 + 레거시 대비 느림. 사용자 정정:
  "출력 시작이 아니라 시작→완료까지 속도".
- **실측(프로덕션 curl + X-Print-Timing)**: 단건 삼련 PDF 총 ~20-23s =
  detail(DB) 1.2s · seal 0.5s · html 0.3s · **pdf(weasyprint) 20.0s** · log 0.2s.
  PDF 자체는 최경량(1페이지·텍스트 전용·이미지 0·서브셋 폰트 2종·190KB).
- **조치**: ① render_pdf 5개 호출부 run_in_threadpool(렌더 중 이벤트 루프
  블로킹 제거 — 동시 사용자·SSE 응답성), ② FontConfiguration 전역 캐시
  (실측 효과 미미 — 병목은 폰트 스캔이 아니라 렌더 CPU), ③ X-Print-Timing
  계측 헤더 상설(재발 시 즉시 분해 측정).
- **결론**: 20s 는 Render 인스턴스 CPU 에서의 weasyprint 렌더 자체.
  후속 선택지: (a) Render 인스턴스 업그레이드(즉효, 운영 결정),
  (b) 명세서 인쇄를 서버 PDF 대신 **HTML 직접 window.print** 로 전환(클라이언트
  CPU 렌더 — 구조 개선), (c) 물리 인쇄(시작→완료) 속도는 프린터 기종 확인 필요
  (레거시=텍스트 직접출력 vs 웹=PDF 그래픽 인쇄 — 도트/삼련 프린터면 구조 차).
- **결정자**: 진행 중 (2026-08-13 — 실측 완료, 후속 선택 대기)
- **참조**: [[sse-realtime-pattern]](브라우저=프린터 드라이버), DEC-064(삼련 양식),
  `print_service.render_pdf`, `routers/print.py` X-Print-Timing

### DEC-155: 특가(G6) 출고 자동반영 + 할인율 메뉴 숨김 — 특별관리 확인 회신 (2026-08-13)

- **보고**: 영업팀 — ① 특별관리(비율관리) 스크린샷 "기존과 동일하게"(거래처×도서
  비율/단가 수기 등록 → 출고 시 자동 반영), ② "할인율 메뉴 숨겨줘",
  ③ "도서구분/거래처구분(별도 구분 기능) 제거".
- **분석**: 특별관리(Sobo16_special, /master/special) 는 기이식 — G6_Ggeo CRUD +
  거래처/도서 양축 조회. 자동 반영은 거래명세서(resolve_line_defaults 3단계)엔
  있었으나 **출고접수 신규(Sobo27)는 클라이언트 계산만이라 특가 미적용**이 갭.
- **구현**: ① OrderLineGrid `resolveSpecial` prop — 도서 확정 시 lineDefaults
  조회, source=G6_Ggeo 일 때만 비율·단가 override(출고접수 신규 배선).
  ② 할인율(Sobo39) 사이드바 숨김(배본처 선례 — route/API 유지).
  ③ 특별관리 페이지 재작성 — 모드 라디오("별도 구분") 제거, 레거시 Subu16
  원형대로 상단=거래처축/하단=도서축 두 패널 동시 표시(각 패널 조회·편집·삭제·
  신규 등록, 관리자만 출판사 코드 입력).
- **추가(같은 날 DEC-156)**: 신규 명세서 라인 ←/→ 좌우 셀 이동(캐럿 가장자리
  에서만 — 텍스트 편집 보존, ↑/↓ 행 이동·수량 ±1 기존 유지).
- **4차(같은 날 — 브라우저 실검증)**: "거래처 선택 후 즉시 조회+조회 버튼 포커스"
  연쇄 수리: ① 커스텀 Enter 핸들러가 MLF 정확일치 자동확정·부분일치 팝업을
  차단 → 표준 위임 복원, ② 조회 중 disabled 버튼 focus 무시 → load 완료 후
  포커스, ③ **근본 원인 = 거래처 인라인 아이템 코드 필드가 gcode 가 아닌
  hcode**(C2 자동완성 API 명명) — 매핑 수리. 로컬 화면 검증(00001+Enter →
  특가 13행 자동 조회, focusin 로그 최종 BUTTON:조회 안착).
- **3차(같은 날)**: 사용자 지적 — 공통 UX 누락 보강: 축/신규 코드 입력
  MasterLookupField(인라인 자동완성·빈값 Enter 통과), 패널 Enter=다음 입력칸,
  그리드 전 컬럼 정렬(클라이언트)+useGridPrefs 컬럼 설정.
- **검증**: tsc 0. 후속: 라이브 확인 + 가드 테스트 보강.
- **결정자**: 영업팀 (2026-08-13)
- **참조**: [[DEC-153]](지점율 — 특가가 상위), `order-line-grid.tsx`

### DEC-154: 저자관리 기입 순서 + 확장 필드(G3_Gjeo_Ext) (2026-08-13)

- **보고**: 영업팀 — 인세 대비 기입 순서 확정(저자구분→저자코드→저자명→학교→
  학과→자택주소→연구소주소→담당자1→담당자2→원천징수→은행명→계좌번호→
  주민등록번호→메일주소→연락처1→연락처2).
- **구현**: 학과·담당자1/2·원천징수·은행명·메일주소는 G3_Gjeo 대응 컬럼 없음
  (여유 f11~ 은 char(1)+기사용 확인) → 전자책 선례(DEC-068)대로 사이드테이블
  **G3_Gjeo_Ext** 신설(author_ext_service, CREATE IF NOT EXISTS + REPLACE INTO,
  3.23 호환, scope_hcode 격리, 부분 갱신 merge, fail-soft). 라우터 GET merge +
  create/update upsert. 폼 재배열 + 재라벨(학교=구 출신학교, 자택/연구소주소=구
  집/직장주소, 연락처1/2=구 전화/팩스, 주민등록번호). 잔여 레거시 필드는 뒤로.
  라이브: remote_153 테이블 생성 + 라운드트립 확인(프로브 행 정리).
- **검증**: `test_dec154_author_entry_order_ext.py` 8 PASS(부분 merge·no-op·
  fail-soft·모델·라우터 merge/upsert 2회·폼 순서/구라벨 금지). 기존실패 1건
  (author list f-gubun 가드 — LocalCombo 전환 이전 가드, 무관).
- **결정자**: 영업팀 (2026-08-13)
- **참조**: [[DEC-068]](사이드테이블 선례), [[DEC-149]](세부내역), `author_ext_service.py`

### DEC-153: 지점 공급율 전용 칸(H2_Gbun.Gsum1) + 전표 라인 실반영 (2026-08-13)

- **보고**: 사용자 — "지사관리에 공급율 기입 칸 별도 추가 + 반영되게" (지점명에
  '75%' 기입했으나 신규 출고 라인 공급율이 거래처 위탁율 85 그대로라는 보고 —
  DEC-150 분석대로 레거시·웹 모두 지점명 % 는 표시용이었음). **웹 신규 확장**
  (레거시에 없던 자동 반영 — 사용자 명시 요청으로 결정).
- **저장소**: `H2_Gbun.Gsum1`(double) 채택 — 레거시 전 빌드 소스 참조 0건 +
  라이브 전 테넌트 비영 0행 확인한 여유 컬럼. 스키마 변경 0. 컬럼 부재
  테넌트는 자동 비활성(select 0 리터럴·insert/update 스킵).
- **구현**:
  - **CRUD**: h2_gbun_adapt select 에 `grate`(COALESCE(Gsum1,0)) + row_to_api,
    create/update 서비스 수치 배선, 모델·프론트 타입, 지점 패널에
    "공급율(%)" 입력(비우면 거래처 비율)·그리드 컬럼.
  - **반영(거래명세서)**: `resolve_line_defaults` 2.5단계 신설 — gjisa 선택 +
    지점율>0 이면 G1(거래처)/G4(도서) 비율을 덮어쓰고(source=H2_Gbun:branch),
    **특가(G6)·직전거래가(4단계)는 계속 상위**. sales-statement/new 는 기존에
    gjisa 를 전달하고 있어 백엔드만으로 적용.
  - **반영(출고접수 신규)**: 선택 지사 grate>0 → effectiveRate/RateMap 으로
    라인 기본 공급율·구분별 맵 전면 대체 + 지사 변경 시 기존 라인 grat1/gssum
    일괄 재계산(수기 수정은 이후 가능).
- **검증**: `test_dec153_branch_rate_field.py` 11 PASS(어댑터 select/row·CRUD
  SQL 캡처·resolver 오버라이드/0율 폴백/특가 우선/무지사 스킵·화면 배선 2종).
  sales-statement 스위트 pre/post 동일(기존 실패 1건 — Sobo21.Edit106 목록
  페이지 가드, 본 변경 무관). tsc 0. 사용법 PDF 5장 자동 반영 기준으로 갱신.
- **결정자**: 사용자 (2026-08-13)
- **참조**: [[DEC-150]](지점관리 정본·% 표시용 분석), DEC-065(비율 자동 적용
  체인), `sales_statement_create_service.resolve_line_defaults`, `h2_gbun_adapt.py`

### DEC-152: 출고검증 메뉴 총판(물류) 전용 노출 (2026-08-13)

- **보고**: 사용자 — 출고검증(1)/(2)/(개별) 메뉴는 총판(물류) 계정에만 표시.
- **구현**: form-registry 4개 항목(Sobo59_1/59_2/59_3 + shipment 별칭
  Sobo59_verification_shipment_alias)에 `distributorOnly: true` — 확립된
  Sobo39 출고내역서 패턴 재사용(사이드바 isVisibleForm 이
  `distributorOnly && !isDistributorViewer` 면 숨김; isDistributorViewer =
  account_type T2_DIST | build_role distributor | 슈퍼유저). 매트릭스/권한
  (licenseFkey F59)은 기존 그대로 — 노출 게이트만 추가(라우트 직접 접근 차단은
  범위 밖, 선례 동일).
- **검증**: `test_dec152_verification_distributor_only.py` 3 PASS(4항목 게이팅·
  사이드바 강제·선례 유지 — id "Sobo39" 가 할인율 화면과 중복 사용 중이라
  캡션으로 특정) + 메뉴 매트릭스 가시성 스위트 PASS, tsc 0.
- **결정자**: 사용자 (2026-08-13)
- **참조**: DEC-RBAC-02/03(메뉴 매트릭스), `distributor-view.ts`,
  Sobo39 출고내역서(2026-07-24 — distributorOnly 선례)

### DEC-151: 도서 목록 전 컬럼 정렬·기본 순서·재고금액 + 전 목록 sticky 헤더 (2026-08-13)

- **보고**: 사용자 — ① 도서 마스터 목록 "모든 셀에 정렬 기능", ② 기본 표시
  순서 확정(도서분류→도서처리→도서코드→도서명→저자명→ISBN→정가→재고→재고금액→
  서가위치→판형→위탁→쪽수→판수→발행일→비고 — 원문 "판형" 2회는 중복으로 1회
  처리), 나머지는 "컬럼에서 개별 선택", ③ (**중요**) 모든 목록표에서 스크롤 시
  헤더가 플로팅되어 필드명 항상 확인 가능하게.
- **구현**:
  - **전 컬럼 정렬(백엔드)**: `_BOOK_SORTS_ALL`(전 세부 필드 + 파생
    `stock_amount`=(COALESCE(Gsqut,0)*COALESCE(Gdang,0))) 신설,
    `_book_sorts_for_columns` 가 SHOW COLUMNS 존재 컬럼으로 필터해 부재 컬럼
    ORDER BY 1054 를 원천 차단(빈 메타=종전 7종 폴백). 라이브: gdang desc
    실정렬·부재 키 안전 폴백 확인.
  - **기본 표시·순서(프론트)**: 확정 16종 표시 + 재고금액 파생 컬럼(id/sortKey
    `stock_amount`), 라벨 정비(제목→도서명·저자→저자명·단가→정가). 나머지
    25종은 `BOOK_DEFAULT_HIDDEN` 기본 숨김 — 저장 키 `master.book.v2` 승격.
  - **useGridPrefs `defaultHidden`**: 저장 prefs 없을 때 코드 기본 숨김 적용,
    resetAll 도 기본 복원. 기본 숨김 그리드는 빈 hidden 도 명시 저장해
    "전부 표시" 선택을 보존(hasStored 판정에 빈 배열 포함).
  - **sticky 헤더(DataGrid 공통 — 63+ 목록 일괄)**: 카드에
    `max-h-[calc(100dvh-14rem)] + overflow-y-auto`(내부 세로 스크롤, DEC-146
    가로 스크롤과 동일 컨테이너 — sticky 축 유효 조건), `th` sticky top-0
    불투명 bg(thead sticky 브라우저 버그 회피), 합계행(tfoot·DEC-146) sticky
    bottom-0. 하단 페이저(sticky bottom, 페이지 스크롤 기준)는 기존 유지.
- **검증**: `test_dec151_book_sort_sticky_header.py` 13 PASS(화이트리스트 필터·
  파생식·부재 키 무시 SQL 캡처·기본 순서/전 컬럼 sortable 정규식·v2 키·sticky
  클래스·prefs 기본숨김). 그리드 인접 가드 27 PASS, tsc 0.
- **결정자**: 사용자 (2026-08-13)
- **참조**: [[DEC-148]](세부내역 컬럼), [[DEC-146]](minWidthPx·가로 스크롤·합계),
  [[DEC-141]](저장 키 승격 선례), `use-grid-prefs.ts`, `data-grid.tsx`

### DEC-150: 지점관리(H2_Gbun) 패널 라벨 정본화 — "지점별 공급율" 확인 회신 (2026-08-13)

- **보고**: 영업팀 — 레거시(출판관리프로그램-교문사 전자책) "기초관리-거래처관리-
  내용각각-지점별 공급율 지정" 기능이 북이오웍스 어디서 되는지 확인 요청.
- **분석(정본 추적)**:
  - 레거시 경로 = 툴바 내용각각(ToolButton07)→Sobo11.Button007→**Seok01/TSeok10
    지점관리 팝업** — `H2_Gbun` CRUD. DFM 캡션(유통 chul_09·출판 New 전 빌드
    동일): 지역(JUBUN)·지점명(GNAME)·코드(ONAME)·구분(GDATE)·번호(GNUM1)·
    출고정지(GBIGO). 출고(Subu21)가 지사 콤보를 "Jubun|Gname" 으로 채우고
    Gbigo 비면 출고, 채워지면 지점 출고정지 차단.
  - **"지점별 공급율"은 자동 적용이 아니라 기입 관례** — 전 빌드에서 H2_Gbun
    % 파싱/금액 적용 코드 0건. 전자책(5097)은 지역='B2B/C'·지점명='50%' 로
    등록해 출고 콤보 "B2B/C|50%" 선택→전표 지사 라벨 저장, 정산 시 참조.
    자동 공급율은 종전대로 G1_Ggeo.Grat1~7(DEC-065)뿐 — 웹도 동일(갭 아님).
  - **웹 커버리지 확인(라이브)**: 거래처 상세 지점 패널(CustomerBranchPanel,
    Seok10 등가)로 CRUD 기이식. 전자책 테넌트(5097, remote_153 chul_09_db 공유)
    스코프로 스크린샷의 실행(id 12475/12476 "B2B/C|50%"/"B2C|70%") 정상 조회 —
    resolve_h2_hcode_for_customer 가 chul_09 계열에서 세션 hcode 사용(격리 OK).
    지점 출고정지 차단도 이식됨(assert_sales_statement_search_allowed).
- **수정(유일 갭 = 오라벨)**: 패널 라벨을 DFM 정본으로 정정 — 지사코드→**지역**,
  담당→**코드**, 일자→**구분**, 정지사유→**출고정지 사유**, 지사명→지점명.
  그리드에 구분(gdate) 컬럼 추가(레거시 팝업 5컬럼 동형). 접이식 제목
  "지점관리 (지사)" + 공급율 기입 관례 설명 추가. 스키마·API 변경 0.
- **검증**: `test_dec150_branch_panel_canonical_labels.py` 3 PASS + branches
  CRUD 8 PASS, tsc 0. 사용법 PDF: `docs/북이오웍스-지점관리-사용법-2026-08-13.pdf`.
- **결정자**: 사용자 (2026-08-13 — "개선 필요 사항만 수정")
- **참조**: [[DEC-149]](거래처 세부내역), DEC-065(Grat1~7 자동 적용),
  `h2_gbun_adapt.py`, `customer-branch-panel.tsx`

### DEC-149: 거래처관리 목록 = 세부내역 전면 + Gpper 오라벨 교정(담당자1) (2026-08-13)

- **보고**: 사용자 — "거래처 관리 화면의 모든 정보가 기본적으로 표에 추가"(누락
  확인 지시) + 기본 순서 확정: 거래처구분(거래처구분2 삭제)→지역→코드→명→
  사업자등록번호→대표자→사업자주소→업태→종목→전화→팩스→이메일→담당자1→담당자2→비고1.
- **정본 교정(레거시 대사)**: Subu11.pas 전 빌드(출판/위러브/New) 동일 —
  **Gpper=담당자(Edit110, 텍스트)** · **Gssum=한도액(Edit131)** ·
  **Gphon=핸드폰번호(Edit132)**. 라이브(00004 영풍문고): Gpper='인터넷, 총판'
  Gphon='02-399-6412' Gssum=20,000,000 = 레거시 화면 정확 일치. 종전 웹은
  gpper 를 "한도액" **숫자**로 취급 — 담당자 실데이터가 0 으로 소실(저장 시
  파괴 위험)되고 진짜 한도액·핸드폰번호는 미노출이었다.
- **구현**:
  - **백엔드**: `list_customer_master` 에 세부 필드 전면 추가(gfax2·gpper·gphon·
    name1·name2·yesno·grat7·gqut1·grat9·gssum — 존재-컬럼 기반 ''/0 안전).
    `customer_detail_select_sql` gpper 텍스트화 + gphon/gssum 추가,
    update/create 경로 gpper·gphon=텍스트, gssum=숫자로 배선.
    `CustomerListItem/Detail/Update/Create` 모델 확장(gpper: float→str).
  - **엑셀**: `CUSTOMER_FULL_COLUMNS` ("한도액",gpper)→("담당자1",gpper) +
    핸드폰번호(gphon)·한도액(gssum) 추가(32→34컬럼), NUMERIC_KEYS gpper 제거·
    gssum 추가(역반영 텍스트 보존).
  - **프론트**: 목록 컬럼 = 확정 순서 15종 + 나머지 상세(비고2·핸드폰·우편번호·
    한도액·비율 7종·신간수량·계산서구분·발행유무✓·출고정지✓). 전화/팩스는
    1·2 합침. ocode(거래처코드2) 목록 제외(삭제 요청). 상세 폼 "한도액"(gpper)
    → "담당자1" 정정 + 핸드폰번호/한도액(진짜) 필드 신설.
- **검증**: `test_dec149_customer_list_detail_columns.py` 6 PASS(정본 시맨틱·
  텍스트 표현식·모델·엑셀 카탈로그·화면 순서/제외·상세 폼 라벨). 인접 40 PASS
  (customer export 32→34 기대치 갱신), tsc 0.
- **결정자**: 사용자 (2026-08-13 — 순서 확정 포함)
- **참조**: [[DEC-148]](도서 동형), [[DEC-146]](minWidthPx·가로 스크롤),
  [[g1-ggeo-column-semantics]](컬럼명≠의미 선례), `g1_ggeo_adapt.py`

### DEC-148: 도서관리 목록 = 도서 세부내역 컬럼 전면 (2026-08-13)

- **보고**: 영업팀 — "기초관리-도서관리: 컬럼에 도서세부내역으로 보여지는 내용
  추가 요청".
- **구현**:
  - **백엔드**: `list_books` SELECT 를 `g4_book_adapt.book_detail_select_sql`
    재사용으로 교체 — 상세 폼(Panel002) 필드 전면(분류 Sname denorm·처리·구분·
    코드2·비율구분·등록번호·판형·단위·묶음·등록일·정지사유·비고·원가·매입가·
    쪽수/판수/덩이/그램·비율 Grat1~7·재고 Gsqut/Jego1~4·플래그 Bigo1/2·Grat9)을
    목록 행으로 반환. 존재-컬럼 기반이라 테넌트 DDL drift 안전(누락 ''/0),
    **JOIN 0**(DEC-068 목록 행증식 금지 — 전자책 사이드테이블 제외).
    SHOW COLUMNS 실패/빈 결과 시 종전 기본 7컬럼 폴백(목록 500 금지).
    hcode/yesno/bigo3 은 목록 미노출.
  - **프론트**: 목록 컬럼 32종 추가(상세 폼 순서: 분류→처리→구분→…→재고 4종→
    플래그 3종 ✓표기). 폭은 컬럼별 `minWidthPx`(DataGrid 확장 — 사용자 px·% 미지정
    시 th 기본 폭으로도 사용) + DEC-146 가로 스크롤. 불필요 컬럼은 컬럼 설정으로
    계정별 숨김. **gpost 라벨 "출판사"→"서가위치" 정정**(상세 폼·라이브 값
    'H13, 25' 기준 오라벨).
- **확장(같은 날 2차 — 엑셀)**: 사용자 보고 "엑셀 저장 헤더도 추가" —
  `BOOK_COLUMNS`(export)를 목록 화면과 1:1(40컬럼, "출판사"→"서가위치" 헤더
  정정)로, `BOOK_IMPORT_MAP`(역반영)을 편집 가능 필드 전면으로 확장(구 헤더
  "출판사" 하위호환 별칭 유지, 읽기전용 재고 5종 import 제외, 수치 필드
  `BOOK_NUMERIC_KEYS` 14종 — 플래그는 텍스트 유지).
- **검증**: `test_dec148_book_list_detail_columns.py` 6 PASS(세부 필드 반환·
  JOIN 0·폴백·화면 라벨/모델·export 카탈로그·import 별칭/읽기전용 제외).
  인접 스위트 31+19(excel export, book_export 기대치 신 헤더 갱신) PASS, tsc 0,
  hcode 감사 변동 없음. **라이브 대사**(교문사 5019, 00004): 41키 — 서가위치
  H13,25 · 도서구분 A · 출고정지 ✓ · 단가 13,000 = 상세 화면 일치. 기존실패
  2건(gbun 분리 가드·book-code scope_hcode)은 HEAD 재현 확인 — 본 변경과 무관.
- **결정자**: 영업팀 (2026-08-13)
- **참조**: [[DEC-146]](최소폭·가로 스크롤), [[DEC-068]](목록 JOIN 금지·전자책
  사이드테이블), [[DEC-033]](DDL drift 어댑터), `g4_book_adapt.py`

### DEC-147: 도서별판매 수량 컬럼 표기 "○○수"→"○○수량" 전면 (2026-08-13)

- **보고**: 영업팀 스크린샷 주석 — "모든 카테고리의 '수'를 '수량'으로 변경".
- **구현**: 도서별판매 화면 그리드 + XLSX 헤더 5종 동시 변경(입고수량·출고수량·
  반품수량·증정수량·폐기수량). 거래처판매는 이미 "○○수량" 표기라 변경 없음.
  "매출부수"(DEC-141 영업팀 명명)와 금액 컬럼("○○액"), 타 화면(도서통계
  Sobo37 축약 라벨, 도서별년말집계)은 범위 외 — 요청 화면 한정.
- **검증**: `test_sales_team_a_batch.py` LabelCorrectionTests 를 신 표기로 갱신
  (화면 needle 6종 + XLSX 5종 + 구표기 금지). 25 PASS, tsc 0.
- **결정자**: 영업팀 (2026-08-13)
- **참조**: [[DEC-141]](매출부수 명명), 영업팀 A3(2026-08-03 — 증정/폐기 오라벨 교정)

### DEC-146: 도서별판매 전체 결과 합계행 + DataGrid 컬럼 최소폭 + 상세 패널 lazy (2026-08-13)

- **보고**: 사용자 — ① 도서별판매 "합계가 나올 수 있을까요?" (합계는 **전체
  검색된 목록** 기준 요청), ② 2분할 화면에서 컬럼 과압축 — 헤더가 한 글자씩
  세로로 꺾이고 숫자가 표(카드) 밖으로 넘침 → 처리 방안 질의에 "공통 DataGrid
  전체 적용" + "상세 패널은 선택 시에만 표시" 확정.
- **구현**:
  - **합계행(서버 계산)**: `get_book_sales_daily` 가 페이징·BOOK_SALES_MAX 상한
    **적용 전** full_rows 에서 `_BOOK_SALES_MEASURE_KEYS` 합계를 계산해
    `totals` 로 반환(재고 3종·정가는 도서별 시점/마스터 값이라 행 합산 무의미 —
    제외). `BookSalesTotals` 모델(+캐멀) 신설, 화면은 DataGrid `<tfoot>` 합계행
    "합계(전체 결과)" — 매출부수/매출액은 행과 동일 파생식(음수 관례 합산=차감).
  - **DataGrid 공통 최소폭**: 컬럼별 최소폭(px 지정 너비 ?? `minWidthPx` ??
    기본 right 104/그 외 96) 합을 `<table style.minWidth>` 로 강제 — 표가
    좁아지면 찌그러지는 대신 기존 카드 `overflow-x-auto` 가로 스크롤 발동.
    table 의 `min-w-0` 클래스 제거(최소폭 무력화 방지). 넓은 화면은 종전과
    동일(w-full 유지).
  - **합계행 공통 prop**: `totals`/`totalsLabel` — 표시 컬럼 순서·숨김에 맞춰
    tfoot 렌더, 값 없는 컬럼 빈 셀, 첫 컬럼에 라벨. **전체 검색 결과 합계**를
    넘기는 것이 규약(페이지 합계 금지).
  - **거래처판매 상세 패널 lazy**: 행 선택 시에만 렌더(빈 안내 패널 제거) —
    평소엔 목록이 전체 폭 사용(도서별판매 DetailPanel 동형). sticky 는 DEC-145
    유지.
- **검증**: `test_dec146_book_sales_totals_grid_minwidth.py` 7 PASS(전체 결과
  기준 합계·측정치 화이트리스트·모델·min-width/tfoot 가드·화면 배선 2종).
  **라이브 대사**(교문사 5019, 91184, 07.11~08.11): 9행 — 합계 출고수 164 /
  출고액 5,457,560 / 증정수 3 = 화면 행 합산 일치. 리포트 스위트 76 PASS,
  tsc 0.
- **결정자**: 사용자 (2026-08-13 — 적용 범위 선택 포함)
- **참조**: [[DEC-145]](상세 sticky), [[DEC-141]](매출부수/매출액 파생),
  [[DEC-138]](일자×도서 축), [[DEC-055]]/[[DEC-068]](그리드 prefs), `data-grid.tsx`

### DEC-145: 거래처판매 수금행 최종거래일 반영 + 도서별 상세 패널 sticky (2026-08-13)

- **보고**: 사용자 — 거래처판매 화면 스크린샷(08-11 15:24 창) "거래처 수금액은
  있는데 거래 종수 등이 모두 0" + "우측 도서 상세가 스크롤을 따라오게" 요청.
- **진단(집계는 정상 — 표시 문제)**: 라이브 대사(교문사 5019, 07.11~08.11) —
  S1_Ssub 판매 데이터 실재(출고 1,435건/6,442부/166,864,330원), 서비스도 지사행에
  정상 집계(79행 중 61행 수량 비영). 다만 ① 수금(H1_Ssub)은 Gcode 단위라
  **본사행(gjisa='')** 에 적재(레거시 Subu62 `Locate('Gcode;Gjisa',[Gcode,''])`
  1:1 — DEC-139 설계 그대로)돼 판매(지사행)와 분리 표시되고, ② 그 수금 전용
  행의 최종거래일이 빈값이라 기본 정렬(최종거래일 asc)에서 **전부 목록 최상단에
  몰려** 첫 화면이 "수금액만 있고 전부 0" 으로 오인됐다.
- **수정**:
  - **백엔드**: H1_Ssub 수금 집계에 `MAX(Gdate)` 포함, 수금 반영 행의
    gdate = max(판매 최종일, 수금 최종일) — 수금 전용 행도 최종거래일을 얻어
    날짜 정렬에 자연 편입(빈값 클러스터 소멸). 라이브 재검증: 00001 본사행
    gdate=2026.08.10(수금최종일) 확인.
  - **프론트**: 우측 "도서별 상세" 패널 `xl:sticky xl:top-4 xl:self-start
    xl:max-h-[calc(100vh-2rem)] xl:overflow-y-auto` — 좌측 목록 스크롤 시 추종,
    긴 상세는 패널 내부 스크롤(도서별판매 Sobo61.DetailPanel 동형).
- **검증**: `test_dec145_customer_sales_sugum_gdate.py` 6 PASS(수금 전용 행
  수금최종일·본사행 max 병합·판매일 우선 유지·asc 정렬 빈값 0건·sticky 클래스
  가드) + dec139/상세 인접 스위트 11 PASS. 정적 감사(hcode/coalesce) critical 0.
- **결정자**: 사용자 보고 전달 (2026-08-13)
- **참조**: [[DEC-139]](수금액 본사행 적재 설계), [[DEC-087]](MAX(Gdate) 표시
  필드), [[DEC-082]](서버 정렬 화이트리스트), `reports_service.get_customer_sales`

### DEC-144: 통계 필터바 Enter 흐름 마감 — 집계단위 픽 필드화 + 룩업 빈값 Enter 통과 (2026-08-11)

- **보고**: 영업팀 — ① 기간별 매출분석 "집계단위 선택 후 '엔터' 조회가
  안 됩니다", ② 거래처별 판매분석 "거래처코드 선택 후 '엔터'로 다음탭이
  안 넘어갑니다" (두 스크린샷 모두 08.10 구 창이지만 ①은 현 배포분에도 실재,
  ②는 빈값 Enter 경로가 실재).
- **원인/교정**:
  - ① 집계단위가 **네이티브 `<select>`** — macOS 드롭다운의 옵션 확정 Enter 는
    OS 메뉴가 소비해 DOM 에 도달하지 않아 advanceFilterOnEnter(자동 조회
    클릭)가 못 받는다. → 확립된 **LocalComboField(픽 필드)** 로 교체(DEC-112/134
    패턴): Enter=팝업→↑↓ 선택→Enter=값+다음 칸, 마지막이면 `advanceAfterSelect`
    가 조회 버튼 자동 실행. 스톱 id(Combo_GroupBy) 유지.
  - ② StatsFilterBar 의 MasterLookupField 5개(hcode·거래처 2·도서 2)가
    ``onKeyDown`` 미전달 — MLF 규약상 빈값 Enter 는 onKeyDown 제공 시 통과
    (버블 → 다음 스톱), 미제공 시 검색 팝업을 연다(DEC-104/105 "빈값 Enter
    통과" 위반 지점). → no-op ``onKeyDown={() => {}}`` 전달(검증된 화면들과
    동일). 확정값 Enter 이동은 DEC-134 정확일치 자동확정(confirmEnter →
    focusNext)이 기존 배포분에서 이미 담당.
- **추가(같은 날 3차 — 도서 회전율)**: "입고, 출고, 반품, 증정, 폐기 순으로
  표기" — get_book_turnover 항목에 return_qut/gift_qut/discard_qut(음수 관례
  그대로) + FE 컬럼·XLSX 헤더를 요청 순서로 추가. Enter 이동·도서명 표기는
  공용 StatsFilterBar 라 본 DEC ①②로 함께 해결됨.
- **검증**: `test_dec144_stats_filter_enter_combo.py` 3 PASS(픽 필드·native
  select 부활 금지·no-op onKeyDown ≥5·회전율 표기 순서/컬럼). 전체 스위트
  실패 집합 = 기존 120건(신규 회귀 0). tsc 0.
- **결정자**: 영업팀 보고 전달 (2026-08-11)
- **참조**: [[DEC-140]](필터바 Enter 스톱), [[DEC-134]](정확일치 자동확정),
  DEC-104/105(빈값 Enter 통과), [[keyboard-input-flow]], `local-combo-field.tsx`

### DEC-143: 거래처별 판매분석 반품·판매 표기 + 거래처명 표기 + 단일 거래처 필터 (2026-08-11)

- **보고**: 영업팀 — "출고관련 자료만 잡힙니다. 반품수, 반품금액, 판매부수,
  판매금액도 표기요청" + "거래처명도 표기 요청"(거래처코드 룩업).
- **구현**: 행 데이터(get_customer_sales 재사용)에는 필드가 이미 있었고 표기만
  누락 — ① totals 에 bqut/bsum/sell_qut/sell_sum 합계 추가, ② 그리드 컬럼
  반품수량/반품금액/판매부수/판매금액(음수 관례 — 판매=출고+반품) + 요약 카드
  총 판매부수/총 판매금액, ③ XLSX 헤더 4종 추가, ④ StatsFilterBar 거래처 룩업
  선택 시 거래처명 표시(DEC-140 도서명 패턴), ⑤ 한쪽만 지정 시 단일 거래처
  필터(get_customer_sales 의 A4 gcode 파라미터로 위임 — 종전 양끝 필수).
- **검증**: `test_dec143_customer_analysis_measures.py` 5 PASS(합계·단일 필터
  위임·export 헤더·화면/필터바 가드). **라이브 대사(00431 알라딘)**: 반품
  −251/−5,308,715·판매부수 6,024·판매금액 157,586,075 — 거래처판매 화면 값과
  정확 일치. 전체 스위트 실패 집합 = 기존 120건(신규 회귀 0). tsc 0.
- **결정자**: 영업팀 요청 전달 (2026-08-11)
- **참조**: [[DEC-139]](수금액 — 동일 행 데이터), [[DEC-140]](룩업 이름 패턴),
  [[DEC-141]](판매부수/매출부수 개념), `stats_service.get_customer_analysis`

### DEC-142: 도서별년말집계 일(day) grain + "파지"→"폐기" 전면 + 도서명 표기 (2026-08-11)

- **보고**: 영업팀 — ① 시작월/종료월에 "일" 추가 요청, ② "파지" 단어를 "폐기"로
  모두 수정, ③ 도서 검색 선택 시 도서명도 함께 표기(그리드에는 이미 있음 —
  필터 룩업 대상).
- **구현**:
  - **일 grain(웹 확장)**: `_grain_key` 에 day 모드(일자 전체 키) + 집계 단위
    라디오 년/월/**일**. 날짜 입력은 `DateFieldYMD monthOnly={grain!=="day"}` 로
    일 정밀 확장, grain 전환 시 값 상호 변환(월→일: 시작=1일/종료=말일, 일→월:
    앞 7자). 백엔드 경계: 'YYYY.MM.DD' 입력은 래핑 없이 그대로, 종전
    'YYYY.MM' 은 `.00/.99` 월 경계 래핑 유지(하위 호환). grain 화이트리스트
    (year/month/day 외 → year). 월/일 드릴다운 parent 필터 동작 동일.
  - **파지→폐기**: 화면 컬럼(파지수/파지액)과 XLSX export 헤더
    (`_YEAR_END_EXPORT_COLUMNS`) 모두 폐기수/폐기액 — A3(DEC-132) 레거시 정본
    캡션(GPQUT=폐기수량)과 정합, 이 화면만 구 라벨이 남아 있었다.
  - **도서명 표기**: 도서코드 시작/끝 룩업 선택 시 도서명을 아래 표시(수기 수정
    시 해제) — DEC-140 StatsFilterBar 와 동일 패턴.
- **검증**: `test_dec142_year_end_day_grain.py` 5 PASS(그레인 키 3종·day 버킷/
  일 정밀 경계·월 래핑 하위 호환·export 헤더·FE 소스 가드). 전체 스위트 실패
  집합 = 기존 120건 그대로(신규 회귀 0). tsc 0.
- **결정자**: 영업팀 요청 전달 (2026-08-11)
- **참조**: [[DEC-132]](A3 파지→폐기 정본), [[DEC-140]](룩업 도서명 패턴),
  Subu67.pas(grain Copy(Gdate,1,4/7)), `DateFieldYMD.monthOnly`

### DEC-141: 도서별판매 반품액(GBSUM)·매출부수/매출액·컬럼 순서 확정 (2026-08-11)

- **보고**: 영업팀 주석(배포된 일자×도서 새 화면 위, 2026-08-11 15:11 라이브 창) —
  ① 증정수를 폐기수 앞으로, ② 출고액 뒤에 반품액 추가, ③ 매출부수(출고수+반품수),
  ④ 매출액(출고액+반품액).
- **구현**: 분기표(`_apply_book_sales_branch`) 반품 분기에 **gbsum(반품액) 누적**
  추가 — 레거시 Subu61 L402~404 정본(Gbqut += T01 **and Gbsum += T02**, 음수
  관례 그대로). 셀 초기화 전 지점(도서요약/일자/일상세/출판사통계/거래처상세)에
  gbsum 슬롯 + 측정치 키 등재(반품액만 있는 행도 0행 제외에 안 걸림).
  매출부수/매출액은 FE 파생(goqut+gbqut / gosum+gbsum — 반품 음수라 합산=차감,
  거래처판매의 판매수량/판매금액과 동일 개념). 컬럼 순서 확정: 날짜·코드·도서명·
  정가·입고·출고·반품·**증정**·폐기·재고 3종·출고액·**반품액**·**매출부수**·
  **매출액**·폐기액. 저장 컬럼순서가 새 기본을 덮지 않도록 그리드 설정 키를
  `reports.book-sales.v2` 로 승격(구 저장 순서·너비 초기화 — 의도된 리셋).
- **검증**: `test_dec141_book_sales_return_amount.py` 3 PASS(반품액 누적·측정치
  키·FE 순서/파생/키 가드) + 기존 정적 가드 1건 신 계약 갱신(GridRow 타입).
  전체 스위트 실패 집합 = 기존 120건 그대로(신규 회귀 0). tsc 0.
- **잔여**: XLSX export(도서 요약 축) 헤더에 반품액/매출부수/매출액 미반영 —
  요청 시 후속.
- **결정자**: 영업팀 주석 전달 (2026-08-11)
- **참조**: [[DEC-138]](일자축·재고 3종), [[DEC-132]](A3 라벨 정본), Subu61.pas
  L402~404, `use-grid-prefs`(DEC-134 applyOrder)

### DEC-140: 기간별 매출분석 단일 패스(30s 타임아웃 교정) + 필터바 도서명·Enter 흐름 (2026-08-11)

- **보고**: 교문사-경리부 — 기간별 매출분석 ① "서버 응답이 30000ms 를 초과했습니다"
  (도서 90008, 01.01~08.10, 일 단위), ② 도서명도 표기 요청, ③ 도서코드 선택 후
  Enter 로 다음 탭 이동 안 됨.
- **원인(①)**: `get_sales_period` 가 슬라이스(일 단위 = 222구간)마다
  `get_book_sales` 를 반복 호출(N+1) — 구간당 S1_Ssub 풀 집계+도서명 lookup+
  Sg_Csum 까지 실행되어 FE 30s 타임아웃 초과. 슬라이스당 limit=2000 절단으로
  합계가 깎일 잠재 오차도 있었다.
- **교정(①)**: `reports_service.get_daily_sales_cells` 신설 — S1_Ssub 를 기간
  전체 **단일 쿼리**(GROUP BY Gdate,Scode,Gubun,Pubun)로 사전 집계하고
  `_apply_book_sales_branch` 로 일자 셀 구성(매출=goqut/gosum·매입=giqut/gisum
  의미 불변, DEC-084 Ocode 절 없음). stats 는 bisect 로 슬라이스 버킷에 합산만 —
  SQL 은 reports 계층에 배치해 "stats 계층 신규 SQL 0"(DEC-040,
  TC-C13-S-03) 아키텍처 가드 준수. 비정형 Gdate 는 warn 후 스킵.
  **라이브: 동일 조건 30s 타임아웃 → 1.1s**(도서 지정), 전체 0.2s. 90008 실적
  0 은 데이터 사실(기간 내 0행/전 기간 39행 — 원시 COUNT 재확인).
  부수 교정: 도서코드 한쪽만 지정 시 종전엔 무시(양끝 필수) → 단일 도서 필터로
  동작(화면 라벨에 명시).
- **교정(②③, StatsFilterBar 공용 — sales-period·book-turnover 등)**:
  도서 선택 시 도서명 표기(수기 수정 시 이름 해제), 필터 Enter=다음 이동
  (DEC-104/116 규약 — 노출 순서대로 스톱 구성: hcode→거래처→도서→시작/종료일→
  집계단위→분기→조회). `refocusAfterSelect` 로 팝업 선택 후 원위치 복귀.
- **검증**: `test_dec140_sales_period_single_pass.py` 4 PASS(일/주 버킷 합산·
  비정형 일자 스킵·단일 bcode 절·필터바 소스 가드). 구계약(N+1 위임) 테스트
  5건 + 정적 가드 정합: dec084 위임→단일패스, dec086 3건, sort_params,
  buckets 2건 갱신 — 스탯 계열 48 PASS. 전체 스위트 실패 집합 = 기존 120건
  그대로(신규 회귀 0). tsc 0·변경 컴포넌트 eslint 0.
- **결정자**: 사용자 (2026-08-11 — 교문사-경리부 확인 요청 전달)
- **참조**: [[DEC-137]](분기표 공유), [[DEC-138]](일자 셀 패턴), DEC-084(Ocode),
  DEC-040/TC-C13-S-03(stats 계층 SQL 0), `stats-filter-bar.tsx`,
  `reports_service.get_daily_sales_cells`

### DEC-139: 거래처판매 수금액 — H1_Ssub 입출금 집계 구현 (2026-08-11)

- **보고**: 교문사-경리부 — "거래처판매: 수금액이 안 잡힙니다"(스크린샷: 00431
  알라딘 수금액 0). 원인은 회귀가 아니라 **의도된 이연**: 서비스 헤더에
  "H1_Ssub 입출금 sub-query(D-INQ-4)는 후속 C5 로 이연 — 0 채움" 으로 기록돼
  있었고, FE 는 DEC-132 에서 gjsum 라벨만 '수금액'으로 정정해 둔 상태였다.
- **정본**(출판 Subu62.pas L410~L486): H1_Ssub(입출금) 기간 집계 —
  거래처(X/Z) 모드 = **Σ입금 − Σ출금**, 입고처(Y) 모드 = 반전(Σ출금 − Σ입금).
  Gcode 단위 집계라 본사행(gjisa='')에 부여하고, 수금만 있고 판매가 없는
  거래처는 행 신설(레거시 Append 동등). 레거시의 상관 서브쿼리 대신 mysql3
  안전형(단일 GROUP BY Hcode,Gcode,Gubun + 파이썬 부호 버킷 — 레거시 ePrnt='2'
  Sum(if(...)) 변형과 동치)으로 구현. H1_Ssub 부재 테넌트는 warn 후 0 유지.
- **검증**: `test_dec139_customer_sales_collections.py` 4 PASS(입금−출금·Y 모드
  반전·수금 전용 거래처 행 신설+이름·H1 부재 0 폴백). **라이브 삼중 대사**
  (remote_153×5019): 00227 영광도서 수금액 **1,700,000** = 레거시 거래처거래원장
  스크린샷 합계와 정확 일치(동시에 출고 67·출고액 1,760,365·반품 −2 도 일치);
  00431 알라딘 0 → 136,833,275, 기존 판매 집계 불변. 전체 스위트 실패 집합 =
  기존 120건 그대로(신규 회귀 0).
- **참고**: 부분 실행(-k) 시 tc_inq_007 실패는 스위트 순서 오염 아티팩트(단독·
  전체 스위트 모두 PASS — C6 라우터 계약 테스트의 module-level auth override 와
  동일 계열). Sg_Gsum 후처리(레거시 Subu62 L489~)는 별도 필드라 범위 외 백로그.
- **결정자**: 사용자 (2026-08-11 — "수정 완료 되었는지 확인해라" → 미구현 확인 후 구현)
- **참조**: [[DEC-132]](gjsum=수금액 라벨 정정), [[DEC-138]], 출판 `Subu62.pas`,
  `reports_service.get_customer_sales`

### DEC-138: 도서별판매 일자×도서 축 + 기간말 재고 3종(수불 누적) — 영업팀 B1/B2 (2026-08-11)

- **회신(영업팀 Q1~Q3, 2026-08-11)**: Q1=② **설정 기간 말 시점 재고(수불 누적)**
  — 예시: 제작 1,000부 = 본사 700 + 창고 300 입고, 모든 입·출고·반품은 본사에서
  조정, 본사 소진 시 재인쇄 또는 창고→본사 이동. Q2=[선택] 버튼 **유지**(오클릭
  대비). Q3=회신 누락 → 원문 의견("동일 일자 여러 도서 → 클릭 시 우측 상세")대로
  **일자×도서 다행 가정** 채택(이견 시 정정 — 본 항목이 가정의 단일 기록).
- **B1 구현**: `GET /reports/book-sales?groupMode=daily` — S1_Ssub GROUP BY
  (Gdate,Bcode,Scode,Gubun,Pubun) → `_apply_book_sales_branch` 재사용(분기표·
  전 측정치 0 행 제외 DEC-137 규칙 공유). 기본 `book` 모드·C14 캡처는 불변.
  `GET /reports/book-sales/day-detail` — 해당 (일자,도서)의 거래처별 내역
  (레거시 도서별수불원장 하단 상세 동등, G1_Ggeo 이름은 자사 Hcode 행 우선).
  프론트: 날짜 1열 + 재고 3종 컬럼, 행 클릭 → 우측 sticky 상세 패널.
- **B2 구현(재고 산식 정본)**: 출판 빌드 `Tong04.pas` TTong40._Sv_Ghng_/_Sv_GhngX
  1:1 — ① 스냅샷일 = Sv_Ghng MAX(Gdate) ≤ 기간말, ② 정품재고 = Σ(Gsusu−Gsqut)
  (Sv_Ghng, 축=Scode LIKE), ③ S1_Ssub 델타(스냅샷<Gdate≤기간말, 축=Ocode LIKE)
  분기표: Y·입고/반품 +q, 출고/증정 −q, 폐기 +q(음수 저장 관례로 실질 차감),
  비품·분기표 밖 0, (비Y)반품 −q. 축: **A=본사 / B=창고 / 무필터=재고합계**
  (영업팀 예시 700+300=1,000 정합). 반품재고(Obqut/Gbqut)·폐기 잔량 버킷은
  1차 미표시(후속 후보). `includeStock=1` 로 두 모드 공통 — 같은 도서의 일자행에
  동일 값 반복(Q1 정의가 '기간말 시점'이라 러닝 잔량이 아님을 명시).
- **라이브 대사(읽기전용, remote_153×5019)**: 도서 3411 asof 07.09=**981** /
  07.16=**960** — 레거시 도서별수불원장 현재고와 정확 일치. 일자 흐름(07.01 증정1
  ~ 07.16 출고6) 전 행 일치, 07.09 상세=알라딘 1부 일치. 본사 981/창고 0(전량
  본사축 도서).
- **검증**: `test_dec138_book_sales_daily_stock.py` 9 PASS(분기표·스냅샷+델타·
  일자축·0행 제외·상세·라우터 배선·프론트 가드·[선택] 버튼 유지). 전체 스위트
  실패 집합 = 기존 120건 그대로(신규 회귀 0). tsc 0·변경 파일 eslint 0.
  라우터 hcode 감사 critical 0(신규 day-detail 포함), 도메인 감사 증감 없음.
  probe 매트릭스에 daily/day-detail GET 등록.
- **잔여(백로그)**: ① XLSX export 는 도서 요약(book) 축 유지 — 일자축 export 는
  요청 시. ② 반품재고/폐기 잔량 버킷 표시. ③ Q3 공식 회신 수령 시 가정 확정.
- **결정자**: 영업팀 회신(2026-08-11) + 사용자 지시("질문사항 반영해서 수정")
- **참조**: [[DEC-137]](0행 제외·측정치 키), DEC-132(A 배치), DEC-084(Ocode),
  `docs/sales-team-feedback-plan-2026-07-31.md`, 출판 `Tong04.pas`(TTong40),
  `Subu32.pas`(도서별수불원장 — 축 필터 원형)

### DEC-137: 원장 축 정본 교정(Gcode=거래처·Hcode=출판사) + 도서별판매 0권 제외 + 재고 메뉴 통합 (2026-08-11)

- **보고**: 교문사-경리부 스크린샷 5매 — ① 도서별판매: 기간 검색 시 해당 기간
  판매 0권(전 컬럼 0) 도서까지 전부 노출, ② 거래처원장: "조회" 시
  `HCODE_FORBIDDEN` 403, ③ 거래처원장에 도서코드 필터 불필요, ④ 수불 관련
  카테고리 3개 → 1개 + 재고관리·재고원장 그룹 통합 제안. 사용자 지시: "이를
  기준으로 전체 계정에 대해서 화면 출력 쿼리 등을 맞춰라".
- **원인(구조 — 축 오배선)**: C6 포팅 계약(customer_book_ledger_phase2.yaml)이
  Subu32 의 Edit107 을 `customer_code` 로 오독 — 그러나 Edit107 라벨은 전 트리
  공통 **'출판사명'** 이고 legacy Subu32 캡션은 '도서별수불원장'(거래처원장은
  Subu31). 레거시 정본은 전 빌드 공통 `S1_Ssub` **Gcode=거래처 / Hcode=출판사 /
  Bcode=도서**: 총판 Subu31 L283~305 `Gcode=Edit103 (+옵션 Hcode=Edit107)`,
  출판 Subu31 L404~406 `Gcode=거래처 and Hcode=Hnnnn(자사 강제)`. 이 오배선으로
  모던 거래처원장이 거래처 코드를 hcode 신원검사(`enforce_hcode_identity`)+
  `Hcode` SQL 축에 바인딩 → 격리 계정(교문사)은 무조건 403, 총판 계정도 잘못된
  축으로 조회(슈퍼 외 실사용 불능). [[slip-key-shared-and-binlog-recovery]]
  (전표키 공유)·DEC-136 실증(S1_Ssub Hcode=출판사코드 수십 개)과 정합.
- **교정 규칙**:
  - 원장 라우터(ledger/customer·customer-integrated): 거래처 식별자에 대한
    403 제거. 격리는 출판사 축 — `resolve_g7_ggeo_list_scope` 산출값(격리=자사
    강제/총판·슈퍼=None/신뢰불가=`SCOPE_DENIED`→자연 0건)을 서비스로 전달.
  - `customer_ledger_service`: 메인 WHERE `Gcode=거래처`(+격리 시 `Hcode=자사`),
    통합 원장 페이지네이션 축 `COUNT/DISTINCT/GROUP BY Hcode→Gcode`(응답 필드명
    hcode/hname 은 표시 키로 유지 — FE 호환), 이월 기준일(Sv_Ghng)·이월 잔량
    (Sb_Csum — Hcode 컬럼 보유 테넌트 한정, SHOW COLUMNS 어댑트)·거래처명
    (G1_Ggeo — 자사 행 우선) 모두 스코프 동반. `_build_filter_where` 에
    `has_gcode` 슬롯 신설(기존 호출자 무영향).
  - 도서별판매(`get_book_sales`): `_BOOK_SALES_MEASURE_KEYS`(입고/매입액/반품/
    폐기/증정/출고/출고액/폐기액) 전부 0 인 도서 행 제외 — 분기표 밖
    Gubun/Pubun(이동·변경 등)·수량 0 행이 만들던 전 컬럼 0 노이즈. 반품 등
    하나라도 비0 이면 유지(과도 제외 방지).
  - 프론트: 거래처원장 도서코드(시작/끝) 필터 제거(스냅샷 스키마 포함),
    도서별수불원장·재고현황·통합 도서수불장의 '거래처/지사' 오라벨 →
    '출판사코드'(`lookupKind="publisher"`). 메뉴: 재고관리+재고원장 그룹 통합
    (원장 4폼은 폼 단위 `menuId: NAV-03` 로 기존 매트릭스 게이트 유지),
    `INVENTORY_SIDEBAR_LAYOUT` 화이트리스트로 도서수불장·통합 도서수불장 감춤
    (레지스트리/라우트/등가 매트릭스 보존 — Sobo15 감춤 선례).
  - 감사 allowlist: `resolve_g7_ggeo_list_scope`/`_guard_distributor` 를
    `audit_router_hcode_coalesce` 허용 헬퍼에 등재 — 종전 outbound `/statement`·
    settlement `/publisher-contract` CRITICAL 2건도 동일 원인의 오탐으로 해소
    (라우터 감사 critical 0).
- **검증**: `test_dec137_ledger_axis_book_sales_menu.py` 12 PASS 신설(0권 제외
  2·단일/통합 축·SCOPE_DENIED 0건·라우터 배선 3·프론트 소스 가드 3). 기존 계약
  테스트 축 갱신: C6 25 PASS, dec084 param-order·ledger_sort·ledger_courier_scan
  (403→스코프 계약) 갱신 후 원장 계열 74 PASS. 전체 스위트 pre/post 실패 집합
  **완전 동일(기존 120건, 신규 회귀 0)**. tsc 0, eslint 신규 0(기존 21 오류
  잔존 — 미변경 파일). 도메인 hcode 감사 증감 없음(기존 critical 1·warn 3).
- **잔여(백로그)**: ① 거래처원장 그리드가 수불형(수량 흐름)으로 남아 있어
  레거시 Subu31(거래처거래원장 — 미수금/수금액형)과 화면 구성이 다름 — 미수금
  원장 별도 과제. ② `delphi_form_screen_matrix --check` 기존 FAIL
  (Sobo_author_history/Subu26_1 LEGACY_MISSING) 별도 정리. ③ 위러브 운영 계정의
  수불원장 '출판사코드' 필터는 비슈퍼 자사 강제(enforce_hcode_isolation) 정책
  유지 — 총판 실사용 피드백 시 재논의.
- **결정자**: 사용자 (2026-08-11 — 교문사-경리부 요청 전달)
- **참조**: [[DEC-136]](fail-closed·공유 좌표), DEC-090/085(총판 전체 합산
  보존), DEC-033(f)(동적 WHERE), DEC-084(Ocode 바인딩 순서), 총판/출판
  `Subu31.pas`·`Subu32.pas`(Edit107='출판사명'),
  `migration/contracts/customer_book_ledger_phase2.yaml`(축 주석 정정)

### DEC-136: 공유 DB 좌표 정산 스코프 fail-closed — 교문사 타사 자료 노출 교정 (2026-08-09)

- **보고**: 교문사-경리부 — 정산관리 하위 화면 값들이 "본인들 자료가 아니다".
- **원인(구조)**: `resolve_g7_ggeo_list_scope`(정산·출판사 lookup·통계 공용 스코프)가
  **T2_PUB / T3+chul_09 만 격리하고 나머지는 전체 합산(fail-open)**. 그런데
  remote_153 의 `chul_09_db` 는 **위러브3 + 교문사가 hcode 로만 구분해 공유**
  (welove-login-tenant-audit B3/B4, 위험도 높음). 교문사 계정의 account_type 이
  T3 가 아니면(미분류/T1/T2_DIST 오분류) 전체 스코프 → **위러브3 데이터가 그대로
  노출**. 로그인 인덱스에서 remote_153 에 로그인 ID '경리부'(hcode 5019,
  chul_09_db, family chul_09) 실재 확인 — 리포트 계정으로 추정.
- **레거시 정본**: 출판 빌드(도서유통-출판 Base01.pas)는 공유 테이블 전 쿼리에
  자사 Hcode(`Hnnnn`)를 강제 — 공유 DB 에서 전체 합산은 레거시에 존재하지 않는
  동작. DSN-DEC-12 fail-closed 원칙과 동일 계열.
- **교정 규칙**(`hcode_isolation.py`):
  - `_SHARED_DB_COORDS = {(remote_153, chul_09)}` — 이 좌표는 **계정 유형 불문**
    (슈퍼 제외) 본인 hcode 강제. `_SHARED_DB_SERVERS = {remote_153}` — 공유 서버
    에서 family 미상 로그인도 격리(어느 회사인지 모호).
  - **미분류**(account_type·family 모두 없음) 계정도 격리 — "모르면 전체" 폐기.
  - 격리 필요 + hcode 신뢰 불가(빈값) → `SCOPE_DENIED_HCODE`(실존 불가 sentinel,
    전 조회 0건) + audit 경고 로그 — 데이터 노출 대신 0건.
  - **보존**: 단일 테넌트 좌표의 운영(T1/T2_DIST) 전체 합산·T3 비 chul_09 전체·
    T2_PUB 본인 강제·슈퍼 전체 (DEC-085/090 동작, 위러브1/2 remote_154/155 포함).
  - 적용 면: settlement(16)·masters(11)·outbound(5)·stats(4) 라우터가 공유하는
    단일 리졸버라 정산 하위 화면 전체 + 출판사 lookup 이 일괄 교정.
- **잔여 리스크(백로그)**: ① `hcode='0000'` 은 `_is_super_ctx` 레거시 규약상 슈퍼
  (C10) — 공유 서버에 0000 로그인은 인덱스상 현재 없음(전수 2건 확인) 이나 규약
  자체는 별도 논의. ② book_07/book_11 은 DB명 공유·서버 좌표 분리라 제외 —
  hcode 격리 키 보강은 감사 리포트 장기 백로그. ③ '경리부' 계정의 account_type
  실값 정비(웹 가입 승인 row) 는 운영 조치 필요.
- **실증 보강(2026-08-09 #2, 라이브 읽기전용 프로브)**: remote_153 기본 DB=
  `chul_09_db`, `G7_Ggeo Gcode='5019' = (주)교문사` — 즉 chul_09_db@153 은 총판
  운영 DB 이고 **교문사는 그 총판의 정산 대상 출판사(포털형 계정)**. S1_Ssub 는
  출판사 hcode 수십 개(5019=153만 행 등), T2_Ssub 저장행은 5019 2행뿐. 2차
  스크린샷(청구서관리 57건 + 상세 403)은 배포 전 잔존 화면 — 57건 = 전 출판사
  파생 행 노출(사고 실체), 403 = 타사 행 상세를 기존 가드가 차단한 것. 배포 후
  scoped 재현: **2026.08 = (주)교문사 1행만(total 1)** — 사용자에게 재조회 안내.
  "붉은 박스만 남의 것" 지적은 클릭한 행 기준이었고 실제로는 자사 1행 외 전부
  타사였음.
- **검증**: `test_dec136_shared_db_scope_fail_closed.py` 10 PASS(공유 좌표 유형
  불문 격리·요청 필터 무시·hcode 부재 0건·미분류 fail-closed·DEC-085/090 보존
  매트릭스). 기존 스코프·정산 스위트 112 PASS(phase1 픽스처에 account_type=T1
  명시 — 미분류 모델은 이제 의도적으로 격리됨). 전체 스위트 pre/post 비교.
- **결정자**: 사용자 보고 → fail-closed 원칙 적용 (2026-08-09)
- **참조**: DSN-DEC-12(fail-closed), [[DEC-090]](운영 계정 전체 합산),
  [[DEC-085]], `docs/welove-login-tenant-audit-samples.md` B1~B4,
  도서유통-출판 `Base01.pas`(Hnnnn), [[settlement-domain-semantics]]

### DEC-135: 도서 검색 다이얼로그 '출고정지 제외' 옵션 — 계정별 기억 (2026-08-09)

- **요청**: 도서 검색 창에서 출고정지 도서를 목록에서 제외하는 옵션 + 사용자
  선택 기억.
- **정본**: 출고정지 = **G4_Book.Grat9**(레거시 Sobo14.CheckBox2, 도서 마스터
  편집 폼과 동일 필드). 백엔드는 도서 마스터 목록에 이미 있던
  `excludeShippingStop`(`IFNULL(Grat9,'') NOT IN ('1','True','true')`) 재사용 —
  신규 SQL 0.
- **구현**: `MasterLookupConfig.filterOption`(범용 선택형 필터 슬롯) 신설 —
  book kind 에 "출고정지 제외" 체크박스. 기억 = `mlf_book_exclude_stop_v1:{serverId}`
  localStorage(계정별). 열 때 저장값을 읽어 **첫 검색 호출에 직접 전달**(setState
  반영 지연으로 첫 검색이 필터 없이 나가는 레이스 방지), 토글 시 즉시 재검색.
  **강제 아님** — 반품 입력/마스터 편집 등 정지 도서가 필요한 업무 보존(인라인
  자동완성에는 미적용, 다이얼로그 전용).
- **검증**: `test_dec135_book_lookup_exclude_stop.py` 7 PASS(설정·파라미터
  패스스루·계정별 영속·오픈 레이스 방지·토글 재검색·백엔드 절). tsc 0·eslint 0.
- **결정자**: 사용자 (2026-08-09)
- **참조**: [[DEC-134]](다이얼로그 공용), Sobo14.CheckBox2, `masters_service.list_books`

### DEC-134: 검색 Enter 확정 최종형 — 다건 정확코드 자동확정 제거(한글 단어형 코드) + 신규 컬럼 기본위치 삽입 (2026-08-09)

- **3차 보고(2026-08-08 밤)**: 새 번들에서도 "기계" Enter 임의선택 재현 스크린샷 —
  드롭다운에 **도서코드가 한글 단어**("축산기계"/"기계화"/"기계설비"/"기계2011"…)인
  테넌트로 확인. 검색어 "기계"가 **실존 도서코드와 정확 일치**(= "기계산업마케팅총람
  2009")해, 남겨두었던 "코드 정확 일치 → 자동확정"(레거시 Seek 동등) 규칙이 다건
  결과에서도 발동한 것이 진짜 뿌리 원인. DEC-133 의 낡은 번들 진단도 사실이나
  (7/30 주문일자 단서) 이 케이스는 새 번들에서도 재현되는 게 맞았다.
  jsdom 시뮬 red/green: 구코드 `onInlineSelect:기계산업마케팅총람` / 신코드 팝업.
- **규칙 최종형**: 자동확정 = **결과 정확히 1건 + (코드 일치/접두 또는 명칭 정확
  일치)**일 때만. 다건은 정확 코드 일치가 있어도 **검색 팝업**(키워드 시드) — 단,
  팝업이 **정확 일치 행을 우선 강조**해 의도적 전체 코드 입력자는 Enter 한 번만
  추가(같은 키워드 재-Enter 확정 흐름). 숫자 코드 테넌트의 단건 고속 입력은 불변.
- **정가 컬럼 위치(같은 날 요청)**: 도서별판매 '정가'가 저장된 컬럼 순서가 있는
  계정에서 맨 끝으로 밀림 — `useGridPrefs.applyOrder` 가 순서 미지정(신설) 컬럼을
  末尾 append 하던 것을 **기본 정의 위치 삽입**(직전 컬럼 뒤)으로 교정. 전 그리드
  공통 개선(저장 순서 자체는 보존), '정가'는 도서명 다음에 등장.
- **검증**: `test_dec134_lookup_confirm_and_column_insert.py` 9 PASS(다건 정확코드
  픽 제거·1건 조건 유지·팝업 정확행 강조·applyOrder 파이썬 미러 4종·TS 소스 가드).
  jsdom 실컴포넌트 시뮬 red/green. tsc 0·eslint 0.
- **결정자**: 사용자 (2026-08-08/09 — "선택하지 않았으면 검색화면" 규칙 명시)
- **참조**: [[DEC-133]](진단 3계층), [[DEC-132]](A1), Subu27 라인 그리드,
  `master-lookup-field.tsx` confirmEnter / `use-grid-prefs.ts` applyOrder

### DEC-133: 낡은 번들 진단 규약 + 새 배포 감지 배너 (2026-08-08)

- **보고**: "도서코드 '기계' Enter 임의선택(7/31 수정분)이 여전히 재현된다" —
  스크린샷 재현 포함 재수정 요청.
- **진단(3중 검증 — 코드/번들/클라이언트 구분)**:
  ① 코드: jsdom+esbuild 실컴포넌트 시뮬(모킹: outbound-api/auth/dialog) —
  "기계" 타이핑+무방향키 Enter → **검색 팝업 열림(seed=기계), 임의선택 없음**.
  ② 프로덕션 번들: `/outbound/orders/new` HTML 의 청크 24개 다운로드,
  MLF 마커("결과 없음 — Enter 로 검색 팝업") 청크에서 수정 로직의 minified
  시그니처 `(r&&r.startsWith(t)||i&&i===t)&&(o=0)` 확인 — 수정 전 파일은
  startsWith 0회. 배포본 정상.
  ③ 클라이언트: 8/8 스크린샷의 주문일자가 여전히 **2026.07.30**(신규 화면 기본값은
  당일) — 워크스페이스 창(iframe)이 7/30 부터 열려 있던 **수정 이전 번들** 실행 중.
  창(iframe)은 다시 열 때만 새 번들을 받는다.
- **재발 방지**: `NewVersionBanner`(셸 전용, embed 분기 제외) — 빌드 스탬프
  `public/version.json`(`scripts/write-version.mjs`, package.json prebuild 훅,
  gitignore) 을 부팅 기준으로 창 포커스+10분 폴링, 변경 감지 시 "새 버전 배포 —
  지금 새로고침" 배너. **자동 리로드 금지**(입력 중 데이터 보호), version.json
  부재(로컬 dev)·오류는 fail-silent.
- **부수 발견**: ⚠ `frontend/.git` **중첩 저장소 잔재**(2026-04-17 initial,
  create-next-app git init 추정 + 7/21 커밋 1건) — 제품 저장소가 frontend 파일을
  정상 추적하므로 배포 무영향이나, frontend/ 안에서 실행되는 스크립트의
  `git rev-parse` 를 가로챈다(버전 스크립트는 VERCEL_GIT_COMMIT_SHA 우선으로 회피).
  제거 여부는 사용자 결정 대기.
- **검증**: `test_dec133_new_version_banner.py` 6 PASS(prebuild 배선·no-store 폴링·
  자동리로드 금지·셸 전용 마운트·MLF Enter 가드 앵커). tsc 0, eslint 신규 0
  (layout 기존 1건 stash 대조 동일).
- **결정자**: 사용자 보고 → 진단 후 재발 방지 장치 (2026-08-08)
- **참조**: [[DEC-132]](A1 원 수정), [[prod-deploy-gap-and-suite-flakes]](배포본≠
  로컬 HEAD 계열 — 본 건은 "배포본≠**클라이언트 실행본**" 신규 유형), Vercel
  청크 정적 검증 절차(스크래치 chunks grep)

### DEC-132: 영업팀 의견 1차 반영(A 배치) — 도서별판매 오라벨 교정·검색 팝업 클릭 확정·단일 코드 필터 (2026-08-03)

- **요청**: 영업팀(북이오웍스) 수정의견(2026-07-31 접수, `docs/sales-team-feedback-plan-2026-07-31.md`)
  중 표준 티어 A3→A1→A2/A4 진행 승인(2026-08-03 사용자).
- **A3 오라벨 교정(핵심 발견)**: 레거시 Subu61.dfm 그리드 캡션 정본 대조 결과 웹
  도서별판매의 **gjqut "재고수"(stats/book "잔량")는 오라벨 — GJQUT=증정수량**이며
  백엔드 `_apply_book_sales_branch` 도 증정(Pubun='증정')을 gjqut 에 누적한다.
  영업팀이 신규 요청한 "증정수"는 라벨 정정만으로 충족. 함께 **gpqut "파지수"→
  "폐기수"(레거시 캡션 폐기수량), gpsum "파지액"→"폐기액"** 정정, 컬럼 순서도
  레거시(입고→출고→증정→반품→폐기)로 정렬. 화면 2곳(reports/book-sales,
  stats/book) + XLSX `_BOOK_SALES_EXPORT_COLUMNS` 동시 반영. ⚠ 수불원장
  (inventory/ledger)의 "재고수/파지수"는 수불 누적 도메인의 정당 라벨 — 미변경.
- **A1**: 검색 팝업(master-lookup-dialog) 행 **단일 클릭 = 즉시 확정**(DataGrid
  기존 onRowClick 활용). 키보드 흐름(↓/Enter/같은 키워드 재-Enter 확정) 불변,
  [선택] 버튼은 Q2(제거 여부) 회신까지 유지.
- **A2/A4 단일 코드 필터**: 도서별판매 "도서코드 시작/끝" → **도서 검색 1개 +
  "전체" 체크박스**(거래처판매 동형). 백엔드 `get_book_sales(bcode=)` /
  `get_customer_sales(gcode=)` 단일 필터 신설 — **지정 시 range 보다 우선**,
  기존 bcodeFrom/To·gcodeFrom/To 는 수불장 등 공유 호출자 호환으로 유지.
  Sg_Csum 후처리도 동일 필터. 라우터·XLSX 4곳 패스스루. 프론트: 입력/선택 시
  "전체" 자동 해제, "전체" 체크 시 코드 클리어, 체크박스 Enter 스톱 편입
  (DEC-116, `Sobo61.Chk_AllBooks`/`Sobo62.Chk_AllCustomers`), 세션 스냅
  bcode/bookAll·gcode/customerAll 로 이행(구 range 스냅 무시, 기본 전체).
- **검증**: `test_sales_team_a_batch.py` 신설 10 PASS(단일 필터 SQL·range 우선순위·
  라벨 정적·클릭 확정 정적). tsc 0·eslint 0. 전체 스위트 pre/post 비교 —
  신규 실패 0건(116건 동일, 차이는 기존 flaky 1건의 출력 포맷). 배포 (제품 커밋).
- **후속(승인 대기)**: B1(기간 전체 거래 내역+우측 상세 — 출판 변형 Subu61 분석
  선행), B2(본사/창고/재고합계 — Q1 재고 정의 회신 필요), Q2/Q3.
- **결정자**: 사용자 (2026-08-03)
- **참조**: `docs/sales-team-feedback-plan-2026-07-31.md`, [[DEC-116]](체크박스 스톱),
  DEC-068(D)(그리드 정렬), Subu61.dfm 632~702(그리드 캡션 정본)

### DEC-131: 청구서 확정 체크(T2.Yesno='1') 보존 — 쓰기·가드 키 월키 정규화 전환 (2026-07-30)

- **보고(2026-07-30 사용자)**: 총판(물류) 청구서관리의 "명세표를 수정해도 청구서 금액이
  변경되지 않도록 하는 확인 체크박스"의 체크 정보가 웹 포팅 후 날아가는 것 같다 —
  레거시 상태를 훼손하지 않도록 레거시 코드 확인 후 보완 지시.
- **정본 해석**(WeLove_FTP/도서유통-New/Subu45.pas): 해당 체크박스 = 상세 패널
  **CheckBox1 ↔ T2_Ssub.Yesno='1'**(dfm 캡션은 '출판사Show' 로 오기돼 있으나 기능은 확정).
  ① 행 더블클릭(DBGrid101DblClick L3807~)이 T2.Yesno='1' 이면 체크 + **재계산
  (Button811 출고내역/812 발송비) 전부 스킵** — 저장자료(Button803)만 로드. 인쇄
  (Button016 L460~)도 체크 시 재계산 스킵. ② 저장(Button301) 시 체크면 T2.Yesno='1'
  (미체크 '') + **T3 전 라인 Yesno='1' 잠금**(L2916~/2958~, 미체크는 라인별 기존값 유지).
  ③ 일자 그리드 '저장' 체크 컬럼 = T3.Yesno 라인 잠금, 재계산 루틴은 `Yesno<>'1'` 만
  갱신(L840/979/1051/1231/1501).
- **웹 결함(구조 원인)**: DEC-091 이 "쓰기 키는 원시 'YYYYMM' 정확 매칭(레거시 행
  오매칭 회피)"로 정했으나, DEC-129 자동 집계의 T2/T3 DELETE 는 **정규화 월키**로
  레거시 점 표기('2026.07') 행까지 지우는 반면 **마감 가드(_SQL_CHECK_YESNO)만 원시
  키 + LIMIT 1** 이라 레거시 확정 행·중복 행(T2 유니크 키 부재, DEC-127a)을 못 봄 —
  확정 월의 T3 라인이 웹 재집계로 재구성(=확정 청구서 금액 변경). 부수 결함:
  ① 091d9ce(2026-07-25 자동집계 최초판)는 T3 DELETE 에 잠금 가드 자체가 없어 배포
  구간에 열람된 월의 잠금 라인이 실제 삭제됨(bb35cab 에서 가드 추가). ② 수동 lines
  집계 경로 `LEFT(Gdate,6)` DELETE(점 표기 불일치로 사문) + 무가드 UPSERT(유니크 키
  부재로 매 호출 중복 '0' 헤더 삽입). ③ confirm/cancel 원시 키 UPDATE — 레거시 행만
  있는 월에서 0행 갱신(웹은 확정으로 알고 레거시는 미확정으로 재계산). ④ recalc
  ON DUPLICATE KEY 무력(중복 삽입) + 대상 조회 원시 키(레거시 확정을 closed_set 에서
  누락). ⑤ 상세 헤더 LIMIT 1 임의 행 — 미확정 중복 행 반환 시 프론트 자동집계 게이트
  (yesno=='0') 관통. ⑥ tax_invoice Chek3/Sdate UPDATE 원시 키(레거시 행 무음 no-op).
- **교정(정책 전환)**: 쓰기·가드도 월키 정규화하되 **Yesno='1'(확정 헤더·잠금 라인)은
  어떤 경로도 삭제/갱신 금지**를 SQL 에 내장(fail-closed):
  - `_SQL_CHECK_YESNO` 정규화 + LIMIT 제거, `assert_period_open` = 전 행 중 '1' 존재
    시 423(`_yesno_states` — 레거시 '' 는 '0' 정규화).
  - 공용 상수 `_SQL_DELETE_T2_UNCONFIRMED`/`_SQL_DELETE_T3_UNLOCKED`(`<> '1'` 가드)/
    `_SQL_SELECT_T3_LOCKED_GDATES` — 자동·수동 집계 공용. 수동 경로도 잠금 일자
    재삽입 스킵. 잠금 조회 실패 시 전량 재구성하던 fail-open 제거(전파).
  - `confirm_billing` = 레거시 Button301 체크 저장 동등: T2 '1'(월 전체) +
    **T3 전 라인 잠금**(`_SQL_CONFIRM_LOCK_LINES`). cancel 도 정규화 키.
  - `recalc_billing`: 대상 조회 정규화, 기존 헤더는 UPDATE(`<> '1'` 가드)·미존재만
    INSERT — 중복 삽입 제거.
  - 상세 헤더 `ORDER BY IF(IFNULL(Yesno,'0')='1',0,1)` — 확정 행 우선(목록 dedupe 와
    동일 우선순위). tax_invoice Chek3/Sdate UPDATE 월키 정규화.
- **데이터 복구 백로그**: 091d9ce~bb35cab 배포 구간에 웹에서 열람된 (월,출판사)의
  T3 잠금 라인 삭제분은 코드로 복구 불가 — 필요 시 binlog 복원(DEC-080 절차) 검토.
  T2 확정('1') 헤더는 전 기간 DELETE 가드가 있어 코드상 삭제된 적 없음.
- **검증**: `test_dec131_billing_confirm_check_preserved.py` 신설 12 PASS(점 표기
  확정 감지·중복 행 전수 검사·수동집계 잠금 보존·확정 라인 잠금·recalc 중복 방지·
  상세 확정 우선). `test_dec091_settlement_normalization.py` WriteKeysStayRaw →
  WriteKeysNormalized 로 정책 갱신. settlement/billing/cash 계열 141 PASS(기존 실패
  1건=계약 버전 정적 검사, 무관). 정적 감사 critical 은 pre/post 동일(기존 2건).
- **결정자**: 사용자 (2026-07-30)
- **참조**: [[DEC-129]]⑥(일자 잠금), [[DEC-127a]](T2 중복·dedupe), [[DEC-091]](월키
  정규화 — 쓰기 키 원시 정책 본 DEC 로 폐기), DEC-031(마감 가드), DEC-080(binlog 복원),
  Subu45.pas DBGrid101DblClick/Button301/Button016/Button821

### DEC-130: 날짜 수기입력 한자리 인식 교정 — DateFieldYMD emit 에코 클로버 (2026-07-27)

- **증상(2026-07-26 사용자)**: 통계관리 도서별판매/거래처별판매 종료일 수기 입력 시
  `2026. 06. 30` → `2026.01.01` 류(월/일 첫 자리만 인식). 전수 조사 결과 개별 화면이 아니라
  **`date-field-ymd.tsx` 공용 컴포넌트 결함 — 사용 화면 48개 전부 해당**(네이티브 date input
  잔존 0). 필터 기본값이 채워진 날짜에서만 발현(빈 값 신규 입력은 emit 조건 미충족으로 잠복,
  DEC-115 도입 이후 미발견 사유). jsdom 키입력 시뮬 재현: `2026. 06. 30` → `2026-01-03`,
  12월 `12` → `01`.
- **원인 3연쇄**: ① `emit()` 이 세그먼트 1자리 시점부터 부분 입력을 정규화("0"→clamp→"01")해
  부모로 올림 → ② 부모 value **에코**를 동기화 useEffect 가 세그먼트 state 에 되씀("0"→"01")
  → ③ 다음 키가 `onlyDigits` slice(0,2) 에서 잘림("016"→"01" — 두 번째 자리 소실).
- **교정(공용 1곳)**: (A) `segsRef` 미러 + `composeEmitted(segsRef.current) === value` 이면
  동기화 스킵 — 자기 emit 에코만 무시, 외부 변경(달력 선택/세션 복원/부모 리셋)은 기존대로
  동기화. (B) blur 표시 정규화 `normalizeSeg`("6"→"06", "13"→"12") 신설 — 단 **이벤트 대상
  DOM 값(`e.currentTarget.value`)을 읽어야 함**: 월 2자리 완성 자동이동(월→일 focus)이
  onChange 와 같은 이벤트에서 blur 를 동기 발생시켜 state 클로저는 한 키 이전 값("0")이라
  클로저 판 1차 수정은 같은 함정으로 실패(시뮬로 검출 후 재수정).
- **검증**: 실컴포넌트 jsdom 키입력 시뮬 red/green — HEAD 재현 FAIL(01-03) → 수정 후
  `2026-06-30`·`2026-12-30`·blur "6"→"06" 3종 PASS. tsc 0, eslint 0. 회귀 가드
  `test/test_date_field_ymd_manual_typing_guard.py` 10 PASS(에코 스킵 존재·미러 선언 순서·
  blur DOM 값 시그니처 정적 가드 + composeEmitted 파이썬 미러).
- **결정자**: 사용자 증상 보고 → 원인 확정 후 즉시 교정 (2026-07-27)
- **참조**: [[DEC-115]](DateFieldYMD 3분할 도입), [[keyboard-input-flow]],
  `도서물류관리프로그램/frontend/src/components/shared/date-field-ymd.tsx`

### DEC-128: 청구서 양식 인쇄 — 레거시 Subu45 일자그리드+4-카테고리 요율 계산 완전 포팅

- **요청**(2026-07-24 사용자): 청구서관리에서 레거시 청구서 인쇄물(첨부 이미지, 0013 2026.07)
  과 동일한 **청구서 출력**. 해당 값으로 구현·검증까지.
- **정본 해석**(WeLove_FTP/도서유통-New/Subu45.pas — 4,896줄 전수 분석):
  - **T2_Ssub = Sum01~Sum69 전체 청구패널 저장 테이블**. ⚠ **Sum26=전월미수, Sum27=당월청구,
    Sum28=VAT, Sum29=월말재고, Sum30=총합계, Sum61=종수** — 웹 C5 목록의 sum26/27/28
    ("당월/세액/합계") 해석과 **한 칸 어긋남**(후속 정정 백로그). 인쇄는 정확 매핑 사용.
  - **요율(계약) = G7_Ggeo 출판사 마스터의 Sum02~Sum68/Yes33~62/Bigo1** (Button902):
    Sum02/04=기본부수·월정료, Sum06=초과단가, Sum09=지방직송, Sum12/15=보호대/박스 단가,
    Sum18/19=입출고 월정, Sum22=입출고 초과, Sum25=거래명세표 발행(>1000 분기), Sum34=재고
    보관단가, Sum43/44/45=해체/시내수거/지방수거, Sum46=적재공간, Sum62=종당, Sum64=전산
    프로그램, Sum68=기타, Yes35=VAT 적용, Yesno=종수 산정 모드(1=G4 Yesno True, 2=G4 전체,
    4=당월 DISTINCT Bcode…), Bigo1=비고.
  - **일자 그리드**(Button821/812): S1(월범위, Gubun='출고', Ocode='B', **Scode 소스는 'Z'
    이나 실데이터 전부 'X' → IN('X','Z') 흡수**, Gcode≠'00002', Gjisa≠'방문출고'), 슬립=
    (일,Gcode,Jubun,Gjisa), **0부 전표 제외**(15일 검증). 시내/지방=**G1_Ggeo.Gubun 폴백체인**
    (Hcode='' 행의 01/02 우선→출판사행 — 영풍문고 케이스). 보호대/박스=**T4_Ssub 슬립 매칭**
    (Gqut2/Gqut3, 소스는 'z'+Hcode Locate 이나 실데이터 무접두 → 둘 다 조회), **비매칭 슬립
    보호대+2**. 반품수거=T6_Ssub Gqut1/2. 반품해체=S1 **Bdate** 기준 음수. 발송비=T1_Ssub
    (일자별 첫 행 서점/지역/화물명, 건수=행수, ΣGssum).
  - **합계식**(Edit201Exit): 당월청구=Σ23항목, VAT=당월/10(정수 절사), 총합계=전월미수+당월+
    VAT. 전월입금/미수(Button905)=전월 T2(Sum26+27+28)−ΣT5(Sdate=전월). 재고(레거시
    Sv_Ghng 누적의 실용 등가)=전월 T2.Sum29+당월입고−출고+수거반품(0013: 8,110+5−144+1=7,972 ✓).
- **테넌트 함정 재확인(DEC-095)**: 한국도서유통 테넌트 DB=**book_kb_db**(remote_138 기본
  chul_09_db 아님) — 프로브는 반드시 테넌트 DB 컨텍스트로.
- **구현**: `settlement_service.billing_invoice`+`compute_invoice_totals`(순수 골든 함수),
  `GET /settlement/billing/{key}/invoice`(_guard_billing_hcode), 프론트
  `/settlement/billing/[key]/invoice` A4 재현+window.print, 청구서관리 [청구서 양식] 버튼.
- **피드백 반영(2026-07-25)**: ① 13·20일 시내 오분류 — G1.Gubun 에 01/02 없는 거래처
  (영풍문고 00023)는 **T1_Gbun.Gname('시내'/'지방') 2차 폴백**(''행 우선, 레거시 Locate 체인
  등가)으로 판정. ② 재고 기본/초과 관리비 항목 추가(stock_base/stock_over, G7 Sum38/41/42) +
  도서종당 관리비를 물류 파트 위치로. ③ 사용자 참고 이미지 기반 블루 테마 리디자인(수신처
  정보바·출고내역 좁게/발송비내역 넓게·01~04 섹션·입금계좌) + **발행자 메모 편집**
  (localStorage `portal_invoice_issuer_v1:{serverId}`). 제품 3c6b5c0.
- **HOTFIX(2026-07-25 #2, '청구서 생성이 안된다')**: 실제 막힌 곳은 invoice 가 아니라
  **행 선택 시 상세 500**(book_kb_db T3_Ssub 에 `Idx` 없음)과 **기존 [인쇄] 500**(G7 에
  `Bname/Gadd1/Gadd2` 없음) — DDL drift 1054. `table_columns`(SHOW COLUMNS 캐시, **키에
  테넌트 DB 포함** — 기존 `_t2_columns` 의 서버 단위 캐시는 DEC-095 오염 소지) 신설,
  T3 라인/G7 수신처 SELECT 를 존재 컬럼 기반 빌더로. 라이브: 상세·인쇄·양식 3종 OK,
  브라우저에서 13일 시내 1·청구서 양식 렌더 확인. 제품 99441ae.
- **검증**: 골든(실인쇄물 0013 2026.07, 22일 컷 실측 수량): **당월 491,864 / V.A.T 49,186 /
  합계 541,050 / 전월입금 557,777 / 미수 0 — 정확 일치**. `test_billing_invoice` 5/5
  (골든식·VAT미적용·초과부수·그리드 규칙(0부 제외/G1 폴백/T4 매칭)·검증오류), 라이브 서비스
  호출(book_kb_db) 동작. next build 라우트 생성 ✓. 배포 `eed5d37`.
- **결정자**: 사용자 (2026-07-24)
- **참조**: [[DEC-127]](청구 목록 파생), [[settlement-domain-semantics]], DEC-095(테넌트 DB),
  DEC-033(IN 청크/IFNULL), `Subu45.pas` Button821/812/601/602/902/905/Edit201Exit

### DEC-129: 청구서관리 레거시 완전 재현 2차 — 자동집계·월바·상세패널·계약편집·메모장·일자잠금

- **요청(2026-07-25 사용자, 6건)**: ① 출판사 선택 시 자동 집계, ② 하단 1~12월 선택 버튼,
  ③ 하단 상세 계산 패널(보이기) + 출판사별 기본값 편집·저장, ④ 출판사관리(총판)에 4-계약
  섹션, ⑤ 계약내용 메모장(레거시 데이터 존재), ⑥ 일자별 '저장' 체크박스, ⑦ 우측 상세 sticky.
- **①자동 집계**: `aggregate_billing(lines=[])` 를 "빈 라인+0 헤더"(구 Phase1 단순화 — 목록
  '부수 0' 저장의 원인)에서 **`billing_invoice` 정본 계산 기반 재구성**으로 교체. T2 헤더는
  DEC-128 정확 매핑(Sum01/26/27/28/29/30/61)으로 DELETE+INSERT(중복 정리), T3 일자 라인
  재구성(컬럼: Gqut1=시내/2=지방/3=박스/4=보호대/5=해체/6=수거시내/7=수거지방, Idx 유무 분기).
  프론트 행 선택(클릭/Enter/월전환/첫행) 시 미집계(404)·라인0(임시)이면 자동 실행 — 확정/취소
  월 불변. 라이브: 0013 중복 2행→1행, Sum27=492,395.
- **③④출판사 계약**: `GET/PUT /settlement/publisher-contract`(총판 게이트, 컬럼 어댑터) —
  **Yes33~62 청구/미청구 플래그 전체 해석**(Button902 두번째 SELECT cells[0..20] 매핑, '1'=청구
  '2'=미청구, 0013 라디오 실화면 대조). `compute_invoice_totals(flags=)` 통합 — 미청구 항목
  금액 0(골든 불변). 공용 `PublisherContractEditor`(4그룹×수량·금액+라디오+비고+메모장) —
  청구서관리 하단 `BillingCalcPanel`(집계표+합계+에디터, 저장 시 자동 재집계)과
  출판사관리(/master/publisher, isDistributorViewer 게이트) 양쪽 사용.
- **⑤메모장**: `G7_Ggeo.Memos` = **레거시 TRichEdit RTF(cp949 \'xx)** — `rtf_memo.py`
  파서/생성기(라운드트립 가드, 0013 실데이터 529자 파싱 검증, ⚠ `\pard` 를 `\par` 보다
  먼저 제거해야 'd' 잔여물 없음). 웹은 플레인 편집, 저장 시 레거시 호환 RTF 재인코딩 +
  `Gmemo`(수정시각) 갱신.
- **⑥일자 잠금**: 레거시 '저장' 체크박스 = **T3.Yesno='1' 잠금**(Button821 `Yesno<>'1'` 갱신
  스킵 동등). 자동 집계의 T3 DELETE/INSERT 모두 잠금 라인 보존, 상세 그리드 '저장' 체크 토글
  (`POST /billing/{key}/line-lock`, 확정월 423).
- **②⑦**: 청구 라인 하단 월 선택 바(선택 출판사 유지 preferHcode) + 우측 패널
  `lg:sticky top-0 self-start`(DEC-125 패턴).
- **검증**: settlement 계열 126 PASS(선재 1 무관), tsc 0·eslint 0·next build 112 페이지,
  라이브(자동집계/계약/메모/병합) + 브라우저(자동집계 상세·월바·잠금 체크·sticky) 확인.
  배포 `091d9ce`/`bb35cab`.
- **후속(2026-07-25 #2)**: ⑧ 목록 라벨 정정 — "부수/세액/합계금액"→"전월미수/당월청구/
  부가세"+합계금액(26+27+28 합성, 정렬 지원). 파생 행 sum 배치도 T2 와 통일(sum26=0/
  sum27=당월/sum28=VAT) — 아래 '한계' 해소. ⑨ 메모장 HTML 리치 편집기 — `rtf_to_html/
  html_to_rtf`(b/i/u/br, cp949) + contentEditable 편집기(B/I/U 툴바), PUT memoHtml 우선.
  `test_rtf_memo` 7/7(레거시 \pard 경계·볼드·라운드트립·contentEditable div). 제품 해당 커밋.
- **한계(백로그)**: 목록 컬럼 라벨 "부수/세액/합계금액"은 실제 Sum26=미수/27=당월/28=VAT 와
  어긋남(DEC-128 발견) — 자동집계 후 목록 '부수 0' 으로 보이는 원인. 라벨 정정 별도.
- **결정자**: 사용자 (2026-07-25)
- **참조**: [[DEC-128]], [[DEC-127a]], `rtf_memo.py`, `publisher-contract-editor.tsx`,
  `billing-calc-panel.tsx`, Subu45.pas Button821/902/903/905

### DEC-127a: 부분 집계 월 병합 — total==0 전면 게이트 결함 교정 (2026-07-25)

- **증상**: 예방의학사(0013) 하나를 [집계]한 순간 7월 조회가 그 1건만 반환("7월 출판사
  조회가 예방의학사만") — DEC-127 의 `total==0` 전면 게이트가 월 단위 all-or-nothing 이라
  한 출판사 집계로 나머지 152개 파생이 전부 꺼지는 결함.
- **교정**: `list_billing` 을 **(월,출판사) 키 단위 병합**으로 — T2 저장행 전량(범위 내) +
  T2 에 없는 키만 파생(`_derive_billing_rows`), 집계행 항상 우선, 취소행 키는 유지(파생
  부활 방지), 병합 후 파이썬 정렬·슬라이스. **T2 (gdate,hcode) 표시 dedupe** 추가 —
  T2_Ssub 에 유니크 키가 없어 [집계] 재클릭 시 동일 키 행 중복 삽입(book_kb 0013 실사례,
  id 36111/36112 전부 0값): 확정('1') 우선, 그 외 최신 행. ⚠ 쓰기 경로(aggregate/recalc 의
  ON DUPLICATE KEY)는 유니크 인덱스 부재 시 무력 — 중복 삽입 방지는 후속 백로그.
- **부수(2026-07-25 사용자)**: 청구서관리 Enter 흐름에 취소포함/종료숨김 체크박스 스톱 편입
  (Sobo45.Check101/102, DEC-116 규약 — 콤보 선택 후 포커스가 체크박스로 가 멈추던 문제),
  구 Sobo46 [인쇄] 버튼 제거·[청구서 양식]→[청구서 인쇄], 종료 출판사 숨기기 체크박스,
  청구서 서식 반품수거 폭 −50%·발송비 내역 셀 확대. 브라우저: Enter 연타→조회 실행,
  7월 153건(집계 1 + 파생 152, 중복 제거) 확인. 제품 97ae2a0/cb2c475.
- **참조**: [[DEC-127]], [[DEC-116]](체크박스 스톱), `_derive_billing_rows`/`list_billing`

### DEC-127: 청구서관리 목록 실시간 파생 — 미집계 월도 총판이 '열면 바로' 조회

- **요청**(2026-07-24 사용자): 레거시 발송비/입금 메뉴의 **청구서관리**를 총판(물류) 로그인에서
  사용 가능하게. **조사 결과**: 웹 청구서관리(`Sobo45_billing`, `/settlement/billing`)는 이미
  총판 정산관리 메뉴에 노출·동작하며 스코프도 정상(`resolve_publisher_row_scope` → 총판=전체
  교차뷰). **실제 문제 = 미집계 월 "조회 결과 0건"**: 웹 목록은 사전집계 `T2_Ssub` 만 읽는데
  레거시는 출고−반품 실시간 계산이라 데이터가 보였던 것.
- **결정(사용자 택1)**: **실시간 파생**(레거시 일치). `list_billing` 이 T2 미집계(total=0)면
  `_derive_billing_list` 로 (월,출판사)별 청구를 출고(S1)−반품(R3)에서 **읽기전용 파생** —
  `Sum26=출고Gssum−반품Gssum`, `Sum27=round(×0.1)`, `Sum28=합계`, `Yesno='0'`(임시). recalc_billing
  공식과 자기일관(집계 시 나올 값과 동일). **DEC-091 함정 회피**: Yesno 필터 없음(S1 '2'=완료·
  DEC-081), 월키 정규화(`LEFT(REPLACE…,6)` 점표기 흡수), R3_Ssub 부재 서버 반품 0 폴백. 집계된
  월(total>0)은 기존 T2 경로 유지(파생 미개입 — 확정/조정 데이터 보존). 정렬 월desc·출판사asc,
  페이지네이션 파이썬 슬라이스(파생 결과셋 소규모).
- **경계(현 스코프)**: 목록은 파생되지만 **상세(우측 일자별 14컬럼)** 는 T3_Ssub 라인 의존이라
  미집계 월은 여전히 "[집계]로 재구성" 안내. 총판이 행 선택 후 [집계]/[월 일괄 재집계]로 T2·T3
  생성. (관측: 집계월 2026.06 상세가 500 — 별도 선재 이슈, 본 변경과 무관.) 웹 청구는 발송비
  기반 간소 모델(레거시 4-카테고리 배송/물류/반품/기타 요율계산 아님) — 기존 C5 한계 유지.
- **검증·배포**: `test_billing_live_derive` 4/4(공식·정렬·R3부재·빈원천), 기존 settlement 115 PASS
  (선재 실패 1건 `test_c7_print` PDF계약=무관). 브라우저: 총판 2026.07 미집계월 **0건→153건(임시)**
  (예: 도서출판 소동 14,822,860). 배포 `2c6960e`.
- **결정자**: 사용자 (2026-07-24)
- **참조**: [[DEC-085]]/[[settlement-domain-semantics]](정산 월키·조회0건 트리오), DEC-091(Yesno제거·
  월키정규화), DEC-081(출고 Yesno='2'=완료), `settlement_service._derive_billing_list`

### DEC-126: 출고내역서 키보드 자동조회 + 조회 성능 최적화 + 종료 출판사 숨김

- **요청**(2026-07-24 사용자): ① 출고내역서 좌측 목록을 키보드로 이동하면 클릭처럼 조회,
  ② 조회 쿼리 속도 최적화 검토, ③ 현황판에서 "종료" 출판사 숨김 옵션.
- **①키보드 자동조회**: 좌측 목록 `onSelectedRowChange`(화살표 이동)에서 **디바운스(250ms)**
  후 `selectPublisher` 호출(홀드로 매행 조회 폭주 방지), 클릭은 즉시. **요청 시퀀싱**
  (`reqSeqRef` — 느린 응답 도착 순서역전 시 최신 선택만 반영) + **(date\|hcode) 결과 캐시**
  (재선택 왕복 0). 날짜 변경 시 캐시 무효화.
- **②성능 진단**(브라우저 resource timing + 백엔드 per-query 타이밍): distributor-board
  median 363ms(빠름), outbound_statement median 2.4s·max 9.5s로 느려 보였으나 **웜 쿼리는
  130~220ms**(Q1 S1=39~140ms, Q2 T4~30ms, Q3 G1~40ms). 2.4s+ 는 전부 **연결 풀 콜드스타트**
  (uvicorn 리로드/유휴 후 aiomysql 풀 재생성 + SSH 터널 핸드셰이크 ~0.7~6s). 즉 병목은 쿼리가
  아니라 콜드 연결. **코드 레벨 최적화**: (a) `outbound_statement` Q1(수량)·Q2(포장) 병렬화
  (`asyncio.gather`, (Gdate,Hcode)만 의존). (b) `_g1_names_and_region` Q3 `OR-of-ANDs
  (Gcode=A AND (Hcode=H OR '')) OR …` → `Gcode IN (…) AND (Hcode=H OR '')` 등가 재작성
  (거래처 많은 출판사 조건폭발/인덱스미사용 해소). (c) 출고내역서 목록 로드는 카운트
  불필요 → `distributor_board(include_counts=False)`(신규 파라미터/`includeCounts` 쿼리)로
  **전일자 S1 슬립 스캔 생략**. **콜드스타트 근본 완화(풀 프리웜/`pool_recycle`/Render
  keep-warm/레거시 (Hcode,Gdate) 인덱스)는 권고만** — `lifespan` 이 "풀 lazy 생성"을 의도적
  설계로 명시해 무단 변경 지양.
- **③종료 필터**: 현황판·출고내역서에 "종료 출판사 숨기기" 체크박스(**기본 켜짐**) — 출판사명
  `<종료>` 포함 항목을 `baseRows` 로 목록·요약·카운트에서 일괄 제외(`<정지>` 등은 유지).
- **검증·배포**: tsc 0·eslint 0, `test_distributor_board` 5/5(+include_counts 가드)·
  `test_outbound_statement` 4/4. 브라우저: 화살표 이동→우측 자동조회(0017 빈결과/0013 데이터
  캐시 즉시), 종료필터 650→269. 배포 `ccf0a7c`.
- **결정자**: 사용자 (2026-07-24)
- **참조**: [[DEC-124]]/[[DEC-125]](출고내역서), DEC-033(3.23 IN 청크/IFNULL), `grid-page.ts`

### DEC-125: 총판 신규 화면 표준 목록표 기능(정렬·셀선택·클라이언트 페이징) + 출고내역서 우측 sticky

- **요청**(2026-07-24 사용자): 새로 추가된 총판 화면(현황판 [[DEC-123]]·출고내역서 [[DEC-124]])에
  표준 목록표 기능(정렬/셀이동/셀선택/페이징) 부여 + 출고내역서에서 **좌측 출판사 목록을
  스크롤해도 우측(요약+상세) 패널이 계속 보이도록 플로팅**.
- **정렬/셀선택**: 공통 프롭 재사용 — 헤더 클릭 정렬 `useClientSort`(`grid-sort.ts`),
  키보드 셀이동/선택 `DataGrid enableKeyboardNav`+`selectedRowKey`/`onSelectedRowChange`.
  ⚠ `moveTo` 는 `onSelectedRowChange` 가 있어야 동작 → 키보드 네비 그리드마다 필수 제공.
  좌측 출판사 목록은 "화살표=포커스 이동, Enter/클릭=조회" 패턴(포커스 상태 `pubFocus`
  분리 → 로드 스팸·in-flight 레이스 회피).
- **클라이언트 페이징 신규 공용 훅** `lib/grid-page.ts` `useClientPage(rows,{initialLimit,resetKey})`:
  전량 로딩 데이터(현황판 소속 출판사·내역서 라인)를 서버 왕복 없이 슬라이스, `DataGridPager`
  `page`/`onChange` 결합(상단 풀 `toolbarTop` + 하단 컴팩트 `pager`). `resetKey`(필터/정렬/
  선택 전환) 변경 시 1페이지 리셋은 **렌더 중 이전값 비교 setState**(effect 미사용 —
  `react-hooks/set-state-in-effect` 회피), offset 범위 이탈 시 표시상 첫 페이지 클램프.
- **sticky 플로팅**: 출고내역서 2열 그리드 우측 패널 `lg:sticky lg:top-0 lg:self-start`.
  스크롤 조상 = embed 래퍼(`h-screen overflow-auto`, 내부 헤더 없음), 부모
  `LIST_PAGE_ROOT_CLASS` overflow 없음 → sticky 유효. self-start 로 그리드 stretch 해제
  (sticky 이동 공간 확보).
- **검증·배포**: tsc 0 · eslint 0 · dev 서버 `/outbound/orders`·`/statement` 200 컴파일,
  `test/test_distributor_board.py`+`test/test_outbound_statement.py` 8/8. 배포 `0462b37`.
  ⚠ **로그인 세션 만료로 07-22 접수/사용중 라이브 UI 재검증은 사용자 재로그인 필요**(비번
  직접 입력 불가). 접수/사용중 도출 로직은 `test_in_use_pending`(사용중=대기)·
  `test_counts_and_flags`(접수=Yesno '0') 로 커버, 07-22 는 전건 완료 상태라 접수/사용중=0 이 정상.
- **결정자**: 사용자 (2026-07-24)
- **참조**: [[DEC-120]](공통 하단 페이저), [[DEC-123]]/[[DEC-124]](총판 화면),
  `grid-sort.ts`/`grid-page.ts`/`data-grid-pager.tsx`

### DEC-124: 총판 출고내역서(Subu39) — 거래처별 수량/덩이/보호대/박스 + 시내/지방

- **요청**(2026-07-24 사용자): 총판(물류) 계정에 **출고관리 하위 '출고내역서'** 화면 추가 —
  소속 출판사 선택 → 거래처별 출고내역(코드/명/전표/지역/장소/수량/덩이/보호대/박스) +
  시내/지방/합계 요약(레거시 `도서유통-New/Subu39`).
- **데이터 매핑(레거시 dfm 정본)**: 수량=`S1_Ssub.SUM(Gsqut)`; **덩이/보호대/박스=
  `T4_Ssub.Gqut1/Gqut2/Gqut3`**(별도 사이드 테이블 — 없으면 0 폴백); 지역 시내/지방=
  거래처 `G1_Ggeo.Gubun`(`'01'→시내`, else 지방); 장소=`Gjisa`(지점); 전표=`Jubun`;
  거래처명=`G1_Ggeo`(Hcode,Gcode)+('',Gcode) 폴백. 거래처·Gjisa·Jubun 단위 **2쿼리(S1/T4)
  + Python 병합**(3.23 파생테이블 회피, IFNULL). ⚠ S1↔T4 를 JOIN 하면 도서 라인 수만큼
  포장 합계가 fan-out 되므로 각기 집계 후 키 병합.
- **HOTFIX(2026-07-24)**: 상세 "전표" 컬럼이 `Jubun`(거래처별 차수=11)을 표시 → **전표번호
  표시 정본 = Idnum**([[DEC-108]]/[[slip-number-idnum-vs-jubun]]) 위반. 쿼리에 `MAX(Idnum+0)
  AS idnum` 추가(슬립 그룹 내 Idnum 공통 1값), 프론트 컬럼 `jubun`→`idnum` +
  `formatIdnumDisplay(idnum) || jubun`(폴백). 신규 화면 만들며 규약 재발 — 감사목록에 등록.
- **엔드포인트**: `GET /api/v1/outbound/statement?serverId&date&hcode`(선택 출판사).
  총판 게이트(`resolve_g7_ggeo_list_scope=None`), hcode=선택 출판사로 격리 조회(교차 뷰는
  총판만). S1/T4 쿼리는 Hcode 필터 있어 hcode 감사 critical=0.
- **총판 전용 메뉴**: 메뉴 매트릭스는 **show-first**(계정유형으로 숨기지 않음)이고
  `requiredPermission` 은 실제 사이드바를 숨기지 않으므로, **`FormMeta.distributorOnly`**
  플래그 신설 + 사이드바 `isVisibleForm` 게이트로 총판(account_type=T2_DIST **또는**
  build_role=distributor)에게만 노출. Sobo39 는 `menuId:null`(매트릭스 우회) + 출고관리 하위.
- **검증·배포**: tsc·eslint·next build·py_compile 클린, hcode 감사 critical=0,
  `test/test_outbound_statement.py` 4/4, 프로브 `outbound.statement` 등록. 배포 `f8becc0`.
- **결정자**: 사용자 (2026-07-24)
- **참조**: [[DEC-123]](총판 현황판·판별), [[slip-number-idnum-vs-jubun]](전표=Jubun vs Idnum),
  DEC-033(3.23 IFNULL/파생테이블), MENUVIS-DEC-07(show-first)

### DEC-123: 총판(T2_DIST) 출고접수관리 현황판 — 소속 출판사 접수/완료 상태판

- **요청**(2026-07-24 사용자): 총판(물류) `T2_DIST` 계정(예: 한국도서유통)은 출고접수관리
  화면을 **소속 출판사 현황판**으로 제공 — 물류센터가 소속 출판사들의 출고신청 과정을 본다.
  컬럼: 출판사코드/명/전화 + 접수건/완료건 + 미사용/사용중/접수/완료.
- **판별·라우팅**: 백엔드 `ctx["account_type"]=="T2_DIST"`, 프론트 `user.account_type`.
  `/outbound/orders` 진입 시 T2_DIST 면 `DistributorOutboundBoard`, 그 외(출판사)는 기존
  출고접수 목록(대시보드 라우팅 시임과 동일 패턴, 페이지 레벨 분기).
- **데이터**: `GET /api/v1/outbound/distributor-board` → `outbound_service.distributor_board`.
  소속 출판사 = **G7_Ggeo**(출판사 마스터, `Gcode`=코드=`S1_Ssub.Hcode`, `Gname`, `Gtel1/2`).
  접수/완료 = S1_Ssub 슬립단위(`GROUP BY Gdate,Hcode,Gcode,Jubun,Gjisa,Idnum`) `MAX(Yesno)`
  → Hcode별 pending/received/done **Python 집계**(3.23 파생테이블 회피, IFNULL).
- **격리 함정**: `enforce_hcode_isolation` 은 로그인 hcode 를 강제(WHERE Hcode=login)해 교차
  출판사 뷰가 0행 → **금지**. 대신 `resolve_g7_ggeo_list_scope(ctx)` 가 **None(T1/T2_DIST/
  super)** 인 계정만 허용(교차 뷰), 격리(T2_PUB/T3)는 403. S1_Ssub 무-Hcode 쿼리는
  `# noqa: hcode-guard`(총판 게이트 근거).
- **상태 산출**: 접수(received>0)/완료(done>0)는 데이터로 완전 산출. **미사용/사용중은 한계** —
  로그인 세션/last-login 저장이 **전무**(login 은 파이썬 logger 만, DB 미기록)라 실시간 로그인
  여부 불가 → **미사용=당일 슬립 0건(활동 근사)**, **사용중=대기(pending, Yesno='') 슬립 존재**.
  정밀 로그인/presence 는 net-new 인프라 필요(후속).
- **검증·배포**: tsc·eslint·next build·py_compile 클린, hcode 격리 감사 critical=0,
  `test/test_distributor_board.py` 4/4, 프로브 `outbound.distributor_board` 등록. 배포 `37f539b`.
- **결정자**: 사용자 (2026-07-24)
- **참조**: DEC-095(테넌트 DB 라우팅), DEC-081(Yesno '1'·'2'=완료), DEC-033(3.23 IFNULL/파생테이블)

### DEC-122: 신규도서 스캔 심화 — 전역 캡처 + ISBN 중복검사 + 국립중앙도서관 서지 자동채움

- **요청**(2026-07-24 사용자): (1) 스캐너 키 포커스가 다른 곳에 있어도 ISBN 은 **무조건 ISBN
  필드**에, (2) 스캔 ISBN 이 이미 DB 에 있으면 **중복 안내/기존정보 불러오기(수정)**, (3) 신규면
  **국립중앙도서관 서지정보 API** 로 도서 필드 자동 입력.
- **(1) 전역 캡처**: `useBarcodeScanner` 에 `captureGlobal`([[DEC-121]] 라이브러리 확장).
  `document` keydown 을 잡되 **웨지 연타(평균 간격 ≤30ms)만 스캔**으로 인식(사람 타이핑 무시),
  **첫 글자 보존**(gap>60ms 새 시퀀스 시작), 후속 연타는 `preventDefault` 로 포커스 필드 오염
  최소화(스캔 시 최대 1글자만 새고 나머지 차단). 수동 입력은 스캔칸 `onInputKeyDown`(Enter)
  별도 경로 + 최근값 700ms 디듀프로 이중 처리 방지. 저수준 `useScanner`(웨지, DEC-004)는
  scoped 경로에서만 사용해 C8 무영향.
- **(2) 중복검사**: `masters_service.find_book_by_isbn`(G4_Book 을 hcode 스코프에서
  `REPLACE(...Gisbn...)` 숫자 정규화 비교 — 저장측 하이픈/공백 무관). 라우터
  `GET /api/v1/masters/book/by-isbn` — **`/book/{gcode}` 보다 먼저** 정의해 경로 충돌
  (gcode='by-isbn') 회피. 프론트: 스캔 시 조회 → 존재하면 "이미 등록된 도서" 배너 +
  '기존 도서 수정하기'(상세 라우트 이동).
- **(3) 서지 자동채움**: 기존 `/api/v1/integrations/nl/isbn`(국중 SEOJI SearchApi,
  `config.NL_API_KEY`=`BLS_NL_API_KEY`) **재사용** — 스캔 흐름에 연결. `title→도서명(gname)`,
  `author→저자명(gjeja)`, `pub_date→발행일(date1, YYYY-MM-DD 정규화)`, `price→단가(gdang)`.
  키 미설정(`config_missing`)/미발견 시 자동채움 건너뛰고 안내만(ISBN 은 입력됨).
- **검증**: tsc·eslint·next build 클린, 백엔드 py_compile OK, hcode 격리 감사 critical=0,
  라우터 감사 critical=0, `test/test_book_by_isbn_lookup.py` 5/5, 프로브 `masters.book.by_isbn`
  등록. 배포 `ff27d90`(Vercel 프론트 + Render 백엔드).
- **결정자**: 사용자 (2026-07-24)
- **참조**: [[DEC-121]](스캐너 공용 라이브러리), DEC-004(웨지 useScanner), DEC-033(멀티 DB/3.23 REPLACE·IFNULL)

### DEC-121: 범용 USB 바코드 스캐너 공용 라이브러리 (화면별 바코드 종류 주입)

- **요청**(2026-07-23 사용자): 신규도서 등록에서 USB 범용 바코드 스캐너로 책을 스캔하면
  ISBN 이 ISBN 칸에 자동 입력되고 **스캐너 연결 여부가 표시**되어야 함. 범용 스캐너 연동은
  여러 곳에 쓰이므로 **공용 라이브러리**로 구성하고, **바코드 종류는 화면별로 가변**.
- **구조(단일 출처)**:
  - `frontend/src/lib/barcode-scanner.ts` — 공용 훅 `useBarcodeScanner` + `BarcodeFormat`
    (화면별 바코드 종류 주입 인터페이스) + 내장 포맷 `ISBN_FORMAT`/`EAN13_FORMAT`/
    `ANY_BARCODE` + `parseIsbn`(978·979 EAN-13/ISBN-13, 부가기호 앞 13자리, ISBN-10).
  - `frontend/src/components/shared/barcode-scanner-field.tsx` — 즉시 재사용 컴포넌트
    (스캔 input + 연결상태 배지 + WebHID 장치 연결 버튼 + 최근 스캔 결과).
- **저수준 감지**: 신규 구현 없이 기존 `useScanner`(DEC-004 키보드 웨지: 연타 <30ms +
  Enter 종결 버퍼링) 재사용. **전용 스캔 input(`targetRef`)** 사용 — `useScanner` 의
  전역캡처(captureGlobal)는 각 스캔 첫 글자를 흘리는 한계가 있어 회피.
- **연결 여부**: 키보드 웨지 스캐너는 브라우저가 연결을 직접 못 보므로 **첫 스캔 인식 시
  `connected`**("대기 중"→스캔 후 "연결됨"). WebHID(`navigator.hid`) 지원 브라우저 +
  HID 모드 스캐너면 실제 device 연결/해제 감지 + 장치 승인(progressive enhancement —
  미지원/키보드모드에서도 웨지 경로로 정상 스캔).
- **함정**: `eslint-plugin-react-hooks@7`(React Compiler 계열)의 `react-hooks/refs` 규칙이
  **훅 반환 객체에 ref(`inputRef`)가 섞이면** 그 객체 전 멤버 접근을 ref-접근으로 오탐 →
  빌드 실패. **ref 는 컴포넌트가 생성해 훅 옵션으로 주입**하고 훅은 상태값만 반환하도록
  분리해 해결.
- **적용**: `master/book/new` 에 `BarcodeScannerField(format=ISBN_FORMAT)` 배치 → 스캔 시
  `update("gisbn", …)` 자동 입력, `autoFocus` 로 스캔 우선. 타 화면은 자기 `format` 주입.
- **검증·배포**: tsc·eslint·next build 클린 → 커밋 `3afdeb6` → Vercel success.
- **결정자**: 사용자 (2026-07-23)
- **참조**: DEC-004(useScanner 웨지 원형), DEC-040(C8 스캔 매칭 분리)

### DEC-120: 페이징 목록 전면 — 표 하단 우측 공통 페이저(sticky 이전/다음)

- **요청**(2026-07-22 사용자): "페이징이 적용된 모든 목록 표는, 표가 길면 하단에서 다음
  페이지로 이동이 불가능하다. 표 **하단 오른쪽에 이전/다음 버튼**을 추가하고, UX 유지를 위해
  페이징된 모든 표에 **공통**으로 적용해달라." (기존 페이저는 표 **위**에만 있어, 긴 표를
  스크롤해 내려가면 페이지 이동 컨트롤이 화면 밖으로 사라짐.)
- **공통 컴포넌트 2곳만 손대는 단일 출처 방식**:
  - `data-grid-pager.tsx` — `DataGridPager` 에 `variant?: "full" | "compact"` 추가.
    `compact` = **이전 / N·M / 다음** 만(건수 범위·페이지당 select 생략). 단일 페이지
    (이전·다음 모두 불가, 로딩 무관 원시조건)면 `null` 반환 → 짧은 표엔 미노출.
  - `data-grid.tsx` — `DataGrid` 에 `pager?: DataGridPagerProps` prop 추가. 있으면 표
    **하단 footer 우측**에 `compact` 페이저 렌더. **페이지가 2개 이상일 때만**
    `sticky bottom-0 …bg-card/95 backdrop-blur` 로 고정(긴 표 스크롤 중에도 항상 하단
    도달) — 빈 sticky 바 방지 위해 `showBottomPager`(offset>0 || has_more || offset+limit<total)
    로 게이팅. 상단 페이저는 무변경(추가 방식).
- **호출부 규약**: 각 화면이 상단 `<DataGridPager>` 에 넘기던 **동일 props 를 그대로**
  `pager={{...}}` 로 DataGrid 에 전달(contextual typing 으로 `next` 자동 타입 — 신규 import·
  상수 0). `onChange` 인자 순서/함수는 화면별로 상이(`(next)=>load(next.offset,next.limit)`,
  `({limit,offset})=>load(offset,limit)`, `(next)=>load(next.limit,next.offset)`,
  `fetchData/loadList`, `lastValues?load(...)` 등) → **화면 원본 verbatim 전사**.
- **적용 범위**: 목록 화면 63 + 마스터 패널 6 + `simple-master-page` 공통(→ 다수 기초관리).
  다중 뷰 그리드는 전부 편입 — 출고현황 3그리드(요약/상세마스터/목록), 입고현황·거래상태
  2그리드. **제외**: `master-lookup-dialog`(이미 표 아래 full 페이저 존재), 상세 미니그리드·
  집계 미니그리드·수기 master-detail `<table>`(같은 `page` 상태 아님).
- **검증**: 전체 `tsc --noEmit` 0, `eslint`(공통 컴포넌트) 0, `next build` ✓ Compiled,
  누락 감사(`<DataGridPager` 있는데 `pager=`/`variant="compact"` 없는 파일) 0건.
- **결정자**: 사용자 (2026-07-22)
- **참조**: DEC-024(표준 페이지 응답 `{items, page:{limit,offset,total,has_more}}`),
  [[keyboard-input-flow]]

### DEC-119: 필터 셀렉트 전면 픽 필드 전환 + 년말집계 체크박스/라디오 스톱 편입

- **요청**(2026-07-21 사용자): ① 도서별년말집계의 SCode 체크박스·집계단위(년/월)가 Enter 만으로
  진행 불가(스톱 누락). ② 도서구분 같은 **셀렉트류 입력은 Enter=목록 팝업→선택 Enter=값 입력+
  다음 입력창 이동**(픽 필드 — DEC-112 지사/구분 패턴)이어야 한다.
- **① 년말집계 스톱 편입**: FILTER_STOP_IDS 에 `CheckBox2.Input`(체크=Space)·`GrainGroup`
  (라디오 그룹 래퍼 div — 진입 시 첫 라디오 포커스, ←→ 네이티브 same-name 라디오 선택) 추가.
  CDP 검증: 도서구분→SCode→년/월→조회 자동실행 체인.
- **② 필터 셀렉트 15개 픽 필드 전환**: 필터 바 네이티브 `<select>` → `LocalComboField`
  (Enter=포털 목록→↑↓→Enter=선택+`onSelectAdvance`). `advanceAfterSelect` 를
  `filter-enter.ts` 공용으로 승격(MLF 팝업 선택과 동일 규약 — 다음 입력칸 이동, 없으면
  조회/검색 버튼 자동 실행). `data-legacy-id` 는 내부 input 에 verbatim 보존(스톱 체인 유지).
  대상: 년말집계 도서구분, 원장 2종 범위, 반품수불 구분, 청구서 변형, 입금현황 변형(동적
  prefix), 감사 액션, 기초관리 5종 구분, 거래명세서 거래구분·지사(자체 focusNextFilter 체인
  연동 — combobox input 을 체인 셀렉터에 편입). 제외: 그리드 셀 편집 셀렉트(출판사관리
  CHEK3/YESNO), 액션 패널(택배사), 페이지당.
- **검증**: CDP — 년말집계 도서구분 Enter=목록(창고/본사/전체)→선택→SCode 이동 확인. 통합
  tsc·eslint 0. 배포 커밋 `bb923b1`(스톱 편입)·`68b139b`(픽 필드 전환).
- **결정자**: 사용자 (2026-07-21)
- **참조**: DEC-112(LocalComboField 원형), DEC-116(스톱 규약), DEC-118(advanceAfterSelect),
  [[keyboard-input-flow]]

### DEC-118: 기간 조회 날짜 오름차순 기본 + 팝업선택 자동이동/조회 + 년월 세그먼트

- **요청**(2026-07-21 사용자): ① "모든 목록에서 기간 조회 결과는 시작일 날짜가 맨위(오름차순)".
  ② "팝업 검색 선택 Enter = 값 전달 + **다음 입력창 자동 이동**, 다음 창 없으면 최종 조회
  자동 실행 — 점검". ③ "년월만 있는 날짜 입력창도 년 4자리→월 자동 이동(일괄 처리 누락)".
- **① 날짜 오름차순 기본**: 서버정렬 20화면 `useState<DataGridSort>` 초기값을 날짜키 asc
  (gdate/bucket/last_date — boot load 가 상태를 읽는 것 확인), 클라정렬 12그리드
  `useClientSort(rows,{initial:{key:'gdate',dir:'asc'}})`. 날짜 컬럼 없는 집계 화면
  (통합수불장·미수금·재고현황 등)·단일일자 화면은 스킵(에이전트 보고 기준).
  **출고 화면 조화**: 1차 gdate asc + **백엔드 2차 tiebreak 를 전표번호(idnum alias)로 교정**
  (`_status_order_by_sql` default "Gdate DESC, idnum"/"Gdate, idnum", outbound
  `_list_order_by_sql` tiebreak "Gdate DESC, idnum") — 같은 날짜 안 전표번호 오름차순(어제
  전표번호 정렬 요청과 양립). 백엔드 기본 순서 flip: 신간발행 `Gdate asc`, 지불전표
  `cash_service` `Gdate asc`(정렬 UI 없는 카드 목록). CDP 검증: 06.01부터·동일일
  00001→00002→… 확인.
- **② 팝업 선택 자동 이동/조회**: 기존 `refocusAfterSelect` 는 입력칸 복귀까지만(추가 Enter
  필요)이어서 사용자 기대 미달 — **선택 확정 시 `advanceAfterConfirm`**: `data-enter-scope`
  범위에서 자기 루트(자기 검색버튼) 제외 다음 포커서블로 이동, 그것이 조회/검색(`/조회|검색/`)
  버튼이면 50ms 지연 자동 클릭(읽기 전용 조회만). ESC/취소=입력칸 복귀 유지, 신규 등록 흐름
  (기본 false)은 무변경. CDP 검증: 거래처코드 시작 팝업 선택→끝 칸 이동, 끝 선택→자동 조회.
  ※ 검증 함정: 팝업 그리드 단일 클릭=선택 강조만(확정=더블클릭/Enter/선택 버튼).
- **③ 년월 세그먼트**: `DateFieldYMD monthOnly` 모드 — 값 `YYYY-MM`, 년4→월 자동이동, 월
  2자리 입력 완료 시 다음 필드 자동 이동, 월이 마지막 세그먼트(Enter=onKeyDown/자동 이동),
  숨긴 native `type=month` showPicker 로 월 달력 유지. `type="month"` 12개(청구월·조회월·
  시작/종료월·기준년월·연말도서 년월) 전환 — FILTER_STOP legacyId 보존, 필터 필드는 noop
  onKeyDown(컨테이너 자동조회 연결), 쓰기 폼(입금 청구월)은 미적용. CDP 검증: 년 2026 입력→
  월 세그먼트 이동·세그먼트 2개·월 달력.
- **검증**: 통합 tsc·eslint 0. 기존 outbound 정렬 테스트 20건 PASS(1건 실패=기존 알려진
  customer_name 키 flake). 배포 커밋 `d5e81f9`.
- **결정자**: 사용자 (2026-07-21)
- **참조**: DEC-117(자동조회·스톱 규약), DEC-115(DateFieldYMD), DEC-082(서버 정렬),
  [[keyboard-input-flow]]

### DEC-117: 필터 자동조회(마지막 값 Enter=즉시 조회) + 거래처별 판매 마스터-디테일

- **요청**(2026-07-21 사용자): ① 거래처별 판매에서 "모든 값이 정해진 순간 Enter 하면 조회로
  포커스 이동하면서 **버튼에서 Enter 를 안 쳐도 자동 조회**". ② 레거시 Sobo62 하단 상세
  목록(DBGrid201)이 포팅 누락 — 출고현황처럼 **1차 목록 행 선택 → 우측 상세 표**.
- **① 자동 조회**: `advanceFilterOnEnter` — 다음 스톱이 **마지막 스톱이고 버튼**이면 포커스
  이동 + 30ms 지연 `click()`(방금 값의 React 상태 커밋 후 load 가 읽도록). "마지막 스톱=
  읽기 전용 조회 버튼" 규약 위에서만 동작(임의 버튼 클릭 아님). **필터 DateFieldYMD 에
  `onKeyDown={()=>{}}` 일괄(28파일 코드모드 + 신규 배선 7화면)** — 일 세그먼트 Enter 가
  self-advance 대신 컨테이너로 버블돼 **날짜가 마지막인 화면도 자동 조회**. outbound-status
  자체 핸들러 동일 반영. 1차 감사 통과로 미배선이던 7화면(월별통계·입고일보/기간별·반품
  접수/일별/기간별·지불전표)도 배선. 검증: 4개 유형(MLF-마지막/날짜-마지막/radiogroup/체크박스)
  화면 CDP AUTO_RAN 확인. ※ 검증 함정: fetch 스파이 카운터를 버튼 도달 **후** 리셋하면
  30ms 지연 클릭의 fetch 를 지워 NO_AUTO 오탐 — pre/post 비교로 판정할 것.
- **② 마스터-디테일**: 레거시 DBGrid201(도서명·출고수량/금액·증정수량·반품수량/금액·판매
  수량/금액 8컬럼+footer 합계, Sobo62.md §6 out-of-scope 였음) 구현.
  - 백엔드 `GET /reports/customer-sales/detail`(`get_customer_sales_detail`) — 선택 거래처
    **(gcode + COALESCE(Gjisa,'')=gjisa) 고정 + GROUP BY Bcode,Gubun,Pubun**,
    `get_customer_sales` 와 동일 누적 분기(반품→gbqut/gbsum+판매, 증정→gjqut(판매수량 제외),
    출고→goqut/gosum+판매). 도서명 G4_Book `in_clause_lookup`(JOIN 금지/DEC-068), totals 합계,
    BOOK_SALES_MAX 캡. hcode 는 enforce_hcode_isolation.
  - 프론트: 좌(거래처 집계 DataGrid — rowKey 를 (hcode|gcode|gjisa) 안정키로 변경,
    enableKeyboardNav/selectedRowKey)·우(상세 표 `Sobo62.DBGrid201`) 2분할(xl 기준),
    행 클릭/↑↓ 선택 시 지연 조회, 같은 행 재선택=접기, 재조회 시 선택 초기화.
- **검증**: `test_customer_sales_detail.py` 신설(누적 분기·totals·G4_Book hcode 스코프·
  WHERE gcode/gjisa 스코프) 2건 PASS. 프로브 `reports.customer_sales_detail` 등록.
  CDP 라이브: 조회 20행 → 교보문고(인터넷지점) 행 선택 → 도서 3행+합계 실데이터 표시.
  통합 tsc·eslint 0. 배포 커밋 `14c74e4`.
- **결정자**: 사용자 (2026-07-21)
- **참조**: DEC-116(필터 Enter-흐름·스톱 규약), DEC-082(정렬), Sobo62.md §6(DBGrid201
  out-of-scope 해제), `lib/filter-enter.ts`, `reports_service.get_customer_sales_detail`

### DEC-116: 전 조회/필터 화면 키보드 Enter-흐름 일괄 적용 (브라우저 감사 기반)

- **요청**(2026-07-21 사용자): "마우스 없이 검색 필드 설정·조회까지 모두 진행" — 이전 적용
  이슈(날짜 입력 방식·Enter 자동 이동)를 **모든 조회/필터 화면**에. 이후 "먼저 검증 후 안된
  부분만 처리, 브라우저로 확인 후 구현 안 된 부분만 수정" 지시.
- **방법(감사 우선)**: CDP 스크립트로 53개 필터 화면을 **실측**(첫 필터 칸부터 Enter-only
  워크, fetch 스파이 병행) → 판정: REACHED(조회 버튼 도달)/QUERY_RAN(Enter=즉시 조회 실행)/
  POPUP(MLF 빈 Enter 팝업 갇힘)/STUCK(멈춤). 1차: 15개 통과(날짜-only 화면=DateFieldYMD 자동
  이동 덕, master 검색화면=Enter 즉시조회), **~38개 실패**.
- **수정(실패분만)**: customer-sales 템플릿(`advanceFilterOnEnter`+`FILTER_STOP_IDS`+
  `data-enter-scope`) 일괄. 필터 MLF=빈 Enter 통과(`onKeyDown={()=>{}}`)+`refocusAfterSelect`.
  sales-statement 는 자체 흐름 유지하되 전표번호(Edit109) Enter=즉시조회→다음 필드 이동으로
  통일(조회=마지막 필드/버튼/Ctrl+Enter). 재감사에서 남은 STUCK 3개(cash·inbound-statement·
  inbound-status)=**무명 취소포함 체크박스가 날짜 자동이동의 다음 포커서블**이라 멈춤 →
  `Chk_Cancel` id 부여+스톱 포함. **최종 53/53 통과**(REACHED 또는 설계상 QUERY_RAN).
- **함정 기록**: ① 날짜(DateFieldYMD) 일-Enter 자동이동은 "래퍼 다음 첫 포커서블"로 가므로,
  날짜와 조회 버튼 사이의 **모든 포커서블(체크박스 포함)은 스톱이어야** 끊기지 않는다.
  ② 감사 스크립트의 조회버튼 식별이 MLF 팝업 "검색" 버튼과 겹칠 수 있음(오탐) — 판정은
  트레일로 재확인. ③ **공유 워킹트리에서 병렬 에이전트의 git stash/reset 은 재앙**(1차 스윕
  전체가 되돌려짐 — HEAD 는 무사, 워킹트리 복구 후 재실행. 에이전트 지시에 git 전면 금지 명시).
- **검증**: 통합 tsc 0, eslint 신규 0, CDP 재감사 53/53. 배포 커밋 `d34fff2`(38화면)·
  `d00c839`(잔여 3) + 같은 배치에 출고관리 전표번호 기본 오름차순(`a79f3dd`).
- **결정자**: 사용자 (2026-07-21 — "모든 조회/필터 화면 일괄" 확정, "검증 후 안된 부분만")
- **참조**: DEC-113(필터 Enter 패턴 원형), DEC-115(DateFieldYMD), `lib/filter-enter.ts`,
  [[keyboard-input-flow]]

### DEC-115: 모든 날짜 입력 → DateFieldYMD(년 4자리→월 자동이동 + 달력) 앱 전역 전환

- **요청**(2026-07-21 사용자): 네이티브 `<input type="date">` 는 월·일은 입력하면 다음으로
  자동 이동하는데 **년도는 4자리를 넣어도 월로 이동 안 해 불편**하다. 년 4자리→월 자동이동을
  **모든 날짜 컨트롤**에 적용하라.
- **원인/결정**: 네이티브 date 년도 필드는 연도 자릿수 가변이라 4자리에서 자동 이동 안 함
  (브라우저 특성). 세그먼트가 DOM 비노출 + 합성 KeyboardEvent isTrusted=false 라 스크립트로
  제어 불가 → **커스텀 3분할 필요**. 단, 앞서 3분할은 달력 상실로 되돌렸었음 → 이번엔 **숨긴
  네이티브 date + 달력 버튼(`showPicker`)** 을 붙여 달력 선택도 유지 → 채택.
- **`DateFieldYMD`**(`components/shared/date-field-ymd.tsx`): 년(4)/월(2)/일(2) 세그먼트 +
  달력 버튼. 자리수 채우면 자동 다음(년4→월·월2→일), Enter 년→월→일, ↑↓ 값, ←→ 세그먼트,
  Backspace 빈칸 이전, 값 `YYYY-MM-DD`. props: onChange/legacyId/ariaLabel/disabled/className/
  **onKeyDown**(일 세그먼트 Enter=다음 필드/조회)·**inputRef**(년 세그먼트, 자동포커스).
- **전역 전환**: 앱 전역 **82개** date input 을 44개 파일에서 DateFieldYMD 로 일괄 교체
  (6개 병렬 에이전트 배치). min/max 없음, onChange 어댑트(`(e)=>setX(e.target.value)`→`setX`,
  cash 는 dot↔date 변환·복합 setter 래핑), 미사용 `Input` import 정리.
- **후속 보강**: 일부 화면(sales-statement/new·page, edit/search-dialog)이 date input 의
  onKeyDown(Enter→다음/조회)·ref(자동포커스)를 잃어 DateFieldYMD 의 onKeyDown/inputRef 로 재배선.
- **검증**: 통합 `tsc --noEmit` 0, 각 배치 eslint 0. CDP 라이브: 출고현황에서 년 "2025" 입력→
  포커스 월로 자동 이동 확인, 달력 버튼·세그먼트 정상. 배포 커밋 `15be948`(전환).
- **결정자**: 사용자 (2026-07-21)
- **참조**: DEC-113(날짜 3분할 1차 시도·되돌림 시행착오 — 이번에 달력 병행으로 재채택),
  [[keyboard-input-flow]], `date-field-ymd.tsx`

### DEC-114: 출고현황 상세 배치 바로출고/바로재출고 + 접수유형 필터 + 긴급 출력 큐

- **요청**(2026-07-21 사용자): 출고현황 상세에서 ① 선택 헤더로 **접수유형(접수/대기/완료) 필터
  + 전체선택**, ② 선택 여러 건 **"바로출력 (N건)"** 배치 실행(표 위 버튼), ③ **완료** 건은
  한/여러 건 선택 시 **"바로재출고 (N건)"** 로 재출력.
- **UI**: 상세 그리드 toolbarTop 에 접수유형 `<select>`(전체/대기/접수/완료)로 표시 슬립
  (`filteredSlips`)·전체선택 대상 좁힘 + '전체 선택'/'선택 해제'. 선택 조합에 따라 버튼 노출 —
  완료전(대기+접수) 있으면 `바로출력 (N건)`(`Sobo24.BatchImmediateDispatch`), 완료 있으면
  `바로재출고 (N건)`(`Sobo24.BatchReprint`). 기존 '대기 N건 출고요청'은 바로출력에 흡수.
- **동작**: 바로출력=대기분 `requestDispatchBatch`(→접수, 완료 전이 기준) + **완료전 전체
  긴급 출력 큐 적재**. 바로재출고=완료분 긴급 출력 큐 적재(상태 무변경).
- **긴급 출력 큐(핵심, DEC-111 확장)**: `received-stream` 은 접수 신규분만 `seen` dedup 방출해
  **완료 재출력·이미 접수 건 강제 인쇄를 표현 못함**. → `transactions_service._urgent_print_queue`
  (hcode별 메모리) + `POST /transactions/sales-statement/urgent-print`(enforce_hcode_isolation)
  + SSE 제너레이터가 매 tick `_drain_urgent_print(hcode)` → `{type:"urgent",keys}` 방출.
  자동출력 탭 `subscribeReceivedStatements.onUrgent` → **printedRef dedup 우회 강제 인쇄**(완료
  재출력 허용), 인쇄 후 printedRef 추가로 일반 경로 중복만 방지. 키=`serializeStatementKey`.
  **⚠ 단일 인스턴스 가정(Render)** — 다중 인스턴스면 POST/SSE 프로세스 분리로 전달 실패 가능,
  그 경우 DB 백엔드 큐로 승격 필요. 유실돼도 데이터 손상 없음(재클릭/3분 폴 안전망).
- **한계**: 배치 바로출고/재출고의 실제 인쇄는 자동출력 PC 탭이 열려 있어야(2-PC/프린터 필요)
  종단 검증 가능 — 여기선 UI·요청 경로·SSE 방출·hcode 격리만 검증.
- **검증**: `test_dec111` 에 긴급 큐 방출·hcode 격리·공백 제외 회귀 추가(3건 PASS). 프론트
  tsc·eslint 0. 배포 커밋 `56353ba`.
- **결정자**: 사용자 (2026-07-21)
- **참조**: DEC-111(즉시출력 SSE·바로출고 버튼), DEC-109(gjisa 슬립 분리), [[sse-realtime-pattern]]

### DEC-113: 출고현황 필터 방향키+Enter 전용 흐름 (조회까지 진행)

- **요청**(2026-07-21 사용자): 출고현황 필터를 **방향키+Enter 만으로** 값 선택·조회까지
  진행할 수 있어야 하는데 누락. (Enter 로 필드 이동/토글 선택/최종 조회가 안 됨.)
- **원인**: 공용 `advanceFocusOnEnter`(DEC-105)는 input/select/textarea 만 이동 대상이라
  버튼류(도서구분 토글, 조회)를 건너뛴다. 이 필터엔 그 핸들러조차 미부착이었고, 도서구분은
  개별 `<button>` 3개라 키보드 그룹 선택도 불가.
- **구현(재사용 패턴)**: ① 검색 패널에 로컬 `onFilterKeyDown` — `FILTER_STOP_IDS`
  (data-legacy-id 순서: 거래처→도서코드→전표→시작일→종료일→도서구분→조회)로 **Enter=다음
  스톱**. 자동완성 팝업 열림(`aria-expanded`) 시 Enter=선택은 가로채지 않고, **마지막 조회
  버튼은 preventDefault 없이 기본 동작(조회 실행)**으로 둔다(입력/그룹은 preventDefault+이동).
  ② 도서구분을 **radiogroup**(role/aria-checked, tabIndex 0, 내부 버튼 tabIndex -1)으로 —
  ←/↑ 이전·→/↓ 다음(순환)·Home/End, Enter 는 컨테이너로 버블돼 조회로 이동. ③ 필터
  MasterLookupField(거래처/도서코드)는 **빈 값 Enter=팝업 대신 통과**(`onKeyDown={()=>{}}`
  로 empty-Enter 위임 → 컨테이너 이동; 필터=비우면 전체). `data-enter-scope` 부착으로 MLF
  자체 focusNextFrom 과 스톱 경로가 일치(멱등).
- **검증(브라우저 라이브, 백그라운드 탭)**: Enter 워크 포커스 궤적 Edit104→Edit106→Edit109
  →Edit101→Edit102→Panel102→dxButton1 순 정확 이동, 도서구분 ArrowRight 로 전체→본사 순환,
  최종 조회 버튼 도달 확인. tsc·eslint 0. 배포 커밋 `1b964cf`.
- **날짜 입력 시행착오(2026-07-21)**: ① 1차 — "날짜를 년→월→일 세분화 이동" 요청에 년4·월2·
  일2 **3분할 `DateFieldYMD`** 신규(커밋 `1c4aef1`, 라이브 검증까지 통과). ② **되돌림**(커밋
  `b5924d6`) — 사용자 지적: **3분할은 달력(calendar) 선택을 잃는다**. 네이티브 `<input
  type="date">` 유지가 우선. 사용자 요청은 "네이티브 유지 + ↑↓ 값·←→ 세그먼트 + Enter=오른쪽
  화살표(세그먼트 이동) 대체, 불가하면 기존 복원". **Enter=세그먼트 이동은 네이티브 date 에서
  불가능**(세그먼트가 DOM 비노출 + 합성 KeyboardEvent 는 isTrusted=false 라 세그먼트 이동을
  트리거 못함) → 지시대로 **네이티브 date 복원**, `DateFieldYMD` 삭제. 날짜는 필터 Enter 흐름상
  **한 스톱**(Enter=다음 필드), 세그먼트는 브라우저 기본 ←→/↑↓/타이핑/달력으로.
  **교훈: 날짜는 네이티브 date 컨트롤을 유지할 것(달력 필요). 커스텀 3분할 금지.**
- **결정자**: 사용자 (2026-07-21)
- **참조**: DEC-105(Enter=다음 컴포넌트 공통), DEC-104(무지사 Enter 리듬), DEC-101(수량 ↑↓
  증감), `focus-advance.ts`(input 전용 한계), MasterLookupField(aria-expanded 가드).
  **새 필터 바는 이 패턴(FILTER_STOP_IDS + radiogroup + 빈값 통과)을 따르고, 날짜는 네이티브
  date 유지.**

### DEC-112: 지사·구분 콤보 → 픽 필드(팝업 선택) + 출고현황 상세 컬럼 기본순서

- **요청**(2026-07-20 사용자): ① 출고 신규주문의 **지사(거래처 지점)·구분(위탁/현매/매절/납품/
  특별/기타)** 이 네이티브 `<select>` 콤보라 Enter 를 치면 선택 없이 다음 칸으로 넘어간다.
  거래처/도서 검색 팝업(MasterLookupField)처럼 **"Enter→목록 팝업→선택→Enter"** 방식으로
  통일. ② 출고현황 상세 목록 컬럼 기본 순서를 **거래일자→전표번호→거래처명→접수** 로.
- **결정(사용자 확정)**: "항상 팝업(픽 필드)" — 값이 있어도 Enter=팝업 열기. 구분 기본값
  위탁은 팝업에서 미리 강조(그냥 Enter 두 번이면 위탁 유지). **지사에 지점이 없으면(무지사)
  기존 Input 유지**로 Enter=바로 통과(엔터 리듬 보존, DEC-104 — 자동 건너뛰기 금지 원칙).
- **구현**: `components/shared/local-combo-field.tsx`(신규 재사용). API 없는 로컬/고정 옵션용
  콤보박스 — readOnly Input + **portal(body) fixed 리스트박스**(그리드 overflow 비잘림,
  MasterLookupField 동형). 닫힘 Enter/↓/클릭=팝업 열기(현재 값 강조), 열림 ↑↓ 이동·Enter/
  클릭=선택+`onSelectAdvance`(다음 칸)·Esc=닫기(제자리)·타입어헤드. 한글 IME 조합 keydown 무시.
  적용: 출고 신규주문 지사(`orders/new`, 지점 있을 때만), 라인 구분(`OrderLineGrid`, pubun).
  포커스 체인 유지 — 지사 선택→첫 구분, 구분 선택→도서코드(`focusFirstPubunEl`/`bcodeRefs`).
- **컬럼 순서**: `outbound-status` `slipDetailColumns` 정의를 거래일자→전표번호→거래처명→접수로
  재배열(미설정 시 default; 사용자 서버 저장 순서가 있으면 그게 우선).
- **검증**: 프론트 tsc·eslint 0(LocalComboField effect 내 setState 제거로 set-state-in-effect
  해소). 배포 커밋 `2092102`.
- **결정자**: 사용자 (2026-07-20 — AskUserQuestion "항상 팝업" 선택)
- **참조**: DEC-104(무지사 Enter 통과·리듬), DEC-107(라인표 컬럼 기능), MasterLookupField
  (팝업 키보드 흐름 원형), `local-combo-field.tsx`

### DEC-111: 거래명세서 즉시 출력(SSE 준실시간) + 출고목록 전표 흡수 해소 + 컬럼 이동 수정

- **요청**(2026-07-20 사용자): ① 경리부(PC1)가 출고현황 상세에서 완료전 항목을 '바로접수'
  (=출고요청/접수)하면, 프린터+자동출력이 도는 교문사(PC2, 동일 hcode 다른 계정)가 3분 폴
  대기 없이 그 건만 즉시 인쇄+완료. "3분이 아니라 ~5초 이내 준실시간 감시가 백단에 돌아야."
  ② 전표 2 누락(DEC-109) 수정을 다른 명세출력 화면에도 반영(출고접수관리에서 여전히 누락).
  ③ 컬럼 순서 이동이 선택 셀 앞에 안 들어가고 한 칸 건너뜀.
- **즉시 출력 설계(왜 SSE 자가폴인가)**: Render 백엔드는 현장 프린터 직결 불가(OQ-002)라
  인쇄 루프는 반드시 브라우저 탭이어야 한다. 기존 자동출력은 이미 접수→인쇄→완료가 맞고
  **지연만 3분**이었음 — 필요한 건 지연 단축뿐. 서버 푸시 인프라(큐/웹소켓)는 없으나 IoT
  대시보드용 **SSE 자가폴 제너레이터**(`StreamingResponse`+`asyncio.sleep` 루프)와 그
  **fetch+ReadableStream 소비자**(EventSource 는 `Authorization` 헤더 불가 → fetch 로 우회)
  패턴이 검증돼 있어 그대로 재사용.
  - 백엔드: `GET /transactions/sales-statement/received-stream`(text/event-stream) +
    `transactions_service.stream_received_statements` — `received-today` 와 동일 로직
    (`list_sales_statements`+status=='received')으로 ~5초마다 현재 접수 집합을 구해 **직전
    tick 이후 새로 나타난 전표만** yield(seen=order_key JSON dedup), 신규 없으면 heartbeat.
    JWT(`get_user_context`)+`enforce_hcode_isolation`, `maxTicks` 로 스모크 바운드.
  - 프론트: 자동출력 탭이 `subscribeReceivedStatements`(fetch+reader, 백오프 재연결)로 구독
    → 새 건 즉시 인쇄+완료. **3분 폴은 안전망 유지**, `printedRef` 를 SSE·폴이 공유해 중복
    인쇄 차단. "● 실시간 감시" 배지 추가.
- **전표 흡수 해소(출고접수관리 `/outbound/orders`)**: `outbound_service.list_orders`
  GROUP BY 가 `Gdate,Hcode,Gcode,Jubun` 뿐이라 지점만 다른 전표(영풍문고 온라인 vs 종각
  종로점)가 한 행으로 합쳐져 MAX(Idnum)=3 만 보이고 전표 2 가 가려짐. GROUP BY 에
  `Gjisa`·`Idnum` 추가 + SELECT `{gjn} AS gjisa` + **order_key 에 gjisa 노출** +
  `OrderKey` 모델에 `gjisa` 필드 추가(응답 탈락 방지). 상세/수정/취소는 DEC-109 에서 이미
  gjisa 필터 지원 → 목록↔상세 정합. DEC-109(outbound-status)와 동일 grouping.
- **DataGrid 컬럼 이동 버그**: `onHeaderDrop` 이 ① 키 배열을 `c.key` 로 만들어 `id` 있는
  합성 컬럼(거래현황 일자/전표번호=order_key)은 indexOf 가 첫 동일 key 를 잡아 엉뚱한 컬럼이
  이동, ② `splice(to,0)` 이라 `from<to` 시 제거로 밀린 인덱스 때문에 타겟 **뒤**에 삽입(한 칸
  건너뜀). 수정: 키를 `id ?? key`(prefs 규약과 동일), 삽입은 `from<to ? to-1 : to`(타겟 앞).
- **검증**: `test_dec111_immediate_print_and_slip_split.py` 신설(스트림 신규-키만 방출+
  heartbeat, list_orders order_key.gjisa 분리) 2건 PASS. `test_list_count_grouped_mysql3`
  기대 GROUP BY 갱신. 프론트 tsc·eslint 0. 프로브에 received-stream(maxTicks=1) 등록.
  test_pagination_contracts 9건은 단독 통과=기존 파일간 이벤트루프 격리 순서 flakiness(무관).
- **보강(2026-07-21, 사용자 지시 — UI 트리거 누락 보완)**: 최초 요청의 핵심인 **"바로출고"
  기능 버튼**을 출고현황 상세에 추가(초기 구현은 SSE 백엔드+자동출력 구독만 넣고 명시적 버튼을
  누락). 완료전(대기/접수) 전표를 즉시 `requestDispatch`(대기→접수)로 전이 → 자동출력 PC 가
  ~5초 SSE 로 그 건만 인쇄+완료. 경리부(무프린터)에서 눌러도 교문사 PC 에서 출력됨.
  위치 3곳: ① 상세 tab '선택 전표 라인' 패널 '수정' 옆(`Sobo24.ImmediateDispatch`, 완료전만),
  ② 거래명세서 상세 팝업 `OrderDetailDialog` 헤더(`Sobo24.Detail.ImmediateDispatch`, 완료전만),
  ③ **신규 출고 주문 저장 성공 배너**('방금 저장한 주문 보기' 옆, `Sobo27.ImmediateDispatch`,
  저장→바로출고 원스텝, 2026-07-21 사용자 요청). 기존 배치 '대기 N건 출고요청'과 동일 접수 전이
  경로. 배포 커밋 `b4cca12`(상세)·`48fdb54`(신규주문 배너).
  ※ 한계: `request_dispatch` 는 **대기(Yesno='')만 접수 전이** → 이미 접수/완료 전표엔 no-op
  (재출력 안 됨). 상태 불문 '즉시 재출력'은 별도 긴급 출력 큐 필요(후속 옵션).
- **결정자**: 사용자 (2026-07-20, 버튼 보강 2026-07-21)
- **참조**: DEC-109(전표 흡수/gjisa 분리), DEC-071(과거일자 접수 days 창), OQ-002(현장
  프린터 직결 불가), IoT SSE(`stats.stream_dashboard_iot_events` 패턴),
  `auto-print-stream.ts`, `use-grid-prefs.ts`(id??key 규약)

### DEC-110: 거래관리 표 5종 공통그리드 전환 + 팝업 리사이즈

- **요청**(2026-07-20 사용자): ① 거래관리 「기타명세서」·「거래현황 하위 화면들」의 표에
  공통 목록표 기능(정렬·크기조정·순서·표시·셀선택)을 적용, ② 거래명세서 수정 팝업 폭 확대
  (카테고리 등 목록 컬럼 모두 보이게), ③ 모든 팝업창 리사이즈 가능.
- **전환 대상(5종)**: `transactions/other`(기타명세서, 선행), `transactions/withholding`(원천징수),
  `transactions/author-history`(저자별내역), `transactions/production/statement`(제작명세),
  `transactions/production/status`(제작현황), `transactions/status`(거래현황 4-view). 손수-작성
  `<table>` → 표준 `DataGrid` — 헤더 클릭 정렬 + 컬럼 너비/순서/표시(`useGridPrefs`, 계정별
  서버 저장 + `GridColumnSettings`) + 키보드 셀 선택. **합계(tfoot)는 DataGrid에 tfoot이 없어
  그리드 하단 별도 peer 요소로 보존**(값·게이팅 동일), `DataGridPager`는 `toolbarTop`로 이동.
- **거래현황(status) 특수 처리**: 4-view 단일 라우트. 평면 뷰(요약·LIST·메모)는 DataGrid로
  전환하되 **기존 sort/toggleSort 재사용**(요약=클라이언트, LIST/메모=서버 정렬 DEC-082 허용키)을
  `DataGrid.onSortChange`로 위임 — 재조회 로직 무변경. 합성 컬럼(일자/전표번호)은 `key`가
  `string & keyof T` 제약이라 실제 필드(`order_key`) + `id`로 고유식별, 정렬은 `sortKey`
  (`cid=id??key`, `sid=sortKey??key` DataGrid 규약과 일치). **상세(detail) 뷰는 전표 행
  인라인 라인 펼침(펼침 행)이라 평면 DataGrid로 표현 불가 → 손수-작성 표 유지**(헤더 클릭
  서버 정렬은 그대로). 뷰별 컬럼 세트가 달라 gridPrefs 키를 분리(prefs 충돌 방지).
- **팝업 리사이즈**: 콘텐츠 팝업 패널에 CSS `resize` + min/max 폭·높이 부여(모서리 드래그로
  크기 조절) — 거래명세서 수정(`sales-statement-edit-dialog`, 폭 `w-[min(1400px,96vw)]`로 확대)/
  출고 상세(`order-detail-dialog`)/거래현황 검색(`sales-statement-search-dialog`)/Master 검색
  (`master-lookup-dialog`). 소형 확인·비밀번호 팝업은 리사이즈 무의미 → 제외.
- **검증**: 프론트 `tsc --noEmit` 0, `eslint` 신규 0. 배포 커밋 `dd737ba`(표 4종+리사이즈)·
  `b37ce0b`(거래현황).
- **결정자**: 사용자 (2026-07-20 — "5개 전부 전환" 확정)
- **참조**: DEC-082(서버 정렬 화이트리스트), DEC-055(목록 세션 복원), DEC-107(OrderLineGrid
  컬럼 기능), `use-grid-prefs.ts`, `grid-column-settings.tsx`, `data-grid.tsx`(`cid/sid` 규약)

### DEC-109: 출고현황 전표 흡수 버그 — 같은 거래처·Jubun·다른 지점(Gjisa) 전표 분리

- **증상**(2026-07-20 사용자 리포트): 출고현황 요약/상세에 **전표 2가 안 보임**(실재로
  존재). 라이브 API 검증: 출고현황 idnum=[1,3,4,…] (2·10 누락) vs 거래명세서 idnum=[1,2,3,…]
  (2 존재).
- **정확한 원인**: 전표 2=영풍문고(00004) 온라인, 전표 3=영풍문고(00004) **종각 종로점** —
  거래처·Jubun(11) 같고 **지점(Gjisa)만 다름**. `list_outbound_status_slips` 의
  `GROUP BY (Gdate,Hcode,Jubun,Gcode)` 가 Gjisa·Idnum 을 빼서, 전표 2가 전표 3에 흡수되고
  `MAX(Idnum)=3` 만 표시 → 전표 2 소멸. 거래명세서는 `_group_by_stmt_keys` 가
  (Gdate,Hcode,Idnum,Gubun,Jubun,Gjisa,Gcode) 라 1슬립=1행으로 분리해 정상.
- **채택**:
  - GROUP BY 에 `IFNULL(Idnum,0)`·`IFNULL(Gjisa,'')` 추가(1전표=1행, MySQL3 IFNULL —
    no-coalesce 정책). SELECT/order_key 에 gjisa 노출.
  - order_key 직렬화 **5-파트**(`{gdate}|{hcode}|{gcode}|{jubun}|{gjisa}`) — 상세/수정/
    취소/요청/완료 전 경로에 gjisa 스레딩(`_parse_order_key`·`_hdr_where`·`_hdr_params`·
    `get_order_detail`·`update_order`·`cancel_order`·`_transition_yesno`). 같은 거래처·
    다른 지점 전표를 편집 시 서로 안 섞이게(DEC-080-class 데이터 안전). gjisa 빈 값은
    기존 4-파트 backward-compat.
  - 프론트: OutboundStatus/OrderKey.gjisa, slipKey(행 구분)·toOrderKey·serialize/parse.
- **검증**: 회귀 `test_group_by_includes_gjisa_and_idnum`(GROUP BY IFNULL(Gjisa/Idnum)),
  mock/파서 테스트 gjisa 반영. tsc 0. (전체 스위트 customer_name 등은 기존 flake — 격리 통과.)
- **주의**: stash 왕복 중 백엔드 변경이 2회 유실 → 재적용. 큰 백엔드 변경은 커밋 전
  git status 로 파일 포함 재확인할 것.
- **결정자**: 사용자 (2026-07-20)
- **참조**: [[slip-key-shared-and-binlog-recovery]](DEC-080 (Gdate,Hcode,Jubun) 공유키),
  [[slip-number-idnum-vs-jubun]], `_group_by_stmt_keys`(거래명세서 그룹키 정본)

### DEC-108: 전표번호 표시 정본 = Idnum (Jubun 오표시 재발 방지)

- **배경**(2026-07-20 사용자 리포트, "다른 화면에서도 계속 동일 오류 — 정확히 기록해
  두 번 실수 말라"): 출고현황 상세에서 전표 00013 더블클릭 → 편집 팝업 헤더가 "전표 11"
  로 목록과 다르게 표시.
- **정확한 원인**: 같은 S1_Ssub 전표에 두 값 공존 —
  - `Idnum` = **(Hcode, Gdate) 일자별 전표번호**(매일 1부터 채번, 슬립 전 라인 공통 1값).
    목록·거래명세서가 표시하는 **정본 전표번호**(DEC-064/099, 5자리 zero-pad).
  - `Jubun` = **거래처별 채번 차수**(Idnum 과 무관한 별개 값, 예: 11).
  일부 상세/편집 팝업이 `order_key.jubun` 을 "전표"로 그대로 표시 → 목록의 Idnum 기반
  전표번호와 달라 "번호가 틀리다"는 반복 오인.
- **채택**: 전표/슬립 번호 렌더는 **`formatIdnumDisplay(order_key.idnum) || jubun`**
  (idnum 우선, 미제공 시만 jubun 폴백)로 통일. 백엔드 detail 응답은 `order_key.idnum`
  (MAX(Idnum))을 이미 제공. `OrderDetailDialog` 헤더/PDF 요약 정정(a8cca8c).
- **감사 대상(순차 정정)**: `sales-statement/new:728`(전표 {editKey.jubun}),
  `returns/receipts:117`·`returns/inventory:195`(`{key:"jubun", label:"전표번호"}`),
  `settlement/payment-slip:202`, `inbound/receipts/[receiptKey]:271`(입고 체계 확인 요).
  영구 메모리 `slip-number-idnum-vs-jubun.md` 에 규칙·체크리스트 기록.
- **결정자**: 사용자 (2026-07-20)
- **참조**: DEC-064/099(Idnum 5-pad 정본), `sales-statement-jubun.ts` `formatIdnumDisplay`,
  [[slip-key-shared-and-binlog-recovery]]((Gdate,Hcode,Jubun) 공유키)

### DEC-107: 주문 라인표(OrderLineGrid) — 컬럼 표시·순서·크기 + ESC 포커스 복원 + 품명→도서명

- **배경**(2026-07-20 고객 리포트, 신규 출고 주문/주문 상세 라인표):
  ① 도서 검색 팝업 ESC 후 커서가 코드칸이 아닌 검색버튼/공백에 있어 엔터·탭 먹통,
  ② 컬럼 헤더 "품명" → "도서명", ③ 자동완성 선택 시 "코드가 안 들어가고 텍스트만"
  (재현 결과 정상 — 아래), ④ 라인표에도 표준 목록표의 컬럼 표시·순서·크기 기능,
  ⑤ 크기조정 세로바가 안 보임. + "롤백됐다" 오인.
- **조사·판정**:
  - "롤백" 아님 — 제품 저장소 HEAD=최신 커밋, 모든 작업 존재(sync 커밋은 전부 이전).
  - "자동완성 코드 미입력" 아님 — 재현 결과 자동완성은 **G4_Book.Gcode(실제 도서코드)**
    를 입력. 교문사 도서마스터엔 Gcode 가 한글 텍스트인 도서("헤어리베치"=코드,
    "휴가실태"=코드)와 숫자코드("00001")가 혼재. 시스템 전체가 `Gcode AS bcode` 사용 →
    데이터 특성이지 화면 버그 아님(필요 시 도서마스터 데이터 점검 별도).
- **채택**:
  ① `MasterLookupField`: 검색 팝업이 **선택 없이(ESC/취소)** 닫히면 코드 입력칸으로
     포커스 복원(`wrapRef` 내 input 조회). 선택으로 닫힌 경우는 호출자가 다음 칸
     이동 담당이라 제외(`selectedInDialogRef`).
  ② `column-labels.ts` `product_name`/`pname` "품명"→"도서명"(공용 라벨 → 전 화면).
  ④ OrderLineGrid 렌더를 **컬럼 id 구동**(`renderCell`)으로 재구성 + `useGridPrefs`
     (서버 저장, key `outbound.order-line`) + `GridColumnSettings`(⚙) + 헤더 드래그(순서)
     + 우측 경계 드래그(너비). **행 정렬은 입력 순서 유지 위해 제외**(AskUserQuestion
     으로 사용자 확정). 인라인 편집·자동완성·키보드 이동 전부 보존, Enter 셀 이동은
     표시 순서(DOM)를 따름. 헤더/합계(tfoot)도 표시 컬럼 기준 동적 렌더.
  ⑤ 크기조정 핸들을 hover-only 투명 → **항상 보이는 얇은 세로 구분선**(bg-border,
     hover 시 primary 강조 + 그립 확대).
- **검증(실화면, 교문사 remote_153, CDP)**: 헤더 도서명 반영 ✅, 컬럼 설정 버튼 ✅,
  구분 Enter→도서코드(키보드 유지) ✅, ISBN 표시/숨김 ✅, ESC 후 코드칸 복귀(코드 유지).
  tsc 0, eslint 0(기존 setMenuRect set-state-in-effect 1건 잔존, empty-state 따옴표
  정리로 no-unescaped-entities 1건 해소).
- **결정자**: 사용자 (2026-07-20)
- **참조**: [[DEC-104]], [[DEC-105]], DEC-028(위젯 data-legacy-id), `use-grid-prefs.ts`,
  `grid-column-settings.tsx`, `master-lookup-field.tsx`, `column-labels.ts`

### DEC-106: 출고현황(Sobo24_status) 4개 항목 — 날짜 당일 기본·탭 순서·목록 상하 교체·상세 인라인 수정

- **배경**(2026-07-20 고객 리포트 2번, `/transactions/outbound-status`):
  ① 날짜 시작~종료 기본이 1개월 텀 → 접속 당일로, ② 탭 목록/상세/요약 순 →
  상세/요약/목록 순(+열면 상세가 기본), ③ 목록 뷰 상단 도서세부·하단 거래처집계 →
  위치 교체, ④ 상세 우측 라인 패널(읽기전용)에서 도서 출고 수정+저장.
- **채택**:
  1. `dateFrom` 기본값 `fmtDate(monthAgo)` → `fmtDate(today)` (2곳: 초기 state +
     reload eDateFrom), `monthAgo` useMemo 제거. snap(리스트 세션) 값이 있으면 우선.
  2. `parseView` 기본값 `list`→`detail`(파라미터 없을 때), 탭 렌더를
     `Object.keys(VIEW_LABELS)` → 명시 `VIEW_ORDER=["detail","summary","list"]`.
  3. 목록 뷰 Fragment 내 두 블록(라인 목록 / 거래처 rollup) 순서 교체.
  4. 상세 우측 패널에 '수정' 버튼(`Sobo24.EditSlip`) + 좌측 전표 더블클릭 → 편집 팝업.
     **팝업 정정(2026-07-20 사용자 리포트: 로딩 실패)**: 처음엔 `SalesStatementEditDialog`
     를 썼으나 그 팝업은 **StatementKey(gjisa 키)** 기반이고 출고현황 전표는
     **OutboundStatusOrderKey(gcode 키)** 라 키 불일치로 라인 로딩 실패 →
     **`OrderDetailDialog`(gcode 키·`outboundApi.detail`, 좌측 라인 조회와 동일 키)** 로
     교체해 로딩·저장·취소·명세서 PDF 정합. 좌측 DataGrid `onRowDoubleClick`→편집 오픈,
     `onChanged`→`load(0)`+선택 라인 재조회. 실검증: 더블클릭→라인 49개 로딩+저장버튼 ✅.
- **판단(사용자 확인)**: ② 기본 탭=상세, ④ 인라인 그리드 대신 **편집 팝업 재사용**
  (기존 팝업 방식과 일관·저위험) — AskUserQuestion 으로 확정.
- **검증(실화면, 교문사 remote_153, CDP)**: ① from/to=당일 ✅, ② 탭 상세(기본)/요약/
  목록 ✅, ③ 목록 거래처집계(상단)→도서세부(하단) ✅, ④ 당일 12전표→전표 선택→'수정'
  노출→클릭→편집 팝업(Sobo21.EditDialog) 오픈 ✅. tsc 0, eslint 0.
- **추가 요청**(2026-07-20, 스크린샷): 출고접수관리(`/outbound/orders`, "출고 접수" 목록)
  도 신규 화면 진입 시 시작일=종료일=당일. `dateFrom` 기본값 `formatDate(lookbackDay)`
  (today−90일) → `formatDate(today)` (초기 state + reload eDateFrom 2곳), `lookbackDay`
  useMemo 제거. snap 값 우선은 동일.
- **추가 요청 3 — 출고접수 전표번호 정렬 불일치**(2026-07-20 스크린샷: ▲ 오름차순인데
  00014→00003→00007): 전표번호 컬럼 표시=Idnum(DEC-064/099 정본)·정렬키=jubun(거래처별
  차수) 불일치. 백엔드 `_list_order_by_sql` 화이트리스트에 `"idnum"`→SELECT 별칭
  (`MAX(Idnum+0) AS idnum`) 정렬 추가(DEC-082 별칭 패턴, MySQL 3.23 안전), 프론트
  sortKey `jubun`→`idnum`(컬럼 id 불변 — 그리드 프리퍼런스 유지). 회귀:
  `test_outbound_list_server_sort.py::test_idnum_sort_uses_select_alias`. 실화면 검증:
  헤더 클릭 → 00001,00003,00004,… 오름차순 PASS.
- **추가 요청 2 — 거래명세서**(2026-07-20, 고객 리포트 3번, `/transactions/sales-statement`):
  ① 날짜 7일 텀 기본 → 시작=종료=당일 (`weekAgo` 제거, `fmtDate(weekAgo)`→
  `fmtDate(today)` 3곳: 초기 state·reload eDateFrom·저장 후 필터 복원 sFrom).
  ② 조회 버튼(Sobo21.dxButton1) 거래처명 옆(첫줄) → 상세조건 둘째줄 시작일·종료일·
  당일만 옆으로 이동. 상세조건 접힘 시엔 첫줄에 조건부 렌더(항시 접근 보장, DOM 1개 —
  DEC-028 위젯 id 커버리지 유지).
- **결정자**: 사용자 (2026-07-20)
- **참조**: DEC-097(거래명세서 편집 팝업), `SalesStatementEditDialog`, Sobo24/Subu24, Sobo27

### DEC-105: 키보드 Enter=다음 컴포넌트 이동 공통 정합 (DEC-104 확장)

- **배경**(2026-07-20 사용자 지시): DEC-104(출고 신규주문)에서 쓴 Enter=다음 필드/셀
  이동 패턴이 공유 컴포넌트라 다른 화면에도 동일 갭 존재 여부 조사·일괄 수정.
  원칙 "모든 입력은 키보드로 다음 컴포넌트 이동 가능". 브라우저 실검증 기반.
- **조사 결과**(공유 프리미티브 = `lib/focus-advance.ts` `advanceFocusOnEnter`,
  컨테이너에 `onKeyDown` 한 줄 부착 → 내부 input/select Enter 시 다음 focusable 이동;
  textarea·dropdown 열림·`data-enter-advance="off"` opt-out):
  - **이미 준수**: 출고 수정(`[orderKey]`)·`order-detail-dialog`(OrderLineGrid 상속),
    `sales-statement/new`(DEC-097 정본), master customer/book/author/inbound-vendor 폼.
  - **갭 수정 대상**:
    (a) `etc-customer-detail-form` — 형제 4개와 달리 유일하게 핸들러 누락 → 부착.
    (b) 입고 신규 — 헤더 `data-enter-scope` 부여(입고처→지사 스코프 견고화),
        비고 Enter → 새 라인 추가+새 라인 도서코드 포커스(기존 막힘 해소, ref+effect).
    (c) 반품 신규 — 페이지 단일 `data-enter-scope`+`advanceFocusOnEnter`(헤더→그리드
        Enter 흐름), `return-line-grid` 비고 Enter → 새 라인+포커스(ref 보관, effect 내
        setState 회피 — `react-hooks/set-state-in-effect` 대응).
    (d) 거래명세서 수정 팝업 — 편집 가능한 거래일자 Enter → 첫 라인 구분 셀로 이동.
- **범위 제외(중요)**: 검색/목록/필터 화면(master 목록, returns 목록, settlement/cash,
  stats/* 등)은 이미 **Enter=조회/submit** 의도 → `advanceFocusOnEnter` 부착 시 검색을
  깨는 회귀. 원칙은 데이터 입력 폼에만 적용, 검색창 Enter=조회는 레거시 표준 유지.
- **검증(실화면, 교문사 remote_153, CDP 워크스페이스 창 주입)**: 입고 비고 Enter 행
  1→2·새행 도서코드 ✅, 반품 헤더 반품일 Enter→출판사코드·비고 Enter 행 1→2·새행
  도서코드 ✅, 기타거래처 첫 필드 Enter Edit101→Edit102 ✅. tsc 0, 신규 eslint 에러 0.
- **결정자**: 사용자 (2026-07-20)
- **참조**: [[DEC-104]], `lib/focus-advance.ts`, `master-lookup-field.tsx` `focusNextFrom`

### DEC-104: 출고접수관리 신규주문 Enter/포커스 흐름 정합 (거래처→지사→구분→도서코드→공급율)

- **배경**(2026-07-20 고객 리포트, `/outbound/orders/new` = 출고접수관리 신규주문):
  ① 거래처명 Enter 시 지사로 이동 안 함, ② 단독/무지사 거래처(예: 알라딘) 선택 후
  키/클릭 먹통·라인 진입 불가, ③ 구분(pubun)이 건너뛰어져 선택 불가·바로 도서코드로,
  ④ 도서코드 Enter 후 공급율로 이동 안 함.
- **원인**(코드 조사): 지사 Enter 핸들러 `focusFirstBcode` 가 **구분을 건너뛰고 도서코드로
  점프**, 구분 select 에 `onKeyDown` 부재(Enter 무반응), 거래처 확정→지사 포커스 이동
  로직 부재(+지사 비동기 로드), 헤더에 `data-enter-scope` 부재로 자동완성 내부 포커스도
  어긋남, 도서 선택 후 공급율 포커스 이동은 키보드 확정 경로만(마우스 클릭 누락).
- **채택**(거래명세서 신규 DEC-097 보강4 검증 패턴 재사용):
  1. 거래처 확정(onSelect/onInlineSelect)→`focusGjisa` 비동기 대기 후 지사 포커스
     (`branchesForHcodeRef`+nonce, 지사 없으면 첫 구분으로 폴백 — 단독/무지사 거래처도
     흐름 유지). 헤더에 `data-enter-scope` 부여.
  2. 지사 Enter → `focusFirstPubun`(첫 라인 구분 셀, `Sobo27.Line.Pubun`).
  3. OrderLineGrid 구분 select `onKeyDown`: Enter → 같은 행 도서코드.
  4. 도서 확정(onSelect/onInlineSelect 공통)→ 같은 행 공급율(grat1) 포커스
     (`grat1Refs`+focus 인덱스 effect) — 마우스/키보드 전 경로 커버.
  5. 비고(메모) Enter → 새 라인 추가 후 **새 라인의 "구분"으로 포커스**(기존엔 새 라인
     도서코드로 이동 → 구분 선택 흐름 반복 불가). `pubunRefs`+focus 인덱스 effect.
- **항목 매핑(고객 8개 세부요구)**: ①거래처Enter→지사, ②지사Enter→구분, ③구분Enter→
  도서코드, ④단독/무지사 거래처도 지사 지나 구분 도달, ⑤단독거래처 키/클릭 먹통 해소,
  ⑥구분 선택 가능(프리패스 제거), ⑦비고Enter 후 새 라인 구분 선택, ⑧도서코드→공급율.
- **검증**: tsc 0, eslint 신규 이슈 0(기존 2건 잔존), dev 라우트 200.
  - **실화면 E2E(2026-07-20, 프로덕션 books-logistics-web.vercel.app, 교문사 계정
    remote_153/hcode 5019, CDP WebSocket connectOverCDP 로 workspace iframe 구동)**:
    거래처 "북" 검색 10건→첫 결과 `[X]#(주)월드북센타*`(무지사) 선택 →
    ① 활성=`gjisa`(지사) ✅, ② 지사 Enter→`Sobo27.Line.Pubun`(구분) ✅,
    ③ 구분 Enter→`Sobo27.Line.Bcode`(도서코드) ✅, ⑧ 도서 "회계19"(국가회계편람2019)
    선택→공급율(%) 셀(colIdx 5, value 85) 포커스 ✅. 무지사 거래처인데도 지사(폴백
    입력)→구분 도달 = ④ 실증, 라인 생성·키/클릭 정상 = ⑤ 실증. ⑦(비고→새 라인 구분)은
    실 OrderLineGrid 컴포넌트 playwright 검증에서 lines 2→3·새 라인 구분 포커스 PASS.
  - E2E 도중 공급율 입력만 `data-legacy-id` 누락 발견(포커스 대상이 base-ui 자동 id 로
    표시) → `Sobo27.Line.Grat1` 보강(속성만 추가, 동작 불변).
  - playwright-core+Node25 는 `--remote-debugging-pipe` 로 대용량 CDP 이벤트(거대한 JWT
    헤더 ~7.5KB) 파싱 시 크래시 → **connectOverCDP(WebSocket)** 로 우회해야 함.
- **보강 — 엔터 리듬 일정 원칙(2026-07-20 사용자 의견, 최종)**: 레거시(위러브)는
  거래처명→지사→구분→도서코드를 **항상 같은 엔터 횟수**로 통과(엔터→팝업→선택 엔터→
  닫힘→다음) — 필드 자동 건너뛰기는 습관적 엔터 횟수를 바꿔 입력 오류·리듬 붕괴.
  - 1차 시도(무지사→구분 자동 건너뛰기, fdd012a)는 이 원칙 위반으로 **철회**.
  - 진짜 원인 = **비동기 공백**: 지사 목록 로딩 중 `<p>` 플레이스홀더만 렌더 →
    입력 컨트롤 부재 구간에 빠른 엔터가 삼켜져 "스톱"으로 체감.
  - 최종 채택(출고 신규주문 + 거래명세서 신규 동일 적용): ① 로딩 중에도 지사/지점
    Input 유지("지점 확인 중… (Enter로 통과)") + 거래처 확정 **즉시** 포커스(로드
    대기 없음), ② 무지사여도 지사에 서고 Enter 로 통과(엔터 횟수 일정), ③ 로드
    완료 시 select 교체 포커스 이어받되 사용자가 이미 지나갔으면(Enter 핸들러에서
    플래그 해제) 포커스 강탈 금지.
  - 실검증(프로덕션): 무지사 확정직후 지사 포커스→Enter→구분→Enter→도서코드 ✅,
    빠른 연속 Enter×2(로드 완료 전)도 도서코드 도달+강탈 없음 ✅, 지사有(교보문고)
    로드 후 select→Enter→구분 ✅, 거래명세서 신규 동일 ✅.
  - 리듬 감사(동일 위험 전수 점검): 입고 신규 지사=동기 Input(공백 없음) OK,
    MasterLookupField Enter=정확일치/1건 자동확정·다건 팝업→Enter 선택→다음(레거시
    정합) OK, 도서 확정→다음 셀=동기 OK.
- **결정자**: 사용자 (2026-07-20)
- **참조**: DEC-097 보강4(거래처→지점 포커스), `order-line-grid.tsx`, Subu27

### DEC-103: 사용자 화면 텍스트에서 레거시 참조 제거 — 전 화면 스윕

- **배경**(2026-07-18, 사용자 지시): 화면 부제목·설명 앞의 레거시 화면번호·테이블명
  (예: "Sobo11 · G1_Ggeo/G1_Gbun ·")이 일반 사용자에게 불필요 — 전 화면에서 제거.
- **채택**: 화면에 **보이는 텍스트**에서만 레거시 토큰 제거 — 레거시 화면코드
  (Sobo/Subu/Seep/Menu###), 레거시 테이블/컬럼명(G#_XXX, S#_XXX, T#_XXX, Sg_Csum,
  Id_Logn, DBGrid### 등), 코어 시나리오 코드(C1~C15), DEC/NAV 참조, .pas/.dfm 파일
  참조, caps/variant/버전 태그를 부제목·설명·카드 desc·섹션 헤더·탭 라벨·옵션·라벨·
  placeholder·확인창·헤더 툴팁에서 삭제하고 자연스러운 한국어 설명만 남김. 허브
  카드의 "레거시: SoboNN" 배지(`<p>레거시:{c.legacy}</p>`) 렌더 제거.
- **불변 유지(중요)**: 테스트가 의존하는 `data-legacy-id` 속성, DataGrid 컬럼
  `legacyId`, 코드 주석, form-registry id, `useScreenCaps`, `const LEGACY_ID`,
  `V_LABEL`/`menuId`, 그리고 master 허브의 `legacy:` 데이터 필드(data-legacy-id 생성에
  사용)는 **모두 그대로**. admin 전용 계정군 코드(T2_DIST/T2_PUB/dist_hcode)는 실제
  선택값이라 유지.
- **범위**: 프론트 ~50개 파일, ~95개 문자열(순수 문자열 편집 + master 허브 `<p>` 1개
  제거, 로직/구조 변경 0). 4개 병렬 편집 에이전트로 분담 처리.
- **검증**: 보이는 텍스트 레거시 토큰 grep 0(admin 계정군 코드 제외), tsc 0 에러,
  eslint 신규 이슈 0(전부 기존), 라우트 6종 200 컴파일. DEC-028 data-legacy-id
  커버리지 테스트(TC-RT-P2-30 등) 유지.
- **결정자**: 사용자 (2026-07-18)
- **참조**: DEC-028(위젯 data-legacy-id 추적성 — 속성은 유지)

### DEC-102: 기간별 재고원장 상세 — S1_Ssub 재고변동 컬럼 부재 테넌트 500 해소

- **증상**(2026-07-17): 기간별 재고원장 "도서별 누계"에서 도서 행 선택 시
  `returns_ledger_failed: OperationalError (1054, "Unknown column 's.Giqut'")` 500.
- **원인**: 상세 SQL(SQL-RT-29, `SQL_LEDGER_DETAIL`)이 `S1_Ssub` 에서
  `Giqut/Gisum/Goqut/Gosum/Gjqut/Gjsum/Gbqut/Gbsum` 재고변동 컬럼을 **고정 SELECT** —
  해당 컬럼이 없는 테넌트(DDL drift)에서 1054. `ORDER BY s.Idnum` 도 Idnum 부재
  테넌트에서 동일 위험. (마스터/summary 는 core 컬럼만 써서 정상이라 선택 시에만 발현.)
- **채택**(DEC-033 어댑터 패턴): `_build_ledger_detail_sql(server_id)` 신설 —
  `s1_column_names` 로 존재 컬럼만 `COALESCE(s.Col,0) AS alias`, 부재는 `0 AS alias`,
  Idnum 부재 시 ORDER BY 에서 제거. 상세 경로(`detail_for_bcode`)에서만 호출(마스터
  경로·기존 테스트 무영향). alias 는 전부 유지(프론트 계약 보존). `SQL_LEDGER_DETAIL`
  상수는 회귀 가드 토큰 매처용으로 잔존.
- **검증**: `test_dec102_ledger_detail_ddl_drift.py` 신설(부재 컬럼 참조 0·alias 유지·
  Idnum ORDER BY 제거 / 존재 컬럼 COALESCE 참조). 반품·원장 서브셋 pre/post 비교
  신규 회귀 0건.
- **결정자**: 사용자 (2026-07-17 리포트)
- **참조**: DEC-033(다중 DB/DDL drift 어댑터), `s1_ssub_adapt.s1_column_names`
- **보강(2026-07-18, 사용자 지시 — 상세/라인 표 표준화)**: 기간별 재고원장
  "일자별 트랜잭션"(Sobo34_4.DBGrid201)·기간별 반품내역서 "반품 라인"(Sobo58.DBGrid201)
  디테일 표가 수제 `<table>` 이라 표시/숨김·정렬·컬럼순서·너비 조절 미지원(마스터
  그리드만 표준). 두 디테일 표를 공용 `DataGrid` + `useGridPrefs`(별도 키
  `returns.ledger.detail` / `returns.period-report.detail`, 계정별 서버 저장) +
  `GridColumnSettings` + `useClientSort`(숫자 컬럼 수치 정렬)로 전환. `<th>`
  data-legacy-id 는 컬럼 `legacyId` 로 1:1 보존(DEC-028 커버리지 TC-RT-P2-30 유지).

### DEC-101: 수량 입력 컨트롤 ↑/↓ 값 증감 — 전 화면 공용 키 처리

- **배경**(2026-07-17, 사용자 지시): 수량 입력 컨트롤이 날짜 입력처럼 키보드 상/하로
  숫자를 +/− 할 수 있어야 함. 이어서 "모든 수량 컨트롤에 동일하게 적용" 지시.
- **원인**: 신규 명세서 그리드(Sobo21.NewForm)는 `onCellKeyDown` 이 ↑/↓ 를 **행 이동**
  으로 가로채(preventDefault) 네이티브 number 스피너를 막고 있었음. 나머지 수량
  입력들은 `type="number"` 네이티브 +/− 는 되나 증감폭·음수방지 편차가 존재.
- **채택**: 공용 헬퍼 `lib/qty-input.ts::handleQtyArrowKey(e, current, setValue, min=0)`
  신설 — ↑ +1 / ↓ −1(min 미만 방지, 기본 0), 처리 시 true 반환(그리드 행 이동 등
  상위 화살표 동작 스킵), IME 조합 중 무시. **편집 가능한 수량 컨트롤 8곳 전부** 적용:
  신규 명세서 그리드(gsqut 셀 — 행 이동보다 우선), 출고 order-line-grid,
  입고 inbound-line-grid, 반품 return-line-grid(min=1), 거래명세서 전체수정/한줄수정
  팝업, 반품 접수 상세 페이지, 입고 접수 신규 페이지. 기존 Enter 셀 이동 핸들러
  (focusNextCell/enterTo)는 화살표 미처리 시 그대로 위임돼 공존. 읽기전용 재고 필드
  (book-detail-form)는 제외.
- **검증**: tsc 0(helper 타입 `KeyboardEvent<Element>` 로 select/input 공용 셀 핸들러
  호환), eslint 신규 이슈 0(기존 이슈 잔존), dev 라우트 4종 200. 백엔드 무변경.
- **결정자**: 사용자 (2026-07-17)
- **참조**: DEC-097(신규 명세서 그리드 Enter 열 걷기·onCellKeyDown), `lib/qty-input.ts`

### DEC-100: 전자책 판매분석(구 DEC-092) 기능 제거 — 불필요 메뉴

- **배경**(2026-07-17, 사용자 지시): 통계관리 하위 "전자책 판매분석" 메뉴는 불필요 —
  제거 요청. (DEC-092 로 교문사 전자책 워크북 흡수용으로 신설했던 웹 전용 화면.)
- **채택**: 기능 전체 제거 — 프론트 페이지(`stats/ebook-sales/page.tsx`) +
  form-registry 항목(`Stats_ebook_sales`) + stats-api 클라이언트(`ebookSalesApi`
  + 타입) 삭제; 백엔드 stats 라우터의 `/ebook-sales*` 6개 엔드포인트 +
  `ebook_sales_service.py` 삭제(미사용된 `UploadFile`/`File` import 정리);
  회귀 테스트 `test_dec092_ebook_sales.py` 삭제; probe 매트릭스 2개 항목 제거.
- **데이터 보존**: 사용자 입력분이 있는 사이드 테이블 `Web_Ebook_Sales` 는 **DDL/데이터
  미변경**(API 만 제거) — 되살릴 경우 데이터 그대로 재연결 가능.
- **검증**: 백엔드 app import OK(stats 라우트 19개, ebook 0), 프론트 tsc 0(생성
  `.next/types` stale 정리 후)·eslint 0, 통계/c13 서브셋 63 PASS. 전 스위트 수집
  오류 0(삭제 서비스/테스트 잔여 참조 없음). 라우터 hcode 감사 critical 0.
  잔여 참조는 제거 안내 주석 2개(form-registry·stats-api)뿐.
- **결정자**: 사용자 (2026-07-17 — 불필요 메뉴 제거 지시)
- **참조**: DEC-092(원 신설), `masters-export-import-ebook.md`(별개 도서 전자책
  ISBN/가격 `book_ebook_service` — 본 제거와 무관, 유지)

---
*최종 업데이트: 2026-07-17 — DEC-100 신규 (전자책 판매분석 기능 제거 — 프론트
페이지/백엔드 라우트/서비스/테스트/probe 삭제, Web_Ebook_Sales 데이터 보존).
직전: DEC-097 보강3(거래명세서 인라인 필터 Enter) + DEC-098 데이터 조치 완료(교문사
통계 8셀 read) + DEC-099 보강(정렬 헤더 인디케이터·전표번호 경고 오표시).*
*직전: 2026-07-16 — DEC-097 신규 + 보강 (거래명세서 Enter=저장·선택·진행
정합), DEC-098 신규 (교문사 통계 권한 정합 — 사이드바 별칭 인식 + /stats/publisher
게이트 settlement.report.read 통일), DEC-099 신규 (전표번호 Idnum 표기 통일 +
거래현황 컬럼 정렬 + 창 닫기 시 목록 검색세션 초기화). 직전: DEC-096.*
*직전: 2026-07-09 — DEC-096 신규 (로그인 조직 선택 챌린지 — 동일 ID+PW
크로스 DB 672건, 409 ORG_SELECT_REQUIRED + tenantId/dbName 재제출). 직전: DEC-095.*
*직전: 2026-07-09 — DEC-095 신규 (비-기본 DB 테넌트 0건 — 테넌트 DB 요청
컨텍스트 신설, rdb 클레임 적용). 직전: DEC-094.*
*직전: 2026-07-09 — DEC-094 신규 (청구서 인쇄 복구 — Sum38/39 유령 컬럼
동적화 + 월키 정규화). 직전: DEC-093.*
*직전: 2026-07-08 — DEC-093 신규 (반품관리 전면 정비 — Ocode/Yesno/날짜/스코프
데이터 정상화 + inventory 후보목록 신설 + 공통그리드·키보드·엑셀). 직전: DEC-092.*
*직전: 2026-07-08 — DEC-092 신규 (전자책 판매분석 — Web_Ebook_Sales 사이드
테이블 + 입력폼/업로드 + 서식 2종(연간/월범위) 엑셀). 직전: DEC-091 보강.*
*직전: 2026-07-08 — DEC-091 보강 (도서별년말집계 월단위 T00=1 전체집계 복원 +
분기손익 T2 미집계 근본대응: S1−R3 원천 폴백 + 손익 청구−입금(T5) 정본). 직전: DEC-091 신규.*
*직전: 2026-07-08 — DEC-091 신규 (정산관리 9화면 전면 정비 — 월키·Yesno·출판사
스코프 데이터복구 + 공통그리드·룩업·엑셀 + 발송비 T1_Ssub 실이식). 직전: DEC-090.*
*직전: 2026-07-08 — DEC-090 신규 (T2 정산 도메인 hcode 주입 부적합 — 출판사
행 스코프 헬퍼 신설, 분기손익 0원 3차 원인). 직전: DEC-089.*
*직전: 2026-07-08 — DEC-089 신규 (분기손익 Yesno 제외 제거 + 차트 매입 시리즈 +
통계 전 화면 엑셀 export). 직전: DEC-087/088.*
*직전: 2026-07-08 — DEC-087/088 신규 (통계 목록 최종거래일 정렬 필드 +
분기 N개 비교 고도화·월 컬럼 키 교정). 직전: DEC-086.*
*직전: 2026-07-08 — DEC-086 신규 (기간별 매입·매출 월/분기/년 + 엑셀 export +
통계 그룹 R/W3 배지 완료). 직전: DEC-085.*
*직전: 2026-07-08 — DEC-085 신규 (분기/반기 손익 0건 — T2_Ssub 점 구분 월키
정규화). 직전: DEC-084.*
*직전: 2026-07-08 — DEC-084 신규 (통계·원장 완료 거래 미조회 사고 — Ocode 스코프
기본 전체화 + Subu62 무필터 복원 + 통합원장 파라미터 순서 버그 수정). 직전: DEC-083.*
*직전: 2026-07-08 — DEC-083 신규 (통계관리 12화면 전면 정비 — 계정코드 기본 검색
조건 정책 + 거래처/도서/출판사 검색 시맨틱 교정 + 출판사통계 Hcode 축 수정). 직전: DEC-082.*
*직전: 2026-07-07 — DEC-082 신규 (재고관리·재고원장 7화면 공통 그리드 정비 — 서버
정렬 축/비축 아키텍처 + 룩업 + BLS_BOOK_SALES_MAX 상한). 직전: DEC-081.*
*직전: 2026-07-06 — DEC-081 신규 (출고접수 목록 Yesno='2'=완료 항상표시, HAVING 취소
제외 제거). 직전: DEC-080.*
*직전: 2026-07-06 — DEC-080 신규 (거래명세표 대량 소실 사고 — binlog 복원 90라인 +
전표 키 스코프 fail-closed 강제 + Render 재배포 필요). 직전: DEC-079.*
*직전: 2026-07-05 — DEC-079 신규 (거래처 구분별 접두 채번 A~K[I제외]+검색 Enter 네비+목록
선택 컬럼 13종). 직전: DEC-078.*
*직전: 2026-07-05 — DEC-078 신규 (거래명세서 거래일자 변경 허용 — Gcode 정밀 스코프 이동,
Idnum 유지·중복 허용 사용자 합의). 직전: DEC-077.*

*직전: 2026-07-05 — DEC-077 신규 (거래명세서 수정 저장 시 거래처 Gcode·전표번호 Idnum
소실 버그 수정 — desired diff 가 Gcode 를 hcode 로 덮던 회귀). 직전: DEC-076.*

*직전: 2026-07-04 — DEC-076 신규 (삼련 반품처 세로문구 — WeasyPrint writing-mode 미지원
확인, 글자별 `<br>` 줄바꿈으로 대체). 직전: DEC-075.*

*직전: 2026-07-04 — DEC-075 신규 (삼련 마지막 련 auto-height + 하단 padding/border 제거 —
3×99.7mm 피치가 A4 297mm 초과해 2페이지로 분리되던 버그 수정, WeasyPrint 실측으로 검증). 직전: DEC-074.*

*직전: 2026-07-04 — DEC-073 신규 (로고·도장 이미지 DB 영속화 — Web_Print_Assets base64 정본 + 파일 캐시 + 히드레이션, Render 도장 인쇄 복원). 직전: 2026-07-03 — DEC-069~072.*

*이전: 2026-07-03 — DEC-072 신규 (출력된 건만 완료 전이 X-Printed-Keys + Web_Print_Log 상세 이력 + received-today days 조회창 + 출고현황 라인 거래처명). 같은 날: DEC-069/070/071.*

*직전: 2026-07-03 — DEC-071 신규 (일괄 출고요청 — 대기 전표 선택 접수 전이, 배치 API + 두 화면 UI). 같은 날: DEC-069/070.*

*직전: 2026-07-03 — DEC-070 신규 (내정보 preferences DB 정본화 — Render 임시 FS 재배포 리셋 → Web_User_Prefs 사이드 테이블 정본 + 파일 캐시 + back-fill, 회귀 9종). 같은 날: DEC-069 신규+보강.*

*직전: 2026-07-03 — DEC-069 신규 (배포-안전 저장소 상대 경로 탐색 — Render Docker `/app` 얕은 경로에서 `parents[4]` IndexError 로 거래명세서 PDF 500 → `app/core/repo_paths.find_repo_file` 상위 탐색 헬퍼 + `backend/data/contracts/print_sales_statement.yaml` 번들 사본 + Dockerfile fonts-nanum. 회귀 가드 test_print_repo_paths_deploy.py 4종).*

*이전: 2026-06-20 — DEC-066 신규 (부서계정 경리부 전 화면 CRUD = 로그인/리프레시 시 업무 Fxx 전부 'O' 효과매트릭스로 permissions·fxx_caps 승격, login_profile·license_keys 는 원본 유지로 메뉴 무변경, 관리자 플랫폼 Fxx 제외 + JWT permissions 한도 30→64 + BLS_FULL_CRUD_LOGIN_IDS env / MENUVIS-DEC-06 사이드바 가시성 매트릭스 기준 환원 — canAccessScreen 게이트 제거). 직전: 2026-06-14 — DEC-065 + P4 보강 (거래명세서 Sobo21 화면 내 신규추가 — outbound create_order 재사용 + 단가/비율/금액 패리티 + 직전거래가 G7_Ggeo 게이트 + 키보드 전용 in-grid / P4: 거래현황(상세) Subu24 검색 다이얼로그 — bcode/pubun 라인 필터 + 듀얼그리드 + 키보드 전용 모달).*

*이전: 2026-06-01 — DEC-064 신규 (C6 Sobo21 Gjisa variants + 참고 패널 memo_preview Phase 1; Label104 재고는 Phase 2 PrinJing).*

*과거: 2026-05-31 — DEC-059 운영 보강(기초관리 W3 종료 + RU/CRUD 정합). `form-registry.ts` master 그룹의 `roadmapWave: "p3"` 라벨 제거(미설정=p2 기본값), Sobo14 `crudParity` RU→CRUD 상향(상세 삭제 Button103 복원), Sobo16_special RU→CRUD 상향(POST/DELETE + UI + 계약·테스트 동기화). `docs/crud-backlog.md` §2.1 최신화, `analysis/layout_mappings/Sobo14.md`/`Sobo16.md` 이벤트 표 갱신, `analysis/audit/phase1-component-fidelity.md` note 동기화, `test_form_registry_metadata`·`test_masters_special_g6`·`test_master_crud_api_contract` 회귀 가드 확장.*

*과거: 2026-04-23 — DEC-059 신규 추가 (메뉴 메타 3축 분리 — `phase`/`roadmapWave`/`crudParity` 직교 분리). 사용자 요청 "P3/P4 단계로 진행해야할 부분이 있으면 표기하고자 한다" + "CRUD 동등성도 같이 보고싶다". 결과: ① `docs/menu-roadmap-waves.md` 신규(정책 단일 원천 — 3축 정의 + 사이드바 배지 규칙 + tooltip 템플릿 + 정적 가드 §5). ② `docs/crud-backlog.md` 신규(CRUD gap matrix 1차 인벤토리 + G0~G4 보강 절차 + P2/P3/P4 우선순위 권고). ③ `FormMeta` 에 `roadmapWave`/`crudParity`/`crudNotes` 3 필드 추가, 식별된 R/RU/STUB 행 일괄 채움(마스터 6 + 정산 5 + 통계 6 + 반품/원장/감사/택배/특별 등). ④ 사이드바에 보조 배지 2개(`R`/`RU`/`STUB` 회색 outline + `W3`/`W4` sky outline) + tooltip 한 줄 자막. ⑤ `dashboard/data/phase2-screen-cards.json` `$comment` 에 `form-registry` 단일 원천 + 동기화 의무 명시(다음 사이클 일괄 채움 예정). ⑥ 정적 회귀 가드 `test/test_form_registry_metadata.py` 신규 — 허용값 검증 + `phase1` + R/RU/STUB 행은 `crudNotes` 또는 blocker 사유 보유 강제. 검증: pytest PASS(form-registry 메타 가드 신규) · tsc 0 · ReadLints 0.*

*과거: 2026-04-23 — DEC-033 (d++) 보강 (반품 화면 2종 동시 핫픽스 — `returns_service.ledger_query` derived-table → `count_grouped` 헬퍼 + `SQL_PERIOD_MASTER` G1_Ggeo+`g.Hcode=''` → G7_Ggeo 단일키 출판사 lookup, 레거시 `Subu58.pas:376` 패턴 1:1). 사용자 보고 "기간별 반품 내역서 화면에 거래처명이 출력되지 않는다" + "기간별 재고원장 화면은 500 오류". 회귀 가드 `test/test_returns_period_ledger_regression.py` 4/4 + 인접 32/32 무회귀, 광범위 회귀(반품/원장/정산/기간) 278/278 PASS, ReadLints 0.*

*과거: 2026-04-22 (세 번째 사이클) — DEC-056 보강 (분기 0 — admin role 매핑 즉시 채택, Wave B) + DEC-058 보강 (정산 변형사 DB 컬럼 어댑터 — `_t2_columns`/`_build_sql_list_tax`). 사용자 보고("정산 관리 화면에 데이터 조회가 전혀 되지 않는다 / admin 계정인데도 보이지 않는 메뉴가 존재한다 / 통계 화면 403"). 정산 라이브 probe(`debug/probe_settlement_endpoints.py`) 4 서버 × 7 endpoint = 28/28 OK 회복. ① 분기 0 — `auth_service._has_admin_role_mapping(user_id)` 신규 헬퍼 + 동기/비동기 `_resolve_role_and_permissions{,_async}` 양쪽 첫 분기에 호출 (LSP). admin role 매핑된 사용자는 hcode='99999' / Id_Logn Fxx 가 operator 합성하더라도 즉시 admin/['*']. ② tax_invoice — `_t2_columns(server_id)` 컬럼 캐시 + `_build_sql_list_tax(cols)` / `_build_sql_count_tax(cols)` 동적 SELECT (변형사 컬럼 부재 시 `'0' AS Chek3` 정적 리터럴, alias 순서 보존). `t5_ssub_adapt` 패턴 1:1 재사용(신규 패턴 0). ③ 신규 회귀 가드 5종(test_admin_resolver_branch0_priority 5/5 + test_admin_settlement_full_access 4/4 + test_settlement_billing_no_inline_correlated_subquery 1/1 + test_settlement_tax_invoice_chek3_optional 6/6 + test_settlement_cash_status_sdate_response_shape 2/2) = 18/18 PASS. ④ 신규 디버그 도구 2종(debug/probe_settlement_endpoints.py — 정산 7화면 라이브 점검 + debug/show_jwt_claims.py — JWT 클레임 진단). ⑤ 인접 회귀 무영향 — `test_admin_superuser_safety_net` 11/11 PASS, `test_c10_admin_phase1::test_P_01..05` 5/5 PASS. ReadLints 0 (changed files only). 사용자 룰 부합 — 임시방편 0 (인라인 서브쿼리 회귀 가드 정적 grep 으로 일반화 차단), Id_Logn Fxx vs admin role lacuna 를 사용자 ID 단위 우선순위 정책으로 해결(admin 한정 패치 아님 — `role='admin'` 매핑된 모든 사용자가 동일 보장 SOLID-O), 변형사 DB 호환은 `t5_ssub_adapt` 패턴 재사용(신규 모듈 0), 동기/비동기 분기 0 동시 신설로 LSP 보존. 직전 사이클: DEC-056 보강 추가 (admin 슈퍼유저 3중 안전망). 사용자 보고("admin 계정에는 모든 superadmin 권한을 주도록 설정해주세요") → 단일 경로(`hcode='0000'`) 의존을 다중 방어로 격상. ① 안전망 #2 강화 — `_admin_whitelist_ids()` env 미설정 시 기본 폴백 `{'admin'}` 반환(`_DEFAULT_ADMIN_USER_IDS: frozenset` 단일 정본), env="" 명시 시 비활성(보안 격리 의도 존중), env="X,Y" 명시 시 그 값만(운영자 의도 우선). ② 안전망 #3 신설 — `_empty_state()` 가 신규 환경에 admin 사용자(`u-admin-default`) + role-admin 매핑 자동 시드, `_ensure_admin_role_mapping()` idempotent 헬퍼가 `_load_state` 부팅 1회 정규화 사이클에 합류 → 기존 환경에 admin 사용자만 있고 매핑이 누락된 경우 자동 보정(운영자가 admin 사용자 *제거* 한 환경은 의사 존중 — 무동작). ③ 안전망 #3 데이터 — `web_admin.json::web_user_roles` 에 기존 admin(`u-1776757269230`) → role-admin 매핑 1건 추가. 검증: `test/test_admin_superuser_safety_net.py` 11/11 PASS (3 클래스 + 4 테스트 케이스 + 화이트리스트 정책 3 분기 격리). 인접 회귀(test_c10_admin_phase1 P_01..05 + test_auth_resolve_async + test_legacy_permission_map_full_seed + test_id_logn_fxx_matrix + test_sidebar_permission_gating + test_bootstrap_admin_default_hcode_4digit + test_admin_primary_server + test_auth_login_fixed_server + test_c1_login_phase1) 79/79 PASS. ReadLints 0 (changed files only). 사용자 룰 부합 — 기존 `_admin_whitelist_ids` 시그니처 무변동(LSP), `_normalize_primary_servers` 정규화 패턴 재사용, audit 헬퍼 `admin_audit.info` 재사용, `web_admin.json` 스키마 무변동(데이터 1건만 추가). 직전 사이클: DEC-056·DEC-058 신규 추가 (권한 동등성 즉시 적용 — M0+M1+M2+M5). admin/admin123 슈퍼유저 인식 회복 + 사이드바 권한 게이팅(legacy 'X' 동등 = hidden) + Id_Logn Fxx 매트릭스 어댑터 + 카탈로그 52건 시드 일괄. ① M0 — `bootstrap_admin_id_logn.py` 기본값 `'00000'` → `'0000'` (`auth_service` `hcode_norm == "0000"` 슈퍼유저 분기와 정합). ② M1-a — `LegacyIdLognProvider.fetch_fxx_matrix()` 신설 (Chul.pas L441 `SELECT * FROM Id_Logn WHERE gcode` 패턴 재사용, F11~F89 80셀 `_safe_str`+`.strip().upper()`+EucKR bytes 폴백). ③ M1-b/c — `_resolve_role_and_permissions_async()` + `_load_legacy_permission_index()` + `_merge_fxx_to_permissions()` 신설, 기존 동기 `_resolve_role_and_permissions(user_id, hcode)` 시그니처 무변동(LSP 보존 — `test_c10_admin_phase1::test_P_01..05` 무회귀). `authenticate_user` 라우팅 1줄 변경(`await _resolve_role_and_permissions_async(..., server_id)`). 분기 1·2(슈퍼유저/whitelist) → 신규 분기 3(Id_Logn Fxx 합성, `'O'` = 권한 그대로 / `'R'` + `*.write` = `*.read` 페어 자동 합성) → 기존 분기 4·5·6(`admin_service` / `BLS_DEFAULT_ROLE` / `('', [])`) 폴백 위임. ④ M5 — `web_admin.json::legacy_permission_map` + `admin_service._DEFAULT_LEGACY_PERMISSION_MAP` 시드 3건 → **52건**(카탈로그 §1+§4 정본 전수). `_empty_state()` 가 신규 환경에 동일 시드 보장(`dict()` 복사로 mutation 차단). ⑤ M2 — `frontend/src/lib/use-permissions.ts` 신규(`isSuperUser` = `*` ∨ `role==admin` ∨ `hcode==0000` 3-OR), `FormMeta.requiredPermission?: string` 필드 추가 + 52 폼 매핑 일괄, `sidebar.tsx` `isVisibleForm` 게이팅 + 그룹 내 가시 폼 0건 시 그룹 헤더 자체 hidden(legacy 빈 그룹 제거 시각 효과 동등). 신규 테스트 5종(test_bootstrap_admin_default_hcode_4digit / test_legacy_permission_map_full_seed / test_id_logn_fxx_matrix / test_auth_resolve_async_with_id_logn / test_sidebar_permission_gating) 17/17 PASS. 인접 회귀(test_c10_admin_phase1 / test_admin_primary_server / test_auth_login_fixed_server / test_c1_login_phase1) 무회귀 — LSP 보존 확인. tsc 0 · ReadLints 0 (changed files only). 사용자 룰("신규 SQL 0건 + 재귀 오류 금지 + 기존 인터페이스 LSP 보존 + 기존 코드 재활용") 부합 — 기존 LegacyIdLognProvider DIP 인터페이스 + Chul.pas L441 SQL 패턴 + `_safe_str` 정규화 + admin_service.list_legacy_permission_map 인덱스 모두 재사용, 신규 클래스 0건. M3·M4·M6·M7 은 SME 확인 대기(차단 없음). 직전 사이클: DEC-033 (d+) 청구서관리 500 핫픽스 — `_SQL_LIST_BILLING` SELECT 인라인 스칼라 서브쿼리(`(SELECT COUNT(*) FROM T3_Ssub …) AS LineCnt`) 를 별도 헬퍼 `_fetch_billing_line_counts` + `in_clause_lookup` 청크 GROUP BY + Python merge 로 분리(MySQL 3.23 1064 → HTTP 500 회귀 차단, SOLID-O — 신규 패턴 0). 회귀 가드 `test/test_c5_settlement_optional_filters.py::BillingMysql3CompatTests` 3축 신규 PASS, 기존 32/32(C5 phase1) + 14/14(optional_filters) 무회귀, 전체 pytest 677 PASS(2 사전 환경 dfm2html/res_string 무관). 직전 사이클: DEC-033 (f+) 발송비/입금 7화면 422/500 핫픽스 사이클 — DEC-033 (f) 패턴을 settlement 4함수(`list_period_summary`/`cash_status` sdate variant/`list_tax_invoices`/신규 `compute_outstanding_by_customer`)에 일반화 + 5 list 화면(billing/cash/cash-status/tax-invoice/outstanding) DEC-033 (g) 표준 페이저 + DEC-055 useListSession 합류, period/payment-slip 은 useListSession 만(소량 의도). 미수현황은 fetchAllPages 클라이언트 누적 → 신규 서버 집계 endpoint `GET /api/v1/settlement/outstanding`(transactions_service.summarize_sales_statements_by_customer 의 fetch+Python merge 컨벤션 1:1 재사용, 신규 SQL/패턴 0). 계약 v1.2.0 → v1.3.0 (hcode optional + outstanding endpoint + truncated). 회귀 가드 `test/test_c5_settlement_optional_filters.py` 14/14 PASS(5 클래스), 기존 `test_c5_settlement_phase1.py::test_p1_12` 정책 동기화. 검증: pytest 674 PASS(2 사전 환경 dfm2html/res_string 무관, 회귀 0) · tsc 0 · ReadLints 0 · audit_list_state_persistence pages=73 covered=26 violations=0 · audit_legacy_coverage missing=0 mismatch=0 · probe `settlement.outstanding` 추가. 사이드바 표시 변동 0(전 화면 phase1 유지, 핫픽스 사이클).*

*과거: 2026-04-22 — DEC-055 신규 추가 (list 화면 상태 보존 sessionStorage 일반화 + 회귀 가드). 17개 list 화면(`master/{customer,book,publisher,book-code,discount,logistics-cost}` + `outbound/{orders,status}` + `inbound/receipts` + `returns/receipts` + `transactions/sales-statement` + `inventory/status` + `ledger/{book,book-integrated}` + `reports/{book-sales,customer-sales,year-end-book}`) 모두 단일 hook(`useListSession`) 으로 sessionStorage 영속화 — detail 복귀 시 검색조건·페이지·offset·드릴다운 자동 복원. SSR-safe + TTL 30분 + JSON 직렬화 + 라우트 path 기준 자동 키. `bootDone` 플래그 + `LoadOverrides` 패턴으로 `useState` 비동기 갱신 race 회피, `dyn.recommended` reload 가 복원된 페이지 위치를 덮어쓰지 않도록 `snap.limit > 0` 가드. 회귀 가드: `tools/audit_list_state_persistence.py` (DEC-054 audit_legacy_coverage.py 패턴 재사용 — discover/allowlist/`--check`/JSON report 동일 골격) 73 page.tsx 스캔 → 17 covered / 0 violations / 56 skipped, `test/test_list_state_persistence_audit.py` 9/9 PASS(violations 0 + 17쪽 baseline + CLI smoke + stale allowlist 0 + 대표 시나리오 화면 명시 등). 검증: tsc 0 · pytest 647 PASS(2 사전 환경 dfm2html/res_string 무관, 회귀 0) · ReadLints 0 · `--check` exit 0. 사용자 룰("기존 코드 재활용 + 근본 원인 일반화 + 신규 패턴 최소") 부합 — DataGridPager/useDynamicPageSize/useState 시그니처 무변경, hook 1개 + audit 1개만 추가, detail 페이지 무접촉.*

*과거: 2026-04-21 — DEC-054 신규 추가 (레거시 포팅 누락 자동 탐지 — 영구 회귀 가드). DEC-033 (k+1) 사례를 일반화. `tools/audit_legacy_coverage.py`(신규) + `tools/parsers/dfm_parser.py` Caption surface(1줄 보강) + `legacy-analysis/coverage-allowlist.yaml`(baseline 109건) + `analysis/audit/legacy-coverage-report.json`(첫 산출) + `test/test_legacy_coverage_audit.py`(13/13 PASS, 신규 missing 0 + 신규 mismatch 0 + Sobo67 스모크 3축). DFM root caption 163 폼 ↔ registry 68 entry 양방향 비교(`legacy_form` 우선 + id base prefix 매핑), Sobo67_status (출고현황) ↔ DFM Sobo67 (도서별년말집계) baseline allowed 에 명시화 → 라벨 붕괴 재발 시 즉시 FAIL. CLI `--check` exit 0 검증, 의도적 위반 주입(allowlist 1건 제거) 시 FAIL 재현 OK. 검증: pytest 638 PASS(2 사전 환경 dfm2html/res_string 무관, 회귀 0) · ReadLints 0 · `--check` exit 0. 사용자 룰("근본 원인 + 일반화 + 기존 코드 재활용") 부합 — 신규 DFM 파서 0건(LAYOUT_EXPORT_KEYS 기존 추출 능력 surface 만), AST 도구 도입 0(stdlib 정규식 + PyYAML).*

*과거: 2026-04-21 — DEC-033 (k+1) 도서별년말집계(Sobo67_yearbook) 신규 포팅 — 레거시 화면 누락 해소. 사용자 보고: "POC 에는 도서별년말집계가 존재하는데 포팅된 프로그램에 해당 내용이 포팅되어 있나?". 진단: `form-registry.ts::Sobo67_status` 가 `Subu67.dfm Caption='도서별년말집계'` 를 잘못된 의미("출고현황", `/outbound/status`) 로 라벨링하고 있었음. 출고현황 화면은 별도 사용자 가치(데이터 분포가 다름) 가 있어 단순 rename/redirect 가 아닌 신규 포팅(옵션 A) 채택. 채택: 신규 ID `Sobo67_yearbook` + 신규 경로 `/api/v1/reports/year-end-book` + `/reports/year-end-book` (기존 `Sobo67_status` 와 ID/경로 분리 → 사용자 워크플로우 회귀 0). POC `seak80-sample/backend/sobo67_sql.py::build_sobo67_detail_pymysql` + `sobo67_aggregate.py::apply_delphi_line` 검증 자산을 `reports_service.get_year_end_book_aggregate` + `_classify_sobo67_line` 으로 1:1 이식 (POC SQL builder 재구현 없음, Korean literal 분기 보존). 패턴은 기존 `get_book_sales` 의 2-pass(S1_Ssub + Sg_Csum) + Python 누적 + 페이지 슬라이싱 흐름 재사용 (SOLID-O — 신규 패턴 도입 0). grain 토글(year/month) + 부모 도서 드릴다운 + 본사/창고/전체(ALL) book_mode 토글 + scode_filter 체크박스 동등. 회귀 가드 `test/test_year_end_book.py` 22/22 PASS — 5축(분류 7케이스 / book_mode 3 / scode_filter 2 / hcode·bcode 옵셔널 4 / mysql3 호환 2 / grain·드릴다운 3 / Sg_Csum 누적 1). 검증: pytest 625 PASS(2 사전 환경 dfm2html/res_string 무관, 회귀 0) · tsc 0 · ReadLints 0 · 기존 `Sobo67_status` phase1 5축 무회귀(test 7 PASS). 영향 범위: backend(`models/inquiry.py` +YearEndBook* 모델 / `services/reports_service.py` +`_classify_sobo67_line`+`get_year_end_book_aggregate` / `routers/reports.py` +`/year-end-book`), frontend(`lib/inquiry-api.ts` +`reportsApi.yearEndBook`+`YearEndBookRow/Response` / `lib/form-registry.ts` +`Sobo67_yearbook`(statistics) / `app/(app)/reports/year-end-book/page.tsx` 신규), tests(`test/test_year_end_book.py` 신규). 사용자 룰("기존 코드 활용 + 근본 원인 해결 + 일반화") 부합 — POC 자산 + book_sales 패턴 재사용으로 신규 패턴 도입 최소.*

*과거: 2026-04-21 — DEC-033 (k) 입고접수관리(Sobo22) `Scode` 정합화 — 데이터 0행 회귀의 근본 원인 해결. 사용자 보고: "입고접수관리 화면에 데이터가 전혀 검색되지 않는데 POC 에는 다량의 데이터가 검색되었다". 진단: `inbound_service.py` 가 LIST WHERE / `create_receipt` fallback / `update_receipt` fallback / `import_books` 하드코딩 4곳 모두 출고 코드(`Scode='X'`) 를 쓰고 있어 레거시 입고 데이터(`Y`) 가 LIST 에서 모두 필터링됨. 레거시 원본 `Subu22.pas` 는 일관되게 `Ocode='B' AND Scode='Y'` (L408-409, L570-573, L771-772, L839-840, L1207-1210, L1229-1232, L1271-1274, L1469-1470). 형제 화면 비교: 출고접수 `Subu21.pas`=`X`, 거래명세서 `Subu23.pas`=`X`(메인)/`Z`(특수), 반품/입고만 분리. `reports_service.py:143` 주석에 ``Scode='Y' 입고/반품`` 으로 정확한 매핑이 이미 명시되어 있어 inbound 파일 단독 누락 케이스. 채택: 4곳 일괄 `'X'`→`'Y'` + 잘못된 fixture(`test_c3_inbound_phase1.py::VALID_HEADER` `scode='X'`) 동시 정정 — 잘못된 값을 PASS 시키던 회귀 가드 정상화(SOLID-D, 단일 진실 원천=레거시 원본). 영향 범위: 읽기(LIST 0행) + 쓰기(신규/import 시 `X` 오염으로 다른 화면 의미 충돌) 모두 차단. 운영 DB 기존 오염 데이터 마이그레이션은 별도 사이클(plan §5 옵션 B)로 분리. 검증: pytest 603 PASS(2 사전 환경 dfm2html/res_string 무관, 회귀 0) · ReadLints 0 · `test_c3_inbound_phase1.py` 15/15 + `test_list_count_grouped_mysql3.py::test_inbound_*` 무회귀.*

*최신: 2026-05-29 — ACC-DATA-03 (M4 행격리 갭 클로즈) 정식 등록 — 식별자 우회 경로 차단 + 최후 방어선. 배경: Phase 4(2026-05-25)에서 list/집계 GET 의 `hcode` Query 는 `enforce_hcode_isolation` 으로 막혔으나, **식별자 파라미터로 Hcode 를 우회**하는 경로가 잔존(도서 마스터 125,861건 노출과 동일 클래스). 진단된 갭: `ledger.get_customer_ledger`(`customerCode`→서비스에서 그대로 `Hcode`), `ledger.get_integrated_customer_ledger`(`customerPattern`→`Hcode LIKE`), `ledger.list_publisher_settings`(`G7_Ggeo` 전체, hcode 필터 없음), `courier.list_courier_lines`(`hcodeFrom`/`hcodeTo` 구간), `courier.*memo`(`hcode` 단건), `scan.scan_match`(body `hcode`), `transactions.upsert_other_statement_memo`(body `hcode` PATCH) — 모두 `get_current_user` 만 쓰거나 가드 없이 서비스 직통. 채택(사용자 정책): (1) 식별자/범위/패턴 tamper 가드를 `app.core.deps` 에 일반화 신설 — `enforce_hcode_identity`(단건)/`enforce_hcode_range`(구간)/`enforce_hcode_pattern`(LIKE), 격리 계정(T2_PUB·T3 chul_09)은 빈 값=본인 hcode 강제·타사 값=**403 `HCODE_FORBIDDEN`**, T1/T2_DIST/super 는 입력 그대로(광역). (2) 세 라우터(`ledger`/`courier`/`scan`)를 `get_user_context` 로 전환(account_type·점검 오버레이 반영). (3) 서비스 빌더 **최후 방어선** — 요청 범위 ContextVar(`hcode_scope_context.py`)에 `row_filter_required`/`scope_hcode` 를 두고, `hcode_isolation.guard_scope_bound` 가 multi-tenant 테이블 scope 누락을 런타임 검출(`append_hcode_clause(guard=True)` 기본 내장 + 통합원장/출판사설정 직접 호출). `BLS_HCODE_SCOPE_GUARD=strict` 면 `RuntimeError`(테스트/CI), 기본 `warn` 은 `audit.hcode_scope` 로그. (4) 통합 원장 `Hcode LIKE`→`scope_hcode` 정확 일치, 출판사 설정은 테넌트 키 `G7_Ggeo.Gcode=%s`(courier `H7.Gcode=S.Hcode` 매핑과 정합). (5) 정적 감사 `tools/audit_router_hcode_coalesce.py` 를 식별자(`customerCode`/`customerPattern`/`hcodeFrom`/`hcodeTo`) + POST/PATCH body `hcode` 까지 critical 탐지로 확장(신규 헬퍼 3종 `_ALLOWED_HELPERS` 등록, 공개 계정복구 `public_lookup.activate_lookup` 은 비로그인이라 `# noqa` 명시). 검증: `audit_router_hcode_coalesce --strict` endpoints=218 scope_idents=44 critical=0 info=43 skipped_noqa=1, `audit_domain_api_hcode_filter --strict` critical=0/warn=0, 신규 `test_hcode_identifier_guards`(20/20) + `test_ledger_courier_scan_hcode_isolation`(13/13) + 기존 hcode 스위트 32/32 무회귀. 단일 정본: `migration/contracts/_hcode_query_policy.yaml` v2026-05-29(`scope_identity`/`scope_runtime_guard` 태그 신설), `analysis/audit/hcode-isolation-dod.md` §8. 사용자 룰("근본 원인 + 일반화 + 기존 코드 재활용 + 재귀 오류 차단") 부합 — `enforce_hcode_isolation`/`resolve_scope_hcode`/`row_hcode_filter_required` 재사용, inspect_context ContextVar 패턴 1:1, 신규 클래스 1개(ContextVar dataclass)만 추가. DSN-DEC-12(로그인 소유성)와 직교 — 본 건은 **행 레벨** 격리.*

*과거: 2026-05-21 — DSN-DEC-12 신규 추가 (공유 DB 테넌트 소유성 가드 — 타사 데이터 노출 차단). 사고 보고: 통합 로그인 후 사용자에게 다른 회사 데이터가 노출되는 회귀가 보고됨. 분석: WeLove 운영 시드는 `chul_09_db`(위러브1·2·3·교문사 4 테넌트), `book_07_db`(2 테넌트) 등 19 건의 공유 DB 좌표를 보유하며, `auth_service._resolve_account_type` 의 `lookup_by_account_family(family, server_id=server_id)` 가 “첫 매치 테넌트” 를 반환해 사용자 컨텍스트가 실제 소속과 다른 회사로 고정되는 fail-open 결함이 원인. 채택: `tenants_directory_service` 에 `find_owning_tenants` / `is_shared_db` / `resolve_unique_tenant` 3 함수 신설 — `(server_id, db_name, hcode, tenant_id)` 좌표로 단일화 시도(우선순위: tenant_id_hint > account_family_hint > 시드 격리 키 hcode_in/hcode_pattern/hcode_prefix > 후보 1건). 단일화 실패 시 `("ambiguous", None, candidates)` 반환 → `auth_service._resolve_account_type` 가 `tenant`/`account_family`/`active_build_id` 를 None 으로 유지(fail-closed). 기존 `lookup_by_account_family`/`lookup_by_hcode_hint` 폴백은 `ambiguous` 가 아닐 때만 호출(임시 우회 회피). 감사 로그 신설 3 필드: `ownership_status`(unique/ambiguous/none), `ownership_candidate_count`(0..N), `ownership_violation`(Bool). 운영 도구 신설: `tools/audit_welove_routing_consistency.py`(매트릭스↔시드 정합 — `SHARED_DB_NO_HCODE_GUARD`/`PRIMARY_SERVER_MISMATCH`/`DB_NAME_LOGICAL_MISMATCH` 등 6 카테고리 분류, `--strict` 로 PR 차단), `tools/classify_login_audit_logs.py`(`audit.auth` 카테고라이즈 — A_SEED_MISMATCH/B_INDEX_STALE/C_AMBIGUOUS_NARROWING/D_DIRECTORY_SWEEP_HIT/E_OWNERSHIP_VIOLATION/F_TOKEN_BUILD_FAILED/G_INVALID_CREDENTIALS/H_AMBIGUOUS_STRICT 8 분류). 시드 스키마 확장(`hcode_in`/`hcode_pattern`/`hcode_prefix`) — `migration/contracts/tenants_directory.yaml` v1.1.0. 회귀 가드 신설: `test/test_auth_login_cross_tenant_isolation.py`(11건 — pure unit `resolve_unique_tenant` 시나리오 + e2e ownership_* 감사 필드), `test/test_welove_routing_consistency.py`(5건), `test/test_classify_login_audit_logs.py`(9건). 운영 단일 원천: `docs/welove-login-tenant-audit-samples.md`(라우팅 기대 매트릭스 A~F 카테고리), `docs/welove-cross-tenant-exposure-runbook.md`(점검 런북). 슈퍼관리자(`hcode='0000'` / `BLS_ADMIN_USER_IDS`) 호환 — ownership 가드 이전에 T1 결정되어 영향 없음. 변경 영향: `auth.py`(audit 필드 3 추가), `auth_service.py`(_resolve_account_type 우선순위 수정 + ownership 신호 propagation), `tenants_directory_service.py`(3 함수 신설). 검증: 회귀 51 PASS(기존 33 + 신규 18), tsc/lint 무회귀.*

*과거: 2026-04-21 — DEC-033 (j) 재고관리 raw fetch SQL 사전 집계 — `truncated` 잔존 노출의 근본 해결. (i) 사이클(가드 5,000→10,000) 뒤에도 사용자가 동일 배너를 계속 목격 + 배너 본문이 여전히 "기본 5,000행" 으로 드리프트되어 있다는 보고. 분석: `_ledger_rows_sql` 가 LIMIT 없이 `WHERE Gdate IN (page_dates)` raw 를 모두 fetch → 페이지 일자 100개 × 일자별 100행 ≈ 10,000 으로 가드 도달이 자연 발생. 결론: 단순 cap 상향(임시방편) 이 아니라 raw fetch 자체를 압축해야 함. 채택: `GROUP BY (Gdate, Scode, Gubun, Pubun)` + `COALESCE(SUM(Gsqut))` / `COALESCE(SUM(Gssum))` + `MIN(Bcode) AS Bcode` 사전 집계 — `_accumulate_row` 의 분기 누적이 가산이라 N개 raw 행 → (Scode·Gubun·Pubun) 조합 1행 + SUM 으로 압축해도 수학적 동등(원본 Subu31 client-side 누적 결과와 1:1). 동일 컨벤션은 `reports_service.get_book_sales` L112-117 + `returns_service.SQL_LEDGER_MASTER` L1089-1106 에서 mysql3 호환 검증 완료, 신규 패턴 도입 없이 기존 검증 코드 재사용(SOLID-O). raw 행이 100배 이상 압축되어 `BLS_INVENTORY_LEDGER_MAX` 안전망은 정상 데이터 분포에서 도달 불가. 부수: 배너 본문에서 하드코딩 숫자("기본 5,000행"·"기본 10,000행" 등 어떤 cap 값도) 제거하고 `BLS_INVENTORY_LEDGER_MAX` 환경변수 이름만 노출 — 백엔드/프런트 단일 진실 원천 정렬 (Sobo44_inv / Sobo33_ledger 동일 적용). `ORDER BY Gdate, Jubun, Id` 는 사전 집계 후 의미 없어 제거(Subu31 L367 의 원시 정렬은 client-side Locate 용이라 서버 사전 집계와 무관). 검증: pytest 603 PASS(2 사전 환경 dfm2html/res_string 무관, 회귀 0) · tsc 0 · ReadLints 0 · 기존 모킹 패턴(in_clause_lookup 반환 row shape) 동일 유지로 테스트 무수정 통과. 영향 범위: `backend/app/services/inventory_service.py` (`_ledger_rows_sql` 1개 SQL + `get_inventory_ledger` docstring/주석), `(app)/inventory/status/page.tsx` + `(app)/ledger/book/page.tsx` (배너 본문). 사용자 룰("근본 원인 + 일반화 + 기존 코드 재활용") 부합.*

*과거: 2026-04-21 — DEC-033 (i) 재고관리 raw 가드 디폴트 상향(5,000→10,000) + 미사용 Gbigo 컬럼 제거. (1) `BLS_INVENTORY_LEDGER_MAX` 디폴트를 5,000→10,000 으로 상향: 거래 밀도가 높은 단일 일자(예: 월말 정산일)에서 안전망 도달 빈도를 줄여 truncated 배너의 잔존 가능성을 추가 완화. 환경변수 오버라이드 정책은 그대로 유지. (2) `_ledger_rows_sql` SELECT 절에서 누적/응답 어디에도 사용되지 않는 ``Gbigo`` 텍스트 컬럼을 제거 — by_date 누적 dict 에 gbigo 키가 없어 이미 ``LedgerRow.gbigo`` 디폴트 ""만 나가던 동작이라 응답 동등이고, 네트워크/메모리 페이로드는 약 10-20% 절감(특히 페이지 raw 가 안전망 한도까지 도달한 시나리오에서 의미). (3) 부수: B-1(COUNT 제거+over-fetch) / B-2(도서명 lookup 캐시) / B-3(라우터 일자 범위 상한 가드) / B-5(reports_service.get_book_sales 동일 3-step 적용) / B-6(인덱스 권장 문서) 속도 리팩토링 후보를 영향도/리스크 ranked 보고로 제출 — 적용은 사용자 결정 후 별도 사이클. 검증: pytest 603 PASS(2 사전 환경 dfm2html/res_string 무관) · tsc 0 · ReadLints 0 · API/응답 schema 무변동.

*직전: 2026-04-21 — DEC-033 (h) 재고관리 SQL 레벨 일자 페이지네이션 — `truncated` 초기 노출 회귀의 근본 해결. 1차 임시방편(디폴트 1년→1개월) 으로도 1개월치 raw 가 5,000행 초과 시 여전히 배너 노출되는 사용자 보고 후 아키텍처 자체를 재설계. 변경 전: `LIMIT 5001` 으로 raw 행을 모두 fetch 한 뒤 Python 에서 by_date 누적 → limit/offset 슬라이싱(가드와 페이지네이션 직교). 변경 후 3-step: ①`COUNT(DISTINCT Gdate)` 로 페이저 total 산출, ②`SELECT DISTINCT Gdate ... LIMIT N OFFSET M` 으로 현재 페이지 일자 목록만 추출, ③`SELECT ... WHERE Gdate IN (page_dates)` 로 해당 일자에 한해 raw 행 fetch, ④Python 누적. raw 행 fetch 가 "페이지당 일자 수 × 일자별 평균 거래 수" 로 한정 → `BLS_INVENTORY_LEDGER_MAX`(5,000) 가드는 사실상 도달 불가능한 안전망. mysql3 호환은 `apply_limit_offset_syntax` + `limit_offset_bind` + `in_clause_lookup`(raw 행 IN 청크 분할) 로 흡수. truncated 배너 문구 재작성("현재 페이지에 포함된 일자 중 하나에 거래 행이 비정상적으로 많아 안전망 도달, 거래처/도서 코드 함께 적용해 다시 조회해 주세요"). 적용: `backend/app/services/inventory_service.py`(`_build_filter_where`/`_dates_count_sql`/`_dates_page_sql`/`_ledger_rows_sql` 분리 + `get_inventory_ledger` 본체 3-step), `(app)/inventory/status|ledger/book/page.tsx` 배너 문구. 회귀 가드 재설계: `test_inventory_ledger_paging.py` 8/8(`test_total_uses_count_distinct`/`test_empty_result_skips_dates_and_raw_queries`/`test_truncated_flag_safety_net` 신설), `test_inventory_ledger_optional.py` 10/10(메인 SQL = count + dates 두 곳 모두 옵셔널 절 검증, `test_three_step_sqls_emitted` 신설), `test_in_clause_lookup_chunked.py::test_inventory_book_lookup_uses_helper` 갱신(book lookup 호출 = 마지막 in_clause_lookup, raw 호출은 `G4_Book` 미포함으로 분리). 검증: pytest 603 PASS(2 사전 환경 dfm2html/res_string 무관) / tsc 0 / ReadLints 0.

*직전: 2026-04-21 — 재고관리 메뉴 3종(Sobo44_inv 재고현황 / Sobo33_ledger 도서수불장 / Sobo33_1_ledger 통합 도서수불장) 표준 페이지네이션(DEC-033 (g)) + 사이드바 phase1 정식 승격(초록 체크). DEC-033 §결정 사항에 (g) 항목 신규 — 일자(by_date) 누적 결과에 `clamp_limit(default=100, ceil=2000)` + `build_page` 적용, `LedgerResponse.{page, total}` 응답 필드 + 라우터 `limit/offset` 쿼리 파라미터, 통합 도서수불장은 `book_sales` 기존 페이지 메타를 `DataGridPager` 로 노출(기존 `fetchAllPages` 자동 누적 교체). 사이드바 `lib/form-registry.ts` 3건 모두 `phase: "phase2"` → `"phase1"` 으로 승격(P2 amber 배지 → 초록 `CheckCircle2`). 회귀 가드 신규 `test_inventory_ledger_paging.py` 7/7 + 기존 옵셔널화 테스트 13/13 무회귀, 전체 601 PASS(2 사전 환경 dfm2html 외), tsc 0, YAML/JSON OK. 직전 사이클: DEC-033 (f) hcode/bcode 옵셔널화 + truncated 가드 (594 PASS).*

*이전 업데이트(2026-04-21 (f) 사이클): 재고관리 메뉴 3종(Sobo44_inv 재고현황 / Sobo33_ledger 도서수불장 / Sobo33_1_ledger 통합 도서수불장) 필수값 옵셔널화 + 풀스캔 가드 사이클. DEC-033 §결정 사항에 (f) 항목 신규 — 빈/`%` 입력 시 `Hcode`/`Bcode` WHERE 절 동적 제거 + 일자 범위 필수 유지(mysql3 stall 1차 방벽) + 서버 LIMIT(`BLS_INVENTORY_LEDGER_MAX` 기본 5,000행) + `LedgerResponse.truncated` 응답 필드 + 기존 `in_clause_lookup` 청크의 hcode 절 동적 제거 일반화. 적용: `backend/app/routers/inventory.py`, `backend/app/services/inventory_service.py`, `backend/app/models/inquiry.py`, `backend/app/routers/reports.py`, `backend/app/services/reports_service.py`(SQL-INQ-7/8 양쪽), `frontend/src/lib/inquiry-api.ts`, `(app)/inventory/status|ledger/book|ledger/book-integrated/page.tsx`, `migration/contracts/sales_inquiry.yaml`. Sobo33_ledger 의 기존 `hcode='%'` 트릭(정확 일치 SQL 에서 0행 반환되던 잠재 버그) 동시 정리. 부산물: `test/conftest.py` 신설(autouse `_ensure_default_event_loop` — IsolatedAsyncioTestCase 격리 회귀 일반화 차단). 회귀 가드 `test_inventory_ledger_optional.py` 9/9 + `test_book_sales_optional_hcode.py` 4/4 신규 PASS, 전체 스위트 594 PASS(이전 581 + 신규 13, dfm2html 2건 환경 이슈 제외) — c2/c3/c4 서비스 단위 회귀 무영향, tsc 0, JSON/YAML 무결성 OK.*
*이전: 2026-04-21 — 사이드바 「기초관리」 정합화 사이클. (1) DEC-019 §영향 보강 — Sobo19 stub(InputBox 다이얼로그) 사이드바 제거, Wave D `WebAdmEnv` 단일 원천 노출만 유지. (2) DEC-023 §영향 보강 — Sobo39_1/_2/_5 stub 3건 사이드바 제거(대표 Sobo39 + customer_variants contract 단일 원천), `/master/discount/[type]` 동적 라우트 직접 진입은 placeholder 그대로 보존. (3) Sobo16_special(특별관리) phase1 정식 승격 절차 `docs/master-special-implementation-plan.md` 신설(T1~T8 + BLK-SPC-1/2 해소 절차 + 5축 audit §AH 입력 정의). master 그룹 사이드바 11행 → 7행(정식 6 + phase2 1) 정합. 코드 변경 0(메타/문서만), tsc/lint/회귀 0 영향.*
*이전: 2026-04-21 — DEC-053 §운영에 phase1 정식 승격 사례 1건 추가 (Sobo67_status `/outbound/status` 5축 PASS → `form-registry.phase=phase1` + 사이드바 P2 → 초록 체크). 매트릭스 §2.3 phase1 정식 승격 사례 신규(34행 정식 편입은 다음 audit 사이클 예약 — 현 33행 동결 유지). `phase2-screen-cards.json` Sobo67_status 카드 T8=done. 코드 변경 0(라벨 메타만), tsc/lint/회귀 0 영향.*
*이전: 2026-04-21 — DEC-033 §결정 사항에 (e) 보강 1줄 추가 (POC `seak80-sample` 의 `_SOBO67_GNAME_CODES_CHUNK = 400` 정책 일반화 — 마스터 lookup `WHERE Gcode IN (…)` 단발 거대 쿼리 금지, `in_clause_lookup(server_id, sql_template, keys, prefix_params, chunk_size)` 공통 헬퍼 의무 사용). 적용 9곳: 거래/입고/출고/재고/리포트/반품 lookup. 회귀 가드 `test/test_in_clause_lookup_chunked.py` 17/17 PASS, 인접 회귀 `test/test_list_count_grouped_mysql3.py` 11/11 PASS, 전체 581 PASS.*
*이전: 2026-04-21 — DEC-033 §결정 사항에 (d) HOTFIX 항목 1줄 보강 (LIST 엔드포인트 `total` 산출은 `count_grouped` 헬퍼 의무 사용 — 파생 테이블 직접 작성 금지, mysql3 1064→HTTP 500 재발 차단). 4 화면(C2 출고접수/C3 입고접수/C4 반품/C6 거래명세서) 회귀 일괄 수정 + `transactions_service.list_sales_statements` `hcode` 옵셔널화(빈 값 = 전체 거래처). 회귀 `test/test_list_count_grouped_mysql3.py` 11/11 PASS, 인접 스모크 무회귀.*
*이전: 2026-04-21 — DEC-053 신규 추가 (1차 포팅 화면 컴포넌트 동등성 정기 재점검 — `analysis/audit/phase1-component-fidelity.md` 단일 매트릭스 + 5축 W/B/U/D/O + GAP-P0 = 0 phase1 승격 게이트, HA-RET-02 후속 ID 예약). DEC-028 §영향에 phase1 승격 시 매트릭스 GAP-P0 가드 1줄 보강. `.cursor/rules/dfm-layout-input.mdc` §회귀 가드 1줄 추가. 본 사이클 결과 P0 = 0 / P1 = 0.*
*이전: 2026-04-21 — DEC-051/052 신규 추가 (인증 서버 단일화 = `BLS_AUTH_SERVER_ID` 고정 게이트, 로그인 화면 서버 콤보 제거, JWT `sid`=primary 데이터 서버 / 사용자-데이터 서버 1:1(Primary) = `web_user_servers` 다대다→1대1 의미 좁힘 + admin 라디오 UI + 부팅 1회 idempotent 마이그레이션 + 미설정 헤더 경고 배지). DEC-050 등 기존 결정 무변경.*
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

## DEC-182 — 재고현황(Sobo34) 두 그리드 하단 합계 행

- **일자**: 2026-08-22
- **요청**: "재고 현황 화면 각 목록 하단에 합계 정보가 있어야 한다."
- **결정**: `DataGrid` 의 기존 `totals` 프롭(DEC-146 규약, sticky `<tfoot>`)을 그대로 쓴다.
  전용 합계 컴포넌트를 새로 만들지 않는다.
  - **상단(분류)** = 백엔드 `totals` — 페이지가 아니라 **검색 결과 전체** 합계(DEC-146 규약).
  - **하단(도서)** = **선택 분류** 의 도서 합계. 그 분류의 상단 행 값과 일치해야 정합이며,
    어긋나면 Ocode 병합/분류 롤업이 깨진 신호다.
- **합계 대상**: `MEASURE_KEYS` = 전재고·입고·반입·출고·증정·반품·폐기·변경·현재고·재고(반).
  정가(`gdang`)는 **합산하지 않는다** — 단가성 컬럼이라 합계가 무의미하다.
- **근거**: 레거시 `Subu34.dfm` 두 그리드 하단에 「합계」 행이 있다.

## DEC-183 — 재고현황 행 집합은 **거래 + 재고 스냅샷** 합집합

- **일자**: 2026-08-22
- **증상(사용자 리포트)**: "시작일, 기준일 날짜를 동일하게 지정하면 분류 수가 갑자기 3개로 줄어든다."
- **원인**: `get_stock_ledger` 가 행 집합을 **S1_Ssub 기간 거래**로만 시드했다. 기간이
  짧을수록 거래가 있는 도서만 남아, 재고를 들고 있을 뿐 그날 거래가 없는 도서와 그
  분류가 통째로 사라졌다. 전재고·현재고는 기간 거래와 무관하게 존재하므로 명백한 누락.
- **정본**: `Subu34.pas` L1046~1055 — 누적 결과(nSqry)에 없는 도서를 **스냅샷 결과셋
  (sSqry)** 에서 찾아 행으로 **추가**한다. 즉 행 집합 = 기간 거래 ∪ 재고 스냅샷.
- **수정**: `_fetch_snapshot_bcodes(server_id, hcode=, asof=시작일−1)` 로 `Sv_Ghng` 의
  해당 스냅샷 일자 도서코드를 읽어 빈 버킷으로 합류시킨다. `Sv_Ghng` 가 없는 테넌트는
  경고 로그 후 빈 목록(기간 거래 도서만으로 진행) — fail-open 이 아니라 **기능 축소**다.
- **순서 주의**: 시드는 「도서명 또는 코드」 필터(4단계)보다 **앞**이다. 뒤로 옮기면
  검색어가 스냅샷 도서에 적용되지 않아 무관한 도서가 딸려 나온다.
- **상한**: 시드는 `LEDGER_MAX`(기본 10,000) 로 제한한다. 도달 시 조용히 잘리므로,
  카탈로그가 그보다 큰 테넌트가 생기면 상한을 올리거나 검색어를 요구해야 한다.
- **회귀**: `test/test_stock_ledger_sobo34.py::test_snapshot_books_appear_without_period_movement`

## DEC-184 — 재고금액(Sobo34_1 「재고 및 재고금액」) 신설 — 재고현황 수량축 재사용 + 정가×기준율 파생

- **일자**: 2026-08-23
- **요청**: "원장관리-재고현황 메뉴 다음에 재고금액 메뉴를 신설해라. 재고현황 화면과 거의
  동일한데 수량보다는 **금액 관점**에서 정보를 제공하는 화면이다. 첨부 이미지(레거시)와
  같은 역할인데 포팅 시 누락되어 있다. 검색 데이터는 교문사-경리부 계정 검색 결과와 같아야 한다."
- **정본 확정**: 레거시 폼 = **`Subu34_1` / `TSobo34_1`, caption 「재고 및 재고금액」**.
  메뉴는 `한국도서유통/유통/Chul.dfm` `Menu300`(재고원장) → `Menu304_1` — 재고현황(Sobo34 =
  `Menu303` 기간별재고원장)과 **같은 대메뉴**라 사용자 요청 위치와 정확히 맞는다.
  코드 정본은 재고현황과 같은 경로 `한국도서유통/출판/MySQL/Subu34_1.{pas,dfm}` 로 잡았다.
  - dfm 두 그리드 9컬럼(분류코드/도서코드·분류명/도서명·정가·정품재고·재고금액·반품재고·
    재고금액·재고합계·금액합계)이 요청 컬럼 목록과 **정확히 일치**한다.
  - 변형 주의: `도서유통-New/Subu34_1` 은 필터 패널이 다르고(출판사명·「반품재고 제로」 추가,
    `Edit102`/`Panel102` 숨김) 분류 롤업에 `mSqry.Gjqut` **이중 가산 버그**가 있다.
    출판 빌드는 그 줄이 주석 처리돼 있어 재고합계가 단일 가산 — **출판 빌드를 따른다**.
- **핵심 결정 — 재구현하지 않고 `get_stock_ledger` 를 재사용한다.**
  `Subu34_1.pas` Button102Click 의 누적 분기표(L451~633)와 마감 산식은 `Subu34.pas` 와
  **같은 코드**다. 다른 것은 두 가지뿐이다.
  1. 조회축이 기간이 아니라 **거래일자 1일** — L369~370 `Gdate >= Edit101 and Gdate <= Edit101`
     (`Edit102` 는 `Visible=False`). 그 날 **마감 시점** 재고다.
  2. 마지막에 정가를 곱해 금액 4컬럼을 파생(L1189~1213).

  따라서 `get_stock_value_ledger` 는 `get_stock_ledger(date_from=date_to=거래일자)` 를
  호출하고 금액만 얹는다 — DEC-138(전·현재고 라이브 대사) / DEC-182(합계 행) /
  DEC-183(행 집합 = 거래 ∪ 스냅샷) 의 검증 자산을 그대로 승계한다. 900줄 누적 로직 재이식 없음.
  이것이 "교문사 계정 검색 결과와 같아야 한다"는 요구를 만족시키는 가장 안전한 경로다 —
  재고현황이 이미 그 계정으로 대사된 축이기 때문.
- **금액 산식** (`Edit109` = 기준율 %, 기본 100):
  ```
  재고금액(GOSUM)     = 정가(GSQUT) × 정품재고(GSUMY) × 기준율/100
  반품 재고금액(GBSUM) = 정가(GSQUT) × 반품재고(GSSUM) × 기준율/100
  CheckBox3(반품재고 제로) → GSSUM := 0, GBSUM := 0   ※ 금액 산출 **후** 덮어쓰기
  재고합계(GJQUT)     = GSUMY + GSSUM
  금액합계(GJSUM)     = GOSUM + GBSUM
  ```
- **상단 「정가」는 공란이 정답**: 분류 롤업 루프(L1219~1252)가 `mSqry.Gsqut` 를 **누적하지
  않는다**. 레거시 상단 그리드의 정가 칸은 항상 비어 있으므로 웹도 `gdang: null` 로 두고
  빈 칸으로 렌더한다 — 임의 합산은 레거시와 어긋나는 값을 만든다.
- **합계 대상**: dfm `Footer.ValueType = fvtSum` 인 6컬럼(GSUMY/GOSUM/GSSUM/GBSUM/GJQUT/GJSUM).
  정가는 합계 대상이 아니다(DEC-182 와 같은 이유).
- **반올림 안 함**: 기준율 ≠ 100 이면 금액이 소수가 될 수 있다. 백엔드는 float 그대로
  반환하고 표시에서만 원 단위로 반올림한다 — 행별 반올림 후 합산하면 합계가 어긋난다.
- **UI 결정**:
  - 도서 검색은 재고현황 선례대로 **「도서명 또는 코드」 한 칸**(레거시 `Edit103/105` 구간 폐지),
    비우면 전체 도서.
  - 「반품재고 제로」(`CheckBox3`)는 New 빌드 전용 컨트롤이라 노출하되 **기본 해제** —
    출판 정본(컨트롤 없음)의 동작과 같고, 요청 컬럼인 반품재고/반품 재고금액이 채워진다.
- **구현**
  - `backend/app/services/inventory_service.py` `get_stock_value_ledger`
  - `backend/app/routers/inventory.py` `GET /api/v1/inventory/stock-value`
    (`enforce_hcode_isolation` — 비-슈퍼는 로그인 출판사만)
  - `frontend/src/app/(app)/inventory/value/page.tsx` (route `/inventory/value`)
  - `form-registry.ts` `Sobo34_1_value` (`menuId: ACC-MENU-NAV-03`) —
    `INVENTORY_SIDEBAR_LAYOUT` 에서 `Sobo44_inv`(재고현황) **바로 다음**
  - 매핑 노트 `analysis/layout_mappings/Sobo34_1_stock_value.md` (DEC-028)
  - DB 스모크 매트릭스 `debug/probe_backend_all_servers.py` `inventory.stock_value` 등록
  - 표기 축약(「재고 및 재고금액」→「재고금액」)은 `tools/delphi_form_screen_matrix.py`
    `CAPTION_ALLOWLIST_MISMATCH` + `legacy-analysis/coverage-allowlist.yaml`
    `caption_mismatches` 에 등록(같은 화면·같은 dfm, 메뉴 표기만 축약).
- **회귀**: `test/test_stock_value_sobo34_1.py` (19건 — 위임축/금액산식/제로옵션/분류 롤업/
  라우터·스모크 등록/사이드바 위치·dfm 위젯 id·9컬럼)
- **미해결**: 금액 4컬럼의 **라이브 대사 미완**. 수량 축은 DEC-138 검증 자산 승계지만
  교문사(5019, remote_153/chul_09) 실화면과 금액을 대조하지 않았다 — `RUN_DB_SMOKE` 필요.

## DEC-185 — 사이드바 대메뉴 순서 업무 흐름순 재배치

- **일자**: 2026-08-23
- **요청**(사용자 지정 순서): 기초관리 / 입고관리 / 출고관리 / 반품관리 — 원장관리 / 정산관리 /
  통계관리 — 거래관리 / 택배관리 / 발송비·입금 / 웹관리.
- **결정**: `form-registry.ts` `MENU_GROUPS` 배열 순서만 바꾼다. 사이드바(`sidebar.tsx`)가
  이 배열을 그대로 순회하므로 그룹 id·라우트·RBAC 게이트(`MENU_GROUP_MENU_ID`)는 **불변**이다.
- **내역서관리(NAV-15)**: 요청 목록에 없었다. 삭제 근거가 없어 **제거하지 않고** 레거시
  인접 관계(NAV-14 발송비 → NAV-15 내역서)대로 발송비/입금 바로 뒤에 뒀다. 숨김/이동은
  운영 확인 후 재조정.
- **요청의 빈 줄(3블록)** 은 순서 구분으로만 반영했다 — 대메뉴 레벨 구분선 UI 는 미도입.

## DEC-186 — 입금 도메인 테이블 오배선 정정: 입금현황 → 입출금전표(H1_Ssub) 전면 교체

- **일자**: 2026-08-23
- **보고**: 사용자 — 레거시 「입출금전표-거래처」 스크린샷 첨부 + "이 화면이 **일자별 입금
  금액 기입용**으로 활용됐다. 이 기능을 입금현황 화면에 적용해서 기능을 다시 확인하고
  화면의 데이터가 적절하게 검색되는지 확인해달라." / 후속 지시 "항목을 화면과 맞추고,
  입력은 **명세서 라인 입력하듯 목록에 항목을 추가하는 방식**으로."
- **진단 — 화면이 빈 테이블을 보고 있었다** (라이브 확인):

  | 서버 | `T5_Ssub` (종전 배선) | `H1_Ssub` (레거시 실제) |
  | --- | --- | --- |
  | remote_138 | **0** | 131,254 |
  | remote_153 | **0** | 1,145,482 |
  | 교문사 5019 | **0** | 1,515 (2026년) |

  `cash_service`(입금내역·입금전표)와 `settlement_service.cash_status`(입금현황+변형 2종)가
  모두 `T5_Ssub` 를 읽어 **어떤 계정에서도 항상 0건**이었다. 실화면에서도 입금내역이
  "조회 결과가 없습니다"로 재현됐다. 단일 화면 버그가 아니라 **입금 도메인 5화면 전체**의
  데이터원 오배선이다.
- **정본 재확정**: 레거시 폼 = **`Subu41`/`TSobo41` 「입출금전표-거래처」**
  (`Chul.dfm` `Menu400`(회계관리) → `Menu401`, 라이선스 F41), 출판 빌드
  `한국도서유통출판/출판/Subu41.{dfm,pas}`.
  - 종전 포팅(`Sobo41_cash.md`)은 **다른 빌드 변형**(`도서유통-New`/유통 계열, 컬럼
    `입금일자·청구월·출판사코드·출판사명·금액·결재·메모` 7개)을 따라갔다. 사용자
    스크린샷과 컬럼이 일치하는 것은 **출판 빌드**(10컬럼)뿐이다.
- **결정**:
  1. `/settlement/cash-status` 를 **입출금전표**로 전면 교체(`H1_Ssub`). 캡션 「입금현황」→
     「입출금전표」, registry `folder` 도 `Subu42`→`Subu41` 로 정정.
  2. 입금내역(`/settlement/cash`)·입금전표(`/settlement/payment-slip`)·입금현황 변형 2종
     (`?variant=hcode|sdate`)은 **입출금전표로 통합**하고 사이드바에서 숨긴다
     (`menuId: ACC-MENU-HIDDEN-SETTLE-CASH-T5`). route/API/회귀는 보존.
- **이식한 레거시 규칙** (`analysis/layout_mappings/Sobo41_cash_slip.md` 전문):
  - **금액은 DB 에 `Gssum` 한 칸**이고 `Gubun`('입금'/'출금')이 화면 열을 정한다. 조회 시
    분리(L414~421), 저장 시 역변환(L1336~1352). **입고처(Y)만 분기 순서가 뒤집혀 있다** — 원문 보존.
  - 조회 WHERE 에 `Scode<>'A' and Scode<>'B'`(재고 축 배제), 거래처 범위는 **끝 코드가
    있을 때만** 적용(`if Edit106.Text<>''`), 정렬은 입력순 `Gdate,ID` / 기본
    `Gdate,Gubun,Scode,Gcode`, 상한 2,000행.
  - **잔액 `Gsumy` 는 저장 컬럼**이다. 레거시는 거래처를 고르는 순간에만 `Tong40.SetTring03`
    으로 계산해 저장하고 목록은 저장값을 읽는다 — 조회에서 재계산하면 값이 갈린다.
  - 결재 `Pubun` = 현금·어음·은행·카드·공제·기타 (dfm PickList = 사용자 콤보 스크린샷).
  - 신규 기본값(`T4_Sub11NewRecord`): `Gubun='입금'`, `Pubun='현금'`, `Gsumy=0`.
- **모던 강화 (레거시와 의도적 차이)**: 레거시 UPDATE/DELETE 는 `ID`(+`Gdate`)만 쓰지만
  `H1_Ssub` 는 chul_09 4테넌트 **공유 테이블**이라 모던은 `Hcode` 를 WHERE 에 반드시
  포함한다 — 교차 테넌트 수정/삭제 차단.
- **입력 방식**: 레거시도 별도 입력 폼 없이 `DBGrid101` **인라인 편집**이다
  (`DBGrid101KeyPress`/`T4_Sub11BeforePost`). 운영 지시와 같아 모던도 목록 하단에
  «신규 행»을 띄우는 인라인 입력으로 구현했다.
- **라이브 대조 (교문사 5019 / remote_153, 2026.08.03, 거래구분 거래처)** — 사용자 제공
  레거시 스크린샷과 **완전 일치**(백엔드 서비스 + 브라우저 실화면 양쪽 확인):

  | 코드 | 거래처명 | 잔액 | 입금 | 출금 | 결재 |
  | --- | --- | --- | --- | --- | --- |
  | 3292 | #자유서적[파주] | 48,000 | 48,000 | 0 | 현금 |
  | 3315 | 네이버 스마트스토어 | 17,757,360 | 76,290 | 0 | 현금 |
  | **합계** | | | **124,290** | **0** | |

  교문사 실사용 분포: `Pubun` 현금 1,389/공제 108/어음 12/카드 6, `Scode` 는 X 만,
  `Ocode`·`Oname`·`Tcode` 는 전부 공란(스크린샷의 빈 계정과목 칸과 일치).
- **구현**: `backend/app/services/cash_slip_service.py` 신설 /
  `backend/app/routers/settlement.py` `GET·POST·PUT·DELETE /cash-slip` /
  `frontend/src/app/(app)/settlement/cash-status/page.tsx` 재작성 /
  `frontend/src/lib/settlement-api.ts` `cashSlipApi` /
  `debug/probe_backend_all_servers.py` `settlement.cash_slip` 등록
- **회귀**: `test/test_cash_slip_sobo41.py` (31건). 기존
  `test_c5_settlement_phase1.py::test_p1_32_...` 는 화면 정체가 바뀌어 검증 대상
  legacy id 를 Sobo42→Sobo41 로 갱신.
- **미해결**:
  1. 어음(`H4_Iyeo`)·은행(`H5_Bang`) 부가정보 `Sname` 후처리 미구현(교문사 어음 12건).
  2. 인라인 **수정**(PUT)은 API 만 있고 화면은 신규 추가·삭제까지 — 셀 편집 UI 는 후속.
  3. 형제 폼 `Subu42` 「입출금전표-사무실」 미포팅.

## DEC-193 — 폐기 접수 라인 목록을 입고/출고 접수와 같은 공용 부품·규약으로 통일

- **일자**: 2026-08-24
- **요청**(사용자): "폐기 접수 화면의 목록을 공통 컴포넌트로 변경해줘" / "입고접수나
  출고접수처럼 입력 컨트롤 및 목록 기능 및 방식이 적용되도록 한다."
- **범위 판단**: 이 코드베이스에 «편집 가능한 라인 표» 단일 컴포넌트는 없다. C2/C3 는
  각자 표를 갖되 **같은 공용 부품**(`MasterLookupField`/`LocalComboField`/`useGridPrefs`+
  `GridColumnSettings`/`grid-arrow-nav`/`line-grid-focus`/`list-table-card`)을 쓴다. 4번째
  그리드를 새로 만들지 않고, 폐기 접수가 쓰는 `ReturnLineGrid` 를 그 규약으로 끌어올렸다.
  → **반품 접수(Sobo23)도 같은 컴포넌트라 동일하게 바뀐다**(의도된 통일).
- **바뀐 것**:
  1. **도서코드** = 맨 `Input`+blur 조회 → 공용 `MasterLookupField(book) useInlineAutocomplete`
     (↑↓/Enter 선택 · 검색 중/결과/결과 없음 4상태 패널 · 검색 팝업 폴백, DEC-097).
     확정 시 도서명·ISBN·정가를 채우고 커서는 수량으로(출고 접수 흐름 동형).
     커스텀 Enter 는 붙이지 않는다(DEC-155 — 확정 경로는 컴포넌트 단일 관리).
  2. **컬럼 기본 순서** = 입고 접수와 동일(구분·도서코드·도서명·ISBN·수량·단가·할인율·
     금액·비고·상태). 표시/순서/너비 계정 저장(DEC-191)은 그대로.
  3. **표 마크업·색** = 공용 목록표 토큰(`list-table-card`). 하드코딩 gray/red 팔레트 제거
     (Design.md). 셀 높이도 h-6/text-xs → h-8/text-sm 로 접수 화면들과 맞췄다.
- **같이 고친 결함 2건** (기존 마크업이 만들던 것):
  - **합계 행 어긋남**: `<tfoot>` 이 `colSpan={5}/{2}/{3}` 고정이라 컬럼을 숨기거나 순서를
    바꾸면 수량·금액 합계가 다른 칸 밑으로 밀렸다 → `visibleCols` 를 map 한다(출고 접수 동형).
    브라우저 실측: 도서명·ISBN 숨김 상태에서도 합계 정렬 유지.
  - **도서명/ISBN 표기 밀림**: 표기 캐시가 **행 인덱스** 키라 중간 행을 지우면 아래 행
    표기가 한 칸씩 밀렸다(`delete map[idx]` 뒤 행만 당겨짐) → **도서코드** 키 캐시로 교체.
    같은 코드 재조회도 자연히 사라진다.
- **폐기 접수 화면(Sobo23_scrap)**: 「뒤로」(router.back) → **「목록」 = 폐기 현황**
  (입고/출고 접수의 목록 버튼과 동일 자리·동작). 출판사코드에 공용 룩업 + 출판사명
  읽기전용 표기(입고 접수의 «입고처 코드/입고처» 쌍과 동형). 진입 시 입력 대기 1행,
  저장 시 빈 행 제외(입고 접수 규약). 저장 후 화면 초기화 + 폐기 현황 링크.
- **출판사코드는 인라인 자동완성을 켜지 않는다** (중요):
  `MasterLookupField` 의 `publisher` kind 는 **인라인만** `search_customers`(G1 거래처,
  `Gcode AS hcode`)를 타고, 검색 팝업만 `publisherList`(실제 출판사)를 탄다. 필터 화면은
  «거래처/출판사» 겸용이라 무해했지만 폐기는 그 값을 `S1_Ssub.Hcode`(=출판사, DEC-137)로
  **저장**하므로 축이 다르면 안 된다. 실측(remote_153): 인라인 "교" → 00001 (주)교보문고…
  (거래처) / 팝업 "교" → 5019 (주)교문사(출판사). → 팝업 경로만 사용 + `refocusAfterSelect`.
- **`masters/book/{code}` 404 (백엔드 별건, 회피 조치)**: 교문사 remote_153 에서
  `masters/products` 검색이 찾는 코드(`식품통계1~3`)를 `masters/book/{code}` 상세는 404
  로 돌려준다(`G4_Book.Gcode` + hcode 스코프 축 불일치로 추정). 종전 반품/폐기 접수의
  «직접 입력 코드 보충»(DEC-169)이 이 상세만 써서 **이 테넌트에선 도서명·정가가 영영
  비어 있었다**. → 공용 리졸버 `lib/book-code-resolve.ts` 신설: **products 정확일치 우선,
  상세는 폴백**. 반품 접수·폐기 접수 두 화면이 같은 경로를 쓴다. 상세 404 자체의 원인
  규명은 마스터 도메인 별건으로 남긴다.
- **구현**: `components/returns/return-line-grid.tsx` 재작성 /
  `app/(app)/returns/scrap/new/page.tsx` / `app/(app)/returns/receipts/new/page.tsx` /
  `lib/book-code-resolve.ts` 신설
- **회귀**: `test/test_dec193_scrap_receipt_common_grid.py` (14건). 브라우저 실측(교문사
  5019 / remote_153): 도서 자동완성 선택 → 도서명·ISBN·정가 자동 + 수량 포커스, 수량 4 →
  금액 154,000·합계 정합, 비고 Enter → 새 라인+도서코드 포커스, 직접 입력 코드 blur 보충,
  컬럼 숨김 시 합계 정렬 유지.

## DEC-194 — 입고현황(Sobo25_2)을 출고현황과 «같은 3뷰 공용 축»으로 + 입고처축 정합 3건

- **일자**: 2026-08-24 (구현) / 2026-08-25 (축 정합 보정·회귀·기록)
- **요청**(사용자): "입고현황 레이아웃·기능을 출고현황과 동일하게".
- **바뀐 것**: 입고현황 화면(600여 줄 별도 구현)과 API(입고접수 목록 재사용)를 폐기하고
  출고/반품/폐기와 **같은** `TransactionStatusScreen` + `_status_axis_facade` 의 한 축으로
  이관했다. 화면은 얇은 래퍼 17줄, 백엔드는 축 상수 3개만 다르다. 덤으로 레거시에는 있으나
  종전 구현에 없던 **본사/창고(Ocode)·전표(Jubun)·도서코드(Bcode)** 필터가 생겼다.

### 축 정의 — 거래처축을 그대로 복사하면 안 되는 3가지

레거시 `Sobo25_2.Button101Click`(L396-420) 고정 조건은 `Scode='Y'` + `Gcode<>''` 뿐이고,
거래구분(Edit103)은 **선택 콤보**다. 여기서 세 가지가 갈린다.

1. **거래구분은 입고 하나로 고정한다** (`_GUBUN_IN = "Gubun = '입고'"`) — 2026-08-25
   사용자 결정. 레거시 `Sobo25_2` 는 거래구분이 **선택 콤보**(Edit103)라 무입력 시
   「입고처 반품」(`Scode='Y'` & `Gubun='반품'`)도 함께 나왔지만, 모던은 출고·반품·폐기
   현황이 각각 한 거래구분을 맡는 분할이므로 입고현황도 같은 규칙을 따른다
   (사용자: "입고 현황에 입고반품 모두 포함하지 말고 입고만 대상으로 — 반품 관련
   화면은 별도로 있잖아").

   **감수하는 것** — 「입고처 반품」은 모던 어느 화면에서도 조회되지 않는다.
   반품현황은 거래처축(`Scode='X'`)이라 그 행을 잡지 않기 때문이다. 규모는
   `remote_153` 실측(2026-08-25, S1_Ssub 전 기간) 기준 `Scode='Y'` 행 중 입고 9,376 /
   반품 99 이고, 교문사 5019 는 128행 전부 2002~2009 구데이터다. 2026년 행이 남아 있는
   테넌트는 5093(140) · 5101(20) · 5072(12) 세 곳 — 필요해지면 반품현황에 입고처축
   토글을 붙이는 쪽이 맞다(이 화면에 섞지 않는다).

   > **경위**: 최초 구현(2026-08-24)은 `Gubun='입고'` 하드필터였고, 2026-08-25 검토에서
   > 레거시 콤보 기본값과 다르다는 점 때문에 `IN ('입고','반품')` 으로 잠깐 넓혔다가,
   > 화면의 「거래구분: 입고·반품」 표시를 보고 사용자가 입고 전용으로 확정했다.
2. **표시명 원천은 입고처 `G2_Ggwo`** (`name_source='vendor'`). 공용 축이 쓰던
   `fetch_g1_customer_gnames`(거래처 G1_Ggeo)를 그대로 두면 **같은 Gcode 가 전혀 다른
   거래처명으로 뒤바뀐다.** 교문사 5019 실측 — 조회된 입고처 코드 10개가 **10개 모두 충돌**:

   | Gcode | G2_Ggwo (정답) | G1_Ggeo (오표시) |
   | --- | --- | --- |
   | 00062 | 중원아트(랩핑) | 서울여대[서울] |
   | 00060 | 태성제책사 | 덕성여대평생교육원 |
   | 80012 | (주)아트인 | [X][파][폐업]청주대일(일선) |

   2026-08-22 교문사 리포트(원인 2)에서 이미 고쳤던 결함이라, 공용 축 이관이 되살릴
   뻔했다. 리졸버는 `_party_name_resolver(name_source=)` 하나로 축을 가르고, vendor 축은
   기존 `inbound_service._fetch_vendor_names`(레거시 `Hcode=로그인 → '' 폴백`)를 재사용한다.
3. **하단 집계의 주 거래구분은 '입고'** (`primary_gubun='입고'`). 집계 SQL 의 `out_*`
   버킷이 `Gubun='출고'` 하드코딩이라 그대로 두면 **입고수량이 통째로 0** 이었다.
   축 파라미터로 바꿔 `out_*` 가 입고 수량/금액이 된다. 화면 헤더도 축 파생
   (`rollupPrimaryLabel`/`rollupNetLabel`) — 「입고수량·입고금액·순입고수량」.
   축이 입고 전용이라 `return_*`(반품수량/반품금액) 칸은 구조적으로 0 이다 — 표 모양은
   출고현황과 동일하게 유지(요청이 "동일한 레이아웃")하되, 열 정리는 후속 여지로 남긴다.

### 화면

- 「거래처」 리터럴을 전부 축 파생 `party` 로 교체(필터 라벨·표 컬럼·집계 제목/헤더) →
  입고현황은 **「입고처」**(레거시 `Panel104.Caption='입고처명'` 동등).
- 필터 룩업도 축에서: `partyLookupKind='inboundVendor'`(G2_Ggwo). `customer` 로 두면
  인라인 자동완성이 거래처를 물어와 축이 어긋난다(DEC-155 계열).
- 「거래구분」 읽기전용 표시 = **입고**.
- 세션 스냅샷 키는 축별 분리(`transactions.status.<route>`) — 하나면 4개 현황이 서로의
  기간·거래처 필터를 덮어쓴다.

### 정리

- `inbound_service.list_receipts(require_vendor=)` 제거 — 유일한 호출자였던 입고현황이
  공용 축으로 떠나 죽은 파라미터가 됐다.

- **구현**: `backend/app/routers/transactions.py`(축 라우트 + facade 파라미터) /
  `backend/app/services/transactions_service.py`(`_GUBUN_IN_VENDOR`·`_INBOUND_STATUS_FIXED`·
  `_party_name_resolver`·`primary_gubun`) / `backend/app/services/inbound_service.py` /
  `frontend/src/components/transactions/transaction-status-screen.tsx`(축 필드 4개) /
  `frontend/src/app/(app)/transactions/inbound-status/page.tsx`(래퍼) /
  `frontend/src/lib/inquiry-api.ts`
- **회귀**: `test/test_inbound_status_phase1.py`(13, 축 계약 재작성) /
  `test/test_inbound_status_gyomunsa_parity.py`(11, 2026-08-22 4원인을 새 축에서 재고정) /
  `test_shipment_transactions_lookup_apply.py`·`test_outbound_detail_gisbn_response_model.py`
  (공용 컴포넌트 이관 반영). DB 스모크에 `inbound_status_detail` 추가.
- **브라우저 실측**(교문사 5019 / remote_153, 2026.08.01~08.25): 상세 11전표 ·
  요약 11행 · 목록 19라인 + 입고처 집계 5행(중원아트 7,483 / (주)디북 900 …),
  입고처명 전부 G2_Ggwo 정답, 콘솔 에러 0.
- **미해결**: 컬럼 설정(grid-prefs) 키는 아직 `transactions.outbound-status.*` 공용이라
  4개 현황이 컬럼 표시/순서를 공유한다. 같은 표라 무해하지만 화면별 분리 여지는 남는다.

## DEC-195 — 신간발행(Menu209)을 입고현황과 «같은 3뷰 공용 축»으로 + 공용 화면의 접수 도메인(kind) 분리

- **일자**: 2026-08-25
- **요청**(사용자): "신간발행 화면을 입고현황 (목록, 상세 …) 화면과 동일한 폼으로 수정해줘".
- **축 결정 — 신간발행 = 입고현황 ∩ 전표구분 「신간」**.
  레거시 `Subu29`(신간명세서)는 거래처축(`Scode='X'`) 명세 폼이지만, 교문사(5019, remote_153)
  실데이터의 「신간」은 **입고처축 입고 라인**이다:
  `Scode='Y'`+`Gubun='입고'`+`Pubun='신간'` **1,155행**(2011~2026.08, 현행) vs
  `Scode='X'`+`Gubun='출고'`+`Pubun='신간'` 314행은 **전부 2007~2015 구데이터**.
  메뉴 위치도 입고관리 아래(form-registry 별칭, 2026-08-22 운영 요청)라 업무 의미와 맞는다.
  → `_GUBUN_IN_NEW_RELEASE = "Gubun = '입고' AND Pubun = '신간'"` 한 절만 입고현황과 다르고,
  고정 조건(`Scode='Y' AND Gcode<>''`)·표시명 원천(G2_Ggwo)·집계 주 거래구분('입고')은 동일.
- **폐기된 것**: 기타명세서 facade(`list_other_statements(pubun='신간')`)·Sobo29 위젯 ID 부착·
  전체메모(S1_Memo) 편집. 전체메모는 기타명세서(`/transactions/other`)에 그대로 남는다.
  종전 API 응답 형태(OtherStatementsResponse)도 사라진다 — 호출자는 이 화면뿐이었다.
- **공용 화면에 접수 도메인(`TransactionStatusAxis.kind`)을 도입** — 이관 중 발견한 결함.
  `TransactionStatusScreen` 의 상세 우측 라인·편집 팝업·바로출고·바로재출고·거래명세서 출력이
  전부 **출고 전용**(`outboundApi.detail`, `OrderDetailDialog`, `requestDispatch`, 거래명세서 PDF)
  이었다. DEC-194 로 입고현황이 이 화면에 합류했을 때 그대로 물려받아, 입고 전표의 「수정」이
  **출고 주문 팝업**(PUT `/outbound/orders`)을 열고 바로출고 버튼이 입고 전표에 노출되는 상태였다.
  - `kind: "outbound"`(기본, 출고/반품/폐기) — 종전 그대로.
  - `kind: "inbound"`(입고현황·신간발행) — 상세 라인 `inboundApi.detail`(라인 `bname` →
    `product_name` 으로 맞춰 같은 표), 편집 `ReceiptDetailDialog`(PUT `/inbound/receipts/{key}`),
    출고 전용 버튼 3종(배치 툴바·단건 바로출고·단건 출력)은 렌더하지 않는다.
  - 저장 후 재조회는 `onSlipChanged` 하나로 모아 축별 상세 API 를 탄다.
- **구현**: `backend/app/routers/transactions.py`(`/new-release` 3뷰 축 라우트) /
  `backend/app/services/transactions_service.py`(`_GUBUN_IN_NEW_RELEASE`) /
  `frontend/src/components/transactions/transaction-status-screen.tsx`(`kind`·`fetchDetailLines`·
  `onSlipChanged`·`NEW_RELEASE_AXIS`) / `frontend/src/app/(app)/transactions/new-release/page.tsx`
  (래퍼 17줄) / `frontend/src/lib/inquiry-api.ts`(`newRelease`) / `frontend/src/lib/form-registry.ts`
  (crudNotes) / `migration/contracts/new_release.yaml`(variant)
- **회귀**: `test/test_new_release_phase1.py`(재작성 — 축 계약 5 + 화면 5) /
  `test_inbound_status_phase1.py`(`kind: "inbound"` 가드) / `test_shipment_transactions_lookup_apply.py`
  (래퍼 추적) / `test_outbound_status_print_on_this_pc.py`(저장 후 재조회 경로 = `onSlipChanged`).
  DB 스모크 `transactions.new_release{,_detail,_summary}`.
- **미해결**: 컬럼 설정(grid-prefs) 키는 5개 현황이 `transactions.outbound-status.*` 공용(DEC-194 잔여).

## DEC-196 — 거래처별판매(Sobo62): 기본 집계는 거래처(Gcode) 단위 — 「지점별검색」 체크 시에만 지점 분리

- **일자**: 2026-08-25
- **리포트**(사용자): "통계관리-거래처판매 검색 자료값 중 일부 거래처의 자료들이 미반영된 것
  같다. 상단=거래처판매내용 / 하단=지정 거래처 세부내용이 출력되어야 하는데 지금은
  거래처세부내용들이 보인다." + 화면명 「거래처별판매」로 변경.
- **원인**: 모던 `get_customer_sales` 가 **항상** `(Hcode, Gcode, Gjisa)` 로 행을 만들었다.
  레거시 `Subu62.Button101Click`(L330~335)은 `CheckBox1`「지점별검색」이 켜졌을 때만
  `St6:=Gjisa` 이고 아니면 `''` 로 `Locate('Gcode;Gjisa')` → **기본은 거래처 단위 합산**.
  교문사(5019) 2026-08 실측: 교보문고(00001)가 「본사 0부/0원(수금만) · 부곡리(매장) 30 ·
  부곡리(본관) 458」 3행으로 갈려 **거래처 행이 0 으로 보였다** — "미반영"의 정체. 같은 식으로
  6개 거래처(영풍문고 5지점, 예스24, 전남대생협, 고성도서유통, 연세대생협)가 쪼개져 있었다.
  하단 상세(`get_customer_sales_detail`)도 `COALESCE(Gjisa,'')=%s` 로 지점 하나만 보여
  거래처 전체 세부가 아니었다(레거시 `Button201Click` 은 `Gcode=St3 and Scode=St2` — Gjisa 절 없음).
- **결정**:
  1. `by_branch`(API `byBranch`, 기본 False) 도입 — False 면 지점을 거래처 행으로 합산,
     True 면 종전처럼 (Gcode, Gjisa) 행. 집계·상세·엑셀 세 경로 동일 파라미터.
  2. 상세는 `by_branch` 일 때만 `Gjisa` 로 좁힌다(기본 = 거래처 전체).
  3. 화면에 레거시 `CheckBox1` 동등 「지점별검색」 체크박스(`Sobo62.CheckBox1`, 기본 해제,
     세션 스냅샷 보존). 지사 컬럼은 종전대로 기본 숨김.
  4. 집계 분기에 `Gubun='입고'` 추가(입고처 Y 모드 대비, Subu62 L365~369) — X 모드 영향 없음.
  5. 화면명 「거래처별판매」(사이드바 caption·h1). 레거시 Menu602 caption 은 「거래처판매」라
     매트릭스 `CAPTION_ALLOWLIST_MISMATCH` 에 등재(OK_EXEMPT).
- **실측**(교문사 5019, 2026-08-01~25): 기본 155행(거래처 수와 동일) — 교보문고 1행
  **488부 / 14,411,450원 / 수금 85,629,320**; 하단 상세 167종·출고 488 (거래처 합과 일치).
  지점별검색 ON → 168행, 교보문고 3행(종전 형상). 거래처 단위 합은 SQL 직접 집계와 152/152 일치.
- **구현**: `backend/app/services/reports_service.py`(`by_branch`) / `backend/app/routers/reports.py`
  (`byBranch` ×3) / `frontend/src/app/(app)/reports/customer-sales/page.tsx` / `frontend/src/lib/inquiry-api.ts`
  / `frontend/src/lib/form-registry.ts` / `tools/delphi_form_screen_matrix.py`(allowlist)
- **회귀**: `test/test_customer_sales_detail.py`(기본=거래처 전체 / by_branch=지점) +
  `test/test_dec196_customer_sales_branch_merge.py`(신규).

## DEC-197 — 거래처별판매·도서별판매 합계 행(전체 결과) + 거래처별판매 하단은 검색 직후 «전체 거래처» 도서별

- **일자**: 2026-08-25
- **레거시 엑셀 대조**(사용자 제공 「통계관리_거래처판매(260824).xlsx」, 교문사 5019):
  조회 기간은 파일에 없어 교보문고 행(출고 3,087 / 80,960,430)과 거래처 수 140 을 재현하는
  기간을 탐색 → **2026-07-24 ~ 08-24** 확정. 결과:
  - 상단 140/140 거래처 존재, 불일치 7건 = 전부 export 이후 입력분(계명문화대 +12부는 8/25
    10:49 입력(Gdate 8/24), 수금 6건은 8/24자 입금 ID 1187837~1187844 연속 배치). 모던에만 있는
    1건(경화서점 수금 85,500)도 같은 배치.
  - 하단 시트 「지정거래처-하단출력(내용 전체)」는 **전체 거래처의 도서별 합**(합계가 상단
    합계와 동일 12,558 / 315,328,625) — 레거시 `Button201Click` 의 `T00=1` 모드(검색 직후
    하단 DBGrid201 은 전체, 거래처를 고르면 `Gcode=` 로 좁힘). SQL 동등 집계와 682/682 도서
    일치, 불일치 1건(공중보건학 5판 +12)은 위 계명문화대 입력분.
  → **기간이 같으면 상단·하단 100% 일치.**
- **요청**(사용자): "각각 레거시 화면처럼 하단에 합계가 보이도록" / "도서별 판매 화면에 대해서도
  합계 출력 필요".
- **결정**:
  1. `get_customer_sales` 가 `totals`(goqut/gosum/gjqut/gbqut/gbsum/gsusu/gjsum/gssum, 검색 결과
     전체·페이지 무관)를 돌려주고 상단 DataGrid 에 합계 행(레거시 DBGrid101 Footer fvtSum).
  2. `get_book_sales`(목록)에도 `totals` — 종전엔 일별 API 에만 있어 화면 합계 행이 비어 있었다.
  3. 거래처별판매 하단 = 검색 직후 **전체 거래처 도서별**(`gcode` 생략), 거래처 선택 시 그
     거래처(재선택 시 전체로 복귀). `get_customer_sales_detail` 의 `gcode` 옵션화.
- **구현**: `reports_service.get_customer_sales/get_book_sales/get_customer_sales_detail`,
  `routers/reports.py`, `models/inquiry.py`(`CustomerSalesResponse.totals`),
  `reports/customer-sales/page.tsx`(`topTotals`·`loadDetail`).
- **회귀**: `test/test_dec197_customer_sales_totals_all_detail.py`(8).

## DEC-198 — 엑셀 내보내기 = 화면에 보이는 컬럼·순서 / 도서별판매 도서분류 응답 누락 수정

- **일자**: 2026-08-25
- **원칙**(사용자): "엑셀 출력은 화면에 보이도록 설정된 필드가 동일한 순서로 출력되어야 한다."
- **리포트**: "도서별판매 엑셀 다운 시 누락 출력 컬럼이 있다" / "도서별판매 화면에 도서분류가
  출력되지 않는다".
- **원인**:
  1. 엑셀은 서버 고정 목록(`_BOOK_SALES_EXPORT_COLUMNS` 등)이라 화면의 도서분류·판매수량·
     판매금액·재고 3종이 빠지고, 사용자가 컬럼 설정으로 바꾼 숨김/순서도 반영되지 않았다.
  2. `BookSalesRow` 응답 모델에 `sname`/`gubun_code` 가 없어 서비스가 부착한 도서분류를
     FastAPI `response_model` 이 잘라냈다(DEC-169 ISBN 누락과 같은 유형 — **부착 필드는 반드시
     모델에도 선언**).
- **결정**: 내보내기 라우트가 `columns`(JSON `[{key,label}]`)를 받아 **그 키·라벨·순서 그대로**
  쓴다. 화면은 `visibleColumns`(컬럼 설정 반영)를 넘긴다. 키는 화이트리스트(임의 필드 유출
  방지, 위반 시 422), 화면 파생 키(판매수량/판매금액/재고 3종)는 서버가 같은 산식으로 채우고
  재고 키가 있을 때만 기간말 재고를 부착한다. `columns` 미전달(구 클라이언트)은 종전 목록.
  대상: 도서별판매·거래처별판매. (년말집계 등 다른 내보내기는 후속.)
- **구현**: `routers/reports.py`(`_parse_export_columns`·`_derive_book_sales_export_fields`),
  `models/inquiry.py`(`BookSalesRow.sname/gubun_code`), `lib/inquiry-api.ts`(`ExportColumn`),
  두 page.tsx.
- **회귀**: `test/test_dec198_export_follows_visible_columns.py`(7) — 헤더 순서·숨김 반영·
  파생값·화이트리스트 422·기본 목록 호환·모델 필드·화면 배선.

### DEC-198 보강 — 일괄 적용 (2026-08-25, 사용자 "일괄 적용해 주세요")

- **범위**: 엑셀 저장 버튼이 있는 목록 화면 **17곳 전부**(도서별·거래처별판매 포함) /
  내보내기 라우트 **14곳** — reports(도서별판매·거래처별판매·년말집계), stats(기간별매입매출·
  거래처판매분석·도서회전율·출판사통계·분기요약), returns(재고원장·기간별반품·일별반품),
  settlement(청구년월·발송비내역·발송비현황). **제외**: 기초관리 마스터 내보내기
  (customer/book/authors/inbound-vendors — 재입력 템플릿이며 이미 `fields` 파라미터로 선택 저장),
  호출 화면이 없는 라우트(cash-status·billing·outstanding·tax-invoice·returns receipts).
- **공용 리졸버** `app/services/export_columns.py::resolve_export_columns(spec, default, fields, rows)`:
  화면 키 → (1) 라우트 `fields` 별칭/파생 → (2) 기본 목록 키 → (3) **행에 실제 있는 키**(목록 API
  가 이미 노출한 필드라 새 유출 아님) → 그 외 422. 라우트별 화이트리스트를 손으로 유지하지
  않아도 되고, 화면 키가 행 키와 다른 화면(반품원장 `book_name`·정산 `name1`·발송비 `name1/2`)은
  (3)으로 자동 해결됐다. 파생이 필요한 곳만 `fields` — 기간별매입매출 `group_by`(표시 라벨),
  도서별판매(판매수량/판매금액/재고 3종).
- **다중 시트**(분기요약): 월별 시트만 화면 컬럼, 「분기 비교」 시트는 화면 고정 표라 기본 유지.
- **실DB 종단 점검**(교문사 5019, 2026-07-24~08-24): 15개 화면 키 목록 전부 200·헤더 순서 일치
  (년말집계 4,783행·반품원장 1,299행·거래처판매분석 1,320행·도서회전율 2,000행 …).
- **화면 함정**: 엑셀 저장 핸들러가 `useCallback` 이라 `visibleColumns` 를 deps 에 넣지 않으면
  첫 렌더의 컬럼으로 굳는다(컬럼 설정 변경이 엑셀에 안 실림) — 17곳 deps 보강, eslint
  exhaustive-deps 가 가드.
- **회귀**: `test/test_dec198_export_columns_batch.py`(11) — 리졸버 규칙 5 · 라우트 3(집계단위
  라벨·분기 다중시트·일별반품) · 화면 17곳 배선 · API 4개 lib 전달.


## DEC-199 — 기본 화면 디자인 1차 적용 (사용자 목업 2026-08-25)

- **일자**: 2026-08-25
- **요청**(사용자): "디자인 개선을 위해 기본 화면 디자인 목업 파일이다. 1차적으로 적용할 수 있는
  부분을 반영해서 기본 디자인으로 적용해라. 작업전 커밋 및 푸시 후 적용."
- **목업 해석**: 최상단 전폭 흰 헤더(워드마크 「bukio WORKS」 · 우측 「(주)교문사 | 경리부」) /
  어두운 회색 사이드바(상단 진회색 접기 박스 «, 아이콘+메뉴+›) / 회색 탭 바에 라임 pill 활성 탭 /
  연회색 콘텐츠 캔버스 + 「대시보드」 제목 밑줄.
- **1차 적용 범위 결정 — 토큰 + 셸 4파일만**(화면 페이지 무수정, Design.md §8-4 OCP):
  1. `globals.css :root` — `--background` #F5F5F5(캔버스), 사이드바 5토큰 어두운 톤, 신규 토큰
     `--sidebar-header`/`--tabbar`/`--tab-active`/`--tab-active-foreground`(+`@theme inline`, `.dark`).
  2. `(app)/layout.tsx` — 헤더를 최상단 전폭으로, 그 아래 [사이드바 | 캔버스].
  3. `header.tsx` — 워드마크(마케팅 PNG; CMS 전용 SVG 자산은 §9 미수신) + 사용자 칩
     「회사 | 사용자」. 계정 유형·상위 총판 뱃지는 드롭다운으로. 화면 제목 표기는 활성 탭이 대신.
  4. `sidebar.tsx` — 회사/로고 블록을 접기 박스(«/»)로 교체(중복 제거), 밝은 배경 전제 클래스
     (`text-muted-foreground`·`bg-muted/*`·`text-foreground`)를 전부 사이드바 토큰으로.
  5. `workspace-toolbar.tsx` + `workspace-canvas.tsx` — 탭 줄과 도구 줄(탭/바둑판/자유창·창 수·
     모두 닫기)을 회색 한 줄로 합치고 활성 탭을 라임 pill 로.
- **Vivid Lime 예외**: Design.md §8-1 은 CTA/알림 외 금지지만, 목업이 «현재 화면» 표시(활성 탭)에
  쓰므로 `--tab-active` 한 토큰에 한정해 허용. `--primary`/`--sidebar-primary` 는 여전히 중립.
- **보류(후속)**: 페이지 제목 밑줄(각 화면 h1 — 페이지 수정 필요), 메뉴명 띄어쓰기 표기
  (「출고 관리」 — 내용 정책), 헤더 시계·날씨 위젯(목업엔 없으나 운영 기능이라 유지), 계정별
  `[data-theme]` 10종의 사이드바 톤 재정렬, CMS 워드마크 SVG 자산.
- **검증**: `test/test_dec199_base_design_shell.py`(9) + `test_theme_contrast_guard`(사이드바 대비) +
  브라우저 실측(교문사 계정, 워크스페이스).

### DEC-199 보강 — 로고 투명화 (2026-08-25, 사용자 제공 「bukio WORKS」 이미지)

- 사용자 이미지(흰 바탕 + 연회색 격자 위 진회색 워드마크, 1572×386)를 명도 기반 알파
  (gray ≥205 → 투명, ≤90 → 불투명, 사이 선형 램프)로 배경·격자 제거 → 잉크를 Bukio Black
  `#282828` 로 통일한 투명 PNG `public/brand/bukioworks-wordmark.png`(1459×245, 격자 잔여 alpha 0)
  + 어두운 배경용 `-light.png`(Inverse Text 잉크).
- `Logo` 에 `variant="wordmark" appearance="cms"`(+`tone`) 분기 신설 — 앱 셸 헤더·로그인 페이지가
  사용. 마케팅 랜딩·공지·풋터의 라임 바탕 워드마크는 그대로(마케팅 자산).
- 가드: `test_dec199_base_design_shell.py::test_header_and_login_use_transparent_cms_wordmark`
  (자산 존재·모서리 alpha 0·분기·헤더/로그인 배선).


### DEC-199 보강 — 사이드바 플라이아웃 · 시계/날씨 위젯 (2026-08-25 13:03~13:04)

- **사이드바 목업**: 대메뉴 행(아이콘·라벨·›)을 누르면 오른쪽에 서브메뉴 패널. 현재 화면(포커스
  창)이 속한 대메뉴·항목 = 라임(`--nav-active` 신설, `--tab-active` 도 이를 참조), 열린 다른 창 = ✓.
  사용자 제약 "메뉴 순서 등은 수정 금지" — `MENU_GROUPS`/`SIDEBAR_LAYOUTS`(항목·구분선·서브그룹
  순서)를 그대로 그리고 렌더링만 아코디언→플라이아웃으로. 닫힘 = 바깥 클릭·Esc·iframe 포커스 이동
  (window blur — 캔버스가 iframe 이라 document mousedown 이 오지 않는다). 접힘 모드도 같은 패널.
  `position: fixed`+`z-50` 으로 aside 의 overflow-hidden 과 iframe 위를 넘는다.
- **시계·날씨 위젯**: 흰 헤더에 맞춰 검정 박스·라임 글로우·rgba 그림자 제거 → `text-foreground`/
  `text-muted-foreground`. 13:12 「테두리 제거」— 카드 `border-border`·`shadow-sm` 도 제거(텍스트만).
- **함정**: Next(Turbopack) dev 서버가 globals.css 의 두 번째 토큰 추가(`--nav-active`)를 반영하지
  않아 클래스는 붙는데 배경이 투명이었다. `./restart.sh frontend` 만으로는 **안 낫고** 서빙 CSS 에
  첫 편집본(`--tab-active: var(--vivid-lime)`)이 그대로 남았다 — `.next` 캐시를 지우고 재기동해야
  했다(`./stop.sh frontend && rm -rf 도서물류관리프로그램/frontend/.next && ./start.sh frontend`).
  토큰을 추가했는데 화면에 안 보이면 먼저
  `getComputedStyle(document.documentElement).getPropertyValue('--토큰')` 을 본다.
- 가드: `test_dec199_base_design_shell.py`(12) — 플라이아웃 구조·nav-active 토큰·시계 위젯 클래스.

### DEC-200 — 화면 상단 흰 띠(PageHeader) 전 화면 일괄 반영 (2026-08-25 13:18)

- **요청**: 「도서별 수불원장 디폴트」 목업 — "반영할 요소 추출해서 모든 화면에 동일하게 반영".
- **추출 요소**: ① 제목 좌 + 필터·「검색」 우가 한 흰 띠(전폭, 아래 경계선, 카드 프레임 없음) ② 필터
  라벨 인라인 ③ 「검색」 Bukio Black 채움 ④ 회색 캔버스 위 프레임 없는 가운데 안내문(조회 전).
- **방식**: 공용 컴포넌트가 없어(81개 화면이 같은 `<h1>`+부제 블록, 46개가 같은 필터 카드 문자열 복제)
  `components/shared/page-header.tsx` 를 신설하고 scratch 스크립트(JSX-lite 스캐너 — 속성 안
  `{…}`/`=>`/문자열을 건너뛰며 요소 짝 맞춤)로 106개 파일을 일괄 이관: 제목 블록(`<div>`/`<header>`
  래퍼, bare h1, 뒤로가기 링크 행, `justify-between` 액션 행) + 인접 액션 행 + 인접 필터 카드 →
  `<PageHeader title subtitle leading titleAside actions>{필터}</PageHeader>`. 40개는 필터까지 병합,
  66개는 띠만(필터가 인접하지 않거나 등록 폼 패널 — `h2` 있는 패널은 필터로 보지 않음).
- **보존 규약**: 필터 컨테이너의 `onKeyDown`(DEC-104/105 Enter 이동)·`data-legacy-id`·`ref` 는
  `display:contents` 래퍼로 남긴다(첫 시도에서 버려져 `advanceFilterOnEnter` 미사용 경고로 발각 →
  되돌리고 재적용). `PortalScreenTitle` 은 `PageHeader` 위임.
- **부제 유지**: 목업엔 없으나 운영 설명이라 제목 옆 작은 글자로(좁으면 숨김) — 내용 삭제는 설계 범위 밖.
- **대표 화면 기본 상태**: `/inventory/ledger` 조회 전엔 하단 상세 카드까지 숨기고 「거래일자와
  도서명으로 검색하세요」 한 줄(`EmptyHint`).
- **미적용(후속)**: 날짜 범위 한 알약(DEC-115 3분할 우선), 라벨을 입력 안 칩으로, 다른 화면의 조회 전
  표 카드 숨김(화면별 상태 판단 필요).
- 가드: `test_dec200_page_header_band.py`(컴포넌트 계약·이관 커버리지≥95·프레임 잔존 0·속성 보존·검정
  버튼·대표 화면). 전체 스위트 2366 통과, tsc 클린.

### DEC-201 — 시계·날짜·날씨는 브라우저 위치 권한 후 위치 반영 (2026-08-25)

- **규칙(사용자)**: "시간, 날짜 정보 관련해서는 현재 브라우저 위치 정보 접근 허가를 득한 뒤 위치정보를
  반영해야한다."
- **원인**: 헤더 위젯이 「서울」 고정 — 계정 지역이 `source: "manual"`(구 프리셋 키 이관 시 일괄
  manual)이라 `setGeolocationRegion` 이 조기 반환, 브라우저 권한이 granted 인데도 미반영. 「나중에」는
  localStorage 영구 dismissed 라 재요청도 없었다.
- **결정**: 권한 허용 시 **위치 우선**(manual 가드 제거, 수동 프리셋은 권한 없는 동안의 폴백).
  `navigator.permissions.query` 로 granted → 묻지 않고 반영(+`onchange` 재반영), denied → 조용히 유지,
  prompt → 배너. 「나중에」는 sessionStorage(이번 접속만). effect 본문 setState 는 마이크로태스크.
- 가드: `test_dec201_location_permission_first.py`.

### DEC-202 — 검색 필드 빈값 Enter: 이동 스코프 없는 화면은 팝업 (2026-08-25)

- **확인 요청**: "도서 검색 창에서 빈입력창 또는 키워드 입력해서 엔터 → 검색창이 떠야 / 값을 선택하면
  코드·도서명이 자동 입력돼야."
- **점검 결과**: 키워드 Enter → 팝업(다건)/자동확정(1건 정확 일치, DEC-134), 선택 → 입력창에 코드 +
  옆에 도서명·정가 + 즉시 조회 — 모두 정상. **빈값 Enter 만** 도서별수불원장·거래처거래원장에서 죽어
  있었다: MLF 에 빈 `onKeyDown={() => {}}` 를 넘겨 「통과」 경로를 타는데 패널에 Enter 이동
  스코프(`advanceFilterOnEnter`/`data-enter-scope`)가 없어 아무 데도 가지 않았다.
- **결정**: 빈 핸들러는 **패널 Enter 이동 스코프가 있을 때만** 쓴다(DEC-104/105/144 = 빈값 Enter →
  다음 입력칸, 36개 화면 유지). 스코프가 없는 두 화면은 빈 핸들러를 제거 → MLF 기본(빈값 Enter=검색
  팝업, 레거시 Seek 폼과 동일). 가드: `test_dec202_lookup_empty_enter_popup.py` — 빈 핸들러가 있는
  화면은 반드시 스코프를 가져야 한다(죽은 Enter 0).

### DEC-203 — 표(목록) 공통 디자인 · 섹션 헤더 · 「내용 전체 보기」/엑셀/출력 (2026-08-25 14:30~14:42)

- **요청**: 도서별 수불원장 결과 목업(14:30) + 「내용 전체 보기」 정의(14:31: 체크하면 거래일자 표가
  스크롤 없이 모두 보이도록 영역 자동 확장) + 거래처 원장 디폴트(14:34)·상세(14:41) 목업 —
  "표(목록) 등에 대한 부분은 모든 화면에 공통 적용".
- **공통 반영**(Design.md §7.5): 표 프레임 제거(`LIST_TABLE_SCROLL_CARD_CLASS`·DataGrid·인라인 12파일),
  회색 헤더행 `--table-head`, 선택 행 `--row-selected`(민트), 포커스 행 `--row-focus`(파랑, DataGrid
  `group/dg` + `group-focus-within`), 합계행 회색·굵게, 표 제목 h2 상향(27파일).
- **섹션 헤더** `components/shared/section-header.tsx` — 제목+메타+액션. 「내용 전체 보기」 = `showAll`
  → 표 `overflow-visible`·높이 상한 해제 + `SplitListPanes disabled` (스택). 
- **엑셀/출력**: 범용 `POST /api/v1/export/table-xlsx`(`routers/export_table.py`, 인증만, 행 상한
  50,000, 화면 표시 컬럼 순서 그대로 — 엑셀 규칙 정합) + `api.postBlob` + `lib/table-export.ts`
  (`exportTableXlsx`/`printTable`). 새 창 인쇄는 표만.
- **거래처 원장 표 컬럼**(14:41 목업): 「외N」 컬럼을 거래내역 「… 외」로 접고 출고종수(=1+외N),
  판매수량/판매금액(=출고+반품, 반품 음수 관례 가산 → 목업 합계 14,739−1,115=13,624 일치) 추가.
  상세 「%」→「공급률(%)」(두 원장 공통).
- **2단 분할**(14:29 요청): 두 원장 화면 `SplitListPanes`(구분선 드래그) — 일자/전표 미선택·전체 보기면
  스택.
- **함정 재발**: 새 CSS 토큰이 Turbopack 캐시로 비어 나옴 → `.next` 삭제 재기동(메모리 기록 그대로).
- 가드: `test_dec203_table_design_common.py`(토큰·상수·DataGrid·프레임 잔존 0·섹션 헤더·두 원장 화면·
  컬럼 순서·백엔드 라우트 xlsx 생성/행 상한).

### DEC-204 — 입고현황 「선택 삭제」: 입고 명세서 통째 삭제 (2026-08-25 14:53)

- **요청**: "해당 명세서를 완전 삭제하라고 하는데 안 되는 것 같다. 명세서 선택 삭제 추가 가능?" — 입고
  명세서는 수정 다이얼로그의 행 삭제(소프트 취소 Yesno='2')만 있어 물리 삭제 경로가 없었다.
- **결정**: `DELETE /api/v1/inbound/receipts/{receipt_key}` 신설 — 전표의 입고 라인(`Scode='Y'`) 전부
  DELETE. 스코프는 취소와 같은 `_SQL_INBOUND_ROW_WHERE`(헤더키+Scode='Y', DEC-174 출고 전표 보호).
  **상태 잠금 없음** — 레거시 입고 폼(Subu22)에 삭제 잠금이 없고 요청이 「완전 삭제」(출고 거래명세서의
  완료/확정 잠금과 의도적으로 다름). 메모(S1_Memo)는 같은 헤더키 라인이 0건일 때만 삭제(출고와 공유
  가능). hcode 는 `enforce_hcode_identity` 로 로그인 소유 고정, audit.inbound `deleted`.
- **화면**: 공용 현황 화면(`transaction-status-screen.tsx`) 입고축에만 「선택 삭제 (N건)」 destructive
  버튼 → `ConfirmDialog(danger)` → 체크 전표 순차 삭제 → 결과 요약(성공/실패 전표번호) → 목록 재조회,
  열려 있던 상세 닫기. 출고축(출고현황)엔 렌더하지 않는다.
- **DEC-012 대체**: 1차 결정(물리 삭제 미제공, 소프트 취소만)은 입고 명세서에 한해 이 요청으로
  대체된다(`test_c3_inbound_phase1` 의 405 가드 → 라우트 존재 가드로 교체). 출고 주문 DELETE 미제공은 그대로.
- 가드: `test_dec204_inbound_receipt_batch_delete.py`(서비스 스코프·메모 조건·404·라우트·감사 어휘·화면
  배선). 운영 DB 에서 실제 삭제는 실행하지 않고 버튼·확인창까지만 검증.

### DEC-205 — 재고현황 목업: 도서 단위 단일 표 + 번호형 페이저 (2026-08-25 15:06~15:07)

- **요청**: 재고 현황 목업 2장(기본: 「전체 기간」 헤더 + 도서코드·도서명·ISBN·정가·입고·출고·반품·폐기·잔량
  단일 표 + 하단 가운데 « ‹ 1 2 3 4 5 … 100 › » 페이저 / 특정 도서 선택: 「도서명 코드  기간」 헤더 + 1행).
- **구조 변경**: 2026-08-22 요청으로 만든 분류→도서 2단(SplitListPanes)을 **도서 단위 단일 표 기본**으로.
  분류 롤업은 섹션 헤더의 「분류별 집계」 체크로 유지(분류 행 클릭 → 그 분류 도서만, 「분류 해제」).
  기본 표시 컬럼은 목업 9개(전재고·반입·증정·변경·재고(반)은 「컬럼」에서 켤 수 있음, `defaultHidden`),
  「현재고」 라벨 → 「잔량」. 도서 행에 ISBN 부착(`attach_book_meta`, price 미변경, 실패 무시).
- **페이저(공통)**: `DataGridPager` compact 변형을 번호형(현재 페이지 라임 원, 처음/이전/다음/끝)으로 바꾸고
  DataGrid footer 가운데 슬롯에 놓았다 — 하단 페이저를 쓰는 모든 표에 적용. 재고현황은 응답이 전체 행이라
  클라이언트 페이지(정렬 후 slice, 기본 100건).
- 섹션 헤더: 도서 1종 → 「도서명 코드 기간」, 분류 선택 → 「분류 · 이름」, 아니면 「전체 기간 · N종」.
  엑셀 다운로드/출력은 현재 보이는 컬럼·행(DEC-203 범용 경로).
- 조회 전: 「거래일자와 도서명으로 검색하세요」(EmptyHint).

### DEC-206 — 거래 명세서 상세 팝업: 거래일자 수정 + 팝업 드래그 이동 (2026-08-25 15:39)

- **요청**: 상세 팝업 스크린샷에 "날짜도 수정 가능하게" / "팝업창을 원하는 위치로 이동하게 될까요?".
- **일자 수정**: DEC-078(거래명세서 편집 폼)의 정밀 스코프 이동을 **출고 주문 PUT**(`update_order`)에도
  넣었다 — `newGdate` 가 현재와 다르면 라인 diff 보다 먼저 `UPDATE S1_Ssub SET Gdate=new WHERE 옛 키
  (거래처·지점 스코프)` 후 diff 는 새 일자 키로, 전표번호 Idnum 유지(DEC-078 합의: 대상 일자 중복 허용).
  상세 팝업 일자 = `DateFieldYMD`(취소 전표는 읽기 전용), 「라인 저장」에 함께 실려 저장되며 일자가 바뀌면
  팝업의 키가 낡으므로 목록 새로고침 후 닫는다. 입고 상세는 요청 범위 밖(필요 시 같은 방식).
- **드래그 이동**: 공용 `useDraggablePanel(open)` — 헤더 pointer 드래그, `transform: translate` (Tailwind v4
  `translate` 유틸과 충돌 없음), 열릴 때 원위치, 버튼/입력 위 드래그 무시. 거래 명세서 상세·입고 명세서 상세·
  도서/거래처 검색 팝업에 적용.
- 가드: `test_dec206_detail_dialog_date_and_drag.py`(이동 문장 선행·스코프·새 일자 diff·동일 일자 무이동·
  계약·화면 배선). 운영 데이터로 실제 일자 이동은 실행하지 않고 UI 까지만 확인.

### DEC-207 — 출고현황 상세 「선택 삭제」 + 재고현황 라벨 「현재고」 (2026-08-25 17:00~17:08)

- **요청**: "출고현황 - 상세 화면에서 출고명세를 선택하면 삭제할 수 있는 기능이 활성화되도록" / 재고현황
  「잔량」 항목을 「현재고」로.
- **결정**: 공용 현황 화면의 「선택 삭제」를 출고축에도 렌더 — 출고는 기존 `DELETE
  /api/v1/transactions/sales-statement/{order_key}`(완료·확정 Yesno 1·2 잠금 → 422 STATEMENT_LOCKED)를 그대로
  쓰고, 잠긴 전표는 결과 요약의 실패 목록(전표번호·사유)에 남는다. 입고축(DEC-204)은 잠금 없음 그대로.
- 재고현황 컬럼 라벨은 목업의 「잔량」 대신 레거시 용어 「현재고」 유지(사용자 지시).
- **인프라 사고 정리(같은 날)**: 허브 `pre-push` 훅이 제품 저장소에 `git add -A` 로 런타임 산출물
  (`.run/logs`, `backend/data/login_id_index.json`)까지 sync 커밋했고, 허브 테스트가 모듈 로드 후 실제
  인덱스 파일을 덮어써 13k행 → 5행이 푸시됐다. 복원(제품 18abd16) + 훅 pathspec 제외 + `test/conftest.py`
  에서 `BLS_LOGIN_ID_INDEX_PATH` 를 임시 경로로 고정.

### DEC-208 — 입고·출고 상세 도서명 hcode 스코프 + 신간발행 우측 라인 「신간」만 (2026-08-26 01:00)

- **보고**: 신간발행 우측 「선택 전표 라인」에 재생 라인까지 보이고, 3063 도서명이 「당신을버릴때」(교문사 도서
  아님; 레거시 입고명세서는 「패션과 영상문화 2판」).
- **원인**: `_fetch_product_names`(입고·출고 서비스 각각)가 `G4_Book` 을 **Hcode 없이** `Gcode IN` 으로만
  찾아 같은 코드를 쓰는 다른 출판사의 도서명을 가져왔다 — 공유 테이블 fail-open(DSN-DEC-12 위반). 목록
  경로는 다른 조회를 써서 정상이라 상세에서만 드러났다.
- **결정**: `scope_hcode` 인자를 두고 상세·목록 호출부가 로그인 hcode 를 넘기면
  `book_meta_lookup.fetch_book_meta`(로그인 출판사 → Hcode='' 공용 마스터 2단계, 레거시 Subu24 동등)만
  쓴다. 다른 테넌트 행은 절대 안 쓴다(코드가 없으면 빈 이름). 무스코프 경로는 관리자 전체 목록 등 스코프가
  없을 때만.
- **신간발행 축**: `TransactionStatusAxis.linePubun`(신간발행=「신간」) — 우측 라인을 전표구분으로 걸러
  목록 행의 항목수/수량(신간 롤업)과 같은 범위. 수정 팝업은 전표 단위라 모든 라인 그대로.
- 가드: `test_dec208_book_name_hcode_scope.py`.

### DEC-209 — 거래 명세서 상세 팝업: 단가 편집 + 단가·공급율·비고 변경 저장 (2026-08-26 01:02)

- **요청**: "팝업 내 추가 수정 가능 값 및 팝업 창 이동 가능하도록" (이동은 DEC-206).
- **발견**: 상세 팝업 「라인 저장」(`update_order`)의 기존 라인 UPDATE 가 Pubun/Gsqut/Gssum 만 비교·갱신해
  팝업에서 고친 공급율·비고(그리고 새로 연 단가)가 **조용히 버려졌다**(신규 라인 INSERT 는 동적 컬럼으로
  이미 저장). DEC-078 편집 폼 경로는 저장하던 값이라 두 경로가 어긋나 있었다.
- **결정**: 존재 컬럼(`_OPTIONAL_LINE_COLS` Gdang/Grat1/Gbigo)을 SELECT 로 읽어 비교하고 UPDATE SET 에
  포함(DDL 드리프트 서버는 자동 제외). 라인 그리드 단가를 입력 셀로(콤마 표시, 변경 시 금액 = 단가×공급율×
  수량 자동 재계산, Enter 흐름 포함).
- 가드: `test_dec209_detail_dialog_price_rate_memo_persist.py`(공급율·비고 저장, 단가만 변경, 무변경, DDL
  드리프트, 그리드 단가 입력).

### DEC-210 — 도서별 판매 「내용 전체 보기」 (2026-08-26 09:25)

- **요청**: 도서별 판매 화면에 「내용 전체 보기」 체크·기능 추가(재고현황·원장과 같은 의미).
- **결정**: DataGrid 에 `unbounded` 모드(뷰포트 상한·내부 스크롤 해제, fillHeight 우선) 신설 → 도서별 판매
  상단 표는 체크 시 `unbounded` + `SplitListPanes disabled`(스택). 서버 페이지는 그대로(현재 페이지 행을
  모두 펼침 — 행 수는 「페이지당」으로 조절). 다른 DataGrid 화면도 같은 두 prop 으로 붙인다.
- 가드: `test_dec210_book_sales_show_all.py`.

### DEC-211 — 화면 공간 효율: 상단 띠 최소화·화면 설명 제거·표 밀도 (2026-08-26 09:34)

- **요청**: 도서별 판매 상단 레이아웃 공간 활용 최적화 + 화면별 설명 텍스트를 전체 화면에서 일단 제거 +
  높이를 최소화해 하단 목록이 더 많이 보이게.
- **공통 조치**: PageHeader 부제(화면 설명)를 띠에 그리지 않음(제목 툴팁으로만 유지 — 페이지 prop 은 그대로),
  띠 py-2.5→1.5·제목 22→20px·필터 세로 가운데; 페이지 루트 `gap-6 pb-8` → `gap-3 pb-4`(85파일);
  SectionHeader pb-2→1·18→16px; 표 셀 py-3→py-2(DataGrid·list-table-card·원장 2화면), DataGrid 툴바 간격
  space-y-3→2, 빈 행 py-6→4.
- 가드: 기존 표 스타일 가드의 py 값 갱신(test_dec203/151/cash_slip).

### DEC-212 — 원장 2화면 DataGrid 전환 + 표 기능 기준선 가드 (2026-08-26 09:48)

- **보고**: "디자인이 변경되면서 각 목록표의 필드 추가삭제·정렬·좌우이동 기능이 누락됐다" (도서별수불원장
  스크린샷). **규칙(사용자)**: 디자인 변경으로 기존 기능이 누락·제거되지 않았는지 이후 꼭 확인 과정을 거친다.
- **조사**: 디자인 커밋(1d5d151~)에서 DataGrid 화면들의 컬럼 설정/정렬/이동/리사이즈 지표가 줄어든 파일은
  0. 도서별수불원장·거래처원장은 DEC-164(2026-08-14) 재작성 때부터 **수동 `<table>`** 이라 그 기능이 원래
  없던 화면 — 이번에 눈에 띈 것.
- **조치**: 두 화면의 상·하단 4개 표를 공용 DataGrid 로 전환(컬럼 설정 `GridColumnSettings`, 정렬
  `useClientSort`, 리사이즈·드래그 이동 `useGridPrefs`, 키보드 행 이동·Enter 상세, 합계 푸터). 전일재고/
  전일미수 행은 정렬과 충돌하지 않게 표 위 스트립(`toolbarTop`)으로. 엑셀/출력 컬럼 = 표시 컬럼 순서.
- **재발 방지**: `tools/grid_feature_baseline.py` — 화면별 표 기능 지표(DataGrid·컬럼설정·정렬·이동·리사이즈·
  키보드·페이저)를 `analysis/audit/grid-feature-baseline.json` 에 기록, `--check` 가 어느 화면이든 지표가
  줄면 실패(테스트 `test_grid_feature_baseline.py` 로 CI 게이트). 의도한 변경은 기준선 재생성으로 승인.

### DEC-213 — 남은 필터 카드 11개 화면 띠 병합 + 「내용 전체 보기」 헤더·합계 고정 (2026-08-26 09:50)

- **요청**: 입고처관리처럼 상단 띠(제목+액션) 아래에 조회 필터 카드가 따로 남은 화면을 다른 화면처럼 통합.
  + 도서별 판매 「내용 전체 보기」 상태에서 스크롤 시 헤더·합계행 고정.
- **병합**: DEC-200 스크립트가 제목 블록 뒤 액션 행/표현식 때문에 놓친 11개(입고 접수·저자·도서·할인·기타거래처·
  입고처·출고 접수·입금전표·세금계산서·청구·거래명세서)를 스캐너 재사용으로 병합(컨테이너 onKeyDown·
  data-legacy-id 는 contents 래퍼 보존, grid 변형은 `flex flex-wrap items-end gap-3`). 등록 폼·관리자
  설정 패널(rbac/settings/super/menu-policy/platform-portal/courier)은 필터가 아니라 제외.
- **고정**: DataGrid `unbounded` 모드에서 카드의 overflow 를 전부 빼 스크롤 컨테이너가 되지 않게 함 → th
  `sticky top-0`·tfoot `sticky bottom-0` 이 페이지 스크롤(임베드 래퍼)에 붙어 헤더·합계가 고정된다.
- 가드: `test_dec200_page_header_band.py::RemainingFilterCardsMerged`, 표 기능 기준선 `--check` 통과.

### DEC-214 — 공용 현황 화면 상단 3블록 → 한 헤드 블록 + 뷰 탭 최하단 (2026-08-26 10:14)

- **요청**(신간발행 스크린샷): 제목 띠 / 상세·요약·목록 탭 / 필터 카드로 나뉜 3블록을 하나의 헤드 블록으로
  통합, 화면 상태 전환(상세/목록/요약)은 가장 하단으로, 검색 필터는 화면명 우측·하단에(다른 목업 참조).
- **조치**: `transaction-status-screen.tsx`(출고·입고·신간발행·반품·폐기·거래 현황 공유) — 검색 패널을
  PageHeader children 으로(contents 래퍼가 `data-enter-scope`/`onKeyDown`/legacy id 보존, 카드 프레임 제거),
  뷰 전환은 화면 최하단 `sticky bottom-0` 바(라임 활성 알약, role=tablist). 루트 `min-h-full` + `mt-auto` 로
  내용이 짧아도 바닥에 붙는다.
- 가드: `test_dec200_page_header_band.py::StatusScreenHeadBlock`.

### DEC-215 — 특별관리(Sobo16) 목업 결 레이아웃 (2026-08-26 10:27)

- **요청**: 특별관리 화면을 제공된 목업 디자인과 결이 맞게 재구성.
- **조치**: 제목 띠를 전폭으로(종전엔 justify-between 행 안에 갇혀 제목만큼만 흰 상자) + 관리자 출판사 필터를
  띠 안에; 거래처/도서 두 축 패널의 카드 프레임·설명 문단 제거 → `SectionHeader`(제목 + 선택 이름·비율 방식
  메타 + 검색·조회·컬럼 액션) + 프레임 없는 DataGrid(fillHeight); 두 축은 `SplitListPanes`(구분선 드래그);
  선택 행 편집 블록은 민트 톤 행으로. 등록·수정·삭제·자동완성·Enter 흐름·legacy id 는 그대로.
- 가드: `test_dec200_page_header_band.py::SpecialScreenLayout`, 표 기능 기준선 `--check`.

### DEC-216 — 띠 래퍼 행 해제(20화면) + 등록 폼 헤더 입력 띠 병합 (2026-08-26 10:30)

- **보고**(신규 입고 접수·신규 출고 주문 스크린샷): 띠가 제목만큼만 흰 상자로 보이고 헤더 입력(거래일자·거래처·
  지사)이 별도 카드.
- **원인**: DEC-200 이관이 제목 블록만 `<PageHeader>` 로 바꾸고, 원래 액션 버튼을 오른쪽에 두던 바깥
  `flex … justify-between` 행을 남겨 띠가 그 행 안에서 shrink-wrap 됐다(자식이 PageHeader 하나뿐).
- **조치**: 자식이 PageHeader 뿐인 래퍼 행 20개 해제(스캐너 재사용, 다른 자식이 있으면 건너뜀 — 0건).
  등록 폼 3화면(신규 입고 접수·신규 출고 주문·거래 명세서 신규)의 헤더 입력 카드(`Panel_header`,
  `data-enter-scope`)를 띠 children 으로(contents 래퍼로 Enter 스코프·legacy id 보존).
- 가드: `test_dec200_page_header_band.py::NoTrappedBand`.

### DEC-217 — 제목 띠 전수 점검: 남은 3화면 (2026-08-26 10:40)

- **요청**: "모든 화면 제목 영역 디자인 목업에 맞게 — 수정 안 된 화면만".
- **전수 조사**: (app) 120개 page.tsx 중 띠 100 / PortalScreenTitle 2 / 없음 18. 없음 18 = 리다이렉트·래퍼
  (공용 현황·대시보드 컴포넌트가 띠를 가짐)·워크스페이스 15 + 실제 내용 화면 3.
- **조치**: 일별 반품내역서(검색 패널을 띠 children 으로, 조회 검정 버튼), 내 정보(띠 추가), 청구서 인쇄 화면
  (뒤로가기·메모 편집·새로고침·인쇄를 띠 leading/actions 로, `print:hidden`).
- 가드: `test_dec200_page_header_band.py::EveryContentScreenHasBand` — 래퍼 예외 목록 밖의 화면에 띠가 없으면
  실패(새 화면 추가 시 자동 점검).

### DEC-218 — 목록표 가로 스크롤 힌트(가려진 컬럼 표시) (2026-08-26 23:26)

- **요청**: "모든 화면에 대해서 목록표의 필드 항목이 많아서 좌우 스크롤이 생겼을 때 좌우로 감춰진 필드가
  존재한다는 것을 간단한 애니메이션으로 사용자에게 표시".
- **구현**: `components/shared/h-scroll-hint.tsx` — `useHorizontalOverflowHint(ref)` 가 스크롤 컨테이너의
  scroll/ResizeObserver/MutationObserver 로 `{left,right}` 를 계산, `<HScrollEdgeHints>` 가 가려진 쪽 가장자리에
  카드색 그라데이션 + 흔들리는 화살표 배지(`.hscroll-hint-badge`, 1.2s nudge, 감속 선호 시 정지)를 띄운다.
  배지 클릭 = 그쪽으로 폭의 2/3 스크롤. 끝에 닿으면 그쪽 힌트는 사라진다.
- **적용 범위**: 공용 `DataGrid` 스크롤 카드(전 화면) + 수동 `<table>` 래퍼 10곳을 `<HScrollBox>` 로 교체
  (통합 거래처원장 2, 감사 로그, 가입 신청, 계정 관리 2, 거래 현황, 입고 접수 신규/상세, 반품 접수 상세,
  일별 반품내역서 상세, 현황 공용 메모 표). `unbounded`(내용 전체 보기) 모드는 페이지가 스크롤하므로 제외.
- 가드: `test/test_dec218_hscroll_hint.py`.

### DEC-219 — 거래 현황 공용 화면: 우측 라인·집계 표도 DataGrid, 컬럼 설정 전 축 공통 (2026-08-27 00:05)

- **지적**: "입고현황 양쪽 목록표 필드 정렬, 이동, 보이기옵션 처리 등이 누락된 부분이 존재한다."
- **원인**: ① 좌측 전표 표의 `GridColumnSettings` 가 `{isOutbound && …}` 블록 안에 있어 입고·신간 축에서 숨겨짐.
  ② 우측 「선택 전표 라인」(`Sobo24.DBGrid102`)과 목록 뷰 「거래처 집계」(`Sobo24.DBGrid202`)는 수동 `<table>`.
- **조치**: 컬럼 설정을 축 공통 슬롯으로 이동; 두 표를 `DataGrid` + `useGridPrefs`(`transactions.outbound-status.detail-lines` / `.rollup`)
  + `useClientSort` 로 전환(정렬·컬럼 이동/폭/표시·키보드·합계 행 유지, ISBN 컬럼 유지). 가로 스크롤 힌트는 DataGrid 가 제공.
- 가드: `test/test_dec219_status_screen_grids.py`, 표 기능 기준선 재생성.

### DEC-220 — 입고명세서 하단 라인 표 DataGrid + 「내용 전체 보기」 (2026-08-27 00:14)

- **지적**: "입고 명세서 화면의 하단 테이블이 디자인 반영이 안 되었고, 상단 테이블 전체보기 기능의 전체 내용 보기
  체크박스 기능을 추가해야 한다."
- **조치**: 하단 「선택 전표 라인」 수동 `<table>` → `DataGrid<ReceiptLineDetail>`(정렬·컬럼 이동/폭/표시·키보드·
  합계 행, prefs `transactions.inbound-statement.lines`, 레거시 DBGrid101 FieldName 은 컬럼 `legacyId` 유지, ISBN 유지).
  상단 표 툴바에 「내용 전체 보기」(`Sobo22.ShowAll`) — DEC-210 도서별 판매 동형(`unbounded`, 분할 해제).
- 가드: `test/test_dec220_inbound_statement_lines_grid.py`, 표 기능 기준선 재생성.

### DEC-221 — 폐기·반품 접수 신규 입력: 헤더 입력 카드를 제목 띠로 병합 (2026-08-27 00:28)

- **지적**: "화면 명칭과 검색 필터 등 구성이 목업 디자인과 달리 나눠져 있다" (폐기 접수 신규 입력 스크린샷).
- **조치**: DEC-216(신규 입고 접수 등) 과 같은 방식 — 띠 아래 `SurfacePanel` 헤더 카드(폐기일/출판사코드/출판사/거래처/비고,
  반품일/출판사코드/지사/비고)를 `PageHeader` children(`Panel201` contents 래퍼, `data-enter-scope`)으로 이동.
  라벨 회색·h-8 압축 클래스는 띠 공통 규칙에 맡겨 제거. 같은 유형인 반품 접수 신규 입력도 함께.
- 가드: `test/test_dec221_returns_forms_band.py`.

### DEC-222 — 반품 재고 처리(재생/해체/변경): 제목 띠 공통 디자인 정합 (2026-08-27 00:48)

- **지적**: 메뉴 반품재고(재생)/(해체)/(변경) 화면의 "상단 화면 명칭 부분의 공통 디자인이 반영되지 않았다".
- **원인**: 띠는 있었으나 라벨이 회색 소형(`text-xs text-gray-600`)이고, 재생/해체/변경 **탭 스트립이 띠 아래 별도 블록**.
- **조치**: 라벨 공통화, 탭 스트립 제거 → 띠 안 「처리 구분」 radiogroup(방향키 전환, `Sobo24.TabStrip`/`Sobo24.Tab.*`),
  `?tab=` 딥링크·`Tabs` 콘텐츠 전환 로직(`selectTab`)은 그대로.

### DEC-223 — 일별 반품내역서: 조회 오류 안내·상세 스코프·전표번호 (2026-08-27 00:49)

- **지적**: "검색 오류 발생 원인 확인 … 전표 번호가 이상하다" (배너 `오류: 0`, 전표번호 `21`).
- **원인**: ① `오류: 0` = `ApiError.status 0` = 클라이언트 타임아웃(30s)/네트워크 실패를 상태코드처럼 표기한 것.
  로컬 계측은 6개월 범위도 0.2~1.6s 라 DB 지연은 아님 — 운영(Render 재배포·터널) 순간 단절 또는 대용량 응답
  (6개월 상세 4,444행: 상세가 **선택 일자와 무관하게 기간 전체**를 내려보냄) 이 유력. ② 상세 SQL 이 `s.Jubun AS idnum`
  — 전표번호 정본은 Idnum(DEC-099/108), Jubun 은 거래처별 차수. ③ 할인율이 `grat1*100`(저장값이 이미 % 단위 → 8500%).
- **조치**: 상세 스코프에 `detailForGdate`(선택 마스터 행 일자) 추가 — 레거시 DBGrid201(커서 행 라인) 동형·응답 축소;
  `s.Idnum AS idnum`(DDL 드리프트 시 0, `s1_column_names`), 5자리 표기(`formatIdnumDisplay`); 할인율 `85%`;
  조회 실패는 `ApiErrorBanner`(TIMEOUT/NETWORK/HTTP 구분 + 재시도)로, 이 보고서 요청 타임아웃 60s;
  상세 표를 DataGrid(정렬·컬럼 설정·이동)로 전환.
- 가드: `test/test_dec222_223_returns_reports_and_inventory.py`; DEC-093 상세 스코프 테스트는 Idnum 마커로 갱신.

### DEC-224 — 가로 스크롤 힌트 배지를 뷰포트 가시 구간에 고정 (2026-08-27 01:01)

- **지적**: 일별 반품내역서 우측 라인 표에 "좌우 숨겨진 내용 표시용 애니메이션 기능 누락".
- **원인**: 배지는 카드 **전체 높이**의 세로 중앙(`inset-y-0` + `items-center`)에 놓였는데, 이 표는 높이 상한 없이
  페이지 스크롤로 길어지는 패널이라 중앙이 화면 아래(폴드 밖)에 있어 보이지 않았다(좌측 짧은 표는 보임).
- **조치**: `useVisibleBand` — 카드 `getBoundingClientRect` × 뷰포트 교집합을 조상 스크롤(캡처)·리사이즈·RO 로 추적해
  오버레이 `top/height` 를 가시 구간으로 두고 그 중앙에 배지. 측정 전엔 종전(inset-y-0) 폴백.
- 검증: 로컬 하네스(카드 2,300px, 뷰포트 949px) 에서 배지 y=575 가시 구간 중앙 확인. 가드 `test_dec218_hscroll_hint.py` 보강.

### DEC-225 — 기간별 재고원장·기간별 반품내역서 띠 정합 + 「반품재고관리(통합)」 메뉴 제거 (2026-08-27 03:20)

- **지적**: 반품 메뉴 하단 화면들의 "화면 명칭 영역이 목업 디자인에 따르지 않았다. 수정하고, 마지막 메뉴는 제거".
- **띠**: 두 화면 모두 띠 안 필터 묶음이 `flex flex-wrap items-end` 블록 래퍼라 제목 옆 인라인 정렬이 깨졌다 →
  `className="contents"` 래퍼(다른 화면과 동일), 조회 버튼 래퍼 제거.
- **메뉴 제거**: `MenuShippingReturnsInventory`(ACC-MENU-NAV-12, `/shipping/returns-inventory`) 는 정본 `/returns/inventory`
  로 안내만 하던 허브 MVP 스텁 → form-registry 항목·페이지 삭제, RBAC 단일 원천 `docs/onboarding-rbac-menu-matrix.md`
  행 삭제 후 `extract_rbac_matrix.py` 재생성(yaml/json), 폼 매트릭스·list-state 리포트 재생성.
  `welove_screen_contract_coverage.json` 은 재생성 시 무관한 드리프트(매핑 노트 40→55, 미커버 1)가 섞여 HEAD 유지.
- 가드: `test/test_dec225_returns_reports_band_and_menu.py`. `check_menu_rbac_consistency.py` 의 HIDDEN-* 6건 FAIL 은 기존 상태.

### DEC-226 — 띠 화면 루트 패딩 제거(13화면): 제목 띠가 화면 가장자리까지 (2026-08-27 03:45)

- **지적**: 기간별 재고원장 "이 부분에 왜 여백이 들어가지? 다른 부분(화면)과 다르다".
- **원인**: 페이지 루트가 `p-4`/`p-6` — 띠(`-mx-[5px]`)가 루트 패딩 안쪽에 갇혀 양옆·위에 회색 여백. 정본 루트는
  `flex w-full min-w-0 flex-col gap-3 pb-4`(좌우·상단 패딩 없음).
- **조치**: 띠가 있는 화면 전수 스캔 → 루트 좌우/상단 패딩 제거·`w-full min-w-0`·`pb-4` 통일 13화면
  (반품 3, 반품 접수 2, 반품 재고 처리, 정산 3, 관리자 4).
- 가드: `test_dec200_page_header_band.py::NoPaddedRootAroundBand`.

### DEC-227 — 거래처 화면 제목 「거래처(마스터)」 → 「거래처현황」 (2026-08-27 04:00, 사용자 지시)

- `/master/customer` 띠 제목만 변경. 메뉴 캡션(form-registry)·라우트·legacy-id 는 그대로.

### DEC-228 — 거래처·입고처·기타거래처 상세/신규: 등록·저장·삭제를 제목 띠 actions 로 (2026-08-27 21:51)

- **지적**: "거래처 관리 저장, 삭제 버튼이 하단에 존재해서 사용자에게 잘 눈에 띄지 않는다 … 거래처 상세·입고처 상세 공통으로
  목업 디자인에 부합되도록".
- **조치**: 세 폼(`customer/inbound-vendor/etc-customer-detail-form.tsx`)의 하단 버튼 바 제거, 같은 파일에서
  `XxxFormActions`(등록/저장/삭제, 레거시 id Sobo11/12/15.Button101~103 유지, WriteGate 권한 게이트 유지) 를 export 해
  6개 페이지의 `PageHeader actions`(우측 상단) 에서 렌더 — 신규 입고 접수 등 다른 등록 화면의 「저장」 위치와 동일.
  저장/등록=기본(검정) 버튼+아이콘, 삭제=outline-destructive. 폼 Props 에서 onCreate/onSave/onDelete/caps/busy 제거.
- 가드: `test/test_dec228_master_form_actions_in_band.py`.

### DEC-229 — 제목 옆 메뉴 계층 경로(브레드크럼) 전 화면 자동 표시 (2026-08-27 22:14)

- **요청**: "모든 화면 선택 시 해당 화면의 메뉴 계층 구조를 (참고 이미지) 상단처럼 표시. 텍스트 크기는 화면 명칭의 60% 정도".
- **구현**: `lib/menu-trail.ts::resolveMenuTrail(pathname, search)` — form-registry 단일 원천으로
  「대메뉴(MENU_GROUPS 라벨) › 사이드바 서브그룹(SIDEBAR_LAYOUTS group 라벨) › 메뉴 항목(caption) › 상세/신규/인쇄」.
  레지스트리 경로의 세그먼트 접두 일치(가장 깊은 것, `?tab=` 변형은 검색문자열로 구분). 메뉴 항목 조각은 링크.
  `PageHeader` 가 제목 h1 옆에 `MenuTrail`(text-xs ≈ 12px = 20px×60%)로 자동 렌더 — `trail={false}` 로 숨김, 배열로 지정.
- 가드: `test/test_dec229_menu_trail.py`.

### DEC-230 — 거래처 상세 재배치(기본정보/청구정보) + 확장 필드 사이드 테이블 + 우편번호 검색 (2026-08-27 22:30)

- **요청**: 기본정보 4행(거래처구분/지역/코드/거래정지/사유 · 거래처명/대표자/사업자등록번호/업태/종목/한도 · 주소1+연락처 ·
  주소2+연락처), 주소는 우편번호/주소/상세주소 분리 + 우편번호 검색, 청구정보(비율 → 계산서 → 담당관리자1·2 → 메모).
- **저장 컬럼 없는 항목** → `G1_Ggeo_Ext` 사이드 테이블(DEC-068 전자책 선례, `customer_ext_service.py`): 우편번호2·상세주소1/2·
  유선전화2·팩스2·휴대전화2·이메일2·거래정지 사유·담당관리자1 연락처·메모. 상세 GET 에 병합, PATCH/POST 에서 분리 upsert,
  DELETE 시 정리. 스코프 hcode 로 격리. 테이블 생성 실패 시 확장 필드 없이 계속(graceful).
- **매핑 결정**: 유선전화/팩스(주소1 행)=레거시 지역번호+번호 두 칸(Gtel1/2·Gfax1/2) 유지; 휴대전화=Gphon(DEC-149); 한도=Gssum(2행,
  비율 행에는 중복 표기 안 함); 거래정지=Grat9 유/무 선택; 계산서=Pubun(출고즉시/월말/입금액/현영/기타 입력, 기존 자유 텍스트
  호환); 담당관리자2 연락처=Gnum1(레거시 Edit130 추가번호 — 담당자2 옆 칸); 거래처코드2(Ocode)·Gjuso 는 UI 에서 제외(값 보존).
- **우편번호 검색**: `components/shared/postcode-search.tsx` — 카카오 우편번호 서비스(키 불필요) 스크립트 지연 로드, 화면 내 모달
  embed(iframe 팝업 차단 회피), 선택 시 우편번호·도로명주소 채우고 상세주소로 포커스.
- 가드: `test/test_dec230_customer_detail_layout.py`.

### DEC-231 — 구분·지점 관리 패널 7종: 등록/저장/삭제/신규 입력을 카드 우측 상단으로 (2026-08-27 23:02)

- **지적**: "거래처 구분 관리 부분에도 등록·저장·삭제 버튼이 눈에 띄지 않는다. 카드 오른쪽 상단으로 이동하고 잘 보이도록,
  유사한 인터페이스에 모두 동일하게".
- **조치**: 편집 카드 하단 버튼 행 → 카드 첫 줄 헤더(좌 「신규 등록/선택 항목 수정」 제목, 우 버튼, 아래 구분선). 활성 버튼은
  검정(저장의 secondary 제거), 삭제는 outline-destructive(DEC-228 동형). 적용: 거래처구분·입고처구분·기타거래처구분·저자구분·
  도서분류·거래처 지점·단순 마스터 공용 페이지. 레거시 id(Sobo1x.Button201~205)·WriteGate 유지.
- 가드: `test/test_dec231_master_panel_actions_top.py`.

### DEC-232 — 목록표 틀고정(엑셀 동형): 지정 컬럼까지 왼쪽 고정, 오른쪽만 가로 스크롤 (2026-08-28 00:10)

- **요청**: "거래처관리 목록표에서 특정 필드를 하나 지정하면 해당 필드 오른쪽의 표만 좌우 이동되도록(엑셀 틀고정 유사)".
- **구현**: 공용 DataGrid `frozenUntil`(컬럼 id) — 표시 컬럼 중 그 컬럼까지 th/td/tfoot 셀에 `position: sticky; left: 누적폭`
  (헤더 셀 실폭을 rAF+ResizeObserver 로 측정, 리사이즈·컬럼 변경 추종). 헤더는 top+left 이중 sticky(z-20), 본문 셀은 `bg-inherit`
  로 행 배경(기본 bg-card·선택 mint·hover accent 불투명) 승계, 마지막 고정 컬럼 우측 구분선.
  설정 UI: 「컬럼」 팝오버의 「틀고정」 셀렉트(표시 컬럼 중 선택, 고정 안 함). 저장: `useGridPrefs.frozenUntil`(hcode 계정 종속 서버 prefs).
  전 화면 배선(DataGrid 50·컬럼 설정 51) — 표 기능 공통 규칙.
- 가드: `test/test_dec232_grid_freeze.py` (배선 누락 화면이 생기면 실패), 표 기능 기준선에 `freeze` 지표 추가.

### DEC-233 — 띠 안 팝오버는 인라인 라벨 규칙 제외 (컬럼 설정 체크 목록 세로 복원) (2026-08-28 18:03)

- **지적**: 「컬럼」 팝오버의 컬럼 체크 목록이 가로로 흘러 좌우 스크롤이 생김 — "원래대로 세로 스크롤로".
- **원인**: DEC-200 띠 CSS `.page-header div:has(> label:first-child){display:flex;row}` 가 띠 actions 안에서 열리는 팝오버의
  체크 목록 컨테이너(첫 자식이 label)에도 적용.
- **조치**: 팝오버 루트에 `data-band-exempt` + 규칙에 `:not(:is([data-band-exempt],[role="dialog"]) *)` — 띠 안 팝오버/다이얼로그는
  원래 레이아웃 유지. 검증: 로컬 3001 실화면(거래처관리)에서 목록 세로 정렬·자체 스크롤 복원. `.next` 캐시로 CSS 미반영 → 재기동.
- 가드: `test_dec200_page_header_band.py::BandPopoversExempt`.

### DEC-234 — 전화/팩스 한 칸 통합 + 거래처 엑셀 헤더=화면 라벨 + 신규 거래처 CTA (2026-08-28 18:08)

- **요청**: "전화번호·팩스번호가 지역번호 필드로 나눠져 있는데 하나로 통합, 엑셀 저장에도 반영. 거래처현황 엑셀 헤더가 화면
  필드명 그대로인지 확인. 신규 거래처 버튼이 눈에 띄도록".
- **통합**: 저장 구조(레거시 Gtel1/Gtel2·Gfax1/Gfax2 = 지역번호/번호)는 유지, 화면은 `PhoneField` 한 칸(「02-737-6111」) —
  입력값을 지역번호 정규식(`02|0[3-9]\d|01\d|050\d|030\d`)으로 분리 저장(`lib/phone-format.ts` ↔ `masters_excel.split_phone`
  동일 규칙). 거래처·입고처·기타거래처·저자 4개 폼, PairField 폐기.
- **엑셀**: 카탈로그 전화번호1/2·팩스번호1/2 → 「전화번호」「팩스번호」 합본(`Derived` accessor, 가상 키 gtel/gfax); 업로드(역반영)는
  `expand_phone_fields` 로 두 컬럼 분리, 예전 파일의 분리 헤더·구 라벨은 별칭으로 계속 수용. 헤더를 거래처현황 그리드 라벨과
  통일(사업자번호→사업자등록번호, X공급율→위탁/현매/…, 사업자주소 합본 추가). 미포함: 한도(Grat7) — 전체 목록 API 미제공.
- **CTA**: 신규 거래처 = `brand-primary`(Vivid Lime 채움, semibold) — 화면당 1개 라임 규칙(조회는 검정) 유지.
- 검증: 로컬 3001 실화면(거래처 상세 유선전화 「02-737-6111」·팩스 합본 표시, CTA 라임 32px), 스위트 통과. 가드 `test_dec234_phone_merge.py`.

### DEC-235 — 북이오웍스 계정 전환: 이메일 계정 = 기존 Id_Logn 행 오버레이, 웹 로그인은 이메일 전용, 델파이는 그대로 (2026-09-03)

- **요청**: "북이오웍스 로그인은 이메일 아이디/비번. 하단 [위러브솔루션→북이오웍스 계정 전환하기] → 전환 페이지에서
  기존 [출판사/아이디/비번] + 이메일 입력 → 메일 인증코드 확인 → 코드 입력 + 비밀번호 설정(평문 저장, 추후 북이오 계정 재사용)
  → 로그인 페이지로." 보강 2건: "기존 계정·방식은 레거시 델파이에서 병행 사용", "웹에서는 신규 포팅된 계정으로만 로그인,
  델파이는 그대로". 메일 = Brevo SMTP 무료 티어(smtp-relay.brevo.com:587), 발신자 admin@bukio.works.
- **결정** (설계 정본 `docs/decision-bukioworks-account-migration.md`, 추적 `ACM-*`):
  1. **오버레이(ACM-DEC-00, INV-1~7)**: 전환은 계정 이전이 아니라 이메일 자격을 기존 `Id_Logn` 행에 연결하는 것. 전환·이메일
     로그인·재설정·링크 경로는 `Id_Logn` 을 INSERT/UPDATE/DELETE 하지 않는다(정적 가드). 두 비밀번호(델파이 Gpass/웹) 독립.
     매 로그인 `Id_Logn` 행 존재 확인 + 권한 재도출; 행 부재·`_이름_` 잠금·Gcode 변경은 fail-closed `ACCT_LINK_STALE` → 재연결.
  2. **저장소(ACM-DEC-01)**: remote_138 전용 DB `bukio_web_db` 의 `Web_Accounts`/`Web_Account_Links`/`Web_Account_Codes`
     (MySQL 3.23 호환 DDL, 명시 한정). JSON 파일 금지(Render 비영속).
  3. **로그인 코어 추출(ACM-DEC-02)**: `auth_login_core.resolve_and_authenticate` 를 `/auth/login` 과
     `/public/account-switch/verify-legacy` 가 공유. 라우터는 HTTP·감사만. 로그인 회귀 70건 무변경 PASS.
  4. **티켓·코드(ACM-DEC-03/04)**: 전환 티켓 = 서명 JWT(type=switch, 15분, jti). 코드 6자리·10분·5회·재발송 60초·
     이메일 시간당 5·IP 20, salted SHA-256 저장, 코드는 티켓 jti 에 바인딩.
  5. **비밀번호(ACM-DEC-05)**: 요구대로 `PwPlain` 보관 + `PwHash`(bcrypt) 병행, 검증은 해시만. `BLS_ACCOUNT_PW_STORE=aesgcm`
     이면 AES-GCM 봉투(권장 대안, 코덱 1곳 차이).
  6. **웹 로그인 = 이메일 전용(ACM-DEC-06/07)**: `userId` 에 `@` → 이메일 경로(동일 JWT 클레임 + `acct`/`lvia`). 레거시 ID 는
     `BLS_LEGACY_ID_LOGIN`(코드 기본 on = 선공개 기간, 컷오버 커밋에서 off) 이 off 면 403 `ACCT_SWITCH_REQUIRED`.
     `GET /auth/login-policy` 가 프론트 UI(콤보·전환 버튼)를 결정.
  7. **링크 규칙(ACM-DEC-08)**: 이메일 1=계정 1, identity `(ServerId, DbName, Hcode, Gcode)` 는 계정 최대 1(PK), 한 계정에
     여러 회사 링크 허용(로그인 시 DEC-096 선택 카드 재사용), `link`/`relink` 모드.
  8. **메일(ACM-DEC-09)**: `email_dispatch_service` console/smtp(Brevo, certifi TLS), 템플릿 인증코드 + 델파이 안내 문구 고정,
     `debug/send_test_email.py --check|--to`. 활성화 안내도 같은 서비스(연결은 후속).
  9. **재설정(ACM-DEC-10)**: `/account/reset` 동일 코드 인프라, 컷오버 전 필수 → 구현 완료.
  10. **보류**: ACM-DEC-11(가입 활성화 토큰 → 전환 티켓 교환)은 C10 Id_Logn 실 DB 생성(인메모리 상태) 이후로 이연.
- **구현(2026-09-03)**: backend `web_accounts_db` · `account_secret_codec` · `auth_login_core` · `account_switch_service` ·
  `email_dispatch_service` · `email_templates/account_code` · `routers/public_account_switch` · `auth.py`(이메일 경로·정책) ·
  `auth_service.load_user_by_identity`; frontend `/account/switch`(SwitchWizard) · `/account/reset` · 로그인 페이지 개편 ·
  `lib/account-switch-api` · `lib/login-org-select`(DEC-096 공용화) · middleware PUBLIC_PATHS.
- **가드**: `test_acm_switch_flow.py`(23) · `test_acm_delphi_coexistence.py`(6) · `test_acm_store_and_codec.py`(6) ·
  `test_acm_email_dispatch.py`(11) + 기존 로그인 회귀 70건. 복원 포인트 태그 `restore-pre-email-account-2026-09-03`.
- **롤아웃**: Phase 0 준비(완료: 복원 포인트·Brevo·DB 기준선) → Phase 1 선공개(전환 페이지·재설정, 로그인은 기존 방식 병행,
  `switchAvailable` 은 Render 메일 env 등록 시 자동 노출) → Phase 2 컷오버(`BLS_LEGACY_ID_LOGIN=off` + 코드 기본값 변경)
  → Phase 3 북이오 통합(PwPlain 이관 후 폐기). 델파이는 전 단계 무변경.
- **잔여 결정**: ACM-Q-1(평문 vs AES-GCM), Q-5(다중 링크 허용 — 구현은 허용), Q-7(저장소 서버), 선공개 기간.
- **결정자**: 사용자(요구·병행·이메일 전용·Brevo·발신자) + 메인개발자(설계·구현)
- **보강(2026-09-03 저녁, 사용자 요청)**: ① `/account/reset` 미등록 이메일은 404 `ACCT_EMAIL_NOT_REGISTERED` 즉시 안내(열거 방지 예외 — B2B 폐쇄 환경). ② 「기 등록 계정 찾기」(`/activate/lookup`)를 **내 계정 찾기**로 개편 — `POST /public/account-switch/lookup`: 로그인과 같은 자격 검증만으로 전환된 이메일 계정(이메일·연결일·마지막 로그인)을 보여주고, 없으면 전환 티켓을 줘 바로 전환 2단계로 잇는다. ③ 전환·재설정·계정 찾기 히어로 로고 = 사용자 제공 워드마크 WebP(`Logo` 단일 진입점). ④ **회사 미선택 스윕 지연 가드** — 운영 실측 89초(후보 39개)로 프론트 30초 타임아웃을 넘기던 문제: `BLS_LOGIN_SWEEP_BUDGET_SEC`(기본 20초, 추측 후보 한정) 예산 + 409 `ACCT_ORG_HINT_REQUIRED` 안내, 계정 계열 프론트 타임아웃 150초.
