# app/utils/fetchers.py
import requests
from typing import List, Dict
from app.utils.teammap import ESPN_TO_DISPLAY  # e.g., {"LAR":"Rams", ...}

def fetch_week_scores_stub(week: int):
    return []

def _get_espn_scoreboard_json_2025(week: int, seasontype: int):
    """
    Try the canonical ESPN endpoints for 2025. We try a few variants since ESPN
    hosts two similar paths; the first one should succeed.
    """
    urls = [
        # ✅ primary: supports ?year=
        f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?year=2025&seasontype={seasontype}&week={week}",
        # fallback (sometimes works even without year)
        f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?seasontype={seasontype}&week={week}",
        # legacy-ish variants (rarely needed, but kept as backup)
        f"https://site.api.espn.com/apis/v2/sports/football/nfl/scoreboard?year=2025&seasontype={seasontype}&week={week}",
        f"https://site.api.espn.com/apis/v2/sports/football/nfl/scoreboard?seasontype={seasontype}&week={week}",
    ]
    last_err = None
    for url in urls:
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            last_err = e
            continue
    # If all failed, surface the last error
    raise last_err or RuntimeError("All ESPN endpoints failed")

def fetch_week_scores_espn_2025(week: int, seasontype: int = 2) -> List[Dict]:
    """
    Fetch COMPLETED NFL games for WEEK of the 2025 season.
    seasontype: 1=Preseason, 2=Regular, 3=Postseason
    Returns: [{"team": <display name>, "result": "W"|"L"|"T", "meta": {"road": bool, "shutout": bool}}, ...]
    """
    data = _get_espn_scoreboard_json_2025(week=week, seasontype=seasontype)

    out: List[Dict] = []
    for ev in data.get("events", []):
        comps = ev.get("competitions") or []
        if not comps:
            continue
        comp = comps[0]

        # only completed games
        stype = (comp.get("status") or {}).get("type") or {}
        if not stype.get("completed", False):
            continue

        competitors = comp.get("competitors") or []
        if len(competitors) != 2:
            continue

        side = []
        for c in competitors:
            team = c.get("team", {}) or {}
            abbr = (team.get("abbreviation") or "").upper()
            score = float(c.get("score") or 0)
            winner = bool(c.get("winner"))
            homeaway = c.get("homeAway")  # 'home' or 'away'
            side.append({"abbr": abbr, "score": score, "winner": winner, "homeaway": homeaway})

        # W/L/T
        if side[0]["score"] == side[1]["score"]:
            res = {side[0]["abbr"]: "T", side[1]["abbr"]: "T"}
        else:
            res = {s["abbr"]: ("W" if s["winner"] else "L") for s in side}

        shutout = (side[0]["score"] == 0 or side[1]["score"] == 0)
        road_winner_abbr = next((s["abbr"] for s in side if s["winner"] and s["homeaway"] == "away"), None)

        # emit rows only for mapped teams
        for s in side:
            abbr = s["abbr"]
            display = ESPN_TO_DISPLAY.get(abbr)
            if not display:
                continue
            
            # Find opponent
            opponent_side = next((other for other in side if other["abbr"] != abbr), None)
            opponent_display = ESPN_TO_DISPLAY.get(opponent_side["abbr"]) if opponent_side else None
            
            meta = {
                "road": (abbr == road_winner_abbr),
                "shutout": shutout and s["score"] > 0,
                "team_score": int(s["score"]),
                "opponent_score": int(opponent_side["score"]) if opponent_side else None,
                "opponent": opponent_display
            }
            out.append({"team": display, "result": res[abbr], "meta": meta})

    return out

# Optional compatibility wrapper if your admin code still calls fetch_week_scores_espn(...)
def fetch_week_scores_espn(week: int, season_year: int, seasontype: int = 2) -> List[Dict]:
    # Pinned to 2025 regardless of season_year
    return fetch_week_scores_espn_2025(week=week, seasontype=seasontype)
