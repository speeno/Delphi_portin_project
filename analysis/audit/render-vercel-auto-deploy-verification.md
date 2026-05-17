# Render/Vercel 자동 배포 정합성 검증

- 대상 계획: `/Users/speeno/.cursor/plans/render-vercel-auto-deploy_f32fd928.plan.md`
- 검증 일자: 2026-05-15
- 권장 모델 티어: 고급모델 권장 (레거시 DB 불변 원칙·AI-IS 경계까지 함께 판단)

본 문서는 빌드 명령, 환경변수, 레거시 DB 불변 원칙 세 축이 실제 코드/배포 산출물과 일치하는지 점검한 결과다. 회귀 발생 시 같은 형식으로 갱신한다.

## 1. 검증 매트릭스

| # | 검증 항목 | 기대 상태 | 실측 결과 | 판정 |
| --- | --- | --- | --- | --- |
| 1 | Backend Dockerfile start command | `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}` | `도서물류관리프로그램/backend/Dockerfile` L25와 일치, `app.main`에 `app = FastAPI(...)` 정의 (`backend/app/main.py` `health` 핸들러 함께 존재) | OK |
| 2 | WeasyPrint 시스템 패키지 매핑 | `requirements.txt` 주석의 시스템 패키지가 Dockerfile `apt-get install`에 모두 포함 | `libpango-1.0-0`, `libcairo2`, `libgdk-pixbuf-2.0-0`, `libffi8`, `shared-mime-info` 일치 | OK |
| 3 | SSH 의존성 | `openssh-client` 설치, `use_system_ssh: true` 프로파일 동작 가능 | Dockerfile L11에서 설치, `servers.example.yaml` remote_154/155가 `use_system_ssh: true` + `system_ssh_local_port` 사용 | OK |
| 4 | Backend Health endpoint | `/api/v1/health` → `{"status":"ok"}` | `backend/app/main.py` L163-166 동일 | OK |
| 5 | Frontend rewrite 환경변수 | `BLS_API_PROXY_TARGET`이 rewrite destination에 사용 | `frontend/next.config.ts` L7-25 일치 | OK |
| 6 | Frontend 직접 호출 분리 | `NEXT_PUBLIC_API_URL` 미설정 시 동일 출처 프록시 모드 | `frontend/src/lib/api-client.ts` `_rawBase`가 빈 값일 때 `/api/v1` 상대 경로 사용 | OK |
| 7 | Vercel 빌드 명령 | `npm ci` + `npm run build` 가능 | `frontend/package.json`에 `build: next build` 정의 | OK |
| 8 | Secret 주입 경로 | `BLS_SERVERS_CONFIG`로 `servers.yaml` 경로 주입 | `backend/app/core/config.py` L53에서 `os.environ.get("BLS_SERVERS_CONFIG", str(BACKEND_DIR / "servers.yaml"))` | OK |
| 9 | smoke 스크립트 read-only 확인 | health endpoint만 호출, 쓰기 없음 | `도서물류관리프로그램/scripts/check_deploy_targets.sh` curl GET `/api/v1/health` 두 번 호출, 쓰기 호출 없음 | OK |
| 10 | `.gitignore`에 `servers.yaml` 등록 | Git 커밋 차단 | `도서물류관리프로그램/.gitignore` L23 `servers.yaml` | OK |
| 11 | 이미지에 비밀/데이터 누출 차단 | `.dockerignore`로 `servers.yaml`, `data/*`, `migrations/`, `__pycache__/` 제외 | 본 검증에서 누락 발견 → `도서물류관리프로그램/backend/.dockerignore` 신규 추가 | FIX 적용 |
| 12 | 백엔드 부팅 시 migrations 자동 실행 여부 | 자동 실행 없음 (AI-IS 불변 원칙) | `backend/app/` 트리에서 `migrations` 문자열 매치 없음 → 자동 실행 경로 없음 | OK |
| 13 | 자동 배포 모드 명시 | Render auto deploy + Vercel git integration | `docs/deploy-render-vercel.md` §3.1/§4.1/§9 | OK |
| 14 | 레거시 DB 불변 원칙 명시 | 마이그레이션·스키마·계정·방화벽 변경 없음 | `docs/deploy-render-vercel.md` §0/§9 | OK |
| 15 | 쓰기 검증 사전 승인 명시 | 운영자 승인된 테스트 계정/전표로만 | `docs/deploy-render-vercel.md` §0 + plan §검증 계획 | OK |

## 2. 발견과 대응

### 2.1 `.dockerignore` 부재 (FIX 적용)

