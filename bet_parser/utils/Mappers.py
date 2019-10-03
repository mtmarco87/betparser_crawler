import re
from typing import List
from bet_parser.models.Match import Match
from .MachineLearning import ML


class MatchMapper:
    ml_algorithm: ML = None

    def __init__(self, ml_algorithm: ML = ML('cosine')):
        self.ml_algorithm = ml_algorithm

    def remap_all(self, parsed_matches: List[Match]):
        if parsed_matches:
            for match in parsed_matches:
                if match.Team1:
                    match.Team1 = self.ml_algorithm.get_by_similarity(match.Team1)
                if match.Team2:
                    match.Team2 = self.ml_algorithm.get_by_similarity(match.Team2)

        return parsed_matches

    def remap(self, team_name):
        if team_name:
            team_name = self.ml_algorithm.get_by_similarity(team_name)
        return team_name
