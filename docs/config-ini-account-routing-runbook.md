# Config.Ini 기반 계정·라우팅 카탈로그 런북 (DSN-DEC-13)

| 항목 | 내용 |
| ---- | ---- |
| 작성일 | 2026-05-23 |
| 단일 원천(설계) | [docs/decision-login-db-routing.md](decision-login-db-routing.md) §DSN-DEC-13 |
| 카탈로그 도구 | [tools/build_config_account_routing_catalog.py](../tools/build_config_account_routing_catalog.py) |
| 입력 인벤토리 | [tools/inventory_legacy_config_ini.py](../tools/inventory_legacy_config_ini.py) → [`analysis/welove_config_ini_inventory.json`](../analysis/welove_config_ini_inventory.json) (591 건) |
| 산출 | [`analysis/welove_config_account_routing_catalog.json`](../analysis/welove_config_account_routing_catalog.json), [`analysis/welove_config_routing_review_queue.json`](../analysis/welove_config_routing_review_queue.json) |
| 회귀 | [`test/test_config_account_routing_catalog.py`](../test/test_config_account_routing_catalog.py), [.github/workflows/welove-routing-consistency.yml](../.github/workflows/welove-routing-consistency.yml) |
| 비밀 정책 | G3 — `UserName`/`Password`/DB 비번 미수집·미출력 |

---

## 0. 본 런북의 위치

**범위 안**:

- `WeLove_FTP/**/Config.Ini` 591 건을 raw → inventory → catalog 로 정규화하는 절차.
- 카탈로그를 통한 빌드·고객 폴더 단위 라우팅 라벨 추적.
- 운영 시드/매트릭스 불일치 발견 시 dry-run overlay 제안.

**범위 밖** (다른 런북 참조):

- 공유 DB `hcode_in` 격리 키 채움 → [docs/welove-cross-tenant-exposure-runbook.md](welove-cross-tenant-exposure-runbook.md), [tools/extract_shared_db_hcodes.py](../tools/extract_shared_db_hcodes.py).
- 개별 로그인 ID 인덱스 → [tools/build_login_id_index.py](../tools/build_login_id_index.py).
- 단일 계정 라우팅 진단 → [debug/diagnose_login_routing.py](../debug/diagnose_login_routing.py).

---

## 1. 일반 절차

```bash
# 1) Config.Ini 인벤토리 (591 건 — G3 sanitize)
python3 tools/inventory_legacy_config_ini.py

# 2) 카탈로그·review_queue 산출 (--apply 로 디스크 저장)
python3 tools/build_config_account_routing_catalog.py --apply

# 3) (선택) overlay dry-run 제안 — apply 는 절대 자동 수행하지 않음
python3 tools/build_config_account_routing_catalog.py --apply \
  --emit-overlay analysis/welove_config_routing_overlay_proposals.json

# 4) 정합 감사 — 운영 시드 정책 확인 (DSN-DEC-12)
python3 tools/audit_welove_routing_consistency.py --json | jq '.summary'

# 5) 회귀 묶음
python3 -m pytest test/test_inventory_legacy_config_ini.py \
                  test/test_config_account_routing_catalog.py -q
```

기대 행수 (현재 시점 기준):

| 항목 | 값 |
|------|-----|
| 인벤토리 | **591** 행 |
| 카탈로그 | 591 행 (행수 일치 가드 — `--strict`) |
| `match.status` 분포 | `matched` / `partial` / `review` / `infra_skip` |
| `confidence` 분포 | `high` / `medium` / `low` |
| `shared_db.is_shared` 행 | 시드의 동일 `(primary_server, db_name_logical)` ≥ 2 |

---

## 2. 카탈로그 행 해석

```json
{
  "config_path": "도서유통-출판/MySQL/도서유통/chul_03(한강도서)/Config.Ini",
  "config_kind": "customer_build",
  "account_family_inferred": "chul_03",
  "customer_folder": "한강도서",
  "client": { "name": "...", "uses": "...", "base": "...", "port": "...", "pcip1": "..." },
  "routing": {
    "primary_server_label": "서버3",
    "remote_id": "remote_153",
    "db_name_logical": "chul_03_db",
    "tenant_id": "...",
    "tenant_label_kor": "한강도서",
    "build_role": "distributor",
    "default_account_type": "T2_DIST"
  },
  "match": {
    "status": "matched|partial|review|infra_skip",
    "confidence": "high|medium|low",
    "sources": ["path_family", "matrix", "seed", "chul_pas", "label_fuzzy"],
    "reasons": []
  },
  "shared_db": { "is_shared": false, "needs_hcode_guard": false }
}
```

### `match.status`

| 코드 | 트리거 | 후속 처리 |
|------|--------|-----------|
| `matched` | family + matrix + seed 일치 (또는 family + matrix만) | 운영 시드와 정렬됨. `confidence=medium` 면 `reasons` 점검 |
| `partial` | family 추출됐지만 matrix·seed 둘 다 부재 | 신규 SKU 후보 — SME 가 매트릭스 추가 검토 |
| `review` | family 미추출 또는 `label_fuzzy` 단독 | review_queue 로 분리, SME 가 `tenant_id`/`account_family` 지정 |
| `infra_skip` | `config_kind` ∈ {`infra_mysql`, `infra_login`, `root_other`} | 카탈로그 보존, DSN 미연결 |

### `match.reasons` 주요 코드

