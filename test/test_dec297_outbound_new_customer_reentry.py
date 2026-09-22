"""DEC-297 — 신규 출고 주문(출고 접수) 거래처 재입력 먹통 + 거래처명 한 줄 + 도서명 입력칸 기준 (2026-09-22).

원문 1: "처음 거래처 입력 후 엔터는 잘 됩니다. 그런데, 저장하지 않고 입력한 거래처를 삭제하고, 동일한
거래처를 다시 입력하면 팝업도 안뜨고. 지사칸에서 엔터도 안넘어 갑니다."
원문 2: "거래처 표기 「거래처명」 으로 변경하고 컨트롤을 두줄이 아니라 한줄이 들어가도록 수정해라.
도서명 : 입력 부분에 입력 컨트롤 기반으로 값을 넣어줘."

원인 (실측 — 로컬 dev + Chrome 계측)
- 거래처 칸의 **입력 글자**(hcode)가 그대로 지사 목록·거래처 참조 조회 키였다. 타이핑·지우기 한 글자마다
  "0","00","000"… 부분 코드로 `/customer/{code}/branches` + `customer-preview` 가 2건씩 나가(응답은 버려도
  서버는 끝까지 처리) 서버가 밀렸고, 정작 거래처 확정용 자동완성 조회가 Enter 후 **8초** 뒤에야 끝났다.
  지우고 다시 치면 적체가 두 배 → "팝업도 안 뜨고 지사 Enter 가 안 넘어간다".
- MLF `clearInline` 이 결과만 비우고 "어느 검색어의 결과인가"(fetchedTermRef)는 남겨, **같은 값**을 다시
  치고 바로 Enter 하면 빈 결과를 캐시로 오인 → 자동확정 대신 검색 팝업(엔터 리듬 깨짐).

수정
- 화면: 입력 글자(hcode)와 **확정 거래처 코드(customerCode)** 분리. 지사·참조·특가·저장은 확정 코드만.
  입력이 확정 코드와 달라지면 확정 해제 + 앞 거래처 지사 비움. 재고 참조 도서도 도서명이 채워진(확정) 라인만.
- MLF: `clearInline` 이 fetchedTermRef 도 비움, Enter 확정은 진행 중 디바운스 조회를 seq 로 무효화.
- 라벨 「거래처명」 + 고른 거래처명은 입력칸 같은 줄 끝(`data-field-suffix`, 신규 입고 접수 「입고처명」 동형).
- 도서명: 도서코드 직접 입력 blur 보충 조회(DEC-169 `onLookupBook`) 배선 + 코드를 고쳐 쓰면 도서명·ISBN 비움.
  비동기 응답(보충 조회·특가)은 요청 시점 스냅샷이 아니라 최신 라인에 반영(linesRef).
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
PAGE = FE / "app" / "(app)" / "outbound" / "orders" / "new" / "page.tsx"
MLF = FE / "components" / "master" / "master-lookup-field.tsx"
GRID = FE / "components" / "outbound" / "order-line-grid.tsx"


def _fn_body(src: str, header: str) -> str:
    i = src.index(header)
    return src[i : src.index("\n  }\n", i)]


class LookupFieldForgetsClearedTerm(TestCase):
    def setUp(self) -> None:
        self.src = MLF.read_text(encoding="utf-8")

    def test_clear_inline_resets_fetched_term(self) -> None:
        body = _fn_body(self.src, "function clearInline()")
        self.assertIn('fetchedTermRef.current = ""', body)

    def test_confirm_enter_invalidates_inflight_before_cache_check(self) -> None:
        body = _fn_body(self.src, "async function confirmEnter(")
        bump = body.index("++seqRef.current")
        cache = body.index("fetchedTermRef.current !== term")
        self.assertLess(bump, cache, "Enter 확정은 캐시 판단 전에 진행 중 조회를 무효화해야 한다")


class OutboundNewUsesConfirmedCustomer(TestCase):
    def setUp(self) -> None:
        self.src = PAGE.read_text(encoding="utf-8")

    def test_confirmed_code_state_exists(self) -> None:
        self.assertIn('const [customerCode, setCustomerCode] = useState("")', self.src)

    def test_lookups_are_keyed_on_confirmed_code_not_typed_text(self) -> None:
        # 지사 목록·거래처 참조 effect 는 입력 글자(hcode)가 아니라 확정 코드에만 반응.
        self.assertIn("}, [serverId, customerCode]);", self.src)
        self.assertIn("}, [serverId, customerCode, refBcode, gjisa, gdate]);", self.src)
        self.assertNotRegex(self.src, r"\}, \[serverId, hcode[\],]")
        self.assertNotIn("const gc = hcode.trim()", self.src)

    def test_save_and_reference_use_confirmed_code(self) -> None:
        self.assertIn("const customer = customerCode;", self.src)
        self.assertIn("gcode={customerCode}", self.src)
        self.assertNotIn("gcode={hcode.trim()}", self.src)

    def test_both_confirm_paths_set_code_and_edit_unconfirms(self) -> None:
        self.assertIn("setCustomerCode(applyCustomerToHcode(selection, setHcode))", self.src)
        self.assertIn('setCustomerCode((c.hcode ?? "").trim())', self.src)
        self.assertIn("if (next.trim() !== customerCode) {", self.src)

    def test_clearing_customer_drops_previous_branch(self) -> None:
        i = self.src.index("const gc = customerCode;\n    if (!serverId || !gc) {\n      setBranchOptions")
        self.assertIn('setGjisa("");', self.src[i : i + 400])

    def test_stock_reference_only_for_resolved_books(self) -> None:
        self.assertIn("const resolvedBcode = (l?: DraftLine) =>", self.src)


class OutboundNewCustomerNameOneLine(TestCase):
    def setUp(self) -> None:
        self.src = PAGE.read_text(encoding="utf-8")

    def test_label_is_customer_name(self) -> None:
        self.assertIn('<Label htmlFor="hcode">거래처명</Label>', self.src)
        self.assertIn('placeholder="거래처명 또는 코드"', self.src)

    def test_name_is_suffix_on_same_line(self) -> None:
        m = re.search(r"<span\s+data-field-suffix[^>]*>\s*\{customerName\}\s*</span>", self.src)
        self.assertIsNotNone(m, "거래처명은 data-field-suffix 로 입력칸 같은 줄 끝에")
        self.assertNotIn("{customerName}({hcode})", self.src)


class SlipNoMovedToHeaderAfterBranch(TestCase):
    """원문 3: "전표 번호 항목입력 박스를 상단의 지사 입력 박스 다음으로 위치 이동해줘"."""

    def setUp(self) -> None:
        self.src = PAGE.read_text(encoding="utf-8")

    def test_slip_no_follows_branch_in_header(self) -> None:
        branch = self.src.index('<Label htmlFor="gjisa">지사 (선택)</Label>')
        slip = self.src.index('<Label htmlFor="slip-no" data-legacy-id="Sobo21.Panel201">전표번호</Label>')
        lines = self.src.index('linesLegacyId="Sobo27.PanelLines"')
        self.assertLess(branch, slip)
        self.assertLess(slip, lines, "전표번호는 헤더 입력 줄(headerForm) 안")

    def test_slip_no_is_readonly_and_outside_enter_flow(self) -> None:
        i = self.src.index('id="slip-no"')
        block = self.src[i : i + 300]
        self.assertIn("readOnly", block)
        self.assertIn("tabIndex={-1}", block)

    def test_reference_panel_hides_its_slip_no_here_only(self) -> None:
        self.assertIn("showSlipNo={false}", self.src)
        panel = (FE / "components" / "transactions" / "sales-statement-reference-panel.tsx").read_text(encoding="utf-8")
        self.assertIn("showSlipNo = true,", panel)  # 다른 3개 화면은 종전대로 패널에 표시


class BookNameFollowsCodeInput(TestCase):
    def test_outbound_wires_typed_code_lookup(self) -> None:
        src = PAGE.read_text(encoding="utf-8")
        self.assertIn("onLookupBook={lookupBook}", src)
        self.assertIn("resolveBookByCode(user.server_id, bcode)", src)

    def test_editing_code_clears_stale_name(self) -> None:
        src = GRID.read_text(encoding="utf-8")
        self.assertIn('{ bcode: next, product_name: "", isbn: "" }', src)

    def test_async_results_apply_to_latest_lines(self) -> None:
        src = GRID.read_text(encoding="utf-8")
        self.assertIn("function setAt(idx: number, patch: Partial<DraftLine>, base: T[] = lines)", src)
        body = _fn_body(src, "async function lookupTypedBook(")
        self.assertIn("const cur = linesRef.current[idx];", body)
        self.assertIn("linesRef.current,", body)
        # 특가 응답도 최신 라인 기준(요청 시점 스냅샷으로 도서명을 지우던 경로 제거).
        self.assertIn("applySpecial(idx, selection.code, sp)", src)
        self.assertNotIn("setAt(idx, { ...(sp.grat1", src)

    def test_list_pick_skips_redundant_blur_lookup(self) -> None:
        src = GRID.read_text(encoding="utf-8")
        self.assertIn("if (!onLookupBook || pickedRef.current[idx]) return;", src)
        self.assertEqual(src.count("pickedRef.current[idx] = true;"), 2)


if __name__ == "__main__":
    main()
