## Team 1 Flu Shot Project — Concise Actionable Outline

### 1. Background & Urgency
- **Problem**: Seasonal influenza remains a major health risk for Hong Kong schoolchildren; participation in the School Outreach Vaccination Programme is still far below universal coverage, leaving large pockets unprotected.
- **Data gap**: Latest public figures stop at 2016–17 (18.7% uptake). We must request 2022–24 vaccination/absence data from the Department of Health (DH) to ground current analysis.
- **Action items**
  - Draft and send an official data request to DH (vaccination uptake, outbreaks, absenteeism by school level/district, 2022–24).
  - Collect recent media reports/community alerts on flu-related school incidents to evidence urgency.
  - Compile baseline indicators from available CHP press releases while waiting for updated DH data.

### 2. Objectives & Supporting Math Models
- **Objective A**: Pressure school principals to boost vaccination uptake through transparent accountability.
  - **Model #1 — School Vaccination Report Card**  
    - Based on Leung et al. 2017 school surveillance approach.  
    - Inputs: vaccination % (dose-level), URTI absenteeism, outbreak history, parent engagement metrics, eHealth enrollment.  
    - Outputs: “Prevention Readiness Score”, risk tiers, recommended interventions.  
    - Scenario simulations (synthetic data) show effect of improving uptake on absenteeism and outbreak probability.
- **Objective B**: Use eHealth-enabled analytics to measure vaccination effectiveness without onsite research teams.
  - **Model #2 — eHealth Test-Negative VE Model**  
    - Anchored on Lee et al. 2024 + Cowling et al. 2021 multi-season VE studies.  
    - Inputs: eHealth clinical encounters (lab-confirmed influenza vs negatives), vaccination status, demographic risk factors, school-level uptake.  
    - Outputs: strain-specific VE estimates, age group differentials, confidence intervals to communicate to parents/policymakers.
- **Action items**
  - Develop synthetic datasets mirroring Leung/Lee study structures to prototype both models.  
  - Draft methodological appendix describing assumptions, equations, and validation steps.  
  - Confirm with supervisors that these two models cover decision needs; adjust scope if required.

### 3. Data Requirements Driven by the Models
- **From DH**: school-level vaccination uptake (dose 1/2, outreach participation), lab-confirmed outbreak logs, URTI hospitalization/clinic visit data, historical absenteeism/outbreak correlations for calibration.
- **From EDB/Schools**: daily attendance and sick-leave reason codes, parent consent records, PTA engagement stats, timeline of school promotion activities, infrastructure readiness (nurse availability, venue capacity).
- **From HB/eHealth**: anonymized encounter-level data (vaccination status, diagnoses, lab results, timestamps), linkage keys/pseudonyms, API specifications, eHealth enrollment counts by school district.
- **Action items**
  - Incorporate these data fields into the DH data request letter and school survey template.  
  - Define data quality thresholds (e.g., acceptable missingness, reporting lag) necessary for the models to run reliably.  
  - Prepare draft data dictionaries and sample submission formats for each stakeholder.

### 4. Ideal Data Governance Scheme (Target State)
- Unified protocol mandating: standardized data fields,  weekly submission cadence, automated validation, shared dashboards accessible to DH, EDB, HB, and participating schools.
- eHealth integration: automatic syncing of vaccination/diagnosis events to school dashboards; privacy-preserving linkage to attendance data.
- Enforcement: KPIs embedded in school quality reviews, funding incentives for high compliance, escalation process for chronic underperformers.
- **Action items**
  - Design architecture diagram (data sources, pipelines, dashboards, governance roles).  
  - Draft policy brief outlining legal basis and resource requirements for the unified scheme.  
  - Identify quick wins (e.g., pilot integration for a subset of schools) to demonstrate feasibility.

