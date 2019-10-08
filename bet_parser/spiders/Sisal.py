# -*- coding: utf-8 -*-
import locale
import scrapy
from scrapy import Selector
from typing import Dict
from bet_parser.constants.Sisal import Const
from bet_parser.utils.Mappers import MatchMapper
from bet_parser.utils.ParserUtils import *
from bet_parser.utils.Writers import *


class SisalSpider(scrapy.Spider):
    name: str = 'sis'
    allowed_domains: list = ['sisal.it']
    start_urls: Dict[str, str] = {
        'https://www.sisal.it/scommesse-matchpoint': 'sisal_main',  # Main Page
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=18&fil=0&isMSpec=false': 'sisal_champions',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=21&fil=0&isMSpec=false': 'sisal_ita_serie_a',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=22&fil=0&isMSpec=false': 'sisal_ita_serie_b',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=86&fil=0&isMSpec=false': 'sisal_eng_premier_league',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=79&fil=0&isMSpec=false': 'sisal_esp_liga',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=14&fil=0&isMSpec=false': 'sisal_fra_ligue_1',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=4&fil=0&isMSpec=false': 'sisal_ger_bundesliga',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=29&fil=0&isMSpec=false': 'sisal_ned_eredivise',
        'https://www.sisal.it/scommesse-matchpoint/palinsesto?dis=1&man=54&fil=0&isMSpec=false': 'sisal_por_primera_liga',

    }
    # Set datetime locale to italian (needed for Bet365 italian pages)
    locale.setlocale(locale.LC_TIME, Const.datetime_italian_locale)
    match_mapper = MatchMapper()

    def start_requests(self):
        for url, name in self.start_urls.items():
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'selenium': {
                                     'driver': 'chrome',
                                     'render_js': True,
                                     # 'wait_until': EC.presence_of_element_located([By.ID, 'manifestazioneKey']),
                                     'wait_time': 10,
                                     'headless': False}
                                 })

    def parse(self, response):
        # Write quotes to File
        file_writer = FileWriter('output')
        file_writer.write(self.start_urls[response.url], [], response.body)

        # All the parsed data will be filled in the following array
        parsed_matches: List[Match] = []

        # Looping over Matches Groups
        # (this is the main loop, here we iterate on each div containing a group of matches, with its description
        # and quotes)
        match_rows = response.css(Const.css_matches_groups)

        index = 0
        for match_row in match_rows:
            match_names = match_row.css(Const.css_name_event)
            if match_names and match_names[0] is not None:
                match_name = get_text_from_html_element(match_names[0])
                if match_name is not None:
                    # Matches description extraction
                    self.parse_matches_description(match_row, parsed_matches)
                    # Matches quotes extraction
                    self.parse_matches_quotes(match_row, index, parsed_matches)
                    index += 1

        parsed_matches = self.match_mapper.map_all(parsed_matches)
        # Write quotes to Firebase
        fb_writer = FirebaseWriter()
        fb_writer.write(parsed_matches)
        self.log('Saved parsed quotes on Firebase: %s' % self.name)

        # Write quotes to File
        file_writer = FileWriter('output')
        file_writer.write(self.start_urls[response.url], parsed_matches, response.body)

    def parse_matches_description(self, match_row: Selector, parsed_matches: List[Match]):
        if match_row:
            match_name = get_text_from_first_html_element(match_row, Const.css_name_event)
            match_date = get_text_from_first_html_element(match_row, Const.css_date_event)
            if match_name and match_date:
                teams = match_name.split(' - ')
                team1 = teams[0].strip()
                team2 = teams[1].strip()
                print(team1)
                print(team2)
                split_match_date = match_date.split('ore');
                data = split_match_date[0].strip()
                ora = split_match_date[1].strip()
                if '/' in data:
                    data = format_date(data, Const.sisal_date_format, Const.output_date_format)
                elif '-' in data:
                    data = format_date(data, Const.sisal_date_format2, Const.output_date_format)
                print(data)
                print(ora)

                parsed_match = Match()
                parsed_match.Bookmaker = self.name
                parsed_match.StartDate = data
                parsed_match.StartTime = ora
                parsed_match.RealTime = Const.txt_not_available
                parsed_match.Team1 = team1
                parsed_match.Team2 = team2
                parsed_match.Result = Const.txt_not_available
                parsed_matches.append(parsed_match)

    @staticmethod
    def parse_matches_quotes(match_row: Selector, index: int, parsed_matches: List[Match]):
        # Looping over Column 2, 3, 4 rows (Quotes 1, X, 2)
        dictKeys = {0: 'Quote1', 1: 'QuoteX', 2: 'Quote2'}
        try:
            for x in range(0, 3):
                odd = get_text_from_html_element_at_position(match_row, Const.css_event_type, x)
                setattr(parsed_matches[index], dictKeys[x], odd)
                print(odd)
        except IndexError:
            print('Index Error')

    def spider_idle(self):
        # At the end of all the requests write down validation output of ML (unique array through all the parsed teams)
        self.match_mapper.write_validation_dataset()