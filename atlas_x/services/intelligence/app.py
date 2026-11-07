from __future__ import annotations
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from atlas_intelligence import DeterministicProvider, JobAnalysisRequest

PROVIDER = DeterministicProvider()
MAX_BODY = 128 * 1024

class Handler(BaseHTTPRequestHandler):
    server_version = "ATLAS-Intelligence/0.1"

    def _send(self, status: int, data: dict) -> None:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        if self.path == "/healthz":
            self._send(200, {"status": "ok", "engine": "deterministic-keyword-baseline"})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/v1/job-analysis":
            self._send(404, {"error": "not found"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self._send(400, {"error": "invalid content length"})
            return
        if length <= 0 or length > MAX_BODY:
            self._send(413, {"error": "body missing or too large"})
            return
        try:
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("body must be an object")
            title = payload.get("job_title", "")
            description = payload.get("job_description", "")
            proof = payload.get("profile_evidence", [])
            if not isinstance(title, str) or not isinstance(description, str) or not isinstance(proof, list):
                raise ValueError("invalid field types")
            if len(title) > 200 or len(description) > 25_000 or len(proof) > 100:
                raise ValueError("field limit exceeded")
            if any(not isinstance(x, str) or len(x) > 2_000 for x in proof):
                raise ValueError("profile_evidence must contain short strings")
            request = JobAnalysisRequest(title, description, tuple(proof))
            result = PROVIDER.analyze_job(request)
            self._send(200, {
                "engine": result.engine,
                "job_title": result.job_title,
                "extracted_requirements": list(result.extracted_requirements),
                "evidence_map": [
                    {"skill": x.skill, "matched": x.matched, "evidence": list(x.evidence)}
                    for x in result.evidence_map
                ],
                "unsupported_requirements": list(result.unsupported_requirements),
                "disclaimer": result.disclaimer,
            })
        except (json.JSONDecodeError, ValueError) as exc:
            self._send(400, {"error": str(exc)})
        except Exception:
            self._send(500, {"error": "internal analysis error"})

    def log_message(self, fmt: str, *args) -> None:
        print("ATLAS intelligence:", fmt % args)

if __name__ == "__main__":
    host = os.getenv("ATLAS_INTELLIGENCE_HOST", "127.0.0.1")
    port = int(os.getenv("ATLAS_INTELLIGENCE_PORT", "8090"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"ATLAS intelligence listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
