# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TtxspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    subtitle = scrapy.Field()
    img = scrapy.Field()
    intro = scrapy.Field()
    content = scrapy.Field()
    link = scrapy.Field()
    dlink = scrapy.Field()
    price = scrapy.Field()
    vendor = scrapy.Field()
    author_name = scrapy.Field()
    tag = scrapy.Field()
    up_num = scrapy.Field()
    down_num = scrapy.Field()
    reply_num = scrapy.Field()
    follow_num = scrapy.Field()
    created = scrapy.Field()
    #vote = scrapy.Field()
    #star = scrapy.Field()
    #comment = scrapy.Field()
    #user = scrapy.Field()
