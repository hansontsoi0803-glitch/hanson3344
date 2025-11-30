## Team 1 Flu Shot Project — Actionable Outline v2 (Objective-Centric)

### 0. Background & Problem Statement
- **Risk**: Seasonal influenza continues to sideline Hong Kong schoolchildren; outreach vaccination coverage remains far from universal.
- **Data gap**: Latest public numbers (18.7% in 2016–17) are outdated. Updated 2022–24 vaccination + absentee data from DH is essential.
- **Immediate actions**
  1. File formal DH data request (vaccination uptake, outbreaks, URTI absenteeism by school level/district).
  2. Compile recent media/CHP alerts highlighting ongoing outbreaks.
  3. Assemble baseline dataset from available CHP press releases while awaiting DH response.

---

### Objective A — Pressure Principals via School Vaccination Report Card
**Goal**: Make principals accountable by comparing vaccination performance and URTI-related absenteeism across schools.

1. **Math Model & Analytics**
   - Hypothesis: higher vaccination rate → lower URTI absentee rate.
   - Model: Linear/log-linear regression `URTI_absence = β0 + β1 * vaccination_rate`.
   - Leaderboard: rank schools by vaccination %, absenteeism, and composite “Protection Score”; publish quartile badges (Gold/Silver/Amber/Red).
   - Evidence base: Leung et al. 2017 school surveillance (test-negative approach) + synthetic dataset (`data/synthetic_school_report_card.csv`).

2. **Data Needed**
   - Weekly vaccination % (dose 1/2) by class; outreach participation logs.
   - Daily absenteeism by reason (URTI/influenza).
   - Engagement signals: PTA attendance, parent info sessions, communications volume.
   - eHealth enrollment counts to verify vaccination claims.

3. **Governance & Accountability**
   - Schools upload standardized CSV/API feeds; DH/eHealth push confirmation feeds.
   - Automated checks for data quality; random audits vs eHealth records.
   - Dashboards: principal view (scatter plot, rank, alerts), EDB command center (heatmap, action tracker), optional parent badge.
   - Pressure levers (EDB): integrate into School Development & Accountability (SDA) reviews, principal appraisal, Quality Assurance inspections, and funding/extra nurse support linkage.

4. **Deliverables**
   - Report card methodology memo (math description + visuals).
   - Sample dashboard (including `figures/vaccination_vs_absence.png`, `figures/vaccination_leaderboard.png`).
   - Policy note outlining EDB enforcement triggers.

---

### Objective B — Assess Vaccine Effectiveness via eHealth-Enabled Test-Negative Analysis
**Goal**: Demonstrate vaccine effectiveness (VE) without on-site research teams by leveraging eHealth + school data.

1. **Math Model & Analytics**
   - Test-negative design (conditional logistic regression) using hospital/clinic encounters recorded in eHealth.
   - Inputs: vaccination status (verified via eHealth), lab-confirmed influenza vs negative tests, demographic risk factors, school-level vaccination coverage.
   - Outputs: VE (%) by strain (A(H3N2), A(H1N1), B) and age group; sensitivity analyses for time since vaccination.
   - Evidence base: Lee et al. 2024 (*Vaccine X*), Cowling et al. 2021 (*Vaccine*).

2. **Data Needed**
   - eHealth encounter data (diagnosis, lab results, vaccination timestamps) with school/district tags via consent/pseudonyms.
   - DH surveillance context (circulating strains, epidemic periods).
   - School outreach rosters to link uptake with VE results.

3. **Governance & Implementation**
   - HB manages secure data exchange; define consent workflow for parents to link eHealth accounts with school IDs.
   - DH consolidates VE outputs and shares dashboards with EDB/principals to reinforce urgency.
   - Incentives: highlight VE findings in parent communications; tie eHealth enrollment progress to report-card scoring.

4. **Deliverables**
   - Analytical protocol + synthetic data proof-of-concept.
   - eHealth data-sharing policy brief (privacy, consent, APIs).
   - Messaging pack translating VE results for parents and policy makers.

---

### Cross-Cutting: Ideal Data Governance → Gap Analysis
1. **Target State**
   - Unified data hub combining school uploads, DH surveillance, and eHealth confirmations.
   - Weekly cadence, standardized fields, automated validation, role-based dashboards.
   - Clear accountability: schools (data entry + action plans), DH (analytics & oversight), EDB (enforcement), HB (eHealth integration).

2. **Questions for Government Agencies**
   - DH: What current datasets and refresh cycles exist for school vaccination & outbreaks? Are there legal barriers to sharing school-level data?
   - EDB: Are attendance reason codes standardized? How can report-card metrics plug into SDA/QA processes?
   - HB/eHealth: What consent, technical architecture, and privacy safeguards are needed to produce school-linked vaccination stats?

3. **Gap Assessment & Advocacy**
   - Compare actual responses vs target-state requirements; document missing data fields, latency, or policy tools.
   - Use Objective A/B models to quantify impact if gaps remain (e.g., inability to verify vaccination, lack of VE evidence).
   - Conclude: closing the governance gap is necessary to protect students and meet both objectives.

---

### Workplan & Ownership
| Week | Key Tasks | Owners (TBD) |
|------|-----------|--------------|
| 1 | Submit DH/HB/EDB data requests, finalize data dictionaries | Data/Governance lead |
| 2–3 | Build synthetic datasets, run regression/leaderboard + VE prototypes | Modeling lead |
| 4 | Draft governance architecture + dashboard wireframes | Gov/Data lead + Designer |
| 5 | Compile policy briefs (report card enforcement, eHealth integration) | Policy/Comms lead |
| 6–7 | Integrate analyses into final report, presentation, and advocacy materials | All |

---

### Immediate Next Steps Checklist
- [ ] Finalize DH data request letter (vaccination, absenteeism, outbreak metrics).  
- [ ] Prepare questionnaires for EDB and HB/eHealth on data standards and consent requirements.  
- [ ] Build/update synthetic datasets for Objectives A and B; rerun regression/VE proofs.  
- [ ] Draft storyboard for dashboards (principal, EDB, parent).  
- [ ] Schedule supervisor check-in to validate scope and messaging for both objectives.

