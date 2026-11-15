"""HTTP/1.1 Request and Response models and streaming parser."""

from __future__ import annotations
from dataclasses import dataclass, field
import json
from typing import Any, Dict, Optional
import urllib.parse

STATUS_TEXTS = {
    200: "OK",
    201: "Created",
    204: "No Content",
    400: "Bad Request",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
    101: "Switching Protocols",
}


@dataclass
class HTTPRequest:
    method: str
    path: str
    query_params: Dict[str, str] = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)
    body: bytes = b""


@dataclass
class HTTPResponse:
    status_code: int = 200
    status_text: str = "OK"
    headers: Dict[str, str] = field(default_factory=dict)
    body: bytes = b""

    def serialize(self) -> bytes:
        status_text = self.status_text or STATUS_TEXTS.get(self.status_code, "Unknown")
        headers = dict(self.headers)
        if "Content-Length" not in headers:
            headers["Content-Length"] = str(len(self.body))

        lines = [f"HTTP/1.1 {self.status_code} {status_text}"]
        for k, v in headers.items():
            lines.append(f"{k}: {v}")
        lines.append("")
        lines.append("")

        header_bytes = "\r\n".join(lines[:-1]).encode("latin1") + b"\r\n"
        return header_bytes + self.body

    @classmethod
    def text(cls, text_content: str, status_code: int = 200) -> HTTPResponse:
        data = text_content.encode("utf-8")
        return cls(
            status_code=status_code,
            headers={"Content-Type": "text/plain; charset=utf-8"},
            body=data,
        )

    @classmethod
    def html(cls, html_content: str, status_code: int = 200) -> HTTPResponse:
        data = html_content.encode("utf-8")
        return cls(
            status_code=status_code,
            headers={"Content-Type": "text/html; charset=utf-8"},
            body=data,
        )

    @classmethod
    def json(cls, data_dict: Any, status_code: int = 200) -> HTTPResponse:
        payload = json.dumps(data_dict).encode("utf-8")
        return cls(
            status_code=status_code,
            headers={"Content-Type": "application/json"},
            body=payload,
        )


def parse_http_request(raw: bytes) -> Optional[HTTPRequest]:
    header_end = raw.find(b"\r\n\r\n")
    if header_end == -1:
        return None

    header_bytes = raw[:header_end]
    body = raw[header_end + 4 :]

    lines = header_bytes.decode("latin1").split("\r\n")
    if not lines or not lines[0]:
        return None

    # Request Line
    parts = lines[0].split(" ")
    if len(parts) < 2:
        return None

    method = parts[0].upper()
    full_url = parts[1]

    # Split query parameters
    url_parts = urllib.parse.urlsplit(full_url)
    path = url_parts.path
    query_params = dict(urllib.parse.parse_qsl(url_parts.query))

    # Headers
    headers: Dict[str, str] = {}
    for line in lines[1:]:
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    # Verify content length
    content_len = int(headers.get("content-length", 0))
    if len(body) > content_len:
        body = body[:content_len]

    return HTTPRequest(
        method=method,
        path=path,
        query_params=query_params,
        headers=headers,
        body=body,
    )
