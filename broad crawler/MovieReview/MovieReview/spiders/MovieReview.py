# -*- encoding:utf-8 -*-
import sys
import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor

reload(sys)
sys.setdefaultencoding('utf-8')

class MovieReviewSpider(scrapy.Spider):
    name = "movie"
    start_urls = ['http://chuansong.me/account/duliyumovie?start=96',]

    # generate navigation page urls
    def parse(self, response):
        num_of_a = 0
        leaf_divs = []
        div_lenOfa = []
        divs = response.xpath('//div')
        # find leaf divs
        for div in divs:
            if len(div.xpath('.//div').extract()) == 0:
                leaf_divs.append(div)
        # calculate the number of a tags in a div
        for div in leaf_divs:
            div_lenOfa.append((div, len(div.xpath('.//a'))))
        # sort by the number of tags
        nav_divs = [x[0] for x in sorted(div_lenOfa, key=lambda tup:tup[1], reverse=True)]
        # locate page number tage
        for div in nav_divs:
            txt_in_a_tag = div.xpath('.//a/text()').extract()
            if len(txt_in_a_tag) == 0:
                continue
            if txt_in_a_tag[-1] == '下一页':
                url_next_page = div.xpath('.//a/@href').extract()[-1]
                url = response.urljoin(url_next_page)
                yield scrapy.Request(url, callback=self.parse)

    # extract links of a single navigation page, send to parse_page method
    def extractLinks(self, response):
        pass

    # parse specific pages
    def parsePage(self, response):
        pass
