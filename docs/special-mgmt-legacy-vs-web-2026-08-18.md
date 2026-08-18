# 특별관리(Subu16 → /master/special) — 레거시 처리절차 재검토 vs 현행 구현 차이 (2026-08-18)

- **요청**: "특별관리 화면에 대해서 레거시 프로그램의 처리절차를 다시 검토해서 현재 구현된 방식과
  차이를 확인" + 영업팀 스크린샷 4건(기존 도서 클릭 시 추가 경로 소실 / 정가 자동계산 안 됨 /
  도서기준 패널 용도 불명 / 신규 거래처 불필요).
- **정본 소스**: 교문사 테넌트 활성 빌드 = `BLD-PUB-WAREHOUSE-WELOVE`(경로 `WeLove_FTP/도서유통-New/…chul_09(위러브)`)
  → **`WeLove_FTP/도서유통-New/Subu16.pas/.dfm`** + `Base01.pas`(TBase10 `T1_Sub61/62 BeforePost·AfterDelete`)
  + 적용처 `Subu21.pas`(거래명세서) / `Tong02.pas` `PrinRat1` / `Seek07.pas`(신간 배본).
  ⚠ 기존 매핑 노트(`analysis/layout_mappings/Sobo16.md`)는 **총판 빌드**(`도서유통-총판/Subu16.dfm`:
  비율 1개+단가) 기준으로 작성돼 "저장 컬럼 = Grat1, Gssum" 로 요약 — 출판(New) 빌드와 다름(아래 §2).

## 1. 레거시 처리절차 (New/출판 빌드)

| # | 절차 | 레거시 동작 |
|---|---|---|
| L1 | 화면 진입 | 기본 표시 패널 = **Panel005 (거래처별 특별비율 모드)**: 출판사코드(Edit307)+`검색`(dxButton1) → `G6_Ggeo WHERE Bcode='' AND Hcode` (도서 없이 **거래처별 기본 특별비율 행**) — DBGrid301 컬럼 거래처코드/거래처명/위탁/현매/매절/납품/특별/기타(Grat1~6)/**신간수량(Gssum)**. 툴바 `자료변환`(Button004) 로 두 축 모드(Panel001~004)와 토글. |
| L2 | 거래처축 조회 | Edit101(거래처코드) Enter/5자리 자동 → Seek10 조회(1건 자동확정, 다건 팝업) → `Button101`: `G6 WHERE Gcode AND Hcode ORDER BY Bcode` + Bname 보강(G4 Locate → Hcode ''→ 서버 Seek). 그리드 DBGrid101: 도서코드/도서명/**위탁·현매·매절·납품·특별·기타(Grat1~6)**/단가(Gssum). |
| L3 | 도서축 조회 | Edit201(도서코드) → Seek40 → `Button201`: `G6 WHERE Bcode AND Hcode ORDER BY Gcode`, Gname 보강(G1 Hcode → '' 폴백). DBGrid201: 거래처코드/거래처명/Grat1~6/단가. |
| L4 | 그리드 내 편집(신규 포함) | 셀 Enter 로 우측 이동, **마지막 칸(8) Enter → `Append`(새 행)** → 코드 칸 Enter → Seek40/Seek10 조회(1건 자동, 다건 팝업) → **도서명 + `Gssum := 도서 정가(Gdang)` 자동**. Delete 키 → 확인 후 `DELETE … WHERE ID`. Esc → 상단 코드 입력으로. |
| L5 | 저장 | `T1_Sub61/62BeforePost`: INSERT/UPDATE `G6_Ggeo (Hcode,Gcode,Bcode,Grat1~Grat9,Gssum)` — **비율 9종+단가 저장**, UPDATE 는 `ID AND Hcode`. |
| L6 | 부가 | `최근공급율저장하기`(Button401, 숨김 버튼): 거래처별 행에 S1_Ssub 최근 출고 비율(위탁→Grat1, 현매→Grat2, 매절→Grat3, 납품→Grat4, 특별→Grat5, 한도→Grat7, 기타→Grat6, 신간→Gssum) 채움. HTML 저장(010/011), 컬럼 설정(012/013), 인쇄(014~017), 줌, 레코드 카운터. |
| L7 | **적용(출고)** | `Subu21` 도서 확정 시: G4 정가/G1 비율(PrinZing) → **G6 (Gcode,Bcode,Hcode) 존재 시 `Grat1 := G6.Grat1`, `Gdang(단가) := G6.Gssum`** → 이어서 `Tong20.PrinRat1` 이 **판매유형별 재적용**: 위탁·신간·반품→Grat1, 현매→Grat2, 매절→Grat3, 납품→Grat4, 특별→Grat5, 한도→Grat6, 증정→0, 단가:=Gssum. |
| L8 | 적용(신간 배본) | `Seek07`(신간명세서 배본): 거래처별 비율 = `G6(Hcode,Bcode,Gcode)` → 없으면 **`G6(Hcode,'',Gcode)`(거래처별 기본행) 폴백**, 배본 수량 = 거래처별 행 `Gssum(신간수량)`; 배본 후 `UPDATE G6 SET Gssum … WHERE Bcode=''`. |

## 2. 현행 웹(/master/special, masters_service.list/create/update/delete_special_master) 와의 차이

