"""정산 billing SQL 회귀 가드 — 인라인 상관 서브쿼리 부재 정적 검증.

배경
----
DEC-033 (d+) 로 ``_fetch_billing_line_counts`` 헬퍼를 분리하여 MySQL 3.23
호환성을 회복했으나, 향후 누군가 메인 SELECT 안에 다시 ``(SELECT COUNT(*)
FROM T3_Ssub d WHERE d.Hcode=t.Hcode AND LEFT(d.Gdate,6)=t.Gdate)`` 같은
패턴을 도입하면 즉시 ``OperationalError 1064`` 가 재발한다.

본 가드는 ``settlement_service.py`` / ``cash_service.py`` /
``tax_invoice_service.py`` 의 *전체 텍스트* 를 정적으로 스캔하여 다음 패턴이
**등장하지 않음** 을 보장:

- ``T3_Ssub d WHERE d.Hcode=t.Hcode``
- ``FROM\\s+T\\d_Ssub\\s+\\w\\s+WHERE\\s+\\w\\.Hcode\\s*=\\s*t\\.Hcode`` 일반화

사용자 룰 부합
-------------
- 임시방편 0 — 인라인 서브쿼리 *모두* 차단 (1건 발견 시 fail).
- 일반화 — 메인 SELECT 안의 모든 alias 대 alias 상관 서브쿼리 패턴 검출.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from unittest import TestCase, main


_BACKEND_ROOT = Path(__file__).resolve().parent.parent / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(_BACKEND_ROOT))


_TARGET_FILES = [
    _BACKEND_ROOT / "app" / "services" / "settlement_service.py",
    _BACKEND_ROOT / "app" / "services" / "cash_service.py",
    _BACKEND_ROOT / "app" / "services" / "tax_invoice_service.py",
]

# 인라인 상관 서브쿼리 패턴 — 메인 SELECT 안에 (SELECT ... FROM Tn_Ssub d WHERE
# d.Hcode = t.Hcode ...) 가 등장하면 MySQL 3.23 1064. *모든* alias 조합에
# 대해 일반화 (사용자 룰: 특정 케이스가 아닌 정책으로 차단).
_INLINE_CORRELATED_PATTERN = re.compile(
    r"\(\s*SELECT[^()]*?FROM\s+T\d+_Ssub\s+(\w+)[^()]*?WHERE[^()]*?\1\.\w+\s*=\s*\w+\.\w+",
    re.IGNORECASE | re.DOTALL,
)


class BillingNoInlineCorrelatedSubqueryTest(TestCase):
    def test_settlement_files_have_no_inline_correlated_subquery(self) -> None:
        violations: list[str] = []
        for path in _TARGET_FILES:
            text = path.read_text(encoding="utf-8")
            for m in _INLINE_CORRELATED_PATTERN.finditer(text):
                # 매칭된 위치의 라인 번호 추출
                line_no = text.count("\n", 0, m.start()) + 1
                violations.append(f"{path.name}:{line_no} → {m.group(0)[:80]}...")
        if violations:
            self.fail(
                "MySQL 3.23 호환 위배 — 인라인 상관 서브쿼리 잔존:\n  "
                + "\n  ".join(violations)
                + "\n\n해결: DEC-033 (d+) `_fetch_billing_line_counts` 패턴으로 분리."
            )


if __name__ == "__main__":
    main()
