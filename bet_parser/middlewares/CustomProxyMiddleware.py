from scrapy import signals, Selector
from scrapy.http import HtmlResponse
from itertools import cycle
import requests


class CustomProxyDownloaderMiddleware(object):
    proxies: list = []
    proxy_pool = None
    request_count: int = 0

    def __init__(self, crawler):
        self.crawler = crawler
        self.update_proxy_list()

        self.crawler.signals.connect(self.spider_opened, signals.spider_opened)
        self.crawler.signals.connect(self.spider_idle, signals.spider_idle)

    def update_proxy_list(self):
        # url = 'https://www.sslproxies.org/'
        url = 'https://free-proxy-list.net'
        response = requests.get(url)
        parser = Selector(response)
        proxies = []
        for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                # Grabbing IP and corresponding PORT
                proxy = ":".join([i.xpath('.//td[1]/text()')[0].get(), i.xpath('.//td[2]/text()')[0].get()])
                proxies.append(proxy)
        self.proxies = proxies
        self.proxy_pool = cycle(self.proxies)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        if 'custom_proxy' not in request.meta:
            return

        do_yourself = request.meta['custom_proxy']['do_yourself'] if 'do_yourself' in request.meta['custom_proxy'] \
            else None
        regenerate = request.meta['custom_proxy']['regenerate'] if 'regenerate' in request.meta['custom_proxy'] else \
            None
        proxies = request.meta['custom_proxy']['proxies'] if 'proxies' in request.meta['custom_proxy'] else \
            None
        fail_if = request.meta['custom_proxy']['fail_if'] if 'fail_if' in request.meta['custom_proxy'] else \
            None
        accept_only_if = request.meta['custom_proxy']['accept_only_if'] if 'accept_only_if' in request.meta[
            'custom_proxy'] else None

        if proxies:
            self.proxies = proxies
            self.proxy_pool = cycle(self.proxies)

        # The output can be a Response or a new Request depending on do_yourself param
        if do_yourself:
            return self.get_response(request, spider, fail_if, accept_only_if)
        else:
            return self.get_request(request, spider)

    def get_response(self, request, spider, fail_if, accept_only_if):
        response = ''

        # Get a proxy from the pool
        proxy = None
        count_retries = 0
        while count_retries < 5:
            try:
                proxy = next(self.proxy_pool)
                print('Trying with proxy ==> ' + proxy + '(remaining proxies: ' + str(len(self.proxies)) + ')')
                response = requests.get(request.url, proxies={"http": proxy, "https": proxy}, timeout=5)
                if fail_if and fail_if in response:
                    raise Exception
                elif accept_only_if and accept_only_if not in response:
                    raise Exception
                self.request_count += 1
                print('OK!')
                break
            except Exception as e:
                if isinstance(e, StopIteration):
                    # If after many retries all the proxies have been removed
                    # we regenerate the proxy list
                    self.update_proxy_list()
                else:
                    # Most free proxies will often get connection errors. You will have retry the entire request using
                    # another proxy to work.
                    if proxy in self.proxies:
                        self.proxies.remove(proxy)
                        self.proxy_pool = cycle(self.proxies)
                    spider.log("Skipping. Connnection error")
                    spider.log("Retry")

        return HtmlResponse(request.url, body=response.content, encoding='utf-8', request=request)

    def get_request(self, request, spider):
        proxy = next(self.proxy_pool)
        request.meta['proxy'] = proxy
        self.request_count += 1

        return request

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        pass

    def spider_idle(self, spider):
        pass
