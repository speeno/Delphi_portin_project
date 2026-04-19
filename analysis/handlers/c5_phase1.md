# 이벤트 핸들러 · SQL 인덱스: C5 Phase 1 (정산 청구·집계·입금)

_생성: 2026-04-19 — C5 Phase 1 T2_

> Sobo45/45_1/47/41/42/42_1 의 OnClick·OnChange·OnUpdateData 등 dfm 이벤트와 `Subu*.pas` 의 SQL/메시지를 1:1 표로 정리. T3 contract 의 `actions[]` / T4 backend 라우터·서비스 메서드 매핑의 단일 출처.

## 0. 표기 규약

- **Form**: dfm 폼 ID (`Sobo45` 등)
- **dfm 이벤트**: `<위젯>.<이벤트>` (예: `Button702.OnClick`)
- **dfm 핸들러**: `Subu*.pas` 절차명 (예: `Button702Click`)
- **Pas Line**: `Subu*.pas` 의 시작 라인 번호 (참조용)
- **SQL ID**: `analysis/screen_cards/c5_settlement.md §4` 의 SQL-ST-N
- **Contract Action**: T3 `migration/contracts/settlement_billing.yaml` 의 액션 ID
- **Backend**: T4 라우터/서비스 메서드 (예: `settlement_service.confirm_billing`)
- **Frontend**: T6 페이지의 핸들러 함수명

## 1. 청구서관리 — Sobo45 / Sobo45_1

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| `Sobo45.OnActivate` | `FormActivate` | n/a | (mount only) | — | — | `useEffect(load)` |
| `Sobo45.OnShow` | `FormShow` | n/a | (mount only) | — | — | (same) |
| `Button101.OnClick` (Visible=false) | `Button101Click` | (보조) | SQL-ST-1 (SELECT) | `list_billing` | `settlement_service.list_billing` | `onSearch` |
| `Button201.OnClick` (Visible=false) | `Button201Click` | (보조) | — | (modal trigger) | — | `onOpenNew` |
| `Button701.OnClick` | `Button701Click` | n/a (Phase 2) | — | (Phase 2 print_invoice) | — | (out-of-scope Phase 1) |
| `Button702.OnClick` | `Button702Click` | n/a | SQL-ST-3 + audit | `confirm_billing` | `settlement_service.confirm_billing` | `onConfirmClose` (AuditPasswordModal) |
| `DBGrid201.Columns[10].OnUpdateData` | `DBGrid201Columns10UpdateData` | 2644~2971 | SQL-ST-1, SQL-ST-2 | `upsert_billing_line` | `settlement_service.upsert_billing_line` | `onLineEdit` |
| `DBGrid201.OnDblClick` | `DBGrid201DblClick` | n/a | (drilldown) | — | — | `onLineDrilldown` |
| `Edit101.OnChange` | `Edit101Change` | n/a | (state only) | — | — | `setDateFrom` |
| `Edit103.OnChange` (출판사코드) | `Edit103Change` | n/a | SQL-ST-1 (lookup) | `list_billing` (refresh) | — | `setHcode` |
| `Edit103.OnKeyDown` (autocomplete) | `Edit103KeyDown` | n/a | — | — | — | `<CustomerSearchInput>` 흡수 |
| (run-time) `Button004` Gpass 변경 | `Button004Click` 또는 InputBox | **372~381** (Subu45.pas) | SQL-ST-12 + audit | `rotate_audit_password` (DEC-032) | `audit_password_service.rotate_password(scope='gpass_change')` | AuditPasswordModal `rotate` 액션 |
| (취소 라인) | `DBGrid201Columns13UpdateData` (`YESNO='2'`) | 980 (분기), 1052 | SQL-ST-4 | `cancel_billing` | `settlement_service.cancel_billing` | `onCancelLine` (DEC-012 soft) |
| (트리거) | `Tong40._Sv_Ghng_` | 3282~3304, 4523 | SQL-ST-5 | (자동 — confirm_billing 내부) | `settlement_service._touch_sv_ghng` | (automatic) |

