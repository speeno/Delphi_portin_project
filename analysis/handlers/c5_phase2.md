# 이벤트 핸들러 · SQL 인덱스: C5 Phase 2 (청구서출력·세금계산서·재집계·audit 회전 UI)

_생성: 2026-04-19 — C5 Phase 2 T2_

> Sobo46 / Sobo49 의 OnClick·OnChange·OnUpdateData·BeforePost 등 dfm 이벤트와 `Subu46.pas` / `Subu49.pas` 의 SQL/메시지를 1:1 표로 정리. T3 contract 의 `actions[]` / T5 backend 라우터·서비스 메서드 매핑의 단일 출처. **표기 규약은 [`c5_phase1.md`](c5_phase1.md) §0 와 동일.**

## 0. Phase 2 진입 결정 요약

| 결정 ID | 내용 | 근거 |
| --- | --- | --- |
| DEC-034 | Phase 2 인쇄 = HTML 미리보기, PDF/실인쇄/일괄 = C7 이연 | 사용자 결정 (이번 세션) |
| DEC-035 | 세금계산서 외부 발행 채널 = stub (`/issue` → 200 NOT_INTEGRATED + audit 영속화) | OQ-ST-1 종결 |
| DEC-036 | Chek3 단건/일괄 토글 = 단일 SQL 헬퍼 흡수, `Code1='1' ⇔ Chek3='1'` 매핑 동결 | OQ-ST-2 종결 + 코드 중복 제거 (3곳) |

## 1. 청구서출력 — Sobo46

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| `Sobo46.OnActivate` (`L303`) | `FormActivate` | 303 | (mount only) | — | — | (URL `[billingKey]` 활성) |
| `Sobo46.OnShow` (`L310`) | `FormShow` | 310 | SQL-ST-17 | `list_print_targets` (Phase 1 list 재사용) | — | (목록 페이지 책임) |
| `Button101.OnClick` | `Button101Click` (검색) | 485~563 | SQL-ST-15 | `list_billing` (Phase 1) | `settlement_service.list_billing` | (목록 페이지) |
| `Button201.OnClick` (Visible=false) | `Button201Click` (단건 선택) | 565~ | SQL-ST-13 + SQL-ST-14 + SQL-ST-16 | `get_print_data` | `settlement_print_service.get_print_data` | `useEffect(load)` (단건 페이지 mount) |
| `Button016.OnClick` | `Button016Click` (일괄 인쇄1) | 418~432 | (Phase 2 미구현 — C7 후속) | — | — | (out-of-scope DEC-034) |
| `Button017.OnClick` | `Button017Click` (일괄 인쇄2) | 434~448 | (Phase 2 미구현 — C7 후속) | — | — | (out-of-scope) |
| `Button701.OnClick` | (인쇄) | n/a | (Phase 2 단순화) | — | — | `<button onClick={window.print()}>` |
| `Button702.OnClick` | (마감) | n/a | SQL-ST-3 (Phase 1) | `confirm_billing` | (목록 페이지 책임) | (Phase 1) |
| `T4_Sub61BeforePost` (Edit201~315 표시 전용) | (없음) | n/a | — | — | — | — |
| (인쇄 미리보기) | — (모던 신설) | — | — | `print_preview_html` | `settlement_print_service.render_preview` (Jinja2) | `<iframe>` 또는 본 페이지 자체 |

### 1.1 Edit201~Edit315 → 백엔드 응답 매핑 (1:N)

레거시 `SetVal` 67개 호출은 단일 응답 `summary{}` JSON 으로 흡수 (모던 페이지에서 `Sobo46.Summary.{key}` data-legacy-id 1:1):

```python
# settlement_print_service._build_summary
SUMMARY_FIELD_MAP: dict[str, str] = {
    # core 5
    "sum26": "Sum26",  # Edit226 — 당월금액
    "sum27": "Sum27",  # Edit227 — 세액
    "sum28": "Sum28",  # Edit228 — 합계금액
    "gsusu": "Gsusu",  # Edit310 — 입금액
    "vdate": "Vdate",  # Edit238 — 입금일
    # supplemental — Sum01..Sum25, Sum29..Sum48, Sum51..Sum69
    **{f"sum{n:02d}": f"Sum{n:02d}" for n in (*range(1, 26), *range(29, 49), *range(51, 70))},
    "bigo1": "Bigo1",
    "bigo2": "Bigo2",
}
```

