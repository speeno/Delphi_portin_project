# DB 연동 점검 런북 (멀티 DB API smoke)

백엔드 ↔ `servers.yaml` 의 모든 DB(현재 4대: 138 / 153 / 154 / 155)에서 핵심 GET API 가 정상 응답하는지 확인하는 절차. C5 정산 회귀 사건(2026-04 `Sdate` 컬럼 누락) 이후, 동일한 종류의 문제를 사전에 잡기 위한 표준화된 점검 도구.

## 범위 (점검 계층)

| 계층 | 항목 | 설명 |
|----|----|----|
| L0 | 설정 요약 | `servers.yaml` 프로필 — id / db / ssh / mysql3 |
| L2 | DB 추상화 | `execute_query("SELECT 1")` — 단일 진입점 통과 여부 |
| L4 | 라우터 GET | FastAPI `TestClient` + `dependency_overrides` 로 인증 우회 후 핵심 GET 매트릭스 호출 |
| R | 리포팅 | 콘솔 + 옵션 JSON artifact |

L4 매트릭스(서버별):

```
common.servers / common.health
masters.customer / masters.book / masters.publisher
outbound.orders / inbound.receipts / returns.list
settlement.cash
settlement.cash_status_hcode / settlement.cash_status_sdate
settlement.billing
transactions.statement
```

## 로컬 실행

```bash
PYTHONPATH=도서물류관리프로그램/backend \
  python3 debug/probe_backend_all_servers.py \
  --layer all \
  --date-from 2026.04.01 --date-to 2026.04.30 --month 202604 \
  --write-json artifacts/db-smoke.json
```

옵션:

- `--layer l2|l4|all` — 검증 계층 선택 (기본 `all`).
- `--include-cancelled` — 목록 GET 의 `includeCancelled=true` 토글.
- `--write-json PATH` — 결과 JSON 저장(비밀 없음, CI artifact 용).

환경 변수:

- `RUN_DB_SMOKE=1` 미설정 → **dry-run** (라우터/서버 매트릭스만 인쇄, 네트워크 호출 없음).
- `RUN_DB_SMOKE=1` 설정 → **live** (실제 SSH 터널 + DB + 라우터 호출).

## 출력 형식 (JSON 스키마)

```jsonc
{
  "checkedAt": "2026-04-19T18:00:00+09:00",
  "mode": "live | dry-run",
  "layer": "l2 | l4 | all",
  "servers": [
    { "id": "remote_138", "label": "...", "host": "...", "db": "chul_09_db",
      "mysql3": false, "ssh": true, "ssh_host": "..." }
  ],
  "l2": {
    "remote_138": { "layer": "L2", "ok": true, "detail": "rows=1 mysql3=False" }
  },
  "l4": {
    "remote_138": [
      { "layer": "L4", "group": "settlement.cash_status_sdate",
        "path": "/api/v1/settlement/cash-status?...",
        "ok": true, "status": 200, "detail": "200 bytes=123" }
    ]
  }
}
```

DoD (Definition of Done):

- L2: 모든 서버 SELECT 1 = `ok:true`.
- L4: `ok:false` 가 0건. 빈 결과(예: 해당 기간 거래 없음)는 200 으로 처리되므로 OK.
- 알려진 스키마 차이로 200 이 아닌 경우(예: T5_Ssub `Sdate` 누락 → 어댑터 적용 후에도 일부 테이블 누락) → reason 분류 후 `analysis/decisions.md` 또는 `customer_variants` 에 기록.

## 정기 점검 / opt-in CI

워크플로우 파일: `.github/workflows/db-smoke.yml`.

정책:

1. **PR/Push 자동 트리거 금지** — DB 비밀 노출 위험 + 외부 망/SSH 의존.
2. `workflow_dispatch` 로 수동 실행 가능 (`layer`, `include_cancelled` 입력).
3. `schedule` 로 매주 월 09:00 KST 실행 — `RUN_DB_SMOKE` secret + `SERVERS_YAML` secret 둘 다 설정된 환경에서만 실효성. 둘 중 하나라도 없으면 자동으로 dry-run 으로 강등.
4. 결과는 `db-smoke` artifact 로만 보존, 콘솔/로그에는 비밀이 출력되지 않게 한다 (스크립트가 host/port 만 인쇄).
5. 실패 시 (DoD 위반) → 별도 이슈/Slack 알림은 후속 작업으로 분리.

필요한 GitHub secrets:

| Secret | 용도 |
|----|----|
| `RUN_DB_SMOKE` | `1` 일 때만 live 모드 |
| `SERVERS_YAML` | `도서물류관리프로그램/backend/config/servers.yaml` 의 전체 텍스트 |
| (선택) `SSH_KEY` | SSH 터널 사용 서버용 키 (config 내 경로가 actions 내 키 위치를 가리키도록 유지) |

## 변경 시 점검 체크리스트

새 라우터 GET 또는 새 서비스 함수 추가 시:

1. `_routes_for(server_id, args)` 에 그룹 1개 추가.
2. `LIMIT %s OFFSET %s` 패턴이 새로 들어왔다면 `app/core/sql_mysql3.py` 의 `apply_limit_offset_syntax` + `limit_offset_bind` 적용.
3. T5_Ssub 처럼 변종 스키마가 있는 테이블을 새로 사용한다면 `app/services/<table>_adapt.py` 패턴으로 어댑터 추가.
4. dry-run 으로 매트릭스 변경 확인 후, 가능하면 로컬 live 실행으로 한 번 검증.

## 관련 결정/문서

- **DEC-033** (`legacy-analysis/decisions.md`): 멀티 DB 호환 의무 — `sql_mysql3` 페이지네이션, `<table>_adapt.py` 스키마 어댑터, `probe_backend_all_servers.py` 매트릭스 등록 (`.cursor/rules/multi-db-compat.mdc` alwaysApply).
- DEC-031, DEC-032 (`legacy-analysis/decisions.md`): 정산 close 정책, Gpass 회전 정책.
- `docs/mysql-3.23-legacy-connection-notes.md`: 154/155 핸드셰이크 호환 메모.
- `docs/core-scenarios-porting-plan.md` 룰 7: `dfm→html` 산출물 입력화.
