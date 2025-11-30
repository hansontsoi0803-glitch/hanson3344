## Linking Vaccination Records to URTI Sick Leave

### 1. New Synthetic Datasets
1. **School-level vaccination vs absence (`data/synthetic_school_vaccination_vs_absence.csv`)**
   - Columns: vaccinated students, vaccinated URTI sick leave count, unvaccinated students, unvaccinated URTI sick leave count.
   - Enables estimation of risk ratios or odds ratios comparing vaccinated vs unvaccinated within each school.

2. **Student-level records (`data/synthetic_student_records.csv`)**
   - One row per student with fields: `StudentID`, `School`, `Vaccinated` (0/1), `URTIAbsenceDays`.
   - Allows logistic or Poisson regression that controls for school fixed effects and quantifies the probability of sick leave as a function of vaccination.

### 2. Model Adjustments
- **Risk Ratio per School**

  For each school \(s\), compute:
  $$
  RR_s = \frac{\text{VaccinatedURTISickLeave}_s / \text{VaccinatedStudents}_s}
               {\text{UnvaccinatedURTISickLeave}_s / \text{UnvaccinatedStudents}_s}
  $$
  Values < 1 reinforce that vaccinated students take fewer sick days. These ratios can be displayed beside the report card leaderboard to strengthen the case for higher uptake.

- **Logistic Regression (Student-level)**

  Using the second dataset, fit:
  $$
  \text{logit}\big(P(\text{URTI Absence Days} > 0)\big)
   = \alpha + \beta \cdot \text{Vaccinated} + \gamma_{\text{school}}
  $$
  where \( \beta \) captures the protective effect of vaccination after controlling for school fixed effects \( \gamma_{\text{school}} \). This outputs interpretable odds ratios (e.g., vaccinated students are 60% less likely to take URTI sick leave), which can be cited in dashboards and policy briefs.

- **Count Model for Absence Days**

  Alternatively, apply a Poisson/negative binomial regression on `URTIAbsenceDays` to estimate expected sick days for vaccinated vs unvaccinated students.

### 3. Dashboard Integration
- Add panels showing:
  - Vaccinated vs unvaccinated sick-leave rates per school (bar chart).
  - System-wide odds ratio/relative risk from student-level regression.
  - Student-level scatter/box plots to visualize distribution of absence days by vaccination status.

### 4. Next Steps
1. Implement the risk ratio calculations for each school and incorporate them into the report card template.
2. Run logistic regression on `synthetic_student_records.csv` (can be scaled up once DH provides actual data) and document coefficients.
3. Update communication materials to highlight the “individual-level protection” evidence, reinforcing both objectives (principal accountability + parent persuasion).

