"""PyMySQL tweaks for legacy MySQL/MariaDB (auth handshake quirks)."""

from __future__ import annotations

import socket
import struct
from contextlib import contextmanager
from typing import Any, Generator


# ---------------------------------------------------------------------------
# MySQL 3.x / 4.0 old-protocol raw connector
# ---------------------------------------------------------------------------

def _hash_password_323(password: bytes) -> tuple[int, int]:
    nr = 1345345333
    add = 7
    nr2 = 0x12345671
    for c in password:
        if c == 32 or c == 9:
            continue
        nr ^= (((nr & 63) + add) * c) + ((nr << 8) & 0xFFFFFFFF)
        nr &= 0xFFFFFFFF
        nr2 = (nr2 + (((nr2 << 8) & 0xFFFFFFFF) ^ nr)) & 0xFFFFFFFF
        add = (add + c) & 0xFFFFFFFF
    return nr & 0x7FFFFFFF, nr2 & 0x7FFFFFFF


class _RandStruct323:
    def __init__(self, seed1: int, seed2: int) -> None:
        self.max_value = 0x3FFFFFFF
        self.seed1 = seed1 % self.max_value
        self.seed2 = seed2 % self.max_value

    def my_rnd(self) -> float:
        self.seed1 = (self.seed1 * 3 + self.seed2) % self.max_value
        self.seed2 = (self.seed1 + self.seed2 + 33) % self.max_value
        return float(self.seed1) / float(self.max_value)


def _scramble_323(message: bytes, password: bytes) -> bytes:
    if not password:
        return b""
    hp = _hash_password_323(password)
    hm = _hash_password_323(message)
    rnd = _RandStruct323(hp[0] ^ hm[0], hp[1] ^ hm[1])
    out = bytearray(int(rnd.my_rnd() * 31) + 64 for _ in range(len(message)))
    extra = int(rnd.my_rnd() * 31)
    for i in range(len(out)):
        out[i] ^= extra
    return bytes(out)


def _read_packet(sock: socket.socket) -> tuple[int, bytes]:
    hdr = b""
    while len(hdr) < 4:
        chunk = sock.recv(4 - len(hdr))
        if not chunk:
            raise ConnectionError("Connection closed reading header")
        hdr += chunk
    pkt_len = struct.unpack("<I", hdr[:3] + b"\x00")[0]
    seq = hdr[3]
    body = b""
    while len(body) < pkt_len:
        chunk = sock.recv(pkt_len - len(body))
        if not chunk:
            raise ConnectionError("Connection closed reading body")
        body += chunk
    return seq, body


def _write_packet(sock: socket.socket, seq: int, data: bytes) -> None:
    hdr = struct.pack("<I", len(data))[:3] + bytes([seq & 0xFF])
    sock.sendall(hdr + data)


def connect_mysql3(
    *,
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    connect_timeout: int = 30,
    read_timeout: int = 120,
) -> dict[str, Any]:
    """
    Minimal MySQL 3.23 / 4.0 old-protocol connector.
    Returns {'version': str, 'sock': socket} on success.
    Raises OperationalError on failure.
    """
    import pymysql.err as perr

    sock = socket.create_connection((host, port), timeout=connect_timeout)
    sock.settimeout(read_timeout)
    try:
        seq, body = _read_packet(sock)
        proto = body[0]
        nul = body.index(0, 1)
        version = body[1:nul].decode("latin-1")
        off = nul + 1
        off += 4  # thread_id
        scramble = body[off : off + 8]
        off += 9  # scramble(8) + filler(1)
        caps_low = struct.unpack("<H", body[off : off + 2])[0]

        pwd_bytes = password.encode("latin-1") if isinstance(password, str) else password
        auth_resp = _scramble_323(scramble, pwd_bytes)

        user_bytes = user.encode("latin-1") if isinstance(user, str) else user
        db_bytes = database.encode("latin-1") if isinstance(database, str) else database

        # Old-style HandshakeResponse: client_flags(2) + max_packet(3) + user\0 + scramble\0
        # CLIENT_LONG_PASSWORD (0x0001) must be set so the server treats
        # the auth response as a scramble rather than a raw password hash.
        # CLIENT_COMPRESS (0x0020) must be cleared: we don't implement
        # the compressed packet framing that the server would switch to.
        client_flags = (caps_low | 0x0001) & ~0x0020 & 0xFFFF
        has_connect_db = bool(client_flags & 0x0008)  # CLIENT_CONNECT_WITH_DB
        pkt = struct.pack("<H", client_flags)
        pkt += struct.pack("<I", 2**24 - 1)[:3]
        pkt += user_bytes + b"\x00"
        pkt += auth_resp + b"\x00"
        if has_connect_db:
            pkt += db_bytes + b"\x00"

        _write_packet(sock, 1, pkt)

        rseq, rbody = _read_packet(sock)
        if rbody[0] == 0xFF:
            errno = struct.unpack("<H", rbody[1:3])[0]
            msg = rbody[3:].decode("latin-1", errors="replace")
            sock.close()
            raise perr.OperationalError(errno, msg)
        if rbody[0] != 0x00:
            sock.close()
            raise perr.OperationalError(
                2013, f"Unexpected handshake response 0x{rbody[0]:02x}"
            )
        return {"version": version, "sock": sock}
    except perr.OperationalError:
        raise
    except Exception as e:
        try:
            sock.close()
        except Exception:
            pass
        raise perr.OperationalError(2013, f"MySQL 3.x handshake failed: {e}") from e


