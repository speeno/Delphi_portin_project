"""
Per-server SSH port forwarding for MySQL (local PyMySQL -> ssh -> remote 127.0.0.1:3306).

Used when servers.yaml sets ssh_tunnel.enabled for old hosts that only allow local MySQL
or block direct 3306 from the WAN.
"""

from __future__ import annotations

import atexit
import os
import shutil
import socket
import subprocess
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, Callable

import paramiko

_lock = threading.RLock()
_servers: dict[str, Any] = {}
_legacy_forwarder_cls: type | None = None


class SSHTunnelError(Exception):
    """SSH port-forward could not be established (before PyMySQL connect)."""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def _apply_legacy_paramiko() -> None:
    """
    Align Paramiko with OpenSSH for old gateways, e.g.:
      -o KexAlgorithms=+diffie-hellman-group1-sha1
      -o HostKeyAlgorithms=+ssh-rsa
      -o PubkeyAcceptedAlgorithms=+ssh-rsa
    Plus Transport(..., strict_kex=False) via LegacySSHTunnelForwarder.

    Idempotent so repeated tunnel opens do not stack patches.
    """
    import paramiko.transport as tr

    keys = list(tr.Transport._preferred_keys)
    if keys and keys[0] != "ssh-rsa" and "ssh-rsa" in keys:
        tr.Transport._preferred_keys = tuple(
            ["ssh-rsa"] + [k for k in keys if k != "ssh-rsa"]
        )

    pubkeys = list(tr.Transport._preferred_pubkeys)
    if pubkeys and pubkeys[0] != "ssh-rsa" and "ssh-rsa" in pubkeys:
        tr.Transport._preferred_pubkeys = tuple(
            ["ssh-rsa"] + [k for k in pubkeys if k != "ssh-rsa"]
        )

    kex = list(tr.Transport._preferred_kex)
    if not kex or kex[0] != "diffie-hellman-group1-sha1":
        for alg in (
            "diffie-hellman-group1-sha1",
            "diffie-hellman-group-exchange-sha1",
        ):
            if alg in kex:
                kex.remove(alg)
            kex.insert(0, alg)
        tr.Transport._preferred_kex = tuple(kex)


def _legacy_sshtunnel_forwarder_class() -> type:
    """SSHTunnelForwarder with Transport(..., strict_kex=False) for pre-strict-kex servers."""
    global _legacy_forwarder_cls
    if _legacy_forwarder_cls is not None:
        return _legacy_forwarder_cls

    from sshtunnel import SSH_TIMEOUT, SSHTunnelForwarder

    class LegacySSHTunnelForwarder(SSHTunnelForwarder):
        def _get_transport(self):
            if self.ssh_proxy:
                if isinstance(self.ssh_proxy, paramiko.proxy.ProxyCommand):
                    proxy_repr = repr(self.ssh_proxy.cmd[1])
                else:
                    proxy_repr = repr(self.ssh_proxy)
                self.logger.debug("Connecting via proxy: %s", proxy_repr)
                _socket = self.ssh_proxy
            else:
                _socket = (self.ssh_host, self.ssh_port)
            if isinstance(_socket, socket.socket):
                _socket.settimeout(SSH_TIMEOUT)
                _socket.connect((self.ssh_host, self.ssh_port))
            transport = paramiko.Transport(_socket, strict_kex=False)
            sock = transport.sock
            if isinstance(sock, socket.socket):
                sock.settimeout(SSH_TIMEOUT)
            transport.set_keepalive(self.set_keepalive)
            transport.use_compression(compress=self.compression)
            transport.daemon = self.daemon_transport
            if isinstance(sock, socket.socket):
                sock_timeout = sock.gettimeout()
                sock_info = repr((sock.family, sock.type, sock.proto))
                self.logger.debug(
                    "Transport socket info: %s, timeout=%s", sock_info, sock_timeout
                )
            return transport

    _legacy_forwarder_cls = LegacySSHTunnelForwarder
    return LegacySSHTunnelForwarder


def _expand_key(path: str | None) -> str | None:
    if path is None or not str(path).strip():
        return None
    p = Path(str(path).strip()).expanduser()
    return str(p) if p.is_file() else None


