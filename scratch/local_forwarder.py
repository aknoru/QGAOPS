import sys
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

LOCAL_PORT = 8080
TARGET_HOSTS = ["http://10.51.10.38:8080", "http://192.168.0.221:8080", "http://192.168.0.220:8080", "http://192.168.3.1:8080"]
if len(sys.argv) > 1:
    TARGET_HOSTS.insert(0, sys.argv[1] if sys.argv[1].startswith("http") else f"http://{sys.argv[1]}")

class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, format, *args):
        pass

    def do_proxy(self):
        try:
            body = None
            if "Content-Length" in self.headers:
                length = int(self.headers["Content-Length"])
                body = self.rfile.read(length)

            resp = None
            for host in TARGET_HOSTS:
                try:
                    url = f"{host}{self.path}"
                    resp = requests.request(
                        method=self.command,
                        url=url,
                        data=body,
                        headers={k: v for k, v in self.headers.items() if k.lower() not in ["host", "content-length"]},
                        timeout=30
                    )
                    break
                except Exception:
                    continue

            if resp is None:
                self.send_error(502, "Board unreachable")
                return

            self.send_response(resp.status_code)
            for k, v in resp.headers.items():
                if k.lower() not in ["transfer-encoding", "content-encoding", "content-length", "connection"]:
                    self.send_header(k, v)
            self.send_header("Content-Length", str(len(resp.content)))
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(resp.content)
            self.wfile.flush()
        except Exception as e:
            print("Proxy error:", e)

    do_GET = do_proxy
    do_POST = do_proxy

def main():
    server = HTTPServer(("127.0.0.1", LOCAL_PORT), ProxyHandler)
    print(f"Proxy active: http://localhost:{LOCAL_PORT} -> {TARGET_HOSTS[0]}")
    sys.stdout.flush()
    server.serve_forever()

if __name__ == "__main__":
    main()
