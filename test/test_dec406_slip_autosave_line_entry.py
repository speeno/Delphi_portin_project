"""DEC-406 — 출고 · 입고 · 반품 · 폐기 접수: 줄 단위 자동저장(레거시 BeforePost 동등) (교문사 2026-10-15).

요청: 「출고접수, 입고접수 등 명세서 입력하는 것에 대해 항상 "저장"이 있습니다. 자동저장이 안 되는 거죠. 입출금전표는
입력하는 것 그대로 저장이 되어 있네요. 이렇게 자동저장되는 것을 출고접수 · 입고접수 · 반품접수 · 폐기접수에도 반영할 수
있나요? 위러스솔루션은 입출금전표처럼 자동저장되고 있습니다.」

레거시 정본 — Subu21(거래명세서) · Subu22(입고명세서) · Subu23(반품명세서): 그리드 줄을 넘기면 `nSqry.Append` →
`Base10.T2_Sub11/21/31BeforePost` 가 그 줄을 바로 `INSERT INTO S1_Ssub`. 줄 저장 버튼이 없다(Subu21 Button801 은 비고 저장).

웹 구현
- `lib/slip-autosave.ts` — 순수 스케줄러: 저장 대상 줄(도서 확정 · 수량 있음) 스냅샷이 바뀌면 debounce 뒤 첫 줄은 create(POST),
  이후는 update(PUT 원하는 상태 전체). 직렬 · 같은 내용 재전송 없음 · 실패 시 같은 내용 재전송 없음(변경/retry) ·
  헤더 식별자 변경 = 앞 전표 마감(대기분 먼저 저장) 후 화면이 줄을 비울 때까지 새 줄 무시 · 줄 전부 삭제 = 전표 소멸.
- 반품 · 폐기 PUT 은 idnum diff 라 자동저장에 못 쓴다 → 서비스 `replace_return_lines`(Bcode 기준 desired-state, 축은 기존 줄에서
  베낌, 하드 DELETE) + 라우터 `desiredLines` 분기.
- 네 화면: `useSlipAutosave` · 상태 표시 · 「저장」→「새 전표」 · 입고처 확정 코드(`vendorCode`).

런타임 없이 소스 + node 하네스 + 서비스 모킹으로 본다(실화면 검증은 DEC-406 본문). 사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main, skipUnless
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
FE = FRONTEND / "src"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from app.models.outbound import OrderCreateResponse  # noqa: E402
from app.models.returns import ReturnCreateResponse  # noqa: E402
from app.services import returns_service as svc  # noqa: E402

AUTOSAVE_TS = FE / "lib" / "slip-autosave.ts"
HOOK = FE / "components" / "transactions" / "use-slip-autosave.ts"
STATUS = FE / "components" / "transactions" / "slip-autosave-status.tsx"
LAYOUT = FE / "components" / "transactions" / "slip-entry-layout.tsx"
OUT_PAGE = FE / "app" / "(app)" / "outbound" / "orders" / "new" / "page.tsx"
IN_PAGE = FE / "app" / "(app)" / "inbound" / "receipts" / "new" / "page.tsx"
RT_PAGE = FE / "app" / "(app)" / "returns" / "receipts" / "new" / "page.tsx"
SC_PAGE = FE / "app" / "(app)" / "returns" / "scrap" / "new" / "page.tsx"
RETURNS_API = FE / "lib" / "returns-api.ts"
ROUTER = BACKEND / "app" / "routers" / "returns.py"
SERVICE = BACKEND / "app" / "services" / "returns_service.py"


def _read(p: Path) -> str:
    return p.read_text(encoding="utf-8").replace("\r\n", "\n")


# ═══════════════════════════════════════════════════════════════════════════════
# §1 정적 — 네 화면 · 골격 · API 클라이언트 · 라우터
# ═══════════════════════════════════════════════════════════════════════════════
class StaticWiring(TestCase):
    PAGES = {"outbound": OUT_PAGE, "inbound": IN_PAGE, "returns": RT_PAGE, "scrap": SC_PAGE}

    def test_all_four_entry_pages_autosave(self) -> None:
        for name, p in self.PAGES.items():
            src = _read(p)
            self.assertIn('from "@/components/transactions/use-slip-autosave"', src, name)
            self.assertIn("useSlipAutosave<", src, name)
            self.assertIn("<SlipAutosaveStatus", src, name)
            self.assertIn("isSavableLine(", src, name)
            self.assertIn("countUnsavableLines(", src, name)
            self.assertIn("isCompleteYmd(gdate)", src, f"{name}: 일자가 완성값일 때만 저장")
            self.assertIn('label: "새 전표",', src, f"{name}: 저장 버튼은 「새 전표」")
            self.assertIn('icon: "new",', src, name)
            self.assertIn("status={", src, name)
            self.assertIn("await autosave.finish();", src, f"{name}: 「새 전표」 = 대기분 저장 후 마감")
            self.assertIn('if (autosave.state.status === "error")', src, f"{name}: 저장 실패 줄이 있으면 마감 금지")
            self.assertIn("onFinished: (f) => {", src, f"{name}: 헤더 변경 마감 처리")
            self.assertIn("product_name", src, f"{name}: 미확정 도서(도서명 없음)는 마감 전 검증")

    def test_payload_mappers_strip_display_fields(self) -> None:
        for name, p, fn in (
            ("outbound", OUT_PAGE, "function toOrderLineInput("),
            ("inbound", IN_PAGE, "function toReceiptLineInput("),
            ("returns", RT_PAGE, "function toReturnLineInput("),
            ("scrap", SC_PAGE, "function toScrapLineInput("),
        ):
            src = _read(p)
            i = src.index(fn)
            body = src[i : src.index("\n}\n", i)]
            self.assertNotIn("product_name", body, f"{name}: 표시 전용 필드는 저장 지문에 넣지 않는다")
            self.assertNotIn("isbn", body, name)

    def test_outbound_specifics(self) -> None:
        src = _read(OUT_PAGE)
        # DEC-404 물음은 자동저장된(대기) 전표가 없을 때만.
        i = src.index("function noteCustomerConfirmed(")
        body = src[i : src.index("\n  }\n", i)]
        self.assertIn('if (a.key || a.status === "pending" || a.status === "saving" || a.status === "finishing") return;', body)
        # 응답 키에 지점이 없어 PUT 스코프용으로 보존.
        self.assertIn("return { key: { ...res.order_key, gjisa: h.gjisa }, idnum: res.idnum ?? res.order_key.idnum ?? null };", src)
        self.assertIn("const autosaveHeaderId = `${gdate}|${companyHcode}|${customerCode}|${gjisa.trim()}`;", src)
        self.assertIn("await outboundApi.update(k.key, serverId, ls);", src)
        # 전표번호 칸은 채번되면 바로 보인다.
        self.assertIn('value={formatIdnumDisplay(autosave.state.key?.idnum) || autosave.state.key?.key.jubun || ""}', src)
        self.assertIn("readOnly={saving}", src)
        self.assertNotIn("orderLines: submitLines.map(", src, "한 번에 POST 하는 종전 저장 경로 제거")
        # DEC-297 가드 호환 — 확정 코드만 저장에 쓴다.
        self.assertIn("const customer = customerCode;", src)

    def test_inbound_confirmed_vendor_code(self) -> None:
        src = _read(IN_PAGE)
        self.assertIn('const [vendorCode, setVendorCode] = useState("");', src)
        self.assertIn("if (next.trim() !== vendorCode) {", src, "입력이 확정 코드와 달라지면 확정 해제")
        self.assertIn("setVendorCode(selection.code.trim());", src)
        self.assertIn('setVendorCode((v.gcode ?? "").trim());', src)
        self.assertIn("const autosaveReady = !!serverId && isCompleteYmd(gdate) && !!hcode.trim() && !!vendorCode;", src)
        self.assertIn("receiptHeader: { gdate: h.gdate, hcode: h.hcode, gcode: h.gcode, gjisa: \"\" },", src)
        # 줄 전부 삭제는 메모까지 지우는 DELETE.
        self.assertIn("await inboundApi.delete(k.key, serverId);", src)
        self.assertIn("receiptMemo: memoPayload(h.memo)", src, "메모도 자동저장(헤더 지문에 포함)")
        self.assertIn("readOnly={saving}", src)

    def test_returns_and_scrap_use_replace_lines(self) -> None:
        rt = _read(RT_PAGE)
        sc = _read(SC_PAGE)
        for name, src in (("returns", rt), ("scrap", sc)):
            self.assertIn("returnsApi.replaceLines({ serverId, returnKey: k.keyStr, lines: ls })", src, name)
            self.assertIn("serializeReturnKey(res.return_key)", src, name)
        # 반품: 저장 후 상세 이동 대신 배너 + 이어서 입력.
        self.assertNotIn("useRouter", rt)
        self.assertNotIn("router.push", rt)
        self.assertIn("saved={", rt)
        self.assertIn('linkLabel: "방금 저장한 반품 보기",', rt)
        # DEC-281 가드 호환 — 회사 코드는 프로필에 따라 로그인 스코프.
        self.assertIn("returnHeader: { gdate, hcode: company", rt)
        self.assertIn('const RETURN_SAVABLE: SavableRule = { qty: "nonzero", requirePubun: true };', rt)
        # 폐기: 비율 · 금액 0 고정(DEC-190), 거래처 미확정이면 대기.
        self.assertIn('const SCRAP_SAVABLE: SavableRule = { qty: "nonzero" };', sc)
        self.assertIn("const customerUnconfirmed = !!gcode.trim() && !customerCode;", sc)
        self.assertIn("!customerUnconfirmed;", sc)

    def test_layout_status_slot_and_new_icon(self) -> None:
        src = _read(LAYOUT)
        self.assertIn("status?: ReactNode;", src)
        i = src.index('className="ml-auto flex flex-wrap items-center gap-2"')
        block = src[i : i + 700]
        self.assertLess(block.index("{status}"), block.index("{extraActions}"), "상태 표시는 버튼 왼쪽")
        self.assertIn('save.icon === "new" ? <FilePlus2', src)
        self.assertIn("save.onClick", src)  # DEC-264 가드 호환

    def test_hook_acks_after_page_handles_finish(self) -> None:
        src = _read(HOOK)
        i = src.index("if (!state.finished) return;")
        block = src[i : i + 160]
        self.assertLess(block.index("onFinishedRef.current(state.finished);"), block.index("ctrl.ackFinished();"))
        self.assertIn('window.addEventListener("beforeunload", handler);', src)
        self.assertIn("formatError: formatApiError,", src)

    def test_status_chip_states(self) -> None:
        src = _read(STATUS)
        for s in ('case "saving":', 'case "pending":', 'case "finishing":', 'case "saved":', 'case "error":'):
            self.assertIn(s, src)
        self.assertIn("자동저장됨", src)
        self.assertIn("다시 시도", src)
        self.assertIn("미확정 {unsavable}줄", src)

    def test_returns_api_replace_lines_body(self) -> None:
        src = _read(RETURNS_API)
        i = src.index("replaceLines: (params:")
        block = src[i : i + 600]
        self.assertIn("{ desiredLines: params.lines }", block)
        self.assertIn("api.put<", block)

    def test_router_branches_on_desired_lines(self) -> None:
        src = _read(ROUTER)
        i = src.index("async def put_return_lines(")
        body = src[i : src.index("\n\n\n", i)]
        self.assertIn('desired = body.get("desiredLines", body.get("desired_lines"))', body)
        self.assertIn("returns_service.replace_return_lines(", body)
        self.assertIn("returns_service.update_return_lines(", body, "종전 idnum diff 경로 유지")

    def test_service_sql_keeps_hcode_scope(self) -> None:
        src = _read(SERVICE)
        for const in ("SQL_INSERT_LINE_LIKE_SLIP", "SQL_DELETE_LINE_HARD"):
            i = src.index(f"{const} = (")
            block = src[i : src.index("\n)\n", i)]
            self.assertIn("Hcode", block, const)
        self.assertIn("async def replace_return_lines(", src)

    def test_create_responses_carry_idnum(self) -> None:
        self.assertEqual(OrderCreateResponse.model_validate({
            "order_key": {"gdate": "2026.10.15", "hcode": "5019", "jubun": "1"},
            "idnum": 12, "lines": 1, "qty": 1, "amount": 0, "created_at": "x",
        }).idnum, 12)
        self.assertIsNone(ReturnCreateResponse.model_validate({
            "return_key": {"gdate": "2026.10.15", "hcode": "5019", "jubun": "1"},
            "lines": 1, "qty": -1, "amount": 0, "created_at": "x",
        }).idnum)


# ═══════════════════════════════════════════════════════════════════════════════
# §2 서비스 — replace_return_lines (desired-state, 축 베낌, 하드 DELETE)
# ═══════════════════════════════════════════════════════════════════════════════
def _row(**over: Any) -> dict[str, Any]:
    base = {
        "Gdate": "2026.10.15", "Hcode": "5019", "Jubun": "4", "Gjisa": "", "Bcode": "3411", "Pubun": "정품",
        "Gsqut": -1, "Gdang": 30000, "Grat1": 85, "Gssum": -25500, "Gbigo": "", "Yesno": "1",
        "Gubun": "반품", "Ocode": "B", "Scode": "X", "Gcode": "00238",
    }
    base.update(over)
    return base


def _fake_query(existing: list[dict[str, Any]], idnum_rows: list[dict[str, Any]] | None = None):
    async def fake(server_id: str, sql: str, params: Any = None, *a: Any, **k: Any) -> list[dict[str, Any]]:
        if "MAX(Idnum+0)" in sql:
            return idnum_rows if idnum_rows is not None else [{"idnum": 12}]
        return existing
    return fake


class ReplaceReturnLines(IsolatedAsyncioTestCase):
    async def _run(self, existing, desired, *, cols=frozenset({"idnum", "gdate"}), idnum_rows=None):
        captured: list[tuple[str, tuple]] = []

        async def fake_tx(server_id: str, ops: list) -> list[int]:
            captured.extend(ops)
            return [1] * len(ops)

        with patch.object(svc, "execute_query", AsyncMock(side_effect=_fake_query(existing, idnum_rows))), \
             patch.object(svc, "execute_in_transaction", AsyncMock(side_effect=fake_tx)), \
             patch.object(svc, "s1_column_names", AsyncMock(return_value=set(cols))):
            result = await svc.replace_return_lines(
                server_id="remote_153", return_key_str="G|2026.10.15|5019|4", desired_lines=desired,
            )
        return result, captured

    async def test_insert_new_bcode_copies_slip_axis_and_idnum(self) -> None:
        result, ops = await self._run(
            [_row()],
            [{"bcode": "3411", "pubun": "정품", "gsqut": -1, "gdang": 30000, "grat1": 85},
             {"bcode": "3320", "pubun": "비품", "gsqut": 2, "gdang": 20000, "grat1": 85}],
        )
        self.assertEqual((result["inserted"], result["updated"], result["deleted"]), (1, 0, 0))
        self.assertEqual(result["idnum"], 12)
        self.assertEqual(result["total_lines"], 2)
        self.assertEqual(result["return_key"], {"gdate": "2026.10.15", "bdate": None, "hcode": "5019", "jubun": "4"})
        self.assertEqual(len(ops), 1)
        sql, params = ops[0]
        self.assertTrue(sql.startswith("INSERT INTO S1_Ssub"))
        self.assertEqual(sql.count("%s"), len(params), "자리 수 일치(DEC-380 재발 방지)")
        self.assertIn(", Idnum)", sql)
        self.assertEqual(params[-1], 12, "새 줄도 전표 공통 Idnum")
        # (Gdate, Hcode, Jubun, Gjisa, Pubun, Bcode, Gubun, Ocode, Scode, Gcode, Yesno, Gsqut, Gdang, Grat1, Gssum, Gbigo)
        self.assertEqual(params[:11], ("2026.10.15", "5019", "4", "", "비품", "3320", "반품", "B", "X", "00238", "1"))
        self.assertEqual(params[11:16], (-2, 20000, 85.0, -34000, ""), "음수 수량 · 서버 금액(DEC-301)")

    async def test_unchanged_line_is_not_rewritten(self) -> None:
        result, ops = await self._run([_row()], [{"bcode": "3411", "pubun": "정품", "gsqut": -1, "gdang": 30000, "grat1": 85}])
        self.assertEqual(ops, [])
        self.assertEqual((result["inserted"], result["updated"], result["deleted"]), (0, 0, 0))

    async def test_changed_qty_updates_in_place(self) -> None:
        result, ops = await self._run([_row()], [{"bcode": "3411", "pubun": "정품", "gsqut": 3, "gdang": 30000, "grat1": 85}])
        self.assertEqual((result["inserted"], result["updated"], result["deleted"]), (0, 1, 0))
        sql, params = ops[0]
        self.assertTrue(sql.startswith("UPDATE S1_Ssub"))
        self.assertEqual(params, ("정품", -3, 30000, 85.0, -76500, "", "2026.10.15", "5019", "4", "3411"))

    async def test_missing_bcode_is_hard_deleted_with_gcode_scope(self) -> None:
        result, ops = await self._run([_row(), _row(Bcode="3320", Gsqut=-2)], [{"bcode": "3411", "pubun": "정품", "gsqut": -1, "gdang": 30000, "grat1": 85}])
        self.assertEqual((result["inserted"], result["updated"], result["deleted"]), (0, 0, 1))
        sql, params = ops[0]
        self.assertTrue(sql.startswith("DELETE FROM S1_Ssub"))
        self.assertIn("Hcode=%s", sql)
        self.assertIn("Gcode=%s", sql)
        self.assertIn("Yesno<>'2'", sql, "상세 화면에서 소프트 취소된 줄은 건드리지 않는다")
        self.assertEqual(params, ("2026.10.15", "5019", "4", "00238", "3320"))

    async def test_empty_desired_deletes_everything(self) -> None:
        result, ops = await self._run([_row(), _row(Bcode="3320")], [])
        self.assertEqual(result["deleted"], 2)
        self.assertEqual(result["total_lines"], 0)
        self.assertTrue(all(q.startswith("DELETE") for q, _ in ops))

    async def test_scrap_slip_keeps_scrap_axis_and_zero_amounts(self) -> None:
        existing = [_row(Gubun="폐기", Scode="Z", Ocode="A", Gcode="APL2", Yesno="N", Grat1=0, Gssum=0, Pubun="정품")]
        result, ops = await self._run(existing, [
            {"bcode": "3411", "pubun": "정품", "gsqut": -1, "gdang": 30000, "grat1": 0},
            {"bcode": "3320", "pubun": "비품", "gsqut": 5, "gdang": 20000, "grat1": 85},  # 화면이 비율을 보내도 폐기는 0
        ])
        self.assertEqual((result["inserted"], result["updated"], result["deleted"]), (1, 0, 0))
        sql, params = ops[0]
        self.assertEqual(params[6:11], ("폐기", "A", "Z", "APL2", "N"))
        self.assertEqual(params[11:15], (-5, 20000, 0.0, 0))

    async def test_soft_cancelled_rows_are_ignored(self) -> None:
        with self.assertRaises(LookupError):
            await self._run([_row(Yesno="2")], [{"bcode": "3411", "gsqut": -1}])

    async def test_not_found_and_validation(self) -> None:
        with self.assertRaises(LookupError):
            await self._run([], [{"bcode": "3411", "gsqut": -1}])
        with self.assertRaises(ValueError):
            await self._run([_row()], [{"bcode": "", "gsqut": -1}])
        with self.assertRaises(ValueError):
            await self._run([_row()], [{"bcode": "3320", "gsqut": 0}])
        with self.assertRaises(ValueError):
            await svc.replace_return_lines(server_id="remote_153", return_key_str="X|bad", desired_lines=[])

    async def test_server_without_idnum_column(self) -> None:
        result, ops = await self._run([_row()], [{"bcode": "3320", "pubun": "정품", "gsqut": -1, "gdang": 1000, "grat1": 85}], cols=frozenset())
        self.assertIsNone(result["idnum"])
        self.assertEqual(len(ops), 2, "3411 삭제 + 3320 추가")
        ins = next(q for q, _ in ops if q.startswith("INSERT"))
        self.assertNotIn("Idnum", ins)


# ═══════════════════════════════════════════════════════════════════════════════
# §3 라우터 — PUT /returns/{key} desiredLines 분기
# ═══════════════════════════════════════════════════════════════════════════════
class PutDesiredLinesRoute(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        from fastapi.testclient import TestClient
        from app.main import app
        from app.routers.auth import get_current_user

        cls.app = app
        cls.dep = get_current_user
        cls.prev = app.dependency_overrides.get(get_current_user)
        app.dependency_overrides[get_current_user] = lambda: {"user_id": "hong01", "server_id": "remote_1", "role": "manager"}
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls) -> None:
        if cls.prev is None:
            cls.app.dependency_overrides.pop(cls.dep, None)
        else:
            cls.app.dependency_overrides[cls.dep] = cls.prev

    KEY = "G%7C2026.10.15%7C5019%7C4"

    def test_desired_lines_goes_to_replace(self) -> None:
        captured: dict[str, Any] = {}

        async def fake_replace(**kwargs):
            captured.update(kwargs)
            return {"return_key": {"gdate": "2026.10.15", "bdate": None, "hcode": "5019", "jubun": "4"},
                    "idnum": 12, "inserted": 1, "updated": 0, "deleted": 0, "total_lines": 2}

        with patch.object(svc, "replace_return_lines", side_effect=fake_replace), \
             patch.object(svc, "update_return_lines", side_effect=AssertionError("idnum diff 경로로 가면 안 된다")):
            res = self.client.put(
                f"/api/v1/returns/{self.KEY}?serverId=remote_1",
                json={"desiredLines": [{"bcode": "3411", "gsqut": -1}, {"bcode": "3320", "gsqut": 2}]},
            )
        self.assertEqual(res.status_code, 200, res.text)
        self.assertEqual(captured["return_key_str"], "G|2026.10.15|5019|4")
        self.assertEqual(len(captured["desired_lines"]), 2)
        self.assertEqual(res.json()["idnum"], 12)

    def test_legacy_lines_body_still_uses_idnum_diff(self) -> None:
        async def fake_update(**kwargs):
            return {"return_key": {"gdate": "2026.10.15", "bdate": None, "hcode": "5019", "jubun": "4"},
                    "inserted": 0, "updated": 1, "deleted": 0, "total_lines": 1, "total_qty": -1, "total_amount": 0}

        with patch.object(svc, "update_return_lines", side_effect=fake_update), \
             patch.object(svc, "replace_return_lines", side_effect=AssertionError("desiredLines 없이는 교체 모드 금지")):
            res = self.client.put(f"/api/v1/returns/{self.KEY}?serverId=remote_1", json={"lines": [{"idnum": 1, "bcode": "3411", "gsqut": -1}]})
        self.assertEqual(res.status_code, 200, res.text)

    def test_replace_not_found_is_404(self) -> None:
        async def fake_replace(**kwargs):  # noqa: ARG001
            raise LookupError("return not found")

        with patch.object(svc, "replace_return_lines", side_effect=fake_replace):
            res = self.client.put(f"/api/v1/returns/{self.KEY}?serverId=remote_1", json={"desiredLines": []})
        self.assertEqual(res.status_code, 404, res.text)


# ═══════════════════════════════════════════════════════════════════════════════
# §4 행동(node) — 순수 스케줄러
# ═══════════════════════════════════════════════════════════════════════════════
HARNESS_JS = r"""
const path = require("path");
const m = require(path.join(__dirname, "slip-autosave.js"));
const results = [];
function check(name, actual, expected) {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  results.push({ name, ok, actual, expected });
}
let clock = 0; const timers = new Map(); let tid = 0;
const setTimer = (fn, ms) => { const id = ++tid; timers.set(id, { fn, at: clock + ms }); return id; };
const clearTimer = (id) => { timers.delete(id); };
const tick = () => new Promise((r) => setImmediate(r));
async function settle() { for (let i = 0; i < 12; i++) await tick(); }
async function advance(ms) {
  const target = clock + ms;
  for (;;) {
    const due = [...timers.entries()].filter(([, t]) => t.at <= target).sort((a, b) => a[1].at - b[1].at);
    if (!due.length) break;
    const [id, t] = due[0]; timers.delete(id); clock = t.at; t.fn(); await settle();
  }
  clock = target; await settle();
}
function makeApi() {
  const api = {
    calls: [], failNext: null, slow: null, nextId: 0,
    create: (header, lines) => api._do("create", { header, lines }, () => ({ id: ++api.nextId })),
    update: (key, header, lines) => api._do("update", { key, header, lines }, () => undefined),
    async _do(kind, rec, result) {
      api.calls.push({ kind, ...rec });
      if (api.failNext) { const msg = api.failNext; api.failNext = null; throw new Error(msg); }
      if (api.slow) { const p = api.slow; api.slow = null; await p; }
      return result();
    },
    hold() { let release; api.slow = new Promise((r) => (release = r)); return release; },
  };
  return api;
}
function make(api) {
  const c = { state: null, ctrl: null };
  c.ctrl = m.createSlipAutosave({ create: api.create, update: api.update, onState: (s) => (c.state = s), debounceMs: 700, now: () => clock, setTimer, clearTimer });
  c.state = c.ctrl.getState();
  return c;
}
const HA = { gdate: "2026-10-15", hcode: "5019", customer: "00238" };
const HB = { gdate: "2026-10-15", hcode: "5019", customer: "00500" };
const snapA = (lines) => ({ ready: true, headerId: "A", header: HA, lines });
const snapB = (lines) => ({ ready: true, headerId: "B", header: HB, lines });
const L1 = { bcode: "3411", gsqut: 1 };
const L2 = { bcode: "3320", gsqut: 2 };
const kinds = (api) => api.calls.map((x) => x.kind);

