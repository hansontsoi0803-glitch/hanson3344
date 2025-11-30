# Team 1 – Flu Shot Project: Updated Outline & Data Governance Plan

_Last updated: 18 Nov 2025_

## 1. Objectives & Storyline Refresh
- **Pressure + Support**: Provide every principal with a “report card” showing (a) vaccination uptake vs. comparable schools and (b) upper respiratory absence rates; pair this with concrete support (templates, data workflow, eHealth push).
- **Evidence-based ask**: Show that Hong Kong already has precedents for school-based VE surveillance (Leung 2017) and that similar designs overseas (Wang 2013) can run if data governance gaps are closed.
- **Two deliverables** for Presentation 2 (Week 11):
  1. **Pilot report card pack** (mock dashboard + data request memo).
  2. **Data governance blueprint** that enables routine school-based VE studies without deploying field teams.

## 2. Presentation 2 (Week 11) Outline
1. **Hook (Ophelia)** – 1 slide on the latest CHP figures + reminder that two school-aged deaths triggered public anxiety; principals still rely on guesswork.
2. **What the literature shows (Eric)** – Summarise Leung 2017 (623 HK students, bi-weekly swabs, VE 42–52% for ILI; data needs: repeated FNPS, parent consent, vaccination verification) and Wang 2013 (case-control in 44 schools, VE 83%; needs immunisation cards, classmate controls). Emphasise that both studies were feasible because schools cooperated on data entry.
3. **Gap analysis (Aries)** – Contrast those requirements with HK’s current silos: no standardised principal reporting, eHealth adoption stalled at ~60%, vaccination records stored as free text, illness absences not linked to vaccination.
4. **Our proposal (Jackson)**  
   - Report card data flow: school MIS → Education Bureau hub → CHP analytics → returned dashboards.  
   - VE surveillance flow: schools upload line lists (vaccination status, ILI episodes, rapid-test results) to CHP secure portal; CHP cross-matches with eHealth (dose lot, date) and HA (hospitalisations).
5. **Policy call (Hanson)** – Ask LegCo/CHP for:
   - Mandated monthly uploads of vaccination & respiratory absence numbers via eHealth APIs.
   - Funding for a joint DOH/Edu Bureau data team + minimum eHealth adoption targets (≥90% of students syncing cards by 2026).
   - Permission to publicly share anonymised school report cards to create peer pressure.

## 3. Insights from School-Based VE Studies & Governance Implications
| Study | Design & Key Data Needs | Data Governance Improvements for HK |
| --- | --- | --- |
| `Influenza Resp Viruses - 2017 - Leung` | Prospective cohort of 623 HK students, bi-weekly nasopharyngeal swabs, parental questionnaires, verified vaccination records, linkage to PCR labs. | - Create a CHP-managed consent + specimen scheduling platform so schools only manage logistics.<br>- Standardise digital vaccination verification (eHealth QR + clinic uploads).<br>- Automate lab result feedback to schools/parents within 48h. |
| `Single-dose varicella vaccine effectiveness in school settings in China` | Matched case-control (180 cases/679 controls) across 44 schools; relied on home immunisation cards and classmate matching to estimate VE=83%. | - Require schools to maintain digitised class lists with vaccination status flags.<br>- Allow CHP to query attendance/absence data to auto-select controls.<br>- Mandate storage of immunisation card images in eHealth so verification does not depend on paper. |

**Proposed governance enablers**
1. **Unified School Health Data Hub**: DOH + EDB host a secure data lake (students anonymised ID, vaccination dates, ILI episodes, absence reasons, hospital referrals). Access tiers: school (own data), EDB (district view), CHP (territory view).
2. **Standardised data dictionary**:  
   - Vaccination fields: vaccine type, dose #, lot, date, provider.  
   - Illness fields: ILI symptom checklist, test type, result, absence duration, hospitalisation indicator.  
   - Context: class ID, grade, special programmes (SEN, boarding, etc.).
3. **eHealth Auto-Sync Mandate**: Link student ID → eHealth ID → HA/clinic data. Schools only need to confirm consent; the platform ingests dose data automatically.
4. **Rapid ethics + consent workflow**: Pre-approved templates for prospective surveillance so schools can opt-in quickly when CHP activates a cohort (reduces 6–8 week lag seen in Leung 2017 recruitment).

