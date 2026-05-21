"""DSN-DEC-12 보조 — Config.Ini 인벤토리 도구 회귀 가드."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from unittest import TestCase, main


ROOT = Path(__file__).resolve().parents[1]
TOOL_PATH = ROOT / "tools" / "inventory_legacy_config_ini.py"


def _load_tool():
    spec = importlib.util.spec_from_file_location(
        "inventory_legacy_config_ini", TOOL_PATH
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("inventory_legacy_config_ini", mod)
    spec.loader.exec_module(mod)
    return mod


class ParseIniTests(TestCase):
    def setUp(self) -> None:
        self.tool = _load_tool()

    def test_parses_client_section_with_korean_value(self):
        text = (
            "[Client]\n"
            "Name=도서유통-총판\n"
            "Uses=Client01\n"
            "Base=D:\\Chul-Data\\PubBook\\Chul2002.GDB\n"
            "PORT=6000\n"
            "PCIP1=korea-v6psam44\n"
            "UserName=MA==\n"
            "Password=MA==\n"
            "\n[Remote]\n"
            "Code=P58\n"
        )
        parsed = self.tool.parse_ini(text)
        self.assertEqual(parsed["Client"]["Name"], "도서유통-총판")
        self.assertEqual(parsed["Client"]["Uses"], "Client01")
        self.assertEqual(parsed["Remote"]["Code"], "P58")

    def test_parse_ignores_comments_and_blank(self):
        text = "; comment\n# also\n[Client]\nName=AA\n"
        parsed = self.tool.parse_ini(text)
        self.assertEqual(parsed, {"Client": {"Name": "AA"}})


class SecretsPolicyTests(TestCase):
    def setUp(self) -> None:
        self.tool = _load_tool()

    def test_username_and_password_excluded_from_row(self, tmp_path: Path = None):  # type: ignore[assignment]
        tmp_path = tmp_path or Path("/tmp/test_inventory_legacy_config_ini")
        tmp_path.mkdir(parents=True, exist_ok=True)
        cfg = tmp_path / "Config.Ini"
        cfg.write_text(
            "[Client]\nName=AA\nUses=BB\nUserName=cred1\nPassword=cred2\n",
            encoding="utf-8",
        )
        try:
            row = self.tool._client_row(cfg, tmp_path)
            self.assertEqual(row["name"], "AA")
            self.assertEqual(row["uses"], "BB")
            self.assertNotIn("username", row.get("_client_keys", []))
            self.assertNotIn("password", row.get("_client_keys", []))
            for v in row.values():
                if isinstance(v, str):
                    self.assertNotIn("cred1", v)
                    self.assertNotIn("cred2", v)
        finally:
            cfg.unlink(missing_ok=True)


class LabelMatchTests(TestCase):
    def setUp(self) -> None:
        self.tool = _load_tool()

    def test_partial_match_handles_parens(self):
        pool = {self.tool._normalize_label("교문사")}
        self.assertTrue(self.tool._label_match("(주)교문사", pool))
        self.assertTrue(self.tool._label_match("교문사 (Pub)", pool))

    def test_diff_marks_unmatched(self):
        inv = [
            {"config_path": "p1", "name": "(주)교문사", "uses": "U1"},
            {"config_path": "p2", "name": "전혀다른업체", "uses": "U2"},
        ]
        diff = self.tool.build_diff(
            inv,
            seed_labels={"교문사"},
            matrix_labels=set(),
        )
        self.assertEqual(diff["summary"]["missing_label_match"], 1)
        self.assertEqual(diff["missing_label_match"][0]["config_path"], "p2")


if __name__ == "__main__":
    main()
