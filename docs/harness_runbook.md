# 하네스 운영 런북

## 1. 일상 운영

### 1.1 일일 점검 사항
1. Comparison Harness 불일치 건수 확인 → 대시보드 확인
2. Routing Harness 현재 전환 비율 확인
3. 에러 로그 확인 (API 서버, 하네스 미들웨어)
4. 응답 시간 추이 확인

### 1.2 대시보드 데이터 업데이트
```bash
# 하네스 파이프라인 실행 후 대시보드 데이터 갱신
python tools/harness/pipeline.py \
  --capture-dir captured/ \
  --eval-dir migration/test-cases/ \
  --comparison-dir comparison_results/ \
  --routing-config tools/harness/routing_config.json \
  --dashboard-output dashboard/data/pipeline.json

# Git push로 대시보드 반영
git add dashboard/data/ && git commit -m "Update dashboard data" && git push
```

---

## 2. 점진적 전환

### 2.1 전환 비율 변경
```bash
# 현재 상태 확인
python tools/harness/progressive_rollout.py \
  --routing-config tools/harness/routing_config.json \
  --comparison-dir comparison_results/ \
  --action status

# 다음 단계로 전환 (10% → 30% → 50% → 80% → 100%)
python tools/harness/progressive_rollout.py \
  --routing-config tools/harness/routing_config.json \
  --comparison-dir comparison_results/ \
  --action next
```

### 2.2 전환 조건
- Comparison 불일치율 = 0%
- 현재 단계에서 최소 24시간 안정 운영
- 에러율 < 1%
- Go/No-Go 체크 통과

### 2.3 Go/No-Go 판단
```bash
python tools/harness/go_nogo.py \
  --comparison-dir comparison_results/ \
  --eval-report analysis/eval_report.json \
  --routing-config tools/harness/routing_config.json \
  --approvals dashboard/data/approvals.json \
  --output go_nogo_report.json
```

---

## 3. 장애 대응

### 3.1 즉시 롤백
```bash
# 긴급 롤백 (1분 내 100% 레거시 복귀)
python tools/harness/progressive_rollout.py \
  --routing-config tools/harness/routing_config.json \
  --action rollback \
  --reason "긴급 롤백: [사유]"
```

### 3.2 Comparison 불일치 발생 시
1. 불일치 로그 확인: `comparison_results/comparison_YYYY-MM-DD.jsonl`
2. 불일치 유형 분류:
   - `value_mismatch`: 데이터 값 차이 → 로직 버그 가능성
   - `missing_in_new`: 신규 시스템에서 누락 → 기능 미구현
   - `status_code`: HTTP 상태 코드 차이 → 에러 핸들링 불일치
3. 버그 수정 후 재비교
4. 전환 비율 변경 전까지 불일치 0건 확인

### 3.3 하네스 자체 장애
1. 하네스 미들웨어 장애 → 바이패스 모드로 전환
   - `routing_config.json`의 `mode`를 `legacy_only`로 수동 변경
2. Comparison Harness 장애 → 비교 일시 중단 (운영에 영향 없음)
3. 캡처 파이프라인 장애 → 캡처 재시작

---

## 4. Feature Toggle 관리

### 4.1 개별 기능 토글
```python
# routing_config.json 직접 편집
{
  "feature_toggles": {
    "api.inbound.create": {"enabled": true, "percent": 50},
    "api.outbound.create": {"enabled": false, "percent": 0}
  }
}
```

### 4.2 고객사별 롤아웃
```python
# routing_config.json의 user_groups
{
  "user_groups": {
    "pilot": ["user001", "user002"],
    "beta": ["user003", "user004", "user005"]
  }
}
```

---

## 5. 모니터링 지표

| 지표 | 정상 범위 | 경고 임계값 | 조치 |
|------|-----------|-------------|------|
| Comparison 불일치율 | 0% | > 0% | 전환 중단, 원인 분석 |
| API 에러율 | < 0.1% | > 1% | 즉시 롤백 |
| 응답 시간 비율 | < 120% | > 150% | 성능 프로파일링 |
| 캡처 파이프라인 | 동작 중 | 중단 | 재시작 |

