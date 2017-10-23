# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv

class CrawlerMtimePipeline(object):
    def process_item(self, item, spider):
        csvfile = file('mtime.csv', 'a')
        writer = csv.writer(csvfile)
        data =[item['title'],\
                item['source'],\
                item['date'],\
                item['content']]
        writer.writerow(data)
        csvfile.close()
