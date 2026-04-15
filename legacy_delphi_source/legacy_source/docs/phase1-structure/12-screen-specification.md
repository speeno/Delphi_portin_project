# 화면 정의서 (루트 Chulpan.dpr 기준)

생성: [`debug/generate_screen_specification.py`](../../debug/generate_screen_specification.py) 재실행.

## 범위

- **기준 DPR**: [`Chulpan.dpr`](../Chulpan.dpr) `uses` 에 명시된 유닛만.
- **DFM**: 각 `.pas` 와 동일 경로의 `.dfm` (텍스트 DFM만; 이진형 DFM은 스킵).
- **메뉴 경로**: `Chul.dfm` 메뉴 + `Chul.pas` `Menu*Click`에서 **열리는 주 폼 클래스**와 매칭 (툴바/다른 경로는 미포함).
- **ShowModal**: DPR `uses`에 포함된 각 `.pas`에서 `*.ShowModal` 검색 (동일 식별자가 여러 파일에서 쓰이면 모두 나열).

## 요약

| 항목 | 개수 |
|------|------:|
| Form (추정) | 126 |
| DataModule | 1 |
| Frame | 1 |
| 텍스트 DFM 발견 | 123 |
| 총 DPR 엔트리 | 128 |

## 부팅 시 `Application.CreateForm` (로그인 이후)

| 순서 | 클래스 | 변수(인스턴스) |
|------|----------|-------------|
| 1 | `TSubu00` | `Subu00` |
| 2 | `TBase10` | `Base10` |
| 3 | `TSeak10` | `Seak10` |
| 4 | `TSeak20` | `Seak20` |
| 5 | `TSeak30` | `Seak30` |
| 6 | `TSeak40` | `Seak40` |
| 7 | `TSeak40_1` | `Seak40_1` |
| 8 | `TSeak50` | `Seak50` |
| 9 | `TSeak60` | `Seak60` |
| 10 | `TSeak70` | `Seak70` |
| 11 | `TSeak80` | `Seak80` |
| 12 | `TSeak80_1` | `Seak80_1` |
| 13 | `TSeak90` | `Seak90` |
| 14 | `TSeek10` | `Seek10` |
| 15 | `TSeek20` | `Seek20` |
| 16 | `TSeek30` | `Seek30` |
| 17 | `TSeek40` | `Seek40` |
| 18 | `TSeek50` | `Seek50` |
| 19 | `TSeek60` | `Seek60` |
| 20 | `TSeek70` | `Seek70` |
| 21 | `TSeek80` | `Seek80` |
| 22 | `TSeek90` | `Seek90` |
| 23 | `TSeok10` | `Seok10` |
| 24 | `TSeok20` | `Seok20` |
| 25 | `TSeok40` | `Seok40` |
| 26 | `TSeok80` | `Seok80` |
| 27 | `TTong20` | `Tong20` |
| 28 | `TTong30` | `Tong30` |
| 29 | `TTong40` | `Tong40` |
| 30 | `TTong60` | `Tong60` |
| 31 | `TTong80` | `Tong80` |
| 32 | `TSobo40` | `Sobo40` |
| 33 | `TSobo71` | `Sobo71` |

로그인: `Sobo10 := TSobo10.Create(Application);` 후 `ShowModal` 성공 시에만 위 `CreateForm`이 실행됩니다.

## 전체 표 (메뉴 / 모달 / 부팅 / 컴포넌트 개수)

