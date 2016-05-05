#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2016 webeta

from lib.query import Query

class ItemModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "item"
        super(ItemModel, self).__init__()

    def add_new_item(self, item_info):
        return self.data(item_info).add()

    def get_item_by_item_uuid(self, item_uuid):
        where = "item.item_uuid = '%s'" % item_uuid
        return self.where(where).find()

    def get_item_by_item_id_and_author_id(self, item_id, author_id):
        where = "item.item_id = '%s' AND item.author_id = '%s'" % (item_id, author_id)
        return self.where(where).find()

    def update_item_by_item_uuid(self, item_uuid, item_info):
        where = "item.item_uuid = '%s'" % item_uuid
        return self.where(where).data(item_info).save()

    def delete_item_by_item_uuid(self, item_uuid):
        where = "item.item_uuid = %s" % item_uuid
        return self.where(where).delete()

    def get_user_all_items(self, author_id, num = 10, current_page = 1):
        where = "item.author_id = '%s'" % author_id
        order = "item.order_num ASC, item.updated DESC, item.created DESC, item.id DESC"
        return self.where(where).order(order).pages(current_page = current_page, list_rows = num)
