# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, signals
from typing import Dict
from bet_parser.spiders.constants.Eurobet import Const
from bet_parser.middlewares.SeleniumRequest import SeleniumRequest
from bet_parser.utils.Mappers import MatchMapper
from bet_parser.utils.ParserUtils import *
from bet_parser.utils.Writers import *
from datetime import date


class SisalSpider(scrapy.Spider):
    name: str = 'eurobet'
    allowed_domains: list = ['eurobet.it']
    start_urls: Dict[str, str] = {
        #'http://sports.williamhill.it/bet_ita/it/betting/y/5/Calcio.html': 'william_main',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/33193/Qualificazioni+UEFA+EURO+2020.html': 'william_euro_2020_qualifications',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/9009/Qual.+Campionati+Europei+U21.html': 'william_euro_u21_qualifications',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/33159/Coppa+del+Mondo+2022+-+Qualificazioni+Asia.html': 'william_asia_fifa_2022_qualifications',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/344/UEFA+Champions+League.html': 'william_champions',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/1935/UEFA+Europa+League.html': 'william_europa_league',
        'https://www.eurobet.it/it/scommesse/?splash=false#!/calcio/it-serie-a/': 'eurobet_ita_serie_a',
        'https://www.eurobet.it/it/scommesse/?splash=false#!/calcio/it-serie-b1/': 'eurobet_ita_serie_b'
        #'http://sports.williamhill.it/bet_ita/it/betting/t/295/Inghilterra+Premier+League.html': 'william_eng_premier_league',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/338/Spagna+La+Liga.html': 'william_esp_liga',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/312/Francia+Ligue+1.html': 'william_fra_ligue1',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/315/Germania+Bundesliga.html': 'william_ger_bundesliga',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/306/Olanda+Eredivisie.html': 'william_ned_eredivise',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/331/Portogallo+Primeira+Liga.html': 'william_por_primeira_liga',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/1713/Brasile+Serie+B.html': 'william_brazil_serie_b',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/356/Coppa+Libertadores.html': 'william_copa_libertadores',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/7480/Copa+Argentina.html': 'william_copa_argentina',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/3252/Argentina+Primera+B+Nacional.html': 'william_arg_prim_b_nac',
        #'http://sports.williamhill.it/bet_ita/it/betting/t/3131/Argentina+Primera+B+Metropolitana.html': 'william_arg_prim_b_metr',
    }
    parsed_matches: List[Match] = []

    def start_requests(self):
        # Connect the idle status (end of all requests) to self.spider_idle method
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

        for url, name in self.start_urls.items():
            yield SeleniumRequest(url=url,
                                  callback=self.parse,
                                  driver_type='chrome',
                                  render_js=True,
                                  wait_time=20,
                                  headless=False)

    def parse(self, response):
        # Looping over Matches Groups
        # (this is the main loop, here we iterate on each div containing a group of matches, with its description
        # and quotes)
        match_rows = response.css(Const.css_matches_rows)
        print('ho' + str(len(match_rows)) + 'partite da parsare')
        index = len(self.parsed_matches)
        for match_row in match_rows:
                time_box = get_first_element(match_row, '.time-box')
                date_infos = get_elements(match_row, 'p')
                if len(date_infos) > 1:
                    match_date = get_text_from_html_element_at_position(time_box, 'p', 0);
                    match_ora = get_text_from_html_element_at_position(time_box, 'p', 1);
                else:
                    match_date = 'Oggi';
                    match_ora = get_text_from_html_element_at_position(time_box, 'p', 0);

                match_name = ""
                for x in range (0,3):
                    match_name += get_text_from_html_element_at_position(match_row, '.event-players a span', x)

                print(match_date)
                print(match_ora)
                print(match_name)
                if match_date and match_ora and match_name:
                    # Matches description extraction
                    self.parse_matches_description(match_date, match_ora, match_name, self.parsed_matches)
                    # Matches quotes extraction
                    self.parse_matches_quotes(match_row, index, self.parsed_matches)
                    index += 1

        # # Write quotes to File
        # file_writer = FileWriter('output')
        # file_writer.write(self.start_urls[response.url], parsed_matches, response.body)

    def parse_matches_description(self, match_date: str, match_ora: str, match_name: str, parsed_matches: List[Match]):
        match_date = match_date.strip()
        if match_date == 'Oggi':
             today = date.today()
             match_date = today.strftime("%d/%m")
        # elif match_date == 'Domani':
        #     tomorrow = date.today() + timedelta(days=1)
        #     match_date = tomorrow.strftime("%d %b")
        # The year is missing in William Hill
        match_date = match_date + '/' + str(datetime.today().year)

        if match_name and match_date:
            teams = match_name.split('-')
            team1 = teams[0].strip()
            team2 = teams[1].strip()
            print(team1)
            print(team2)

            data = format_date(match_date, Const.eurobet_date_format, Const.output_date_format)
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
        dict_keys = {0: 'Quote1', 1: 'QuoteX', 2: 'Quote2'}
        try:
            for x in range(0, 3):
                odd = get_text_from_html_element_at_position(match_row, Const.css_event_type, x).strip()
                setattr(parsed_matches[index], dict_keys[x], odd)
                print(odd)
        except IndexError:
            print('Index Error')

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
