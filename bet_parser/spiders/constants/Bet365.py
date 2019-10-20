from datetime import datetime


class Const:
    """
    Bet365 Spider Constants file
    """
    # Cookies Config
    access_cookie_key: str = 'aps03'
    access_cookie_value: str = 'cf=N&cg=1&cst=0&ct=97&hd=N&lng=6&oty=2&tzi=4'

    # B365 CSS Selectors
    css_matches_groups: str = '.gll-MarketGroupContainer'
    css_description_column: str = '.sl-MarketCouponFixtureLabelBase'
    css_date_row: str = '.sl-MarketHeaderLabel_Date'
    css_name_result_time_row: str = '.sl-CouponParticipantWithBookCloses'
    css_name_result_cell: str = '.sl-CouponParticipantWithBookCloses_NameContainer'
    css_time_cell: str = '.sl-CouponParticipantWithBookCloses_LeftSideContainer'
    css_quote_columns: str = '.sl-MarketCouponValuesExplicit33'
    css_quote_header: str = '.gll-MarketColumnHeader'

    # Sub pages Selectors
    css_sub_team_names: str = '.cl-EnhancedDropDown'
    css_sub_market_group: str = '.gll-MarketGroup'
    css_sub_market_group_header: str = '.gll-MarketGroupButton_Text'
    css_sub_market_group_header2: str = '.cm-CouponMarketGroupButton_Text' # for Under/Over section
    css_sub_double_chance: str = 'Doppia chance'
    css_sub_goal_nogoal: str = 'Entrambe le squadre segnano'
    css_sub_quote: str = '.gll-Participant_General'
    css_sub_under_over: str = 'Goal: under/over'
    css_sub_under_over_type: str = '.gll-ParticipantRowValue'
    css_sub_under_over_quote_cols: str = '.gll-MarketValuesExplicit2'
    css_sub_under_over_quote_row: str = '.gll-ParticipantOddsOnly_Odds'


    # Global CSS/XPath Selectors
    css_child_divs: str = ' > div'
    css_get_all_text: str = ' *::text'
    xpath_get_class: str = '@class'
    xpath_get_text: str = './/text()'
    xpath_child_divs: str = './div'

    # Other Constants
    match_date_divider: str = ' '
    match_name_divider: str = ' v '
    current_year: int = datetime.today().year
    datetime_italian_locale: str = 'it_IT'
    b365_date_format: str = '%d %b %Y'
    output_date_format: str = '%Y_%m_%d'
