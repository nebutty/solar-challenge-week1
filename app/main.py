# app/main.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Solar — Cross Country", layout="wide")
st.title("Solar Data — Cross-Country Comparison")

# mapping to local CSVs (data/ is in .gitignore)
FILES = {
    "Benin": 'data/benin-malanville_clean.csv',
    "Sierra Leone": 'data/sierraleone-bumbuna_clean.csv',
    "Togo": 'data/togo-dapaong_qc_clean.csv'
}

countries = st.multiselect("Select countries", list(FILES.keys()), default=list(FILES.keys()))
metric = st.selectbox("Select metric", ["GHI","DNI","DHI"])

dfs = []
for c in countries:
    try:
        df = pd.read_csv(FILES[c], parse_dates=['Timestamp'])
        df['Country'] = c
        dfs.append(df[['Timestamp', metric, 'Country']])
    except Exception as e:
        st.error(f"Could not load {c}: {e}")

if dfs:
    combined = pd.concat(dfs, ignore_index=True).dropna(subset=[metric])
    st.subheader(f"{metric} boxplot")
    fig = px.box(combined, x='Country', y=metric, points='outliers')
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average by country")
    avg = combined.groupby('Country')[metric].mean().reset_index().sort_values(metric, ascending=False)
    st.table(avg.round(2))
