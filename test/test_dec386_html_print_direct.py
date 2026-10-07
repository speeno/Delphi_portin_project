"""DEC-386 — 거래명세서 인쇄: 서버 PDF 생성 없이 HTML 을 브라우저가 바로 인쇄.

사용자(2026-10-07) 「PDF를 생성하지 말고 HTML로 바로 인쇄처리해」 · 「자동 프린트 기능이 작동하지 않는다 … 테스트 진행해서 오류를
찾아 수정해라」.

Render 로그(2026-10-07 20:13~20:47 KST): 단건 PDF 19~105초 · 일괄 181초(WeasyPrint CPU). 20:27:37 · 20:38:08/18 바로출고는
PDF 요청이 진행 중일 때 배포 재시작(20:29:40 · 20:38:51)에 끊겼고, 모니터는 실패한 바로출고를 «시도함»으로 지워 다시 인쇄하지 않았다.

가드
----
- ``.html`` 단건 · ``batch.html`` 일괄 라우트 = PDF 와 같은 파라미터 · ``X-Printed-Keys`` · 출력 이력 kind, 본문은 text/html.
- ``browser_print_html``: ``@page`` 여백 → 0 + «장» 블록 padding(머리글 · 바닥글 · 대화상자 여백 설정에 안전), 색 그대로.
- PDF 라우트는 같은 준비 경로를 타고 ``pdf=`` 계측이 남는다(리팩터 회귀).
- 프론트: 자동출력 · 거래명세서 목록 · 현황 «이 PC 출력» 이 HTML 경로를 쓰고, 실패한 바로출고는 보관에 남겨 폴 · 재연결 때 재시도.
"""

from __future__ import annotations

import base64
import json
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.core.deps import get_user_context
from app.main import app
from app.routers.auth import get_current_user
from app.services import (
    print_log_db,
    print_service,
    sales_statement_layout_registry,
    tenant_print_assets,
    transactions_service,
)

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
_SID = "remote_1"
_KEY = "2026.10.07|H1|00001|"
_KEY2 = "2026.10.07|H1|00002|"


def _auth() -> dict:
    return {"user_id": "u1", "server_id": _SID, "hcode": "H1", "role": "operator", "permissions": ["outbound.write"]}


def _read(rel: str) -> str:
    return (FE / rel).read_text(encoding="utf-8").replace("\r\n", "\n")


def _detail(jubun: str = "00001") -> dict:
    return {
        "order_key": {"gdate": "2026.10.07", "hcode": "H1", "jubun": jubun, "gjisa": ""},
        "customer": {"hcode": "H1", "gname": "테스트거래처"},
        "lines": [{"gcode": "00001", "bcode": "B1", "product_name": "도서A", "shelf": "", "pubun": "위탁",
                   "gsqut": 3, "gdang": 10000, "grat1": 70, "gssum": 21000, "gbigo": ""}],
    }


def _decode(h: str) -> list[str]:
    return json.loads(base64.b64decode(h).decode("utf-8"))


class BrowserPrintHtml(unittest.TestCase):
    def test_triplicate_margins_move_to_sheet(self) -> None:
        html = ("<html><head><style>@page { size: 210mm 297mm; margin: 6mm 8mm; }"
                "@page { margin-top: 0mm; margin-bottom: 0mm; }</style></head><body></body></html>")
        out = print_service.browser_print_html(html, sheet_selector=".triplicate-sheet")
        self.assertIn("@page { margin: 0; }", out)
        self.assertIn(".triplicate-sheet { padding: 0mm 8mm 0mm 8mm; box-sizing: border-box; }", out)
        self.assertIn("print-color-adjust: exact", out)
        self.assertLess(out.index("margin: 6mm 8mm"), out.index("@page { margin: 0; }"))  # 뒤 선언이 이긴다

    def test_a4_margins(self) -> None:
        out = print_service.browser_print_html(
            "<html><head><style>@page { size: 210mm 297mm; margin: 6mm 8mm; }</style></head><body></body></html>",
            sheet_selector=".statement-page",
        )
        self.assertIn(".statement-page { padding: 6mm 8mm 6mm 8mm; box-sizing: border-box; }", out)

    def test_sheet_selector_registry(self) -> None:
        self.assertEqual(sales_statement_layout_registry.sheet_selector_for("legacy_triplicate"), ".triplicate-sheet")
        self.assertEqual(sales_statement_layout_registry.sheet_selector_for("default"), ".statement-page")
        self.assertEqual(sales_statement_layout_registry.sheet_selector_for("nope"), "body")
        for row in sales_statement_layout_registry.list_layout_entries():
            self.assertNotIn("sheet_selector", row)  # API 노출 목록은 종전과 같다


