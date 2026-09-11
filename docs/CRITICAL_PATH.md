# Critical path: from published cases to tested remedies

This is an implementation roadmap, not a report of completed causal research. The historical atlas has already been explored. The prepared analysis plan is a prospective proposal, **not a preregistration**. No task below claims that a visualization proves a system unsafe or creates a legal entitlement.

## The next deliverable

Make the published material usable as one research workbench: a searchable case explorer, consistent filters, source-linked views, explicit data-readiness labels, and a path from each apparent pattern to a testable question. The current workbench uses the published annotations. Additional chart types remain visible as research requirements until their measurements exist.

The next research bottleneck is **measurement and sampling**, not chart quantity. A well-designed dashboard cannot recover unrecorded outcomes, establish a representative denominator, or distinguish correlated errors from independent evidence without source-level coding.

## What is available and what is not

| Resource | Present state | Permitted interpretation |
|---|---|---|
| Curated historical atlas | 62 selected human-centered litigation families, plus one separately identified organization comparator | Descriptive case comparison and hypothesis generation; not a population success rate |
| Habeas subset | 19 identified proceedings in the selected collection | Source-linked legal examples; not all habeas petitions and not all caused by software faults |
| Supreme Court Database | Reproducible acquisition workflow and aggregate coverage analyses for 29,270 records | Coverage and variable assessment; Supreme Court petitioning party is not necessarily the affected human |
| Integrated workbench | First implementation available; local browser acceptance check remains | Explore available data and inspect missing measurements |
| Normalized claims and dated events | Schema and blank template supplied; full historical coding not completed | No longitudinal remedy estimates yet |
| Defined filing cohort | Not acquired or specified; FJC data are a candidate source, not an established cohort | No filing-to-remedy funnel or general habeas win estimate yet |
| Independent duplicate coding | Not completed | No measured inter-reviewer reliability yet |
| Operational load, delay, recurrence, and endpoint updates | Not collected | No measured queue model, controller performance, or correction-propagation result yet |
| Intervention evaluation | Proposed only | No causal-effect estimate, intervention confidence interval, or safety certification |

## Milestones and dependencies

Dependencies establish order rather than arbitrary dates. Publication remains versioned and correctable throughout.

| Milestone | Work packages | State | Dependency | Acceptance evidence |
|---|---|---|---|---|
| M0 — Publish the research baseline | Existing release | Published | None | Public source-linked data, codebook, methods, dashboards, licensing and correction guidance |
| M1 — Integrate the research workbench | WP01 | Implemented; browser acceptance pending | M0 | Available views use the same filtered cohort; each shows unit, denominator, sources, and limitations; unsupported views explain required data |
| M2 — Normalize and independently review evidence | WP02, WP03 | Templates ready; coding pending | M0; can overlap M1 | Claims and events link to source passages; review disagreements retained; disputed facts and unknown outcomes remain explicit |
| M3 — Establish a defined filing cohort | WP04 | Pending | M2 measurement rules | Reproducible jurisdiction/period/route selection; inclusion log, deduplication, coverage audit, follow-up plan, source rights checked |
| M4 — Validate patterns and associations | WP05 | Pending | M2 and M3 | Discovery/test separation; feature and model specification; sensitivity and cluster-stability analyses; uncertainty tied to design |
| M5 — Test proposed interventions | WP06 | Design only | M2; study-specific M3/M4 inputs | Controlled simulation first where appropriate; protocol registered before evaluation; independent outcomes, fidelity, adverse events, null results reported |
| M6 — Translate findings into legislation and replication | WP07 | Drafting may begin; evidentiary validation pending | M4/M5 for empirical effectiveness claims | Each proposed duty links to a test, auditable record, responsible role, failure response, review route, and replication plan |

Critical research sequence: **measurement → independent coding → cohort definition → validation → intervention evaluation → evidence-supported legislative revision**. Workbench development and legal drafting can proceed alongside it, with proposal and evidence clearly labeled.

## Work packages

### WP01 — One coherent dashboard experience

- Connect the case atlas, relationship views, corpus coverage, and research plan through consistent controls.
- Use the [25-view registry](../data/research/dashboard-registry.json) as a readiness inventory, not a promise that all plots are statistically meaningful today.
- Show the observational unit and current denominator beside each plot. Separate selected family counts, opinions, claims, events, and people.
- Keep source inspection one action away from a pattern. Allow users to inspect alternative sector coding without describing the difference as a confidence interval.
- Acceptance: default counts reproduce the published baseline; filtering preserves source access; selected tags are never labeled proven failure rates; missing data are distinguishable from zero.

#### WP01A / WP01B — Familiar exploration with fewer setup decisions

