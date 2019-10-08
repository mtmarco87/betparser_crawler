# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from datetime import datetime, timedelta
from typing import Dict
from bet_parser.constants.Bwin import Const
from bet_parser.middlewares.SeleniumRequest import SeleniumRequest
from bet_parser.utils.Mappers import MatchMapper
from bet_parser.utils.Writers import *


class BwinSpider(scrapy.Spider):
    name = 'bwin'
    allowed_domains = ['bwin.fr']
    start_urls: Dict[str, str] = {
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/monde-6': 'bwin_world',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/europe-7': 'bwin_europe',
        'https://sports.bwin.fr/fr/sports/football-4/paris-sportifs/italie-20': 'bwin_italy',
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
                                  wait_time=0.5,
                                  scroll_to_element='footer-bottom',
                                  headless=False)

    def parse(self, response: HtmlResponse):
        # tmp = FileWriter('output')
        # tmp.write('test', [], response.body)

        # Looping over Matches Groups
        # (this is the main loop, here we iterate on each div containing a group of matches, with its description
        # and quotes)
        matches_groups = response.css(Const.css_matches_groups)
        for matches_group in matches_groups:
            # Match rows extraction
            self.parse_matches_rows(matches_group, self.parsed_matches)

    def parse_matches_rows(self, matches_group: Selector, parsed_matches: List[Match]):
        # Looping over Matches Rows (Dates, Times, Match names, results, quotes)
        matches_start_date = None
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
                elif Const.bwin_real_time_1 in match_start_date_time or Const.bwin_real_time_2 in match_start_date_time:
                    # Real Time Match
                    match_start_date = datetime.today().strftime(Const.output_date_format)
                    match_real_time = match_start_date_time.replace(Const.bwin_real_time_1, '').replace(
                        Const.bwin_real_time_2, '').strip()
                    pass
                else:
                    # Future date
                    match_start_date_time = datetime.strptime(match_start_date_time, Const.bwin_date_format)
                    match_start_date = match_start_date_time.date().strftime(Const.output_date_format)
                    match_start_time = match_start_date_time.time().strftime(Const.output_time_format)
            except Exception:
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

            # Append the parsed Match to the list
            parsed_matches.append(parsed_match)

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
