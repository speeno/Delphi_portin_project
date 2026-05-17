# W5 — 발송비/입금 메뉴 P3 (레거시 전용) 착수 로드맵

**원천**: `migration/coverage/billing-deposit-menu-legacy-to-web-map.md` §4  
**전제**: P2 진짜 발송비(`Sobo43_shipping_ledger` / `Sobo44_shipping_status`)는 `billing-subu43-44-shipping-backlog.md` 트랙과 병행한다.

## 시나리오 카드 1건씩 (권장 순서)

| 우선순위 | 레거시 참조 | 웹 방향(초안) | 산출물 |
|----------|-------------|---------------|--------|
| P3 | `Sobo24_9` 등 명세서 발송건수 | 정산·리포트 IA 하에서 별도 라우트 또는 기존 명세서 화면 확장 | `analysis/screen_cards/Sobo24_9.md` + 계약 초안 |
| P3 | `Sobo38_1` 운임관리-택배 | `Sobo28_delivery` 와 경계 정리 후 택배 변형 전용 플로우 | `migration/contracts/` 확장 또는 신규 yaml |
| P3 | `Seok30` 메시지 팝업 | Wave D 알림 통합 후보 — UI 스텁 vs 백엔드 이벤트만 | DEC + `phase2_screen_blockers.yaml` |

## DoD (카드 착수)

- `form-registry.ts` 에 **신규 ID** (기존 wrong_id 라우트 **변경 없이**).
- `dashboard/data/phase2-screen-cards.json` T1 한 줄 이상.
- `debug/probe_backend_all_servers.py` 에 신규 GET 이 있으면 그룹 1행 추가.
