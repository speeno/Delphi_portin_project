# 레이아웃 매핑: Sobo45_1 (청구서관리 — 택배 변형) → 모던 `/settlement/billing?variant=takbae` [C5 Phase 1]

> 본 노트는 [`Sobo45_billing.md`](Sobo45_billing.md) 의 **택배 변형 diff 만** 기록한다. 위젯/이벤트/마감 정책은 본 폼과 동일.

DEC-019 — 변형 차이는 코드 분기 금지, 단일 모던 컴포넌트 + 데이터 주도 분기 (C9 Sobo39 4 변종 통합 패턴 재사용).

## 0. 입력 산출물

- 변형 본 폼: [`tools/.../legacy_source_root/Subu45_1/Sobo45_1.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu45_1/Sobo45_1.html) + `.form.json` + `.tree.json` + `.pas_analysis.json`
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu45_1.dfm`](../../legacy_delphi_source/legacy_source/Subu45_1.dfm)
- 원 pas: [`legacy_delphi_source/legacy_source/Subu45_1.pas`](../../legacy_delphi_source/legacy_source/Subu45_1.pas) — `nForm := '45_1'`, 폼 로컬 ClientDataSet `T4_Sub51/52` 정의
- 본 폼 매핑: [`Sobo45_billing.md`](Sobo45_billing.md)

## 1. 핵심 차이 (Sobo45 vs Sobo45_1)

| 분류 | Sobo45 본 (일반) | Sobo45_1 (택배) |
| --- | --- | --- |
| 데이터셋 | `Base10.T4_Sub11/12` (전역 DataModule) | 폼 로컬 `T4_Sub51/52` ClientDataSet — `mSqry := nil` 우회 |
| 폼 식별자 | `nForm := '45'` | `nForm := '45_1'` (라우터/저장소 분기에 사용) |
| 컬럼 5~7 (출고내역 vs 택배비) | `GQUT5` 반품내역\|총부수, `GQUT6/7` 반품수거 시내/지방 | `GQUT5` 택배비\|大, `GQUT6` 택배비\|中, `GQUT7` 택배비\|小 |
| 컬럼 시각화 | 단가/수량 위주 | 택배비 합계(大+中+小) 푸터 SUM 추가 |
| 발송비 NAME1/NAME2 | 지역·화물명 (출판물 흐름 라벨) | 택배사·운송장 라벨 (운영 의미 차이 — OQ-ST-4) |

## 2. 컬럼 매핑 (DBGrid201 — 차이 부분만)

| dfm FieldName | Sobo45 본 | Sobo45_1 (택배) | 모던 컬럼 (variant=takbae) | data-legacy-id |
| --- | --- | --- | --- | --- |
| `GQUT5` | 반품내역\|총부수 | 택배비\|大 | `<th>大</th>` (택배비 그룹) | `Sobo45_1.DBGrid201.GQUT5` |
| `GQUT6` | 반품수거\|시내 | 택배비\|中 | `<th>中</th>` | `Sobo45_1.DBGrid201.GQUT6` |
| `GQUT7` | 반품수거\|지방 | 택배비\|小 | `<th>小</th>` | `Sobo45_1.DBGrid201.GQUT7` |

> 그 외 14컬럼(`GDATE/GQUT1~4/NAME1/NAME2/GNAME/GSQUT/GSSUM/YESNO`) 및 좌측 출판사 그리드(`HCODE/HNAME`) 는 본 폼과 동일.

## 3. 데이터 주도 분기 — contract `customer_variants` 항목

```yaml
# settlement_billing.yaml (T3 발췌)
customer_variants:
  takbae:
    description: "택배 전용 변형 (Sobo45_1)"
    columns_diff:
      GQUT5: { from: "반품내역|총부수", to: "택배비|大" }
      GQUT6: { from: "반품수거|시내",   to: "택배비|中" }
      GQUT7: { from: "반품수거|지방",   to: "택배비|小" }
    dataset_scope: "form_local"   # T4_Sub51/52
    nForm: "45_1"
```

## 4. 회귀 가드 체크리스트

- [ ] 단일 컴포넌트 — `if (variant === 'takbae') ...` 의 분기는 컬럼 헤더/푸터 SUM 라벨에만 한정
- [ ] DOM 의 `data-legacy-id` 가 본 폼은 `Sobo45.*`, 변형은 `Sobo45_1.*` 로 정확히 분리
- [ ] 마감/확정/취소 액션은 본 폼과 동일 contract 액션 (`confirm_billing`, `cancel_billing`) 사용 — variant 별 라우터 신설 금지
- [ ] OQ-ST-4 (택배비 의미) 답변 후 필요 시 `dataset_scope` / 컬럼 SUM 정책 갱신

## 5. 참조

- DEC-019: customer_variants — 코드 분기 금지
- DEC-028: dfm 산출물 영구 입력
- 본 폼: [`Sobo45_billing.md`](Sobo45_billing.md)
- contract: [`migration/contracts/settlement_billing.yaml`](../../migration/contracts/settlement_billing.yaml) (T3)
- 선례: `Sobo23_1.md` (반품 라인 다이얼로그 변형), C9 Sobo39 4 변종 통합 (참고)
