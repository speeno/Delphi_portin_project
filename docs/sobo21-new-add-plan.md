# 거래명세서(Sobo21) 신규추가 — 적용계획

> 입력 근거: 레거시 시연 영상 `거래명세서 신규추가 및 검색.mp4` (132초) 프레임 분석 + `analysis/layout_mappings/Sobo21.md` + 현 백엔드(`transactions`/`outbound` 라우터).
> 작성일: 2026-06-14. 상태: **계획(미착수)**.

## 0. 배경 — 무엇이 빠졌나

레거시 `거래명세서-(본사)`(Sobo21)는 **한 화면에서 생성·조회·검색**을 모두 한다. 영상 확인 사실:

- 거래일자 → 거래구분(출고/반품/파지) → 거래처코드 입력 시 거래처명 자동 채움 → 지점명(Gjisa) 드롭다운.
- **그리드 in-grid 키 입력**: 도서코드만 치면 도서명·단가·비율 자동 조회, 수량 입력 → **금액 = 수량 × 단가 × 비율% 자동계산**(영상: 1 × 30,000 × 85% = 25,500), 줄 자동 추가.
- 저장 시 **전표번호 자동 채번**(영상: 00001 → 00003).
- 검색 버튼 → `거래현황(상세)` 다이얼로그(거래일자 범위·거래구분·전표번호·거래처명·도서구분·도서코드 필터 + 전표목록/라인상세 듀얼 그리드).

현 모던 포팅은 Sobo21을 **읽기 전용**(목록·상세·메모 PATCH)으로만 구현했고, 신규추가는 `Sobo21.md`에서 `Button201 = out-of-scope ("거래명세서 신규는 C2 outbound 와 분리")`로 의도적 제외돼 있다. 생성 능력은 `POST /outbound/orders`(C2, `/outbound/orders`)에 존재하나 (a) **다른 화면**이고 (b) `gubun='출고' 고정`, **라인에 단가/비율/비고/배송·자동계산 없음**(클라이언트가 `gssum` 선계산).

## 1. 확정 결정 (사용자)

| # | 결정 | 내용 |
|---|------|------|
| D1 | **생성 동선** | 거래명세서 화면 내 신규(레거시 충실). Sobo21 페이지에 신규 모드 추가, in-grid 라인 입력 + 검색 한 화면. |
| D2 | **1차 거래구분 범위** | **출고만**(Gubun 11/12). 반품(21/22)·파지는 후속. |
| D3 | **라인 충실도** | **풀 패리티** — 도서코드→단가·비율 자동조회, 수량→금액 자동계산, 비고·배송 포함. |

→ 위 결정은 기존 "거래명세서 신규 = outbound 와 분리" 결정을 **부분 번복**한다. **신규 DEC-065** 로 기록.

## 2. 접근 개요

핵심 원칙: **백엔드 생성은 기존 `outbound_service.create_order`(S1_Ssub INSERT, 트랜잭션, 전표 자동채번, audit)를 1차 자산으로 재사용**하고, **거래명세서 라인 패리티(단가/비율/비고/배송)만큼 모델·서비스를 확장**한다. 프론트는 Sobo21 페이지에 **신규 모드**를 더해 in-grid 입력 + 검색을 한 화면에 둔다. 레거시와 동일 테이블(S1_Ssub)을 쓰므로 새 SQL 표면은 최소화(DEC-040 정합).

```
[Sobo21 page]  ──(조회모드)─→ 기존 GET list/detail (변경 없음)
                └(신규모드)─→ in-grid 라인 입력 ─→ POST /transactions/sales-statement
                                                     └ 내부적으로 outbound create_order(확장) 재사용
                └(검색)──────→ 거래현황(상세) 다이얼로그 = 기존 GET list 필터 재사용
보조: GET …/line-defaults?bcode= → 도서코드별 단가·비율·도서명 (자동조회)
```

## 3. 백엔드 작업

### 3.1 라인 모델 확장 (표준)
`backend/app/models/outbound.py` `OrderLineInput` 에 거래명세서 라인 컬럼 추가:
- `gdang: int`(단가, S1_Ssub.Gdang), `grat1: float`(비율, S1_Ssub.Grat1), `gbigo: str`(비고, S1_Ssub.Gbigo), `yesno`(배송/상태) — **기존 outbound 호출부 깨지지 않게 전부 기본값 부여**(BC 유지).
- 서버측 금액 검증: `gssum == round(gsqut * gdang * grat1/100)` 불일치 시 422(레거시 자동계산 신뢰선 일치).

### 3.2 create_order INSERT 컬럼 확장 (표준)
`outbound_service.py` `_SQL_INSERT_LINE` 에 Gdang/Grat1/Gbigo 컬럼 반영. **`s1_ssub_adapt.py`** 의 `SHOW COLUMNS` 어댑터를 통해 서버별 컬럼 존재 분기(154/155 MySQL3 vs 138 슬림) — 서비스 레이어 if 금지(DEC-033). 누락 컬럼은 INSERT 목록에서 제외하고 `customer_variants` 에 기록.

