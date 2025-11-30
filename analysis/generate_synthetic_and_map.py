#!/usr/bin/env python3
"""
Generate synthetic school data across 18 districts and plot a map marking schools with
high vaccination and low absence rates.

Outputs:
  - analysis/output/synthetic_schools_18districts.csv
  - analysis/output/schools_map.png
  - analysis/output/schools_map.pdf

Assumptions:
  - 18 districts, each with between 2 and 6 schools (randomized) -> ~50-70 schools total
  - Districts are represented by cluster centers within a bounding box (simulated lat/lon)
  - Vaccination and absence rates are negatively correlated with added noise
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def generate_schools(n_districts=18, seed=42):
    rng = np.random.default_rng(seed)
    districts = [f"District {i+1}" for i in range(n_districts)]

    # Create cluster centers (lat, lon) inside an arbitrary bounding box
    # We'll use a box roughly like a small region: lat 22.20-22.40, lon 114.00-114.25 (HK-like)
    lat_min, lat_max = 22.20, 22.40
    lon_min, lon_max = 114.00, 114.25
    centers_lat = rng.uniform(lat_min + 0.01, lat_max - 0.01, size=n_districts)
    centers_lon = rng.uniform(lon_min + 0.01, lon_max - 0.01, size=n_districts)

    rows = []
    school_id = 0
    for i, d in enumerate(districts):
        n_schools = rng.integers(2, 7)  # between 2 and 6 schools per district
        for s in range(n_schools):
            school_id += 1
            name = f"{d} School {s+1}"
            # sample lat/lon around cluster center
            lat = centers_lat[i] + rng.normal(scale=0.01)
            lon = centers_lon[i] + rng.normal(scale=0.01)
            enrollment = int(rng.integers(200, 900))

            # Generate vaccination rate and absence with inverse relationship
            # Start with district-level tendency
            district_vax = rng.uniform(50, 95)
            vax = np.clip(district_vax + rng.normal(scale=8), 20, 100)

            # absence roughly decreases with vaccination, plus noise
            base_abs = 8.0 - 0.07 * vax  # e.g., at vax=90 -> base_abs=1.7
            absence = max(0.2, base_abs + rng.normal(scale=0.6))

            rows.append({
                'school_id': school_id,
                'school_name': name,
                'district': d,
                'latitude': round(lat, 6),
                'longitude': round(lon, 6),
                'enrollment': enrollment,
                'vaccination_rate_pct': round(vax, 1),
                'absence_rate_pct': round(absence, 2),
            })

    df = pd.DataFrame(rows)
    return df


def label_high_vax_low_abs(df, vax_thresh=80.0, absence_thresh=2.5):
    df = df.copy()
    df['high_vax_low_abs'] = (df['vaccination_rate_pct'] >= vax_thresh) & (df['absence_rate_pct'] <= absence_thresh)
    return df


def plot_map(df: pd.DataFrame, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(10, 10))
    sns.scatterplot(data=df, x='longitude', y='latitude', hue='vaccination_rate_pct', size='enrollment', palette='viridis', sizes=(20, 200), alpha=0.8, edgecolor='k')

    # Highlight and label schools with high vaccination and low absence
    highlight = df[df['high_vax_low_abs']]
    plt.scatter(highlight['longitude'], highlight['latitude'], facecolors='none', edgecolors='red', s=200, linewidths=1.5)
    for _, r in highlight.iterrows():
        plt.text(r['longitude'] + 0.002, r['latitude'] + 0.002, r['school_name'], fontsize=8, weight='bold', color='red')

    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Synthetic Schools: vaccination rate (color) and enrollment (size)\nRed outlines = high vaccination & low absence')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    png_path = out_dir / 'schools_map.png'
    pdf_path = out_dir / 'schools_map.pdf'
    plt.savefig(png_path, dpi=200)
    plt.savefig(pdf_path)
    plt.close()
    print('Map written to:', png_path, pdf_path)


def main():
    out_dir = Path(__file__).resolve().parent / 'output'
    df = generate_schools(n_districts=18, seed=2025)
    df = label_high_vax_low_abs(df, vax_thresh=80.0, absence_thresh=2.5)
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / 'synthetic_schools_18districts.csv'
    df.to_csv(csv_path, index=False)
    print('Synthetic data written to:', csv_path)
    plot_map(df, out_dir)


if __name__ == '__main__':
    main()
