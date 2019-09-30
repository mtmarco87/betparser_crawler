# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime
import locale
from bet_parser.constants.Bet365 import Const
from bet_parser.utils.Writers import *


class Bet365Spider(scrapy.Spider):
    name: str = 'b365'
    allowed_domains: list = ['bet365.it']
    start_urls: dict = {
        'https://www.bet365.it/#/HO/': 'b365_main',                             # Main Page
        'https://www.bet365.it/#/AC/B1/C1/D13/E113/F16/': 'b365_ita_league',    # Italian Championship
        'https://www.bet365.it/#/AC/B1/C1/D13/E108/F16/': 'b365_europe_elite'   # Europe Elite
    }

    def start_requests(self):
        for url, name in self.start_urls.items():
            yield SplashRequest(url, self.parse,
                                args={'wait': 3, 'html': 0, 'png': 0},
                                session_id=1,
                                cookies={Const.access_cookie_key: Const.access_cookie_value}
                                )

    def parse(self, response):
        # All the parsed data will be filled in the following array
        parsed_matches = []
        # Set datetime locale to italian
        locale.setlocale(locale.LC_TIME, Const.datetime_italian_locale)

        # Looping over Matches Groups
        # (this is the main loop, here we iterate on each div containing a group of matches, with its description
        # and quotes)
        matches_groups = response.css(Const.css_matches_groups)
        for matches_group in matches_groups:
            first_match_of_group = len(parsed_matches)
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

    def parse_matches_description(self, matches_group, parsed_matches):
        # Looping over Column 1 rows (Dates, Times, Match names and results)
        matches_start_date = Const.txt_not_available
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
                match_team_1 = match_team_2 = match_result = Const.txt_not_available
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
                match_start_time = Const.txt_not_available
                match_real_time = Const.txt_not_available
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

                parsed_matches.append({'Bookmaker': self.name,
                                       'StartDate': matches_start_date,
                                       'StartTime': match_start_time,
                                       'RealTime': match_real_time,
                                       'Team1': match_team_1,
                                       'Team2': match_team_2,
                                       'Result': match_result})

    @staticmethod
    def parse_matches_quotes(matches_group, first_match_of_group, parsed_matches):
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
                    parsed_matches[match_number]['Quote' + quote_type] = quote
                    match_number += 1
