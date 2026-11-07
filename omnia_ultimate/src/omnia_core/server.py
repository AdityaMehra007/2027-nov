from __future__ import annotations
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from urllib.parse import urlparse
from .engine import WorkflowEngine

def make_handler(engine: WorkflowEngine):
    class Handler(BaseHTTPRequestHandler):
        server_version = "OMNIA-Local/0.1"

        def _send(self, status: int, body: dict):
            raw = json.dumps(body, ensure_ascii=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(raw)

        def _body(self):
            length = int(self.headers.get("Content-Length", "0"))
            if length > 1_000_000:
                raise ValueError("Request body too large")
            raw = self.rfile.read(length) if length else b"{}"
            data = json.loads(raw.decode("utf-8"))
            if not isinstance(data, dict):
                raise ValueError("JSON body must be an object")
            return data

        def log_message(self, fmt, *args):
            # Local prototype: standard request logs only. Do not log request bodies.
            super().log_message(fmt, *args)

        def do_GET(self):
            path = urlparse(self.path).path
            if path == "/healthz":
                return self._send(200, {"status": "ok", "service": "omnia-local-workflow-core"})
            if path == "/v1/tasks":
                return self._send(200, {"items": [t.to_dict() for t in engine.repo.list_tasks()]})
            if path == "/v1/audit/verify":
                from .audit import verify_chain
                events = engine.repo.events()
                return self._send(200, {"valid": verify_chain(events), "event_count": len(events)})
            if path == "/v1/audit/events":
                return self._send(200, {"items": engine.repo.events()})
            return self._send(404, {"error": "not_found"})

        def do_POST(self):
            try:
                path = urlparse(self.path).path
                body = self._body()
                if path == "/v1/tasks":
                    task = engine.create_task(
                        title=str(body.get("title", "")),
                        action=str(body.get("action", "")),
                        action_class=str(body.get("action_class", "draft")),
                        payload=body.get("payload", {}),
                        actor=str(body.get("actor", "local-user")),
                    )
                    return self._send(201, {"task": task.to_dict()})

                parts = [p for p in path.split("/") if p]
                if len(parts) == 4 and parts[:2] == ["v1", "tasks"]:
                    task_id, operation = parts[2], parts[3]
                    if operation == "request-approval":
                        approval = engine.request_approval(
                            task_id, str(body.get("requested_by", "local-user")),
                            str(body.get("reason", ""))
                        )
                        return self._send(201, {"approval": approval.to_dict()})
                    if operation == "approve":
                        approval = engine.decide_approval(
                            task_id, str(body.get("approval_id", "")),
                            str(body.get("approved_by", "")),
                            str(body.get("reason", "")), True
                        )
                        return self._send(200, {"approval": approval.to_dict()})
                    if operation == "reject":
                        approval = engine.decide_approval(
                            task_id, str(body.get("approval_id", "")),
                            str(body.get("decided_by", "local-user")),
                            str(body.get("reason", "")), False
                        )
                        return self._send(200, {"approval": approval.to_dict()})
                    if operation == "execute":
                        task = engine.execute(task_id, str(body.get("actor", "local-user")))
                        return self._send(200, {"task": task.to_dict()})
                    if operation == "cancel":
                        task = engine.cancel(task_id, str(body.get("actor", "local-user")))
                        return self._send(200, {"task": task.to_dict()})
                return self._send(404, {"error": "not_found"})
            except KeyError as exc:
                return self._send(404, {"error": "not_found", "detail": str(exc)})
            except PermissionError as exc:
                return self._send(403, {"error": "policy_denied", "detail": str(exc)})
            except (ValueError, TypeError, json.JSONDecodeError) as exc:
                return self._send(400, {"error": "bad_request", "detail": str(exc)})
            except Exception as exc:
                return self._send(500, {"error": "internal_error", "detail": type(exc).__name__})

        def do_OPTIONS(self):
            self.send_response(204)
            self.send_header("Allow", "GET, POST, OPTIONS")
            self.end_headers()

    return Handler

def serve(host: str = "127.0.0.1", port: int = 8765, db: str = "data/omnia.db"):
    if host not in ("127.0.0.1", "localhost", "::1"):
        raise SystemExit("Refusing non-loopback bind: this prototype has no authentication or TLS.")
    engine = WorkflowEngine()
    engine.repo = engine.repo.__class__(db)
    server = ThreadingHTTPServer((host, port), make_handler(engine))
    print(f"OMNIA local prototype listening on http://{host}:{port}")
    print("WARNING: unauthenticated local development server; do not expose publicly.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
