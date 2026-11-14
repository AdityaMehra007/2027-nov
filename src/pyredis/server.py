"""Asyncio TCP Socket Server for Redis Clone."""

from __future__ import annotations
import asyncio
import logging
from typing import Optional, Set
from pyredis.commands import CommandDispatcher
from pyredis.persistence import AOFEngine
from pyredis.protocol import RESPParser
from pyredis.store import DataStore

logger = logging.getLogger("pyredis.server")


class RedisServer:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 6379,
        aof_filepath: Optional[str] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.aof_filepath = aof_filepath
        self.store = DataStore()
        self.dispatcher = CommandDispatcher(self.store)
        self.aof: Optional[AOFEngine] = None
        if aof_filepath:
            self.aof = AOFEngine(aof_filepath, self.store, self.dispatcher)

        self._server: Optional[asyncio.Server] = None
        self._active_writers: Set[asyncio.StreamWriter] = set()
        self.actual_port = port

    async def start(self) -> asyncio.Server:
        """Starts the Redis server: replays AOF, launches TTL sweep, and begins TCP listening."""
        if self.aof:
            replayed = self.aof.replay()
            logger.info("Replayed %d commands from AOF log (%s)", replayed, self.aof_filepath)

        # Start active background expiration sweep
        self.store.start_active_expiration(interval_sec=0.1)

        self._server = await asyncio.start_server(
            self._handle_client,
            host=self.host,
            port=self.port,
        )

        sockets = self._server.sockets
        if sockets:
            self.actual_port = sockets[0].getsockname()[1]
        logger.info("PyRedis server listening on %s:%d", self.host, self.actual_port)
        return self._server

    async def stop(self) -> None:
        """Stops the server gracefully, cleans up active connections, and flushes AOF."""
        self.store.stop_active_expiration()

        if self._server:
            self._server.close()
            await self._server.wait_closed()
            self._server = None

        # Close all active client connections
        for writer in list(self._active_writers):
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        self._active_writers.clear()

        if self.aof:
            self.aof.close()
            self.aof = None

    async def _handle_client(
        self,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
    ) -> None:
        self._active_writers.add(writer)
        parser = RESPParser()

        try:
            while not reader.at_eof():
                chunk = await reader.read(4096)
                if not chunk:
                    break

                parser.feed(chunk)

                # Process all completely framed commands (handles pipelining)
                while True:
                    cmd_obj = parser.get_next_object()
                    if cmd_obj is None:
                        break

                    if isinstance(cmd_obj, list):
                        resp_bytes, is_mutation = self.dispatcher.dispatch(cmd_obj)
                        if is_mutation and self.aof:
                            self.aof.append(cmd_obj)

                        writer.write(resp_bytes)
                        await writer.drain()
                    else:
                        # Non-array command or raw payload
                        pass
        except (ConnectionResetError, BrokenPipeError):
            pass
        except Exception as e:
            logger.debug("Error handling client connection: %s", e)
        finally:
            self._active_writers.discard(writer)
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
