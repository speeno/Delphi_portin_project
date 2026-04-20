"""C15 cut-over validator 의 실 DB 어댑터 모음 (Phase 2 — T6).

설계 원칙
---------
- 본 패키지는 **시스템/구조 쿼리만** 허용한다. (COUNT(*), SHOW, information_schema,
  sys.columns 등) 비즈니스 SELECT/DML 신규 추가 ❌ — DEC-040/044 정합.
- 식별자(테이블·컬럼명) 는 화이트리스트 정규식으로 검증한 뒤 백틱/대괄호로 quoting.
- 자격 정보는 YAML 프로필 또는 환경변수만 사용 — 코드/커밋 평문 ❌.
"""

from scripts.adapters.base import resolve_profile, sanitize_identifier
from scripts.adapters.mysql import MysqlDataSource
from scripts.adapters.sqlserver import SqlServerDataSource

__all__ = [
    "MysqlDataSource",
    "SqlServerDataSource",
    "resolve_profile",
    "sanitize_identifier",
]
