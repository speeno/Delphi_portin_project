# Sv_Ghng Field1/2/3 동적 컬럼명 9종 카탈로그 (OQ-RT-3)

> 작성: 2026-04-19 (C4 Phase 2 — `assume_default` 추정 매핑. 운영팀 확정 후 수정 가능)
> 출처: `legacy_delphi_source/legacy_source/Base01.pas` `_Sv_Ghng_` 헬퍼 (L8731~) + `Subu51.pas` 변경 트랜잭션
> 결정 근거: DEC-030 §OQ-RT-3, [`c4_returns_phase2_flow.md`](c4_returns_phase2_flow.md) §SQL-RT-39

## 0. 배경

레거시 `Sv_Ghng` 테이블의 INSERT/UPDATE 는 `Field1, Field2, Field3` 가 동적으로 다른 회계 컬럼명에 바인딩됨 (Delphi 의 `_Sv_Ghng_(St0,St1,St2,St3,Field1,Field2,Field3,Sq1,Sq2)` 헬퍼). Phase 1 는 변경(Sobo51)의 핵심 5종만 매핑. Phase 2 는 9종 추정 매핑 + `process_change` 가 모드별로 자동 선택.

## 1. 9종 컬럼 카탈로그 (assume_default)

| # | 컬럼 | 한글 의미 | 부호 | 사용 모드 (Subu*) | 회계 분류 |
| --- | --- | --- | --- | --- | --- |
| 1 | `Giqut` | 입고수량 | + | 입고 (Subu22) | 정품/상품 입고 |
| 2 | `Gsusu` | 매입수량 (수송수) | + | 입고 보강 | 직거래 매입 |
| 3 | `Gosum` | 출고수량 | − | 출고 (Subu21) | 정품/상품 출고 |
| 4 | `Gjqut` | 조정수량 | ± | **변경 (Subu51) — Phase 1 핵심** | 재고 조정 (오차 보정) |
| 5 | `Gsqut` | 매출수량 | − | 매출/판매 (Subu23 일반) | 매출 |
| 6 | `Goqut` | 폐기수량 | − | **폐기 (Subu34_4) — Phase 2 신규** | 손실 처분 |
| 7 | `Gbqut` | 변경수량 (분류 변환) | ± | **변경 (Subu51) — Phase 1 핵심** | 정품→비품 등 분류 변경 |
| 8 | `Gbsum` | 변경금액 (분류 변환) | ± | **변경 (Subu51) — Phase 1 핵심** | 변경 금액 누계 |
| 9 | `Gosum2` | 출고금액 보조 | − | 출고 (Subu21) — Phase 1 보류 | 출고 누계 금액 (Phase 3) |

**범례**: `+` = 재고 증가, `−` = 재고 감소, `±` = 양방향 (조정/변경).

## 2. 모드별 Field 매핑 (process_change 확장)

```python
# app/services/returns_service.py — Phase 2 process_change 매핑
SV_GHNG_FIELD_MAP: dict[str, tuple[str, str, str]] = {
    "regen":       ("Gjqut", "Gjsum", "Gosum"),    # 재생: 조정 + 출고
    "disassemble": ("Gjqut", "Gjsum", "Gosum"),    # 해체: 조정 + 출고
    "change":      ("Gbqut", "Gbsum", "Gjqut"),    # 변경: 변경 누계 + 조정 (Phase 1 핵심)
    # Phase 2 신규 (assume_default — 운영팀 확정 후 수정)
    "discard":     ("Goqut", "Gosum", "Gjqut"),    # 폐기 (Sobo34_4)
    "inbound":     ("Giqut", "Gsusu", "Gjqut"),    # 입고 누계 (C5 후속)
    "outbound":    ("Gosum", "Gsqut", "Gjqut"),    # 출고 누계 (C5 후속)
}
```

## 3. INSERT/UPDATE 패턴 (SQL-RT-39 보강)

```sql
-- INSERT (신규 변경 이력)
INSERT INTO Sv_Ghng (
    Gdate, Hcode, Gcode, Bcode,
    <Field1>, <Field2>, <Field3>,        -- 모드별 동적 컬럼명
    Time1, Reason
) VALUES (
    NOW(), :hcode, :gcode, :bcode,
    :val1, :val2, :val3,
    NOW(), :reason
)
-- 모드='change' 시 Field1=Gbqut, Field2=Gbsum, Field3=Gjqut
-- 모드='discard' 시 Field1=Goqut, Field2=Gosum, Field3=Gjqut
-- ...

-- UPDATE (동일 키 누적 — Max(Gdate) 비교 후 새 row 가 더 최신이면 누적)
UPDATE Sv_Ghng SET <Field1>=<Field1>+:val1,
                   <Field2>=<Field2>+:val2,
                   <Field3>=<Field3>+:val3,
                   Time2=NOW()
 WHERE <D_Select>
   AND Hcode=:hcode AND Gcode=:gcode AND Bcode=:bcode
   AND Gdate=:current_max_gdate
```

## 4. 동시성 보강 (OQ-RT-5 + SQL-RT-39)

```python
# Phase 2: SELECT FOR UPDATE → 충돌 시 ConcurrentChangeError → 409
async def _next_change_gdate(tx, hcode, gcode, bcode):
    rows = await tx.exec("""
        SELECT Max(Gdate) AS Gdate
          FROM Sv_Ghng
         WHERE Hcode=:hcode AND Gcode=:gcode AND Bcode=:bcode
         FOR UPDATE
    """, hcode=hcode, gcode=gcode, bcode=bcode)
    return rows[0]["Gdate"] if rows else None
```

## 5. 검증 가이드 (운영팀 협업)

- **확정 필요**: `Goqut/Gosum2` 의 정확한 의미 — 폐기인지 출고 보조인지 (현재 추정).
- **추가 가능**: 운영 데이터에 Field1/2/3 가 위 9종 외 다른 컬럼을 가리키는 경우 발견 시 `SV_GHNG_FIELD_MAP` 확장.
- **검증 스크립트**: `scripts/validate_sv_ghng_columns.py` (Phase 2 T5d 작성 — Sv_Ghng 의 실제 컬럼 카탈로그와 본 표 대조).

## 6. 영향 범위

- `app/services/returns_service.py` — `SV_GHNG_FIELD_MAP` 상수 + `process_change` 모드 분기
- `migration/contracts/return_receipt.yaml v1.1.0` — `endpoints[/returns/change]` 의 `mode` 파라미터 enum 확장 (regen/disassemble/change/discard)
- `test/test_c4_returns_phase2.py` — 9종 매핑 단위 테스트 (TC-RT-P2-23~25)

## 7. 참조

- Base01.pas `_Sv_Ghng_` 헬퍼 (L8731~)
- Subu51.pas L482/648/718 (변경 이력 검사)
- Phase 1 흐름: [`c4_returns_flow.md`](c4_returns_flow.md) §2.3
- Phase 2 흐름: [`c4_returns_phase2_flow.md`](c4_returns_phase2_flow.md) §1.C SQL-RT-39
- DEC-030 OQ-RT-3 정본 정의
