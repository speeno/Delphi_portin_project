# 화면·비즈니스 플로우 정리 (루트 정본)

**범위**: 워크스페이스 루트 [`Chul.pas`](../Chul.pas) MDI `Subu00`의 **메인 메뉴·팝업 메뉴**에 연결된 `Menu*Click` 핸들러를 기준으로 자동 추출했습니다.

**한계**: 툴바(`ToolButton*Click`), `nForm` 문자열로 여는 `Sobo*` 단추(배경 이미지 등)는 이 표에 **포함되지 않습니다**.

**권한**: `Base10.Seek_Uses('Fxx')` 결과가 `X`이면 `E_Connect`로 막힙니다. 실제 표시 여부는 DB 권한 테이블에 따릅니다.

관련: [06-forms-runtime-graph.md](06-forms-runtime-graph.md), [08-base01-inventory.md](08-base01-inventory.md), [09-settings-external.md](09-settings-external.md).

## 비즈니스 플로우(대메뉴) 개요

아래는 **대메뉴 섹션**별로 하위 메뉴 경로와 열리는 폼/권한 키를 정리한 표입니다.

## 플로우: 기초관리

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 메인 메뉴 / 기초관리 / E&xit | `Menu109Click` | `TSobo19` | `Subu19.pas` | `Subu19.pas` | F19 | — |
| 메인 메뉴 / 기초관리 / 거래처관리-개별 | `Menu105Click` | `TSobo15` | `Subu15.pas` | `Subu15.pas` | F13 | — |
| 메인 메뉴 / 기초관리 / 거래처관리-통합 | `Menu101Click` | `TSobo11` | `Subu11.pas` | `Subu11.pas` | F13 | — |
| 메인 메뉴 / 기초관리 / 도서관리 | `Menu104Click` | `TSobo14` | `Subu14.pas` | `Subu14.pas` | F14 | — |
| 메인 메뉴 / 기초관리 / 입고처관리 | `Menu102Click` | `TSobo12` | `Subu12.pas` | `Subu12.pas` | F12 | — |
| 메인 메뉴 / 기초관리 / 종당관리(도서) | `Menu108Click` | `TSobo18` | `Subu18.pas` | `Subu18.pas` | F15 | — |
| 메인 메뉴 / 기초관리 / 지역분류(시내+지방) | `Menu103Click` | `TSobo13` | `Subu13.pas` | `Subu13.pas` | F17 | — |
| 메인 메뉴 / 기초관리 / 출고증정렬 | `Menu103_1Click` | `TSobo13_1` | `Subu13_1.pas` | `Subu13_1.pas` | F17 | — |
| 메인 메뉴 / 기초관리 / 출판사관리 | `Menu107Click` | `TSobo17` | `Subu17.pas` | `Subu17.pas` | F11 | — |
| 메인 메뉴 / 기초관리 / 출판사관리(설정) | `Menu408Click` | `TSobo48` | `Subu48.pas` | `Subu48.pas` | F11 | — |
| 메인 메뉴 / 기초관리 / 출판사관리-택배 | `Menu107_1Click` | `TSobo17_1` | `Subu17_1.pas` | `Subu17_1.pas` | F11 | — |
| 메인 메뉴 / 기초관리 / 특별관리 | `Menu106Click` | `TSobo16` | `Subu16.pas` | `Subu16.pas` | F16 | — |
| 메인 메뉴 / 기초관리 / 환경설정 | `Menu110Click` | `TSobo10` | `Subu10.pas` | `Subu10.pas` | F18 | login/register modal Subu10 |

