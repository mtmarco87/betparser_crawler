from datetime import datetime


class Const:
    """
    William Spider Constants file
    """
    # Cookies Config TODO to be updated

    # William CSS Selectors
    css_matches_rows: str = '.rowOdd'
    css_descr_col: str = '.leftPad'
    css_event_type: str = '.eventprice'

    # Other Constants
    william_date_format: str = '%d %b %Y'
    output_date_format: str = '%Y_%m_%d'
    txt_not_available: str = 'N/A'