> **Sobo45_1 (택배 변형)** — 위 표 동일, `Pas Line` 만 `Subu45_1.pas` 기준으로 ±300 차이. variant 분기는 backend/frontend 모두 단일 메서드 + `variant=takbae` 파라미터로 흡수.

## 2. 청구금액(년월) — Sobo47

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| `Sobo47.OnActivate` | `FormActivate` | n/a | — | — | — | `useEffect(load)` |
| `Button101.OnClick` | `Button101Click` | 271~316 | SQL-ST-6 | `list_period_summary` | `settlement_service.list_period_summary` | `onSearch` |
| `Edit104.OnChange` (시작년월) | `Edit104Change` | n/a | — | — | — | `setFromMonth` |
| `Edit105.OnChange` (종료년월) | `Edit105Change` | n/a | — | — | — | `setToMonth` |
| (보고 호출) | `Tong20.Srart_47_01` | n/a | (모던 화면이 결과 자체) | — | — | (omitted — Phase 2 인쇄 후속 C7) |

## 3. 입금내역 — Sobo41

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| `Sobo41.OnActivate` | `FormActivate` | n/a | — | — | — | `useEffect(load)` |
| `Button101.OnClick` | `Button101Click` | n/a | SQL-ST-7 | `list_cash` | `cash_service.list_cash` | `onSearch` |
| `Button201.OnClick` | `Button201Click` | n/a | — | (modal trigger) | — | `onNew` |
| `Button700.OnClick` (저장) | `Button700Click` | 343/353/563 | SQL-ST-8 (INSERT) / SQL-ST-9 (UPDATE) | `register_cash` (UPSERT) | `cash_service.register_cash` | `onSave` |
| `Button701.OnClick` (취소) | `Button701Click` | n/a | — | — | — | `onReset` |
| `DBGrid101.OnDblClick` | (n/a — Phase 1 클릭) | n/a | — | — | — | `onLineEdit` (입력 패널 prefill) |
| `Edit301.OnChange` (거래처코드) | `Edit301Change` | n/a | — | — | — | `setFormHcode` |
| `Edit303.OnChange` (입금일자) | `Edit303Change` | n/a | — | — | — | `setFormGdate` |
| `Edit306.OnChange` (입금액) | `Edit306Change` | n/a | — | — | — | `setFormGssum` |

## 4. 입금현황 — Sobo42 / Sobo42_1

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| `Sobo42.OnActivate` | `FormActivate` | n/a | — | — | — | `useEffect(load)` |
| `Button101.OnClick` | `Button101Click` | 278 (본) / 297 (변형) | SQL-ST-10 (본) / SQL-ST-11 (변형) | `cash_status` (variant 파라미터) | `settlement_service.cash_status(variant)` | `onSearch` |
| `Button201.OnClick` | `Button201Click` | n/a | — | (Phase 1 미사용) | — | (out-of-scope) |
| `Button700.OnClick` | `Button700Click` | n/a | (Phase 2 인쇄) | — | — | (out-of-scope) |
| `Edit101.OnChange` (기준년월) | `Edit101Change` | n/a | — | — | — | `setMonth` |
| `Edit107.OnChange` (거래처코드) | `Edit107Change` | n/a | — | — | — | `setHcode` |

## 5. 마감 가드 패턴 (모든 쓰기 액션 공통)

```python
# T4 settlement_service.assert_period_open
async def assert_period_open(server_id: str, gdate: str, hcode: str) -> None:
    rows = await execute_query(
        server_id,
        "SELECT Yesno FROM T2_Ssub WHERE Gdate=%s AND Hcode=%s LIMIT 1",
        (gdate, hcode),
    )
    yesno = (rows[0] or {}).get("Yesno") if rows else None
    if yesno == "1":
        raise PeriodClosedError("마감된 자료입니다.")  # i18n key: c5.errors.period_closed
```