| 코드 | 의미 |
|------|------|
| `family_has_multiple_seed_tenants` | 같은 family 에 활성 테넌트 2 건 이상 (예: `chul_09` → 위러브1·2·3·교문사) |
| `family_not_in_matrix_or_seed` | 신규/구빌드 SKU |
| `chul_remote_id_mismatch` / `chul_db_name_mismatch` | Chul.pas 의 호스트·DB 와 matrix 가 불일치 |
| `chul_unknown_host_ip:<ip>` | servers.yaml 에 없는 호스트 IP |
| `shared_db_no_hcode_guard` | 공유 DB 인데 시드 격리 키 부재 (DSN-DEC-12 가드 입력 필요) |
| `label_fuzzy_only` / `no_family_no_label_match` | review 큐 사유 |
| `seed_missing_for_family` / `matrix_missing_for_family` | 한쪽만 있어 정합 보강 필요 |

---

## 3. review_queue 처리 (SME)

`analysis/welove_config_routing_review_queue.json` 의 각 행은 SME 가 두 가지 중 하나로 결정한다.

1. **신규 매트릭스/시드 행 등록**: family 가 추출됐지만 매트릭스에 없는 경우 — 매트릭스 1 행 + tenants_directory overlay 1 행 추가 PR.
2. **빌드 무시 (인수인계 / 자료전송 변형)**: 더 이상 운영 라우팅과 연결되지 않는 폴더 — `notes` 또는 `customer_variants` 로만 기록.

기록 위치는 [migration/contracts/welove_build_coverage.yaml](../migration/contracts/welove_build_coverage.yaml) 의 `customer_variants` 또는 [migration/contracts/tenants_directory.yaml](../migration/contracts/tenants_directory.yaml) 의 신규 row.

권장: review 처리는 `Config.Ini` 의 `Uses` / `Name` 한글 라벨 해석이 필요해 **고급 모델 (Chat)** 에서 일괄 분류 후 PR 로 합치는 워크플로가 효율적이다 ([planning-model-tiers.mdc](../.cursor/rules/planning-model-tiers.mdc)).

---

## 4. dry-run overlay 제안

`--emit-overlay <path>` 로 생성되는 JSON 은 다음 조건을 모두 만족한 행만 담는다.

1. `match.confidence == "high"`
2. `match.sources` 에 `matrix` + `seed` 동시 존재
3. `match.reasons` 에 `chul_remote_id_mismatch` 또는 `chul_db_name_mismatch` 포함

이는 **Chul.pas 정본 vs 운영 매트릭스/시드** 불일치만을 잡고, `label_fuzzy` 단독 결정으로 시드를 흔드는 일을 막는다 (DSN-DEC-06).

실제 적용:

- 자동 apply 금지. 본 도구는 dry-run JSON 만 생성.
- 운영자가 [tools/apply_hcode_isolation_overlay.py](../tools/apply_hcode_isolation_overlay.py) 패턴 (또는 동등한 라우팅 전용 apply 스크립트) 으로 검토 후 `tenants_directory_overlay.json` 에 머지.
- 머지 후 [tools/audit_welove_routing_consistency.py](../tools/audit_welove_routing_consistency.py) `--strict` 가 통과해야 한다.

---

## 5. 자주 묻는 케이스

### 5.1 `chul_09(위러브)` 폴더가 4 곳에 흩어져 있다

`chul_09` 는 **공유 DB** (`chul_09_db` 4 테넌트). 카탈로그에서 `family_has_multiple_seed_tenants` + `shared_db.is_shared=true` 로 표기되며, **실제 사용자 → 테넌트 격리는 `hcode_in` 으로만 가능**하다 ([docs/welove-cross-tenant-exposure-runbook.md](welove-cross-tenant-exposure-runbook.md)). 본 카탈로그는 빌드 단위 메타까지만 책임진다.

### 5.2 `자료전송/<출판사>/Config.Ini` 가 `review` 로 분류

`config_kind=data_transfer` 폴더는 EDI/자료전송용 별도 빌드라 family 가 폴더 경로에 없다. 운영 라우팅과 무관 — `customer_variants` 로 기록하거나 단순 보관.

### 5.3 `Welove_인수인계/.../Chulpan.Net` 의 `Config.Ini` 가 다수

레거시 인수인계 보관본. family 가 폴더명에 없는 경우가 많아 `review` 로 분류된다. 운영 라우팅과 정합이 필요한 행은 SME 가 골라서 매트릭스에 추가, 그 외는 보관 처리.

---

## 6. 회귀 가드 체크리스트 (PR 용)

- [ ] `python3 tools/inventory_legacy_config_ini.py` 실행 후 `welove_config_ini_inventory.json` 의 `count == 591` (또는 신규 빌드 추가 시 +n)
- [ ] `python3 tools/build_config_account_routing_catalog.py --apply --strict` 통과 (행수 ↔ inventory.count 일치)
- [ ] `pytest test/test_inventory_legacy_config_ini.py test/test_config_account_routing_catalog.py -q` 통과
- [ ] (시드 변경 PR 한정) `tools/audit_welove_routing_consistency.py --strict` 의 `SHARED_COORD_NO_HCODE_GUARD` / `PRIMARY_SERVER_MISMATCH` / `DB_NAME_LOGICAL_MISMATCH` 0 또는 운영 화이트리스트 처리됨
- [ ] overlay 적용은 본 도구가 아닌 별도 단계에서 사람이 승인한 후 수행 — `--emit-overlay` 결과를 직접 머지하지 않음
- [ ] 본 런북·[docs/decision-login-db-routing.md](decision-login-db-routing.md) §DSN-DEC-13 과 서술 충돌 없음
