from typing import List
from bet_parser.models.Match import Match
from googletrans import Translator


class MatchTranslator:
    translator: Translator = None
    from_lang: str = 'en'
    to_lang: str = 'en'
    word_by_word: bool = True

    def __init__(self, from_lang: str = 'en', to_lang: str = 'en', word_by_word: bool = True):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.word_by_word = word_by_word
        self.translator = Translator()

    def translate_all(self, parsed_matches: List[Match]):
        if parsed_matches:
            first = True
            big_string = ''
            for match in parsed_matches:
                if first:
                    first = False
                else:
                    big_string += ' € '

                if match.Team1:
                    big_string += '£ '
                    big_string += match.Team1.strip()
                if match.Team2:
                    big_string += ' $ '
                    big_string += match.Team2.strip()

            if self.word_by_word:
                big_string = big_string.replace(' ', '.')

            big_string = self.translator.translate(big_string, src=self.from_lang,
                                                   dest=self.to_lang).text.replace('\u200b', '')

            if self.word_by_word:
                big_string = big_string.replace('.', ' ')

            rebuilt_matches = big_string.split(' € ')
            match_index = 0
            for match in parsed_matches:
                match_team_1 = None
                match_team_2 = None

                rebuilt_match = rebuilt_matches[match_index]
                search_team_1 = rebuilt_match.split('£')
                if len(search_team_1) > 1:
                    # Team 1 is there, let's search for Team 2
                    search_team_2 = search_team_1[1].split('$')
                    match_team_1 = search_team_2[0].strip()
                    if len(search_team_2) > 1:
                        # There is also Team 2
                        match_team_2 = search_team_2[1].strip()
                else:
                    search_team_2 = search_team_1[0].split('$')
                    if len(search_team_2) > 1:
                        # There is only Team 2
                        match_team_2 = search_team_2[1].strip()

                match.Team1 = match_team_1
                match.Team2 = match_team_2
                match_index += 1

        return parsed_matches

    def translate(self, team_name):
        if team_name:
            if self.word_by_word:
                team_name = team_name.replace(' ', ',')
            team_name = self.translator.translate(team_name, src=self.from_lang, dest=self.to_lang).text
            if self.word_by_word:
                team_name.replace(',', ' ')
        return team_name