---

## 6. L1 인수인계 자산 반입 절차 (`MAN-*` / `SCH-*` / `DSN-*` / `ONB-*`)

본 절차는 [`harness-architecture.md` L1](../harness-architecture.md#L1) 의 운영 측면이다 — 신규 인수인계 자산이 도착했을 때 따른다.

### 6.1 메뉴얼 (`MAN-*`)

1. 신규 파일을 [`WeLove_FTP/Welove_인수인계/`](../WeLove_FTP/Welove_인수인계) 하위 적정 폴더에 보존.
2. [`docs/manual-catalog.md`](manual-catalog.md) §2~§4 표에 1 행 추가 — 채널·주제·비밀 표기(○/△/×)를 [`docs/secrets-policy.md`](secrets-policy.md) 기준으로 분류.
3. 비밀 자산(○)은 본문 인용 금지, 메타만 §5 매핑 표에 합류.

### 6.2 스키마 사전 (`SCH-WELOVE-출판-*`)

1. `MAN-030` ([`출판(테이블구조).xls`](../WeLove_FTP/Welove_인수인계/출판setting/weelove/출판(테이블구조).xls)) 가 갱신되면:
   ```bash
   python3 tools/extract_welove_schema.py
   ```
2. 갱신된 [`analysis/welove_schema_dictionary.json`](../analysis/welove_schema_dictionary.json) 와 운영 DB 스키마(`tools/db/schema_diff.py`) 를 [`docs/welove-schema-reconciliation.md`](welove-schema-reconciliation.md) §3 표로 교차 검증.
3. 신규 불일치는 `SCH-RECON-*` ID 부여 후 OQ 등록.

### 6.3 DSN 라우팅 메타 (`DSN-*`)

1. `MAN-017` 또는 `MAN-018` (`DB정보·DB_FTP 엑셀정리.xlsx`) 가 갱신되면:
   ```bash
   python3 tools/extract_welove_db_routes.py
   ```
2. 갱신된 [`analysis/welove_db_route_matrix.json`](../analysis/welove_db_route_matrix.json) 의 `routes[]` 와 admin 화면(DEC-052) 을 정합 — 신규 테넌트는 (메타 1행) + (vault 비번 적재) + (admin 라디오 노출) 3 단계 PR.
3. 본 JSON 에는 절대 자격증명을 추가하지 않는다 — `has_credentials_in_source` 플래그만 갱신.

### 6.4 온보딩·RBAC 매트릭스 (`ONB-*` / `ACC-*`)

1. 회의/SME 결과로 계정 유형·메뉴 노출이 변경되면 [`docs/onboarding-rbac-menu-matrix.md`](onboarding-rbac-menu-matrix.md) §2~§7 의 표 1행 갱신.
2. 본 표 변경은 PermissionGuard / 라우터 가드 PR 의 1차 입력 — 커밋 메시지에 `ACC-MENU-*` 또는 `ACC-API-*` 추적 ID 명시.
3. 가입 트랙 정책(A AND B / A OR B / A only) 변경은 [`docs/onboarding-governance-spec.md`](onboarding-governance-spec.md) §3 의 옵션을 굵게 동결한 후 DEC ONB-001 로 등록.

### 6.5 회귀 시나리오 갱신

신규 계정 유형 또는 가입 정책 변경 시 다음 4 시나리오를 반드시 갱신/추가한다 — [`docs/manual-to-scenario-matrix.md`](manual-to-scenario-matrix.md) §3:

| ID | 트리거 |
|----|---|
| `SCN-MIN-T1-01` | admin 콘솔 변경 |
| `SCN-MIN-T2-DIST-01` | 총판 승인 흐름 변경 |
| `SCN-MIN-T2-PUB-01` | 가입 게이트(A/B 옵션) 변경 |
| `SCN-MIN-T3-01` | 독립 출판사 트랙·DSN 부여 변경 |

---

*문서 버전: v1.1*
*작성일: 2026-04-11 (v1.0) → 2026-04-23 (v1.1: §6 L1 반입 절차 추가)*
