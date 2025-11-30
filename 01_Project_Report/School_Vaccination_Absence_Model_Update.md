## Model Update: Incorporating Individual-Level Vaccination vs URTI Absence Data

### 1. Scaling Considerations
The initial synthetic student dataset (`data/synthetic_student_records.csv`) contains a handful of records per school purely to illustrate schema and math steps. In real deployment we would load the full school population (e.g., 400–800 students). The same modeling logic extends automatically once DH provides full vaccination rosters and attendance logs.

### 2. Adjusted Modeling Framework
1. **School-Level Risk Ratios**
   - Using `synthetic_school_vaccination_vs_absence.csv`:
     $$
     RR_s = \frac{ \text{VaccinatedURTISickLeave}_s / \text{VaccinatedStudents}_s }{ \text{UnvaccinatedURTISickLeave}_s / \text{UnvaccinatedStudents}_s }
     $$
   - Insight: quantifies how much less likely vaccinated students are to take URTI leave within each school. Values < 1 reinforce the accountability argument.

2. **Student-Level Logistic Regression**
   - With the expanded dataset (scale up once real data arrives):
     $$
     \text{logit}\big(P(\text{AbsenceDays}>0)\big) = \alpha + \beta \cdot \text{Vaccinated}_{i} + \gamma_{\text{school}(i)}
     $$
   - $\beta$ gives the odds ratio for vaccination; $\gamma$ terms capture persistent school-level differences (promotion, ventilation, socioeconomics).
   - Insight: direct estimate of vaccination protection after adjusting for school fixed effects.

3. **Count Model for Absence Days**
   - Poisson or negative binomial:
     $$
     \mathbb{E}[\text{AbsenceDays}_i] = \exp(\alpha + \beta \cdot \text{Vaccinated}_i + \gamma_{\text{school}(i)})
     $$
   - Insight: expected sick days per student; can underpin predicted vs actual charts in the report card.

### 3. Insights Enabled by the New Data
- **Individual-Level Evidence**: Show parents and principals hard numbers (e.g., “vaccinated students have 0.6 fewer sick days per term”) instead of only school averages.
- **Equity Checks**: School fixed effects reveal whether certain schools have high sickness despite good vaccination, pointing to ventilation or promotion gaps.
- **Targeted Interventions**: Identify unvaccinated clusters (class-level rosters) and track the impact of specific promotion actions on subsequent sick leave.

### 4. Next Steps
1. Expand the synthetic student dataset to hundreds of rows per school once modeling scripts are finalized.
2. Run logistic/Poisson regressions and produce sample odds ratios vs absence days plots.
3. Embed the derived metrics into the School Vaccination Report Card dashboards and messaging packages.

### 5. Demonstration Visuals & Outputs
- **Vaccinated vs unvaccinated URTI sick-leave rates (per school)**  
  `figures/vaccinated_vs_unvaccinated_rates.png`  
  (Source data: `data/synthetic_school_vaccination_vs_absence.csv`)
- **Student-level absence distribution by vaccination status**  
  `figures/absence_days_boxplot.png`  
  (Source data: `data/synthetic_student_records.csv`)
- **Logistic regression summary**  
  `figures/student_logistic_summary.txt` – includes odds ratio estimate (vaccinated students ≈ exp(coef) times less likely to take URTI sick leave).

These visuals illustrate how the adjusted models feed tangible insights into the report card: principals and parents can see both school-level risk ratios and student-level protective effects.

