# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, signals
from typing import Dict
from scrapy.http import HtmlResponse
from bet_parser.constants.Sisal import Const
from bet_parser.middlewares.SeleniumRequest import SeleniumRequest
from bet_parser.utils.Mappers import MatchMapper
from bet_parser.utils.ParserUtils import *
from bet_parser.utils.Writers import *


class SisalSpider(scrapy.Spider):
    name: str = 'sis'
    allowed_domains: list = ['sisal.it']
    start_urls: Dict[str, str] = {
        'https://www.sisal.it/scommesse-matchpoint': 'sisal_main',  # Main Page
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=42&fil=0&isMSpec=false': 'sisal_euro_2020_qualifications',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=178&fil=0&isMSpec=false': 'sisal_euro_u21_qualifications',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=185&fil=0&isMSpec=false': 'sisal_euro_u19_qualifications',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=132&fil=0&isMSpec=false': 'sisal_asia_fifa_2022_qualifications',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=18&fil=0&isMSpec=false': 'sisal_champions',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=153&fil=0&isMSpec=false': 'sisal_europa_league',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=21&fil=0&isMSpec=false': 'sisal_ita_serie_a',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=22&fil=0&isMSpec=false': 'sisal_ita_serie_b',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=86&fil=0&isMSpec=false': 'sisal_eng_premier_league',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=79&fil=0&isMSpec=false': 'sisal_esp_liga',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=14&fil=0&isMSpec=false': 'sisal_fra_ligue_1',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=4&fil=0&isMSpec=false': 'sisal_ger_bundesliga',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=29&fil=0&isMSpec=false': 'sisal_ned_eredivise',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=54&fil=0&isMSpec=false': 'sisal_por_primera_liga',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=555&fil=0&isMSpec=false': 'sisal_arg_b_metropolitana',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=256&fil=0&isMSpec=false': 'sisal_arg_b_nacional',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=33&fil=0&isMSpec=false': 'sisal_copa_libertadores',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=257&fil=0&isMSpec=false': 'sisal_brazil_serie_b',
    }
    parsed_matches: List[Match] = []

    def start_requests(self):
        # Connect the idle status (end of all requests) to self.spider_idle method
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

        # Start requests
        for url, name in self.start_urls.items():
            yield SeleniumRequest(url=url,
                                  callback=self.parse,
                                  driver_type='chrome',
                                  render_js=True,
                                  wait_time=2,
                                  # 'wait_until': EC.presence_of_element_located([By.ID, 'manifestazioneKey']),
                                  headless=False,
                                  user_data_dir=False)

    def parse(self, response: HtmlResponse):
        # Checking if we are in a page specific to certain Match Name Types (U21, U23, etc)
        page_type = None
        try:
            page_type = self.start_urls[response.url]
        except Exception as e:
            self.log('Error: ' + e)
        default_match_type = self.get_match_name_type(page_type)

        # Looping over Matches Groups
        # (this is the main loop, here we iterate on each div containing a group of matches, with its description
        # and quotes)
        match_rows = response.css(Const.css_matches_groups)
        index = len(self.parsed_matches)
        for match_row in match_rows:
            match_names = match_row.css(Const.css_name_event)
            if match_names and match_names[0] is not None:
                match_name = get_text_from_html_element(match_names[0])
                if match_name is not None:
                    # Matches description extraction
                    result = self.parse_matches_description(match_row, default_match_type, self.parsed_matches)

                    if result:
                        # Matches quotes extraction
                        self.parse_matches_quotes(match_row, index, self.parsed_matches)
                        index += 1

        # # Write quotes to File
        # file_writer = FileWriter('output')
        # file_writer.write(self.start_urls[response.url], parsed_matches, response.body)

    def parse_matches_description(self, match_row: Selector, default_match_type: str, parsed_matches: List[Match]):
        if match_row:
            match_name = get_text_from_first_html_element(match_row, Const.css_name_event)
            if not default_match_type:
                default_match_type = self.get_match_name_type(get_text_from_first_html_element(match_row,
                                                                                               Const.css_name_type))
            match_date = get_text_from_first_html_element(match_row, Const.css_date_event)

            # Here we discard empty rows composed only by a Match name with no quotes
            if 'speciali live' in match_name.lower():
                return False

            if match_name and match_date:
                teams = match_name.split(' - ')
                team1 = teams[0].strip()
                team2 = teams[1].strip()
                # print(team1)
                # print(team2)
                if default_match_type:
                    team1 += ' ' + default_match_type
                    team2 += ' ' + default_match_type

                split_match_date = match_date.lower().split('ore')
                data = split_match_date[0].strip()
                ora = split_match_date[1].strip()

                if '/' in data:
                    data = format_date(data, Const.sisal_date_format, Const.output_date_format)
                elif '-' in data:
                    data = format_date(data, Const.sisal_date_format2, Const.output_date_format)
                elif data == '':
                    data = datetime.today().strftime(Const.output_date_format)

                if ora:
                    ora = format_date(ora, Const.sisal_time_format, Const.output_time_format)
                # print(data)
                # print(ora)

                parsed_match = Match()
                parsed_match.Bookmaker = self.name
                parsed_match.StartDate = data
                parsed_match.StartTime = ora
                parsed_match.RealTime = Const.txt_not_available
                parsed_match.Team1 = team1
                parsed_match.Team2 = team2
                parsed_match.Result = Const.txt_not_available
                parsed_matches.append(parsed_match)

                return True

    @staticmethod
    def parse_matches_quotes(match_row: Selector, index: int, parsed_matches: List[Match]):
        # Looping over Column 2, 3, 4 rows (Quotes 1, X, 2)
        dictKeys = {0: 'Quote1', 1: 'QuoteX', 2: 'Quote2'}
        try:
            for x in range(0, 3):
                odd = get_text_from_html_element_at_position(match_row, Const.css_event_type, x)
                setattr(parsed_matches[index], dictKeys[x], odd)
                # print(odd)
        except IndexError:
            print('Index Error')

    @staticmethod
    def get_match_name_type(event_type: str):
        if event_type:
            event_type = event_type.upper()
            type_u19 = 'U19'
            type_u20 = 'U20'
            type_u21 = 'U21'
            type_u23 = 'U23'
            if type_u19 in event_type:
                return type_u19
            elif type_u20 in event_type:
                return type_u20
            elif type_u21 in event_type:
                return type_u21
            elif type_u23 in event_type:
                return type_u23
        return None

    def spider_idle(self):
        # End of all the requests

        match_mapper = MatchMapper()
        # Try to remap each match team name to the global en-EN one (if found by the ML system)
        self.parsed_matches = match_mapper.map_all(self.parsed_matches)
        # Write down validation output of ML to file (unique array through all the parsed teams)
        match_mapper.write_validation_dataset()

        # Write quotes to Firebase
        FirebaseWriter().write(self.parsed_matches)
        self.log('Saved parsed quotes on Firebase: %s' % self.name)
