#!/usr/bin/env python3
"""Serve the research workbench on this computer using only Python's stdlib."""
import argparse
import functools
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PREFIXES = ("web", "data/curated", "data/research", "reports", "docs", "methods", "schemas", "templates")
PUBLIC_FILES = {"README.md", "RESEARCH_GUIDE.md", "SCDB_DATA.md", "LICENSE", "LICENSE-DATA.md", "CONTRIBUTING.md"}


def allowed_path(raw_path, root=ROOT):
    """Return a public existing file; reject dot paths, traversal, and symlink escapes."""
    path = unquote(urlsplit(raw_path).path)
    parts = path.strip("/").split("/")
    if any(part.startswith(".") or "\\" in part or "\x00" in part for part in parts):
        return None
    relative = "/".join(parts)
    if relative not in PUBLIC_FILES and not any(relative == p or relative.startswith(p + "/") for p in PUBLIC_PREFIXES):
        return None
    target = root.joinpath(*parts).resolve()
    if target.is_dir():
        target = target / "index.html"
    try:
        resolved_relative = target.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None
    if any(part.startswith(".") for part in Path(resolved_relative).parts):
        return None
    if resolved_relative not in PUBLIC_FILES and not any(resolved_relative.startswith(p + "/") for p in PUBLIC_PREFIXES):
        return None
    return target if target.is_file() else None


class WorkbenchHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, root=ROOT, **kwargs):
        self.root = root.resolve()
        super().__init__(*args, directory=str(self.root), **kwargs)

    def send_head(self):
        if urlsplit(self.path).path == "/":
            self.send_response(302)
            self.send_header("Location", "/web/")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return None
        target = allowed_path(self.path, self.root)
        if target is None:
            self.send_error(404, "Not a published workbench resource")
            return None
        handle = target.open("rb")
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(str(target)))
        self.send_header("Content-Length", str(target.stat().st_size))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self'; object-src 'none'; base-uri 'self'; frame-ancestors 'none'")
        self.end_headers()
        return handle

    def log_message(self, format, *args):
        # Deliberately omit URLs and query strings from routine terminal output.
        return


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-open", action="store_true", help="Do not automatically open a browser tab")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    required = [ROOT / "web/index.html", ROOT / "data/curated/cases.json"]
    if not all(p.is_file() for p in required):
        parser.error("workbench files are missing; run git pull --ff-only from the repository")
    try:
        server = ThreadingHTTPServer(("127.0.0.1", args.port), functools.partial(WorkbenchHandler, root=ROOT))
    except OSError as error:
        parser.exit(1, "Cannot open the local port: %s\nTry --port 8766.\n" % error)
    address = "http://127.0.0.1:%s/" % args.port
    print("Human Remedy Observatory: " + address, flush=True)
    print("Local research snapshot. Press Control-C to stop.", flush=True)
    if not args.no_open:
        timer = threading.Timer(0.4, webbrowser.open, args=(address,))
        timer.daemon = True
        timer.start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nWorkbench stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
