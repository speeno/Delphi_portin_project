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

*문서 버전: v1.0*
*작성일: 2026-04-11*
