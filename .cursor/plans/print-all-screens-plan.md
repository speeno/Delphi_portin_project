# 전체 화면 프린트 기능 포팅 개발 계획

## 1. 현황 요약

### 1.1 레거시 프린트 아키텍처

레거시 델파이 앱의 프린트 기능은 **중앙 허브 패턴**으로 구현되어 있다.

- **`Tong04.pas` (`TTong40`)**: `PrinTing00(St0..St9)` 진입점 → `St0` 번호로 화면 분기 → 해당 FRF 파일 로드 → FastReport `ShowReport`/`PrepareReport` 호출
- **`Print_XX_YY` 함수**: 총 **140+개** 프로시저 (11~68번 그룹 + 99번 특수). `XX` = 화면 그룹, `YY` = `_01` Preview / `_02` Direct Print 패턴
- **FRF 서식 파일**: `Report\Report_X_YY.frf` 형식. 고유 파일 약 **90종**, 변형 포함 약 170종이 `Tong04.pas`에서 참조됨
- **호출 화면**: `Subu*.pas` 약 80개 유닛에서 `Tong40.PrinTing00()` 또는 `Tong40.Print_XX_YY()` 를 호출

### 1.2 FRF 자산 변환 상태

| 지표 | 값 |
|---|---|
| 총 .frf 변환 완료 (IR/HTML) | **1,744건** |
| 고유 Report ID 종류 | **~170종** (변형 포함) |
| 좌표 복원 평균 | 0.9887 |
| 바인딩 충진 평균 | 0.5696 |
| 운영 등록 완료 (auto/) | 2건 (`Report_2_11`, `Report_1_21`) |
| 화이트리스트 등록 | 8 form_id (`label_form_1..5`, `sales_statement_base`, `outbound_statement_base`, `return_receipt_base`) |

### 1.3 현재 모던 앱 프린트 구현 상태

| 양식 ID | 화면 | API 엔드포인트 | FRF Report | 상태 |
|---|---|---|---|---|
| **P1-A** | Sobo46 청구서 | (settlement 라우터 내부) | Report_4_95/96 | ✅ HTML 빌더 존재 |
| **P1-B** | Sobo49 세금계산서 | (settlement 라우터 내부) | Report_4_93/94 | ✅ HTML 빌더 존재 |
| **P1-C** | Sobo27 출고 거래명세서 | `/print/outbound-statement/{key}.pdf` | Report_4_51 | ✅ **dual style** (legacy+modern) |
| **P1-D** | Sobo23 반품 영수증 | `/print/return-receipt/{key}.pdf` | Report_2_14 | ✅ **dual style** (legacy+modern) |
| **P1-E** | Sobo21 거래명세서 | `/print/sales-statement/{key}.pdf` | Report_2_11 | ✅ FRF auto + modern fallback |
| **P1-F** | Seep13 라벨 | `/print/label/{key}.pdf` | Report_1_21~25 | ✅ form 1~5 + auto IR registry |

---

## 2. 미구현 프린트 기능 전수 조사

### 2.1 Tong04.pas Print 함수 ↔ FRF ↔ 화면 매핑 (전체)

`Print_XX_01` = 미리보기(Preview), `Print_XX_02` = 직접 인쇄(Print)

