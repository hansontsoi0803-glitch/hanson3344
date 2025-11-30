#!/usr/bin/env python3
"""
Generate one-page PDF report cards for each school for principals.

Outputs:
  - analysis/output/principal_reports/report_card_<school_id>_<safe_name>.pdf

Each report includes:
  - School name, district, enrollment
  - Vaccination rate, absence rate
  - Small bar chart comparing school vax to district mean and overall mean
  - Suggested action if vax < threshold
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import re


def safe_name(s: str) -> str:
    return re.sub(r'[^A-Za-z0-9_-]', '_', s)


def load_report_card(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def make_report_for_school(r, district_mean, overall_mean, out_path: Path, threshold: float = 70.0):
    # r is a pandas Series for one school
    fig = plt.figure(figsize=(8.5, 11))
    ax = fig.add_axes([0.1, 0.55, 0.8, 0.4])
    ax.axis('off')

    # Header
    fig.suptitle(f"School Report Card — {r['School']}", fontsize=18, y=0.95)

    # Key metrics box
    metrics_text = (
        f"District: {r.get('district', '')}\n"
        f"Enrollment: {int(r.get('enrollment', 0))}\n"
        f"Vaccination rate: {r.get('vaccination_rate_pct', float('nan'))}%\n"
        f"URTI absence rate: {r.get('absence_rate_pct', float('nan'))}%\n"
    )
    ax.text(0, 0.85, metrics_text, fontsize=12, va='top')

    # Recommendation
    vax = float(r.get('vaccination_rate_pct', np.nan))
    rec = ''
    if vax < threshold:
        rec = f"Action: Vaccination below {threshold}%. Recommend targeted outreach (parent workshops, SMS reminders), eHealth sync follow-up, and priority for school nurse visits."
    else:
        rec = 'Action: Keep up outreach. Share peer best-practices and continue monitoring.'
    ax.text(0, 0.45, rec, fontsize=11, va='top', color='red' if vax < threshold else 'green')

    # Small bar chart comparing vax
    ax2 = fig.add_axes([0.12, 0.15, 0.35, 0.25])
    labels = ['School', 'District mean', 'Overall mean']
    values = [vax, district_mean, overall_mean]
    colors = ['#4c72b0', '#55a868', '#c44e52']
    ax2.bar(labels, values, color=colors)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel('Vaccination rate (%)')
    ax2.set_title('Vaccination coverage comparison')

    # Small bar for absence rate
    ax3 = fig.add_axes([0.55, 0.15, 0.35, 0.25])
    labels2 = ['School absence']
    values2 = [float(r.get('absence_rate_pct', np.nan))]
    ax3.bar(labels2, values2, color=['#ff7f0e'])
    ax3.set_ylabel('URTI absence rate (%)')
    ax3.set_title('Absence rate')

    # Footer notes
    fig.text(0.1, 0.05, 'Generated from synthetic/report data. For enquiries contact project data team.', fontsize=9)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with PdfPages(out_path) as pdf:
        pdf.savefig(fig)
    plt.close(fig)


def main():
    base = Path(__file__).resolve().parent / 'output'
    csv = base / 'report_card.csv'
    if not csv.exists():
        raise SystemExit('Report card CSV not found. Run generate_report_and_model.py first.')

    df = load_report_card(csv)

    # Ensure expected columns
    if 'district' not in df.columns:
        # try to infer district from School if possible (synthetic data uses 'district' in synthetic file)
        df['district'] = df.get('district', '')

    overall_mean = df['vaccination_rate_pct'].mean()

    # compute district means using synthetic dataset if available
    if 'district' in df.columns and df['district'].notna().any():
        district_means = df.groupby('district')['vaccination_rate_pct'].mean().to_dict()
    else:
        district_means = {}

    out_dir = base / 'principal_reports'

    for _, row in df.iterrows():
        district = row.get('district', '')
        district_mean = district_means.get(district, overall_mean)
        sid = int(row.get('school_id', row.name if 'school_id' in row else 0))
        fname = out_dir / f"report_card_{sid}_{safe_name(str(row['School']))}.pdf"
        make_report_for_school(row, district_mean, overall_mean, fname)

    print('Report cards written to:', out_dir)


if __name__ == '__main__':
    main()
