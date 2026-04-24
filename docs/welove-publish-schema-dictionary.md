# 출판 테이블 구조 사전 (`SCH-WELOVE-출판-*`)

| 항목 | 내용 |
|------|------|
| 작성일 | 2026-04-23 |
| 원천 | [`WeLove_FTP/Welove_인수인계/출판setting/weelove/출판(테이블구조).xls`](../WeLove_FTP/Welove_인수인계/출판setting/weelove/출판(테이블구조).xls) (`MAN-030`) |
| 추출 도구 | [`tools/extract_welove_schema.py`](../tools/extract_welove_schema.py) |
| JSON 정본 | [`analysis/welove_schema_dictionary.json`](../analysis/welove_schema_dictionary.json) |
| 추적 ID | 테이블 단위 `SCH-WELOVE-출판-<TABLE>`, 필드 단위 `SCH-WELOVE-출판-<TABLE>.<field>` |

본 사전은 [`docs/db-schema-porting-readiness.md`](db-schema-porting-readiness.md) 의 컬럼 차이 진단과 [`migration/contracts/*.yaml`](../migration/contracts) 의 `data_access` 단락에 합류한다. 표시 사이즈는 레거시 운영 DB 의 ALTER 흔적(전·후) 을 그대로 보존했다.

## 1. 테이블 카탈로그 (인덱스 시트)

`v` 표기는 원본 시트의 「변경된 테이블」 마킹을 그대로 옮긴 것.

| 변경 | 테이블 | 한글 명칭 |
|:-:|---|---|
| v | `G1_Ggeo` | 거래처 |
| v | `H1_Gbun` | 계정과목 |
|  | `G1_Gbun` | 거래처구분 |
|  | `H2_Gbun` | 거래처지점/ |
| v | `G2_Ggwo` | 입고처 |
| v | `H1_Ssub` | 입출금 |
|  | `G2_Gbun` | 입고처구분 |
| v | `H4_Iyeo` | 어음 |
| v | `H5_Bang` | 은행 |
| v | `G3_Gjeo` | 저자 |
|  | `G3_Gbun` | 저자구분 |
|  | `In_Gsum` | 초기미수 |
|  | `In_Csum` | 초기재고 |
| v | `G4_Book` | 도서 |
|  | `G4_Gbun` | 도서분류 |
| v | `S1_Ssub` | 거래명세서 |
| v | `S1_Memo` | 거래명세서메모 |
| v | `G5_Ggeo` | 기타거래처 |
|  | `S1_CheK` | 거래명세서체크 |
|  | `G5_Gbun` | 거래처구분 |
| v | `S2_Ssub` | 제작명세서 |
|  | `G6_Ggeo` |  |
| v | `S3_Ssub` | 원천징수 |
|  | `S4_Ssub` | 가입고 요청서 |
| v | `G7_Ggeo` | 출판사 |
|  | `G7_Gbun` | 출판사구분 |
| v | `Sb_Csum` |  |
| v | `G8_Ggeo` |  |
| v | `Sg_Gsum` | 장부대조 |
|  | `G8_Gbun` |  |
| v | `Sg_Csum` | 재고대조 |
|  | `Gg_Magn` |  |
|  | `Sv_Gsum` |  |
|  | `Gg_Megn` |  |
|  | `Sv_Csum` |  |
|  | `Gg_Post` | 우편번호 |
|  | `Sv_Chng` | 마감(거래처) |
|  | `Gg_Prnt` |  |
|  | `Sv_Ghng` | 마감(재고) |
|  | `Gs_Gsum` |  |
| v | `T1_Gbun` | 지역분류(출판사별로) |
|  | `Gs_Csum` |  |
|  | `T1_Ssub` | 발송비 |
|  | `T2_Ssub` | 청구서 |
|  | `J1_Ggeo` | 사원관리 |
|  | `T3_Ssub` | 청구서(저장) |
|  | `J1_Ssub` |  |
| v | `T4_Ssub` | 출고내역서 |
|  | `T5_Ssub` | 입금내역 |
|  | `P1_Ggeo` |  |
|  | `T6_Ssub` | 반품수거내역 |
|  | `P1_Ssub` |  |
|  | `T7_Ssub` | 반품비 |
|  | `P2_Ssub` |  |
| v | `Id_Logn` | 로그인(계정) |
|  | `Sx_CheK` |  |
|  | `Id_Memo` | 로그인(ip별로 기록) |
| v | `Sx_Host` |  |
|  | `Ie_Logn` | 로그인(저자별) |
| v | `Sx_Memo` |  |
|  | `Ie_Memo` | 로그인(ip별로 기록) |
|  | `Me_Sage` | 메시지 |

## 2. 테이블별 필드 사전

표기: **Size(전)** = 운영 중 ALTER 이전 값, **Size(후)** = 변경 후. `c/n` = 문자(c) / 숫자(n) 구분 — 빈 값은 사전 미명시.

### `G1_Gbun` — 거래처구분

필드 6 개. 추적 ID 접두사: `SCH-WELOVE-출판-G1_Gbun`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 구분코드 | 5 |  |  |
| `gname` | 구분명 | 20 |  |  |
| `check` |  | 1 |  |  |
| `gmmeo` | timestamp | 14 |  |  |

### `G1_Ggeo` — 거래처