| 그룹 | Print 함수 | FRF Report | 화면(Sobo/Subu) | 용도 | 현재 상태 |
|---|---|---|---|---|---|
| **11** | Print_11_01/02 | Report_1_11 | Seep11 (도서 바코드) | 도서 바코드 출력 | ❌ 미구현 |
| **12** | Print_12_01/02 | Report_1_21~25 | Seep13 (라벨) | 배송 라벨 인쇄 | ✅ P1-F |
| **13** | Print_13_01/02 | Report_1_21~25 | Seep13 (라벨 변형) | 라벨 변형 | ✅ P1-F |
| **14** | Print_14_01/02/11 | Report_1_40, 1_61, 1_62, 1_71 | Subu14/Subu17 (도서 마스터) | 도서 목록 출력 | ❌ 미구현 |
| **15** | Print_15_01/02 | (Canvas 직접 출력) | Subu15 (출판사) | 출판사 목록 | ❌ 미구현 |
| **16** | Print_16_01/02 | (Canvas 직접 출력) | Subu16 (특별관리) | 특별관리 목록 | ❌ 미구현 |
| **17** | Print_17_01/02/03 | (Canvas 직접 출력) | Subu17/17_1 (도서 관리) | 도서 관리 목록 | ❌ 미구현 |
| **21** | Print_21_01/02 | Report_2_11, 2_13, 2_19 | Sobo21 (거래명세서) | 거래명세서 출력 | ✅ P1-E |
| **22** | Print_22_01/02 | Report_2_12 | Sobo22 (입고명세서) | 입고 명세서 출력 | ❌ 미구현 |
| **23** | Print_23_01/02 | Report_2_14 | Sobo23 (반품명세서) | 반품 영수증 출력 | ✅ P1-D |
| **24** | Print_24_01/02 | Report_2_41~46 | Sobo24 (일별 출고내역) | 일별 출고 내역서 | ❌ 미구현 |
| **25** | Print_25_01/02 | Report_2_51~52 | Sobo25 (기간별 출고) | 기간별 출고 내역서 | ❌ 미구현 |
| **26** | Print_26_01/02 | Report_2_61~62 | Sobo26 (출고접수현황) | 출고 접수 현황 | ❌ 미구현 |
| **27** | Print_27_01/02 | Report_2_71~72 | Sobo27_1 (출고현황 변형) | 출고 현황 변형 | ⚠️ 부분 (P1-C는 Report_4_51) |
| **28** | Print_28_01/02 | Report_2_83~84 | Sobo28 (출고택배관리) | 택배 관리 출력 | ❌ 미구현 |
| **29** | Print_29_01/02 | — | Sobo29 | (미사용) | ⛔ 스킵 |
| **31** | Print_31_01/02 | Report_3_11~12 | Sobo31 (도서별 수불원장) | 수불원장 출력 | ❌ 미구현 |
| **32** | Print_32_01/02 | Report_3_21~22 | Sobo32 (재고 현황) | 재고 현황 출력 | ❌ 미구현 |
| **33** | Print_33_01~04 | Report_3_31~34 | Sobo33 (재고 조정) | 재고 조정 출력 | ❌ 미구현 |
| **34** | Print_34_01/02/05/06 | Report_2_41, 3_41~45, 3_52 | Sobo34 (도서별 매출현황) | 매출 현황 출력 | ❌ 미구현 |
| **35** | Print_35_01/02 | Report_3_41(재사용) | Sobo35 (반품재고-폐기) | 반품 재고 출력 | ❌ 미구현 |
| **36** | Print_36_01/02 | Report_3_61~62 | Sobo36 (일별 입금내역) | 입금 내역 출력 | ❌ 미구현 |
| **37** | Print_37_01/02 | Report_3_71 | Sobo37 (기간별 입금) | 기간별 입금 출력 | ❌ 미구현 |
| **38** | Print_38_01/02 | — | Sobo38 (FTP 수신) | (미사용) | ⛔ 스킵 |
| **39** | Print_39_01~21 | Report_3_91~92, 5_91~92 | Sobo39 (출고현황 집계) | 출고 집계 출력 (11종 변형) | ❌ 미구현 |
| **41** | Print_41_01/02 | Report_4_11~12 | Sobo41 (입금 관리) | 입금 관리 출력 | ❌ 미구현 |
| **42** | Print_42_01/02 | Report_4_21~22 | Sobo42 (입금 관리 변형) | 입금 관리 변형 | ❌ 미구현 |
| **43** | Print_43_01/02 | Report_4_31~32 | Sobo43 (매출채권 현황) | 매출채권 출력 | ❌ 미구현 |
| **44** | Print_44_01/02 | Report_4_41~42 | Sobo44 (미수금 현황) | 미수금 출력 | ❌ 미구현 |
| **45** | Print_45_01/02 | Report_4_51~52 (대량) | Sobo45 (청구서 관리) | 청구서 출력 | ⚠️ P1-A는 별도 빌더 |
| **46** | Print_46_01/02 | Report_4_51 (재사용, 대량) | Sobo46 (청구서 출력) | 청구서 대량 출력 | ⚠️ P1-A는 별도 빌더 |
| **47** | Print_47_01/02 | Report_4_71~72 | Sobo47 (청구금액 년월) | 청구금액 출력 | ❌ 미구현 |
| **48** | Print_48_01/02 | Report_4_81, 4_92 | Sobo48 (미정산 현황) | 미정산 출력 | ❌ 미구현 |
| **49** | Print_49_01/02 | Report_4_91~92 | Sobo49 (세금계산서) | 세금계산서 출력 | ⚠️ P1-B는 별도 빌더 |
| **51** | Print_51_01/02 | Report_5_21, 5_12 | Sobo51 (반품재고 변경) | 반품재고 출력 | ❌ 미구현 |
| **52** | Print_52_01/02 | Report_5_21~22 | Sobo52 (일별 반품) | 일별 반품 출력 | ❌ 미구현 |
| **53** | Print_53_01/02 | Report_5_31~32 | Sobo53 (기간별 반품) | 기간별 반품 출력 | ❌ 미구현 |
| **54** | Print_54_01/02 | Report_5_41~42 | Sobo54 (일별 입고) | 일별 입고 출력 | ❌ 미구현 |
| **55** | Print_55_01~04 | Report_5_51~54 | Sobo55 (기간별 입고) | 기간별 입고 출력 | ❌ 미구현 |
| **56** | Print_56_01/02 | Report_5_61~63 | Sobo56 (입고집계) | 입고 집계 출력 | ❌ 미구현 |
| **57** | Print_57_01/02 | Report_5_71~72 | Sobo57 (기간별 입고) | 기간별 입고 변형 | ❌ 미구현 |
| **58** | Print_58_01/02 | Report_5_81~82 | Sobo58 (입고현황) | 입고 현황 출력 | ❌ 미구현 |
| **59** | Print_59_01/02/11/12 | Report_5_63~64, 2_46 | Sobo59 (입고 분석) | 입고 분석 출력 | ❌ 미구현 |
| **61** | Print_61_01/02 | Report_6_11~12 | Sobo61 (도서별 판매) | 도서별 판매 출력 | ❌ 미구현 |
| **62** | Print_62_01/02 | Report_6_21~22 | Sobo62 (거래처 판매) | 거래처별 판매 출력 | ❌ 미구현 |
| **63** | Print_63_01/02 | Report_6_91~93 | Sobo63 | 집계 출력 | ❌ 미구현 |
| **64** | Print_64_01/02 | Report_6_42, 6_52 | Sobo64 | 내역 출력 | ❌ 미구현 |
| **65** | Print_65_01/02 | Report_6_51~52 | Sobo65 | 내역 출력 | ❌ 미구현 |
| **66** | Print_66_01/02 | Report_6_61~62 | Sobo66 | 통계 출력 | ❌ 미구현 |
| **67** | Print_67_01/02 | Report_6_71~72 | Sobo67 (출고현황) | 출고 현황 출력 | ❌ 미구현 |
| **68** | Print_68_01/02 | Report_6_81~82 | Sobo68 | 통계 출력 | ❌ 미구현 |
| **99** | Print_99_01/02 | Report_3_91~92 | Sobo99 (관리 리포트) | 관리 리포트 | ❌ 미구현 |

