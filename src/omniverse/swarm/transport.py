"""Duplex WebSocket mesh transport layer for OmniSwarm."""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Awaitable, Callable
import websockets
from websockets.asyncio.server import Server
from omniverse.swarm.models import SwarmMessage

logger = logging.getLogger(__name__)


class MeshTransport:
    """Manages duplex WebSocket listener and peer connection pooling for node-to-node frames."""

    def __init__(
        self,
        local_node_id: str,
        host: str = "127.0.0.1",
        port: int = 9091,
    ) -> None:
        self.local_node_id = local_node_id
        self.host = host
        self.port = port

        self._inbound_handler: Callable[[SwarmMessage], Awaitable[None]] | None = None
        self._outbound_connections: dict[str, Any] = {}
        self._server: Server | None = None
        self._active_inbound_sockets: set[Any] = set()
        self._running = False

    def register_inbound_handler(
        self,
        handler: Callable[[SwarmMessage], Awaitable[None]],
    ) -> None:
        """Registers the callback invoked when a valid SwarmMessage frame is received."""
        self._inbound_handler = handler

    async def start_server(self) -> None:
        """Starts the inbound WebSocket server listener."""
        self._running = True
        self._server = await websockets.serve(
            self._handle_inbound_connection,
            self.host,
            self.port,
        )
        logger.info(
            "Swarm mesh transport listening at ws://%s:%d/ws/swarm",
            self.host,
            self.port,
        )

    async def _handle_inbound_connection(self, websocket: Any) -> None:
        """Processes inbound frames from a connected peer."""
        self._active_inbound_sockets.add(websocket)
        try:
            async for raw_frame in websocket:
                if not self._running:
                    break
                try:
                    if isinstance(raw_frame, bytes):
                        raw_frame = raw_frame.decode("utf-8")
                    data = json.loads(raw_frame)
                    message = SwarmMessage(**data)
                    if self._inbound_handler:
                        await self._inbound_handler(message)
                except Exception as exc:
                    logger.warning("Failed to decode inbound swarm frame: %s", exc)
        except Exception:
            pass
        finally:
            self._active_inbound_sockets.discard(websocket)

    async def connect_to_peer(self, peer_node_id: str, url: str) -> bool:
        """Establishes an outbound client WebSocket connection to a remote peer."""
        try:
            conn = await websockets.connect(url)
            self._outbound_connections[peer_node_id] = conn
            logger.info("Connected to peer node %s at %s", peer_node_id, url)
            return True
        except Exception as exc:
            logger.warning("Failed to connect to peer %s at %s: %s", peer_node_id, url, exc)
            return False

    async def send_frame(self, target_node_id: str, message: SwarmMessage) -> bool:
        """Sends a framed message to a target peer node over the connection pool."""
        conn = self._outbound_connections.get(target_node_id)
        if not conn:
            return False

        try:
            payload = message.model_dump_json()
            await conn.send(payload)
            return True
        except Exception as exc:
            logger.warning(
                "Failed to send frame to peer %s: %s. Evicting connection.",
                target_node_id,
                exc,
            )
            self._outbound_connections.pop(target_node_id, None)
            return False

    async def stop(self) -> None:
        """Shuts down server listener and terminates all active peer connections."""
        self._running = False

        # Close all outbound sockets
        for node_id, conn in list(self._outbound_connections.items()):
            try:
                await conn.close()
            except Exception:
                pass
        self._outbound_connections.clear()

        # Close all inbound sockets
        for sock in list(self._active_inbound_sockets):
            try:
                await sock.close()
            except Exception:
                pass
        self._active_inbound_sockets.clear()

        # Close server
        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
