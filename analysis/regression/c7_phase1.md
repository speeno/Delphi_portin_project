# C7 Phase 1 — 회귀 매트릭스 (T7)

본 노트는 C7 Phase 1 (라벨/송장 인쇄 — 양식 5종 + 라벨 1종) 의 **회귀 가드 5축**을 단일 표로 모은다. 모든 항목은 PR 단계에서 **반드시** 통과해야 한다.

## 1. 5축 매트릭스

| 축 | 명령 | 통과 기준 | 본 페이즈 추가 |
| --- | --- | --- | --- |
| **axis_test** | `cd 도서물류관리프로그램/backend && python3 -m pytest /Users/speeno/Delphi_porting/test/test_c7_print_phase1.py` | 22/22 PASSED | T4 신규 22 케이스 |
| **axis_type** | `cd 도서물류관리프로그램/frontend && npx tsc --noEmit` | 0 error | T6a/T6b 신규 5 페이지 + `lib/print-api.ts` |
| **axis_lint** | `cd 도서물류관리프로그램/frontend && npx eslint src/lib/print-api.ts $(find src/app/\(app\)/print src/app/\(app\)/outbound/orders src/app/\(app\)/returns/receipts src/app/\(app\)/transactions/sales-statement src/app/\(app\)/settlement/billing src/app/\(app\)/settlement/tax-invoice -name 'page.tsx')` | 0 error | T6a 부착, T6b 신규 4 페이지 |
| **axis_data** | `python3 debug/probe_backend_all_servers.py` (dry-run) → 5 그룹 신규 출력 | `print.outbound_statement_pdf` / `print.return_receipt_pdf` / `print.sales_statement_pdf` / `print.label_pdf` / `settlement.invoice_pdf` 5 그룹이 4 서버 전체에 출력 | T7 신규 |
| **axis_doc** | `grep -l "DEC-037" analysis/layout_mappings/{Sobo46_billing,Sobo49_tax,Sobo27,Sobo23,Sobo21,Seep13_label}.md analysis/print_specs/c7_phase1.md analysis/handlers/c7_phase1.md migration/contracts/{print_invoice,print_label,settlement_billing}.yaml` | 9 파일 모두 매칭 | T1/T2/T3 노트·계약 |

## 2. DEC-028 grep — `data-legacy-id` 누락 0건

C7 Phase 1 신규/변경된 모든 프론트 페이지가 매핑 노트의 `legacy_id` 와 1:1 일치해야 한다.

### 2.1. 미리보기 페이지 (T6a/T6b) 5종 + 라벨 1종

| 페이지 | legacy_form | data-legacy-id 최소 보장 |
| --- | --- | --- |
| `settlement/billing/[billingKey]/print/page.tsx` (T6a) | `Sobo46` | `Sobo46.Button.PrintPdf` |
| `settlement/tax-invoice/[billingKey]/print/page.tsx` (T6a) | `Sobo49` | `Sobo49.Button.PrintPdf` |
| `outbound/orders/[orderKey]/print/page.tsx` (T6b 신규) | `Sobo27` | `Sobo27.Print`, `Sobo27.Button.PrintPdf`, `Sobo27.Button.Print` |
| `returns/receipts/[returnKey]/print/page.tsx` (T6b 신규) | `Sobo23` | `Sobo23.Print`, `Sobo23.Button.PrintPdf`, `Sobo23.Button.Print` |
| `transactions/sales-statement/[orderKey]/print/page.tsx` (T6b 신규) | `Sobo21` | `Sobo21.Print`, `Sobo21.Button.PrintPdf`, `Sobo21.Button.Print` |
| `print/label/[shipmentKey]/page.tsx` (T6b 신규) | `Seep13` | `Seep13.Print`, `Seep13.Label.Form`, `Seep13.Button.PrintPdf` |

### 2.2. 검사 명령

```bash
# C7 Phase 1 신규/변경 페이지 6종 모두에서 data-legacy-id 출현 검사
for f in \
  "도서물류관리프로그램/frontend/src/app/(app)/settlement/billing/[billingKey]/print/page.tsx" \
  "도서물류관리프로그램/frontend/src/app/(app)/settlement/tax-invoice/[billingKey]/print/page.tsx" \
  "도서물류관리프로그램/frontend/src/app/(app)/outbound/orders/[orderKey]/print/page.tsx" \
  "도서물류관리프로그램/frontend/src/app/(app)/returns/receipts/[returnKey]/print/page.tsx" \
  "도서물류관리프로그램/frontend/src/app/(app)/transactions/sales-statement/[orderKey]/print/page.tsx" \
  "도서물류관리프로그램/frontend/src/app/(app)/print/label/[shipmentKey]/page.tsx"; do
  count=$(grep -c "data-legacy-id" "$f" 2>/dev/null || echo 0)
  test "$count" -ge 2 || echo "FAIL: $f data-legacy-id < 2건"
done
```

5축 + DEC-028 grep 모두 통과 시 PR 통과 (5축 평가 정책 — `dfm-layout-input.mdc` §회귀 가드).

## 3. 신규 SQL 0건 검증 (DEC-037 §7)

- `print_service.py` — SELECT/INSERT/UPDATE/DELETE 0건 (출력 변환만).
- `label_service.py` — SQL-PR-6 (1건) 만 허용 (`handlers/c7_phase1.md §7`).
- `outbound_service.render_outbound_statement_html` / `returns_service.render_return_receipt_html` / `transactions_service.render_sales_statement_html` — 모두 SQL 0건 (기존 detail SQL 재사용).

자동 검증: `test_TC_PR_P1_24_no_new_sql_in_print_services` (T4).

## 4. 변형 폴더 인벤토리 — 본 페이즈 영향 0

C2 (Subu27/Subu27_1/Subu27_2), C4 (Subu23/Subu23_1/Subu23_2), C6 (Subu21/Subu21_1/Subu21_2) 의 변형은 **데이터 컬럼만 다름** — PDF 빌더는 동일. `customer_variants` (각 contract) 가 흡수.

## 5. 운영 배포 체크 (Phase 1 종료 후)

- [ ] WeasyPrint + libpango/libcairo 시스템 설치 (DEC-037 / `requirements.txt` 메모).
- [ ] `backend/static/fonts/NanumGothic.ttf` 배치 (DEC-037 / `static/fonts/README.md`).
- [ ] 4 운영 서버 (`remote_138/153/154/155`) 에서 `axis_data` 5 그룹 모두 200/404/422/503 응답 확인.

## 참조

- `analysis/layout_mappings/{Sobo46_billing,Sobo49_tax,Sobo27,Sobo23,Sobo21,Seep13_label}.md`
- `analysis/print_specs/c7_phase1.md` / `analysis/handlers/c7_phase1.md`
- `migration/contracts/{print_invoice,print_label,settlement_billing}.yaml`
- `test/test_c7_print_phase1.py`
- `legacy-analysis/decisions.md` DEC-037 / DEC-038 / DEC-039