| 인스턴스 | 폼 클래스 | 유닛 | DPR `in` | 종류 | 부팅 CreateForm | UI 역할 | DFM Caption | FormStyle | BorderStyle | ClientWxH | 메뉴 경로(일부) | ShowModal 연속 | Grid | CDS | Panel | Edit |
|-----------|----------|------|----------|------|----------------|----------|-------------|-----------|------------|---------|----------------|---------------|-----|-----|-------|------|
| `Base10` | `TBase10` | `Base01` | `Base01.pas` | DataModule | yes | non-visual DataModule | — | — | — | — | — | — | 0 | 0 | 0 | 0 |
| `Subu00` | `TSubu00` | `Chul` | `Chul.pas` | Form | yes | MDI parent | 도서물류관리프로그램 | fsMDIForm | — | — | — | — | 0 | 0 | 0 | 0 |
| `Seak10` | `TSeak10` | `Seak01` | `Seak01.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 자료찾기 | — | bsSingle | 298x153 | — | Subu17.pas: Seak10.ShowModal;; Subu15.pas: Seak10.ShowModal;; Subu12.pas: Seak10.ShowModal;; Subu11.pas: Seak10.ShowModa | 0 | 0 | 0 | 0 |
| `Seak20` | `TSeak20` | `Seak02` | `Seak02.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 자료검색 | — | bsSingle | 452x367 | — | Subu17.pas: if Seak20.ShowModal=mrOK then; Subu12.pas: if Seak20.ShowModal=mrOK then; Subu11.pas: if Seak20.ShowModal=mr | 1 | 1 | 0 | 0 |
| `Seak30` | `TSeak30` | `Seak03` | `Seak03.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 자료정렬 | — | bsSingle | 418x321 | — | Subu14.pas: Seak30.ShowModal;; Subu11.pas: Seak30.ShowModal;; Subu15.pas: Seak30.ShowModal;; Subu17.pas: Seak30.ShowModa | 0 | 0 | 0 | 0 |
| `Seak40` | `TSeak40` | `Seak04` | `Seak04.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 우편번호검색현황 | — | bsSingle | 492x303 | — | Subu11.pas: if Seak40.ShowModal=mrOK Then begin; Subu15.pas: if Seak40.ShowModal=mrOK Then begin; Subu17_1.pas: if Seak4 | 1 | 1 | 0 | 0 |
| `Seak40_1` | `TSeak40_1` | `Seak04_1` | `Seak04_1.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 우편번호검색 | fsStayOnTop | bsSingle | 772x441 | — | — | 0 | 0 | 0 | 0 |
| `Seak50` | `TSeak50` | `Seak05` | `Seak05.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 프린터출력 | — | bsSingle | 362x221 | — | Tong04.pas: Seak50.ShowModal; Seak50.PrinTing(Seen58.QuickRep1);; Tong04.pas: Seak50.ShowModal; Seak50.PrinTing(Seen57.Q | 0 | 0 | 0 | 0 |
| `Seak60` | `TSeak60` | `Seak06` | `Seak06.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 출력셋팅 | — | bsSingle | 586x533 | — | Subu21.pas: Seak60.ShowModal;; Subu22.pas: Seak60.ShowModal;; Subu23.pas: Seak60.ShowModal;; Subu91.pas: Seak60.ShowModa | 0 | 0 | 0 | 0 |
| `Seak70` | `TSeak70` | `Seak07` | `Seak07.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 거래명세서출력자료 | — | — | — | — | Subu26.pas: { if Key=VK_F7 Then Seak70.ShowModal; }; Subu23.pas: if Key=VK_F7 Then Seak70.ShowModal;; Subu21.pas: if Key | 2 | 0 | 0 | 0 |
| `Seak80` | `TSeak80` | `Seak08` | `Seak08.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 출판사검색현황 | — | bsSingle | 492x303 | — | Subu13.pas: if Seak80.ShowModal=mrOK Then begin; Subu16.pas: if Seak80.ShowModal=mrOK Then begin; Subu13_1.pas: if Seak8 | 1 | 1 | 0 | 0 |
| `Seak80_1` | `TSeak80_1` | `Seak08_1` | `./도서유통/book_kb(반품과)/Seak08_1.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 출판사검색현황 | — | bsSingle | 492x303 | — | 도서유통/book_kb(반품과)/Subu39_3.pas: if Seak80_1.ShowModal=mrOK Then begin; 도서유통/book_kb(반품과)/Subu39_4.pas: if Seak80_1.ShowM | 1 | 1 | 0 | 0 |
| `Seak90` | `TSeak90` | `Seak09` | `Seak09.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 계약내용 | fsStayOnTop | — | — | — | — | 0 | 0 | 0 | 0 |
| `Seek10` | `TSeek10` | `Seek01` | `Seek01.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 거래처검색현황 | — | bsSingle | 492x303 | — | Subu16.pas: if Seek10.ShowModal=mrOK Then begin; Subu13.pas: if Seek10.ShowModal=mrOK Then begin; Subu13_1.pas: if Seek1 | 1 | 1 | 0 | 0 |
| `Seek20` | `TSeek20` | `Seek02` | `Seek02.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 입고처검색현황 | — | bsSingle | 492x303 | — | Subu22_1.pas: if Seek20.ShowModal=mrOK Then begin; Subu22.pas: if Seek20.ShowModal=mrOK Then begin; Subu22_2.pas: if See | 1 | 1 | 0 | 0 |
| `Seek30` | `TSeek30` | `Seek03` | `Seek03.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 저자검색현황 | — | bsSingle | 492x303 | — | — | 1 | 1 | 0 | 0 |
| `Seek40` | `TSeek40` | `Seek04` | `Seek04.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 도서검색현황 | — | bsSingle | 650x303 | — | Subu16.pas: if Seek40.ShowModal=mrOK Then begin; Seek07.pas: if Seek40.ShowModal=mrOK Then begin (+77) | 1 | 1 | 0 | 0 |
| `Seek50` | `TSeek50` | `Seek05` | `Seek05.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 기타거래처검색현황 | — | bsSingle | 492x303 | — | Subu68.pas: if Seek50.ShowModal=mrOK Then begin; Subu91.pas: if Seek50.ShowModal=mrOK Then begin; Subu62.pas: if Seek50. | 1 | 1 | 0 | 0 |
| `Seek60` | `TSeek60` | `Seek06` | `Seek06.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 계정검색현황 | — | bsSingle | 492x303 | — | — | 1 | 1 | 0 | 0 |
| `Seek70` | `TSeek70` | `Seek07` | `Seek07.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 신간발행 | — | bsSingle | 614x401 | — | Subu29.pas: if Key=VK_F4 Then Seek70.ShowModal; | 1 | 1 | 0 | 0 |
| `Seek80` | `TSeek80` | `Seek08` | `Seek08.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 배본처검색현황 | — | bsSingle | 492x303 | — | — | 1 | 1 | 0 | 0 |
| `Seek90` | `TSeek90` | `Seek09` | `Seek09.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 운송비 계정코드 | — | bsSingle | 492x348 | — | — | 1 | 1 | 0 | 0 |
| `Seen11` | `TSeen11` | `Seep11` | `Seep11.pas` | Form | no | typical Form (check ShowModal vs Show in code) | — | — | — | — | — | Tong04.pas: nPrnt:='14'; Seen11.ShowModal;; Tong04.pas: nPrnt:='11'; Seen11.ShowModal;; Tong04.pas: nPrnt:='15'; Seen11. | 0 | 0 | 0 | 0 |
| `Seen13` | `TSeen13` | `Seep13` | `Seep13.pas` | Form | no | typical Form (check ShowModal vs Show in code) | — | — | — | — | — | Tong04.pas: nPrnt:='11'; Seen13.ShowModal;; Tong04.pas: nPrnt:='15'; Seen13.ShowModal;; Tong04.pas: nPrnt:='12'; Seen13. | 0 | 0 | 0 | 0 |
| `Seok10` | `TSeok10` | `Seok01` | `Seok01.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 지점관리 | — | — | 756x243 | — | Subu15.pas: Seok10.ShowModal;; Subu11.pas: Seok10.ShowModal; | 1 | 1 | 0 | 0 |
| `Seok20` | `TSeok20` | `Seok02` | `Seok02.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 거래명세서-천일 | — | bsSingle | 770x440 | — | Subu43.pas: if Seok20.ShowModal=mrOK Then begin; Data/Subu36.pas: { if Seok20.ShowModal=mrOK Then begin | 0 | 1 | 0 | 0 |
| `Seok30` | `TSeok30` | `Seok03` | `Seok03.pas` | Form | no | MDI child | 메세지(팝업창) | fsMDIChild | bsSingle | 823x597 | 메인 메뉴 / 발송비/입금관리 / 메세지(팝업창) | — | 2 | 2 | 0 | 1 |
| `Seok40` | `TSeok40` | `Seok04` | `Seok04.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 메세지 | fsStayOnTop | bsSingle | 427x499 | — | — | 0 | 0 | 0 | 0 |
| `Seok80` | `TSeok80` | `Seok08` | `Seok08.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | — | — | — | 335x243 | — | Chul.pas: Seok80.ShowModal; | 0 | 0 | 0 | 0 |
| `Seok90` | `TSeok90` | `Seok09` | `Seok09.pas` | Form | no | typical Form (check ShowModal vs Show in code) | DownLoad......... | — | bsSingle | 286x268 | — | Data/Subu38.pas: Seok90.ShowModal; | 0 | 0 | 3 | 0 |
| `Sobo10` | `TSobo10` | `Subu10` | `Subu10.pas` | Form | yes (pre-CreateForm login) | typical Form (check ShowModal vs Show in code) | 로그인 | — | bsSingle | 284x160 | — | Chul.pas: if Sobo10.ShowModal=mrOK Then begin | 0 | 0 | 0 | 0 |
| `Sobo11` | `TSobo11` | `Subu11` | `Subu11.pas` | Form | no | MDI child | 거래처관리-통합 | fsMDIChild | bsSingle | 901x566 | 메인 메뉴 / 기초관리 / 거래처관리-통합 | — | 2 | 0 | 0 | 0 |
| `Sobo12` | `TSobo12` | `Subu12` | `Subu12.pas` | Form | no | MDI child | 입고처관리 | fsMDIChild | bsSingle | 901x566 | 메인 메뉴 / 기초관리 / 입고처관리 | — | 2 | 0 | 0 | 0 |
| `Sobo13` | `TSobo13` | `Subu13` | `Subu13.pas` | Form | no | MDI child | 지역분류(시내+지방) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 기초관리 / 지역분류(시내+지방) | — | 1 | 0 | 0 | 0 |
| `Sobo13_1` | `TSobo13_1` | `Subu13_1` | `Subu13_1.pas` | Form | no | MDI child | 출고증정렬 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 기초관리 / 출고증정렬 | — | 1 | 1 | 0 | 0 |
| `Sobo14` | `TSobo14` | `Subu14` | `Subu14.pas` | Form | no | MDI child | 도서관리 | fsMDIChild | bsSingle | 901x566 | 메인 메뉴 / 기초관리 / 도서관리 | — | 2 | 0 | 0 | 0 |
| `Sobo15` | `TSobo15` | `Subu15` | `Subu15.pas` | Form | no | MDI child | 거래처관리-개별 | fsMDIChild | bsSingle | 901x566 | 메인 메뉴 / 기초관리 / 거래처관리-개별 | — | 2 | 0 | 0 | 0 |
| `Sobo16` | `TSobo16` | `Subu16` | `Subu16.pas` | Form | no | MDI child | 특별관리 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 기초관리 / 특별관리 | — | 3 | 0 | 0 | 0 |
| `Sobo17` | `TSobo17` | `Subu17` | `Subu17.pas` | Form | no | MDI child | 출판사관리 | fsMDIChild | bsSingle | 917x627 | 메인 메뉴 / 기초관리 / 출판사관리 | — | 2 | 0 | 0 | 1 |
| `Sobo17_1` | `TSobo17_1` | `Subu17_1` | `Subu17_1.pas` | Form | no | MDI child | 출판사관리-택배 | fsMDIChild | bsSingle | 917x627 | 메인 메뉴 / 기초관리 / 출판사관리-택배 | — | 2 | 2 | 0 | 1 |
| `Sobo18` | `TSobo18` | `Subu18` | `Subu18.pas` | Form | no | MDI child | 종당관리 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 기초관리 / 종당관리(도서) | — | 0 | 1 | 0 | 0 |
| `Sobo19` | `TSobo19` | `Subu19` | `Subu19.pas` | Form | no | typical Form (check ShowModal vs Show in code) | Sobo19 | — | bsSingle | 306x137 | 메인 메뉴 / 기초관리 / E&xit | Subu14.pas: Sobo19.ShowModal;; Subu12.pas: Sobo19.ShowModal;; Subu11.pas: Sobo19.ShowModal;; Subu15.pas: Sobo19.ShowModa | 0 | 0 | 0 | 0 |
| `Sobo20` | `TSobo20` | `Subu20` | `Subu20.pas` | Form | no | typical Form (check ShowModal vs Show in code) | 거래내역변경 | — | — | — | — | Subu21.pas: Sobo20.ShowModal;; Subu22.pas: Sobo20.ShowModal;; Subu23.pas: Sobo20.ShowModal;; Subu22_2.pas: Sobo20.ShowMo | 0 | 0 | 0 | 0 |
| `Sobo21` | `TSobo21` | `Subu21` | `Subu21.pas` | Form | no | MDI child | 거래명세서 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 출고관리 / 거래명세서 | — | 0 | 0 | 0 | 0 |
| `Sobo22` | `TSobo22` | `Subu22` | `Subu22.pas` | Form | no | MDI child | 입고명세서 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 출고관리 / 입고명세서 | — | 0 | 0 | 0 | 0 |
| `Sobo22_1` | `TSobo22_1` | `Subu22_1` | `Subu22_1.pas` | Form | no | MDI child | 가입고 요청서 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 출고관리 / 신간가입고 관리 / 가입고요청서 | — | 0 | 2 | 0 | 0 |
| `Sobo22_2` | `TSobo22_2` | `Subu22_2` | `Subu22_2.pas` | Form | no | MDI child | 가입고 현황 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 출고관리 / 신간가입고 관리 / 가입고현황 | — | 0 | 2 | 0 | 0 |
| `Sobo23` | `TSobo23` | `Subu23` | `Subu23.pas` | Form | no | MDI child | 반품명세서 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 출고관리 / 반품명세서 | — | 0 | 0 | 0 | 0 |
| `Sobo23_1` | `TSobo23_1` | `Subu23_1` | `./도서유통/book_kb(반품과)/Subu23_1.pas` | Form | no | MDI child | 반품명세서 | fsMDIChild | bsSingle | 989x613 | 메인 메뉴 / 반품관리 / 반품명세서 | — | 2 | 3 | 0 | 0 |
| `Sobo24` | `TSobo24` | `Subu24` | `Subu24.pas` | Form | no | MDI child | 반품재고(정품입고)-재생 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고관리 / 반품재고(정품입고)-재생 | — | 0 | 0 | 0 | 0 |
| `Sobo24_9` | `TSobo24_9` | `Subu24_9` | `./도서유통/Subu24_9.pas` | Form | no | MDI child | 거래명세서 발행건수 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 명세서 발송건수 | — | 0 | 1 | 0 | 0 |
| `Sobo25` | `TSobo25` | `Subu25` | `Subu25.pas` | Form | no | MDI child | 반품재고(반품입고)-해체 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고관리 / 반품재고(반품입고)-해체 | — | 0 | 0 | 0 | 0 |
| `Sobo26` | `TSobo26` | `Subu26` | `Subu26.pas` | Form | no | MDI child | 출고접수현황 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 출고관리 / 출고접수현황 | — | 0 | 0 | 0 | 0 |
| `Sobo27` | `TSobo27` | `Subu27` | `Subu27.pas` | Form | no | MDI child | 출고접수관리 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 출고관리 / 출고접수관리 | — | 0 | 0 | 0 | 0 |
| `Sobo28` | `TSobo28` | `Subu28` | `Subu28.pas` | Form | no | MDI child | 출고택배관리 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 출고관리 / 출고택배관리 | — | 0 | 2 | 0 | 0 |
| `Sobo29` | `TSobo29` | `Subu29` | `Subu29.pas` | Form | no | MDI child | 신간명세서 | fsMDIChild | bsSingle | 901x549 | 메인 메뉴 / 출고관리 / 신간발행 | — | 1 | 0 | 0 | 0 |
| `Sobo30` | `TSobo30` | `Subu30` | `Subu30.pas` | Form | no | MDI child | Sobo30 | fsMDIChild | bsToolWindow | 772x526 | — | — | 0 | 0 | 0 | 0 |
| `Sobo31` | `TSobo31` | `Subu31` | `Subu31.pas` | Form | no | MDI child | 도서별수불원장 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고원장 / 도서별수불원장 | — | 0 | 0 | 0 | 0 |
| `Sobo32` | `TSobo32` | `Subu32` | `Subu32.pas` | Form | no | MDI child | 기간별평균재고 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고원장 / 기간별평균재고 | — | 2 | 0 | 0 | 0 |
| `Sobo32_1` | `TSobo32_1` | `Subu32_1` | `Subu32_1.pas` | Form | no | MDI child | 출판사별 재고 현황 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고원장 / 출판사재고현황 | — | 0 | 1 | 0 | 0 |
| `Sobo33` | `TSobo33` | `Subu33` | `Subu33.pas` | Form | no | MDI child | 기간별재고원장 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고원장 / 기간별재고원장 | — | 0 | 0 | 1 | 0 |
| `Sobo34` | `TSobo34` | `Subu34` | `./도서유통/Subu34.pas` | Form | no | MDI child | 정품재고(폐기) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고관리 / 정품재고(폐기) | — | 0 | 2 | 0 | 0 |
| `Sobo34_1` | `TSobo34_1` | `Subu34_1` | `Subu34_1.pas` | Form | no | MDI child | 재고 및 재고금액 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고원장 / 재고 및 재고금액 | — | 0 | 2 | 0 | 0 |
| `Sobo34_2` | `TSobo34_2` | `Subu34_2` | `Subu34_2.pas` | Form | no | MDI child | 기간별재고원장(상세)-정품 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고원장 / 기간별재고(세분) / 기간별재고원장(정품) | — | 0 | 2 | 0 | 0 |
| `Sobo34_3` | `TSobo34_3` | `Subu34_3` | `Subu34_3.pas` | Form | no | MDI child | 기간별재고원장(상세)-비품 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고원장 / 기간별재고(세분) / 기간별재고원장(비품) | — | 0 | 2 | 0 | 0 |
| `Sobo34_4` | `TSobo34_4` | `Subu34_4` | `Subu34_4.pas` | Form | no | MDI child | 기간별재고원장(상세)-폐기 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고원장 / 기간별재고(세분) / 기간별재고원장(폐기) | — | 0 | 2 | 0 | 0 |
| `Sobo35` | `TSobo35` | `Subu35` | `./도서유통/Subu35.pas` | Form | no | MDI child | 반품재고(폐기) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고관리 / 반품재고(폐기) | — | 0 | 2 | 0 | 0 |
| `Sobo36` | `TSobo36` | `Subu36` | `./Data/Subu36.pas` | Form | no | MDI child | 반품수거내역 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 반 품 수 거 / 반품수거내역 | — | 0 | 2 | 0 | 0 |
| `Sobo37` | `TSobo37` | `Subu37` | `./Data/Subu37.pas` | Form | no | MDI child | 반품수거현황 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 반 품 수 거 / 반품수거현황 | — | 0 | 2 | 0 | 0 |
| `Sobo38` | `TSobo38` | `Subu38` | `./Data/Subu38.pas` | Form | no | MDI child | 전송자료받기 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 출고관리 / 전송자료받기(FTP) | — | 0 | 3 | 0 | 0 |
| `Sobo38_1` | `TSobo38_1` | `Subu38_1` | `Subu38_1.pas` | Form | no | MDI child | 운임관리-택배 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 운임관리-택배 | — | 0 | 1 | 0 | 0 |
| `Sobo39` | `TSobo39` | `Subu39` | `./도서유통/book_kb(반품과)/Subu39.pas` | Form | no | MDI child | 출고내역서 | fsMDIChild | bsSingle | 997x606 | 메인 메뉴 / 발송비/입금관리 / 출고내역서 | — | 0 | 3 | 0 | 0 |
| `Sobo39_1` | `TSobo39_1` | `Subu39_1` | `./Data/Subu39_1.pas` | Form | no | MDI child | 반품재고처리 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고관리 / 반품재고입력-자체운영 | — | 0 | 1 | 0 | 0 |
| `Sobo39_2` | `TSobo39_2` | `Subu39_2` | `./Data/Subu39_2.pas` | Form | no | MDI child | 반품재고현황 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고관리 / 반품재고현황-자체운영 | — | 0 | 1 | 0 | 0 |
| `Sobo39_3` | `TSobo39_3` | `Subu39_3` | `./도서유통/book_kb(반품과)/Subu39_3.pas` | Form | no | MDI child | 반품재고원장 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 반품관리 / 반품재고원장 | — | 0 | 1 | 0 | 0 |
| `Sobo39_4` | `TSobo39_4` | `Subu39_4` | `./도서유통/book_kb(반품과)/Subu39_4.pas` | Form | no | MDI child | 반품재고현황 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 반품관리 / 반품재고현황 | — | 0 | 1 | 0 | 0 |
| `Sobo39_5` | `TSobo39_5` | `Subu39_5` | `./Data/Subu39_5.pas` | Form | no | MDI child | 폐기재고(파기) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고관리 / 폐기재고(파기) | — | 0 | 1 | 0 | 0 |
| `Sobo40` | `TSobo40` | `Subu40` | `Subu40.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | — | — | — | — | — | Chul.pas: if Sobo40.ShowModal=mrOK Then; Chul.pas: if Sobo40.ShowModal=mrOK Then begin (+6) | 0 | 0 | 0 | 0 |
| `Sobo41` | `TSobo41` | `Subu41` | `Subu41.pas` | Form | no | MDI child | 입금내역 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 입금관리 / 입금내역 | — | 0 | 0 | 0 | 0 |
| `Sobo42` | `TSobo42` | `Subu42` | `Subu42.pas` | Form | no | MDI child | 입금현황(1) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 입금관리 / 입금현황(1) | — | 0 | 0 | 0 | 0 |
| `Sobo42_1` | `TSobo42_1` | `Subu42_1` | `Subu42_1.pas` | Form | no | MDI child | 입금현황(2) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 입금관리 / 입금현황(2) | — | 0 | 1 | 0 | 0 |
| `Sobo43` | `TSobo43` | `Subu43` | `Subu43.pas` | Form | no | MDI child | 발송비내역 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 발송비관리 / 발송비내역 | — | 0 | 0 | 0 | 0 |
| `Sobo44` | `TSobo44` | `Subu44` | `Subu44.pas` | Form | no | MDI child | 발송비현황 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 발송비관리 / 발송비현황 | — | 0 | 0 | 0 | 0 |
| `Sobo45` | `TSobo45` | `Subu45` | `Subu45.pas` | Form | no | MDI child | 청구서관리 | fsMDIChild | bsSingle | 995x627 | 메인 메뉴 / 발송비/입금관리 / 청구서관리 | — | 0 | 0 | 0 | 0 |
| `Sobo45_1` | `TSobo45_1` | `Subu45_1` | `Subu45_1.pas` | Form | no | MDI child | 청구서관리-택배 | fsMDIChild | bsSingle | 995x627 | 메인 메뉴 / 발송비/입금관리 / 청구서관리-택배 | — | 0 | 2 | 0 | 0 |
| `Sobo46` | `TSobo46` | `Subu46` | `Subu46.pas` | Form | no | MDI child | 청구서출력 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 발송비/입금관리 / 청구서출력 | — | 0 | 2 | 0 | 0 |
| `Sobo47` | `TSobo47` | `Subu47` | `Subu47.pas` | Form | no | MDI child | 청구금액(년월) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 청구금액(년월) | — | 0 | 0 | 0 | 0 |
| `Sobo48` | `TSobo48` | `Subu48` | `Subu48.pas` | Form | no | MDI child | 출판사관리(설정) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 기초관리 / 출판사관리(설정) | — | 0 | 1 | 0 | 0 |
| `Sobo49` | `TSobo49` | `Subu49` | `Subu49.pas` | Form | no | MDI child | 세금계산서발행 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 발송비/입금관리 / 세금계산서 | — | 0 | 2 | 0 | 0 |
| `Sobo50` | `TSobo50` | `Subu50` | `Subu50.pas` | Form | no | typical Form (check ShowModal vs Show in code) | Sobo50 | — | — | — | — | — | 0 | 0 | 0 | 0 |
| `Sobo51` | `TSobo51` | `Subu51` | `Subu51.pas` | Form | no | MDI child | 반품재고(변경) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고관리 / 반품재고(변경) | — | 0 | 0 | 0 | 0 |
| `Sobo52` | `TSobo52` | `Subu52` | `Subu52.pas` | Form | no | MDI child | 정품재고(변경) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 재고관리 / 정품재고(변경) | — | 0 | 0 | 0 | 0 |
| `Sobo53` | `TSobo53` | `Subu53` | `Subu53.pas` | Form | no | MDI child | 일별 출고내역서 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 내역서관리 / 일별 출고내역서 | — | 0 | 0 | 0 | 0 |
| `Sobo54` | `TSobo54` | `Subu54` | `Subu54.pas` | Form | no | MDI child | 일별 입고내역서 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 내역서관리 / 일별 입고내역서 | — | 0 | 0 | 0 | 0 |
| `Sobo55` | `TSobo55` | `Subu55` | `Subu55.pas` | Form | no | MDI child | 일별 반품내역서 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 내역서관리 / 일별 반품내역서 | — | 0 | 0 | 0 | 0 |
| `Sobo55_1` | `TSobo55_1` | `Subu55_1` | `./도서유통/book_kb(반품과)/Subu55_1.pas` | Form | no | MDI child | 일자별 반품내역서 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 반품관리 / 일자별 반품내역서 | — | 0 | 2 | 0 | 0 |
| `Sobo56` | `TSobo56` | `Subu56` | `Subu56.pas` | Form | no | MDI child | 기간별출고내역서 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 내역서관리 / 기간별출고내역서 | — | 0 | 0 | 0 | 0 |
| `Sobo57` | `TSobo57` | `Subu57` | `Subu57.pas` | Form | no | MDI child | 기간별입고내역서 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 내역서관리 / 기간별입고내역서 | — | 0 | 0 | 0 | 0 |
| `Sobo58` | `TSobo58` | `Subu58` | `Subu58.pas` | Form | no | MDI child | 기간별반품내역서 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 내역서관리 / 기간별반품내역서 | — | 0 | 0 | 0 | 0 |
| `Sobo58_1` | `TSobo58_1` | `Subu58_1` | `./도서유통/book_kb(반품과)/Subu58_1.pas` | Form | no | MDI child | 기간별 반품내역서 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 반품관리 / 기간별 반품내역서 | — | 0 | 2 | 0 | 0 |
| `Sobo59` | `TSobo59` | `Subu59` | `Subu59.pas` | Form | no | MDI child | 기간별택배내역서 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 내역서관리 / 기간별택배내역서 | — | 0 | 2 | 0 | 0 |
| `Sobo59_1` | `TSobo59_1` | `Subu59_1` | `Subu59_1.pas` | Form | no | MDI child | 일별 내역서(요약) | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 내역서관리 / 일별 내역서(요약) | — | 0 | 0 | 0 | 0 |
| `Sobo59_2` | `TSobo59_2` | `Subu59_2` | `Subu59_2.pas` | Form | no | MDI child | 출고 검증관리 | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 출고관리 / 출고검증관리 | — | 0 | 4 | 0 | 0 |
| `Sobo59_3` | `TSobo59_3` | `Subu59_3` | `Subu59_3.pas` | Form | no | MDI child | 출고 검증관리(개별) | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 출고관리 / 출고검증관리(개별) | — | 0 | 4 | 0 | 0 |
| `Sobo60` | `TSobo60` | `Subu60` | `Subu60.pas` | Form | no | typical Form (check ShowModal vs Show in code) | Sobo60 | — | — | — | — | — | 0 | 0 | 0 | 0 |
| `Sobo61` | `TSobo61` | `Subu61` | `Subu61.pas` | Form | no | MDI child | 도서별판매 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 통계관리 / 도서별판매 | — | 0 | 0 | 0 | 0 |
| `Sobo62` | `TSobo62` | `Subu62` | `Subu62.pas` | Form | no | MDI child | 거래처판매 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 통계관리 / 거래처판매 | — | 0 | 0 | 0 | 0 |
| `Sobo63` | `TSobo63` | `Subu63` | `./Data/Subu63.pas` | Form | no | MDI child | 출판사월별집계(1) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 통계관리 / 출판사월별집계(1) | — | 0 | 1 | 0 | 0 |
| `Sobo64` | `TSobo64` | `Subu64` | `./Data/Subu64.pas` | Form | no | MDI child | 출판사월별집계(2) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 통계관리 / 출판사월별집계(2) | — | 0 | 1 | 0 | 0 |
| `Sobo65` | `TSobo65` | `Subu65` | `./Data/Subu65.pas` | Form | no | MDI child | 출판사별판매(1) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 통계관리 / 출판사별판매(1) | — | 0 | 0 | 0 | 0 |
| `Sobo66` | `TSobo66` | `Subu66` | `./Data/Subu66.pas` | Form | no | MDI child | 출판사별판매(2) | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 통계관리 / 출판사별판매(2) | — | 0 | 0 | 0 | 0 |
| `Sobo67` | `TSobo67` | `Subu67` | `Subu67.pas` | Form | no | MDI child | 도서별년말집계 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 통계관리 / 도서별년말집계 | — | 0 | 0 | 0 | 0 |
| `Sobo68` | `TSobo68` | `Subu68` | `Subu68.pas` | Form | no | MDI child | 거래처년말집계 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 통계관리 / 거래처년말집계 | — | 0 | 0 | 0 | 0 |
| `Sobo69` | `TSobo69` | `Subu69` | `Subu69.pas` | Form | no | typical Form (check ShowModal vs Show in code) | Sobo69 | — | bsSingle | 772x533 | — | — | 0 | 0 | 0 | 0 |
| `Sobo71` | `TSobo71` | `Subu71` | `Subu71.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | — | fsStayOnTop | bsSingle | 194x448 | — | — | 1 | 0 | 0 | 0 |
| `Sobo91` | `TSobo91` | `Subu91` | `Subu91.pas` | Form | no | MDI child | 기타명세서 | fsMDIChild | bsSingle | 901x533 | 메인 메뉴 / 택배관리 / 기타명세서 | — | 0 | 3 | 0 | 0 |
| `Sobo93` | `TSobo93` | `Subu93` | `Subu93.pas` | Form | no | MDI child | 일별 출고내역서-(택배) | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 택배관리 / 일별 출고내역서 | — | 0 | 2 | 0 | 0 |
| `Sobo96` | `TSobo96` | `Subu96` | `Subu96.pas` | Form | no | MDI child | 출고접수현황-(택배) | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 택배관리 / 출고접수현황 | — | 0 | 3 | 0 | 0 |
| `Sobo97` | `TSobo97` | `Subu97` | `Subu97.pas` | Form | no | MDI child | 출고접수관리-(택배) | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 택배관리 / 출고접수관리 | — | 0 | 3 | 0 | 0 |
| `Sobo98` | `TSobo98` | `Subu98` | `Subu98.pas` | Form | no | MDI child | 출고택배관리-(택배) | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 택배관리 / 출고택배관리 | — | 0 | 2 | 0 | 0 |
| `Sobo99` | `TSobo99` | `Subu99` | `Subu99.pas` | Form | no | MDI child | 출고내역서-(택배) | fsMDIChild | bsSingle | 964x606 | 메인 메뉴 / 택배관리 / 출고내역서 | — | 0 | 3 | 0 | 0 |
| `Tong10` | `Tong10` | `Tong01` | `Tong01.pas` | Form | no | typical Form (check ShowModal vs Show in code) | — | — | — | — | — | Base01.pas: Tong10.ShowModal; (+18) | 0 | 0 | 0 | 0 |
| `Tong20` | `Tong20` | `Tong02` | `Tong02.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | — | — | — | — | — | Tong04.pas: { if Tong20.ShowModal=mrOK Then begin | 0 | 0 | 0 | 0 |
| `Tong30` | `TTong30` | `Tong03` | `Tong03.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | 특수문자 | — | — | — | — | — | 0 | 0 | 0 | 0 |
| `Tong40` | `TTong40` | `Tong04` | `Tong04.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | Tong40 | — | bsSingle | 292x36 | — | — | 0 | 0 | 0 | 0 |
| `Tong50` | `TTong50` | `Tong05` | `Tong05.pas` | Form | no | typical Form (check ShowModal vs Show in code) | 메일전송 | — | — | — | — | Seak07.pas: Tong50.ShowModal; | 0 | 0 | 5 | 3 |
| `Tong60` | `TTong60` | `Tong06` | `Tong06.pas` | Form | yes | typical Form (check ShowModal vs Show in code) | Tong60 | — | — | — | — | — | 0 | 0 | 0 | 0 |
| `Tong70` | `Tong70` | `Tong07` | `Tong07.pas` | Frame | no | embeddable Frame | — | — | — | — | — | — | 0 | 0 | 0 | 0 |

## CSV

동일 내용을 스프레드시트용으로: [12-screen-specification.csv](12-screen-specification.csv) (UTF-8 BOM).

## 관련 문서

- [11-screen-business-flows.md](11-screen-business-flows.md) 메뉴 플로우 상세
- [06-forms-runtime-graph.md](06-forms-runtime-graph.md)
