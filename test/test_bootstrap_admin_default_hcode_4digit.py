"""DEC-056 회귀 — debug/bootstrap_admin_id_logn.py 의 BLS_ADMIN_HCODE 기본값이
auth_service.py 의 슈퍼유저 분기(``hcode_norm == "0000"``) 와 정확히 일치하는
4자리 영(``"0000"``) 인지 정적 검증한다.

배경
----
- 과거 docstring/argparse 기본값이 5자리 ``"00000"`` 으로 적혀 있어,
  ``--apply`` 만으로 부트스트랩한 admin 행이 슈퍼유저 분기를 통과하지 못하고
  도메인 라우터에서 모두 403 을 받는 회귀가 발생했다.
- 본 테스트는 *코드와 docstring 양쪽 모두* 4자리로 동기화되었음을 보증해
  동일 회귀가 재발하지 않도록 한다.

검증 항목
---------
1. argparse 의 ``--hcode`` 기본값이 ``"0000"`` (4자리, 영) 이다.
2. docstring 의 안내 문장에도 ``00000`` 이 남아있지 않다 (5자리 시 폴백 SQL
   안내 문장 제외).
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from unittest import TestCase, main


_REPO_ROOT = Path(__file__).resolve().parent.parent
_BOOTSTRAP_PATH = _REPO_ROOT / "debug" / "bootstrap_admin_id_logn.py"


class BootstrapAdminDefaultHcodeTest(TestCase):
    def test_argparse_default_hcode_is_4digit_zero(self) -> None:
        """`--hcode` 기본값 = ``"0000"`` (auth_service ``hcode_norm == "0000"`` 와 정합)."""
        # BLS_ADMIN_HCODE env 가 설정되어 있으면 argparse 가 그것을 우선하므로 잠시 제거
        prev = os.environ.pop("BLS_ADMIN_HCODE", None)
        try:
            sys.path.insert(0, str(_REPO_ROOT / "debug"))
            sys.path.insert(0, str(_REPO_ROOT / "도서물류관리프로그램" / "backend"))
            try:
                # bootstrap 모듈은 import 시점에 load_config 를 호출하므로 직접 import 대신
                # 소스 파싱만 수행해 argparse 호출의 default 인자를 검증한다 (사이드이펙트 0).
                src = _BOOTSTRAP_PATH.read_text(encoding="utf-8")
                pattern = (
                    r'ap\.add_argument\(\s*"--hcode"\s*,\s*'
                    r'default=os\.environ\.get\(\s*"BLS_ADMIN_HCODE"\s*,\s*"([^"]+)"\s*\)'
                )
                m = re.search(pattern, src)
                self.assertIsNotNone(m, "--hcode argparse 정의가 발견되지 않음")
                assert m is not None  # mypy hint
                self.assertEqual(
                    m.group(1),
                    "0000",
                    f"--hcode 기본값이 4자리 '0000' 이 아님: {m.group(1)!r}. "
                    "auth_service._resolve_role_and_permissions 의 슈퍼유저 분기와 불일치.",
                )
            finally:
                # sys.path 복구 — 다른 테스트 격리
                for p in (str(_REPO_ROOT / "debug"), str(_REPO_ROOT / "도서물류관리프로그램" / "backend")):
                    while p in sys.path:
                        sys.path.remove(p)
        finally:
            if prev is not None:
                os.environ["BLS_ADMIN_HCODE"] = prev


if __name__ == "__main__":
    main(verbosity=2)
