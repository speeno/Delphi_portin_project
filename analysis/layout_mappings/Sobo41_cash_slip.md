# 레이아웃 매핑: Sobo41 (입출금전표-거래처) → `/settlement/cash-status`

DEC-028 의무 — dfm→(영역, 위젯 ID, TabOrder, DBGrid 컬럼, 이벤트) 1:1 매핑. 픽셀/폰트/색상 제외.

> **배경(2026-08-23 운영 리포트)**: "이 화면이 레거시에서 **일자별 입금 금액 기입용**으로
> 쓰였다. 이 기능을 입금현황 화면에 적용하고, 항목을 화면과 맞추고, 입력은 **명세서 라인
> 입력하듯 목록에 항목을 추가하는 방식**으로 하라."
>
> 조사 결과 기존 입금 3화면이 **잘못된 테이블**에 배선돼 있었다 — 아래 §0-b.

## 0. 입력 산출물 (정본)

- dfm/pas: `WeLove_FTP/도서유통-출판/MySQL/도서유통/한국도서유통출판/출판/Subu41.{dfm,pas}`
  (caption `입출금전표-거래처`, 1,457줄)
- 메뉴: `한국도서유통출판/출판/Chul.dfm` `Menu400`(회계관리) → `Menu401` = `입출금전표-거래처`
  → `Menu401Click` 이 `TSobo41` 생성 (라이선스 키 **F41**). 형제 `Menu402` = 입출금전표-**사무실**(Subu42).
- 핸들러: `Button101Click`(조회, L332~435) / `T4_Sub11BeforePost`(쓰기, L1301~1420) /
  `T4_Sub11NewRecord`(신규 기본값, L1427~) / `DBGrid101KeyPress`(인라인 편집, L711~)

> **변형 주의**: `Subu41.dfm` 은 빌드별로 그리드가 크게 다르다. 첨부 스크린샷과 컬럼이
> 일치하는 것은 **출판 빌드 2개**(`도서유통-출판/Subu41.dfm`, `한국도서유통출판/출판/Subu41.dfm`)
> 뿐이다. `도서유통-New`/`유통` 계열은 `입금일자·청구월·출판사코드·출판사명·금액·결재·메모`
> 7컬럼으로 **다른 화면**이며, 종전 포팅(`Sobo41_cash.md`)이 그 변형을 따라간 것이다.

## 0-b. 왜 화면을 교체했나 — 라이브 근거

| 서버 | `T5_Ssub` (종전 배선) | `H1_Ssub` (레거시 실제) |
| --- | --- | --- |
| remote_138 | **0** | 131,254 |
| remote_153 | **0** | 1,145,482 |
| 교문사(5019) | **0** | 1,515 (2026년) |

`cash_service`(입금내역·입금전표)와 `settlement_service.cash_status`(입금현황+변형 2종)가
모두 `T5_Ssub` 를 읽어 **어떤 계정에서도 항상 빈 화면**이었다. 실제 입출금 데이터는 전부
`H1_Ssub` 에 있다. → 입금현황을 본 문서의 입출금전표로 교체하고 나머지는 통합·숨김(DEC-186).

## 1. 화면 구조

| 영역 | dfm | 역할 | 모던 매핑 |
| --- | --- | --- | --- |
| 검색 `Panel001` | Edit101/102(거래일자 from~to)·Edit103(거래구분)·Edit104/106(거래처 코드 범위)·CheckBox2(입력순)·dxButton1(검색) | 조회 조건 | 상단 필터 바 |
| 그리드 `Panel002` | `DBGrid101` 10컬럼 + Footer 합계 | 목록 **겸 입력** | `<table>` + 인라인 신규 행 |
| 상태 `Panel007` | ProgressBar/레코드 패널 | 진행 표시 | `loading` 흡수 |

