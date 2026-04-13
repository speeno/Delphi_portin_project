# 확보 델파이 소스 분석 절차

이 문서는 프로젝트에 반입된 델파이 소스(현재 1차: `WeLove_FTP/`)를 **정적 분석(L2)** 도구로 처리하는 순서를 정리합니다. 실행 기준은 저장소의 [`tools/run_analysis.py`](../tools/run_analysis.py) 및 개별 파서·[`README.md`](../README.md) 델파이/DB 가이드와 동일합니다.

## 0. 전제 조건

- **Python 3.10+** (파서·스크립트 실행)
- 소스 디렉터리: 예) `WeLove_FTP/` 전체 또는 분석용으로 복사한 `delphi-source/`
- **DB 분석(산출물 #4 등)**은 MariaDB 접속 정보가 있을 때 별도 절차([README.md](../README.md) 「DB 정보 입수 후 실행 가이드」)로 수행합니다. 소스만으로도 #1~#3, #5, #6 및 카탈로그 일부까지 진행 가능합니다.

## 1. 분석 전 준비 (권장)

### 1.1 분석 루트 정하기

- `WeLove_FTP/` 는 **도서유통-New·도서유통-출판 등 복수 트리**가 섞여 있어 용량·중복이 큽니다.
- **권장**: 포팅 1차 대상(예: 단일 고객/단일 제품 라인)만 `delphi-source/` 등으로 복사한 뒤 그 경로만 파이프라인에 넣습니다.
- **전체 스캔**이 필요하면 `python3 tools/run_analysis.py WeLove_FTP/` 로 가능하나, 시간·디스크·중복 폼/유닛이 많아질 수 있습니다.

### 1.2 스캔에서 제외할 파일(정책)

- **컴파일 산출**: `.dcu` 등 — 소스 분석 대상이 아님.
- **에디터 백업**: `.~pas`, `.~dfm`, `.~dpr` 등 — 필요 시 정책에 따라 제외하거나, 동일 유닛의 정본 `.pas`만 남기도록 디렉터리를 정리합니다.
- 저장소 [`.gitignore`](../.gitignore)에 일부 경로가 이미 있을 수 있으나, **파서는 디렉터리 트리를 직접 순회**하므로 “어느 폴더를 인자로 줄지”가 실질적인 필터입니다.

### 1.3 출력 디렉터리

- 파이프라인은 프로젝트 루트 기준으로 다음을 사용합니다.
  - `inventory/` — 예: `dpr_files.json`
  - `analysis/` — 폼·이벤트·SQL·검증·분기·카탈로그 등 JSON 산출

실행 전 해당 폴더가 없으면 `run_analysis.py`가 `inventory`·`analysis`를 생성합니다.

## 2. 통합 파이프라인 (1회 실행)

프로젝트 루트에서:

```bash
python3 tools/run_analysis.py <delphi_source_dir>
```

예:

```bash
python3 tools/run_analysis.py delphi-source/
# 또는 (주의: 규모 큼)
python3 tools/run_analysis.py WeLove_FTP/
```

### 2.1 내부 실행 순서 (`run_analysis.py`와 동일)

| 순서 | 단계 | 명령 역할 | 주요 산출 |
|------|------|-----------|-----------|
| 1 | DPR 파서 | `tools/parsers/dpr_parser.py` | `inventory/dpr_files.json` (프로젝트·유닛 구조) |
| 2 | DFM 파서 | `tools/parsers/dfm_parser.py` | `analysis/form_inventory.json` (**#1**), `analysis/event_flow.json` (**#2**) |
| 3 | PAS 파서 | `tools/parsers/pas_parser.py` | `analysis/query_catalog.json` (**#3**), `analysis/validation_rules.json` (**#5**), `analysis/customer_variants.json` (**#6**), `analysis/unit_dependency_graph.json` (유닛 의존) |
| 4 | Legacy Object Catalog | `tools/catalog_builder.py` | `analysis/legacy_object_catalog.json` |

종료 후 **요약**이 `analysis/sprint1_report.json` 에 기록됩니다.

### 2.2 단계 실패 시

- `run_analysis.py`는 하위 단계가 비정상 종료해도 다음 단계를 시도합니다(코드상 `WARNING`만 출력).
- 특정 단계만 다시 돌리려면 아래 **3절** 개별 실행을 사용합니다.

## 3. 개별 파서만 실행 (필요 시)

프로젝트 루트·`<delphi_source_dir>` 기준:

```bash
# .dpr
python3 tools/parsers/dpr_parser.py <delphi_source_dir> inventory/dpr_files.json

# .dfm → #1, #2
python3 tools/parsers/dfm_parser.py <delphi_source_dir> analysis/

# .pas → #3, #5, #6 + unit_dependency_graph
python3 tools/parsers/pas_parser.py <delphi_source_dir> analysis/
```

카탈로그만 재생성:

```bash
python3 tools/catalog_builder.py analysis/ analysis/legacy_object_catalog.json
```

## 4. DB 연계 분석 (선행: 스키마·SQL)

**비밀 관리**: DB 호스트·계정·비밀번호는 **Git에 추적되는 파일에 넣지 마세요.** 로컬 `.env`에만 두고(`.gitignore` 적용), 변수 이름 예시는 프로젝트 루트 [`.env.example`](../.env.example)를 참고하세요. `schema_extractor.py`는 현재 CLI 인자(`--host`, `--password` 등)를 받습니다. 인자에 직접 비밀번호를 쓰면 셸 히스토리에 남을 수 있으니, 가능하면 환경 변수에서 읽어 채우는 방식(또는 대화형 입력)을 팀에서 권장할 수 있습니다.

소스 기반 **#3 SQL 카탈로그**와 결합해 **#4 DB 영향도**를 만들려면 README의 다음 흐름을 따릅니다.

1. `tools/db/schema_extractor.py` — 스키마 JSON (`analysis/tables.json` 등)
2. (선택) `tools/db/db_impact_builder.py` — SQL 카탈로그 + 스키마 → 영향도 매트릭스
3. (운영) `tools/db/query_capture.py` — 캡처 하네스와 연계한 쿼리 수집

자세한 인자는 [README.md](../README.md) 「DB 정보 입수 후 실행 가이드」 참고.

## 5. 산출물 점검 체크리스트

- [ ] `inventory/dpr_files.json` 존재·크기 합리적
- [ ] `analysis/form_inventory.json`, `event_flow.json` 존재
- [ ] `analysis/query_catalog.json`, `validation_rules.json`, `customer_variants.json` 존재
- [ ] `analysis/unit_dependency_graph.json` 존재(PAS 파서 경로)
- [ ] `analysis/legacy_object_catalog.json` 존재
- [ ] `analysis/sprint1_report.json`으로 각 산출물 건수·상태 확인
- DB 연계 시: `analysis/db_impact_matrix.json`(또는 `_full` 등 빌더 출력) 확인

## 6. 상태 추적·대시보드와의 연동 (L6)

- 분석 진행·이슈는 [`legacy-analysis/progress.md`](../legacy-analysis/progress.md), [`legacy-analysis/open-questions.md`](../legacy-analysis/open-questions.md) 등에 반영합니다.
- 대시보드 JSON(`dashboard/data/deliverables.json` 등)은 팀 정책에 따라 산출물 완료도와 맞춰 수동 갱신할 수 있습니다.

## 7. 이후 단계(참고)

정적 분석 산출물은 **마이그레이션 계약·Eval 케이스·하네스**로 이어집니다.

- `tools/contracts/contract_generator.py`, `eval_case_generator.py`
- `tools/harness/` 파이프라인·골든마스터·비교 하네스

해당 범위는 [harness-architecture.md](../harness-architecture.md), [harness_runbook.md](harness_runbook.md)를 따릅니다.

---

*본 절차는 저장소 도구 기준으로 작성되었으며, 파서 동작 세부사항은 각 `tools/parsers/*.py` 구현을 기준으로 합니다.*