### 3.3 신규 엔드포인트 (표준)
거래명세서 의미로 노출(내부는 outbound 재사용, 라우터 thin):
- `POST /api/v1/transactions/sales-statement` — header(gdate/hcode/gjisa, gubun='출고' 고정) + lines[] → create_order 위임. 201 + 채번된 order_key.
- `GET /api/v1/transactions/sales-statement/line-defaults?serverId=&customer=&bcode=&pubun=` — 도서코드별 단가·비율 자동조회. 레거시 `Subu21.pas Button201Click` 규격(아래 §3.3.1) 그대로 서버에서 해석. **`in_clause_lookup` 청크 규칙 준수**(DEC-033), 단건이라도 헬퍼 경유.

### 3.3.1 라인 자동조회·계산 규격 (레거시 Tong02.pas / Subu21.pas 확정)

> 출처: `WeLove_FTP/도서유통-출판/{Subu21,Tong02}.pas`. `Hnnnn` = 본사/지점(지점명) 코드, `Edit104` = 거래처코드, `Bcode` = 도서코드.

**(a) 단가·비율 3단 override — 뒤가 앞을 덮어씀(last-wins):**
1. **거래처 비율** `Select Grat1..Grat7 From G1_Ggeo Where Gcode=거래처 and Hcode=Hnnnn` → NODATA 시 `Hcode=''`(전사 공통) 재시도. → PrinZing 으로 Pubun 별 1개 선택(§b). `Grat1≠0` 일 때만 적용.
2. **도서마스터** `Select Grat1..Grat7,Gname,Gjeja,Gdang,Scode From G4_Book Where Gcode=Bcode and Hcode=Hnnnn` → 도서명·저자·**단가(Gdang)**·재고(Jeago) 채움, `Grat1≠0` 이면 비율 덮어씀.
3. **거래처×도서 특가** `Select Grat1,Gssum From G6_Ggeo Where Gcode=거래처 and Bcode=도서 and Hcode=Hnnnn` → 존재 시 **비율·단가 모두 최우선 덮어씀.**
4. **직전 거래가 재사용** `PrinRat1` — **1차 포함(확정)**. 회사/지점 설정으로 게이트되는 정책:
   - 조회: `Select Gdang,Grat1 From S1_Ssub Where Gcode=거래처 and Bcode=도서 and Pubun=품목구분 and Hcode=Hnnnn Order By id DESC Limit 0,1` — 동일 (거래처+도서+품목구분+본사) 마지막 거래.
   - **설정 키 = `G7_Ggeo`(본사/지점 행, Gcode=Hnnnn)**: `xChek=Chek3`, `mChek=Chek2`.
     - `Chek3='grat1'` → 직전 거래의 **단가+비율 모두** 재사용.
     - `Chek3='grat2'` → 직전 거래의 **비율만** 재사용(단가 유지).
     - 그 외(빈 값/기타) → **비활성**(대부분 회사 기본).
     - 특정 고객 DB(`chul_01/03/05/06/07_db`, `book_01..06_db`, `book_kb_db`) + `Chek2≠'True'` → 조회 키에 **지사(Gjisa)** 추가.
   - **적용 위치/우선순위**: 레거시에선 **in-grid 타이핑**(Bcode·Pubun OnChange, `Subu21.pas` L1206~1516)에서만 호출되고 팝업선택(`Button201Click`)엔 없음. 활성 시 직전거래가가 §1~3 위에 얹혀 단가/비율을 덮음 — 단 §3(G6 특가) 와의 정확한 선후는 P1 구현 시 OnChange 호출 순서로 확정(verify-at-impl).
   - **모던 반영**: `line-defaults` 응답에 직전거래가를 별 필드로 싣고, 활성 여부는 회사 설정(아래)으로 결정. 설정은 `customer_variants` + 백엔드 회사 컨텍스트(G7_Ggeo Chek2/Chek3 로드)로 표현, **코드 분기 금지**(DEC-033/DEC-028).

**(b) 비율은 품목구분(Pubun)으로 7종 중 선택 (PrinZing):**

| Pubun | 적용 비율 컬럼 |
|-------|---------------|
| 위탁 / 질 / 신간, (Gubun)반품 | Grat1 |
| 현매 | Grat2 |
| 매절 | Grat3 |
| 납품 | Grat4 |
| 특별 | Grat5 |
| 기타 | Grat6 |
| 한도 | Grat7 |
| 증정 | 0 |

→ 신규 라인 기본 Pubun = **위탁**(영상 확인). `OrderLineInput.pubun` 이미 존재 — 재사용.

