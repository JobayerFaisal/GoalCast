"""
streamlit_app/app.py
FIFA World Cup 2026 — Data & Prediction Dashboard
Sprint 1: skeleton with data overview. Predictions added in Sprint 3-4.

Run locally:
    streamlit run streamlit_app/app.py

Deploy:
    Push to GitHub → share.streamlit.io → New app → point to this file.
"""

import sys
from pathlib import Path

# Make src/ importable when run via `streamlit run`
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.config import DATA_PROC_DIR, DATA_RAW_DIR

st.set_page_config(
    page_title="FIFA World Cup 2026 — Predictions",
    page_icon="⚽",
    layout="wide",
)

# ── Header ─────────────────────────────────────────────────────────────────
st.title("⚽ FIFA World Cup 2026 — Data & Prediction Dashboard")
st.caption("MSc Project — Agile Sprint 1: Data Foundation")

st.markdown("""
This dashboard will grow sprint by sprint:
- **Sprint 1 (current):** Data collection & exploration ✅
- **Sprint 2:** Feature engineering & EDA
- **Sprint 3:** ML model predictions
- **Sprint 4:** Live fixtures, group standings & polished UI
""")

# ── Load data ──────────────────────────────────────────────────────────────
@st.cache_data
def load_historical_data() -> pd.DataFrame:
    path = DATA_PROC_DIR / "historical_matches.csv"
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path, parse_dates=["date"])
    return df


@st.cache_data
def load_teams() -> pd.DataFrame:
    path = DATA_RAW_DIR / "teams_2026.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


df = load_historical_data()
teams_df = load_teams()

if df.empty:
    st.warning(
        "⚠️ No data found yet. Run `python -m src.data.load_kaggle` "
        "(and `python -m src.data.collect` with an API key) to populate data."
    )
    st.stop()

# ── Sidebar filters ────────────────────────────────────────────────────────
st.sidebar.header("Filters")
all_teams = sorted(set(df["home_team"]) | set(df["away_team"]))
selected_team = st.sidebar.selectbox("Focus on a team", ["All teams"] + all_teams)

if selected_team != "All teams":
    df = df[(df["home_team"] == selected_team) | (df["away_team"] == selected_team)]

# ── Top metrics ────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
col1.metric("Matches loaded", len(df))
col2.metric("Teams covered", len(all_teams))
col3.metric("Avg home goals", f"{df['home_score'].mean():.2f}")
col4.metric("Avg away goals", f"{df['away_score'].mean():.2f}")

st.divider()

# ── Goals over time ────────────────────────────────────────────────────────
st.subheader("Goals scored over time")
goals_over_time = (
    df.groupby(df["date"].dt.to_period("M"))[["home_score", "away_score"]]
    .mean()
    .reset_index()
)
goals_over_time["date"] = goals_over_time["date"].dt.to_timestamp()

fig = px.line(
    goals_over_time,
    x="date",
    y=["home_score", "away_score"],
    labels={"value": "Avg goals", "date": "Month", "variable": "Side"},
    title="Average goals per match over time",
)
st.plotly_chart(fig, use_container_width=True)

# ── Win/draw/loss breakdown ────────────────────────────────────────────────
st.subheader("Match outcomes")

def get_result(row):
    if row["home_score"] > row["away_score"]:
        return "Home win"
    elif row["home_score"] < row["away_score"]:
        return "Away win"
    return "Draw"

df["result"] = df.apply(get_result, axis=1)
result_counts = df["result"].value_counts().reset_index()
result_counts.columns = ["Result", "Count"]

fig2 = px.pie(result_counts, names="Result", values="Count", title="Outcome distribution")
st.plotly_chart(fig2, use_container_width=True)

# ── Raw data ────────────────────────────────────────────────────────────────
with st.expander("📄 View raw data"):
    st.dataframe(df, use_container_width=True)

if not teams_df.empty:
    with st.expander("🏳️ World Cup 2026 teams"):
        st.dataframe(teams_df, use_container_width=True)

# ── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.caption("Built with Streamlit · Data: API-Football & Kaggle · Agile Sprint 1 deliverable")
