#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2016 webeta

from lib.query import Query

class TaobaoModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "taobao"
        super(TaobaoModel, self).__init__()

    def add_new_taobao(self, taobao_info):
        return self.data(taobao_info).add()

    def get_taobao_by_item_uuid(self, item_uuid):
        where = "taobao.item_uuid = '%s'" % item_uuid
        return self.where(where).find()

    def get_taobao_by_item_id_and_author_id(self, item_id, author_id):
        where = "taobao.item_id = '%s' AND taobao.author_id = '%s'" % (item_id, author_id)
        return self.where(where).find()

    def update_taobao_by_item_uuid(self, item_uuid, taobao_info):
        where = "taobao.item_uuid = '%s'" % item_uuid
        return self.where(where).data(taobao_info).save()

    def delete_taobao_by_item_uuid(self, item_uuid):
        where = "taobao.item_uuid = %s" % item_uuid
        return self.where(where).delete()

    def get_user_all_taobaos(self, author_id, num = 10, current_page = 1):
        where = "taobao.author_id = '%s'" % author_id
        order = "taobao.order_num ASC, taobao.updated DESC, taobao.created DESC, taobao.id DESC"
        return self.where(where).order(order).pages(current_page = current_page, list_rows = num)

    def get_shop_all_items(self, shop_uuid, num = 10, current_page = 1):
        where = "taobao.shop_uuid = '%s'" % shop_uuid
        order = "taobao.order_num ASC, taobao.updated DESC, taobao.created DESC, taobao.id DESC"
        return self.where(where).order(order).pages(current_page = current_page, list_rows = num)
