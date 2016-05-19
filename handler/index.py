#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2014 avati

import uuid
import hashlib
import Image
import StringIO
import time
import json
import re
import urllib2
import tornado.web
import lib.jsonp
import pprint
import math
import datetime
import os
import requests
import MySQLdb
import helper

from base import *
from lib.sendmail import send
from lib.variables import *
from lib.variables import gen_random
from lib.xss import XssCleaner
from lib.utils import find_mentions
from lib.reddit import hot
from lib.utils import pretty_date
from pyquery import PyQuery as pyq
from lib.dateencoder import DateEncoder

from lib.mobile import is_mobile_browser
from lib.mobile import is_weixin_browser
from form.post import *

from qiniu import Auth
from qiniu import BucketManager
from qiniu import put_data

import xml.etree.ElementTree as ET
import commands

access_key = "8RGFv3IumZByltTM1dxc9ZMAeij78rvTkjDd6WLs"
secret_key = "Ge61JJtUSC5myXVrntdVOqAZ5L7WpXR_Taa9C8vb"
q = Auth(access_key, secret_key)
bucket = BucketManager(q)


class IndexHandler(BaseHandler):
    def get(self, template_variables = {}):
        self.redirect("/baicai")

class PostHandler(BaseHandler):
    def get(self, post_id, template_variables = {}):
        source = self.get_argument("source", "")
        print source
        if (source == ""):
            post = self.post_model.get_post_by_id(post_id)
        else:
            print post_id
            post = self.post_model.get_post_by_pid_and_source(post_id, source)
        template_variables["post"] = post
        self.render("post.html", **template_variables)

class ListHandler(BaseHandler):
    def get(self, template_variables = {}):
        self.render("list.html", **template_variables)

class GetListItemsHandler(BaseHandler):
    def get(self, template_variables = {}):
        p = int(self.get_argument("p", "1"))
        items = self.post_model.get_all_posts(current_page = p)
        for item in items["list"]:
            self.jinja2 = self.settings.get("jinja2")
            item["thumb"] = helper.Filters(self.jinja2).mp_content_process(item["thumb"])
            item["created"] = helper.Filters(self.jinja2).pretty_date(item["created"])
        result_json = json.dumps(items, cls=DateEncoder)
        self.write(result_json)

class TaobaoHandler(BaseHandler):
    def get(self, template_variables = {}):
        url = self.get_argument("url", "")
        template_variables["tmall_link"] = url

        if is_weixin_browser(self):
            tmall_pattern = re.compile(r'http://detail.tmall.com/item.htm?\S*id=(\d+)')
            tmall_match = tmall_pattern.search(url) 
            if tmall_match: 
                sku = tmall_match.group(1)

                doc=pyq("http://djaa.cn/ajax/cm_details/to_cm_details_tmall.php", 
                    headers={'User-Agent': 'Mozilla/5.0 (MicroMessenger;iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4'},
                    method='post',
                    data={'id': sku, 'shopUrl': url, 'shop_type': 'tmall', 'small_shop_type': 'cm_details'})
                    #print doc
                title = doc('.dtif-h').text()
                content = doc('.viewport').outerHtml()
                template_variables["title"] = title
                template_variables["content"] = content
                self.render("tmall.html", **template_variables)  
        else:
            if is_mobile_browser:
                self.redirect("http://djaa.cn/cm_details.php?shop_type=tmall&Advertisement=0&small_shop_type=cm_details&shopUrl="+url)
            else:
                self.redirect(url)


class TaobaoPromptHandler(BaseHandler):
    def get(self, template_variables = {}):
        url = self.get_argument("url", "")
        template_variables["tmall_link"] = url

        if is_weixin_browser(self):
            self.render("prompt.html", **template_variables)
        else:
            self.redirect("http://djaa.cn/cm_details.php?shop_type=tmall&Advertisement=0&small_shop_type=cm_details&shopUrl="+url)