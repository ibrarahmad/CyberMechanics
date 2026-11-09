#!/usr/bin/env python3
"""HTTP Demo Service — independent second listener for Episode 01 (loopback only)."""
from __future__ import annotations

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HOST = os.environ.get("CM_HOST", "127.0.0.1")
PORT = int(os.environ.get("CM_PORT", "8080"))
BANNER = "CyberMechanics-HTTP-Demo/1.0"

PAGE = f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"/><title>HTTP Demo Service</title>
<style>body{{font-family:system-ui;background:#101820;color:#F5F1E8;padding:2rem}}</style>
</head>
<body>
  <h1>HTTP Demo Service</h1>
  <p>Banner: {BANNER}</p>
  <p>Purpose: a second open port beside the training app on this computer only.</p>
</body>
</html>
""".encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    # Branded Server header comes from BaseHTTPRequestHandler via version_string().
    server_version = BANNER
    sys_version = ""

    def version_string(self) -> str:
        return self.server_version

    def _send(self, code: int, body: bytes) -> None:
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        self._send(200, PAGE)

    def do_HEAD(self) -> None:  # noqa: N802
        self._send(200, PAGE)

    def log_message(self, fmt: str, *args) -> None:
        return


def main() -> None:
    if HOST not in ("127.0.0.1", "localhost", "::1"):
        raise SystemExit(f"Refusing to bind non-loopback host: {HOST!r}")
    httpd = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"http-demo listening on {HOST}:{PORT} banner={BANNER}", flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
