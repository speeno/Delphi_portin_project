"""신규 입고 저장이 입고 축(Scode='Y')으로 들어가는지 — 2026-08-25 사용자 리포트 회귀.

증상
----
"입고현황 : 신규 입력한 8월22일 내용이 목록·상세에서 검색 안나옵니다."

원인
----
요청 모델 ``ReceiptHeaderInput`` 이 ``scode='X'`` / ``ocode='B'`` 를 **기본값으로 박아**
항상 값을 실어보냈다. 서비스의 축 폴백(``_safe_str(header.get("scode")) or "Y"``,
``or _inbound_ocode(server_id)``)은 값이 비어 있을 때만 동작하므로 죽어 있었고,
신규 입고가 전부 ``Scode='X'``(거래처축) + ``Ocode='B'`` 로 저장됐다.

입고 조회는 전부 ``Scode='Y'`` 축이라(입고접수 목록·입고명세서·입고현황) 방금 입력한
전표가 **어느 화면에서도 보이지 않는다.** 교문사 remote_153 실측: 2026.08.22 입력분
2행이 `Scode='X'`/`Ocode='B'` 로 저장돼 있었고, 같은 테넌트의 다른 입고 9,376행은
전부 `Scode='Y'`/`Ocode='A'` 다.

가드
----
1. 모델 기본값이 축을 덮지 않는다(빈 문자열).
2. 요청이 scode/ocode 를 생략하면 INSERT 파라미터가 'Y' / 서버 정본 Ocode 다.
3. 명시 지정은 존중한다(마이그레이션·보정 경로).

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from app.models.inbound import ReceiptHeaderInput  # noqa: E402
from app.services import inbound_service  # noqa: E402


class HeaderModelDefaultTests(TestCase):
    def test_scode_ocode_default_empty_so_server_decides(self) -> None:
        h = ReceiptHeaderInput(gdate="2026-08-22", hcode="5019", gcode="00062")
        # 'X'/'B' 를 기본값으로 두면 서비스 폴백이 죽는다 — 축 결정은 서버 몫.
        self.assertEqual(h.scode, "")
        self.assertEqual(h.ocode, "")
        self.assertEqual(h.gubun, "입고")


class CreateReceiptAxisTests(TestCase):
    """create_receipt 가 INSERT 에 싣는 Scode/Ocode."""

    def _captured_insert(self, header_extra: dict) -> dict:
        statements: list[tuple[str, tuple]] = []

        async def fake_tx(server_id, stmts):
            statements.extend(stmts)

        async def fake_cols(server_id):
            return {"idnum"}

        async def fake_locked(server_id, gdate):
            return False

        async def fake_idnum(server_id, gdate, hcode):
            return 7

        header = {"gdate": "2026-08-22", "hcode": "5019", "gcode": "00062", "jubun": "07"}
        header.update(header_extra)

        with patch.object(inbound_service, "execute_in_transaction", side_effect=fake_tx), \
             patch.object(inbound_service, "_present_cols", side_effect=fake_cols), \
             patch.object(inbound_service, "_is_period_locked", side_effect=fake_locked), \
             patch.object(inbound_service, "allocate_idnum", side_effect=fake_idnum):
            asyncio.run(
                inbound_service.create_receipt(
                    server_id="remote_153",
                    header=header,
                    lines=[{"bcode": "3411", "gsqut": 1, "gdang": 30000, "pubun": "신간"}],
                    memo=None,
                )
            )

        sql, params = statements[0]
        cols = [c.strip() for c in sql.split("(", 1)[1].split(")", 1)[0].split(",")]
        return dict(zip(cols, params))

    def test_omitted_axis_falls_back_to_inbound(self) -> None:
        row = self._captured_insert({})
        self.assertEqual(row["Scode"], "Y", "입고는 Subu22 원본 Scode='Y'")
        # remote_153(chul_09_db)은 창고 서버 → 'A'. 교문사 레거시 입고 행과 같다.
        self.assertEqual(row["Ocode"], "A")
        self.assertEqual(row["Gubun"], "입고")

    def test_model_default_does_not_leak_customer_axis(self) -> None:
        """모델을 통과한 헤더(기본값 포함)도 축이 유지된다 — 회귀의 정확한 재현 경로."""
        h = ReceiptHeaderInput(gdate="2026-08-22", hcode="5019", gcode="00062", jubun="07")
        row = self._captured_insert(h.model_dump())
        self.assertEqual(row["Scode"], "Y")
        self.assertEqual(row["Ocode"], "A")

    def test_explicit_axis_is_respected(self) -> None:
        """명시 지정은 존중 — 데이터 보정/마이그레이션 경로를 막지 않는다."""
        row = self._captured_insert({"scode": "X", "ocode": "B"})
        self.assertEqual(row["Scode"], "X")
        self.assertEqual(row["Ocode"], "B")


if __name__ == "__main__":
    main()
