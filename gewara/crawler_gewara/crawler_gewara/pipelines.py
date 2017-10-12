# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import process_item
import sqlite3

class CrawlerGewaraPipeline(object):
    pass

class SQLiteStorePipeline(object):
    def __init__(self):
        # settings = get_project_settings()
        # self.__class__.sqlite_name = settings.get('sqlite_name')
        # self.conn = sqlite3.connect(str(self.__class__.sqlite_name))
        self.conn = sqlite3.connect('sample.db')
    def process_item(self, item, spider):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS broad 
                    (Title TEXT NOT NULL, 
                    Grade TEXT NOT NULL, 
                    ReleaseTime TEXT NOT NULL,
                    Types TEXT NOT NULL,
                    Country TEXT NOT NULL,
                    Language TEXT NOT NULL,
                    MovieTime TEXT NOT NULL,
                    Director TEXT NOT NULL,
                    Actor TEXT NOT NULL)""")
            record = (item['Title'], \
                    item['Grade'], \
                    item['ReleaseTime'], \
                    item['Types'], \
                    item['Country'], \
                    item['Language'], \
                    item['MovieTime'], \
                    item['Director'], \
                    item['Actor'])

            cursor.execute('INSERT INTO broad VALUES (?,?,?,?,?,?,?,?,?)', record)
            self.conn.commit()
        except sqlite3.ProgrammingError as e:
            print 'SQLite ERROR: ' + e.message

    def __del__(self):
self.conn.close()