### 2.2 `PrinTing00` 직접 호출 (자체 인쇄 포함 화면)

`PrinTing00(St0='24', ...)` 등으로 인쇄를 직접 호출하는 화면:

| 호출 화면 | St0 값 | 의미 | 비고 |
|---|---|---|---|
| Subu27/27_1 (출고접수) | '24' | 일별 출고내역서 | 출고 확정 시 자동 인쇄 |
| Subu26 (출고접수현황) | '24' | 일별 출고내역서 | 상동 |
| Subu96/97 (변형) | '24' | 일별 출고내역서 | 고객사 분기 |
| Subu91 | '21' | 거래명세서 | 조회 후 인쇄 |
| Subu49 | '49' | 세금계산서 | 발행 시 인쇄 |
| Subu28/98 | '32' | 재고 현황 | 택배 관련 출력 |
| Subu34/34_1~4 | Print_56_01/02 | 입고집계 | F2/F3 단축키 |
| Subu33/32 | Print_56_01/02 | 입고집계 | F2/F3 단축키 |
| Subu59_2/3 | '24' | 일별 출고내역서 | 입고 분석 화면에서 |

---

## 3. 개발 계획 — 단계별 로드맵

### 3.0 설계 원칙

1. **이중 출력 방식 (Dual Print Style)**: Sobo27 패턴 재사용. 모든 양식에 `style=legacy|modern` 파라미터 제공
2. **FRF 참조 전용**: DEC-039에 따라 `.frf`는 참조용. IR/HTML은 `debug/output/frf_converted_all`에 보관, 운영 등록은 화이트리스트 PR 단위
3. **공통 파이프라인 재사용**: `print_service.render_pdf()` + `print_template_registry` + `print_context_adapters` + `print_ir_compiler`
4. **신규 SQL 최소화**: 기존 list/detail API 응답을 재사용하는 `context_adapter` 패턴
5. **멀티 DB 호환**: MySQL 3.23 호환 필수 (workspace rule)