## 플로우: 내역서관리

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 메인 메뉴 / 내역서관리 / 기간별반품내역서 | `Menu508Click` | `TSobo58` | `Subu58.pas` | `Subu58.pas` | F57 | — |
| 메인 메뉴 / 내역서관리 / 기간별입고내역서 | `Menu507Click` | `TSobo57` | `Subu57.pas` | `Subu57.pas` | F56 | — |
| 메인 메뉴 / 내역서관리 / 기간별출고내역서 | `Menu506Click` | `TSobo56` | `Subu56.pas` | `Subu56.pas` | F55 | — |
| 메인 메뉴 / 내역서관리 / 기간별택배내역서 | `Menu509Click` | `TSobo59` | `Subu59.pas` | `Subu59.pas` | F58 | — |
| 메인 메뉴 / 내역서관리 / 일별 내역서(요약) | `Menu509_1Click` | `TSobo59_1` | `Subu59_1.pas` | `Subu59_1.pas` | F54 | — |
| 메인 메뉴 / 내역서관리 / 일별 반품내역서 | `Menu505Click` | `TSobo55` | `Subu55.pas` | `Subu55.pas` | F53 | — |
| 메인 메뉴 / 내역서관리 / 일별 입고내역서 | `Menu504Click` | `TSobo54` | `Subu54.pas` | `Subu54.pas` | F52 | — |
| 메인 메뉴 / 내역서관리 / 일별 출고내역서 | `Menu503Click` | `TSobo53` | `Subu53.pas` | `Subu53.pas` | F51 | — |

## 플로우: 등록

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 그리드 팝업 / 등록 | `Menu012Click` |  |  |  | — | popup grid: nSqry.Post |

## 플로우: 반품관리

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 메인 메뉴 / 반품관리 / 기간별 반품내역서 | `Menu805Click` | `TSobo58_1` | `Subu58_1.pas` | `./도서유통/book_kb(반품과)/Subu58_1.pas` | F75 | — |
| 메인 메뉴 / 반품관리 / 반품명세서 | `Menu801Click` | `TSobo23_1` | `Subu23_1.pas` | `./도서유통/book_kb(반품과)/Subu23_1.pas` | F71 | — |
| 메인 메뉴 / 반품관리 / 반품재고원장 | `Menu802Click` | `TSobo39_3` | `Subu39_3.pas` | `./도서유통/book_kb(반품과)/Subu39_3.pas` | F72 | — |
| 메인 메뉴 / 반품관리 / 반품재고현황 | `Menu803Click` | `TSobo39_4` | `Subu39_4.pas` | `./도서유통/book_kb(반품과)/Subu39_4.pas` | F73 | — |
| 메인 메뉴 / 반품관리 / 일자별 반품내역서 | `Menu804Click` | `TSobo55_1` | `Subu55_1.pas` | `./도서유통/book_kb(반품과)/Subu55_1.pas` | F74 | — |

