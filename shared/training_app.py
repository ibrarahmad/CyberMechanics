#!/usr/bin/env python3
"""Cyber Mechanics shared training app (loopback only).

Serves Episode 01 health + index, Episode 03 invoice authz demos,
and Episode 04 product-search demos. Fictional data only.
"""
from __future__ import annotations

import json
import os
import sqlite3
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get("CM_DB", ROOT / "data" / "training.db"))
HOST = os.environ.get("CM_HOST", "127.0.0.1")
PORT = int(os.environ.get("CM_PORT", "5050"))
BANNER = "CyberMechanicsTraining/1.0"

INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Cyber Mechanics Training App</title>
  <style>
    body{font-family:system-ui,-apple-system,sans-serif;background:#111;color:#eee;padding:2rem;line-height:1.5;max-width:46rem}
    code{background:#222;padding:.15rem .4rem;border-radius:4px}
  </style>
</head>
<body>
  <h1>Cyber Mechanics Training App</h1>
  <p>Local authorized training surface on <code>127.0.0.1</code>. Fictional data only.</p>
  <ul>
    <li><code>GET /health</code> — JSON health check</li>
    <li><code>POST /login</code> — <code>{"username":"alice"}</code> or <code>bob</code></li>
    <li><code>GET /api/invoices/unsafe/{id}</code> — missing owner check (teaching flaw)</li>
    <li><code>GET /api/invoices/safe/{id}</code> — owner check (403 if wrong owner)</li>
    <li><code>GET /api/products/search/unsafe?q=</code> — string-built SQL (teaching flaw)</li>
    <li><code>GET /api/products/search/safe?q=</code> — parameterized SQL</li>
  </ul>
  <p>HTTP 200 means the endpoint answered. It does <strong>not</strong> prove the app is secure.</p>
</body>
</html>
"""


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def seed() -> None:
    conn = connect()
    conn.executescript(
        """
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS invoices;
        DROP TABLE IF EXISTS products;
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            display_name TEXT NOT NULL
        );
        CREATE TABLE invoices (
            id INTEGER PRIMARY KEY,
            owner_id INTEGER NOT NULL,
            label TEXT NOT NULL,
            amount_cents INTEGER NOT NULL,
            FOREIGN KEY(owner_id) REFERENCES users(id)
        );
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            sku TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL
        );
        """
    )
    users = [(1, "alice", "Alice Trainer"), (2, "bob", "Bob Trainer")]
    invoices = [
        (101, 1, "Alice lab invoice A", 1200),
        (102, 1, "Alice lab invoice B", 3400),
        (201, 2, "Bob lab invoice A", 5600),
        (202, 2, "Bob lab invoice B", 7800),
    ]
    products = [
        (1, "CM-NODE-01", "Sensor Node", "hardware"),
        (2, "CM-CABLE-02", "Patch Cable", "hardware"),
        (3, "CM-NOTE-03", "Lab Notebook", "supplies"),
        (4, "CM-BADGE-04", "Trainer Badge", "supplies"),
        (5, "CM-KEY-05", "Practice Key Fob", "hardware"),
    ]
    conn.executemany("INSERT INTO users VALUES (?,?,?)", users)
    conn.executemany("INSERT INTO invoices VALUES (?,?,?,?)", invoices)
    conn.executemany("INSERT INTO products VALUES (?,?,?,?)", products)
    conn.commit()
    conn.close()


SESSIONS: dict[str, int] = {}


def issue_session(user_id: int) -> str:
    token = f"cm-session-{uuid.uuid4().hex}"
    SESSIONS[token] = user_id
    return token


def user_from_cookie(cookie: str | None) -> int | None:
    if not cookie:
        return None
    for part in cookie.split(";"):
        part = part.strip()
        if part.startswith("session="):
            return SESSIONS.get(part.split("=", 1)[1].strip())
    return None


def row_to_dict(row: sqlite3.Row | None) -> dict | None:
    if row is None:
        return None
    return {k: row[k] for k in row.keys()}


class Handler(BaseHTTPRequestHandler):
    server_version = BANNER
    sys_version = ""

    def version_string(self) -> str:
        return self.server_version

    def log_message(self, fmt: str, *args) -> None:
        return

    def _json(self, code: int, payload: dict, extra_headers: list[tuple[str, str]] | None = None) -> None:
        body = (json.dumps(payload, indent=2) + "\n").encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        if extra_headers:
            for k, v in extra_headers:
                self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _html(self, code: int, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8") or "{}")

    def do_HEAD(self) -> None:  # noqa: N802
        self.do_GET()

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = parsed.path
        qs = parse_qs(parsed.query)

        if path in ("/", "/index.html"):
            self._html(200, INDEX_HTML)
            return
        if path == "/health":
            self._json(200, {"ok": True, "service": "training-app", "port": PORT})
            return
        if path.startswith("/api/invoices/unsafe/"):
            self._invoice(path.rsplit("/", 1)[-1], safe=False)
            return
        if path.startswith("/api/invoices/safe/"):
            self._invoice(path.rsplit("/", 1)[-1], safe=True)
            return
        if path == "/api/products/search/unsafe":
            self._search(qs.get("q", [""])[0], safe=False)
            return
        if path == "/api/products/search/safe":
            self._search(qs.get("q", [""])[0], safe=True)
            return
        self._json(404, {"error": "not_found"})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        if parsed.path == "/login":
            data = self._read_json()
            username = (data.get("username") or "").strip().lower()
            conn = connect()
            row = conn.execute(
                "SELECT id, username, display_name FROM users WHERE username=?",
                (username,),
            ).fetchone()
            conn.close()
            if not row:
                self._json(401, {"error": "unknown_user"})
                return
            token = issue_session(int(row["id"]))
            self._json(
                200,
                {"ok": True, "user": row_to_dict(row)},
                extra_headers=[("Set-Cookie", f"session={token}; Path=/; HttpOnly")],
            )
            return
        if parsed.path == "/reset":
            seed()
            SESSIONS.clear()
            self._json(200, {"ok": True, "reset": True})
            return
        self._json(404, {"error": "not_found"})

    def _invoice(self, invoice_id: str, safe: bool) -> None:
        uid = user_from_cookie(self.headers.get("Cookie"))
        if uid is None:
            self._json(401, {"error": "login_required"})
            return
        try:
            iid = int(invoice_id)
        except ValueError:
            self._json(400, {"error": "bad_id"})
            return
        conn = connect()
        row = conn.execute(
            "SELECT id, owner_id, label, amount_cents FROM invoices WHERE id=?",
            (iid,),
        ).fetchone()
        conn.close()
        if row is None:
            self._json(404, {"error": "missing_invoice"})
            return
        if safe and int(row["owner_id"]) != uid:
            self._json(403, {"error": "forbidden", "reason": "owner_mismatch"})
            return
        self._json(200, {"invoice": row_to_dict(row), "mode": "safe" if safe else "unsafe"})

    def _search(self, q: str, safe: bool) -> None:
        conn = connect()
        if safe:
            rows = conn.execute(
                "SELECT id, sku, name, category FROM products WHERE name LIKE ?",
                (f"%{q}%",),
            ).fetchall()
        else:
            # Intentionally unsafe for local training only. Do not copy to production.
            sql = f"SELECT id, sku, name, category FROM products WHERE name LIKE '%{q}%'"
            try:
                rows = conn.execute(sql).fetchall()
            except sqlite3.Error as exc:
                conn.close()
                self._json(400, {"error": "query_error", "detail": str(exc), "mode": "unsafe"})
                return
        conn.close()
        self._json(
            200,
            {
                "mode": "safe" if safe else "unsafe",
                "query_echo": q,
                "count": len(rows),
                "products": [row_to_dict(r) for r in rows],
            },
        )


def main() -> None:
    if HOST not in ("127.0.0.1", "localhost", "::1"):
        raise SystemExit(f"Refusing to bind non-loopback host: {HOST!r}")
    if not DB_PATH.exists() or os.environ.get("CM_FORCE_SEED") == "1":
        seed()
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"training-app listening on {HOST}:{PORT}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
