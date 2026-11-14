import asyncio
import os
import tempfile
import unittest
from pyredis.server import RedisServer

class TestServerIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.aof_path = os.path.join(self.temp_dir.name, "server_test.aof")
        # Use port 0 to let OS bind to an available port
        self.server = RedisServer(host="127.0.0.1", port=0, aof_filepath=self.aof_path)
        await self.server.start()
        # Retrieve actual bound port
        self.port = self.server.actual_port

    async def asyncTearDown(self):
        await self.server.stop()
        self.temp_dir.cleanup()

    async def test_single_client_command_and_response(self):
        reader, writer = await asyncio.open_connection("127.0.0.1", self.port)

        # Send PING
        writer.write(b"*1\r\n$4\r\nPING\r\n")
        await writer.drain()
        resp = await reader.read(1024)
        self.assertEqual(resp, b"+PONG\r\n")

        # Send SET and GET
        writer.write(b"*3\r\n$3\r\nSET\r\n$4\r\ncity\r\n$5\r\nTokyo\r\n")
        await writer.drain()
        resp = await reader.read(1024)
        self.assertEqual(resp, b"+OK\r\n")

        writer.write(b"*2\r\n$3\r\nGET\r\n$4\r\ncity\r\n")
        await writer.drain()
        resp = await reader.read(1024)
        self.assertEqual(resp, b"$5\r\nTokyo\r\n")

        writer.close()
        await writer.wait_closed()

    async def test_pipelining(self):
        reader, writer = await asyncio.open_connection("127.0.0.1", self.port)

        # Pipeline 3 commands in a single TCP write
        pipelined_payload = (
            b"*3\r\n$3\r\nSET\r\n$1\r\na\r\n$1\r\n1\r\n"
            b"*3\r\n$3\r\nSET\r\n$1\r\nb\r\n$1\r\n2\r\n"
            b"*2\r\n$3\r\nGET\r\n$1\r\na\r\n"
        )
        writer.write(pipelined_payload)
        await writer.drain()

        # Read back until all 3 responses arrive
        collected = bytearray()
        while len(collected) < len(b"+OK\r\n+OK\r\n$1\r\n1\r\n"):
            chunk = await reader.read(1024)
            if not chunk:
                break
            collected.extend(chunk)

        self.assertEqual(bytes(collected), b"+OK\r\n+OK\r\n$1\r\n1\r\n")

        writer.close()
        await writer.wait_closed()

    async def test_concurrent_clients(self):
        async def client_worker(client_id: int):
            r, w = await asyncio.open_connection("127.0.0.1", self.port)
            key = f"client:{client_id}"
            val = f"val:{client_id}"

            # SET
            w.write(f"*3\r\n$3\r\nSET\r\n${len(key)}\r\n{key}\r\n${len(val)}\r\n{val}\r\n".encode())
            await w.drain()
            resp = await r.read(1024)
            self.assertEqual(resp, b"+OK\r\n")

            # GET
            w.write(f"*2\r\n$3\r\nGET\r\n${len(key)}\r\n{key}\r\n".encode())
            await w.drain()
            resp = await r.read(1024)
            self.assertEqual(resp, f"${len(val)}\r\n{val}\r\n".encode())

            w.close()
            await w.wait_closed()

        # Run 10 clients concurrently
        tasks = [client_worker(i) for i in range(10)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    unittest.main()
