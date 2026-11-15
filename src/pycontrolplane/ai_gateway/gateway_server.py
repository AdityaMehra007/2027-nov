import json
import time
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, Dict, Any
from .omniroute_engine import OmniRouteEngine
from .compressor import CompressionMode
from .guardrails import SecurityViolationException


class OmniRouteHTTPRequestHandler(BaseHTTPRequestHandler):
    """Zero-dependency HTTP handler compatible with standard OpenAI SDKs."""

    engine: Optional[OmniRouteEngine] = None

    def log_message(self, format: str, *args: Any) -> None:
        """Suppress standard HTTP server logging to stderr during normal test runs."""
        pass

    def _send_json(self, status_code: int, data: Dict[str, Any]) -> None:
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def do_GET(self) -> None:
        eng = self.engine or OmniRouteEngine()

        if self.path == "/health" or self.path == "/status":
            cooldown_count = sum(1 for ep in eng.endpoints.values() if ep.is_in_cooldown)
            self._send_json(200, {
                "status": "healthy",
                "service": "OmniRoute-Native-Gateway",
                "version": "1.0.0",
                "total_requests": eng.total_requests_served,
                "total_tokens_saved": eng.total_tokens_saved,
                "endpoints_count": len(eng.endpoints),
                "cooldown_endpoints": cooldown_count,
            })
            return

        if self.path == "/v1/models":
            models_data = []
            for name, ep in eng.endpoints.items():
                models_data.append({
                    "id": name,
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": ep.provider,
                    "tier": ep.tier.value,
                    "is_free": ep.is_free,
                    "is_available": not ep.is_in_cooldown,
                })
            self._send_json(200, {"object": "list", "data": models_data})
            return

        self._send_json(404, {"error": {"message": f"Endpoint not found: {self.path}", "code": 404}})

    def do_POST(self) -> None:
        eng = self.engine or OmniRouteEngine()

        if self.path == "/v1/chat/completions":
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length == 0:
                self._send_json(400, {"error": {"message": "Empty request body", "code": 400}})
                return

            try:
                raw_body = self.rfile.read(content_length).decode("utf-8")
                payload = json.loads(raw_body)
            except Exception as e:
                self._send_json(400, {"error": {"message": f"Malformed JSON: {str(e)}", "code": 400}})
                return

            messages = payload.get("messages", [])
            model = payload.get("model")
            mode_str = payload.get("compression_mode", "CAVEMAN").upper()
            try:
                mode = CompressionMode(mode_str)
            except ValueError:
                mode = CompressionMode.CAVEMAN

            try:
                result = eng.route_and_generate(
                    messages=messages,
                    model=model,
                    compression_mode=mode,
                )
                self._send_json(200, result)
            except SecurityViolationException as sve:
                self._send_json(400, {"error": {"message": str(sve), "type": "security_violation", "code": 400}})
            except Exception as exc:
                self._send_json(503, {"error": {"message": str(exc), "type": "routing_failure", "code": 503}})
            return

        self._send_json(404, {"error": {"message": f"Endpoint not found: {self.path}", "code": 404}})


class OmniRouteGatewayServer:
    """Threaded HTTP server running the OpenAI-compatible OmniRoute Gateway."""

    def __init__(self, host: str = "127.0.0.1", port: int = 4000, engine: Optional[OmniRouteEngine] = None):
        self.host = host
        self.port = port
        self.engine = engine or OmniRouteEngine()
        self.server: Optional[HTTPServer] = None
        self.thread: Optional[threading.Thread] = None

    def start(self, blocking: bool = False) -> None:
        handler = OmniRouteHTTPRequestHandler
        handler.engine = self.engine
        self.server = HTTPServer((self.host, self.port), handler)

        if blocking:
            print(f"[+] OmniRoute Native Gateway listening on http://{self.host}:{self.port}")
            self.server.serve_forever()
        else:
            self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
            self.thread.start()
            print(f"[+] OmniRoute Native Gateway started background thread on http://{self.host}:{self.port}")

    def stop(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=2.0)
            print("[*] OmniRoute Native Gateway stopped.")
