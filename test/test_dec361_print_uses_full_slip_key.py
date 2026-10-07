"""DEC-361 — 거래명세서 인쇄(단건·일괄·자동출력)는 전표 키 **전체**로 조회·완료한다.

배경(2026-10-01 교문사 「자동출력이 안 된다」): 인쇄 라우트가 7세그먼트 키
(`일자|회사|차수|지점|전표번호|구분|거래처`)에서 앞 4축만 써서, 같은 날·같은 차수의 **지점 없는
거래처 전표들이 한 장으로 합쳐져** 인쇄됐다(운영 데이터: 8개 거래처 23줄이 한 거래처 이름으로).
`X-Printed-Keys` 도 4축 키를 돌려줘 프론트의 완료 전이가 다른 거래처 전표까지 완료시켰다.
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path
from unittest import TestCase
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import print_log_db  # noqa: E402
from app.services import transactions_service as tx  # noqa: E402

_SID = "remote_1"
# 알라딘(00431) 전표번호 67 · 세종대(00058) 전표번호 70 — 둘 다 2026.10.01 / 차수 1 / 지점 없음.
_K_ALADIN = "2026.10.01|H1|1||67|출고|00431"
_K_SEJONG = "2026.10.01|H1|1||70|출고|00058"


def _auth() -> dict:
    return {"user_id": "u1", "server_id": _SID, "hcode": "H1"}


def _detail(gcode: str) -> dict:
    return {
        "order_key": {"gdate": "2026.10.01", "hcode": "H1", "jubun": "1", "gjisa": ""},
        "customer": {"gcode": gcode, "gname": f"거래처{gcode}"},
        "lines": [{"gcode": gcode, "bcode": "B1", "gsqut": 1, "gssum": 1000}],
    }


def _decode(value: str) -> list[str]:
    return json.loads(base64.b64decode(value).decode("utf-8"))


class PrintUsesFullSlipKey(TestCase):
    def setUp(self) -> None:
        self._prev = {d: app.dependency_overrides.get(d) for d in (get_current_user, get_user_context)}
        for d in self._prev:
            app.dependency_overrides[d] = _auth
        self.client = TestClient(app)

    def tearDown(self) -> None:
        for d, prev in self._prev.items():
            if prev is not None:
                app.dependency_overrides[d] = prev
            else:
                app.dependency_overrides.pop(d, None)

    def _patches(self, detail_mock):
        from app.services import print_service

        return (
            patch.object(tx, "get_sales_statement_detail", detail_mock),
            patch.object(tx, "render_sales_statement_html", return_value="<html/>"),
            patch.object(tx, "render_sales_statements_combined_html", return_value="<html/>"),
            patch.object(print_service, "render_pdf", return_value=b"%PDF-1.4 f"),
            patch.object(print_log_db, "record_printed", AsyncMock(return_value=1)),
        )

    def test_single_pdf_passes_idnum_gubun_gcode(self) -> None:
        mock = AsyncMock(return_value=_detail("00431"))
        p = self._patches(mock)
        with p[0], p[1], p[2], p[3], p[4]:
            r = self.client.get(
                f"/api/v1/print/sales-statement/{_K_ALADIN.replace('|', '%7C')}.pdf?serverId={_SID}&source=auto"
            )
        self.assertEqual(r.status_code, 200, r.text)
        kw = mock.await_args.kwargs
        self.assertEqual((kw["jubun"], kw["gjisa"]), ("1", ""))
        self.assertEqual((kw["idnum"], kw["gubun"], kw["gcode"]), (67, "출고", "00431"))
        # 완료 전이용 키 = 요청받은 키 그대로(전표 단위) — 4축으로 줄이면 다른 거래처까지 완료된다.
        self.assertEqual(_decode(r.headers["X-Printed-Keys"]), [_K_ALADIN])

    def test_batch_pdf_keeps_each_slip_separate(self) -> None:
        seen: list[tuple] = []

        async def fake_detail(**kw):  # noqa: ANN001
            seen.append((kw["idnum"], kw["gcode"]))
            return None if kw["gcode"] == "00058" else _detail(kw["gcode"])

        p = self._patches(AsyncMock(side_effect=fake_detail))
        keys = ",".join(k.replace("|", "%7C") for k in (_K_ALADIN, _K_SEJONG))
        with p[0], p[1], p[2], p[3], p[4]:
            r = self.client.get(f"/api/v1/print/sales-statement/batch.pdf?serverId={_SID}&keys={keys}")
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(sorted(seen), [(67, "00431"), (70, "00058")])
        # 자료 없는 키는 제외, 남은 키는 요청 그대로.
        self.assertEqual(_decode(r.headers["X-Printed-Keys"]), [_K_ALADIN])

    def test_legacy_4_segment_key_still_works(self) -> None:
        mock = AsyncMock(return_value=_detail("00431"))
        p = self._patches(mock)
        with p[0], p[1], p[2], p[3], p[4]:
            r = self.client.get(f"/api/v1/print/sales-statement/2026.10.01%7CH1%7C1%7C.pdf?serverId={_SID}")
        self.assertEqual(r.status_code, 200, r.text)
        kw = mock.await_args.kwargs
        self.assertEqual((kw["idnum"], kw["gubun"], kw["gcode"]), (None, None, None))
        self.assertEqual(_decode(r.headers["X-Printed-Keys"]), ["2026.10.01|H1|1|"])

    def test_print_routes_do_not_use_4_axis_parser(self) -> None:
        src = (BACKEND / "app/routers/print.py").read_text(encoding="utf-8")
        # DEC-386 — 단건 · 일괄 · PDF · HTML 네 라우트가 한 준비 함수를 탄다(키 파싱은 그 한 곳).
        body = src[src.index("async def _prepare_sales_statement_print("):]
        self.assertNotIn("_parse_order_key_4(", body)
        self.assertEqual(body.count("_parse_stmt_key("), 1)
