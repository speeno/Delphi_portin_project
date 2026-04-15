# 확보 델파이 소스 분석 절차

이 문서는 프로젝트에 반입된 델파이 소스(현재 1차: `WeLove_FTP/`)를 **정적 분석(L2)** 도구로 처리하는 순서를 정리합니다. 실행 기준은 저장소의 [`tools/run_analysis.py`](../tools/run_analysis.py) 및 개별 파서·[`README.md`](../README.md) 델파이/DB 가이드와 동일합니다.

## 0. 전제 조건

- **Python 3.10+** (파서·스크립트 실행)
- 소스 디렉터리: 예) `WeLove_FTP/` 전체 또는 분석용으로 복사한 `delphi-source/`
- **통합 파이프라인**(`run_analysis.py`)은 SQL 카탈로그만으로 **산출물 #4**(영향도 매트릭스 JSON)를 `tools/db/db_impact_builder.py`로 생성합니다(DB 연결 불필요). **실 DB 스키마 덤프·`schema_extractor.py`** 는 [README.md](../README.md) 「DB 정보 입수 후 실행 가이드」 등 별도 절차입니다.

## 1. 분석 전 준비 (권장)

### 1.1 분석 루트 정하기

- **`legacy_delphi_source/`** (일부 워크스페이스): 현재 트리에서는 `.pas`/`.dfm`이 **`legacy_delphi_source/legacy_source/` 한곳**에만 있습니다. 폼·PAS를 함께 맞추려면 인자로 **`legacy_delphi_source/legacy_source`** 또는 상위 **`legacy_delphi_source`** 를 주세요. `legacy_source` 밖의 다른 하위만 지정하면 해당 폴더에 `.dfm`이 없어 DFM 산출물이 비게 됩니다.
- `WeLove_FTP/` 는 **도서유통-New·도서유통-출판 등 복수 트리**가 섞여 있어 용량·중복이 큽니다.
- **권장**: 포팅 1차 대상(예: 단일 고객/단일 제품 라인)만 `delphi-source/` 등으로 복사한 뒤 그 경로만 파이프라인에 넣습니다.
- **전체 스캔**이 필요하면 `python3 tools/run_analysis.py WeLove_FTP/` 로 가능하나, 시간·디스크·중복 폼/유닛이 많아질 수 있습니다.

### 1.2 소스 파일 인코딩

- 파서(`.pas`/`.dfm`/`.dpr`)는 [`tools/parsers/delphi_source_encoding.py`](../tools/parsers/delphi_source_encoding.py) 기준으로 **UTF-8(BOM)·UTF-8·CP949·EUC-KR** 순으로 읽습니다. 한국 레거시 소스가 CP949인 경우 `validation_rules.json` 등 문자열 리터럴이 깨지지 않습니다.

### 1.3 스캔에서 제외할 파일(정책)

- **컴파일 산출**: `.dcu` 등 — 소스 분석 대상이 아님.
- **에디터 백업**: `.~pas`, `.~dfm`, `.~dpr` 등 — 필요 시 정책에 따라 제외하거나, 동일 유닛의 정본 `.pas`만 남기도록 디렉터리를 정리합니다.
- 저장소 [`.gitignore`](../.gitignore)에 일부 경로가 이미 있을 수 있으나, **파서는 디렉터리 트리를 직접 순회**하므로 “어느 폴더를 인자로 줄지”가 실질적인 필터입니다.

### 1.4 출력 디렉터리

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
| 2 | DFM 파서 | `tools/parsers/dfm_parser.py` | `analysis/form_inventory.json` (**#1**), `analysis/event_flow.json` (**#2**), `analysis/dfm_summary.json` |
| 3 | PAS 파서 | `tools/parsers/pas_parser.py` | `analysis/query_catalog.json` (**#3**), `analysis/validation_rules.json` (**#5**), `analysis/customer_variants.json` (**#6**), `analysis/unit_dependency_graph.json` (유닛 의존) |
| 4 | DB Impact Matrix | `tools/db/db_impact_builder.py` | `analysis/db_impact_matrix.json` (**#4**, SQL 카탈로그·이벤트 흐름·PAS 인벤토리 기반) |
| 5 | Legacy Object Catalog | `tools/catalog_builder.py` | `analysis/legacy_object_catalog.json` |

종료 후 **요약**이 `analysis/sprint1_report.json` 에 기록됩니다.

### 2.1.1 산출물 #1·#2·#4가 `미생성`으로만 보일 때

- **`sprint1_report.json`** 은 각 JSON **파일 존재 여부**로만 완료/미생성을 판별합니다.
- **#1·#2**: 인자로 준 `<delphi_source_dir>` 아래에 **`.dfm` 이 한 개도 없으면**(예: `.pas`만 있는 하위 폴더만 지정) 이전 구현은 산출 파일을 만들지 않고 PAS만 진행될 수 있었습니다. 현재는 **빈 배열 JSON**을 써서 리포트와 후속 단계가 일치합니다. 전체 트리를 쓰려면 예: `WeLove_FTP/` 를 인자로 주세요.
- **#4**: 통합 파이프라인에 **`db_impact_builder` 단계가 포함**되어 있어, PAS 이후 `analysis/db_impact_matrix.json` 이 생성됩니다. 예전에 수동으로만 돌렸다면 한 번 `run_analysis.py` 전체를 다시 실행하세요.

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

**소스만으로 #4**: `run_analysis.py` 가 `db_impact_builder.py` 를 호출해 `analysis/db_impact_matrix.json` 을 만듭니다(SQL 카탈로그·이벤트 흐름·`pas_inventory.json` 기반).

**실 DB 스키마와 결합**하려면 README의 다음 흐름을 추가로 따릅니다.

1. `tools/db/schema_extractor.py` — 스키마 JSON (`analysis/tables.json` 등)
2. (선택) 스키마·캡처 결과와 병합한 확장 영향도 — 팀 정책에 따라 별도 스크립트 또는 수동
3. (운영) `tools/db/query_capture.py` — 캡처 하네스와 연계한 쿼리 수집

자세한 인자는 [README.md](../README.md) 「DB 정보 입수 후 실행 가이드」 참고.

호스트별 **연결만** 빠르게 확인할 때는 [`debug/db_connect_probe.py`](../debug/db_connect_probe.py)로 `MARIADB_PASSWORD` 등을 환경 변수로 준 뒤 실행하고, `--write-json dashboard/data/db-status.json`으로 대시보드용 요약을 갱신할 수 있습니다(비밀은 JSON에 쓰이지 않음). **MySQL 3.23(극구버전)** 인스턴스는 이 스크립트와 다른 클라이언트가 필요할 수 있으며, 115.68.3.154/155 테스트 요약은 [`mysql-3.23-legacy-connection-notes.md`](mysql-3.23-legacy-connection-notes.md)를 참고합니다.

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
