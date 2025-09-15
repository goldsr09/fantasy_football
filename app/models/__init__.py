from datetime import datetime
from app import db

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class Pick(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("participant.id"), nullable=False)
    pick_order = db.Column(db.Integer, nullable=False)  # 1, 2, 3
    team = db.Column(db.String, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("participant_id", "pick_order", name="uq_participant_pickorder"),
    )

class TeamResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer, nullable=False)
    team = db.Column(db.String, nullable=False)         # must match Pick.team
    result = db.Column(db.String, nullable=False)       # "W" / "L" / "T"
    points = db.Column(db.Float, nullable=False, default=0.0)
    team_score = db.Column(db.Integer, nullable=True)   # team's score in the game
    opponent_score = db.Column(db.Integer, nullable=True)  # opponent's score in the game
    opponent = db.Column(db.String, nullable=True)      # opponent team name
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("week", "team", name="uq_week_team"),
    )
