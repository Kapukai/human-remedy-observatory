#!/usr/bin/env python3
"""Reproduce SCDB source downloads against the publisher's public endpoints.

Only the Python standard library is needed. Run from the directory containing
source-manifest.json. Inputs remain separately licensed; this downloader grants
no rights in third-party data. No outcome analysis is performed.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import urllib.request
import zipfile


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="data/sources/scdb-source-manifest.json")
    parser.add_argument("--output", default="data/raw/scdb")
    args = parser.parse_args()
    manifest = json.loads(Path(args.manifest).read_text())
    destination = Path(args.output)
    destination.mkdir(parents=True, exist_ok=True)
    all_ids = []
    for item in manifest["datasets"]:
        with urllib.request.urlopen(item["download_url"], timeout=90) as response:
            zipped = response.read()
        if sha(zipped) != item["zip_sha256"]:
            raise ValueError(f"Publisher ZIP changed for {item['release']}; do not silently accept a different source release")
        with zipfile.ZipFile(io.BytesIO(zipped)) as archive:
            data = archive.read(item["csv_filename"])
        if sha(data) != item["csv_sha256"]:
            raise ValueError(f"CSV checksum mismatch for {item['release']}")
        rows = list(csv.DictReader(io.StringIO(data.decode(item["encoding_used"]))))
        if len(rows) != item["row_count"] or list(rows[0]) != item["columns"]:
            raise ValueError(f"Schema or row count mismatch for {item['release']}")
        ids = [row["caseId"] for row in rows]
        if len(set(ids)) != item["unique_case_ids"] or not all(ids):
            raise ValueError(f"Identifier validation failed for {item['release']}")
        (destination / item["zip_filename"]).write_bytes(zipped)
        (destination / item["csv_filename"]).write_bytes(data)
        all_ids.extend(ids)
        print(f"Verified {item['release']}: {len(rows):,} case-centered rows")
    if len(all_ids) != manifest["combined"]["row_count"] or len(set(all_ids)) != manifest["combined"]["unique_case_ids"]:
        raise ValueError("Combined identifier validation failed")
    print(f"Verified {len(all_ids):,} rows, {len(set(all_ids)):,} unique SCDB cases. No outcome analysis performed.")


if __name__ == "__main__":
    main()