필드 48 개. 추적 ID 접두사: `SCH-WELOVE-출판-G1_Ggeo`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `tcode` | 북앤북(배본처) | 5 |  |  |
| `gubun` | 구분코드 | 5 |  |  |
| `jubun` | 지역 | 6 |  |  |
| `pubun` | 출고증구분 | 2 |  |  |
| `scode` |  | 1 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `ocode` |  | 5 |  |  |
| `gname` | 거래처명 | 24 | 50 |  |
| `gposa` | 대표자명 | 20 | 30 |  |
| `gnumb` | 사업자번호 | 12 |  |  |
| `guper` | 업태 | 20 | 30 |  |
| `gjomo` | 종목 | 20 | 30 |  |
| `gpost` | 우편번호 | 7 |  |  |
| `gadd1` | 주소(1) | 44 |  |  |
| `gadd2` | 주소(2) | 44 |  |  |
| `gtel1` | 전화(1) | 4 |  |  |
| `gtel2` | 전화(2) | 20 |  |  |
| `gfax1` | 팩스(1) | 4 |  |  |
| `gfax2` | 팩스(2) | 20 |  |  |
| `grat1` | 비율1(위탁) | 3 |  | n |
| `grat2` | 비율2(현매) | 3 |  | n |
| `grat3` | 비율3(매절) | 3 |  | n |
| `grat4` | 비율4(납품) | 3 |  | n |
| `grat5` | 비율5(특별) | 3 |  | n |
| `grat6` | 비율6(기타) | 3 |  | n |
| `grat7` | 비율6(한도) | 3 |  | n |
| `grat8` |  | 3 |  | n |
| `grat9` | 정지유무(0,1) | 3 |  | n |
| `gqut1` | 신간부수 |  |  | n |
| `yesno` | 계산서발행유무 | 5 |  |  |
| `name1` | 비고2 | 40 | 50 |  |
| `name2` | 계산서(거래처명) | 40 | 50 |  |
| `gpper` | 담당자 | 10 | 20 |  |
| `gbigo` | 비고1 | 40 | 50 |  |
| `gphon` | 핸드폰번호 | 15 | 50 |  |
| `email` | 정지사유 | 15 | 50 |  |
| `bigo1` | 거래방법(위탁,우수,…) | 8 |  |  |
| `bigo2` | 배송방법(소망,택배,…) | 4 |  |  |
| `bigo3` | 출력안함,일괄출력 | 8 |  |  |
| `bigo4` | 유지,보류,종료 | 4 |  |  |
| `gnum1` | 번호(수레사,해피데이) | 10 |  |  |
| `gnum2` |  | 10 |  |  |
| `memos` | 메모 | <blob> |  |  |
| `gssum` | 한도액 |  |  | n |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `G2_Gbun` — 입고처구분

필드 6 개. 추적 ID 접두사: `SCH-WELOVE-출판-G2_Gbun`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 구분코드 | 5 |  |  |
| `gname` | 구분명 | 20 |  |  |
| `check` |  | 1 |  |  |
| `gmmeo` | timestamp | 14 |  |  |

### `G2_Ggwo` — 입고처

필드 48 개. 추적 ID 접두사: `SCH-WELOVE-출판-G2_Ggwo`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `tcode` |  | 5 |  |  |
| `gubun` | 구분코드 | 5 |  |  |
| `jubun` | 지역 | 6 |  |  |
| `pubun` | 출고증구분 | 2 |  |  |
| `scode` |  | 1 |  |  |
| `gcode` | 입고처코드 | 5 |  |  |
| `ocode` |  | 5 |  |  |
| `gname` | 거래처명 | 24 | 50 |  |
| `gposa` | 대표자명 | 20 | 30 |  |
| `gnumb` | 사업자번호 | 12 |  |  |
| `guper` | 업태 | 20 | 30 |  |
| `gjomo` | 종목 | 20 | 30 |  |
| `gpost` | 우편번호 | 7 |  |  |
| `gadd1` | 주소(1) | 44 |  |  |
| `gadd2` | 주소(2) | 44 |  |  |
| `gtel1` | 전화(1) | 4 |  |  |
| `gtel2` | 전화(2) | 20 |  |  |
| `gfax1` | 팩스(1) | 4 |  |  |
| `gfax2` | 팩스(2) | 20 |  |  |
| `grat1` | 비율1(위탁) | 3 |  | n |
| `grat2` | 비율2(현매) | 3 |  | n |
| `grat3` | 비율3(매절) | 3 |  | n |
| `grat4` | 비율4(납품) | 3 |  | n |
| `grat5` | 비율5(특별) | 3 |  | n |
| `grat6` | 비율6(기타) | 3 |  | n |
| `grat7` |  | 3 |  | n |
| `grat8` |  | 3 |  | n |
| `grat9` | 정지유무(0,1) | 3 |  | n |
| `gqut1` | 신간부수 |  |  | n |
| `yesno` | 계산서발행유무 | 5 |  |  |
| `name1` | 비고2 | 40 | 50 |  |
| `name2` | 계산서(거래처명) | 40 | 50 |  |
| `gpper` | 담당자 | 10 | 20 |  |
| `gbigo` | 비고1 | 40 | 50 |  |
| `gphon` | 핸드폰번호 | 15 | 50 |  |
| `email` | 정지사유 | 15 | 50 |  |
| `bigo1` | 거래방법(위탁,우수,…) | 8 |  |  |
| `bigo2` | 배송방법(소망,택배,…) | 4 |  |  |
| `bigo3` | 출력안함,일괄출력 | 8 |  |  |
| `bigo4` | 유지,보류,종료 | 4 |  |  |
| `gnum1` |  | 10 |  |  |
| `gnum2` |  | 10 |  |  |
| `memos` | 메모 | <blob> |  |  |
| `gssum` | 한도액 |  |  | n |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `G3_Gbun` — 저자구분

필드 6 개. 추적 ID 접두사: `SCH-WELOVE-출판-G3_Gbun`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 구분코드 | 5 |  |  |
| `gname` | 구분명 | 20 |  |  |
| `check` |  | 1 |  |  |
| `gmmeo` | timestamp | 14 |  |  |

### `G3_Gjeo` — 저자

