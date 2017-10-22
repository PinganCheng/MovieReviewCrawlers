# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class Sqlite3Pipeline(object):
    def __init__(self):
        self.conn = sqlite3.connect('MovieNews.db')
    
    def process_item(self, item, spider):
        with open('hehe', 'w') as f:
            f.write('sigh')
        try:
            cursor = self.conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS MovieNews
                    (Title VARCHAR(300) NOT NULL,\
                    Source VARCHAR(50) NOT NULL,\
                    Time VARCHAR(30) NOT NULL,\
                    Content TEXT NOT NULL)""")
            record = (item['Title'], item['Source'],\
                    item['Time'], item['Content'], item['Images'])
            cursor.execute('INSERT INTO MovieNews VALUES (?,?,?,?, ?)',\
                    record)
            self.conn.commit()
        except sqlite3.ProgrammingError as e:
            print "SQLite3 Error: " + e.message

    def __del__(self):
        self.conn.close()