호출자는 모든 쓰기 contract action 진입 직후 `assert_period_open(...)` 을 부른다 (DEC-031). 라우터 변환 표:

| Exception | HTTP | Code | i18n key |
| --- | --- | --- | --- |
| `PeriodClosedError` | 423 | `ST_PERIOD_CLOSED` | `c5.errors.period_closed` |
| `AuditTokenError` | 401 | `ST_AUDIT_INVALID` | `c5.errors.audit_invalid` |
| `AuditLockedError` | 429 | `ST_AUDIT_LOCKED` | `c5.errors.audit_locked` |
| `AlreadyCancelledError` | 409 | `ST_ALREADY_CANCELLED` | `c5.errors.already_cancelled` |
| `ValidationError` (Pubun/Hcode) | 422 | `ST_VALIDATION` | `c5.errors.validation_*` |

## 6. SQL 인덱스 (재사용 — c5_settlement.md §4 와 동일 키)

| SQL ID | 폼 | 핸들러 | SQL 본문 (요지) |
| --- | --- | --- | --- |
| SQL-ST-1 | Sobo45 | `DBGrid201Columns10UpdateData` | `INSERT/UPDATE T2_Ssub SET ... WHERE Gdate=? AND Hcode=?` |
| SQL-ST-2 | Sobo45 | (same) | `INSERT/UPDATE T3_Ssub SET ... WHERE Gdate=? AND Hcode=? AND Idx=?` |
| SQL-ST-3 | Sobo45 | `Button702Click` (마감) | `UPDATE T2_Ssub SET Yesno='1' WHERE Gdate=? AND Hcode=?` |
| SQL-ST-4 | Sobo45 | `Button702Click` (취소) | `UPDATE T2_Ssub SET Yesno='2' WHERE ...` (DEC-012) |
| SQL-ST-5 | Sobo45 | `Tong40._Sv_Ghng_` | `UPDATE Sv_Ghng SET ... WHERE ...` (트리거) |
| SQL-ST-6 | Sobo47 | `Button101Click` | `SELECT Gdate, Sum(Sum26..28) FROM T2_Ssub WHERE Hcode=? AND Gdate BETWEEN ? AND ? GROUP BY Gdate` |
| SQL-ST-7 | Sobo41 | `Button101Click` | `SELECT * FROM T5_Ssub LEFT JOIN G7_Ggeo ON ... WHERE Gdate BETWEEN ? AND ?` |
| SQL-ST-8 | Sobo41 | `Button700Click` (insert) | `INSERT INTO T5_Ssub (Gdate, Hcode, Sdate, Gssum, Pubun, Gbigo) VALUES (...)` |
| SQL-ST-9 | Sobo41 | `Button700Click` (update) | `UPDATE T5_Ssub SET Gssum=?, Pubun=?, Gbigo=? WHERE Gdate=? AND Hcode=? AND Jubun=?` |
| SQL-ST-10 | Sobo42 | `Button101Click` | `SELECT Hcode, Sum(Sum26..28) FROM T2_Ssub WHERE Sdate=? GROUP BY Hcode` + `LEFT JOIN T5_Ssub` |
| SQL-ST-11 | Sobo42_1 | `Button101Click` | `SELECT Gdate, Sum(Sum26..28) FROM T2_Ssub WHERE Hcode=? GROUP BY Gdate` (변형) |
| SQL-ST-12 | (Subu45.pas L372~381) | `InputBox` (평문 — DEC-032 폐기) | `UPDATE Id_Logn SET Gpass=? WHERE Hcode='0001'` → `audit_password_service.rotate_password` |

## 7. 메시지 카탈로그 → `i18n/messages/c5.ko.json`

레거시 메시지 박스 캡처 (`Subu*.pas` 의 `ShowMessage(...)` 와 `Base01.pas` 상수) 를 단일 i18n 사전으로 흡수. T2 산출물 [`i18n/messages/c5.ko.json`](../../i18n/messages/c5.ko.json) 참조.

