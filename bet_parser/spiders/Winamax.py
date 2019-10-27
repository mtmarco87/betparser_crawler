# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector, signals
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
        'http://sports.williamhill.it/bet_ita/it/betting/y/5/Calcio.html': 'william_main',
        'http://sports.williamhill.it/bet_ita/it/betting/t/33193/Qualificazioni+UEFA+EURO+2020.html': 'william_euro_2020_qualifications',
        'http://sports.williamhill.it/bet_ita/it/betting/t/344/UEFA+Champions+League.html': 'william_champions',
        'http://sports.williamhill.it/bet_ita/it/betting/t/1935/UEFA+Europa+League.html': 'william_europa_league',
        'http://sports.williamhill.it/bet_ita/it/betting/t/321/Serie+A.html': 'william_ita_serie_a',
        'http://sports.williamhill.it/bet_ita/it/betting/t/23532/Serie+B.html': 'william_ita_serie_b',
        'http://sports.williamhill.it/bet_ita/it/betting/t/295/Inghilterra+Premier+League.html': 'william_eng_premier_league',
        'http://sports.williamhill.it/bet_ita/it/betting/t/338/Spagna+La+Liga.html': 'william_esp_liga',
        'http://sports.williamhill.it/bet_ita/it/betting/t/312/Francia+Ligue+1.html': 'william_fra_ligue1',
        'http://sports.williamhill.it/bet_ita/it/betting/t/315/Germania+Bundesliga.html': 'william_ger_bundesliga',
        'http://sports.williamhill.it/bet_ita/it/betting/t/306/Olanda+Eredivisie.html': 'william_ned_eredivise',
        'http://sports.williamhill.it/bet_ita/it/betting/t/331/Portogallo+Primeira+Liga.html': 'william_por_primeira_liga',
        'http://sports.williamhill.it/bet_ita/it/betting/t/1713/Brasile+Serie+B.html': 'william_brazil_serie_b',
        'http://sports.williamhill.it/bet_ita/it/betting/t/356/Coppa+Libertadores.html': 'william_copa_libertadores',
        'http://sports.williamhill.it/bet_ita/it/betting/t/7480/Copa+Argentina.html': 'william_copa_argentina',
        'http://sports.williamhill.it/bet_ita/it/betting/t/3252/Argentina+Primera+B+Nacional.html': 'william_arg_prim_b_nac',
        'http://sports.williamhill.it/bet_ita/it/betting/t/3131/Argentina+Primera+B+Metropolitana.html': 'william_arg_prim_b_metr',
    }
    parsed_matches: List[Match] = []
    script_kill_banners = 'document.querySelector("#modalOverlay_dimmer").remove(); ' + \
                          'document.querySelector("#popup").remove(); '

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
                                  extract_sub_links_by_class='.rowOdd td:nth-of-type(8)')

    def parse(self, response):
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
