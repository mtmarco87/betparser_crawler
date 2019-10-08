from datetime import datetime

xpath_get_text: str = './/text()'


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


def format_date(data, inputDateFormat, outputDateFormat):
    return datetime.strptime(data, inputDateFormat).strftime(outputDateFormat)