### Phase 1 — 기존 구현 보강 (우선순위: 높음)

이미 API가 존재하는 화면의 legacy 스타일 지원 및 회귀 보강.

| 작업 | 대상 | FRF | 산출물 | 추정 |
|---|---|---|---|---|
| **T1-1** P1-D 반품 영수증 dual style | Sobo23 | Report_2_14 | ✅ `style=legacy` 추가, context adapter, 화이트리스트 등록 | 0.5일 |
| **T1-2** P1-A 청구서 dual style | Sobo46 | Report_4_95/96 | ⚠️ 보류: legacy 정본/IR 매핑 재확정 필요 | 1일 |
| **T1-3** P1-B 세금계산서 dual style | Sobo49 | Report_4_93/94 | ⚠️ 보류: legacy 정본/IR 매핑 재확정 필요 | 1일 |
| **T1-4** P1-F 라벨 변형 완성 | Seep13 | Report_1_21~25 | ✅ 5종 라벨 variant 등록 | 0.5일 |

### Phase 2 — 핵심 업무 화면 프린트 (우선순위: 높음)

핵심 시나리오(C2~C6)에 속하는 화면 중 프린트가 필수인 것.

| 작업 | 대상 | FRF | 시나리오 | 산출물 | 추정 |
|---|---|---|---|---|---|
| **T2-1** 입고 명세서 | Sobo22 | Report_2_12 | C3 입고 | 신규 API + HTML 빌더 + context adapter | 1.5일 |
| **T2-2** 일별 출고 내역서 | Sobo24 | Report_2_41~46 | C2 출고 | 자동 인쇄 연동 (PrinTing00 '24') | 2일 |
| **T2-3** 기간별 출고 내역서 | Sobo25 | Report_2_51~52 | C2 출고 | 신규 API | 1일 |
| **T2-4** 출고 접수 현황 | Sobo26 | Report_2_61~62 | C2 출고 | 기존 화면에 인쇄 버튼 추가 | 1일 |
| **T2-5** 출고 택배 관리 | Sobo28 | Report_2_83~84 | C2 출고 | 택배 관리 출력 | 1일 |
| **T2-6** 입금 관리 출력 | Sobo41/42 | Report_4_11~22 | C5 정산 | 입금 명세 출력 | 1.5일 |
| **T2-7** 매출채권/미수금 | Sobo43/44 | Report_4_31~42 | C5 정산 | 채권 현황 출력 | 1일 |
| **T2-8** 청구금액 년월 | Sobo47 | Report_4_71~72 | C5 정산 | 청구금액 출력 | 0.5일 |

### Phase 3 — 조회/분석 화면 프린트 (우선순위: 중간)

C6 읽기 전용 조회 화면의 프린트 기능.

| 작업 | 대상 | FRF | 산출물 | 추정 |
|---|---|---|---|---|
| **T3-1** 도서별 수불원장 | Sobo31 | Report_3_11~12 | 신규 API | 1일 |
| **T3-2** 재고 현황 | Sobo32 | Report_3_21~22 | 신규 API | 1일 |
| **T3-3** 재고 조정 | Sobo33 | Report_3_31~34 | 4종 변형 지원 | 1.5일 |
| **T3-4** 도서별 매출현황 | Sobo34 | Report_3_41~45 | 5종 변형 (일/월/연/총) | 2일 |
| **T3-5** 반품재고 | Sobo35/51 | Report_3_41(재사용), 5_12~21 | 2개 화면 통합 | 1일 |
| **T3-6** 입금 내역 | Sobo36/37 | Report_3_61~62, 3_71 | 일별/기간별 입금 | 1일 |
| **T3-7** 출고 집계 (대형) | Sobo39 | Report_3_91~92, 5_91~92 | **11종 변형** — 데이터 주도 통합 | 3일 |
| **T3-8** 도서별 판매 통계 | Sobo61/62 | Report_6_11~22 | 판매 통계 출력 | 1.5일 |
| **T3-9** 출고현황 조회 | Sobo67 | Report_6_71~72 | 기존 화면 프린트 추가 | 1일 |
| **T3-10** 기타 통계 | Sobo63~66,68 | Report_6_4x~9x | 잔여 통계 출력 | 3일 |

