from flask import Blueprint, render_template
from app import db
from app.models import Participant, Pick, TeamResult

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    participants = Participant.query.order_by(Participant.name).all()
    rows = []
    for p in participants:
        picks = Pick.query.filter_by(participant_id=p.id).order_by(Pick.pick_order).all()
        teams = [pk.team for pk in picks]
        total_points = db.session.query(
            db.func.coalesce(db.func.sum(TeamResult.points), 0.0)
        ).filter(TeamResult.team.in_(teams)).scalar() or 0.0

        rows.append({"name": p.name, "teams": teams, "points": round(total_points, 2)})

    rows.sort(key=lambda r: (-r["points"], r["name"].lower()))
    return render_template("leaderboard.html", rows=rows, title="Leaderboard")

@main_bp.route("/participants")
def participants():
    rows = db.session.query(Participant, Pick)\
        .join(Pick, Participant.id == Pick.participant_id)\
        .order_by(Participant.name, Pick.pick_order).all()

    table = {}
    for p, pk in rows:
        table.setdefault(p.name, [None, None, None])
        table[p.name][pk.pick_order - 1] = pk.team

    return render_template("participants.html", table=table, title="Participants")

@main_bp.route("/player/<player_name>")
def player_detail(player_name):
    # Get the participant
    participant = Participant.query.filter_by(name=player_name).first()
    if not participant:
        return "Player not found", 404
    
    # Get their picks
    picks = Pick.query.filter_by(participant_id=participant.id).order_by(Pick.pick_order).all()
    teams = [pk.team for pk in picks]
    
    # Get all weeks and team results for this player's teams
    weeks = db.session.query(TeamResult.week).filter(TeamResult.team.in_(teams)).distinct().order_by(TeamResult.week).all()
    weeks = [w[0] for w in weeks]
    
    # Build weekly data
    weekly_data = []
    for week in weeks:
        week_results = TeamResult.query.filter_by(week=week).filter(TeamResult.team.in_(teams)).all()
        week_total = sum(tr.points for tr in week_results)
        
        team_results = {}
        for tr in week_results:
            team_results[tr.team] = {
                'result': tr.result,
                'points': tr.points,
                'team_score': tr.team_score,
                'opponent_score': tr.opponent_score,
                'opponent': tr.opponent
            }
        
        weekly_data.append({
            'week': week,
            'total_points': round(week_total, 2),
            'team_results': team_results
        })
    
    # Calculate total points
    total_points = db.session.query(
        db.func.coalesce(db.func.sum(TeamResult.points), 0.0)
    ).filter(TeamResult.team.in_(teams)).scalar() or 0.0
    
    return render_template("player_detail.html", 
                         participant=participant, 
                         teams=teams, 
                         weekly_data=weekly_data,
                         total_points=round(total_points, 2),
                         title=f"{participant.name} - Team Scores")
