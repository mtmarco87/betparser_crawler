from datetime import datetime


class Const:
    """
    Sisal Spider Constants file
    """
    # B365 CSS Selectors
    css_matches_groups: str = '.gll-MarketGroupContainer'
    css_description_column: str = '.sl-MarketCouponFixtureLabelBase'
    css_date_row: str = '.sl-MarketHeaderLabel_Date'
    css_name_result_time_row: str = '.sl-CouponParticipantWithBookCloses'
    css_name_result_cell: str = '.sl-CouponParticipantWithBookCloses_NameContainer'
    css_time_cell: str = '.sl-CouponParticipantWithBookCloses_LeftSideContainer'
    css_quote_columns: str = '.sl-MarketCouponValuesExplicit33'
    css_quote_header: str = '.gll-MarketColumnHeader'

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
    txt_not_available: str = 'N/A'