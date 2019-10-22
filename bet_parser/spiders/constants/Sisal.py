from datetime import datetime


class Const:
    """
    Sisal Spider Constants file
    """
    # Sisal CSS Selectors
    css_matches_groups: str = '.multiscommessa__row'
    css_name_event: str = '.multiscommessa__dettagli__nome'
    css_name_type: str = '.multiscommessa__dettagli__manifestazione'
    css_date_event: str = '.multiscommessa__dettagli__data'
    css_event_type: str = '.multiscommessa__box__esito__singolo'

    # Sisal sub events CSS Selectors
    css_sub_team_names: str = '#dettaglioAvvenimento .sottotitolo'
    css_sub_events: str = '#dettaglioAvvenimento .event[id]'
    css_sub_event_name: str = '.name'
    css_sub_event_double_chance: str = 'doppia chance'
    css_sub_event_goal_no_goal: str = 'goal/nogoal'
    css_sub_event_uo_05: str = 'u/o 0.5'
    css_sub_event_uo_15: str = 'u/o 1.5'
    css_sub_event_uo_25: str = 'u/o 2.5'
    css_sub_event_uo_35: str = 'u/o 3.5'
    css_sub_event_uo_45: str = 'u/o 4.5'
    css_sub_event_values: str = '.quota-label'

    # Other Constants
    datetime_italian_locale: str = 'ita_ITA'
    sisal_date_format: str = '%d/%m/%Y'
    sisal_date_format2: str = '%d-%m-%Y'
    output_date_format: str = '%Y_%m_%d'
    sisal_time_format: str = '%H.%M'
    output_time_format: str = '%H:%M'
    txt_not_available: str = 'N/A'
