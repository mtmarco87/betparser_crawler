from datetime import datetime


class Const:
    """
    Sisal Spider Constants file
    """
    # Sisal CSS Selectors
    css_matches_groups: str = '.multiscommessa__row'
    css_name_event: str = '.multiscommessa__dettagli__nome'
    css_date_event: str = '.multiscommessa__dettagli__data'
    css_event_type: str = '.multiscommessa__box__esito__singolo'
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
    sisal_date_format: str = '%d/%m/%Y'
    sisal_date_format2: str = '%d-%m-%Y'
    output_date_format: str = '%Y_%m_%d'
    txt_not_available: str = 'N/A'
