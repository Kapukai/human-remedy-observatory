# Human Remedy Observatory

**Version 0.1 — 11 September 2026. Public research on people challenging consequential systems.**

This project connects legal history, evidence provenance, and systems engineering. It asks what was challenged, who operated the system, what a court actually decided, and whether practical correction is documented. The initial release is exploratory research, not a causal study, complete legal citator, safety certification, or individual legal advice.

## Start here

- [Case catalogue](methods/CASE_CATALOGUE.md): 63 source-linked litigation families; 62 human-centered families included by default and one organization comparator excluded by default.
- [Actual habeas cases](methods/HABEAS_CASES.md): 19 identified proceedings, including false evidence, unreliable science, translation allegations, immigration classification, and an actual execution-equipment failure. Non-habeas computer-warrant cases are separately marked.
- [Codebook](methods/CODEBOOK.md): what every category does and does not mean.
- [Research plan and 25 ranked visuals](methods/ANALYSIS_PLAN.md): hypotheses, sampling, power, independent validation, and causal identification.
- [Larger dataset](SCDB_DATA.md): 29,270 SCDB case-centered records, downloaded and verified from the publisher; reproducible acquisition, provenance, and descriptive coverage.
- [Publication and legal scope](methods/PUBLICATION_AND_LEGAL_SCOPE.md).
- [Case figures](reports/atlas/case-patterns.png), [large-corpus figures](reports/scdb/scdb_coverage_dashboard.png), and [research-design figures](reports/research-design.png).
- Interactive dashboards: download the repository and open `dashboard/case-patterns.html` and `dashboard/research-design.html`. These are self-contained local viewers apart from their pinned D3 library; they do not fetch case records or send selections to a server.

## What is in this release

The default atlas contains **44 Public, 13 Private, and 5 Mixed** system families. At the latest selected stage, **38 are Favorable, 12 Mixed, and 12 Adverse** to the human claimant. There are 57 US families and five international comparators. These are selection counts, not estimated population win probabilities. All 19 identified habeas families in this selection concern public custody; they cannot identify a public-versus-private habeas effect.

A litigation family is not one human, one independent system, or one final remedy. Cahoo and Bauserman concern the same MiDAS system. Public/private is an operational classification, not a judicial determination of state action. A hearing, injunction, settlement, and verified release or payment remain separate. The restoration field records limited evidence at any stage, which can predate the selected judgment. Missing follow-up is not proof of failed compliance.

The atlas was purposively selected for historical and conceptual relevance. Judicial reasons were read after outcomes; they are not independent predictors. Topic similarity reflects annotations, not discovered natural clusters. The release reports descriptive counts and Cramér's V without inferential p-values or population confidence intervals. A larger Supreme Court corpus does not supply all lower-court filings, nonfilers, operational load, or completed remedies.

## Reproduce

Python 3.10 or later is recommended. Install the scientific plotting dependencies in your own environment:

```sh
python -m pip install -r requirements.txt
python scripts/analyze_case_patterns.py --input data/curated/cases.json --output reports/atlas
python scripts/power_scenarios.py
python scripts/download_scdb.py --manifest data/sources/scdb-source-manifest.json --output data/raw/scdb
python scripts/scdb_descriptive.py --raw data/raw/scdb --output reports/scdb
```

The downloader verifies release-specific archive and CSV hashes, schema, row counts, and identifiers. Publisher changes cause an explicit failure rather than silently changing the research dataset. Raw SCDB files are excluded from version control: public download access and citation instructions were verified, but an explicit wholesale redistribution license was not established. Download them directly from the publisher using the supplied script. Our source-linked annotations and aggregate research outputs are included here.

## Exploration is valid; confirmation needs separation

Looking at data is appropriate for quality checks and hypothesis generation. A hypothesis developed after inspection must not be presented as a prediction made before inspection. This atlas is discovery material. A future confirmatory study must specify eligibility, intervention, comparator, outcome, effect size, analysis, exclusions, and stopping rules before opening its independent evaluation data. The analysis plan is a proposal; this release does not claim a completed preregistration or causal experiment.

## Contribute and correct

Submit a source-linked correction identifying the family, disputed field, exact judgment or passage, proposed revision, and impact on downstream counts. Keep disagreement records. New cases need an inclusion reason and procedural-stage verification; they should not be selected merely because they support a hypothesis. See [CONTRIBUTING.md](CONTRIBUTING.md).

Do not submit private family records, sealed documents, credentials, identifiers, addresses, or raw medical files. Public case captions are retained for traceability; the project does not invite new allegations about private people. Researchers must check current law and later history before litigation use. The book and repository do not automatically become admissible evidence or shift a government's legal burden.

## Licensing and provenance

Original project code is MIT licensed. Original annotations, methods, and aggregate figures are offered under CC BY 4.0; see [LICENSE-DATA.md](LICENSE-DATA.md). This does not relicense judicial-source websites, commercial headnotes, third-party datasets, or linked documents. Each source retains its own applicable rights. SCDB attribution and source-release details are in its manifest and data note.
