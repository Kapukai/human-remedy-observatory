#!/usr/bin/env python3
"""Validate source provenance and linked research records without downloading or modifying data."""
import argparse
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def validate(root=ROOT):
    errors = []
    data = root / "data/curated/cases.json"
    cases = json.loads(data.read_text(encoding="utf-8"))
    summary = json.loads((root / "reports/atlas/summary.json").read_text(encoding="utf-8"))
    ids = [c.get("id") for c in cases]
    if not all(ids) or len(ids) != len(set(ids)):
        errors.append("Case family identifiers are missing or duplicated")
    for c in cases:
        for key in ["name", "country", "sector", "technology", "direction", "stage", "implementation", "summary", "limit", "sources", "tags", "plaintiff", "system_group"]:
            if key not in c:
                errors.append("%s: missing %s" % (c.get("id"), key))
        if c.get("sector") not in {"Public", "Private", "Mixed"}:
            errors.append("%s: invalid sector" % c.get("id"))
        if c.get("direction") not in {"Favorable", "Mixed", "Adverse"}:
            errors.append("%s: invalid direction" % c.get("id"))
        if c.get("included_by_default") != (c.get("plaintiff") != "Organization comparator"):
            errors.append("%s: comparator inclusion mismatch" % c.get("id"))
        if not c.get("sources") or any(not s.get("url", "").startswith("https://") for s in c.get("sources", [])):
            errors.append("%s: missing HTTPS source provenance" % c.get("id"))
    included = [c for c in cases if c.get("plaintiff") != "Organization comparator"]
    if summary.get("source_sha256") != hashlib.sha256(data.read_bytes()).hexdigest():
        errors.append("Atlas summary source hash differs from the shipped case dataset")
    if summary.get("default_included") != len(included) or summary.get("total_records") != len(cases):
        errors.append("Atlas summary family counts differ from case data")
    for field in ["sector", "direction", "stage", "technology", "implementation"]:
        if dict(collections.Counter(c.get(field) for c in included)) != summary.get(field + "_counts"):
            errors.append("Atlas summary %s counts differ from case data" % field)
    with (root / "data/curated/cases.csv").open(encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    if {r["id"] for r in csv_rows} != set(ids) or len(csv_rows) != len(cases):
        errors.append("CSV and JSON family identifiers differ")
    csv_map = {r["id"]: r for r in csv_rows}
    for c in cases:
        for key in ["sector", "direction", "stage", "technology", "implementation"]:
            if csv_map.get(c["id"], {}).get(key) != c[key]:
                errors.append("%s: CSV/JSON %s mismatch" % (c["id"], key))
    registry_path = root / "data/research/dashboard-registry.json"
    if not registry_path.exists():
        errors.append("Dashboard registry is missing")
    else:
        views = json.loads(registry_path.read_text(encoding="utf-8"))
        if sorted(v["rank"] for v in views) != list(range(1, 26)) or len({v["id"] for v in views}) != 25:
            errors.append("Dashboard registry must contain 25 uniquely ranked views")
        if any(v["status"] not in {"available", "needs-data", "design-only"} for v in views):
            errors.append("Dashboard registry has an unknown readiness state")
    intervention_path = root / "data/research/interventions.json"
    if not intervention_path.exists():
        errors.append("Proposed intervention records are missing")
    else:
        interventions = json.loads(intervention_path.read_text(encoding="utf-8"))
        if sorted(i["id"] for i in interventions) != ["H1", "H2", "H3", "H4"]:
            errors.append("Intervention records must contain H1 through H4 exactly once")
        for intervention in interventions:
            if intervention.get("status") != "Proposed; untested":
                errors.append("Intervention status must preserve its untested designation")
            if not intervention.get("guardrails") or not intervention.get("sources"):
                errors.append("Intervention safeguards or sources are missing")
    source_summary = json.loads((root / "reports/scdb/summary.json").read_text(encoding="utf-8"))
    manifest = json.loads((root / "data/sources/scdb-source-manifest.json").read_text(encoding="utf-8"))
    if source_summary["source_case_count"] != sum(d["row_count"] for d in manifest["datasets"]):
        errors.append("SCDB coverage and acquisition manifest totals differ")
    with (root / "reports/scdb/coverage_by_term.csv").open(encoding="utf-8", newline="") as handle:
        total = sum(int(r["case_count"]) for r in csv.DictReader(handle))
    if total != source_summary["source_case_count"]:
        errors.append("SCDB term aggregates do not reconcile to the frozen corpus")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        print("DATA CHECK FAILED")
        for error in errors:
            print("- " + error)
        raise SystemExit(1)
    print("PASS: dataset provenance, identifiers, summary counts, CSV/JSON agreement, dashboard registry, and SCDB coverage totals.")
    print("This checks consistency and provenance, not the truth of every legal interpretation.")


if __name__ == "__main__":
    main()
