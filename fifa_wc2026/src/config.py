"""
config.py — Central configuration for the FIFA WC 2026 project.
All paths, constants, and settings live here.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR        = Path(__file__).resolve().parent.parent
DATA_RAW_DIR    = BASE_DIR / "data" / "raw"
DATA_PROC_DIR   = BASE_DIR / "data" / "processed"
MODELS_DIR      = BASE_DIR / "models"
NOTEBOOKS_DIR   = BASE_DIR / "notebooks"

for d in [DATA_RAW_DIR, DATA_PROC_DIR, MODELS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── API credentials ───────────────────────────────────────────────────────────
API_FOOTBALL_KEY      = os.getenv("API_FOOTBALL_KEY", "")
API_FOOTBALL_BASE_URL = os.getenv("API_FOOTBALL_BASE_URL", "https://v3.football.api-sports.io")

# ── Tournament constants ──────────────────────────────────────────────────────
WC_2026_LEAGUE_ID = int(os.getenv("WC_2026_LEAGUE_ID", 1))
WC_2026_SEASON    = int(os.getenv("WC_2026_SEASON", 2026))

# Historical seasons used for model training
HISTORICAL_SEASONS   = [2018, 2022]
HISTORICAL_LEAGUE_ID = 1   # FIFA World Cup on API-Football

# ── Feature columns ───────────────────────────────────────────────────────────
FEATURE_COLS = [
    "home_fifa_ranking",
    "away_fifa_ranking",
    "ranking_diff",
    "home_form_pts",       # points from last 5 games
    "away_form_pts",
    "home_goals_scored_avg",
    "away_goals_scored_avg",
    "home_goals_conceded_avg",
    "away_goals_conceded_avg",
    "head_to_head_home_wins",
    "head_to_head_away_wins",
    "head_to_head_draws",
]

TARGET_COL = "result"   # "home_win" | "draw" | "away_win"

# ── Model settings ────────────────────────────────────────────────────────────
RANDOM_STATE  = 42
TEST_SIZE     = 0.2
CV_FOLDS      = 5
