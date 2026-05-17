# Sobo43_shipping_ledger — 발송비내역 (Subu43)

**ID**: `Sobo43_shipping_ledger`  
**라우트**: `/settlement/shipping-ledger`  
**API**: `GET /api/v1/settlement/shipping-ledger` (v0.1 scaffold)  
**계약**: `migration/contracts/shipping_ledger.yaml`  
**wrong_id**: `Sobo43_stats_route` (`/stats/publisher`, 출판사통계) — **캡션·라우트 변경 금지** (DEC-049 e).

## T1 레거시 정본

- 소스: `legacy_delphi_source/legacy_source/Source/Subu43.pas`, 대응 dfm `Sobo43.dfm` (산출물은 `tools/delphi_porting_accelerator/examples/generated/...` 규칙에 따름).
- 도메인 키워드: `T3_Ssub` 라인의 `NAME1`, `NAME2`, `GSSUM` 등 발송비 항목 (청구 T3 라인과 의미 분리 — billing-subu43-44-shipping-backlog §3).

## CRUD 갭 (G0)

| 레거시(예상) | 웹 v0.1 | 비고 |
|--------------|---------|------|
| 그리드 조회 + 필터 | GET scaffold 빈 목록 | T2 SQL |
| 저장/삭제 버튼 | 미구현 | G2 + DEC-031 마감 |

## 이벤트 / SQL (T2 placeholder)

- T2 완료 시 본 절에 `Button*Click` → 서비스 함수 → pytest 이름을 1:1로 적는다.

## DEC

- DEC-049 (e): wrong_id 분리 + 신규 ID.
- DEC-040: 신규 SQL 0 — 기존 헬퍼 재사용 우선.
- DEC-033: 멀티 DB 페이징·count_grouped.
