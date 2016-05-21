# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class TtxspiderItem(Item):
    # define the fields for your item here like:
    pid = Field()
    title = Field()
    subtitle = Field()
    img = Field()
    intro = Field()
    content = Field()
    link = Field()
    dlink = Field()
    price = Field()
    vendor = Field()
    author_name = Field()
    tag = Field()
    up_num = Field()
    down_num = Field()
    reply_num = Field()
    follow_num = Field()
    created = Field()
    post_type = Field()