**(c) 금액 공식 (PrinYing):**
```
Grat1 = 0      → Gssum = 0
Grat1 ≠ 0      → Gssum = round(Gdang × Gsqut × Grat1 / 100)
Gubun ∈ {반품, 폐기} → Gsqut 음수화 후 계산 (Gssum 음수)
Pubun = 증정   → Gssum = 0 (단 Grat1≠0 이면 정상식)
```
영상 검증: 위탁 1 × 30,000 × 85 / 100 = 25,500 ✓. 서버에서 동일 계산·검증(클라이언트 값 불일치 422).

### 3.3.2 회사 설정(G7_Ggeo) 로드 — 직전거래가 정책 (표준)
백엔드에 회사/지점(Hnnnn) 단위 설정 컨텍스트 추가: `Select Chek2,Chek3 From G7_Ggeo Where Gcode=Hnnnn` → `price_reuse_mode ∈ {off,'grat1','grat2'}`, `jisa_keyed: bool`. `line-defaults` 가 이 설정을 읽어 직전거래가 적용. 설정 로드는 세션/회사 컨텍스트 캐시(매 라인 조회마다 G7 재조회 금지). 서버별 G7_Ggeo 컬럼 부재 시 off 로 폴백.

### 3.4 멀티테넌트·격리 가드 (표준, 보안 필수)
- **주의**: S1_Ssub.Hcode 는 *거래처 코드*(레거시 컬럼 의미)이며 **테넌트 격리 hcode 와 다름**. 격리는 서버/DB 선택(servers.yaml)으로 이뤄짐 — 두 개념 혼동 금지. `tools/audit_domain_api_hcode_filter.py --strict` 가 신규 INSERT 를 critical 로 잡으면 의도 `noqa` 사유 표기.
- 쓰기 경로이므로 `audit.outbound 'created'`(또는 'sales_statement_created') 로그 유지.

## 4. 프론트 작업

### 4.1 Sobo21 신규 모드 (표준 + 일부 고급)
`frontend/src/app/(app)/transactions/sales-statement/page.tsx` 에 모드 토글(조회/신규):
- 헤더 폼: 거래일자·거래구분(출고 고정 표기)·거래처 `MasterLookupField`·지점명(`customerBranchList` 동적 로드, 기존 status 페이지 패턴 재사용).
- **편집 그리드**(신규): 도서코드 입력 → `line-defaults` 호출로 도서명·단가·비율 채움 → 수량 입력 시 금액 자동계산 → Enter 시 다음 줄 자동 추가(레거시 in-grid 흐름). 키보드 TabOrder 보존.
- 저장 → `POST …/sales-statement` → 성공 시 채번 전표 표시 후 조회 모드 전환.
- **모든 위젯에 `data-legacy-id`**(Edit101/102/104/105/106/109, DBGrid101.{BCODE,BNAME,GSQUT,GDANG,GRAT1,GSSUM,GBIGO,YESNO}, Button201, dxButton1) 부착 — `Sobo21.md` 매핑 노트 기준.

### 4.2 검색 다이얼로그 (표준)
`거래현황(상세)` 는 신규 SQL 없이 **기존 list GET 의 필터 확장**으로 흡수(거래일자 범위·거래구분·전표번호·거래처명·도서코드). 이미 `status` 뷰가 유사 — 컴포넌트 재사용 우선.

## 5. 계약·문서·DEC

- `migration/contracts/sales_inquiry.yaml`: `POST /sales-statement`, `GET …/line-defaults` 추가. 라인 컬럼·자동계산식·BC 명시. `customer_variants` 에 서버별 Gdang/Grat1/Gbigo 컬럼 차이 기록.
- `analysis/layout_mappings/Sobo21.md`: `Button201 신규등록 out-of-scope → in-scope` 로 갱신, §6/§7 deltas 정리, `data-legacy-id` 신규 목록 추가.
- `legacy-analysis/decisions.md`: **DEC-065**(거래명세서 화면 내 신규추가 — outbound create_order 재사용 + 라인 패리티 확장; 기존 분리 결정 부분 번복).
- `docs/core-scenarios-porting-plan.md` / `dashboard/data/porting-screens.json`: C6/C2 관련 항목 상태 갱신.

## 6. 테스트·회귀 가드

