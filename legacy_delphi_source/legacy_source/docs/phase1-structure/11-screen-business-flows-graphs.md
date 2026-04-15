# 비즈니스 플로우 다이어그램 (Mermaid)

메인/팝업 메뉴에서 `Menu*Click`으로 열리는 화면을 **Subu00(MDI)**에서 연결한 그래프입니다. 툴바나 `nForm` 단추 경로는 포함되지 않습니다.

관련: [11-screen-business-flows.md](11-screen-business-flows.md) (표 버전).

## 기초관리

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_0 ["기초관리"]
    n_0_0["Subu19 - E&xit - TSobo19 (F19)"]
    n_0_1["Subu15 - 거래처관리-개별 - TSobo15 (F13)"]
    n_0_2["Subu11 - 거래처관리-통합 - TSobo11 (F13)"]
    n_0_3["Subu14 - 도서관리 - TSobo14 (F14)"]
    n_0_4["Subu12 - 입고처관리 - TSobo12 (F12)"]
    n_0_5["Subu18 - 종당관리(도서) - TSobo18 (F15)"]
    n_0_6["Subu13 - 지역분류(시내+지방) - TSobo13 (F17)"]
    n_0_7["Subu13_1 - 출고증정렬 - TSobo13_1 (F17)"]
    n_0_8["Subu17 - 출판사관리 - TSobo17 (F11)"]
    n_0_9["Subu48 - 출판사관리(설정) - TSobo48 (F11)"]
    n_0_10["Subu17_1 - 출판사관리-택배 - TSobo17_1 (F11)"]
    n_0_11["Subu16 - 특별관리 - TSobo16 (F16)"]
    n_0_12["Subu10 - 환경설정 - TSobo10 (F18)"]
  end
  root00 -->|F19| n_0_0
  root00 -->|F13| n_0_1
  root00 -->|F13| n_0_2
  root00 -->|F14| n_0_3
  root00 -->|F12| n_0_4
  root00 -->|F15| n_0_5
  root00 -->|F17| n_0_6
  root00 -->|F17| n_0_7
  root00 -->|F11| n_0_8
  root00 -->|F11| n_0_9
  root00 -->|F11| n_0_10
  root00 -->|F16| n_0_11
  root00 -->|F18| n_0_12
```

## 내역서관리

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_1 ["내역서관리"]
    n_1_0["Subu58 - 기간별반품내역서 - TSobo58 (F57)"]
    n_1_1["Subu57 - 기간별입고내역서 - TSobo57 (F56)"]
    n_1_2["Subu56 - 기간별출고내역서 - TSobo56 (F55)"]
    n_1_3["Subu59 - 기간별택배내역서 - TSobo59 (F58)"]
    n_1_4["Subu59_1 - 일별 내역서(요약) - TSobo59_1 (F54)"]
    n_1_5["Subu55 - 일별 반품내역서 - TSobo55 (F53)"]
    n_1_6["Subu54 - 일별 입고내역서 - TSobo54 (F52)"]
    n_1_7["Subu53 - 일별 출고내역서 - TSobo53 (F51)"]
  end
  root00 -->|F57| n_1_0
  root00 -->|F56| n_1_1
  root00 -->|F55| n_1_2
  root00 -->|F58| n_1_3
  root00 -->|F54| n_1_4
  root00 -->|F53| n_1_5
  root00 -->|F52| n_1_6
  root00 -->|F51| n_1_7
```

## 등록

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_2 ["등록"]
    n_2_0["등록 - `Menu012Click`"]
  end
  root00 --> n_2_0
```

## 반품관리

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_3 ["반품관리"]
    n_3_0["Subu58_1 - 기간별 반품내역서 - TSobo58_1 (F75)"]
    n_3_1["Subu23_1 - 반품명세서 - TSobo23_1 (F71)"]
    n_3_2["Subu39_3 - 반품재고원장 - TSobo39_3 (F72)"]
    n_3_3["Subu39_4 - 반품재고현황 - TSobo39_4 (F73)"]
    n_3_4["Subu55_1 - 일자별 반품내역서 - TSobo55_1 (F74)"]
  end
  root00 -->|F75| n_3_0
  root00 -->|F71| n_3_1
  root00 -->|F72| n_3_2
  root00 -->|F73| n_3_3
  root00 -->|F74| n_3_4
```

