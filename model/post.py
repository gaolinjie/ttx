#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2016 webeta

from lib.query import Query

class PostModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "post"
        super(PostModel, self).__init__()

    def add_new_post(self, post_info):
        return self.data(post_info).add()

    def get_post_by_id(self, post_id):
        where = "post.id = %s" % post_id
        return self.where(where).find()

    def get_post_by_pid_and_source(self, pid, source):
        where = "post.pid = %s AND post.source = '%s'" % (pid, source)
        return self.where(where).find()

    def update_post_by_post_uuid(self, uuid, post_info):
        where = "post.post_uuid = %s" % post_uuid
        return self.where(where).data(post_info).save()

    def delete_post_by_post_uuid(self, post_uuid):
        where = "post.post_uuid = %s" % post_uuid
        return self.where(where).delete()

    def get_user_all_posts(self, author_id, num = 10, current_page = 1):
        where = "post.author_id = '%s'" % author_id
        order = "post.created DESC, post.id DESC"
        return self.where(where).order(order).pages(current_page = current_page, list_rows = num)

    def get_all_posts(self, num = 10, current_page = 1):
        where = "post.post_type = '%s'" % "baicai-featured"
        order = "post.created DESC, post.id DESC"
        return self.where(where).order(order).pages(current_page = current_page, list_rows = num)
