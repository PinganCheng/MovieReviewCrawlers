# -*- encoding:utf-8 -*-
import sys
import scrapy
from MovieReview.items import MoviereviewItem
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

class MovieReviewSpider(scrapy.Spider):
    name = "movie"
    start_urls = ['http://maoyan.com/news?showTab=2']

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
        nav_divs = sorted(div_lenOfa, key=lambda tup:tup[1], reverse=True)
        divs = response.xpath('./div').extract()
        
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
            div_lenDiv.append([div, len(div.xpath('./div'))])
        sorted_divs = sorted(div_lenDiv, key=lambda div_lenDiv:div_lenDiv[1], reverse=True)
        urls = sorted_divs[0][0].xpath('.//a/@href').extract()
        for url in urls:
            complete_url = response.urljoin(url)
            if complete_url not in comment_urls:
                comment_urls.append(complete_url)
        for url in comment_urls:
            yield scrapy.Request(url=url, callback=self.parsePage)

# parse specific pages
    def parsePage(self, response):
        item = MoviereviewItem()
        div_lenOfP = []
        title = ''.join(response.xpath('//h1/text()').extract_first().split())
        if title == None or title == '':
            return
        url = str(response.url).replace('http://', '').\
                replace('https://', '').replace('www.', '')
        source = url.split('.')[0]
        divs = response.xpath('//div')
        for div in divs:
            div_lenOfP.append([div, len(div.xpath('./p'))])
        sorted_divs = sorted(div_lenOfP, key=lambda div_lenOfP:div_lenOfP[1], reverse=True)
        content_div = sorted_divs[0][0]
        content = ''.join(content_div.xpath('.//p/text()').extract())
        imgs = [x for x in content_div.xpath('.//img/@src').extract()]
        hashed_images = [hash(x) for x in imgs]
        item['Title'] = title
        item['Source'] = source
        item['Time'] = "some time"
        item['Images'] = str(hashed_images)
        item['Content'] = content
        item['image_urls'] = imgs
        yield item

    def determineMain(div, tag):
        maxTag = 0
        bestDiv = div
        divs = div.xpath('./div').extract()
        for _div in divs:
            retDiv, noOfTag = determineMain(_div, tag)
            if noOfTag > maxTag:
                maxTag = noOfTag
                bestDiv = retDiv
        search_string = './' + tag
        noOfDiv = len(div.xpath(search_string).extract())
        if maxTag < noOfDiv:
            maxTag = noOfDiv
            bestDiv = div
        return div, maxTag
            
        return div
