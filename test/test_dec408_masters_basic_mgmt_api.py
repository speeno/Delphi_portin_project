"""DEC-408 — 기초관리 API 수정 요청(프론트 개발, 2026-10-17 「북이오 웍스 API 수정 요청 리스트」).

거래처 관리
  1. 거래처구분 생성: 이름만 보내면 구분코드는 서버가 만든다(입고처 · 저자 · 도서 구분도 동일).
  2. 엑셀로 받은 거래처 목록을 한 번에 생성하는 API — 실패한 목록만 응답(입고처 · 저자 · 도서 동일).
  3. 지점관리 여러 개 삭제.
  4. 이메일2 · 주소2 를 입력해도 목록 조회 응답에 안 나온다 — 원인: 목록에 확장 필드 미병합 + 주소1/2 를 `gjuso` 한 줄로
     합쳐 90자에서 잘라 저장(짧은 주소2 가 Gadd1 뒤에 붙고 Gadd2 는 빔).
  5. 「한도액」 = gssum, 「한도」 = Grat7(레거시 출판 빌드 Subu11 Edit130 · Grat8 은 항상 0) — 생성 · 수정 요청에 grat7 추가.
특별 관리
  1. 비고1 · 비고2 — G6_Ggeo 에 칸이 없어(4 서버 DDL) 사이드 테이블 G6_Ggeo_Ext(레거시 무변경).

DB 없이 서비스 모킹 + TestClient 로 본다. 사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path
from typing import Any
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))

from fastapi.testclient import TestClient  # noqa: E402
from openpyxl import Workbook  # noqa: E402

from app.core.deps import get_user_context  # noqa: E402
from app.main import app  # noqa: E402
from app.models import master as models  # noqa: E402
from app.routers.auth import get_current_user  # noqa: E402
from app.services import customer_ext_service, masters_excel, masters_service, special_ext_service  # noqa: E402

_SID = "remote_138"
_HC = "5019"
_CAPS = {f"F{n}": {"read": True, "write": True, "print": True} for n in range(11, 18)}


def _ctx() -> dict[str, Any]:
    return {
        "user_id": "t_fe", "server_id": _SID, "role": "operator", "hcode": _HC, "branch_id": _HC,
        "permissions": ["master.write"], "tenant_id": "", "account_family": "", "active_build_id": "",
        "build_role": "", "account_type": "", "dist_hcode": "", "fxx_caps": dict(_CAPS),
    }


async def _override_user() -> dict[str, Any]:
    return _ctx()


async def _override_ctx() -> dict[str, Any]:
    return _ctx()


class _ClientCase(TestCase):
    def setUp(self) -> None:
        self._prev = {d: app.dependency_overrides.get(d) for d in (get_current_user, get_user_context)}
        app.dependency_overrides[get_current_user] = _override_user
        app.dependency_overrides[get_user_context] = _override_ctx
        self.client = TestClient(app)

    def tearDown(self) -> None:
        for dep, prev in self._prev.items():
            if prev is None:
                app.dependency_overrides.pop(dep, None)
            else:
                app.dependency_overrides[dep] = prev


def _xlsx(headers: list[str], rows: list[list[Any]]) -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.append(headers)
    for r in rows:
        ws.append(r)
    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()


# ═══════════════════════════════════════════════════════════════════════════════
# 1. 구분 생성 — 이름만 보내면 서버 채번
# ═══════════════════════════════════════════════════════════════════════════════
_CATEGORY_ROUTES = (
    ("customer-categories", "G1_Gbun", "create_customer_category"),
    ("inbound-vendor-categories", "G2_Gbun", "create_inbound_vendor_category"),
    ("author-categories", "G3_Gbun", "create_author_category"),
    ("book-categories", "G4_Gbun", "create_book_category"),
)


class CategoryAutoCode(_ClientCase):
    def test_name_only_gets_server_code_for_all_four(self) -> None:
        for path, table, fn in _CATEGORY_ROUTES:
            with self.subTest(path=path):
                created = AsyncMock(return_value={"gcode": "07", "created_at": "t"})
                with patch.object(masters_service, "find_gbun_category_by_name", AsyncMock(return_value=None)) as find, \
                     patch.object(masters_service, "next_master_code", AsyncMock(return_value="07")) as nxt, \
                     patch.object(masters_service, fn, created):
                    res = self.client.post(f"/api/v1/masters/{path}", json={"serverId": _SID, "gname": "온라인서점"})
                self.assertEqual(res.status_code, 201, res.text)
                self.assertEqual(res.json()["gcode"], "07")
                self.assertEqual(nxt.await_args.kwargs["table"], table)
                self.assertEqual(nxt.await_args.kwargs["scope_hcode"], _HC)
                self.assertEqual(find.await_args.kwargs["gname"], "온라인서점")
                self.assertEqual(created.await_args.kwargs["payload"]["gcode"], "07")

    def test_explicit_code_skips_numbering(self) -> None:
        with patch.object(masters_service, "next_master_code", AsyncMock(side_effect=AssertionError("채번 금지"))), \
             patch.object(masters_service, "create_customer_category", AsyncMock(return_value={"gcode": "X1", "created_at": "t"})):
            res = self.client.post("/api/v1/masters/customer-categories", json={"serverId": _SID, "gcode": "X1", "gname": "가"})
        self.assertEqual(res.status_code, 201, res.text)

    def test_same_name_returns_409_with_existing_code(self) -> None:
        with patch.object(masters_service, "find_gbun_category_by_name", AsyncMock(return_value="03")), \
             patch.object(masters_service, "next_master_code", AsyncMock(side_effect=AssertionError("채번 금지"))):
            res = self.client.post("/api/v1/masters/author-categories", json={"serverId": _SID, "gname": "국내저자"})
        self.assertEqual(res.status_code, 409, res.text)
        detail = res.json()["detail"]
        self.assertEqual(detail["code"], "MASTER_DUPLICATE_NAME")
        self.assertEqual(detail["gcode"], "03")

    def test_numbering_exhausted_is_422(self) -> None:
        with patch.object(masters_service, "find_gbun_category_by_name", AsyncMock(return_value=None)), \
             patch.object(masters_service, "next_master_code", AsyncMock(return_value="")):
            res = self.client.post("/api/v1/masters/book-categories", json={"serverId": _SID, "gname": "교재"})
        self.assertEqual(res.status_code, 422, res.text)
        self.assertEqual(res.json()["detail"]["code"], "CODE_UNAVAILABLE")

    def test_request_models_make_code_optional(self) -> None:
        for cls in ("CustomerCategoryCreateRequest", "InboundVendorCategoryCreateRequest",
                    "AuthorCategoryCreateRequest", "BookCategoryCreateRequest"):
            m = getattr(models, cls)(serverId=_SID, gname="가")
            self.assertIsNone(m.gcode, cls)


class CategoryServiceInsert(IsolatedAsyncioTestCase):
    async def test_shared_insert_scopes_hcode_and_rejects_duplicates(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def tx(server_id: str, ops: list) -> list[int]:
            captured.extend(ops)
            return [1]

        with patch.object(masters_service, "execute_query", AsyncMock(return_value=[])), \
             patch.object(masters_service, "execute_in_transaction", AsyncMock(side_effect=tx)):
            out = await masters_service.create_inbound_vendor_category(
                server_id=_SID, payload={"gcode": "05", "gname": "직거래"}, scope_hcode=_HC,
            )
        self.assertEqual(out["gcode"], "05")
        self.assertEqual(captured, [("INSERT INTO G2_Gbun (Gcode, Gname, Hcode) VALUES (%s,%s,%s)", ("05", "직거래", _HC))])
        with patch.object(masters_service, "execute_query", AsyncMock(return_value=[{"Gcode": "05"}])):
            with self.assertRaises(ValueError) as cm:
                await masters_service.create_book_category(server_id=_SID, payload={"gcode": "05", "gname": "x"}, scope_hcode=_HC)
        self.assertEqual(str(cm.exception), "MASTER_DUPLICATE")

    async def test_name_lookup_is_hcode_scoped(self) -> None:
        q = AsyncMock(return_value=[{"gcode": "02"}])
        with patch.object(masters_service, "execute_query", q):
            code = await masters_service.find_gbun_category_by_name(server_id=_SID, table="G3_Gbun", gname=" 국내 ", scope_hcode=_HC)
        self.assertEqual(code, "02")
        sql, params = q.await_args.args[1], q.await_args.args[2]
        self.assertIn("FROM G3_Gbun", sql)
        self.assertIn("Hcode", sql)
        self.assertEqual(params, ("국내", _HC))


# ═══════════════════════════════════════════════════════════════════════════════
# 2. 일괄 생성(JSON · 엑셀) — 실패 행만 응답
# ═══════════════════════════════════════════════════════════════════════════════
class BulkCreateJson(_ClientCase):
    def test_customer_bulk_reports_only_failures(self) -> None:
        def create(*, server_id: str, payload: dict, scope_hcode: str | None) -> dict:
            if payload["gcode"] == "00002":
                raise ValueError("MASTER_DUPLICATE")
            return {"gcode": payload["gcode"], "created_at": "t"}

        items = [
            {"gname": "가서점", "email2": "b@x.kr", "gtel": "02-123-4567"},  # 코드 비움 → 숫자 채번 · 확장 · 전화 분리
            {"gcode": "00002", "gname": "나서점"},                          # 중복
            {"gcode": ""},                                                  # 이름 없음
            {"gname": "라서점", "gbun_name": "구내서점"},                     # 접두 채번
            {"gname": "마서점", "grat1": "abc"},                              # 숫자 검증 실패
        ]
        ext = AsyncMock(return_value=["email2"])
        with patch.object(masters_service, "create_customer_master", AsyncMock(side_effect=create)) as svc, \
             patch.object(masters_service, "next_master_code", AsyncMock(side_effect=["00010", "00011"])), \
             patch.object(masters_service, "next_customer_code_by_prefix", AsyncMock(return_value="A00001")) as pre, \
             patch.object(customer_ext_service, "upsert_ext", ext):
            res = self.client.post("/api/v1/masters/customer/bulk", json={"serverId": _SID, "items": items})
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual((body["entity"], body["total"], body["created"], body["failed_count"]), ("customer", 5, 2, 3))
        self.assertEqual([f["index"] for f in body["failed"]], [1, 2, 4])
        self.assertEqual([f["code"] for f in body["failed"]], ["MASTER_DUPLICATE", "MASTER_VALIDATION", "MASTER_VALIDATION"])
        self.assertEqual(body["failed"][0]["item"], {"gcode": "00002", "gname": "나서점"}, "원본 입력을 돌려준다")
        self.assertIn("grat1", body["failed"][2]["message"])
        created_codes = [c.kwargs["payload"]["gcode"] for c in svc.await_args_list if c.kwargs["payload"]["gcode"] != "00002"]
        self.assertEqual(created_codes, ["00010", "A00001"])
        self.assertEqual(pre.await_args.kwargs["prefix"], "A")
        first = svc.await_args_list[0].kwargs["payload"]
        self.assertEqual((first["gtel1"], first["gtel2"]), ("02", "123-4567"))
        self.assertNotIn("email2", first, "확장 필드는 G1_Ggeo INSERT 가 아니라 사이드 테이블로")
        self.assertEqual(ext.await_args.kwargs["values"], {"email2": "b@x.kr"})

    def test_item_limit_and_server_ownership(self) -> None:
        too_many = [{"gname": f"n{i}"} for i in range(models.MASTER_BULK_MAX_ITEMS + 1)]
        res = self.client.post("/api/v1/masters/authors/bulk", json={"serverId": _SID, "items": too_many})
        self.assertEqual(res.status_code, 422, res.text)
        res = self.client.post("/api/v1/masters/authors/bulk", json={"serverId": "remote_999", "items": [{"gposa": "a"}]})
        self.assertEqual(res.status_code, 403, res.text)

    def test_author_and_inbound_vendor_use_their_own_name_key(self) -> None:
        with patch.object(masters_service, "create_author", AsyncMock(return_value={"gcode": "0101", "created_at": "t"})), \
             patch.object(masters_service, "next_master_code", AsyncMock(return_value="0101")) as nxt, \
             patch("app.services.author_ext_service.upsert_ext", AsyncMock(return_value=None)):
            res = self.client.post("/api/v1/masters/authors/bulk", json={"serverId": _SID, "items": [{"gposa": "홍길동"}, {"gname": "직장만"}]})
        body = res.json()
        self.assertEqual((body["created"], body["failed_count"]), (1, 1))
        self.assertIn("저자명", body["failed"][0]["message"])
        self.assertEqual(nxt.await_args.kwargs["table"], "G3_Gjeo")
        with patch.object(masters_service, "create_inbound_vendor", AsyncMock(return_value={"gcode": "0501", "created_at": "t"})), \
             patch.object(masters_service, "next_master_code", AsyncMock(return_value="0501")) as nxt:
            res = self.client.post("/api/v1/masters/inbound-vendors/bulk", json={"serverId": _SID, "items": [{"gname": "인쇄소"}]})
        self.assertEqual(res.json()["created"], 1, res.text)
        self.assertEqual(nxt.await_args.kwargs["table"], "G2_Ggwo")


class BulkCreateXlsx(_ClientCase):
    def test_book_upload_numbers_by_band_and_reports_sheet_rows(self) -> None:
        data = _xlsx(
            ["도서코드", "제목", "저자", "도서구분", "단가"],
            [["", "새 교재", "홍길동", "교재", 15000], ["B001", "기존 도서", "", "", 9000], ["", "", "이름없음", "", 0]],
        )

        def create(*, server_id: str, payload: dict, scope_hcode: str | None) -> dict:
            if payload["gcode"] == "B001":
                raise ValueError("MASTER_DUPLICATE")
            return {"gcode": payload["gcode"], "created_at": "t"}

        with patch.object(masters_service, "create_book", AsyncMock(side_effect=create)) as svc, \
             patch.object(masters_service, "_resolve_g4_gubun_code", AsyncMock(return_value="03")) as gub, \
             patch("app.services.book_code_bands.propose_book_code", AsyncMock(return_value={"code": "30001", "band": {"from": "30000"}, "reason": None})) as band:
            res = self.client.post(
                f"/api/v1/masters/book/bulk.xlsx?serverId={_SID}",
                files={"file": ("books.xlsx", data, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")},
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual((body["total"], body["created"], body["failed_count"]), (3, 1, 2))
        self.assertEqual([(f["row"], f["code"]) for f in body["failed"]], [(3, "MASTER_DUPLICATE"), (4, "MASTER_VALIDATION")])
        self.assertEqual(band.await_args.kwargs["gubun"], "03", "도서구분 이름 → 코드 → 대역 채번")
        self.assertEqual(gub.await_args.kwargs["payload"]["sname"], "교재")
        new = svc.await_args_list[0].kwargs["payload"]
        self.assertEqual((new["gcode"], new["gname"], new["gjeja"], new["gdang"]), ("30001", "새 교재", "홍길동", 15000))

    def test_template_and_size_errors(self) -> None:
        bad = _xlsx(["코드", "아무거나"], [["", "x"]])
        res = self.client.post(f"/api/v1/masters/customer/bulk.xlsx?serverId={_SID}", files={"file": ("c.xlsx", bad, "application/octet-stream")})
        self.assertEqual(res.status_code, 400, res.text)
        self.assertIn("거래처명", res.json()["detail"]["message"])
        big = _xlsx(["거래처명"], [[f"n{i}"] for i in range(501)])
        res = self.client.post(f"/api/v1/masters/customer/bulk.xlsx?serverId={_SID}", files={"file": ("c.xlsx", big, "application/octet-stream")})
        self.assertEqual(res.status_code, 422, res.text)
        self.assertEqual(res.json()["detail"]["code"], "TOO_MANY_ROWS")
        empty = _xlsx(["거래처명"], [])
        res = self.client.post(f"/api/v1/masters/customer/bulk.xlsx?serverId={_SID}", files={"file": ("c.xlsx", empty, "application/octet-stream")})
        self.assertEqual(res.json()["detail"]["code"], "EMPTY_SHEET")

    def test_customer_upload_splits_phone_and_keeps_address_columns(self) -> None:
        data = _xlsx(["거래처명", "전화", "주소1", "주소2", "한도"], [["가서점", "031-955-1234", "파주시", "고양시", 70]])
        with patch.object(masters_service, "create_customer_master", AsyncMock(return_value={"gcode": "00010", "created_at": "t"})) as svc, \
             patch.object(masters_service, "next_master_code", AsyncMock(return_value="00010")):
            res = self.client.post(f"/api/v1/masters/customer/bulk.xlsx?serverId={_SID}", files={"file": ("c.xlsx", data, "application/octet-stream")})
        self.assertEqual(res.json()["created"], 1, res.text)
        p = svc.await_args.kwargs["payload"]
        self.assertEqual((p["gtel1"], p["gtel2"], p["gadd1"], p["gadd2"], p["grat7"]), ("031", "955-1234", "파주시", "고양시", 70.0))


class ParseWithoutCode(TestCase):
    def test_require_pk_false_keeps_codeless_rows_with_sheet_numbers(self) -> None:
        data = _xlsx(["코드", "저자명"], [["", "가"], ["A1", "나"], ["A1", "다"], ["", "라"]])
        out = masters_excel.parse_master_xlsx(
            data, pk=masters_excel.AUTHOR_IMPORT_PK, field_map=masters_excel.AUTHOR_IMPORT_MAP, require_pk=False,
        )
        self.assertTrue(out["header_ok"])
        self.assertEqual([(r["row"], r["gcode"], r["payload"]["gposa"]) for r in out["rows"]], [(2, "", "가"), (3, "A1", "나"), (5, "", "라")])
        self.assertTrue(any("중복" in w for w in out["warnings"]))
        self.assertIn("gposa", out["mapped_keys"])
        # 종전(수정 업로드)은 그대로 — 코드 없는 행 건너뜀.
        old = masters_excel.parse_master_xlsx(data, pk=masters_excel.AUTHOR_IMPORT_PK, field_map=masters_excel.AUTHOR_IMPORT_MAP)
        self.assertEqual([r["gcode"] for r in old["rows"]], ["A1"])

    def test_header_without_code_column_allowed_only_for_create(self) -> None:
        data = _xlsx(["저자명"], [["가"]])
        self.assertTrue(masters_excel.parse_master_xlsx(data, pk=masters_excel.AUTHOR_IMPORT_PK, field_map=masters_excel.AUTHOR_IMPORT_MAP, require_pk=False)["header_ok"])
        self.assertFalse(masters_excel.parse_master_xlsx(data, pk=masters_excel.AUTHOR_IMPORT_PK, field_map=masters_excel.AUTHOR_IMPORT_MAP)["header_ok"])


# ═══════════════════════════════════════════════════════════════════════════════
# 3. 지점 일괄 삭제
# ═══════════════════════════════════════════════════════════════════════════════
class BranchBulkDelete(_ClientCase):
    def test_partial_success_and_dedupe(self) -> None:
        async def delete(*, server_id: str, gcode: str, branch_id: int, scope_hcode: str | None):
            if branch_id == 2:
                return None
            if branch_id == 3:
                raise ValueError("gcode is required")
            return {"id": branch_id, "gcode": gcode, "deleted_at": "t"}

        with patch.object(masters_service, "delete_customer_branch", AsyncMock(side_effect=delete)) as svc:
            res = self.client.post(
                "/api/v1/masters/customer/00001/branches/bulk-delete",
                json={"serverId": _SID, "ids": [1, 2, 3, 1, 4]},
            )
        self.assertEqual(res.status_code, 200, res.text)
        body = res.json()
        self.assertEqual((body["gcode"], body["requested"], body["deleted"]), ("00001", 4, [1, 4]))
        self.assertEqual([(f["id"], f["code"]) for f in body["failed"]], [(2, "MASTER_NOT_FOUND"), (3, "MASTER_INVALID")])
        self.assertEqual({c.kwargs["scope_hcode"] for c in svc.await_args_list}, {_HC})

    def test_other_server_is_forbidden(self) -> None:
        res = self.client.post("/api/v1/masters/customer/00001/branches/bulk-delete", json={"serverId": "remote_999", "ids": [1]})
        self.assertEqual(res.status_code, 403, res.text)


# ═══════════════════════════════════════════════════════════════════════════════
# 4 · 5. 거래처 — 주소1/2 따로 저장 · 목록 확장 필드 · 한도(grat7)
# ═══════════════════════════════════════════════════════════════════════════════
_G1_COLS = {"gcode", "gname", "hcode", "gubun", "gadd1", "gadd2", "grat7", "gssum", "email", "gpost"}
_G1_EXACT = {c: c.capitalize() for c in _G1_COLS}


class CustomerAddressAndLimit(IsolatedAsyncioTestCase):
    async def _insert(self, payload: dict) -> dict[str, Any]:
        captured: list[tuple[str, tuple]] = []

        async def tx(server_id: str, ops: list) -> list[int]:
            captured.extend(ops)
            return [1]

        with patch.object(masters_service, "g1_geo_column_meta", AsyncMock(return_value=(_G1_COLS, _G1_EXACT))), \
             patch.object(masters_service, "ensure_code_fits", AsyncMock(return_value=None)), \
             patch.object(masters_service, "_resolve_gubun_code", AsyncMock(return_value="")), \
             patch.object(masters_service, "execute_query", AsyncMock(return_value=[])), \
             patch.object(masters_service, "execute_in_transaction", AsyncMock(side_effect=tx)):
            await masters_service.create_customer_master(server_id=_SID, payload=payload, scope_hcode=_HC)
        sql, params = captured[0]
        cols = sql[sql.index("(") + 1 : sql.index(")")].split(", ")
        return dict(zip(cols, params))

    async def test_create_keeps_address1_and_address2_apart(self) -> None:
        row = await self._insert({"gcode": "00010", "gname": "가", "gadd1": "파주시 문발로", "gadd2": "고양시 일산", "gjuso": "무시"})
        self.assertEqual((row["Gadd1"], row["Gadd2"]), ("파주시 문발로", "고양시 일산"))

    async def test_create_legacy_gjuso_still_splits(self) -> None:
        row = await self._insert({"gcode": "00010", "gname": "가", "gjuso": "서울"})
        self.assertEqual((row["Gadd1"], row["Gadd2"]), ("서울", ""))

    async def test_create_writes_limit_rate(self) -> None:
        row = await self._insert({"gcode": "00010", "gname": "가", "grat7": 65, "gssum": 1000000})
        self.assertEqual((row["Grat7"], row["Gssum"]), (65.0, 1000000.0))

    async def test_update_address2_only_and_limit(self) -> None:
        captured: list[tuple[str, tuple]] = []

        async def tx(server_id: str, ops: list) -> list[int]:
            captured.extend(ops)
            return [1]

        with patch.object(masters_service, "g1_geo_column_meta", AsyncMock(return_value=(_G1_COLS, _G1_EXACT))), \
             patch.object(masters_service, "execute_in_transaction", AsyncMock(side_effect=tx)):
            out = await masters_service.update_customer_master(
                server_id=_SID, gcode="00010", payload={"gadd2": "고양시", "gjuso": "옛 합본", "grat7": 70}, scope_hcode=_HC,
            )
        sql, params = captured[0]
        self.assertIn("Gadd2=%s", sql)
        self.assertNotIn("Gadd1=%s", sql, "보낸 칸만 바꾼다(gjuso 는 gadd1/gadd2 가 있으면 무시)")
        self.assertIn("Grat7=%s", sql)
        self.assertEqual(params[:2], ("고양시", 70.0))
        self.assertEqual(out["updated_fields"], ["gadd2", "grat7"])

    def test_models_accept_limit_rate(self) -> None:
        self.assertEqual(models.CustomerCreateRequest(serverId=_SID, gcode="1", gname="a", grat7=70).grat7, 70.0)
        self.assertEqual(models.CustomerUpdateRequest(serverId=_SID, grat7=55).grat7, 55.0)
        self.assertIn("grat7", masters_excel.CUSTOMER_IMPORT_MAP.values(), "엑셀 「한도」 칸도 역반영")
        self.assertIn("grat7", masters_excel.CUSTOMER_NUMERIC_KEYS)

    async def test_list_returns_addresses_and_extension_fields(self) -> None:
        rows = [
            {"gcode": "00001", "gname": "가", "hcode": _HC, "gubun_code": "", "gadd1": "파주", "gadd2": "고양", "grat7": 70},
            {"gcode": "00002", "gname": "나", "hcode": _HC, "gubun_code": "", "gadd1": "", "gadd2": ""},
        ]
        q = AsyncMock(side_effect=[rows, [{"row_count": 2}]])
        ext = AsyncMock(return_value={"00001": {"email2": "b@x.kr", "zip2": "10881", "add2_detail": "3층"}})
        with patch.object(masters_service, "g1_geo_column_meta", AsyncMock(return_value=(_G1_COLS, _G1_EXACT))), \
             patch.object(masters_service, "_customer_search_cols", AsyncMock(return_value=("Gcode", "Gname"))), \
             patch.object(masters_service, "_gbun_code_name_map", AsyncMock(return_value={})), \
             patch.object(masters_service, "execute_query", q), \
             patch.object(customer_ext_service, "get_ext_many", ext):
            out = await masters_service.list_customer_master(server_id=_SID, scope_hcode=_HC)
        self.assertIn("Gadd2", q.await_args_list[0].args[1])
        a, b = out["items"]
        self.assertEqual((a["gadd1"], a["gadd2"], a["email2"], a["zip2"], a["add2_detail"], a["grat7"]), ("파주", "고양", "b@x.kr", "10881", "3층", 70.0))
        self.assertEqual((b["email2"], b["memo"]), ("", ""), "확장 행이 없는 거래처는 빈 값")
        self.assertEqual(ext.await_args.kwargs["gcodes"], ["00001", "00002"])
        for key in ("gadd1", "gadd2", "email2", "zip2", "add1_detail", "add2_detail", "tel2", "phon2", "memo"):
            self.assertIn(key, models.CustomerListItem.model_fields, f"응답 모델이 {key} 를 잘라내면 안 된다")


# ═══════════════════════════════════════════════════════════════════════════════
# 특별관리 비고1 · 비고2 — 사이드 테이블
# ═══════════════════════════════════════════════════════════════════════════════
class SpecialBigoSideTable(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        special_ext_service._ensured.clear()

    async def test_get_many_drops_rows_whose_link_changed(self) -> None:
        found = [
            {"id": 5, "gcode": "G1", "bcode": "B1", "bigo1": "택배", "bigo2": ""},
            {"id": 6, "gcode": "G2", "bcode": "OLD", "bigo1": "옛 비고", "bigo2": ""},
        ]
        with patch.object(special_ext_service, "execute_query", AsyncMock(return_value=[])), \
             patch.object(special_ext_service, "in_clause_lookup", AsyncMock(return_value=found)) as lk:
            out = await special_ext_service.get_many(
                server_id=_SID, hcode=_HC, rows=[{"id": 5, "gcode": "G1", "bcode": "B1"}, {"id": 6, "gcode": "G2", "bcode": "B2"}],
            )
        self.assertEqual(out, {5: {"bigo1": "택배", "bigo2": ""}})
        self.assertEqual(lk.await_args.kwargs["prefix_params"], (_HC,))
        self.assertIn("WHERE Hcode=%s", lk.await_args.kwargs["sql_template"])

    async def test_upsert_merges_and_deletes_when_empty(self) -> None:
        calls: list[tuple[str, tuple]] = []

        async def q(server_id: str, sql: str, params: tuple = ()) -> list[dict]:
            calls.append((sql, params))
            if sql.startswith("SELECT"):
                return [{"gcode": "G1", "bcode": "B1", "bigo1": "a", "bigo2": "b"}]
            return []

        with patch.object(special_ext_service, "execute_query", AsyncMock(side_effect=q)):
            changed = await special_ext_service.upsert(server_id=_SID, hcode=_HC, row_id=5, gcode="G1", bcode="B1", values={"bigo2": "c", "grat1": "9"})
        self.assertEqual(changed, ["bigo2"])
        self.assertIn(("REPLACE INTO G6_Ggeo_Ext (Hcode, Id, Gcode, Bcode, Bigo1, Bigo2) VALUES (%s,%s,%s,%s,%s,%s)",
                       (_HC, 5, "G1", "B1", "a", "c")), calls)
        self.assertTrue(any("CREATE TABLE IF NOT EXISTS G6_Ggeo_Ext" in s for s, _ in calls))
        calls.clear()
        with patch.object(special_ext_service, "execute_query", AsyncMock(side_effect=q)):
            await special_ext_service.upsert(server_id=_SID, hcode=_HC, row_id=5, gcode="G1", bcode="B1", values={"bigo1": "", "bigo2": ""})
        self.assertIn(("DELETE FROM G6_Ggeo_Ext WHERE Hcode=%s AND Id=%s", (_HC, 5)), calls)

    async def test_update_with_only_bigo_touches_side_table(self) -> None:
        up = AsyncMock(return_value=["bigo1"])
        with patch.object(masters_service, "execute_query", AsyncMock(return_value=[{"ID": 5, "Gcode": "G1", "Bcode": "B1"}])), \
             patch("app.services.g6_ggeo_adapt.g6_column_names", AsyncMock(return_value=set())), \
             patch.object(special_ext_service, "upsert", up):
            out = await masters_service.update_special_master(server_id=_SID, row_id=5, hcode=_HC, payload={"bigo1": "택배"})
        self.assertEqual(out["updated_fields"], ["bigo1"])
        self.assertEqual((up.await_args.kwargs["gcode"], up.await_args.kwargs["bcode"]), ("G1", "B1"))

    async def test_create_and_delete_follow_the_row(self) -> None:
        up = AsyncMock(return_value=["bigo1", "bigo2"])
        q = AsyncMock(side_effect=[[], [{"id": 41}]])
        with patch.object(masters_service, "execute_query", q), \
             patch.object(masters_service, "execute_in_transaction", AsyncMock(return_value=[1])), \
             patch("app.services.g6_ggeo_adapt.g6_column_names", AsyncMock(return_value=set())), \
             patch.object(special_ext_service, "upsert", up):
            out = await masters_service.create_special_master(
                server_id=_SID, hcode=_HC, payload={"gcode": "G1", "bcode": "B1", "grat1": "60", "bigo1": "택배", "bigo2": "월말"},
            )
        self.assertEqual(out["id"], 41)
        self.assertEqual(up.await_args.kwargs["row_id"], 41)
        rm = AsyncMock(return_value=None)
        with patch.object(masters_service, "execute_query", AsyncMock(return_value=[{"ID": 41}])), \
             patch.object(masters_service, "execute_in_transaction", AsyncMock(return_value=[1])), \
             patch.object(special_ext_service, "delete", rm):
            await masters_service.delete_special_master(server_id=_SID, row_id=41, hcode=_HC)
        self.assertEqual(rm.await_args.kwargs, {"server_id": _SID, "hcode": _HC, "row_id": 41})

    def test_models_carry_bigo(self) -> None:
        self.assertIn("bigo1", models.SpecialListItem.model_fields)
        self.assertEqual(models.SpecialUpdateRequest(serverId=_SID, hcode=_HC, bigo2="x").bigo2, "x")
        self.assertEqual(models.SpecialCreateRequest(serverId=_SID, hcode=_HC, gcode="G", bcode="B", bigo1="y").bigo1, "y")


class SpecialListMergesBigo(IsolatedAsyncioTestCase):
    async def test_list_items_carry_bigo(self) -> None:
        rows = [{"id": 5, "hcode": _HC, "gcode": "G1", "bcode": "B1", "grat1": "60", "gssum": 0}]
        with patch.object(masters_service, "execute_query", AsyncMock(side_effect=[[{"row_count": 1}], rows])), \
             patch("app.services.g6_ggeo_adapt.g6_column_names", AsyncMock(return_value=set())), \
             patch("app.services.book_meta_lookup.attach_book_meta", AsyncMock(return_value=None)), \
             patch.object(special_ext_service, "get_many", AsyncMock(return_value={5: {"bigo1": "택배", "bigo2": "월말"}})):
            out = await masters_service.list_special_master(server_id=_SID, mode="publisher", hcode=_HC)
        self.assertEqual((out["items"][0]["bigo1"], out["items"][0]["bigo2"]), ("택배", "월말"))


if __name__ == "__main__":
    main()
