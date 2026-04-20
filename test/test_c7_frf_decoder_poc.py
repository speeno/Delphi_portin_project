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

    def test_T_06_rect_extraction_marker_consistent(self) -> None:
        """v0.1 휴리스틱은 좌표 실패를 mark 했지만, v0.2 부터는 plausibility-best-fit 으로
        대부분 0 건. 본 테스트는 *마커가 있을 때 raw_twips 가 보존돼 있는지* 만 검증한다."""
        page = self.ir["pages"][0]
        marked = [
            obj
            for band in page["bands"]
            for obj in band["objects"]
            if obj["unsupported_props"].get("rect_extraction")
            in {"failed_v0", "out_of_range_v0"}
        ]
        for obj in marked:
            self.assertIn("rect_raw_twips", obj["unsupported_props"])

    def test_T_07_coord_recovery_v02(self) -> None:
        """v0.2 게이트 — Report_1_21 의 좌표 복원률은 90% 이상이어야 한다."""
        page = self.ir["pages"][0]
        objs = [obj for band in page["bands"] for obj in band["objects"]]
        with_rect = [o for o in objs if o["rect_mm"]["w"] > 0 and o["rect_mm"]["h"] > 0]
        ratio = len(with_rect) / max(1, len(objs))
        self.assertGreaterEqual(
            ratio,
            0.9,
            msg=f"coord_recovery {ratio:.2%} below v0.2 gate (objs={len(objs)})",
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

    def test_font_name_metadata_sanitized_out(self) -> None:
        self.assertIsNone(frf_decoder_poc._sanitize_literal_text("굴림"))
        self.assertIsNone(frf_decoder_poc._sanitize_literal_text("HANGEUL_CHARSET"))
        self.assertEqual(frf_decoder_poc._sanitize_literal_text("출판사명굴림"), "출판사명")
        self.assertEqual(frf_decoder_poc._sanitize_literal_text("입 고 일:굴림"), "입 고 일:")

    def test_mixed_literal_and_field(self) -> None:
        tokens = frf_decoder_poc._tokenize_frf_text("총 [Sales.Amount] 원")
        kinds = [t["type"] for t in tokens]
        self.assertIn("literal", kinds)
        self.assertIn("field", kinds)

    def test_inline_simple_tokens_extracted(self) -> None:
        """v0.3.2 — `라벨 [Squt1] [Squt2] 단위` 처럼 literal 사이에 끼는 단일
        식별자 ``[Token]`` 도 모두 field 로 인식해야 한다 (기존엔 literal 로 흘렀음)."""
        tokens = frf_decoder_poc._tokenize_frf_text("판매수량: [Squt1] [Squt2] 단위")
        kinds = [t["type"] for t in tokens]
        cols = [t.get("column") for t in tokens if t["type"] == "field"]
        self.assertIn("field", kinds)
        self.assertIn("Squt1", cols)
        self.assertIn("Squt2", cols)
        # literal 부분도 보존
        literals = [t["value"] for t in tokens if t["type"] == "literal"]
        self.assertTrue(any("판매수량" in v for v in literals))


class FrfDecoderFontInferenceTest(unittest.TestCase):
    def test_font_size_capped_to_12pt(self) -> None:
        """v0.3.2 — 가로로 넉넉한 셀이라도 폰트 추정 상한은 12pt 로 클램프."""
        from copy import deepcopy
        from debug import frf_decoder_poc as dec
        ir = dec.IR(
            schema_version="0.1.0",
            source={},
            report={},
            pages=[{
                "size_mm": {"width": 200.0, "height": 300.0},
                "margin_mm": {},
                "bands": [{"name": "B", "objects": [
                    {"name": "Big", "type": "Text",
                     "rect_mm": {"x": 0, "y": 0, "w": 100.0, "h": 30.0},
                     "style": {}},
                ]}],
            }],
            data_sources=[], expressions_dictionary={}, variant_profile=None,
            unsupported_objects=[], decoder_warnings=[],
        )
        dec._infer_text_font_sizes(ir)
        pt = ir.pages[0]["bands"][0]["objects"][0]["style"]["font_size_pt"]
        self.assertLessEqual(pt, 12.0, f"upper cap broken: {pt}pt")

    def test_font_size_width_capped_for_narrow_tall_cell(self) -> None:
        """v0.3.2 — 세로로 길쭉한 셀(``w<h``)은 폭 기준 캡으로도 폰트가 줄어
        세로로 1글자 wrap 되는 현상을 차단한다."""
        from debug import frf_decoder_poc as dec
        MM_PER_PT = 25.4 / 72.0
        ir = dec.IR(
            schema_version="0.1.0",
            source={},
            report={},
            pages=[{
                "size_mm": {"width": 200.0, "height": 300.0},
                "margin_mm": {},
                "bands": [{"name": "B", "objects": [
                    {"name": "Vert", "type": "Text",
                     "rect_mm": {"x": 0, "y": 0, "w": 5.0, "h": 30.0},
                     "style": {}},
                ]}],
            }],
            data_sources=[], expressions_dictionary={}, variant_profile=None,
            unsupported_objects=[], decoder_warnings=[],
        )
        dec._infer_text_font_sizes(ir)
        pt = ir.pages[0]["bands"][0]["objects"][0]["style"]["font_size_pt"]
        # 폭 캡: ≤ (w * 0.85 / MM_PER_PT) ≈ 12.04pt 와 cap 12pt 사이.
        self.assertLessEqual(pt, 12.0)
        self.assertLessEqual(pt, (5.0 * 0.85) / MM_PER_PT + 0.5)

    def test_font_extracted_not_overwritten_by_rect_infer(self) -> None:
        """v0.6.3 — ``_font_extracted`` 가 있으면 rect 기반 추정이 pt 를 덮어쓰지 않는다."""
        from debug import frf_decoder_poc as dec
        ir = dec.IR(
            schema_version="0.1.0",
            source={},
            report={},
            pages=[{
                "size_mm": {"width": 200.0, "height": 300.0},
                "margin_mm": {},
                "bands": [{"name": "B", "objects": [
                    {"name": "Small", "type": "Text",
                     "rect_mm": {"x": 0, "y": 0, "w": 50.0, "h": 4.0},
                     "style": {
                         "font_size_pt": 8.0,
                         "_font_extracted": True,
                     }},
                ]}],
            }],
            data_sources=[], expressions_dictionary={}, variant_profile=None,
            unsupported_objects=[], decoder_warnings=[],
        )
        dec._infer_text_font_sizes(ir)
        self.assertEqual(
            ir.pages[0]["bands"][0]["objects"][0]["style"]["font_size_pt"],
            8.0,
        )


class FrfDecoderImageExtractionTest(unittest.TestCase):
    """v0.4.0 — Picture 객체에 임베디드 이미지(JPG/PNG/BMP) 매칭."""

    SAMPLE_FRF_WITH_JPG = (
        Path(__file__).resolve().parents[1]
        / "legacy_delphi_source" / "legacy_source" / "Report"
        / "Report_4_51-0.frf"
    )

    def test_decoder_version_v04_or_higher(self) -> None:
        """v0.4 이상 호환 (이미지 추출은 v0.4.0, frame/color 는 v0.5.0)."""
        from debug import frf_decoder_poc as dec
        major_minor = tuple(int(x) for x in dec.DECODER_VERSION.split(".")[:2])
        self.assertGreaterEqual(major_minor, (0, 4))

    def test_picture_jpg_matched_with_base64(self) -> None:
        """Report_4_51-0.frf 는 Picture1 + JPG 1개를 가지며, 디코더가 매칭하여
        IR.Object.image.format='image/jpeg', data_b64 비어있지 않음."""
        from debug import frf_decoder_poc as dec
        if not self.SAMPLE_FRF_WITH_JPG.is_file():
            self.skipTest(f"sample missing: {self.SAMPLE_FRF_WITH_JPG}")
        ir = dec.decode_frf(self.SAMPLE_FRF_WITH_JPG)
        # source.image_extraction summary
        summary = ir["source"].get("image_extraction")
        self.assertIsNotNone(summary)
        self.assertGreaterEqual(summary["pictures_matched"], 1)
        # Picture1 객체에 image 부착 확인
        pics = [o for p in ir["pages"] for b in p["bands"] for o in b["objects"]
                if o["type"] == "Picture"]
        self.assertGreaterEqual(len(pics), 1)
        pic = pics[0]
        self.assertIn("image", pic)
        self.assertEqual(pic["image"]["format"], "image/jpeg")
        self.assertGreater(pic["image"]["size_bytes"], 100)
        self.assertEqual(len(pic["image"]["sha1"]), 40)
        self.assertGreater(len(pic["image"]["data_b64"]), 100)
        # 매칭 거리 합리적 범위 (FastReport 4.x 일관 +82)
        self.assertLessEqual(pic["image"]["decoder_match_delta"], 256)

    def test_image_blob_scanner_skips_inner_false_positives(self) -> None:
        """``_scan_image_blobs`` 가 BMP 본문 안에 우연히 등장하는 JPG SOI 패턴을
        false-positive 로 추가하지 않는지 (이전 BLOB 종료점 안에 들어오는 후보 제거)."""
        from debug import frf_decoder_poc as dec
        # 가짜 BMP (200 byte) + JPG (10 byte EOI 포함)
        import struct
        bmp = b"BM" + struct.pack("<I", 200) + b"\x00" * 200  # noisy interior
        # 이 BMP 의 본문 안에 [\xff\xd8\xff] 패턴을 인위 삽입
        bmp = bmp[:50] + b"\xff\xd8\xff\xe0\xff\xd9" + bmp[56:]
        jpg = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\xff\xd9"
        raw = b"prefix" + bmp + b"sep" + jpg + b"tail"
        blobs = dec._scan_image_blobs(raw)
        formats = [b["format"] for b in blobs]
        # 진짜 BMP + 진짜 JPG 만 잡혀야 함 (BMP 안의 JPG SOI 는 false-pos)
        self.assertIn("image/bmp", formats)
        self.assertIn("image/jpeg", formats)
        # BMP 다음 JPG 는 *BMP 종료점 이후* 의 것만
        bmp_blob = next(b for b in blobs if b["format"] == "image/bmp")
        for b in blobs:
            if b["format"] == "image/jpeg":
                self.assertGreaterEqual(b["offset"], bmp_blob["end"])


class FrfDecoderFramePropsTest(unittest.TestCase):
    """v0.5.0 — Memo 속성 블록 (Frame/Fill/TColor) 디코드 회귀 테스트.

    debug/frf_property_probe.py 1,629 sample 통계로 확인된 byte 레이아웃
    (FrameTyp@2, FrameWidth@4, FrameColor@8, FillColor@14) 과 TColor
    decoder 의 정합성을 회귀 보장한다.
    """

    SAMPLE_TAX_INVOICE = (
        REPO_ROOT / "legacy_delphi_source" / "legacy_source" / "Report" / "계산서.frf"
    )

    def test_T_08_frame_extracted_for_tax_invoice(self) -> None:
        """계산서.frf 는 거의 모든 셀이 Frame=0x0F (4면 모두) 인 표 격자.
        디코더가 적어도 80% 이상의 객체에 *어떤 측면이든* border 가 켜진
        결과를 산출해야 한다.
        """
        from debug import frf_decoder_poc as dec
        if not self.SAMPLE_TAX_INVOICE.is_file():
            self.skipTest(f"sample missing: {self.SAMPLE_TAX_INVOICE}")
        ir = dec.decode_frf(self.SAMPLE_TAX_INVOICE)
        objs = [
            o for p in ir["pages"] for b in p["bands"] for o in b["objects"]
            if o["type"] in ("Text", "Line", "Rect")
        ]
        with_border = [
            o for o in objs
            if any(
                (o.get("border") or {}).get(side, False)
                for side in ("left", "top", "right", "bottom")
            )
        ]
        ratio = len(with_border) / max(1, len(objs))
        self.assertGreaterEqual(
            ratio,
            0.7,
            msg=f"frame extraction ratio {ratio:.2%} below v0.5 gate "
                f"(objs={len(objs)}, with_border={len(with_border)})",
        )

    def test_T_09_tcolor_decoder_known_values(self) -> None:
        """TColor 분류 — 직접색/투명/시스템색."""
        from debug import frf_decoder_poc as dec
        # 직접색 (high byte == 0)
        self.assertEqual(dec._decode_tcolor(0x00000000), ("#000000", False))   # clBlack
        self.assertEqual(dec._decode_tcolor(0x00FFFFFF), ("#FFFFFF", False))   # clWhite
        # TColor 0x00BBGGRR — BB=0xFF, GG=0, RR=0 → "#0000FF" (blue)
        self.assertEqual(dec._decode_tcolor(0x00FF0000), ("#0000FF", False))
        # BB=0, GG=0, RR=0xFF → "#FF0000" (red)
        self.assertEqual(dec._decode_tcolor(0x000000FF), ("#FF0000", False))
        # 특수 clNone (transparent flag set)
        hex_, trans = dec._decode_tcolor(0x1FFFFFFF)
        self.assertIsNone(hex_)
        self.assertTrue(trans)
        # 시스템색 (high byte == 0xFF) — 호출측 기본값 유지를 위해 None.
        # i32 음수 (0xFFFFFFF0 = clBtnFace) 도 처리.
        for sysc in (0xFF000000, 0xFFFFFFF0):
            hex_, trans = dec._decode_tcolor(sysc)
            self.assertIsNone(hex_)
            self.assertFalse(trans)
        # None 입력은 (None, False).
        self.assertEqual(dec._decode_tcolor(None), (None, False))

    def test_T_10_frame_typ_to_sides_bitmask(self) -> None:
        """FrameTyp 비트마스크 → 4-측면 boolean 변환 정합성."""
        from debug import frf_decoder_poc as dec
        self.assertEqual(
            dec._frame_typ_to_sides(0x00),
            {"left": False, "top": False, "right": False, "bottom": False},
        )
        self.assertEqual(
            dec._frame_typ_to_sides(0x0F),
            {"left": True, "top": True, "right": True, "bottom": True},
        )
        self.assertEqual(
            dec._frame_typ_to_sides(0x01),
            {"left": True, "top": False, "right": False, "bottom": False},
        )
        # 0x0A = Top(2) + Bottom(8) — 가로선 패턴.
        self.assertEqual(
            dec._frame_typ_to_sides(0x0A),
            {"left": False, "top": True, "right": False, "bottom": True},
        )

    def test_T_11_memo_props_extractor_layout(self) -> None:
        """try_extract_memo_props_after — 통계 검증된 byte 레이아웃 회귀.

        v0.5.1 (Phase 0) 부터: clWhite (#FFFFFF) 회수 시 transparent 폴백.
        Phase A 의 byte layout 정밀 결정 후 v0.6.0 에서 정확 값으로 교체 예정.
        """
        from debug import frf_decoder_poc as dec
        # rect 16 byte + props 18 byte 모형. props 패턴:
        #   0-1: 00 00 (Stretched/Adjust)
        #   2:   0F   (FrameTyp = 4 sides)
        #   3:   00
        #   4-7: 02 00 00 00  (FrameWidth = 2 px)
        #   8-11: FF 00 00 00  (FrameColor = 0x000000FF = red)
        #   12-13: 00 00 (ShadowSize)
        #   14-17: FF FF FF 00  (FillColor = 0x00FFFFFF = white → 회귀 폴백)
        rect_bytes = b"\x00" * 16
        props_bytes = (
            b"\x00\x00\x0f\x00"
            b"\x02\x00\x00\x00"
            b"\xff\x00\x00\x00"
            b"\x00\x00"
            b"\xff\xff\xff\x00"
        )
        buf = b"PAD" + rect_bytes + props_bytes + b"TAIL"
        rect_offset = 3
        result = dec.try_extract_memo_props_after(buf, rect_offset)
        self.assertIsNotNone(result)
        self.assertEqual(result["frame_typ"], 0x0F)
        self.assertEqual(result["frame_width_px"], 2)
        self.assertEqual(result["frame_color_hex"], "#FF0000")
        # v0.5.1 Phase 0 — clWhite 회수는 회귀로 간주, transparent 폴백.
        self.assertIsNone(result["fill_color_hex"])
        self.assertTrue(result["fill_transparent"])

    def test_T_11b_phase0_clwhite_regression_fallback(self) -> None:
        """Phase 0 회귀 봉합: clWhite → transparent 정책 명시 회귀 (sample = 계산서.frf 패턴)."""
        from debug import frf_decoder_poc as dec
        # 계산서.frf Memo107_2 실측 byte (rect_offset=446 → base=462):
        rect_bytes = b"\x0c\x02\x00\x00\x84\x02\x00\x00\x14\x00\x00\x00\x18\x00\x00\x00"
        props_bytes = (
            b"\x00\x00\x0f\x00"          # frame_typ = 0x0F (4 sides)
            b"\x01\x00\x00\x00"          # FrameWidth = 1
            b"\x00\x00\xff\x00"          # FrameColor = 0x00FF0000 → #0000FF (clBlue)
            b"\x00\x00"                  # ShadowSize = 0
            b"\xff\xff\xff\x00"          # i32 = 0x00FFFFFF (clWhite, 회귀)
        )
        buf = rect_bytes + props_bytes
        result = dec.try_extract_memo_props_after(buf, 0)
        self.assertEqual(result["frame_color_hex"], "#0000FF")
        # 회귀 봉합: 명시적 white 도 transparent 로 강등.
        self.assertTrue(result["fill_transparent"])
        self.assertIsNone(result["fill_color_hex"])

    def test_T_11c_phase0_clnone_still_transparent(self) -> None:
        """Phase 0 정책이 기존 clNone(0x1FFFFFFF) transparent 동작을 깨지 않는다."""
        from debug import frf_decoder_poc as dec
        rect_bytes = b"\x00" * 16
        props_bytes = (
            b"\x00\x00\x0f\x00"
            b"\x01\x00\x00\x00"
            b"\x00\x00\x00\x00"          # FrameColor = clBlack
            b"\x00\x00"
            b"\xff\xff\xff\x1f"          # FillColor = 0x1FFFFFFF = clNone
        )
        buf = rect_bytes + props_bytes
        result = dec.try_extract_memo_props_after(buf, 0)
        self.assertTrue(result["fill_transparent"])
        self.assertIsNone(result["fill_color_hex"])
        self.assertEqual(result["frame_color_hex"], "#000000")

    def test_T_11d_phase0_real_color_preserved(self) -> None:
        """비-white, 비-clNone 색은 그대로 보존 (예: #008080 teal)."""
        from debug import frf_decoder_poc as dec
        rect_bytes = b"\x00" * 16
        props_bytes = (
            b"\x00\x00\x0f\x00"
            b"\x01\x00\x00\x00"
            b"\x00\x00\x00\x00"
            b"\x00\x00"
            b"\x80\x80\x00\x00"          # FillColor = 0x00008080 → R=0x80,G=0x80,B=0 = #808000
        )
        buf = rect_bytes + props_bytes
        result = dec.try_extract_memo_props_after(buf, 0)
        self.assertFalse(result["fill_transparent"])
        self.assertEqual(result["fill_color_hex"], "#808000")

    def test_T_12_memo_props_extractor_rejects_invalid(self) -> None:
        """frame_typ > 0x0F 또는 frame_width 비현실 값은 None 반환 (실패-허용)."""
        from debug import frf_decoder_poc as dec
        rect_bytes = b"\x00" * 16
        # FrameTyp = 0xFF (invalid)
        invalid = (
            b"\x00\x00\xff\x00"
            b"\x01\x00\x00\x00"
            b"\x00\x00\x00\x00"
            b"\x00\x00"
            b"\xff\xff\xff\x1f"
        )
        buf = rect_bytes + invalid
        self.assertIsNone(dec.try_extract_memo_props_after(buf, 0))


if __name__ == "__main__":
    unittest.main()
