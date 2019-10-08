import scrapy
from scrapy_splash.utils import to_native_str


class SeleniumRequest(scrapy.Request):
    """
    scrapy.Request subclass which instructs Scrapy to render
    the page using Selenium.

    It requires SeleniumMiddleware to work.
    """

    def __init__(self,
                 url=None,
                 method='GET',
                 callback=None,
                 driver_type='chrome',
                 cookies=None,
                 wait_time=None,
                 wait_until=None,
                 script=None,
                 render_js=False,
                 rebuild=False,
                 window_size=None,
                 headless=None,
                 user_data_dir=None,
                 meta=None,
                 **kwargs):
        if url is None:
            url = 'about:blank'
        url = to_native_str(url)

        meta = meta or {}
        selenium_meta = meta.setdefault('selenium', {})
        selenium_meta.setdefault('driver_type', driver_type)
        selenium_meta.setdefault('cookies', cookies)
        selenium_meta.setdefault('wait_time', wait_time)
        selenium_meta.setdefault('wait_until', wait_until)
        selenium_meta.setdefault('script', script)
        selenium_meta.setdefault('render_js', render_js)
        selenium_meta.setdefault('rebuild', rebuild)
        selenium_meta.setdefault('window_size', window_size)
        selenium_meta.setdefault('headless', headless)
        selenium_meta.setdefault('user_data_dir', user_data_dir)

        super(SeleniumRequest, self).__init__(url, callback, method, dont_filter=True, meta=meta,
                                              **kwargs)
