"""backend/.dockerignore 가 Git 시드 JSON(공지·메뉴)을 Docker 이미지에서 빼지 않는지 회귀 가드."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCKERIGNORE = ROOT / "도서물류관리프로그램" / "backend" / ".dockerignore"

MUST_NOT_EXCLUDE_GLOB = "data/*.json"
MUST_EXIST_IN_IMAGE = (
    "backend/data/platform_portal.json",
    "backend/data/menu_policy_overrides.json",
)


def test_dockerignore_does_not_blanket_exclude_data_json():
    text = DOCKERIGNORE.read_text(encoding="utf-8")
    assert MUST_NOT_EXCLUDE_GLOB not in text, (
        f"{DOCKERIGNORE}: '{MUST_NOT_EXCLUDE_GLOB}' 는 platform_portal·menu_policy 를 "
        "이미지에서 제외해 배포 공지/메뉴가 비게 됩니다."
    )


def test_seed_json_files_exist_in_repo():
    for rel in MUST_EXIST_IN_IMAGE:
        path = ROOT / "도서물류관리프로그램" / rel.replace("backend/", "backend/")
        assert path.is_file(), f"missing seed file: {rel}"
