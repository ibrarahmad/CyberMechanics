#!/usr/bin/env python3
"""Positive and negative tests for Episode 01 lab control."""
from __future__ import annotations

import http.client
import json
import socket
import subprocess
import sys
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
HOST = "127.0.0.1"


def run_ctl(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PY, str(ROOT / "labctl.py"), *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


def curl_status(url: str) -> tuple[int | None, bytes]:
    try:
        with urllib.request.urlopen(url, timeout=2.0) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()
    except Exception:
        return None, b""


def port_open(port: int) -> bool:
    try:
        with socket.create_connection((HOST, port), timeout=0.4):
            return True
    except OSError:
        return False


def listeners(port: int) -> list[int]:
    try:
        out = subprocess.check_output(
            ["lsof", f"-tiTCP:{port}", "-sTCP:LISTEN"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return []
    return [int(x) for x in out.splitlines() if x.strip().isdigit()]


class LabLifecycleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        run_ctl("down")
        time.sleep(0.3)

    @classmethod
    def tearDownClass(cls) -> None:
        run_ctl("down")

    def setUp(self) -> None:
        run_ctl("down")
        time.sleep(0.2)

    def tearDown(self) -> None:
        run_ctl("down")

    def test_01_lab_up_health_and_demo(self) -> None:
        rc = run_ctl("up")
        self.assertEqual(rc.returncode, 0, rc.stderr + rc.stdout)
        status, body = curl_status("http://127.0.0.1:5050/health")
        self.assertEqual(status, 200)
        data = json.loads(body.decode())
        self.assertTrue(data.get("ok") is True)
        self.assertEqual(data.get("service"), "training-app")
        self.assertEqual(data.get("port"), 5050)
        status2, page = curl_status("http://127.0.0.1:8080/")
        self.assertEqual(status2, 200)
        self.assertIn(b"HTTP Demo Service", page)

    def test_02_stop_demo_keeps_training(self) -> None:
        self.assertEqual(run_ctl("up").returncode, 0)
        self.assertEqual(run_ctl("stop-demo").returncode, 0)
        status8080, _ = curl_status("http://127.0.0.1:8080/")
        self.assertIsNone(status8080)
        self.assertFalse(port_open(8080))
        status5050, body = curl_status("http://127.0.0.1:5050/health")
        self.assertEqual(status5050, 200)
        self.assertTrue(json.loads(body.decode()).get("ok"))

    def test_03_start_demo_restores(self) -> None:
        self.assertEqual(run_ctl("up").returncode, 0)
        self.assertEqual(run_ctl("stop-demo").returncode, 0)
        self.assertEqual(run_ctl("start-demo").returncode, 0)
        status, page = curl_status("http://127.0.0.1:8080/")
        self.assertEqual(status, 200)
        self.assertIn(b"HTTP Demo Service", page)

    def test_04_idempotent_up(self) -> None:
        self.assertEqual(run_ctl("up").returncode, 0)
        again = run_ctl("up")
        self.assertEqual(again.returncode, 0)
        self.assertIn("already running", again.stdout.lower() + again.stderr.lower())

    def test_05_repeated_stop_start(self) -> None:
        self.assertEqual(run_ctl("up").returncode, 0)
        for _ in range(3):
            self.assertEqual(run_ctl("stop-demo").returncode, 0)
            self.assertIsNone(curl_status("http://127.0.0.1:8080/")[0])
            self.assertEqual(run_ctl("start-demo").returncode, 0)
            self.assertEqual(curl_status("http://127.0.0.1:8080/")[0], 200)

    def test_06_verify_and_status(self) -> None:
        self.assertEqual(run_ctl("up").returncode, 0)
        self.assertEqual(run_ctl("verify").returncode, 0)
        self.assertEqual(run_ctl("status").returncode, 0)

    def test_07_port_conflict_refuses(self) -> None:
        # Occupy 8080 with an unmanaged listener, then start-demo must fail safely.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, 8080))
        sock.listen(1)
        try:
            self.assertEqual(run_ctl("start-training").returncode, 0)
            conflict = run_ctl("start-demo")
            self.assertNotEqual(conflict.returncode, 0)
            self.assertIn("already in use", conflict.stderr.lower() + conflict.stdout.lower())
        finally:
            sock.close()
            run_ctl("stop-training")

    def test_08_stop_unmanaged_refuses_kill(self) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((HOST, 8080))
        sock.listen(1)
        try:
            before = listeners(8080)
            self.assertTrue(before, "test fixture must hold 8080 before stop-demo")
            # No lab meta — stop-demo must refuse and leave the foreign listener alone.
            rc = run_ctl("stop-demo")
            self.assertNotEqual(rc.returncode, 0, rc.stdout + rc.stderr)
            self.assertIn("not a lab-managed", (rc.stderr + rc.stdout).lower())
            after = listeners(8080)
            self.assertTrue(after, "unmanaged listener must survive stop-demo")
            self.assertEqual(before, after)
        finally:
            sock.close()

    def test_09_single_server_header_and_head_length(self) -> None:
        self.assertEqual(run_ctl("up").returncode, 0)

        def assert_headers(host: str, port: int, path: str, expect_server: str) -> None:
            conn = http.client.HTTPConnection(host, port, timeout=2.0)
            try:
                conn.request("GET", path)
                get_resp = conn.getresponse()
                get_body = get_resp.read()
                get_headers = get_resp.getheaders()
                servers = [v for k, v in get_headers if k.lower() == "server"]
                self.assertEqual(get_resp.status, 200)
                self.assertEqual(servers, [expect_server], f"duplicate/missing Server: {servers}")
                get_len = int(dict((k.lower(), v) for k, v in get_headers)["content-length"])
                self.assertEqual(get_len, len(get_body))

                conn.request("HEAD", path)
                head_resp = conn.getresponse()
                head_body = head_resp.read()
                head_headers = head_resp.getheaders()
                head_servers = [v for k, v in head_headers if k.lower() == "server"]
                self.assertEqual(head_resp.status, 200)
                self.assertEqual(head_body, b"")
                self.assertEqual(head_servers, [expect_server])
                head_len = int(dict((k.lower(), v) for k, v in head_headers)["content-length"])
                self.assertEqual(head_len, get_len, "HEAD Content-Length must match GET body size")
            finally:
                conn.close()

        assert_headers(HOST, 5050, "/health", "CyberMechanicsTraining/1.0")
        assert_headers(HOST, 8080, "/", "CyberMechanics-HTTP-Demo/1.0")

    def test_10_ok_line_has_no_pid(self) -> None:
        rc = run_ctl("up")
        self.assertEqual(rc.returncode, 0, rc.stderr + rc.stdout)
        combined = rc.stdout + rc.stderr
        self.assertIn("OK training-app listening on 127.0.0.1:5050", combined)
        self.assertIn("OK http-demo listening on 127.0.0.1:8080", combined)
        self.assertNotIn("(pid ", combined)


if __name__ == "__main__":
    unittest.main()
