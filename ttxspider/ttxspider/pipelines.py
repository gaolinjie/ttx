# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
from scrapy.http import Request

import MySQLdb
import MySQLdb.cursors
import os
import uuid
import time

from qiniu import Auth
from qiniu import BucketManager

access_key = "DaQzr1UhFQD6im_kJJjZ8tQUKQW7ykiHo4ZWfC25"
secret_key = "Ge61JJtUSC5myXVrntdVOqAZ5L7WpXR_Taa9C8vb"
bucket_name = "mmm-cdn"

dup = 0
DUP_THRESHOLD = 1000

q = Auth(access_key, secret_key)
bucket = BucketManager(q)
source = "smzdm"

class TtxspiderPipeline(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',
			db = 'ttx',
			user = 'ttx',
			passwd = 'ttx',
			cursorclass = MySQLdb.cursors.DictCursor,
			charset = 'utf8',
			use_unicode = False
		)
		dup = 0

	def process_item(self, item, spider):
		query = self.dbpool.runInteraction(self._conditional_insert, item)
		query.addErrback(self.handle_error)
		return item

	def _conditional_insert(self, tx, item):
		global dup
		tx.execute("select * from post where pid=%s", (item['pid'],))
		result=tx.fetchone()
		if result:
			dup = dup + 1
			if dup > DUP_THRESHOLD:
				print '重复的条目已经达到上限，关闭爬虫'
				os._exit(0)
		else:
			if  len(item['content']) == 0:
				item['content'].append("")
			if  len(item['intro']) == 0:
				item['intro'].append("")
			if 	len(item['dlink']) == 0:
				item['dlink'].append("/")

			author_name = item['author_name'][0]
			if author_name != "":
				author_name = author_name.replace(u'\u7206\u6599\u4eba\uff1a', u'');
			#print author_name
			created = item['created'][0].replace(u'\u65f6\u95f4\uff1a', u'')
			if created.find("-") != -1:
				created = time.strftime('%Y-') + created + ":00"
			else:
				created = time.strftime('%Y-%m-%d ') + created + ":00"
			print created
			tx.execute(\
				"insert into post (pid, title, subtitle, content, post_type, thumb, link, dlink, source, price, vendor, author_name, up_num, down_num, reply_num, follow_num, created) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",\
				(item['pid'], item['title'][0], item['subtitle'][0], item['content'][0], item['post_type'], item['img'][0], item['link'], item['dlink'][0], source, item['subtitle'][0], item['vendor'][0], author_name, item['up_num'][0], item['down_num'][0], item['reply_num'][0], item['follow_num'][0], created))

	def handle_error(self, e):
		print e
