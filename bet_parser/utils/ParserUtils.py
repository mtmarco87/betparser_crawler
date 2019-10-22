from datetime import datetime

xpath_get_text: str = './/text()'


def get_elements(html_element, css_selector):
    if html_element:
        return html_element.css(css_selector)


def get_element_at_position(html_element, css_selector, position):
    if html_element:
        elements = html_element.css(css_selector)
        if elements and elements[position]:
            return elements[position]


def get_first_element(html_element, css_selector):
    return get_element_at_position(html_element, css_selector, 0)


def get_text_from_html_element(html_element):
    return html_element.xpath(xpath_get_text).get()


def get_text_from_html_element_at_position(html_element, css_selector, position):
    element = get_element_at_position(html_element, css_selector, position)
    if element:
        return get_text_from_html_element(element)


def get_text_from_first_html_element(html_element, css_selector):
    return get_text_from_html_element_at_position(html_element, css_selector, 0)


def format_date(data, input_date_format, output_date_format):
    return datetime.strptime(data, input_date_format).strftime(output_date_format)


def convert_date_ita_to_eng(extr_date):
    converted_date = extr_date
    splitted = converted_date.split(' ')
    if len(splitted) == 3:
        day_number = splitted[0].strip()
        month_name = splitted[1].strip().lower()
        if month_name in 'gen':
            month_name = 'Jan'
        elif month_name in 'feb':
            month_name = 'Feb'
        elif month_name in 'mar':
            month_name = 'Mar'
        elif month_name in 'apr':
            month_name = 'Apr'
        elif month_name in 'mag':
            month_name = 'May'
        elif month_name in 'giu':
            month_name = 'Jun'
        elif month_name in 'lug':
            month_name = 'Jul'
        elif month_name in 'ago':
            month_name = 'Aug'
        elif month_name in 'set':
            month_name = 'Sep'
        elif month_name in 'ott':
            month_name = 'Oct'
        elif month_name in 'nov':
            month_name = 'Nov'
        elif month_name in 'dic':
            month_name = 'Dec'
        year = splitted[2].strip()

        converted_date = day_number + ' ' + month_name + ' ' + year

    return converted_date
