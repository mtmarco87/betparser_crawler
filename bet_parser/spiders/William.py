# -*- coding: utf-8 -*-
import locale
import scrapy
from scrapy import Selector
from typing import Dict
from bet_parser.constants.William import Const
from bet_parser.utils.Mappers import MatchMapper
from bet_parser.utils.ParserUtils import *
from bet_parser.utils.Writers import *
from datetime import date


class SisalSpider(scrapy.Spider):
    name: str = 'william'
    allowed_domains: list = ['williamhill.it']
    start_urls: Dict[str, str] = {
        'http://sports.williamhill.it/bet_ita/it/betting/t/321/Serie+A.html': 'william_ita_serie_a',
        'http://sports.williamhill.it/bet_ita/it/betting/t/295/Inghilterra+Premier+League.html': 'william_eng_premier',
        'http://sports.williamhill.it/bet_ita/it/betting/t/23532/Serie+B.html': 'william_ita_serie_b',
        'http://sports.williamhill.it/bet_ita/it/betting/t/338/Spagna+La+Liga.html': 'william_esp_liga',
        'http://sports.williamhill.it/bet_ita/it/betting/t/312/Francia+Ligue+1.html': 'william_fra_ligue1'
    }
    # Set datetime locale to italian (needed for Bet365 italian pages)
    locale.setlocale(locale.LC_TIME, Const.datetime_italian_locale)
    match_mapper = MatchMapper()

    def start_requests(self):
        for url, name in self.start_urls.items():
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 # cookies={Const.access_cookie_key: Const.access_cookie_value},
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
        match_rows = response.css(Const.css_matches_rows)
        index = 0
        for match_row in match_rows:
            tds = match_row.css('td');
            if len(tds) > 2:
                match_date = get_text_from_first_html_element(tds[0], 'span')
                match_ora =  get_text_from_first_html_element(tds[1], 'span')
                match_name =  get_text_from_first_html_element(tds[2], 'span')
                if match_date and match_ora and match_name:
                     # Matches description extraction
                     self.parse_matches_description(match_date,match_ora,match_name, parsed_matches)
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

    def parse_matches_description(self, match_date: str,match_ora: str, match_name: str, parsed_matches: List[Match]):
        match_date = match_date.strip()
        if(match_date == 'Oggi'):
            today = date.today()
            match_date = today.strftime("%d %b")
        elif match_date == 'Domani':
            tomorrow = date.today() + datetime.timedelta(days=1)
            match_date = tomorrow.strftime("%d %b")
        #The year is missing in William Hill
        match_date = match_date + ' 2019'

        if match_name and match_date:
            teams = match_name.split(' - ')
            team1 = teams[0].strip()
            team2 = teams[1].strip()
            print(team1)
            print(team2)

            data = format_date(match_date, Const.william_date_format, Const.output_date_format)
            print(data)
            print(match_ora)

            parsed_match = Match()
            parsed_match.Bookmaker = self.name
            parsed_match.StartDate = data
            parsed_match.StartTime = match_ora
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
                odd = get_text_from_html_element_at_position(match_row, Const.css_event_type, x).strip()
                setattr(parsed_matches[index], dictKeys[x], odd)
                print(odd)
        except IndexError:
            print('Index Error')

    def spider_idle(self):
        # At the end of all the requests write down validation output of ML (unique array through all the parsed teams)
        self.match_mapper.write_validation_dataset()

