# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class DirettaSpider(scrapy.Spider):
    name = 'dir'
    allowed_domains = ['http://diretta.it']
    start_urls = ['https://www.diretta.it/serie-a/classifiche/']

    def writeOnFile(self, filename, content):
        with open(filename, 'wb') as f:
            f.write(content)
        self.log('Saved file %s' % filename)

    def getHTMLElementText(element):
        element.xpath('@class').extract_first()

    def getHTMLElements(element, selector):
        return element.css(selector)

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                args={'wait': 2, 'png': 0}
                                )

    def parse(self, response):
        self.writeOnFile('quotes-diretta.html', response.body)

        clubList = DirettaSpider.getHTMLElements(response, '.table__body .table__row')
        count = 0
        for club in clubList:
            count += 1
            print('squadra ' + str(count))
            names = DirettaSpider.getHTMLElements(club, '.table__cell--participant_name')
            for name in names:
                print(str(DirettaSpider.getHTMLElementText(name)))
        pass
