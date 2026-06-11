"""
src/data/api_client.py
Handles all communication with the API-Football v3 endpoint.
"""

import time
import logging
import requests
from typing import Optional

from src.config import API_FOOTBALL_KEY, API_FOOTBALL_BASE_URL

logger = logging.getLogger(__name__)


class APIFootballClient:
    """
    Thin wrapper around the API-Football REST API.

    Free tier: 100 requests/day.
    We cache responses to disk to avoid burning quota on re-runs.
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or API_FOOTBALL_KEY
        self.base_url = API_FOOTBALL_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            "x-apisports-key": self.api_key,
            "Accept": "application/json",
        })
        self._request_count = 0

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """Make a GET request, respecting a short delay between calls."""
        if not self.api_key or self.api_key == "your_api_key_here":
            raise ValueError(
                "API_FOOTBALL_KEY is not set. "
                "Copy .env.example to .env and add your key."
            )

        url = f"{self.base_url}/{endpoint}"
        time.sleep(0.5)          # stay well within rate limits
        self._request_count += 1

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("errors"):
                logger.error("API error: %s", data["errors"])
                raise RuntimeError(f"API returned errors: {data['errors']}")

            logger.info("GET %s — %d results", endpoint, data.get("results", 0))
            return data

        except requests.RequestException as exc:
            logger.error("Request failed: %s", exc)
            raise

    # ── Public methods ────────────────────────────────────────────────────────

    def get_fixtures(self, league_id: int, season: int) -> list[dict]:
        """Return all fixtures for a given league and season."""
        data = self._get("fixtures", params={"league": league_id, "season": season})
        return data.get("response", [])

    def get_team_statistics(self, team_id: int, league_id: int, season: int) -> dict:
        """Return aggregated team statistics for a season."""
        data = self._get(
            "teams/statistics",
            params={"team": team_id, "league": league_id, "season": season},
        )
        return data.get("response", {})

    def get_standings(self, league_id: int, season: int) -> list[dict]:
        """Return league standings (includes form, points, goal diff)."""
        data = self._get("standings", params={"league": league_id, "season": season})
        return data.get("response", [])

    def get_head_to_head(self, team1_id: int, team2_id: int, last: int = 10) -> list[dict]:
        """Return head-to-head history between two teams."""
        data = self._get(
            "fixtures/headtohead",
            params={"h2h": f"{team1_id}-{team2_id}", "last": last},
        )
        return data.get("response", [])

    def get_teams(self, league_id: int, season: int) -> list[dict]:
        """Return all teams participating in a tournament."""
        data = self._get("teams", params={"league": league_id, "season": season})
        return data.get("response", [])

    @property
    def requests_used(self) -> int:
        return self._request_count
