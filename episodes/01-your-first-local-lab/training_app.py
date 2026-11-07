#!/usr/bin/env python3
"""Cyber Mechanics Training App — Episode 01 (loopback only)."""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = os.environ.get("CM_HOST", "127.0.0.1")
PORT = int(os.environ.get("CM_PORT", "5050"))
BANNER = "CyberMechanicsTraining/1.0"


INDEX_HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Cyber Mechanics Training App</title>
  <style>
    body{font-family:system-ui,-apple-system,sans-serif;background:#111;color:#eee;padding:2rem;line-height:1.5;max-width:42rem}
    code{background:#222;padding:.15rem .4rem;border-radius:4px}
    a{color:#8FCFEA}
  </style>
</head>
<body>
  <h1>Cyber Mechanics Training App</h1>
  <p>Local authorized training surface. Runs only on <code>127.0.0.1</code>.</p>
  <ul>
    <li><code>GET /health</code> — JSON health check (this lesson)</li>
    <li>Later episodes add fictional users and search demos on the same app family</li>
  </ul>
  <p>HTTP 200 means the endpoint answered. It does <strong>not</strong> prove the app is secure.</p>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    # Branded Server header comes from BaseHTTPRequestHandler via version_string().
    # Do not also send_header("Server", ...) — that duplicates the header.
    # Override version_string: default appends " " + sys_version even when empty.
    server_version = BANNER
    sys_version = ""

    def version_string(self) -> str:
        return self.server_version

    def _send(self, code: int, body: bytes, content_type: str) -> None:
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        # HEAD must advertise the same Content-Length as GET would return.
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_HEAD(self) -> None:  # noqa: N802
        self.do_GET()

    def do_GET(self) -> None:  # noqa: N802
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            self._send(200, INDEX_HTML.encode("utf-8"), "text/html; charset=utf-8")
            return
        if path == "/health":
            payload = {"ok": True, "service": "training-app", "port": PORT}
            body = (json.dumps(payload, indent=2) + "\n").encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")
            return
        self._send(404, b'{"error":"not_found"}\n', "application/json; charset=utf-8")

    def log_message(self, fmt: str, *args) -> None:
        return


def main() -> None:
    if HOST not in ("127.0.0.1", "localhost", "::1"):
        raise SystemExit(f"Refusing to bind non-loopback host: {HOST!r}")
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"training-app listening on {HOST}:{PORT}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
