# 레이아웃 매핑: Sobo14 (도서 마스터) → 모던 `/master/book` (목록 + 상세)

DEC-028 — `Subu14/Sobo14.*` 단일 원천. C2(Sobo27.md) / C6(Sobo21.md) 11 섹션 구조 그대로 재사용.

## 0. 입력 산출물 (참고용)

- DFM HTML/JSON: [`tools/.../legacy_source_root/Subu14/Sobo14.html`](../../tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Subu14/Sobo14.html), `Sobo14.form.json`, `Sobo14.tree.json`, `Sobo14.meta.json`
- 변형 폴더: `Subu14_1/Sobo14_1.*` (도서 lookup picker — §9)
- 원 dfm: [`legacy_delphi_source/legacy_source/Subu14.dfm`](../../legacy_delphi_source/legacy_source/Subu14.dfm)
- 화면 카드: [`analysis/screen_cards/Sobo14.md`](../screen_cards/Sobo14.md), [`analysis/screen_cards/Sobo14_1.md`](../screen_cards/Sobo14_1.md)
- 모던 라우트:
  - 목록: [`도서물류관리프로그램/frontend/src/app/(app)/master/book/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/master/book/page.tsx)
  - 상세: [`도서물류관리프로그램/frontend/src/app/(app)/master/book/[gcode]/page.tsx`](../../도서물류관리프로그램/frontend/src/app/(app)/master/book/[gcode]/page.tsx)
- 계약: `migration/contracts/master_data.yaml` (`/api/v1/masters/book*`)

## 1. 의미 분기 — Sobo11 과 동일 패턴 (목록·상세 동시 윈도우 → 라우트 2개)

레거시 Sobo14 도 Sobo11 과 동일하게 **상단 그리드 + 하단 등록·수정 폼** 단일 윈도우. 모던에서는 `/master/book` (목록) + `/master/book/[gcode]` (상세) 로 분리.

| 영역 | 모던 라우트 |
| --- | --- |
| Panel001 / DBGrid101 | `/master/book` |
| Panel002 (Edit101~ + Button) | `/master/book/[gcode]` |

## 2. dfm 영역 인벤토리 (tree.json 기준)

- Sobo14 (root)
  - 코너: `CornerButton2/3/4`
  - 라벨: `Label002/003/309/100~110/300/301`
  - **Panel001** → `DBGrid101` (Gcode/Gname/Gjeja/Gisbn/Gdang/Gpost 등)
  - **Panel002** (등록·수정 폼)
    - Panel100 액션: `Button101` (등록), `Button102` (수정), `Button103` (삭제)
    - Panel101~119 (필드 컨테이너)
    - `Edit101~` (입력 시리즈 — 제목/저자/ISBN/단가/출판사/구분 등)

## 3. 상단 그리드 패널 위젯 매핑

목록 페이지 = `master/book/page.tsx`.

| dfm 위젯 | 의미 | 모던 위치 | `data-legacy-id` |
| --- | --- | --- | --- |
| `Sobo14.DBGrid101` | 도서 그리드 wrapper | `<DataGrid>` `<table>` | `Sobo14.DBGrid101` |
| `Sobo14.DBGrid101.GCODE` | 도서코드 | `<th>` (key=gcode) | `Sobo14.DBGrid101.GCODE` |
| `Sobo14.DBGrid101.GNAME` | 제목 | `<th>` (key=gname) | `Sobo14.DBGrid101.GNAME` |
| `Sobo14.DBGrid101.GJEJA` | 저자 | `<th>` (key=gjeja) | `Sobo14.DBGrid101.GJEJA` |
| `Sobo14.DBGrid101.GISBN` | ISBN | `<th>` (key=gisbn) | `Sobo14.DBGrid101.GISBN` |
| `Sobo14.DBGrid101.GDANG` | 단가 | `<th>` (key=gdang, align=right) | `Sobo14.DBGrid101.GDANG` |
| `Sobo14.DBGrid101.GPOST` | 출판사 코드 | `<th>` (key=gpost) | `Sobo14.DBGrid101.GPOST` |

## 4. 상세/등록 패널 위젯 매핑 (Panel002)

상세 페이지 = `master/book/[gcode]/page.tsx`.

| dfm 위젯 | 의미 | 모던 위치 | `data-legacy-id` |
| --- | --- | --- | --- |
| `Sobo14.Panel002` | 상세 폼 wrapper | `<div className="grid ...">` | `Sobo14.Panel002` |
| `Sobo14.Edit101` | 제목 (Gname) | `<Input>` 제목 | `Sobo14.Edit101` |
| `Sobo14.Edit102` | 저자 (Gjeja) | `<Input>` 저자 | `Sobo14.Edit102` |
| `Sobo14.Edit103` | ISBN (Gisbn) | `<Input>` ISBN | `Sobo14.Edit103` |
| `Sobo14.Edit104` | 단가 (Gdang) | `<Input type="number">` 단가 | `Sobo14.Edit104` |
| `Sobo14.Edit105` | 출판사 코드 (Gpost) | `<Input>` 출판사 코드 | `Sobo14.Edit105` |
| `Sobo14.Edit106` | 구분 (Gubun, read-only) | `<Input disabled>` 구분 | `Sobo14.Edit106` |
| `Sobo14.Edit107` | 분류명 (Gbun_name, read-only) | `<Input disabled>` 분류명 | `Sobo14.Edit107` |
| `Sobo14.Button101` | 등록 | — (1차 PATCH only, §6) | (미부착) |
| `Sobo14.Button102` | 수정/저장 | `<Button>저장 (수정)` | `Sobo14.Button102` |
| `Sobo14.Button103` | 삭제 | — (DEC-019, §6) | (미부착) |
| `Sobo14.FormClose` | 목록 복귀 | `<Button variant="ghost">목록` | `Sobo14.FormClose` |

## 5. 메모/기타

해당 없음 (Sobo14 메모 영역 없음).

## 6. out-of-scope 위젯 (1차 미부착)

- `CornerButton2/3/4`, 정적 라벨 전체
- `Sobo14.Button101`(Insert), `Sobo14.Button103`(Delete) — DEC-019
- 추가 보조 입력 (Sobo14 Edit108~)·Panel109~119 — phase2

## 7. deltas (모던 신설)

| 모던 위젯 | 사유 |
| --- | --- |
| 검색 입력 `<Input id="q">` (코드/제목/ISBN LIKE) | 단일 검색박스 — dfm 의 lookup 헬퍼 패턴과 다름, 신설 |
| 조회 버튼 | 페이징 트리거 (모던 신설) |
| `<DataGridPager>` | 서버 사이드 페이징 |

## 8. 이벤트 매핑

| dfm 이벤트 | 모던 핸들러 |
| --- | --- |
| `DBGrid101.OnDblClick` | `onRowClick={r => router.push("/master/book/{gcode}")}` |
| `Button102.OnClick` (수정) | `save()` → `masterApi.bookUpdate(gcode, body)` |
| `FormClose` | `router.push("/master/book")` |

## 9. 변형 차이 (`Sobo14` 본 vs `Sobo14_1`)

`Subu14_1/Sobo14_1.tree.json` 인벤토리:

```
Sobo14_1
  CornerButton1/2/9
  Label301/302/309
  Panel001
    Label100, Panel101, Edit201
```

→ Sobo14_1 은 **위젯이 사실상 Edit201 1개**인 lookup picker 미니 폼이다(도서 코드 입력 + 즉시 lookup 후 모폼 닫기). 모던에서는 별도 라우트로 노출하지 않고 자동완성/검색 박스 안에 흡수 (`master/book/page.tsx` 의 `<Input id="q">`). UI variant 0건(기능 차이만 — `data-legacy-id` 추가 부착 대상 없음).

## 10. 회귀 가드 체크리스트

- [ ] `master/book/page.tsx` / `[gcode]/page.tsx` 동작 변화 0
- [ ] tsc/eslint 경고 0 신규
- [ ] `test/test_pagination_contracts.py::C9MastersListPageContract::test_book` PASS
- [ ] `test/test_masters_q_search.py` PASS

## 11. 참조

- DEC-019, DEC-023, DEC-028, DEC-016/017/018
- HA-RET-01
- 화면 카드: `analysis/screen_cards/Sobo14.md`, `Sobo14_1.md`
- 계약: `migration/contracts/master_data.yaml` v1.1.0
- 테스트: 위 §10
- 선례: `Sobo27.md` (C2), `Sobo21.md` (C6)