def query_mysql3(
    conn: dict[str, Any],
    sql: str,
    charset: str = "euc-kr",
) -> list[dict[str, Any]]:
    """Run a SELECT on a MySQL 3.x raw connection and return list[dict]."""
    import pymysql.err as perr

    sock: socket.socket = conn["sock"]
    sql_bytes = sql.encode(charset, errors="replace") if isinstance(sql, str) else sql
    _write_packet(sock, 0, b"\x03" + sql_bytes)  # COM_QUERY

    seq, body = _read_packet(sock)
    if body[0] == 0xFF:
        errno = struct.unpack("<H", body[1:3])[0]
        msg = body[3:].decode(charset, errors="replace")
        raise perr.OperationalError(errno, msg)

    # Result set: first packet = field_count (length-coded)
    field_count = body[0]
    if field_count == 0:
        return []

    # Field descriptions ? MySQL 3.x format:
    #   [table(LCS), name(LCS), col_length(LCB), col_type(LCB), flags_dec(LCB)]
    # Column name is parts[1] (second length-coded string).
    columns: list[str] = []
    for _ in range(field_count):
        _, fbody = _read_packet(sock)
        off = 0
        # table
        tl = fbody[off]; off += 1 + tl
        # name
        nl = fbody[off]; off += 1
        col_name = fbody[off : off + nl].decode("latin-1", errors="replace")
        columns.append(col_name)

    # EOF after fields
    _, eof = _read_packet(sock)

    # Row data
    rows: list[dict[str, Any]] = []
    while True:
        _, rbody = _read_packet(sock)
        if rbody[0] == 0xFE and len(rbody) < 9:
            break
        off = 0
        row: dict[str, Any] = {}
        for col in columns:
            if rbody[off] == 0xFB:
                row[col] = None
                off += 1
            else:
                ln = rbody[off]
                off += 1
                if ln >= 251:
                    if ln == 252:
                        ln = struct.unpack("<H", rbody[off : off + 2])[0]
                        off += 2
                    elif ln == 253:
                        ln = struct.unpack("<I", rbody[off : off + 3] + b"\x00")[0]
                        off += 3
                    elif ln == 254:
                        ln = struct.unpack("<Q", rbody[off : off + 8])[0]
                        off += 8
                val = rbody[off : off + ln].decode(charset, errors="replace")
                off += ln
                row[col] = val
        rows.append(row)
    return rows


def close_mysql3(conn: dict[str, Any]) -> None:
    try:
        sock: socket.socket = conn["sock"]
        _write_packet(sock, 0, b"\x01")  # COM_QUIT
        sock.close()
    except Exception:
        pass


