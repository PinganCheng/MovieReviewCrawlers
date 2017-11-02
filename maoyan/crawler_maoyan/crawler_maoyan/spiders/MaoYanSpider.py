#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import time
import random
import scrapy
from bs4 import BeautifulSoup
      
reload(sys) 
sys.setdefaultencoding('utf-8') 
      
class MaoYanSpider(scrapy.Spider):
    name = "maoyan"
    start_urls = ['http://maoyan.com/news?showTab=2&offset=0']
      
    def parse(self, response):
        urls = []
        news_divs = response.xpath('//div[@class="news-container"]/div')
        if len(news_divs) == 0:
            return
        for news_div in news_divs:
            news_url = news_div.xpath('./a/@href').extract_first()
            urls.append(response.urljoin(news_url))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_news)
        url_list = response.url.split('=')
        post_url = int(response.url.split('=')[-1]) + 10
        url = url_list[0] + '=' + url_list[1] + '=' + str(post_url)
        yield scrapy.Request(url=url, callback=self.parse)
      
    def parse_news(self, response):
        filename = str(hash(response.url))
        with open('files/' + filename, 'w+') as f:
            f.write(response.text)
