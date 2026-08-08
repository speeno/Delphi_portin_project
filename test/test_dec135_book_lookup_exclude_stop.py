"""DEC-135 — 도서 검색 다이얼로그 '출고정지 제외' 옵션 + 계정별 기억 회귀 가드.

출고정지 = G4_Book.Grat9 (레거시 Sobo14.CheckBox2). 검색 다이얼로그(book kind)에
체크박스를 추가하고 `mlf_book_exclude_stop_v1:{serverId}` localStorage 로 기억.
백엔드는 도서 마스터 목록의 기존 `excludeShippingStop` 파라미터 재사용.
반품/마스터 편집 등 정지 도서가 필요한 업무가 있어 강제 아님(옵션).
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "도서물류관리프로그램" / "frontend"
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))


class LookupConfigTests(TestCase):
    def setUp(self) -> None:
        self.src = (FRONTEND / "src/lib/master-lookup-config.ts").read_text("utf-8")

    def test_book_has_filter_option_with_storage_key(self) -> None:
        self.assertIn('label: "출고정지 제외"', self.src)
        self.assertIn("mlf_book_exclude_stop_v1", self.src)

    def test_book_search_passes_param(self) -> None:
        self.assertIn("excludeShippingStop: excludeShippingStop || undefined", self.src)


class LookupDialogTests(TestCase):
    def setUp(self) -> None:
        self.src = (
            FRONTEND / "src/components/master/master-lookup-dialog.tsx"
        ).read_text("utf-8")

    def test_persists_per_account(self) -> None:
        self.assertIn("${filterOpt.storageKey}:${user?.server_id", self.src)
        self.assertIn("localStorage.setItem(filterStorageKey", self.src)

    def test_open_restores_saved_filter_before_first_search(self) -> None:
        # 열 때 저장값을 읽어 **첫 검색에 직접 전달** — setState 반영 지연으로 첫
        # 검색이 필터 없이 나가는 레이스 방지.
        self.assertIn("const savedFilter = readSavedFilter();", self.src)
        self.assertIn("doSearchWith(seed, 0, initialLimit, savedFilter)", self.src)

    def test_toggle_researches_with_next_value(self) -> None:
        self.assertIn("doSearchWith(q, 0, nextLimit, next)", self.src)
        self.assertIn("CommonLookupDialog.FilterOption", self.src)


class BackendClauseTests(TestCase):
    def test_masters_service_grat9_clause(self) -> None:
        src = (
            ROOT / "도서물류관리프로그램" / "backend" / "app" / "services" / "masters_service.py"
        ).read_text("utf-8")
        self.assertIn("IFNULL(Grat9,'') NOT IN ('1','True','true')", src)


if __name__ == "__main__":
    main()
