# From observed failure to a testable legislative proposal

Version 1.0 · 11 September 2026 · **Discussion draft; proposed controls remain untested.**

This document translates research questions into a bounded federal-agency pilot. It is not enacted law, a complete introduction-ready bill, a finding of general governmental liability, or a universal route to habeas relief. Its four interventions are available as machine-readable records in [interventions.json](../data/research/interventions.json); study design is specified in the [analysis plan](../methods/ANALYSIS_PLAN.md).

## Preserve the chain from evidence to proposal

Every proposed requirement needs separate entries for a source-supported finding, an analyst's inference, a countermeasure, a test, an outcome, and a proposed clause. A selected historical victory does not validate a modern intervention.

| Source-supported finding | Engineering inference—not an additional court holding | Proposed countermeasure | Test and measured outcome | Draft clause |
|---|---|---|---|---|
| In *Miller v. Pate*, paint was knowingly presented as blood; the Court invalidated the conviction. | Data integrity must include the relationship between a representation and its underlying evidence. | H1: source-linked explanations and a usable challenge path. | Randomized additional assistance; independently verified correction within 30 days. | §2(b) |
| *Kyles v. Whitley* required cumulative consideration of suppressed favorable evidence. | Review should preserve contradictory evidence and distinguish independent origins from repeated assertions. | H2: provenance display with common-origin warnings. | Randomized fixed-ground-truth simulation; false-corroboration errors per eligible task. | §2(a), §3(a) |
| *Accardi* initially obtained a hearing; the later decision accepted independent administrative discretion. | An opportunity for review and a favorable final result are different states. Capacity and authority require separate measurement. | H3: additional reviewer time and authority within the agency's lawful powers. | Office-level randomized additional capacity; timely verified correction. | §3(b) |
| *Han Tak Lee* obtained conditional habeas relief based on discredited arson-science foundations. The reviewed opinion does not establish that every downstream record was corrected. | A remedy order leaves a separate implementation question. | H4: endpoint verification and recurrence monitoring. | Cluster-randomized additional verification; repeated adverse action using superseded data within 90 days. | §4(b)–(c) |

