# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is the **hub repo** for a Delphi → web porting project: a legacy Delphi book-logistics
system (도서물류관리프로그램, "Book Logistics Management Program") is being ported, without
downtime, to a modern web stack using an "8-layer harness engineering" methodology.

The hub holds **docs, the porting harness, analysis tools, audits, the project dashboard, and
the regression test suite**. The shippable web product lives in the **`도서물류관리프로그램/`**
subdirectory, which has its **own separate `.git`** and is gitignored from the hub. Treat it as a
nested product repo: the hub's `backend/` and `frontend/` are an older second copy of the same
product shape — the source of truth for the running app is `도서물류관리프로그램/`.

Most prose, decision records, and cursor rules are in **Korean**; match that language when editing
those docs.

## Product stack (`도서물류관리프로그램/`)

- **Frontend**: Next.js 15 (App Router) + React 19 + TypeScript + Tailwind + shadcn/ui
- **Backend**: FastAPI + Uvicorn + aiomysql (async pool), JWT auth (python-jose) against the legacy DB
- **DB**: legacy MySQL across 4 servers (`remote_138/153/154/155`), some running **MySQL 3.23**, reached over optional SSH tunnels

## Commands

### Run the product app
```bash
./start.sh                 # backend + frontend (delegates to 도서물류관리프로그램/scripts/start.sh)
./start.sh backend         # backend only;  ./start.sh frontend for frontend only
./stop.sh / ./status.sh / ./restart.sh

# manual:
cd 도서물류관리프로그램/backend && uvicorn app.main:app --reload --port 8000
cd 도서물류관리프로그램/frontend && npm run dev      # http://localhost:3000
```

### Tests (the hub's `test/` suite, ~216 files)
The suite tests the **product backend** by injecting `도서물류관리프로그램/backend` onto
`sys.path` via `test/conftest.py` — so tests import `from app.routers...`, `from app.services...`
even though the code lives in the product dir. Run pytest from the **hub root**.
```bash
python -m pytest -q                                   # whole suite
python -m pytest test/test_routers_hcode_coalesce.py  # one file
python -m pytest test/test_x.py::TestClass::test_y    # one case
python -m pytest -k hcode                              # by keyword
```
Many tests use `unittest.IsolatedAsyncioTestCase`; conftest has an autouse fixture that repairs the
default event loop between async and sync tests — don't remove it.

### Static audits / guards (these gate CI; run before relying on a change)
```bash
python3 tools/audit_welove_routing_consistency.py --strict   # routing seeds/matrix/mappings
python3 tools/audit_domain_api_hcode_filter.py --strict      # multi-tenant SQL missing hcode filter
python3 tools/audit_router_hcode_coalesce.py
python3 tools/classify_login_audit_logs.py
```

### DB smoke (live, opt-in)
Local/PR runs are **dry-run** unless `RUN_DB_SMOKE` is set. Matrix lives in
`debug/probe_backend_all_servers.py` (`_routes_for(...)`); live policy in
`.github/workflows/db-smoke.yml`. Register every new router GET in that probe matrix.

### Dashboard (static site → GitHub Pages, separate public repo)
```bash
cd dashboard && python3 -m http.server 8000           # local
./tools/deploy_dashboard.sh sync                       # push to public delphi-dashboard repo
```
Dashboard state is plain JSON under `dashboard/data/` — edit JSON + push, no build step.

## Architecture and invariants

The hard rules below are enforced by tests/audits and recorded as **DEC-NNN** entries in
`legacy-analysis/decisions.md`. When a change touches one of these areas, read the cited DEC first;
the `.cursor/rules/*.mdc` files are the authoritative long-form versions and apply to Claude too.

### Multi-tenant hcode isolation (security-critical)
Many legacy tables are **shared across tenants** keyed by `hcode`. Every SQL touching a multi-tenant
table must filter by hcode; writes especially. Helpers/guards live in
`backend/app/core/hcode_isolation.py` and `hcode_scope_context.py` (`enforce_hcode_identity/range/pattern`).
Never "fail-open to the first matching tenant" — shared-DB lookups must stay **fail-closed**, keeping
`tenant_id`/`account_family`/`active_build_id` as `None` when ownership is ambiguous (DSN-DEC-12).
Login audit logs must preserve `ownership_status` / `ownership_candidate_count` / `ownership_violation`.