필드 38 개. 추적 ID 접두사: `SCH-WELOVE-출판-G3_Gjeo`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gubun` | 구분코드 | 5 |  |  |
| `scode` |  | 1 |  |  |
| `gcode` | 저자코드 | 5 |  |  |
| `gposa` | 저자명 | 20 | 30 |  |
| `gname` | 직작명 | 24 | 50 |  |
| `date1` | 등록일자 | 10 |  |  |
| `date2` |  | 10 |  |  |
| `gjice` | 직책명 | 20 |  |  |
| `gscho` | 출신학교 | 20 |  |  |
| `gnumb` | 사업자번호 | 20 |  |  |
| `gnum1` | 주민등록 | 20 |  |  |
| `gnum2` | 계좌번호 | 20 |  |  |
| `gtel1` | 전화(1) | 4 |  |  |
| `gtel2` | 전화(2) | 9 | 20 |  |
| `gfax1` | 팩스(1) | 4 |  |  |
| `gfax2` | 팩스(2) | 9 | 20 |  |
| `gpost` | 집주소 | 7 |  |  |
| `gadd1` | 주소(1) | 44 |  |  |
| `gadd2` | 주소(2) | 44 |  |  |
| `gpost` | 직장주소 | 7 |  |  |
| `gadd1` | 주소(1) | 44 |  |  |
| `gadd2` | 주소(2) | 44 |  |  |
| `gbigo` | 비고1 | 40 | 50 |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |
| `f11~f19` | 필드사용 유무체크 |  |  |  |
| `f21~f29` |  |  |  |  |
| `f31~f39` |  |  |  |  |
| `f41~f49` |  |  |  |  |
| `f51~f59` |  |  |  |  |
| `f61~f69` |  |  |  |  |
| `f71~f79` |  |  |  |  |
| `f81~f89` |  |  |  |  |
| `Ghost` | 아이디 |  |  |  |
| `Gpass` | 패스워드 |  |  |  |
| `yesno` | 사용정지(유무) |  |  |  |

### `G4_Book` — 도서

필드 55 개. 추적 ID 접두사: `SCH-WELOVE-출판-G4_Book`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `tcode` | 북앤북(수량,부록,CD,태잎) | 5 |  |  |
| `gubun` | 분류코드 | 5 |  |  |
| `jubun` | 도서처리 | 6 |  |  |
| `pubun` |  | 2 |  |  |
| `scode` | 도서구분 | 1 |  |  |
| `gcode` | 도서코드 | 10 |  |  |
| `ocode` |  | 10 |  |  |
| `gname` | 도서명 | 40 | 80 |  |
| `gjeja` | 저자 | 20 | 30 |  |
| `gdabi` | 단위 | 6 |  |  |
| `gdang` | 단가 |  |  | n |
| `odang` | 매입가 |  |  | n |
| `price` | 원가 |  |  | n |
| `gisbn` | ISBN | 20 |  |  |
| `grat1` | 비율1(위탁) | 3 |  | n |
| `grat2` | 비율2(현매) | 3 |  | n |
| `grat3` | 비율3(매절) | 3 |  | n |
| `grat4` | 비율4(납품) | 3 |  | n |
| `grat5` | 비율5(특별) | 3 |  | n |
| `grat6` | 비율6(기타) | 3 |  | n |
| `grat7` | 비율7(한도),세액(손수레,북앤북) |  |  | n |
| `grat8` | 셋트(물류청구) |  |  | n |
| `grat9` | 정지유무(0,1) |  |  | n |
| `srat1` | 인세율 |  |  | n |
| `gbill` | 도서질 | 6 |  |  |
| `date1` | 발행일 | 10 |  |  |
| `date2` | 등록일 | 10 |  |  |
| `gnumb` | 등록번호 | 20 |  |  |
| `name1` | 판형 | 40 | 50 |  |
| `name2` | 정지사유 | 40 | 50 |  |
| `gpage` | 페이지(쪽수) |  |  | n |
| `gpan1` | 페이지(판수) |  |  | n |
| `gpan2` |  |  |  | n |
| `gbigo` | 비고1 | 40 | 50 |  |
| `yesno` | 종당관리비(유,무) | 5 |  |  |
| `jeja1` |  | 20 |  |  |
| `jeja2` |  | 20 |  |  |
| `apost` | 창고동위치 | 20 |  |  |
| `gpost` | 서가위치 | 20 |  |  |
| `opost` |  | 20 |  |  |
| `bcode` |  | 13 |  |  |
| `bigo1` | 세액유무 | 2 |  |  |
| `bigo2` | 재고절판,재고현황에서 안보이기 | 2 |  |  |
| `bigo3` | 전자책 | 2 |  |  |
| `bigo4` | 청구서에 재고미청구 | 2 |  |  |
| `memo1` | 계약조건 | 50 |  |  |
| `memo2` | 메모2 | 50 |  |  |
| `memos` | 메모 | <blob> |  |  |
| `gqut1` | 덩이(라벨) |  |  | n |
| `gqut2` | 그람(라벨) |  |  | n |
| `gssum` |  |  |  | n |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `G4_Gbun` — 도서분류

필드 10 개. 추적 ID 접두사: `SCH-WELOVE-출판-G4_Gbun`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 구분코드 | 5 |  |  |
| `gname` | 구분명 | 20 |  |  |
| `grat1` |  | 3 |  | n |
| `grat2` |  | 3 |  | n |
| `grat3` |  | 3 |  | n |
| `grat4` |  | 3 |  | n |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `G5_Gbun` — 거래처구분

필드 6 개. 추적 ID 접두사: `SCH-WELOVE-출판-G5_Gbun`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 구분코드 | 5 |  |  |
| `gname` | 구분명 | 20 |  |  |
| `check` |  | 1 |  |  |
| `gmmeo` | timestamp | 14 |  |  |

### `G5_Ggeo` — 기타거래처

필드 48 개. 추적 ID 접두사: `SCH-WELOVE-출판-G5_Ggeo`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `tcode` |  | 5 |  |  |
| `gubun` | 구분코드 | 5 |  |  |
| `jubun` | 지역 | 6 |  |  |
| `pubun` | 출고증구분 | 2 |  |  |
| `scode` |  | 1 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `ocode` |  | 5 |  |  |
| `gname` | 거래처명 | 24 | 50 |  |
| `gposa` | 대표자명 | 20 | 30 |  |
| `gnumb` | 사업자번호 | 12 |  |  |
| `guper` | 업태 | 20 | 30 |  |
| `gjomo` | 종목 | 20 | 30 |  |
| `gpost` | 우편번호 | 7 |  |  |
| `gadd1` | 주소(1) | 44 |  |  |
| `gadd2` | 주소(2) | 44 |  |  |
| `gtel1` | 전화(1) | 4 |  |  |
| `gtel2` | 전화(2) | 20 |  |  |
| `gfax1` | 팩스(1) | 4 |  |  |
| `gfax2` | 팩스(2) | 20 |  |  |
| `grat1` | 비율1(위탁) | 3 |  | n |
| `grat2` | 비율2(현매) | 3 |  | n |
| `grat3` | 비율3(매절) | 3 |  | n |
| `grat4` | 비율4(납품) | 3 |  | n |
| `grat5` | 비율5(특별) | 3 |  | n |
| `grat6` | 비율6(기타) | 3 |  | n |
| `grat7` |  | 3 |  | n |
| `grat8` |  | 3 |  | n |
| `grat9` | 정지유무(0,1) | 3 |  | n |
| `gqut1` | 신간부수 |  |  | n |
| `yesno` | 계산서발행유무 | 5 |  |  |
| `name1` | 비고2 | 40 | 50 |  |
| `name2` | 계산서(거래처명) | 40 | 50 |  |
| `gpper` | 담당자 | 10 | 20 |  |
| `gbigo` | 비고1 | 40 | 50 |  |
| `gphon` | 핸드폰번호 | 15 | 50 |  |
| `email` | 정지사유 | 15 | 50 |  |
| `bigo1` | 거래방법(위탁,우수,…) | 8 |  |  |
| `bigo2` | 배송방법(소망,택배,…) | 4 |  |  |
| `bigo3` | 출력안함,일괄출력 | 8 |  |  |
| `bigo4` | 유지,보류,종료 | 4 |  |  |
| `gnum1` |  | 10 |  |  |
| `gnum2` |  | 10 |  |  |
| `memos` | 메모 | <blob> |  |  |
| `gssum` | 한도액 |  |  | n |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `G6_Ggeo`

필드 19 개. 추적 ID 접두사: `SCH-WELOVE-출판-G6_Ggeo`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `bcode` | 도서코드 | 10 |  |  |
| `gubun` | 구분명 | 20 |  |  |
| `jubun` | 지역명 | 6 | 20 |  |
| `gpper` | 담당자 | 10 | 20 |  |
| `grat1` | 비율1(위탁) | 3 |  | n |
| `grat2` | 비율2(현매) | 3 |  | n |
| `grat3` | 비율3(매절) | 3 |  | n |
| `grat4` | 비율4(납품) | 3 |  | n |
| `grat5` | 비율5(특별) | 3 |  | n |
| `grat6` | 비율6(기타) | 3 |  | n |
| `grat7` |  | 3 |  | n |
| `grat8` |  | 3 |  | n |
| `grat9` |  | 3 |  | n |
| `gssum` |  | 10 |  | n |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `G7_Ggeo` — 출판사

필드 54 개. 추적 ID 접두사: `SCH-WELOVE-출판-G7_Ggeo`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `chek1` | 반품입력유무(True),개별거래처(본사,창고) | 5 |  |  |
| `chek2` | List별도(True,False),개별거래처(폐기->정품),북앤북:신영(과거자료수정할수있게) | 5 |  |  |
| `chek3` | 유통(도서셋트수량:사용유무) | 5 | ok:(더북)->창고재고 수정못하게 |  |
| `chek4` | 코업북(자료전송) | 5 |  |  |
| `chek5` | 과거자료수정유무(True,False) | 5 |  |  |
| `hcode` | 전표번호(사용유무),(bqut:반품입력시 정품이 먼저) | 5 |  |  |
| `gubun` | 구분코드 | 5 |  |  |
| `jubun` | 지역 | 6 |  |  |
| `scode` | 출고중지유무(Y,N) | 1 |  |  |
| `gcode` | 출판사코드 | 5 |  |  |
| `ocode` | (1:사용중지,전송중지) | 5 |  |  |
| `gname` | 출판사명 | 24 | 50 |  |
| `gposa` | 대표자명 | 20 | 30 |  |
| `gnumb` | 사업자번호 | 12 |  |  |
| `guper` | 업태 | 20 | 30 |  |
| `gmemo` | 종목 | 20 | 30 |  |
| `name1` | 핸드폰번호 | 30 | 50 |  |
| `name2` | 참고내용 | 30 | 50 |  |
| `jumin` | 계산서발행유무(True) | 14 |  |  |
| `gpper` | 담당자 | 10 | 20 |  |
| `gpost` | 우편번호 | 7 |  |  |
| `gadd1` | 주소(1) | 44 |  |  |
| `gadd2` | 주소(2) | 44 |  |  |
| `gtel1` | 전화(1) | 4 |  |  |
| `gtel2` | 전화(2) | 20 |  |  |
| `gfax1` | 팩스(1) | 4 |  |  |
| `gfax2` | 팩스(2) | 20 |  |  |
| `email` |  | 40 | 50 |  |
| `gbigo` | 비고 | 40 | 50 |  |
| `bigo1` | 비고(청구서) | 40 | 50 |  |
| `bigo2` | 계좌번호 | 40 | 50 |  |
| `gnum1` | 번호(수레사,해피데이) | 10 |  |  |
| `memo1` | 명세서하단출력1 | 50 |  |  |
| `memo2` | 명세서하단출력2 | 50 |  |  |
| `memo3` | 명세서하단출력3 | 50 |  |  |
| `gdate` | 계약일자 | 10 |  |  |
| `date1` | 시작일 | 2 |  |  |
| `date2` | 종료일 | 2 |  |  |
| `yesno` |  | 5 |  |  |
| `memos` | 메모장 |  | blob |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |
| `chek3` | ok: 창고(접수된 자료 수정못하고), 예)더북 |  |  |  |
| `` | 거래명세서,입고명세서,재고변경 창고재고 못하게, 예)최강물류 |  |  |  |
| `` | True: 거래처(창고 미접수시 전송못하게), 예)경문사 |  |  |  |
| `` | :배본사(도서셋트시 사용) |  |  |  |
| `` | False: |  |  |  |
| `` | Jeago: 도서관리에 (본사,창고) 재고 보이게, 예)학고재 |  |  |  |
| `` | isbn: 도서검색,거래현황isbn나오게, 예)K & J |  |  |  |
| `` | grat1,grat2: 입력전 내용불러오기(단가,비율), 예)스타리치북스 |  |  |  |
| `` | grat9:거래명세서(사용유무된 거래처,도서)안나오게, 예)골든벨 |  |  |  |
| `` | send: 문화유통,북센 등 자료전송, 예)플로스예감 |  |  |  |
| `` | bqut: 반품입력시 정품이 먼저, 예)경문사 |  |  |  |

### `G8_Gbun`

필드 6 개. 추적 ID 접두사: `SCH-WELOVE-출판-G8_Gbun`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 구분코드 | 5 |  |  |
| `gname` | 구분명 | 20 |  |  |
| `check` |  | 1 |  |  |
| `gmmeo` | timestamp | 14 |  |  |

### `G8_Ggeo`

필드 23 개. 추적 ID 접두사: `SCH-WELOVE-출판-G8_Ggeo`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gubun` |  | 5 |  |  |
| `jubun` |  | 6 |  |  |
| `scode` |  | 1 |  |  |
| `gcode` |  | 5 |  |  |
| `ocode` |  | 5 |  |  |
| `gname` |  | 24 | 50 |  |
| `gposa` |  | 30 |  |  |
| `gdate` |  | 10 |  |  |
| `name1` |  | 30 | 50 |  |
| `name2` |  | 30 | 50 |  |
| `gpost` | 우편번호 | 7 |  |  |
| `gadd1` | 주소(1) | 44 |  |  |
| `gadd2` | 주소(2) | 44 |  |  |
| `gtel1` | 전화(1) | 4 |  |  |
| `gtel2` | 전화(2) | 14 | 20 |  |
| `gfax1` | 팩스(1) | 4 |  |  |
| `gfax2` | 팩스(2) | 14 | 20 |  |
| `email` |  | 40 | 50 |  |
| `gbigo` |  | 40 | 50 |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `H1_Gbun` — 계정과목