Primary opinions: [Miller](https://supreme.justia.com/cases/federal/us/386/1/), [Kyles](https://supreme.justia.com/cases/federal/us/514/419/), [Accardi 1954](https://supreme.justia.com/cases/federal/us/347/260/), [Accardi 1955](https://supreme.justia.com/cases/federal/us/349/280/), [Han Tak Lee](https://www2.ca3.uscourts.gov/opinarch/143876p.pdf). These are mechanism-generating historical analogies, not causal evaluations of H1–H4.

## Existing foundations and the proposed addition

The Privacy Act already provides covered individuals with access and amendment procedures and imposes accuracy, relevance, timeliness, and completeness requirements for agency records used in determinations. It has defined coverage and exemptions; it is not a universal all-person, all-record correction statute. [5 U.S.C. §552a(a), (d), (e)(5), (j), (k)](https://www.law.cornell.edu/uscode/text/5/552a).

The APA requires prompt notice of certain denials and, subject to its exceptions, a brief statement of grounds. Section 702 addresses judicial review and nonmonetary relief while preserving other limitations. The pilot below adds operational documentation, testing, and verification duties within its scope; it does not claim these sections already require every proposed control. [5 U.S.C. §555(e)](https://www.law.cornell.edu/uscode/text/5/555), [§702](https://www.law.cornell.edu/uscode/text/5/702).

Federal review of state custody remains subject to the applicable habeas framework, including §2254 standards and §2244 limitations and successive-petition provisions. A dashboard score neither changes these rules nor authorizes an agency to disregard a court order. [28 U.S.C. §2254](https://www.law.cornell.edu/uscode/text/28/2254), [§2244](https://www.law.cornell.edu/uscode/text/28/2244).

## Public Decision Evidence and Correction Pilot Act

**The following four sections are proposed legislative language. All deadlines and scope choices are drafting choices for review.** Appropriations, agency-specific amendments, enforcement, and legislative counsel review remain necessary before introduction.

### Section 1. Scope, administration, and preservation of rights

(a) Subject to appropriations, the Director of the Office of Management and Budget shall designate participating executive agencies for a 24-month pilot concerning administrative benefit and eligibility decisions. A covered decision includes an agency action or failure to act that materially determines an identified person's access to a covered benefit. Contractor-operated components used to make or implement that decision are included in the agency's inventory and contractual audit requirements.

(b) Every natural person affected by a covered decision shall have access to the pilot's challenge process regardless of citizenship, language, disability, or access to technology. This is a proposed pilot entitlement and does not restate the narrower definition of “individual” in the Privacy Act. Existing lawful eligibility rules remain subject to their governing law; identity attributes shall not substitute for evidence supporting a decision.

(c) No pilot assignment shall diminish required notice, review, representation, accommodations, or substantive rights. No experimental system shall determine criminal guilt, impose custody, remove a child, or override a judicial order under this Act. If correction requires judicial action, the responsible agency shall preserve relevant records and promptly seek relief through authorized procedures. Participation shall not require waiver of a claim or appeal.

(d) The agency inspector general shall oversee an evaluation team institutionally separate from implementation management. The protocol shall disclose conflicts, protect confidential information, and publish de-identified methods and aggregate results. This draft creates no new damages action and does not displace otherwise available review; a final bill must resolve enforcement expressly.

### Section 2. Evidence, understandable notice, and error classification

(a) Each covered decision shall retain a versioned evidence manifest identifying the asserted fact, source, collection method, relevant event time, receipt time, transformation history, applicable rule version, responsible decision function, and known contradiction or uncertainty. Linked reports sharing a source shall be identified as such. The agency shall preserve corrections and superseded versions according to applicable records law without presenting a superseded assertion as current fact.

(b) The affected person shall receive an accessible explanation identifying the material grounds, review route, applicable deadlines, and evidence they may lawfully inspect. A protected source may be withheld only under applicable authority; the agency shall record the basis and provide whatever explanation and review access the law permits. Plain-language and machine-readable versions shall correspond. A requested readback or translation check shall verify meaning without making agreement a condition of service.

(c) Review records shall classify identified discrepancies as identity linkage, factual evidence, provenance duplication, temporal order or staleness, translation or meaning, statistical inference, rule application, authorization, transmission or storage, equipment, capacity or delay, or correction propagation. Each classification shall include status—alleged, disputed, established, corrected, or unresolved—and supporting evidence. Multiple classifications may apply. Uncertainty shall not be silently converted into certainty.

These proposed controls extend existing records and notice foundations. Audit, configuration, and information-integrity controls offer implementation components, not proof that the recorded claim is true. [5 U.S.C. §552a](https://www.law.cornell.edu/uscode/text/5/552a), [NIST SP 800-53 Rev. 5, including the release 5.2.0 notice](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final).

### Section 3. Verification before use and usable correction capacity

(a) Before a new pilot component affects live decisions, independent evaluators shall test the specified requirements and validate performance with representative users and operational conditions. Tests shall include incorrect identity matches, common-source repetition, misleading statistics, ambiguous translation, stale records, lost acknowledgments, overload, and equipment unavailability. Test data shall be synthetic or lawfully obtained and protected. A requirement-to-test-to-result matrix shall record configurations, observed failures, residual risk, and corrective retesting.

(b) Each agency shall designate a reviewer with adequate time, access to material evidence, and lawful authority to correct covered decisions. A vendor's recommendation or a role title alone shall not establish evidentiary truth. Published procedures shall route unresolved matters to a person authorized to act; a referral without acceptance shall remain open.

(c) Before outcome collection, evaluators shall timestamp the primary hypotheses, eligibility rules, time zero, estimands, comparison design, sample-size assumptions, missingness treatment, stopping rules, and multiplicity plan. Additional safeguards may be randomized; required protections may not. H2 shall begin in simulation. A protocol shall define suspension triggers for attributable serious harm or a failure to contain a known critical error. Passing a finite test suite shall not constitute a guarantee of zero harm.

NASA distinguishes requirements verification from operational validation and includes the human interfaces in testing. NIST AI RMF supports documented testing before deployment, independent assessment, and continuing monitoring. These sources inform the proposed approach; they do not endorse this bill or transfer flight certification to government. [NASA verification](https://www.nasa.gov/reference/5-3-product-verification/), [NASA validation](https://www.nasa.gov/reference/5-4-product-validation/), [NIST AI RMF 1.0, MEASURE](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf).

### Section 4. Deadlines, completed correction, and public evaluation

(a) A participating agency shall acknowledge a challenge within five business days and record its determination and, when warranted and within its authority, operative correction within 30 calendar days of receipt. These are proposed maximum pilot periods; any shorter legal deadline controls. Where an imminent serious harm is alleged, a designated official shall assess urgency immediately and no later than 24 hours. A deadline is not permission to postpone an earlier necessary response. Delay shall trigger independent escalation, notice of reasons, interim protective measures within lawful authority, and a dated completion plan; repeated requests shall not reset the original clock.

(b) For an established correction, the agency shall identify all known operative endpoints, transmit the versioned correction lawfully, obtain a receipt, and independently verify each endpoint's operative state. Receipt alone shall not establish completion. Failed delivery, an unknown endpoint inventory, or a continuing court constraint shall be recorded as unresolved; the record shall identify the official responsible for the next lawful action. Contradictory evidence shall remain available to authorized reviewers.

(c) Evaluators shall monitor repeat adverse actions based on superseded data for 90 days after the defined correction event. Quarterly aggregate reports shall publish denominators, missing follow-up, case complexity, correction latency, residual errors, accessibility, adverse effects, and cost. No person shall receive lower protection because a group is expensive to serve. Final recommendations shall report null and adverse findings and identify which proposed obligations the evidence supports, rejects, or leaves unresolved.

## Measurement contract for code and dashboards

These are proposed operational definitions. Thresholds require policy justification and empirical validation; they are not physical constants or existing universal legal standards. Zero harm is an objective, not a statistically demonstrated property of this atlas.

| Metric | Computation | Unit and interpretation |
|---|---|---|
| Timely verified correction | `R_D = count(eligible cases corrected and independently verified by D) / count(all eligible cases)` | Proportion; report percentage, missingness, and denominator. Define eligibility independently of treatment. Unknown verification is not a verified success. |
| Correction latency | `T_i = t_verified_i - t_receipt_i` | Hours; report median, p95, and unresolved cases separately. Never discard unresolved cases to claim fast service. |
| Endpoint coverage | `C_i = verified operative endpoints / inventoried required endpoints` | Proportion conditional on a verified inventory. Zero or unknown denominator gives “not estimable,” never 100%. |
| False corroboration | `F = erroneous independent-source judgments / eligible ground-truth tasks` | Errors per task; simulation reference truth and adjudicator uncertainty documented. |
| Recurrence | `Q_90 = cases with repeat superseded-data action by day 90 / baseline eligible corrected cases` | Proportion, with loss to follow-up and competing events reported. |
| Review load | `rho = lambda / (c * mu)` | Dimensionless; arrival rate in cases/hour, service rate per reviewer in cases/hour, `c` available reviewers. Approximation assumes comparable work and capacity; `rho < 1` does not certify safe delay. |
| Intervention effect | `Delta = P(Y=1 | assigned intervention) - P(Y=1 | assigned comparison)` | Percentage-point difference after multiplying by 100; design-aware interval and fixed outcome required. H0: Delta = 0; two-sided H1: Delta != 0. |

For timestamp differences, retain event and ingestion times, timezone, clock source, ordering evidence, and estimated clock uncertainty. A timestamp discrepancy smaller than that uncertainty does not establish sequence. The formulas specify analysis requirements; operational data for most metrics have not yet been collected.

## Human, machine, and hybrid implementation

The EE analogy separates sensing from action: **observability** asks whether the available evidence distinguishes a valid state from a dangerous one; **controllability** asks whether an authorized intervention can actually reach the required corrected state. These are design questions here—not a claim that human institutions satisfy a linear state-space model.

A human control is an accessible readback with source inspection; a machine control is schema, version, integrity, and endpoint checking; a hybrid control combines these with an independent reviewer able to change the operative action. Readback detects transmission or meaning mismatch only if compared against a reliable reference. It cannot make a false source true. A CRC verifies a defined relationship among bytes; neither a matching CRC nor a cryptographic digest proves factual truth. [RFC 1952, CRC32 field](https://www.rfc-editor.org/rfc/rfc1952).

Before expansion, require an auditable trace from **claim → source → rule → decision → challenge → authorized correction → verified endpoint state**. Keep the evidence, metric, legal authority, and test result distinct. That trace makes a proposed remedy testable; it does not predetermine its success.
