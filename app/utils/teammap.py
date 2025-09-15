# Map your display names <-> ESPN abbreviations
DISPLAY_TO_ESPN = {
    "Ravens":"BAL","Steelers":"PIT","Seahawks":"SEA",
    "Eagles":"PHI","Cardinals":"ARI","Falcons":"ATL",
    "Packers":"GB","Jags":"JAX","Giants":"NYG",
    "Bills":"BUF","Bears":"CHI","Titans":"TEN",
    "Chiefs":"KC","Cowboys":"DAL","Pats":"NE",
    "Lions":"DET","Texans":"HOU","Dolphins":"MIA",
    "Wash":"WSH","Chargers":"LAC","Jets":"NYJ",
    "Rams":"LAR","Bucs":"TB","Panthers":"CAR",
    "49ers":"SF","Vikings":"MIN","Colts":"IND",
    "Broncos":"DEN","Bengals":"CIN","Browns":"CLE",
}

ESPN_TO_DISPLAY = {v: k for k, v in DISPLAY_TO_ESPN.items()}