필드 15 개. 추적 ID 접두사: `SCH-WELOVE-출판-H1_Gbun`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 계정코드 | 5 |  |  |
| `gname` | 계정과목(화면) | 20 | 50 |  |
| `oname` | 계정과목(출력) | 40 | 50 |  |
| `gdate` | 초기일자 | 10 |  |  |
| `clas1` | 현금 |  |  | n |
| `clas2` | 어음 |  |  | n |
| `clas3` | 은행 |  |  | n |
| `gsum1` |  |  |  | n |
| `gsum2` |  |  |  | n |
| `gsum3` |  |  |  | n |
| `scode` | 구분(1,2,3,0) | 1 |  |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `H1_Ssub` — 입출금

필드 21 개. 추적 ID 접두사: `SCH-WELOVE-출판-H1_Ssub`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `idnum` |  |  |  |  |
| `hcode` | 출판사코드 | 5 |  |  |
| `gdate` | 거래일자 | 10 |  |  |
| `gubun` | 구분(입금,출금) | 4 |  |  |
| `scode` | 구분(X,Y,Z) | 1 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `gname` | 거래처명 | 24 | 50 |  |
| `tcode` |  | 1 |  |  |
| `ocode` | 계정코드 | 5 |  |  |
| `oname` | 계정명 | 20 | 50 |  |
| `gssum` | 금액 | 10 |  | n |
| `gsumx` | 전잔액 | 10 |  | n |
| `gsumy` | 미수금 | 10 |  | n |
| `pubun` | 구분(현금,어음,은행) | 4 |  |  |
| `gbigo` | 비고 | 15 | 50 |  |
| `check` |  | 1 |  |  |
| `time1` | datetime |  |  |  |
| `time2` | datetime |  |  |  |
| `time3` | datetime |  |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `H2_Gbun` — 거래처지점/