### 5. Objective A — Pressure Principals via Data-Driven Accountability
- **Goal**: Through improved governance, create transparent incentives/penalties that push principals to raise vaccination uptake.
- **Key components**
  1. **School Vaccination Report Card Model (Model #1)**  
     - Inputs: vaccination uptake %, absenteeism due to upper respiratory infections, outbreak history, parent engagement metrics.  
     - Outputs: composite “Prevention Readiness Score” benchmarked across schools; triggers for DH/EDB follow-up.  
     - Use synthetic data to show how increased uptake lowers sickness absence; scenario analysis for different thresholds. Anchor design on the school-based surveillance methods from Leung et al. 2017 (Influenza Other Respiratory Viruses).
  2. **Stakeholder Engagement Loop**  
     - Dashboards for principals/PTAs; monthly alerts for schools falling below targets; recognition or resource allocation linked to scores.
  - **Action items**
    - Define minimal dataset schools must submit (fields, format, cadence).  
    - Build synthetic dataset mirroring typical school metrics to calibrate the report card model.  
    - Draft accountability mechanisms (public dashboards, school development plan requirements, incentive grants).

### 6. Objective B — eHealth-Enabled Vaccine Effectiveness Assessment
- **Goal**: Leverage eHealth to monitor vaccination effectiveness without dispatching research teams to every school.
- **Key components**
  1. **eHealth Test-Negative Effectiveness Model (Model #2)**  
     - Use anonymized eHealth clinical encounters + school-level vaccination data to estimate flu vaccine effectiveness (VE).  
     - Synthetic dataset to demonstrate methodology (link vaccination status, lab-confirmed flu diagnoses, demographics). Structure analysis on test-negative VE frameworks used by Lee et al. 2024 (Vaccine X) and related HK hospital studies.
  2. **Governance Scheme**  
     - Automate data exchanges between eHealth, DH surveillance, and EDB attendance systems; establish privacy-preserving identifiers.
  - **Action items**
    - Specify data-sharing protocol (consent, encryption, role of HB).  
    - Design synthetic microdata to test the VE analysis pipeline (R/Python notebook).  
    - Propose incentives to boost eHealth enrollment (e.g., streamlined consent via schools, link to report card scoring).

### 7. Evidence Strategy & Messaging
- **Reference evidence for modeling choices**
  - School surveillance VE: Leung et al., *Influenza Other Respiratory Viruses* 2017 — prospective multi-school sampling + test-negative analysis.
  - Hospital VE and eHealth relevance: Lee et al., *Vaccine X* 2024; Cowling et al., *Vaccine* 2021 — show dependency on integrated vaccination + clinical data.
  - Governance & forecasting context: Ali & Cowling, *Annu. Rev. Public Health* 2021 — highlights need for unified data streams to power decision models.
- **Pressure principals**: Use model outputs to show cost of inaction (higher sick leave, potential reputational penalties); recommend KPIs tied to quality assurance reviews.
- **Convince parents**: Use transparent dashboard + eHealth data to highlight effectiveness, contrast vaccinated vs non-vaccinated absenteeism and hospitalization risks.
- **Action items**
  - Prepare data visualizations connecting vaccination to absence reductions.  
  - Craft parent-facing briefs summarizing VE findings and eHealth benefits.  
  - Outline media/communication plan coordinated with DH/EDB.

### 8. Project Workplan & Deliverables
1. **Week 1–2**: Data requests, current-state mapping, synthetic data design.
2. **Week 3–4**: Build Model #1 (report card) and Model #2 (eHealth VE) using synthetic data; validate assumptions with supervisors.
3. **Week 5–6**: Draft policy proposals (governance scheme, accountability levers, eHealth integration) with supporting visuals.
4. **Week 7**: Stakeholder-ready report, executive summary, and presentation deck.

- **Team assignments (to confirm)**
  - Data request & governance mapping: [Name]
  - Synthetic datasets & modeling: [Name]
  - Policy & communications package: [Name]

### 9. Immediate Next Actions Checklist

### 10. Diagnose Government Practices & Close the Governance Gap
- **Key questions to DH / EDB / HB**
  1. What data standards and sharing agreements currently exist for influenza vaccination and absenteeism reporting?
  2. How frequently do DH and EDB exchange school vaccination/absence data, and what systems/formats are used?
  3. What prevents schools from uploading vaccination rosters or linking to eHealth IDs today?
  4. Can DH provide historical absenteeism tied to outbreaks to validate report-card thresholds?
  5. What legal/privacy constraints limit eHealth data use for aggregated VE analysis, and what consent mechanisms are acceptable?
- **Gap assessment**
  - Compare responses to the ideal governance scheme; document discrepancies in data availability, latency, standards, and enforcement.
  - Quantify the impact of the gap using the two models (e.g., simulation showing lost vaccination uptake or unmeasured VE when data is missing).
- **Argument framing**
  - If DH/EDB/HB close the gap (align to target state), we can implement the two models, pressure principals, and give parents trustworthy VE evidence; therefore, bridging the gap is a prerequisite for protecting schoolchildren.
- **Action items**
  - Prepare structured interview/questionnaire for agencies.  
  - Populate gap analysis matrix once responses are received.  
  - Integrate findings into final recommendations and advocacy strategy.
- [ ] Finalize DH data request letter (include vaccination, absenteeism, outbreak metrics).  
- [ ] Schedule alignment meeting with supervisors to confirm scope of two models.  
- [ ] Set up shared workspace for synthetic data modeling (Git/Notebook).  
- [ ] Draft template for school report card dashboard.  
- [ ] Outline eHealth data-sharing policy brief.

