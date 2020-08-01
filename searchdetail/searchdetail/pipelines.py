# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class SearchdetailPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("searchdetail.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        # self.curr.execute("""DROP TABLE IF EXISTS detail""")
        # self.curr.execute("""create table detail(
        # url text,
        # email text,
        # country text,
        # keyword text,
        # city text,
        # type text
        # )""")
        pass

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""insert into detail values (?,?,?,?,?,?)""",(
            item['url'],
            item['email'],
            item['country'],
            item['keyword'],
            item['city'],
            item['type']
        ))
        self.conn.commit()