필드 17 개. 추적 ID 접두사: `SCH-WELOVE-출판-H2_Gbun`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `gname` | 지점명 | 20 |  |  |
| `oname` | 코드 | 40 |  |  |
| `jubun` | 지역 | 15 |  |  |
| `gdate` | 구분(시내,지방) | 10 |  |  |
| `clas1` |  |  |  | n |
| `clas2` |  |  |  | n |
| `clas3` |  |  |  | n |
| `gsum1` |  |  |  | n |
| `gsum2` |  |  |  | n |
| `gsum3` |  |  |  | n |
| `scode` | 구분(X,Y,Z) | 1 |  |  |
| `gbigo` | 출고정지사유 | 40 |  |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `H4_Iyeo` — 어음

필드 20 개. 추적 ID 접두사: `SCH-WELOVE-출판-H4_Iyeo`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `idnum` |  | int |  |  |
| `hcode` | 출판사코드 | 5 |  |  |
| `gnumb` | 어음번호 | 12 |  |  |
| `gname` | 발행처 | 20 | 50 |  |
| `gposa` | 발행인 | 20 | 30 |  |
| `date1` | 발행일자 | 10 |  |  |
| `date2` | 받은일자 | 10 |  |  |
| `date3` | 지급일자 | 10 |  |  |
| `date4` | 만기일자 | 10 |  |  |
| `gbang` | 지급은행 | 12 | 50 |  |
| `name1` | 지급처 | 12 | 50 |  |
| `name2` | 지급지점 | 20 | 50 |  |
| `scode` | 처리코드(보유증,할인율) | 8 |  |  |
| `grat1` | 할인율 | int |  | n |
| `gosum` | 금액 | 10 |  | n |
| `gssum` | 할인금액 | 10 |  | n |
| `gbigo` | 비고 | 50 |  |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `H5_Bang` — 은행

