from datetime import datetime


class Const:
    """
    Bwin Spider Constants file
    """
    # Bwin CSS Selectors
    css_matches_groups: str = '.event-group'
    css_match_rows: str = '.grid-event-wrapper'
    css_match_teams: str = '.grid-event-name .participant'
    css_match_team_type: str = '.participant-country::text'
    css_match_start_date_time: str = '.grid-event-timer'
    css_match_score_values: str = '.grid-scoreboard .cell'
    css_match_score_values_inner_vals: str = ' * > div > div *::text'
    css_match_quotes_groups: str = '.grid-option-group'
    css_match_quotes_values: str = '.grid-option'

    # Global CSS/XPath Selectors
    css_get_all_text: str = ' *::text'

    # DateTime Constants
    bwin_real_time_1: str = 'mt1'
    bwin_real_time_2: str = 'mt2'
    bwin_today_date: str = 'aujourd\'hui /'
    bwin_tomorrow_date: str = 'demain /'
    bwin_date_format: str = '%d/%m/%Y %H:%M'
    output_date_format: str = '%Y_%m_%d'
    output_time_format: str = '%H:%M'
