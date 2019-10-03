from typing import List
from .MachineLearning import WordSimilarityML
from bet_parser.utils.Writers import FileWriter
from bet_parser.models.Match import Match
from bet_parser.settings import *


class MatchMapper:
    """
    Match Mapper

    This class can remap all the team names in a set of parsed matches, or in a single match to the
    corresponding standard en-EN team name.
    To perform the matching the class make use of a Machine Learning algorithm and a source/target dataset.

    After each matching the class produces a validation output, with still unknown team names, that can be lately
    manually added to the source dataset for increased knowledge of the model.
    """
    ml_algorithm: WordSimilarityML = None
    validation_dataset: dict = {}

    def __init__(self, ml_algorithm: WordSimilarityML = WordSimilarityML(dataset_source=TEAM_NAMES_DATASET_SOURCE,
                                                                         dataset_target=TEAM_NAMES_DATASET_TARGET,
                                                                         algorithm='cos',
                                                                         sanitize_array=TEAM_NAMES_SANITIZE_ARRAY)):
        self.ml_algorithm: WordSimilarityML = ml_algorithm

    def map_all(self, parsed_matches: List[Match]):
        if parsed_matches:
            for match in parsed_matches:
                if match.Team1:
                    match.Team1 = self.map(match.Team1)
                if match.Team2:
                    match.Team2 = self.map(match.Team2)

        return parsed_matches

    def map(self, team_name):
        result = team_name

        if team_name:
            # Search for Team Name mapping through ML
            ml_result = self.ml_algorithm.get(team_name)
            if ml_result.mapped_word:
                # If a mapping is found take it
                result = ml_result.mapped_word
            elif ml_result.key_word not in self.validation_dataset.keys():
                # If there is no mapping, return the original value, and collect validation data
                # if it hasn't been taken yet (sanitized word+original word)
                self.validation_dataset[ml_result.key_word] = team_name

        return result

    def write_validation_dataset(self):
        if self.validation_dataset and TEAM_NAMES_VALIDATION_PATH and \
                (TEAM_NAMES_VALIDATION_FILE or
                 SANITIZED_TEAM_NAMES_VALIDATION_FILE or
                 ORIGINAL_TEAM_NAMES_VALIDATION_FILE):
            file_writer = FileWriter(TEAM_NAMES_VALIDATION_PATH)
            for key, original in self.validation_dataset.items():
                if TEAM_NAMES_VALIDATION_FILE:
                    file_writer.append(TEAM_NAMES_VALIDATION_FILE, key + ',' + original + '\n')
                if SANITIZED_TEAM_NAMES_VALIDATION_FILE:
                    file_writer.append(SANITIZED_TEAM_NAMES_VALIDATION_FILE, key + '\n')
                if ORIGINAL_TEAM_NAMES_VALIDATION_FILE:
                    file_writer.append(ORIGINAL_TEAM_NAMES_VALIDATION_FILE, original + '\n')
