# -*- coding: UTF-8 -*-
'''
This spider extracts specific content from given movie links which can be 
accessed from Redis Database by redis_key "movie_links" and stores the data
to HBase.
Moreover, this spider should export link to more reviews to Redis Database
as redis_key "more_reviews".
'''

import os
import sys
import scrapy
from scrapy_redis.spiders import RedisSpider
from crawler_gewara.items import MovieItem

reload(sys)
sys.setdefaultencoding('utf-8')

class MovieContentSpider(RedisSpider):
    name = "movieContent"
    redis_key = "movie_links"

    def parse(self, response):
        host = self.settings['REDIS_HOST']
        item = MovieItem()
        title = response.xpath('//h1/text()').extract()[0]
        try:
            director = response.xpath('//em[@class="lineBox clear"]/text()').extract()[0]
        except IndexError:
            director = ''
        actor = response.xpath('//span[@class="name"]/text()').extract()[0]
        response.xpath('//li[@class="first"]/text()').extract()
        lis = response.xpath('//ul[@class="clear"]/li').extract()
        time = lis[0]
        time1, time2 = time.split(':', 1)
        type = lis[1]
        type1, type2 = type.split(':', 1)
        country = lis[2]
        country1, country2 = country.split(':', 1)
        language = lis[3]
        language1, language2 = language.split(':', 1)
        images =  response.xpath('.//img/@src').extract()]
        hashed_images = [hash images]
        item['Images'] = str(hashed_images)
        item['Content'] = content
        item['image_urls'] = images
        item['url'] = response.url
        item['Title'] = name
        item['Director'] = director
        item['ReleaseTime'] = time2
        item['Types'] = type2
        item['Country'] = country2
        item['Actor'] = actor
        more_reviews = response.url + 'reviews'
        command = 'redis-cli -h ' + host + ' lpush more_reviews ' \
                + more_reviews
        os.system(command)
        yield item
