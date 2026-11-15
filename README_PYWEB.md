# PyWeb: Async HTTP/1.1 & WebSocket Server from Scratch in Python

A high-concurrency, zero-dependency async web server and RFC 6455 WebSocket engine built with Python 3.13 standard library (`asyncio`).

---

## Features

- **HTTP/1.1 Streaming Parser:** Parses request lines, URL paths, query parameters, headers, and payload bodies.
- **RFC 6455 WebSocket Support:**
  - Handshake negotiation with SHA-1 + base64 `Sec-WebSocket-Accept` computation.
  - Frame framing and parsing: FIN bit, opcodes (Text, Binary, Ping, Pong, Close), variable length encoding, and XOR client payload unmasking.
- **Route Decorators:** Simple `@server.route(path, method)` and `@server.websocket(path)` registration.
- **Native JSON & HTML Utilities:** `HTTPResponse.json()`, `HTTPResponse.html()`, `HTTPResponse.text()`.

---

## Quickstart Usage

```python
import asyncio
from pyweb.server import WebServer
from pyweb.http import HTTPResponse
from pyweb.websocket import build_websocket_frame, parse_websocket_frame

app = WebServer(host="127.0.0.1", port=8080)

@app.route("/api/hello", method="GET")
async def hello(req):
    name = req.query_params.get("name", "World")
    return HTTPResponse.json({"message": f"Hello, {name}!"})

@app.websocket("/ws/chat")
async def chat(reader, writer):
    while not reader.at_eof():
        data = await reader.read(4096)
        if not data:
            break
        frame = parse_websocket_frame(data)
        if frame:
            reply = build_websocket_frame(f"Echo: {frame.payload.decode('utf-8')}")
            writer.write(reply)
            await writer.drain()

if __name__ == "__main__":
    asyncio.run(app.start())
```

---

## Running Tests

```bash
python -m unittest tests/test_pyweb.py tests/test_pyweb_integration.py
```
```
......
----------------------------------------------------------------------
Ran 6 tests in 4.823s

OK
```
