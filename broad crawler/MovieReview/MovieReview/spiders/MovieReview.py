import scrapy
from scrapy_redis.spiders import RedisSpider
from scrapy.http import Request, HtmlResponse
from scrapy.linkextractors import LinkExtractor


class MovieReviewSpider(RedisSpider):
    name = "movie"
    redis_key + "start_url"

    # generate navigation page urls
    def parse(self, response):
        pass

    # extract links of a single navigation page, send to parse_page method
    def extractLinks(self, response):
        pass

    # parse specific pages
    def parse_page(self, response):
        pass
