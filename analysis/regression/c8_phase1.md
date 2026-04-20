# C8 Phase 1 — 회귀 매트릭스 (T7)

본 노트는 C8 Phase 1 (바코드 스캔 매칭 — Sobo21/22/23 의 FTong07 통합) 의 **회귀 가드 5축**을 단일 표로 모은다. 모든 항목은 PR 단계에서 **반드시** 통과해야 한다.

## 1. 5축 매트릭스

| 축 | 명령 | 통과 기준 | 본 페이즈 추가 |
| --- | --- | --- | --- |
| **axis_test** | `cd /Users/speeno/Delphi_porting && python3 -m unittest test.test_c8_scan_phase1 -v` | 22/22 PASSED (skip 0) | T4 신규 22 케이스 |
| **axis_type** | `cd 도서물류관리프로그램/frontend && npx tsc --noEmit` | 0 error | T6 신규 `lib/scanner.ts` + `lib/scan-api.ts` + `components/shared/scan-input.tsx` |
| **axis_lint** | `cd 도서물류관리프로그램/frontend && npx eslint src/lib/scanner.ts src/lib/scan-api.ts src/components/shared/scan-input.tsx 'src/app/(app)/outbound/orders/[orderKey]/page.tsx' 'src/app/(app)/inbound/receipts/[receiptKey]/page.tsx' 'src/app/(app)/returns/receipts/[returnKey]/page.tsx'` | 0 error | T6 신규/통합 |
| **axis_data** | `python3 debug/probe_backend_all_servers.py` (dry-run) → `scan.match` 1 그룹 출현, 4 server 모두 | 4 행 출력 + (선택) live `RUN_DB_SMOKE=1` 시 200/400/422/503 만 통과 | T7 신규 |
| **axis_doc** | `grep -l "DEC-040" analysis/layout_mappings/c8_scan_match.md analysis/handlers/c8_scan.md analysis/screen_cards/Tong08.md migration/contracts/barcode_scan.yaml i18n/messages/c8.ko.json` | 5 파일 모두 매칭 | T1/T2/T3 노트·계약 |

## 2. DEC-028 grep — `data-legacy-id` 누락 0건

C8 Phase 1 의 핵심 위젯은 단일 공통 컴포넌트 `components/shared/scan-input.tsx` 에 통합된다 (단일 책임 원칙 — SRP). 따라서 DEC-028 검사는 **공통 컴포넌트 1건 + 통합 페이지 3건** 으로 분리한다.

### 2.1. 공통 컴포넌트 (필수 부착)

| 컴포넌트 | legacy_id | 비고 |
| --- | --- | --- |
| `components/shared/scan-input.tsx` `<input>` | `FTong07.Edit101` | 레거시 Tong07.pas L78 Button100Click 의 Edit101.Text 모던 등가 |
| `components/shared/scan-input.tsx` 토스트 영역 | `FTong07.Body_Data` | 레거시 nMsg.Body_Data ('NODATA' 등) 출력 위치 |

### 2.2. 통합 페이지 (ScanInput 임포트 필수)

| 페이지 | context | hcode 출처 | 통합 모드 |
| --- | --- | --- | --- |
| `outbound/orders/[orderKey]/page.tsx` | `outbound` | `detail.customer.hcode` | 항상 (취소 상태 제외) |
| `inbound/receipts/[receiptKey]/page.tsx` | `inbound` | `detail.publisher.hcode` | `editing` true 일 때만 |
| `returns/receipts/[returnKey]/page.tsx` | `return` | `key.hcode` | `editMode` true + 취소 아님 |

### 2.3. 검사 명령

```bash
# 공통 컴포넌트 — FTong07.Edit101 부착
grep -F 'data-legacy-id="FTong07.Edit101"' \
  도서물류관리프로그램/frontend/src/components/shared/scan-input.tsx \
  || echo "FAIL: scan-input.tsx FTong07.Edit101 누락"

# 3 페이지 — ScanInput 임포트
for f in \
  '도서물류관리프로그램/frontend/src/app/(app)/outbound/orders/[orderKey]/page.tsx' \
  '도서물류관리프로그램/frontend/src/app/(app)/inbound/receipts/[receiptKey]/page.tsx' \
  '도서물류관리프로그램/frontend/src/app/(app)/returns/receipts/[returnKey]/page.tsx'; do
  grep -q '@/components/shared/scan-input' "$f" \
    || echo "FAIL: $f ScanInput 미통합"
done
```

