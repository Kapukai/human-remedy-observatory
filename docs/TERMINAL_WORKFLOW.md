# Run the research workbench

The app requires Git for cloning and updates, Python 3, and a modern browser. No Python packages, Node.js, GitHub password, API key, or cloud account are needed to run it. Cloning this public repository does not grant permission to push changes.

## First setup or update on macOS / Linux

Paste this entire block into Terminal. It stops if a command fails and preserves existing local edits. If you already cloned the repository somewhere else, use that location instead of creating another copy.

```bash
(
  set -e
  mkdir -p "$HOME/Projects"
  cd "$HOME/Projects"
  if [ ! -d human-remedy-observatory/.git ]; then
    git clone https://github.com/Kapukai/human-remedy-observatory.git
  fi
  cd human-remedy-observatory
  git pull --ff-only
  python3 scripts/check_data.py
  python3 scripts/serve_workbench.py
)
```

Your browser should open at `http://127.0.0.1:8765/`. If it does not, enter that address manually. Keep this terminal open while exploring. Press **Control-C** to stop the server. This serves published research files on this computer only; it does not host a public website or upload anything.

If Terminal reports that Git or Python is missing, install the missing prerequisite through its official distribution and rerun the block. Do not paste credentials into a support conversation.

## What to explore first

1. **Atlas:** inspect coverage and source records before comparing directions of decisions. Default: 57 US litigation families. All jurisdictions: 62 human-centered families. The organization comparator is excluded unless selected.
2. **Relationships:** examine sector, technology, topic overlap, and alternative coding. A descriptive association or neighboring case is a question to investigate, not evidence of a shared cause.
3. **Larger corpus:** inspect frozen coverage aggregates for 29,270 SCDB records. Atlas filters do not filter this separate corpus. Habeas issue codes identify candidates, not a verified population of petitions.
4. **Research & legislation:** inspect the 25-view readiness inventory and H1–H4 proposals. Missing-data panels explain what must be collected before a plot or test is justified.

Exports contain the selected rows, filter settings, and denominator. A downloaded CSV is a research extract, not a filing or a certified statement of law. Follow sources from the case inspector for the scope of each coded holding.

## Send a status report back

Open another terminal, or stop the server with Control-C, then run:

```bash
(
  set -e
  cd "$HOME/Projects/human-remedy-observatory"
  python3 scripts/status_report.py
)
```

Paste the printed JSON into the conversation. It reports the revision, Python version, dataset hash, counts, dashboard readiness, and file presence. It omits usernames, home-directory paths, tokens, and case uploads. `scdb_raw_files_present: false` is normal: the workbench uses included aggregates and does not require downloading the third-party corpus.

## Update after a new published increment

Stop the server before updating:

```bash
(
  set -e
  cd "$HOME/Projects/human-remedy-observatory"
  git pull --ff-only
  python3 scripts/check_data.py
  python3 scripts/serve_workbench.py
)
```

If Git reports local changes or diverged history, stop and share the message. Do not force reset your work. If the port is occupied, run `python3 scripts/serve_workbench.py --port 8766` and open `http://127.0.0.1:8766/`.

## Reproduce checks or larger-corpus figures

The consistency and HTTP checks use only Python's standard library:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

If Node.js 18 or later is already installed, the browser calculation tests can also be run:

```bash
node --test tests/analysis.test.js
```

These checks verify denominators, descriptive calculations, exports, source-hash agreement, and local resource boundaries. They do not certify legal interpretations or establish causal effects.

For optional raw-corpus downloads and scientific figure regeneration, follow [SCDB_DATA.md](../SCDB_DATA.md) and the [reproduction guide](../RESEARCH_GUIDE.md). Those workflows have additional scientific dependencies and source-rights conditions; they are not required to use the workbench.

## Next research gate

Use [CRITICAL_PATH.md](CRITICAL_PATH.md) to move from M1 to M2. Record source-supported events using the schema and blank template. Do not rename exploratory results as preregistered. Complete a study-specific hypothesis plan, declare prior data access, and register it before examining independent evaluation outcomes. Required safeguards apply in every study arm.
