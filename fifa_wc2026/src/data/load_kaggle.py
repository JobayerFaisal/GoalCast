"""
src/data/load_kaggle.py
Loads historical FIFA / international match datasets from Kaggle CSVs.

Recommended dataset (download manually and place in data/raw/):
  "International football results from 1872 to 2024"
  https://www.kaggle.com/datasets/martj42/international-football-results-from-1872-to-2017

Expected file: data/raw/results.csv with columns:
  date, home_team, away_team, home_score, away_score, tournament, city, country, neutral

Usage:
    python -m src.data.load_kaggle
"""

import logging
import pandas as pd
from src.config import DATA_RAW_DIR, DATA_PROC_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)-8s  %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger(__name__)


def load_results_csv() -> pd.DataFrame:
    """Load the Kaggle international results CSV."""
    path = DATA_RAW_DIR / "results.csv"
    if not path.exists():
        logger.warning(
            "results.csv not found at %s.\n"
            "Download from Kaggle (search 'international football results') "
            "and place it there. Generating a small synthetic sample instead.",
            path,
        )
        return _generate_sample_data()

    df = pd.read_csv(path, parse_dates=["date"])
    logger.info("Loaded %d historical matches.", len(df))
    return df


def _generate_sample_data() -> pd.DataFrame:
    """
    Create a small synthetic dataset so the pipeline is runnable end-to-end
    even before real data is downloaded. Replace with real Kaggle data ASAP.
    """
    import numpy as np
    np.random.seed(42)

    teams = [
        "Brazil", "Argentina", "France", "England", "Spain", "Germany",
        "Portugal", "Netherlands", "Belgium", "Croatia", "Italy", "Uruguay",
        "USA", "Mexico", "Japan", "Morocco",
    ]

    rows = []
    dates = pd.date_range("2018-01-01", "2026-01-01", freq="7D")
    for date in dates:
        h, a = np.random.choice(teams, 2, replace=False)
        hs = np.random.poisson(1.4)
        as_ = np.random.poisson(1.1)
        rows.append({
            "date": date,
            "home_team": h,
            "away_team": a,
            "home_score": hs,
            "away_score": as_,
            "tournament": "Friendly",
            "city": "Neutral City",
            "country": "Neutral",
            "neutral": True,
        })

    df = pd.DataFrame(rows)
    out_path = DATA_RAW_DIR / "results.csv"
    df.to_csv(out_path, index=False)
    logger.info("Synthetic sample data written to %s (%d rows).", out_path, len(df))
    return df


def filter_world_cup_matches(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only World Cup-relevant matches (or all, for the synthetic sample)."""
    wc_mask = df["tournament"].str.contains("World Cup", case=False, na=False)
    if wc_mask.sum() == 0:
        logger.info("No 'World Cup' rows found — using full dataset (likely synthetic sample).")
        return df
    logger.info("Filtered to %d World Cup matches.", wc_mask.sum())
    return df[wc_mask].reset_index(drop=True)


def main():
    df = load_results_csv()
    wc_df = filter_world_cup_matches(df)

    DATA_PROC_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DATA_PROC_DIR / "historical_matches.csv"
    wc_df.to_csv(out_path, index=False)
    logger.info("Saved processed historical matches → %s (%d rows)", out_path, len(wc_df))


if __name__ == "__main__":
    main()
