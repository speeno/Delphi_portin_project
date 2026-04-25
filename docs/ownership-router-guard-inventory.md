# 로그인 DB 소유권 가드 인벤토리

로그인 DB 고정 계획의 Phase 1 기준으로, 도메인 라우터의 `serverId` 입력 지점과 공통 가드 적용 상태를 정리했다.

## 점검 기준

- 대상 라우터: `inbound`, `transactions`, `outbound`, `inventory`, `ledger`, `settlement`, `returns`, `reports`, `stats`, `masters`, `print`
- 필수 조건: 각 라우터 `APIRouter`에 `dependencies=[Depends(require_server_ownership("serverId"))]` 존재
- 결과 해석: `guard=True` 면 해당 라우터의 모든 엔드포인트가 로그인 서버 소유권 검증을 공통 적용받는다.

## 인벤토리 결과

- `inbound.py`: `serverId` 파라미터 7건, `guard=True`
- `transactions.py`: `serverId` 파라미터 3건, `guard=True`
- `outbound.py`: `serverId` 파라미터 5건, `guard=True`
- `inventory.py`: `serverId` 파라미터 1건, `guard=True`
- `ledger.py`: `serverId` 파라미터 2건, `guard=True`
- `settlement.py`: `serverId` 파라미터 14건, `guard=True`
- `returns.py`: `serverId` 파라미터 10건, `guard=True`
- `reports.py`: `serverId` 파라미터 3건, `guard=True`
- `stats.py`: `serverId` 파라미터 4건, `guard=True`
- `masters.py`: `serverId` 파라미터 9건, `guard=True`
- `print.py`: `serverId` 파라미터 4건, `guard=True`

## 결론

- Phase 1 대상 라우터 전체에 서버 소유권 가드가 적용됨.
- 현재 대상 라우터군에서는 `tenant_id` 입력 엔드포인트가 없어서, `assert_tenant_ownership`의 라우터별 추가 적용 포인트는 없음.
