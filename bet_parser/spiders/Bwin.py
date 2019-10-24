# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from datetime import datetime, timedelta
from typing import Dict
from bet_parser.spiders.constants.Bwin import Const
from bet_parser.middlewares.SeleniumRequest import SeleniumRequest
from bet_parser.utils.Mappers import MatchMapper
from bet_parser.utils.Writers import *


class BwinSpider(scrapy.Spider):
    name = 'bwin'
    allowed_domains = ['bwin.fr']
    start_urls: Dict[str, str] = {
        # 'https://sports.bwin.fr/fr/sports/football-4': 'bwin_main', # it's a bit unstable, since the match are changing frequently
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/monde-6': 'bwin_world',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/europe-7': 'bwin_europe',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/italie-20': 'bwin_italy',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/angleterre-14/premier-league-46': 'bwin_eng_premier_league',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/espagne-28/laliga-16108': 'bwin_esp_liga',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/france-16/ligue-1-4131': 'bwin_fra_ligue_1',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/allemagne-17/bundesliga-43': 'bwin_ger_bundesliga',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/pays-bas-36/eredivisie-6361': 'bwin_ned_eredivise',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/portugal-37/primeira-liga-16199': 'bwin_por_primeira_liga',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/am%C3%A9rique-du-sud-42/copa-libertadores-110': 'bwin_copa_libertadores',
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
                                  wait_time=1,
                                  scroll_to_element='.footer-bottom',
                                  headless=False,
                                  extract_sub_links_by_class=['.grid-event-wrapper .grid-info-wrapper'])

    def parse(self, response: HtmlResponse):
        # Here we store the sub pages related to each match in the page (if any was found)
        sub_pages = response.request.meta['sub_pages']

        # Looping over Matches Groups
        # (this is the main loop, here we iterate on each div containing a group of matches, with its description
        # and quotes)
        matches_groups = response.css(Const.css_matches_groups)
        for matches_group in matches_groups:
            # Match rows extraction
            self.parse_matches_rows(matches_group, sub_pages, self.parsed_matches)
        del sub_pages
        del response.request.meta['sub_pages']

    def parse_matches_rows(self, matches_group: Selector, sub_pages: List[Selector], parsed_matches: List[Match]):
        # Looping over Matches Rows (Dates, Times, Match names, results, quotes)
        rows = matches_group.css(Const.css_match_rows)
        for row in rows:
            # Extracts Team names (required)
            match_teams = row.css(Const.css_match_teams)
            match_team_1 = None
            match_team_2 = None
            if len(match_teams) == 2:
                match_team_1 = match_teams[0].css(Const.css_get_all_text).get(default=None)
                match_team_1 = match_team_1.strip() if match_team_1 else match_team_1
                match_team_2 = match_teams[1].css(Const.css_get_all_text).get(default=None)
                match_team_2 = match_team_2.strip() if match_team_2 else match_team_2
            if match_team_1 is None or match_team_2 is None:
                continue

            # Extracts if any the teams type (U21, U23, etc)
            match_team_1_type = match_teams[0].css(Const.css_match_team_type).get(default=None)
            if self.is_valid_team_type(match_team_1_type):
                match_team_1 += ' ' + match_team_1_type.strip()

            match_team_2_type = match_teams[1].css(Const.css_match_team_type).get(default=None)
            if self.is_valid_team_type(match_team_2_type):
                match_team_2 += ' ' + match_team_2_type.strip()

            # Extracts Match Start Date (required) and time
            match_start_date = match_start_time = match_real_time = None
            match_start_date_time = row.css(Const.css_match_start_date_time + Const.css_get_all_text).get(
                default='').lower()
            try:
                if Const.bwin_today_date in match_start_date_time:
                    # Today
                    match_start_date = datetime.today().strftime(Const.output_date_format)
                    match_start_time = match_start_date_time.replace(Const.bwin_today_date, '').strip()
                elif Const.bwin_tomorrow_date in match_start_date_time:
                    # Tomorrow
                    match_start_date = (datetime.today() + timedelta(days=1)).strftime(Const.output_date_format)
                    match_start_time = match_start_date_time.replace(Const.bwin_tomorrow_date, '').strip()
                elif Const.bwin_real_time_1 in match_start_date_time or Const.bwin_real_time_2 in match_start_date_time\
                        or Const.bwin_real_time_3 in match_start_date_time:
                    # Real Time Match
                    match_start_date = datetime.today().strftime(Const.output_date_format)
                    if Const.bwin_real_time_3 not in match_start_date_time:
                        match_real_time = match_start_date_time.replace(Const.bwin_real_time_1, '').replace(
                            Const.bwin_real_time_2, '').strip()
                else:
                    # Future date
                    match_start_date_time = datetime.strptime(match_start_date_time, Const.bwin_date_format)
                    match_start_date = match_start_date_time.date().strftime(Const.output_date_format)
                    match_start_time = match_start_date_time.time().strftime(Const.output_time_format)
            except Exception as e:
                pass
            if match_start_date is None:
                continue

            # Extracts Live Results (if available)
            match_result = None
            match_score_values = row.css(Const.css_match_score_values)
            if len(match_score_values) == 2:
                team_1_result = match_score_values[0].css(Const.css_match_score_values_inner_vals).getall()
                if len(team_1_result) > 0:
                    match_result = team_1_result[0]
                team_2_result = match_score_values[1].css(Const.css_match_score_values_inner_vals).getall()
                if len(team_2_result) > 0:
                    match_result += '-' + team_2_result[0]

            # Extracts Match Quotes
            match_quote_1 = None
            match_quote_x = None
            match_quote_2 = None
            match_quotes_groups = row.css(Const.css_match_quotes_groups)
            if len(match_quotes_groups) > 0:
                match_quotes_values = match_quotes_groups[0].css(Const.css_match_quotes_values)
                if len(match_quotes_values) == 3:
                    match_quote_1 = match_quotes_values[0].css(Const.css_get_all_text).get(default=None)
                    match_quote_x = match_quotes_values[1].css(Const.css_get_all_text).get(default=None)
                    match_quote_2 = match_quotes_values[2].css(Const.css_get_all_text).get(default=None)

            # Creates and fill Match object
            parsed_match = Match()
            parsed_match.Bookmaker = self.name
            parsed_match.StartDate = match_start_date
            parsed_match.StartTime = match_start_time
            parsed_match.RealTime = match_real_time
            parsed_match.Result = match_result
            parsed_match.Team1 = match_team_1
            parsed_match.Team2 = match_team_2
            parsed_match.Quote1 = match_quote_1
            parsed_match.QuoteX = match_quote_x
            parsed_match.Quote2 = match_quote_2

            # Analyzing the sub page related to the currently parsed match
            sub_page_index = self.find_sub_page(sub_pages, parsed_match)
            if sub_page_index is not None:
                self.parse_sub_page(sub_pages[sub_page_index], parsed_match)
                del sub_pages[sub_page_index]
            else:
                print("ERROR: SubPage not found!!!")

            # Append the parsed Match to the list
            parsed_matches.append(parsed_match)

    @staticmethod
    def is_valid_team_type(team_type: str):
        if team_type:
            team_type = team_type.upper()
            type_u19 = 'U19'
            type_u20 = 'U20'
            type_u21 = 'U21'
            type_u23 = 'U23'
            if type_u19 in team_type or type_u20 in team_type or type_u21 in team_type or type_u23 in team_type:
                return True
        return False

    @staticmethod
    def find_sub_page(sub_pages: List[Selector], parsed_match: Match):
        if sub_pages:
            index = 0
            for sub_page in sub_pages:
                team_names = sub_page.css(Const.css_sub_option_team_names)
                if team_names and len(team_names) == 2:
                    team1 = team_names[0].css(Const.css_get_all_text).get(default='').strip()
                    team2 = team_names[1].css(Const.css_get_all_text).get(default='').strip()
                    if team1 == parsed_match.Team1 and team2 == parsed_match.Team2:
                        return index
                index += 1
        return None

    def parse_sub_page(self, sub_page: Selector, parsed_match: Match):
        # Selects all the Odds in the sub page
        odd_panels = sub_page.css(Const.css_sub_option_panel)
        for odd_panel in odd_panels:
            odd_name = odd_panel.css(Const.css_sub_option_panel_name + Const.css_get_all_text).get(default='').lower()
            if Const.css_sub_option_panel_double_chance == odd_name:
                odds_values = odd_panel.css(Const.css_sub_option_panel_values)
                if len(odds_values) >= 3:
                    parsed_match.Quote1X = odds_values[0].css(Const.css_get_all_text).get(default=None)
                    parsed_match.Quote2X = odds_values[1].css(Const.css_get_all_text).get(default=None)
                    parsed_match.Quote12 = odds_values[2].css(Const.css_get_all_text).get(default=None)
            elif Const.css_sub_option_panel_goal_no_goal == odd_name:
                odds_values = odd_panel.css(Const.css_sub_option_panel_values)
                if len(odds_values) >= 2:
                    parsed_match.QuoteGoal = odds_values[0].css(Const.css_get_all_text).get(default=None)
                    parsed_match.QuoteNoGoal = odds_values[1].css(Const.css_get_all_text).get(default=None)
            elif Const.css_sub_option_panel_under_over == odd_name:
                odds_names_and_values = odd_panel.css(Const.css_sub_option_panel_sub_names_with_values)
                for odd_name_and_value in odds_names_and_values:
                    self.fill_under_over(odd_name_and_value, parsed_match)

    @staticmethod
    def fill_under_over(odd_name_and_value: Selector, parsed_match: Match):
        odd_name = odd_name_and_value.css(Const.css_sub_option_panel_sub_names + Const.css_get_all_text).get(default='')
        odd_name = odd_name.replace(',', '').replace('.', '').lower()
        odd_value = odd_name_and_value.css(Const.css_sub_option_panel_values + Const.css_get_all_text).get(default=None)
        if not odd_value:
            return

        if 'plus de 05' in odd_name:
            parsed_match.QuoteO05 = odd_value
        elif 'moins de 05' in odd_name:
            parsed_match.QuoteU05 = odd_value
        elif 'plus de 15' in odd_name:
            parsed_match.QuoteO15 = odd_value
        elif 'moins de 15' in odd_name:
            parsed_match.QuoteU15 = odd_value
        elif 'plus de 25' in odd_name:
            parsed_match.QuoteO25 = odd_value
        elif 'moins de 25' in odd_name:
            parsed_match.QuoteU25 = odd_value
        elif 'plus de 35' in odd_name:
            parsed_match.QuoteO35 = odd_value
        elif 'moins de 35' in odd_name:
            parsed_match.QuoteU35 = odd_value
        elif 'plus de 45' in odd_name:
            parsed_match.QuoteO45 = odd_value
        elif 'moins de 45' in odd_name:
            parsed_match.QuoteU45 = odd_value

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
