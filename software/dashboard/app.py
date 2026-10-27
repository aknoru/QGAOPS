"""Minimal dependency-free dashboard backend using Python's standard library."""

from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
import json
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]


def dashboard_payload() -> dict:
    benchmark = ROOT / "results/raw/stage6_cpu_benchmark.json"
    gesture = ROOT / "results/processed/gesture_fixture_result.json"
    return {
        "software_only": True,
        "hardware_status": "not integrated; no FPGA measurements available",
        "benchmark": json.loads(benchmark.read_text()) if benchmark.exists() else None,
        "gesture": json.loads(gesture.read_text()) if gesture.exists() else None,
    }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route = urlparse(self.path).path
        if route == "/api/status":
            body = json.dumps(dashboard_payload()).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
        elif route == "/":
            body = b"<html><body><h1>QGAOPS-QGPU software-only dashboard</h1><p>Hardware not integrated.</p><pre id='data'></pre><script>fetch('/api/status').then(r=>r.json()).then(x=>document.getElementById('data').textContent=JSON.stringify(x,null,2))</script></body></html>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
        else:
            self.send_error(404)
            return
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def serve(host="127.0.0.1", port=8000):
    HTTPServer((host, port), Handler).serve_forever()


if __name__ == "__main__":
    serve()
