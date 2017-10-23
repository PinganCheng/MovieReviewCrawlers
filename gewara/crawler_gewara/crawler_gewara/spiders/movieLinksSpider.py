'''
This spider crawls iterates index pages and then release movie links 
to Redis Database with redis_key: "movie_links"
'''

import os
import scrapy
import urlparse

class DoubanMovieSpider(scrapy.Spider):
    start_urls = ["http://www.gewara.com/movie/searchMovieStore.xhtml?movietype=&order=releasedate&moviestate=&movietime=all&playtype=&searchkey=",]
    name = "movieLinks"
    basic_url = "http://www.gewara.com"
    
    def parse(self, response):
        host = self.settings['REDIS_HOST']
        initial_lists = response.xpath('//div[@class="title"]/a/@href').extract()\
        lists = urlparse.urljoin(basic_url,initial_lists)
        for li in lists:
            command = "redis-cli -h " + host + " lpush movie_links " + li
            os.system(command)
        try:
            initial_url = response.xpath('//span[@class="next"]/a/@href').extract()[0]
            url = urlparse.urljoin(basic_url,initial_url)
        except:
            return
        yield scrapy.Request(url, callback=self.parse)
