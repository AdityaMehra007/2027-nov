import asyncio
import unittest
from pyweb.http import HTTPResponse
from pyweb.server import WebServer
from pyweb.websocket import build_websocket_frame, parse_websocket_frame

class TestPyWebIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.server = WebServer(host="127.0.0.1", port=0)

        @self.server.route("/api/ping", method="GET")
        async def handle_ping(req):
            return HTTPResponse.json({"pong": True})

        @self.server.websocket("/ws/echo")
        async def handle_ws(reader, writer):
            while not reader.at_eof():
                data = await reader.read(4096)
                if not data:
                    break
                frame = parse_websocket_frame(data)
                if frame:
                    # Echo back
                    reply = build_websocket_frame(frame.payload, opcode=frame.opcode)
                    writer.write(reply)
                    await writer.drain()

        await self.server.start()
        self.port = self.server.actual_port

    async def asyncTearDown(self):
        await self.server.stop()

    async def test_live_http_request(self):
        reader, writer = await asyncio.open_connection("127.0.0.1", self.port)
        http_raw = (
            f"GET /api/ping HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{self.port}\r\n"
            f"\r\n"
        ).encode("utf-8")
        writer.write(http_raw)
        await writer.drain()

        response_data = await reader.read(4096)
        self.assertTrue(response_data.startswith(b"HTTP/1.1 200 OK\r\n"))
        self.assertIn(b'{"pong": true}', response_data)

        writer.close()
        await writer.wait_closed()

    async def test_live_websocket_connection(self):
        reader, writer = await asyncio.open_connection("127.0.0.1", self.port)
        key = "dGhlIHNhbXBsZSBub25jZQ=="
        ws_req = (
            f"GET /ws/echo HTTP/1.1\r\n"
            f"Host: 127.0.0.1:{self.port}\r\n"
            f"Upgrade: websocket\r\n"
            f"Connection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            f"Sec-WebSocket-Version: 13\r\n\r\n"
        ).encode("utf-8")
        writer.write(ws_req)
        await writer.drain()

        handshake_resp = await reader.read(1024)
        self.assertTrue(handshake_resp.startswith(b"HTTP/1.1 101 Switching Protocols\r\n"))

        # Send a masked WebSocket text frame
        client_frame = build_websocket_frame("PyWeb Live Echo!", mask=True)
        writer.write(client_frame)
        await writer.drain()

        echo_data = await reader.read(1024)
        server_frame = parse_websocket_frame(echo_data)
        self.assertIsNotNone(server_frame)
        self.assertEqual(server_frame.payload.decode("utf-8"), "PyWeb Live Echo!")

        writer.close()
        await writer.wait_closed()

if __name__ == "__main__":
    unittest.main()
