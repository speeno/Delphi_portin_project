# 레이아웃 매핑: Sobo25 (입고현황) — 거래관리 Menu205

DEC-028 의무 — dfm→html 산출물의 (영역, 위젯 ID, TabOrder, DBGrid 컬럼, 이벤트) 1:1 매핑. 픽셀/폰트/색상 제외.

## 0. 입력 산출물 (Publisher 정본)

- 본 폼: [`tools/delphi_porting_accelerator/examples/generated/publisher_source_root/Subu25/Sobo25.html`](../../tools/delphi_porting_accelerator/examples/generated/publisher_source_root/Subu25/Sobo25.html) + `Sobo25.form.json` + `Sobo25.tree.json`
- 원 dfm: [`WeLove_FTP/도서유통-출판/Subu25.dfm`](../../WeLove_FTP/도서유통-출판/Subu25.dfm) (caption `입고현황`)
- PAS: [`WeLove_FTP/도서유통-출판/Subu25.pas`](../../WeLove_FTP/도서유통-출판/Subu25.pas) (Button101Click 메인 조회 L361~L381)

> **P0 정정(2026-05-31)**: 직전 P0 문서는 가속기 입력이 물류(`legacy_source_root`) 트리뿐이라 Subu25 추출본이
> 「반품재고(반품입고)-해체」로 잡혀 “Publisher DFM 없음(블록)”으로 결론냈다. 실제 Publisher 정본
> `WeLove_FTP/도서유통-출판/Subu25.dfm` 는 `입고현황` 이며, `publisher_source_root` 로 재추출해 본 매핑을 확정했다.

## 1. 영역 분할

| 영역 | dfm 컨테이너 | 모던 컴포넌트 | 역할 |
| --- | --- | --- | --- |
| 상단 검색 패널 | `Edit101/102`(기간 마스크)·`Edit103`(전표구분)·`Edit105/106`(입고처)·`Edit108`(도서)·`Edit107`(본사/창고) + `Button101`(조회)·`Button201`(신규) | 검색 폼 + 뷰 탭 | 기간·코드 검색 |
| 중단 그리드 | `DBGrid101` (TDBGridEh) | `DataGrid` | 입고 전표/라인 |
| 진행 바·상태 | `ProgressBar1` | `StatusBar` | 조회 진행 |

## 2. 검색 위젯 매핑 (Subu25.pas Button101Click 기준)

| dfm ID | 클래스 | 역할 | WHERE 절 (S1_Ssub) | 모던 매핑 |
| --- | --- | --- | --- | --- |
| `Edit101` | TFlatMaskEdit | 시작일 | `Gdate >= '<from>'` | `data-legacy-id="Sobo25.Edit101"` 시작일 |
| `Edit102` | TFlatMaskEdit | 종료일 | `Gdate <= '<to>'` | `Sobo25.Edit102` 종료일 |
| `Edit107` | (본사/창고) | 본사=`Ocode='A'`, 창고=`Ocode='B'` | `Ocode = '<A\|B>'` | store_kind 토글 (기본 창고 B — `list_receipts` 현행) |
| `Edit103` | TFlatComboBox | 전표구분(Gubun) | `Gubun = '<v>'` | `Sobo25.Edit103` |
| `Edit104` | TFlatEdit | Jubun LIKE | `Jubun LIKE '%<v>%'` | (옵션) |
| `Edit105` | TFlatEdit | 입고처코드 | `Gcode = '<v>'` | `Sobo25.Edit105` |
| `Edit108` | TFlatEdit | 도서코드 | `Bcode = '<v>'` | `Sobo25.Edit108` |
| `Button101` | TFlatButton | 조회 | — | `Sobo25.Button101` |

고정 조건: `Scode = 'Y'`(입고), `Hcode = '<로그인 hcode>'`, `Gcode <> ''`.  
정렬: `ORDER BY Gdate, Gcode, Gubun, Jubun, Gjisa, ID` · `LIMIT 0,3000`.

### 2.1 2026-06 공통 검색창 보강

- LIST/상세 필터의 `hcode`(`Sobo25.Edit106`)는 `lookupKind="publisher"`로,
  `gcode`(`Sobo25.Edit105`)는 `lookupKind="inboundVendor"`로 보강했다.
- 검색 입력은 기존 `data-legacy-id` 를 유지하며 보조 버튼(`Sobo25.LookupHcode/Gcode`)만 추가했다.

## 3. 모던 라우트·facade (구현)

거래현황(`/transactions/status`) facade 와 동형. 입고는 입고접수(`/inbound/receipts`)·입고명세서(C1)와
동일 `S1_Ssub` 입고 데이터(`Gubun='입고'`, `Scode='Y'`)이므로 **신규 SQL 0** 으로 재사용한다.

| 뷰 | route | 백엔드 | 재사용 |
| --- | --- | --- | --- |
| LIST | `/transactions/inbound-status?view=list` | `GET /api/v1/transactions/inbound-status?view=list` | `inbound_service.list_receipts` |
| 상세 | `?view=detail` | `?view=detail` | 동일 + 행 펼침 시 `/inbound/receipts/{key}` 지연 조회 |
| 요약 | `?view=summary` | `?view=summary` | `inbound_service.period_report` (기간 출판사/거래처 집계) |

registry: `Sobo25_status_list` / `Sobo25_status_detail` / `Sobo25_status_summary` (3 id → 1 페이지).

## 4. 이벤트·비즈니스 규칙

| 트리거 | 레거시 | 모던 |
| --- | --- | --- |
| `Button101Click` | `SELECT * FROM S1_Ssub WHERE ...`(L380) | `view=list/detail` → `list_receipts` |
| 본사/창고 토글 | `Edit107` → `Ocode A/B` | store_kind(기본 B 창고, 현행 회귀 보존) |
| 입고처명 lookup | `G2_Ggwo.Locate` 행별 Gname 보강 | `list_receipts` 의 `_fetch_vendor_names` (in_clause_lookup 청크) |

## 5. Out-of-scope (§6)

- `Button201`(신규 입력)·전표 편집·인쇄(`CornerButton1~3,9`) — 입고현황은 조회 화면(`crudParity: R`). 입력은 입고접수(Sobo22 `/inbound/receipts`).
- 본사/창고 토글의 본사(A) 데이터: 현행 `list_receipts` 는 창고(B) 고정. 본사 노출이 필요하면 Sobo67 `store_kind` 패턴으로 후속 확장(deltas).