### Phase 4 — 입고/반품 분석 프린트 (우선순위: 보통)

| 작업 | 대상 | FRF | 산출물 | 추정 |
|---|---|---|---|---|
| **T4-1** 일별/기간별 반품 | Sobo52/53 | Report_5_21~32 | 반품 내역서 출력 | 1.5일 |
| **T4-2** 일별/기간별 입고 | Sobo54/55 | Report_5_41~54 | 입고 내역서 출력 (4종) | 2일 |
| **T4-3** 입고 집계/현황 | Sobo56/57/58 | Report_5_61~82 | 입고 집계 출력 | 2일 |
| **T4-4** 입고 분석 | Sobo59 | Report_5_63~64, 2_46 | 분석 리포트 | 1일 |

### Phase 5 — 특수 출력 (우선순위: 낮음)

| 작업 | 대상 | FRF | 산출물 | 추정 |
|---|---|---|---|---|
| **T5-1** 도서 바코드 | Seep11/Seok03 | Report_1_11 | 바코드 이미지 생성 | 1일 |
| **T5-2** 도서 목록 출력 | Subu14/17 | Report_1_40~71 | 마스터 목록 출력 | 1일 |
| **T5-3** Canvas 직접 출력 | Subu15/16/17 | (Canvas) | Printer.Canvas → HTML 변환 | 2일 |
| **T5-4** 관리 리포트 | Sobo99 | Report_3_91~92 | 관리용 출력 | 0.5일 |

---

## 4. 기술 구현 계획

### 4.1 백엔드 아키텍처 확장

#### 4.1.1 프린트 라우터 그룹화

```
print.py (현재, P1 양식)
print_reports.py (신규, Phase 2~4 리포트 양식)
print_master.py (신규, Phase 5 마스터/바코드)
```

각 라우터는 동일한 패턴을 따른다:
1. URL 파싱 + `style`/`variant` 파라미터 수신
2. 기존 service의 `list`/`detail` 함수로 데이터 조회
3. `context_adapter`로 FRF/modern 공통 컨텍스트 생성
4. `style=legacy` → `try_render_with_ir(force=True)`, 실패 시 modern fallback
5. `style=modern` → 수동 HTML 빌더
6. `print_service.render_pdf(html)` → PDF 응답

#### 4.1.2 Context Adapter 확장

`print_context_adapters.py`에 양식별 함수 추가:

```python
def inbound_receipt_context(detail: dict) -> dict:  # Sobo22
def daily_outbound_context(detail: dict) -> dict:   # Sobo24
def period_outbound_context(detail: dict) -> dict:  # Sobo25
def settlement_context(detail: dict) -> dict:       # Sobo41/42
def inventory_ledger_context(detail: dict) -> dict:  # Sobo31
# ... 양식별 추가
```

#### 4.1.3 Template Registry 확장

`_WHITELIST`에 양식별 `form_id` 추가:
- FRF IR 파일이 품질 게이트를 통과하면 (`binding_fill ≥ 0.5`, `coord_recovery ≥ 0.95`) 화이트리스트 등록
- 미통과 시 modern HTML 빌더만 사용 (FRF 서식은 참조 문서로만 활용)

### 4.2 프런트엔드 공통 패턴

#### 4.2.1 프린트 버튼 컴포넌트

```typescript
// components/PrintButtons.tsx
interface PrintButtonsProps {
  formType: string;
  orderKey: string;
  serverId: string;
  supportLegacy?: boolean;
}
```

- `supportLegacy=true`이면 "기존 서식 PDF" / "새 서식 PDF" 이중 버튼
- `supportLegacy=false`이면 단일 "PDF 다운로드" 버튼

#### 4.2.2 print-api.ts 확장

```typescript
// 범용 PDF URL 생성
export function reportPdfUrl(
  formType: ReportFormType,
  key: string,
  serverId: string,
  options?: { style?: PrintStyle; variant?: string }
): string;
```

### 4.3 FRF 화이트리스트 등록 워크플로

```
1. debug/output/frf_converted_all 에서 해당 Report_X_YY.ir.json 확인
2. 품질 점수 확인 (binding_fill, coord_recovery)
3. context adapter 작성 (detail → FRF placeholder 매핑)
4. print_template_registry._WHITELIST에 등록
5. 필요 시 auto/ 폴더에 IR 복사
6. 회귀 테스트 추가
```

