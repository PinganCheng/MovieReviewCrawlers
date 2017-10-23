#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import sys
import scrapy
from bs4 import BeautifulSoup
from crawler_mtime.items import CrawlerMtimeItem

reload(sys)
sys.setdefaultencoding('utf-8')

class MtimeSpider(scrapy.Spider):
    name = "mtime"

    def start_requests(self):
        urls = ['http://news.mtime.com/movie/all/#nav',
                'http://news.mtime.com/movie/all/index-2.html',
                'http://news.mtime.com/movie/all/index-3.html',
                'http://news.mtime.com/movie/all/index-4.html',
                'http://news.mtime.com/movie/all/index-5.html',
                'http://news.mtime.com/movie/all/index-6.html',
                'http://news.mtime.com/movie/all/index-7.html',
                'http://news.mtime.com/movie/all/index-8.html',
                'http://news.mtime.com/movie/all/index-9.html',
                'http://news.mtime.com/movie/all/index-10.html']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news_urls = []
        newslist = response.xpath('//ul[@id="newslist"]/li')
        for news in newslist:
            news_urls.append(news.xpath('.//h4/a/@href').extract_first())
        for news_url in news_urls:
            yield scrapy.Request(url=news_url, callback=self.parseNews)

    def parseNews(self, response):
        item = CrawlerMtimeItem()
        title = response.xpath('//h2/text()').extract_first() + ' ' +\
                response.xpath('//h3/text()').extract_first()
        source = '时光网'
        date = response.xpath('//div[@class="newsheader "]/p/text()').\
                extract_first()
        soup = BeautifulSoup(response.text, "lxml")
        newsnote = soup.find(class_ = "newsnote")
        newscontent = soup.find('div', {'id':'newsContent'})
        content = newsnote.text + '\n' + newscontent.text
        # lack of image processing
        item['title'] = title
        item['source'] = source
        item['date'] = date
        item['content'] = content
        yield item
