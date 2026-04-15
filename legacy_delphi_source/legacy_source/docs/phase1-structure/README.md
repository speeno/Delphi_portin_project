# 1단계 산출물: 구조·화면·DB (도서유통-New)

이 폴더는 **루트 [`Chulpan.dpr`](../../Chulpan.dpr)** 기준 빌드 클로저와, 저장소 안의 다른 변형(`book_*` 등)과의 **대조**를 정리합니다. 생성에는 [`debug/delphi_build_closure.py`](../../debug/delphi_build_closure.py), [`debug/phase1_generate_reports.py`](../../debug/phase1_generate_reports.py) 및 아래 각 스크립트를 사용합니다.

## 이해관계자·준비도 (먼저 읽기)

| 문서 | 설명 |
|------|------|
| [00-phase1-summary-for-stakeholders.md](00-phase1-summary-for-stakeholders.md) | 비전문가용 요약, 차트(`figures/`), 리스크 |
| [00-porting-readiness-checklist.md](00-porting-readiness-checklist.md) | 웹 포팅 전 정보 충분성 체크리스트 |
| [00-wireframe-coverage-gap.md](00-wireframe-coverage-gap.md) | 화면 스펙 vs 와이어프레임 SVG 일치 여부 |
| [figures/](figures/) | `generate_phase1_charts.py`로 생성한 SVG 차트 |

## 산출물 인덱스

| 파일 | 설명 |
|------|------|
| [01-build-closure.md](01-build-closure.md) | DPR 기준 `uses` 클로저(예: 129유닛), CreateForm 요약 |
| [02-variant-chulpan-catalog.md](02-variant-chulpan-catalog.md) | `Chulpan.dpr` 변형 카탈로그 |
| [03-variant-dpr-diff.md](03-variant-dpr-diff.md) | 변형 간 DPR `uses` 차이 |
| [03b-variant-sample-diff-Subu30.md](03b-variant-sample-diff-Subu30.md) | 샘플 유닛 unified diff |
| [04-variant-core-matrix.md](04-variant-core-matrix.md) | `Base01` / `Chul` / `Subu30` 등 핵심 파일 해시 |
| [05-book-member-registry.md](05-book-member-registry.md) | `book_*` 멤버 레지스트리 |
| [05-book-member-registry.csv](05-book-member-registry.csv) | 위 내용 CSV (UTF-8 BOM) |
| [06-forms-runtime-graph.md](06-forms-runtime-graph.md) | `Chul` MDI·Show/ShowModal 그래프 |
| [07-book-member-delta.md](07-book-member-delta.md) | 변형 간 Base01/Chul/Subu30·dfm 차이 |
| [08-base01-inventory.md](08-base01-inventory.md) | `Base01` 인벤토리 |
| [09-settings-external.md](09-settings-external.md) | Config.Ini, Registry, FTP 등 |
| [10-report-deps.md](10-report-deps.md) | Tong02/04/06·Word·FastReport 의존성 |
| [11-screen-business-flows.md](11-screen-business-flows.md) | 메인 메뉴·업무 흐름 (`generate_chul_menu_flows.py`) |
| [11-screen-business-flows-graphs.md](11-screen-business-flows-graphs.md) | 위와 동일 내용 Mermaid |
| [12-screen-specification.md](12-screen-specification.md) | 화면 상세(DFM 캡션, 메뉴 경로, 컴포넌트 수 등) |
| [12-screen-specification.csv](12-screen-specification.csv) | 화면 스펙 CSV |
| [13-db-surface.md](13-db-surface.md) | SQL/테이블 참조 요약 (`extract_db_sql_references.py`) |
| [13-db-sql-references.csv](13-db-sql-references.csv) | SQL 토큰별 히트 행 (UTF-8 BOM) |
| [14-mysql-schema.sql](14-mysql-schema.sql) | *(선택)* 라이브 DDL (`check_mysql_hosts.py --export`) |
| [14-mysql-columns.csv](14-mysql-columns.csv) | *(선택)* `information_schema.COLUMNS` |
| [14-mysql-tables-summary.md](14-mysql-tables-summary.md) | *(선택)* 테이블/엔진/추정 행 수 |
| [14-db-code-vs-live.md](14-db-code-vs-live.md) | 코드 vs 라이브 테이블명 (export 후 자동 갱신) |
| [15-db-porting-and-optimization.md](15-db-porting-and-optimization.md) | DB 포팅·최적화 노트 (`generate_db_porting_report.py`) |
| [15-db-table-usage.csv](15-db-table-usage.csv) | 테이블별 히트·라이브 포함 여부 |
| [16-socket-runsql-surface.md](16-socket-runsql-surface.md) | 소켓·`RunSQL` 경로 개요 |
| [wireframes/README.md](wireframes/README.md) | DFM 기반 와이어프레임 SVG (`generate_wireframes.py`) |

