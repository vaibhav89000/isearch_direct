# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SearchdetailItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    email = scrapy.Field()
    country = scrapy.Field()
    keyword = scrapy.Field()
    city = scrapy.Field()
    type = scrapy.Field()
    # pass
