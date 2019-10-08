from datetime import datetime


class Const:
    """
    William Spider Constants file
    """
    # Cookies Config TODO to be updated
    access_cookie_key: str = 'aps03'
    access_cookie_value: str = 'lng=6&ct=97&cg=1&cst=0&hd=N&cf=N&tzi=19&oty=2'

    # William CSS Selectors
    css_matches_rows: str = '.rowOdd'
    css_descr_col: str = '.leftPad'
    css_name_event: str = '.multiscommessa__dettagli__nome'
    css_date_event: str = '.multiscommessa__dettagli__data'
    css_event_type: str = '.eventprice'
    css_description_column: str = '.AvvenimentoDetailWrapper-w9f4wf-0'
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
    datetime_italian_locale: str = 'ita_ITA'
    william_date_format: str = '%d %b %Y'
    output_date_format: str = '%Y_%m_%d'
    txt_not_available: str = 'N/A'