필드 16 개. 추적 ID 접두사: `SCH-WELOVE-출판-H5_Bang`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 은행코드 | 8 |  |  |
| `gname` | 은행명 | 24 | 50 |  |
| `gposa` | 예금주 | 10 | 30 |  |
| `gnumb` | 계좌번호 | 24 |  |  |
| `gubun` | 은행구분 | 20 |  |  |
| `gtels` | 전화번호 | 15 |  |  |
| `name1` | 고객번호 | 20 |  |  |
| `name2` | 거래점 | 20 |  |  |
| `gdate` | 초기일자 | 10 |  |  |
| `class` | 초기금액 | 10 |  | n |
| `gssum` |  | 10 |  | n |
| `gsusu` |  | 10 |  | n |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `Id_Logn` — 로그인(계정)

필드 15 개. 추적 ID 접두사: `SCH-WELOVE-출판-Id_Logn`.

> **운영 의미 보조 (DEC-RBAC-01 — 계약 정본 기준)**
>
> 본 표의 한글 라벨은 원본 사전 그대로다. 실제 운영 계약(`migration/contracts/login.yaml` v1.1.0,
> `docs/profile-password-ux-spec.md`) 기준 의미는 다음과 같이 **반대로** 매핑된다:
>
> - `gcode` → **로그인 ID / 사번 (Logn2)** — Pydantic 모델의 `user_id`. **불변**.
> - `gname` → **표시명 / 작업자 이름 (Logn1)** — `UserInfo.display_name`. 본인 프로필에서 수정 가능.
> - `hname` → **조직명 / 출판사명** — `UserInfo.user_name`. 헤더 표시.
> - `hcode` → 권한·고객사 분기 키 — RBAC 게이트와 ACTR-DEC-02 슈퍼유저 신호(`'0000'`) 의 1차 키.
>
> 사전 라벨과 운영 의미 간 불일치는 [`docs/decision-rbac-and-id-logn-truth.md`](decision-rbac-and-id-logn-truth.md)
> DEC-RBAC-01 에서 영구 결정. 코드/UI 가시 라벨은 본 보조 의미를 따른다.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `hname` | 출판사명 | 50 |  |  |
| `gcode` | 사용자 | 50 | 50 |  |
| `gname` | 아이디 | 50 | 50 |  |
| `f11~f19` |  |  |  |  |
| `f21~f29` |  |  |  |  |
| `f31~f39` |  |  |  |  |
| `f41~f49` |  |  |  |  |
| `f51~f59` |  |  |  |  |
| `f61~f69` |  |  |  |  |
| `f71~f79` |  |  |  |  |
| `f81~f89` |  |  |  |  |
| `gpass` | paaword | 20 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `Ie_Logn` — 로그인(저자별)

필드 7 개. 추적 ID 접두사: `SCH-WELOVE-출판-Ie_Logn`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `scode` | 구분(T) | 1 |  |  |
| `gcode` | 저자코드 | 5 |  |  |
| `bcode` | 도서코드 | 10 |  |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `S1_CheK` — 거래명세서체크

필드 17 개. 추적 ID 접두사: `SCH-WELOVE-출판-S1_CheK`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gdate` | 거래일자 | 10 |  |  |
| `scode` | 구분(X,Y,Z) | 1 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `ocode` | 구분(A,B) | 1 |  |  |
| `jubun` | 전표구분 | 2 |  |  |
| `gjisa` | 지점명 | 15 | 30 |  |
| `bcode` | 도서코드 | 10 |  |  |
| `gsqut` | 수량 | 10 |  | n |
| `yesno` |  | 5 |  |  |
| `check` |  | 1 |  |  |
| `time1` | datetime |  |  |  |
| `time2` | datetime |  |  |  |
| `time3` | datetime |  |  |  |
| `time4` | datetime |  |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `S1_Memo` — 거래명세서메모

필드 19 개. 추적 ID 접두사: `SCH-WELOVE-출판-S1_Memo`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gdate` | 거래일자 | 10 |  |  |
| `scode` | 구분(X,Y,Z) | 1 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `gubun` | 구분(입고,출고,반품) | 4 |  |  |
| `jubun` | 전표구분 | 2 |  |  |
| `ocode` | 구분(A,B) | 1 |  |  |
| `gbigo` | 비고(1) | 50 |  |  |
| `sbigo` | 비고(2) | 50 |  |  |
| `gtel1` | 핸드폰번호 | 20 |  |  |
| `gtel2` | 전화번호 | 20 |  | n |
| `gname` | 받는사람 | 30 |  | n |
| `gjisa` | 지점명 | 15 | 30 | n |
| `check` |  | 1 |  |  |
| `time1` | datetime |  |  |  |
| `time2` | datetime |  |  |  |
| `time3` | datetime |  |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `S1_Ssub` — 거래명세서

