#!/usr/bin/env python
# -*- coding:utf-8 -*-

from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request, FormRequest
from ttxspider.items import TtxspiderItem
import re
import uuid
from pyquery import PyQuery as pyq


class TtxSipder(CrawlSpider) :
    print '11111111111111111111111111111'
    name = "ttxspider"
    allowed_domains = ["www.smzdm.com"]
    start_urls = [
        "http://www.smzdm.com/tag/%E7%99%BD%E8%8F%9C%E5%85%9A/youhui/",
    ]

    def parse(self, response) :
        print '2222222222222222222222'
    	sel = Selector(response)

        urls = sel.xpath('//div[@class="listTitle"]/h3/a/@href').extract()  
        for url in urls:  
            print url
            yield Request(url, callback=self.parse_page)
        print '333333333333333333333'

    def parse_page(self, response) :
        '''
        doc=pyq('http://m.smzdm.com/p/6115909?from=search')
        print doc
        print response
        '''
        print response.status
        #print response.body
        #print response.meta


    	sel = HtmlXPathSelector(text=response.body)
        topic = sel.xpath('//article')
        print topic[0]

        item = TtxspiderItem()
        item['title']  = topic.xpath('./h1/em/text()').extract()
        print item['title']
        item['subtitle']  = topic.xpath('./h1/span[@class="red"]/text()').extract()
        item['intro']  = topic.xpath('./div[@class="news_content"]/p/text()').extract()
        item['content']  = topic.xpath('./div[@class="news_content"]/p').extract()
        item['img']  = topic.xpath('./div[@class="news_content"]/div[@class="article_picwrap"]/a[@class="picLeft"]/img/@src').extract()
        item['link']  = response.url
        item['dlink']  = topic.xpath('./div[@class="news_content"]/div[@class="article_picwrap"]/div[@class="buy"]/a/@href').extract()
        item['tag']  = topic.xpath('./div[@class="article_meta"]/span[@class="lFloat"]/text()').extract()
        item['vendor']  = topic.xpath('./div[@class="news_content"]/div[@class="article_picwrap"]/a[@class="mall"]/text()').extract()
        item['author_name'] = topic.xpath('./div[@class="article_meta"]/div[@class="recommend"]/text()').extract()
        item['up_num'] = sel.xpath('//div[@class="score_rateBox"]/span[@class="red"]/text()').extract()
        item['down_num'] = sel.xpath('//div[@class="score_rateBox"]/span[@class="grey"]/text()').extract()
        item['reply_num'] = sel.xpath('//div[@class="leftLayer"]/em[@class="commentNum"]/text()').extract()
        item['follow_num'] = sel.xpath('//div[@class="leftLayer"]/a[@class="fav"]/em/text()').extract()
        item['created'] = topic.xpath('./div[@class="article_meta"]/span[@class="lrTime"]/text()').extract()
        print item['created']

        return item