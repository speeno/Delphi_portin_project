"""거래명세서 테넌트 도장 저장소 회귀 테스트."""
from __future__ import annotations

import base64
import os
import tempfile
import unittest
from pathlib import Path


_MINI_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8"
    "z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==",
)


def _png_with_dimensions(width: int, height: int) -> bytes:
    raw = bytearray(_MINI_PNG)
    raw[16:20] = width.to_bytes(4, "big")
    raw[20:24] = height.to_bytes(4, "big")
    return bytes(raw)


class TenantPrintAssetsTests(unittest.TestCase):
    def test_save_read_delete_seal(self) -> None:
        from app.services import tenant_print_assets

        with tempfile.TemporaryDirectory() as td:
            os.environ["BLS_TENANT_PRINT_ASSETS_DIR"] = str(Path(td) / "assets")
            os.environ["BLS_TENANT_PRINT_META_PATH"] = str(Path(td) / "meta.json")
            try:
                meta = tenant_print_assets.save_seal_bytes("remote/138", _MINI_PNG)
                self.assertEqual(meta["filename"], "sales_statement_seal.png")
                self.assertTrue(tenant_print_assets.seal_bytes_exist("remote/138"))
                self.assertEqual(tenant_print_assets.read_seal_bytes("remote/138"), _MINI_PNG)
                self.assertIsNotNone(tenant_print_assets.seal_meta_snapshot("remote/138"))

                tenant_print_assets.delete_seal("remote/138")
                self.assertFalse(tenant_print_assets.seal_bytes_exist("remote/138"))
                self.assertIsNone(tenant_print_assets.seal_meta_snapshot("remote/138"))
            finally:
                os.environ.pop("BLS_TENANT_PRINT_ASSETS_DIR", None)
                os.environ.pop("BLS_TENANT_PRINT_META_PATH", None)

    def test_rejects_large_dimensions_without_pillow(self) -> None:
        from app.services import tenant_print_assets

        with tempfile.TemporaryDirectory() as td:
            os.environ["BLS_TENANT_PRINT_ASSETS_DIR"] = str(Path(td) / "assets")
            os.environ["BLS_TENANT_PRINT_META_PATH"] = str(Path(td) / "meta.json")
            try:
                with self.assertRaises(ValueError):
                    tenant_print_assets.save_seal_bytes(
                        "remote_138",
                        _png_with_dimensions(999, 1),
                    )
            finally:
                os.environ.pop("BLS_TENANT_PRINT_ASSETS_DIR", None)
                os.environ.pop("BLS_TENANT_PRINT_META_PATH", None)


if __name__ == "__main__":
    unittest.main()