필드 27 개. 추적 ID 접두사: `SCH-WELOVE-출판-S1_Ssub`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `idnum` |  | int |  |  |
| `hcode` | 출판사코드 | 5 |  |  |
| `gdate` | 거래일자 | 10 |  |  |
| `bdate` | 반품일자 | 10 |  |  |
| `scode` | 구분(X,Y,Z) | 1 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `ocode` | 구분(A,B) | 1 |  |  |
| `bcode` | 도서코드 | 10 |  |  |
| `gubun` | 구분(입고,출고,반품) | 4 |  |  |
| `jubun` | 전표구분 | 2 |  |  |
| `pubun` | 구분(위탁,현매,매절…) | 4 |  |  |
| `gsqut` | 수량 | 10 |  | n |
| `qsqut` |  | 10 |  | n |
| `gdang` | 단가 | 10 |  | n |
| `grat1` | 비율 | int |  | n |
| `gssum` | 금액 | 10 |  | n |
| `jeago` | 재고 | 10 |  | n |
| `gbigo` | 비고 | 20 | 50 |  |
| `yesno` | 접수유무 | 5 |  |  |
| `gjisa` | 지점명 | 15 | 30 |  |
| `check` |  | 1 |  |  |
| `time1` | datetime |  |  |  |
| `time2` | datetime |  |  |  |
| `time3` | datetime |  |  |  |
| `time4` | datetime |  |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `S2_Ssub` — 제작명세서

필드 59 개. 추적 ID 접두사: `SCH-WELOVE-출판-S2_Ssub`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `ycode` | 출판사코드 | 5 |  |  |
| `gdate` | 거래일자 | 10 |  |  |
| `gubun` | 제작구분 | 10 |  |  |
| `scode` |  | 1 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `gname` | 거래처명 | 24 | 50 |  |
| `hcode` |  | 1 |  |  |
| `ocode` | 계정코드 | 5 |  |  |
| `oname` | 계정명 | 24 | 50 |  |
| `bcode` | 도서코드 | 10 |  |  |
| `jubun` |  | 20 |  |  |
| `gsqut` |  | 10 |  | n |
| `gdang` |  | 10 |  | n |
| `gssum` | 금액 | 10 |  | n |
| `gbigo` | 비고 | 20 | 50 |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |
| `id` | auto |  |  | n |
| `gdate` | 거래일자 | 10 |  |  |
| `sdate` |  | 10 |  |  |
| `hcode` | 출판사코드 | 5 |  |  |
| `sum01` | 당월총출고부수 |  |  | n |
| `sum02` | 기본부수및및월정료(부수) |  |  | n |
| `sum03` | 기본부수및및월정료(금액) |  |  | n |
| `sum04` | 기본부수및및월정료(합계) |  |  | n |
| `sum05` | 초과부수(부수) |  |  | n |
| `sum06` | 초과부수(금액) |  |  | n |
| `sum07` | 초과부수(합계) |  |  | n |
| `sum08` | 지방직송비(부수) |  |  | n |
| `sum09` | 지방직송비(금액) |  |  | n |
| `sum10` | 지방직송비(합계) |  |  | n |
| `sum11` | 책보호대(부수) |  |  | n |
| `sum12` | 책보호대(금액) |  |  | n |
| `sum13` | 책보호대(합계) |  |  | n |
| `sum14` | 박스대(부수) |  |  | n |
| `sum15` | 박스대(금액) |  |  | n |
| `sum16` | 박스대(합계) |  |  | n |
| `sum17` | 발송비 |  |  | n |
| `sum18` | 입출고월정관리비(부수) |  |  | n |
| `sum19` | 입출고월정관리비(금액) |  |  | n |
| `sum20` | 입출고월정관리비(합계) |  |  | n |
| `sum21` | 입출고초과관리비(부수) |  |  | n |
| `sum22` | 입출고초과관리비(금액) |  |  | n |
| `sum23` | 입출고초과관리비(합계) |  |  | n |
| `sum24` | 반품월정관리 |  |  | n |
| `sum25` | 전산작업업무비 |  |  | n |
| `sum26` | 전월미수금 |  |  | n |
| `sum27` | 당월청구비 |  |  | n |
| `sum28` | 부가세 |  |  | n |
| `sum29` | 월말정폼도서총재고 |  |  | n |
| `sum30` | 합계금액 |  |  | n |
| `sum31` |  |  |  | n |
| `sum32` |  |  |  | n |
| `sum33` | 정품재고월보관비(부수) |  |  | n |
| `sum34` | 정품재고월보관비(금액) |  |  | n |
| `sum35` | 정품재고월보관비(합계) |  |  | n |
| `sum36` | 비고(금액) |  |  | n |
| `sum37` | 참고사항(금액) |  |  | n |

### `S3_Ssub` — 원천징수

필드 13 개. 추적 ID 접두사: `SCH-WELOVE-출판-S3_Ssub`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 저자코드 | 5 |  |  |
| `gname` | 저자명 | 20 | 50 |  |
| `gdate` | 거래일자 | 10 |  |  |
| `bcode` | 적요 | 10 | 50 |  |
| `gssum` | 지급액 | 10 |  | n |
| `grat1` | 세율 | 10 |  | n |
| `gisum` | 소득세 | 10 |  | n |
| `gosum` | 주민세 | 10 |  | n |
| `gbsum` | 합계 | 10 |  | n |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `S4_Ssub` — 가입고 요청서

