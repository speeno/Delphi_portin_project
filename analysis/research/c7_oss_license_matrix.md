# C7 비-FastReport 트랙 — OSS 라이선스 매트릭스 (2026-04-20)

> **목적**: [`c7_oss_shortlist.md`](./c7_oss_shortlist.md) 의 12 후보별 라이선스 의무
> (저작권 표시 / NOTICE / 재배포 / Copyleft 전염성 등) 를 한 표로 정리.
> 본 트랙이 운영 incorporate 하기 전 **법적 게이트** — 위반 항목은 incorporate 금지.
>
> **본 트랙의 채택 정책 (전제)**:
> 1. 운영 코드에 incorporate 가능한 라이선스: MIT / BSD-2 / BSD-3 / Apache-2.0 / ISC.
> 2. LGPL: 동적 링크 가능 + 변경분 공개 의무 → **본 트랙은 incorporate ❌, 참조 only**.
> 3. GPL/AGPL: 전염성으로 본 시스템 전체 라이선스 변경 강요 → **incorporate 금지**.
> 4. 미확인 라이선스: incorporate 전 별도 조사 필수.

## 1. 매트릭스

| ID | 후보 | 라이선스 | Copyleft? | NOTICE 필수? | 저작권 표시 | 본 트랙 incorporate | 의무 이행 위치 |
|---|---|---|:---:|:---:|---|:---:|---|
| F-01 | FastReports/FreeReport | **BSD-2-Clause** | ❌ | ❌ | ✅ 필수 (소스 + 바이너리 양쪽) | ✅ (알고리즘 Python 포팅) | `frf_decoder.py` 헤더 주석 + `THIRD_PARTY_NOTICES.md` |
| F-02 | FastReports/FastReport (.NET) | **MIT** | ❌ | ⚠️ 권장 | ✅ 필수 (저작권 + 라이선스 텍스트 사본) | ❌ (참조 only — .NET 운영 도입 ❌) | 코드 incorporate 없음 → NOTICE 의무 없음. *문서 인용 시* 출처 표시만. |
| F-03 | FastReports/FastReport.Documentation | **MIT** | ❌ | ⚠️ 권장 | ✅ 필수 (인용 시 출처) | ✅ (스키마 명세 인용) | `frf_ir_schema.md` 머리말 + `THIRD_PARTY_NOTICES.md` |
| F-04 | LazReport `lr_class.pas` | **LGPL with linking exception** | ✅ (약) | ✅ | ✅ 필수 (소스 변경 시 공개) | ❌ (참조 only — 비교 디버깅 자료) | 코드 incorporate 없음 → 의무 없음 |
| D-01 | DSDfmParser | **(미확인)** | — | — | — | ❌ (배제) | n/a |
| D-02 | Dadie/dfm-toolkit | **(미확인)** | — | — | — | ❌ (배제) | n/a |
| D-03 | MHumm/BinaryDFMFinder | **(미확인)** | — | — | — | ❌ (배제) | n/a |
| D-04 | pyparsing/pyparsing | **MIT** | ❌ | ⚠️ 권장 | ✅ 필수 (incorporate 시) | ❌ (참조 only — 패턴만 차용) | 코드 incorporate 없음 → 의무 없음 |
| D-05 | lmbelo/python4delphi | **MIT** | ❌ | ⚠️ 권장 | ✅ 필수 | ❌ (운영 OPS=1, dev-only 도구로만 옵션) | dev 환경 incorporate 시 `requirements-dev.txt` + NOTICE |
| M-01 | lincolnloop/python-qrcode | **BSD-3-Clause** | ❌ | ❌ | ✅ 필수 (소스 + 바이너리 + 광고 금지 조항) | ✅ (`requirements.txt`) | `requirements.txt` + `THIRD_PARTY_NOTICES.md` (BSD-3 텍스트 전문) |
| M-02 | Kryvich's Delphi Reporter | **LGPL-3.0** | ✅ (강) | ✅ | ✅ 필수 | ❌ (참조 only — token 문법 1회 비교) | 코드 incorporate 없음 → 의무 없음 |
| M-03 | WeasyPrint Issue #718/#75 | (이슈 — N/A) | — | — | — | ❌ (코드가 아닌 가이드) | 패턴 차용, NOTICE 무관 |

## 2. 의무 이행 — 운영 incorporate 3 건의 NOTICE 정리

### 2.1. F-01 (FreeReport, BSD-2)

**의무**:
1. 저작권 보존: `Copyright (c) 1998-2008, Fast Reports Inc.`
2. 라이선스 텍스트 (BSD-2) 보존: 소스 배포 + 바이너리 배포 양쪽.

**이행 위치**: PoC 단계 — `debug/frf_decoder_poc.py` 헤더 주석. 운영 도입 시 —
`도서물류관리프로그램/THIRD_PARTY_NOTICES.md` 신규 파일.

**예시 헤더 주석**:
```python
"""
frf_decoder — Pascal `FR_Class.pas` (FreeReport 2.3) 의 `LoadFromStream`
알고리즘을 Python 으로 포팅. 원본은 FastReports/FreeReport (BSD-2-Clause).

Copyright (c) 1998-2008, Fast Reports Inc.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice, …
"""
```

### 2.2. F-03 (FastReport.Documentation, MIT)

**의무**:
1. 인용 시 출처 표시.
2. MIT 라이선스 텍스트 사본 동봉 (운영 incorporate 시).

**이행 위치**: `analysis/print_specs/frf_ir_schema.md` 머리말 — "본 스키마는
FastReports/FastReport.Documentation (MIT) 의 `ReportObjects.md` 등 명세를 참조함".

### 2.3. M-01 (python-qrcode, BSD-3)

**의무**:
1. 저작권 보존.
2. BSD-3 의 *3rd 조항*: 기여자/저작자명을 광고에 사용 금지.
3. 라이선스 텍스트 보존.

**이행 위치**: `requirements.txt` 명시 + `THIRD_PARTY_NOTICES.md` 에 BSD-3 전문 동봉.

## 3. 결정 요약

- **운영 incorporate 가능 / 의무 명확**: F-01 (BSD-2), F-03 (MIT), M-01 (BSD-3) — 3 건.
- **참조 only / 의무 없음**: F-02, D-04, F-04, M-02, M-03 — 5 건.
- **dev-only 옵션 (운영 ❌)**: D-05 (MIT) — 1 건.
- **배제** (라이선스 미확인 + 본 트랙 가치 낮음): D-01, D-02, D-03 — 3 건.

> **검증 게이트**: 회귀 테스트팩 `test_c7_print_phase3_*` 의 정적 검사에 `frf_decoder.py`
> 와 `requirements.txt` 양쪽에서 위 의무 텍스트 / 출처 표시가 누락되지 않았는지
> 자동 점검을 추가 (regression-gates 단계에서 구현).

## 4. 변경 이력

| 일자 | 버전 | 변경 |
|---|---|---|
| 2026-04-20 | v0 | 초기 12 건 후보 라이선스 정리, 3 분류와 incorporate 의무 동결 |
