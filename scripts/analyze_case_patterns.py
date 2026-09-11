#!/usr/bin/env python3
"""Recompute descriptive outputs for the selected historical litigation atlas.

Run with the runtime-owned Python. No network or inferential significance tests.
The input remains the source of truth; outputs are regenerated on every run.
"""

from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
import shutil
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np


SECTORS = ["Public", "Private", "Mixed"]
TECHNOLOGIES = ["Physical", "Administrative", "Computerized"]
DIRECTIONS = ["Favorable", "Mixed", "Adverse"]
STAGES = ["Damages judgment", "Merits or injunction", "Procedural or interim",
          "Settlement", "Mixed disposition", "Adverse"]
IMPLEMENTATIONS = ["Documented some restoration", "Not established in sources"]
COMPARATOR = "Organization comparator"
TEAL, GOLD, BLACK, GREY = "#007A7A", "#B68A2D", "#171717", "#D9D9D5"
SECTOR_COLORS = [BLACK, GOLD, TEAL]
STAGE_COLORS = [GOLD, TEAL, "#6A8C8C", "#DCC28C", "#747474", BLACK]


def count_table(cases, rowfield, colfield, rows, cols, sector_overrides=False):
    matrix = np.zeros((len(rows), len(cols)), dtype=int)
    for case in cases:
        row = case[rowfield]
        col = case[colfield]
        if sector_overrides:
            alternate = case.get("alternative_sector")
            if rowfield == "sector" and alternate:
                row = alternate
            if colfield == "sector" and alternate:
                col = alternate
        matrix[rows.index(row), cols.index(col)] += 1
    return matrix


def table_json(matrix, rows, cols):
    return {row: {col: int(matrix[i, j]) for j, col in enumerate(cols)}
            for i, row in enumerate(rows)}


def cramers_v(matrix):
    """Uncorrected descriptive Cramer's V; never a p-value or causal statistic."""
    matrix = matrix[np.sum(matrix, axis=1) > 0]
    matrix = matrix[:, np.sum(matrix, axis=0) > 0]
    n = int(matrix.sum())
    divisor = min(matrix.shape) - 1
    if n == 0 or divisor <= 0:
        return None
    expected = np.outer(matrix.sum(axis=1), matrix.sum(axis=0)) / n
    chi2_descriptive = float(np.sum((matrix - expected) ** 2 / expected))
    return math.sqrt(chi2_descriptive / (n * divisor))


def validate(cases):
    required = {"id", "name", "short", "year", "last_year", "country", "sector",
                "technology", "direction", "stage", "implementation", "plaintiff",
                "tags", "summary", "limit", "sources", "sector_note",
                "alternative_sector", "restoration_note"}
    ids = set()
    for case in cases:
        missing = required - case.keys()
        if missing:
            raise ValueError(f"Missing fields for {case.get('id', '?')}: {missing}")
        if case["id"] in ids:
            raise ValueError(f"Duplicate family id: {case['id']}")
        ids.add(case["id"])
        for field, labels in [("sector", SECTORS), ("technology", TECHNOLOGIES),
                              ("direction", DIRECTIONS), ("stage", STAGES),
                              ("implementation", IMPLEMENTATIONS)]:
            if case[field] not in labels:
                raise ValueError(f"Unknown {field}: {case[field]}")
        if case["alternative_sector"] not in [None, *SECTORS]:
            raise ValueError(f"Unknown alternate sector for {case['id']}")
        if not isinstance(case["tags"], list) or len(set(case["tags"])) != len(case["tags"]):
            raise ValueError(f"Tags must be a unique list: {case['id']}")
        if not isinstance(case["year"], int):
            raise ValueError(f"Year must be an integer: {case['id']}")
        for source in case["sources"]:
            if not source.get("label") or not source.get("url", "").startswith("https://"):
                raise ValueError(f"Missing source provenance: {case['id']}")


def wrap(label, width=22):
    return "\n".join(textwrap.wrap(label, width=width))


def style_axis(ax):
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color("#BBBBB5")
    ax.tick_params(length=0, pad=8)
    ax.set_axisbelow(True)


def panel_title(ax, title, subtitle):
    ax.set_title(title, loc="left", fontsize=18, fontweight="bold", pad=41)
    ax.text(0, 1.035, subtitle, transform=ax.transAxes, ha="left", va="bottom", fontsize=11)


