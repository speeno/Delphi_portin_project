"""DEC-264/265 — 전표 입력 띠 필드 좌측 정렬 · 팝업 저장 후 자동 닫기 (2026-09-08 사용자 피드백 ①②).

① DEC-264 — 「신규 입고 접수」의 거래일자·입고처 코드가 띠 **우측 끝**에 몰려 있어 제목(좌상단)과
   멀었다("너무 우측으로 치우쳐 있습니다. 좌측 상단으로 이동 요청"). `PageHeader` 에
   `filtersAlign="start"` 를 두고 전표 입력 골격(SlipEntryLayout)이 그것을 쓴다 —
   필드는 제목 옆(좌), 액션(저장)만 우측 끝.

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


class SlipHeaderFieldsOnTheLeft(TestCase):
    """DEC-264 — 띠 필드 정렬 스위치와 전표 입력 화면의 사용."""

    def test_page_header_supports_start_align(self) -> None:
        src = _read("components/shared/page-header.tsx")
        self.assertIn('filtersAlign?: "start" | "end"', src)
        self.assertIn('filtersAlign = "end"', src)  # 기존 화면(조회 필터)은 우측 그대로
        self.assertIn('filtersAlign === "start" ? "justify-start" : "justify-end"', src)
        # 필드가 좌측일 때 액션(저장 등)은 우측 끝으로 밀린다
        self.assertIn('filtersAlign === "start" && "ml-auto"', src)

    def test_slip_entry_layout_uses_start_align(self) -> None:
        src = _read("components/transactions/slip-entry-layout.tsx")
        self.assertIn('filtersAlign="start"', src)

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
