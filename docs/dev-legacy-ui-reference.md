# 레거시 델파이 화면 참조 가이드 (개발자용)

모던 앱 사이드바에는 **포팅 대상으로 등록된 폼만** [`FORM_REGISTRY`](../도서물류관리프로그램/frontend/src/lib/form-registry.ts) 기준으로 노출된다. 예전에 「입고관리(레거시)」「출고접수(레거시)」로 열던 **Subu12 / Subu13(Sobo12 / Sobo13)** 은 메뉴에서 제거되었으며, 업무 화면은 각각 **Sobo22 입고 접수**, **Sobo27 출고 접수** 포팅 라우트를 사용한다.

구 화면의 **위젯 트리·컬럼·탭 순서**를 확인할 때는 아래 산출물을 본다.

## Sobo12 / Subu12

| 목적 | 경로 (저장소 루트 기준) |
|------|-------------------------|
| dfm→HTML 등 가속기 산출물 | `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu12/Sobo12.html` 및 동일 폴더의 `Sobo12.form.json`, `Sobo12.tree.json`, `*.pas_analysis.json`, `*.meta.json` |
| 원본 dfm / pas | `legacy_delphi_source/legacy_source/Subu12.dfm`, `Subu12.pas` |
| 화면 카드 요약 | `analysis/screen_cards/Sobo12.md` |
| 정적 JSON (로컬 서버에서 직접 열람) | 앱 실행 후 `http://localhost:<port>/forms/Subu12/Sobo12.form.json` — **사이드바 미등록 시 앱 탭으로는 열리지 않음** |

## Sobo13 / Subu13

| 목적 | 경로 |
|------|------|
| 가속기 산출물 | `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu13/Sobo13.html` 및 동일 폴더 부속 파일 |
| 원본 dfm / pas | `legacy_delphi_source/legacy_source/Subu13.dfm`, `Subu13.pas` |
| 화면 카드 요약 | `analysis/screen_cards/Sobo13.md` |
| 정적 JSON | `http://localhost:<port>/forms/Subu13/Sobo13.form.json` (조건 동일) |

## 업무상 대체 포팅 화면 (권장 진입)

| 업무 | 레거시 폼 (참고용) | 모던 폼 ID | 라우트 | 레이아웃 매핑 노트 |
|------|-------------------|------------|--------|-------------------|
| 입고 접수 흐름 | Subu22 계열이 정식 매핑 | Sobo22 | `/inbound/receipts` | `analysis/layout_mappings/Sobo22.md` |
| 출고 접수 흐름 | Subu27 | Sobo27 | `/outbound/orders` | `analysis/layout_mappings/Sobo27.md` |

Subu12·Subu13 은 델파이 메뉴 구조상 출고관리 그룹에 붙어 있었으나, **가속기 HTML 표제/캡션**은 예를 들어 Sobo12 «입고처관리», Sobo13 «지역분류(시내+지방)» 등으로 나올 수 있다. 예전 UI 라벨「입고관리」「출고접수」와 문자열이 1:1로 같지 않을 수 있으니, 회귀·매핑은 **위젯 ID·`analysis` 문서**를 우선한다.

## 관련 규칙

- **DEC-028**: dfm→html 산출물을 공식 입력으로 쓰고, 모던 DOM에는 `data-legacy-id` 로 위젯 ID를 남긴다 (픽셀 좌표·구 폰트는 이식하지 않음).
