from datetime import datetime


class Const:
    """
    Sisal Spider Constants file
    """
    # Sisal CSS Selectors
    css_matches_groups: str = '.multiscommessa__row'
    css_matches_groups_dynamic: str = 'div[class^="TabellaEsitiRow"]'
    css_name_event: str = '.multiscommessa__dettagli__nome'
    css_name_event_dynamic: str = 'span[class^="AvvenimentoDescription"]'
    css_name_type: str = '.multiscommessa__dettagli__manifestazione'
    css_name_type_dynamic: str = 'span[class^="ManifestazioneDetailDescription"]'
    css_date_event: str = '.multiscommessa__dettagli__data'
    css_date_event_dynamic: str = 'span[class^="AvvenimentoDate"]'
    css_event_type: str = '.multiscommessa__box__esito__singolo'
    css_event_type_dynamic: str = 'div[class^="EsitoButton"]'
    css_sub_link: str = '.multiscommessa:not([style="display: none;"]) .multiscommessa__accordion'
    css_sub_link_dynamic: str = 'div[class^="TabellaEsitiRow"] a[class^="RelatedBetsButton"]'

    # Sisal sub events CSS Selectors
    css_sub_team_names: str = '#dettaglioAvvenimento .sottotitolo'
    css_sub_team_names_dynamic: str = 'span[class^="SchedaAvvenimentoSubHeaderName"]'
    css_sub_team_names_dynamic_live: str = 'div[class^="EventDetailLive__StyledAvvenimentoDescription"]'
    css_sub_events: str = '#dettaglioAvvenimento .event[id]'
    css_sub_events_dynamic: str = 'div[class^="TabellaDettagliRow"]'
    css_sub_event_name: str = '.name'
    css_sub_event_name_dynamic: str = 'span[class^="InfoAggiuntivaDetailDescription"]'
    css_sub_event_double_chance: str = 'doppia chance'
    css_sub_event_goal_no_goal: str = 'goal/nogoal'
    css_sub_event_uo_05: str = 'u/o 0.5'
    css_sub_event_uo_15: str = 'u/o 1.5'
    css_sub_event_uo_25: str = 'u/o 2.5'
    css_sub_event_uo_35: str = 'u/o 3.5'
    css_sub_event_uo_45: str = 'u/o 4.5'
    css_sub_event_values: str = '.quota-label'
    css_sub_event_values_dynamic: str = 'div[class^="EsitoButton-"]'

    # Other Constants
    datetime_italian_locale: str = 'ita_ITA'
    sisal_date_format: str = '%d/%m/%Y'
    sisal_date_format2: str = '%d-%m-%Y'
    output_date_format: str = '%Y_%m_%d'
    sisal_time_format: str = '%H.%M'
    sisal_time_format2: str = '%H:%M'
    output_time_format: str = '%H:%M'
    txt_not_available: str = 'N/A'
