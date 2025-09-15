import json
from flask import current_app

DEFAULT_SCORING = {
    "win": 1,
    "loss": 0,
    "tie": 0,
    "shutout_bonus": 0,
    "road_win_bonus": 0,
    "upset_bonus": 0
}

def load_scoring():
    path = current_app.config.get("SCORING_FILE", "scoring.json")
    try:
        with open(path) as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SCORING.copy()

def compute_points_for_result(result, meta=None):
    meta = meta or {}
    scoring = load_scoring()
    r = (result or "").upper()

    pts = 0
    if r == "W":
        pts += scoring.get("win", 0)
        if meta.get("road"):
            pts += scoring.get("road_win_bonus", 0)
        if meta.get("shutout"):
            pts += scoring.get("shutout_bonus", 0)
        if meta.get("upset"):
            pts += scoring.get("upset_bonus", 0)
    elif r == "T":
        pts += scoring.get("tie", 0)
    else:
        pts += scoring.get("loss", 0)

    # margin-based hook (customize if your PDF requires)
    # margin = meta.get("margin")
    # if margin is not None and margin >= 14:
    #     pts += 1

    return pts
