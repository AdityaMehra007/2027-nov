"""High-concurrency asyncio HTTP/1.1 and WebSocket server."""

from __future__ import annotations
import asyncio
import logging
from typing import Callable, Coroutine, Dict, Optional, Tuple
from pyweb.http import HTTPRequest, HTTPResponse, parse_http_request
from pyweb.websocket import (
    OPCODE_CLOSE,
    OPCODE_PING,
    OPCODE_PONG,
    OPCODE_TEXT,
    WebSocketFrame,
    build_websocket_frame,
    compute_accept_key,
    parse_websocket_frame,
)

logger = logging.getLogger("pyweb.server")

Handler = Callable[[HTTPRequest], Coroutine[None, None, HTTPResponse]]
WSHandler = Callable[[asyncio.StreamReader, asyncio.StreamWriter], Coroutine[None, None, None]]


class WebServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8080) -> None:
        self.host = host
        self.port = port
        self.actual_port = port
        self.routes: Dict[Tuple[str, str], Handler] = {}
        self.ws_routes: Dict[str, WSHandler] = {}
        self._server: Optional[asyncio.Server] = None

    def route(self, path: str, method: str = "GET"):
        def decorator(fn: Handler):
            self.routes[(method.upper(), path)] = fn
            return fn
        return decorator

    def websocket(self, path: str):
        def decorator(fn: WSHandler):
            self.ws_routes[path] = fn
            return fn
        return decorator

    async def start(self) -> asyncio.Server:
        self._server = await asyncio.start_server(
            self._handle_connection,
            host=self.host,
            port=self.port,
        )
        if self._server.sockets:
            self.actual_port = self._server.sockets[0].getsockname()[1]
        logger.info("PyWeb server listening on %s:%d", self.host, self.actual_port)
        return self._server

    async def stop(self) -> None:
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._server = None

    async def _handle_connection(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        try:
            raw_data = await reader.read(8192)
            if not raw_data:
                return

            req = parse_http_request(raw_data)
            if not req:
                resp = HTTPResponse.text("Bad Request", status_code=400)
                writer.write(resp.serialize())
                await writer.drain()
                return

            # Check if WebSocket upgrade
            upgrade_header = req.headers.get("upgrade", "").lower()
            if upgrade_header == "websocket" and req.path in self.ws_routes:
                sec_key = req.headers.get("sec-websocket-key")
                if sec_key:
                    accept_key = compute_accept_key(sec_key)
                    handshake = (
                        b"HTTP/1.1 101 Switching Protocols\r\n"
                        b"Upgrade: websocket\r\n"
                        b"Connection: Upgrade\r\n"
                        b"Sec-WebSocket-Accept: " + accept_key.encode("utf-8") + b"\r\n\r\n"
                    )
                    writer.write(handshake)
                    await writer.drain()

                    # Hand over to WS handler
                    await self.ws_routes[req.path](reader, writer)
                    return

            # Standard HTTP route dispatch
            handler = self.routes.get((req.method, req.path))
            if handler:
                resp = await handler(req)
            else:
                resp = HTTPResponse.json({"error": "Not Found", "path": req.path}, status_code=404)

            writer.write(resp.serialize())
            await writer.drain()

        except Exception as e:
            logger.debug("Connection error: %s", e)
        finally:
            try:
                writer.close()
            except Exception:
                pass