class HtmlPrintRoutes(unittest.TestCase):
    def setUp(self) -> None:
        # test_dec361 과 같은 격리 — JWT · 소유성 컨텍스트(다른 테스트가 남긴 ownership_server)를 타지 않는다.
        self._prev = {d: app.dependency_overrides.get(d) for d in (get_current_user, get_user_context)}
        app.dependency_overrides[get_current_user] = _auth
        app.dependency_overrides[get_user_context] = _auth
        self.client = TestClient(app)
        self.hdr = {"Authorization": "Bearer test"}

    def tearDown(self) -> None:
        for dep, prev in self._prev.items():
            if prev is None:
                app.dependency_overrides.pop(dep, None)
            else:
                app.dependency_overrides[dep] = prev

    def _patches(self, details: dict[str, dict | None]):
        async def _detail_of(*, server_id, gdate, hcode, jubun, gjisa, **_scope):
            return details.get(jubun)

        self.log = AsyncMock(return_value=1)
        return (
            patch.object(transactions_service, "get_sales_statement_detail", AsyncMock(side_effect=_detail_of)),
            patch.object(tenant_print_assets, "hydrate_seal_from_db", AsyncMock(return_value=None)),
            patch.object(print_log_db, "record_printed", self.log),
        )

    def test_single_html(self) -> None:
        p1, p2, p3 = self._patches({"00001": _detail()})
        with p1, p2, p3:
            r = self.client.get(
                f"/api/v1/print/sales-statement/{_KEY.replace('|', '%7C')}.html"
                f"?serverId={_SID}&layout=legacy_triplicate&borders=off&source=auto",
                headers=self.hdr,
            )
        self.assertEqual(r.status_code, 200, r.text[:300])
        self.assertTrue(r.headers["content-type"].startswith("text/html"))
        self.assertEqual(_decode(r.headers["X-Printed-Keys"]), [_KEY])
        self.assertIn("html=", r.headers["X-Print-Timing"])
        self.assertNotIn("pdf=", r.headers["X-Print-Timing"])
        self.assertIn("@page { margin: 0; }", r.text)
        self.assertIn(".triplicate-sheet { padding: 0mm 8mm 0mm 8mm;", r.text)
        self.assertIn("class='preprinted'", r.text)
        self.assertEqual(self.log.await_args.kwargs["kind"], "auto")

    def test_batch_html_only_found_keys(self) -> None:
        p1, p2, p3 = self._patches({"00001": _detail(), "00002": None})
        keys = ",".join(k.replace("|", "%7C") for k in (_KEY, _KEY2))
        with p1, p2, p3:
            r = self.client.get(
                f"/api/v1/print/sales-statement/batch.html?serverId={_SID}&keys={keys}&layout=legacy_triplicate",
                headers=self.hdr,
            )
        self.assertEqual(r.status_code, 200, r.text[:300])
        self.assertEqual(_decode(r.headers["X-Printed-Keys"]), [_KEY])
        self.assertEqual(self.log.await_args.kwargs["kind"], "batch")
        self.assertIn("@page { margin: 0; }", r.text)

    def test_batch_html_rejects_empty_and_bad_layout(self) -> None:
        r = self.client.get(f"/api/v1/print/sales-statement/batch.html?serverId={_SID}&keys=", headers=self.hdr)
        self.assertEqual(r.status_code, 422)
        r = self.client.get(
            f"/api/v1/print/sales-statement/batch.html?serverId={_SID}&keys={_KEY.replace('|', '%7C')}&layout=zzz",
            headers=self.hdr,
        )
        self.assertEqual(r.status_code, 422)

    def test_pdf_route_still_shares_path(self) -> None:
        p1, p2, p3 = self._patches({"00001": _detail()})
        with p1, p2, p3, patch.object(print_service, "render_pdf", return_value=b"%PDF-1.4 f"):
            r = self.client.get(
                f"/api/v1/print/sales-statement/{_KEY.replace('|', '%7C')}.pdf?serverId={_SID}&layout=legacy_triplicate",
                headers=self.hdr,
            )
        self.assertEqual(r.status_code, 200, r.text[:300])
        self.assertEqual(r.headers["content-type"], "application/pdf")
        self.assertIn("pdf=", r.headers["X-Print-Timing"])
        self.assertEqual(_decode(r.headers["X-Printed-Keys"]), [_KEY])
        self.assertEqual(self.log.await_args.kwargs["kind"], "single")


