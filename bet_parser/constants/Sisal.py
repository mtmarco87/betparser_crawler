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

    # Other Constants
    datetime_italian_locale: str = 'ita_ITA'
    sisal_date_format: str = '%d/%m/%Y'
    sisal_date_format2: str = '%d-%m-%Y'
    output_date_format: str = '%Y_%m_%d'
    sisal_time_format: str = '%H.%M'
    output_time_format: str = '%H:%M'
    txt_not_available: str = 'N/A'