> 모던 응답: `summary` 는 dict, 표시 시 alias 매핑은 프론트 `lib/settlement-api.ts` 가 흡수. 67개 모두 직렬화하지만 UI 는 핵심 5종 + `<details>` 토글만 표시.

## 2. 세금계산서발행 — Sobo49

| dfm 이벤트 | dfm 핸들러 | Pas Line | SQL ID | Contract Action | Backend | Frontend |
| --- | --- | --- | --- | --- | --- | --- |
| `Sobo49.OnActivate` (`L154`) | `FormActivate` | 154 | (mount only) | — | — | `useEffect(mount)` |
| `Sobo49.OnShow` (`L161`) | `FormShow` | 161 | (default dates) | — | — | (same) |
| `Button101.OnClick` / `dxButton1.OnClick` | `Button101Click` (조회) | 327~420 | SQL-ST-18 + SQL-ST-19 | `list_tax_invoice` | `tax_invoice_service.list_targets` | `onSearch` |
| `DBGrid101.Columns[7].OnUpdateData` | `DBGrid101Columns7UpdateData` (단건) | 695~715 | SQL-ST-20 | `toggle_chek3` (`bulk:false`) | `tax_invoice_service.toggle_chek3` | `onChek3Change(row)` |
| `RadioButton4.OnClick` | `RadioButton4Click` (일괄 ON) | 717~744 | SQL-ST-20 | `toggle_chek3` (`bulk:true, toggle:'1'`) | (same) | `onBulkIssueOn` |
| `RadioButton5.OnClick` | `RadioButton5Click` (일괄 OFF) | 746~773 | SQL-ST-20 | `toggle_chek3` (`bulk:true, toggle:'0'`) | (same) | `onBulkIssueOff` |
| `T4_Sub91.BeforePost` (`dsEdit`) | `T4_Sub91BeforePost` | 657~677 | SQL-ST-21 | `update_sdate` | `tax_invoice_service.update_sdate` | `onSdateBlur(row)` |
| `Button200.OnClick` (단건 인쇄) | `Button200Click` | 601~613 | (Phase 2 단순화) | `get_tax_print_data` | `tax_invoice_service.get_print_data` | `<Link href=/{key}/print>` |
| `Button016.OnClick` / `Button017.OnClick` (일괄 인쇄) | n/a | 282/287 | (Phase 2 미구현 — C7) | — | — | (out-of-scope) |
| (모던 신설) 외부 발행 stub | — | — | SQL-ST-22 (audit) | `issue_external_stub` | `tax_invoice_service.issue_stub` | `onIssue(row)` |
| (모던 신설) 인쇄 미리보기 | — | — | (재사용 SQL-ST-18/19) | `tax_print_preview_html` | `tax_invoice_service.render_preview` | `<iframe>` 또는 페이지 자체 |

### 2.1 Chek3 토글 단일 SQL 헬퍼 (DEC-036)

레거시 3곳(L699/723/752)에 동일 SQL 패턴이 존재 — 모던은 단일 헬퍼로 흡수:

```python
# tax_invoice_service.py — 단일 진실원
async def _update_chek3(
    server_id: str,
    *,
    gdate_month: str,   # 'YYYYMM' 6자
    hcode: str | None,  # None ⇒ 일괄 (월 전체)
    new_value: str,     # '0' or '1'
) -> int:
    if hcode is None:
        sql = "UPDATE T2_Ssub SET Chek3 = %s WHERE Gdate = %s AND Sum27 <> 0"
        params = (new_value, gdate_month)
    else:
        sql = "UPDATE T2_Ssub SET Chek3 = %s WHERE Gdate = %s AND Hcode = %s"
        params = (new_value, gdate_month, hcode)
    return await execute_query(server_id, sql, params)
```

> 단건 토글은 호출자 측에서 "현재 Chek3 의 부정값" 을 결정해 `new_value` 로 전달 (레거시 `if Code1='1' then '0' else '1'` 의미 보존). 일괄은 `'1'` 또는 `'0'` 명시.

## 3. 재집계 잡 — `recalc_billing`

