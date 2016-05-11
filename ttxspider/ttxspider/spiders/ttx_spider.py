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

smzdm_pattern = re.compile(r'http://www.smzdm.com/p/([0-9]{7})')

class TtxSipder(CrawlSpider) :
    name = "ttxspider"
    allowed_domains = ["www.smzdm.com"]
    start_urls = [
        "http://www.smzdm.com/tag/%E7%99%BD%E8%8F%9C%E5%85%9A/youhui/",
    ]

    def parse(self, response) :
    	sel = Selector(response)

        urls = sel.xpath('//div[@class="listTitle"]/h3/a/@href').extract()  
        for url in urls:  
            #print url
            yield Request(url, meta={'post_type': 'baicai-featured'}, callback=self.parse_page)

        

    def parse_page(self, response) :
        item = TtxspiderItem()
        smzdm_match = smzdm_pattern.search(response.url)
        if smzdm_match: 
            item['pid'] = smzdm_match.group(1)
        item['title']  = response.xpath('//h1/em/text()').extract()
        item['subtitle']  = response.xpath('//h1/em/span[@class="red"]/text()').extract()
        item['intro']  = response.xpath('//div[@class="inner-block"]/p[1]/text()').extract()
        item['content']  = response.xpath('//div[@class="inner-block"]').extract()
        if len(item['content']) == 0:
            item['content'] = response.xpath('//div[@class="baoliao-block"]').extract()
        item['img']  = response.xpath('//a[@class="pic-Box"]/img/@src').extract()
        item['link']  = response.url
        item['dlink']  = response.xpath('//div[@class="buy"]/a/@href').extract()
        item['tag']  = response.xpath('//span[@class="tags"]/text()').extract()
        item['vendor']  = response.xpath('//div[@class="article-meta-box"]/div[@class="article_meta"][2]/span[1]/a/text()').extract()
        item['up_num'] = response.xpath('//div[@class="score_rate"]/span[@class="red"]/text()').extract()
        item['down_num'] = response.xpath('//div[@class="score_rate"]/span[@class="grey"][2]/text()').extract()
        item['reply_num'] = response.xpath('//em[@class="commentNum"]/text()').extract()
        item['follow_num'] = response.xpath('//a[@class="fav"]/em/text()').extract()
        item['author_name'] = response.xpath('//div[@class="article-meta-box"]/div[@class="article_meta"][1]/span[1]/text()').extract()
        item['created'] = response.xpath('//div[@class="article-meta-box"]/div[@class="article_meta"][1]/span[2]/text()').extract()
        if len(item['created']) == 0:
            item['created'] = response.xpath('//div[@class="article-meta-box"]/div[@class="article_meta"][1]/span[1]/text()').extract()
            item['author_name'] = [""]
        item['post_type'] = response.meta['post_type']

        yield item

        links = response.xpath('//div[@class="inner-block"]//a/@href').extract()
        for link in links:
            smzdm_match = smzdm_pattern.search(link)
            if smzdm_match: 
                yield Request(link, meta={'post_type': 'baicai'}, callback=self.parse_page)