필드 18 개. 추적 ID 접두사: `SCH-WELOVE-출판-S4_Ssub`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `bcode` | 도서코드 | 10 |  |  |
| `gdate` | 거래일자 | 10 |  |  |
| `sdate` | 출간예정일 | 10 |  |  |
| `gbigo` | 담당자 | 20 |  |  |
| `memo1` | 메모 | text |  |  |
| `gsqut` | 수량 | 10 |  |  |
| `gdang` | 단가 | 10 |  |  |
| `code1` | 신간 | 2 |  |  |
| `code2` | 요청 | 2 |  |  |
| `code3` | 확인 | 2 |  |  |
| `check` |  | 1 |  |  |
| `time1` | datetime |  |  |  |
| `time2` | datetime |  |  |  |
| `time3` | datetime |  |  |  |
| `time4` | datetime |  |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `T1_Gbun` — 지역분류(출판사별로)

필드 9 개. 추적 ID 접두사: `SCH-WELOVE-출판-T1_Gbun`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `gname` | 구분 | 20 |  |  |
| `gjisa` | 지정명 | 15 | 30 |  |
| `jubun` | 지역 | 15 |  |  |
| `bebon` | 배본 | 10 |  |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `T1_Ssub` — 발송비

필드 14 개. 추적 ID 접두사: `SCH-WELOVE-출판-T1_Ssub`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gdate` | 거래일자 | 10 |  |  |
| `gcode` |  | 5 |  |  |
| `gname` | 거래처명 | 24 |  |  |
| `name1` | 지역명 | 30 |  |  |
| `name2` | 화물명 | 30 |  |  |
| `gnumb` | 운송장번호 | 30 |  |  |
| `gbigo` | 비고 | 50 |  |  |
| `gsqut` | 부수 | 10 |  | n |
| `gdang` | 단가 | 10 |  | n |
| `gssum` | 금액 | 10 |  | n |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `T3_Ssub` — 청구서(저장)

필드 25 개. 추적 ID 접두사: `SCH-WELOVE-출판-T3_Ssub`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gdate` | 거래일자 | 10 |  |  |
| `gcode` |  | 5 |  |  |
| `gname` | 서점명 | 24 |  |  |
| `name1` | 발송비내역 | 30 |  |  |
| `name2` | 반품내역 | 30 |  |  |
| `gqut1` | 시내부수 |  |  | n |
| `gqut2` | 지방부수 |  |  | n |
| `gqut3` | 박스대 |  |  | n |
| `gqut4` | 보호대 |  |  | n |
| `gqut5` | 반품총부수 |  |  | n |
| `gqut6` | 반품내역(박스) |  |  | n |
| `gqut7` | 반품내역(금액) |  |  | n |
| `gqut8` |  |  |  | n |
| `gqut9` |  |  |  | n |
| `gsqut` | 발송내역(박스) |  |  | n |
| `gssum` | 발송내역(금액) |  |  | n |
| `aqut1` |  |  |  | n |
| `aqut2` |  |  |  | n |
| `bqut1` |  |  |  | n |
| `bqut2` |  |  |  | n |
| `yesno` | 저장유무 | 5 |  |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `T4_Ssub` — 출고내역서

필드 14 개. 추적 ID 접두사: `SCH-WELOVE-출판-T4_Ssub`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gdate` | 거래일자 | 10 |  |  |
| `gcode` | 거래처코드 | 5 |  |  |
| `gjisa` | 지점명 | 15 | 30 |  |
| `jubun` | 전표구분 | 2 |  |  |
| `pubun` |  | 2 |  |  |
| `gsqut` |  |  |  | n |
| `gqut1` | 덩이 |  |  | n |
| `gqut2` | 보호대 |  |  | n |
| `gqut3` | 박스 |  |  | n |
| `gbigo` | 비고 | 40 |  |  |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

### `T5_Ssub` — 입금내역

필드 9 개. 추적 ID 접두사: `SCH-WELOVE-출판-T5_Ssub`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `sdate` | 입금일자 | 7 |  |  |
| `gdate` | 청구일자 | 10 |  |  |
| `gssum` | 금액 |  |  | n |
| `pubun` | 결재 | 4 |  |  |
| `gbigo` | 비고 | 40 |  |  |
| `check` |  | 1 |  |  |
| `gmmeo` | timestamp | 14 |  |  |

### `T6_Ssub` — 반품수거내역

필드 13 개. 추적 ID 접두사: `SCH-WELOVE-출판-T6_Ssub`.

| 필드 | 설명 | Size(전) | Size(후) | c/n |
|---|---|---|---|---|
| `id` | auto |  |  | n |
| `hcode` | 출판사코드 | 5 |  |  |
| `gdate` | 거래일자 | 10 |  |  |
| `gcode` |  | 5 |  |  |
| `gname` | 거래처명 | 24 |  |  |
| `name1` | 지역명 | 30 |  |  |
| `name2` | 화물명 | 30 |  |  |
| `gnumb` | 운송장번호 | 30 |  |  |
| `gbigo` | 비고 | 50 |  |  |
| `gqut1` | 시내 |  |  | n |
| `gqut2` | 지방 |  |  | n |
| `check` |  | 1 |  |  |
| `gmemo` | timestamp | 14 |  |  |

## 3. 활용

- **컬럼 어댑터** (`*_adapt.py`): 본 사전의 `Size(전)→Size(후)` 변경 흔적이 mysql3 호환 어댑터(DEC-033)의 1차 후보가 된다.
- **CRUD 동등성**: `crud-backlog.md` 의 갭 표는 본 사전과 `analysis/db_impact_matrix.json` 의 교차 결과(`docs/welove-schema-reconciliation.md`)에 의존한다.
- **계약 보강**: 마스터 계약(`migration/contracts/master_data.yaml`) 의 `endpoints[*].columns` 는 본 사전 행을 단일 원천으로 인용한다.
