# 소켓·`RunSQL` 데이터 접근 개요 (1단계)

웹/API 포팅 시 **중간 서버로 SQL을 보내는 경로**를 빠르게 파악하기 위한 **얇은 인벤토리**입니다. 와이어 포맷·프로토콜 버전 등 **상세 스펙은 2단계**에서 소스·패킷 캡처로 확정하는 것을 권장합니다.

## 어디에 모여 있는가

- **핵심 구현**: 루트 [`Base01.pas`](../../Base01.pas)의 `TBase10` / `Socket` 사용부.
- **호출 패턴 (코드에서 반복 확인)**:
  - `Base10.Socket.RunSQL(Sqlen)` 또는 `RunSQL(Sqlon+Sqlen)` 직후 `BusyLoop`.
  - 응답 검사: `Base10.Socket.Body_Data = 'ERROR'` 이면 삽입/수정/삭제 등 오류 메시지 표시.
- **이름 기반 조회**: `Seek_Name` 등은 `Base01`에 선언·구현되어 있으며, 화면 단에서는 `Seek_*` 유닛과 함께 쓰입니다 ([`08-base01-inventory.md`](08-base01-inventory.md)).

## 정량 요약

[`15-db-porting-and-optimization.md`](15-db-porting-and-optimization.md) §1에 Chulpan 클로저 전체에 대한 **대략적인 횟수**가 정리되어 있습니다 (`RunSQL`, `Socket.*`, `Seek_Name` 등). 정확한 API 계약은 해당 수치와 별개로 **서버 측 구현**을 봐야 합니다.

## 포팅 시 의사결정 포인트

1. **유지**: 동일 중간 서버를 두고 HTTP/JSON 래핑만 할지.  
2. **대체**: 애플리케이션 서버가 DB에 **직접 연결**하고 `RunSQL` 문자열을 **저장 프로시저/ORM**으로 치환할지.  
3. **트랜잭션**: 현재는 요청 단위로 `RunSQL` + `BusyLoop`; 웹에서는 **명시적 트랜잭션 경계**와 **재시도 정책**이 필요합니다.

## 관련 산출물

- DB·SQL 문자열: [`13-db-surface.md`](13-db-surface.md), [`13-db-sql-references.csv`](13-db-sql-references.csv)  
- 외부 설정(FTP 등): [`09-settings-external.md`](09-settings-external.md)  
- 패턴 집계: [`15-db-porting-and-optimization.md`](15-db-porting-and-optimization.md)
