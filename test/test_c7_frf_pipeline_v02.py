"""
C7 FRF 파이프라인 v0.2 회귀 게이트 — 디코더/컴파일러/품질 리포트 통합 검증.

검증 항목:
  - V_01 디코더 v0.2 의 Report_1_21 좌표 복원률 ≥ 95%
  - V_02 디코더 v0.2 가 binding 토큰 (expressions_dictionary) ≥ 5 종 추출
  - V_03 컴파일러 v0.2 가 Line/Rect/Picture/Barcode/SubReport 객체를 모두 렌더
  - V_04 컴파일러 debug_outline 모드는 [data-legacy-id] 라벨 CSS 를 활성화
  - V_05 컴파일러 binding diagnostics 가 placeholders/literal/empty 카운트를 누적
  - V_06 quality_report.evaluate_ir 의 priority_score 는 0..3.25 범위 내
  - V_07 batch 산출 디렉터리 존재 시 quality_report 집계 키가 모두 존재
  - V_08 SVG 컴파일러가 모든 객체 타입에 대해 SVG 요소를 emit
  - V_09 SVG debug_outline 모드는 분홍 점선 overlay 를 추가
  - V_10 빈 IR 입력에 대해 SVG fallback (`(빈 IR)`) 을 반환
  - V_11 fit=auto 가 객체 bbox 를 모두 포함하도록 viewBox 를 확장
  - V_12 fit=page 는 디코더 page.size_mm 를 그대로 사용
  - V_13 디코더 v0.3 버전 보고
  - V_14 좌표 단위가 px_96 으로 교정됨 (Memo01.x ≈ 100mm)
  - V_15 페이지 크기 추정이 합리적 범위 (>=150×100mm)
  - V_16 모든 객체 좌표가 plausibility 한도 안 (outlier 0)
  - V_17 render_template_with_context 가 긴 실제 데이터에 맞춰 HTML font-size 를 축소
  - V_18 render_template_with_context 가 SVG text 를 재랩핑/축소
"""
from __future__ import annotations

import importlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "도서물류관리프로그램" / "backend"))

from debug import frf_decoder_poc  # noqa: E402
from debug import frf_quality_report  # noqa: E402
from app.services import print_ir_compiler  # noqa: E402


SAMPLE_FRF = (
    REPO_ROOT
    / "legacy_delphi_source"
    / "legacy_source"
    / "Report"
    / "Report_1_21.frf"
)


