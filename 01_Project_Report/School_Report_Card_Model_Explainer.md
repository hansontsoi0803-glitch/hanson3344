## School Report Card Model Explainer

### 1. Concept Overview
To hold principals accountable, we compare each school’s influenza vaccination rate with its URTI-related absenteeism. The underlying hypothesis, supported by Leung et al. (2017, *Influenza Other Respiratory Viruses*), is that higher vaccination coverage among students reduces mild influenza infections and thus sick leave. Our report-card model adds a leaderboard layer to create peer pressure: schools with high vaccination and low absenteeism receive higher “Protection Scores,” while laggards are flagged for intervention by the Education Bureau (EDB).

### 2. Mathematical Approach
We fit a simple regression:

$$
\widehat{\text{URTI Absence}}_i = \beta_0 + \beta_1 \cdot \text{VaccinationRate}_i
$$

where:
- $ \text{URTI Absence}_i $ is the percentage of students in school $i$ who take sick leave due to URTI.
- $ \text{VaccinationRate}_i $ is the school’s influenza vaccination percentage.
- $ \beta_0, \beta_1 $ are coefficients estimated from data.

This reflects the negative relationship highlighted in Leung et al.’s school surveillance, where vaccinated cohorts had lower ILI incidence. We also draw on Lee et al. (2024, *Vaccine X*), which demonstrates how higher coverage improves vaccine effectiveness in Hong Kong’s school outreach program, further justifying the accountability link.

### 3. Applying the Model with Synthetic Data
Dataset: `data/synthetic_school_report_card.csv`

Columns: school name, vaccination rate, URTI absence rate, enrollment, outreach sessions, eHealth enrollment, PTA meeting attendance.

Regression result (via least squares):

$$
\widehat{\text{URTI Absence}} = 9.11 - 0.085 \cdot \text{VaccinationRate}
$$

Interpretation:
- Each 10-point increase in vaccination lowers URTI absences by ~0.85 percentage points.
- A school with 60% coverage is predicted at \( 9.11 - 0.085 \times 60 = 4.01\% \) URTI absence.
- A school with 85% coverage is predicted at \( 9.11 - 0.085 \times 85 = 1.89\% \), illustrating how higher uptake halves sick leave.

### 4. Leaderboard & Accountability Mapping
Using the regression plus actual values, we rank schools:
- Compute residuals (actual – predicted). Large positive residuals imply more absences than expected given vaccination → targeted audits.
- Assign quartile badges (Gold/Silver/Amber/Red) based on vaccination % and absences.
- EDB integrates the report card into School Development & Accountability reviews; principals in Amber/Red must submit improvement plans, aligning with the relationship described in Education Bureau QA guidelines.

### 5. Reproducibility Steps
1. Load synthetic data.
2. Fit linear regression (vaccination rate → URTI absence).
3. Plot scatter with regression line (see `figures/vaccination_vs_absence.png`).
4. Produce leaderboard bar chart (see `figures/vaccination_leaderboard.png`).
5. Highlight interpretation in report/presentation with citations to Leung et al. 2017 and Lee et al. 2024 to demonstrate empirical grounding.

This simplified math model shows how the report card quantifies the “vaccinate more, miss fewer classes” relationship, providing a transparent basis for EDB to pressure school leadership.

