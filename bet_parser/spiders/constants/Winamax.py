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

    # William sub event CSS Selectors
    css_sub_team_names: str = '#contentHead h2'
    css_sub_events: str = '.marketHolderExpanded'
    css_sub_event_name: str = '.title > span'
    css_sub_event_double_chance: str = 'doppia chance'
    css_sub_event_goal_no_goal: str = 'segneranno entrambe le squadre?'
    css_sub_event_uo_05: str = 'over/under 0.5 goal'
    css_sub_event_uo_15: str = 'over/under 1.5 goal'
    css_sub_event_uo_25: str = 'over/under 2.5 goal'
    css_sub_event_uo_35: str = 'over/under 3.5 goal'
    css_sub_event_uo_45: str = 'over/under 4.5 goal'
    css_sub_event_values: str = '.eventprice'

    # Other Constants
    william_date_format: str = '%d %b %Y'
    output_date_format: str = '%Y_%m_%d'
    txt_not_available: str = 'N/A'