### Multi-DB / MySQL 3.23 compatibility (DEC-033)
One API must serve all 4 servers without 500s; differences go in **data/contracts only, never code
branches in the service layer**. Use `backend/app/core/sql_mysql3.py`:
- Pagination: wrap with `apply_limit_offset_syntax(sql, server_id)` + `limit_offset_bind(...)`.
- **No derived tables** (`SELECT COUNT(*) FROM (subquery)`) — MySQL 3.23 errors 1064. Use
  `count_grouped(server_id, table=, where_sql=, group_by=, having=, params=)`.
- **No giant `IN (...)`** single queries — chunk via `in_clause_lookup(server_id, sql_template=, keys=, chunk_size=)`.
- Avoid `CAST AS CHAR`, `CASE WHEN`, `COALESCE`; prefer `CONCAT/IF/IFNULL`.
- Per-tenant column differences (DDL drift) go in one `app/services/<table>_adapt.py` module
  (driven by `SHOW COLUMNS`), not service-layer `if`s.

### 북이오웍스 계정 전환 · 이메일 로그인 (ACM / DEC-235)
Web login is moving to **email accounts** that are an *overlay* on the legacy `Id_Logn` row
(`docs/decision-bukioworks-account-migration.md`). The legacy Delphi program keeps logging in with the
same `Id_Logn` rows, so the switch / email-login / reset / link code paths must **never write `Id_Logn`**
(static guard `test/test_acm_delphi_coexistence.py`). Accounts live in the dedicated DB `bukio_web_db`
on `remote_138` (`app/services/web_accounts_db.py`); every email login re-checks that the linked
`Id_Logn` row still exists and re-derives permissions (`auth_service.load_user_by_identity`), failing
closed with `ACCT_LINK_STALE`. `POST /auth/login` shares its candidate/challenge logic with
`verify-legacy` through `app/services/auth_login_core.py` — change the core, not the router copy.
`BLS_LEGACY_ID_LOGIN` (code default `on` until cutover) gates legacy-ID web login; mail goes through
`app/services/email_dispatch_service.py` (Brevo SMTP, `debug/send_test_email.py --check`).

### Login / DB routing (DSN-DEC-08/12)
Secret verification happens on the **metadata-selected data server's `Id_Logn`**, not a single global
auth server. Don't add code/comments assuming `BLS_AUTH_SERVER_ID` authenticates all users. Don't
rename or drop `AliasChoices` on `userId`/`tenantId`/`hcode` request fields without also editing
`도서물류관리프로그램/frontend/src/contexts/auth-context.tsx`. Design source: `docs/decision-login-db-routing.md`.

### Porting modern screens from Delphi forms (DEC-028 / DEC-053)
Delphi `.dfm` forms are pre-converted by `tools/delphi_porting_accelerator/` into HTML/JSON under
`tools/delphi_porting_accelerator/examples/generated/legacy_source_root/<Subu*>/`. Use these as the
**official input** — don't hand-redesign. Workflow: inventory all variant folders → write a mapping
note `analysis/layout_mappings/<Sobo*>.md` (regions, widget IDs, **TabOrder**, DBGrid columns/sort/totals,
event handlers) → build the page attaching `data-legacy-id="<original id>"` to every widget → test that
zero dfm widget IDs are missing. Customer variant differences (`Sobo22`/`Sobo22_1`/...) go only in the
`customer_variants` section of `migration/contracts/<flow>.yaml` — **never code branches**; use one
data-driven component.

## Screen mapping status (WeLove_FTP → 도서물류관리프로그램)

Two trackers, both authoritative for different questions. **Treat the numbers below as a snapshot —
regenerate/re-read before relying on them.**

**1. Form-level equivalence matrix** — which legacy `Subu*.dfm` form maps to which modern screen,
and whether captions/folders line up. Auto-generated; **do not hand-edit**:

```bash
python3 tools/delphi_form_screen_matrix.py            # regenerate JSON + md
python3 tools/delphi_form_screen_matrix.py --check     # CI: every registered Subu* has a .dfm
python3 tools/delphi_form_screen_matrix.py --strict     # also gate single-map CAPTION_DIFF
```

- Source of truth: `analysis/audit/delphi-form-screen-matrix.json`; human view: `docs/delphi-form-screen-equivalence-matrix.md`.
- As of the last generation: **77** modern registry forms, **91** legacy DFM stems, **45 orphan legacy
  stems** (legacy forms with no modern screen yet — the remaining port backlog), 0 missing DFM.
- `status` vocabulary per row: `MATCH` (captions identical), `NEAR_MATCH`, `CAPTION_DIFF` (mapped but
  title differs — review first, see the `note`/similarity), `MULTI_MAP` (one legacy folder → several
  modern routes, e.g. `Subu21` → sales-statement + status views), `OK_EXEMPT` (intentional rename on
  allowlist), `WEB_ONLY` (modern screen with no legacy form, e.g. `_WebAdm`), `DFM_PLACEHOLDER`.
- Per-screen layout mapping notes (the manual 1:1 widget/TabOrder/grid tables required before porting)
  live in `analysis/layout_mappings/<Sobo*>.md`.

**2. Core-scenario porting progress** — the 10 core scenarios (C1–C10) plus extensions (C11/C13/C14/C15),
organized by DEC-003 risk stages (auth → read-only → register → edit/cancel → batch/print → permissions →
cutover). Tracker: `dashboard/data/porting-screens.json` (`status`: `not_started|in_progress|review|done|blocked`);
narrative plan: `docs/core-scenarios-porting-plan.md`. Delivery lines defined there:
beta-minimum = `C1,C2,C7`; beta-recommended = `+C6,C8`; internal-open = `C1–C10`. Overall project
progress is tracked in `dashboard/data/project.json` (`overallProgress`).

Unported/incomplete features are inventoried in `analysis/audit/incomplete-features-inventory.{json,md}`.

### Design system (북이오웍스 / Bukioworks)

UI/color/typography changes follow `docs/Design.md` as SSOT. No hardcoded hex in TSX (guard:
`rg '#[0-9a-fA-F]{6}\b' 도서물류관리프로그램/frontend/src`), reference `var(--…)` tokens only; one
`brand-primary` (Vivid Lime/Sky) CTA per screen.

## Key directories

- `도서물류관리프로그램/` — the shippable product (own git; gitignored here). `backend/app/{core,routers,services,models}`.
- `test/` — hub regression suite (imports the product backend via conftest).
- `tools/` — porting harness (`harness/`), Delphi parsers (`parsers/`), `delphi_porting_accelerator/`, and `audit_*.py` guards.
- `migration/contracts/*.yaml` — API contracts + `customer_variants` (the place to record per-customer differences).
- `analysis/layout_mappings/<Sobo*>.md` — per-screen legacy→modern mapping notes.
- `legacy-analysis/` — state tracking: `decisions.md` (DEC log), `progress.md`, `open-questions.md`, `known-risks.md`.
- `WeLove_FTP/` — **the legacy Delphi source** (`.pas/.dfm/.dpr`, multiple customer/variant trees) that is the subject of the port; the web app under `도서물류관리프로그램/` is its in-progress port. This is the primary source-of-truth for legacy behavior to reproduce. `legacy_delphi_source/` is an additional captured tree.
- `dashboard/` — static project dashboard (JSON-driven) deployed to a separate public repo.
- `docs/` — runbooks and decision docs; `harness-architecture.md` and `guardrails.md` at root describe the 8-layer harness.

## Conventions

- When planning, split tasks into **standard** vs **advanced-model-recommended** tiers and let the
  human pick the model — don't declare an advanced model mandatory (`planning-model-tiers.mdc`).
- Record non-obvious decisions as new **DEC-NNN** entries in `legacy-analysis/decisions.md`.
- New backend behavior gets a regression test in `test/` and, for routes, an entry in the
  `debug/probe_backend_all_servers.py` smoke matrix.