자동 검증: `test_TC_SC_P1_22_scan_input_in_three_pages` (T4).

5축 + DEC-028 grep 모두 통과 시 PR 통과 (5축 평가 정책 — `dfm-layout-input.mdc` §회귀 가드).

## 3. 신규 SQL 0건 검증 (DEC-040)

- `app/services/scan_match_service.py` — SELECT 1건 (G4_Book Gisbn 단건 매칭 — **기존 마스터 테이블 재해석**). INSERT/UPDATE/DELETE 0건.
- `app/services/pricing_service.py` — SELECT 최대 2건 (G1_Ggeo / G2_Ggwo Hcode='' → Hcode='@Hcode' 폴백 — **기존 outbound/inbound/returns 서비스의 Grat 조회와 동일 패턴 추출 (DRY)**). INSERT/UPDATE/DELETE 0건.
- `app/routers/scan.py` — DB 직접 호출 0건 (서비스 위임).

자동 검증: `test_TC_SC_P1_20_scan_match_service_no_new_dml` + `test_TC_SC_P1_21_pricing_service_no_new_dml` (T4).

## 4. C2/C3/C4 desired-state PUT 흐름 무영향

C8 의 매칭 결과 `resolved` 객체는 **클라이언트 측 라인 배열에만 추가** (DEC-040 — DRY/SRP). 저장은 기존 `PUT /orders/{key}` (C2) / `PUT /inbound/receipts/{key}` (C3) / `PUT /returns/receipts/{key}` (C4) 의 **desired-state diff** 로 흡수.

→ **백엔드 회귀 0** (기존 라우터/서비스 코드 변경 없음, 테스트 케이스 변경 0).

## 5. 변형 폴더 인벤토리 — 본 페이즈 영향 0

`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu21/Subu22/Subu23/` 의 변형 (Subu21_1/22_1/23_1 등) 은 모두 동일한 `FTong07` 프레임을 인스턴스화 → 동일 `Tong07.Button100Click` 호출. 단일 백엔드 + 단일 ScanInput 컴포넌트로 흡수.

`barcode_scan.yaml` `customer_variants` 에 G4_Book / G1_Ggeo / G2_Ggwo 컬럼 차이만 어댑터 파라미터로 명시 (서비스 분기 금지 — multi-db-compat 룰 §3).

## 6. 운영 배포 체크 (Phase 1 종료 후)

- [ ] USB-HID 호환 스캐너 (CR/Enter 종결 모드) 1대 이상 사양 확인 — DEC-004.
- [ ] 4 운영 서버 (`remote_138/153/154/155`) 에서 `axis_data` `scan.match` 그룹 모두 200/400/422/503 응답 확인 (`RUN_DB_SMOKE=1`).
- [ ] 출고/입고/반품 3 화면에서 실 ISBN 1건 스캔 → 라인 추가 → 기존 `PUT` 저장 → 회귀 무 (axis_test 통과로 정적 보증).
- [ ] OQ-002-R (Web Serial 직결) 미해소 상태로 잔류 — 사용자가 USB-HID 스캐너 구비 시까지 보류.

## 참조

- `analysis/layout_mappings/c8_scan_match.md`
- `analysis/handlers/c8_scan.md`
- `analysis/screen_cards/Tong08.md`
- `migration/contracts/barcode_scan.yaml`
- `i18n/messages/c8.ko.json`
- `test/test_c8_scan_phase1.py`
- `legacy-analysis/decisions.md` DEC-004 / DEC-010 / DEC-040
- `legacy-analysis/open-questions.md` OQ-002-R
- `.cursor/rules/dfm-layout-input.mdc` (룰 7) / `.cursor/rules/multi-db-compat.mdc`
