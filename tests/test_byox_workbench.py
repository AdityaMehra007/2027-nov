# Copyright 2026 CASHFLOW INFINITY: OMNIVERSE
# Apache License, Version 2.0

"""Comprehensive End-to-End Test Suite for BYOX Interactive Visual Workbench.

Built on Python 3.13 Standard Library (unittest.IsolatedAsyncioTestCase).
Zero external runtime dependencies.
"""

from __future__ import annotations
import asyncio
import json
import os
import shutil
import tempfile
import unittest

from byox.workbench.server import WorkbenchServer
from pyweb.websocket import (
    build_websocket_frame,
    parse_websocket_frame,
)


async def async_http_request(
    method: str,
    path: str,
    port: int,
    body: bytes = b"",
    headers: dict[str, str] | None = None,
) -> tuple[int, dict[str, str], bytes]:
    """Pure asyncio HTTP/1.1 client request helper."""
    reader, writer = await asyncio.open_connection("127.0.0.1", port)
    req_lines = [f"{method.upper()} {path} HTTP/1.1", f"Host: 127.0.0.1:{port}", "Connection: close"]
    if headers:
        for k, v in headers.items():
            req_lines.append(f"{k}: {v}")
    if body:
        req_lines.append(f"Content-Length: {len(body)}")
    raw_req = "\r\n".join(req_lines).encode("utf-8") + b"\r\n\r\n" + body
    writer.write(raw_req)
    await writer.drain()

    # Read headers
    buf = bytearray()
    while b"\r\n\r\n" not in buf:
        chunk = await reader.read(4096)
        if not chunk:
            break
        buf.extend(chunk)

    split_idx = buf.find(b"\r\n\r\n")
    header_part = bytes(buf[:split_idx])
    body_part = bytearray(buf[split_idx + 4 :])

    lines = header_part.decode("utf-8", errors="replace").split("\r\n")
    status_code = int(lines[0].split()[1]) if lines and len(lines[0].split()) > 1 else 0
    resp_headers = {}
    content_len = 0
    for line in lines[1:]:
        if ":" in line:
            hk, hv = line.split(":", 1)
            hk_lower = hk.strip().lower()
            resp_headers[hk_lower] = hv.strip()
            if hk_lower == "content-length":
                content_len = int(hv.strip())

    while len(body_part) < content_len:
        chunk = await reader.read(min(4096, content_len - len(body_part)))
        if not chunk:
            break
        body_part.extend(chunk)

    writer.close()
    try:
        await writer.wait_closed()
    except Exception:
        pass

    return status_code, resp_headers, bytes(body_part)


