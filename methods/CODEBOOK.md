# Case catalog codebook

Research snapshot: 11 September 2026. This repository presents public-case research and original analyst annotations for a selected historical catalog. The reviewed sources include judicial opinions and official implementation announcements. Source review is partial and case-specific; this is not an exhaustive legal citator, a certification of current law, a representative lawsuit dataset, or a court filing.

## Unit and denominator

The catalog contains **63 litigation-family records**, of which **62** represent individual people or represented human interests and are selected by default. **The T.J. Hooper** is retained as an organizational-plaintiff comparator and excluded by default. A family can encompass linked decisions or a settlement sequence. It is not a count of people, distinct injuries, independent systems, or all lawsuits involving an institution.

**Nineteen records identify actual habeas proceedings:** three in the initial catalog and sixteen added after targeted habeas research. They concern public custody in this selected set. This does not establish that every possible habeas respondent or custodial setting must be public. The “original” and “added” cohorts reflect research selection; they are not temporal treatment/control cohorts or training/test datasets.

Cahoo and Bauserman are separate litigation families involving the same **MiDAS** system. Their `system_group` is shared. Other dependence through precedent, institutions, related legal doctrines or historical circumstances remains possible even where group identifiers differ. Do not describe 62 records as 62 independent systems.

Brown I and II count once. Tumey and Ward, Hamdi and Boumediene, and SCHUFA and CK count separately. The Robodebt sequence counts once. Hamilton's 39 successful and three unsuccessful appeals are outcomes within one family; they are not 42 additional catalog records. Counts of affected people and money must not be pooled without independent definitions and denominators.

## Required record fields

| Field | Type / values | Meaning |
|---|---|---|
| `id` | Unique string | Stable record identifier; an identifier is not a legal citation. |
| `name`, `short` | Strings | Full case-family name and compact display label. |
| `year`, `last_year` | Integers | First and latest cited anchor years in this record; not necessarily filing, injury, release, or final case-closure years. |
| `country` | `US`, `UK`, `Australia`, `Netherlands`, `EU` | Jurisdictional grouping. EU decisions are comparative authorities, not binding US precedent. |
| `sector` | `Public`, `Private`, `Mixed` | Functional classification of the challenged consequential process. |
| `sector_note` | String | Basis and limits of sector classification. |
| `alternative_sector` | Sector value or `null` | A plausible alternate classification for sensitivity analysis; do not count both simultaneously. |
| `technology` | `Physical`, `Administrative`, `Computerized` | Coarse classification of the salient mechanism; categories do not imply that a malfunction was proved. |
| `direction` | `Favorable`, `Mixed`, `Adverse` | Claimant-relative direction of the latest cited disposition on the reviewed scope. |
| `stage` | `Damages judgment`, `Merits or injunction`, `Procedural or interim`, `Settlement`, `Mixed disposition`, `Adverse` | Display summary of the kind of disposition; exact relief remains in `summary` and `limit`. |
| `implementation` | `Documented some restoration`, `Not established in sources` | Whether the reviewed sources report some restoration anywhere in the recorded sequence. It is not a compliance or completeness score. |
| `restoration_note` | String | What was actually reported, when, and which inferences remain unsupported. |
| `plaintiff` | `Human`, `Represented humans`, `Organization comparator` | Affected claimant category used for the default comparator exclusion. This is not a claim that every named party is a natural person. |
| `tags` | Array of allowed topic labels | Nonexclusive analyst-coded topics of the challenge; not findings that every alleged defect occurred. |
| `summary`, `limit` | Strings | Disposition and essential qualifications. These should remain available next to aggregates. |
| `sources` | Array of `{label, url}` | Sources supporting the record. A link to a reproduced opinion supports the judicial text, not every editorial statement on the hosting page. |
| `cohort` | `original`, `added` | Research-selection cohort. |
| `habeas_vehicle` | String or `null` | Describes the actual habeas proceeding when established; blank values are not a complete adjudication of every proceeding in a person's history. |
| `system_group` | String | Known common-system link, with MiDAS explicitly joining Cahoo and Bauserman. |

## Sector: control and responsibility

**Public** means the challenged consequential rule, detention, adjudication, classification, or public service is controlled by a government institution. Logan remains public despite the private employer in its caption: the disputed forfeiture resulted from state adjudicatory procedures. Craft concerns a municipal utility.

**Private** means the challenged product, information service or consequential commercial practice is privately operated. SCHUFA and CK primarily concern private scoring and explanation duties even though proceedings involve regulators. Government regulation alone does not make a private product a mixed system.

**Mixed** means public power and private initiation or execution materially intersect in the challenged chain. Fuentes combines private-creditor assertions with state seizure. West combines a state custodial duty with contracted medical delivery. Boyle combines federal specifications with private equipment manufacture. Cahoo combines public adjudication and collection with supplier involvement. Hamilton combines enterprise technology and employer prosecution with criminal enforcement. These labels describe this analysis, not a judicial holding that every participant is a state actor.

Houston and Loomis are primarily public employment or sentencing decisions with material private scoring components; mixed alternatives are retained. CK has a mixed alternative because public enforcement of private disclosure duties matters. Alternative coding should be tested before attributing a pattern to sector.

## Technology: mechanism, not fault certification

- **Physical / forensic (data key `Physical`):** Physical products or equipment, forensic specimens or scientific methods, and drug-mediated evidence production. This includes the newer forensic habeas cases, not only product-liability litigation.
- **Administrative:** Institutional rules, evidence handling, classification, hearings, authority, capacity or correction procedures where no specific computerized operation is the salient issue.
- **Computerized:** A salient computerized score, record, inference, allocation or billing process. Human and organizational conduct remain part of every such system.