## 발송비/입금관리

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_4 ["발송비/입금관리"]
    n_4_0["Seok03 - 메세지(팝업창) - TSeok30 (F49)"]
    n_4_1["Subu24_9 - 명세서 발송건수 - TSobo24_9 (F24)"]
    n_4_2["Subu36 - 반품수거내역 - TSobo36 (F42)"]
    n_4_3["Subu37 - 반품수거현황 - TSobo37 (F42)"]
    n_4_4["Subu43 - 발송비내역 - TSobo43 (F41)"]
    n_4_5["Subu44 - 발송비현황 - TSobo44 (F41)"]
    n_4_6["Subu49 - 세금계산서 - TSobo49 (F45)"]
    n_4_7["Subu38_1 - 운임관리-택배 - TSobo38_1 (F29)"]
    n_4_8["Subu41 - 입금내역 - TSobo41 (F46)"]
    n_4_9["Subu42 - 입금현황(1) - TSobo42 (F46)"]
    n_4_10["Subu42_1 - 입금현황(2) - TSobo42_1 (F46)"]
    n_4_11["Subu47 - 청구금액(년월) - TSobo47 (F47)"]
    n_4_12["Subu45 - 청구서관리 - TSobo45 (F43)"]
    n_4_13["Subu45_1 - 청구서관리-택배 - TSobo45_1 (F43)"]
    n_4_14["Subu46 - 청구서출력 - TSobo46 (F44)"]
    n_4_15["Subu39 - 출고내역서 - TSobo39 (F48)"]
  end
  root00 -->|F49| n_4_0
  root00 -->|F24| n_4_1
  root00 -->|F42| n_4_2
  root00 -->|F42| n_4_3
  root00 -->|F41| n_4_4
  root00 -->|F41| n_4_5
  root00 -->|F45| n_4_6
  root00 -->|F29| n_4_7
  root00 -->|F46| n_4_8
  root00 -->|F46| n_4_9
  root00 -->|F46| n_4_10
  root00 -->|F47| n_4_11
  root00 -->|F43| n_4_12
  root00 -->|F43| n_4_13
  root00 -->|F44| n_4_14
  root00 -->|F48| n_4_15
```

## 삭제

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_5 ["삭제"]
    n_5_0["삭제 - `Menu013Click`"]
  end
  root00 --> n_5_0
```

## 재고관리

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_6 ["재고관리"]
    n_6_0["Subu25 - 반품재고(반품입고)-해체 - TSobo25 (F36)"]
    n_6_1["Subu51 - 반품재고(변경) - TSobo51 (F35)"]
    n_6_2["Subu24 - 반품재고(정품입고)-재생 - TSobo24 (F36)"]
    n_6_3["Subu35 - 반품재고(폐기) - TSobo35 (F37)"]
    n_6_4["Subu39_1 - 반품재고입력-자체운영 - TSobo39_1 (F38)"]
    n_6_5["Subu39_2 - 반품재고현황-자체운영 - TSobo39_2 (F39)"]
    n_6_6["Subu52 - 정품재고(변경) - TSobo52 (F35)"]
    n_6_7["Subu34 - 정품재고(폐기) - TSobo34 (F37)"]
    n_6_8["Subu39_5 - 폐기재고(파기) - TSobo39_5 (F39)"]
  end
  root00 -->|F36| n_6_0
  root00 -->|F35| n_6_1
  root00 -->|F36| n_6_2
  root00 -->|F37| n_6_3
  root00 -->|F38| n_6_4
  root00 -->|F39| n_6_5
  root00 -->|F35| n_6_6
  root00 -->|F37| n_6_7
  root00 -->|F39| n_6_8
```

## 재고원장

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_7 ["재고원장"]
    n_7_0["Subu34_3 - 기간별재고원장(비품) - TSobo34_3 (F34)"]
    n_7_1["Subu34_2 - 기간별재고원장(정품) - TSobo34_2 (F34)"]
    n_7_2["Subu34_4 - 기간별재고원장(폐기) - TSobo34_4 (F34)"]
    n_7_3["Subu33 - 기간별재고원장 - TSobo33 (F32)"]
    n_7_4["Subu32 - 기간별평균재고 - TSobo32 (F33)"]
    n_7_5["Subu31 - 도서별수불원장 - TSobo31 (F31)"]
    n_7_6["Subu34_1 - 재고 및 재고금액 - TSobo34_1 (F34)"]
    n_7_7["Subu32_1 - 출판사재고현황 - TSobo32_1 (F34)"]
  end
  root00 -->|F34| n_7_0
  root00 -->|F34| n_7_1
  root00 -->|F34| n_7_2
  root00 -->|F32| n_7_3
  root00 -->|F33| n_7_4
  root00 -->|F31| n_7_5
  root00 -->|F34| n_7_6
  root00 -->|F34| n_7_7
```

