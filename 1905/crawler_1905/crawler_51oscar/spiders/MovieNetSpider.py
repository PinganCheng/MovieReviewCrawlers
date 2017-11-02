#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import scrapy
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

class MovieNetSpider(scrapy.Spider):
    name = "movienet"
    pre_url = "http://www.1905.com/film/filmnews/yp/"
    post_url = ".shtml"
    page = 1

    def start_requests(self):
        url = self.pre_url + str(self.page) + self.post_url
        self.page += 1
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        links = response.xpath('//dl[@class="classf_box"]//a/@href').\
                extract()
        links = set(links)
        for link in links:
            yield scrapy.Request(url=link, callback=self.parsePage)
        if self.page < 34:
            url = self.pre_url + str(self.page) + self.post_url
            self.page += 1
            yield scrapy.Request(url=url, callback=self.parse)

    def parsePage(self, response):
        with open('files/' + str(hash(response.url)), 'w') as f:
            f.write(response.text)
