"""Regression checks for the research denominator and local server boundary."""
import functools
import importlib.util
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


server_module = module("serve_workbench")
check_module = module("check_data")


class WorkbenchChecks(unittest.TestCase):
    def test_frozen_data_reconciles(self):
        self.assertEqual(check_module.validate(), [])

    def test_public_resource_boundary(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "web").mkdir()
            (root / "web/index.html").write_text("public", encoding="utf-8")
            (root / "private.txt").write_text("private", encoding="utf-8")
            (root / "web/leak.txt").symlink_to(root / "private.txt")
            self.assertEqual(server_module.allowed_path("/web/?view=atlas", root), root / "web/index.html")
            for path in ["/.git/config", "/.env", "/private.txt", "/web/../private.txt", "/web/%2e%2e/private.txt", "/web/leak.txt", "/web/%00"]:
                with self.subTest(path=path):
                    self.assertIsNone(server_module.allowed_path(path, root))

    def test_http_serves_app_and_data_but_not_checkout_metadata(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(server_module.WorkbenchHandler, root=ROOT))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = "http://127.0.0.1:%s" % server.server_port
        try:
            with urlopen(base + "/", timeout=5) as response:
                self.assertTrue(response.url.endswith("/web/"))
                self.assertIn("text/html", response.headers["Content-Type"])
            for path in ["/web/app.js", "/web/styles.css", "/web/analysis.js", "/data/research/dashboard-registry.json", "/data/research/interventions.json"]:
                with urlopen(base + path, timeout=5) as response:
                    self.assertEqual(response.status, 200)
                    self.assertTrue(response.read())
                    self.assertIn("default-src 'self'", response.headers["Content-Security-Policy"])
            with urlopen(base + "/data/curated/cases.json", timeout=5) as response:
                self.assertEqual(len(json.load(response)), 63)
            for path in ["/.git/config", "/data/raw/scdb/", "/web/%2e%2e/README.md", "/scripts/status_report.py"]:
                with self.subTest(path=path), self.assertRaises(HTTPError) as caught:
                    urlopen(base + path, timeout=5)
                self.assertEqual(caught.exception.code, 404)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
