#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2016 webeta

from lib.query import Query

class ShopModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "shop"
        super(ShopModel, self).__init__()

    def add_new_shop(self, shop_info):
        return self.data(shop_info).add()

    def get_shop_by_shop_uuid(self, shop_uuid):
        where = "shop.shop_uuid = '%s'" % shop_uuid
        return self.where(where).find()

    def get_shop_by_link_and_author(self, shop_link, author_id):
        where = "shop.shop_uuid = '%s' AND shop.author_id = '%s'" % (shop_link, author_id)
        return self.where(where).find()

    def get_shop_by_author(self, author_id):
        where = "shop.author_id = '%s'" % author_id
        return self.where(where).find()

    def update_shop_by_shop_uuid(self, uuid, shop_info):
        where = "shop.shop_uuid = %s" % shop_uuid
        return self.where(where).data(shop_info).save()

    def delete_shop_by_shop_uuid(self, shop_uuid):
        where = "shop.shop_uuid = %s" % shop_uuid
        return self.where(where).delete()

    def get_user_all_shops(self, author_id, num = 10, current_page = 1):
        where = "shop.author_id = '%s'" % author_id
        order = "shop.created DESC, shop.id DESC"
        return self.where(where).order(order).pages(current_page = current_page, list_rows = num)
