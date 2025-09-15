import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db
from app.models import Participant, Pick, TeamResult
from app.utils.seed import SEED
from app.utils.scoring import compute_points_for_result
from app.utils.fetchers import fetch_week_scores_stub, fetch_week_scores_espn

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/", methods=["GET", "POST"])
def admin_index():
    if request.method == "POST":
        action = request.form.get("action")
        week = int(request.form.get("week") or 1)

        if action == "seed":
            if Participant.query.count() == 0:
                for name, teams in SEED.items():
                    p = Participant(name=name)
                    db.session.add(p)
                    db.session.flush()
                    for i, team in enumerate(teams, start=1):
                        db.session.add(Pick(participant_id=p.id, pick_order=i, team=team))
                db.session.commit()
                flash("Seeded participants and picks.")
            else:
                flash("Participants already exist; skipping seed.")
            return redirect(url_for("admin.admin_index"))

        if action == "ingest_json":
            raw = request.form.get("json_payload") or "[]"
            try:
                payload = json.loads(raw)
                upserted = _upsert_results(week, payload)
                flash(f"Ingested/updated {upserted} rows for week {week}.")
            except Exception as e:
                flash(f"Error parsing JSON: {e}")
            return redirect(url_for("admin.admin_index"))

        if action == "fetch_stub":
            results = fetch_week_scores_stub(week)
            upserted = _upsert_results(week, results)
            flash(f"Stub fetch upserted {upserted} rows for week {week}.")
            return redirect(url_for("admin.admin_index"))

        if action == "fetch_espn":
            season_year = int(current_app.config.get("NFL_SEASON_YEAR", 2025))
            try:
                results = fetch_week_scores_espn(week=week, season_year=season_year)
                upserted = _upsert_results(week, results)
                flash(f"ESPN fetch upserted {upserted} rows for week {week} ({season_year}).")
            except Exception as e:
                flash(f"ESPN fetch failed: {e}")
            return redirect(url_for("admin.admin_index"))

        if action == "wipe_week":
            TeamResult.query.filter_by(week=week).delete()
            db.session.commit()
            flash(f"Wiped results for week {week}.")
            return redirect(url_for("admin.admin_index"))

    latest_week = db.session.query(TeamResult.week)\
        .order_by(TeamResult.week.desc()).limit(1).scalar()
    recent = TeamResult.query.filter_by(week=latest_week).order_by(TeamResult.team).all() if latest_week else []

    return render_template("admin.html",
                           latest_week=latest_week,
                           recent=recent,
                           title="Admin")

def _upsert_results(week: int, results: list) -> int:
    """Upsert list[{team, result, meta}] into TeamResult with computed points."""
    upserted = 0
    for r in results:
        team = r["team"]
        result = (r.get("result") or "").upper()
        meta = r.get("meta", {})
        pts = compute_points_for_result(result, meta)

        existing = TeamResult.query.filter_by(week=week, team=team).first()
        if existing:
            existing.result = result
            existing.points = pts
            existing.team_score = meta.get("team_score")
            existing.opponent_score = meta.get("opponent_score")
            existing.opponent = meta.get("opponent")
        else:
            db.session.add(TeamResult(
                week=week, 
                team=team, 
                result=result, 
                points=pts,
                team_score=meta.get("team_score"),
                opponent_score=meta.get("opponent_score"),
                opponent=meta.get("opponent")
            ))
            upserted += 1
    db.session.commit()
    return upserted
