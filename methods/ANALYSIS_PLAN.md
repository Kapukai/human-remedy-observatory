# Analysis plan: human remedies and system accountability

Version 1.0 — 11 September 2026. **Status: prospective research proposal, not a completed hypothesis test or preregistration.** The historical atlas has already been inspected. This public repository contains public court data and research materials; personal family records are outside its scope.

## What exploration and confirmation each contribute

Exploratory data analysis is valid scientific work: it checks data, reveals anomalies, generates hypotheses, and exposes measurement gaps. A hypothesis need not precede every visualization. The distinction is whether a claimed test was chosen before inspecting the data used to evaluate it. We cannot retroactively preregister hypotheses about the already examined atlas of approximately 62 families. Preserve it as discovery material; timestamp hypotheses, outcomes, exclusions, models, and stopping rules before opening an independently reserved test set or collecting prospective outcomes. Document prior knowledge and protocol changes. Preregistration supports this separation; it does not establish validity by itself. [Nosek et al., The preregistration revolution (2018)](https://doi.org/10.1073/pnas.1708274114).

More records improve precision only when their sampling and measurement fit the question. Thousands of selected published victories still lack the denominator needed to estimate how often injured people obtain remedies. Separate three datasets: the curated historical atlas; a documented jurisdiction-and-period filing cohort; and a prospective intervention study. Nonfiling, settlement, unpublished dispositions, missing follow-up, and connected litigation require explicit treatment. Never pool different countries, legal routes, years, and remedies into a supposedly universal success rate.

A p-value does not measure effect size, practical importance, probability that the hypothesis is true, or causation. Report effect estimates and uncertainty alongside model assumptions; never treat p < .05 as a certification of lawful or safe governance. [American Statistical Association statement (2016)](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf).

## Ranked visualization roadmap

**Now** means descriptive use of existing coded atlas fields; **Enrich** requires additional public records or event coding; **Prospective** requires a defined cohort, experiment, or independently validated measurements. The ranking prioritizes auditability and actionable questions before sophisticated modeling.

| Rank | Visualization and research question | Outcome / unit | Readiness | Principal limit |
|---:|---|---|---|---|
| 1 | Evidence-coverage matrix: what is actually known? | Field completeness / family | Now | Unknown is not failure. |
| 2 | Sector–disposition heatmap: where do remedies differ? | Category counts / family | Now | Selected composition, not population probabilities. |
| 3 | Outcome-stage matrix: what kind of victory? | Access, order, restoration / family | Now | Summary coding compresses mixed events. |
| 4 | Habeas route map: which review mechanism applied? | Vehicle and disposition / family | Now | Similar harms can follow different legal routes. |
| 5 | Technology–sector bars: who operates which systems? | Type counts / family | Now | Ownership does not determine state action. |
| 6 | Topic heatmap: which mechanisms recur? | Positive tags / family | Now | Untagged does not establish absence. |
| 7 | Jaccard matrix: which annotations overlap? | Tag intersection/union / families | Now | Similarity, not causal correlation. |
| 8 | Source-linked timeline: when were anchors decided? | Anchor year / family | Now | Historical coverage, not litigation incidence. |
| 9 | Sensitivity slopegraph: does sector recoding matter? | Descriptive association / coding scenario | Now | Scenarios are not confidence intervals. |
| 10 | Restoration-evidence bars: is practical relief documented? | Any-stage evidence / family | Now | Release may precede the selected judgment. |
| 11 | Causal DAG: what must be measured? | Assumed relationships / variable | Now | Arrows are hypotheses, not fitted effects. |
| 12 | Legal-barrier map: where are claims blocked? | Standing, immunity, merits / claim | Enrich | Distinguish holding from analyst interpretation. |
| 13 | Event-state swimlanes: what changed after appeal? | Linked dispositions / event | Enrich | Requires complete dated event history. |
| 14 | Review funnel: where are people lost? | Eligible → filed → heard → remedied / cohort | Enrich | Needs nonselected denominators and branching paths. |
| 15 | Cumulative-incidence curves: how long until relief? | Time to relief / eligible case | Enrich | Competing events and censoring need specification. |
| 16 | Court-year small multiples: does context differ? | Standardized outcomes / cohort | Enrich | No naive ranking of incomparable caseloads. |
| 17 | Citation network: how do doctrines connect? | Cited authority / opinion | Enrich | Citation is neither agreement nor causal influence. |
| 18 | Reviewer-agreement matrix: are labels reproducible? | Agreement/disagreement / double-coded claim | Enrich | Agreement does not guarantee truth. |
| 19 | Hierarchical-cluster stability plot: do patterns replicate? | Membership stability / family | Enrich | Hold outcomes out; external validation required. |
| 20 | Capacity–delay curve: where does backlog grow? | Arrival, service, delay / office-day | Prospective | Load and case complexity can confound. |
| 21 | Latency decomposition: which handoff delays correction? | Verified duration / process event | Prospective | Timestamp definitions must match across systems. |
| 22 | Error confusion matrix: what errors escape review? | Error type / independently adjudicated decision | Prospective | Reference adjudication itself has uncertainty. |
| 23 | Control chart: does error recurrence depart from baseline? | Recurrence per eligible decision / period | Prospective | Stable denominators; account for autocorrelation. |
| 24 | Intervention-effect forest plot: what worked where? | Prespecified effects and intervals / study or stratum | Prospective | Multiplicity, overlap, and transportability matter. |
| 25 | Correction-propagation network: did the fix reach every operative record? | Acknowledgment and verified update / system endpoint | Prospective | A received message is not an effective correction. |

Current clusters remain exploratory coded patterns. Publish features, distance, missingness rules, and alternatives; check stability and replication on separately obtained cases. [Ullmann, Hennig and Boulesteix, cluster-validation framework](https://arxiv.org/abs/2103.01281).

## Four proposed confirmatory hypotheses

For each study, define an intention-to-treat risk difference Δ = P(Y=1 | assigned intervention) − P(Y=1 | assigned comparator). **H0: Δ=0; H1: Δ≠0**, tested two-sided; the expected direction is specified below. None has been tested by this atlas. Preserve legally required safeguards in every arm.

| Hypothesis | Intervention and outcome | Assignment / analysis unit | Identification and expected direction |
|---|---|---|---|
| H1 Usable explanations | Add plain-language, source-linked explanations; independently verified operative correction by day 30 | Eligible person or case; family-linked analysis | Randomized offer above required notice; Δ>0 expected. Measure actual receipt separately. |
| H2 Source provenance | Display common origins of apparently separate reports; false-corroboration error on fixed-ground-truth tasks | Reviewer, with repeated task outcomes | Randomized simulation; Δ<0 expected. Field effectiveness requires a separate study. |
| H3 Review capacity | Add reviewer time and authority to change actions; verified correction within a prespecified deadline | Office; eligible cases nested within office | Randomize additional capacity where feasible; Δ>0 expected. Track case complexity and quality. |
| H4 Correction propagation | Add endpoint verification after correction; repeat adverse action based on superseded data within 90 days | Office or network; cases nested within cluster | Randomize additional verification; Δ<0 expected. Record spillovers and implementation fidelity. |

Fix eligibility, comparator, time zero, outcome, follow-up, estimand, adjudication protocol, and analysis before collecting test outcomes. Observational alternatives need justified exchangeability, positivity, consistency, and an explicit causal diagram; adjustment alone does not establish causation. [Hernán and Robins, Causal Inference: What If](https://miguelhernan.org/whatifbook).

## Illustrative sample-size planning

This example concerns **correction within 30 days**, not winning litigation. Assume baseline p0=.20, equal allocation, independent Bernoulli observations, two-sided α=.05, power=.80, and normal approximation without continuity correction. These are planning assumptions, not estimates from historical cases.

For p̄=(p0+p1)/2, approximate evaluable sample per arm:

\[
n=\left\lceil\frac{\left[z_{.975}\sqrt{2\bar p(1-\bar p)}+z_{.80}\sqrt{p_0(1-p_0)+p_1(1-p_1)}\right]^2}{(p_1-p_0)^2}\right\rceil.
\]

| Prespecified effect scenario | Evaluable per arm | Evaluable total | Independent enrollment with 15% attrition | Illustrative clustered enrollment total |
|---|---:|---:|---:|---:|
| 20% → 25%; +5 percentage points | 1,094 | 2,188 | 2,576 | 5,136 |
| 20% → 30%; +10 percentage points | 294 | 588 | 692 | 1,392 |
| 20% → 35%; +15 percentage points | 138 | 276 | 326 | 672 |

For clustered examples, assume 20 observed cases per office and intraclass correlation ρ=.05: DEFF=1+(20−1)ρ=1.95. Required offices per arm are ceil(1.95n/20): 107, 29, and 14. Enroll 24 per office to allow approximately 15% attrition, giving the displayed totals. This simple inflation is approximate: unequal cluster size, few offices, crossover, interference, baseline imbalance, and uncertain ICC require design-specific simulation and often larger samples. [CONSORT extension for cluster trials](https://doi.org/10.1136/bmj.e5661).

Reproduce these numbers with `python scripts/power_scenarios.py` from the repository root. The script uses only the Python standard library.

These scenarios are sensitivity planning, not three chances to obtain significance. Choose the smallest practically important effect before final power calculation. If four hypotheses are co-primary, adjust multiplicity and recalculate power; the table assumes one primary contrast. Do not keep adding observations or stop recruitment when p falls below .05. Use a fixed protocol or a separately specified sequential design with valid monitoring boundaries.

## Estimation, multiplicity, and release controls

The selected atlas receives **no population confidence intervals**: resampling the same selection cannot repair its sampling bias. For a suitable prospective independent binary sample, Wilson intervals can describe a single proportion; treatment contrasts require an appropriate interval for the contrast. For clustered designs, preserve offices or families in resampling and use design-aware methods with enough independent clusters. [NIST proportion-interval methods](https://www.itl.nist.gov/div898/handbook/prc/section2/prc241.htm).

Prespecify confirmatory primary outcomes and test families. For a separate planned exploratory screen, report every tested comparison and control false discovery rate at q=.05 using Benjamini–Hochberg only under its applicable dependence assumptions; use a justified alternative for more general dependence. A collection of charts is not automatically a collection of tests. Correction for multiplicity does not cure outcome leakage or biased sampling. [Armstrong, FDR adjustments](https://arxiv.org/abs/2209.13686).

Preserve public source URLs, extraction/version dates, docket and family IDs, inclusion reasons, coding disagreements, disposition stages, and explicit missingness. Reserve independent holdout data by family and, where appropriate, time or jurisdiction; never split linked opinions across discovery and test sets. Publish protocols, code, null results, deviations, and uncertainty with the findings. No result from this plan is a universal certification of safety or an automatic legal entitlement.
