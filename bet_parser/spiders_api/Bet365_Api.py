# -*- coding: utf-8 -*-
from math import floor
import urllib.parse
import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse
from datetime import datetime
from typing import Dict
from bet_parser.spiders_api.constants.Bet365_Api import Const, MainAPI, InnerAPI
from bet_parser.utils.Mappers import MatchMapper
from bet_parser.utils.Writers import *


class Bet365Decoder:
    seed: int = None
    decoded_cache: dict = {}

    def __init__(self, encrypted_seed: str):
        self.seed = Bet365Decoder.get_decoded_seed(encrypted_seed)

    @staticmethod
    def get_decoded_seed(tk: str):
        seed = None
        if tk and len(tk) >= 2:
            seed = ord(tk[0]) ^ ord(tk[1])
        return seed

    def get_decoded_odd(self, encoded_odd: str):
        decoded_odd: str = ''

        if not encoded_odd or not self.seed:
            return encoded_odd

        cache_key = encoded_odd + "%" + str(self.seed)
        if cache_key in self.decoded_cache.keys():
            return self.decoded_cache[cache_key]

        for i in range(len(encoded_odd)):
            decoded_odd += chr(ord(encoded_odd[i]) ^ self.seed)
        self.decoded_cache[cache_key] = decoded_odd

        return decoded_odd

    def get_decoded_decimal_odd(self, encoded_odd: str):
        decoded_fractional_odd = self.get_decoded_odd(encoded_odd)
        fraction_parts = decoded_fractional_odd.split('/')

        try:
            decimal_odd = floor(((int(fraction_parts[0]) / int(fraction_parts[1])) + 1) * 100) / 100
        except Exception as e:
            decimal_odd = decoded_fractional_odd

        return decimal_odd


