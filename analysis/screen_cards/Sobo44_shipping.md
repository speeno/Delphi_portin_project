# Sobo44_shipping_status — 발송비현황 (Subu44)

**ID**: `Sobo44_shipping_status`  
**라우트**: `/settlement/shipping-status`  
**API**: `GET /api/v1/settlement/shipping-status` (v0.1 scaffold)  
**계약**: `migration/contracts/shipping_ledger.yaml` (`shipping_status_list`)  
**wrong_id**: `Sobo44_inv` (`/inventory/status`, 재고현황) — **캡션·라우트 변경 금지**.

## T1 레거시 정본

- 소스: `legacy_delphi_source/legacy_source/Source/Subu44.pas`, `Sobo44.dfm`.
- 집계 축(거래처·기간 등)은 T2에서 확정.

## CRUD 갭 (G0)

| 레거시(예상) | 웹 v0.1 | 비고 |
|--------------|---------|------|
| 현황 그리드 조회 | GET scaffold 빈 rows | T2 SQL |
| 출력/엑셀 등 | 미구현 | C7 / 리포트 트랙 |

## DEC

- DEC-049 (e), DEC-040, DEC-033 — `Sobo43_shipping.md` 와 동일 원칙.
