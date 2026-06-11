"""
src/data/collect.py
Sprint 1 main script: fetch all raw data and save to data/raw/.

Usage:
    python -m src.data.collect
"""

import json
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime

from src.config import (
    DATA_RAW_DIR,
    WC_2026_LEAGUE_ID,
    WC_2026_SEASON,
    HISTORICAL_SEASONS,
    HISTORICAL_LEAGUE_ID,
)
from src.data.api_client import APIFootballClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def save_json(data: list | dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    logger.info("Saved → %s (%d records)", path.name, len(data) if isinstance(data, list) else 1)


def fetch_fixtures(client: APIFootballClient) -> None:
    """Fetch WC 2026 fixtures + historical WC fixtures for training."""
    # Live WC 2026 fixtures
    logger.info("Fetching WC 2026 fixtures …")
    fixtures_2026 = client.get_fixtures(WC_2026_LEAGUE_ID, WC_2026_SEASON)
    save_json(fixtures_2026, DATA_RAW_DIR / "fixtures_2026.json")

    # Historical fixtures for model training
    for season in HISTORICAL_SEASONS:
        logger.info("Fetching WC %d fixtures …", season)
        fixtures = client.get_fixtures(HISTORICAL_LEAGUE_ID, season)
        save_json(fixtures, DATA_RAW_DIR / f"fixtures_{season}.json")


def fetch_standings(client: APIFootballClient) -> None:
    """Fetch current WC 2026 group stage standings."""
    logger.info("Fetching WC 2026 standings …")
    standings = client.get_standings(WC_2026_LEAGUE_ID, WC_2026_SEASON)
    save_json(standings, DATA_RAW_DIR / "standings_2026.json")


def fetch_teams(client: APIFootballClient) -> None:
    """Fetch all 48 teams in WC 2026."""
    logger.info("Fetching WC 2026 teams …")
    teams = client.get_teams(WC_2026_LEAGUE_ID, WC_2026_SEASON)
    save_json(teams, DATA_RAW_DIR / "teams_2026.json")

    # Build a flat CSV mapping team_id → name for easy joins
    rows = [
        {
            "team_id": t["team"]["id"],
            "team_name": t["team"]["name"],
            "team_code": t["team"]["code"],
            "country": t["team"]["country"],
            "logo_url": t["team"]["logo"],
        }
        for t in teams
    ]
    df = pd.DataFrame(rows)
    df.to_csv(DATA_RAW_DIR / "teams_2026.csv", index=False)
    logger.info("Teams CSV saved with %d entries.", len(df))


def fetch_head_to_head(client: APIFootballClient) -> None:
    """
    Fetch head-to-head history for every pair of teams in WC 2026.
    This is called lazily during feature engineering — here we just
    demonstrate a single example pair and save it.
    """
    teams_path = DATA_RAW_DIR / "teams_2026.json"
    if not teams_path.exists():
        logger.warning("teams_2026.json not found; run fetch_teams first.")
        return

    with open(teams_path) as f:
        teams = json.load(f)

    if len(teams) < 2:
        logger.warning("Not enough teams to compute H2H.")
        return

    t1_id = teams[0]["team"]["id"]
    t2_id = teams[1]["team"]["id"]
    logger.info("Fetching sample H2H: team %d vs team %d …", t1_id, t2_id)
    h2h = client.get_head_to_head(t1_id, t2_id, last=10)
    save_json(h2h, DATA_RAW_DIR / f"h2h_{t1_id}_vs_{t2_id}.json")


def build_collection_manifest() -> None:
    """Write a manifest file noting when data was last collected."""
    manifest = {
        "collected_at": datetime.utcnow().isoformat() + "Z",
        "files": [str(p.name) for p in DATA_RAW_DIR.glob("*.json")]
                 + [str(p.name) for p in DATA_RAW_DIR.glob("*.csv")],
    }
    save_json(manifest, DATA_RAW_DIR / "_manifest.json")


def main():
    client = APIFootballClient()
    logger.info("═══ Sprint 1 — Data collection starting ═══")

    fetch_teams(client)
    fetch_fixtures(client)
    fetch_standings(client)
    fetch_head_to_head(client)
    build_collection_manifest()

    logger.info("═══ Collection complete. API requests used: %d ═══", client.requests_used)


if __name__ == "__main__":
    main()
