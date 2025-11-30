#!/usr/bin/env python3
"""
Generate automated alerts for schools below a vaccination threshold.

Outputs:
  - analysis/output/flagged_schools_<threshold>pct.csv
  - analysis/output/flagged_schools_map_<threshold>pct.png

Usage:
  python3 analysis/generate_alerts.py --threshold 70
"""
from pathlib import Path
import argparse
import pandas as pd
import matplotlib.pyplot as plt


def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def write_flagged(df: pd.DataFrame, threshold: float, out_dir: Path) -> Path:
    flagged = df[df['vaccination_rate_pct'] < threshold].copy()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / f'flagged_schools_{int(threshold)}pct.csv'
    flagged.to_csv(out_csv, index=False)
    return out_csv


def plot_flagged_map(df: pd.DataFrame, threshold: float, out_dir: Path) -> Path:
    flagged = df[df['vaccination_rate_pct'] < threshold].copy()
    out_dir.mkdir(parents=True, exist_ok=True)
    out_png = out_dir / f'flagged_schools_map_{int(threshold)}pct.png'
    if flagged.empty:
        # create a small plot which says 'no flagged schools'
        plt.figure(figsize=(6, 3))
        plt.text(0.5, 0.5, f'No schools below {threshold}% vaccination', ha='center', va='center')
        plt.axis('off')
        plt.savefig(out_png, dpi=150)
        plt.close()
        return out_png

    # Compute bounding box with margin
    lon_min, lon_max = flagged['longitude'].min(), flagged['longitude'].max()
    lat_min, lat_max = flagged['latitude'].min(), flagged['latitude'].max()
    lon_pad = max(0.01, (lon_max - lon_min) * 0.2)
    lat_pad = max(0.01, (lat_max - lat_min) * 0.2)

    plt.figure(figsize=(8, 6))
    # Plot all schools in light grey for context
    plt.scatter(df['longitude'], df['latitude'], c='lightgrey', s=30, alpha=0.6, label='All schools')
    # Plot flagged schools in red
    plt.scatter(flagged['longitude'], flagged['latitude'], c='red', s=80, alpha=0.9, label='Flagged schools')

    for _, r in flagged.iterrows():
        plt.text(r['longitude'] + 0.002, r['latitude'] + 0.002, r['school_name'], fontsize=8, color='red')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title(f'Schools with vaccination < {threshold}%')
    plt.legend()
    plt.xlim(lon_min - lon_pad, lon_max + lon_pad)
    plt.ylim(lat_min - lat_pad, lat_max + lat_pad)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()
    return out_png


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--threshold', type=float, default=70.0, help='Vaccination percentage threshold')
    args = parser.parse_args()

    base = Path(__file__).resolve().parent / 'output'
    csv = base / 'synthetic_schools_18districts.csv'
    if not csv.exists():
        raise SystemExit('Synthetic schools CSV not found. Run generate_synthetic_and_map.py first.')

    df = load_data(csv)
    out_csv = write_flagged(df, args.threshold, base)
    out_png = plot_flagged_map(df, args.threshold, base)

    print('Flagged CSV:', out_csv)
    print('Flagged map PNG:', out_png)


if __name__ == '__main__':
    main()
