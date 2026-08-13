"""DEC-154 — 저자관리 기입 순서 + 확장 필드(G3_Gjeo_Ext 사이드테이블) 회귀 가드.

2026-08-13 영업팀: 인세 대비 기입 순서 확정 — 저자구분→저자코드→저자명→학교→학과→
자택주소→연구소주소→담당자1→담당자2→원천징수→은행명→계좌번호→주민등록번호→
메일주소→연락처1→연락처2. 학과·담당자1/2·원천징수·은행명·메일주소는 G3_Gjeo 에
대응 컬럼이 없어(여유 f11~ 은 char(1)+기사용) DEC-068 전자책 선례대로 사이드테이블
``G3_Gjeo_Ext`` 신설. 연락처1/2 = 구 전화/팩스(gtel/gfax) 재라벨.

라이브 검증: remote_153 CREATE TABLE + upsert/get 라운드트립 후 프로브 행 삭제.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import IsolatedAsyncioTestCase, TestCase, main
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "도서물류관리프로그램" / "backend"))

from app.services import author_ext_service as ax  # noqa: E402

FRONTEND = ROOT / "도서물류관리프로그램" / "frontend" / "src"


class AuthorExtServiceTests(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        ax.clear_ensured_for_tests()
        self.addCleanup(ax.clear_ensured_for_tests)

    async def test_upsert_merges_partial_payload(self) -> None:
        captured: list[tuple[str, tuple]] = []
        state = {"row": {"dept": "식품영양학과", "manager1": "", "manager2": "",
                         "withhold": "", "bank_name": "", "email": ""}}

        async def fake_exec(server_id, sql, params=()):
            captured.append((sql, params))
            if sql.startswith("SELECT"):
                return [state["row"]]
            return []

        with patch.object(ax, "execute_query", fake_exec):
            ok = await ax.upsert_ext(
                server_id="remote_1", gcode="A001",
                payload={"bank_name": "국민은행"}, scope_hcode="5019",
            )
        self.assertTrue(ok)
        replace_sql, params = next(
            (s, p) for s, p in captured if s.startswith("REPLACE INTO")
        )
        self.assertIn("G3_Gjeo_Ext", replace_sql)
        # 부분 갱신 merge — 기존 dept 유지 + bank_name 신규.
        self.assertIn("식품영양학과", params)
        self.assertIn("국민은행", params)

    async def test_noop_when_no_ext_keys(self) -> None:
        async def fail_exec(server_id, sql, params=()):
            raise AssertionError("확장 키 없으면 DB 접근 금지")

        with patch.object(ax, "execute_query", fail_exec):
            ok = await ax.upsert_ext(
                server_id="remote_1", gcode="A001",
                payload={"gposa": "저자"}, scope_hcode="5019",
            )
        self.assertTrue(ok, "확장 키 없음 = no-op 성공")

    async def test_get_fails_soft(self) -> None:
        async def broken(server_id, sql, params=()):
            raise RuntimeError("denied")

        with patch.object(ax, "execute_query", broken):
            got = await ax.get_ext(server_id="remote_1", gcode="A001", scope_hcode="5019")
        self.assertEqual(got, ax.EMPTY_EXT)


class ModelAndRouterGuard(TestCase):
    def test_author_models_carry_ext_fields(self) -> None:
        from app.models.master import AuthorCreateRequest, AuthorDetail, AuthorUpdateRequest

        for k in ("dept", "manager1", "manager2", "withhold", "bank_name", "email"):
            self.assertIn(k, AuthorDetail.model_fields)
            self.assertIn(k, AuthorCreateRequest.model_fields)
            self.assertIn(k, AuthorUpdateRequest.model_fields)

    def test_router_merges_and_upserts_ext(self) -> None:
        src = (ROOT / "도서물류관리프로그램" / "backend" / "app" / "routers"
               / "masters.py").read_text(encoding="utf-8")
        self.assertIn("author_ext_service.get_ext", src)
        self.assertEqual(src.count("author_ext_service.upsert_ext"), 2, "create+update")


class FormOrderGuard(TestCase):
    FORM = (FRONTEND / "components" / "master" / "author-detail-form.tsx")

    def test_entry_order_matches_request(self) -> None:
        src = self.FORM.read_text(encoding="utf-8")
        order = ["저자구분", "저자코드", "저자명", "학교", "학과",
                 "자택주소1", "연구소주소1", "담당자1", "담당자2", "원천징수",
                 "은행명", "계좌번호", "주민등록번호", "메일주소", "연락처1", "연락처2"]
        pos = []
        for lbl in order:
            i = src.find(f'label="{lbl}"')
            self.assertGreater(i, -1, f"{lbl} 필드 누락")
            pos.append(i)
        self.assertEqual(pos, sorted(pos), "기입 순서 = 영업팀 확정 순서")
        # 구 라벨 재발 금지(재라벨 확인).
        for stale in ('label="출신학교"', 'label="전화번호"', 'label="팩스번호"',
                      'label="집주소1"', 'label="직장주소1"', 'label="주민등록"'):
            self.assertNotIn(stale, src)


if __name__ == "__main__":
    main()
