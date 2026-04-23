# 출판 스키마 사전 ↔ 정적 분석 교차 검증

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-23 |
| 좌측 입력 (사전) | [`analysis/welove_schema_dictionary.json`](../analysis/welove_schema_dictionary.json) — 33 테이블 / 62 카탈로그 행 (`SCH-WELOVE-출판-*`) |
| 우측 입력 (정적 분석) | [`analysis/db_impact_matrix.json`](../analysis/db_impact_matrix.json) — 53 테이블 / [`analysis/query_catalog.json`](../analysis/query_catalog.json) — 1325 SQL 라인 |
| 추적 ID | 불일치 1건 = 1 OQ 또는 1 DEC 후보 (`SCH-RECON-NN`) |
| 단일 원천 | 본 문서. 후속 변경은 양 입력 갱신 + 본 문서 §4 표만 갱신. |

레거시에서 모호했던 데이터 의미가 본 사전으로 **명확화** 되었으므로, [`migration/contracts/login.yaml`](../migration/contracts/login.yaml) 등 일부 계약은 **표기 정정 후보**가 된다(§4).

---

## 1. 한 줄 요약

- 사전(33) ⊆ DB 영향(53). 사전에 없는 코드 사용 테이블 23 개 발견 → §3.1 표.
- 사전에 있으나 정적 분석에서 미사용 3 개 → §3.2 표 (deprecated 후보).
- **`Id_Logn` 의 `gcode` / `gname` 의미가 사전과 현 계약에서 충돌** — 사용자/아이디 의미가 뒤바뀌어 있음. §4.1 의 `SCH-RECON-01`.
- `S1_Chek` vs `S1_CheK` 대소문자 차이(MySQL 케이스 민감도 의존) — §4.2 `SCH-RECON-02`.

---

## 2. 정합 통계

| 분류 | 건수 | 비고 |
|------|------|------|
| 사전 ∩ DIM (정합) | 30 | 본문 합류 가능 |
| 사전 only (DIM 미사용) | 3 | `G8_Gbun`, `Ie_Logn`, `S1_CheK` (대소문자 후보) |
| DIM only (사전 미수록) | 23 | §3.1 |
| 카탈로그(인덱스 시트) only — 상세 시트 부재 | 29 | §3.3 — 운영 신규/2차·3차 테이블 후보 |

---

## 3. 분류별 상세

### 3.1 정적 분석에서만 등장 (사전 미수록)

이들 테이블은 델파이 코드에서 SELECT/INSERT 등으로 명시 사용되지만 사전 시트가 없다. 신규 화면 추가 시 사전 누락은 **CRUD 동등성 가드(`crud-backlog.md`) 의 회귀 위험**.

`G7_Gbun`, `G7_Ssub`, `Gg_Magn`, `Gg_Megn`, `Gs_Csum`, `Gs_Gsum`, `In_Csum`, `In_Gsum`, `Me_Sage`, `S1_Chek`, `Sb_Csum`, `Sg_Csum`, `Sg_Gsum`, `Sm_Ggeo`, `Sv_Chng`, `Sv_Csum`, `Sv_Ghng`, `Sv_Gsum`, `T0_Gbun`, `T2_Ssub`, `T7_Ssub`, `T8_Gbun`, `T8_Ssub`.

→ 처리: §4.2 `SCH-RECON-02` (대소문자) + §4.3 `SCH-RECON-03` (사전 누락) OQ 등록.

### 3.2 사전에만 등장 (코드 미사용)

`G8_Gbun`, `Ie_Logn`, `S1_CheK` — 사전상 정의는 있으나 정적 분석에 등장하지 않음. 향후 메모리얼 deprecation 또는 `S1_CheK ≡ S1_Chek` 케이스 차이 가능.

### 3.3 카탈로그(인덱스 시트) only — 상세 시트 부재

운영 변경분 또는 메모성 테이블이 인덱스에는 적혔지만 상세 시트가 없다. 다음 사이클에서 필드 정의가 필요한 항목:

| 표 카탈로그 항목 | 추정 |
|---|---|
| `Id_Memo`, `Ie_Memo` | 로그인 IP 기록(테이블 분리). 카탈로그에서는 캡션 명시. |
| `J1_Ggeo`, `J1_Ssub` | 사원관리. |
| `P1_Ggeo`, `P1_Ssub`, `P2_Ssub` | 운영(프린트?) — 캡션 미기재. |
| `Sg_Gsum`, `Sg_Csum` | 장부대조·재고대조. |
| `Sv_*` | 마감 (거래처/재고). |
| `Sx_*` | (시스템) 호스트·메모·체크. |
| `Me_Sage` | 메시지. |
| `T2_Ssub`, `T7_Ssub` | 청구서·반품비. |
| `Gg_Post`, `Gg_Prnt` | 우편번호·프린터(?). |
| `In_Gsum`, `In_Csum` | 초기미수·초기재고. |

→ 처리: 본 사이클은 카탈로그 행만 `welove_schema_dictionary.json:catalog[]` 에 보존. 다음 사이클 SME 회의에서 **사전 보강 PR** 으로 분리.

---

## 4. 의미 충돌 / DEC·OQ 후보

### 4.1 `SCH-RECON-01` — `Id_Logn` 의 `gcode` / `gname` 의미가 현행 계약과 반대