Tableau's documented action patterns include filtering related views, highlighting selected marks, linking sources, and navigation. Those interactions are useful design references for this observatory. The following priorities are our design decisions, not claims of Tableau feature parity. [Tableau dashboard actions](https://help.tableau.com/current/pro/desktop/en-us/actions.htm).

| Priority | Interaction | Delivery / acceptance |
|---|---|---|
| 1 | One set of filters and one visible denominator | WP01A implemented: atlas and relationship views share the selection; the separate SCDB corpus is explicitly distinguished |
| 2 | Source inspection from a selected case | WP01A implemented: case selector, timeline marks, and topic neighbors open the same evidence inspector |
| 3 | Reopen a view and export its selection | WP01A implemented: local view links, CSV/JSON extracts, and SVG chart exports; links need a compatible local checkout and data version |
| 4 | Click a chart cell to select its cases across charts | WP01B next: show active selection, support clear/undo, and verify no hidden denominator change |
| 5 | Compare two saved cohorts side by side | WP01B next: lock the comparison definition, disclose different denominators and connected families; no automatic causal or significance label |
| 6 | Explain a finding with its evidence trail | WP01B next: export a reproducible research note containing question, filters, data version, descriptive result, alternative explanations, and proposed test |

Avoid asking readers to construct joins or calculate a metric before viewing the evidence. Use ordinary labels first, with formulas and assumptions available on demand. A chart builder and live data integrations come after the metric definitions and event model are stable. These usability improvements can proceed alongside WP02; they do not replace evidence coding or cohort construction.

### WP02 — Normalize records without manufacturing certainty

Model `litigation_family`, `case`, `claim`, `opinion`, `evidence_assertion`, `source`, `event`, `system`, and opaque `subject_reference` separately. Store join tables because a family may concern several systems and subjects, a system may recur across families, and one opinion may resolve several claims. A case caption does not establish identity equivalence across datasets.

Use an append-only event history: new information creates a new version linked by `supersedes_event_ids`; it does not silently overwrite the original interpretation. Retractions, corrected classifications, appeal reversals, and data-release changes must remain inspectable. Public retention must still honor applicable privacy, sealing, and removal obligations; append-only means auditable research history, not an irrevocable duty to expose personal information.

Code the occurrence time separately from the time a source was published, extracted, verified, and added. Preserve unknown dates and date precision. Never fabricate a day from a known year. Distinguish an ordered remedy, stayed order, actual release, verified payment, operative record update, and reported recurrence.

Artifacts: [event schema](../schemas/research-events.schema.json), [blank event CSV](../templates/evidence-event.csv). Acceptance: each affirmative factual or outcome claim has a source locator and evidence status; schemas reject contradictory date precision and unsupported event types; no private identifying data are needed for the public model.

The CSV is intentionally header-only. Serialize nested arrays and objects in its `*_json` columns; map `occurrence_value` and `occurrence_precision` into the schema’s `occurrence` object. Enable JSON Schema format assertions for calendar-date validation. A separate dataset validator must check source-reference existence, unique event IDs, supersession cycles, revision order, and distinct reviewer identities; a schema cannot establish factual truth or privacy on its own.

### WP03 — Independent coding and adjudication

Freeze definitions before measuring agreement. Use two independent reviewers for the evaluation sample; keep their initial labels separate. Where practical, hide each reviewer's labels and the research hypothesis, intervention assignment, and final outcome when coding antecedent features. Record what could not be blinded; historical opinions often disclose outcomes.

Report the overlap sample and sampling method, confusion tables, raw agreement, chance-adjusted agreement where appropriate, missingness, and category prevalence. Use a third reviewer or documented consensus protocol for disagreements without discarding the original labels. Agreement measures reproducibility, not factual truth.

Acceptance: a predeclared, field-specific reliability criterion is met for fields used in confirmatory claims; unresolved critical disagreement is resolved, excluded under a declared rule, or propagated through sensitivity analyses. Do not select a convenient numerical threshold after seeing agreement results. No claim of independent human review until qualified independent reviewers actually complete it.

### WP04 — Acquire a cohort suited to the question

Specify the target population before selecting records: legal route, jurisdiction, filing period, time zero, inclusion/exclusion rules, unit, repeated filings, connected families, and follow-up cutoff. Evaluate Federal Judicial Center administrative data as one candidate; check the actual release, codebook, coverage, access, and redistribution terms before using it. Its broad administrative fields may not establish data corruption, legal merits, or completed correction.

Published opinions alone cannot represent unfiled claims, unpublished dispositions, informal corrections, or every settlement. Link permissible public records only with documented match rules and uncertainty. Distinguish the filing population from the population of people harmed; they are not interchangeable.

Acceptance: a cohort flow is reproducible from a manifest; excluded/duplicate/ambiguous records remain countable; outcome ascertainment and loss to follow-up are measured; linked cases remain together when dividing discovery and evaluation data.