- 증상: `backend/Dockerfile`이 `COPY . .`로 빌드 컨텍스트 전체를 이미지에 복사한다. Render Git auto deploy는 git tree만 빌드 컨텍스트로 사용하므로 커밋되지 않은 로컬 `servers.yaml`은 어차피 들어가지 않는다. 그러나 로컬에서 `docker build`로 만든 이미지가 운영에 흘러가면 비밀이 이미지 안에 박힐 수 있다. 또한 `migrations/2026_*.sql` DDL이 이미지에 포함되어 운영자가 실수로 실행할 위험이 있다.
- 대응: `도서물류관리프로그램/backend/.dockerignore` 추가. 다음을 제외한다.
  - 비밀/환경: `servers.yaml`, `.env`, `.env.*`
  - DDL: `migrations/`
  - 로컬 상태: `data/uploads/`, `data/its/`, `data/kma/`, `data/tenant_print/`, `data/*.json`
  - 캐시/테스트/IDE: `__pycache__/`, `*.pyc`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `tests/`, `.git/`
- 효과: 로컬·CI·Render 빌드 어느 경로에서 만든 이미지든 비밀 누출과 DDL 동봉을 차단한다. 영속 데이터는 §3.5의 Persistent Disk/외부 저장소 정책으로 분리한다는 가이드와 일관된다.

### 2.2 Render `system_ssh_local_port` 충돌 — 운영 가드만 유지

- Render scale-out 시 동일 컨테이너 이미지가 여러 인스턴스로 늘어나면 `remote_154 (41554)`, `remote_155 (41555)` 같은 고정 로컬 포트가 충돌할 수 있다.
- 본 배포 계획은 instance 1 고정을 명시했고, scale-out 시 별도 작업으로 분리한다고 `docs/deploy-render-vercel.md` §3.1/§3.4/§8에 명문화되어 있어 추가 변경은 하지 않는다.

### 2.3 Vercel Preview의 운영 DB 누수 — 정책으로 차단

- 직접 호출 모드(`NEXT_PUBLIC_API_URL`)를 Preview에 잘못 설정하면 Preview 빌드가 운영 백엔드/레거시 DB로 직행한다.
- `docs/deploy-render-vercel.md` §4.1/§4.3에서 Preview는 별도 backend 또는 비활성 정책을 사용한다고 명시했고, 운영 환경변수는 Production 환경에만 등록한다. 추가 코드 변경은 불필요하다.

## 3. 배포 전 사용자 체크리스트

배포 전에 운영자가 한 번만 확인하면 되는 항목이다.

1. Render service의 Auto Deploy가 켜져 있고, Production branch가 운영 브랜치인지
1. Render Secret File에 `servers.yaml`이 등록되고 `BLS_SERVERS_CONFIG=/etc/secrets/servers.yaml` 환경변수가 설정됐는지
1. Render에서 `BLS_JWT_SECRET`이 기본값이 아닌지 (`openssl rand -hex 32`)
1. Render `BLS_CORS_ORIGINS`가 Vercel/커스텀 도메인을 정확히 가리키는지
1. Vercel Production 환경변수 `BLS_API_PROXY_TARGET`이 Render backend URL인지
1. Vercel Preview에는 운영 DB로 흘러갈 환경변수가 없는지
1. 배포 후 `도서물류관리프로그램/scripts/check_deploy_targets.sh` 결과가 `[ok] 배포 health/rewrite smoke 통과` 인지

## 4. 미적용 / 후속 작업

- Render Persistent Disk 또는 외부 object storage 이전: 업로드/JSON 상태 보존이 필요할 때 별도 작업으로 분리.
- 고정 outbound IP 또는 NAT gateway: 레거시 DB/SSH 방화벽 정책에 따라 운영자 승인 후 별도 작업으로 분리.
- 쓰기 시나리오 검증: 운영자가 승인한 테스트 계정/테스트 전표로만, 본 자동 배포 검증 범위와 분리.

## 5. 모델 선택

| 검증 축 | 권장 티어 | 메모 |
| --- | --- | --- |
| Dockerfile / requirements / health endpoint 매핑 | 표준모델 | 기계적 대조 |
| `.dockerignore` 누락 같은 보안/운영 리스크 판단 | 고급모델 권장 | AI-IS 불변 원칙·운영자 실수 시나리오를 함께 검토 |
| Vercel Preview / 운영 DB 누수 정책 | 고급모델 권장 | 운영 보안 정책 판단 |

## 6. Harness

- Harness: N/A