| 키 | 한글 메시지 | 출처 (Pas Line) |
| --- | --- | --- |
| `c5.success.saved` | "저장완료" | Subu45.pas L2982, Subu45_1.pas L3144 |
| `c5.success.updated` | "수정되었습니다." | Subu45.pas L381, Subu45_1.pas L433 |
| `c5.errors.open` | "오픈시 에러가 발생했습니다.\n다시 시도해 주십시오." | Base01.pas L13 (`E_Open`) |
| `c5.errors.insert` | "입력시 에러가 발생했습니다.\n다시 시도해 주십시오." | Base01.pas L14 (`E_Insert`) |
| `c5.errors.update` | "수정시 에러가 발생했습니다.\n다시 시도해 주십시오." | Base01.pas L15 (`E_Update`) |
| `c5.errors.delete` | "삭제시 에러가 발생했습니다.\n다시 시도해 주십시오." | Base01.pas L16 (`E_Delete`) |
| `c5.errors.connect` | "사용관한이 없습니다.\n관리자에게 문의하십시오." | Base01.pas L17 (`E_Connect`) |
| `c5.validation.publisher_required` | "출판사명을 입력해 주세요." | Base01.pas L12 (`E_Ggeo`) |
| `c5.validation.publisher_register` | "출판사를 등록해 주세요." | Subu41.pas L719 |
| `c5.validation.publisher_select` | "거래처를 선택하세요." | (T8 신설 — ST-RULE-5) |
| `c5.validation.pubun_select` | "결재구분을 선택하세요." | (T8 신설 — ST-RULE-4) |
| `c5.errors.period_closed` | "마감된 자료입니다." | (T8 신설 — DEC-031, ST-RULE-1) |
| `c5.errors.already_cancelled` | "이미 취소된 자료입니다." | (T8 신설 — ST-RULE-3) |
| `c5.errors.audit_invalid` | "비밀번호가 일치하지 않습니다." | (T8 신설 — ST-RULE-2 / DEC-029) |
| `c5.errors.audit_locked` | "비밀번호 시도 한도를 초과했습니다. 30분 후 다시 시도하세요." | (T8 신설 — DEC-029 lockout) |
| `c5.dialog.password_change_title` | "Password변경" | Subu45.pas L372 |
| `c5.dialog.password_change_prompt` | "비밀번호를 입력 하세요." | Subu45.pas L372 |

> 신설 키 5개(`period_closed`, `already_cancelled`, `audit_*`, `validation_*_select`) 는 레거시 명시 메시지가 없어서 운영 어조를 따라 신설 — DEC-031 결정 시점에 동결.

## 8. 회귀 가드

- `assert_period_open` 호출 누락 정적 검사: T7 에서 `settlement_service.py` 의 모든 `INSERT/UPDATE` 쿼리 위에 `await self.assert_period_open(...)` 가 선행하는지 grep 정규식으로 검사.
- i18n 사전 키 일관성: 백엔드 예외 코드(예: `ST_PERIOD_CLOSED`) ↔ 프론트엔드 메시지 키(`c5.errors.period_closed`) 매칭 1:1.
- DEC-029 audit token 헤더 누락 시 401, 잠금 시 429.
- DEC-019 — 변형 분기는 backend `variant` 파라미터 + frontend `?variant=` query 만 허용, 코드 분기 금지.

## 9. 참조

- 화면 카드: [`analysis/screen_cards/c5_settlement.md`](../screen_cards/c5_settlement.md)
- 매핑 노트: [`analysis/layout_mappings/Sobo45_billing.md`](../layout_mappings/Sobo45_billing.md) 외 5건
- contract: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) (T3)
- backend: [`도서물류관리프로그램/backend/app/services/settlement_service.py`](../../도서물류관리프로그램/backend/app/services/settlement_service.py) (T4)
- i18n: [`i18n/messages/c5.ko.json`](../../i18n/messages/c5.ko.json) (T2 산출물)
- 결정: DEC-009/012/019/024/028/029/031/032