## 플로우: 발송비/입금관리

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 메인 메뉴 / 발송비/입금관리 / 메세지(팝업창) | `Menu310Click` | `TSeok30` | `Seok03.pas` | `Seok03.pas` | F49 | info modal Seok80 |
| 메인 메뉴 / 발송비/입금관리 / 명세서 발송건수 | `Menu204_9Click` | `TSobo24_9` | `Subu24_9.pas` | `./도서유통/Subu24_9.pas` | F24 | — |
| 메인 메뉴 / 발송비/입금관리 / 반 품 수 거 / 반품수거내역 | `Menu306Click` | `TSobo36` | `Subu36.pas` | `./Data/Subu36.pas` | F42 | — |
| 메인 메뉴 / 발송비/입금관리 / 반 품 수 거 / 반품수거현황 | `Menu307Click` | `TSobo37` | `Subu37.pas` | `./Data/Subu37.pas` | F42 | — |
| 메인 메뉴 / 발송비/입금관리 / 발송비관리 / 발송비내역 | `Menu403Click` | `TSobo43` | `Subu43.pas` | `Subu43.pas` | F41 | — |
| 메인 메뉴 / 발송비/입금관리 / 발송비관리 / 발송비현황 | `Menu404Click` | `TSobo44` | `Subu44.pas` | `Subu44.pas` | F41 | — |
| 메인 메뉴 / 발송비/입금관리 / 세금계산서 | `Menu409Click` | `TSobo49` | `Subu49.pas` | `Subu49.pas` | F45 | info modal Seok80 |
| 메인 메뉴 / 발송비/입금관리 / 운임관리-택배 | `Menu308_1Click` | `TSobo38_1` | `Subu38_1.pas` | `Subu38_1.pas` | F29 | — |
| 메인 메뉴 / 발송비/입금관리 / 입금관리 / 입금내역 | `Menu401Click` | `TSobo41` | `Subu41.pas` | `Subu41.pas` | F46 | password modal Subu40 |
| 메인 메뉴 / 발송비/입금관리 / 입금관리 / 입금현황(1) | `Menu402Click` | `TSobo42` | `Subu42.pas` | `Subu42.pas` | F46 | password modal Subu40 |
| 메인 메뉴 / 발송비/입금관리 / 입금관리 / 입금현황(2) | `Menu402_1Click` | `TSobo42_1` | `Subu42_1.pas` | `Subu42_1.pas` | F46 | password modal Subu40 |
| 메인 메뉴 / 발송비/입금관리 / 청구금액(년월) | `Menu407Click` | `TSobo47` | `Subu47.pas` | `Subu47.pas` | F47 | password modal Subu40 |
| 메인 메뉴 / 발송비/입금관리 / 청구서관리 | `Menu405Click` | `TSobo45` | `Subu45.pas` | `Subu45.pas` | F43 | info modal Seok80 |
| 메인 메뉴 / 발송비/입금관리 / 청구서관리-택배 | `Menu405_1Click` | `TSobo45_1` | `Subu45_1.pas` | `Subu45_1.pas` | F43 | — |
| 메인 메뉴 / 발송비/입금관리 / 청구서출력 | `Menu406Click` | `TSobo46` | `Subu46.pas` | `Subu46.pas` | F44 | info modal Seok80 |
| 메인 메뉴 / 발송비/입금관리 / 출고내역서 | `Menu309Click` | `TSobo39` | `Subu39.pas` | `./도서유통/book_kb(반품과)/Subu39.pas` | F48 | — |

## 플로우: 삭제

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 그리드 팝업 / 삭제 | `Menu013Click` |  |  |  | — | popup grid: Delete key (grid row) |

## 플로우: 재고관리

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 메인 메뉴 / 재고관리 / 반품재고(반품입고)-해체 | `Menu205Click` | `TSobo25` | `Subu25.pas` | `Subu25.pas` | F36 | — |
| 메인 메뉴 / 재고관리 / 반품재고(변경) | `Menu501Click` | `TSobo51` | `Subu51.pas` | `Subu51.pas` | F35 | password modal Subu40 |
| 메인 메뉴 / 재고관리 / 반품재고(정품입고)-재생 | `Menu204Click` | `TSobo24` | `Subu24.pas` | `Subu24.pas` | F36 | — |
| 메인 메뉴 / 재고관리 / 반품재고(폐기) | `Menu305Click` | `TSobo35` | `Subu35.pas` | `./도서유통/Subu35.pas` | F37 | — |
| 메인 메뉴 / 재고관리 / 반품재고입력-자체운영 | `Menu319Click` | `TSobo39_1` | `Subu39_1.pas` | `./Data/Subu39_1.pas` | F38 | — |
| 메인 메뉴 / 재고관리 / 반품재고현황-자체운영 | `Menu329Click` | `TSobo39_2` | `Subu39_2.pas` | `./Data/Subu39_2.pas` | F39 | — |
| 메인 메뉴 / 재고관리 / 정품재고(변경) | `Menu502Click` | `TSobo52` | `Subu52.pas` | `Subu52.pas` | F35 | password modal Subu40 |
| 메인 메뉴 / 재고관리 / 정품재고(폐기) | `Menu304Click` | `TSobo34` | `Subu34.pas` | `./도서유통/Subu34.pas` | F37 | — |
| 메인 메뉴 / 재고관리 / 폐기재고(파기) | `Menu359Click` | `TSobo39_5` | `Subu39_5.pas` | `./Data/Subu39_5.pas` | F39 | — |

