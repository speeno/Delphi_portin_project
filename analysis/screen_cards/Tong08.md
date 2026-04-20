# 화면 카드: Tong08 (TTong80) — 바코드 스캔 진입점

_생성: 2026-04-20 — C8 T1 (수동 작성, accelerator 미산출)_

## 0. 한눈 요약
- 파일(DFM): `legacy_delphi_source/legacy_source/Tong08.dfm` (TComPort + TComTerminal)
- 파일(PAS): `legacy_delphi_source/legacy_source/Tong08.pas` (62 LOC)
- 컴포넌트 수: **2** (TComTerminal × 1, TComPort × 1) / 이벤트 수: **2** (ComTerminalStrRecieved, ComPortRxChar)
- 핵심 SQL 수: **0** (자체 SQL 없음 — `Tong07.Button100Click` 으로 위임)
- 매핑 시나리오: **C8 (바코드 스캔 → 출고/입고/반품 매칭)**

## 1. UI 구성
- **TComPort** (시리얼 포트 컴포넌트) — 직접 USB 시리얼/COM 수신
- **TComTerminal** (시리얼 터미널) — 미사용 (코드 주석 처리됨, 라인 32~38)
- DFM 자체는 비가시 데이터 모듈에 가까움 (사용자 화면이 없음)

## 2. 이벤트 흐름

| event | component | handler | 설명 |
| --- | --- | --- | --- |
| StrReceived | ComTerminal | `ComTerminalStrRecieved` | **주석 처리됨** (구버전 흐름) |
| RxChar | ComPort | `ComPortRxChar` | **활성** — 바이트 버퍼 → `#13` 종결 → 분기 호출 |

### 2.1 핵심 흐름 (`ComPortRxChar`, L40~61)

```pascal
I := ComPort.Read(Buf, Count);
for J := 0 to I - 1 do begin
  if Buf[J] = #13 then begin
    if nForm='21' Then Sobo21.FTong07.Button104Click(nBarcode);
    if nForm='22' Then Sobo22.FTong07.Button104Click(nBarcode);
    if nForm='23' Then Sobo23.FTong07.Button104Click(nBarcode);
    Break;
  end;
  nBarcode := nBarcode + Buf[J];
end;
```

- **종결 문자**: `#13` (CR) — Enter 가 아닌 raw byte CR.
- **컨텍스트 분기**: 전역 변수 `nForm` ('21'/'22'/'23') 으로 출고/입고/반품 화면을 선택.
- **위임**: `Sobo*.FTong07.Button104Click(nBarcode)` 로 바코드 문자열 전달 (FTong07 = Tong07 frame instance).

### 2.2 위임 대상 (`Tong07.Button104Click` → `Button100Click`)

```pascal
// Tong07.pas L333-338
procedure TTong70.Button104Click(nBarcode: String);
begin
  if nForm='21' Then begin
    Edit101.Text := Copy(nBarcode, nLen1, nLen1);
    Button100Click(Self);
  end;
end;
```

- **주의**: `nForm='22'`/`'23'` 은 빈 분기 → 시리얼 경로로는 **출고만 자동 동작**. 입고/반품은 사용자가 `Edit101` 에 직접 입력 후 Enter (`Edit101KeyPress`) 가 필요.
- `Button100Click` 본체는 nForm 21/22/23 모두에 대해 동일 SQL 체인 (G4_Book → G1_Ggeo / G2_Ggwo) 을 갖고 있으므로, **키보드 웨지 입력 + Enter 만으로** 22/23 도 동일하게 동작.

## 3. 데이터 액세스 (SQL)
- 본 폼: **0건**
- 위임 대상 (`Tong07.Button100Click`): SQL-SC-1 (G4_Book), SQL-SC-2 (G1_Ggeo), SQL-SC-3 (G2_Ggwo) — `analysis/handlers/c8_scan.md` 참조

## 4. DB 영향
- 본 폼: 직접 영향 없음 (위임만)
- 매칭 결과는 클라이언트 그리드 (`nSqry.Append`) 에 라인 추가 — 실제 DB UPDATE/INSERT 는 호출 화면 (Sobo21/22/23) 의 저장 액션에서 발생

## 5. 검증 규칙
- (자체 검증 없음 — 매칭 NODATA 시 무음 종료)

## 6. 고객사 분기
- (없음 — 모든 거래처 공통)

## 7. 관련 OQ·GAP·DEC
- **DEC-004**: 바코드 = USB-HID 키보드 웨지 1차 (Web Serial 보류)
- **DEC-010**: C2 출고 1차 포팅에서 Tong08 제외, 별도 시나리오 (= C8) 로 분리
- **DEC-040** (예정, 본 시나리오에서 신설): 서버 매칭 + 클라이언트 라인 반영 분리, 단가 폴백 Hcode='' 우선
- **OQ-002 / OQ-002-R**: 시리얼·Web Serial·라벨 직결은 OQ-002-R 잔여

## 8. 인쇄·바코드 연관
- 정밀 조사: `docs/legacy-print-scanner-integration-survey.md`
- 결정: `docs/decision-print-scanner-web.md`

## 9. 포팅 체크리스트
- [x] `migration/contracts/barcode_scan.yaml v1.0.0` (C8 T3)
- [x] `app/services/scan_match_service.py` + `app/routers/scan.py` (C8 T5)
- [x] `frontend/src/lib/scanner.ts` (keyboard wedge buffer + CR delimiter, C8 T6)
- [x] 호출 화면 통합 (Sobo21 = outbound/orders, Sobo22 = inbound/receipts, Sobo23 = returns/receipts)
- [x] 5축 회귀 매트릭스 + 4 server probe (C8 T7)
