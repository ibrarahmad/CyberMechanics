#!/usr/bin/env python3
"""Safe process control for Cyber Mechanics shared lab services (loopback only)."""
from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RUN = ROOT / ".run"
HOST = "127.0.0.1"
TRAINING_PORT = 5050
DEMO_PORT = 8080
READY_TIMEOUT = 8.0


def run_dir() -> Path:
    RUN.mkdir(parents=True, exist_ok=True)
    return RUN


def pid_path(name: str) -> Path:
    return run_dir() / f"{name}.pid"


def meta_path(name: str) -> Path:
    return run_dir() / f"{name}.json"


def log_path(name: str) -> Path:
    return run_dir() / f"{name}.log"


def port_open(host: str, port: int) -> bool:
    try:
        with socket.create_connection((host, port), timeout=0.4):
            return True
    except OSError:
        return False


def who_listens(port: int) -> list[int]:
    """Best-effort PIDs listening on TCP port (Linux/macOS lsof). Empty if unavailable."""
    try:
        out = subprocess.check_output(
            ["lsof", f"-tiTCP:{port}", "-sTCP:LISTEN"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    pids = []
    for line in out.splitlines():
        line = line.strip()
        if line.isdigit():
            pids.append(int(line))
    return pids


def alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def read_meta(name: str) -> dict | None:
    path = meta_path(name)
    if not path.is_file():
        return None
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return None


def write_meta(name: str, pid: int, port: int, cmd: list[str]) -> None:
    meta_path(name).write_text(
        json.dumps(
            {
                "pid": pid,
                "port": port,
                "host": HOST,
                "cmd": cmd,
                "started_at": time.time(),
            },
            indent=2,
        )
        + "\n"
    )
    pid_path(name).write_text(str(pid) + "\n")


def clear_meta(name: str) -> None:
    for p in (pid_path(name), meta_path(name)):
        try:
            p.unlink()
        except FileNotFoundError:
            pass


def owned_pid(name: str, port: int) -> int | None:
    """Return PID only if metadata says we own it and the process still matches."""
    meta = read_meta(name)
    if not meta:
        return None
    pid = int(meta.get("pid", -1))
    if pid <= 0 or not alive(pid):
        clear_meta(name)
        return None
    if int(meta.get("port", -1)) != port:
        return None
    # Refuse to manage a PID that is not the listener on our port (stale / hijacked).
    listeners = who_listens(port)
    if listeners and pid not in listeners:
        print(f"WARNING: pid {pid} from .run/{name}.json is not listening on {port}; ignoring", file=sys.stderr)
        return None
    return pid


def wait_ready(url: str, timeout: float = READY_TIMEOUT) -> bool:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=0.5) as resp:
                if 200 <= resp.status < 300:
                    return True
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            time.sleep(0.15)
    return False


def start_service(name: str, script: Path, port: int, ready_url: str) -> int:
    existing = owned_pid(name, port)
    if existing and port_open(HOST, port):
        print(f"OK {name} already running on {HOST}:{port}")
        return 0

    foreign = who_listens(port)
    if foreign and not existing:
        print(
            f"ERROR: port {port} is already in use by PID(s) {foreign}, not managed by this lab.",
            file=sys.stderr,
        )
        print("Free the port or stop the other process, then retry.", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(script)]
    env = os.environ.copy()
    env["CM_HOST"] = HOST
    env["CM_PORT"] = str(port)
    if name == "training-app":
        env["CM_DB"] = str(ROOT / "data" / "training.db")
        env.setdefault("CM_FORCE_SEED", "1")
    log = open(log_path(name), "ab", buffering=0)
    proc = subprocess.Popen(
        cmd,
        cwd=str(ROOT),
        env=env,
        stdout=log,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    write_meta(name, proc.pid, port, cmd)
    if not wait_ready(ready_url):
        print(f"ERROR: {name} did not become ready at {ready_url}", file=sys.stderr)
        stop_service(name, port, force_meta_only=True)
        return 1
    # PID is stored under .run/ and shown by `make status` — keep OK line learner-clean.
    print(f"OK {name} listening on {HOST}:{port}")
    return 0


def stop_service(name: str, port: int, force_meta_only: bool = False) -> int:
    pid = owned_pid(name, port)
    if pid is None:
        foreign = who_listens(port)
        occupied = bool(foreign) or port_open(HOST, port)
        if occupied and not force_meta_only:
            print(
                f"ERROR: something is listening on {port}, but it is not a lab-managed {name} process.",
                file=sys.stderr,
            )
            print("Refusing to kill an unmanaged process.", file=sys.stderr)
            return 1
        print(f"{name} is not running")
        clear_meta(name)
        return 0

    try:
        os.kill(pid, signal.SIGTERM)
    except OSError as exc:
        print(f"WARNING: could not signal pid {pid}: {exc}", file=sys.stderr)

    deadline = time.time() + 5.0
    while time.time() < deadline:
        if not alive(pid):
            break
        time.sleep(0.1)
    else:
        print(f"WARNING: pid {pid} did not exit after SIGTERM", file=sys.stderr)

    clear_meta(name)
    if port_open(HOST, port):
        print(f"WARNING: port {port} still open after stop", file=sys.stderr)
        return 1
    print(f"Stopped {name}")
    return 0


def status() -> int:
    rows = [
        ("training-app", TRAINING_PORT, "http://127.0.0.1:5050/health"),
        ("http-demo", DEMO_PORT, "http://127.0.0.1:8080/"),
    ]
    code = 0
    for name, port, url in rows:
        pid = owned_pid(name, port)
        listening = port_open(HOST, port)
        managed = "managed" if pid else "unmanaged/none"
        print(f"{name:14} port={port} listening={listening} pid={pid or '-'} ({managed})")
        if listening:
            try:
                with urllib.request.urlopen(url, timeout=1.0) as resp:
                    print(f"  probe {url} -> HTTP {resp.status}")
            except Exception as exc:  # noqa: BLE001
                print(f"  probe {url} -> FAIL ({exc})")
                code = 1
    return code


def verify() -> int:
    """Confirm training health JSON and demo HTML while both are up."""
    try:
        with urllib.request.urlopen("http://127.0.0.1:5050/health", timeout=2.0) as resp:
            body = json.loads(resp.read().decode())
            if resp.status != 200 or body.get("ok") is not True or body.get("port") != 5050:
                print("FAIL training /health", resp.status, body, file=sys.stderr)
                return 1
            print("OK training /health", body)
        with urllib.request.urlopen("http://127.0.0.1:8080/", timeout=2.0) as resp:
            text = resp.read().decode()
            if resp.status != 200 or "HTTP Demo Service" not in text:
                print("FAIL http-demo /", resp.status, file=sys.stderr)
                return 1
            print("OK http-demo /")
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL verify: {exc}", file=sys.stderr)
        return 1
    # Loopback-only: refuse if process claims 0.0.0.0 in our meta host field.
    for name in ("training-app", "http-demo"):
        meta = read_meta(name)
        if meta and meta.get("host") not in (None, "127.0.0.1", "localhost"):
            print(f"FAIL {name} host is not loopback: {meta.get('host')}", file=sys.stderr)
            return 1
    print("OK verify-lab")
    return 0


def lab_up() -> int:
    a = start_service(
        "training-app",
        ROOT / "training_app.py",
        TRAINING_PORT,
        "http://127.0.0.1:5050/health",
    )
    b = start_service(
        "http-demo",
        ROOT / "http_demo.py",
        DEMO_PORT,
        "http://127.0.0.1:8080/",
    )
    return a or b


def lab_down() -> int:
    # Stop demo first, then training — order matches teaching cleanup.
    rc = stop_service("http-demo", DEMO_PORT)
    rc2 = stop_service("training-app", TRAINING_PORT)
    return rc or rc2


def main() -> int:
    p = argparse.ArgumentParser(description="Cyber Mechanics shared lab control")
    p.add_argument(
        "action",
        choices=[
            "up",
            "down",
            "status",
            "verify",
            "start-demo",
            "stop-demo",
            "start-training",
            "stop-training",
        ],
    )
    args = p.parse_args()
    if args.action == "up":
        return lab_up()
    if args.action == "down":
        return lab_down()
    if args.action == "status":
        return status()
    if args.action == "verify":
        return verify()
    if args.action == "start-demo":
        return start_service("http-demo", ROOT / "http_demo.py", DEMO_PORT, "http://127.0.0.1:8080/")
    if args.action == "stop-demo":
        return stop_service("http-demo", DEMO_PORT)
    if args.action == "start-training":
        return start_service(
            "training-app", ROOT / "training_app.py", TRAINING_PORT, "http://127.0.0.1:5050/health"
        )
    if args.action == "stop-training":
        return stop_service("training-app", TRAINING_PORT)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
