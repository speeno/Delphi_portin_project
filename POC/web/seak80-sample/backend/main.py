"""
Seak80 sample API: multi MySQL profiles + G7_Ggeo publisher search.
Aligned with Seak08.pas FilterTing (prefix LIKE on gcode, gname, gposa; no D_Select/Lower).
"""

from __future__ import annotations

import json
import logging
import os
import shutil
from contextlib import asynccontextmanager
from datetime import date
from io import StringIO
from pathlib import Path
from typing import Any, Iterator

import pymysql
import pymysql.err
import yaml
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pymysql.cursors import DictCursor
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse

from pymysql_compat import (
    close_mysql3,
    connect_mysql3,
    install_auth_switch_request_fix,
    install_handshake_plugin_auth_capability_fix,
    pymysql_default_auth_plugin,
    query_mysql3,
)
from seek_sql import (
    build_seek20_mysql3_sql,
    build_seek20_pymysql,
    build_seek30_mysql3_sql,
    build_seek30_pymysql,
    enrich_seek20_rows,
)
from seak04_sql import build_seak04_mysql3_sql, build_seak04_pymysql
from sobo67_aggregate import (
    aggregate_detail_rows,
    footer_totals,
    merge_aggregate_grids,
    merge_sg_csum_gpsum,
)
from sobo67_sql import (
    _escape_literal,
    build_sobo67_detail_mysql3_sql,
    build_sobo67_detail_pymysql,
    build_sobo67_sg_csum_mysql3_sql,
    build_sobo67_sg_csum_pymysql,
)
from phase2_masters_sql import (
    build_phase2_simple_select_mysql3_sql,
    build_phase2_simple_select_pymysql,
    phase2_resolve_form,
)
from sobo_phase1_sql import (
    build_sobo12_g2_gbun_mysql3_sql,
    build_sobo12_g2_gbun_pymysql,
    build_sobo13_t1_gbun_mysql3_sql,
    build_sobo13_t1_gbun_pymysql,
)
from ssh_tunnels import (
    SSHTunnelError,
    invalidate_server_tunnel,
    mysql_connect_host_port,
    shutdown_all_ssh_tunnels,
    tunnel_enabled,
)

install_handshake_plugin_auth_capability_fix()
install_auth_switch_request_fix()

logger = logging.getLogger(__name__)

BACKEND_DIR = Path(__file__).resolve().parent
SAMPLE_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = SAMPLE_ROOT / "frontend"
CONFIG_PATH = Path(
    os.environ.get("SEAK80_SERVERS_CONFIG", str(BACKEND_DIR / "servers.yaml"))
)

# Defaults for remote MySQL; override per server in servers.yaml (connect_timeout, read_timeout).
_DEFAULT_CONNECT_TIMEOUT = int(os.environ.get("SEAK80_DEFAULT_CONNECT_TIMEOUT", "15"))
_DEFAULT_READ_TIMEOUT = int(os.environ.get("SEAK80_DEFAULT_READ_TIMEOUT", "120"))
_SOBO67_DETAIL_CAP = int(os.environ.get("SEAK80_SOBO67_DETAIL_LIMIT", "25000"))
_SOBO67_DETAIL_CHUNK_DEFAULT = int(os.environ.get("SEAK80_SOBO67_DETAIL_CHUNK", "100"))
_SOBO67_READ_TIMEOUT_MAX = int(os.environ.get("SEAK80_SOBO67_READ_TIMEOUT_MAX", "900"))
# G4_Book batch fill: avoid one giant IN(...) / long OR chain (timeouts, mysql3 stalls).
_SOBO67_GNAME_CODES_CHUNK = int(os.environ.get("SEAK80_SOBO67_GNAME_CODES_CHUNK", "400"))
_SOBO67_GNAME_OR_CHUNK = int(os.environ.get("SEAK80_SOBO67_GNAME_OR_CHUNK", "120"))
_SEAK04_DEFAULT_LIMIT = int(os.environ.get("SEAK80_SEAK04_LIMIT", "500"))


@asynccontextmanager
async def _lifespan(app: FastAPI):
    yield
    shutdown_all_ssh_tunnels()


app = FastAPI(
    title="Seak80 sample API",
    version="0.1.0",
    lifespan=_lifespan,
)

# allow_credentials=True is incompatible with allow_origins=["*"] in browsers
_cors_raw = os.environ.get("SEAK80_CORS_ORIGINS", "*").strip()
if _cors_raw == "*":
    _origins, _cred = ["*"], False
else:
    _origins = [o.strip() for o in _cors_raw.split(",") if o.strip()]
    _cred = True
