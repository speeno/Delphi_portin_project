# 이벤트 핸들러 · SQL 인덱스: C8 Phase 1 (바코드 스캔 → 출고/입고/반품 매칭)

_생성: 2026-04-20 — C8 T2_

> 레거시 `Tong07.pas` 의 `Button100Click` (스캔 매칭 핵심) 이 발행하는 SQL 4종을 모던 백엔드의 단일 매칭 엔드포인트 (`POST /api/v1/scan/match`) 로 흡수한다. **신규 SQL 0건** — 모두 기존 G4_Book/G1_Ggeo/G2_Ggwo 의 재해석. **DEC-004 (USB-HID 1차) / DEC-010 (C2 분리 → C8) / DEC-040 (서버 매칭 + 클라 라인 분리, 단가 폴백 Hcode='' 우선) 의 단일 운영 출처.**

## 0. Phase 1 진입 결정 요약

| 결정 ID | 내용 | 근거 |
| --- | --- | --- |
| DEC-040 | 서버 매칭 (`POST /scan/match`) + 클라이언트 라인 반영 분리. 단가 폴백 = `Hcode=''` 우선 → 라인 `Hcode` 폴백 | 레거시 Tong07.pas L126-149 / L159-184 / L192-218 동일 패턴 |
| DEC-004 | 입력 = USB-HID 키보드 웨지 1차. Web Serial / 시리얼 브리지 = OQ-002-R | 사용자 결정 (이번 세션) |
| DEC-010 | C2 출고 1차 포팅에서 Tong08 분리, 본 시나리오 (C8) 에서 통합 | 기존 |

## 1. 레거시 진입점

| dfm 이벤트 | dfm 핸들러 | Pas Line | 역할 |
| --- | --- | --- | --- |
| `ComPort.OnRxChar` (Tong08) | `ComPortRxChar` | Tong08.pas L40 | COM 시리얼 수신 → `#13` (CR) 종결 → `Sobo*.FTong07.Button104Click` 호출 |
| `Edit101.OnKeyPress` (Tong07/FTong07) | `Edit101KeyPress` | Tong07.pas L66 | 사용자 Enter 시 `Button100Click` 호출 (키보드 웨지 표준 경로) |
| `Button104.OnClick` (외부 호출용) | `Button104Click` | Tong07.pas L333 | `nForm='21'` 만 `Edit101` 채우고 Button100Click — 시리얼 진입 (출고 한정) |
| `Button100.OnClick` | `Button100Click` | Tong07.pas L78 | **매칭 핵심** — G4_Book → G1/G2_Ggeo (단가 폴백) → nSqry.Append |

## 2. SQL 카탈로그 (4종, 모두 재해석)

### SQL-SC-1 — G4_Book 도서 매칭 (Gisbn + Hcode)

- 위치: `Tong07.pas` L80-91
- 원문:

```sql
Select Gcode, Gname, Gjeja, Ocode, Gdang
  From G4_Book
 Where {D_Select} Gisbn = '@Gisbn' and Hcode = '@Hcode'
```

- 모던: `app/services/scan_match_service.py::_select_book_by_isbn(barcode, hcode, server_id)` — 단건 LIMIT 1, NODATA 시 `status=nodata` 반환 (200 OK).
- 멀티 DB: `apply_limit_offset_syntax` 적용 가능 형태 (현 단건이지만 미래 확장 대비).

### SQL-SC-2 — G1_Ggeo 출고/반품 단가 (Hcode='' 우선 → 라인 Hcode 폴백)

- 위치: `Tong07.pas` L126-149 (출고), L192-218 (반품) — 동일 패턴
- 원문 (1순위, 공통 단가):

```sql
Select Grat1, Grat2, Grat3, Grat4, Grat5, Grat6
  From G1_Ggeo
 Where {D_Select} Gcode = '@Gcode' and Hcode = ''
```

- 원문 (2순위, NODATA 시 라인 거래처 폴백):

```sql
Select Grat1, Grat2, Grat3, Grat4, Grat5, Grat6
  From G1_Ggeo
 Where {D_Select} Gcode = '@Gcode' and Hcode = '@Hcode'
```

- 모던: `app/services/pricing_service.py::resolve_grats(context, gcode, hcode, server_id)` — 1순위 → NODATA → 2순위 순서 보존. 둘 다 NODATA 면 `grats=null`.

### SQL-SC-3 — G2_Ggwo 입고 단가 (동일 폴백 패턴)