| 의미 | 모던 액션 | SQL ID | 입력 | 출력 |
| --- | --- | --- | --- | --- |
| 출고/반품 원천에서 `T2_Ssub.Sum26~28` 재계산 | `recalc_billing` | SQL-ST-23 | `{server_id, gdate_month, hcode?}` | `{updated: N, recomputed: {...}}` |

```python
# settlement_service.recalc_billing
# 1) 마감 가드: assert_period_open(gdate_month, hcode) — DEC-031 일관
# 2) 출고/반품 원천에서 재집계
#    aggregate_billing 함수 (Phase 1) 가 이미 같은 로직 사용 → 단일 헬퍼로 흡수
# 3) audit_settlement INSERT (action='billing_recalculated')
```

## 4. audit 회전 UI — `/admin/audit-rotate`

| 의미 | 모던 액션 | 백엔드 | 비고 |
| --- | --- | --- | --- |
| audit_settlement 최근 N건 조회 | `list_audit_settlement` | `GET /api/v1/audit/settlement` (T5d) | `?scope=audit\|gpass_change\|all`, `?limit=…` |
| Gpass 회전 (DEC-032) | `rotate_gpass` (재사용) | (Phase 1 `audit_password_service.rotate_password(scope='gpass_change')`) | 기존 엔드포인트 재사용 |
| Audit Pwd 회전 (반품용) | `rotate_audit` (재사용) | (Phase 1 `rotate_password(scope='audit')`) | 기존 엔드포인트 재사용 |

## 5. SQL 인덱스 — Phase 2 추가

| ID | 폼 | 종류 | 테이블 | 요약 |
| --- | --- | --- | --- | --- |
| SQL-ST-13 | Sobo46 | SELECT | `T2_Ssub` | `SELECT Sum01..Sum69, Gsusu, Vdate, Bigo1, Bigo2 FROM T2_Ssub WHERE Gdate=? AND Hcode=?` (1행) |
| SQL-ST-14 | Sobo46 | SELECT | `T3_Ssub` | `SELECT Gdate, Gqut1..Gqut7, Name1, Name2, Gname, Gcode, Gsqut, Gssum, Yesno FROM T3_Ssub WHERE Gdate=? AND Hcode=? ORDER BY Gdate` |
| SQL-ST-15 | Sobo46 | SELECT | `T2_Ssub` ⨝ `G7_Ggeo` | `SELECT Hcode, Bcode, Yesno FROM T2_Ssub WHERE Gdate=? AND Bcode='완료' AND Yesno='O' ORDER BY Hcode` |
| SQL-ST-16 | Sobo46 | SELECT (lookup) | `G7_Ggeo` | `SELECT Hname, Bname FROM G7_Ggeo WHERE Hcode=?` |
| SQL-ST-17 | Sobo46 | SELECT (콤보) | `T2_Ssub` | `SELECT DISTINCT Gdate FROM T2_Ssub ORDER BY Gdate DESC LIMIT 200` |
| SQL-ST-18 | Sobo49 | SELECT | `T2_Ssub` | `SELECT Hcode, Sum26, Sum27, Sum28, Chek3, Sdate FROM T2_Ssub WHERE Gdate=? AND Sum27 <> 0` |
| SQL-ST-19 | Sobo49 | SELECT (lookup) | `G7_Ggeo` | `SELECT Hname FROM G7_Ggeo WHERE Hcode=?` (`Seek_Name` 흡수) |
| SQL-ST-20 | Sobo49 | UPDATE | `T2_Ssub.Chek3` | `UPDATE T2_Ssub SET Chek3=? WHERE Gdate=? AND (Hcode=? OR Sum27<>0)` (단일 헬퍼, DEC-036) |
| SQL-ST-21 | Sobo49 | UPDATE | `T2_Ssub.Sdate` | `UPDATE T2_Ssub SET Sdate=? WHERE Gdate=? AND Hcode=?` |
| SQL-ST-22 | Sobo49 | INSERT | `audit_settlement` | `INSERT INTO audit_settlement (...) VALUES (..., 'tax_issued_stub', ...)` (DEC-035) |
| SQL-ST-23 | (재집계) | SELECT + UPDATE | `S1_Ssub` / `R*_Ssub` → `T2_Ssub` | `aggregate_billing` 헬퍼 (Phase 1) 호출 — 출고/반품 원천에서 Sum26~28 재구성 |

