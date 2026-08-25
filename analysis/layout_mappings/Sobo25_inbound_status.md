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

> **DEC-174 (2026-08-22)** — 고정 조건에 **`Gubun` 은 없다**. Gubun 은 검색 콤보(Edit103)라
> 무입력 시 입고·반품이 함께 나온다. `Yesno` 도 무필터 — 2는 접수완료 잠금이지 취소가 아니다.
>
> **DEC-194 (2026-08-24)** — 화면·API 가 출고현황과 같은 공용 축으로 이관되며 이 조건들은
> 축 상수로 옮겨갔다: `_GUBUN_IN_VENDOR = "Gubun IN ('입고','반품')"` +
> `_INBOUND_STATUS_FIXED = "Scode = 'Y' AND Gcode <> ''"`. `list_receipts(require_vendor=)`
> 는 호출자가 사라져 제거됐다(입고접수/입고명세서는 `Gubun='입고'` 기본 그대로).

### 2.1 2026-06 공통 검색창 보강

- LIST/상세 필터의 `hcode`(`Sobo25.Edit106`)는 `lookupKind="publisher"`로,
  `gcode`(`Sobo25.Edit105`)는 `lookupKind="inboundVendor"`로 보강했다.
- 검색 입력은 기존 `data-legacy-id` 를 유지하며 보조 버튼(`Sobo25.LookupHcode/Gcode`)만 추가했다.

## 3. 모던 라우트·facade (구현 — DEC-194, 2026-08-24 재작성)

**출고현황(Subu24)과 같은 컴포넌트·같은 facade** 를 «입고처 축»으로 탄다
(사용자 요청 "입고현황 레이아웃·기능을 출고현황과 동일하게"). 화면은 얇은 래퍼이고,
축이 다른 부분은 아래 3개뿐이다 — 나머지는 출고/반품/폐기와 완전히 공유한다.

| 축 파라미터 | 값 | 이유 |
| --- | --- | --- |
| `slip_gubun`/`rollup_gubun` | `Gubun IN ('입고','반품')` | 레거시 고정 조건에 Gubun 이 없다(§2). 하드필터하면 「입고처 반품」이 웹 어디서도 안 보인다(반품현황은 `Scode='X'` 축) |
| `scode_clause` | `Scode = 'Y' AND Gcode <> ''` | 레거시 고정 조건 그대로 |
| `name_source` / `primary_gubun` | `vendor` / `입고` | 표시명은 **G2_Ggwo**(§4), 하단 집계 `out_*` 버킷이 입고 |

| 뷰 | route | 백엔드 서비스 |
| --- | --- | --- |
| 상세(기본) | `/transactions/inbound-status?view=detail` | `list_outbound_status_slips` + 행 선택 시 `outboundApi.detail` 지연 조회 |
| 요약 | `?view=summary` | `list_outbound_status_slips` (동일 형태) |
| 목록 | `?view=list` | `list_outbound_status_lines` + `outbound_status_customer_rollup` |

화면: `app/(app)/transactions/inbound-status/page.tsx` (17줄 래퍼) →
`components/transactions/transaction-status-screen.tsx` `INBOUND_STATUS_AXIS`.
표시 라벨도 축 파생 — 「입고처」(레거시 `Panel104.Caption='입고처명'`) ·
거래구분 「입고·반품」 · 집계 「입고수량/입고금액/순입고수량」.

레거시에는 있으나 종전 구현에 없던 **본사/창고(`Ocode`, Edit107) · 전표(`Jubun`, Edit104) ·
도서코드(`Bcode`, Edit108)** 필터가 이관과 함께 생겼다.

registry: `Sobo25_status_list` / `Sobo25_status_detail` / `Sobo25_status_summary` (3 id → 1 페이지).

## 4. 이벤트·비즈니스 규칙

| 트리거 | 레거시 | 모던 |
| --- | --- | --- |
| `Button101Click` | `SELECT * FROM S1_Ssub WHERE ...`(L380) | `_status_axis_facade` 3뷰 (DEC-194) |
| 본사/창고 토글 | `Edit107` → `Ocode A/B` | `storeKind` A/B/ALL — 기본 ALL(본사·창고 합산) |
| 입고처명 lookup | `G2_Ggwo.Locate('Hcode;Gcode')` → 실패 시 `Hcode=''` 폴백 (L455~L475) | `_party_name_resolver(name_source='vendor')` → `_fetch_vendor_names` — **G2_Ggwo** `Hcode IN (<scope>,'')` 청크 lookup, 정확 일치 우선 (DEC-174/194). 거래처 G1_Ggeo 를 쓰면 교문사 실측 기준 조회 코드 10개가 10개 모두 다른 이름으로 뒤바뀐다 |

## 5. Out-of-scope (§6)

- `Button201`(신규 입력)·전표 편집·인쇄(`CornerButton1~3,9`) — 입고현황은 조회 화면(`crudParity: R`). 입력은 입고접수(Sobo22 `/inbound/receipts`).
- ~~본사/창고 토글의 본사(A) 데이터~~ — DEC-194 로 `storeKind` A/B/ALL 지원(해소).
- 컬럼 설정(grid-prefs) 키는 4개 현황이 `transactions.outbound-status.*` 를 공유한다(DEC-194 미해결).
