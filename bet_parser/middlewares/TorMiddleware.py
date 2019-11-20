import requests
from scrapy import signals
from stem import Signal
from stem.control import Controller
import time
import scrapy


class TorDownloaderMiddleware(object):
    regenerate_after_n_req: int = 0
    request_count: int = 0
    oldIP = "0.0.0.0"
    newIP = "0.0.0.0"
    nbrOfIpAddresses = 3  # IP Address through which iterate
    secondsBetweenChecks = 2  # time between IP address checks

    def __init__(self, crawler):
        self.crawler = crawler
        self.regenerate_after_n_req = crawler.settings.get('TOR_REGENERATE_AFTER_N_REQ')
        if not self.regenerate_after_n_req or self.regenerate_after_n_req <= 0:
            TorDownloaderMiddleware.regenerate_tor()

        self.crawler.signals.connect(self.spider_opened, signals.spider_opened)
        self.crawler.signals.connect(self.spider_idle, signals.spider_idle)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # Signal TOR for a new connection
    @staticmethod
    def regenerate_tor():
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password='EmaMarcoFricaTrina123')
            controller.signal(Signal.NEWNYM)
            controller.close()

    # request a URL
    @staticmethod
    def get_current_ip():
        # communicate with TOR via a local proxy (privoxy)
        http_proxy = "http://127.0.0.1:8118"
        https_proxy = "http://127.0.0.1:8118"
        ftp_proxy = "http://127.0.0.1:8118"

        proxy_dict = {
            "http": http_proxy,
            "https": https_proxy,
            "ftp": ftp_proxy
        }

        response = requests.get("http://icanhazip.com/", proxies=proxy_dict)

        return response.text if response.text is not None else "0.0.0.0"

    def process_request(self, request, spider):
        if 'tor' not in request.meta:
            return

        regenerate = request.meta['tor']['regenerate'] if 'regenerate' in request.meta['tor'] else None
        if regenerate or \
                (self.regenerate_after_n_req > 0 and self.request_count % self.regenerate_after_n_req == 0):
            # remember the "new" IP address as the "old" IP address
            self.oldIP = self.newIP
            # refresh the TOR connection
            self.regenerate_tor()
            # obtain the "new" IP address
            self.newIP = self.get_current_ip()

            # loop until the "new" IP address is different than the "old" IP address, as it may take the TOR
            # network some time to effect a different IP address
            while self.oldIP == self.newIP:
                # sleep this thread for the specified duration
                time.sleep(self.secondsBetweenChecks)
                # obtain the current IP address
                self.newIP = self.get_current_ip()
                # signal that the program is still awaiting a different IP address
                # print("%d seconds elapsed awaiting a different IP address." % seconds)
            # output the new IP address
            print("")
            print("newIP: %s" % self.newIP)

        del request.meta['tor']
        request.meta['proxy'] = '127.0.0.1:8118'

        return scrapy.Request(url=request.url, callback=request.callback, meta={'proxy': 'http://127.0.0.1:8118'},
                              dont_filter=True)

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        pass

    def spider_opened(self, spider):
        pass

    def spider_idle(self, spider):
        pass

    ## Alternative Tor implementation
    # from torrequest import TorRequest
    # @staticmethod
    # def regenerate_tor():
    #     tor: TorRequest = None
    #     tor = TorRequest(password='EmaMarcoFricaTrina123')
    #     tor.reset_identity()
    #     return tor

    # return HtmlResponse(request.url, body=response.content, encoding='utf-8', request=request)

    # def try_tor_retrieve(self, url):
    #     response = None
    #     try:
    #         response = self.tor.get(url)
    #         self.request_count += 1
    #     except Exception as e:
    #         self.try_tor_retrieve(url)
    #
    #     return response