| 출처 | `gcode` 의미 | `gname` 의미 |
|---|---|---|
| **사전 (`Id_Logn` 시트)** | **사용자(작업자명)** | **아이디(로그인 키)** |
| `migration/contracts/login.yaml` v1.1.1 | 로그인 코드/사번 | 작업자 이름(한글 가능) |
| `legacy_delphi_source/legacy_source/Chul.pas:441` | `Where Gcode = '<Logn2>' and Gname = '<Logn1>'` (Logn2=ID, Logn1=Name) — 변수 명령에서 모호 |

- **영향**: `auth_service.authenticate_user` 가 `userId` 파라미터를 `Gcode` 로 매핑하는데, 사전 정의에 따르면 `userId(=ID)` 는 `Gname` 으로 가야 함. **현 운영이 동작하므로 실제 운영 DB 의 컬럼 사용은 사전 정의를 따르지 않을 가능성** 또는 **사전이 잘못 표기되어 있을 가능성** 둘 중 하나로 갈린다.
- **상태**: **OQ-LOGIN-2 후보** (신규). `BLS_AUTH_SERVER_ID=remote_138` `Id_Logn` 1행을 SME 와 함께 직접 조회해 SSOT 결정 후 DEC 동결.
- **임시 정책**: 본 사이클에서 코드 변경 0. login.yaml `inputs.gcode/gname` 본문에 본 SCH-RECON-01 링크만 추가하는 후속 PR.

### 4.2 `SCH-RECON-02` — `S1_Chek` vs `S1_CheK` 대소문자

- 사전: `S1_CheK` (대문자 K). 정적 분석: `S1_Chek` (소문자 k).
- MySQL 의 테이블명 케이스 민감도(`lower_case_table_names`)는 OS 따라 달라짐. 운영 4 서버 모두 Linux → 기본 1(소문자 보장) 또는 0(보존).
- **상태**: 정적 분석 출처(`legacy_source/*.pas`) 가 코드 정본으로 우세 → 사전을 정정해야 한다. 사전은 정본이지만 본 행만 **수동 정정** 가능.
- **처리**: 본 사이클에서 사전(`welove_schema_dictionary.json`) 은 변경하지 않고 OQ-DBL-NEW-1 등록. 운영 DB 에서 `SHOW TABLES LIKE 'S1_Che%'` 확인 후 정정.

### 4.3 `SCH-RECON-03` — 코드 사용 23 테이블의 사전 누락

- §3.1 의 23 테이블은 `analysis/db_impact_matrix.json::table_details[*]` 의 `accessed_by_units/forms` 가 비어있지 않으므로 운영에서 실제 사용 중.
- **영향**: 신규 화면 포팅 또는 컬럼 변경(예: `T2_Ssub` 청구서) 시 사전 부재로 SME 협의가 길어짐 — DEC-060 (DFM Caption 대조 게이트) 의 데이터 측 등가물.
- **처리**: 다음 사이클 SME 회의 의제 — 23 테이블 중 *현 사이클 우선 5*(`T2_Ssub`, `T7_Ssub`, `Sg_Gsum`, `Sg_Csum`, `Me_Sage`) 만 사전 보강 PR 후보.

### 4.4 `SCH-RECON-04` — `Size(전)` → `Size(후)` ALTER 흔적의 컬럼 어댑터 단서

| 테이블 | 컬럼 | 전 | 후 | 운영 의미 |
|---|---|---|---|---|
| `Id_Logn` | `gcode` | 50 | 50 | 변경 없음 |
| `Id_Logn` | `gname` | 50 | 50 | 변경 없음 |
| `G1_Ggeo` | `gname` | 24 | 50 | 거래처명 길이 확장 |
| `G1_Ggeo` | `gposa` | 20 | 30 | 대표자명 |
| `G1_Ggeo` | `guper` | 20 | 30 | 업태 |
| `G1_Ggeo` | `gjomo` | 20 | 30 | 종목 |
| `G1_Ggeo` | `name1` | 30 | 50 | 핸드폰번호 (실제는 자유 문자열) |
| `G7_Ggeo` | `gname` | 24 | 50 | 출판사명 길이 확장 |

→ 운영 DB 4대 서버에서 동시에 ALTER 가 적용되었는지 [`tools/db/schema_diff.py`](../tools/db/schema_diff.py) 로 정기 점검 의무화. **DEC-033(멀티 DB 호환) 의 컬럼 어댑터 패턴**(예: `t5_ssub_adapt.py`)에 행 추가 후보로 등록.

---

## 5. 산출물 합류

| 산출물 | 합류 방식 |
|---|---|
| `migration/contracts/master_data.yaml` | 마스터 카탈로그 행에 `SCH-WELOVE-출판-<TABLE>` 링크 1줄 (다음 사이클 PR) |
| `migration/contracts/login.yaml` | §4.1 `SCH-RECON-01` OQ 링크 (`inputs.gcode/gname.note`) |
| `docs/db-schema-porting-readiness.md` | §3 컬럼 어댑터 후보로 §4.4 인용 |
| `docs/crud-backlog.md` | §3.1 의 23 테이블 미사전 표 + §4.3 우선 5 항목 backlog 추가 |
| `legacy-analysis/open-questions.md` | OQ-LOGIN-2 / OQ-DBL-NEW-1 / OQ-SCH-NEW-1 (각 §4 항목 1:1) |

---

## 6. 재현

```bash
python3 tools/extract_welove_schema.py            # 사전 갱신
python3 -c "import json; \
  sd=json.load(open('analysis/welove_schema_dictionary.json')); \
  dim=json.load(open('analysis/db_impact_matrix.json')); \
  print(sorted({t['table'] for t in sd['tables']} ^ set(dim['table_details'])))"
```

대조 결과는 본 문서 §3 의 합집합과 일치해야 한다.
