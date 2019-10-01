# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


class SeleniumDownloaderMiddleware(object):
    selenium_driver_chrome = ''
    selenium_driver_firefox = ''

    def __init__(self, crawler, selenium_driver_chrome, selenium_driver_firefox):
        self.crawler = crawler
        self.selenium_driver_chrome = selenium_driver_chrome
        self.selenium_driver_firefox = selenium_driver_firefox
        self.crawler.signals.connect(self.spider_opened, signals.spider_opened)

    @classmethod
    def from_crawler(cls, crawler):
        selenium_driver_chrome = crawler.settings.get('SELENIUM_DRIVER_CHROME',
                                                      cls.selenium_driver_chrome)
        selenium_driver_firefox = crawler.settings.get('SELENIUM_DRIVER_FIREFOX',
                                                       cls.selenium_driver_firefox)

        return cls(crawler, selenium_driver_chrome, selenium_driver_firefox)

    def process_request(self, request, spider):
        if 'selenium' not in request.meta:
            return

        driver_type = request.meta['selenium']['driver'] if 'driver' in request.meta['selenium'] else None
        wait_time = request.meta['selenium']['wait_time'] if 'wait_time' in request.meta['selenium'] else None
        wait_until = request.meta['selenium']['wait_until'] if 'wait_until' in request.meta['selenium'] else None
        render_js = request.meta['selenium']['render_js'] if 'render_js' in request.meta['selenium'] else None
        script = request.meta['selenium']['script'] if 'script' in request.meta['selenium'] else None
        window_size = request.meta['selenium']['window_size'] if 'window_size' in request.meta['selenium'] else None
        headless = request.meta['selenium']['headless'] if 'headless' in request.meta['selenium'] else None

        if driver_type == 'chrome':
            options = webdriver.ChromeOptions()
        else:
            options = webdriver.FirefoxOptions()

        if window_size:
            options.add_argument('window-size=' + window_size)
        if headless:
            options.add_argument('headless')

        driver = None
        if driver_type == 'chrome':
            driver = webdriver.Chrome(chrome_options=options,
                                      executable_path=self.selenium_driver_chrome)
        elif driver_type == 'firefox':
            driver = webdriver.Firefox(firefox_options=options,
                                       executable_path=self.selenium_driver_firefox)
        else:
            return

        driver.get(request.url)

        if wait_time is not None and wait_until is not None:
            WebDriverWait(driver, wait_time).until(wait_until)
        elif wait_time is not None:
            time.sleep(wait_time)

        if script:
            driver.execute_script(script)

        if render_js:
            body = driver.execute_script("return document.body.innerHTML;")
        else:
            body = driver.page_source

        return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        pass


class BetParserSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BetParserDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
