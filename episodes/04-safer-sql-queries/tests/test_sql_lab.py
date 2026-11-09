#!/usr/bin/env python3
"""Episode 04 — unsafe vs safe product search counts."""
from __future__ import annotations

import json
import subprocess
import sys
import unittest
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SHARED = Path(__file__).resolve().parents[1].parent.parent / "shared"
LABCTL = SHARED / "labctl.py"
BASE = "http://127.0.0.1:5050"


def get_json(url: str):
    try:
        with urllib.request.urlopen(url, timeout=8) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode() or "{}")


class SqlLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(LABCTL), "up"])

    @classmethod
    def tearDownClass(cls) -> None:
        subprocess.call([sys.executable, str(LABCTL), "down"])

    def test_01_normal_unsafe_one(self) -> None:
        code, payload = get_json(f"{BASE}/api/products/search/unsafe?q=Sensor")
        self.assertEqual(code, 200)
        self.assertEqual(payload.get("count"), 1)

    def test_02_normal_safe_one(self) -> None:
        code, payload = get_json(f"{BASE}/api/products/search/safe?q=Sensor")
        self.assertEqual(code, 200)
        self.assertEqual(payload.get("count"), 1)

    def test_03_crafted_unsafe_five_safe_zero(self) -> None:
        # Lab-only probe string — not for narration / YouTube copy.
        probe = "' OR '1'='1"
        q = urllib.parse.quote(probe)
        code_u, payload_u = get_json(f"{BASE}/api/products/search/unsafe?q={q}")
        code_s, payload_s = get_json(f"{BASE}/api/products/search/safe?q={q}")
        self.assertEqual(code_u, 200)
        self.assertEqual(payload_u.get("count"), 5)
        self.assertEqual(code_s, 200)
        self.assertEqual(payload_s.get("count"), 0)


if __name__ == "__main__":
    unittest.main()