class FrontendWiring(unittest.TestCase):
    def test_print_api_html_path(self) -> None:
        src = _read("lib/print-api.ts")
        for s in ("export function salesStatementHtmlUrl(", "export function salesStatementBatchHtmlUrl(",
                  "export async function printHtmlFromUrl(", "iframe.srcdoc = html;",
                  'if (!contentType.includes("text/html")', "win?.document?.fonts?.ready"):
            self.assertIn(s, src, s)

    def test_call_sites_use_html(self) -> None:
        page = _read("app/(app)/transactions/sales-statement/auto-print/page.tsx")
        self.assertIn("printHtmlFromUrl(url, { settleMs: gapMs })", page)
        self.assertIn("? salesStatementHtmlUrl(keys[0], sid, opts)", page)
        self.assertNotIn("printPdfFromUrl", page)
        lst = _read("app/(app)/transactions/sales-statement/page.tsx")
        self.assertIn("printHtmlFromUrl(url)", lst)
        self.assertNotIn("printPdfFromUrl", lst)
        st = _read("components/transactions/transaction-status-screen.tsx")
        self.assertIn("printHtmlFromUrl(url)", st)
        self.assertNotIn("printPdfFromUrl", st)

    def test_preview_page_uses_html(self) -> None:
        """미리보기 화면도 HTML(사용자 2026-10-07 「미리보기 화면도 HTML로 바꿔줘」) — 다운로드만 PDF."""
        page = _read("app/(app)/transactions/sales-statement/[orderKey]/print/page.tsx")
        self.assertIn("useAuthenticatedHtmlPreview(htmlUrl)", page)
        self.assertIn("srcDoc={previewHtml}", page)
        self.assertIn('id="sales-preview-frame"', page)
        self.assertNotIn("useAuthenticatedPdfPreview", page)
        self.assertIn("downloadPdfWithAuth(\n        pdfUrl,", page)  # 파일 다운로드는 서버 PDF 그대로
        hook = _read("hooks/use-authenticated-html-preview.ts")
        self.assertIn("fetchAuthenticatedPrintHtml(htmlUrl)", hook)
        self.assertIn("@media screen {", hook)  # 화면 전용 종이 모양 — 인쇄 결과엔 무영향
        layout = _read("hooks/use-sales-statement-pdf-layout.ts")
        self.assertIn("const buildHtmlUrl = useCallback(", layout)

    def test_failed_urgent_keys_are_retried(self) -> None:
        page = _read("app/(app)/transactions/sales-statement/auto-print/page.tsx")
        self.assertIn("const urgentInFlightRef = useRef<Set<string>>(new Set());", page)
        self.assertIn("if (ok) {\n            removePendingUrgentKey(key);\n            printedRef.current.add(key);", page)
        # 재시도 지점: 다시 열렸을 때 · 폴 틱마다 · 스트림 재연결 직후
        self.assertGreaterEqual(page.count("printUrgentKeys(loadPendingUrgentKeys());"), 3)
        self.assertIn("if (ok) printUrgentKeys(loadPendingUrgentKeys());", page)


if __name__ == "__main__":
    unittest.main()
