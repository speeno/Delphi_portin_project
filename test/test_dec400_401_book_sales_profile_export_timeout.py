"""DEC-400 · DEC-401 — 도서별판매 레거시 불일치(교문사 경리부) · 엑셀 저장 AbortError (2026-10-13).

DEC-400 「원장관리 - 도서별판매 1900-01-01~2026.10.10: 북이오웍스 · 위러브솔루션 자료가 다르다」
  웹 반품 −1,373,376 · 폐기 −326,231 · 반품액 −21,883,528,287 ↔ 레거시 −1,373,369 · −633,388 · −21,883,637,347.
  운영 DB 재계산: 유통 규칙 = 웹 값, 출판 규칙 = 레거시 값(정확히 일치) — 빠진 것은 Scode Z · Gubun 「폐기」 6,747줄 −307,150부.
  chul_09_db 로그인은 소유성 ambiguous(DSN-DEC-12) → account_family 가 비어 출판 규칙 변형(DEC-372)에 매칭되지 않았다.
DEC-401 「엑셀 다운로드 시 오류」 — 전 기간 엑셀이 서버에서 31 · 34초, 내려받기 기본 대기 30초라 브라우저가 끊었다.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from app.services import reports_service as rs
from app.services import sales_classify_profile as scp

ROOT = Path(__file__).resolve().parents[1]
FE = ROOT / "도서물류관리프로그램" / "frontend" / "src"
HUB_CONTRACT = ROOT / "migration" / "contracts" / "sales_classification.yaml"
BUNDLE_CONTRACT = ROOT / "도서물류관리프로그램" / "backend" / "data" / "contracts" / "sales_classification.yaml"


class ProfileByVerifiedDb(unittest.TestCase):
    def setUp(self) -> None:
        scp.reload_for_tests()

    def tearDown(self) -> None:
        scp.reload_for_tests()

    def test_ambiguous_ownership_login_on_chul_09_db_is_publisher(self) -> None:
        ctx = {"hcode": "5019", "user_id": "경리부", "account_family": "", "resolved_db": "chul_09_db"}
        self.assertEqual(scp.resolve_sales_classify_profile(ctx), "publisher")
        self.assertEqual(scp.resolve_sales_classify_profile({"rdb": "chul_09_db"}), "publisher")  # JWT 키
        self.assertEqual(scp.resolve_sales_classify_profile({"account_family": "chul_09"}), "publisher")  # 종전 변형 유지

    def test_other_dbs_stay_distributor(self) -> None:
        for ctx in ({}, {"resolved_db": "chul_21_db"}, {"account_family": "chul_21", "resolved_db": "book_99_db"}):
            self.assertEqual(scp.resolve_sales_classify_profile(ctx), "distributor", ctx)

    def test_contract_copies_identical(self) -> None:
        self.assertEqual(HUB_CONTRACT.read_text(encoding="utf-8"), BUNDLE_CONTRACT.read_text(encoding="utf-8"))
        self.assertIn("resolved_db: chul_09_db", HUB_CONTRACT.read_text(encoding="utf-8"))


def _total(rows: list[tuple[str, str, str, int, int]], profile: str) -> dict[str, int]:
    scp._request_profile.set(profile)
    cell = {k: 0 for k in ("giqut", "gisum", "gbqut", "gpqut", "gjqut", "goqut", "gosum", "gbsum", "gpsum")}
    for scode, gubun, pubun, q, s in rows:
        rs._apply_book_sales_branch(cell, scode=scode, gubun=gubun, pubun=pubun, gsqut=q, gssum=s)
    return cell


class LegacyTotals(unittest.TestCase):
    """운영 실측 묶음(교문사 5019 · 1900.01.01~2026.10.10)에서 차이를 만든 줄만 — 규칙에 따라 폐기 칸이 달라진다."""

    ROWS = [
        ("Z", "폐기", "정품", -307150, -3449650),      # Gubun 폐기 — 출판 규칙만 폐기 칸
        ("Z", "반품", "폐기", -264567, -2331659587),   # Pubun 폐기 — 두 규칙 모두 폐기 칸
        ("Z", "반품", "폐기", -61664, -989040675),
        ("Z", "반품", "반품", -554, -8974200),
    ]

    def tearDown(self) -> None:
        scp.reload_for_tests()

    def test_publisher_counts_gubun_waste(self) -> None:
        self.assertEqual(_total(self.ROWS, "distributor")["gpqut"], -326231)  # 웹 화면 값
        self.assertEqual(_total(self.ROWS, "publisher")["gpqut"], -633381)    # + Gubun 폐기 −307,150


class DownloadTimeout(unittest.TestCase):
    def test_get_blob_waits_three_minutes_and_explains_timeout(self) -> None:
        src = (FE / "lib" / "api-client.ts").read_text(encoding="utf-8")
        self.assertIn("const DOWNLOAD_TIMEOUT_MS = 180_000;", src)
        body = src.split("getBlob: async (path: string, opts?: FetchOptions): Promise<Blob> => {", 1)[1].split("\n  },", 1)[0]
        self.assertIn("const limitMs = timeout ?? DOWNLOAD_TIMEOUT_MS;", body)
        self.assertIn('err.name === "AbortError"', body)
        page = (FE / "app" / "(app)" / "reports" / "book-sales" / "page.tsx").read_text(encoding="utf-8")
        self.assertIn("setError(formatApiError(e)); // DEC-401", page)


if __name__ == "__main__":
    unittest.main()
