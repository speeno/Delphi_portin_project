# 도서물류관리프로그램 Render/Vercel 배포 가이드

이 문서는 `도서물류관리프로그램`을 백엔드와 프론트엔드로 분리해 배포하는 절차를 정리한다.

> **제품 Git (`speeno/books-logistics-web`, Private):** Render Root = `backend`, Vercel Root = `frontend`.  
> 운영 체크리스트·Blueprint는 제품 레포 [`docs/DEPLOY.md`](../도서물류관리프로그램/docs/DEPLOY.md)·[`render.yaml`](../도서물류관리프로그램/render.yaml) 를 우선 참고한다.

- Backend: FastAPI/Uvicorn을 Render Web Service로 배포
- Frontend: Next.js를 Vercel Project로 배포
- Repository: 같은 Git 저장소를 사용하되 각 서비스의 Root Directory를 다르게 지정
- 자동 배포: Render와 Vercel 모두 **Git integration 기반 auto deploy**가 표준 운영 모드이다.

## 0. AI-IS 연결 모드와 레거시 DB 불변 원칙

이 배포는 신규 솔루션 런칭이 아니라, 운영 중인 **레거시 솔루션 위에 AI-IS(AI-Integrated Service) 형태로 웹 포팅본을 붙이는** 작업이다. 다음 원칙을 깨면 배포 자체를 보류한다.

- 레거시 DB는 정본이다. 본 배포는 DB 마이그레이션·스키마 변경·데이터 이관·신규 운영 DB 프로비저닝을 수행하지 않는다.
- 레거시 DB/SSH 서버 설정·방화벽 정책·계정 권한은 자동 배포 대상이 아니다. 변경이 필요한 경우 운영자가 기존 인프라 승인 절차로 수행한다.
- `servers.yaml`은 **기존 레거시 접속 정보**(DB host/port/user/pw, SSH endpoint)를 그대로 담는 연결 프로파일이다. Render Secret File 또는 동등한 Secret 주입 경로로만 관리하고 Git에는 절대 커밋하지 않는다.
- 쓰기 API는 레거시 솔루션과 같은 DB를 바라본다. 배포 직후 검증은 health/조회 위주로 두고, 쓰기 검증은 운영자가 사전 승인한 테스트 전표/계정으로만 수행한다.

## 1. 배포 구조

```text
사용자 브라우저
  -> Vercel Next.js frontend
  -> /api/v1/* rewrite 또는 직접 fetch
  -> Render FastAPI backend
  -> legacy MySQL / SSH tunnel / external Open APIs
```

권장 연결 방식은 **Vercel 동일 출처 프록시**이다.

- 프론트 브라우저는 `https://<frontend>.vercel.app/api/v1/...`를 호출한다.
- Vercel `next.config.ts` rewrite가 Render 백엔드로 전달한다.
- 브라우저 관점에서는 동일 출처 요청이므로 CORS 문제를 줄일 수 있다.

현재 프론트엔드 구현은 이 방식에 맞춰져 있다.

```ts
// 도서물류관리프로그램/frontend/next.config.ts
const apiProxyTarget = (
  process.env.BLS_API_PROXY_TARGET ?? "http://127.0.0.1:8000"
).replace(/\/$/, "");
```

## 2. 사전 준비

1. GitHub 등 Render/Vercel이 접근 가능한 원격 저장소에 코드를 push한다.
2. `도서물류관리프로그램/backend/servers.yaml`의 실제 접속 정보는 커밋하지 않는다.
3. 프로덕션용 `BLS_JWT_SECRET`을 생성한다.

```bash
openssl rand -hex 32
```

1. Render에서 legacy DB 또는 SSH 서버로 나가는 outbound 연결이 허용되는지 확인한다.
   - DB/SSH 서버에 방화벽이 있으면 Render outbound IP 허용이 필요하다.
   - 고정 outbound IP가 필요하면 Render의 해당 플랜/네트워크 기능을 검토한다.

## 3. Backend: Render 배포

### 3.1 권장 방식: Docker Web Service + Git Auto Deploy

백엔드는 `weasyprint`, `sshtunnel`, `paramiko`, 시스템 `ssh` 의존성이 있다. PDF 출력과 SSH 터널을 안정적으로 쓰려면 Render의 Native Python 런타임보다 **Docker 배포**를 권장한다.

Render 설정:

| 항목 | 값 |
| --- | --- |
| Service Type | Web Service |
| Runtime | Docker |
| Repository | `도서물류관리프로그램` 모노레포 |
| Branch | 운영용 브랜치 (예: `main`) |
| Root Directory | `도서물류관리프로그램/backend` |
| Dockerfile Path | `Dockerfile` |
| Health Check Path | `/api/v1/health` |
| Auto Deploy | `On` (해당 브랜치 push 시 자동 빌드/배포) |
| Instance Count | 초기 `1` 고정 (SSH 터널 중복 방지) |

Render dashboard 절차:

1. Render dashboard → `New +` → `Web Service` → GitHub/Git provider 연결
2. 위 모노레포를 선택하고 운영 브랜치를 지정
3. Settings → `Build & Deploy` 에서 Root Directory `도서물류관리프로그램/backend`, Runtime `Docker`, Dockerfile Path `Dockerfile`, Health Check Path `/api/v1/health` 설정
4. Settings → `Build & Deploy` → `Auto-Deploy`를 `Yes`로 둔다.
5. Settings → `Scaling`에서 인스턴스 수를 `1`로 고정한다. scale-out은 `system_ssh_local_port` 충돌 검토 이후로 미룬다.

Render 자동 배포는 운영 브랜치에 push가 들어오면 새 Docker 빌드와 컨테이너 교체를 자동으로 수행한다. Secret/환경변수는 dashboard에 한 번 등록하면 이후 배포에서 그대로 재사용된다.

권장 Dockerfile 예시:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    openssh-client \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf-2.0-0 \
    libffi8 \
    shared-mime-info \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```

위 Dockerfile을 실제로 추가하지 않고 Native Python으로 먼저 시도할 수도 있지만, PDF 출력이 `PR_ENGINE_UNAVAILABLE`로 떨어지면 Docker 방식으로 전환한다.

### 3.2 대안: Native Python Web Service

PDF 출력 또는 시스템 SSH 의존성이 당장 필요 없을 때만 사용한다.

| 항목 | 값 |
| --- | --- |
| Service Type | Web Service |
| Runtime | Python |
| Root Directory | `도서물류관리프로그램/backend` |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/api/v1/health` |

### 3.3 Render 환경변수

필수:

| 변수 | 예시 | 설명 |
| --- | --- | --- |
| `BLS_JWT_SECRET` | `openssl rand -hex 32` 결과 | JWT 서명 키. 배포 후 변경하면 기존 세션은 무효화된다. |
| `BLS_CORS_ORIGINS` | `https://<frontend>.vercel.app,https://<custom-domain>` | 직접 API 호출 모드 또는 점검용 CORS 허용 Origin |
| `BLS_SERVERS_CONFIG` | `/etc/secrets/servers.yaml` | Render Secret File로 올린 DB 서버 설정 경로 |

권장:

| 변수 | 기본값 | 설명 |
| --- | --- | --- |
| `BLS_JWT_ACCESS_MINUTES` | `15` | Access token 만료 시간 |
| `BLS_JWT_REFRESH_DAYS` | `7` | Refresh token 만료 일수 |
| `BLS_CONNECT_TIMEOUT` | `15` | 서버별 값이 없을 때 DB 연결 timeout |
| `BLS_READ_TIMEOUT` | `120` | 서버별 값이 없을 때 DB read timeout |
| `BLS_OPEN_API_SSL_VERIFY` | `1` | 외부 Open API TLS 검증 |
| `BLS_OPEN_API_CA_BUNDLE` | 빈 값 | 사내 CA bundle 경로 |

외부 API 기능을 사용할 때만 설정:

| 변수 | 용도 |
| --- | --- |
| `BLS_ITS_API_KEY` | ITS 교통 API |
| `BLS_KMA_API_KEY` | 기상청 API |
| `BLS_KMA_WARNING_API_KEY` | 기상특보 API |
| `BLS_OPINET_CODE` | 오피넷 유가 API |
| `BLS_NL_API_KEY` | 국립중앙도서관 API |

### 3.4 `servers.yaml` Secret File

`servers.yaml`은 레거시 DB/SSH 비밀번호를 포함하므로 절대 Git에 커밋하지 않는다. Render에서는 Secret File로 등록한다.

1. Render Service > Environment > Secret Files
2. 파일명: `servers.yaml`
3. 내용: `도서물류관리프로그램/backend/servers.example.yaml`을 기반으로 실제 값 입력
4. 환경변수:

```text
BLS_SERVERS_CONFIG=/etc/secrets/servers.yaml
```

주의:

