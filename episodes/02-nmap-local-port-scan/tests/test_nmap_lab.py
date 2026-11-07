#!/usr/bin/env python3
"""Episode 02 — loopback port discovery without requiring nmap."""
from __future__ import annotations

import socket
import subprocess
import sys
import unittest
from pathlib import Path

SHARED = Path(__file__).resolve().parents[1].parent.parent / "shared"
LABCTL = SHARED / "labctl.py"
HOST = "127.0.0.1"


def port_open(port: int) -> bool:
    try:
        with socket.create_connection((HOST, port), timeout=0.4):
            return True
    except OSError:
        return False


class NmapLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        subprocess.check_call([sys.executable, str(LABCTL), "up"])

    @classmethod
    def tearDownClass(cls) -> None:
        subprocess.call([sys.executable, str(LABCTL), "down"])

    def test_01_both_open_9090_closed(self) -> None:
        self.assertTrue(port_open(5050))
        self.assertTrue(port_open(8080))
        self.assertFalse(port_open(9090))

    def test_02_stop_demo_closes_8080_keeps_5050(self) -> None:
        subprocess.check_call([sys.executable, str(LABCTL), "stop-demo"])
        self.assertTrue(port_open(5050))
        self.assertFalse(port_open(8080))

    def test_03_start_demo_restores_8080(self) -> None:
        subprocess.check_call([sys.executable, str(LABCTL), "start-demo"])
        self.assertTrue(port_open(5050))
        self.assertTrue(port_open(8080))


if __name__ == "__main__":
    unittest.main()
