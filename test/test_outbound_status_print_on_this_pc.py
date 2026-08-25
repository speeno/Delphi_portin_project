"""출고 현황 — 선택분을 「이 PC 프린터」로 출력 (2026-08-22 운영 요청).

요청 원문
--------
"출고 현황에 선택한 항목 바로재출고(지정된 자동 출력용) 버튼과 유사하게 현재 사용자 PC
출력 가능하도록 거래명세서 출력 기능 및 버튼을 추가해주세요."

배경
----
기존 「바로출고」/「바로재출고」는 *지정된 자동출력 PC* 의 인쇄 큐로 보내는 **원격 지시**
(`transactionsApi.urgentPrint`)라, 지금 앉아 있는 PC 에서 뽑을 수단이 없었다.

추가 동작
--------
- 거래 명세서 목록의 단건/일괄 인쇄와 **같은 엔드포인트**
  (`salesStatementPdfUrl`/`salesStatementBatchPdfUrl`)를 쓰되, 양식은
  **2단 일반**(`layout=default` — A4 1장에 공급자·공급받는자 상·하 블록, 절취선)이다
  (2026-08-22 운영 요청. 종전 레거시 삼련에서 변경. `borders` 는 삼련 전용이라 미전달).
  `printPdfFromUrl` 로 브라우저 인쇄 대화상자를 띄운다.
- 2건 이상은 batch PDF 1개로 묶어 대화상자가 1회만 뜬다.
- **상태 전이 없음** — 바로재출고와 동일하게 출력 수단만 추가한 것이다.
- 키는 `serializeStatementKey`(인쇄 API 규약). 화면의 선택키 `slipKey`
  (`gdate|hcode|jubun|gjisa|gcode`)와 **다르다** — 혼용하면 전표가 어긋난다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
PAGE = (
    ROOT / "도서물류관리프로그램" / "frontend" / "src"
    / "components" / "transactions" / "transaction-status-screen.tsx"
)


class PrintOnThisPcTests(TestCase):
    def setUp(self) -> None:
        self.src = PAGE.read_text(encoding="utf-8")
        i = self.src.index("async function doPrintOnThisPc")
        self.fn = self.src[i : self.src.index("async function doBatchReprint")]

    def test_button_present_and_labelled(self) -> None:
        self.assertIn('data-legacy-id="Sobo24.PrintOnThisPc"', self.src)
        self.assertIn("거래 명세서 출력", self.src)

    def test_button_shown_for_any_selection(self) -> None:
        """상태 무관 — 선택이 1건이라도 있으면 노출(바로출고/재출고는 상태별 카운트 조건)."""
        self.assertIn("{checkedKeys.size > 0 && (", self.src)

    def test_uses_browser_print_not_remote_queue(self) -> None:
        """이 PC 출력은 printPdfFromUrl(브라우저 인쇄) — urgentPrint(원격 큐)가 아니다."""
        self.assertIn("printPdfFromUrl(url)", self.fn)
        self.assertNotIn("urgentPrint", self.fn)

    def test_single_vs_batch_endpoint(self) -> None:
        self.assertIn("keys.length === 1", self.fn)
        self.assertIn("salesStatementPdfUrl(keys[0], sid, opts)", self.fn)
        self.assertIn("salesStatementBatchPdfUrl(keys, sid, opts)", self.fn)

    def test_uses_two_tier_default_form(self) -> None:
        """양식 = 2단 일반(`layout=default`) — A4 1장에 공급자·공급받는자 상·하 블록(절취선).

        2026-08-22 운영 요청. 종전에는 거래 명세서 목록과 같은 레거시 삼련
        (`legacy_triplicate`)이었다. `borders`(양식지 테두리)는 삼련 전용 옵션이라
        이 경로에서는 넘기지 않는다.
        """
        # 주석에 등장하는 단어는 제외 — 실제 코드만 본다.
        code = "\n".join(
            ln for ln in self.fn.splitlines() if not ln.strip().startswith("//")
        )
        self.assertIn('layout: "default"', code)
        self.assertNotIn("legacy_triplicate", code)
        self.assertNotIn("borders", code)

    def test_immediate_dispatch_untouched(self) -> None:
        """「바로출고」/「바로재출고」는 원래 기능 그대로 — 원격 큐(urgentPrint) 유지."""
        self.assertIn("doBatchImmediateDispatch", self.src)
        self.assertIn("doBatchReprint", self.src)
        self.assertIn("urgentPrint", self.src)

    def test_uses_statement_key_not_slip_key(self) -> None:
        """인쇄 API 키는 serializeStatementKey — 화면 선택키(slipKey)와 혼용 금지."""
        self.assertIn("serializeStatementKey(s.order_key)", self.fn)
        self.assertNotIn("slipKey(s.order_key))\n      .map", self.fn)

    def test_does_not_change_status(self) -> None:
        """출력 수단만 추가 — 완료 전이/출고요청 호출이 섞이면 안 된다."""
        for forbidden in ("completeSalesStatement", "requestDispatch", "batchRequest"):
            self.assertNotIn(forbidden, self.fn, f"{forbidden} 가 이 PC 출력 경로에 있으면 안 된다")

    def test_selected_slip_can_print_in_place(self) -> None:
        """선택 → 상세 → 수정 → 저장 → **출력** 을 한 자리에서 끝낼 수 있어야 한다.

        상단 일괄 버튼은 체크박스(checkedKeys) 기반이라, 행을 클릭만 한 전표는
        대상이 아니었다(2026-08-22 사용자 확인 요청). 우측 상세 액션 줄의 「출력」이
        지금 보고 있는 전표 1건을 명시 대상으로 넘긴다.
        """
        self.assertIn('data-legacy-id="Sobo24.PrintSelected"', self.src)
        self.assertIn("doPrintOnThisPc([selectedSlip])", self.src)
        # 핸들러가 명시 대상을 받도록 열려 있어야 한다(없으면 체크박스 선택만 인쇄됨).
        self.assertIn("doPrintOnThisPc(targets?: OutboundStatusSlipItem[])", self.src)
        self.assertIn("targets ?? slips.filter", self.src)

    def test_edit_then_save_refreshes_selected_lines(self) -> None:
        """수정 팝업 저장 후 목록·선택 라인이 재조회돼야 출력이 최신 내용을 담는다."""
        self.assertIn('data-legacy-id="Sobo24.EditSlip"', self.src)
        # 2026-08-25(DEC-195) — 저장 후 재조회는 축별 상세 API 를 타는 onSlipChanged 하나로
        # 모였다(출고축 outboundApi.detail / 입고축 inboundApi.detail). 팝업 두 종 모두 이를 쓴다.
        self.assertEqual(self.src.count("onChanged={onSlipChanged}"), 2)
        i = self.src.index("function onSlipChanged()")
        block = self.src[i : i + 500]
        self.assertIn("void load(0)", block)
        self.assertIn("fetchDetailLines(it, user.server_id)", block)
        fn = self.src[self.src.index("async function fetchDetailLines") :][:700]
        self.assertIn("outboundApi.detail(key, sid)", fn)
        self.assertIn("inboundApi.detail(key, sid)", fn)

    def test_remote_queue_buttons_still_present(self) -> None:
        """기존 바로출고/바로재출고(자동출력 PC 큐)는 그대로 남아 있어야 한다."""
        self.assertIn('data-legacy-id="Sobo24.BatchImmediateDispatch"', self.src)
        self.assertIn('data-legacy-id="Sobo24.BatchReprint"', self.src)
        self.assertIn("urgentPrint", self.src)


if __name__ == "__main__":
    main()
