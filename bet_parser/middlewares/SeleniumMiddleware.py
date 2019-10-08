from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


class SeleniumDownloaderMiddleware(object):
    chrome_driver = None
    chrome_driver_path = ''
    firefox_driver = None
    firefox_driver_path = ''
    headless = None
    window_size = None
    chrome_user_data_dir = None
    download_delay = 0

    def __init__(self, crawler, chrome_driver_path, firefox_driver_path, headless, window_size,
                 chrome_user_data_dir, download_delay):
        self.crawler = crawler
        self.chrome_driver_path = chrome_driver_path
        self.firefox_driver_path = firefox_driver_path
        self.headless = headless
        self.window_size = window_size
        self.chrome_user_data_dir = chrome_user_data_dir
        self.download_delay = download_delay

        self.crawler.signals.connect(self.spider_opened, signals.spider_opened)
        self.crawler.signals.connect(self.spider_idle, signals.spider_idle)

    @classmethod
    def from_crawler(cls, crawler):
        chrome_driver_path = crawler.settings.get('SELENIUM_CHROME_DRIVER')
        firefox_driver_path = crawler.settings.get('SELENIUM_FIREFOX_DRIVER')
        headless = crawler.settings.get('SELENIUM_HEADLESS')
        window_size = crawler.settings.get('SELENIUM_WINDOW_SIZE')
        chrome_user_data_dir = crawler.settings.get('SELENIUM_CHROME_USER_DATA_DIR')
        download_delay = crawler.settings.get('DOWNLOAD_DELAY',
                                              cls.download_delay)

        return cls(crawler, chrome_driver_path, firefox_driver_path, headless, window_size,
                   chrome_user_data_dir, download_delay)

    def get_chrome_driver(self, rebuild: bool = False, window_size=None, headless=None, user_data_dir=None):
        if not self.chrome_driver or rebuild:
            options = webdriver.ChromeOptions()

            window_size = window_size if window_size is not None else self.window_size
            headless = headless if headless is not None else self.headless
            user_data_dir = user_data_dir if user_data_dir is not None else self.chrome_user_data_dir

            if window_size:
                options.add_argument('window-size=' + window_size)
            if headless:
                options.add_argument('headless')
            if user_data_dir:
                options.add_argument("user-data-dir=" + user_data_dir)
                options.add_argument("--disable-plugins-discovery")

            self.chrome_driver = webdriver.Chrome(chrome_options=options,
                                                  executable_path=self.chrome_driver_path)
        return self.chrome_driver

    def get_firefox_driver(self, rebuild: bool = False, window_size=None, headless=None):
        if not self.firefox_driver or rebuild:
            options = webdriver.FirefoxOptions()

            window_size = window_size if window_size is not None else self.window_size
            headless = headless if headless is not None else self.headless

            if window_size:
                options.add_argument('window-size=' + window_size)
            if headless:
                options.add_argument('headless')

            self.firefox_driver = webdriver.Firefox(firefox_options=options,
                                                    executable_path=self.firefox_driver_path)
        return self.firefox_driver

    def process_request(self, request, spider):
        if 'selenium' not in request.meta:
            return

        # Driver Execution params
        driver_type = request.meta['selenium']['driver_type'] if 'driver_type' in request.meta['selenium'] else None
        cookies = request.meta['selenium']['cookies'] if 'cookies' in request.meta['selenium'] else None
        wait_time = request.meta['selenium']['wait_time'] if 'wait_time' in request.meta['selenium'] else None
        wait_until = request.meta['selenium']['wait_until'] if 'wait_until' in request.meta['selenium'] else None
        script = request.meta['selenium']['script'] if 'script' in request.meta['selenium'] else None
        render_js = request.meta['selenium']['render_js'] if 'render_js' in request.meta['selenium'] else False

        # Driver Build/Rebuild params
        rebuild = request.meta['selenium']['rebuild'] if 'rebuild' in request.meta['selenium'] else False
        window_size = request.meta['selenium']['window_size'] if 'window_size' in request.meta['selenium'] else None
        headless = request.meta['selenium']['headless'] if 'headless' in request.meta['selenium'] else None
        user_data_dir = request.meta['selenium']['user_data_dir'] if 'user_data_dir' in request.meta[
            'selenium'] else None

        driver = None
        try:
            if driver_type == 'chrome':
                driver = self.get_chrome_driver(rebuild, window_size, headless, user_data_dir)
            elif driver_type == 'firefox':
                driver = self.get_firefox_driver(rebuild, window_size, headless)
            else:
                return
        except Exception as e:
            spider.log('Error opening Selenium Driver: ' + str(e))
        pass

        if cookies:
            driver.get(request.url)
            driver.add_cookie(cookies)
            time.sleep(self.download_delay)
            driver.get(request.url)
        else:
            driver.get(request.url)

        if wait_time and wait_until:
            WebDriverWait(driver, wait_time).until(wait_until)
        elif wait_time:
            time.sleep(wait_time)

        if script:
            driver.execute_script(script)

        if render_js:
            body = driver.execute_script("return document.body.innerHTML;")
        else:
            body = driver.page_source

        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        if 'selenium' in request.meta:
            rebuild = request.meta['selenium']['rebuild'] if 'rebuild' in request.meta['selenium'] else False
            if rebuild and self.chrome_driver:
                self.chrome_driver.close()
            elif rebuild and self.firefox_driver:
                self.firefox_driver.close()
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        pass

    def spider_idle(self, spider):
        if self.chrome_driver:
            self.chrome_driver.close()
        if self.firefox_driver:
            self.firefox_driver.close()
        pass