class FrfDecoderV02Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not SAMPLE_FRF.is_file():
            raise unittest.SkipTest(f"sample frf missing: {SAMPLE_FRF}")
        cls.ir = frf_decoder_poc.decode_frf(SAMPLE_FRF)

    def test_V_01_coord_recovery_ratio(self) -> None:
        objs = [
            o
            for p in self.ir["pages"]
            for b in p["bands"]
            for o in b["objects"]
        ]
        with_rect = [o for o in objs if o["rect_mm"]["w"] > 0 and o["rect_mm"]["h"] > 0]
        ratio = len(with_rect) / max(1, len(objs))
        self.assertGreaterEqual(ratio, 0.95, f"coord recovery {ratio:.2%}")

    def test_V_02_expressions_dictionary_min_5(self) -> None:
        self.assertGreaterEqual(len(self.ir["expressions_dictionary"]), 5)

    def test_V_13_decoder_version_v03_or_later(self) -> None:
        """단위 교정이 적용된 v0.3+ 디코더 버전을 IR.source 가 보고."""
        ver = str(self.ir["source"]["decoder_version"])
        major, minor, *_ = ver.split(".")
        self.assertEqual(major, "0")
        self.assertGreaterEqual(int(minor), 3, f"got decoder version {ver}")

    def test_V_14_coord_unit_calibrated_to_px96(self) -> None:
        """v0.3 단위 교정: 좌표 단위가 96 DPI 픽셀 (1mm = 3.7795 raw int) 로 환산되면
        Report_1_21 의 첫 본문 라벨 (Memo01, [Gadd1] 바인딩) 의 x_mm 가 80~140mm
        (영수증 양식 가운데 영역) 안에 들어와야 한다.

        이전 (v0.2 TWIPS 가정) 에는 x_mm ≈ 6.84 mm — 페이지 좌상단 1cm 띠로 압축됨.
        """
        page = self.ir["pages"][0]
        memo01 = None
        for band in page["bands"]:
            for obj in band["objects"]:
                if obj["name"] == "Memo01":
                    memo01 = obj
                    break
        self.assertIsNotNone(memo01, "Memo01 not found")
        x = memo01["rect_mm"]["x"]
        self.assertGreaterEqual(x, 80.0, f"Memo01.x={x}mm — 단위 교정 전 (TWIPS) 값")
        self.assertLessEqual(x, 140.0, f"Memo01.x={x}mm — 단위 교정 결과가 비현실적")

    def test_V_15_page_size_realistic(self) -> None:
        """v0.3 페이지 크기 추정 — 200×148mm 영수증 양식에 대해 width/height 가
        합리적 범위 (가로 ≥ 150mm, 세로 ≥ 100mm) 로 추정돼야 한다."""
        page = self.ir["pages"][0]
        size = page["size_mm"]
        self.assertGreaterEqual(size["width"], 150.0,
                                f"page width {size['width']}mm 는 단위 교정 누락 의심")
        self.assertLessEqual(size["width"], 320.0,
                             f"page width {size['width']}mm 는 plausibility 초과")
        self.assertGreaterEqual(size["height"], 100.0)
        self.assertLessEqual(size["height"], 1200.0)

    def test_V_16_no_coord_outliers_beyond_plausibility(self) -> None:
        """v0.3 plausibility 게이트 — 모든 객체의 x/y/w/h 는 (-20..1200mm) 안에 있어야."""
        page = self.ir["pages"][0]
        for band in page["bands"]:
            for obj in band["objects"]:
                rect = obj["rect_mm"]
                if rect["w"] <= 0 or rect["h"] <= 0:
                    continue
                self.assertGreaterEqual(rect["x"], -20.0, obj["name"])
                self.assertLessEqual(rect["x"], 320.0, obj["name"])
                self.assertGreaterEqual(rect["y"], -20.0, obj["name"])
                self.assertLessEqual(rect["y"], 1200.0, obj["name"])


