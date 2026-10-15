"""Local-only preview of public-html, with a real HTTP 404 and root-safe assets."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse

PUBLIC = Path(__file__).resolve().parents[1] / "public-html"


class PublicHandler(SimpleHTTPRequestHandler):
    def send_head(self):
        if not Path(self.translate_path(self.path)).resolve().is_relative_to(PUBLIC.resolve()):
            self.send_error(404)
            return None
        return super().send_head()

    def send_error(self, code, message=None, explain=None):
        page = PUBLIC / "404.html"
        if code == 404 and page.is_file():
            body = page.read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)
        else:
            super().send_error(code, message, explain)

    def list_directory(self, path):
        self.send_error(404)
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()
    handler = partial(PublicHandler, directory=str(PUBLIC))
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
        print(f"Alejandría local: http://127.0.0.1:{args.port}/ (Ctrl+C para detener)", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
