class Config:
    SECRET_KEY = "dev"
    SQLALCHEMY_DATABASE_URI = "sqlite:///league.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCORING_FILE = "scoring.json"
    NFL_SEASON_YEAR = 2025   # <-- add this
