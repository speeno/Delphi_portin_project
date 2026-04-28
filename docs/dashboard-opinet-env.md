# 대시보드 유가 위젯 — 오피넷 환경 변수

저장소에는 인증키를 넣지 않는다. 운영 서버에만 설정하고 키 회전 시 동일 이름으로 교체한다.

| 변수 | 설명 |
|------|------|
| `BLS_OPINET_CODE` | 오피넷 오픈 API 인증코드. 미설정 시 `BLS_DIESEL_PRICE_KRW`(기본 1580)로만 표시·추정한다. |
| `BLS_OPINET_API_BASE_URL` | 선택. 기본 `https://www.opinet.co.kr/api` |
| `BLS_OPINET_DIESEL_PRODCD` | 선택. 경유 제품코드. 기본 `D047` |
| `BLS_OPINET_CACHE_TTL_SEC` | 선택. 전국·시도 캐시 TTL(초). 기본 7200 |
| `BLS_OPINET_REQUEST_TIMEOUT_SEC` | 선택. HTTP 타임아웃. 기본 5 |
| `BLS_DIESEL_PRICE_KRW` | 오피넷 미조회 시 단가 fallback |
| `BLS_FUEL_DIFF_ALERT_KRW` | 전일 대비 등락 절대값(원/L)이 이 값 초과 시 위젯 `warn`, 약 2배 초과 시 `crit` |