### WP05 — Explore, then validate

For discovery, inspect coverage, strata, annotation overlap, and alternative coding. For any clustering, disclose features, scaling, distance, missingness treatment, linkage/algorithm, and all tuning. Outcome-derived features must not leak into a purported prospective predictor. Reserve an independent validation set or later cohort by connected family/system as required by the estimand.

Test cluster stability under resampling and coding changes, then evaluate replication on new cases. Associations need case-mix and selection analysis; a public/private association may reflect different legal routes, available remedies, time periods, or publication selection. Bootstrap intervals cannot repair a selected historical sample.

Acceptance: exploratory and confirmatory outputs are marked separately; effect estimates, justified intervals, null results, multiplicity decisions, and protocol deviations are reported. No causal label without an identification argument and defensible assumptions.

### WP06 — Test remedies as interventions

Start with the four proposals in [ANALYSIS_PLAN.md](../methods/ANALYSIS_PLAN.md): usable explanations, source provenance, review capacity, and verified correction propagation. Use controlled simulations with fixed reference answers when testing human/machine communication, duplicated-source detection, or review interfaces. A simulated improvement does not establish field effectiveness.

For a prospective pilot, define the intervention, comparator, eligible population, assignment unit, estimand, time zero, outcome, adverse-event monitoring, follow-up, and stopping rule. Do not withhold legally required safeguards. Prefer randomization of additional protections where appropriate; otherwise state the observational identification assumptions and test their implications.

Use [hypothesis-plan.json](../templates/hypothesis-plan.json) as an unfilled planning template. Select the practically important effect first, then plan power around independent units, clustering, attrition, and multiplicity. Do not enlarge a dataset until a desired p-value appears.

Acceptance: protocol status and timestamp are verifiable before evaluation outcomes are opened; independent outcome adjudication and implementation fidelity are measured; the study reports unsuccessful and harmful effects as well as improvements.

### WP07 — Legislation with verification and correction built in

Translate each candidate solution into a proposed duty and an executable acceptance test. For example: preserve source provenance → inspect a sample for traceable origins; deliver a correction → verify each operative endpoint; maintain review capacity → measure deadline compliance and error quality under specified load.

Drafting can begin now. Label numerical thresholds as proposed until justified, and distinguish new proposed rights from existing law. A mathematical expression alone does not define jurisdiction, legal responsibility, funding, remedy, enforcement, or review. Map each duty to a responsible role, required record, independent evaluator, response deadline, corrective action, appeal, budget, and evaluation provision.

Acceptance: independent replication reproduces the analysis; pilot evidence supports any claimed performance improvement; the bill includes an evaluation and revision mechanism; evidence gaps remain explicit rather than being filled by rhetoric.

## What each discipline contributes

| Lens | Useful contribution | What would be an overclaim |
|---|---|---|
| Data science | Sampling, missingness, reproducible coding, uncertainty, validation and causal identification | A larger convenience sample automatically yields valid population inference |
| Software architecture | Normalized entities, provenance links, versioned events, correction propagation and access controls | A database schema makes disputed facts true |
| Systems engineering | Hazard identification, interface failures, requirements traceability, verification and independent validation | A safety checklist certifies every institution or legal decision |
| Electrical/control engineering | Observable state, feedback latency, capacity, saturation, signal provenance and error containment | Legal rights or human welfare have a universally established transfer function |

The engineering analogy is testable when variables are measured. Define queue arrivals, service completions, pending work, review latency, error escapes, and acknowledged versus effective corrections. Investigate whether increased load predicts delay after accounting for task complexity. Do not fit a transfer function to sparse legal narratives or claim zero harm from zero observed errors in a finite test. **Zero preventable harm is a design objective; it is not an empirical guarantee.**

## Methods references

- Nosek et al., [The preregistration revolution](https://doi.org/10.1073/pnas.1708274114): distinguish exploration and prespecified evaluation.
- American Statistical Association, [statement on p-values](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf): significance does not establish effect size, importance, or causation.
- Hernán and Robins, [Causal Inference: What If](https://miguelhernan.org/whatifbook): causal questions require identification assumptions and study design.
- Ullmann, Hennig and Boulesteix, [cluster-validation framework](https://arxiv.org/abs/2103.01281): assess stability and external validation.
- [Federal Judicial Center](https://www.fjc.gov/): candidate source to assess during WP04; no FJC cohort has been acquired by this roadmap.

See the [codebook](../methods/CODEBOOK.md), [analysis plan](../methods/ANALYSIS_PLAN.md), and [publication scope](../methods/PUBLICATION_AND_LEGAL_SCOPE.md) for existing definitions and limitations.
