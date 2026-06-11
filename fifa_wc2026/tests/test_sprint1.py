"""
tests/test_sprint1.py
Smoke tests for Sprint 1 — Data layer.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd
from src.data.load_kaggle import load_results_csv, filter_world_cup_matches
from src.config import FEATURE_COLS, DATA_PROC_DIR


def test_load_results_returns_dataframe():
    df = load_results_csv()
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_required_columns_present():
    df = load_results_csv()
    required = {"date", "home_team", "away_team", "home_score", "away_score"}
    assert required.issubset(df.columns)


def test_filter_world_cup_matches_returns_dataframe():
    df = load_results_csv()
    wc_df = filter_world_cup_matches(df)
    assert isinstance(wc_df, pd.DataFrame)


def test_processed_data_exists():
    path = DATA_PROC_DIR / "historical_matches.csv"
    assert path.exists(), "Run `python -m src.data.load_kaggle` first."


def test_feature_columns_defined():
    assert len(FEATURE_COLS) >= 8
