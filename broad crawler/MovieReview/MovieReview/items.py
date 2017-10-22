# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MoviereviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Title = scrapy.Field()
    Source = scrapy.Field()
    Time = scrapy.Field()
    Content = scrapy.Field()
    Images = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
