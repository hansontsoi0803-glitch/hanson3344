#!/usr/bin/env python3
"""
Generate a school report card CSV and run a regression of absence rate on vaccination rate.

Input (default):
  ../01_Project_Report/data/synthetic_school_report_card_with_promo.csv

Outputs (written to ./analysis/output/):
  - report_card.csv
  - regression_summary.txt
  - scatter.png

Requires: pandas, statsmodels, matplotlib, seaborn
"""
import os
from pathlib import Path
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def make_report_card(df: pd.DataFrame) -> pd.DataFrame:
    # Normalize column names to a predictable set
    cols = {c.lower(): c for c in df.columns}
    # Expected columns: School, VaccinationRatePct, URTIAbsencePct, Enrollment, PromotionEffortScore...
    # We'll pick the ones we need if they exist.
    use = [
        'School',
        'VaccinationRatePct',
        'URTIAbsencePct',
        'Enrollment',
        'PromotionEffortScore',
        'ParentWorkshopsPerTerm',
        'SMSRemindersPerTerm',
    ]
    present = [c for c in use if c in df.columns]
    report = df[present].copy()
    report = report.rename(columns={
        'VaccinationRatePct': 'vaccination_rate_pct',
        'URTIAbsencePct': 'absence_rate_pct',
        'Enrollment': 'enrollment',
        'PromotionEffortScore': 'promotion_effort_score',
        'ParentWorkshopsPerTerm': 'parent_workshops_per_term',
        'SMSRemindersPerTerm': 'sms_reminders_per_term',
    })
    # Ensure numeric types
    for c in ['vaccination_rate_pct', 'absence_rate_pct', 'enrollment', 'promotion_effort_score']:
        if c in report.columns:
            report[c] = pd.to_numeric(report[c], errors='coerce')
    return report


def run_regressions(report: pd.DataFrame, out_path: Path):
    results = []

    # Simple unadjusted model: absence ~ vaccination
    if {'absence_rate_pct', 'vaccination_rate_pct'}.issubset(report.columns):
        y = report['absence_rate_pct']
        X = sm.add_constant(report['vaccination_rate_pct'])
        model = sm.OLS(y, X, missing='drop')
        res = model.fit()
        results.append(('Unadjusted: absence_rate_pct ~ vaccination_rate_pct', res))

    # Adjusted model: include promotion effort and enrollment if available
    adj_vars = ['vaccination_rate_pct']
    for extra in ['promotion_effort_score', 'enrollment']:
        if extra in report.columns:
            adj_vars.append(extra)
    if {'absence_rate_pct'}.issubset(report.columns) and len(adj_vars) > 1:
        y = report['absence_rate_pct']
        X = sm.add_constant(report[adj_vars])
        model = sm.OLS(y, X, missing='drop')
        res = model.fit()
        results.append((f"Adjusted: absence_rate_pct ~ {' + '.join(adj_vars)}", res))

    # Write summaries
    with open(out_path / 'regression_summary.txt', 'w') as f:
        for title, res in results:
            f.write(title + '\n')
            f.write(res.summary().as_text())
            f.write('\n' + ('-' * 80) + '\n')

    return results


def make_scatter(report: pd.DataFrame, out_path: Path):
    if {'absence_rate_pct', 'vaccination_rate_pct'}.issubset(report.columns):
        plt.figure(figsize=(8, 6))
        sns.regplot(x='vaccination_rate_pct', y='absence_rate_pct', data=report, scatter_kws={'s': 60})
        plt.xlabel('Vaccination rate (%)')
        plt.ylabel('URTI absence rate (%)')
        plt.title('Absence rate vs Vaccination rate')
        plt.tight_layout()
        plt.savefig(out_path / 'scatter.png', dpi=150)
        plt.close()


def make_pdf(report: pd.DataFrame, out_path: Path):
    """Create a simple PDF report containing the scatter plot and a table of the report card."""
    pdf_file = out_path / 'report_card.pdf'
    with PdfPages(pdf_file) as pdf:
        # Page 1: scatter plot (reuse regplot)
        fig, ax = plt.subplots(figsize=(8.5, 6))
        sns.regplot(x='vaccination_rate_pct', y='absence_rate_pct', data=report, scatter_kws={'s': 60}, ax=ax)
        ax.set_xlabel('Vaccination rate (%)')
        ax.set_ylabel('URTI absence rate (%)')
        ax.set_title('Absence rate vs Vaccination rate')
        fig.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

        # Page 2: table of the report card
        # Render a table (subset columns to fit page)
        cols_to_show = [c for c in ['School', 'vaccination_rate_pct', 'absence_rate_pct', 'enrollment', 'promotion_effort_score'] if c in report.columns or c == 'School']
        # Ensure 'School' label exists in DataFrame for table (it's the index/column)
        table_df = report.copy()
        if 'School' not in table_df.columns and 'School' in report.columns:
            table_df = table_df
        # Prepare table text
        display_df = table_df[ [c for c in ['vaccination_rate_pct', 'absence_rate_pct', 'enrollment', 'promotion_effort_score'] if c in table_df.columns] ].copy()
        display_df.insert(0, 'School', report['School'] if 'School' in report.columns else report.index)

        fig, ax = plt.subplots(figsize=(8.5, 11))
        ax.axis('off')
        ax.set_title('School Report Card', fontsize=14, pad=12)

        # Create table
        table = ax.table(cellText=display_df.values, colLabels=display_df.columns, loc='center', cellLoc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 1.2)
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close(fig)

    print('PDF report written to:', pdf_file)


def main():
    base = Path(__file__).resolve().parent
    data_path = base.parent / '01_Project_Report' / 'data' / 'synthetic_school_report_card_with_promo.csv'
    if not data_path.exists():
        # fallback to other synthetic file
        data_path = base.parent / '01_Project_Report' / 'data' / 'synthetic_school_report_card.csv'

    df = load_data(data_path)
    report = make_report_card(df)

    out_dir = base / 'output'
    out_dir.mkdir(parents=True, exist_ok=True)
    report.to_csv(out_dir / 'report_card.csv', index=False)

    results = run_regressions(report, out_dir)
    make_scatter(report, out_dir)
    # create PDF report with plot and table
    make_pdf(report, out_dir)

    print('Report card written to:', out_dir / 'report_card.csv')
    print('Regression summaries written to:', out_dir / 'regression_summary.txt')
    print('Scatter plot written to:', out_dir / 'scatter.png')


if __name__ == '__main__':
    main()