class CompilerCoverageTest(unittest.TestCase):
    def _make_ir(self) -> dict:
        return {
            "schema_version": "0.1.0",
            "source": {"filename": "synthetic.frf"},
            "report": {"title": "synthetic"},
            "pages": [
                {
                    "size_mm": {"width": 100.0, "height": 148.0},
                    "margin_mm": {"top": 8.0, "right": 8.0, "bottom": 8.0, "left": 8.0},
                    "bands": [
                        {
                            "name": "Band1",
                            "objects": [
                                {
                                    "name": "TextA",
                                    "type": "Text",
                                    "rect_mm": {"x": 5, "y": 5, "w": 40, "h": 6},
                                    "binding": {"kind": "literal", "value": "Hello"},
                                },
                                {
                                    "name": "L1",
                                    "type": "Line",
                                    "rect_mm": {"x": 5, "y": 12, "w": 40, "h": 0.3},
                                    "border": {"color": "#000", "width_pt": 1.0},
                                    "binding": {"kind": "literal", "value": ""},
                                },
                                {
                                    "name": "R1",
                                    "type": "Rect",
                                    "rect_mm": {"x": 5, "y": 14, "w": 40, "h": 10},
                                    "border": {"color": "#777", "width_pt": 0.5,
                                               "left": True, "top": True,
                                               "right": True, "bottom": True},
                                    "binding": {"kind": "literal", "value": ""},
                                },
                                {
                                    "name": "Pic1",
                                    "type": "Picture",
                                    "rect_mm": {"x": 5, "y": 25, "w": 20, "h": 20},
                                    "binding": {"kind": "literal", "value": ""},
                                },
                                {
                                    "name": "BC1",
                                    "type": "Barcode",
                                    "rect_mm": {"x": 30, "y": 25, "w": 50, "h": 20},
                                    "binding": {
                                        "kind": "expression",
                                        "raw": "[Code]",
                                        "tokens": [
                                            {"type": "field", "table": None, "column": "Code"}
                                        ],
                                    },
                                },
                                {
                                    "name": "Sub1",
                                    "type": "SubReport",
                                    "rect_mm": {"x": 5, "y": 50, "w": 90, "h": 30},
                                    "binding": {"kind": "literal", "value": ""},
                                },
                            ],
                        }
                    ],
                }
            ],
            "data_sources": [],
            "expressions_dictionary": {"[Code]": {"table": None, "column": "Code"}},
            "variant_profile": None,
            "unsupported_objects": [],
            "decoder_warnings": [],
        }

    def test_V_03_renders_all_object_types(self) -> None:
        html, diag = print_ir_compiler.compile_ir_to_html(
            self._make_ir(), return_diagnostics=True
        )
        self.assertIn("frf-line", html)
        self.assertIn("frf-rect", html)
        self.assertIn("frf-pic", html)
        self.assertIn("frf-barcode", html)
        self.assertIn("frf-sub", html)
        for t in ("Text", "Line", "Rect", "Picture", "Barcode", "SubReport"):
            self.assertGreaterEqual(diag["rendered_by_type"].get(t, 0), 1, t)

    def test_V_04_debug_outline_adds_legacy_id_label(self) -> None:
        html_off = print_ir_compiler.compile_ir_to_html(self._make_ir(), debug_outline=False)
        html_on = print_ir_compiler.compile_ir_to_html(self._make_ir(), debug_outline=True)
        self.assertNotIn("attr(data-legacy-id)", html_off)
        self.assertIn("attr(data-legacy-id)", html_on)

    def test_V_05_binding_diagnostics_counts(self) -> None:
        _, diag = print_ir_compiler.compile_ir_to_html(
            self._make_ir(), return_diagnostics=True
        )
        self.assertGreaterEqual(diag["binding_literal_filled"], 1)
        self.assertGreaterEqual(len(diag["binding_placeholders"]), 1)
        self.assertIn("Code", diag["binding_placeholders"])

    def test_V_08_svg_renders_all_object_types(self) -> None:
        svg = print_ir_compiler.compile_ir_to_svg(self._make_ir())
        # 헤더/뷰포트 (v0.3: viewBox 좌상단은 0.0, page 100×148 안에 모든 객체 포함 → page 그대로)
        self.assertTrue(svg.startswith("<svg"))
        import re as _re
        m = _re.search(r"viewBox='([\-0-9.]+) ([\-0-9.]+) ([\-0-9.]+) ([\-0-9.]+)'", svg)
        self.assertIsNotNone(m)
        vx, vy, vw, vh = (float(m.group(i)) for i in range(1, 5))
        self.assertLessEqual(vx, 0.0)
        self.assertLessEqual(vy, 0.0)
        self.assertGreaterEqual(vw, 100.0)
        self.assertGreaterEqual(vh, 148.0)
        for legacy in ("TextA", "L1", "R1", "Pic1", "BC1", "Sub1"):
            self.assertIn(f"data-legacy-id='{legacy}'", svg, legacy)
        self.assertIn("<line ", svg)
        self.assertIn("<rect ", svg)
        self.assertIn("<text ", svg)
        self.assertIn("data-role='page-boundary'", svg)
        # v0.3.3 — placeholder/Barcode 라벨은 더 이상 ``{{ ctx.X }}`` 로 그리지 않고
        # ``[Code]`` 압축 마커 또는 박스+컬럼명 라벨로 표시한다 (Text placeholder 의
        # 박스+라벨 UX 는 V_19 에서 단독 검증).
        self.assertNotIn("{{ ctx.Code }}", svg)
        self.assertIn("data-binding='literal'", svg)
        self.assertIn("Hello", svg)

    def test_V_09_svg_debug_outline_adds_overlay(self) -> None:
        off = print_ir_compiler.compile_ir_to_svg(self._make_ir(), debug_outline=False)
        on = print_ir_compiler.compile_ir_to_svg(self._make_ir(), debug_outline=True)
        self.assertNotIn("rgba(255,0,128,0.4)", off)
        self.assertIn("rgba(255,0,128,0.4)", on)

    def test_V_10_svg_empty_ir_fallback(self) -> None:
        svg = print_ir_compiler.compile_ir_to_svg({"pages": []})
        self.assertIn("(빈 IR)", svg)
        self.assertTrue(svg.startswith("<svg"))

    def test_V_11_svg_fit_auto_expands_for_outliers(self) -> None:
        """페이지 size_mm 가 객체보다 작으면 fit=auto 가 union 으로 확장한다."""
        ir = self._make_ir()
        # 인위적으로 페이지를 50×50 으로 좁히면 viewBox 는 객체 bbox 까지 확장돼야 함
        ir["pages"][0]["size_mm"] = {"width": 50.0, "height": 50.0}
        svg = print_ir_compiler.compile_ir_to_svg(ir, fit="auto")
        import re as _re
        m = _re.search(r"viewBox='([\-0-9.]+) ([\-0-9.]+) ([\-0-9.]+) ([\-0-9.]+)'", svg)
        vx, vy, vw, vh = (float(m.group(i)) for i in range(1, 5))
        self.assertGreater(vw, 50.0, "viewBox 가 작은 페이지를 넘어 확장돼야 함")
        self.assertGreater(vh, 50.0)

    def test_V_12_svg_fit_page_keeps_declared_size(self) -> None:
        ir = self._make_ir()
        ir["pages"][0]["size_mm"] = {"width": 50.0, "height": 50.0}
        svg = print_ir_compiler.compile_ir_to_svg(ir, fit="page")
        self.assertIn("viewBox='0.0 0.0 50.0 50.0'", svg)

    def test_V_17_render_context_shrinks_html_font_for_long_data(self) -> None:
        ir = self._make_ir()
        ir["pages"][0]["bands"][0]["objects"][0] = {
            "name": "TextFit",
            "type": "Text",
            "rect_mm": {"x": 5, "y": 5, "w": 18, "h": 6},
            "style": {"font_size_pt": 12.0, "halign": "left", "color": "#222222"},
            "binding": {
                "kind": "expression",
                "raw": "[Name]",
                "tokens": [{"type": "field", "table": None, "column": "Name"}],
            },
        }
        html = print_ir_compiler.compile_ir_to_html(ir)
        rendered = print_ir_compiler.render_template_with_context(
            html,
            {"Name": "한국도서유통주식회사"},
        )
        self.assertIn("한국도서유통주식회사", rendered)
        import re as _re
        m = _re.search(r"font-size:([0-9.]+)pt;", rendered)
        self.assertIsNotNone(m)
        self.assertLess(float(m.group(1)), 12.0)

    def test_V_18_render_context_marks_html_placeholder_bound(self) -> None:
        """v0.3.3 — frf-placeholder 셀에 실데이터를 주입하면 .is-bound 클래스가
        토글되어 옅은 박스+컬럼명 라벨이 일반 셀 외관으로 전환된다."""
        ir = self._make_ir()
        ir["pages"][0]["bands"][0]["objects"][0] = {
            "name": "TextFitHtml",
            "type": "Text",
            "rect_mm": {"x": 5, "y": 5, "w": 18, "h": 8},
            "style": {"font_size_pt": 12.0, "halign": "left", "color": "#222222"},
            "binding": {
                "kind": "expression",
                "raw": "[Name]",
                "tokens": [{"type": "field", "table": None, "column": "Name"}],
            },
        }
        html = print_ir_compiler.compile_ir_to_html(ir)
        # 컴파일 직후: frf-placeholder 클래스 + data-field 부착, .is-bound 토글 미적용.
        self.assertIn("frf-placeholder", html)
        self.assertIn("data-field='Name'", html)
        self.assertNotIn("frf-placeholder is-bound", html)
        rendered = print_ir_compiler.render_template_with_context(
            html, {"Name": "한국도서유통주식회사"}
        )
        # 실데이터 주입 후: .is-bound 토글되고 미치환 placeholder 도 사라진다.
        self.assertIn("frf-placeholder is-bound", rendered)
        self.assertIn("한국도서유통주식회사", rendered)
        self.assertNotIn("{{ ctx.Name }}", rendered)

    def test_V_19_svg_placeholder_renders_box_and_field_label(self) -> None:
        """v0.3.3 — placeholder Text 셀은 ``[Code]`` 텍스트 대신 *옅은 박스*
        와 *우하단 컬럼명 라벨* 로 그려진다."""
        ir = self._make_ir()
        ir["pages"][0]["bands"][0]["objects"] = [
            {
                "name": "Memo01",
                "type": "Text",
                "rect_mm": {"x": 10, "y": 10, "w": 20, "h": 6},
                "style": {"font_size_pt": 9.0, "halign": "left", "color": "#222222"},
                "binding": {
                    "kind": "expression",
                    "raw": "[Squt1]",
                    "tokens": [{"type": "field", "table": None, "column": "Squt1"}],
                },
            }
        ]
        svg = print_ir_compiler.compile_ir_to_svg(ir)
        # placeholder 박스 + 라벨 ID/속성
        self.assertIn("data-binding='placeholder'", svg)
        self.assertIn("data-field='Squt1'", svg)
        # placeholder 박스 색상 (옅은 파랑)
        self.assertIn("#eef4fb", svg)
        # 우하단 컬럼명 라벨 (1.6mm 이탤릭)
        self.assertIn(">Squt1</text>", svg)
        # placeholder 텍스트는 더 이상 본문에 ``[Squt1]`` 로 표시되지 않음
        self.assertNotIn(">[Squt1]<", svg)
        self.assertNotIn("{{ ctx.Squt1 }}", svg)

    def test_V_20_svg_placeholder_skips_label_in_tiny_cell(self) -> None:
        """v0.3.3 — 셀 높이가 ``_PLACEHOLDER_LABEL_MIN_H_MM`` (3mm) 미만이면
        라벨을 생략하고 박스만 남긴다 (라벨이 셀을 침범하지 않게)."""
        ir = self._make_ir()
        ir["pages"][0]["bands"][0]["objects"] = [
            {
                "name": "TinyMemo",
                "type": "Text",
                "rect_mm": {"x": 10, "y": 10, "w": 6, "h": 2.0},
                "style": {"font_size_pt": 9.0, "halign": "left", "color": "#222222"},
                "binding": {
                    "kind": "expression",
                    "raw": "[Tiny]",
                    "tokens": [{"type": "field", "table": None, "column": "Tiny"}],
                },
            }
        ]
        svg = print_ir_compiler.compile_ir_to_svg(ir)
        self.assertIn("data-binding='placeholder'", svg)
        self.assertIn("data-field='Tiny'", svg)
        # 라벨 폰트 (1.6mm) 가 등장하지 않아야 한다.
        self.assertNotIn("font-size='1.6mm'", svg)
        # 그러나 박스 (옅은 파랑) 는 그려진다.
        self.assertIn("#eef4fb", svg)

    # ------------------------------------------------------------------
    # v0.4.0 — Picture 임베디드 이미지 (HTML <img> / SVG <image>)
    # ------------------------------------------------------------------

    @staticmethod
    def _ir_with_picture_image() -> dict:
        """1×1 투명 PNG 임베디드 이미지를 가진 IR 샘플."""
        import base64
        # 1×1 transparent PNG
        png = bytes.fromhex(
            "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4"
            "890000000d49444154789c63000100000005000100190b1d550000000049454e"
            "44ae426082"
        )
        b64 = base64.b64encode(png).decode("ascii")
        import hashlib
        sha1 = hashlib.sha1(png).hexdigest()
        return {
            "schema_version": "0.1.0",
            "source": {"filename": "img.frf"},
            "report": {"title": "img"},
            "pages": [{
                "size_mm": {"width": 100.0, "height": 148.0},
                "margin_mm": {},
                "bands": [{"name": "B", "objects": [
                    {
                        "name": "PicLogo",
                        "type": "Picture",
                        "rect_mm": {"x": 10, "y": 10, "w": 30, "h": 20},
                        "binding": {"kind": "literal", "value": ""},
                        "image": {
                            "format": "image/png",
                            "size_bytes": len(png),
                            "sha1": sha1,
                            "data_b64": b64,
                            "decoder_match_delta": 82,
                        },
                    },
                    {
                        "name": "PicMissing",
                        "type": "Picture",
                        "rect_mm": {"x": 50, "y": 10, "w": 30, "h": 20},
                        "binding": {"kind": "literal", "value": ""},
                    },
                ]}],
            }],
            "data_sources": [],
            "expressions_dictionary": {},
            "variant_profile": None,
            "unsupported_objects": [],
            "decoder_warnings": [],
        }

    def test_V_21_html_picture_inlines_dataURI(self) -> None:
        """v0.4.0 — IR.Picture.image 가 있으면 HTML 은 ``<img src='data:...'>`` 로
        인라인 렌더, 없으면 기존 ``[image]`` placeholder fallback."""
        ir = self._ir_with_picture_image()
        html = print_ir_compiler.compile_ir_to_html(ir)
        # 첫 Picture: 이미지 인라인
        self.assertIn("frf-pic-img", html)
        self.assertIn("data:image/png;base64,", html)
        self.assertIn("data-image-format='image/png'", html)
        self.assertIn("data-legacy-id='PicLogo'", html)
        # 두 번째 Picture: image 없음 → placeholder fallback
        self.assertIn("frf-pic", html)
        self.assertIn("data-legacy-id='PicMissing'", html)
        self.assertIn("[image]", html)

    def test_V_22_svg_picture_inlines_image_element(self) -> None:
        """v0.4.0 — IR.Picture.image 가 있으면 SVG 는 ``<image href='data:...'>`` 로
        인라인 렌더, 없으면 placeholder 박스 fallback."""
        ir = self._ir_with_picture_image()
        svg = print_ir_compiler.compile_ir_to_svg(ir)
        # PicLogo: SVG <image>
        self.assertIn("<image ", svg)
        self.assertIn("data-legacy-id='PicLogo'", svg)
        self.assertIn("href='data:image/png;base64,", svg)
        self.assertIn("preserveAspectRatio='xMidYMid meet'", svg)
        # PicMissing: data-type='placeholder' fallback
        self.assertIn("data-legacy-id='PicMissing'", svg)
        self.assertIn("data-type='placeholder'", svg)


class QualityReportTest(unittest.TestCase):
    def test_V_06_priority_score_in_range(self) -> None:
        m = frf_quality_report.IRMetrics(
            rel_path="x",
            objects=10,
            objects_with_rect=5,
            objects_with_binding=3,
            unsupported_objects=2,
            expressions=1,
        )
        score = m.priority_score
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 3.25)

    def test_V_07_aggregate_keys_present(self) -> None:
        agg = frf_quality_report.aggregate(
            [
                frf_quality_report.IRMetrics(
                    rel_path="a",
                    objects=4,
                    objects_with_rect=4,
                    objects_with_binding=2,
                    expressions=1,
                ),
                frf_quality_report.IRMetrics(
                    rel_path="b",
                    objects=2,
                    objects_with_rect=0,
                    objects_with_binding=0,
                    unsupported_objects=1,
                ),
            ]
        )
        for k in (
            "files",
            "objects_total",
            "coord_recovery_overall",
            "binding_fill_overall",
            "buckets_by_coord_recovery",
        ):
            self.assertIn(k, agg)
        self.assertIn("empty_layout", agg["buckets_by_coord_recovery"])


if __name__ == "__main__":
    unittest.main()
