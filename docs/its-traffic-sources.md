# ITS 교통 정보 — OpenAPI와 WMTS 래스터

**요청 파라미터·도로등급·노선 목록·CSV 스키마**는 [its-traffic-reference-codes.md](./its-traffic-reference-codes.md)에 정리한다.

국가교통정보센터(ITS) **교통소통정보** 오픈데이터는 집계 주기 **약 5분**이며, **속성 API**(링크·속도 JSON/XML)와 **지도 타일**(실시간 소통 래스터, API 키 없이 URL 패턴)이 분리되어 있다. 대시보드의 `its_traffic_client`·교통 위젯은 OpenAPI 쪽을 사용한다.

출처: ITS 오픈데이터 포털 교통소통정보(요청변수·샘플 타일·예제 실행).

## OpenAPI — 실시간 소통 (`trafficInfo`)

- **샘플 베이스 URL**: `https://openapi.its.go.kr:9443/trafficInfo` (운영 연동 시 환경 변수로 호스트·경로 조정)
- **인증**: `apiKey` (필수)

| 요청변수   | 조건   | 설명 |
|------------|--------|------|
| `apiKey`   | 필수   | 발급 인증키 |
| `type`     | 필수   | 도로 유형: `all`(전체) / `ex`(고속도로) / `its`(국도) |
| `routeNo`  | 필수*  | 노선 번호. `type`이 `all`이 아니면 필수 |
| `drcType`  | 필수*  | 방향: `all` / `up` / `down` / `start` / `end`. `type`이 `all`이 아니면 필수 |
| `minX`…`maxY` | 선택 | `type`·`drcType`이 `all`인 영역 조회 시 경도·위도 bbox |
| `getType`  | 필수   | `xml` 또는 `json` (기본 xml) |

\* 포털 표에 따른 조건. 영역 `all` 조합 시에는 문서상 bbox 파라미터 사용 가능.

**응답(요약)**: `resultCode` / `resultMsg`, `totalCount`, 항목별 `roadName`, `roadDrcType`, `linkNo`, `linkId`, `startNodeId`, `endNodeId`, `speed`(km/h), `travelTime`(초), `createdDate`(YYYYMMDDHH24MISS).

백엔드 설정: `app/core/config.py`, `.env.example` 의 `BLS_ITS_*`.

## OpenAPI — 예측 소통 (`bypassFCastInfo`, 포털 Java 샘플)

교통 **예측**용으로 포털에서 별도 엔드포인트를 안내하는 경우가 있다. 공식 샘플 베이스 URL은 다음과 같다.

- **샘플 베이스 URL**: `https://openapi.its.go.kr:9443/bypassFCastInfo`
- **인증**: `apiKey` (필수)

| 요청변수      | 조건 | 설명 |
|---------------|------|------|
| `apiKey`      | 필수 | 발급 인증키 |
| `sectionId`   | 필수 | 본선 도로 구간 ID |
| `fCastDate`   | 필수 | 예측 날짜, `YYYYMMDD` (예: `20201217`) |
| `fCastHour`   | 필수 | 예측 시각(문자열, 샘플은 `00` 등) |
| `getType`     | 필수 | `xml` 또는 `json` |

이 스펙은 **실시간 `trafficInfo`(type·routeNo·bbox)** 와 요청 변수가 다르다.

### 대시보드 백엔드와의 관계

- `app/services/its_traffic_client.py` 의 `fetch_traffic_result(..., forecast=True)` 는 **실시간과 동일한 형태의 쿼리**(`type`=`all`, `drcType`=`all`, 선택적 bbox 등)를 붙여 `BLS_ITS_FORECAST_SERVICE_PATH` 로 호출한다. 기본값은 **`/fcTrafficInfo`** 로 두어 그런 스타일의 예측 API와 맞춘 것이다.
- 포털이 안내하는 **`/bypassFCastInfo`** 는 위 표의 `sectionId`·`fCastDate`·`fCastHour` 가 필요하므로, 해당 경로만 바꿔서는 응답이 나오지 않는다. `bypassFCastInfo` 를 쓰려면 **별도 요청 조립·응답 파싱**이 필요하다.

## WMTS 실시간 소통 타일 (브라우저 지도 오버레이)

GeoServer GWC REST WMTS 형태. **EPSG:3857**, `format=image/png8`.

### 공식 문서상 URL (TileRow / TileCol)

```text
https://its.go.kr:9443/geoserver/gwc/service/wmts/rest/ntic:N_LEVEL_{zoomLevel}/ntic:REALTIME/EPSG:3857/EPSG:3857:{zoomLevel}/{TileRow}/{TileCol}?format=image/png8
```

- **유효 줌: 7 ~ 15**

### OpenLayers·Leaflet용 XYZ 형태 (포털 타일 샘플과 동일)

공식 예제는 `ol.source.XYZ`에 아래와 같이 넣는다. 경로 세그먼트 순서가 **`{z}` 다음 `{y}` 그다음 `{x}`** 이다(Web Mercator 타일 행·열).

```text
https://its.go.kr:9443/geoserver/gwc/service/wmts/rest/ntic:N_LEVEL_{z}/ntic:REALTIME/EPSG:3857/EPSG:3857:{z}/{y}/{x}?format=image/png8
```

- **대응**: `TileRow` → 타일 **행** 인덱스(샘플의 `{y}`), `TileCol` → **열** 인덱스(샘플의 `{x}`). Leaflet `TileLayer`는 동일 토큰 `{z}/{y}/{x}`로 치환할 때 이 순서를 그대로 쓰면 된다.

**뷰 설정 참고(공식 샘플)**: 중심 예시 좌표 `127.766922, 35.907757`(위경도), `minZoom: 7`, `maxZoom: 15`, projection EPSG:3857.

### 프론트엔드 코드

- `도서물류관리프로그램/frontend/src/lib/its-map-tiles.ts` — Leaflet용 템플릿·줌 상수·필요 시 `(z, row, col)` 조립.

### 운영 시 유의

- **CORS**: 브라우저 직접 요청이 차단되면 백엔드 타일 프록시 등 검토.
- **HTTPS**: 페이지와 동일 스킴 권장.
- **이용 조건**: 국토교통부/ITS 오픈데이터 고지 준수.
