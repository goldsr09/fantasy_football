# Fantasy Football League

A Flask-based fantasy football league application that tracks team picks, weekly results, and provides detailed player statistics.

## Features

- **Leaderboard**: View current standings with total points
- **Player Details**: Click on any player to see their weekly team performance with actual NFL scores
- **Real-time Data**: Fetches live NFL scores from ESPN
- **Admin Panel**: Manage participants, picks, and game results
- **Responsive Design**: Works on desktop and mobile devices

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/goldsr09/fantasy_football.git
   cd fantasy_football
   ```

2. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 run.py
   ```

4. **Access the app**:
   - Local: http://localhost:5010
   - Admin: http://localhost:5010/admin/

## Usage

1. **Seed Data**: Go to the admin panel and click "Seed" to add sample participants and picks
2. **Fetch Scores**: Use "Fetch ESPN" to get real NFL game results with actual scores
3. **View Results**: Check the leaderboard and click on player names for detailed weekly breakdowns

## Project Structure

```
fantasy-league/
├── app/
│   ├── models/          # Database models
│   ├── routes/          # Flask routes
│   ├── templates/       # HTML templates
│   └── utils/           # Utility functions
├── instance/            # Database files (not in git)
├── run.py              # Application entry point
└── requirements.txt    # Python dependencies
```

## Technologies Used

- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Bootstrap**: Frontend styling
- **ESPN API**: Real NFL data
- **SQLite**: Database

## Contributing

Feel free to submit issues and enhancement requests!