---

## 5. 화면별 프린트 버튼 UI 위치

| 화면 | 트리거 | 레거시 위치 | 모던 위치 |
|---|---|---|---|
| 거래명세서 (Sobo21) | 버튼 클릭 | 상단 툴바 | 상세 페이지 헤더 |
| 입고명세서 (Sobo22) | 버튼 클릭 | 상단 툴바 | 상세 페이지 헤더 |
| 반품명세서 (Sobo23) | 버튼 클릭 | 상단 툴바 | 상세 페이지 헤더 |
| 출고접수 (Sobo27) | 확정 시 + 수동 | `PrinTing00('24')` | 출고 상세 → 인쇄 |
| 일별 출고내역 (Sobo24) | 자동 + 버튼 | 상단 툴바 | 목록 상단 |
| 청구서 (Sobo46) | 버튼 클릭 | 상단 툴바 | 청구서 상세 |
| 세금계산서 (Sobo49) | 발행 시 | `PrinTing00('49')` | 상세 페이지 |
| F2/F3 단축키 화면 | 키보드 | Subu32~34 | `Ctrl+P` 또는 버튼 |

---

## 6. 회귀 테스트 전략

### 6.1 테스트 계층

| 계층 | 범위 | 파일 |
|---|---|---|
| L1 PDF 시그니처 | `%PDF-` + Content-Type 검사 | `test/test_c7_print_phase1.py` 확장 |
| L2 텍스트 추출 | pypdf로 헤더/합계 텍스트 검증 | `test/test_c7_print_phase2.py` 신설 |
| L3 스타일 분기 | `style=legacy` → `frf-obj` 클래스, `style=modern` → `<table>` | 동일 파일 |
| L4 데이터 정합 | context adapter 출력 vs API detail 필드 매핑 | `test/test_print_context_adapters.py` |
| L5 정적 검사 | `data-legacy-id` 누락 검사 | DEC-028 가드 |

### 6.2 FRF 품질 게이트

신규 화이트리스트 등록 시:
- `coord_recovery ≥ 0.95` → 통과
- `binding_fill ≥ 0.5` → 통과
- `binding_fill < 0.3` → legacy style 미제공 (modern only)
- 중간(0.3~0.5) → 수동 검토 후 결정

---

## 7. 일정 요약

| Phase | 범위 | 화면 수 | 추정 기간 |
|---|---|---|---|
| Phase 1 | 기존 구현 보강 | 4건 보강 | 3일 |
| Phase 2 | 핵심 업무 프린트 | 8건 신규 | 10일 |
| Phase 3 | 조회/분석 프린트 | 10건 신규 | 16일 |
| Phase 4 | 입고/반품 분석 | 4건 신규 | 6.5일 |
| Phase 5 | 특수 출력 | 4건 신규 | 4.5일 |
| **합계** | | **30건** | **~40일** |

---

## 8. 전제 조건 및 의존성

| 항목 | 상태 | 차단 여부 |
|---|---|---|
| WeasyPrint 설치 + DYLD 전파 | ✅ 해결 | — |
| NanumGothic 폰트 번들 | ✅ 준비 | — |
| FRF 1,744건 IR/HTML 변환 | ✅ 완료 | — |
| 각 화면 API (list/detail) | ⚠️ 일부 미구현 | Phase 2~4 착수 시 선행 필요 |
| 멀티 DB 호환 (MySQL 3.23) | ✅ 프레임워크 준비 | 신규 API SQL 작성 시 적용 |
| 프런트엔드 화면 포팅 | ⚠️ 진행 중 | 프린트 버튼은 화면 포팅 완료 후 추가 |

---

## 9. 참조 결정사항

| DEC | 제목 | 관련 |
|---|---|---|
| DEC-004 | 하이브리드 인쇄 (브라우저 + 서버 PDF) | 전체 방향 |
| DEC-028 | dfm 산출물 영구 입력 | data-legacy-id 의무 |
| DEC-037 | PDF 엔진 = WeasyPrint 단일 | 기술 선택 |
| DEC-038 | Phase 1 라벨 1종 한정 | Phase 1 범위 |
| DEC-039 | .frf 참조용 카탈로그 | FRF 운영 정책 |
| DEC-046 | 단일 원천 (frf-html-form-catalog) | 변환 자산 관리 |
