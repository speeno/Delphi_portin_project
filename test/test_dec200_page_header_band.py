"""DEC-200 — 화면 상단 흰 띠(PageHeader) 전 화면 일괄 반영 가드 (2026-08-25 13:18 목업 「도서별 수불원장 디폴트」).

목업에서 추출해 모든 화면에 같은 방식으로 반영한 요소
----------------------------------------------
1. 제목(굵게) 왼쪽 + 필터·「검색」 오른쪽이 **한 흰 띠**(전폭, 아래 경계선) — 카드 프레임 없음.
2. 필터 라벨은 입력 옆(인라인) — 띠 안의 `.space-y-1` 세로 묶음을 CSS 로 가로로.
3. 「검색/조회」는 Bukio Black 채움(Button 기본 variant) — secondary/outline/sm 제거.
4. 회색 캔버스 위 조회 전 안내문은 프레임 없이 가운데(`EmptyHint`).

이관은 scratch 스크립트(JSX-lite 스캐너)로 106개 파일을 일괄 변환했다. 아래는 그 결과가
되돌아가지 않도록 잡는 구조 가드다.
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
APP = FRONT / "app" / "(app)"


def _read(rel: str) -> str:
    return (FRONT / rel).read_text(encoding="utf-8")


def _app_pages() -> list[Path]:
    return sorted(p for p in APP.glob("**/page.tsx") if "/print/" not in str(p))


class PageHeaderComponentContract(TestCase):
    def test_component_shape(self) -> None:
        src = _read("components/shared/page-header.tsx")
        # 전폭 흰 띠 — 임베드 래퍼 px-[5px] 상쇄, 아래 경계선, 카드 프레임(rounded/shadow) 없음
        self.assertIn("-mx-[5px]", src)
        self.assertIn("border-b border-border bg-card", src)
        self.assertNotIn("rounded-2xl", src)
        self.assertNotIn("shadow-sm", src)
        # 제목 좌 / 필터·액션 우 (md 이상 2열 그리드)
        self.assertIn("md:grid-cols-[auto_minmax(0,1fr)]", src)
        self.assertIn('data-slot="page-header-filters"', src)
        for prop in ("leading", "titleAside", "actions", "children", "subtitle"):
            self.assertIn(prop, src, prop)
        # 조회 전 안내 — 프레임 없는 가운데 회색 글자
        self.assertIn("export function EmptyHint", src)
        self.assertNotIn('data-slot="empty-hint"\n      className={cn(\n        "rounded', src)

    def test_portal_screen_title_delegates(self) -> None:
        src = _read("components/shared/portal-screen-title.tsx")
        self.assertIn("<PageHeader", src)
        self.assertNotIn("<h1", src)

    def test_inline_label_css_scoped_to_band(self) -> None:
        css = _read("app/globals.css")
        self.assertIn(".page-header :is(.space-y-1, .space-y-1\\.5, .space-y-2)", css)
        self.assertIn("flex-direction: row", css)
        # 띠 밖(등록 폼 등)의 space-y-1 은 건드리지 않는다 — 선택자는 반드시 .page-header 로 시작
        for ln in css.splitlines():
            if "space-y-1" in ln and "{" in ln:
                self.assertTrue(ln.strip().startswith(".page-header"), ln)


class MigrationCoverage(TestCase):
    def test_most_screens_use_page_header(self) -> None:
        pages = _app_pages()
        using = [p for p in pages if "<PageHeader" in p.read_text(encoding="utf-8")]
        self.assertGreaterEqual(len(using), 95, f"PageHeader 사용 화면 {len(using)}/{len(pages)}")

    def test_no_legacy_title_block_left(self) -> None:
        """종전 81개 화면이 복제하던 제목 블록(h1.text-xl + p.text-sm.text-muted-foreground)이 남아 있으면 안 된다."""
        legacy = re.compile(
            r'<h1 className="text-xl font-semibold tracking-tight">[^<]*</h1>\s*<p className="text-sm text-muted-foreground'
        )
        left = [str(p.relative_to(APP)) for p in _app_pages() if legacy.search(p.read_text(encoding="utf-8"))]
        self.assertEqual(left, [], left)

    def test_no_filter_card_frame_directly_under_page_header(self) -> None:
        """띠 안(PageHeader children)에는 카드 프레임 문자열이 없어야 한다."""
        frame = "flex flex-wrap items-end gap-3 rounded-2xl border border-border bg-card p-4 shadow-sm"
        bad = []
        for p in _app_pages():
            src = p.read_text(encoding="utf-8")
            i = src.find("<PageHeader")
            if i == -1:
                continue
            j = src.find("</PageHeader>", i)
            if j != -1 and frame in src[i:j]:
                bad.append(str(p.relative_to(APP)))
        self.assertEqual(bad, [], bad)

    def test_filter_container_attributes_preserved(self) -> None:
        """필터 컨테이너의 onKeyDown(Enter 이동, DEC-104/105)·data-legacy-id 는 display:contents 래퍼로 보존된다."""
        src = _read("app/(app)/inventory/status/page.tsx")
        i = src.index("<PageHeader")
        j = src.index("</PageHeader>", i)
        band = src[i:j]
        self.assertIn('className="contents"', band)
        self.assertIn("onKeyDown=", band)
        self.assertIn("advanceFilterOnEnter", src)

    def test_search_button_is_dark_filled(self) -> None:
        """대표 화면 3곳 — 띠 안의 조회/검색 버튼에 secondary/outline/sm 이 남아 있지 않다."""
        for rel in (
            "app/(app)/inventory/ledger/page.tsx",
            "app/(app)/master/customer/page.tsx",
            "app/(app)/reports/book-sales/page.tsx",
        ):
            src = _read(rel)
            i = src.index("<PageHeader")
            j = src.index("</PageHeader>", i)
            band = src[i:j]
            for m in re.finditer(r"<Button\b([^>]*?)>\s*(?:<RefreshCw[^>]*/>\s*)?(조회|검색)\s*</Button>", band, re.DOTALL):
                attrs = m.group(1)
                self.assertNotIn('variant="secondary"', attrs, rel)
                self.assertNotIn('variant="outline"', attrs, rel)
                self.assertNotIn('size="sm"', attrs, rel)


class ReferenceScreenDefaultState(TestCase):
    """도서별 수불원장(Sobo31, /inventory/ledger) — 목업의 기본 상태."""

    def test_ledger_default_state(self) -> None:
        src = _read("app/(app)/inventory/ledger/page.tsx")
        self.assertIn('title="도서별수불원장"', src)
        self.assertIn("<EmptyHint>거래일자와 도서명으로 검색하세요</EmptyHint>", src)
        # 조회 전엔 분할 영역(상단 표·하단 상세) 전체를 숨김 — 캔버스에 안내문 하나만
        self.assertIn("<SplitListPanes", src)
        self.assertIn('storageKey="inventory.ledger"', src)
        # 2단 분할(사용자 요청 2026-08-25 14:29) — 일자 미선택(하단 안내문)일 땐 분할 off
        self.assertIn("disabled={selDate === null || showAll}", src)  # DEC-203 전체 보기면 분할 off
        # DEC-203/212 — 표는 프레임 없이, 공용 DataGrid 가 분할 칸 채움·높이 상한을 담당
        self.assertNotIn("rounded-2xl border border-border bg-card shadow-sm", src)
        self.assertIn("<DataGrid<DayGridRow>", src)
        self.assertNotIn("max-h-[46vh]", src)
        self.assertNotIn("max-h-[38vh]", src)


class RemainingFilterCardsMerged(TestCase):
    """DEC-213 (2026-08-26 09:50) — 띠 아래에 따로 남아 있던 조회 필터 카드 11개 화면을 띠로 병합.

    사용자: "레이아웃을 신규 적용된 다른 화면의 상단 레이아웃처럼 통합해서 정리해" (입고처관리 스크린샷).
    등록 폼·관리자 설정 패널은 필터가 아니라 제외.
    """

    PAGES = (
        "inbound/receipts", "master/author", "master/book", "master/discount", "master/etc-customer",
        "master/inbound-vendor", "outbound/orders", "settlement/payment-slip", "settlement/tax-invoice",
        "settlement/billing", "transactions/sales-statement",
    )

    def test_filter_lives_inside_band(self) -> None:
        for rel in self.PAGES:
            src = (APP / rel / "page.tsx").read_text(encoding="utf-8")
            i = src.index("<PageHeader")
            j = src.find("</PageHeader>", i)
            self.assertNotEqual(j, -1, f"{rel}: PageHeader 에 children(필터) 없음")
            band = src[i:j]
            self.assertRegex(band, r"<(Label|Input|Select|DateFieldYMD|MasterLookupField|LocalComboField)\b", rel)
            self.assertNotIn("rounded-2xl border border-border bg-card", band, f"{rel}: 띠 안 카드 프레임")


class StatusScreenHeadBlock(TestCase):
    """DEC-214 (2026-08-26 10:14) — 공용 현황 화면(출고·입고·신간발행·반품·폐기·거래 현황) 상단 3블록 통합.

    제목 띠 / 뷰 탭 / 필터 카드 → 필터는 띠 안(contents 래퍼로 Enter 스코프·legacy id 보존),
    뷰 전환(상세/요약/목록)은 화면 최하단 sticky 바.
    """

    def test_filter_panel_inside_band_and_view_tabs_at_bottom(self) -> None:
        src = (FRONT / "components" / "transactions" / "transaction-status-screen.tsx").read_text(encoding="utf-8")
        i = src.index("<PageHeader")
        j = src.index("</PageHeader>", i)
        band = src[i:j]
        self.assertIn('data-legacy-id="Sobo24.SearchPanel"', band)
        self.assertIn("data-enter-scope", band)
        self.assertIn("onKeyDown={onFilterKeyDown}", band)
        self.assertIn('className="contents"', band)
        self.assertNotIn("rounded-2xl border border-border bg-card", band)
        # 뷰 탭은 띠 뒤(최하단 바)에만
        k = src.index('aria-label="화면 보기"')
        self.assertGreater(k, j)
        bar = src[k - 200 : k + 900]
        self.assertIn("sticky bottom-0", bar)
        self.assertIn("mt-auto", bar)
        self.assertIn("Sobo24_status.tab.${v}", bar)
        self.assertIn("min-h-full", src, "루트가 뷰포트 높이를 채워야 mt-auto 로 바가 바닥에 붙는다")


class SpecialScreenLayout(TestCase):
    """DEC-215 (2026-08-26 10:27) — 특별관리(Sobo16)를 목업 결로: 띠(관리자 필터 포함) + 2단 분할 + 섹션 헤더 +
    프레임 없는 표. 패널 카드 프레임·설명 문단 제거, 검색·조회·컬럼은 섹션 헤더 액션."""

    def test_special_page_mockup_layout(self) -> None:
        src = (APP / "master" / "special" / "page.tsx").read_text(encoding="utf-8")
        i = src.index("<PageHeader")
        j = src.index("</PageHeader>", i)
        self.assertIn('data-legacy-id="Sobo16.Edit107"', src[i:j], "관리자 출판사 필터는 띠 안")
        self.assertIn('storageKey="master.special"', src)
        self.assertEqual(src.count("<SectionHeader"), 1, "AxisPane 공용 렌더 1곳(거래처·도서 두 축이 재사용)")
        self.assertNotIn("rounded-2xl border border-border bg-card p-4 shadow-sm", src)
        self.assertIn("fillHeight", src)
        # 검색·조회·컬럼이 섹션 헤더 액션에 함께 있다
        k = src.index("<SectionHeader")
        block = src[k : src.index("/>", src.index("<GridColumnSettings", k))]
        self.assertIn("<MasterLookupField", block)
        self.assertIn("조회", block)


class NoTrappedBand(TestCase):
    """DEC-216 (2026-08-26 10:30) — 띠가 `flex … justify-between` 래퍼 행에 갇혀 제목만큼만 흰 상자로
    보이던 20개 화면 해제 + 등록 폼(신규 입고 접수·신규 출고 주문·거래 명세서 신규)의 헤더 입력을 띠 안으로."""

    WRAPPER = re.compile(r'^<div className="flex[^"]*(justify-between|items-center|items-start)[^"]*">$')

    def test_page_header_is_not_sole_child_of_a_flex_row(self) -> None:
        trapped = []
        for p in _app_pages():
            src = p.read_text(encoding="utf-8")
            i = src.find("<PageHeader")
            if i == -1:
                continue
            prev = src[:i].rstrip().split("\n")[-1].strip()
            if self.WRAPPER.match(prev):
                trapped.append(str(p.relative_to(APP)))
        self.assertEqual(trapped, [], trapped)

    def test_slip_form_header_fields_inside_band(self) -> None:
        for rel in ("inbound/receipts/new", "outbound/orders/new", "transactions/sales-statement/new"):
            src = (APP / rel / "page.tsx").read_text(encoding="utf-8")
            i = src.index("<PageHeader")
            j = src.index("</PageHeader>", i)
            band = src[i:j]
            self.assertIn("data-enter-scope", band, rel)  # 헤더 카드의 Enter 스코프가 띠 안 contents 래퍼로
            self.assertIn("<DateFieldYMD", band, rel)
            self.assertNotIn("rounded-2xl border border-border bg-card", band, rel)


class EveryContentScreenHasBand(TestCase):
    """DEC-217 (2026-08-26 10:40) — "모든 화면 제목 영역을 목업에 맞게, 수정 안 된 화면만".

    내용이 있는 (app) 화면은 전부 `<PageHeader`(또는 그 위임 `PortalScreenTitle`)를 가진다.
    예외 = 리다이렉트/래퍼(공용 화면 컴포넌트를 렌더)/워크스페이스/인쇄 라우트.
    """

    WRAPPERS = {
        "admin", "dashboard", "dashboard/distributor", "dashboard/iot", "dashboard/pub", "dashboard/super",
        "dashboard/t3", "delivery/management", "master/discount/[type]", "returns/scrap/status", "returns/status",
        "transactions/inbound-status", "transactions/new-release", "transactions/outbound-status", "workspace",
    }

    def test_all_pages_have_band(self) -> None:
        missing = []
        for p in _app_pages():
            rel = str(p.relative_to(APP)).replace("/page.tsx", "")
            if rel in self.WRAPPERS:
                continue
            src = p.read_text(encoding="utf-8")
            if "<PageHeader" not in src and "<PortalScreenTitle" not in src:
                missing.append(rel)
        self.assertEqual(missing, [], missing)


if __name__ == "__main__":
    main()


class NoPaddedRootAroundBand(TestCase):
    """DEC-226 — 띠 화면의 루트 래퍼에 좌우/상단 패딩이 있으면 띠가 가장자리에 못 붙는다(회색 여백)."""

    def test_no_root_padding(self) -> None:
        import re
        bad: list[str] = []
        for f in sorted((FRONT / "app" / "(app)").glob("**/page.tsx")):
            src = f.read_text(encoding="utf-8")
            if "<PageHeader" not in src:
                continue
            m = re.search(r"\n  return \(\n\s*<(div|section|main)\b([^>]*)>", src)
            if not m:
                continue
            cm = re.search(r'className="([^"]*)"', m.group(2))
            if not cm:
                continue
            pads = [t for t in cm.group(1).split() if re.fullmatch(r"p[xytlr]?-(\d+|\[.*\])", t)]
            if pads:
                bad.append(f"{f.relative_to(FRONT)}: {pads}")
        self.assertEqual(bad, [], "루트 좌우/상단 패딩 제거 — pb-* 만 허용")


class BandPopoversExempt(TestCase):
    """DEC-233 — 띠 안에서 열리는 팝오버(컬럼 설정)는 인라인 라벨 규칙에서 제외돼 세로 목록을 유지한다."""

    def test_css_and_popover_marker(self) -> None:
        css = (FRONT / "app" / "globals.css").read_text(encoding="utf-8")
        self.assertEqual(css.count(':not(:is([data-band-exempt], [role="dialog"]) *)'), 5, "4개 셀렉터 + margin 규칙")
        pop = (FRONT / "components" / "data-grid" / "grid-column-settings.tsx").read_text(encoding="utf-8")
        self.assertIn('data-band-exempt="" data-slot="grid-column-settings"', pop)
        # 엑셀 저장 필드 선택 팝오버(거래처·입고처)도 동일 (2026-08-28 18:20 지적)
        for rel in ("master/customer", "master/inbound-vendor"):
            src = (FRONT / "app" / "(app)" / rel / "page.tsx").read_text(encoding="utf-8")
            self.assertIn('data-band-exempt="" role="dialog" aria-label="저장할 필드 선택"', src, rel)