def figure(cases, topics, tables, topic_sector, cooccurrence, jaccard, out, summary):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 12,
                         "axes.labelsize": 12, "xtick.labelsize": 11,
                         "ytick.labelsize": 12, "svg.fonttype": "none",
                         "figure.facecolor": "white", "axes.facecolor": "white",
                         "savefig.facecolor": "white"})
    fig, axes = plt.subplots(3, 2, figsize=(26, 26))
    fig.subplots_adjust(left=.13, right=.97, bottom=.10, top=.87,
                        hspace=.57, wspace=.46)
    n = len(cases)
    fig.text(.06, .971, "HUMANS CHALLENGING SYSTEMS", size=28, weight="bold", color=BLACK)
    fig.text(.06, .945, f"{n} selected litigation families  •  Six descriptive views  •  Public / private / mixed",
             size=17, color=BLACK)
    fig.text(.06, .924, "A curated historical atlas: counts describe this selection, not population win probabilities or causal effects.",
             size=13, color="#555555")

    ax = axes[0, 0]
    table = tables["sector_by_stage"]
    positions = np.arange(len(SECTORS))
    left = np.zeros(len(SECTORS), dtype=int)
    for j, (stage, color) in enumerate(zip(STAGES, STAGE_COLORS)):
        bars = ax.barh(positions, table[:, j], left=left, color=color, height=.52,
                       edgecolor="white", linewidth=1.5, label=stage)
        for i, bar in enumerate(bars):
            if table[i, j]:
                textcolor = BLACK if color == "#DCC28C" else "white"
                ax.text(left[i] + table[i, j] / 2, positions[i], str(table[i, j]),
                        ha="center", va="center", color=textcolor, weight="bold", size=12)
        left += table[:, j]
    ax.set_yticks(positions, SECTORS)
    ax.invert_yaxis()
    ax.set_xlabel("Selected families (count)")
    ax.set_xlim(0, max(left) * 1.06)
    ax.xaxis.get_major_locator().set_params(integer=True)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -.18), ncol=2,
              frameon=False, fontsize=11, columnspacing=1.8)
    panel_title(ax, "A  Sector × disposition category", "One summary category per family; full case details preserve mixed outcomes.")
    style_axis(ax)

    ax = axes[0, 1]
    table = tables["sector_by_technology"]
    width = .24
    for j, technology in enumerate(TECHNOLOGIES):
        bars = ax.bar(positions + (j - 1) * width, table[:, j], width,
                      color=[GREY, GOLD, TEAL][j], label=technology)
        ax.bar_label(bars, labels=[str(x) if x else "" for x in table[:, j]], padding=4, fontsize=12)
    ax.set_xticks(positions, SECTORS)
    ax.set_ylabel("Selected families (count)")
    ax.set_ylim(0, max(1, table.max()) * 1.22)
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.legend(loc="upper right", ncol=3, frameon=False, fontsize=11)
    panel_title(ax, "B  Sector × system type", "Analyst coding of the challenged system; technology does not establish state action.")
    style_axis(ax)

    ax = axes[1, 0]
    ax.imshow(topic_sector, cmap=LinearSegmentedColormap.from_list("topic", ["#FAFAF6", "#DCC28C", TEAL]), aspect="auto")
    ax.set_xticks(range(3), SECTORS)
    ax.set_yticks(range(len(topics)), [wrap(topic, 24) for topic in topics])
    for i in range(len(topics)):
        for j in range(3):
            value = int(topic_sector[i, j])
            ax.text(j, i, str(value), ha="center", va="center", fontsize=12,
                    color="white" if value > topic_sector.max() * .67 else BLACK)
    panel_title(ax, "C  Coded topics × sector", "Counts overlap: one family can have several topics. Tags are interpretations.")
    ax.tick_params(length=0, pad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax = axes[1, 1]
    table = tables["sector_by_implementation"]
    for j, state in enumerate(IMPLEMENTATIONS):
        bars = ax.barh(positions, table[:, j], left=table[:, :j].sum(axis=1), height=.52,
                       color=[TEAL, GREY][j], label=state, edgecolor="white", linewidth=1.5)
        for i, bar in enumerate(bars):
            if table[i, j]:
                ax.text(table[i, :j].sum() + table[i, j] / 2, positions[i], str(table[i, j]),
                        ha="center", va="center", size=12, weight="bold",
                        color="white" if j == 0 else BLACK)
    ax.set_yticks(positions, SECTORS)
    ax.invert_yaxis()
    ax.set_xlabel("Selected families (count)")
    ax.set_xlim(0, max(table.sum(axis=1)) * 1.06)
    ax.xaxis.get_major_locator().set_params(integer=True)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -.18), frameon=False, fontsize=11)
    panel_title(ax, "D  Restoration evidence reported (any stage)", "Includes predecision release or quashing; not an order-compliance or causal rate.")
    style_axis(ax)

    ax = axes[2, 0]
    im = ax.imshow(jaccard, vmin=0, vmax=1,
                   cmap=LinearSegmentedColormap.from_list("overlap", ["#FAFAF6", "#DCC28C", TEAL]),
                   aspect="auto")
    topic_ids = [f"T{i + 1}" for i in range(len(topics))]
    ax.set_xticks(range(len(topics)), topic_ids)
    ax.set_yticks(range(len(topics)), [f"T{i+1}  {wrap(topic, 21)}" for i, topic in enumerate(topics)])
    for i in range(len(topics)):
        for j in range(len(topics)):
            v = jaccard[i, j]
            ax.text(j, i, f"{v:.2f}" if np.isfinite(v) else "—", ha="center", va="center",
                    fontsize=11, color="white" if v > .68 else BLACK)
    panel_title(ax, "E  Topic overlap (Jaccard)", "Shared positive annotations / union. Not a correlation coefficient or causal cluster.")
    ax.tick_params(length=0, pad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)

    ax = axes[2, 1]
    min_decade = min(c["year"] for c in cases) // 10 * 10
    max_decade = max(c["year"] for c in cases) // 10 * 10
    decades = list(range(min_decade, max_decade + 1, 10))
    for sector, color in zip(SECTORS, SECTOR_COLORS):
        counts = collections.Counter(c["year"] // 10 * 10 for c in cases if c["sector"] == sector)
        ax.plot(decades, [counts[d] for d in decades], marker="o", markersize=5,
                linewidth=2, label=sector, color=color)
    ax.set_xticks(decades[::3])
    ax.set_ylabel("Selected families (count)")
    ax.set_xlabel("Decade of anchor decision (not duration to remedy)")
    ax.yaxis.get_major_locator().set_params(integer=True)
    ax.set_ylim(bottom=0)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -.18), ncol=3,
              frameon=False, fontsize=11)
    panel_title(ax, "F  Historical coverage of this atlas", "Selection density across time; not a trend in all harms, filings, or legal success.")
    style_axis(ax)

    fig.text(.06, .044, "Unit: litigation family; linked opinions are not independent events. Organization-only comparator excluded from these panels.", size=12)
    fig.text(.06, .029, "Ownership and legal route differ. Topic absence means 'not tagged here,' not a demonstrated absence of that failure mode.", size=12)
    fig.text(.06, .014, "Source-linked data, code, alternative-sector sensitivity, definitions, and causal study proposals accompany this figure.", size=12)
    fig.savefig(out / "case-patterns.png", dpi=170)
    fig.savefig(out / "case-patterns.svg")
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("build/cases-coded.json"))
    parser.add_argument("--output", type=Path, default=Path("output/case-pattern-research"))
    args = parser.parse_args()
    cases = json.loads(args.input.read_text())
    if isinstance(cases, dict):
        cases = cases["cases"]
    validate(cases)
    selected = [c for c in cases if c["plaintiff"] != COMPARATOR]
    if not selected:
        raise ValueError("No default-included families")
    topics = sorted({tag for case in selected for tag in case["tags"]})
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    tables = {}
    table_definitions = [("sector_by_stage", "stage", STAGES),
                         ("sector_by_technology", "technology", TECHNOLOGIES),
                         ("sector_by_direction", "direction", DIRECTIONS),
                         ("sector_by_implementation", "implementation", IMPLEMENTATIONS)]
    for name, field, labels in table_definitions:
        tables[name] = count_table(selected, "sector", field, SECTORS, labels)
    topic_sector = np.array([[sum(tag in c["tags"] and c["sector"] == sector for c in selected)
                              for sector in SECTORS] for tag in topics])
    cooccurrence = np.array([[sum(a in c["tags"] and b in c["tags"] for c in selected)
                              for b in topics] for a in topics])
    totals = np.diag(cooccurrence)
    union = totals[:, None] + totals[None, :] - cooccurrence
    jaccard = np.divide(cooccurrence, union, out=np.full(union.shape, np.nan), where=union > 0)
    exported = [{**case, "included_by_default": case["plaintiff"] != COMPARATOR} for case in cases]
    (out / "cases.json").write_text(json.dumps(exported, ensure_ascii=False, indent=2) + "\n")
    csvfields = list(dict.fromkeys(key for case in exported for key in case))
    with (out / "cases.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=csvfields)
        writer.writeheader()
        for case in exported:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (list, dict))
                             else value for key, value in case.items()})
    with (out / "topic-cooccurrence.csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["topic_a", "topic_b", "both_tagged", "either_tagged", "jaccard_annotation_overlap"])
        for i, a in enumerate(topics):
            for j, b in enumerate(topics):
                writer.writerow([a, b, int(cooccurrence[i, j]), int(union[i, j]),
                                 float(jaccard[i, j]) if np.isfinite(jaccard[i, j]) else ""])
    sensitivity = {}
    for name, field, labels in table_definitions:
        alternate = count_table(selected, "sector", field, SECTORS, labels, sector_overrides=True)
        sensitivity[name] = {"all_alternatives_together": table_json(alternate, SECTORS, labels),
                             "descriptive_cramers_v": cramers_v(alternate) if field != "implementation" else None}
    summary = {
        "title": "Selected historical litigation families: descriptive research atlas",
        "research_cutoff": "2026-09-11",
        "source_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest(),
        "unit": "litigation family; events within families are not independent",
        "selection": "purposive historical selection, emphasizing consequential human challenges; not a representative sample",
        "total_records": len(cases), "default_included": len(selected),
        "excluded_comparator_ids": [c["id"] for c in cases if c["plaintiff"] == COMPARATOR],
        "sector_counts": dict(collections.Counter(c["sector"] for c in selected)),
        "technology_counts": dict(collections.Counter(c["technology"] for c in selected)),
        "direction_counts": dict(collections.Counter(c["direction"] for c in selected)),
        "stage_counts": dict(collections.Counter(c["stage"] for c in selected)),
        "implementation_counts": dict(collections.Counter(c["implementation"] for c in selected)),
        "topic_counts": {topic: int(totals[i]) for i, topic in enumerate(topics)},
        "topic_by_sector": table_json(topic_sector, topics, SECTORS),
        "tables": {name: table_json(tables[name], SECTORS, labels) for name, _, labels in table_definitions},
        "descriptive_cramers_v": {name: cramers_v(tables[name]) for name, _, _ in table_definitions if name != "sector_by_implementation"},
        "cramers_v_interpretation": "Uncorrected association strength among these selected coded families only; no p-value, population claim, or causal interpretation. Sensitive to coding, sparse cells, and corpus selection.",
        "alternative_sector_sensitivity": {
            "interpretation": "All specified alternative sector assignments applied together; an analyst scenario, not a confidence interval or exhaustive uncertainty bound.",
            "changed_families": [{"id": c["id"], "from": c["sector"], "to": c["alternative_sector"]}
                                 for c in selected if c.get("alternative_sector") and c["sector"] != c["alternative_sector"]],
            "tables": sensitivity,
        },
        "jaccard_interpretation": "Overlap of positive topic annotations, not verified feature prevalence. Untagged does not establish absence. No validated natural clusters are claimed.",
        "implementation_interpretation": "Restoration evidence reported at any stage can include predecision release or judicial quashing. It does not establish complete remedy, compliance with the selected decision, or an effect caused by that decision. Not established in sources means unverified in this research, not failed or absent implementation.",
        "money_policy": "No monetary totals or cross-case aggregation; judgments, settlements, and payments differ.",
    }
    extra_fields = ["habeas_vehicle", "data_failure", "holding_scope", "actual_computer_fault"]
    summary["habeas_and_data_fields"] = {}
    for field in extra_fields:
        if any(field in case for case in selected):
            values = collections.Counter()
            for case in selected:
                value = case.get(field, "Not coded")
                key = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list, bool)) else str(value)
                values[key] += 1
            summary["habeas_and_data_fields"][field] = dict(values)
    (out / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
    figure(selected, topics, tables, topic_sector, cooccurrence, jaccard, out, summary)
    source_script = Path(__file__).resolve()
    shutil.copy2(source_script, out / source_script.name)
    methods = source_script.parent / "causal-design.md"
    if methods.exists():
        shutil.copy2(methods, out / methods.name)
    readme = f"""# Human remedies: selected historical case patterns

Research cutoff: 11 September 2026. **{len(selected)} default-included litigation families**; {len(cases) - len(selected)} organization-only comparator(s) retained in exports but excluded from figures and default counts.

This is an analyst-coded, purposively selected historical atlas, heavily shaped by landmark litigation. It is not a probability sample, exhaustive case census, validated prediction model, legal citator, or causal study. Counts are counts of these families. None is a population win rate, harm rate, or measure of the chance of obtaining a remedy.

## Reproduce

Use Python 3 with NumPy and Matplotlib. From this directory run:

```sh
python analyze_case_patterns.py --input cases.json --output regenerated
```

The script recalculates all counts, overlap matrices, scenario statistics, and plots from the supplied input. The exported cases include `included_by_default`; the authoritative exclusion rule remains `plaintiff == Organization comparator`. No network is required. `summary.json` records a SHA-256 hash of the input used for that run.

## Files and units

- `cases.json` and `cases.csv`: full source-linked family records, including comparator and coding caveats. CSV array fields contain JSON.
- `summary.json`: default counts, contingency tables, uncorrected descriptive Cramer's V, and simultaneous alternative-sector scenario.
- `topic-cooccurrence.csv`: positive annotation intersection, union, and Jaccard overlap for every topic pair.
- `case-patterns.png` and `case-patterns.svg`: six reproducible scientific plots. SVG is scalable and retains text.
- `causal-design.md`: measurement rules, eight dashboard specifications, and four proposed causal studies.
- `analyze_case_patterns.py`: exact regeneration script.

A row is a litigation family, not one person or one statistically independent decision. The anchor year is not the duration of injury or time to restoration. A selected family can include different judgments, claims, or later developments. Consult its summary, limit, sources, and restoration note before interpreting a summary category.

## Classification and uncertainty

Ownership is coded Public / Private / Mixed. It does not by itself determine state action, immunity, jurisdiction, or the applicable claim. `sector_note` explains the choice; `alternative_sector` supplies a defensible alternative where specified. The sensitivity scenario changes all listed alternatives together. It is not a confidence interval and does not exhaust every plausible coding.

System type is Physical (including forensic methods) / Administrative / Computerized, a deliberately coarse description of the challenged system. Direction is Favorable / Mixed / Adverse at the latest selected stage, not an adjudication of every allegation. Disposition stage is a summary category, not an ordinal remedy score. An injunction, a remand, a settlement, and actual compensation are distinct outcomes.

The chart labels the implementation field **Restoration evidence reported (any stage)**. `Documented some restoration` requires the source-linked note to identify practical relief, which may precede the selected decision or consist of judicial quashing. It is not a certification of complete restoration, compliance with that decision, or an effect caused by that decision. `Not established in sources` means the reviewed sources do not establish restoration; it does not mean no one benefited or the government disobeyed an order. Unknown follow-up cannot be converted into an institutional failure rate. Optional habeas and data-failure fields remain intact in both exports; uncoded entries are counted separately, not assumed negative.

Topic tags record positive analyst annotations. Their absence is **not** demonstrated absence of a mechanism. The Jaccard measure is |tags A and B| / |tags A or B|. It describes annotation overlap only. No latent clusters, causal pathways, or independently measured error rates are inferred from this matrix. Distinct coding and a different case selection may produce different patterns.

Cramer's V is computed from each displayed sector contingency table after removing empty margins: sqrt(chi-square / (n × min(r−1,c−1))). It is uncorrected and purely descriptive here. No p-values, confidence intervals, generalization, or causal inference are provided. Judicial reasons coded after outcomes must not be presented as independent predictors of those same outcomes.

## Sources

Every family retains original source labels and URLs. The following register is included for audit and offline handoff; these links require internet access:

"""
    for case in cases:
        readme += f"### {case['id']} — {case['name']}\n\n"
        readme += f"Sector: {case['sector']}. {case['sector_note']}\n\n"
        readme += f"Interpretation limit: {case['limit']}\n\n"
        for source in case["sources"]:
            readme += f"- [{source['label']}]({source['url']})\n"
        readme += "\n"
    (out / "README.md").write_text(readme)
    print(json.dumps({"output": str(out), "included": len(selected), "total": len(cases),
                      "topics": len(topics), "cramers_v": summary["descriptive_cramers_v"]}, indent=2))


if __name__ == "__main__":
    main()
