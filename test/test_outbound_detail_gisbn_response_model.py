"""출고 상세 라인 ISBN 이 응답에서 잘려나가던 회귀 — 2026-08-22 사용자 리포트.

증상
----
출고현황(Sobo67_status) **상세** 뷰 우측 라인 목록의 ISBN 칸이 항상 비어 있었다.
목록(view=list) 뷰는 정상 — 서로 다른 엔드포인트를 쓰기 때문이다.

원인
----
`outbound_service.get_order_detail` 은 `product_name` 과 **같은 G4_Book lookup**
(`SELECT ... IFNULL(Gisbn,'') AS gisbn`)에서 `gisbn` 을 이미 채워 반환한다.
그런데 라우터가 `response_model=OrderDetailResponse` 로 검증하는데
`OrderLineDetail` 모델에 `gisbn` 필드가 없어 **Pydantic 이 응답에서 잘라냈다.**
(FastAPI response_model 은 모델에 없는 키를 조용히 버린다.)

DEC-169 대상 목록의 B15(출고현황 라인 목록 + 상세)가 상세 쪽만 누락된 상태였다.

가드
----
1. 모델에 `gisbn` 필드 존재.
2. 서비스가 돌려준 `gisbn` 이 모델 직렬화를 **통과**한다(잘리지 않는다).
3. 같은 lookup 을 쓰는 `product_name` 과 동일 경로임을 확인 — ISBN 만 빠지지 않도록.

사용자 규칙: test 폴더에 저장.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import TestCase, main

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "도서물류관리프로그램" / "backend"
FRONT = ROOT / "도서물류관리프로그램" / "frontend" / "src"
sys.path.insert(0, str(BACKEND))

from app.models.outbound import OrderDetailResponse, OrderLineDetail  # noqa: E402


def _service_shaped_detail() -> dict:
    """`outbound_service.get_order_detail` 이 만드는 dict 와 동일한 모양."""
    return {
        "order_key": {
            "gdate": "2026.08.21", "hcode": "5019", "gcode": "C001",
            "jubun": "11", "gjisa": "", "idnum": 42,
        },
        "customer": {"hcode": "5019", "gcode": "C001", "gname": "신화서점"},
        "status": "received",
        "lines": [
            {
                "gcode": "C001", "bcode": "B1", "pubun": "위탁",
                "gsqut": 3, "gssum": 21000, "gdang": 10000, "grat1": 70,
                "gbigo": "", "gisbn": "9788900000011",
                "yesno": "0", "product_name": "도서A",
            },
            # 마스터에 ISBN 이 없는 도서 — 빈 문자열로 흡수(응답 자체는 유지).
            {
                "gcode": "C001", "bcode": "B2", "pubun": "위탁",
                "gsqut": 1, "gssum": 7000, "gdang": 7000, "grat1": 100,
                "gbigo": "", "gisbn": "",
                "yesno": "0", "product_name": "도서B",
            },
        ],
    }


class OrderLineDetailIsbnFieldTests(TestCase):
    def test_model_declares_gisbn(self) -> None:
        self.assertIn(
            "gisbn", OrderLineDetail.model_fields,
            "OrderLineDetail 에 gisbn 이 없으면 response_model 이 ISBN 을 잘라낸다",
        )

    def test_gisbn_survives_response_model_validation(self) -> None:
        """서비스 dict → 모델 → JSON 왕복에서 gisbn 이 살아남는다."""
        dumped = OrderDetailResponse.model_validate(_service_shaped_detail()).model_dump()
        lines = dumped["lines"]
        self.assertEqual(len(lines), 2)
        self.assertEqual(lines[0]["gisbn"], "9788900000011")
        # 도서명과 같은 lookup 경로 — 하나만 통과하고 다른 하나가 잘리면 안 된다.
        self.assertEqual(lines[0]["product_name"], "도서A")
        self.assertEqual(lines[1]["gisbn"], "")

    def test_missing_gisbn_defaults_to_empty(self) -> None:
        """구서버(컬럼 부재)에서 gisbn 키가 없어도 상세가 500 나지 않는다."""
        payload = _service_shaped_detail()
        for ln in payload["lines"]:
            ln.pop("gisbn")
        dumped = OrderDetailResponse.model_validate(payload).model_dump()
        self.assertEqual(dumped["lines"][0]["gisbn"], "")


class OutboundStatusDetailGridTests(TestCase):
    """우측 라인 표(Sobo24.DBGrid102)가 ISBN 을 렌더한다."""

    def setUp(self) -> None:
        self.src = (
            FRONT / "components" / "transactions" / "transaction-status-screen.tsx"
        ).read_text(encoding="utf-8")

    def test_detail_line_table_renders_gisbn(self) -> None:
        # DEC-219 — 우측 라인 표가 DataGrid 로 바뀌어 ISBN 은 컬럼 정의(key: "gisbn")로 렌더된다
        self.assertIn('{ key: "gisbn", label: "ISBN", sortable: true', self.src)

    def test_left_slip_columns_default_order(self) -> None:
        """좌측 전표 목록 기본 순서 = (선택) 전표번호 · 거래일자 · 거래처 · 수량 · 금액 · 접수.

        2026-08-22 2차 요청으로 전표번호가 거래일자 앞으로 이동 — 입고 현황·출고 접수
        목록과 동일하게 전표번호가 선두다.

        거래처 칸은 2026-08-24 입고축 합류 후 축 파생 라벨(`party`)이다 —
        입고현황에서는 「입고처」로 렌더된다.
        """
        start = self.src.index("const slipDetailColumns")
        block = self.src[start : self.src.index("const lineColumns")]
        wanted = ['"전표번호"', '"거래일자"', "party", '"수량"', '"금액"', '"접수"']
        pos = []
        for label in wanted:
            idx = block.find(f"label: {label}")
            self.assertNotEqual(idx, -1, f"좌측 목록 컬럼 누락: {label}")
            pos.append(idx)
        self.assertEqual(pos, sorted(pos), f"좌측 목록 기본 순서 불일치: {wanted}")

    def test_select_column_is_first_and_not_reorderable(self) -> None:
        """「선택」은 prefs reorder 밖에서 항상 맨 앞에 붙는다."""
        self.assertIn("const detailCols = [\n    requestSelectCol,", self.src)
        self.assertIn('label: "선택"', self.src)


if __name__ == "__main__":
    main()