app.add_middleware(
    CORSMiddleware,
    allow_origins=_origins or ["*"],
    allow_credentials=_cred,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EnsureUtf8CharsetMiddleware(BaseHTTPMiddleware):
    """StaticFiles often serves text/* without charset; browsers may mis-decode Korean."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        ct = response.headers.get("content-type")
        if not ct or "charset=" in ct.lower():
            return response
        main = ct.split(";", 1)[0].strip().lower()
        if main in (
            "text/html",
            "text/css",
            "text/javascript",
            "application/javascript",
        ):
            response.headers["content-type"] = main + "; charset=utf-8"
        return response


app.add_middleware(EnsureUtf8CharsetMiddleware)


@app.middleware("http")
async def _log_upstream_errors(request: Request, call_next):
    response = await call_next(request)
    if response.status_code >= 502:
        logger.warning("HTTP %s %s", response.status_code, request.url.path)
    return response


def _read_yaml_file_text(path: Path) -> str:
    """Decode servers.yaml as UTF-8, CP949, or euc-kr (Korean Windows notepad)."""
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig")
    for enc in ("utf-8", "cp949", "euc-kr"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _load_raw_config() -> dict[str, Any]:
    if not CONFIG_PATH.is_file():
        return {"servers": []}
    text = _read_yaml_file_text(CONFIG_PATH)
    try:
        data = yaml.safe_load(StringIO(text))
    except yaml.YAMLError as e:
        raise HTTPException(
            status_code=500,
            detail=f"servers.yaml YAML error ({CONFIG_PATH}): {e}",
        ) from e
    return data if isinstance(data, dict) else {"servers": []}


def _profile_by_id(server_id: str) -> dict[str, Any]:
    sid = (server_id or "").strip()
    for s in _load_raw_config().get("servers", []):
        if not isinstance(s, dict):
            continue
        if (s.get("id") or "").strip() == sid:
            return s
    raise HTTPException(
        status_code=404,
        detail=_error_detail(
            "config",
            f"Unknown serverId {sid!r}: no matching servers[].id in servers.yaml "
            f"(env SEAK80_SERVERS_CONFIG if set). The /api/... URL path is valid; "
            f"404 here means the id is missing from configuration, not a wrong route. "
            f"[KO] "
            + "\uc774 serverId\ub294 servers.yaml\uc5d0 \uc5c6\uc2b5\ub2c8\ub2e4. "
            + "GET /api/servers\ub85c \ub4f1\ub85d\ub41c id\ub97c \ud655\uc778\ud558\uc138\uc694.",
        ),
    )


def _int_from_profile(profile: dict[str, Any], key: str, default: int) -> int:
    if key not in profile or profile[key] is None:
        return default
    return int(profile[key])


def _mysql_password(profile: dict[str, Any]) -> str:
    """YAML password; if missing or whitespace-only, SEAK80_MYSQL_ROOT_PASSWORD."""
    raw = profile.get("password")
    if raw is None:
        return (os.environ.get("SEAK80_MYSQL_ROOT_PASSWORD") or "").strip()
    s = str(raw)
    if not s.strip():
        return (os.environ.get("SEAK80_MYSQL_ROOT_PASSWORD") or "").strip()
    return s


def _mysql_connect_error_detail(exc: pymysql.Error) -> str:
    msg = f"MySQL connection failed: {exc}"
    detail = str(exc)
    if isinstance(exc, pymysql.err.OperationalError) and exc.args and exc.args[0] == 1043:
        msg += (
            " | 1043 Bad handshake: often client/server protocol or charset mismatch. "
            "Try charset: utf8 for MySQL 5.0/5.1, or utf8mb4 for 5.5+; ensure server allows "
            "the chosen default_auth_plugin."
        )
    if isinstance(exc, pymysql.err.OperationalError) and exc.args and exc.args[0] == 1115:
        msg += (
            " | 1115 Unknown character set: older MySQL may not support utf8mb4; "
            "set charset to utf8 in servers.yaml for those hosts."
        )
    if isinstance(exc, pymysql.err.OperationalError) and exc.args and exc.args[0] == 1045:
        msg += (
            " | 1045: Wrong password, or this MySQL user is not allowed from your client IP "
            "(see 'user'@'host' in the message). root is often localhost-only. On the DB server, "
            "CREATE USER ... IDENTIFIED BY ...; GRANT ... TO 'user'@'client_ip_or_%'; FLUSH PRIVILEGES;"
        )
        if "localhost" in detail or "127.0.0.1" in detail:
            msg += (
                " | After an SSH tunnel, MySQL sees the client as localhost: "
                "use 'root'@'localhost' password or a user granted for localhost; "
                "WAN-only accounts (e.g. user@'%') differ. Empty yaml password can use env SEAK80_MYSQL_ROOT_PASSWORD."
            )
    if "unknown auth switch" in detail.lower():
        msg += (
            " | Auth switch: ensure 'cryptography' is installed; try default_auth_plugin: "
            "mysql_native_password in servers.yaml; on DB use ALTER USER ... "
            "IDENTIFIED WITH mysql_native_password BY '...' if the account uses caching_sha2."
        )
    if isinstance(exc, pymysql.err.OperationalError) and exc.args and exc.args[0] == 2013:
        msg += (
            " | 2013: Dropped during handshake or query. Over SSH: app retries once with a fresh tunnel; "
            "try charset utf8 like MySQL 5.1 hosts, longer connect_timeout, and mysqld max_allowed_packet."
        )
    return msg


def _error_detail(stage: str, message: str) -> dict[str, str]:
    """Structured API error for classifying SSH vs MySQL failures (non-138 tunnel paths)."""
    return {"stage": stage, "message": message}


def _connect(
    profile: dict[str, Any],
    *,
    read_timeout_override: int | None = None,
) -> pymysql.connections.Connection:
    charset = str(profile.get("charset") or "utf8mb4").strip() or "utf8mb4"
    if read_timeout_override is not None:
        read_t = int(read_timeout_override)
        write_t = read_t
    else:
        read_t = _int_from_profile(profile, "read_timeout", _DEFAULT_READ_TIMEOUT)
        if "write_timeout" in profile and profile["write_timeout"] is not None:
            write_t = int(profile["write_timeout"])
        else:
            write_t = read_t
    dap = profile.get("default_auth_plugin")
    auth_plugin = str(dap).strip() if dap is not None and str(dap).strip() else None
    connect_timeout = _int_from_profile(
        profile, "connect_timeout", _DEFAULT_CONNECT_TIMEOUT
    )
    server_id = (profile.get("id") or "").strip()
    use_tunnel_retry = tunnel_enabled(profile) and bool(server_id)
    attempts = 2 if use_tunnel_retry else 1

    for attempt in range(attempts):
        try:
            mysql_host, mysql_port = mysql_connect_host_port(profile)
        except ValueError as e:
            raise HTTPException(
                status_code=500, detail=_error_detail("config", str(e))
            ) from e
        except SSHTunnelError as e:
            raise HTTPException(
                status_code=502, detail=_error_detail("ssh", str(e))
            ) from e
        try:
            with pymysql_default_auth_plugin(auth_plugin):
                return pymysql.connect(
                    host=mysql_host,
                    port=mysql_port,
                    user=profile["user"],
                    password=_mysql_password(profile),
                    database=profile["database"],
                    charset=charset,
                    cursorclass=DictCursor,
                    connect_timeout=connect_timeout,
                    read_timeout=read_t,
                    write_timeout=write_t,
                )
        except pymysql.OperationalError as e:
            if (
                use_tunnel_retry
                and attempt == 0
                and e.args
                and e.args[0] == 2013
            ):
                invalidate_server_tunnel(server_id)
                continue
            raise HTTPException(
                status_code=502,
                detail=_error_detail("mysql", _mysql_connect_error_detail(e)),
            ) from e
        except pymysql.Error as e:
            raise HTTPException(
                status_code=502,
                detail=_error_detail("mysql", _mysql_connect_error_detail(e)),
            ) from e

    raise RuntimeError("_connect: unexpected fall-through")  # pragma: no cover


@app.get("/api/health")
def health() -> dict[str, Any]:
    # Deployment probe: legacy stacks may return only {"status": "ok"} without "capabilities".
    return {
        "status": "ok",
        "capabilities": {
            "seek20Search": True,
            "seek30Search": True,
            "sobo12G2Gbun": True,
            "sobo13T1Gbun": True,
            "phase2MastersRead": True,
            "sobo67Search": True,
            "sobo67Subu67Pipeline": True,
            "seak04Search": True,
        },
    }


@app.get("/api/ssh-env")
def ssh_env() -> dict[str, str]:
    """154/155 use_system_ssh needs `ssh` and usually `sshpass` on PATH (502 often = missing sshpass or pipe deadlock)."""
    return {
        "ssh_path": shutil.which("ssh") or "",
        "sshpass_path": shutil.which("sshpass") or "",
    }


@app.get("/api/servers")
def list_servers() -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    for s in _load_raw_config().get("servers", []):
        if not isinstance(s, dict):
            continue
        sid = (s.get("id") or "").strip()
        if not sid:
            continue
        out.append({"id": sid, "label": (s.get("label") or sid).strip()})
    return out


def _build_publisher_sql(term: str, limit: int | None) -> str:
    base = (
        "SELECT gubun, jubun, gcode, ocode, gname, gposa, gtel1, gtel2, gadd1, gadd2"
        " FROM G7_Ggeo"
    )
    if term:
        escaped = term.replace("'", "''").replace("\\", "\\\\")
        where = (
            f" WHERE (gcode LIKE '{escaped}%'"
            f" OR gname LIKE '{escaped}%'"
            f" OR gposa LIKE '{escaped}%')"
        )
    else:
        where = " WHERE 1=1"
    sql = base + where + " ORDER BY gcode"
    if limit is not None:
        sql += f" LIMIT {int(limit)}"
    return sql


def _is_mysql3_profile(profile: dict[str, Any]) -> bool:
    return bool(profile.get("mysql3_protocol"))


def _d_select_sql_prefix(profile: dict[str, Any]) -> str:
    """Legacy D_Select fragment concatenated right after WHERE (see servers.yaml d_select_sql)."""
    raw = profile.get("d_select_sql")
    if raw is None:
        return ""
    return str(raw).strip()


def _seek20_search_impl(
    profile: dict[str, Any],
    server_id: str,
    term: str,
    hcode: str,
    *,
    lower_mode: bool,
    exclude_grat9: bool,
    limit200: bool,
    limit_cap: int | None,
) -> list[dict[str, Any]]:
    d_sel = _d_select_sql_prefix(profile)
    include_gqut9 = True

    def run_mysql3(gq: bool) -> list[dict[str, Any]]:
        sql = build_seek20_mysql3_sql(
            term,
            hcode,
            d_sel,
            lower_mode=lower_mode,
            exclude_grat9=exclude_grat9,
            limit200=limit200,
            limit_cap=limit_cap,
            include_gqut9=gq,
        )
        conn3: dict[str, Any] | None = None
        try:
            mysql_host, mysql_port = mysql_connect_host_port(profile)
            conn3 = connect_mysql3(
                host=mysql_host,
                port=mysql_port,
                user=profile["user"],
                password=_mysql_password(profile),
                database=profile["database"],
                connect_timeout=_int_from_profile(
                    profile, "connect_timeout", _DEFAULT_CONNECT_TIMEOUT
                ),
                read_timeout=_int_from_profile(
                    profile, "read_timeout", _DEFAULT_READ_TIMEOUT
                ),
            )
            mysql3_charset = str(profile.get("mysql3_charset") or "euc-kr").strip()
            return query_mysql3(conn3, sql, charset=mysql3_charset)
        finally:
            if conn3 is not None:
                close_mysql3(conn3)

    def run_pymysql(gq: bool) -> list[dict[str, Any]]:
        sql, params = build_seek20_pymysql(
            term,
            hcode,
            d_sel,
            lower_mode=lower_mode,
            exclude_grat9=exclude_grat9,
            limit200=limit200,
            limit_cap=limit_cap,
            include_gqut9=gq,
        )
        rows: list[Any] = []
        conn: Any = None
        try:
            for attempt in range(2):
                conn = _connect(profile)
                try:
                    with conn.cursor() as cur:
                        cur.execute(sql, params)
                        rows = cur.fetchall()
                    break
                except pymysql.OperationalError as e:
                    try:
                        conn.close()
                    except Exception:
                        pass
                    conn = None
                    if (
                        attempt == 0
                        and e.args
                        and e.args[0] == 2013
                        and tunnel_enabled(profile)
                    ):
                        invalidate_server_tunnel(server_id)
                        continue
                    if e.args and e.args[0] == 1054:
                        raise
                    raise HTTPException(
                        status_code=502,
                        detail=_error_detail("mysql_query", f"Query failed: {e}"),
                    ) from e
                except pymysql.Error as e:
                    try:
                        conn.close()
                    except Exception:
                        pass
                    conn = None
                    raise HTTPException(
                        status_code=502,
                        detail=_error_detail("mysql_query", f"Query failed: {e}"),
                    ) from e
            else:
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail(
                        "mysql_query",
                        "Query failed: SSH tunnel retry exhausted (2013)",
                    ),
                )
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
        return rows

    if _is_mysql3_profile(profile):
        try:
            try:
                rows = run_mysql3(include_gqut9)
            except pymysql.OperationalError as e:
                if e.args and e.args[0] == 1054 and include_gqut9:
                    rows = run_mysql3(False)
                else:
                    raise HTTPException(
                        status_code=502,
                        detail=_error_detail("mysql_query", f"Query failed: {e}"),
                    ) from e
        except SSHTunnelError as e:
            raise HTTPException(
                status_code=502, detail=_error_detail("ssh", str(e))
            ) from e
        except ValueError as e:
            raise HTTPException(
                status_code=500, detail=_error_detail("config", str(e))
            ) from e
        return enrich_seek20_rows(rows)

    try:
        rows = run_pymysql(include_gqut9)
    except pymysql.OperationalError as e:
        if e.args and e.args[0] == 1054 and include_gqut9:
            rows = run_pymysql(False)
        else:
            raise HTTPException(
                status_code=502,
                detail=_error_detail("mysql_query", f"Query failed: {e}"),
            ) from e
    return enrich_seek20_rows(rows)


def _seek30_search_impl(
    profile: dict[str, Any],
    server_id: str,
    term: str,
    hcode: str,
    *,
    lower_mode: bool,
    limit200: bool,
    limit_cap: int | None,
) -> list[dict[str, Any]]:
    d_sel = _d_select_sql_prefix(profile)

    if _is_mysql3_profile(profile):
        sql = build_seek30_mysql3_sql(
            term,
            hcode,
            d_sel,
            lower_mode=lower_mode,
            limit200=limit200,
            limit_cap=limit_cap,
        )
        conn3: dict[str, Any] | None = None
        try:
            try:
                mysql_host, mysql_port = mysql_connect_host_port(profile)
                conn3 = connect_mysql3(
                    host=mysql_host,
                    port=mysql_port,
                    user=profile["user"],
                    password=_mysql_password(profile),
                    database=profile["database"],
                    connect_timeout=_int_from_profile(
                        profile, "connect_timeout", _DEFAULT_CONNECT_TIMEOUT
                    ),
                    read_timeout=_int_from_profile(
                        profile, "read_timeout", _DEFAULT_READ_TIMEOUT
                    ),
                )
                mysql3_charset = str(profile.get("mysql3_charset") or "euc-kr").strip()
                return query_mysql3(conn3, sql, charset=mysql3_charset)
            except pymysql.OperationalError as e:
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
            except pymysql.Error as e:
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
        except SSHTunnelError as e:
            raise HTTPException(
                status_code=502, detail=_error_detail("ssh", str(e))
            ) from e
        except ValueError as e:
            raise HTTPException(
                status_code=500, detail=_error_detail("config", str(e))
            ) from e
        finally:
            if conn3 is not None:
                close_mysql3(conn3)

    sql, params = build_seek30_pymysql(
        term,
        hcode,
        d_sel,
        lower_mode=lower_mode,
        limit200=limit200,
        limit_cap=limit_cap,
    )
    rows: list[Any] = []
    conn: Any = None
    try:
        for attempt in range(2):
            conn = _connect(profile)
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    rows = cur.fetchall()
                break
            except pymysql.OperationalError as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                if (
                    attempt == 0
                    and e.args
                    and e.args[0] == 2013
                    and tunnel_enabled(profile)
                ):
                    invalidate_server_tunnel(server_id)
                    continue
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
            except pymysql.Error as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
        else:
            raise HTTPException(
                status_code=502,
                detail=_error_detail(
                    "mysql_query",
                    "Query failed: SSH tunnel retry exhausted (2013)",
                ),
            )
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
    return rows


def _seak04_search_impl(
    profile: dict[str, Any],
    server_id: str,
    term: str,
    *,
    limit_rows: int,
) -> list[dict[str, Any]]:
    """Gg_Post postal search (Seak04.pas FilterTing). Caller validates term length."""
    if _is_mysql3_profile(profile):
        sql = build_seak04_mysql3_sql(term, limit_rows)
        conn3: dict[str, Any] | None = None
        try:
            try:
                mysql_host, mysql_port = mysql_connect_host_port(profile)
                conn3 = connect_mysql3(
                    host=mysql_host,
                    port=mysql_port,
                    user=profile["user"],
                    password=_mysql_password(profile),
                    database=profile["database"],
                    connect_timeout=_int_from_profile(
                        profile, "connect_timeout", _DEFAULT_CONNECT_TIMEOUT
                    ),
                    read_timeout=_int_from_profile(
                        profile, "read_timeout", _DEFAULT_READ_TIMEOUT
                    ),
                )
                mysql3_charset = str(profile.get("mysql3_charset") or "euc-kr").strip()
                return query_mysql3(conn3, sql, charset=mysql3_charset)
            except pymysql.OperationalError as e:
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
            except pymysql.Error as e:
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
        except SSHTunnelError as e:
            raise HTTPException(
                status_code=502, detail=_error_detail("ssh", str(e))
            ) from e
        except ValueError as e:
            raise HTTPException(
                status_code=500, detail=_error_detail("config", str(e))
            ) from e
        finally:
            if conn3 is not None:
                close_mysql3(conn3)

    sql, params = build_seak04_pymysql(term, limit_rows)
    rows: list[Any] = []
    conn: Any = None
    try:
        for attempt in range(2):
            conn = _connect(profile)
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    rows = cur.fetchall()
                break
            except pymysql.OperationalError as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                if (
                    attempt == 0
                    and e.args
                    and e.args[0] == 2013
                    and tunnel_enabled(profile)
                ):
                    invalidate_server_tunnel(server_id)
                    continue
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
            except pymysql.Error as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
        else:
            raise HTTPException(
                status_code=502,
                detail=_error_detail(
                    "mysql_query",
                    "Query failed: SSH tunnel retry exhausted (2013)",
                ),
            )
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass
    return rows


def _search_mysql3(
    profile: dict[str, Any],
    server_id: str,
    term: str,
    limit: int | None,
) -> list[dict[str, Any]]:
    """Query via raw MySQL 3.x protocol (no PyMySQL)."""
    try:
        mysql_host, mysql_port = mysql_connect_host_port(profile)
    except ValueError as e:
        raise HTTPException(
            status_code=500, detail=_error_detail("config", str(e))
        ) from e
    except SSHTunnelError as e:
        raise HTTPException(
            status_code=502, detail=_error_detail("ssh", str(e))
        ) from e

    sql = _build_publisher_sql(term, limit)
    conn3: dict[str, Any] | None = None
    try:
        conn3 = connect_mysql3(
            host=mysql_host,
            port=mysql_port,
            user=profile["user"],
            password=_mysql_password(profile),
            database=profile["database"],
            connect_timeout=_int_from_profile(
                profile, "connect_timeout", _DEFAULT_CONNECT_TIMEOUT
            ),
            read_timeout=_int_from_profile(profile, "read_timeout", _DEFAULT_READ_TIMEOUT),
        )
        mysql3_charset = str(profile.get("mysql3_charset") or "euc-kr").strip()
        return query_mysql3(conn3, sql, charset=mysql3_charset)
    except pymysql.OperationalError as e:
        raise HTTPException(
            status_code=502,
            detail=_error_detail("mysql", _mysql_connect_error_detail(e)),
        ) from e
    except pymysql.Error as e:
        raise HTTPException(
            status_code=502,
            detail=_error_detail("mysql", _mysql_connect_error_detail(e)),
        ) from e
    finally:
        if conn3 is not None:
            close_mysql3(conn3)


@app.get("/api/publishers")
def search_publishers(
    server_id: str = Query(..., alias="serverId"),
    q: str = Query(
        "",
        description="Prefix search; empty returns all rows ordered by gcode (unless limit is set)",
    ),
    limit: int | None = Query(
        None,
        ge=1,
        description="Optional max rows; omit for no LIMIT (full result set)",
    ),
) -> dict[str, Any]:
    profile = _profile_by_id(server_id)
    term = (q or "").strip()

    if _is_mysql3_profile(profile):
        rows = _search_mysql3(profile, server_id, term, limit)
        return {"rows": rows, "count": len(rows), "serverId": server_id, "q": term}

    base_sql = """
        SELECT
            gubun AS gubun,
            jubun AS jubun,
            gcode AS gcode,
            ocode AS ocode,
            gname AS gname,
            gposa AS gposa,
            gtel1 AS gtel1,
            gtel2 AS gtel2,
            gadd1 AS gadd1,
            gadd2 AS gadd2
        FROM G7_Ggeo
    """

    if term:
        where = """
            WHERE (
                gcode LIKE %s OR gname LIKE %s OR gposa LIKE %s
            )
        """
        prefix = term + "%"
        params: list[Any] = [prefix, prefix, prefix]
    else:
        where = "WHERE 1=1"
        params = []

    sql = base_sql + where + " ORDER BY gcode"
    if limit is not None:
        sql += " LIMIT %s"
        params.append(limit)

    rows: list[Any] = []
    conn: Any = None
    try:
        for attempt in range(2):
            conn = _connect(profile)
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    rows = cur.fetchall()
                break
            except pymysql.OperationalError as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                if (
                    attempt == 0
                    and e.args
                    and e.args[0] == 2013
                    and tunnel_enabled(profile)
                ):
                    invalidate_server_tunnel(server_id)
                    continue
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
            except pymysql.Error as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
        else:
            raise HTTPException(
                status_code=502,
                detail=_error_detail(
                    "mysql_query",
                    "Query failed: SSH tunnel retry exhausted (2013)",
                ),
            )
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass

    return {"rows": rows, "count": len(rows), "serverId": server_id, "q": term}


@app.get("/api/seek20/search")
def seek20_search(
    server_id: str = Query(..., alias="serverId"),
    q: str = Query(
        "",
        description="Search term; empty omits keyword filter (all rows under D_Select / limits)",
    ),
    hcode: str = Query(
        "",
        description="Hcode filter (legacy Hnnnn); empty omits Hcode predicate (all Hcode values)",
    ),
    limit200: bool = Query(False, alias="limit200"),
    lower: bool = Query(False, description="LOWER(col) LIKE LOWER('%%term%%') when Lower='1'"),
    exclude_grat9: bool = Query(False, alias="excludeGrat9"),
    limit: int | None = Query(
        None,
        ge=1,
        description="Optional max rows; combined with limit200 as min(200,limit) when both set",
    ),
) -> dict[str, Any]:
    """Seek20 inbound supplier search on G2_Ggwo (Seek02.pas FilterTing)."""
    term = (q or "").strip()
    hc = (hcode or "").strip()
    profile = _profile_by_id(server_id)
    rows = _seek20_search_impl(
        profile,
        server_id,
        term,
        hc,
        lower_mode=lower,
        exclude_grat9=exclude_grat9,
        limit200=limit200,
        limit_cap=limit,
    )
    return {
        "rows": rows,
        "count": len(rows),
        "serverId": server_id,
        "q": term,
        "hcode": hc,
    }


@app.get("/api/seek30/search")
def seek30_search(
    server_id: str = Query(..., alias="serverId"),
    q: str = Query(
        "",
        description="Search term; empty omits keyword filter (all rows under D_Select / limits)",
    ),
    hcode: str = Query(
        "",
        description="Hcode (legacy Edit3); empty omits Hcode predicate (all Hcode values)",
    ),
    limit200: bool = Query(False, alias="limit200"),
    lower: bool = Query(False, description="LOWER() contains match when Lower='1'"),
    limit: int | None = Query(
        None,
        ge=1,
        description="Optional max rows; with limit200 uses min(200,limit)",
    ),
) -> dict[str, Any]:
    """Seek30 author search on G3_Gjeo (Seek03.pas FilterTing)."""
    term = (q or "").strip()
    hc = (hcode or "").strip()
    profile = _profile_by_id(server_id)
    rows = _seek30_search_impl(
        profile,
        server_id,
        term,
        hc,
        lower_mode=lower,
        limit200=limit200,
        limit_cap=limit,
    )
    return {
        "rows": rows,
        "count": len(rows),
        "serverId": server_id,
        "q": term,
        "hcode": hc,
    }


@app.get("/api/seak04/search")
def seak04_search(
    server_id: str = Query(..., alias="serverId"),
    q: str = Query("", description="post/addr contains match (Seak04 FilterTing)"),
    limit: int = Query(
        _SEAK04_DEFAULT_LIMIT,
        ge=1,
        le=5000,
        description="Max rows (Delphi had no LIMIT; API safety cap)",
    ),
) -> dict[str, Any]:
    """Postal code / address search on Gg_Post (Seak04.pas FilterTing)."""
    term = (q or "").strip()
    profile = _profile_by_id(server_id)
    if not term:
        return {"rows": [], "count": 0, "serverId": server_id, "q": term, "limit": limit}
    if len(term) < 4:
        raise HTTPException(
            status_code=400,
            detail=_error_detail(
                "validation",
                "\ud55c\uae002\uc790,\uc22b\uc7904\uc790 \uc774\uc0c1 \uc785\ub825\ud558\uc138\uc694.",
            ),
        )
    rows = _seak04_search_impl(profile, server_id, term, limit_rows=limit)
    return {
        "rows": rows,
        "count": len(rows),
        "serverId": server_id,
        "q": term,
        "limit": limit,
    }


def _sobo13_t1_gbun_rows(
    profile: dict[str, Any],
    server_id: str,
    *,
    hcode: str,
    gcode: str,
    limit_rows: int,
) -> list[dict[str, Any]]:
    """Read-only T1_Gbun (Subu13 Button101-style WHERE)."""
    d_sel = _d_select_sql_prefix(profile)
    if _is_mysql3_profile(profile):
        try:
            sql = build_sobo13_t1_gbun_mysql3_sql(
                d_select_prefix=d_sel,
                hcode=hcode,
                gcode=gcode,
                limit_rows=limit_rows,
            )
        except ValueError as e:
            raise HTTPException(
                status_code=400, detail=_error_detail("validation", str(e))
            ) from e
        conn3: dict[str, Any] | None = None
        try:
            try:
                mysql_host, mysql_port = mysql_connect_host_port(profile)
                conn3 = connect_mysql3(
                    host=mysql_host,
                    port=mysql_port,
                    user=profile["user"],
                    password=_mysql_password(profile),
                    database=profile["database"],
                    connect_timeout=_int_from_profile(
                        profile, "connect_timeout", _DEFAULT_CONNECT_TIMEOUT
                    ),
                    read_timeout=_int_from_profile(
                        profile, "read_timeout", _DEFAULT_READ_TIMEOUT
                    ),
                )
                mysql3_charset = str(profile.get("mysql3_charset") or "euc-kr").strip()
                raw = query_mysql3(conn3, sql, charset=mysql3_charset)
                return [_sobo67_normalize_row(x) for x in raw]
            except ValueError as e:
                raise HTTPException(
                    status_code=400, detail=_error_detail("validation", str(e))
                ) from e
            except SSHTunnelError as e:
                raise HTTPException(
                    status_code=502, detail=_error_detail("ssh", str(e))
                ) from e
        finally:
            if conn3 is not None:
                close_mysql3(conn3)

    try:
        sql, params = build_sobo13_t1_gbun_pymysql(
            d_select_prefix=d_sel,
            hcode=hcode,
            gcode=gcode,
            limit_rows=limit_rows,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=_error_detail("validation", str(e))
        ) from e
    conn: Any = None
    try:
        for attempt in range(2):
            conn = _connect(profile)
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    return [_sobo67_normalize_row(x) for x in cur.fetchall()]
            except pymysql.OperationalError as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                if (
                    attempt == 0
                    and e.args
                    and e.args[0] == 2013
                    and tunnel_enabled(profile)
                ):
                    invalidate_server_tunnel(server_id)
                    continue
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
            except pymysql.Error as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
        raise HTTPException(
            status_code=502,
            detail=_error_detail(
                "mysql_query",
                "Query failed: SSH tunnel retry exhausted (2013)",
            ),
        )
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


def _sobo12_g2_gbun_rows(
    profile: dict[str, Any],
    server_id: str,
    *,
    hcode: str,
    limit_rows: int,
) -> list[dict[str, Any]]:
    """Read-only G2_Gbun (Subu12 G2_Gbun grid)."""
    d_sel = _d_select_sql_prefix(profile)
    if _is_mysql3_profile(profile):
        try:
            sql = build_sobo12_g2_gbun_mysql3_sql(
                d_select_prefix=d_sel,
                hcode=hcode,
                limit_rows=limit_rows,
            )
        except ValueError as e:
            raise HTTPException(
                status_code=400, detail=_error_detail("validation", str(e))
            ) from e
        conn3: dict[str, Any] | None = None
        try:
            mysql_host, mysql_port = mysql_connect_host_port(profile)
            conn3 = connect_mysql3(
                host=mysql_host,
                port=mysql_port,
                user=profile["user"],
                password=_mysql_password(profile),
                database=profile["database"],
                connect_timeout=_int_from_profile(
                    profile, "connect_timeout", _DEFAULT_CONNECT_TIMEOUT
                ),
                read_timeout=_int_from_profile(
                    profile, "read_timeout", _DEFAULT_READ_TIMEOUT
                ),
            )
            mysql3_charset = str(profile.get("mysql3_charset") or "euc-kr").strip()
            raw = query_mysql3(conn3, sql, charset=mysql3_charset)
            return [_sobo67_normalize_row(x) for x in raw]
        except ValueError as e:
            raise HTTPException(
                status_code=400, detail=_error_detail("validation", str(e))
            ) from e
        except SSHTunnelError as e:
            raise HTTPException(
                status_code=502, detail=_error_detail("ssh", str(e))
            ) from e
        finally:
            if conn3 is not None:
                close_mysql3(conn3)

    try:
        sql, params = build_sobo12_g2_gbun_pymysql(
            d_select_prefix=d_sel,
            hcode=hcode,
            limit_rows=limit_rows,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=_error_detail("validation", str(e))
        ) from e
    conn: Any = None
    try:
        for attempt in range(2):
            conn = _connect(profile)
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    return [_sobo67_normalize_row(x) for x in cur.fetchall()]
            except pymysql.OperationalError as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                if (
                    attempt == 0
                    and e.args
                    and e.args[0] == 2013
                    and tunnel_enabled(profile)
                ):
                    invalidate_server_tunnel(server_id)
                    continue
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
            except pymysql.Error as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
        raise HTTPException(
            status_code=502,
            detail=_error_detail(
                "mysql_query",
                "Query failed: SSH tunnel retry exhausted (2013)",
            ),
        )
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


@app.get("/api/sobo13/t1-gbun")
def sobo13_t1_gbun(
    server_id: str = Query(..., alias="serverId"),
    hcode: str = Query("", description="Hcode; empty = all Hcode (Seek30-style)"),
    gcode: str = Query("", description="Optional Gcode filter (Subu13 Edit101)"),
    limit: int = Query(500, ge=1, le=2000),
) -> dict[str, Any]:
    """Phase-1 POC: Sobo13 ???????? ? T1_Gbun read-only list."""
    profile = _profile_by_id(server_id)
    rows = _sobo13_t1_gbun_rows(
        profile,
        server_id,
        hcode=hcode,
        gcode=gcode,
        limit_rows=limit,
    )
    return {
        "rows": rows,
        "count": len(rows),
        "serverId": server_id,
        "hcode": (hcode or "").strip(),
        "gcode": (gcode or "").strip(),
        "table": "T1_Gbun",
    }


@app.get("/api/sobo12/g2-gbun")
def sobo12_g2_gbun(
    server_id: str = Query(..., alias="serverId"),
    hcode: str = Query("", description="Hcode; empty = all Hcode (Seek20-style)"),
    limit: int = Query(500, ge=1, le=2000),
) -> dict[str, Any]:
    """Phase-1 POC: Sobo12 ???? ? G2_Gbun read-only list."""
    profile = _profile_by_id(server_id)
    rows = _sobo12_g2_gbun_rows(
        profile,
        server_id,
        hcode=hcode,
        limit_rows=limit,
    )
    return {
        "rows": rows,
        "count": len(rows),
        "serverId": server_id,
        "hcode": (hcode or "").strip(),
        "table": "G2_Gbun",
    }


def _sobo67_normalize_row(r: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for k, v in r.items():
        lk = k.lower() if isinstance(k, str) else k
        out[str(lk)] = v
    return out


def _phase2_master_rows(
    profile: dict[str, Any],
    server_id: str,
    *,
    form_id: str,
    hcode: str,
    limit_rows: int,
) -> tuple[list[dict[str, Any]], str]:
    """Read-only single-table list for phase-2 masters hub (PyMySQL or mysql3)."""
    spec = phase2_resolve_form(form_id)
    if not spec:
        raise HTTPException(
            status_code=404,
            detail=_error_detail(
                "validation",
                f"Unknown phase2 form: {(form_id or '').strip()!r}",
            ),
        )
    table, order_by = spec
    d_sel = _d_select_sql_prefix(profile)
    if _is_mysql3_profile(profile):
        try:
            sql = build_phase2_simple_select_mysql3_sql(
                d_select_prefix=d_sel,
                table=table,
                order_by=order_by,
                hcode=hcode,
                limit_rows=limit_rows,
            )
        except ValueError as e:
            raise HTTPException(
                status_code=400, detail=_error_detail("validation", str(e))
            ) from e
        conn3: dict[str, Any] | None = None
        try:
            mysql_host, mysql_port = mysql_connect_host_port(profile)
            conn3 = connect_mysql3(
                host=mysql_host,
                port=mysql_port,
                user=profile["user"],
                password=_mysql_password(profile),
                database=profile["database"],
                connect_timeout=_int_from_profile(
                    profile, "connect_timeout", _DEFAULT_CONNECT_TIMEOUT
                ),
                read_timeout=_int_from_profile(
                    profile, "read_timeout", _DEFAULT_READ_TIMEOUT
                ),
            )
            mysql3_charset = str(profile.get("mysql3_charset") or "euc-kr").strip()
            raw = query_mysql3(conn3, sql, charset=mysql3_charset)
            return [_sobo67_normalize_row(x) for x in raw], table
        except ValueError as e:
            raise HTTPException(
                status_code=400, detail=_error_detail("validation", str(e))
            ) from e
        except SSHTunnelError as e:
            raise HTTPException(
                status_code=502, detail=_error_detail("ssh", str(e))
            ) from e
        finally:
            if conn3 is not None:
                close_mysql3(conn3)

    try:
        sql, params = build_phase2_simple_select_pymysql(
            d_select_prefix=d_sel,
            table=table,
            order_by=order_by,
            hcode=hcode,
            limit_rows=limit_rows,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=_error_detail("validation", str(e))
        ) from e
    conn: Any = None
    try:
        for attempt in range(2):
            conn = _connect(profile)
            try:
                with conn.cursor() as cur:
                    cur.execute(sql, params)
                    return [_sobo67_normalize_row(x) for x in cur.fetchall()], table
            except pymysql.OperationalError as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                if (
                    attempt == 0
                    and e.args
                    and e.args[0] == 2013
                    and tunnel_enabled(profile)
                ):
                    invalidate_server_tunnel(server_id)
                    continue
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
            except pymysql.Error as e:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
                raise HTTPException(
                    status_code=502,
                    detail=_error_detail("mysql_query", f"Query failed: {e}"),
                ) from e
        raise HTTPException(
            status_code=502,
            detail=_error_detail(
                "mysql_query",
                "Query failed: SSH tunnel retry exhausted (2013)",
            ),
        )
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


@app.get("/api/phase2/{form_id}/list")
def phase2_master_list(
    form_id: str,
    server_id: str = Query(..., alias="serverId"),
    hcode: str = Query("", description="Hcode; empty = all Hcode (Seek20-style)"),
    limit: int = Query(500, ge=1, le=2000),
) -> dict[str, Any]:
    """Phase-2 POC: read-only single-table list per masters-hub form_id."""
    profile = _profile_by_id(server_id)
    rows, table = _phase2_master_rows(
        profile,
        server_id,
        form_id=form_id,
        hcode=hcode,
        limit_rows=limit,
    )
    return {
        "rows": rows,
        "count": len(rows),
        "serverId": server_id,
        "formId": (form_id or "").strip().lower(),
        "hcode": (hcode or "").strip(),
        "table": table,
    }


def _sobo67_fill_missing_gnames_pymysql(
    conn: Any, filter_hcode: str, rows: list[dict[str, Any]]
) -> None:
    """Seek_Code-style batch when JOIN left Gname empty (G4_Book)."""
    if not rows:
        return
    fh = (filter_hcode or "").strip()
    pairs: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for r in rows:
        if str(r.get("gname") or "").strip():
            continue
        bc = str(r.get("bcode") or r.get("gcode") or "").strip()
        if not bc:
            continue
        rh = (fh or str(r.get("row_hcode") or "")).strip()
        if not rh:
            continue
        key = (rh, bc)
        if key not in seen:
            seen.add(key)
            pairs.append(key)
    if not pairs:
        return

    found: dict[tuple[str, str], str] = {}
    with conn.cursor() as cur:
        if fh:
            codes = sorted({bc for _rh, bc in pairs})
            ch = max(50, min(_SOBO67_GNAME_CODES_CHUNK, 2000))
            for off in range(0, len(codes), ch):
                sub = codes[off : off + ch]
                if not sub:
                    break
                placeholders = ",".join(["%s"] * len(sub))
                sql = (
                    "SELECT Gcode AS gcode, MAX(Gname) AS gname FROM G4_Book "
                    f"WHERE Hcode = %s AND TRIM(Gcode) IN ({placeholders}) GROUP BY Gcode"
                )
                params: list[Any] = [fh] + sub
                cur.execute(sql, params)
                for x in cur.fetchall():
                    gco = str(x["gcode"]).strip()
                    if gco:
                        found[(fh, gco)] = str(x.get("gname") or "").strip()
        else:
            och = max(20, min(_SOBO67_GNAME_OR_CHUNK, 300))
            for off in range(0, len(pairs), och):
                chunk = pairs[off : off + och]
                if not chunk:
                    break
                or_parts = ["(Hcode = %s AND TRIM(Gcode) = %s)"] * len(chunk)
                flat: list[Any] = []
                for rh, bc in chunk:
                    flat.extend([rh, bc])
                sql = (
                    "SELECT Hcode AS hcode, Gcode AS gcode, Gname AS gname FROM G4_Book WHERE "
                    + " OR ".join(or_parts)
                )
                cur.execute(sql, flat)
                for x in cur.fetchall():
                    hk = str(x["hcode"]).strip()
                    gk = str(x["gcode"]).strip()
                    if hk and gk:
                        found[(hk, gk)] = str(x.get("gname") or "").strip()

    for r in rows:
        if str(r.get("gname") or "").strip():
            continue
        bc = str(r.get("bcode") or r.get("gcode") or "").strip()
        rh = (fh or str(r.get("row_hcode") or "")).strip()
        if bc and rh:
            r["gname"] = found.get((rh, bc), "")


def _sobo67_fill_missing_gnames_mysql3(
    conn3: dict[str, Any],
    filter_hcode: str,
    rows: list[dict[str, Any]],
    charset: str,
) -> None:
    """G4_Book batch fill for mysql3_protocol (same semantics as _sobo67_fill_missing_gnames_pymysql)."""
    if not rows:
        return
    fh = (filter_hcode or "").strip()
    pairs: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for r in rows:
        if str(r.get("gname") or "").strip():
            continue
        bc = str(r.get("bcode") or r.get("gcode") or "").strip()
        if not bc:
            continue
        rh = (fh or str(r.get("row_hcode") or "")).strip()
        if not rh:
            continue
        key = (rh, bc)
        if key not in seen:
            seen.add(key)
            pairs.append(key)
    if not pairs:
        return

    esc = _escape_literal
    found: dict[tuple[str, str], str] = {}

    if fh:
        codes = sorted({bc for _rh, bc in pairs})
        ch = max(50, min(_SOBO67_GNAME_CODES_CHUNK, 2000))
        for off in range(0, len(codes), ch):
            sub = codes[off : off + ch]
            if not sub:
                break
            in_list = ",".join(f"'{esc(c)}'" for c in sub)
            sql = (
                "SELECT Gcode AS gcode, MAX(Gname) AS gname FROM G4_Book "
                f"WHERE Hcode = '{esc(fh)}' AND TRIM(Gcode) IN ({in_list}) GROUP BY Gcode"
            )
            raw = query_mysql3(conn3, sql, charset=charset)
            for x in raw:
                nx = _sobo67_normalize_row(x)
                gco = str(nx.get("gcode") or "").strip()
                if gco:
                    found[(fh, gco)] = str(nx.get("gname") or "").strip()
    else:
        och = max(20, min(_SOBO67_GNAME_OR_CHUNK, 300))
        for off in range(0, len(pairs), och):
            chunk = pairs[off : off + och]
            if not chunk:
                break
            or_parts = [
                f"(Hcode = '{esc(rh)}' AND TRIM(Gcode) = '{esc(bc)}')"
                for rh, bc in chunk
            ]
            sql = (
                "SELECT Hcode AS hcode, Gcode AS gcode, Gname AS gname FROM G4_Book WHERE "
                + " OR ".join(or_parts)
            )
            raw = query_mysql3(conn3, sql, charset=charset)
            for x in raw:
                nx = _sobo67_normalize_row(x)
                hk = str(nx.get("hcode") or "").strip()
                gk = str(nx.get("gcode") or "").strip()
                if hk and gk:
                    found[(hk, gk)] = str(nx.get("gname") or "").strip()

    for r in rows:
        if str(r.get("gname") or "").strip():
            continue
        bc = str(r.get("bcode") or r.get("gcode") or "").strip()
        rh = (fh or str(r.get("row_hcode") or "")).strip()
        if bc and rh:
            r["gname"] = found.get((rh, bc), "")


def _sobo67_clamp_read_timeout_for_search(read_timeout_sec: int | None) -> int | None:
    if read_timeout_sec is None:
        return None
    return max(10, min(int(read_timeout_sec), _SOBO67_READ_TIMEOUT_MAX))


def _sobo67_proto_search_events_mysql3(
    profile: dict[str, Any],
    *,
    gk: str,
    year_grain: bool,
    d_sel: str,
    date_from: str,
    date_to: str,
    hcode: str,
    book_mode: str,
    scode_filter: bool,
    bcode_from: str,
    bcode_to: str,
    parent_gcode: str,
    t00: int,
    detail_cap: int,
    chunk: int,
    read_timeout_override: int | None,
) -> Iterator[dict[str, Any]]:
    sql_sg = build_sobo67_sg_csum_mysql3_sql(
        d_select_prefix=d_sel,
        date_from=date_from,
        date_to=date_to,
        hcode=hcode,
        book_mode=book_mode,
        bcode_from=bcode_from,
        bcode_to=bcode_to,
        parent_bcode=parent_gcode,
        t00=t00,
        limit_rows=detail_cap,
    )
    read_mysql3 = (
        int(read_timeout_override)
        if read_timeout_override is not None
        else _int_from_profile(profile, "read_timeout", _DEFAULT_READ_TIMEOUT)
    )
    conn3: dict[str, Any] | None = None
    try:
        mysql_host, mysql_port = mysql_connect_host_port(profile)
        conn3 = connect_mysql3(
            host=mysql_host,
            port=mysql_port,
            user=profile["user"],
            password=_mysql_password(profile),
            database=profile["database"],
            connect_timeout=_int_from_profile(
                profile, "connect_timeout", _DEFAULT_CONNECT_TIMEOUT
            ),
            read_timeout=read_mysql3,
        )
        mysql3_charset = str(profile.get("mysql3_charset") or "euc-kr").strip()
        merged: list[dict[str, Any]] = []
        offset = 0
        batch = 0
        while offset < detail_cap:
            batch += 1
            take = min(chunk, detail_cap - offset)
            yield {
                "type": "progress",
                "phase": "detail",
                "batch": batch,
                "detailOffset": offset,
                "detailLimit": take,
                "detailCap": detail_cap,
                "readTimeoutSec": read_mysql3,
                "message": (
                    f"\ucffc\ub9ac \uc9c4\ud589 \uc911\u2026 S1_Ssub detail \uadf8\ub8f9 "
                    f"{offset}~{offset + take} (\ubc30\uce58 {batch}, read_timeout={read_mysql3}s, mysql3)"
                ),
            }
            sql_detail = build_sobo67_detail_mysql3_sql(
                grid=gk,  # type: ignore[arg-type]
                d_select_prefix=d_sel,
                date_from=date_from,
                date_to=date_to,
                hcode=hcode,
                book_mode=book_mode,
                scode_filter=scode_filter,
                bcode_from=bcode_from,
                bcode_to=bcode_to,
                parent_bcode=parent_gcode,
                t00=t00,
                limit_rows=take,
                detail_offset=offset,
            )
            raw_d = query_mysql3(conn3, sql_detail, charset=mysql3_charset)
            detail = [_sobo67_normalize_row(x) for x in raw_d]
            if not detail:
                break
            _sobo67_fill_missing_gnames_mysql3(
                conn3, hcode, detail, charset=mysql3_charset
            )
            part = aggregate_detail_rows(detail, year_grain=year_grain)
            merged = merge_aggregate_grids(merged, part, year_grain=year_grain)
            offset += len(detail)
            if len(detail) < take:
                break
        if not merged:
            yield {
                "type": "result",
                "rows": [],
                "footerTotals": {},
                "count": 0,
                "detailRowsFetched": offset,
            }
            return
        yield {
            "type": "progress",
            "phase": "sg_csum",
            "message": (
                "\ucffc\ub9ac \uc9c4\ud589 \uc911\u2026 Sg_Csum(Gpsum) \uc870\ud68c "
                f"(read_timeout={read_mysql3}s, mysql3)"
            ),
            "readTimeoutSec": read_mysql3,
        }
        raw_sg = query_mysql3(conn3, sql_sg, charset=mysql3_charset)
        sg = [_sobo67_normalize_row(x) for x in raw_sg]
        merge_sg_csum_gpsum(merged, sg, year_grain=year_grain)
        ft = footer_totals(merged)
        yield {
            "type": "result",
            "rows": merged,
            "footerTotals": ft,
            "count": len(merged),
            "detailRowsFetched": offset,
        }
    except ValueError as e:
        raise HTTPException(
            status_code=500, detail=_error_detail("config", str(e))
        ) from e
    except SSHTunnelError as e:
        raise HTTPException(
            status_code=502, detail=_error_detail("ssh", str(e))
        ) from e
    finally:
        if conn3 is not None:
            close_mysql3(conn3)


def _sobo67_proto_search_events(
    profile: dict[str, Any],
    server_id: str,
    *,
    grid: str,
    date_from: str,
    date_to: str,
    hcode: str,
    book_mode: str,
    scode_filter: bool,
    limit_rows: int,
    bcode_from: str = "",
    bcode_to: str = "",
    parent_gcode: str = "",
    t00: int = 0,
    detail_chunk_size: int = _SOBO67_DETAIL_CHUNK_DEFAULT,
    read_timeout_sec: int | None = None,
) -> Iterator[dict[str, Any]]:
    """
    Yields progress dicts then one result dict (type=result).
    S1_Ssub detail is read in LIMIT/OFFSET chunks of detail_chunk_size rows (grouped).
    """
    gk: str = "grid2" if grid.strip().lower() in ("2", "grid2", "month") else "grid1"
    year_grain = gk == "grid1"
    d_sel = _d_select_sql_prefix(profile)
    detail_cap = max(100, min(_SOBO67_DETAIL_CAP, max(limit_rows, 1) * 100))
    chunk = max(1, min(int(detail_chunk_size), 500))
    rt_ov = _sobo67_clamp_read_timeout_for_search(read_timeout_sec)

    if _is_mysql3_profile(profile):
        yield from _sobo67_proto_search_events_mysql3(
            profile,
            gk=gk,
            year_grain=year_grain,
            d_sel=d_sel,
            date_from=date_from,
            date_to=date_to,
            hcode=hcode,
            book_mode=book_mode,
            scode_filter=scode_filter,
            bcode_from=bcode_from,
            bcode_to=bcode_to,
            parent_gcode=parent_gcode,
            t00=t00,
            detail_cap=detail_cap,
            chunk=chunk,
            read_timeout_override=rt_ov,
        )
        return

    sql_sg, params_sg = build_sobo67_sg_csum_pymysql(
        d_select_prefix=d_sel,
        date_from=date_from,
        date_to=date_to,
        hcode=hcode,
        book_mode=book_mode,
        bcode_from=bcode_from,
        bcode_to=bcode_to,
        parent_bcode=parent_gcode,
        t00=t00,
        limit_rows=detail_cap,
    )
    conn: Any = None
    read_applied = (
        rt_ov
        if rt_ov is not None
        else _int_from_profile(profile, "read_timeout", _DEFAULT_READ_TIMEOUT)
    )
    for attempt in range(2):
        try:
            conn = _connect(profile, read_timeout_override=rt_ov)
            merged: list[dict[str, Any]] = []
            offset = 0
            batch = 0
            while offset < detail_cap:
                batch += 1
                take = min(chunk, detail_cap - offset)
                yield {
                    "type": "progress",
                    "phase": "detail",
                    "batch": batch,
                    "detailOffset": offset,
                    "detailLimit": take,
                    "detailCap": detail_cap,
                    "readTimeoutSec": read_applied,
                    "message": (
                        f"\ucffc\ub9ac \uc9c4\ud589 \uc911\u2026 S1_Ssub detail \uadf8\ub8f9 "
                        f"{offset}~{offset + take} (\ubc30\uce58 {batch}, read_timeout={read_applied}s)"
                    ),
                }
                sql_d, params_d = build_sobo67_detail_pymysql(
                    grid=gk,  # type: ignore[arg-type]
                    d_select_prefix=d_sel,
                    date_from=date_from,
                    date_to=date_to,
                    hcode=hcode,
                    book_mode=book_mode,
                    scode_filter=scode_filter,
                    bcode_from=bcode_from,
                    bcode_to=bcode_to,
                    parent_bcode=parent_gcode,
                    t00=t00,
                    limit_rows=take,
                    detail_offset=offset,
                )
                with conn.cursor() as cur:
                    cur.execute(sql_d, params_d)
                    detail = [_sobo67_normalize_row(x) for x in cur.fetchall()]
                _sobo67_fill_missing_gnames_pymysql(conn, hcode, detail)
                if not detail:
                    break
                part = aggregate_detail_rows(detail, year_grain=year_grain)
                merged = merge_aggregate_grids(merged, part, year_grain=year_grain)
                offset += len(detail)
                if len(detail) < take:
                    break
            if not merged:
                yield {
                    "type": "result",
                    "rows": [],
                    "footerTotals": {},
                    "count": 0,
                    "detailRowsFetched": offset,
                }
                return
            yield {
                "type": "progress",
                "phase": "sg_csum",
                "message": (
                    "\ucffc\ub9ac \uc9c4\ud589 \uc911\u2026 Sg_Csum(Gpsum) \uc870\ud68c "
                    f"(read_timeout={read_applied}s)"
                ),
                "readTimeoutSec": read_applied,
            }
            with conn.cursor() as cur:
                cur.execute(sql_sg, params_sg)
                sg = [_sobo67_normalize_row(x) for x in cur.fetchall()]
            merge_sg_csum_gpsum(merged, sg, year_grain=year_grain)
            ft = footer_totals(merged)
            yield {
                "type": "result",
                "rows": merged,
                "footerTotals": ft,
                "count": len(merged),
                "detailRowsFetched": offset,
            }
            return
        except pymysql.OperationalError as e:
            try:
                if conn is not None:
                    conn.close()
            except Exception:
                pass
            conn = None
            if (
                attempt == 0
                and e.args
                and e.args[0] == 2013
                and tunnel_enabled(profile)
            ):
                invalidate_server_tunnel(server_id)
                continue
            raise HTTPException(
                status_code=502,
                detail=_error_detail("mysql_query", f"Query failed: {e}"),
            ) from e
        except pymysql.Error as e:
            try:
                if conn is not None:
                    conn.close()
            except Exception:
                pass
            conn = None
            raise HTTPException(
                status_code=502,
                detail=_error_detail("mysql_query", f"Query failed: {e}"),
            ) from e
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass
                conn = None
    raise HTTPException(
        status_code=502,
        detail=_error_detail(
            "mysql_query",
            "Query failed: SSH tunnel retry exhausted (2013)",
        ),
    )


def _sobo67_proto_search_impl(
    profile: dict[str, Any],
    server_id: str,
    *,
    grid: str,
    date_from: str,
    date_to: str,
    hcode: str,
    book_mode: str,
    scode_filter: bool,
    limit_rows: int,
    bcode_from: str = "",
    bcode_to: str = "",
    parent_gcode: str = "",
    t00: int = 0,
    detail_chunk_size: int = _SOBO67_DETAIL_CHUNK_DEFAULT,
    read_timeout_sec: int | None = None,
) -> tuple[list[dict[str, Any]], dict[str, float]]:
    """Subu67-aligned pipeline (non-streaming consumer of _sobo67_proto_search_events)."""
    rows: list[dict[str, Any]] = []
    ft: dict[str, float] = {}
    for ev in _sobo67_proto_search_events(
        profile,
        server_id,
        grid=grid,
        date_from=date_from,
        date_to=date_to,
        hcode=hcode,
        book_mode=book_mode,
        scode_filter=scode_filter,
        limit_rows=limit_rows,
        bcode_from=bcode_from,
        bcode_to=bcode_to,
        parent_gcode=parent_gcode,
        t00=t00,
        detail_chunk_size=detail_chunk_size,
        read_timeout_sec=read_timeout_sec,
    ):
        if ev.get("type") == "result":
            rows = ev.get("rows") or []
            ft = ev.get("footerTotals") or {}
    return rows, ft


@app.get("/api/sobo67/hcode-check")
def sobo67_hcode_check(
    server_id: str = Query(..., alias="serverId"),
    hcode: str = Query(..., description="Hcode to validate (G4_Book sample row)"),
) -> dict[str, Any]:
    """Lightweight check: row exists for Hcode (Seek_Ggeo-style gate for Subu67)."""
    profile = _profile_by_id(server_id)
    hc = (hcode or "").strip()
    if not hc:
        return {"ok": False, "serverId": server_id, "hcode": hc, "reason": "empty"}

    if _is_mysql3_profile(profile):
        esc = hc.replace("\\", "\\\\").replace("'", "''")
        sql = f"SELECT Gcode FROM G4_Book WHERE Hcode = '{esc}' LIMIT 1"
        conn3: dict[str, Any] | None = None
        try:
            mysql_host, mysql_port = mysql_connect_host_port(profile)
            conn3 = connect_mysql3(
                host=mysql_host,
                port=mysql_port,
                user=profile["user"],
                password=_mysql_password(profile),
                database=profile["database"],
                connect_timeout=_int_from_profile(
                    profile, "connect_timeout", _DEFAULT_CONNECT_TIMEOUT
                ),
                read_timeout=_int_from_profile(
                    profile, "read_timeout", _DEFAULT_READ_TIMEOUT
                ),
            )
            mysql3_charset = str(profile.get("mysql3_charset") or "euc-kr").strip()
            rows = query_mysql3(conn3, sql, charset=mysql3_charset)
        finally:
            if conn3 is not None:
                close_mysql3(conn3)
        return {
            "ok": bool(rows),
            "serverId": server_id,
            "hcode": hc,
        }

    conn: Any = None
    try:
        conn = _connect(profile)
        with conn.cursor() as cur:
            cur.execute("SELECT Gcode FROM G4_Book WHERE Hcode = %s LIMIT 1", (hc,))
            row = cur.fetchone()
        return {"ok": row is not None, "serverId": server_id, "hcode": hc}
    except pymysql.Error as e:
        raise HTTPException(
            status_code=502,
            detail=_error_detail("mysql_query", f"hcode check failed: {e}"),
        ) from e
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


@app.get("/api/sobo67/search")
def sobo67_search(
    server_id: str = Query(..., alias="serverId"),
    grid: str = Query(
        "1",
        description="1=year grain (DBGrid101), 2=month grain (DBGrid201)",
    ),
    date_from: str = Query(
        "",
        alias="dateFrom",
        description="Start yyyy.mm; empty defaults to current month",
    ),
    date_to: str = Query(
        "",
        alias="dateTo",
        description="End yyyy.mm; empty defaults to current month",
    ),
    hcode: str = Query("", description="Hcode; recommended for G4_Book Gname join"),
    book_mode: str = Query(
        "book",
        alias="bookMode",
        description="book|warehouse -> Ocode %%B%%, hq -> %%A%%",
    ),
    scode_filter: bool = Query(
        False,
        alias="scodeFilter",
        description="CheckBox2-style Scode filter when true",
    ),
    limit: int = Query(500, ge=1, le=5000, description="Cap for merged grid rows"),
    bcode_from: str = Query("", alias="bcodeFrom", description="Optional Bcode lower (S1_Ssub)"),
    bcode_to: str = Query("", alias="bcodeTo", description="Optional Bcode upper (S1_Ssub)"),
    parent_gcode: str = Query(
        "",
        alias="parentGcode",
        description="Selected year-grid Bcode for month grid (grid=2)",
    ),
    t00: int = Query(
        0,
        ge=0,
        le=1,
        description="Subu67 T00: 1=all books month pass; 0=filter by parentGcode",
    ),
    stream: bool = Query(
        False,
        description="If true, response is application/x-ndjson (progress lines + final result)",
    ),
    detail_chunk: int = Query(
        _SOBO67_DETAIL_CHUNK_DEFAULT,
        ge=1,
        le=500,
        alias="detailChunk",
        description="S1_Ssub grouped detail rows per DB round-trip (default 100)",
    ),
    read_timeout_sec: int | None = Query(
        None,
        ge=10,
        le=900,
        alias="readTimeoutSec",
        description="Override read_timeout (s) for this search; caps at SEAK80_SOBO67_READ_TIMEOUT_MAX",
    ),
) -> Any:
    """Subu67-aligned S1_Ssub detail aggregate + Sg_Csum gpsum (see docs/phase1-structure/sobo67-porting-notes.md)."""
    profile = _profile_by_id(server_id)
    hc = (hcode or "").strip()
    today = date.today()
    default_ym = f"{today.year:04d}.{today.month:02d}"
    df = (date_from or "").strip() or default_ym
    dt = (date_to or "").strip() or default_ym

    if stream:

        def _ndjson_bytes() -> Iterator[bytes]:
            try:
                for ev in _sobo67_proto_search_events(
                    profile,
                    server_id,
                    grid=grid,
                    date_from=df,
                    date_to=dt,
                    hcode=hc,
                    book_mode=(book_mode or "").strip(),
                    scode_filter=scode_filter,
                    limit_rows=limit,
                    bcode_from=(bcode_from or "").strip(),
                    bcode_to=(bcode_to or "").strip(),
                    parent_gcode=(parent_gcode or "").strip(),
                    t00=int(t00),
                    detail_chunk_size=detail_chunk,
                    read_timeout_sec=read_timeout_sec,
                ):
                    if ev.get("type") == "result":
                        ev = {
                            **ev,
                            "serverId": server_id,
                            "grid": grid,
                            "dateFrom": df,
                            "dateTo": dt,
                            "hcode": hc,
                            "bookMode": (book_mode or "").strip(),
                            "bcodeFrom": (bcode_from or "").strip(),
                            "bcodeTo": (bcode_to or "").strip(),
                            "parentGcode": (parent_gcode or "").strip(),
                            "t00": int(t00),
                            "subu67": True,
                        }
                    line = json.dumps(ev, ensure_ascii=False, default=str) + "\n"
                    yield line.encode("utf-8")
            except HTTPException as he:
                err = {
                    "type": "error",
                    "status": he.status_code,
                    "detail": he.detail,
                }
                yield (json.dumps(err, ensure_ascii=False, default=str) + "\n").encode(
                    "utf-8"
                )
            except Exception as ex:
                err = {"type": "error", "status": 500, "detail": str(ex)}
                yield (json.dumps(err, ensure_ascii=False, default=str) + "\n").encode(
                    "utf-8"
                )

        return StreamingResponse(
            _ndjson_bytes(),
            media_type="application/x-ndjson; charset=utf-8",
        )

    rows, ft = _sobo67_proto_search_impl(
        profile,
        server_id,
        grid=grid,
        date_from=df,
        date_to=dt,
        hcode=hc,
        book_mode=(book_mode or "").strip(),
        scode_filter=scode_filter,
        limit_rows=limit,
        bcode_from=(bcode_from or "").strip(),
        bcode_to=(bcode_to or "").strip(),
        parent_gcode=(parent_gcode or "").strip(),
        t00=int(t00),
        detail_chunk_size=detail_chunk,
        read_timeout_sec=read_timeout_sec,
    )
    return {
        "rows": rows,
        "count": len(rows),
        "footerTotals": ft,
        "serverId": server_id,
        "grid": grid,
        "prototype": False,
        "subu67": True,
        "dateFrom": df,
        "dateTo": dt,
        "hcode": hc,
        "bookMode": (book_mode or "").strip(),
        "bcodeFrom": (bcode_from or "").strip(),
        "bcodeTo": (bcode_to or "").strip(),
        "parentGcode": (parent_gcode or "").strip(),
        "t00": int(t00),
        "detailChunk": detail_chunk,
        "readTimeoutSec": read_timeout_sec,
    }


@app.get("/sobo67", include_in_schema=False)
def redirect_sobo67_to_html() -> RedirectResponse:
    """StaticFiles does not map extensionless paths; browsers often omit .html."""
    return RedirectResponse(url="/sobo67.html", status_code=307)


@app.get("/seek20", include_in_schema=False)
def redirect_seek20_to_html() -> RedirectResponse:
    return RedirectResponse(url="/seek20.html", status_code=307)


@app.get("/seek30", include_in_schema=False)
def redirect_seek30_to_html() -> RedirectResponse:
    return RedirectResponse(url="/seek30.html", status_code=307)


@app.get("/seak04", include_in_schema=False)
def redirect_seak04_to_html() -> RedirectResponse:
    return RedirectResponse(url="/seak04.html", status_code=307)


@app.get("/sobo12", include_in_schema=False)
def redirect_sobo12_to_html() -> RedirectResponse:
    return RedirectResponse(url="/sobo12.html", status_code=307)


@app.get("/sobo13", include_in_schema=False)
def redirect_sobo13_to_html() -> RedirectResponse:
    return RedirectResponse(url="/sobo13.html", status_code=307)


@app.get("/masters", include_in_schema=False)
def redirect_masters_hub() -> RedirectResponse:
    return RedirectResponse(url="/masters-hub.html", status_code=307)


@app.get("/phase2", include_in_schema=False)
def redirect_phase2_hub_alias() -> RedirectResponse:
    return RedirectResponse(url="/masters-hub.html", status_code=307)


@app.get("/masters-hub", include_in_schema=False)
def redirect_masters_hub_extensionless() -> RedirectResponse:
    return RedirectResponse(url="/masters-hub.html", status_code=307)


@app.get("/masters-read", include_in_schema=False)
def redirect_masters_read_extensionless(request: Request) -> RedirectResponse:
    q = request.url.query
    loc = "/masters-read.html" + ("?" + q if q else "")
    return RedirectResponse(url=loc, status_code=307)


@app.get("/stub-sobo10", include_in_schema=False)
def redirect_stub_sobo10_extensionless() -> RedirectResponse:
    return RedirectResponse(url="/stub-sobo10.html", status_code=307)


@app.get("/stub-sobo19", include_in_schema=False)
def redirect_stub_sobo19_extensionless() -> RedirectResponse:
    return RedirectResponse(url="/stub-sobo19.html", status_code=307)


if FRONTEND_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