- `remote_154`, `remote_155`처럼 `use_system_ssh: true`를 쓰면 컨테이너에 `openssh-client`가 필요하다.
- `system_ssh_local_port`가 겹치면 안 된다.
- Render 인스턴스가 여러 개로 scale-out되면 각 인스턴스가 별도 SSH 터널을 열 수 있다. 안정화 전에는 instance count를 1로 둔다.

### 3.5 파일 저장소

백엔드는 다음 로컬 경로를 사용한다.

- `backend/data/uploads`
- `backend/data/*.json` 일부 운영 상태 파일

Render의 기본 파일 시스템은 재배포 시 사라질 수 있다. 운영에서 업로드 파일 또는 JSON 상태를 보존해야 하면 다음 중 하나를 선택한다.

- Render Persistent Disk를 `backend/data`에 연결
- S3/R2 등 외부 object storage로 후속 이전
- 가입/테넌트/첨부 파일 상태를 별도 DB로 이전

초기 배포 검증만 할 때는 디스크 없이도 헬스 체크와 로그인 흐름을 먼저 확인할 수 있다.

## 4. Frontend: Vercel 배포

### 4.1 프로젝트 생성 + Git Auto Deploy

Vercel 설정:

| 항목 | 값 |
| --- | --- |
| Framework Preset | Next.js |
| Repository | `도서물류관리프로그램` 모노레포 |
| Production Branch | 운영 브랜치 (예: `main`) |
| Root Directory | `도서물류관리프로그램/frontend` |
| Install Command | `npm ci` |
| Build Command | `npm run build` |
| Output Directory | 비움, Next.js 기본값 사용 |
| Auto Deploy | Git integration 기본값(Production = production branch push, Preview = 그 외 branch/PR) |

Vercel dashboard 절차:

1. Vercel dashboard → `Add New...` → `Project` → Git provider 연결
2. 같은 모노레포를 선택하고 `Root Directory`에서 `도서물류관리프로그램/frontend`를 지정
3. Framework Preset이 `Next.js`로 자동 감지되는지 확인하고, Install/Build Command가 위 표와 같은지 검증
4. Settings → `Git`에서 Production Branch가 운영 브랜치인지, Preview 배포 정책이 의도와 맞는지 확인
5. Settings → `Environment Variables`에서 운영(`Production`)과 미리보기(`Preview`)를 분리해 등록한다. 운영 DB가 그대로 노출되지 않도록 Preview는 별도 backend 또는 비활성 정책을 사용한다.

### 4.2 Vercel 환경변수

권장 프록시 방식:

| 변수 | 값 |
| --- | --- |
| `BLS_API_PROXY_TARGET` | `https://<backend-service>.onrender.com` |
| `NEXT_PUBLIC_API_URL` | **변수를 추가하지 않음** (Vercel은 빈 값 저장 불가 — 목록에 없으면 OK) |

`NEXT_PUBLIC_API_URL`을 “비워서” 등록할 필요가 없습니다. Vercel Environment Variables 목록에 **해당 키가 아예 없으면** 프록시 모드입니다.

이렇게 두면 프론트는 동일 출처 `/api/v1/*`를 호출하고, Vercel이 Render로 rewrite한다.

직접 API 호출 방식:

| 변수 | 값 |
| --- | --- |
| `NEXT_PUBLIC_API_URL` | `https://<backend-service>.onrender.com` |
| `BLS_API_PROXY_TARGET` | 설정하지 않아도 됨 |

직접 API 호출 방식을 쓰면 Render 백엔드의 `BLS_CORS_ORIGINS`에 Vercel 도메인을 반드시 추가한다.

내부 검수용:

| 변수 | 값 |
| --- | --- |
| `NEXT_PUBLIC_SHOW_DESIGN_GUIDE` | `1`일 때 공개 랜딩에 디자인 가이드 섹션 표시 |

운영에서는 `NEXT_PUBLIC_SHOW_DESIGN_GUIDE`를 설정하지 않는다.

### 4.3 Preview/Production 분리

Preview 배포도 API를 호출해야 하면 다음 중 하나를 선택한다.

1. Vercel Preview 환경에도 `BLS_API_PROXY_TARGET=https://<render-backend>.onrender.com` 설정
2. Render `BLS_CORS_ORIGINS`에 Preview 도메인 패턴을 허용하지 말고, Vercel rewrite 방식만 사용
3. Preview 전용 Render backend를 별도 생성

운영 데이터 보호를 위해 Preview가 운영 DB에 붙지 않도록 주의한다.

