"""
C7 비-FastReport 트랙 — `.frf → IR` 디코더 PoC 회귀 테스트 (R2 단계).

본 테스트는 [c7-nofr-porting](../) 계획의 § "2) FRF Decoder PoC (1양식)" 의 DoD 게이트.

검증 항목:
  - T_01 IR JSON 가 `analysis/print_specs/frf_ir_schema.md` v0.1.0 의 최상위 키 구조 충족
  - T_02 Report_1_21.frf 디코딩 결과에 라벨용 데이터 토큰 (Gname/Gposa/Gadd1/Gadd2/Gpost)
        5 종이 expressions_dictionary 에 모두 등록됨
  - T_03 Memo* (text 객체) 가 *최소 5 개 이상* 식별됨 (수동 정본 P1-F 대조)
  - T_04 unsupported_objects[] 와 decoder_warnings[] 키가 정상 존재 (실패-허용 정책)
  - T_05 단일 토큰 `[Gname]` 이 expression / field 로 분류됨 (literal 아님)
  - T_06 비현실 좌표는 unsupported_props.rect_extraction = 'out_of_range_v0' 로 마크
  - L_01 디코더 헤더 주석에 BSD-2 저작권 표시가 포함되어 있음 (라이선스 매트릭스 §2.1)
  - L_02 IR 스키마 / shortlist / license matrix 3 산출물 존재 (OSS 게이트 종료조건)
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from debug import frf_decoder_poc  # noqa: E402


SAMPLE_FRF = (
    REPO_ROOT
    / "legacy_delphi_source"
    / "legacy_source"
    / "Report"
    / "Report_1_21.frf"
)


class FrfDecoderPoCTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not SAMPLE_FRF.is_file():
            raise unittest.SkipTest(f"sample frf missing: {SAMPLE_FRF}")
        cls.ir = frf_decoder_poc.decode_frf(SAMPLE_FRF)

    def test_T_01_top_level_schema_keys(self) -> None:
        required = {
            "schema_version",
            "source",
            "report",
            "pages",
            "data_sources",
            "expressions_dictionary",
            "variant_profile",
            "unsupported_objects",
            "decoder_warnings",
        }
        self.assertTrue(required.issubset(self.ir.keys()), msg=f"missing: {required - self.ir.keys()}")
        self.assertEqual(self.ir["schema_version"], frf_decoder_poc.SCHEMA_VERSION)
        self.assertEqual(self.ir["source"]["kind"], "frf")
        self.assertGreaterEqual(len(self.ir["pages"]), 1)

    def test_T_02_label_tokens_in_expressions_dict(self) -> None:
        keys = set(self.ir["expressions_dictionary"].keys())
        expected = {"[Gname]", "[Gposa]", "[Gadd1]", "[Gadd2]", "[Gpost]"}
        missing = expected - keys
        self.assertFalse(missing, msg=f"label tokens missing: {missing} (got {keys})")

    def test_T_03_at_least_five_text_objects_identified(self) -> None:
        page = self.ir["pages"][0]
        text_objects = [
            obj
            for band in page["bands"]
            for obj in band["objects"]
            if obj["type"] == "Text"
        ]
        self.assertGreaterEqual(len(text_objects), 5, msg=f"got {len(text_objects)} text objects")

    def test_T_04_failure_tolerant_policy_present(self) -> None:
        self.assertIsInstance(self.ir["unsupported_objects"], list)
        self.assertIsInstance(self.ir["decoder_warnings"], list)

    def test_T_05_single_token_classified_as_field(self) -> None:
        page = self.ir["pages"][0]
        gname_obj = None
        for band in page["bands"]:
            for obj in band["objects"]:
                if obj.get("binding", {}).get("raw") == "[Gname]":
                    gname_obj = obj
                    break
            if gname_obj is not None:
                break
        self.assertIsNotNone(gname_obj, "object with [Gname] binding not found")
        binding = gname_obj["binding"]
        self.assertEqual(binding["kind"], "expression")
        self.assertTrue(any(t["type"] == "field" for t in binding["tokens"]))

    def test_T_06_out_of_range_rect_marked(self) -> None:
        page = self.ir["pages"][0]
        marked = [
            obj
            for band in page["bands"]
            for obj in band["objects"]
            if obj["unsupported_props"].get("rect_extraction") in {"failed_v0", "out_of_range_v0"}
        ]
        self.assertGreaterEqual(
            len(marked),
            1,
            msg="PoC v0 휴리스틱 한계 — 일부 객체는 좌표 추출 실패가 예상되며 마킹돼야 함",
        )

    def test_L_01_decoder_header_has_bsd2_notice(self) -> None:
        header = (REPO_ROOT / "debug" / "frf_decoder_poc.py").read_text(encoding="utf-8")[:3000]
        for token in ("BSD-2", "Fast Reports", "Redistribution"):
            self.assertIn(token, header, msg=f"BSD-2 notice token missing: {token}")

    def test_L_02_oss_gate_deliverables_exist(self) -> None:
        for rel in (
            "analysis/research/c7_oss_discovery_log_20260420.md",
            "analysis/research/c7_oss_shortlist.md",
            "analysis/research/c7_oss_license_matrix.md",
            "analysis/print_specs/frf_ir_schema.md",
        ):
            path = REPO_ROOT / rel
            self.assertTrue(path.is_file(), msg=f"missing OSS gate deliverable: {rel}")
            self.assertGreater(path.stat().st_size, 1000, msg=f"too small: {rel}")


class FrfDecoderTokenizerTest(unittest.TestCase):
    def test_field_with_table(self) -> None:
        tokens = frf_decoder_poc._tokenize_frf_text("[Employees.LastName]")
        self.assertEqual(len(tokens), 1)
        self.assertEqual(tokens[0]["type"], "field")
        self.assertEqual(tokens[0]["table"], "Employees")
        self.assertEqual(tokens[0]["column"], "LastName")

    def test_field_with_format(self) -> None:
        tokens = frf_decoder_poc._tokenize_frf_text('[Sales.Date "yyyy-mm-dd"]')
        self.assertEqual(tokens[0]["type"], "field")
        self.assertEqual(tokens[0]["format_spec"], "yyyy-mm-dd")

    def test_simple_token_treated_as_field(self) -> None:
        tokens = frf_decoder_poc._tokenize_frf_text("[Gname]")
        self.assertEqual(tokens[0]["type"], "field")
        self.assertIsNone(tokens[0]["table"])
        self.assertEqual(tokens[0]["column"], "Gname")

    def test_function_token(self) -> None:
        tokens = frf_decoder_poc._tokenize_frf_text("[PageN]")
        self.assertEqual(tokens[0]["type"], "function")
        self.assertEqual(tokens[0]["name"], "PageN")

    def test_none_literal_emptied(self) -> None:
        tokens = frf_decoder_poc._tokenize_frf_text("[None]")
        self.assertEqual(tokens[0]["type"], "literal")
        self.assertEqual(tokens[0]["value"], "")

    def test_mixed_literal_and_field(self) -> None:
        tokens = frf_decoder_poc._tokenize_frf_text("총 [Sales.Amount] 원")
        kinds = [t["type"] for t in tokens]
        self.assertIn("literal", kinds)
        self.assertIn("field", kinds)


if __name__ == "__main__":
    unittest.main()
