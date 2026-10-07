"""DEC-380 — 반품 · 폐기 줄 기본 수량 -1 + 음수 수량 저장 허용 + 수정 화면 줄 추가 (교문사 2026-10-07).

보고: 「반품접수 시 도서명을 선택하면 수량은 기본 -1」 + 캡처 `(422) returnLines.0.gsqut — Input should be greater than or equal to 1`.
- 입력 모델이 수량 ≥ 1 만 받아 -1 이 거절됐다. 서버는 어차피 음수로 저장(-abs, DEC-301)하므로 **0 만** 막는다.
- 수정 화면(update_return_lines)의 줄 추가 INSERT 가 거래처(Gcode) 값을 빠뜨려 자리 수가 맞지 않았다(12/13) + 수량 · 금액을 정규화하지 않았다.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

from pydantic import ValidationError

from app.models.returns import ReturnLineInput
from app.services import returns_service as svc

FE = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "frontend" / "src"


class QtyValidation(TestCase):
    def test_negative_and_positive_ok_zero_rejected(self) -> None:
        self.assertEqual(ReturnLineInput(bcode="3320", gsqut=-1).gsqut, -1)
        self.assertEqual(ReturnLineInput(bcode="3320", gsqut=2).gsqut, 2)
        with self.assertRaises(ValidationError):
            ReturnLineInput(bcode="3320", gsqut=0)

    def test_frontend_default_minus_one(self) -> None:
        src = (FE / "components" / "outbound" / "order-line-grid.tsx").read_text(encoding="utf-8")
        self.assertIn("newLine: { gsqut: -1, grat1: RETURN_GRAT1_DEFAULT },", src)


class UpdateAddsLineCorrectly(IsolatedAsyncioTestCase):
    async def test_insert_has_gcode_and_negative_qty(self) -> None:
        existing = [{"Gdate": "2026.10.07", "Hcode": "5019", "Jubun": "4", "Bcode": "3411", "Gcode": "00238",
                     "Pubun": "정품", "Gsqut": -1, "Gdang": 30000, "Grat1": 85, "Gssum": -25500, "Gbigo": "", "Yesno": "1"}]
        captured: list[tuple[str, tuple]] = []

        async def fake_tx(server_id: str, ops: list) -> list[int]:
            captured.extend(ops)
            return [1] * len(ops)

        with patch.object(svc, "execute_query", AsyncMock(return_value=existing)), \
             patch.object(svc, "execute_in_transaction", AsyncMock(side_effect=fake_tx)), \
             patch.object(svc, "_default_outbound_ocode", return_value="A"), \
             patch.object(svc, "build_d_select_clause", AsyncMock(return_value="")):
            await svc.update_return_lines(
                server_id="remote_153", return_key_str="G|2026.10.07|5019|4",
                lines=[{"idnum": 0, "bcode": "3411", "pubun": "정품", "gsqut": -1, "gdang": 30000, "grat1": 85},
                       {"bcode": "3320", "pubun": "정품", "gsqut": 2, "gdang": 20000, "grat1": 85}],
            )
        inserts = [(q, p) for q, p in captured if q.startswith("INSERT INTO S1_Ssub")]
        self.assertEqual(len(inserts), 1)
        sql, params = inserts[0]
        self.assertEqual(sql.count("%s"), len(params))
        self.assertIn("00238", params)  # 거래처 = 기존 전표의 거래처
        self.assertIn(-2, params)  # 양수 입력도 음수로 저장
        self.assertIn(-34000, params)  # 금액 = round(20000 × -2 × 85 / 100)


if __name__ == "__main__":
    main()