## 권장 재생성 순서 (로컬)

저장소 루트 `도서유통-New`에서:

```bash
# 클로저·변형 리포트(필요 시)
python3 debug/phase1_generate_reports.py

# 화면 스펙 → 와이어프레임
python3 debug/generate_screen_specification.py
python3 debug/generate_wireframes.py --all

# 메뉴 플로우(수정 시)
python3 debug/generate_chul_menu_flows.py

# DB 정적 스캔
python3 debug/extract_db_sql_references.py

# 라이브 MySQL (자격 증명은 환경 변수만; 비밀번호 커밋 금지)
pip install -r debug/requirements-db.txt
export MYSQL_USER='...'
export MYSQL_PASSWORD='...'
export MYSQL_HOST='...'
# 구형 MySQL utf8mb4 오류 시: export MYSQL_CHARSET=utf8
python3 debug/check_mysql_hosts.py --export --database chul_09_db --export-on-host <호스트>

# 15 리포트 + 차트 + 와이어프레임 갭
python3 debug/generate_db_porting_report.py
pip install -r debug/requirements-charts.txt
python3 debug/generate_phase1_charts.py
python3 debug/report_wireframe_coverage_gap.py
```

## PDF로 배포할 때 (선택)

이 폴더의 Markdown은 차트를 **`./figures/...svg`** 상대 경로로 참조합니다. [Pandoc](https://pandoc.org/) 예시:

```bash
cd docs/phase1-structure
pandoc 00-phase1-summary-for-stakeholders.md -o /tmp/phase1-stakeholders.pdf --resource-path=.:figures
```

## 원격 MySQL 요약

`pip install -r debug/requirements-db.txt`. `python3 debug/check_mysql_hosts.py --tcp-probe --hosts 'h1,h2'` 는 3306 포트만 검사합니다. `MYSQL_USER`, `MYSQL_PASSWORD` 또는 `--password-file`, `MYSQL_HOST` 또는 `MYSQL_HOSTS`, 선택 `MYSQL_PORT`, `MYSQL_DATABASE`, 선택 `MYSQL_CHARSET`(스크립트 기본 **`utf8`**)을 설정한 뒤 `check_mysql_hosts.py` 실행; `--export --database <이름>`으로 `14-mysql-*` 생성 시 **`14-db-code-vs-live.md`** 가 기본 갱신됩니다(`--no-crossref`로 생략). 이후 `generate_db_porting_report.py` → 차트·와이어프레임 갭 스크립트를 권장합니다.

라이브 연동·방화벽 메모: [13-db-surface.md](13-db-surface.md)의 *Live schema sync* 절.

## 빌드 산출물

**이 폴더에는 실행 파일(EXE)이 없습니다.** 실제 빌드 결과물은 `Chulpan.dpr` 등으로 별도 컴파일합니다.


## Phase 1 POC checklist (UTF-8)

- [00-phase1-poc-stage1-checklist.md](00-phase1-poc-stage1-checklist.md) - stage-1 read-only POC, remote_153/154 smoke (S6), phase-2 entry gate.
- Automated (no DB): `python3 -m pytest test/test_phase1_api_contract.py test/test_sobo_phase1_sql.py -q`
