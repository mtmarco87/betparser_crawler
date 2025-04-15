# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, signals
from scrapy.http import HtmlResponse
from typing import Dict
from bet_parser.spiders.constants.William import Const
from bet_parser.middlewares.SeleniumRequest import SeleniumRequest
from bet_parser.utils.Mappers import MatchMapper
from bet_parser.utils.ParserUtils import *
from bet_parser.utils.Writers import *
from datetime import date, timedelta


class SisalSpider(scrapy.Spider):
    name: str = 'william'
    allowed_domains: list = ['williamhill.it']
    start_urls: Dict[str, str] = {
        'https://sports.williamhill.it/betting/it-it/calcio/coppe-europee/uefa-champions-league?marketId': 'william_champions',
        'https://sports.williamhill.it/betting/it-it/calcio/coppe-europee/uefa-europa-league': 'william_europa_league',
        'https://sports.williamhill.it/betting/it-it/calcio/italia/serie-a': 'william_ita_serie_a',
        'https://sports.williamhill.it/betting/it-it/calcio/italia/serie-b': 'william_ita_serie_b',
        'https://sports.williamhill.it/betting/it-it/calcio/inghilterra/premier-league': 'william_eng_premier_league',
        'https://sports.williamhill.it/betting/it-it/calcio/spagna/la-liga': 'william_esp_liga',
        'https://sports.williamhill.it/betting/it-it/calcio/francia/ligue-1': 'william_fra_ligue1',
        'https://sports.williamhill.it/betting/it-it/calcio/germania/bundesliga': 'william_ger_bundesliga',
        'https://sports.williamhill.it/betting/it-it/calcio/olanda/eredivisie': 'william_ned_eredivise',
        'https://sports.williamhill.it/betting/it-it/calcio/portogallo/primeira-liga': 'william_por_primeira_liga',
        'https://sports.williamhill.it/betting/it-it/calcio/brasile/brasileiro-serie-b': 'william_brazil_serie_b',
        'https://sports.williamhill.it/betting/it-it/calcio/club-internazionali/conmebol-libertadores-group-a': 'william_copa_libertadores',
        'https://sports.williamhill.it/betting/it-it/calcio/argentina/copa-argentina': 'william_copa_argentina',
        'https://sports.williamhill.it/betting/it-it/calcio/argentina/liga-profesional': 'william_arg_liga',
    }
    parsed_matches: List[Match] = []
    script_kill_banners = 'try { ' + \
                          'document.querySelector("#modalOverlay_dimmer").remove(); ' + \
                          'document.querySelector("#popup").remove(); } ' + \
                          'catch(ex) { }'

    def start_requests(self):
        # Connect the idle status (end of all requests) to self.spider_idle method
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

        for url, name in self.start_urls.items():
            yield SeleniumRequest(url=url,
                                  callback=self.parse,
                                  driver_type='chrome',
                                  script=self.script_kill_banners,
                                  render_js=True,
                                  wait_time=2,
                                  headless=False,
                                  user_data_dir=False,
                                  extract_sub_links_by_class=['.rowOdd td:nth-of-type(8)'])

    def parse(self, response: HtmlResponse):
        # Here we store the sub pages related to each match in the page (if any was found)
        sub_pages = response.request.meta['sub_pages']

        # Looping over Matches Groups
        # (this is the main loop, here we iterate on each div containing a group of matches, with its description
        # and quotes)
        match_rows = response.css(Const.css_matches_rows)
        index = len(self.parsed_matches)
        for match_row in match_rows:
            tds = match_row.css('td')
            if len(tds) > 2:
                match_date = get_text_from_first_html_element(tds[0], 'span') \
                             or get_text_from_first_html_element(tds[0], 'a')
                match_ora = get_text_from_first_html_element(tds[1], 'span') or get_text_from_first_html_element(tds[1],
                                                                                                                 'a')
                match_name = get_text_from_first_html_element(tds[2], 'span')
                if match_date and match_ora and match_name:
                    # Matches description extraction
                    self.parse_matches_description(match_date, match_ora, match_name, self.parsed_matches, sub_pages)
                    # Matches quotes extraction
                    self.parse_matches_quotes(match_row, index, self.parsed_matches)
                    index += 1
        del sub_pages
        del response.request.meta['sub_pages']

        # # Write quotes to File
        # file_writer = FileWriter('output')
        # file_writer.write(self.start_urls[response.url], parsed_matches, response.body)

    def parse_matches_description(self, match_date: str, match_ora: str, match_name: str, parsed_matches: List[Match],
                                  sub_pages: List[Selector]):
        match_date = match_date.strip()
        if match_date == 'Oggi':
            today = date.today()
            match_date = today.strftime("%d %b")
        elif match_date == 'Domani':
            tomorrow = date.today() + timedelta(days=1)
            match_date = tomorrow.strftime("%d %b")
        # The year is missing in William Hill
        match_date = match_date + ' ' + str(datetime.today().year)

        if match_name and match_date:
            teams = match_name.split(' - ')
            team1 = teams[0].strip()
            team2 = teams[1].strip()
            # print(team1)
            # print(team2)

            # Here we convert the italian locale date to english locale
            match_date = convert_date_ita_to_eng(match_date)
            data = format_date(match_date, Const.william_date_format, Const.output_date_format)
            # print(data)
            # print(match_ora)

            parsed_match = Match()
            parsed_match.Bookmaker = self.name
            parsed_match.StartDate = data
            parsed_match.StartTime = match_ora
            parsed_match.RealTime = Const.txt_not_available
            parsed_match.Team1 = team1
            parsed_match.Team2 = team2
            parsed_match.Result = Const.txt_not_available

            # Analyzing the sub page related to the currently parsed match to extract Extra Quotes
            sub_page_index = self.find_sub_page(sub_pages, parsed_match)
            if sub_page_index is not None:
                self.parse_sub_page(sub_pages[sub_page_index], parsed_match)
                del sub_pages[sub_page_index]
            else:
                print("ERROR: SubPage not found!!!")

            parsed_matches.append(parsed_match)

    @staticmethod
    def find_sub_page(sub_pages: List[Selector], parsed_match: Match):
        if sub_pages:
            index = 0
            for sub_page in sub_pages:
                team_names = sub_page.css(Const.css_sub_team_names + ' *::text').get(
                    default='').strip().split(' - ')
                if team_names and len(team_names) >= 2:
                    team1 = team_names[0]
                    team2 = team_names[1]
                    if team1 == parsed_match.Team1 and team2 == parsed_match.Team2:
                        return index
                index += 1
        return None

    @staticmethod
    def parse_sub_page(sub_page: Selector, parsed_match: Match):
        # Selects all the Odds in the sub page
        odd_rows = sub_page.css(Const.css_sub_events)
        for odd_row in odd_rows:
            odd_name = odd_row.css(Const.css_sub_event_name + ' *::text').get(default='').replace('\n', '').replace(
                '\t', '').lower()
            if Const.css_sub_event_double_chance == odd_name:
                odds_values = odd_row.css(Const.css_sub_event_values)
                if len(odds_values) >= 3:
                    parsed_match.Quote1X = odds_values[0].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
                    parsed_match.Quote2X = odds_values[1].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
                    parsed_match.Quote12 = odds_values[2].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
            elif Const.css_sub_event_goal_no_goal == odd_name:
                odds_values = odd_row.css(Const.css_sub_event_values)
                if len(odds_values) >= 2:
                    parsed_match.QuoteGoal = odds_values[0].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
                    parsed_match.QuoteNoGoal = odds_values[1].css(' *::text').get(default=None).replace('\n',
                                                                                                        '').replace(
                        '\t', '')
            elif Const.css_sub_event_uo_05 == odd_name:
                odds_values = odd_row.css(Const.css_sub_event_values)
                if len(odds_values) >= 2:
                    parsed_match.QuoteU05 = odds_values[0].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
                    parsed_match.QuoteO05 = odds_values[1].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
            elif Const.css_sub_event_uo_15 == odd_name:
                odds_values = odd_row.css(Const.css_sub_event_values)
                if len(odds_values) >= 2:
                    parsed_match.QuoteU15 = odds_values[0].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
                    parsed_match.QuoteO15 = odds_values[1].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
            elif Const.css_sub_event_uo_25 == odd_name:
                odds_values = odd_row.css(Const.css_sub_event_values)
                if len(odds_values) >= 2:
                    parsed_match.QuoteU25 = odds_values[0].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
                    parsed_match.QuoteO25 = odds_values[1].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
            elif Const.css_sub_event_uo_35 == odd_name:
                odds_values = odd_row.css(Const.css_sub_event_values)
                if len(odds_values) >= 2:
                    parsed_match.QuoteU35 = odds_values[0].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
                    parsed_match.QuoteO35 = odds_values[1].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
            elif Const.css_sub_event_uo_45 == odd_name:
                odds_values = odd_row.css(Const.css_sub_event_values)
                if len(odds_values) >= 2:
                    parsed_match.QuoteU45 = odds_values[0].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')
                    parsed_match.QuoteO45 = odds_values[1].css(' *::text').get(default=None).replace('\n', '').replace(
                        '\t', '')

    @staticmethod
    def parse_matches_quotes(match_row: Selector, index: int, parsed_matches: List[Match]):
        # Looping over Column 2, 3, 4 rows (Quotes 1, X, 2)
        dict_keys = {0: 'Quote1', 1: 'QuoteX', 2: 'Quote2'}
        try:
            for x in range(0, 3):
                odd = get_text_from_html_element_at_position(match_row, Const.css_event_type, x).strip()
                setattr(parsed_matches[index], dict_keys[x], odd)
                # print(odd)
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
