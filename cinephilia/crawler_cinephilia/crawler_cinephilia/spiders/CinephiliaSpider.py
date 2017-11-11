#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import scrapy

reload(sys)
sys.setdefaultencoding('utf-8')

class CinephiliaSpider(scrapy.Spider):
    name = "cine"
    pre_url = "http://cinephilia.net/page/"
    page = 260

    def start_requests(self):
        url = self.pre_url + str(self.page)
        self.page += 1
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        articles = response.xpath('//div[@class="posts border ajaxify-pagination"]/article')
        for article in articles:
            url = article.xpath('.//h3/a/@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parsePage)
        url = self.pre_url + str(self.page)
        self.page += 1   
        yield scrapy.Request(url=url, callback=self.parse)

    def parsePage(self, response):
        with open('files/' + str(hash(response.url)), 'w') as f:
            f.write(response.text)
