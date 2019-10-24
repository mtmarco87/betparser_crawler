na: str = 'N/A'


class Match:
    """
    Match common data model
    """
    Bookmaker: str = na
    Team1: str = na
    Team2: str = na
    StartDate: str = na
    StartTime: str = na
    RealTime: str = na
    Result: str = na
    Quote1: str = na
    QuoteX: str = na
    Quote2: str = na
    Quote1X: str = na
    Quote2X: str = na
    Quote12: str = na
    QuoteGoal: str = na
    QuoteNoGoal: str = na
    QuoteU05: str = na
    QuoteO05: str = na
    QuoteU15: str = na
    QuoteO15: str = na
    QuoteU25: str = na
    QuoteO25: str = na
    QuoteU35: str = na
    QuoteO35: str = na
    QuoteU45: str = na
    QuoteO45: str = na
    InnerLink: str = na

    def __init__(self, bookmaker: str = na, startdate: str = na, starttime: str = na, realtime: str = na,
                 team1: str = na, team2: str = na, result: str = na):
        self.Bookmaker = bookmaker
        self.StartDate = startdate
        self.StartTime = starttime
        self.RealTime = realtime
        self.Team1 = team1
        self.Team2 = team2
        self.Result = result

    def dict(self):
        return {
            'Bookmaker': self.Bookmaker if self.Bookmaker else na,
            'StartDate': self.StartDate if self.StartDate else na,
            'StartTime': self.StartTime if self.StartTime else na,
            'RealTime': self.RealTime if self.RealTime else na,
            'Team1': self.Team1 if self.Team1 else na,
            'Team2': self.Team2 if self.Team2 else na,
            'Result': self.Result if self.Result else na,
            'Quote1': self.Quote1 if self.Quote1 else na,
            'QuoteX': self.QuoteX if self.QuoteX else na,
            'Quote2': self.Quote2 if self.Quote2 else na,
            'Quote1X': self.Quote1X if self.Quote1X else na,
            'Quote2X': self.Quote2X if self.Quote2X else na,
            'Quote12': self.Quote12 if self.Quote12 else na,
            'QuoteGoal': self.QuoteGoal if self.QuoteGoal else na,
            'QuoteNoGoal': self.QuoteNoGoal if self.QuoteNoGoal else na,
            'QuoteU05': self.QuoteU05 if self.QuoteU05 else na,
            'QuoteO05': self.QuoteO05 if self.QuoteO05 else na,
            'QuoteU15': self.QuoteU15 if self.QuoteU15 else na,
            'QuoteO15': self.QuoteO15 if self.QuoteO15 else na,
            'QuoteU25': self.QuoteU25 if self.QuoteU25 else na,
            'QuoteO25': self.QuoteO25 if self.QuoteO25 else na,
            'QuoteU35': self.QuoteU35 if self.QuoteU35 else na,
            'QuoteO35': self.QuoteO35 if self.QuoteO35 else na,
            'QuoteU45': self.QuoteU45 if self.QuoteU45 else na,
            'QuoteO45': self.QuoteO45 if self.QuoteO45 else na
        }
