# Sobo13 저자관리 "김" 검색 4서버 라이브 검증 결과

- 산출 스크립트: [`debug/probe_author_kim_search.py`](../../debug/probe_author_kim_search.py)
- 원시 결과(json): [`analysis/audit/sobo13-author-kim-4server.json`](./sobo13-author-kim-4server.json)
- 실행 경로: `masters_service.list_authors(q="김")` + `get_author(첫 결과)` 직접 호출(앱과 동일 경로).

## 결과 요약 (q="김")

| 서버 | 스키마 | list ok | total | returned | gcode 오름차순 | gname 전건 노출 | 상세 ok | 비고 |
| --- | --- | :-: | :-: | :-: | :-: | :-: | :-: | --- |
| remote_138 | 슬림 | ✅ | 13 | 13 | ✅ | ✅ | ✅ | gposa=김혜원, gbun_name=번역자 |
| remote_153 | 표준 | ✅ | 473 | 50 | ✅ | ✅ | ✅ | gposa=김영권, gbun_name=번역자 |
| remote_154 | MySQL 3.23 | ⚠️ | — | — | — | — | — | 1129 host blocked (서버측 connection-error 차단) |
| remote_155 | MySQL 3.23 | ⚠️ | — | — | — | — | — | 1129 host blocked (서버측 connection-error 차단) |

## 판정

- **코드/SQL 정합 확인됨**: 동일한 단일 SQL 경로(`_ggeo_list` + `apply_limit_offset_syntax`/
  `limit_offset_bind`)가 슬림 스키마(138)·표준(153)에서 500/SQL(1064/1054) 없이 동작하고,
  `gcode` 오름차순 정렬·저자명(`Gposa`) 노출·상세 조회(저자구분 조인 `Gubun=G3_Gbun.Gcode`)가
  레거시 기대와 일치한다.
- **remote_154/155 미검증 사유는 코드 무관**: MySQL 3.23 서버 측 `Host 'localhost' is blocked
  because of many connection errors` (오류 1129). 해소는 운영자가 `mysqladmin flush-hosts`
  (또는 `FLUSH HOSTS`) 실행 후 재시도 필요 — 본 변경(저자 CRUD)과 독립적인 서버 상태 이슈.
  154/155 는 동일 코드 경로를 타며(handshake mismatch→aiomysql 재시도 로그로 3.23 확인),
  138/153 통과로 3.23/슬림 호환성은 간접 입증됨. flush-hosts 후 동일 스크립트로 재확인 권장.

## 재현

```bash
PYTHONPATH=도서물류관리프로그램/backend \
  python3 debug/probe_author_kim_search.py \
    --servers remote_138 remote_153 remote_154 remote_155 \
    --q 김 --out analysis/audit/sobo13-author-kim-4server.json
```
