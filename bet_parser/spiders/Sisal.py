# -*- coding: utf-8 -*-
import locale
import scrapy
from scrapy import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from typing import Dict
from bet_parser.constants.Sisal import Const
from bet_parser.utils.Writers import *


class SisalSpider(scrapy.Spider):
    name: str = 'sis'
    allowed_domains: list = ['sisal.it']
    start_urls: Dict[str, str] = {
        'https://www.sisal.it/scommesse-matchpoint': 'sisal_main',  # Main Page
    }
    # Set datetime locale to italian (needed for Bet365 italian pages)
    locale.setlocale(locale.LC_TIME, Const.datetime_italian_locale)

    def start_requests(self):
        for url, name in self.start_urls.items():
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'selenium': {
                                     'driver': 'chrome',
                                     'render_js': True,
                                     'wait_time': 1,
                                     'headless': True}
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
        matches_groups = response.css(Const.css_matches_groups)
        for matches_group in matches_groups:
            first_match_of_group: int = len(parsed_matches)
            # Matches description extraction
            self.parse_matches_description(matches_group, parsed_matches)
            # Matches quotes extraction
            self.parse_matches_quotes(matches_group, first_match_of_group, parsed_matches)

        # Write quotes to Firebase
        fb_writer = FirebaseWriter()
        fb_writer.write(parsed_matches)
        self.log('Saved parsed quotes on Firebase: %s' % self.name)

        # Write quotes to File
        file_writer = FileWriter('output')
        file_writer.write(self.start_urls[response.url], parsed_matches, response.body)

    def parse_matches_description(self, matches_group: Selector, parsed_matches: List[Match]):
        # Looping over Column 1 rows (Dates, Times, Match names and results)
        matches_start_date = None
        column1_rows = matches_group.css(Const.css_description_column + Const.css_child_divs)
        for row in column1_rows:
            row_class = row.xpath(Const.xpath_get_class).get(default='')
            if Const.css_date_row[1:] in row_class:
                # Extracts Matches group start date
                extr_date = row.xpath(Const.xpath_get_text).get()
                if extr_date:
                    # Let's remove the localized day name from the Date string
                    divider_index = extr_date.find(Const.match_date_divider)
                    if divider_index != -1:
                        extr_date = extr_date[divider_index + 1:len(extr_date)]
                        # Here we finally parse the Matches Date, from B365 format (Day 3-char Month and
                        # numeric Year) to BetParser output format (Year_Month_Day)
                        extr_date_with_year = extr_date + ' ' + str(Const.current_year)
                        matches_start_date = datetime.strptime(extr_date_with_year, Const.b365_date_format) \
                            .strftime(Const.output_date_format)
            elif Const.css_name_result_time_row[1:] in row_class:
                is_real_time = False
                # Extracts specific Match name, and if available real-time result (if the match is started already)
                match_team_1 = match_team_2 = match_result = None
                extr_match_name = row.css(Const.css_name_result_cell + Const.css_get_all_text).getall()
                if len(extr_match_name) == 1:
                    # Not yet started match
                    match_str = extr_match_name[0]
                    divider_index = match_str.find(Const.match_name_divider)
                    if divider_index != -1:
                        match_team_1 = match_str[0:divider_index]
                        match_team_2 = match_str[divider_index + 3:len(match_str)]
                elif len(extr_match_name) >= 3:
                    # Live match
                    is_real_time = True
                    match_team_1 = extr_match_name[0]
                    match_result = extr_match_name[1]
                    match_team_2 = extr_match_name[2]

                # Extracts specific Match starting time, and if available real time (if the match is
                # started)
                match_start_time = match_real_time = None
                extr_match_time = row.css(Const.css_time_cell + Const.css_get_all_text).getall()
                if is_real_time:
                    if len(extr_match_time) == 1:
                        match_real_time = extr_match_time[0]
                    if len(extr_match_time) == 2:
                        match_start_time = extr_match_time[0]
                        match_real_time = extr_match_time[1]
                else:
                    if len(extr_match_time) == 1:
                        match_start_time = extr_match_time[0]

                # Creates and fill Match object
                parsed_match = Match()
                parsed_match.Bookmaker = self.name
                parsed_match.StartDate = matches_start_date
                parsed_match.StartTime = match_start_time
                parsed_match.RealTime = match_real_time
                parsed_match.Team1 = match_team_1
                parsed_match.Team2 = match_team_2
                parsed_match.Result = match_result

                # Append the parsed Match to the list
                parsed_matches.append(parsed_match)

    @staticmethod
    def parse_matches_quotes(matches_group: Selector, first_match_of_group: int, parsed_matches: List[Match]):
        # Looping over Column 2, 3, 4 rows (Quotes 1, X, 2)
        quote_columns = matches_group.css(Const.css_quote_columns)
        for column in quote_columns:
            quote_type = ''
            match_number = first_match_of_group
            rows = column.xpath(Const.xpath_child_divs)
            for row in rows:
                row_class = row.xpath(Const.xpath_get_class).get(default='')
                if Const.css_quote_header[1:] in row_class:
                    quote_type = row.css(Const.css_get_all_text).get(default='')
                else:
                    quote = row.css(Const.css_get_all_text).get(default='')
                    setattr(parsed_matches[match_number], 'Quote' + quote_type, quote)
                    match_number += 1