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

---
*최종 업데이트: 2026-07-09 — DEC-095 신규 (비-기본 DB 테넌트 0건 — 테넌트 DB 요청
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
