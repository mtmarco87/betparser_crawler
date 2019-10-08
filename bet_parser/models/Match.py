class Match:
    """
    Match common data model
    """
    na: str = 'N/A'
    Bookmaker: str = na
    StartDate: str = na
    StartTime: str = na
    RealTime: str = na
    Team1: str = na
    Team2: str = na
    Quote1: str = na
    QuoteX: str = na
    Quote2: str = na
    Result: str = na

    def __init__(self, bookmaker: str = na, startdate: str = na, starttime: str = na, realtime: str = na,
                 team1: str = na, team2: str = na, quote1: str = na, quotex: str = na, quote2: str = na,
                 result: str = na):
        self.Bookmaker = bookmaker
        self.StartDate = startdate
        self.StartTime = starttime
        self.RealTime = realtime
        self.Team1 = team1
        self.Team2 = team2
        self.Quote1 = quote1
        self.QuoteX = quotex
        self.Quote2 = quote2
        self.Result = result

    def dict(self):
        return {
            'Bookmaker': self.Bookmaker if self.Bookmaker else Match.na,
            'StartDate': self.StartDate if self.StartDate else Match.na,
            'StartTime': self.StartTime if self.StartTime else Match.na,
            'RealTime': self.RealTime if self.RealTime else Match.na,
            'Team1': self.Team1 if self.Team1 else Match.na,
            'Team2': self.Team2 if self.Team2 else Match.na,
            'Quote1': self.Quote1 if self.Quote1 else Match.na,
            'QuoteX': self.QuoteX if self.QuoteX else Match.na,
            'Quote2': self.Quote2 if self.Quote2 else Match.na,
            'Result': self.Result if self.Result else Match.na
        }
