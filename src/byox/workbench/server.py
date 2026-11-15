"""BYOX Interactive Visual Workbench Backend Server.
Wires together all 6 canonical engines: PyWeb, PyRedis, PyDB, PyGit, PyShell, and PyTransformer.
"""

from __future__ import annotations
import asyncio
import json
import logging
import os
import sys
import time
from typing import Any, Dict, List, Optional

# Import the 6 engines
from pyredis.commands import CommandDispatcher
from pyredis.store import DataStore
from pydb.engine import DatabaseEngine
from pygit.repository import find_repo, init_repo
from pygit.commands import cmd_log, cmd_status, cmd_branch
from pyshell.executor import ShellExecutor
from pytransformer.model import MiniTransformer
from pytransformer.tokenizer import CharacterTokenizer
from pyweb.http import HTTPRequest, HTTPResponse
from pyweb.server import WebServer
from pyweb.websocket import (
    WebSocketFrame,
    build_websocket_frame,
    parse_websocket_frame,
)
from byox.benchmarks.runner import run_all_benchmarks

logger = logging.getLogger("byox.workbench")


class WorkbenchServer:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 9000,
        db_path: str = "data/workbench.db",
        repo_path: str = ".",
    ) -> None:
        self.host = host
        self.port = port
        self.actual_port = port
        self.start_time = time.time()
        self.web = WebServer(host=host, port=port)

        # 1. PyRedis in-memory instance
        self.redis_store = DataStore()
        self.redis_dispatcher = CommandDispatcher(self.redis_store)

        # Prepopulate demo keys
        self.redis_store.set("system:status", "online")
        self.redis_store.set("session:demo_user", "active", ex_sec=3600)
        self.redis_store.hset("metrics:global", {"requests": "1420", "errors": "0"})
        self.redis_store.rpush("pipeline:jobs", "job_sync_ledger", "job_eval_model")

        # 2. PyDB relational database instance
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        self.db_engine = DatabaseEngine(db_path)
        if "metrics" not in self.db_engine.list_tables():
            self.db_engine.execute("CREATE TABLE metrics (id INT, service TEXT, latency_ms REAL);")
            self.db_engine.execute("INSERT INTO metrics VALUES (1, 'PyRedis', 1.86);")
            self.db_engine.execute("INSERT INTO metrics VALUES (2, 'PyDB', 0.10);")
            self.db_engine.execute("INSERT INTO metrics VALUES (3, 'PyWeb', 0.20);")

        # 3. PyGit repository instance
        self.repo = find_repo(repo_path)
        if not self.repo:
            self.repo = init_repo("data/workbench_git")

        # 4. PyShell executor instance
        self.shell = ShellExecutor()

        # 5. PyTransformer LLM instance
        corpus = (
            "The universe of software begins from first principles. "
            "Building systems from scratch gives mastery over computation. "
            "Code is poetry executed by silicon."
        )
        self.tokenizer = CharacterTokenizer(corpus)
        self.transformer = MiniTransformer(
            vocab_size=self.tokenizer.vocab_size,
            embed_dim=32,
            num_heads=4,
            context_len=24,
        )

        self._setup_routes()

    def _setup_routes(self) -> None:
        # Static HTML root
        @self.web.route("/", method="GET")
        async def serve_index(req: HTTPRequest) -> HTTPResponse:
            html_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
            if os.path.exists(html_path):
                with open(html_path, "r", encoding="utf-8") as f:
                    content = f.read()
                return HTTPResponse.html(content)
            return HTTPResponse.text("BYOX Workbench HTML not found", status_code=404)

        # API: Status Overview
        @self.web.route("/api/status", method="GET")
        async def api_status(req: HTTPRequest) -> HTTPResponse:
            redis_keys = len(self.redis_store.keys("*"))
            db_tables = self.db_engine.list_tables()
            git_branch = self.repo.current_branch() if self.repo else "none"

            return HTTPResponse.json(
                {
                    "status": "operational",
                    "uptime_sec": int(time.time() - self.start_time),
                    "engines": {
                        "pyredis": {"keys": redis_keys, "expiring": len(self.redis_store._expires)},
                        "pydb": {"tables": db_tables, "pages": self.db_engine.pager.num_pages()},
                        "pygit": {"branch": git_branch, "git_dir": self.repo.git_dir if self.repo else ""},
                        "pyshell": {"history_count": len(self.shell.history)},
                        "pyweb": {"port": self.web.actual_port},
                        "pytransformer": {
                            "vocab_size": self.tokenizer.vocab_size,
                            "embed_dim": self.transformer.embed_dim,
                            "context_len": self.transformer.context_len,
                        },
                    },
                }
            )

        # API: PyRedis Command Runner
        @self.web.route("/api/redis/command", method="POST")
        async def api_redis_command(req: HTTPRequest) -> HTTPResponse:
            try:
                data = json.loads(req.body.decode("utf-8"))
                cmd_line = data.get("command", "").strip()
                if not cmd_line:
                    return HTTPResponse.json({"error": "Empty command"}, status_code=400)

                parts = cmd_line.split()
                resp_bytes, is_mut = self.redis_dispatcher.dispatch(parts)
                # Decode RESP preview
                resp_preview = resp_bytes.decode("utf-8", errors="replace")
                return HTTPResponse.json({"raw_resp": resp_preview, "is_mutation": is_mut})
            except Exception as e:
                return HTTPResponse.json({"error": str(e)}, status_code=500)

        # API: PyRedis Keyspace
        @self.web.route("/api/redis/keys", method="GET")
        async def api_redis_keys(req: HTTPRequest) -> HTTPResponse:
            keys = self.redis_store.keys("*")
            items = []
            for k in keys:
                val = self.redis_store._data.get(k)
                ttl = self.redis_store.ttl(k)
                type_name = "string"
                if isinstance(val, dict):
                    type_name = "hash"
                elif hasattr(val, "popleft"):
                    type_name = "list"
                items.append({"key": k, "type": type_name, "ttl": ttl, "value": str(val)})
            return HTTPResponse.json({"keys": items})

        # API: PyDB Query Runner
        @self.web.route("/api/db/query", method="POST")
        async def api_db_query(req: HTTPRequest) -> HTTPResponse:
            try:
                data = json.loads(req.body.decode("utf-8"))
                sql = data.get("sql", "").strip()
                t0 = time.perf_counter()
                res = self.db_engine.execute(sql)
                duration_ms = round((time.perf_counter() - t0) * 1000.0, 3)

                return HTTPResponse.json(
                    {
                        "columns": res.columns,
                        "rows": res.rows,
                        "rows_affected": res.rows_affected,
                        "message": res.message,
                        "duration_ms": duration_ms,
                    }
                )
            except Exception as e:
                return HTTPResponse.json({"error": str(e)}, status_code=500)

        # API: PyGit Commit Graph
        @self.web.route("/api/git/graph", method="GET")
        async def api_git_graph(req: HTTPRequest) -> HTTPResponse:
            try:
                logs = cmd_log(self.repo, oneline=True, max_count=20) if self.repo else []
                branches_res = cmd_branch(self.repo) if self.repo else ([], "")
                branches = branches_res[0] if isinstance(branches_res, tuple) else branches_res
                status = cmd_status(self.repo) if self.repo else None
                return HTTPResponse.json(
                    {
                        "branch": self.repo.current_branch() if self.repo else "",
                        "branches": branches if isinstance(branches, list) else [branches],
                        "commits": [{"sha": sha, "message": msg} for sha, msg in logs],
                        "status": {
                            "staged": status.staged if status else [],
                            "modified": status.unstaged_modified if status else [],
                            "untracked": status.untracked if status else [],
                        },
                    }
                )
            except Exception as e:
                return HTTPResponse.json({"error": str(e)}, status_code=500)

        # API: Benchmarks Results
        @self.web.route("/api/benchmarks", method="GET")
        async def api_benchmarks(req: HTTPRequest) -> HTTPResponse:
            json_path = os.path.join("data", "byox_benchmark_results.json")
            if os.path.exists(json_path):
                with open(json_path, "r", encoding="utf-8") as f:
                    bench_data = json.load(f)
                return HTTPResponse.json(bench_data)
            return HTTPResponse.json({"results": [], "message": "No benchmarks executed yet"})

        # WebSocket: Interactive PyShell Terminal
        @self.web.websocket("/ws/shell")
        async def ws_shell(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            welcome = (
                "\033[36mConnected to PyShell WebSocket Bridge\033[0m\r\n"
                "Type commands like 'echo hello', 'pwd', or 'export VAR=value'.\r\n\r\n$ "
            )
            writer.write(build_websocket_frame(welcome))
            await writer.drain()

            while not reader.at_eof():
                data = await reader.read(4096)
                if not data:
                    break
                frame = parse_websocket_frame(data)
                if frame:
                    cmd_line = frame.payload.decode("utf-8", errors="replace").strip()
                    if cmd_line:
                        output = self.shell.run_line(cmd_line)
                        prompt = f"\r\n{output}\r\n$ "
                    else:
                        prompt = "$ "
                    writer.write(build_websocket_frame(prompt))
                    await writer.drain()

        # WebSocket: Streaming PyTransformer Text Generation
        @self.web.websocket("/ws/llm")
        async def ws_llm(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
            while not reader.at_eof():
                data = await reader.read(4096)
                if not data:
                    break
                frame = parse_websocket_frame(data)
                if frame:
                    try:
                        payload = json.loads(frame.payload.decode("utf-8"))
                        prompt = payload.get("prompt", "The")
                        num_tokens = min(int(payload.get("tokens", 10)), 30)

                        input_ids = self.tokenizer.encode(prompt)
                        curr_tokens = list(input_ids)

                        # Stream tokens one by one
                        for _ in range(num_tokens):
                            logits = self.transformer.forward(curr_tokens)
                            last = logits[-1]
                            best_id = 0
                            best_val = last[0].data
                            for i in range(1, len(last)):
                                if last[i].data > best_val:
                                    best_val = last[i].data
                                    best_id = i
                            curr_tokens.append(best_id)
                            char_generated = self.tokenizer.decode([best_id])

                            chunk = json.dumps({"token": char_generated, "done": False})
                            writer.write(build_websocket_frame(chunk))
                            await writer.drain()
                            await asyncio.sleep(0.05)

                        writer.write(build_websocket_frame(json.dumps({"token": "", "done": True})))
                        await writer.drain()
                    except Exception as e:
                        err = json.dumps({"error": str(e), "done": True})
                        writer.write(build_websocket_frame(err))
                        await writer.drain()

    async def start(self) -> asyncio.Server:
        self.redis_store.start_active_expiration(interval_sec=0.1)
        srv = await self.web.start()
        self.actual_port = self.web.actual_port
        return srv

    async def stop(self) -> None:
        self.close()
        await self.web.stop()

    def close(self) -> None:
        self.redis_store.stop_active_expiration()
        self.db_engine.close()
