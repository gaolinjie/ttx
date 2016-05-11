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
        user_info = self.current_user
        template_variables["user_info"] = user_info
        default_ad = self.ad_model.get_ad_by_ad_uuid(user_info.default_ad)
        template_variables["default_ad"] = default_ad
        ads = self.ad_model.get_ads_by_author_id()
        template_variables["ads"] = ads

        self.render("index.html", **template_variables)

class ShareItHandler(BaseHandler):
    def get(self, template_variables = {}):
        print 'asdf'

    def post(self):
        user_info = self.current_user
        data = json.loads(self.request.body)
        link_text = data["link_text"]
        ad_uuid = data["ad_uuid"]

        doc=pyq(link_text)
        title = doc('#activity-name').text()
        content = doc('.rich_media_content').outerHtml()

        topic_uuid = "%s" % uuid.uuid1()
        self.topic_model.add_new_topic({
                "topic_uuid": topic_uuid,
                "ad_uuid": ad_uuid,
                "title": title,
                "content": content,
                "author_id": user_info.wx_id,
                "created": time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        self.write(lib.jsonp.print_JSON({
                    "success": 1,
                    "topic_url": "/t/"+topic_uuid
                }))

class MySharesHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        p = int(self.get_argument("p", "1"))
        shares = self.topic_model.get_user_all_topics(user_info.wx_id, current_page = p)
        template_variables["shares"] = shares
        self.render("shares.html", **template_variables)

class MyAdsHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        p = int(self.get_argument("p", "1"))
        ads = self.ad_model.get_user_all_ads(user_info.wx_id, current_page = p)
        template_variables["ads"] = ads
        self.render("ads.html", **template_variables)


class AddAdHandler(BaseHandler):
    def get(self, template_variables = {}):
        print 'asdf'

    def post(self):
        user_info = self.current_user
        data = json.loads(self.request.body)
        ad_name = data["ad_name"]
        ad_type = data["ad_type"]
        ad_text = data["ad_text"]
        ad_link = data["ad_link"]

        if ad_type == '纯文本广告':
            ad_type = 'only_text'
        elif ad_type == '纯图片广告':
            ad_type = 'only_img'
        elif ad_type == '文本加图片广告':
            ad_type = 'text_and_img'

        ad_uuid = "%s" % uuid.uuid1()
        self.ad_model.add_new_ad({
                "ad_uuid": ad_uuid,
                "ad_name": ad_name,
                "ad_type": ad_type,
                "ad_text": ad_text,
                "ad_link": ad_link,
                "author_id": user_info.wx_id,
                "updated": time.strftime('%Y-%m-%d %H:%M:%S'),
                "created": time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        self.write(lib.jsonp.print_JSON({
                    "success": 1,
                }))

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
        #posts = self.post_model.get_all_posts()
        #template_variables["posts"] = posts
        self.render("list.html", **template_variables)

class GetListItemsHandler(BaseHandler):
    def get(self, template_variables = {}):
        p = int(self.get_argument("p", "1"))
        items = self.post_model.get_all_posts()
        for item in items["list"]:
            self.jinja2 = self.settings.get("jinja2")
            item["thumb"] = helper.Filters(self.jinja2).mp_content_process(item["thumb"])
            item["created"] = helper.Filters(self.jinja2).pretty_date(item["created"])
        result_json = json.dumps(items, cls=DateEncoder)
        self.write(result_json)

class MyTabaosHandler(BaseHandler):
    def get(self, template_variables = {}):
        p = int(self.get_argument("p", "1"))
        user_info = self.current_user
        shop = self.shop_model.get_shop_by_author(user_info.wx_id)
        template_variables["shop"] = shop
        self.render("taobaos.html", **template_variables)

class ShopHandler(BaseHandler):
    def get(self, shop_uuid, template_variables = {}):
        p = int(self.get_argument("p", "1"))
        shop = self.shop_model.get_shop_by_shop_uuid(shop_uuid)
        template_variables["shop"] = shop
        self.render("shop.html", **template_variables)

class GetShopItemsHandler(BaseHandler):
    def get(self, shop_uuid, template_variables = {}):
        p = int(self.get_argument("p", "1"))
        items = self.taobao_model.get_shop_all_items(shop_uuid, current_page = p)
        result_json = json.dumps(items, cls=DateEncoder)
        self.write(result_json)

class GetShopUUIDHandler(BaseHandler):
    def get(self, template_variables = {}):
        user_info = self.current_user
        shop_link = self.get_argument("shop_link", "")
        shop_type= self.get_argument("shop_type", "")
        shop = self.shop_model.get_shop_by_link_and_author(shop_link, user_info.wx_id)
        if shop:
            shop_uuid = shop.shop_uuid
        else:
            shop_uuid = "%s" % uuid.uuid1()
            self.shop_model.add_new_shop({
                "shop_uuid": shop_uuid,
                "shop_type": shop_type,
                "shop_name": shop_link,
                "shop_link": shop_link,
                "author_id": user_info.wx_id,
                "updated": time.strftime('%Y-%m-%d %H:%M:%S'),
                "created": time.strftime('%Y-%m-%d %H:%M:%S'),
            })

        self.write(lib.jsonp.print_JSON({
                    "success": 1,
                    "shop_uuid": shop_uuid,
            }))

class AddTbHandler(BaseHandler):
    def get(self, template_variables = {}):
        print 'asdf'

    def post(self):
        user_info = self.current_user
        data = json.loads(self.request.body)
        shop_uuid = data["shop_uuid"]
        items_text = data["items_text"]
        item_type = data["item_type"]

        doc = pyq("<html><body>"+items_text+"</body></html>")
        items = doc('.item')
        for item in items:
            item = pyq(item)
            if item.find('.thumb'):
                item_id = item.attr('data-id')
                item_title = item.find('.photo img').attr('alt')
                item_thumb = item.find('.photo img').attr('data-ks-lazyload')
                item_thumb = item_thumb[0:-12]
                item_link = item.find('.photo .J_TGoldData').attr('href')
                item_price = item.find('.detail .c-price').text()

                taobao = self.taobao_model.get_taobao_by_item_id_and_author_id(item_id, user_info.wx_id)
                if taobao:
                    self.taobao_model.update_taobao_by_item_uuid(taobao.item_uuid, {
                        "item_title": item_title,
                        "item_thumb": item_thumb,
                        "item_link": item_link,
                        "item_price": item_price,
                        "updated": time.strftime('%Y-%m-%d %H:%M:%S'),
                    })
                else:
                    item_uuid = "%s" % uuid.uuid1()
                    self.taobao_model.add_new_taobao({
                        "shop_uuid": shop_uuid,
                        "item_uuid": item_uuid,
                        "item_type": item_type,
                        "item_id": item_id,
                        "item_title": item_title,
                        "item_thumb": item_thumb,
                        "item_link": item_link,
                        "item_price": item_price,
                        "author_id": user_info.wx_id,
                        "updated": time.strftime('%Y-%m-%d %H:%M:%S'),
                        "created": time.strftime('%Y-%m-%d %H:%M:%S'),
                    })                

        self.write(lib.jsonp.print_JSON({
                    "success": 1
                }))

class TaobaoHandler(BaseHandler):
    def get(self, item_uuid, template_variables = {}):
        taobao = self.taobao_model.get_taobao_by_item_uuid(item_uuid)
        template_variables["taobao"] = taobao

        if is_weixin_browser(self):
            if taobao.src_code and taobao.src_code != '':
                doc=pyq(taobao.src_code)
                tao_content = doc('.viewport').outerHtml()
                template_variables["tao_content"] = tao_content
                if taobao.item_type == 'taobao':
                    self.render("taobao_src.html", **template_variables)
                else:
                    self.render("tmall_src.html", **template_variables)
            else:
                if taobao.item_type == 'taobao':
                    self.render("taobao.html", **template_variables)
                else:
                    self.render("tmall.html", **template_variables)
        else:
            self.redirect(taobao.item_link)

        

class TaobaoPromptHandler(BaseHandler):
    def get(self, item_uuid, template_variables = {}):
        taobao = self.taobao_model.get_taobao_by_item_uuid(item_uuid)
        template_variables["taobao"] = taobao
        if is_weixin_browser(self):
            self.render("prompt.html", **template_variables)
        else:
            self.redirect(taobao.item_link)

class TaobaoEditHandler(BaseHandler):
    def get(self, item_uuid, template_variables = {}):
        user_info = self.current_user
        taobao = self.taobao_model.get_taobao_by_item_uuid(item_uuid)
        template_variables["taobao"] = taobao
        self.render("edit_taobao.html", **template_variables)

    def post(self, item_uuid):
        user_info = self.current_user
        data = json.loads(self.request.body)
        tao_code = data["tao_code"]
        src_code = data["src_code"]
        print tao_code
        self.taobao_model.update_taobao_by_item_uuid(item_uuid, {
            "tao_code": tao_code,
            "src_code": src_code,
            })
        self.write(lib.jsonp.print_JSON({
                    "success": 1
                }))

# for weixin test
class WeixinHandler(BaseHandler):
    def get(self, template_variables = {}):
        print 'ddddddddddddddddd'
        #获取微信公众平台发送的验证参数
        signature = self.get_argument('signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce', '')
        echostr = self.get_argument('echostr', '')
        #定义token，需要和Web页面上填写的一致
        token = 'webeta'
        #将参数放入列表中，并排序
        list=[token,timestamp,nonce]
        list.sort()
        #加密列表中的参数
        sha1=hashlib.sha1()
        map(sha1.update,list)
        #比较加密结果
        hashcode=sha1.hexdigest()
        if hashcode == signature:
            wx = MenuManager()
            accessToken = wx.getAccessToken()
            print 'eeeeeeeeeeeeeeeeee'
            wx.createMenu(accessToken)
            #wx.getMenu(accessToken)

            self.write(echostr)
        else:
            self.write('error,code 403')

    def post(self):
        print 'dddddddddddddd'
        self.write("")
        '''
        body = self.request.body
        data = ET.fromstring(body)
        tousername = data.find('ToUserName').text
        fromusername = data.find('FromUserName').text
        createtime = data.find('CreateTime').text
        msgtype = data.find('MsgType').text
        content = data.find('Content').text
        msgid = data.find('MsgId').text

        if content.strip() in ('ls','pwd','w','uptime'):
            result = commands.getoutput(content)
        else:
            result = '不可以哦!!!'
        textTpl = """<xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[%s]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                    </xml>"""
        out = textTpl % (fromusername, tousername, str(int(time.time())), msgtype, result)
        self.write(out)
        '''

class MenuManager:
    accessUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx9f6b9870de292bb7&secret=970ad300582a06480202fbebd942f801"
    delMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token="
    createUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token="
    getMenuUri="https://api.weixin.qq.com/cgi-bin/menu/get?access_token="
    def getAccessToken(self):
        f = urllib2.urlopen(self.accessUrl)
        accessT = f.read().decode("utf-8")
        jsonT = json.loads(accessT)
        print accessT
        print jsonT
        return jsonT["access_token"]
    def delMenu(self, accessToken):
        html = urllib2.urlopen(self.delMenuUrl + accessToken)
        result = json.loads(html.read().decode("utf-8"))
        print result["errcode"]
        return result["errcode"]
    def createMenu(self, accessToken):
        menu = '''{
                    "button":[
                        {
                            "type":"view",
                            "name":"WeBeta",
                            "url":"http://webeta.ngrok.cc/"
                        },
                    ]
                }'''
        html = urllib2.urlopen(self.createUrl + accessToken, menu.encode("utf-8"))
        result = json.loads(html.read().decode("utf-8"))
        print result
        return result["errcode"]
    def getMenu(self, accessToken):
        html = urllib2.urlopen(self.getMenuUri + accessToken)
        print(html.read().decode("utf-8"))
