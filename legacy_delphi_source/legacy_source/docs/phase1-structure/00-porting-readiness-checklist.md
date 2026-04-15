# 1단계 포팅 준비도 체크리스트

웹 포팅(2단계) 착수 전, **이 저장소의 1단계 산출물**로 무엇까지 알 수 있는지와 **남는 불확실성**을 정리합니다.  
판정: **충족** / **부분** / **미충족**.

| 정보 영역 | 판정 | 근거 산출물 | Gap (미충족·부분 시) |
|-----------|------|-------------|----------------------|
| 제품·코드 범위 (어떤 실행 파일·DPR이 분석 대상인가) | 충족 | [01-build-closure.md](01-build-closure.md), [02-variant-chulpan-catalog.md](02-variant-chulpan-catalog.md) | 저장소 내 `book_*` 등 **다른 변형**은 별도 DPR·클로저로 동일 깊이 분석되지 않을 수 있음. |
| **MVP DB 스키마 범위** | 부분 | [14-db-code-vs-live.md](14-db-code-vs-live.md), [13-db-surface.md](13-db-surface.md) | 라이브 교차는 **`chul_09_db` 스냅샷** 기준. 동일 서버의 `book_*_db` 등은 별도 export 시 확장. |
| 화면·메뉴·업무 흐름 | 충족 | [11-screen-business-flows.md](11-screen-business-flows.md), [12-screen-specification.md](12-screen-specification.md), [wireframes/](wireframes/) | 바이너리 DFM은 와이어프레임이 placeholder 수준([wireframes/README.md](wireframes/README.md)). |
| DB 테이블·SQL 사용(정적) | 충족 | [13-db-surface.md](13-db-surface.md), [13-db-sql-references.csv](13-db-sql-references.csv) | **동적 문자열 SQL**·다른 서비스 접근은 스캔에 안 잡힐 수 있음. |
| 코드 ↔ 라이브 테이블 일치 | 충족 | [14-db-code-vs-live.md](14-db-code-vs-live.md), [15-db-porting-and-optimization.md](15-db-porting-and-optimization.md) | **Code only** 3테이블·**Live only** 테이블은 추가 검증 필요(본 문서 Gap 절). |
| 외부 설정·FTP·Registry | 충족 | [09-settings-external.md](09-settings-external.md) | 웹 배포 시 **Secrets·환경 분리** 방식은 2단계 설계 과제. |
| 리포트·인쇄 | 부분 | [10-report-deps.md](10-report-deps.md) | FastReport/Word 연동을 웹에서 무엇으로 대체할지 **의사결정 필요**. |
| 소켓·미들웨어(`RunSQL` 등) 규약 | 부분 | [15-db-porting-and-optimization.md](15-db-porting-and-optimization.md), [16-socket-runsql-surface.md](16-socket-runsql-surface.md) | 메시지 포맷·에러 코드 **상세 스펙**은 얇게 정리됨; 깊은 역설계는 2단계. |
| 핵심 런타임(`Base01`) | 부분 | [08-base01-inventory.md](08-base01-inventory.md) | 대형 유닛; API 경계는 인벤토리 + DB 리포트 패턴 요약 수준. |

## Gap 요약 (우선순위)

1. **다중 스키마**: 포팅 범위가 위러브(`chul_09`)만이면 명시 OK. 타 고객 스키마까지면 `14-*`를 스키마별로 반복 export.  
2. **Code only 테이블** (`S4_Ssub`, `T0_Gbun`, `T8_Gbun`): [15-db-porting-and-optimization.md](15-db-porting-and-optimization.md) §3.1 및 본 저장소 조사 결론 참고.  
3. **Live only 테이블**: 배치·타 앱·미스캔 가능; 삭제/통합 전 운영 검증.  
4. **이해관계자 요약**: [00-phase1-summary-for-stakeholders.md](00-phase1-summary-for-stakeholders.md).

## 관련 문서

- 비전문가용 요약: [00-phase1-summary-for-stakeholders.md](00-phase1-summary-for-stakeholders.md)  
- 산출물 인덱스: [README.md](README.md)
