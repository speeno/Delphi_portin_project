"""DEC-264/266/265 — 전표 입력 줄 자리 · 팝업 저장 후 자동 닫기 (2026-09-08 사용자 피드백 ①②).

① DEC-264 → **DEC-266** — 「신규 입고 접수」의 거래일자·입고처 코드가 띠 **우측 끝**에 몰려 있었다
   ("너무 우측으로 치우쳐 있습니다. 좌측 상단으로 이동 요청"). 먼저 띠 안에서 좌측 정렬(DEC-264)
   했다가, 이어진 요청("이 부분은 아래 카드 내로 포함하면 어떨까?")으로 **입력 필드와 저장 버튼을
   통째로 「라인」 카드 안 최상단**으로 옮겼다(DEC-266). 띠에는 제목·「목록」만 남는다.

② DEC-265 — 팝업에서 저장/수정을 끝내도 팝업이 열린 채 「저장 완료 …」 배너만 떠서 매번 ✕ 를
   눌러야 했다(입고현황·입고명세서 상세 팝업). **사용자 공통 규칙**: "팝업 화면에서 수정이나 저장
   동작을 수행한 이후에는 해당 팝업 창은 목적을 이루었으니 동시에 자동으로 닫히도록 한다."
   → 편집 팝업의 성공 경로는 `onClose()` 로 끝난다.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


class SlipHeaderFieldsInsideCard(TestCase):
    """DEC-266 — 전표 입력 줄(거래일자·거래처·저장)은 띠가 아니라 라인 카드 안 최상단."""

    def test_band_keeps_only_title_and_list(self) -> None:
        src = _read("components/transactions/slip-entry-layout.tsx")
        band = src[src.index("<PageHeader") : src.index("/>", src.index("<PageHeader"))]
        for gone in ("{headerForm}", "actions=", "save.onClick"):
            self.assertNotIn(gone, band, gone)
        self.assertIn("leading=", band)  # 「목록」 링크는 띠에 남는다

    def test_card_holds_fields_enter_scope_and_save(self) -> None:
        src = _read("components/transactions/slip-entry-layout.tsx")
        card = src[src.index('className="slip-header-form') :]
        self.assertIn('data-enter-scope=""', card)  # 레거시 Enter=Tab 스코프도 같이 내려왔다
        self.assertIn("advanceFocusOnEnter(e)", card)
        self.assertIn("{headerForm}", card)
        self.assertIn("save.onClick", card)
        self.assertIn('className="ml-auto flex flex-wrap items-center gap-2"', card)  # 저장은 줄 우측 끝

    def test_inline_label_css_follows_the_fields(self) -> None:
        """라벨을 입력 옆에 붙이는 규칙이 새 스코프에도 있어야 카드 안에서 띠와 같은 모양이 된다."""
        css = _read("app/globals.css")
        self.assertIn(".slip-header-form :is(.space-y-1, .space-y-1\\.5, .space-y-2)", css)

    def test_page_header_has_no_dead_align_switch(self) -> None:
        """DEC-264 의 filtersAlign 은 DEC-266 이 대체 — 쓰는 곳이 없어 되돌렸다."""
        self.assertNotIn("filtersAlign", _read("components/shared/page-header.tsx"))

    def test_slip_entry_screens_go_through_the_layout(self) -> None:
        """신규 입고/출고/반품/폐기는 골격을 쓰므로 한 곳(위 테스트)만 지키면 된다."""
        for rel in (
            "app/(app)/inbound/receipts/new/page.tsx",
            "app/(app)/outbound/orders/new/page.tsx",
            "app/(app)/returns/receipts/new/page.tsx",
            "app/(app)/returns/scrap/new/page.tsx",
        ):
            self.assertIn("<SlipEntryLayout", _read(rel), rel)


def _fn_body(src: str, name: str) -> str:
    """`async function <name>(` 부터 다음 최상위(2칸 들여쓰기) 함수 시작 전까지."""
    m = re.search(rf"\n  async function {re.escape(name)}\(", src)
    assert m, name
    rest = src[m.end() :]
    nxt = re.search(r"\n  (?:async )?function ", rest)
    return rest[: nxt.start()] if nxt else rest


class DialogClosesAfterSave(TestCase):
    """DEC-265 — 편집 팝업의 저장/확정 성공 경로는 팝업을 닫는다."""

    def test_inbound_receipt_dialog(self) -> None:
        src = _read("components/inbound/receipt-detail-dialog.tsx")
        body = _fn_body(src, "handleSave")
        self.assertIn("onChanged?.();", body)
        self.assertIn("onClose();", body)
        # 열린 채 남기던 「저장 완료 — 추가 …」 배너(info 상태)는 없어졌다
        self.assertNotIn("저장 완료 — 추가", src)
        self.assertNotIn("setInfo(", src)

    def test_outbound_order_dialog_save_and_cancel(self) -> None:
        src = _read("components/outbound/order-detail-dialog.tsx")
        for fn in ("handleSave", "handleCancelConfirm"):
            body = _fn_body(src, fn)
            self.assertIn("onClose();", body, fn)
        self.assertNotIn("저장 완료 — 추가", src)

    def test_sales_statement_dialogs_still_close(self) -> None:
        edit = _read("components/transactions/sales-statement-edit-dialog.tsx")
        self.assertIn("if (ok) onClose(true);", edit)
        line = _read("components/transactions/sales-statement-line-edit-dialog.tsx")
        self.assertIn("onSaveAndClose(", line)


class NoModalKeptOpenAfterMutation(TestCase):
    """새 팝업이 규칙을 어기지 않도록 — 모달 파일의 «쓰기» 호출 뒤엔 닫기 콜백이 있어야 한다.

    대상: `aria-modal` 을 그리는 컴포넌트에서 `await xxxApi.update/create/cancel/save(...)`.
    닫기로 인정: `onClose(` · `onSuccess(` · `onSaveAndClose(` · `onOpenChange(false)` ·
    `return true;`(저장 성공을 호출부에 돌려주고 그쪽이 닫는 형태 — 거래명세서 편집 팝업).
    """

    MUTATIONS = re.compile(r"await\s+\w+Api\.(update|create|cancel|save)\w*\(")
    CLOSERS = ("onClose(", "onSuccess(", "onSaveAndClose(", "onOpenChange(false)", "return true;")

    def test_mutating_modals_close(self) -> None:
        offenders: list[str] = []
        for path in sorted((FRONT).rglob("*.tsx")):
            src = path.read_text(encoding="utf-8")
            if "aria-modal" not in src:
                continue
            for m in self.MUTATIONS.finditer(src):
                after = src[m.end() : m.end() + 900]
                # 성공 경로(= catch 전)만 본다
                success = after.split("} catch", 1)[0]
                if not any(c in success for c in self.CLOSERS):
                    offenders.append(f"{path.relative_to(FRONT)}:{src[: m.start()].count(chr(10)) + 1}")
        self.assertEqual(offenders, [], f"저장/수정 후 닫지 않는 팝업: {offenders}")


if __name__ == "__main__":
    main()