def install_auth_switch_request_fix() -> None:
    """
    Some servers/proxies send AuthSwitchRequest without a null-terminated plugin name.
    PyMySQL's read_string() then returns None and raises 'unknown auth switch request'.
    Default missing/empty plugin to mysql_native_password and ensure PLUGIN_AUTH is set.
    Mirrors pymysql.connections.Connection._request_authentication (keep in sync on pymysql upgrades).
    """
    import struct

    import pymysql.connections as pc
    from pymysql import _auth, err
    from pymysql.charset import charset_by_name
    from pymysql.constants import CLIENT

    if getattr(pc.Connection, "_seak80_auth_switch_request_fix", False):
        return

    _lenenc_int = pc._lenenc_int
    MAX_PACKET_LEN = pc.MAX_PACKET_LEN
    DEBUG = pc.DEBUG

    def _request_authentication(self) -> None:
        if int(self.server_version.split(".", 1)[0]) >= 5:
            self.client_flag |= CLIENT.MULTI_RESULTS

        if self.user is None:
            raise ValueError("Did not specify a username")

        charset_id = charset_by_name(self.charset).id
        if isinstance(self.user, str):
            self.user = self.user.encode(self.encoding)

        data_init = struct.pack(
            "<iIB23s", self.client_flag, MAX_PACKET_LEN, charset_id, b""
        )

        if self.ssl and self.server_capabilities & CLIENT.SSL:
            self.write_packet(data_init)

            self._sock = self.ctx.wrap_socket(self._sock, server_hostname=self.host)
            self._rfile = self._sock.makefile("rb")
            self._secure = True

        data = data_init + self.user + b"\0"

        authresp = b""
        plugin_name = None

        if self._auth_plugin_name == "":
            plugin_name = b""
            authresp = _auth.scramble_native_password(self.password, self.salt)
        elif self._auth_plugin_name == "mysql_native_password":
            plugin_name = b"mysql_native_password"
            authresp = _auth.scramble_native_password(self.password, self.salt)
        elif self._auth_plugin_name == "caching_sha2_password":
            plugin_name = b"caching_sha2_password"
            if self.password:
                if DEBUG:
                    print("caching_sha2: trying fast path")
                authresp = _auth.scramble_caching_sha2(self.password, self.salt)
            else:
                if DEBUG:
                    print("caching_sha2: empty password")
        elif self._auth_plugin_name == "sha256_password":
            plugin_name = b"sha256_password"
            if self.ssl and self.server_capabilities & CLIENT.SSL:
                authresp = self.password + b"\0"
            elif self.password:
                authresp = b"\1"  # request public key
            else:
                authresp = b"\0"  # empty password

        if self.server_capabilities & CLIENT.PLUGIN_AUTH_LENENC_CLIENT_DATA:
            data += _lenenc_int(len(authresp)) + authresp
        elif self.server_capabilities & CLIENT.SECURE_CONNECTION:
            data += struct.pack("B", len(authresp)) + authresp
        else:  # pragma: no cover
            data += authresp + b"\0"

        if self.db and self.server_capabilities & CLIENT.CONNECT_WITH_DB:
            if isinstance(self.db, str):
                self.db = self.db.encode(self.encoding)
            data += self.db + b"\0"

        if self.server_capabilities & CLIENT.PLUGIN_AUTH:
            data += (plugin_name or b"") + b"\0"

        if self.server_capabilities & CLIENT.CONNECT_ATTRS:
            connect_attrs = b""
            for k, v in self._connect_attrs.items():
                k = k.encode("utf-8")
                connect_attrs += _lenenc_int(len(k)) + k
                v = v.encode("utf-8")
                connect_attrs += _lenenc_int(len(v)) + v
            data += _lenenc_int(len(connect_attrs)) + connect_attrs

        self.write_packet(data)
        auth_packet = self._read_packet()

        if auth_packet.is_auth_switch_request():
            if DEBUG:
                print("received auth switch")
            auth_packet.read_uint8()
            sw_plugin = auth_packet.read_string()
            if sw_plugin is None or sw_plugin == b"":
                sw_plugin = b"mysql_native_password"
            if not (self.server_capabilities & CLIENT.PLUGIN_AUTH):
                self.server_capabilities |= CLIENT.PLUGIN_AUTH
            auth_packet = self._process_auth(sw_plugin, auth_packet)
        elif auth_packet.is_extra_auth_data():
            if DEBUG:
                print("received extra data")
            if self._auth_plugin_name == "caching_sha2_password":
                auth_packet = _auth.caching_sha2_password_auth(self, auth_packet)
            elif self._auth_plugin_name == "sha256_password":
                auth_packet = _auth.sha256_password_auth(self, auth_packet)
            else:
                raise err.OperationalError(
                    "Received extra packet for auth method %r", self._auth_plugin_name
                )

        if DEBUG:
            print("Succeed to auth")

    pc.Connection._request_authentication = _request_authentication  # type: ignore[method-assign]
    setattr(pc.Connection, "_seak80_auth_switch_request_fix", True)


def install_handshake_plugin_auth_capability_fix() -> None:
    """
    Some servers omit CLIENT.PLUGIN_AUTH in the initial handshake but still send
    AuthSwitchRequest. PyMySQL then raises 'received unknown auth switch request'.
    OR-ing PLUGIN_AUTH onto parsed server_capabilities allows _process_auth to run.
    """
    import pymysql.connections as pc
    from pymysql.constants import CLIENT

    if getattr(pc.Connection, "_seak80_plugin_auth_handshake_fix", False):
        return
    orig = pc.Connection._get_server_information

    def wrapped(self) -> None:
        orig(self)
        self.server_capabilities |= CLIENT.PLUGIN_AUTH

    pc.Connection._get_server_information = wrapped  # type: ignore[method-assign]
    setattr(pc.Connection, "_seak80_plugin_auth_handshake_fix", True)


@contextmanager
def pymysql_default_auth_plugin(name: str | None) -> Generator[None, None, None]:
    """Force first auth attempt to use a named plugin (e.g. mysql_native_password)."""
    import pymysql.connections as pc

    if not name or not str(name).strip():
        yield
        return
    prev = pc._DEFAULT_AUTH_PLUGIN
    pc._DEFAULT_AUTH_PLUGIN = str(name).strip()
    try:
        yield
    finally:
        pc._DEFAULT_AUTH_PLUGIN = prev
