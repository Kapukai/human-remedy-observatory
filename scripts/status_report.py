#!/usr/bin/env python3
"""Print a small research status report suitable for pasting into a support conversation."""
import collections
import hashlib
import json
import platform
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def report():
    data_path = ROOT / "data/curated/cases.json"
    cases = json.loads(data_path.read_text(encoding="utf-8"))
    included = [c for c in cases if c["plaintiff"] != "Organization comparator"]
    try:
        revision = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = "not a Git checkout"
    registry_path = ROOT / "data/research/dashboard-registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else []
    manifest = json.loads((ROOT / "data/sources/scdb-source-manifest.json").read_text(encoding="utf-8"))
    return {
        "project": "human-remedy-observatory",
        "revision": revision,
        "python": platform.python_version(),
        "case_data_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
        "total_families": len(cases),
        "default_included_families": len(included),
        "workbench_default_us_families": sum(c["country"] == "US" for c in included),
        "identified_habeas_families": sum(bool(c.get("habeas_vehicle")) for c in included),
        "sector_counts": dict(collections.Counter(c["sector"] for c in included)),
        "direction_counts": dict(collections.Counter(c["direction"] for c in included)),
        "registered_views": len(registry),
        "view_readiness": dict(collections.Counter(v["status"] for v in registry)),
        "workbench_files_present": all((ROOT / p).is_file() for p in ["web/index.html", "web/app.js", "web/styles.css"]),
        "scdb_raw_files_present": {d["release"]: (ROOT / "data/raw/scdb" / d["csv_filename"]).is_file() for d in manifest["datasets"]},
        "interpretation": "Selected historical atlas; not a representative sample, completed hypothesis test, or causal estimate."
    }


if __name__ == "__main__":
    print(json.dumps(report(), indent=2, ensure_ascii=False))
