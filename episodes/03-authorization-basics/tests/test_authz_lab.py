#!/usr/bin/env python3
"""Episode 03 — authorization 200 vs 403."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
import urllib.error
import urllib.request
from pathlib import Path

SHARED = Path(__file__).resolve().parents[1].parent.parent / "shared"
LABCTL = SHARED / "labctl.py"
BASE = "http://127.0.0.1:5050"


def req(method: str, url: str, data: dict | None = None, session: str | None = None):
    body = None
    headers = {"Accept": "application/json"}
    if session:
        headers["Cookie"] = f"session={session}"
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=8) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else {}, resp.headers
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            payload = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            payload = {"raw": raw}
        return exc.code, payload, exc.headers


def login(username: str) -> str:
    code, payload, headers = req("POST", f"{BASE}/login", {"username": username})
    assert code == 200 and payload.get("ok"), (code, payload)
    raw = headers.get("Set-Cookie") or ""
    assert "session=" in raw, raw
    return raw.split("session=", 1)[1].split(";", 1)[0].strip()


class AuthzLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(LABCTL), "up"])

    @classmethod
    def tearDownClass(cls) -> None:
        subprocess.call([sys.executable, str(LABCTL), "down"])

    def test_alice_own_safe_200(self) -> None:
        alice = login("alice")
        code, payload, _ = req("GET", f"{BASE}/api/invoices/safe/101", session=alice)
        self.assertEqual(code, 200)
        self.assertEqual(payload.get("invoice", {}).get("id"), 101)

    def test_alice_bob_unsafe_200(self) -> None:
        alice = login("alice")
        code, payload, _ = req("GET", f"{BASE}/api/invoices/unsafe/201", session=alice)
        self.assertEqual(code, 200)
        self.assertEqual(payload.get("invoice", {}).get("owner_id"), 2)

    def test_alice_bob_safe_403(self) -> None:
        alice = login("alice")
        code, payload, _ = req("GET", f"{BASE}/api/invoices/safe/201", session=alice)
        self.assertEqual(code, 403)
        self.assertEqual(payload.get("error"), "forbidden")


if __name__ == "__main__":
    unittest.main()
