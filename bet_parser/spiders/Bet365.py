# -*- coding: utf-8 -*-
import locale
import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from datetime import datetime
from typing import Dict
from bet_parser.constants.Bet365 import Const
from bet_parser.middlewares.SeleniumRequest import SeleniumRequest
from bet_parser.utils.Mappers import MatchMapper
from bet_parser.utils.Writers import *


class Bet365Spider(scrapy.Spider):
    name: str = 'b365'
    allowed_domains: list = ['bet365.it']
    start_urls: Dict[str, str] = {
        'https://www.bet365.it/#/HO/': 'b365_main',  # Main Page
        'https://www.bet365.it/#/AC/B1/C1/D13/E43757159/F2/': 'b365_euro_2020_qualifications',
        'https://www.bet365.it/#/AC/B1/C1/D13/E108/F16/': 'b365_europe_elite',  # Europe Elite
        'https://www.bet365.it/#/AC/B1/C1/D13/E113/F16/': 'b365_ita_list',
        'https://www.bet365.it/#/AC/B1/C1/D13/E43316955/F2/': 'b365_champions',
        'https://www.bet365.it/#/AC/B1/C1/D13/E43330565/F2/': 'b365_europa_league',
        'https://www.bet365.it/#/AC/B1/C1/D13/E42856517/F2/': 'b365_ita_serie_a',
        'https://www.bet365.it/#/AC/B1/C1/D13/E43062117/F2/': 'b365_ita_serie_b',
        'https://www.bet365.it/#/AC/B1/C1/D13/E37628398/F2/': 'b365_eng_premier_league',
        'https://www.bet365.it/#/AC/B1/C1/D13/E42493286/F2/': 'b365_esp_liga',
        'https://www.bet365.it/#/AC/B1/C1/D13/E42481795/F2/': 'b365_fra_ligue_1',
        'https://www.bet365.it/#/AC/B1/C1/D13/E42422049/F2/': 'b365_ger_bundesliga',
        'https://www.bet365.it/#/AC/B1/C1/D13/E42536104/F2/': 'b365_ned_eredivise',
        'https://www.bet365.it/#/AC/B1/C1/D13/E42549026/F2/': 'b365_por_primeira_liga',
        'https://www.bet365.it/#/AC/B1/C1/D13/E42549000/F2/:/AC/B1/C1/D13/E42590533/F2/:/AC/B1/C1/D13/E43069627/F2/:' +
        '/AC/B1/C1/D13/E42869049/F2/:/AC/B1/C1/D13/E43308636/F2/:/AC/B1/C1/D13/E42765933/F2/:' +
        '/AC/B1/C1/D13/E43401262/F2/:/AC/B1/C1/D13/E42478935/F2/': 'b365_custom_latin_america_1'
    }
    # Set datetime locale to italian (needed for Bet365 italian pages)
    locale.setlocale(locale.LC_TIME, Const.datetime_italian_locale)
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
                                  headless=False,
                                  extract_sub_links_by_class='sl-CouponFixtureLinkParticipant_Name')

    def parse(self, response: HtmlResponse):
        # Needed for sub pages processing. It has to be refreshed for each page scraped
        initial_index = len(self.parsed_matches)

        # Looping over Matches Groups (for principal page)
        # (this is the main loop, here we iterate on each div containing a group of matches, with its description
        # and quotes)
        matches_groups = response.css(Const.css_matches_groups)
        for matches_group in matches_groups:
            current_index: int = len(self.parsed_matches)
            # Matches description extraction
            self.parse_matches_description(matches_group, self.parsed_matches)
            # Matches quotes extraction
            self.parse_matches_quotes(matches_group, current_index, self.parsed_matches)

        # Looping over Sub Pages related to any single match already parsed (for principal page)
        sub_pages = response.request.meta['sub_pages']
        self.parse_sub_pages(sub_pages, initial_index, self.parsed_matches)
        del sub_pages
        del response.request.meta['sub_pages']

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
                        try:
                            matches_start_date = datetime.strptime(extr_date_with_year, Const.b365_date_format) \
                                .strftime(Const.output_date_format)
                        except Exception:
                            pass
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
    def parse_matches_quotes(matches_group: Selector, current_index: int, parsed_matches: List[Match]):
        # Looping over Column 2, 3, 4 rows (Quotes 1, X, 2)
        quote_columns = matches_group.css(Const.css_quote_columns)
        for column in quote_columns:
            quote_type = ''
            match_number = current_index
            rows = column.xpath(Const.xpath_child_divs)
            for row in rows:
                row_class = row.xpath(Const.xpath_get_class).get(default='')
                if Const.css_quote_header[1:] in row_class:
                    quote_type = row.css(Const.css_get_all_text).get(default='')
                else:
                    quote = row.css(Const.css_get_all_text).get(default=None)
                    setattr(parsed_matches[match_number], 'Quote' + quote_type, quote)
                    match_number += 1

    @staticmethod
    def parse_sub_pages(sub_pages: List[Selector], initial_index: int, parsed_matches: List[Match]):
        match_number = initial_index
        for sub_page in sub_pages:
            current_match = parsed_matches[match_number]
            quote_groups = sub_page.css(Const.css_sub_market_group)
            for quote_group in quote_groups:
                quote_type = quote_group.css(Const.css_sub_market_group_header + Const.css_get_all_text).get(
                    default=None) or quote_group.css(Const.css_sub_market_group_header2 + Const.css_get_all_text).get(
                    default=None)
                if quote_type.lower() in Const.css_sub_double_chance.lower():
                    # Double chance
                    quotes = quote_group.css(Const.css_sub_quote + Const.css_get_all_text).getall()
                    if len(quotes) == 6:
                        current_match.Quote1X = quotes[1]
                        current_match.Quote2X = quotes[3]
                        current_match.Quote12 = quotes[5]
                elif quote_type.lower() in Const.css_sub_under_over.lower():
                    # Under Over
                    under_over_types = quote_group.css(Const.css_sub_under_over_type + Const.css_get_all_text).getall()
                    under_over_quotes_cols = quote_group.css(Const.css_sub_under_over_quote_cols)
                    Bet365Spider.fill_under_over(current_match, under_over_types, under_over_quotes_cols)
                elif quote_type.lower() in Const.css_sub_goal_nogoal.lower():
                    # Goal No Goal
                    quotes = quote_group.css(Const.css_sub_quote + Const.css_get_all_text).getall()
                    if len(quotes) == 4:
                        current_match.QuoteGoal = quotes[1]
                        current_match.QuoteNoGoal = quotes[3]
            match_number += 1

    @staticmethod
    def fill_under_over(current_match: Match, under_over_types, under_over_quotes_cols):
        if len(under_over_types) > 0 and len(under_over_quotes_cols) == 2:
            over_quotes = under_over_quotes_cols[0].css(
                Const.css_sub_under_over_quote_row + Const.css_get_all_text).getall()
            under_quotes = under_over_quotes_cols[1].css(
                Const.css_sub_under_over_quote_row + Const.css_get_all_text).getall()
            for idx, val in enumerate(under_over_types):
                if '0.5' in val:
                    current_match.QuoteU05 = under_quotes[idx]
                    current_match.QuoteO05 = over_quotes[idx]
                elif '1.5' in val:
                    current_match.QuoteU15 = under_quotes[idx]
                    current_match.QuoteO15 = over_quotes[idx]
                elif '2.5' in val:
                    current_match.QuoteU25 = under_quotes[idx]
                    current_match.QuoteO25 = over_quotes[idx]
                elif '3.5' in val:
                    current_match.QuoteU35 = under_quotes[idx]
                    current_match.QuoteO35 = over_quotes[idx]
                elif '4.5' in val:
                    current_match.QuoteU45 = under_quotes[idx]
                    current_match.QuoteO45 = over_quotes[idx]

    def spider_idle(self):
        # End of all the requests

        # # Apply Google Translate to each Match team names to global EN ones
        # match_translator = MatchTranslator(from_lang='it', to_lang='en', word_by_word=True)
        # parsed_matches = match_translator.translate_all(all_parsed_matches)

        match_mapper = MatchMapper()
        # Try to remap each match team name to the global en-EN one (if found by the ML system)
        self.parsed_matches = match_mapper.map_all(self.parsed_matches)
        # Write down validation output of ML to file (unique array through all the parsed teams)
        match_mapper.write_validation_dataset()

        # Write quotes to Firebase
        FirebaseWriter().write(self.parsed_matches)
        self.log('Saved parsed quotes on Firebase: %s' % self.name)