> 레거시는 **별도 입력 폼이 없다** — `DBGrid101KeyPress`/`ColEnter` 로 그리드 셀을 직접
> 편집하고 `T4_Sub11BeforePost` 가 INSERT/UPDATE 한다. 운영 지시("목록에 항목을 추가하는
> 방식")와 정확히 같아서, 모던도 목록 하단에 «신규 행»을 띄우는 인라인 입력으로 구현했다.

## 2. 그리드 컬럼 (DBGrid101, dfm FieldName 기준)

| 표시 | FieldName | 의미 | 웹 필드 |
| --- | --- | --- | --- |
| 거래일자 | `GDATE` | 거래일 | `gdate` |
| 코드 | `GCODE` | 거래처 코드 | `gcode` |
| 거래처명 | `GNAME` | 거래처명 | `gname` |
| 코드 | `OCODE` | 계정 코드 | `ocode` |
| 계정과목 | `ONAME` | 계정과목명 | `oname` |
| 잔액 | `GSUMY` | **저장 컬럼** (재계산 금지 — §4) | `gsumy` |
| 입금 | `GSSUM` | 입금액 | `gssum` |
| 출금 | `GBSUM` | 출금액 (파생 — §3) | `gbsum` |
| 결재 | `PUBUN` | PickList `현금·어음·은행·카드·공제·기타` | `pubun` |
| 비고 | `GBIGO` | 비고 | `gbigo` |

하단 「합계」 = **입금·출금 2컬럼만** 합산(잔액은 합계 대상 아님).

## 3. 입금/출금 분리 — DB 는 금액이 한 칸이다

`H1_Ssub` 에는 금액 컬럼이 `Gssum` **하나**뿐이고, `Gubun`('입금'/'출금')이 어느 열인지 정한다.

```
조회 후처리 (Button101Click L414~421)
  Gubun='입금' → 입금 = Gssum, 출금 = 0
  그 외        → 출금 = Gssum, 입금 = 0

저장 시 역변환 (T4_Sub11BeforePost L1336~1352 / L1394~1410)
  Scode='Y'(입고처) : 입금액≠0 → Gubun='입금',Gssum=입금액 / 아니면 '출금',Gssum=출금액
  Scode='X','Z'     : 출금액≠0 → Gubun='출금',Gssum=출금액 / 아니면 '입금',Gssum=입금액
```

> 입고처(Y)만 분기 순서가 뒤집혀 있다 — 레거시 원문 그대로 보존한다.

## 4. 잔액(GSUMY)은 재계산하지 않는다

레거시는 그리드에서 **거래처를 고르는 순간에만** `Tong40.SetTring03(Scode, Gdate, '', Gcode, Ocode)`
로 미수 잔액을 구해 `Gsumy` 에 넣고 저장한다(L732~741). 목록 조회는 그 저장값을 그대로 읽는다.
따라서 서비스도 조회 시 재계산하지 않는다 — 재계산하면 레거시와 값이 갈린다.

## 5. 조회 SQL (Button101Click L348~371)

```sql
SELECT * FROM H1_Ssub
WHERE Gdate >= :from AND Gdate <= :to
  AND Scode = :scode AND Scode <> 'A' AND Scode <> 'B'
  [AND Gcode >= :gcodeFrom AND Gcode <= :gcodeTo]   -- 끝 코드가 있을 때만
  AND Hcode = :hcode
ORDER BY Gdate, ID                     -- 입력순(CheckBox2) 체크 시
      or Gdate, Gubun, Scode, Gcode    -- 기본
LIMIT 0, 2000
```

- `Scode` = 거래구분: 거래처 `X` / 입고처 `Y` / 기타 `Z` (dfm Edit103 Items, ItemIndex 0/1/2).
- `Scode<>'A' and Scode<>'B'` 는 재고 축 행 배제 — 레거시 원문 유지.
- 거래처 범위는 **끝 코드가 비어 있으면 아예 걸리지 않는다**(`if Edit106.Text<>''`).

## 6. 쓰기 (T4_Sub11BeforePost / NewRecord)

```sql
INSERT INTO H1_Ssub (Gdate,Gubun,Hcode,Scode,Gcode,Gname,Tcode,Ocode,Oname,
                     Pubun,Gbigo,Gssum,Gsumy,Idnum) VALUES (...)
UPDATE H1_Ssub SET ... WHERE ID=:id AND Hcode=:hcode
```

- 신규 기본값(`T4_Sub11NewRecord`): `Gubun='입금'`, `Pubun='현금'`, `Gsumy=0`, `Scode`=거래구분.
- **모던 강화**: 레거시 UPDATE/DELETE 는 `ID`(+`Gdate`)만 쓰지만, `H1_Ssub` 는 chul_09 4테넌트
  공유 테이블이라 모던은 **`Hcode` 를 WHERE 에 반드시 포함**한다(교차 테넌트 수정 차단).

## 7. 위젯 ID 매핑 (`data-legacy-id`)

| dfm id | 웹 위치 |
| --- | --- |
| `Edit101` / `Edit102` | 거래일자 from~to `DateFieldYMD` |
| `Edit103` | 거래구분 `<select>` (거래처/입고처/기타) |
| `Edit104` / `Edit106` | 거래처 코드 범위 `MasterLookupField` |
| `CheckBox2` | 입력순 체크박스 |
| `dxButton1` | 검색 버튼 |
| `DBGrid101` (+ `.GDATE/.GCODE/.GNAME/.OCODE/.ONAME/.GSUMY/.GSSUM/.GBSUM/.PUBUN/.GBIGO`) | 목록 표·헤더 |
| (모던 신설) `Sobo41.New.*` | 인라인 신규 행의 각 입력 셀 |

## 8. 라이브 대조 (2026-08-23, 교문사 5019 / remote_153)

거래일자 2026.08.03, 거래구분 거래처(X) — 사용자 제공 레거시 스크린샷과 **완전 일치**:

| 거래일자 | 코드 | 거래처명 | 잔액 | 입금 | 출금 | 결재 |
| --- | --- | --- | --- | --- | --- | --- |
| 2026.08.03 | 3292 | #자유서적[파주] | 48,000 | 48,000 | 0 | 현금 |
| 2026.08.03 | 3315 | 네이버 스마트스토어 | 17,757,360 | 76,290 | 0 | 현금 |
| **합계** | | | | **124,290** | **0** | |

교문사 실사용 분포(2026년): `Pubun` 현금 1,389 / 공제 108 / 어음 12 / 카드 6,
`Scode` 는 X 만 사용, `Ocode`·`Oname`·`Tcode` 는 **전부 공란**(스크린샷의 빈 계정과목 칸과 일치).

## 9. 남은 결정

1. 어음(`H4_Iyeo` 받은일자/만기일자/어음처리)·은행(`H5_Bang` 은행명) 부가정보를 `Sname` 으로
   붙이는 후처리(L387~412)는 **미구현**. 교문사는 어음 12건뿐이라 우선순위를 낮췄다.
2. 인라인 **수정**(PUT)은 API 만 있고 화면은 신규 행 추가·삭제까지다. 셀 편집 UI 는 후속.
3. 형제 화면 `Subu42` 「입출금전표-사무실」은 미포팅.

## 10. 참조

- DEC-186(본 교체 결정), DEC-028(레이아웃 매핑 의무), DEC-033(mysql3 호환)
- 구현: `backend/app/services/cash_slip_service.py`,
  `backend/app/routers/settlement.py` `/cash-slip` 4종,
  `frontend/src/app/(app)/settlement/cash-status/page.tsx`
- 종전 문서(다른 빌드 변형): `analysis/layout_mappings/Sobo41_cash.md`
