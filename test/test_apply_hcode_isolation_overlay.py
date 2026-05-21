"""DSN-DEC-12 — 격리 키 overlay 머지 도구 회귀 가드.

[`tools/apply_hcode_isolation_overlay.py`](../tools/apply_hcode_isolation_overlay.py)
의 ``_normalize_filled_template`` 와 ``_merge_overlay`` 만 픽스처로 검증한다.
실제 ``backend/data/tenants_directory_overlay.json`` 파일 IO는 본 가드에서 다루지 않는다 — SRP.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from unittest import TestCase, main


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "apply_hcode_isolation_overlay.py"


def _load_tool():
    spec = importlib.util.spec_from_file_location(
        "apply_hcode_isolation_overlay", TOOL_PATH
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("apply_hcode_isolation_overlay", mod)
    spec.loader.exec_module(mod)
    return mod


_SEED = {
    "tenants": [
        {
            "tenant_id": "TID-WELOVE3",
            "tenant_label_kor": "위러브3",
            "account_family": "chul_09",
            "primary_server": "서버3",
            "db_name_logical": "chul_09_db",
            "is_active": True,
        },
        {
            "tenant_id": "TID-KMS",
            "tenant_label_kor": "교문사",
            "account_family": "chul_09",
            "primary_server": "서버3",
            "db_name_logical": "chul_09_db",
            "is_active": True,
        },
    ]
}


class NormalizeFilledTemplateTests(TestCase):
    def setUp(self) -> None:
        self.tool = _load_tool()
        self.seed_lookup = self.tool._seed_lookup(_SEED)

    def test_skip_unfilled_rows(self):
        filled = {
            "candidates": [
                {
                    "sme_mapping_template": {
                        "TID-WELOVE3": {
                            "hcode_in": [],
                            "hcode_pattern": "",
                            "hcode_prefix": "",
                            "parent_tenant_id": "",
                        }
                    }
                }
            ]
        }
        rows = self.tool._normalize_filled_template(filled, self.seed_lookup)
        self.assertEqual(rows, [])

    def test_hcode_in_emitted_with_account_family(self):
        filled = {
            "candidates": [
                {
                    "sme_mapping_template": {
                        "TID-WELOVE3": {
                            "hcode_in": ["W3-001", "W3-002", " "],  # 빈 항목 strip
                        },
                        "TID-KMS": {
                            "hcode_pattern": r"^KMS-\d+$",
                        },
                    }
                }
            ]
        }
        rows = self.tool._normalize_filled_template(filled, self.seed_lookup)
        rows_by_tid = {r["tenant_id"]: r for r in rows}
        self.assertIn("TID-WELOVE3", rows_by_tid)
        self.assertEqual(rows_by_tid["TID-WELOVE3"]["hcode_in"], ["W3-001", "W3-002"])
        self.assertEqual(rows_by_tid["TID-WELOVE3"]["account_family"], "chul_09")
        self.assertEqual(rows_by_tid["TID-KMS"]["hcode_pattern"], r"^KMS-\d+$")

    def test_unknown_tenant_id_skipped_with_warning(self):
        filled = {
            "candidates": [
                {
                    "sme_mapping_template": {
                        "TID-UNKNOWN": {"hcode_in": ["X"]},
                    }
                }
            ]
        }
        rows = self.tool._normalize_filled_template(filled, self.seed_lookup)
        self.assertEqual(rows, [])


class MergeOverlayTests(TestCase):
    def setUp(self) -> None:
        self.tool = _load_tool()

    def test_merge_overrides_isolation_keys_only(self):
        existing = [
            {
                "tenant_id": "TID-WELOVE3",
                "account_family": "chul_09",
                "notes": "운영자 메모 보존",
                "hcode_in": ["OLD"],
            }
        ]
        incoming = [
            {
                "tenant_id": "TID-WELOVE3",
                "account_family": "chul_09",
                "hcode_in": ["NEW1", "NEW2"],
                "_dsn_dec_12": True,
            }
        ]
        merged = self.tool._merge_overlay(existing, incoming)
        self.assertEqual(len(merged), 1)
        row = merged[0]
        self.assertEqual(row["hcode_in"], ["NEW1", "NEW2"])
        self.assertEqual(row["notes"], "운영자 메모 보존")  # 기존 비격리 필드 보존
        self.assertTrue(row["_dsn_dec_12"])

    def test_merge_appends_new_row(self):
        existing = [
            {"tenant_id": "TID-WELOVE3", "account_family": "chul_09", "hcode_in": ["X"]}
        ]
        incoming = [
            {"tenant_id": "TID-KMS", "account_family": "chul_09", "hcode_pattern": "^K"}
        ]
        merged = self.tool._merge_overlay(existing, incoming)
        self.assertEqual(len(merged), 2)
        tids = {r["tenant_id"] for r in merged}
        self.assertSetEqual(tids, {"TID-WELOVE3", "TID-KMS"})


if __name__ == "__main__":
    main()
