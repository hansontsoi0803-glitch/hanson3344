#!/usr/bin/env python3
"""
Create a geographical-style district map by building Voronoi polygons from district centroids
and plotting a choropleth of mean vaccination rate per district. Overlays school points and
high-vax/low-absence labels.

Outputs:
  - analysis/output/districts_geographical_map.png
  - analysis/output/districts_geographical_map.pdf

This script uses scipy and shapely. It does not require geopandas.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as MplPolygon
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union
from scipy.spatial import Voronoi


def load_data(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def district_centroids(df: pd.DataFrame):
    g = df.groupby('district')
    centroids = g[['longitude', 'latitude']].mean().reset_index()
    return centroids


def voronoi_polygons(pts, bbox):
    # pts: Nx2 numpy array of points (lon, lat)
    vor = Voronoi(pts)
    regions = []
    bbox_poly = Polygon([(bbox[0], bbox[2]), (bbox[1], bbox[2]), (bbox[1], bbox[3]), (bbox[0], bbox[3])])

    for i, region_idx in enumerate(vor.point_region):
        region = vor.regions[region_idx]
        if not region or -1 in region:
            # infinite region: fallback to a buffered point intersect bbox
            poly = Point(pts[i]).buffer(0.03)
            poly = poly.intersection(bbox_poly)
        else:
            polygon = [tuple(vor.vertices[v]) for v in region]
            poly = Polygon(polygon).intersection(bbox_poly)
        regions.append(poly)

    return regions


def plot_map(df, centroids, regions, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    # Aggregate stats per district
    stats = df.groupby('district').agg(
        vaccination_rate_pct=('vaccination_rate_pct', 'mean'),
        absence_rate_pct=('absence_rate_pct', 'mean'),
        schools_count=('school_id', 'count')
    ).reset_index()

    # merge centroids and stats
    centroids = centroids.merge(stats, on='district')

    # Prepare patches
    patches = []
    values = []
    labels = []
    for i, row in centroids.iterrows():
        poly = regions[i]
        if poly is None or poly.is_empty:
            continue
        # ensure polygon is valid
        poly = poly.buffer(0)
        if poly.is_empty:
            continue
        if poly.geom_type == 'MultiPolygon':
            poly = max(poly.geoms, key=lambda p: p.area)
            coords = np.array(poly.exterior.coords)
            patches.append(MplPolygon(coords, closed=True))
            values.append(row['vaccination_rate_pct'])
            labels.append(row['district'])

    fig, ax = plt.subplots(figsize=(10, 10))
    pc = PatchCollection(patches, cmap='YlGnBu', edgecolor='k', linewidths=0.6)
    pc.set_array(np.array(values))
    ax.add_collection(pc)
    cbar = fig.colorbar(pc, ax=ax, fraction=0.036, pad=0.04)
    cbar.set_label('Mean vaccination rate (%)')

    # scatter schools
    ax.scatter(df['longitude'], df['latitude'], c='k', s=10, alpha=0.6)

    # label districts at centroid
    for _, r in centroids.iterrows():
        ax.text(r['longitude'], r['latitude'], r['district'].split()[-1], fontsize=8, ha='center', va='center')

    # highlight high vax & low absence schools
    highlight = df[df['high_vax_low_abs']]
    ax.scatter(highlight['longitude'], highlight['latitude'], facecolors='none', edgecolors='red', s=80, linewidths=1.2)
    for _, s in highlight.iterrows():
        ax.text(s['longitude'] + 0.002, s['latitude'] + 0.002, s['school_name'], fontsize=7, color='red')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('District choropleth (Voronoi) by mean vaccination rate')
    ax.set_aspect('equal', adjustable='box')
    ax.grid(alpha=0.3)
    plt.tight_layout()

    png = out_dir / 'districts_geographical_map.png'
    pdf = out_dir / 'districts_geographical_map.pdf'
    fig.savefig(png, dpi=200)
    fig.savefig(pdf)
    plt.close(fig)
    print('Wrote', png, pdf)


def main():
    out_dir = Path(__file__).resolve().parent / 'output'
    csv = out_dir / 'synthetic_schools_18districts.csv'
    if not csv.exists():
        raise SystemExit('Synthetic schools CSV not found. Run generate_synthetic_and_map.py first.')

    df = pd.read_csv(csv)
    centroids = district_centroids(df)
    pts = centroids[['longitude', 'latitude']].to_numpy()

    # bounding box from data with a small margin
    lon_min, lon_max = df['longitude'].min() - 0.02, df['longitude'].max() + 0.02
    lat_min, lat_max = df['latitude'].min() - 0.02, df['latitude'].max() + 0.02
    bbox = (lon_min, lon_max, lat_min, lat_max)

    regions = voronoi_polygons(pts, bbox)
    plot_map(df, centroids, regions, out_dir)


if __name__ == '__main__':
    main()