## 5. 배포 순서

1. Render backend를 먼저 배포한다.
2. Render `/api/v1/health`가 `{"status":"ok"}`를 반환하는지 확인한다.
3. Vercel frontend를 배포한다.
4. Vercel 환경변수 `BLS_API_PROXY_TARGET`을 Render backend URL로 설정한다.
5. Vercel을 재배포한다.
6. 브라우저에서 다음을 확인한다.

```text
https://<frontend>.vercel.app/api/v1/health
```

응답이 `{"status":"ok"}`이면 Vercel rewrite가 백엔드까지 연결된 것이다.

### 5.1 배포 후 자동 smoke 명령

브라우저 확인과 별개로 배포 후 다음 스크립트로 health/rewrite를 한 번에 검증한다.

```bash
BLS_DEPLOY_BACKEND_URL=https://<backend>.onrender.com \
BLS_DEPLOY_FRONTEND_URL=https://<frontend>.vercel.app \
도서물류관리프로그램/scripts/check_deploy_targets.sh
```

스크립트 동작:

- `BLS_DEPLOY_BACKEND_URL/api/v1/health` 가 HTTP 2xx + `"status":"ok"` 인지 확인
- `BLS_DEPLOY_FRONTEND_URL/api/v1/health` 가 같은 응답인지 확인 (Vercel rewrite → Render 연결 확인)
- 실패 시 DNS/CORS/rewrite/cold start 관련 hint를 stderr로 출력

옵션 환경변수:

| 변수 | 기본값 | 설명 |
| --- | --- | --- |
| `BLS_DEPLOY_HEALTH_PATH` | `/api/v1/health` | 다른 health endpoint로 교체할 때 |
| `BLS_DEPLOY_CHECK_TIMEOUT_SECONDS` | `20` | curl `--max-time` 초 |

Render cold start로 첫 호출이 실패하면 1~2회 재실행한 뒤 결과를 채택한다. AI-IS 원칙상 이 smoke는 **레거시 DB에 쓰지 않는 health endpoint만** 호출한다.

## 6. 배포 후 검증 체크리스트

Backend:

- `GET https://<backend>.onrender.com/api/v1/health` 성공
- Render logs에 `Starting 도서물류관리프로그램 API server` 출력
- `servers.yaml` 경로 오류 없음
- DB/SSH 연결이 필요한 API 호출 시 timeout 또는 auth error가 없는지 확인
- PDF 출력 기능 사용 시 WeasyPrint 관련 503이 없는지 확인

Frontend:

- Vercel build 성공
- `GET https://<frontend>.vercel.app/api/v1/health` 성공
- 로그인 화면 로딩
- 로그인 성공 후 `/dashboard/*` 진입
- 관리자/마스터/입고/출고 등 주요 화면에서 API 네트워크 오류 없음

보안:

- `servers.yaml`, `.env`, DB/SSH 비밀번호가 Git에 없음
- `BLS_JWT_SECRET`이 기본값이 아님
- `BLS_CORS_ORIGINS`가 `*`가 아님
- Vercel `NEXT_PUBLIC_*` 변수에는 공개돼도 되는 값만 있음

## 7. 자주 나는 오류

### Vercel 화면에서 "백엔드에 연결할 수 없습니다"

확인:

- Vercel `BLS_API_PROXY_TARGET`이 Render URL과 일치하는지
- `NEXT_PUBLIC_API_URL`을 잘못 설정해 직접 호출 모드가 된 것은 아닌지
- Render backend가 sleep/cold start 중인지
- `/api/v1/health`를 Vercel 도메인에서 직접 열었을 때 응답하는지

### CORS 오류

프록시 방식이면 일반적으로 CORS가 발생하지 않는다. 직접 API 호출 방식이면 Render 환경변수에 다음처럼 Vercel Origin을 넣는다.

```text
BLS_CORS_ORIGINS=https://<frontend>.vercel.app,https://<custom-domain>
```

`*`는 credentials와 함께 쓸 수 없으므로 운영에서는 피한다.

### 로그인 401 또는 사용자 없음

확인:

- `BLS_SERVERS_CONFIG`가 실제 Secret File 경로인지
- `servers.yaml`의 DB/SSH 비밀번호가 맞는지
- legacy DB 서버가 Render outbound IP를 허용하는지
- `remote_154/155`의 `mysql3_protocol`, `mysql3_charset`, `ssh_tunnel` 설정이 로컬과 같은지

