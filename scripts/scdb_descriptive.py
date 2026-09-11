#!/usr/bin/env python3
"""Descriptive source coverage only: no outcome analysis or inferential tests.

Usage from repository root:
  python scripts/download_scdb.py --manifest data/sources/scdb-source-manifest.json
  python scripts/scdb_descriptive.py --raw data/raw/scdb

Raw third-party inputs are intentionally excluded from the repository.
"""
import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path

ISSUE_AREAS = {1: "Criminal procedure", 2: "Civil rights", 3: "First Amendment", 4: "Due process", 5: "Privacy", 6: "Attorneys", 7: "Unions", 8: "Economic activity", 9: "Judicial power", 10: "Federalism", 11: "Interstate relations", 12: "Federal taxation", 13: "Miscellaneous", 14: "Private action"}
FIELDS = ["caseId", "term", "issue", "issueArea", "petitioner", "respondent", "dateDecision", "caseOrigin", "lawType", "lawSupp", "lawMinor"]
MISSING_FIELDS = ["dateDecision", "petitioner", "respondent", "issue", "issueArea", "caseOrigin", "lawType", "lawSupp", "lawMinor"]
ERAS = [(1791, 1849), (1850, 1899), (1900, 1945), (1946, 1979), (1980, 1999), (2000, 2025)]


def as_int(value):
    return int(float(value)) if value.strip() else None


