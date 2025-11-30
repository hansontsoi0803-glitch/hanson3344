"""Streamlit dashboard for school vaccination monitoring.

Features:
- KPIs (overall vaccination coverage, schools flagged)
- District filter
- Automated alerts: schools with vaccination rate below threshold
- Targeted resource list: exportable CSV of flagged schools sorted by need
- Map: pydeck scatter map of schools (color = vaccination rate, size = enrollment)
- Trend analysis: simulated refusal reasons aggregated by district

Run:
  /Users/tsoihanson/Desktop/Team1_FluShot/.venv/bin/streamlit run analysis/dashboard/streamlit_app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path


@st.cache_data
def load_schools(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def simulate_refusal_reasons(df: pd.DataFrame, seed=2025):
    rng = np.random.default_rng(seed)
    reasons = ['Safety concerns', 'Misinformation', 'Access', 'Religious', 'Other']
    # assign counts proportional to remaining unvaccinated
    df = df.copy()
    df['not_vax_pct'] = 100.0 - df['vaccination_rate_pct']
    # for each school, simulate counts that sum roughly to not_vax_pct * enrollment / 100
    counts = []
    for _, r in df.iterrows():
        total_unvax = max(1, int(round(r['not_vax_pct'] * r['enrollment'] / 100.0)))
        # draw a random multinomial
        probs = rng.random(len(reasons))
        probs = probs / probs.sum()
        draw = rng.multinomial(total_unvax, probs)
        counts.append(dict(zip(reasons, draw)))
    reasons_df = pd.DataFrame(counts)
    reasons_df.index = df.index
    return pd.concat([df, reasons_df], axis=1)


def main():
    st.set_page_config(page_title='School Vaccination Dashboard', layout='wide')
    st.title('School Vaccination Monitoring — Prototype')

    base = Path(__file__).resolve().parent.parent / 'output'
    csv = base / 'synthetic_schools_18districts.csv'
    if not csv.exists():
        st.error(f'Synthetic data not found at {csv}. Run generate_synthetic_and_map.py first.')
        return

    df = load_schools(csv)
    df = simulate_refusal_reasons(df)

    # Sidebar controls
    st.sidebar.header('Controls')
    vax_threshold = st.sidebar.slider('Vaccination threshold (flag if below)', 40, 95, 70)
    selected_district = st.sidebar.selectbox('District', ['All'] + sorted(df['district'].unique().tolist()))

    # Filter
    if selected_district != 'All':
        ddf = df[df['district'] == selected_district]
    else:
        ddf = df

    # KPIs
    col1, col2, col3 = st.columns(3)
    overall_vax = df['vaccination_rate_pct'].mean()
    flagged = df[df['vaccination_rate_pct'] < vax_threshold].shape[0]
    total_schools = df.shape[0]
    col1.metric('Overall mean vaccination (%)', f"{overall_vax:.1f}")
    col2.metric('Schools flagged', f"{flagged} / {total_schools}")
    col3.metric('Selected district schools', f"{ddf.shape[0]}")

    st.markdown('---')

    # Alerts table
    st.header('Automated alerts')
    alerts = ddf[ddf['vaccination_rate_pct'] < vax_threshold].copy()
    alerts = alerts.sort_values(['vaccination_rate_pct', 'absence_rate_pct'])
    st.write(f'Schools below {vax_threshold}% vaccination')
    st.dataframe(alerts[['school_id', 'school_name', 'district', 'enrollment', 'vaccination_rate_pct', 'absence_rate_pct']])

    # Export targeted list
    if not alerts.empty:
        csv_bytes = alerts.to_csv(index=False).encode('utf-8')
        st.download_button('Download targeted list (CSV)', csv_bytes, file_name='targeted_schools.csv')

    st.markdown('---')

    # Map
    st.header('Map view')
    midpoint = (float(df['latitude'].mean()), float(df['longitude'].mean()))
    st.write('Hover markers for school details. Red rings show flagged schools.')

    # Simple map view using streamlit's st.map for a lightweight interactive map
    df_map = ddf.rename(columns={'latitude': 'lat', 'longitude': 'lon'})
    st.map(df_map[['lat', 'lon']])

    st.markdown('---')

    # Trend analysis (simulated refusal reasons)
    st.header('Trend analysis — refusal reasons (simulated)')
    reasons = ['Safety concerns', 'Misinformation', 'Access', 'Religious', 'Other']
    agg = df.groupby('district')[reasons].sum().reset_index()
    # show district-level stacked bar (using Altair via st.bar_chart is simpler)
    st.subheader('Refusal reasons by district (counts)')
    st.dataframe(agg)
    st.bar_chart(agg.set_index('district'))

    st.markdown('---')
    st.write('Notes: refusal reasons are simulated for prototype purposes. For production, provide fields in uploads that record refusal reasons or reasons for absence.')


if __name__ == '__main__':
    main()
