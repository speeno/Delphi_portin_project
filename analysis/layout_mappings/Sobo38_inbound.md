# 레이아웃 매핑: Sobo38 (전송자료받기) → 모던 사용자 파일 업로드 [C3 inbound 전용]

> **[2026-04-19 분리 안내]** 본 노트는 **C3 `/inbound/import` 전용**(Subu38 본 폼 — 빈 셸 + FTP 우회). C9 `master/book-code` 의 도서코드 마스터 변형(Subu38_1 / Subu38_2 의 T3_Sub82·DBGrid101 위젯) 매핑은 [`Sobo38.md`](Sobo38.md) 참조.

DEC-027 — 1차 포팅에서는 외부 FTP 자동수신 대신 **사용자 파일 업로드(EUC-KR CSV/TXT)** 로 우회한다. 따라서 dfm 의 FTP 위젯은 모던 컴포넌트로 옮기지 않고, 동일한 입력 데이터(입고 라인 행집합) 를 받는 단일 업로드 페이지로 대체한다.

## 0. 입력 산출물 (참고용)

- 본 폼 (사실상 빈 dfm): [`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu38/Sobo38.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu38/Sobo38.html)
- 변형: `Subu38_1/Sobo38_1.*`, `Subu38_2/Sobo38_2.*`
- 화면 카드: [`analysis/screen_cards/Sobo38.md`](../screen_cards/Sobo38.md)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu38.dfm`](../../legacy_delphi_source/legacy_source/Subu38.dfm) — `object Sobo38` 1건만(런타임 동적 위젯) — 정적 매핑 대상 없음.

> dfm 자체에 위젯이 1개만 정의되어 있어 전통적 위젯 ID 매핑 대상이 없다. 본 노트는 **데이터 흐름** 만 모던 페이지로 1:1 보존.

## 1. 모던 페이지 구조 (단일 업로드 페이지)

| 영역 | 모던 컴포넌트 | 역할 | `data-legacy-id` |
| --- | --- | --- | --- |
| 헤더 | `<h1>입고 데이터 가져오기</h1>` | 페이지 제목 | `data-legacy-id="Sobo38"` |
| 파일 선택 | `<FileInput accept=".csv,.txt">` | EUC-KR CSV/TXT 1개 선택 | `data-legacy-id="FileInputProxy"` |
| 인코딩 표시 | 안내 라벨 "EUC-KR 자동 디코딩" | DEC-024 가드 명시 | — |
| 업로드 버튼 | `<Button variant="primary">` | POST `/api/v1/inbound/import` (multipart) | `data-legacy-id="ImportProxy"` |
| 미리보기 그리드 | `<DataGrid>` | 업로드 직전 client-side 5행 미리보기 | `data-legacy-id="PreviewGrid"` |
| 결과 메시지 | `<Alert>` | 성공 N건 / 실패 사유 표시 | — |

## 2. 데이터 포맷 (서버 입력 = 입고 라인)

| 컬럼 | 타입 | 의미 | 비고 |
| --- | --- | --- | --- |
| `gdate` | `YYYY-MM-DD` 또는 `YYYYMMDD` | 거래일자 | `_normalize_gdate` 통과 |
| `hcode` | string | 출판사 코드 | G7_Ggeo lookup |
| `gcode` | string | 입고처 코드 | G1_Ggeo lookup |
| `pubun` | string | 구분 | G1_Gbun |
| `bcode` | string | 도서 코드 | G4_Book lookup |
| `gsqut` | number | 수량 | |
| `gdang` | number | 단가 | optional, 없으면 G4_Book 기본 |
| `grat1` | number | 비율 | optional |
| `gbigo` | string | 비고 | optional |

> 실패 시 라인 단위 에러 응답 (라인번호·필드·사유) — 부분 성공 허용.

## 3. 변형 차이 (`Sobo38` 본 vs `_1` vs `_2`)

본 폼은 dfm 정적 위젯이 사실상 없어, 변형 차이 = 사용처 차이(FTP 호스트·계정) 뿐. 모던 업로드 우회는 차이가 없다. (FTP 자동수신 활성화 시 OQ-IN-1 별도 결정 필요.)

## 4. 회귀 가드 체크리스트

- [ ] EUC-KR 한글 파일 업로드 시 백엔드 `_normalize_aiomysql_row` 와 동일 `errors='replace'` 정책 적용 확인.
- [ ] 부분 실패 응답이 라인번호·필드·사유 3종을 모두 포함.
- [ ] 모던 페이지 모든 위젯에 `data-legacy-id` 부착.

## 5. 참조

- DEC-027 (1차 FTP 우회), DEC-028 (dfm 산출물 영구 입력).
- OQ-IN-1: 진짜 FTP 자동수신 후속 이관.
- contract: `migration/contracts/inbound_receipt.yaml` SQL-IN-6 (IMPORT).
