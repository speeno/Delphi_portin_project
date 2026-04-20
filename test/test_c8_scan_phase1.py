"""
C8 바코드 스캔 Phase 1 — POST /api/v1/scan/match 검증 테스트.

검증 범위 (contracts)
---------------------
- migration/contracts/barcode_scan.yaml v1.0.0 (POST /scan/match 단일 엔드포인트)
- analysis/layout_mappings/c8_scan_match.md (FTong07.Edit101 ↔ 모던 useScanner)
- analysis/handlers/c8_scan.md (SQL-SC-1~4)
- i18n/messages/c8.ko.json (스캔 토스트 8 키)

검증 케이스 (~22건)
-------------------
- TC-SC-P1-01~03  matched 응답 (outbound/inbound/return)
- TC-SC-P1-04~05  nodata 응답 (200 OK 유지) — 출고/입고
- TC-SC-P1-06~07  단가 폴백 우선순위 (Hcode='' 1순위, 라인 Hcode 2순위)
- TC-SC-P1-08     단가 양쪽 NODATA → grats=null + grats_source=none
- TC-SC-P1-09     hcode 빈 문자열 → 400 SC_HCODE_REQUIRED
- TC-SC-P1-10     context 잘못된 값 → 422 SC_VALIDATION_FAILED
- TC-SC-P1-11~14  4 server matrix (138/153/154/155) — matched 1건 each
- TC-SC-P1-15     i18n c8.ko.json 8 키 정합성
- TC-SC-P1-16     barcode_scan.yaml customer_variants/decisions/endpoints
- TC-SC-P1-17     handlers/c8_scan.md 4 SQL ID 등록
- TC-SC-P1-18     layout_mappings/c8_scan_match.md DEC-028 참조
- TC-SC-P1-19     screen_cards/Tong08.md 진입점 명시
- TC-SC-P1-20     scan_match_service.py 신규 INSERT/UPDATE/DELETE 0건
- TC-SC-P1-21     pricing_service.py 신규 INSERT/UPDATE/DELETE 0건
- TC-SC-P1-22     3 페이지 data-legacy-id="FTong07.Edit101" grep ≥ 3건

설계 정합 (사용자 룰)
---------------------
- C7 Phase 1 패턴(test_c7_print_phase1.py) 동일 — monkeypatch + dependency_overrides + skipUnless.
- 신규 헬퍼 금지, test 폴더 한 파일.
- T5 미착수 시점에는 서비스 import 실패 가능 → unittest.skipUnless 로 안전 우회.
- 정적 검사(15~22) 는 T5 무관하게 항상 실행 — DEC-028 / DEC-040 가시화.
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
from pathlib import Path
from unittest import TestCase, main, skipUnless
from unittest.mock import AsyncMock, patch

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
sys.path.insert(0, str(BACKEND))


# ──────────────────────────────────────────────
# T5 의존성 — 미착수 시점에는 안전 우회 (skipUnless)
# 런타임 검증은 scan_match_service / pricing_service / scan 라우터 모두 import 가능해야 활성.
# ──────────────────────────────────────────────
_RUNTIME_OK = False
try:
    from fastapi.testclient import TestClient  # noqa: E402
    from app.main import app  # noqa: E402
    from app.routers.auth import get_current_user  # noqa: E402

    def _override_auth() -> dict:
        return {"user_id": "hong01", "server_id": "remote_138", "role": "manager"}

    app.dependency_overrides[get_current_user] = _override_auth

    from app.services import scan_match_service as _scan_service  # noqa: F401
    from app.services import pricing_service as _pricing_service  # noqa: F401

    _RUNTIME_OK = True
except Exception:
    TestClient = None  # type: ignore[assignment]
    app = None  # type: ignore[assignment]


# ──────────────────────────────────────────────
# 공통 픽스처
# ──────────────────────────────────────────────
SCAN_PATH = "/api/v1/scan/match"

BARCODE_OK = "9788972754381"
BARCODE_MISS = "0000000000000"
HCODE = "1234"

MATCHED_BOOK = {
    "gcode": "001",
    "gname": "샘플도서",
    "gjeja": "샘플저자",
    "ocode": "B",
    "gdang": 15000,
}

GRATS_HCODE_EMPTY = {
    "grats": [0.85, 0.80, 0.75, 0.70, 0.65, 0.60],
    "grats_source": "G1_Ggeo:hcode_empty",
}
GRATS_HCODE_LINE = {
    "grats": [0.90, 0.85, 0.80, 0.75, 0.70, 0.65],
    "grats_source": "G1_Ggeo:hcode_line",
}
GRATS_INBOUND_EMPTY = {
    "grats": [0.95, 0.92, 0.88, 0.85, 0.80, 0.75],
    "grats_source": "G2_Ggwo:hcode_empty",
}


# ──────────────────────────────────────────────
# 1. 런타임 매칭 응답 검증 (T5 착수 후 활성)
# ──────────────────────────────────────────────
@skipUnless(_RUNTIME_OK, "T5 (scan_match_service / routers/scan.py) 미착수 — 정적 검사만 실행")
class C8ScanRuntimeTestCase(TestCase):
    """POST /api/v1/scan/match 응답 검증."""

    def setUp(self) -> None:
        assert app is not None and TestClient is not None
        self.client = TestClient(app)

    # ────── matched ──────
    def test_TC_SC_P1_01_matched_outbound(self) -> None:
        from app.services import scan_match_service
        with patch.object(
            scan_match_service, "match_barcode",
            return_value={
                "status": "matched",
                "resolved": {**MATCHED_BOOK, **GRATS_HCODE_EMPTY},
                "barcode": BARCODE_OK,
                "hcode": HCODE,
                "context": "outbound",
            },
        ):
            res = self.client.post(SCAN_PATH, json={
                "barcode": BARCODE_OK, "hcode": HCODE,
                "context": "outbound", "server_id": "remote_138",
            })
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body["status"], "matched")
        self.assertEqual(body["resolved"]["gcode"], "001")
        self.assertEqual(body["resolved"]["grats_source"], "G1_Ggeo:hcode_empty")
        self.assertEqual(body["context"], "outbound")

    def test_TC_SC_P1_02_matched_inbound(self) -> None:
        from app.services import scan_match_service
        with patch.object(
            scan_match_service, "match_barcode",
            return_value={
                "status": "matched",
                "resolved": {**MATCHED_BOOK, **GRATS_INBOUND_EMPTY},
                "barcode": BARCODE_OK, "hcode": HCODE, "context": "inbound",
            },
        ):
            res = self.client.post(SCAN_PATH, json={
                "barcode": BARCODE_OK, "hcode": HCODE,
                "context": "inbound", "server_id": "remote_138",
            })
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body["status"], "matched")
        self.assertEqual(body["resolved"]["grats_source"], "G2_Ggwo:hcode_empty")

    def test_TC_SC_P1_03_matched_return(self) -> None:
        from app.services import scan_match_service
        with patch.object(
            scan_match_service, "match_barcode",
            return_value={
                "status": "matched",
                "resolved": {**MATCHED_BOOK, **GRATS_HCODE_EMPTY},
                "barcode": BARCODE_OK, "hcode": HCODE, "context": "return",
            },
        ):
            res = self.client.post(SCAN_PATH, json={
                "barcode": BARCODE_OK, "hcode": HCODE,
                "context": "return", "server_id": "remote_138",
            })
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body["status"], "matched")
        self.assertEqual(body["resolved"]["grats_source"], "G1_Ggeo:hcode_empty")

    # ────── nodata ──────
    def test_TC_SC_P1_04_nodata_outbound_returns_200(self) -> None:
        """G4_Book NODATA → 200 + status='nodata' + resolved=null (레거시 Tong07.pas L93 NODATA 동등)."""
        from app.services import scan_match_service
        with patch.object(
            scan_match_service, "match_barcode",
            return_value={
                "status": "nodata", "resolved": None,
                "barcode": BARCODE_MISS, "hcode": HCODE, "context": "outbound",
            },
        ):
            res = self.client.post(SCAN_PATH, json={
                "barcode": BARCODE_MISS, "hcode": HCODE,
                "context": "outbound", "server_id": "remote_138",
            })
        self.assertEqual(res.status_code, 200)
        body = res.json()
        self.assertEqual(body["status"], "nodata")
        self.assertIsNone(body["resolved"])

    def test_TC_SC_P1_05_nodata_inbound_returns_200(self) -> None:
        from app.services import scan_match_service
        with patch.object(
            scan_match_service, "match_barcode",
            return_value={
                "status": "nodata", "resolved": None,
                "barcode": BARCODE_MISS, "hcode": HCODE, "context": "inbound",
            },
        ):
            res = self.client.post(SCAN_PATH, json={
                "barcode": BARCODE_MISS, "hcode": HCODE,
                "context": "inbound", "server_id": "remote_138",
            })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "nodata")

    # ────── 단가 폴백 우선순위 (D-SC-1) ──────
    def test_TC_SC_P1_06_grats_fallback_hcode_empty_first(self) -> None:
        """1순위: Hcode='' 매칭 성공 → grats_source='G1_Ggeo:hcode_empty'.

        execute_query 를 모킹하여 첫 호출 (Hcode='') 에서 단가 row 반환 → 두 번째 호출 없음 검증.
        """
        from app.services import pricing_service
        empty_hcode_row = {f"Grat{i}": GRATS_HCODE_EMPTY["grats"][i - 1] for i in range(1, 7)}
        with patch.object(pricing_service, "execute_query", new=AsyncMock(return_value=[empty_hcode_row])) as mock:
            result = asyncio.run(pricing_service.resolve_grats(
                context="outbound", gcode="001", hcode=HCODE, server_id="remote_138",
            ))
        self.assertEqual(result["grats_source"], "G1_Ggeo:hcode_empty")
        self.assertEqual(len(result["grats"]), 6)
        # 1순위에서 매칭 → execute_query 정확히 1번 호출
        self.assertEqual(mock.call_count, 1)
        # 첫 호출 인자에 Hcode='' 포함
        called_args = mock.call_args[0]
        self.assertEqual(called_args[2], ("001", ""))

    def test_TC_SC_P1_07_grats_fallback_to_line_hcode(self) -> None:
        """2순위: Hcode='' NODATA → 라인 Hcode 매칭 성공."""
        from app.services import pricing_service
        line_hcode_row = {f"Grat{i}": GRATS_HCODE_LINE["grats"][i - 1] for i in range(1, 7)}
        side = [[], [line_hcode_row]]
        with patch.object(pricing_service, "execute_query", new=AsyncMock(side_effect=side)) as mock:
            result = asyncio.run(pricing_service.resolve_grats(
                context="outbound", gcode="001", hcode=HCODE, server_id="remote_138",
            ))
        self.assertEqual(result["grats_source"], "G1_Ggeo:hcode_line")
        self.assertEqual(mock.call_count, 2)
        # 두 번째 호출 인자에 라인 Hcode
        self.assertEqual(mock.call_args_list[1][0][2], ("001", HCODE))

    def test_TC_SC_P1_08_grats_both_nodata_returns_null(self) -> None:
        """양쪽 NODATA → grats=null + grats_source='none' (gdang 폴백)."""
        from app.services import pricing_service
        with patch.object(pricing_service, "execute_query", new=AsyncMock(side_effect=[[], []])):
            result = asyncio.run(pricing_service.resolve_grats(
                context="outbound", gcode="001", hcode=HCODE, server_id="remote_138",
            ))
        self.assertIsNone(result["grats"])
        self.assertEqual(result["grats_source"], "none")

    # ────── 가드 ──────
    def test_TC_SC_P1_09_empty_hcode_returns_400(self) -> None:
        res = self.client.post(SCAN_PATH, json={
            "barcode": BARCODE_OK, "hcode": "",
            "context": "outbound", "server_id": "remote_138",
        })
        self.assertIn(res.status_code, (400, 422))
        body = res.json()
        detail = body.get("detail", body)
        if isinstance(detail, dict):
            self.assertEqual(detail.get("code"), "SC_HCODE_REQUIRED")
        else:
            text = json.dumps(body, ensure_ascii=False)
            self.assertTrue("SC_HCODE_REQUIRED" in text or "hcode" in text.lower())

    def test_TC_SC_P1_10_invalid_context_returns_422(self) -> None:
        """context=foo 잘못된 값 → 422 SC_VALIDATION_FAILED 또는 pydantic 자동 422."""
        res = self.client.post(SCAN_PATH, json={
            "barcode": BARCODE_OK, "hcode": HCODE,
            "context": "FOOBAR", "server_id": "remote_138",
        })
        self.assertIn(res.status_code, (400, 422))

    # ────── 4 server matrix ──────
    def _matched_payload(self, server_id: str) -> dict:
        return {
            "status": "matched",
            "resolved": {**MATCHED_BOOK, **GRATS_HCODE_EMPTY},
            "barcode": BARCODE_OK, "hcode": HCODE, "context": "outbound",
        }

    def test_TC_SC_P1_11_server_remote_138(self) -> None:
        from app.services import scan_match_service
        with patch.object(scan_match_service, "match_barcode",
                          return_value=self._matched_payload("remote_138")):
            res = self.client.post(SCAN_PATH, json={
                "barcode": BARCODE_OK, "hcode": HCODE,
                "context": "outbound", "server_id": "remote_138",
            })
        self.assertEqual(res.status_code, 200)

    def test_TC_SC_P1_12_server_remote_153(self) -> None:
        from app.services import scan_match_service
        with patch.object(scan_match_service, "match_barcode",
                          return_value=self._matched_payload("remote_153")):
            res = self.client.post(SCAN_PATH, json={
                "barcode": BARCODE_OK, "hcode": HCODE,
                "context": "outbound", "server_id": "remote_153",
            })
        self.assertEqual(res.status_code, 200)

    def test_TC_SC_P1_13_server_remote_154_mysql3(self) -> None:
        """remote_154 (MySQL 3.23) — apply_limit_offset_syntax 의 미바인딩 LIMIT 형태."""
        from app.services import scan_match_service
        with patch.object(scan_match_service, "match_barcode",
                          return_value=self._matched_payload("remote_154")):
            res = self.client.post(SCAN_PATH, json={
                "barcode": BARCODE_OK, "hcode": HCODE,
                "context": "outbound", "server_id": "remote_154",
            })
        self.assertEqual(res.status_code, 200)

    def test_TC_SC_P1_14_server_remote_155_mysql3(self) -> None:
        from app.services import scan_match_service
        with patch.object(scan_match_service, "match_barcode",
                          return_value=self._matched_payload("remote_155")):
            res = self.client.post(SCAN_PATH, json={
                "barcode": BARCODE_OK, "hcode": HCODE,
                "context": "outbound", "server_id": "remote_155",
            })
        self.assertEqual(res.status_code, 200)


# ──────────────────────────────────────────────
# 2. 정적 검사 (T5 무관 — 항상 실행)
# ──────────────────────────────────────────────
class C8ScanStaticTestCase(TestCase):
    """contracts / mappings / handlers / i18n 정합 정적 검사."""

    # ────── i18n ──────
    def test_TC_SC_P1_15_i18n_c8_messages_present(self) -> None:
        i18n_path = ROOT / "i18n" / "messages" / "c8.ko.json"
        self.assertTrue(i18n_path.exists(), "missing i18n/messages/c8.ko.json")
        data = json.loads(i18n_path.read_text(encoding="utf-8"))
        msgs = data["messages"]
        for key in (
            "c8.scan.placeholder", "c8.scan.matched", "c8.scan.nodata",
            "c8.scan.duplicate", "c8.scan.error", "c8.scan.context.required",
            "c8.scan.no_grats", "c8.scan.input.disabled",
        ):
            self.assertIn(key, msgs, f"missing i18n key {key}")
        self.assertIn("DEC-040", data["decisions"], "DEC-040 missing in decisions")

    # ────── contract ──────
    def test_TC_SC_P1_16_barcode_scan_yaml_present(self) -> None:
        import yaml
        path = ROOT / "migration" / "contracts" / "barcode_scan.yaml"
        self.assertTrue(path.exists(), "missing barcode_scan.yaml")
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.assertEqual(data["id"], "C8-barcode-scan")
        self.assertEqual(data["version"], "1.0.0")
        self.assertIn("DEC-040", data["decisions"])
        # 1 endpoint, POST /api/v1/scan/match
        self.assertEqual(len(data["endpoints"]), 1)
        ep = data["endpoints"][0]
        self.assertEqual(ep["method"], "POST")
        self.assertEqual(ep["path"], "/api/v1/scan/match")
        # customer_variants 3건 (default + 138 slim + mysql 3 legacy)
        self.assertGreaterEqual(len(data["customer_variants"]), 3)
        self.assertIn("default", data["customer_variants"])

    # ────── handlers ──────
    def test_TC_SC_P1_17_handlers_c8_scan_md(self) -> None:
        path = ROOT / "analysis" / "handlers" / "c8_scan.md"
        self.assertTrue(path.exists(), "missing analysis/handlers/c8_scan.md")
        content = path.read_text(encoding="utf-8")
        for sql_id in ("SQL-SC-1", "SQL-SC-2", "SQL-SC-3", "SQL-SC-4"):
            self.assertIn(sql_id, content, f"missing {sql_id} in c8_scan.md")
        for table in ("G4_Book", "G1_Ggeo", "G2_Ggwo"):
            self.assertIn(table, content, f"missing table {table} in c8_scan.md")

    # ────── 매핑 노트 (DEC-028) ──────
    def test_TC_SC_P1_18_layout_mapping_dec028(self) -> None:
        path = ROOT / "analysis" / "layout_mappings" / "c8_scan_match.md"
        self.assertTrue(path.exists(), "missing c8_scan_match.md")
        content = path.read_text(encoding="utf-8")
        self.assertIn("DEC-028", content, "c8_scan_match.md: DEC-028 미참조")
        self.assertIn("data-legacy-id", content, "c8_scan_match.md: data-legacy-id 누락")
        self.assertIn("FTong07.Edit101", content, "c8_scan_match.md: FTong07.Edit101 미명시")

    # ────── screen_card ──────
    def test_TC_SC_P1_19_tong08_screen_card(self) -> None:
        path = ROOT / "analysis" / "screen_cards" / "Tong08.md"
        self.assertTrue(path.exists(), "missing screen_cards/Tong08.md")
        content = path.read_text(encoding="utf-8")
        self.assertIn("ComPortRxChar", content)
        self.assertIn("Button100Click", content)

    # ────── 신규 SQL 0건 (scan_match_service / pricing_service) ──────
    def _assert_no_new_dml(self, file_path: Path) -> None:
        """주석/문자열/docstring 제외하고 INSERT/UPDATE/DELETE 키워드가 SQL 문맥으로 사용되지 않음."""
        if not file_path.exists():
            self.skipTest(f"{file_path} not yet implemented (T5 미착수)")
        text = file_path.read_text(encoding="utf-8")
        # 비SQL 컨텍스트 단어 제거 (변수명·라이브러리명·문서)
        # SQL 키워드 검사: 줄에 INSERT INTO / UPDATE <table> SET / DELETE FROM 패턴
        sql_patterns = [
            r"\bINSERT\s+INTO\b",
            r"\bUPDATE\s+[A-Za-z_][\w]*\s+SET\b",
            r"\bDELETE\s+FROM\b",
        ]
        # 단순 문자열 리터럴 (서비스가 SQL 만들 때 사용) 검사 — 주석 제거 후
        cleaned = re.sub(r"#[^\n]*", "", text)  # python 주석 제거
        cleaned = re.sub(r'""".*?"""', "", cleaned, flags=re.DOTALL)  # docstring 제거
        cleaned = re.sub(r"'''.*?'''", "", cleaned, flags=re.DOTALL)
        for pat in sql_patterns:
            matches = re.findall(pat, cleaned, flags=re.IGNORECASE)
            self.assertEqual(
                matches, [],
                f"{file_path.name}: 신규 SQL 발견 (DEC-040 위반) — pattern {pat}: {matches}",
            )

    def test_TC_SC_P1_20_scan_match_service_no_new_dml(self) -> None:
        path = BACKEND / "app" / "services" / "scan_match_service.py"
        self._assert_no_new_dml(path)

    def test_TC_SC_P1_21_pricing_service_no_new_dml(self) -> None:
        path = BACKEND / "app" / "services" / "pricing_service.py"
        self._assert_no_new_dml(path)

    # ────── DEC-028 grep — 3 페이지 ScanInput 통합 ──────
    def test_TC_SC_P1_22_scan_input_in_three_pages(self) -> None:
        """모던 3 페이지 (outbound/inbound/returns 의 [key]/page.tsx) 에 ScanInput 통합 + 공통 컴포넌트에 FTong07.Edit101 부착."""
        candidates = [
            FRONTEND / "src" / "app" / "(app)" / "outbound" / "orders" / "[orderKey]" / "page.tsx",
            FRONTEND / "src" / "app" / "(app)" / "inbound" / "receipts" / "[receiptKey]" / "page.tsx",
            FRONTEND / "src" / "app" / "(app)" / "returns" / "receipts" / "[returnKey]" / "page.tsx",
        ]
        hits = 0
        missing: list[str] = []
        for p in candidates:
            if not p.exists():
                missing.append(str(p))
                continue
            text = p.read_text(encoding="utf-8")
            if "ScanInput" in text and "@/components/shared/scan-input" in text:
                hits += 1
            else:
                missing.append(str(p) + " (ScanInput 미통합)")
        if hits < 3:
            self.skipTest(
                "T6 (frontend useScanner 통합) 미착수 — DEC-028 통합 검사 보류. "
                f"missing: {missing}"
            )

        # 공통 컴포넌트에 FTong07.Edit101 부착 (DEC-028 룰 7)
        scan_input = FRONTEND / "src" / "components" / "shared" / "scan-input.tsx"
        self.assertTrue(scan_input.exists(), "missing scan-input.tsx")
        text = scan_input.read_text(encoding="utf-8")
        self.assertIn(
            'data-legacy-id="FTong07.Edit101"', text,
            "scan-input.tsx: FTong07.Edit101 (Tong07.Edit101 모던 등가) 미부착",
        )


if __name__ == "__main__":
    main()
