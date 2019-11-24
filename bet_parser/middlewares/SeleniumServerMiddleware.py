import os
from distutils.dir_util import copy_tree
import shutil
import scrapy
from scrapy import signals, Selector
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from typing import List
from .SeleniumExecParams import SeleniumExecParams
import time
from pyvirtualdisplay import Display


class SeleniumServerDownloaderMiddleware(object):
    display = None
    chrome_driver = None
    chrome_driver_path = ''
    firefox_driver = None
    firefox_driver_path = ''
    headless = None
    window_size = None
    chrome_user_data_dir = None
    profiles_tmp_dir = None
    current_profile_dir = None
    download_delay = 0

    def __init__(self, crawler, chrome_driver_path, firefox_driver_path, headless, window_size,
                 chrome_user_data_dir, profiles_tmp_dir, download_delay):
        self.display = Display(visible=0, size=(1920, 1080))
        self.display.start()
        self.crawler = crawler
        self.chrome_driver_path = chrome_driver_path
        self.firefox_driver_path = firefox_driver_path
        self.headless = headless
        self.window_size = window_size
        self.chrome_user_data_dir = chrome_user_data_dir
        self.profiles_tmp_dir = profiles_tmp_dir
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
        profiles_tmp_dir = crawler.settings.get('SELENIUM_PROFILES_TMP_DIR')
        download_delay = crawler.settings.get('DOWNLOAD_DELAY',
                                              cls.download_delay)

        return cls(crawler, chrome_driver_path, firefox_driver_path, headless, window_size,
                   chrome_user_data_dir, profiles_tmp_dir, download_delay)

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
                self.generate_cloned_user_profile(user_data_dir)
                options.add_argument("user-data-dir=" + self.current_profile_dir)
                options.add_argument("--disable-plugins-discovery")

            self.chrome_driver = webdriver.Chrome(chrome_options=options,
                                                  executable_path=self.chrome_driver_path)
        return self.chrome_driver

    def generate_cloned_user_profile(self, user_data_dir):
        index = 0
        temp_profile = 'TempProfile' + str(index)
        while os.path.isdir(self.profiles_tmp_dir + temp_profile):
            index += 1
            temp_profile = 'TempProfile' + str(index)

        self.current_profile_dir = self.profiles_tmp_dir + temp_profile
        copy_tree(user_data_dir, self.current_profile_dir)

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

    @staticmethod
    def get_request_param(request, param, default: bool = None):
        return request.meta['selenium'][param] if param in request.meta['selenium'] else default

    def process_request(self, request, spider):
        if 'selenium' not in request.meta:
            return

        # URL escape/unescape
        original_url = self.get_request_param(request, 'original_url')
        if original_url:
            request._url = original_url

        # Driver Execution params
        driver_type = self.get_request_param(request, 'driver_type')
        cookies = self.get_request_param(request, 'cookies')
        wait_time = self.get_request_param(request, 'wait_time')
        wait_until = self.get_request_param(request, 'wait_until')
        script = self.get_request_param(request, 'script')
        scroll_to_element = self.get_request_param(request, 'scroll_to_element')
        scroll_wait_time = self.get_request_param(request, 'scroll_wait_time')
        render_js = self.get_request_param(request, 'render_js', False)
        kill_timeouts = self.get_request_param(request, 'kill_timeouts', False)
        extract_sub_links_by_class = self.get_request_param(request, 'extract_sub_links_by_class')
        extract_proxies = self.get_request_param(request, 'extract_proxies')

        exec_params = SeleniumExecParams(request.url, cookies, kill_timeouts, wait_time, wait_until, script,
                                         scroll_to_element, scroll_wait_time, render_js, extract_sub_links_by_class,
                                         extract_proxies)

        # Driver Build/Rebuild params
        rebuild = self.get_request_param(request, 'rebuild', False)
        window_size = self.get_request_param(request, 'window_size')
        headless = self.get_request_param(request, 'headless')
        user_data_dir = self.get_request_param(request, 'user_data_dir')

        driver = None
        try:
            if driver_type == 'chrome':
                driver = self.get_chrome_driver(rebuild, window_size, headless, user_data_dir)
            elif driver_type == 'firefox':
                driver = self.get_firefox_driver(rebuild, window_size, headless)
            else:
                return
        except Exception as e:
            spider.log('[ERROR] Selenium Downloader: error opening Selenium Driver: ' + str(e))
        pass

        # Extract the retrieved page (using exec parameters) and eventual sub pages
        page = self.extract_pages(driver, spider, exec_params)

        # Cast subpages if any to selectors and pass them back to the spider
        request.meta['sub_pages'] = list(
            map(lambda sub_page: scrapy.Selector(text=sub_page['body']), page['sub_pages']))

        return HtmlResponse(driver.current_url, body=page['body'], encoding='utf-8', request=request)

    def extract_pages(self, driver, spider, exec_params: SeleniumExecParams):
        if exec_params.url:
            self.navigate(driver, exec_params)

        if exec_params.kill_timeouts:
            driver.execute_script(Scripts.kill_timeouts)

        if exec_params.wait_time and exec_params.wait_until:
            WebDriverWait(driver, exec_params.wait_time).until(exec_params.wait_until)
        elif exec_params.wait_time:
            time.sleep(exec_params.wait_time)

        if exec_params.script:
            driver.execute_script(exec_params.script)

        self.scroll_to_element(driver, spider, exec_params)

        if exec_params.render_js:
            body = driver.execute_script("return document.body.innerHTML;")
        else:
            body = driver.page_source

        sub_pages: List[dict] = self.extract_sub_pages(driver, spider, exec_params)

        body = self.extract_proxies(driver, spider, body, exec_params)

        return {'body': body, 'sub_pages': sub_pages}

    def navigate(self, driver, exec_params: SeleniumExecParams):
        if exec_params.cookies:
            driver.get(exec_params.url)
            driver.add_cookie(exec_params.cookies)
            time.sleep(self.download_delay)
            driver.get(exec_params.url)
        else:
            driver.get(exec_params.url)

    @staticmethod
    def scroll_to_element(driver, spider, exec_params: SeleniumExecParams = None, element: any = None):
        if element or exec_params.scroll_to_element:
            try:
                element = element or driver.find_element_by_css_selector(exec_params.scroll_to_element)
                driver.execute_script(Scripts.scroll_to_element, element)
                time.sleep(exec_params.scroll_wait_time or 0.5)
                while not driver.execute_script(Scripts.is_element_visible, element):
                    driver.execute_script(Scripts.scroll_to_element, element)
                    time.sleep(exec_params.scroll_wait_time or 0.5)
            except Exception as e:
                spider.log('[ERROR] Selenium Downloader: error while trying to scroll to an element: ' + str(e))

    def extract_sub_pages(self, driver, spider, exec_params):
        sub_pages: List[dict] = []
        if exec_params.extract_sub_links_by_class:
            index = 0
            initial_length = 0
            retry_limit = 0
            while True:
                try:
                    elements = None
                    for sub_links_css in exec_params.extract_sub_links_by_class:
                        elements = driver.find_elements_by_css_selector(sub_links_css)
                        if len(elements) > 0:
                            break
                    if initial_length == 0:
                        initial_length = len(elements)
                    if len(elements) == initial_length and initial_length > index:
                        element = elements[index]
                        self.scroll_to_element(driver, spider, exec_params, element)
                        element.click()
                        new_exec_params = exec_params.simplified_clone()
                        sub_page = self.extract_pages(driver, spider, new_exec_params)
                        sub_pages.append(sub_page)
                        if self.current_profile_dir is not None:
                            driver.back()
                        else:
                            self.navigate(driver, exec_params)
                        if exec_params.wait_time:
                            time.sleep(exec_params.wait_time)
                        self.scroll_to_element(driver, spider, exec_params)
                        index += 1
                    elif len(elements) != initial_length and initial_length > index and retry_limit < 20:
                        time.sleep(exec_params.wait_time)
                        retry_limit += 1
                    else:
                        break
                except Exception as e:
                    spider.log(
                        '[ERROR] Selenium Downloader: error while trying to extract sublinks by class: ' + str(e))
                    retry_limit += 1

        return sub_pages

    def extract_proxies(self, driver, spider, body, exec_params):
        body_with_proxies: str = body
        if exec_params.extract_proxies:
            elements = driver.find_elements_by_css_selector('#proxylisttable_next:not(.disabled) > a')
            if len(elements) > 0:
                try:
                    elements[0].click()
                    new_exec_params = exec_params.clone()
                    new_exec_params.url = None
                    next_proxy_pages = self.extract_pages(driver, spider, new_exec_params)
                    if next_proxy_pages:
                        next_proxy_selector = Selector(text=next_proxy_pages['body'])
                        parts = next_proxy_selector.css('body > *').getall()
                        for part in parts:
                            body_with_proxies = body_with_proxies.replace('</body></html>', part + '</body></html>')
                except Exception as e:
                    spider.log('[ERROR] Selenium Downloader: error while trying to extract next proxy page: ' + str(e))

        return body_with_proxies

    def process_response(self, request, response, spider):
        if 'selenium' in request.meta:
            rebuild = self.get_request_param(request, 'rebuild', False)
            if rebuild and self.chrome_driver:
                self.chrome_driver.close()
                if self.current_profile_dir:
                    while os.path.isdir(self.current_profile_dir):
                        try:
                            shutil.rmtree(self.current_profile_dir)
                            break
                        except Exception as e:
                            time.sleep(0.5)
                    self.current_profile_dir = None
            elif rebuild and self.firefox_driver:
                self.firefox_driver.close()
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        pass

    def spider_idle(self, spider):
        self.display.stop()
        self.display = None
        if self.chrome_driver:
            self.chrome_driver.close()
            self.chrome_driver.quit()
            if self.current_profile_dir:
                while os.path.isdir(self.current_profile_dir):
                    try:
                        shutil.rmtree(self.current_profile_dir)
                        break
                    except Exception as e:
                        time.sleep(0.5)
                self.current_profile_dir = None
        if self.firefox_driver:
            self.firefox_driver.close()
            self.firefox_driver.quit()


class Scripts:
    is_element_visible = 'function getElementHeight(elem){ ' + \
                         '  return parseFloat(getComputedStyle(elem, null).height.replace("px", "")); ' + \
                         '} ' + \
                         'function isScrolledIntoView(elem) { ' + \
                         '  var docViewTop = document.body.scrollTop; ' + \
                         '  var docViewBottom = docViewTop + getElementHeight(document.body); ' + \
                         '  var elemRectangle = elem.getBoundingClientRect(); ' + \
                         '  var elemTop = elemRectangle.top + document.body.scrollTop; ' + \
                         '  var elemBottom = elemTop + getElementHeight(elem); ' + \
                         '  return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop)); ' + \
                         '} ' + \
                         'return isScrolledIntoView(arguments[0]);'
    scroll_to_element = 'arguments[0].scrollIntoView(true);'
    kill_timeouts = 'var id = window.setTimeout(function() {}, 0); ' + \
                    'while (id--) { ' + \
                    '   window.clearTimeout(id); ' + \
                    '}'
