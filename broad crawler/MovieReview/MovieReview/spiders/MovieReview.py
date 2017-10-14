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
    start_urls = ['http://www.1905.com/film/filmnews/yp/']

    # generate navigation page urls
    def parse(self, response):
        num_of_a = 0
        leaf_divs = []
        div_lenOfa = []

        yield scrapy.Request(response.url, callback=self.extractLinks)

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

    def extractLinks(self, response):
        div_lenDiv = []
        comment_urls = []
        divs = response.xpath('//div')
        for div in divs:
            div_lenDiv.append([div, len(div.xpath('./dl'))])
        sorted_divs = sorted(div_lenDiv, key=lambda div_lenDiv:div_lenDiv[1], reverse=True)
        urls = sorted_divs[0][0].xpath('.//a/@href').extract()
        for url in urls:
            complete_url = response.urljoin(url)
            if complete_url not in comment_urls:
                comment_urls.append(complete_url)
        for url in comment_urls:
            print url
            yield scrapy.Request(url=url, callback=self.parsePage)

# parse specific pages
    def parsePage(self, response):
        div_lenOfP = []
        title = response.xpath('//title').extract_first()
        divs = response.xpath('//div')
        for div in divs:
            div_lenOfP.append([div, len(div.xpath('./p'))])
        sorted_divs = sorted(div_lenOfP, key=lambda div_lenOfP:div_lenOfP[1], reverse=True)
        content_div = sorted_divs[0][0]
        content = ''.join(content_div.xpath('.//p/text()').extract())
        print content

