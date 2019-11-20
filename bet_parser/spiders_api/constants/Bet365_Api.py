import pytz


class Const:
    """
    Bet365 Api Spider Constants file
    """

    # APIs
    b365_api_template = 'https://www.bet365.it/SportsBook.API/web?lid=6&zid=0&pd=%s&cid=97&ctid=97'

    # Global Response Dividers
    lines_separator = '|'
    fields_separator = ';'
    keyvalue_separator = '='

    # Global Response Keys
    type = 'Type'
    header_type = 'CL'
    group_type = 'MG'
    section_type = 'MA'
    event_type = 'PA'
    enc_seed = 'TK'
    section_id = 'ID'
    section_sy = 'SY'
    section_name = 'NA'
    event_id = 'FI'
    event_name = 'NA'
    event_date = 'BC'
    event_odd = 'OD'
    event_link = 'PD'

    # Bookmaker Name
    b365_name = 'b365'

    # DateTime Formats
    b365_timezone: pytz.UTC = pytz.timezone('Europe/London')
    b365_date_format: str = '%Y%m%d%H%M%S'
    output_timezone: pytz.UTC = pytz.timezone('Europe/Rome')
    output_date_format: str = '%Y_%m_%d'
    output_time_format: str = '%H:%M'


class MainAPI:
    # Main API Response Keys
    sect_events_desc = 'CG'
    sect_events_odds = 'CBJ'
    sect_odds_1_name = '1'
    sect_odds_X_name = 'X'
    sect_odds_2_name = '2'
    sect_events_link = 'CD'


class InnerAPI:
    # Inner API Response Keys
    sect_double_chance = '50401'
    sect_goal_no_goal = '10150'
    group_under_over = '981'
    sect_under_over_05 = '0.5'
    sect_under_over_15 = '1.5'
    sect_under_over_25 = '2.5'
    sect_under_over_35 = '3.5'
    sect_under_over_45 = '4.5'
