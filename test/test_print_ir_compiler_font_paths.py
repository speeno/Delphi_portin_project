"""print_ir_compiler — Docker/로컬 폰트 경로 회귀 (parents[4] IndexError 방지)."""
from __future__ import annotations

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1] / "도서물류관리프로그램" / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_font_candidates_include_backend_assets():
    from app.services.print_ir_compiler import _font_file_candidates

    paths = _font_file_candidates("NanumGothic.otf")
    assert paths, "at least one candidate path"
    backend_font = BACKEND_ROOT / "assets" / "fonts" / "NanumGothic.otf"
    assert backend_font in paths
    assert backend_font.is_file(), "NanumGothic.otf must ship under backend/assets/fonts for Docker"


def test_resolve_font_face_src_does_not_raise():
    from app.services.print_ir_compiler import _NANUM_GOTHIC_SRC, _resolve_font_face_src

    src = _resolve_font_face_src("NanumGothic.otf", ["NanumGothic"])
    assert "local(" in src
    assert _NANUM_GOTHIC_SRC  # module import at load time must succeed