(async () => {
  { // a. 초기 · 빈 스냅샷은 아무 것도 보내지 않는다
    const api = makeApi(); const c = make(api);
    check("a_initial_idle", c.state.status, "idle");
    c.ctrl.notify(snapA([])); await advance(1000);
    check("a_empty_no_call", api.calls.length, 0);
    check("a_empty_idle", c.state.status, "idle");
  }
  { const api = makeApi(); const c = make(api);
    // b. 첫 줄 → debounce 뒤 create
    c.ctrl.notify(snapA([L1]));
    check("b_pending", c.state.status, "pending");
    await advance(600); check("b_debounce_waits", api.calls.length, 0);
    await advance(100); check("b_create_called", kinds(api), ["create"]);
    check("b_create_header", api.calls[0].header, HA);
    check("b_create_lines", api.calls[0].lines, [L1]);
    check("b_saved", c.state.status, "saved"); check("b_key", c.state.key, { id: 1 }); check("b_saved_lines", c.state.savedLines, 1);
    // c. 같은 내용은 보내지 않는다
    c.ctrl.notify(snapA([L1])); await advance(1000);
    check("c_same_no_call", api.calls.length, 1); check("c_still_saved", c.state.status, "saved");
    // d. 둘째 줄 → update(전체)
    c.ctrl.notify(snapA([L1, L2])); await advance(700);
    check("d_update_called", kinds(api), ["create", "update"]);
    check("d_update_key", api.calls[1].key, { id: 1 }); check("d_update_lines", api.calls[1].lines, [L1, L2]);
    // e. 빠른 연속 수정은 마지막 내용 한 번
    c.ctrl.notify(snapA([L1, { ...L2, gsqut: 3 }])); await advance(300);
    c.ctrl.notify(snapA([L1, { ...L2, gsqut: 30 }])); await advance(300);
    check("e_not_yet", api.calls.length, 2);
    await advance(400);
    check("e_one_update", api.calls.length, 3); check("e_latest_lines", api.calls[2].lines[1].gsqut, 30);
    // f. 보내는 동안 바뀐 내용은 끝난 뒤 다시(직렬)
    const release = api.hold();
    c.ctrl.notify(snapA([L1, { ...L2, gsqut: 31 }])); await advance(700);
    check("f_saving", c.state.status, "saving"); check("f_first_sent", api.calls.length, 4);
    c.ctrl.notify(snapA([L1, { ...L2, gsqut: 32 }])); await advance(700);
    check("f_second_waits", api.calls.length, 4);
    release(); await settle(); await advance(0);
    check("f_second_sent_after", api.calls.length, 5); check("f_second_latest", api.calls[4].lines[1].gsqut, 32); check("f_saved", c.state.status, "saved");
    // g. 실패 → 같은 내용 재전송 없음 → 고치면 재시도
    api.failNext = "(422) 공급율 불일치";
    c.ctrl.notify(snapA([L1, { ...L2, gsqut: 40 }])); await advance(700);
    check("g_error", c.state.status, "error"); check("g_error_msg", c.state.error, "(422) 공급율 불일치"); check("g_calls", api.calls.length, 6);
    check("g_key_kept", c.state.key, { id: 1 });
    c.ctrl.notify(snapA([L1, { ...L2, gsqut: 40 }])); await advance(1000);
    check("g_same_not_resent", api.calls.length, 6); check("g_still_error", c.state.status, "error");
    c.ctrl.notify(snapA([L1, { ...L2, gsqut: 41 }])); await advance(700);
    check("g_changed_resent", api.calls.length, 7); check("g_saved_again", c.state.status, "saved");
    // h. retry()
    api.failNext = "네트워크";
    c.ctrl.notify(snapA([L1, { ...L2, gsqut: 42 }])); await advance(700);
    check("h_error", c.state.status, "error");
    c.ctrl.retry(); await settle();
    check("h_retry_sent", api.calls.length, 9); check("h_retry_saved", c.state.status, "saved");
    // i. 헤더 미확정(ready=false) → 대기분을 앞 헤더로 즉시 저장 · 전표 유지 · 같은 헤더 재확정이면 이어서
    c.ctrl.notify(snapA([L1, { ...L2, gsqut: 43 }])); await advance(100);
    check("i_pending", c.state.status, "pending");
    c.ctrl.notify({ ready: false, headerId: "", header: {}, lines: [L1, { ...L2, gsqut: 43 }] }); await settle();
    check("i_flushed_now", api.calls.length, 10); check("i_flushed_old_header", api.calls[9].header, HA); check("i_key_kept", c.state.key, { id: 1 });
    c.ctrl.notify(snapA([L1, { ...L2, gsqut: 43 }])); await advance(1000);
    check("i_resume_same_slip_no_call", api.calls.length, 10); check("i_saved", c.state.status, "saved");
    // j. 헤더 변경(전표 있음) → 마감 · finished → 화면이 줄을 비울 때까지 새 헤더 줄 무시 → 빈 스냅샷 → ack → 새 전표
    c.ctrl.notify(snapB([L1, { ...L2, gsqut: 43 }])); await settle();
    check("j_finishing", c.state.status, "finishing");
    check("j_finished_key", c.state.finished && c.state.finished.key, { id: 1 });
    check("j_finished_lines", c.state.finished && c.state.finished.lines, 2);
    check("j_no_create_for_B", api.calls.length, 10);
    check("j_key_cleared", c.state.key, null);
    c.ctrl.notify(snapB([L1])); await advance(1000);
    check("j_ignored_until_cleared", api.calls.length, 10);
    c.ctrl.notify(snapB([])); await settle();
    check("j_idle_after_clear", c.state.status, "idle"); check("j_finished_kept_until_ack", !!c.state.finished, true);
    c.ctrl.ackFinished(); check("j_acked", c.state.finished, null);
    c.ctrl.notify(snapB([L1])); await advance(700);
    check("j_new_slip_created", kinds(api).slice(-1), ["create"]); check("j_new_header", api.calls[10].header, HB); check("j_new_key", c.state.key, { id: 2 });
    // l. 줄 전부 삭제 → update([]) → 전표 소멸 → 다음 줄은 새 전표
    c.ctrl.notify(snapB([])); await advance(700);
    check("l_update_empty", api.calls[11].kind + ":" + api.calls[11].lines.length, "update:0"); check("l_key_dropped", c.state.key, null); check("l_idle", c.state.status, "idle");
    c.ctrl.notify(snapB([L2])); await advance(700);
    check("l_recreated", api.calls[12].kind, "create"); check("l_new_key", c.state.key, { id: 3 });
    // m. finish() — 대기분 저장 → 전표 비움
    c.ctrl.notify(snapB([L2, L1])); await advance(100);
    const r = await c.ctrl.finish();
    check("m_finish_ok", r.ok, true); check("m_finish_key", r.ok && r.finished && r.finished.key, { id: 3 }); check("m_finish_lines", r.ok && r.finished && r.finished.lines, 2);
    check("m_flushed", api.calls[13].kind + ":" + api.calls[13].lines.length, "update:2"); check("m_idle", c.state.status, "idle"); check("m_key_null", c.state.key, null); check("m_no_finished_flag", c.state.finished, null);
    const r2 = await c.ctrl.finish(); check("m_finish_nothing", r2, { ok: true, finished: null });
    // m3. finish 실패 → ok:false · 전표 · 오류 유지
    c.ctrl.notify(snapB([L1])); await advance(700); check("m3_created", c.state.key, { id: 4 });
    api.failNext = "서버 오류";
    c.ctrl.notify(snapB([L1, L2])); await advance(100);
    const r3 = await c.ctrl.finish();
    check("m3_finish_fail", r3, { ok: false, error: "서버 오류" }); check("m3_key_kept", c.state.key, { id: 4 }); check("m3_error_state", c.state.status, "error");
    c.ctrl.dispose();
  }
  { // k. 전표 없이 대기 중 헤더 변경 → 앞 헤더로 먼저 생성 → 마감
    const api = makeApi(); const c = make(api);
    c.ctrl.notify(snapA([L1])); await advance(100);
    c.ctrl.notify(snapB([L1])); await settle();
    check("k_created_old_header", kinds(api), ["create"]); check("k_old_header", api.calls[0].header, HA);
    check("k_finished_key", c.state.finished && c.state.finished.key, { id: 1 }); check("k_finishing", c.state.status, "finishing");
    c.ctrl.notify(snapB([])); await settle(); c.ctrl.ackFinished();
    check("k_idle", c.state.status, "idle"); check("k_no_extra_calls", api.calls.length, 1);
    c.ctrl.notify(snapA([])); await settle();
    check("k_header_only_change_no_finish", c.state.finished, null); check("k_header_only_idle", c.state.status, "idle");
  }
  // n. 판정 헬퍼
  check("n_savable_ok", m.isSavableLine({ bcode: "3411", product_name: "책", gsqut: 1 }, { qty: "positive" }), true);
  check("n_savable_no_name", m.isSavableLine({ bcode: "3411", product_name: "", gsqut: 1 }, { qty: "positive" }), false);
  check("n_savable_zero_qty", m.isSavableLine({ bcode: "3411", product_name: "책", gsqut: 0 }, { qty: "positive" }), false);
  check("n_savable_negative_positive_rule", m.isSavableLine({ bcode: "3411", product_name: "책", gsqut: -1 }, { qty: "positive" }), false);
  check("n_savable_negative_nonzero_rule", m.isSavableLine({ bcode: "3411", product_name: "책", gsqut: -1 }, { qty: "nonzero" }), true);
  check("n_savable_pubun_required", m.isSavableLine({ bcode: "3411", product_name: "책", gsqut: -1, pubun: "" }, { qty: "nonzero", requirePubun: true }), false);
  check("n_savable_pubun_ok", m.isSavableLine({ bcode: "3411", product_name: "책", gsqut: -1, pubun: "정품" }, { qty: "nonzero", requirePubun: true }), true);
  check("n_unsavable_count", m.countUnsavableLines([{ bcode: "", gsqut: 0 }, { bcode: "1", product_name: "", gsqut: 1 }, { bcode: "2", product_name: "x", gsqut: 0 }, { bcode: "3", product_name: "y", gsqut: 1 }], { qty: "positive" }), 2);
  check("n_ymd_ok", m.isCompleteYmd("2026-10-15"), true); check("n_ymd_empty", m.isCompleteYmd(""), false); check("n_ymd_partial", m.isCompleteYmd("2026-10-1"), false);
  console.log(JSON.stringify(results));
})().catch((e) => { console.error(e && e.stack || e); process.exit(1); });
"""

EXPECTED_CHECKS = 90


def _tooling_available() -> bool:
    return shutil.which("node") is not None and shutil.which("npx") is not None


@skipUnless(_tooling_available(), "node/npx 미설치 — 행동 검증 skip")
class SchedulerBehaviour(TestCase):
    def test_scheduler(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            compiled = subprocess.run(
                ["npx", "tsc", str(AUTOSAVE_TS), "--outDir", str(out),
                 "--target", "es2020", "--module", "commonjs", "--skipLibCheck"],
                cwd=FRONTEND, capture_output=True, text=True, timeout=300,
            )
            self.assertEqual(compiled.returncode, 0, compiled.stdout + compiled.stderr)
            (out / "harness.js").write_text(HARNESS_JS, encoding="utf-8")
            proc = subprocess.run(
                ["node", str(out / "harness.js")],
                cwd=FRONTEND, capture_output=True, text=True, timeout=120,
                env={**os.environ, "NODE_PATH": str(FRONTEND / "node_modules")},
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            results = json.loads(proc.stdout.strip().splitlines()[-1])
        failed = [r for r in results if not r["ok"]]
        self.assertFalse(
            failed,
            "DEC-406 회귀: " + ", ".join(f"{r['name']}(got={json.dumps(r['actual'], ensure_ascii=False)} want={json.dumps(r['expected'], ensure_ascii=False)})" for r in failed),
        )
        self.assertEqual(len(results), EXPECTED_CHECKS, f"검증 항목 수 변경: {len(results)}")
        names = [r["name"] for r in results]
        self.assertEqual(len(names), len(set(names)), "검증 이름 중복")


if __name__ == "__main__":
    main()