def csv_write(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", default="data/raw/scdb")
    parser.add_argument("--manifest", default="data/sources/scdb-source-manifest.json")
    parser.add_argument("--output", default="reports/scdb")
    parser.add_argument("--no-plots", action="store_true")
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(Path(args.manifest).read_text())
    rows = []
    for item in manifest["datasets"]:
        path = Path(args.raw) / item["csv_filename"]
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != item["csv_sha256"]:
            raise ValueError(f"Source checksum mismatch: {path.name}")
        with path.open(encoding=item["encoding_used"], newline="") as handle:
            for original in csv.DictReader(handle):
                row = {key: original[key] for key in FIELDS}
                row["release"] = item["release"]
                row["period"] = "Modern" if item["release"] == "SCDB_2026_01" else "Legacy"
                rows.append(row)
    assert len(rows) == manifest["combined"]["row_count"]
    assert len(set(row["caseId"] for row in rows)) == len(rows)
    assert all("partyWinning" not in row and "caseDisposition" not in row for row in rows)
    terms = Counter((as_int(row["term"]), row["period"]) for row in rows)
    term_rows = [{"term": term, "period": period, "case_count": count} for (term, period), count in sorted(terms.items())]
    issue_counts = Counter((as_int(row["issueArea"]), row["period"]) for row in rows)
    issue_rows = [{"issue_area_code": code if code is not None else "", "issue_area": ISSUE_AREAS.get(code, "Missing/other"), "period": period, "case_count": count} for (code, period), count in sorted(issue_counts.items(), key=lambda item: (str(item[0][0]), item[0][1]))]
    missing_rows = []
    for period in ("Legacy", "Modern"):
        subset = [row for row in rows if row["period"] == period]
        for field in MISSING_FIELDS:
            count = sum(not row[field].strip() for row in subset)
            missing_rows.append({"period": period, "field": field, "blank_count": count, "denominator": len(subset), "blank_percent": round(100 * count / len(subset), 6)})
    habeas_rows = []
    for start, end in ERAS:
        subset = [row for row in rows if start <= as_int(row["term"]) <= end]
        for code, label in ((10020, "Habeas corpus issue"), (90040, "Comity: habeas corpus issue")):
            count = sum(as_int(row["issue"]) == code for row in subset)
            habeas_rows.append({"term_start": start, "term_end": end, "era": f"{start}–{end}", "issue_code": code, "label": label, "candidate_count": count, "all_case_denominator": len(subset), "candidate_percent_of_era": round(100 * count / len(subset), 6)})
    csv_write(out / "coverage_by_term.csv", term_rows, ["term", "period", "case_count"])
    csv_write(out / "issue_mix.csv", issue_rows, ["issue_area_code", "issue_area", "period", "case_count"])
    csv_write(out / "blank_fields.csv", missing_rows, ["period", "field", "blank_count", "denominator", "blank_percent"])
    csv_write(out / "habeas_issue_candidates_by_era.csv", habeas_rows, ["term_start", "term_end", "era", "issue_code", "label", "candidate_count", "all_case_denominator", "candidate_percent_of_era"])
    summary = {"analysis_type": "Exploratory descriptive source coverage; not a hypothesis test", "source_case_count": len(rows), "unique_case_count": len(set(row["caseId"] for row in rows)), "legacy_count": sum(row["period"] == "Legacy" for row in rows), "modern_count": sum(row["period"] == "Modern" for row in rows), "terms": [min(as_int(row["term"]) for row in rows), max(as_int(row["term"]) for row in rows)], "habeas_issue_10020_count": sum(as_int(row["issue"]) == 10020 for row in rows), "habeas_issue_90040_count": sum(as_int(row["issue"]) == 90040 for row in rows), "outcome_fields_analyzed": [], "confidence_intervals": None, "p_values": None, "causal_effects": None, "limitations": ["Counts describe the frozen SCDB releases, not all U.S. petitions or all system failures.", "Issue flags locate candidates, not all cases procedurally arising on habeas.", "Legacy and modern coding and Court jurisdiction differ; historical counts are not failure rates.", "Blank optional fields can be valid not-applicable entries; blanks are not findings of error.", "Exact file counts need no sampling interval. Coding and selection uncertainty are not eliminated.", "No private-versus-public outcome comparison or causal effect has been computed."]}
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    if not args.no_plots:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.ticker import FuncFormatter
        import numpy as np
        plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.titlesize": 13, "axes.titleweight": "bold", "axes.labelsize": 10, "axes.spines.top": False, "axes.spines.right": False, "axes.edgecolor": "#BCC4CC", "text.color": "#152536", "axes.labelcolor": "#152536", "xtick.color": "#405261", "ytick.color": "#405261", "figure.facecolor": "white", "axes.facecolor": "white", "svg.fonttype": "none"})
        navy, teal, gold = "#243E55", "#008B8F", "#B88B35"
        fig, axes = plt.subplots(2, 2, figsize=(16, 11.5))
        fig.subplots_adjust(left=.10, right=.975, top=.84, bottom=.13, wspace=.30, hspace=.43)
        fig.text(.05, .962, "HUMAN REMEDY OBSERVATORY", fontsize=13, weight="bold", color=teal)
        fig.text(.05, .923, "29,270 Supreme Court disputes: what the source covers", fontsize=21, weight="bold")
        fig.text(.05, .885, "Exploratory description • terms 1791–2025 • frozen SCDB releases • no win-rate or causal analysis", fontsize=11, color="#586775")
        ax = axes[0, 0]
        for period, color in (("Legacy", navy), ("Modern", teal)):
            data = [row for row in term_rows if row["period"] == period]
            ax.plot([row["term"] for row in data], [row["case_count"] for row in data], color=color, lw=1.6, label=f"{period} ({sum(row['case_count'] for row in data):,})")
        ax.axvline(1945.5, color=gold, ls="--", lw=1)
        ax.set(title="A  |  Cases available per Court term", xlabel="Supreme Court term", ylabel="Disputes in source")
        ax.set_xlim(1791, 2025);ax.set_ylim(bottom=0);ax.grid(axis="y", alpha=.15);ax.legend(frameon=False, fontsize=9)
        ax = axes[0, 1]
        totals = {code: sum(row["case_count"] for row in issue_rows if row["issue_area_code"] == code) for code in ISSUE_AREAS}
        top = sorted(totals, key=totals.get, reverse=True)[:7]
        categories = [(ISSUE_AREAS[code], [code]) for code in top] + [("Other / blank issue areas", [code for code in ISSUE_AREAS if code not in top] + [""])]
        y = np.arange(len(categories));left = np.zeros(len(categories))
        for period, color in (("Legacy", navy), ("Modern", teal)):
            vals = [sum(row["case_count"] for row in issue_rows if row["issue_area_code"] in codes and row["period"] == period) for _, codes in categories]
            ax.barh(y, vals, left=left, color=color, height=.65);left += np.array(vals)
        ax.set_yticks(y, [label for label, _ in categories], fontsize=9);ax.invert_yaxis();ax.set(title="B  |  Issue mix in this selected Court docket", xlabel="Disputes in source")
        for i, count in enumerate(left): ax.text(count + max(left)*.02, i, f"{int(count):,}", va="center", fontsize=8)
        ax.set_xlim(0, max(left)*1.18);ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x):,}"));ax.grid(axis="x", alpha=.15)
        ax = axes[1, 0]
        fields = ["petitioner", "respondent", "issue", "caseOrigin", "lawType", "lawSupp", "lawMinor"]
        matrix = np.array([[next(row["blank_percent"] for row in missing_rows if row["field"] == field and row["period"] == period) for period in ("Legacy", "Modern")] for field in fields])
        im=ax.imshow(matrix, aspect="auto", cmap="Blues", vmin=0, vmax=100)
        ax.set_xticks([0,1], ["Legacy", "Modern"]);ax.set_yticks(np.arange(len(fields)), fields);ax.set_title("C  |  Blank entries by field (%)")
        for i in range(len(fields)):
            for j in range(2): ax.text(j, i, f"{matrix[i,j]:.1f}%", ha="center", va="center", color="white" if matrix[i,j]>55 else navy, fontsize=10)
        ax.tick_params(length=0);ax.text(0, -.13, "Optional / not-applicable blanks can be correct; this is not an error rate.", transform=ax.transAxes, fontsize=8.5, color="#586775")
        ax = axes[1, 1]
        eras = [f"{a}–{b}" for a,b in ERAS];y = np.arange(len(eras));left = np.zeros(len(eras))
        for code, color, label in ((10020, teal, "10020: habeas"), (90040, gold, "90040: comity / habeas")):
            vals = [next(row["candidate_count"] for row in habeas_rows if row["era"] == era and row["issue_code"] == code) for era in eras]
            ax.barh(y, vals, left=left, color=color, label=label, height=.65);left += np.array(vals)
        for i, count in enumerate(left): ax.text(count + max(left)*.025, i, str(int(count)), va="center", fontsize=9)
        ax.set_yticks(y, eras);ax.invert_yaxis();ax.set(title=f"D  |  {int(sum(left)):,} habeas-issue candidates to verify", xlabel="Disputes with either issue code (not all habeas cases)")
        ax.set_xlim(0, max(left)*1.2);ax.legend(frameon=False, fontsize=8, loc="upper right");ax.grid(axis="x", alpha=.15)
        fig.text(.05, .065, "Source: Supreme Court Database • Legacy 07 + 2026 Release 01 • verified 11 September 2026", fontsize=9)
        fig.text(.05, .043, "Counts are exact for these files. Selection, coding and follow-up uncertainty remain. Larger N does not establish representativeness or causation.", fontsize=9, color="#586775")
        for ext in ("png", "svg", "pdf"):
            fig.savefig(out / f"scdb_coverage_dashboard.{ext}", dpi=180 if ext == "png" else 300, metadata={"Title": "SCDB source coverage — exploratory descriptive analysis"} if ext == "pdf" else None)
        plt.close(fig)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