## 4. Data Collection Blueprint
### 4.1 Principal Report Cards
| Data Element | Source & Action |
| --- | --- |
| Vaccination uptake (%) by grade and by vulnerable groups | eHealth sync + school MIS; monthly auto-ingest. |
| Upper respiratory absence rate (per 1,000 student-days) | School attendance system, tagged reason codes. |
| Severe outcomes (A&E visits, hospitalisations) | Hospital Authority API (de-identified) matched via eHealth ID. |
| Peer benchmarks | EDB hub calculates percentile vs. district & HK-wide averages. |
| Narrative prompts | Auto-generated insights: “Your P3 vaccination rate dropped 8 pts since September; peers improved by +4.” |

### 4.2 Vaccination Effectiveness Assessment
1. **Minimal dataset** (aligned with Leung + Wang):
   - Student pseudonymised ID, age, class, chronic conditions.
   - Vaccination history with lot/date (from eHealth).
   - ILI episodes with onset date, symptoms, testing info (RAT/PCR).
   - Absence duration + outcome (recovered, hospitalised).
2. **Workflow**:
   - Schools upload weekly CSV (or API push).  
   - CHP runs automated test-negative or matched case-control analysis per season; outputs VE estimates within 2 weeks of season end.  
   - Results fed back to schools + EDB for targeted support.
3. **Quality controls**:
   - Automatic validation (missing vaccination fields flagged).  
   - Random audits: CHP cross-checks 5% of entries with clinic records.  
   - Incentives: schools with ≥95% data completeness qualify for additional outreach nurse hours.

## 5. Feedback on Presentation 1 Script
| Issue | Evidence | Fix for Presentation 2 |
| --- | --- | --- |
| Fragmented storyline (jumped from VE to eHealth to causal model) | Noted by both Simon & Talia in transcript (`Course_Docs/Presentation1/Team1_FluShot.md`). | Follow the new outline; each speaker references the same two deliverables. Provide transitions (“Now that we know VE studies are feasible, here’s how we build the data pipes”). |
| Outdated data (2016–17 uptake) | Simon asked to contact CHP for 23/24 numbers. | Assign Hanson to chase CHP/EDB for the latest vaccination + absence stats; even a partial response should be quoted. |
| Lack of concrete literature references | Talia: “we need to look at previous studies” | Insert 2–3 slides summarising Leung (HK data) and Wang (China case-control) with citations. |
| Insufficient explanation of math model relevance | Audience could not see link to practical action. | Frame models as tools to rank schools or optimise incentive schemes; show a mock output (e.g., linear program recommending where to deploy outreach nurses). |

## 6. Team Member Tasking (Next 7 days)
| Member | Primary Deliverable | Specific Tasks |
| --- | --- | --- |
| **Ophelia – Intro & Governance Context** | Slide pack sections 1 & 3 | - Draft hook slide with latest CHP data.<br>- Write 1-page memo summarising principal pain points + quote from commentsSimon (`01_Project_Report/commentsSimon.md`). |
| **Eric – Literature & Model Lead** | Slide pack section 2 + model appendix | - Produce 2-slide summary of Leung 2017 and 1-slide summary of Wang 2013, highlighting data requirements.<br>- Update model notebook to show how report card metrics feed into optimisation (include screenshot for appendix). |
| **Aries – Data Blueprint & Report Cards** | Slide pack section 4 (data workflows) | - Build mock report card (Canva or Google Slides).<br>- Document the weekly data upload spec (fields + validation) leveraging `06_Data_Analysis_Governance_Review/dataRequirement.md`. |
| **Jackson – Policy & Incentives** | Slide pack section 5 (policy asks) | - Draft policy brief for LegCo panel secretary focusing on data-sharing mandate + eHealth adoption incentives.<br>- Coordinate with Eric on quantifying resource ask (e.g., cost of data hub). |
| **Hanson – Action & Comms** | Closing remarks + external outreach | - Contact CHP/EDB for updated vaccination + absence statistics; log responses in `02_Data_Collection/govEnquiries/`.<br>- Draft email copy for principals introducing the upcoming report card pilot and eHealth sync instructions. |

## 7. Next Steps & Deadlines
1. **By Thu (Noon)** – Each member uploads draft slides/notes to the shared Google Drive (link in `05_Project_Admin_Tutoring/adminFluShot.md`).
2. **Thu Evening** – Internal rehearsal; sanity-check storyline flow.
3. **Fri** – Send policy brief + updated govt enquiry to Simon/Talia for feedback; refine slides over weekend.
4. **Mon (Presentation Week)** – Final slide integration + rehearse transitions emphasizing the two concrete deliverables.

---
_Prepared for storage in `Team1_FluShot/05_Project_Admin_Tutoring/`. Please keep this document updated as tasks progress._

