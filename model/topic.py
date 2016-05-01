#!/usr/bin/env python
# coding=utf-8
#
# Copyright 2016 webeta

from lib.query import Query

class TopicModel(Query):
    def __init__(self, db):
        self.db = db
        self.table_name = "topic"
        super(TopicModel, self).__init__()

    def add_new_topic(self, topic_info):
        return self.data(topic_info).add()

    def get_topic_by_topic_uuid(self, topic_uuid):
        where = "topic.topic_uuid = '%s'" % topic_uuid
        return self.where(where).find()

    def update_topic_by_topic_uuid(self, uuid, topic_info):
        where = "topic.topic_uuid = %s" % topic_uuid
        return self.where(where).data(topic_info).save()

    def delete_topic_by_topic_uuid(self, topic_uuid):
        where = "topic.topic_uuid = %s" % topic_uuid
        return self.where(where).delete()

    def get_user_all_topics(self, author_id, num = 10, current_page = 1):
        where = "topic.author_id = '%s'" % author_id
        order = "topic.created DESC, topic.id DESC"
        return self.where(where).order(order).pages(current_page = current_page, list_rows = num)