## 6. 메시지 카탈로그 — Phase 2 추가 (`i18n/messages/c5.ko.json`)

| 키 | 한글 | 비고 |
| --- | --- | --- |
| `c5.print.no_data` | "해당 거래처의 청구 자료가 없습니다." | Sobo46 — `print-data` 빈 응답 |
| `c5.print.preview_only` | "본 화면은 미리보기입니다. PDF/실인쇄는 후속 모듈에서 제공됩니다." | DEC-034 시각화 |
| `c5.tax.external_not_integrated` | "세금계산서 외부 발행 채널이 연결되지 않았습니다. 발행 기록만 저장됩니다." | DEC-035 (`/issue` 응답 표시) |
| `c5.tax.chek3_toggled_single` | "발행 상태를 변경했습니다." | 단건 토글 성공 |
| `c5.tax.chek3_toggled_bulk` | "{count}건의 발행 상태를 변경했습니다." | 일괄 토글 성공 |
| `c5.tax.sdate_updated` | "발행일자를 수정했습니다." | BeforePost UPDATE 성공 |
| `c5.recalc.started` | "재집계를 시작합니다." | `recalc_billing` 진입 |
| `c5.recalc.completed` | "재집계가 완료되었습니다 ({count}건 갱신)." | 완료 |
| `c5.audit_rotate.gpass_done` | "G-Pass 비밀번호를 변경했습니다." | DEC-032 |
| `c5.audit_rotate.audit_done` | "감사 비밀번호를 변경했습니다." | DEC-029 |

> 모든 키는 Phase 1 `c5.ko.json` 의 `messages` 객체에 append (단일 사전 — 신규 파일 금지). 키 prefix `c5.print.*`, `c5.tax.*`, `c5.recalc.*`, `c5.audit_rotate.*` 로 그룹화.

## 7. 회귀 가드

- `assert_period_open` 호출 누락 정적 검사 (Phase 1 그대로 확장): `tax_invoice_service.toggle_chek3`, `update_sdate`, `issue_stub`, `settlement_service.recalc_billing` 4건 모두 첫 줄에 `await assert_period_open(...)`.
- `_update_chek3` 헬퍼 외 다른 곳에서 `UPDATE T2_Ssub SET Chek3` 패턴 grep → 0건 (DEC-036 단일 진실원 보장).
- `tax_invoice_service.issue_stub` 응답 본문 정적 검사: `status="NOT_INTEGRATED"` 와 audit `INSERT` 모두 존재.
- `settlement_print_service` 의 `summary` 응답이 67개 키 전체 직렬화하는지 단위 테스트 (`test_c5_settlement_phase2.py`).
- DEC-019 — 재집계 / 토글 / 인쇄 모두 단일 컴포넌트 + 데이터 주도, 변형(Sobo45_1 등) 분기 코드 0.

## 8. 참조

- 화면 카드: [`analysis/screen_cards/c5_settlement.md`](../screen_cards/c5_settlement.md) §10 Phase 2
- 매핑 노트: [`Sobo46_billing.md`](../layout_mappings/Sobo46_billing.md), [`Sobo49_tax.md`](../layout_mappings/Sobo49_tax.md)
- contract: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) v1.1.0 (T3)
- backend (T5):
  - [`도서물류관리프로그램/backend/app/services/settlement_print_service.py`](../../도서물류관리프로그램/backend/app/services/settlement_print_service.py) (신설)
  - [`도서물류관리프로그램/backend/app/services/tax_invoice_service.py`](../../도서물류관리프로그램/backend/app/services/tax_invoice_service.py) (신설)
  - [`도서물류관리프로그램/backend/app/services/settlement_service.py`](../../도서물류관리프로그램/backend/app/services/settlement_service.py) (`recalc_billing` 추가)
  - [`도서물류관리프로그램/backend/app/routers/settlement.py`](../../도서물류관리프로그램/backend/app/routers/settlement.py) (+8 endpoints)
- i18n: [`i18n/messages/c5.ko.json`](../../i18n/messages/c5.ko.json) (Phase 2 키 append)
- 결정: DEC-029/031/032/033/034/035
- 선례 핸들러: [`c5_phase1.md`](c5_phase1.md), [`c4_phase1.md`](c4_phase1.md)