### PDF/인쇄가 503으로 떨어짐

WeasyPrint 시스템 라이브러리가 없을 가능성이 높다. Docker 배포로 전환하고 아래 패키지가 설치됐는지 확인한다.

```text
libpango-1.0-0
libcairo2
libgdk-pixbuf-2.0-0
libffi8
shared-mime-info
```

### 업로드 파일 또는 가입 신청 상태가 사라짐

Render 기본 파일 시스템은 영속 저장소가 아니다. `backend/data`를 Persistent Disk 또는 외부 저장소로 이전한다.

## 8. 운영 권장값

초기 운영은 다음 구성을 권장한다.

- Render backend: Docker Web Service, instance 1
- Render health check: `/api/v1/health`
- Render Secret File: `/etc/secrets/servers.yaml`
- Vercel frontend: `BLS_API_PROXY_TARGET`만 설정, `NEXT_PUBLIC_API_URL` 미설정
- 운영 도메인 확정 후:
  - Render `BLS_CORS_ORIGINS`에 Vercel/커스텀 도메인 반영
  - Vercel custom domain 연결
  - SSL 자동 발급 확인

## 9. 1회성 Secret 등록 절차 (자동 배포 전제)

Git auto deploy 모드에서는 코드 변경만으로 재배포가 일어난다. Secret/환경변수는 **최초 1회**만 dashboard에 입력하면 이후 배포에 자동 재사용된다. 절차는 다음 순서로 한 번만 수행하고 결과를 별도 운영 보안 채널에 보관한다.

1. Render Secret File 등록
   - Render Service → `Environment` → `Secret Files` → `Add Secret File`
   - 파일명: `servers.yaml`
   - 내용: `도서물류관리프로그램/backend/servers.example.yaml`을 참고해 **운영 중인 레거시 DB/SSH 접속 정보 그대로** 입력
   - 저장 후 환경변수에 `BLS_SERVERS_CONFIG=/etc/secrets/servers.yaml` 등록
1. Render 필수 환경변수 등록 (Environment → Environment Variables)
   - `BLS_JWT_SECRET` (`openssl rand -hex 32` 결과)
   - `BLS_CORS_ORIGINS` (Vercel + 커스텀 도메인)
   - 외부 Open API 키는 필요한 기능만 활성화
1. Vercel 환경변수 등록 (Project → Settings → Environment Variables)
   - `Production`에 `BLS_API_PROXY_TARGET=https://<render-backend>.onrender.com`
   - `Preview`는 운영 DB로 누수되지 않게 별도 backend URL 또는 미설정으로 둔다.
1. Auto Deploy를 켠 상태로 운영 브랜치에 push해 첫 배포를 발생시키고, 5.1의 smoke 스크립트로 검증
1. 이후 코드 변경은 Git push만으로 양 플랫폼이 재배포된다. Secret을 회전해야 할 때만 dashboard에서 값을 갱신한다.

레거시 DB 측에서는 다음을 **변경하지 않는다**.

- 기존 DB 서버 호스트/포트/계정/권한/스키마
- SSH 서버 호스트/포트/계정/포워딩 정책
- 방화벽/네트워크 정책 (Render outbound 차단이 발견되면 본 절차가 아니라 운영자의 기존 인프라 승인 절차로 다룬다.)

## 10. 모델 선택

본 가이드와 짝을 이루는 자동 배포 계획(`/Users/speeno/.cursor/plans/render-vercel-auto-deploy_f32fd928.plan.md`)의 To-Do별 권장 모델 티어다.

| To-Do | 권장 티어 | 사용자 모델 선택 메모 |
| --- | --- | --- |
| `backend-dockerfile` (Dockerfile 추가) | 표준 | requirements와 시스템 패키지 매핑이 명확 |
| `deploy-config-docs` (본 문서 자동 배포 절차) | 고급 권장 | Render Secret, 레거시 DB 불변 원칙, AI-IS 경계 판단 포함 |
| `deploy-smoke-script` (`check_deploy_targets.sh`) | 표준 | health/rewrite URL 확인 중심 |
| `verify-auto-deploy-plan` (정합성 검증) | 고급 권장 | 빌드 명령·환경변수·레거시 DB 불변 원칙을 함께 점검 |

표준 행은 Cursor 기본 모델로 진행 가능하다. 고급 권장 행만 필요 시 모델 드롭다운에서 고급 모델을 선택해 재검토한다.

## 11. Harness

- Harness: N/A