## 플로우: 재고원장

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 메인 메뉴 / 재고원장 / 기간별재고(세분) / 기간별재고원장(비품) | `Menu304_3Click` | `TSobo34_3` | `Subu34_3.pas` | `Subu34_3.pas` | F34 | — |
| 메인 메뉴 / 재고원장 / 기간별재고(세분) / 기간별재고원장(정품) | `Menu304_2Click` | `TSobo34_2` | `Subu34_2.pas` | `Subu34_2.pas` | F34 | — |
| 메인 메뉴 / 재고원장 / 기간별재고(세분) / 기간별재고원장(폐기) | `Menu304_4Click` | `TSobo34_4` | `Subu34_4.pas` | `Subu34_4.pas` | F34 | — |
| 메인 메뉴 / 재고원장 / 기간별재고원장 | `Menu303Click` | `TSobo33` | `Subu33.pas` | `Subu33.pas` | F32 | — |
| 메인 메뉴 / 재고원장 / 기간별평균재고 | `Menu302Click` | `TSobo32` | `Subu32.pas` | `Subu32.pas` | F33 | — |
| 메인 메뉴 / 재고원장 / 도서별수불원장 | `Menu301Click` | `TSobo31` | `Subu31.pas` | `Subu31.pas` | F31 | — |
| 메인 메뉴 / 재고원장 / 재고 및 재고금액 | `Menu304_1Click` | `TSobo34_1` | `Subu34_1.pas` | `Subu34_1.pas` | F34 | — |
| 메인 메뉴 / 재고원장 / 출판사재고현황 | `Menu302_1Click` | `TSobo32_1` | `Subu32_1.pas` | `Subu32_1.pas` | F34 | — |

## 플로우: 추가

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 그리드 팝업 / 추가 | `Menu011Click` |  |  |  | — | popup grid: nSqry.Append |

## 플로우: 출고관리

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 메인 메뉴 / 출고관리 / 거래명세서 | `Menu201Click` | `TSobo21` | `Subu21.pas` | `Subu21.pas` | F24 | — |
| 메인 메뉴 / 출고관리 / 반품명세서 | `Menu203Click` | `TSobo23` | `Subu23.pas` | `Subu23.pas` | F26 | — |
| 메인 메뉴 / 출고관리 / 신간가입고 관리 / 가입고요청서 | `Menu202_1Click` | `TSobo22_1` | `Subu22_1.pas` | `Subu22_1.pas` | F27 | — |
| 메인 메뉴 / 출고관리 / 신간가입고 관리 / 가입고현황 | `Menu202_2Click` | `TSobo22_2` | `Subu22_2.pas` | `Subu22_2.pas` | F27 | — |
| 메인 메뉴 / 출고관리 / 신간발행 | `Menu209Click` | `TSobo29` | `Subu29.pas` | `Subu29.pas` | F28 | — |
| 메인 메뉴 / 출고관리 / 입고명세서 | `Menu202Click` | `TSobo22` | `Subu22.pas` | `Subu22.pas` | F25 | — |
| 메인 메뉴 / 출고관리 / 전송자료받기(FTP) | `Menu308Click` | `TSobo38` | `Subu38.pas` | `./Data/Subu38.pas` | F29 | — |
| 메인 메뉴 / 출고관리 / 출고검증관리 | `Menu509_2Click` | `TSobo59_2` | `Subu59_2.pas` | `Subu59_2.pas` | F23 | — |
| 메인 메뉴 / 출고관리 / 출고검증관리(개별) | `Menu509_3Click` | `TSobo59_3` | `Subu59_3.pas` | `Subu59_3.pas` | F23 | — |
| 메인 메뉴 / 출고관리 / 출고접수관리 | `Menu207Click` | `TSobo27` | `Subu27.pas` | `Subu27.pas` | F21 | — |
| 메인 메뉴 / 출고관리 / 출고접수현황 | `Menu206Click` | `TSobo26` | `Subu26.pas` | `Subu26.pas` | F22 | — |
| 메인 메뉴 / 출고관리 / 출고택배관리 | `Menu208Click` | `TSobo28` | `Subu28.pas` | `Subu28.pas` | F22 | — |

