"""재고금액(Sobo34_1 = 재고 및 재고금액) 신설 회귀.

요청(2026-08-23): "원장관리-재고현황 메뉴 다음에 재고금액 메뉴를 신설해라.
재고현황 화면과 거의 동일한데 수량보다는 금액 관점으로 정보를 제공한다."

정본
----
출판 빌드 `한국도서유통/출판/MySQL/Subu34_1.pas` Button102Click
(레거시 메뉴 「재고원장 > 재고 및 재고금액」 = `한국도서유통/유통/Chul.dfm` Menu304_1).
분석 원문: `analysis/layout_mappings/Sobo34_1_stock_value.md`.

- 조회축은 기간이 아니라 **거래일자 1일** — L369~370 `Gdate >= Edit101 and Gdate <= Edit101`.
- 마감 산식(L1189~1213):
    GOSUM(재고금액)    = GSQUT(정가) × GSUMY(정품재고) × (Edit109/100)
    GBSUM(반품 재고금액) = GSQUT(정가) × GSSUM(반품재고) × (Edit109/100)
    CheckBox3(반품재고 제로) → GSSUM := 0, GBSUM := 0   (금액 산출 **후** 덮어쓰기)
    GJQUT(재고합계)    = GSUMY + GSSUM
    GJSUM(금액합계)    = GOSUM + GBSUM
- 수량 축은 Sobo34(재고현황)와 같은 코드라 `get_stock_ledger` 를 재사용한다 —
  DEC-138/182/183 검증 자산 승계. 본 테스트는 그 위임과 금액 파생을 고정한다.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from unittest import TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
sys.path.insert(0, str(BACKEND))

import app.services.inventory_service as inv  # noqa: E402

FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"


def _run(coro):
    return asyncio.run(coro)


# get_stock_ledger 가 돌려주는 모양(수량 축) — 이 위에 금액만 얹는 게 Sobo34_1 이다.
BASE = {
    "by_book": [
        {"class_code": "C1", "bcode": "B1", "gname": "도서1", "gdang": 10000,
         "gsumy": 120, "gssum": 30},
        {"class_code": "C1", "bcode": "B2", "gname": "도서2", "gdang": 8000,
         "gsumy": 50, "gssum": 0},
        {"class_code": "C2", "bcode": "B3", "gname": "도서3", "gdang": 5000,
         "gsumy": -4, "gssum": 20},
    ],
    "by_class": [
        {"class_code": "C1", "gname": "분류하나"},
        {"class_code": "C2", "gname": "분류둘"},
    ],
    "totals": {},
    "opening_asof": "2026.08.22",
}


def _call(**kw):
    """`get_stock_ledger` 를 BASE 로 고정하고 재고금액만 계산시킨다."""
    captured: dict = {}

    async def fake_ledger(**kwargs):
        captured.update(kwargs)
        return {k: [dict(r) for r in v] if isinstance(v, list) else v
                for k, v in BASE.items()}

    params = {"server_id": "remote_153", "hcode": "5019", "bcode": None,
              "date": "2026-08-23", "scope": "ALL"}
    params.update(kw)
    with patch.object(inv, "get_stock_ledger", new=AsyncMock(side_effect=fake_ledger)):
        out = _run(inv.get_stock_value_ledger(**params))
    return out, captured


class DelegationTests(TestCase):
    """§조회축 — 거래일자 1일이 시작일=기준일로 위임된다."""

    def test_single_trade_date_becomes_from_and_to(self) -> None:
        _, cap = _call(date="2026-08-23")
        self.assertEqual(cap["date_from"], "2026-08-23")
        self.assertEqual(cap["date_to"], "2026-08-23",
                         "Subu34_1 은 Gdate >= Edit101 and Gdate <= Edit101 (1일)")

    def test_filters_are_passed_through(self) -> None:
        _, cap = _call(hcode="5019", bcode="도서2", scope="A")
        self.assertEqual(cap["hcode"], "5019")
        self.assertEqual(cap["bcode"], "도서2")
        self.assertEqual(cap["scope"], "A")

    def test_asof_echoes_normalized_trade_date(self) -> None:
        out, _ = _call(date="2026-08-23")
        self.assertEqual(out["asof"], "2026.08.23")


class AmountFormulaTests(TestCase):
    """§마감 산식 — Subu34_1.pas L1189~1213."""

    def test_amount_is_price_times_qty_at_default_rate(self) -> None:
        out, _ = _call()
        b1 = next(r for r in out["by_book"] if r["bcode"] == "B1")
        self.assertEqual(b1["stock_qty"], 120)
        self.assertEqual(b1["stock_amt"], 10000 * 120, "GOSUM = 정가 × 정품재고 × 100%")
        self.assertEqual(b1["return_qty"], 30)
        self.assertEqual(b1["return_amt"], 10000 * 30, "GBSUM = 정가 × 반품재고 × 100%")

    def test_totals_are_qty_and_amount_sums(self) -> None:
        out, _ = _call()
        b1 = next(r for r in out["by_book"] if r["bcode"] == "B1")
        self.assertEqual(b1["total_qty"], 150, "GJQUT = GSUMY + GSSUM")
        self.assertEqual(b1["total_amt"], 10000 * 150, "GJSUM = GOSUM + GBSUM")

    def test_rate_scales_amounts_only(self) -> None:
        """기준율(Edit109)은 금액에만 곱해지고 수량은 건드리지 않는다."""
        out, _ = _call(rate=80)
        b1 = next(r for r in out["by_book"] if r["bcode"] == "B1")
        self.assertEqual(b1["stock_qty"], 120, "수량은 기준율과 무관")
        self.assertAlmostEqual(b1["stock_amt"], 10000 * 120 * 0.8)
        self.assertAlmostEqual(b1["return_amt"], 10000 * 30 * 0.8)
        self.assertAlmostEqual(b1["total_amt"], 10000 * 150 * 0.8)

    def test_negative_stock_yields_negative_amount(self) -> None:
        """음수 재고는 그대로 음수 금액 — 레거시도 부호를 죽이지 않는다."""
        out, _ = _call()
        b3 = next(r for r in out["by_book"] if r["bcode"] == "B3")
        self.assertEqual(b3["stock_amt"], 5000 * -4)

    def test_zero_return_blanks_return_qty_and_amount(self) -> None:
        """CheckBox3(반품재고 제로) — 반품 수량·금액을 0 으로 덮고 합계를 다시 만든다."""
        out, _ = _call(zero_return=True)
        b1 = next(r for r in out["by_book"] if r["bcode"] == "B1")
        self.assertEqual(b1["return_qty"], 0)
        self.assertEqual(b1["return_amt"], 0)
        self.assertEqual(b1["stock_qty"], 120, "정품재고는 영향 없음")
        self.assertEqual(b1["total_qty"], 120, "재고합계 = 정품재고만")
        self.assertEqual(b1["total_amt"], 10000 * 120)


class ClassRollupTests(TestCase):
    """§분류 롤업 — mSqry(L1219~1252)."""

    def test_class_sums_member_books(self) -> None:
        out, _ = _call()
        by_class = {c["class_code"]: c for c in out["by_class"]}
        self.assertEqual(set(by_class), {"C1", "C2"})
        self.assertEqual(by_class["C1"]["gname"], "분류하나", "이름은 G4_Gbun 해석값 재사용")
        self.assertEqual(by_class["C1"]["stock_qty"], 170, "B1 120 + B2 50")
        self.assertEqual(by_class["C1"]["stock_amt"], 10000 * 120 + 8000 * 50)
        self.assertEqual(by_class["C1"]["return_qty"], 30)
        self.assertEqual(by_class["C1"]["total_qty"], 200)

    def test_class_price_column_stays_blank(self) -> None:
        """레거시 상단 그리드는 Gsqut(정가)를 누적하지 않는다 — 임의 합산 금지."""
        out, _ = _call()
        for c in out["by_class"]:
            self.assertIsNone(c["gdang"], "분류 행의 정가는 공란이어야 한다")

    def test_class_total_equals_sum_of_its_books(self) -> None:
        """하단 「합계」(선택 분류 도서 합) = 상단 그 분류 행 — DEC-182 정합."""
        out, _ = _call()
        by_class = {c["class_code"]: c for c in out["by_class"]}
        for cc, klass in by_class.items():
            books = [r for r in out["by_book"] if r["class_code"] == cc]
            for k in ("stock_qty", "stock_amt", "return_qty",
                      "return_amt", "total_qty", "total_amt"):
                self.assertAlmostEqual(klass[k], sum(b[k] for b in books), msg=f"{cc}.{k}")

    def test_grand_totals_cover_the_six_footer_columns(self) -> None:
        """dfm Footer.ValueType=fvtSum 인 6컬럼만 합계 — 정가는 대상 아님."""
        out, _ = _call()
        self.assertEqual(
            set(out["totals"]),
            {"stock_qty", "stock_amt", "return_qty", "return_amt", "total_qty", "total_amt"})
        self.assertNotIn("gdang", out["totals"])
        self.assertEqual(out["totals"]["stock_qty"], 120 + 50 - 4)
        self.assertEqual(out["totals"]["total_amt"],
                         sum(r["total_amt"] for r in out["by_book"]))


class RouteWiringTests(TestCase):
    def test_route_is_registered(self) -> None:
        from app.routers import inventory as router_mod  # noqa: PLC0415

        paths = {r.path for r in router_mod.router.routes}
        self.assertIn("/api/v1/inventory/stock-value", paths)

    def test_route_is_in_db_smoke_matrix(self) -> None:
        """새 라우터 GET 은 probe 매트릭스에 등록한다(CLAUDE.md 규약)."""
        src = (ROOT / "debug" / "probe_backend_all_servers.py").read_text(encoding="utf-8")
        self.assertIn("inventory/stock-value", src)


class SidebarAndPageTests(TestCase):
    """§DEC-028 — 사이드바 위치 + dfm 위젯 id 부착."""

    def test_menu_sits_right_after_stock_status(self) -> None:
        src = (FRONT / "lib" / "form-registry.ts").read_text(encoding="utf-8")
        layout = src.split("INVENTORY_SIDEBAR_LAYOUT")[1].split("];")[0]
        order = [ln for ln in layout.splitlines() if "formId" in ln]
        idx_status = next(i for i, ln in enumerate(order) if "Sobo44_inv" in ln)
        idx_value = next(i for i, ln in enumerate(order) if "Sobo34_1_value" in ln)
        self.assertEqual(idx_value, idx_status + 1, "재고금액은 재고현황 바로 다음")

    def test_form_registry_entry(self) -> None:
        src = (FRONT / "lib" / "form-registry.ts").read_text(encoding="utf-8")
        self.assertIn('id: "Sobo34_1_value"', src)
        self.assertIn('folder: "Subu34_1"', src)
        self.assertIn('caption: "재고금액"', src)
        self.assertIn('route: "/inventory/value"', src)

    def test_page_carries_dfm_widget_ids(self) -> None:
        page = (FRONT / "app" / "(app)" / "inventory" / "value" / "page.tsx").read_text(
            encoding="utf-8")
        for wid in ("Sobo34_1.Edit101", "Sobo34_1.Edit103", "Sobo34_1.Edit109",
                    "Sobo34_1.Panel102", "Sobo34_1.CheckBox3", "Sobo34_1.dxButton1",
                    "Sobo34_1.DBGrid101", "Sobo34_1.DBGrid201"):
            self.assertIn(wid, page, f"dfm 위젯 id 누락: {wid}")

    def test_page_declares_all_nine_grid_columns(self) -> None:
        """상·하단 9컬럼(dfm FieldName) 이 모두 화면에 있어야 한다."""
        page = (FRONT / "app" / "(app)" / "inventory" / "value" / "page.tsx").read_text(
            encoding="utf-8")
        for label in ("분류코드", "분류명", "도서코드", "도서명", "정가",
                      "정품재고", "재고금액", "반품재고", "재고합계", "금액합계"):
            self.assertIn(label, page, f"컬럼 라벨 누락: {label}")
        for field in ("GSUMY", "GOSUM", "GSSUM", "GBSUM", "GJQUT", "GJSUM"):
            self.assertIn(field, page, f"dfm FieldName legacyId 누락: {field}")

    def test_mapping_note_exists(self) -> None:
        note = ROOT / "analysis" / "layout_mappings" / "Sobo34_1_stock_value.md"
        self.assertTrue(note.exists(), "DEC-028 레이아웃 매핑 노트 필수")


if __name__ == "__main__":
    main()