- 위치: `Tong07.pas` L159-184
- 원문: SQL-SC-2 와 동일 컬럼·동일 폴백, 테이블만 `G2_Ggwo` 로 치환.
- 모던: `pricing_service.resolve_grats` 의 `context='inbound'` 분기에서 `G2_Ggwo` 사용 (단일 함수 + 컨텍스트 분기, LSP 준수).

### SQL-SC-4 — G4_Book Grat 보강 (출고/입고/반품 공통, L254-264)

- 위치: `Tong07.pas` L254-264
- 원문:

```sql
Select Grat1, Grat2, Grat3, Grat4, Grat5, Grat6
  From G4_Book
 Where {D_Select} Gcode = '@Gcode' and Hcode = '@Hcode'
```

- 의미: G1/G2_Ggeo 매칭이 끝난 뒤 **도서 자체 단가 보정** (도서별 자체 할인율). NODATA 면 무시.
- 모던: `scan_match_service.py::_select_book_grats(bcode, hcode, server_id)` — Phase 1 비차단 (Phase 2 정밀화). `resolve_grats` 결과 위에 한번 더 덮어쓰기.

### Out-of-scope (Phase 1 비채택, 카탈로그만 등록)

- **G6_Ggeo 특별 단가** (Tong07.pas L268-289, `nForm='21'` 만): 거래처-도서별 특수 단가. Phase 2 (해당 거래처가 운영 시 활성화).
- **Tong20.PrinJing/PrinZing/PrinYing/PrinRat1**: 단가 보정 헬퍼들 — 프론트의 가격 계산 로직과 통합 시 재현 (Phase 2).
- **`nForm='23_1'` (반품 chul08 변형)**: Tong07.pas L221-252. C4 Phase 2 의 chul08 분기와 동일 흐름이므로 `context='return'` 단일로 흡수, 변형은 거래처 데이터로만 (코드 분기 없음).

## 3. 신규 엔드포인트

| Method | Path | 핸들러 | 핵심 SQL | 응답 형식 |
| --- | --- | --- | --- | --- |
| POST | `/api/v1/scan/match` | `routers/scan.py::scan_match` | SQL-SC-1 → SQL-SC-2/3 → SQL-SC-4 | JSON `{ resolved: {gcode, gname, gjeja, ocode, gdang, grats: [g1..g6]\|null}, status: matched\|nodata }` |

요청 본문:

```json
{
  "barcode": "9788972754381",
  "hcode": "1234",
  "context": "outbound",
  "server_id": "remote_138"
}
```

응답 (matched):

```json
{
  "status": "matched",
  "resolved": {
    "gcode": "001",
    "gname": "도서명",
    "gjeja": "저자",
    "ocode": "B",
    "gdang": 15000,
    "grats": [0.85, 0.80, 0.75, 0.70, 0.65, 0.60],
    "grats_source": "G1_Ggeo:hcode_empty"
  },
  "barcode": "9788972754381",
  "hcode": "1234",
  "context": "outbound"
}
```

응답 (nodata, 200 OK 유지):

```json
{
  "status": "nodata",
  "resolved": null,
  "barcode": "9788972754381",
  "hcode": "1234",
  "context": "outbound"
}
```

## 4. i18n 메시지 키

[`i18n/messages/c8.ko.json`](../../i18n/messages/c8.ko.json) 신규:

| 키 | 메시지 | 용도 |
| --- | --- | --- |
| `c8.scan.matched` | "매칭: {gname} ({gcode})" | 성공 토스트 |
| `c8.scan.nodata` | "미등록 바코드: {barcode}" | NODATA 토스트 (warning) |
| `c8.scan.duplicate` | "이미 추가된 도서입니다 (수량 확인): {gname}" | 클라이언트측 중복 감지 |
| `c8.scan.error` | "스캔 매칭 실패: {detail}" | 5xx 에러 |
| `c8.scan.placeholder` | "바코드를 스캔하거나 ISBN 입력 후 Enter" | input placeholder |
| `c8.scan.context.required` | "거래처를 먼저 선택하세요" | hcode 미설정 가드 |

## 5. 회귀 가드

- 4 server probe 매트릭스: `debug/probe_backend_all_servers.py` 의 `_routes_for(...)` 에 `scan.match` 1 그룹 추가 (멀티 DB 룰 §4).
- 신규 SQL 정적 검사: `test/test_c8_scan_phase1.py` 가 `scan_match_service.py` / `pricing_service.py` 에서 신규 INSERT/UPDATE/DELETE 0건임을 grep 으로 검증.
- DEC-028 grep: 모던 3 페이지에 `data-legacy-id="FTong07.Edit101"` ≥ 3건 부착.