class Bet365ApiSpider(scrapy.Spider):
    name: str = 'b365_api'
    allowed_domains: list = ['bet365.it']
    start_urls: Dict[str, str] = {
        Const.b365_api_template % '%23AP%23B1%23A%5E4%23C%5E1%23D%5E11%23E%5E21%23H%5E4750': 'b365_main_page',
        Const.b365_api_template % '%23AC%23B1%23C1%23D13%23E108%23F16%23': 'b365_europe_elite',
        Const.b365_api_template % '%23AC%23B1%23C1%23D13%23E112%23F16%23': 'b365_international_list',
    }
    custom_settings = {
        'DOWNLOAD_DELAY': 1.8,
        # The download delay setting will honor only one of:
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        # Enable and configure the AutoThrottle extension (disabled by default)
        # See https://docs.scrapy.org/en/latest/topics/autothrottle.html
        'AUTOTHROTTLE_ENABLED': True,
        # The initial download delay
        'AUTOTHROTTLE_START_DELAY': 1.5,
        # The maximum download delay to be set in case of high latencies
        'AUTOTHROTTLE_MAX_DELAY': 5,
        # The average number of requests Scrapy should be sending in parallel to
        # each remote server
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0
    }
    extracted_matches: Dict[str, Match] = {}

    def start_requests(self):
        # Connect the idle status (end of all requests) to self.spider_idle method
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)

        # Start requests
        for url, name in self.start_urls.items():
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 dont_filter=True)

    def parse(self, response: HtmlResponse):
        api_response = response.body_as_unicode()

        # Step 1 - Main API response parsing
        # normally a Main API contains many matches with basic info, so here we transform this response in readable
        # Matches objects
        self.process_api_response(api_response)

        # Step 2 - Single Matches API response parsing (enhancing Matches with extra Odds info)
        match_refs = list(map(lambda key: [key, self.extracted_matches[key].InnerLink], self.extracted_matches.keys()))

        for match_ref in match_refs:
            inner_link = Const.b365_api_template % match_ref[1]
            yield scrapy.Request(url=inner_link,
                                 callback=self.parse_inner,
                                 meta={'event_id': match_ref[0]},
                                 dont_filter=True)

    def parse_inner(self, response: HtmlResponse):
        api_response = response.body_as_unicode()

        # Step 2 - Single Matches API response parsing (enhancing Matches with extra Odds info)
        self.process_api_response(api_response, response.request.meta['event_id'])

    def process_api_response(self, api_response: str, event_id: str = None):
        decoder: any = None
        current_group = {'id': '', 'index': 0, 'mappings': []}
        current_section = {'id': '', 'sy': '', 'name': '', 'index': 0}

        lines = api_response.split(Const.lines_separator)
        for line in lines:
            line_struct = {Const.type: None}

            fields = line.split(Const.fields_separator)
            for field in fields:
                separator_idx = field.find(Const.keyvalue_separator)
                if separator_idx != -1:
                    key = field[0:separator_idx]
                    value = field[separator_idx + 1:len(field)]
                    line_struct[key] = value
                else:
                    if field == '':
                        continue
                    line_struct[Const.type] = field

            # Intercept Response Header, to extract and decode encryption seed
            if line_struct[Const.type] == Const.header_type:
                enc_seed = line_struct[Const.enc_seed] if Const.enc_seed in line_struct.keys() else None
                decoder = Bet365Decoder(enc_seed)

            # (only Inner API) Intercept Response Groups, to correctly parse the Response Events rows
            elif event_id and \
                    line_struct[Const.type] == Const.group_type and \
                    Const.section_id in line_struct.keys():
                current_group = {'id': line_struct[Const.section_id], 'index': 0, 'mappings': []}

            # Intercept Response Sections, to correctly parse the Response Events rows
            elif line_struct[Const.type] == Const.section_type and \
                    Const.section_id in line_struct.keys() and \
                    Const.section_sy in line_struct.keys():
                current_section = {'id': line_struct[Const.section_id],
                                   'sy': line_struct[Const.section_sy],
                                   'name': line_struct[
                                       Const.section_name] if Const.section_name in line_struct.keys() else None,
                                   'index': 0}

            # Intercept Response Events rows, to extract and decode needed data
            elif line_struct[Const.type] == Const.event_type and decoder:
                if not event_id:
                    # Main API
                    self.extract_main_api_event_data(section=current_section,
                                                     event_row=line_struct,
                                                     decoder=decoder,
                                                     extracted_matches=self.extracted_matches)
                else:
                    # Inner API
                    if Const.event_odd not in line_struct.keys() \
                            and Const.event_name in line_struct.keys():
                        # If the current Event row has no Odd, we treat it like an Event mapping descriptor
                        current_group['mappings'].append(line_struct[Const.event_name])
                        pass
                    else:
                        self.extract_inner_api_event_data(group=current_group,
                                                          section=current_section,
                                                          event_row=line_struct,
                                                          decoder=decoder,
                                                          event_id=event_id,
                                                          extracted_matches=self.extracted_matches)
                        # we need to increase group and section counter, since we have different events in the same
                        # section
                        current_group['index'] += 1
                        current_section['index'] += 1

    @staticmethod
    def extract_main_api_event_data(section: dict, event_row: dict, decoder: Bet365Decoder, extracted_matches: dict):
        event_id = None
        team_1 = None
        team_2 = None
        start_date = None
        start_time = None
        quote_1 = None
        quote_x = None
        quote_2 = None
        event_inner_link = None

        if section['sy'] == MainAPI.sect_events_desc:
            # Extracts Match Team Names
            event_id = event_row[Const.event_id]
            event_name = event_row[Const.event_name]
            splitted_event_name = event_name.split(' v ')
            if len(splitted_event_name) == 2:
                team_1 = splitted_event_name[0]
                team_2 = splitted_event_name[1]

            event_date_b365 = event_row[Const.event_date]
            event_date_b365 = Const.b365_timezone.localize(datetime.strptime(event_date_b365, Const.b365_date_format))
            event_date: datetime = event_date_b365.astimezone(Const.output_timezone)
            start_date = event_date.strftime(Const.output_date_format)
            start_time = event_date.strftime(Const.output_time_format)
        elif section['sy'] in MainAPI.sect_events_odds:
            # Extracts Match 1X2 Quotes/Odds
            event_id = event_row[Const.event_id]
            event_odd = event_row[Const.event_odd]
            event_odd = decoder.get_decoded_decimal_odd(event_odd)

            if section['name'] == MainAPI.sect_odds_1_name:
                quote_1 = event_odd
            elif section['name'] == MainAPI.sect_odds_X_name:
                quote_x = event_odd
            elif section['name'] == MainAPI.sect_odds_2_name:
                quote_2 = event_odd
        elif section['sy'] == MainAPI.sect_events_link:
            # Extracts Match Inner API Link (to retrieve all the other odds)
            event_id = event_row[Const.event_id]
            event_inner_link = urllib.parse.quote(event_row[Const.event_link])

        if event_id:
            if event_id in extracted_matches.keys():
                match = extracted_matches[event_id]
            else:
                match = extracted_matches[event_id] = Match(Const.b365_name)

            match.Team1 = team_1 if team_1 else match.Team1
            match.Team2 = team_2 if team_2 else match.Team2
            match.StartDate = start_date if start_date else match.StartDate
            match.StartTime = start_time if start_time else match.StartTime
            match.Quote1 = quote_1 if quote_1 else match.Quote1
            match.QuoteX = quote_x if quote_x else match.QuoteX
            match.Quote2 = quote_2 if quote_2 else match.Quote2
            match.InnerLink = event_inner_link if event_inner_link else match.InnerLink

    @staticmethod
    def extract_inner_api_event_data(group: dict, section: dict, event_row: dict, decoder: Bet365Decoder, event_id: str,
                                     extracted_matches: dict):
        quote_1x = None
        quote_2x = None
        quote_12 = None
        quote_goal = None
        quote_no_goal = None
        quote_under_over = {
            'u05': None,
            'o05': None,
            'u15': None,
            'o15': None,
            'u25': None,
            'o25': None,
            'u35': None,
            'o35': None,
            'u45': None,
            'o45': None
        }

        if Const.event_odd in event_row.keys():
            event_odd = event_row[Const.event_odd]
            event_odd = decoder.get_decoded_decimal_odd(event_odd)
        else:
            return

        if section['id'] in InnerAPI.sect_double_chance and section['index'] == 0:
            # Extracts Match 1X Odd
            quote_1x = event_odd
        elif section['id'] in InnerAPI.sect_double_chance and section['index'] == 1:
            # Extracts Match 2X Odd
            quote_2x = event_odd
        elif section['id'] in InnerAPI.sect_double_chance and section['index'] == 2:
            # Extracts Match 12 Odd
            quote_12 = event_odd
        elif section['id'] in InnerAPI.sect_goal_no_goal and section['index'] == 0:
            # Extracts Match Goal Odd
            quote_goal = event_odd
        elif section['id'] in InnerAPI.sect_goal_no_goal and section['index'] == 1:
            # Extracts Match No Goal Odd
            quote_no_goal = event_odd
        elif group['id'] in InnerAPI.group_under_over and group['mappings']:
            # Extracts Match Over/Under Odd
            goals_amount = group['mappings'][section['index']].replace('.', '')
            try:
                if group['index'] < len(group['mappings']):
                    # Over
                    quote_under_over['o' + goals_amount] = event_odd
                else:
                    # Under
                    quote_under_over['u' + goals_amount] = event_odd
            except Exception as e:
                pass

        if event_id:
            if event_id in extracted_matches.keys():
                match = extracted_matches[event_id]
            else:
                match = extracted_matches[event_id] = Match(Const.b365_name)

            match.Quote1X = quote_1x if quote_1x else match.Quote1X
            match.Quote2X = quote_2x if quote_2x else match.Quote2X
            match.Quote12 = quote_12 if quote_12 else match.Quote12
            match.QuoteGoal = quote_goal if quote_goal else match.QuoteGoal
            match.QuoteNoGoal = quote_no_goal if quote_no_goal else match.QuoteNoGoal
            match.QuoteU05 = quote_under_over['u05'] if quote_under_over['u05'] else match.QuoteU05
            match.QuoteO05 = quote_under_over['o05'] if quote_under_over['o05'] else match.QuoteO05
            match.QuoteU15 = quote_under_over['u15'] if quote_under_over['u15'] else match.QuoteU15
            match.QuoteO15 = quote_under_over['o15'] if quote_under_over['o15'] else match.QuoteO15
            match.QuoteU25 = quote_under_over['u25'] if quote_under_over['u25'] else match.QuoteU25
            match.QuoteO25 = quote_under_over['o25'] if quote_under_over['o25'] else match.QuoteO25
            match.QuoteU35 = quote_under_over['u35'] if quote_under_over['u35'] else match.QuoteU35
            match.QuoteO35 = quote_under_over['o35'] if quote_under_over['o35'] else match.QuoteO35
            match.QuoteU45 = quote_under_over['u45'] if quote_under_over['u45'] else match.QuoteU45
            match.QuoteO45 = quote_under_over['o45'] if quote_under_over['o45'] else match.QuoteO45

    def spider_idle(self):
        # End of all the requests

        # # Apply Google Translate to each Match team names to global EN ones
        # match_translator = MatchTranslator(from_lang='it', to_lang='en', word_by_word=True)
        # parsed_matches = match_translator.translate_all(all_parsed_matches)

        match_mapper = MatchMapper()
        # Try to remap each match team name to the global en-EN one (if found by the ML system)
        match_to_write = match_mapper.map_all(list(self.extracted_matches.values()))
        # Write down validation output of ML to file (unique array through all the parsed teams)
        match_mapper.write_validation_dataset()

        # Write quotes to Firebase
        FirebaseWriter().write(match_to_write)
        self.log('Saved extracted quotes on Firebase: %s' % self.name)

    # # Dynamic Custom Proxies extraction
    # def start_proxies(self):
    #     yield SeleniumRequest(url='https://free-proxy-list.net',
    #                           callback=self.parse_proxies,
    #                           extract_proxies=True)
    #
    # def parse_proxies(self, response):
    #     proxies: list = []
    #     for i in response.xpath('//tbody/tr'):
    #         if i.xpath('.//td[7][contains(text(),"yes")]'):
    #             # Grabbing IP and corresponding PORT
    #             proxy = ":".join([i.xpath('.//td[1]/text()')[0].get(), i.xpath('.//td[2]/text()')[0].get()])
    #             proxies.append(proxy)
    #     # url = 'https://httpbin.org/ip'
