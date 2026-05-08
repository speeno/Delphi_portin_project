# C9 마스터 쓰기 잔여 — 5축 회귀 매트릭스 (v1.4.0, 2026-05-08)

## 범위

| 축 | 항목 |
| --- | --- |
| 계약 | `migration/contracts/master_data.yaml` v1.4.0 — SQL-MAS-7/8/9 (publisher / book-code alias / discount + variant) |
| 백엔드 | `masters_service` + `routers/masters.py` — `master.write` 가드(`require_permission`) |
| 프론트 | `/master/publisher`, `/master/book-code`, `/master/discount` + `master-api.ts` |
| 테스트 | `test_master_*_crud_api_contract.py` ×3, `test_master_crud_api_contract.py`, `test_masters_q_search.py`, `test_pagination_contracts.py::C9MastersListPageContract` |
| 스모크 | `debug/probe_backend_all_servers.py` — masters.book_code / masters.discount GET + publisher·book-code·discount POST/PATCH/DELETE 비파괴(422/404) |

## DoD 체크리스트

- [ ] `pytest test/test_master_publisher_crud_api_contract.py test/test_master_book_code_crud_api_contract.py test/test_master_discount_crud_api_contract.py` PASS
- [ ] `pytest test/test_master_crud_api_contract.py test/test_masters_q_search.py test/test_pagination_contracts.py::C9MastersListPageContract` PASS
- [ ] `master.write` 미보유 시 신규 쓰기 엔드포인트 → 403
- [ ] `audit.master` 1줄 JSON — `entity` publisher / book_code / discount + book-code alias 시 `via: book`

## 참조

- DEC-019 (3폼 한정 INSERT/DELETE 해제) — `master_data.yaml` decisions
- DEC-028 — `data-legacy-id` (Panel002·Button101 등)
- 멀티 DB — `.cursor/rules/multi-db-compat.mdc`