| # | 항목 | 레거시 | 웹 현행 | 판정 |
|---|---|---|---|---|
| D1 | 비율 컬럼 | 판매유형별 **Grat1~6(+7~9 저장)** + 단가 | **Grat1(비율 1개) + Gssum(단가)** 만 목록·편집·저장 (`INSERT (Hcode,Gcode,Bcode,Grat1,Gssum)`) | **차이(기능 축소)** — 총판 빌드 기준 이식. 출판 빌드 사용자는 현매/매절/납품/특별/기타 특가를 등록·확인 불가 |
| D2 | 출고 적용 | Grat1 + **판매유형별 Grat2~6 재적용**, 단가=Gssum | `resolve_line_defaults` 3단계: G6 `Grat1`·`Gssum` 만 (pubun 무관) | **차이** — 위탁 외 판매유형 전표에 특가 위탁율이 적용됨(레거시는 해당 유형 컬럼; 값 0이면 0). D1 해소 전제 |
| D3 | 거래처별 기본행(Bcode='') 모드 | 기본 진입 화면, 신간 배본·PrinRat1 폴백에 사용 | 없음(웹 `publisher` 모드는 Hcode 전체 — DEC-155 에서 UI 제거) | **차이(미이식)** — 신간발행 배본 로직 자체가 웹 미이식이라 현재 영향은 표시/등록 불가에 한정 |
| D4 | 신규 등록 UX | 그리드 마지막 칸 Enter → 새 행, 코드 Enter → 조회·도서명·**단가=정가 자동** | 행 선택 시 신규 블록이 편집 블록으로 대체돼 **등록 경로 소실**, 단가·비율 수기 | **DEC-170 으로 수정 완료**(편집/신규 블록 분리, 단가=정가·비율=거래처 기본 위탁율 자동, 선택 해제/Esc, 등록 후 포커스 복귀) |
| D5 | 도서축 신규 거래처 등록 | 있음(DBGrid201 Append) | 있음 → 영업팀 "불필요" | DEC-170: **접힘 기본**('이 도서에 특가 거래처 추가' 버튼으로 펼침) — 코드/기능 보존 |
| D6 | 빈 결과 안내 | 레코드 카운터 0/0 | "도서를 선택하면 …" 문구가 미선택/0건 공용이라 혼동 | DEC-170: 0건 시 "○○에 등록된 특가 도서/거래처가 없습니다 — 신규 등록에서 추가" + 패널 부제(용도) |
| D7 | 삭제 | Delete 키+확인 | 선택 후 `삭제` 버튼+confirm | 동등 |
| D8 | 정렬/컬럼/엑셀 | TitleClick 정렬, 컬럼 설정, HTML 저장, 인쇄 | 정렬·컬럼 설정 있음(DEC-155 3차), **엑셀 저장/인쇄 없음** | 소차이(공통 export 정책에 따라 후속) |
| D9 | 최근공급율 저장(Button401) | 숨김 버튼(Visible=False) — 실사용 미확인 | 없음 | 미이식(레거시도 숨김) — 보류 |
| D10 | 이름 보강 폴백 | Bname/Gname: Hcode → '' 폴백 | 목록 SQL `LEFT JOIN G4_Book/G1_Ggeo ON Hcode=g.Hcode` (Hcode='' 폴백 없음) | 소차이 — 공용 마스터(Hcode='') 도서/거래처는 이름 공란 가능 → `book_meta_lookup`(DEC-169) 방식으로 폴백 가능 |

## 3. 수정안 (제안 — 결정 필요 항목 포함)

**즉시 반영(완료, DEC-170)** — D4·D5·D6 (배포됨).

**A안(권장) — 판매유형별 특가 컬럼 복원(D1+D2)** → **채택·구현 완료(DEC-171, 2026-08-18): 계정(빌드)별 프로필로 총판=single / 출판=by_pubun 데이터 분기**
1. API/모델: `SpecialListItem` 에 `grat2~grat6` 추가, `POST/PATCH` 도 동일(기존 `grat1/gssum` 호환 유지). `INSERT/UPDATE` 는 레거시처럼 Grat1~6(+7~9 는 0) 컬럼 포함.
2. 화면: 거래처축/도서축 그리드에 **위탁·현매·매절·납품·특별·기타·단가** 7컬럼(레거시 DBGrid101/201 동형), 편집·신규 블록도 7칸(기본값: 도서 정가 + 거래처 기본 비율 7종(G1 Grat1~6)).
3. 적용: `resolve_line_defaults` G6 단계에서 **전표 판매유형(pubun)별 컬럼**(위탁/신간/반품→Grat1, 현매→Grat2, 매절→Grat3, 납품→Grat4, 특별→Grat5, 한도→Grat6, 증정→0) 적용 + 단가=Gssum — 출고접수(`resolveSpecial`)도 동일 경로라 자동 반영. 컬럼 값이 0/빈값일 때 레거시는 0 을 그대로 쓰지만(주의), 웹은 **0 이면 Grat1 폴백** 여부 결정 필요.
4. 회귀 가드: 특별관리 CRUD 7컬럼 + line-defaults pubun 매핑 표 테스트.

**B안 — 현행(비율 1개) 유지 + 안내** — 화면 부제에 "비율은 모든 판매유형에 공통 적용" 명시. 출판 빌드 사용자의 현매/매절 특가는 미지원으로 남음.

**후속(별도 결정)** — D3 거래처별 기본행(Bcode='') 모드는 신간발행 배본(Seek07) 이식과 묶어서; D8 엑셀 저장은 목록 export 공통 정책; D10 이름 폴백은 소규모 개선.

## 4. 참고
- 결정 기록: DEC-155(재작성), DEC-170(이번 UX 수정). 본 문서의 A/B 안은 사용자 결정 후 DEC 로 승격.