class TestBYOXWorkbench(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        db_path = os.path.join(self.tmp_dir, "test_wb.db")
        repo_dir = os.path.join(self.tmp_dir, "test_repo")
        from pygit.repository import init_repo
        init_repo(repo_dir)
        self.server = WorkbenchServer(host="127.0.0.1", port=0, db_path=db_path, repo_path=repo_dir)
        await self.server.start()
        self.port = self.server.actual_port

    async def asyncTearDown(self):
        await self.server.stop()
        try:
            shutil.rmtree(self.tmp_dir)
        except Exception:
            pass

    async def test_workbench_http_endpoints(self):
        # 1. Test Static Index HTML
        code, headers, body = await async_http_request("GET", "/", self.port)
        self.assertEqual(code, 200)
        content = body.decode("utf-8")
        self.assertTrue("BYOX Studio" in content or "Build-Your-Own-X" in content)
        self.assertEqual(headers.get("content-type"), "text/html; charset=utf-8")

        # 2. Test API Status
        code, _, body = await async_http_request("GET", "/api/status", self.port)
        self.assertEqual(code, 200)
        status_data = json.loads(body.decode("utf-8"))
        self.assertEqual(status_data["status"], "operational")
        engines = status_data["engines"]
        self.assertIn("pyredis", engines)
        self.assertIn("pydb", engines)
        self.assertIn("pygit", engines)
        self.assertIn("pyshell", engines)
        self.assertIn("pyweb", engines)
        self.assertIn("pytransformer", engines)

        # 3. Test PyRedis Command API
        set_payload = json.dumps({"command": "SET workbench_test_key 42"}).encode("utf-8")
        code, _, body = await async_http_request(
            "POST",
            "/api/redis/command",
            self.port,
            body=set_payload,
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(code, 200)
        redis_resp = json.loads(body.decode("utf-8"))
        self.assertIn("+OK", redis_resp["raw_resp"])
        self.assertTrue(redis_resp["is_mutation"])

        # Test PyRedis Keyspace API
        code, _, body = await async_http_request("GET", "/api/redis/keys", self.port)
        self.assertEqual(code, 200)
        keys_data = json.loads(body.decode("utf-8"))
        key_names = [item["key"] for item in keys_data["keys"]]
        self.assertIn("workbench_test_key", key_names)

        # 4. Test PyDB Query API (SELECT)
        query_payload = json.dumps({"sql": "SELECT service, latency_ms FROM metrics WHERE id = 1;"}).encode("utf-8")
        code, _, body = await async_http_request(
            "POST",
            "/api/db/query",
            self.port,
            body=query_payload,
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(code, 200)
        db_resp = json.loads(body.decode("utf-8"))
        self.assertEqual(db_resp["columns"], ["service", "latency_ms"])
        self.assertEqual(len(db_resp["rows"]), 1)
        self.assertEqual(db_resp["rows"][0][0], "PyRedis")

        # Test PyDB Query API (INSERT)
        insert_payload = json.dumps({"sql": "INSERT INTO metrics VALUES (4, 'PyTransformer', 0.06);"}).encode("utf-8")
        code, _, body = await async_http_request(
            "POST",
            "/api/db/query",
            self.port,
            body=insert_payload,
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(code, 200)
        insert_resp = json.loads(body.decode("utf-8"))
        self.assertEqual(insert_resp["rows_affected"], 1)

        # 5. Test PyGit Graph API
        code, _, body = await async_http_request("GET", "/api/git/graph", self.port)
        self.assertEqual(code, 200)
        git_data = json.loads(body.decode("utf-8"))
        self.assertIn("branch", git_data)
        self.assertIn("branches", git_data)
        self.assertIn("commits", git_data)
        self.assertIn("status", git_data)

        # 6. Test Benchmarks API
        code, _, body = await async_http_request("GET", "/api/benchmarks", self.port)
        self.assertEqual(code, 200)
        bench_data = json.loads(body.decode("utf-8"))
        self.assertIn("results", bench_data)

    async def test_workbench_websocket_shell(self):
        reader, writer = await asyncio.open_connection("127.0.0.1", self.port)

        sec_key = "dGhlIHNhbXBsZSBub25jZQ=="
        handshake = (
            f"GET /ws/shell HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{self.port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {sec_key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        writer.write(handshake.encode("utf-8"))
        await writer.drain()

        # Read handshake
        buf = bytearray()
        while b"\r\n\r\n" not in buf:
            chunk = await reader.read(4096)
            if not chunk:
                break
            buf.extend(chunk)

        split_idx = buf.find(b"\r\n\r\n")
        handshake_data = bytes(buf[:split_idx + 4])
        self.assertIn(b"101 Switching Protocols", handshake_data)

        # Read welcome frame
        frame_buf = bytearray(buf[split_idx + 4:])
        while True:
            welcome_frame = parse_websocket_frame(bytes(frame_buf))
            if welcome_frame is not None:
                break
            chunk = await reader.read(4096)
            if not chunk:
                break
            frame_buf.extend(chunk)

        self.assertIsNotNone(welcome_frame)
        self.assertIn("Connected to PyShell", welcome_frame.payload.decode("utf-8"))

        # Send command frame: echo "BYOX_SHELL_TEST"
        cmd_frame = build_websocket_frame('echo "BYOX_SHELL_TEST"', mask=True)
        writer.write(cmd_frame)
        await writer.drain()

        # Read response frame
        resp_buf = bytearray()
        while True:
            resp_frame = parse_websocket_frame(bytes(resp_buf))
            if resp_frame is not None:
                break
            chunk = await reader.read(4096)
            if not chunk:
                break
            resp_buf.extend(chunk)

        self.assertIsNotNone(resp_frame)
        self.assertIn("BYOX_SHELL_TEST", resp_frame.payload.decode("utf-8"))

        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass

    async def test_workbench_websocket_llm_stream(self):
        reader, writer = await asyncio.open_connection("127.0.0.1", self.port)

        sec_key = "dGhlIHNhbXBsZSBub25jZQ=="
        handshake = (
            f"GET /ws/llm HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{self.port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {sec_key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        )
        writer.write(handshake.encode("utf-8"))
        await writer.drain()

        buf = bytearray()
        while b"\r\n\r\n" not in buf:
            chunk = await reader.read(4096)
            if not chunk:
                break
            buf.extend(chunk)

        self.assertIn(b"101 Switching Protocols", bytes(buf))

        # Request 3 generated tokens
        req_payload = json.dumps({"prompt": "The", "tokens": 3})
        writer.write(build_websocket_frame(req_payload, mask=True))
        await writer.drain()

        # Collect streamed token events
        tokens_received = []
        is_done = False
        frame_buf = bytearray()

        for _ in range(20):
            chunk = await reader.read(4096)
            if not chunk:
                break
            frame_buf.extend(chunk)
            while True:
                frame = parse_websocket_frame(bytes(frame_buf))
                if frame is None:
                    break
                payload_len = len(frame.payload)
                offset = 2
                if payload_len > 125:
                    offset += 2
                total_len = offset + payload_len
                frame_buf = frame_buf[total_len:]

                event = json.loads(frame.payload.decode("utf-8"))
                if event.get("done"):
                    is_done = True
                    break
                if "token" in event:
                    tokens_received.append(event["token"])
            if is_done:
                break

        self.assertTrue(is_done)
        self.assertEqual(len(tokens_received), 3)

        writer.close()
        try:
            await writer.wait_closed()
        except Exception:
            pass


if __name__ == "__main__":
    unittest.main()