## 추가

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_8 ["추가"]
    n_8_0["추가 - `Menu011Click`"]
  end
  root00 --> n_8_0
```

## 출고관리

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_9 ["출고관리"]
    n_9_0["Subu21 - 거래명세서 - TSobo21 (F24)"]
    n_9_1["Subu23 - 반품명세서 - TSobo23 (F26)"]
    n_9_2["Subu22_1 - 가입고요청서 - TSobo22_1 (F27)"]
    n_9_3["Subu22_2 - 가입고현황 - TSobo22_2 (F27)"]
    n_9_4["Subu29 - 신간발행 - TSobo29 (F28)"]
    n_9_5["Subu22 - 입고명세서 - TSobo22 (F25)"]
    n_9_6["Subu38 - 전송자료받기(FTP) - TSobo38 (F29)"]
    n_9_7["Subu59_2 - 출고검증관리 - TSobo59_2 (F23)"]
    n_9_8["Subu59_3 - 출고검증관리(개별) - TSobo59_3 (F23)"]
    n_9_9["Subu27 - 출고접수관리 - TSobo27 (F21)"]
    n_9_10["Subu26 - 출고접수현황 - TSobo26 (F22)"]
    n_9_11["Subu28 - 출고택배관리 - TSobo28 (F22)"]
  end
  root00 -->|F24| n_9_0
  root00 -->|F26| n_9_1
  root00 -->|F27| n_9_2
  root00 -->|F27| n_9_3
  root00 -->|F28| n_9_4
  root00 -->|F25| n_9_5
  root00 -->|F29| n_9_6
  root00 -->|F23| n_9_7
  root00 -->|F23| n_9_8
  root00 -->|F21| n_9_9
  root00 -->|F22| n_9_10
  root00 -->|F22| n_9_11
```

## 택배관리

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_10 ["택배관리"]
    n_10_0["Subu91 - 기타명세서 - TSobo91 (F21)"]
    n_10_1["Subu93 - 일별 출고내역서 - TSobo93 (F21)"]
    n_10_2["Subu99 - 출고내역서 - TSobo99 (F21)"]
    n_10_3["Subu97 - 출고접수관리 - TSobo97 (F21)"]
    n_10_4["Subu96 - 출고접수현황 - TSobo96 (F21)"]
    n_10_5["Subu98 - 출고택배관리 - TSobo98 (F21)"]
  end
  root00 -->|F21| n_10_0
  root00 -->|F21| n_10_1
  root00 -->|F21| n_10_2
  root00 -->|F21| n_10_3
  root00 -->|F21| n_10_4
  root00 -->|F21| n_10_5
```

## 통계관리

```mermaid
flowchart TB
  root00["Subu00 MDI"]
  subgraph sg_11 ["통계관리"]
    n_11_0["Subu68 - 거래처년말집계 - TSobo68 (F64)"]
    n_11_1["Subu62 - 거래처판매 - TSobo62 (F62)"]
    n_11_2["Subu67 - 도서별년말집계 - TSobo67 (F63)"]
    n_11_3["Subu61 - 도서별판매 - TSobo61 (F61)"]
    n_11_4["Subu65 - 출판사별판매(1) - TSobo65 (F65)"]
    n_11_5["Subu66 - 출판사별판매(2) - TSobo66 (F66)"]
    n_11_6["Subu63 - 출판사월별집계(1) - TSobo63 (F67)"]
    n_11_7["Subu64 - 출판사월별집계(2) - TSobo64 (F68)"]
  end
  root00 -->|F64| n_11_0
  root00 -->|F62| n_11_1
  root00 -->|F63| n_11_2
  root00 -->|F61| n_11_3
  root00 -->|F65| n_11_4
  root00 -->|F66| n_11_5
  root00 -->|F67| n_11_6
  root00 -->|F68| n_11_7
```