class _SystemSshPortForward:
    """
    OpenSSH CLI port forward (same negotiation as interactive `ssh -o ...`).
    Exposes local_bind_port / is_active / stop like sshtunnel.SSHTunnelForwarder.
    """

    def __init__(
        self,
        *,
        ssh_bin: str,
        ssh_host: str,
        ssh_port: int,
        ssh_user: str,
        ssh_password: str | None,
        ssh_pkey: str | None,
        local_port: int,
        remote_host: str,
        remote_port: int,
        strict_host_key: str,
    ) -> None:
        self.local_bind_port = int(local_port)
        self._ssh_bin = ssh_bin
        self._cmd: list[str] = []
        self._proc: subprocess.Popen | None = None
        self._cleanup_pwfile: Callable[[], None] | None = None
        self._build_cmd(
            ssh_host=ssh_host,
            ssh_port=ssh_port,
            ssh_user=ssh_user,
            ssh_password=ssh_password,
            ssh_pkey=ssh_pkey,
            local_port=local_port,
            remote_host=remote_host,
            remote_port=remote_port,
            strict_host_key=strict_host_key,
        )

    def _build_cmd(
        self,
        *,
        ssh_host: str,
        ssh_port: int,
        ssh_user: str,
        ssh_password: str | None,
        ssh_pkey: str | None,
        local_port: int,
        remote_host: str,
        remote_port: int,
        strict_host_key: str,
    ) -> None:
        cmd: list[str] = [self._ssh_bin, "-N", "-n"]
        if not ssh_password:
            cmd += ["-o", "BatchMode=yes"]
        if ssh_pkey:
            cmd += ["-i", ssh_pkey, "-o", "IdentitiesOnly=yes"]
        cmd += [
            "-o",
            "KexAlgorithms=+diffie-hellman-group1-sha1",
            "-o",
            "HostKeyAlgorithms=+ssh-rsa",
            "-o",
            "PubkeyAcceptedAlgorithms=+ssh-rsa",
            "-o",
            "ServerAliveInterval=30",
            "-o",
            "ServerAliveCountMax=6",
            "-o",
            f"StrictHostKeyChecking={strict_host_key}",
        ]
        if ssh_password:
            cmd += ["-o", "NumberOfPasswordPrompts=1"]
        cmd += [
            "-L",
            f"127.0.0.1:{local_port}:{remote_host}:{remote_port}",
            "-p",
            str(ssh_port),
            f"{ssh_user}@{ssh_host}",
        ]
        if ssh_password:
            # SSH_ASKPASS helper: a tiny script that echoes the password.
            # Works without sshpass; SSH_ASKPASS_REQUIRE=force (OpenSSH 8.4+)
            # or DISPLAY="" + -n (no tty) for older versions.
            fd, askpass = tempfile.mkstemp(prefix="seak80_askpass_", suffix=".sh")
            # The password is passed via a separate file read by the helper,
            # avoiding shell quoting issues with special characters.
            fd2, pwfile = tempfile.mkstemp(prefix="seak80_pw_", suffix=".txt")
            try:
                os.write(fd2, ssh_password.encode("utf-8"))
            finally:
                os.close(fd2)
            os.chmod(pwfile, 0o600)
            try:
                os.write(fd, f"#!/bin/sh\ncat '{pwfile}'\n".encode("utf-8"))
            finally:
                os.close(fd)
            os.chmod(askpass, 0o700)

            def _rm() -> None:
                for f in (askpass, pwfile):
                    try:
                        os.unlink(f)
                    except OSError:
                        pass

            self._cleanup_pwfile = _rm
            self._env = {
                **os.environ,
                "SSH_ASKPASS": askpass,
                "SSH_ASKPASS_REQUIRE": "force",
                "DISPLAY": "",
            }
            self._cmd = cmd
        else:
            self._env = None
            self._cmd = cmd

    def start(self) -> None:
        self._proc = subprocess.Popen(
            self._cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            env=self._env,
        )
        stderr_buf = bytearray()
        stderr_lock = threading.Lock()

        def _drain_stderr() -> None:
            if not self._proc or not self._proc.stderr:
                return
            try:
                while True:
                    chunk = self._proc.stderr.read(4096)
                    if not chunk:
                        break
                    with stderr_lock:
                        stderr_buf.extend(chunk)
                        if len(stderr_buf) > 200_000:
                            del stderr_buf[: len(stderr_buf) - 100_000]
            except Exception:
                pass

        drain_t = threading.Thread(target=_drain_stderr, daemon=True)
        drain_t.start()

        deadline = time.monotonic() + 45.0
        err_hint = ""
        while time.monotonic() < deadline:
            if self._proc.poll() is not None:
                drain_t.join(timeout=2.0)
                with stderr_lock:
                    err_hint = bytes(stderr_buf).decode("utf-8", errors="replace")[:4000]
                if self._cleanup_pwfile:
                    self._cleanup_pwfile()
                    self._cleanup_pwfile = None
                raise SSHTunnelError(
                    f"system ssh exited early (code {self._proc.returncode}): {err_hint}"
                )
            try:
                probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                probe.settimeout(0.25)
                probe.connect(("127.0.0.1", self.local_bind_port))
                probe.close()
                break
            except OSError:
                time.sleep(0.15)
        else:
            self.stop()
            drain_t.join(timeout=2.0)
            with stderr_lock:
                err_hint = bytes(stderr_buf).decode("utf-8", errors="replace")[:4000]
            if self._cleanup_pwfile:
                self._cleanup_pwfile()
                self._cleanup_pwfile = None
            raise SSHTunnelError(
                f"system ssh did not open 127.0.0.1:{self.local_bind_port} within 45s. {err_hint}"
            )
        if self._cleanup_pwfile:
            self._cleanup_pwfile()
            self._cleanup_pwfile = None

    @property
    def is_active(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def stop(self) -> None:
        if self._cleanup_pwfile:
            try:
                self._cleanup_pwfile()
            except Exception:
                pass
            self._cleanup_pwfile = None
        if self._proc is None:
            return
        try:
            self._proc.terminate()
            try:
                self._proc.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                self._proc.kill()
        except Exception:
            pass
        self._proc = None


def _start_system_ssh_tunnel(
    tun: dict[str, Any],
    *,
    ssh_host: str,
    ssh_port: int,
    ssh_user: str,
    ssh_password: str | None,
    ssh_pkey: str | None,
    r_host: str,
    r_port: int,
) -> _SystemSshPortForward:
    lp = tun.get("system_ssh_local_port")
    if lp is None:
        raise ValueError(
            "use_system_ssh requires ssh_tunnel.system_ssh_local_port "
            "(unique free TCP port per server, e.g. 41554)"
        )
    local_port = int(lp)
    ssh_bin = shutil.which("ssh") or ""
    if not ssh_bin:
        raise SSHTunnelError("use_system_ssh requires OpenSSH client `ssh` on PATH")
    # accept-new needs OpenSSH 8+; older macOS/OpenSSH fails the whole ssh command.
    raw_strict = tun.get("strict_host_key_checking")
    strict = (
        str(raw_strict).strip()
        if raw_strict is not None and str(raw_strict).strip() != ""
        else "no"
    )
    t = _SystemSshPortForward(
        ssh_bin=ssh_bin,
        ssh_host=ssh_host,
        ssh_port=ssh_port,
        ssh_user=ssh_user,
        ssh_password=ssh_password,
        ssh_pkey=ssh_pkey,
        local_port=local_port,
        remote_host=r_host,
        remote_port=r_port,
        strict_host_key=strict,
    )
    t.start()
    return t


def tunnel_enabled(profile: dict[str, Any]) -> bool:
    tun = profile.get("ssh_tunnel")
    if not isinstance(tun, dict):
        return False
    return bool(tun.get("enabled", True))


def invalidate_server_tunnel(server_id: str) -> None:
    """Drop a cached tunnel so the next connect opens a fresh SSH session (e.g. after MySQL 2013)."""
    sid = (server_id or "").strip()
    if not sid:
        return
    with _lock:
        fwd = _servers.pop(sid, None)
        if fwd is None:
            return
        try:
            fwd.stop()
        except Exception:
            pass


def mysql_connect_host_port(profile: dict[str, Any]) -> tuple[str, int]:
    """Return (host, port) for PyMySQL: direct from profile, or 127.0.0.1 + local port via SSH."""
    if not tunnel_enabled(profile):
        return str(profile["host"]), int(profile.get("port", 3306))

    tun = profile["ssh_tunnel"]
    assert isinstance(tun, dict)

    sid = (profile.get("id") or "").strip()
    if not sid:
        raise ValueError("server id is required when ssh_tunnel is enabled")

    ssh_host = str(tun.get("ssh_host") or profile.get("host") or "").strip()
    if not ssh_host:
        raise ValueError("ssh_tunnel needs ssh_host or profile host")
    ssh_port = int(tun.get("ssh_port", 22))
    ssh_user = str(tun.get("ssh_user", "")).strip()
    if not ssh_user:
        raise ValueError("ssh_tunnel.ssh_user is required")

    use_system_ssh = bool(tun.get("use_system_ssh") or tun.get("system_ssh"))

    spw = tun.get("ssh_password")
    ssh_password = None if spw is None else str(spw)
    if ssh_password == "":
        ssh_password = None
    ssh_pkey = _expand_key(tun.get("ssh_private_key")) or _expand_key(
        os.environ.get("SEAK80_SSH_PRIVATE_KEY")
    )

    if ssh_password is None and not ssh_pkey:
        raise ValueError("ssh_tunnel needs ssh_password or ssh_private_key")

    r_host = str(tun.get("remote_mysql_host") or "127.0.0.1").strip()
    r_port = int(tun.get("remote_mysql_port", profile.get("port", 3306)))

    legacy = bool(tun.get("legacy_algorithms") or tun.get("ssh_legacy"))
    if not use_system_ssh and legacy:
        _apply_legacy_paramiko()

    with _lock:
        existing = _servers.get(sid)
        if existing is not None and getattr(existing, "is_active", False):
            return "127.0.0.1", int(existing.local_bind_port)

        if existing is not None:
            try:
                existing.stop()
            except Exception:
                pass
            _servers.pop(sid, None)

        if use_system_ssh:
            try:
                fwd = _start_system_ssh_tunnel(
                    tun,
                    ssh_host=ssh_host,
                    ssh_port=ssh_port,
                    ssh_user=ssh_user,
                    ssh_password=ssh_password,
                    ssh_pkey=ssh_pkey,
                    r_host=r_host,
                    r_port=r_port,
                )
            except SSHTunnelError:
                raise
            except ValueError:
                raise
            except Exception as e:
                raise SSHTunnelError(
                    f"system ssh tunnel to {ssh_host}:{ssh_port} failed: {e}"
                ) from e
            _servers[sid] = fwd
            return "127.0.0.1", int(fwd.local_bind_port)

        try:
            from sshtunnel import SSHTunnelForwarder
        except ImportError as e:
            raise SSHTunnelError(
                "ssh_tunnel requires sshtunnel and paramiko; pip install -r requirements.txt"
            ) from e

        # strict_kex=False matches old sshd that does not implement RFC-style strict KEX.
        Fwd = (
            _legacy_sshtunnel_forwarder_class() if legacy else SSHTunnelForwarder
        )
        fwd = Fwd(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_password,
            ssh_pkey=ssh_pkey,
            remote_bind_address=(r_host, r_port),
            local_bind_address=("127.0.0.1", 0),
            # Steady keepalive helps legacy SSH + long MySQL handshakes (reduces spurious 2013).
            set_keepalive=30.0,
            compression=False,
        )
        try:
            fwd.start()
        except Exception as e:
            raise SSHTunnelError(f"SSH tunnel to {ssh_host}:{ssh_port} failed: {e}") from e
        _servers[sid] = fwd
        return "127.0.0.1", int(fwd.local_bind_port)


def shutdown_all_ssh_tunnels() -> None:
    with _lock:
        for _, fwd in list(_servers.items()):
            try:
                fwd.stop()
            except Exception:
                pass
        _servers.clear()


atexit.register(shutdown_all_ssh_tunnels)
