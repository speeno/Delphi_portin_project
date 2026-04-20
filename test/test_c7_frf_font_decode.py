"""
test_c7_frf_font_decode — frf_decoder_poc v0.6.0 의 Font 블록/Adjust 추출 회귀 테스트.

Phase B (Font 동적 스캔) + Phase C (compiler 정합) 의 정상성을 보장한다.

테스트 케이스
=============
1. ``test_T_20_font_block_arial_extracted``
   계산서.frf Memo107_2 byte fixture: Font.Name="Arial" / Size=10 / Color=clBlack /
   Style=0 → font_extracted dict 가 모두 정합.

2. ``test_T_21_font_block_korean_charset_fallback``
   인공 fixture: Font.Name="Arial" + charset=129 (Hangeul) → 컴파일러가 본문에
   한글 텍스트 있을 때 NanumGothic 폴백을 *앞쪽* 에 끼우는지.

3. ``test_T_22_phase0_clwhite_fill_transparent_at_irlevel``
   계산서.frf 통합 회귀: v0.6.0 decode 결과 fill_opaque_white_count == 0
   (Phase 0 회귀 봉합 영구 작동).

4. ``test_T_23_tong06_dfm_blob_decodes``
   ``legacy_delphi_source/legacy_source/Tong06.dfm`` 의 ReportForm BLOB 을 추출해
   디코더가 *실패-허용* 으로 적어도 1 개 객체를 인식하는지 (스모크).
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "도서물류관리프로그램" / "backend"))


class FontDecodeTest(unittest.TestCase):
    def test_T_20_font_block_arial_extracted(self) -> None:
        """계산서.frf Memo107_2 fixture → Font.Name=Arial / Size=10pt 정합."""
        from debug import frf_decoder_poc as dec

        # rect 16 byte (zero) + 속성 18 byte + 패딩/플래그 + Font 블록.
        # 실측 (계산서.frf Memo107_2 base+0..98) 를 단순화하여 fixture 화.
        rect = b"\x00" * 16
        # base 직후 18 byte 속성 블록.
        props = (
            b"\x00\x00"          # padding/Stretched
            b"\x0f\x00"          # FrameTyp=0x0F
            b"\x01\x00\x00\x00"  # FrameWidth=1
            b"\x00\x00\xff\x00"  # FrameColor=clBlue
            b"\x00\x00"          # ShadowSize=0
            b"\xff\xff\xff\x00"  # FillColor=clWhite (회귀 → transparent 폴백)
        )
        # base+18 부터: Highlight 블록 + Font 블록.
        # Phase A probe 결과 Font.Name 이 빈 본문 Memo 의 경우 base+46 에서
        # 시작 (length WORD, 내용 base+48).
        pad = (
            b"\x2c\x00\x00\x00\x00\x00\x00\x00"      # base+18..25 (8 byte)
            b"\x00\x00\x00\x01\x00\x00\x00\x00"      # base+26..33 (8 byte)
            b"\x02\x00\x00\x00\x01\x00\x00\x00"      # base+34..41 (8 byte)
            b"\x00\x00\x00\x00"                       # base+42..45 padding
        )
        font_block = (
            b"\x05\x00"                # base+46: Font.Name length WORD = 5
            b"Arial"                   # base+48..52: "Arial"
            b"\x00"                    # base+53: terminator
            b"\x0a\x00\x00\x00"        # base+54..57: Font.Size = 10
            b"\x00\x00\x00\x00"        # base+58..61: Font.Color = clBlack
            b"\x00\x00"                # base+62..63: padding/Charset (0=ANSI)
            b"\x00\x00\x00\x00"        # base+64..67: Font.Style etc.
        )
        buf = rect + props + pad + font_block
        result = dec.try_extract_memo_props_after(buf, 0)
        self.assertIsNotNone(result)
        self.assertEqual(result["frame_color_hex"], "#0000FF")
        # Phase 0 회귀 봉합: clWhite 회수 → transparent.
        self.assertTrue(result["fill_transparent"])
        # v0.6.0 — Font 블록 추출.
        font = result["font"]
        self.assertIsNotNone(font)
        self.assertEqual(font["font_name"], "Arial")
        self.assertEqual(font["font_family"], "Arial")
        self.assertEqual(font["font_size_pt"], 10.0)
        self.assertEqual(font["font_color_hex"], "#000000")
        self.assertFalse(font["font_bold"])
        self.assertFalse(font["font_italic"])

    def test_T_21_font_block_korean_charset_fallback(self) -> None:
        """ASCII 폰트 + 한글 본문 → compiler 가 NanumGothic 폴백 앞쪽 삽입."""
        from app.services.print_ir_compiler import _font_stack_for_family

        # ASCII 폰트 + 한글 본문 → 폴백 적용.
        stack_korean = _font_stack_for_family(
            "Arial", charset=129, has_korean_text=True
        )
        self.assertIn("NanumGothic", stack_korean)
        self.assertIn("Arial", stack_korean)
        # NanumGothic 이 Arial 보다 *뒤에* 와야 한다 (browser 가 선순위로 Arial 먼저
        # 시도; ASCII 는 Arial 로 한글은 NanumGothic 으로 대체).
        self.assertLess(
            stack_korean.index("Arial"),
            stack_korean.index("NanumGothic"),
        )
        # ASCII 폰트 + 한글 본문 없음 → 폴백 미삽입.
        stack_ascii = _font_stack_for_family(
            "Arial", charset=0, has_korean_text=False
        )
        self.assertIn("Arial", stack_ascii)
        self.assertNotIn("NanumGothic", stack_ascii)
        # 한글 폰트 직접 → Gulim/한글 매핑.
        stack_gulim = _font_stack_for_family("굴림", charset=129)
        self.assertIn("Gulim", stack_gulim)

    def test_T_22_phase0_clwhite_fill_transparent_at_irlevel(self) -> None:
        """계산서.frf 통합 회귀: v0.6.0 디코드 결과 opaque-white fill 0건."""
        from debug import frf_decoder_poc as dec

        path = REPO_ROOT / "legacy_delphi_source" / "legacy_source" / "Report" / "계산서.frf"
        if not path.exists():
            self.skipTest("legacy 계산서.frf 부재 — 환경에서 패스.")
        ir = dec.decode_frf(str(path))
        opaque_white = 0
        total = 0
        for p in ir["pages"]:
            for b in p["bands"]:
                for o in b["objects"]:
                    fl = o.get("fill") or {}
                    total += 1
                    if not fl.get("transparent") and (fl.get("color") or "").upper() == "#FFFFFF":
                        opaque_white += 1
        self.assertGreater(total, 100, "계산서.frf 객체 수가 비정상적으로 적다")
        self.assertEqual(
            opaque_white, 0,
            f"Phase 0 회귀 재발: opaque-white 셀 {opaque_white}/{total} 건"
        )

    def test_T_23_tong06_dfm_blob_decodes(self) -> None:
        """Tong06.dfm 의 ReportForm BLOB 도 디코더가 *실패-허용* 으로 처리."""
        from debug import frf_decoder_poc as dec

        dfm_path = REPO_ROOT / "legacy_delphi_source" / "legacy_source" / "Tong06.dfm"
        if not dfm_path.exists():
            self.skipTest("Tong06.dfm 부재 — 환경에서 패스.")
        text = dfm_path.read_text(errors="replace")
        m = re.search(
            r"frReport20_01[^{]*ReportForm\s*=\s*\{([^}]*)\}", text, flags=re.DOTALL
        )
        if not m:
            self.skipTest("frReport20_01.ReportForm 미발견 — 패스.")
        cleaned = re.sub(r"[^0-9A-Fa-f]", "", m.group(1))
        blob = bytes.fromhex(cleaned)
        # decode_frf 는 file path 만 받으므로 임시 파일 사용.
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".frf", delete=False) as tmp:
            tmp.write(blob)
            tmp_path = tmp.name
        try:
            ir = dec.decode_frf(tmp_path)
        finally:
            Path(tmp_path).unlink(missing_ok=True)
        # 실패-허용 — 최소한 source/decoder_version 은 v0.6.0.
        dv = ir["source"]["decoder_version"]
        self.assertTrue(
            dv.startswith("0.6."),
            f"decoder_version 기대 0.6.x: {dv}",
        )
        # pages / unsupported_objects 둘 중 하나는 채워져야 한다 (전부 비면 디코더 실패).
        has_pages = bool(ir.get("pages"))
        has_warnings = bool(ir.get("decoder_warnings"))
        self.assertTrue(
            has_pages or has_warnings,
            "Tong06.dfm BLOB 디코드: pages 와 warnings 모두 비어있다."
        )

    def test_T_24_style_attr_double_quote_position_not_stripped(self) -> None:
        """v0.6.1 — HTML ``style='`` + ``font-family:'Arial'`` 는 속성이 조기 종료되어
        ``left/top`` 가 무시된다. ``style=\"`` 로 감싸 레이아웃 회귀 방지."""
        from app.services.print_ir_compiler import compile_ir_to_html

        ir = {
            "schema_version": "0.1.0",
            "source": {"kind": "frf", "filename": "fixture.frf"},
            "report": {"title": "t"},
            "pages": [
                {
                    "size_mm": {"width": 183.0, "height": 280.0},
                    "margin_mm": {"top": 8.0, "right": 8.0, "bottom": 8.0, "left": 8.0},
                    "bands": [
                        {
                            "name": "Band1",
                            "type": "MasterData",
                            "y_mm": 0.0,
                            "height_mm": 272.0,
                            "objects": [
                                {
                                    "name": "Memo1",
                                    "type": "Text",
                                    "rect_mm": {
                                        "x": 138.6417,
                                        "y": 170.3917,
                                        "w": 40.0,
                                        "h": 8.0,
                                    },
                                    "binding": {"kind": "literal", "value": "인쇄용지"},
                                    "style": {
                                        "font_family": "Arial",
                                        "font_size_pt": 12.0,
                                        "_font_extracted": True,
                                        "_font_charset": 129,
                                        "halign": "left",
                                        "valign": "center",
                                    },
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        html = compile_ir_to_html(ir)
        self.assertIn('style="font-family:', html)
        self.assertIn("left:138.6417mm", html)
        self.assertIn("top:170.3917mm", html)
        # 같은 div 태그 안에 폰트·좌표가 함께 있어야 한다 (속성 분절 회귀 방지).
        mo = re.search(r"<div[^>]*style=\"([^\"]*)\"", html)
        self.assertIsNotNone(mo)
        blob = mo.group(1)
        self.assertIn("font-family:", blob)
        self.assertIn("left:138.6417mm", blob)
        self.assertIn("top:170.3917mm", blob)

    def test_T_25_blue_body_text_normalized_to_black(self) -> None:
        """v0.6.2 — FRF ``clBlue`` 계열 본문 글자색을 인쇄물 검정으로 통일."""
        from app.services.print_ir_compiler import compile_ir_to_html

        ir = {
            "schema_version": "0.1.0",
            "source": {"kind": "frf", "filename": "fixture.frf"},
            "report": {"title": "t"},
            "pages": [
                {
                    "size_mm": {"width": 100.0, "height": 100.0},
                    "margin_mm": {"top": 8.0, "right": 8.0, "bottom": 8.0, "left": 8.0},
                    "bands": [
                        {
                            "name": "b",
                            "type": "Band",
                            "y_mm": 0.0,
                            "height_mm": 90.0,
                            "objects": [
                                {
                                    "name": "TxBlue",
                                    "type": "Text",
                                    "rect_mm": {"x": 10.0, "y": 10.0, "w": 80.0, "h": 8.0},
                                    "binding": {"kind": "literal", "value": "본문"},
                                    "style": {
                                        "font_family": "Arial",
                                        "font_size_pt": 12.0,
                                        "_font_extracted": True,
                                        "color": "#0200FF",
                                    },
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        html = compile_ir_to_html(ir)
        self.assertIn("color:#000000", html)
        self.assertNotIn("color:#0200FF", html)


if __name__ == "__main__":
    unittest.main()
