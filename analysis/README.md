# School report card & regression analysis

This folder contains a small script to generate a school report card CSV and run a regression of absence rate on vaccination rate.

Files:
- `generate_report_and_model.py`: Loads data from `01_Project_Report/data/` (prefers `synthetic_school_report_card_with_promo.csv`), writes `analysis/output/report_card.csv`, `analysis/output/regression_summary.txt`, and `analysis/output/scatter.png`.
- `requirements.txt`: Packages required to run the script.

How to run (macOS / zsh):

1. Create or activate a Python environment (recommended).
2. Install dependencies:

   python3 -m pip install -r analysis/requirements.txt

3. Run the script:

   python3 analysis/generate_report_and_model.py

Outputs will be written into `analysis/output/`.