These are coarse, sometimes contestable, single-category annotations. The `Physical` category does not establish instrument malfunction; the `Computerized` category does not establish a code bug. A false evidentiary statement, wrong statistical interpretation, defective legal rule and hardware breakdown are different mechanisms.

## Outcomes, trajectories and actual relief

**Favorable** records a material claimant success at the cited stage. **Mixed** records material division among reviewed claims, claimants or forms of relief. **Adverse** records failure of the reviewed challenge at that stage. These are not a ranking of wellbeing or a probability that the system is safe.

An earlier win does not override a later cited loss. Accardi's 1954 hearing opportunity is retained in the narrative, but the latest cited 1955 dismissal is coded adverse. Cahoo is adverse for the cited 2023 officials' immunity appeal; supplier claims remained pending. Pending claims and a remand alone are not successful claims. `trajectory_note` is a proposed optional field for future releases to separate longitudinal histories from the latest-disposition field.

A hearing, review-access ruling, injunction, damages judgment, settlement, new trial, quashed conviction and physical release are different outcomes. In particular, **a conditional writ requiring retrial or release is not evidence that release actually occurred**. An innocence gateway allows further review; it is not itself exoneration. A settlement does not necessarily admit every alleged violation. Judicially recognized procedural rights do not establish complete operational compliance.

Five records report some restoration at some stage: Donaldson's earlier release, Thompson's earlier release and acquittal in the Connick history, convictions quashed in Hamilton, agency-reported Robodebt refunds/payments, and individual reversals and money returns recorded in Bauserman. These events differ in timing and scope. This coverage field tracks release, payment, or conviction correction; it does not count every lesser form of relief. For example, Mooney’s opinion reports an earlier death-to-life commutation, which is outside this stated coverage definition. The other 57 default records do not establish completed restoration in the reviewed source set; that does not mean no restoration occurred. **Five of 62 is a source-reporting count, not a compliance rate, human success rate or causal effect.** Prior release must not be attributed to a later judgment. The relevant sources are the [O'Connor opinion](https://supreme.justia.com/cases/federal/us/422/563/), [Connick opinion](https://supreme.justia.com/cases/federal/us/563/51/), [Hamilton judgment](https://caselaw.nationalarchives.gov.uk/ewca/crim/2021/577), [Robodebt implementation report](https://www.servicesaustralia.gov.au/robodebt-class-action-settlement), and [Bauserman opinion](https://law.justia.com/cases/michigan/supreme-court/2022/160813.html).

## Optional habeas and mechanism fields

The sixteen added records contain more detailed annotations. Missing optional fields in other records mean unreviewed or unavailable annotation, not false, zero or inapplicable.

| Field | Interpretation |
|---|---|
| `citation` | Legal citation, where separately recorded. |
| `data_failure` | Described information problem, which may be alleged or contested. Read with `data_status`. |
| `data_status` | Narrative distinguishing established findings, allegations, disputed classification, inaccessible information and other evidentiary status. The schema does not use `habeas_data_status`. |
| `holding_scope` | What the particular holding reaches and what remains undecided. |
| `actual_computer_fault` | For the added cases, `false` means no computer malfunction was identified as the basis of the reviewed holding. It does not certify all technology operated correctly or describe every event in the case. |
| `computer_fault_note` | Additional scope for the preceding field. |
| `actual_equipment_failure` | Where present and true, identifies an established physical-equipment failure. Francis concerns an unsuccessful electrocution; the precise component fault was not diagnosed. |
| `electronic_filing_issue` | Identifies a separate electronic-filing issue; it is not automatically the ground on which habeas relief was granted. |
| `computer_issue_scope` | Distinguishes the filing issue from the merits. In Han Tak Lee, the electronic-filing discussion preserved the state's appeal; habeas relief concerned unreliable forensic evidence. |
| `proposed_model` | An analyst's proposed engineering transfer, not an additional judicial holding. |

## Topic labels

Allowed tags are `Design and components`, `Evidence and data`, `Classification`, `Notice and hearing`, `Authority and rules`, `Capacity and delay`, `Incentives and independence`, and `Remedy access`. Tags are nonexclusive and reflect topics raised by a challenge. Their totals may exceed the number of records. An incentives tag does not establish corruption; a remedy tag does not mean relief was denied; an evidence tag does not establish intentional falsification.

## Permitted and unsupported analysis

The catalog supports descriptive counts, source inspection, chronology, case comparison, and exploratory grouping under disclosed coding choices. It does not support population success rates, estimates of how often public versus private systems fail, individualized litigation predictions, or causal effects of public ownership, automation or a proposed safeguard.

Selection around landmark victories, published decisions and salient failures creates selection bias. Era, jurisdiction, claim type, requested relief, procedural stage, legal doctrine, documentation availability and case dependence can all explain apparent clusters. Clustering topics and then observing outcomes may generate hypotheses; clustering on outcomes and claiming to have predicted those same outcomes is circular. Do not treat an arbitrary numerical ordering of categories as a meaningful metric distance.

For a new causal study, predefine a population, intervention, comparator, outcome and follow-up window; record confounders before outcomes; independently double-code a sample; retain disagreements and missingness; and distinguish case-family, person and system denominators. No causal design is supplied merely by a dashboard.

## Public-data boundary and maintenance

Public-facing case descriptions use public judicial or official source material and original analytical summaries. This methods directory does not include private manuscripts, user uploads, personal filings, confidential records or source attachments from the working session. Public availability of a court opinion does not eliminate the need to avoid unnecessary personal detail; the catalog uses case identifiers and details necessary to explain the legal mechanism.

Corrections should identify the record, disputed field, primary source and proposed replacement. Preserve earlier versions, record the research date, and update dependent visual counts. Current litigation requires checking subsequent history, applicable statutes and local procedure; this historical research does not perform that task for a particular litigant.