## 플로우: 택배관리

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 메인 메뉴 / 택배관리 / 기타명세서 | `Menu901Click` | `TSobo91` | `Subu91.pas` | `Subu91.pas` | F21 | — |
| 메인 메뉴 / 택배관리 / 일별 출고내역서 | `Menu903Click` | `TSobo93` | `Subu93.pas` | `Subu93.pas` | F21 | — |
| 메인 메뉴 / 택배관리 / 출고내역서 | `Menu909Click` | `TSobo99` | `Subu99.pas` | `Subu99.pas` | F21 | — |
| 메인 메뉴 / 택배관리 / 출고접수관리 | `Menu907Click` | `TSobo97` | `Subu97.pas` | `Subu97.pas` | F21 | — |
| 메인 메뉴 / 택배관리 / 출고접수현황 | `Menu906Click` | `TSobo96` | `Subu96.pas` | `Subu96.pas` | F21 | — |
| 메인 메뉴 / 택배관리 / 출고택배관리 | `Menu908Click` | `TSobo98` | `Subu98.pas` | `Subu98.pas` | F21 | — |

## 플로우: 통계관리

| 메뉴 경로 | 핸들러 | 주 폼 클래스 | 유닛 | DPR `in` 경로 | `Seek_Uses` | 비고 |
|-----------|--------|-------------|------|---------------|-------------|------|
| 메인 메뉴 / 통계관리 / 거래처년말집계 | `Menu608Click` | `TSobo68` | `Subu68.pas` | `Subu68.pas` | F64 | — |
| 메인 메뉴 / 통계관리 / 거래처판매 | `Menu602Click` | `TSobo62` | `Subu62.pas` | `Subu62.pas` | F62 | — |
| 메인 메뉴 / 통계관리 / 도서별년말집계 | `Menu607Click` | `TSobo67` | `Subu67.pas` | `Subu67.pas` | F63 | — |
| 메인 메뉴 / 통계관리 / 도서별판매 | `Menu601Click` | `TSobo61` | `Subu61.pas` | `Subu61.pas` | F61 | — |
| 메인 메뉴 / 통계관리 / 출판사별판매(1) | `Menu605Click` | `TSobo65` | `Subu65.pas` | `./Data/Subu65.pas` | F65 | — |
| 메인 메뉴 / 통계관리 / 출판사별판매(2) | `Menu606Click` | `TSobo66` | `Subu66.pas` | `./Data/Subu66.pas` | F66 | — |
| 메인 메뉴 / 통계관리 / 출판사월별집계(1) | `Menu603Click` | `TSobo63` | `Subu63.pas` | `./Data/Subu63.pas` | F67 | — |
| 메인 메뉴 / 통계관리 / 출판사월별집계(2) | `Menu604Click` | `TSobo64` | `Subu64.pas` | `./Data/Subu64.pas` | F68 | — |

## 보조: 팝업 메뉴(그리드)

| 메뉴 경로 | 핸들러 | 비고 |
|-----------|--------|------|
| 그리드 팝업 / 등록 | `Menu012Click` | popup grid: nSqry.Post |
| 그리드 팝업 / 삭제 | `Menu013Click` | popup grid: Delete key (grid row) |
| 그리드 팝업 / 추가 | `Menu011Click` | popup grid: nSqry.Append |

