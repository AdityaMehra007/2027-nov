import asyncio
import unittest
from pyweb.http import HTTPRequest, HTTPResponse, parse_http_request
from pyweb.websocket import compute_accept_key, parse_websocket_frame, build_websocket_frame

class TestPyWeb(unittest.TestCase):
    def test_http_request_parsing(self):
        raw = (
            b"POST /api/echo?format=json HTTP/1.1\r\n"
            b"Host: localhost:8080\r\n"
            b"Content-Type: application/json\r\n"
            b"Content-Length: 17\r\n"
            b"\r\n"
            b'{"message":"hi"}'
        )
        req = parse_http_request(raw)
        self.assertIsNotNone(req)
        self.assertEqual(req.method, "POST")
        self.assertEqual(req.path, "/api/echo")
        self.assertEqual(req.query_params.get("format"), "json")
        self.assertEqual(req.headers.get("content-type"), "application/json")
        self.assertEqual(req.body, b'{"message":"hi"}')

    def test_http_response_serialization(self):
        resp = HTTPResponse.json({"status": "ok", "code": 200}, status_code=200)
        serialized = resp.serialize()
        self.assertTrue(serialized.startswith(b"HTTP/1.1 200 OK\r\n"))
        self.assertIn(b"Content-Type: application/json\r\n", serialized)
        self.assertIn(b'{"status": "ok", "code": 200}', serialized)

    def test_websocket_handshake_key(self):
        # Canonical RFC 6455 test vector
        test_key = "dGhlIHNhbXBsZSBub25jZQ=="
        expected_accept = "s3pPLMBiTxaQ9kYGzzhZRbK+xOo="
        computed = compute_accept_key(test_key)
        self.assertEqual(computed, expected_accept)

    def test_websocket_frame_roundtrip(self):
        payload = "Hello WebSocket!"
        frame_bytes = build_websocket_frame(payload, opcode=0x1)  # 0x1 = text

        frame = parse_websocket_frame(frame_bytes)
        self.assertIsNotNone(frame)
        self.assertEqual(frame.opcode, 0x1)
        self.assertEqual(frame.payload.decode("utf-8"), payload)

if __name__ == "__main__":
    unittest.main()
