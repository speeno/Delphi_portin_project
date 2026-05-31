# 배본처관리 레거시 식별 노트 (2026-05-31)

## 배경

기초관리 메뉴를 레거시 스크린샷 순서로 복원하는 과정에서, `배본처관리` 항목의
정확한 `Menu### → TSobo##` 매핑을 재확인했다.

## 조사 범위

- 가속기 산출물: `tools/delphi_porting_accelerator/examples/generated/legacy_source_root/Chul/Subu00.tree.json`
- 메뉴 핸들러 인벤토리: `analysis/welove_chul_menu_handlers.json`
- 운영 메모(업무일지) 키워드: `배본처관리`, `물류코드`

## 관찰 결과

1. `Subu00.tree.json` 의 `기초관리(Menu100)` 하위에는 빌드 기준으로
   `거래처/입고처/도서/특별관리/출판사/환경설정/...` 이 존재하나, 동일 산출물에서
   `Caption='배본처관리'` 문자열은 직접 확인되지 않았다.
2. 메뉴 핸들러 인벤토리에서 `Menu106Click -> TSobo16` 이며,
   `Sobo16` 은 `G6_Ggeo` 기반으로 `거래처/도서` 링크와 `Grat1/Gssum` 을 다룬다.
3. 운영 메모의 `배본처관리` 설명은 반복적으로
   `거래처명 + 도서 + 물류코드` 입력/수정 흐름을 가리킨다.

## 결론(포팅 결정)

- 현재 저장소에서 `배본처관리` 전용 캡션 DFM 단일 증거가 부족하므로,
  기능적으로 가장 근접한 레거시 실체를 `Sobo16(G6_Ggeo)` 로 채택했다.
- 모던에서는 신규 경로 `/master/baebon` 을 추가하고,
  `masterApi.specialList/specialPatch` 를 사용해
  `거래처/도서/물류코드(gssum)` 중심 UI로 재표기한다.
- 기존 `/master/special` 은 유지(특별관리), 신규 `/master/baebon` 은
  동일 데이터원을 배본처 업무 용어로 노출하는 별도 진입점이다.