| 테스트 | 목적 |
|--------|------|
| `test/test_sales_statement_create_contract.py` (신규) | POST 계약·201·채번·필수값 422 |
| `test/test_sales_statement_line_autocalc.py` (신규) | 금액 = 수량×단가×비율% 서버검증, 불일치 422 |
| `test/test_sales_statement_line_defaults.py` (신규) | line-defaults 3단 override(G1→G4→G6) + Pubun 별 비율 선택, in_clause_lookup 청크 |
| `test/test_sales_statement_price_reuse.py` (신규) | 직전거래가(PrinRat1): Chek3='grat1' 단가+비율 재사용 / 'grat2' 비율만 / off 미적용 / 지사키 변형 |
| `test/test_outbound_*` (기존) | create_order BC 회귀 — 라인모델 확장이 기존 출고 깨지지 않음 |
| `test/test_list_count_grouped_mysql3.py` 외 (기존) | mysql3 파생테이블·IN 규칙 유지 |
| `test/test_layout_mappings_sobo21.py` (기존, 갱신) | data-legacy-id 누락 0건 |
| `debug/probe_backend_all_servers.py` | 신규 GET(line-defaults) 4서버 매트릭스 등록 |

DoD(단계별): 4서버 L2 SELECT 1 + L4 신규 GET 성공 / `audit_domain_api_hcode_filter --strict` 통과 / data-legacy-id 일치 / 기존 outbound 회귀 0.

## 7. 단계별 적용(Phase) — 권장 순서

1. **P0 계약·DEC·매핑**: sales_inquiry.yaml 확장, DEC-065, Sobo21.md 갱신. (코드 0)
2. **P1 백엔드 모델/서비스**: OrderLineInput 확장 + create INSERT 컬럼 + s1_ssub_adapt 분기 + 기존 outbound 회귀 그린.
3. **P2 백엔드 엔드포인트**: POST /sales-statement, GET /line-defaults + 계약/자동계산 테스트.
4. **P3 프론트 신규 모드**: 헤더 폼 + in-grid 편집 그리드 + 자동조회/자동계산 + data-legacy-id.
5. **P4 검색 다이얼로그**: 기존 list 필터 확장 재사용.
6. **P5 4서버 스모크 + 회귀 종합 + 대시보드 상태 갱신.**

## 8. 모델 티어 (planning-model-tiers.mdc)

| 서브태스크 | 권장 티어 | 메모 |
|------------|-----------|------|
| 계약/DEC/매핑 노트, 모델·INSERT 확장, 엔드포인트, 회귀 테스트 | **표준** | 규칙 명확 |
| in-grid 키보드 흐름·자동계산 UX 재현(레거시 시연과 1:1) | 표준~고급 권장 | 다단 상호작용 정합 — 실행 전 모델 수동 선택 가능 |
| 서버별 S1_Ssub DDL 차이 해석(154/155 vs 138) | 고급 권장 | 불완전 스키마 추정 |

## 9. 위험·미해결

- **R1 단가/비율 출처 — ✅ 해결**(레거시 `Subu21.pas`/`Tong02.pas`/`Base01.pas` 분석). §3.3.1 에 3단 override(G1_Ggeo→G4_Book→G6_Ggeo) + Pubun 별 비율 선택 + 금액식 + **직전거래가 재사용(PrinRat1, 1차 포함, G7_Ggeo Chek2/Chek3 게이트)** 확정. 잔여: PrinRat1 과 G6 특가의 선후만 P1 구현 시 OnChange 호출 순서로 확정.
- **R1b hcode 의미 충돌 — 신규**: 마스터 조회는 `Hcode=Hnnnn`(본사/지점 코드)로 키잉되는데, 모던 `OrderHeaderInput.hcode` 는 *거래처코드*(S1_Ssub.Hcode)로 정의돼 있다. **Hnnnn(회사/지점) vs 거래처코드 두 개념을 분리**해 전달해야 자동조회가 맞는다 — line-defaults 는 `Hnnnn`(세션/지점 컨텍스트)과 `거래처코드`를 별 파라미터로 받는다. 계약·모델에 명시.
- **R2 전표 채번 규칙**: outbound 채번이 거래명세서 출고 채번과 동일 키(Gdate+Hcode+Jubun)인지 — `analysis/c2_outbound_flow.md` 대조.
- **R3 반품/파지(D2 후속)**: returns(Sobo23) 플로우와 채번·부호(반품 수량 음수화, §3.3.1c) 규칙 정합 — 본 1차 범위 밖, DEC 에 후속 명시.
- **R4 레거시 버그 `T2_Sub41: Field 'Jeago' not found`**: 영상에 노출. Jeago(재고)는 G4_Book 조회 시 `PrinJing` 으로 채우는 계산 필드 — 재고 컬럼/소스 부재 환경에서 터지는 버그. 모던은 재고 미확보 시 graceful(null) 처리, 재현 금지.
- **R5 고객사 변형**: `GSQUTChange` 에 `book_kb_db`(교보 전용 DB)·`거래명세서-(창고)` 캡션 분기(재고 부족 시 수량 0 강제)가 있음. 변형 차이는 코드 분기 금지 → `migration/contracts/sales_inquiry.yaml customer_variants` 에 기록(DEC-028). 변형 폴더: `도서유통-{출판,총판,New}`, `MySQL/.../chul_0X(*)`.
