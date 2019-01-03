from django.db import models
from mongoengine import *
# Create your models here.

# connect('novel_info', 'mongodb://lranc:mongolranc@132.232.2.195:27017/JJ_Novel')


class NovelAuthor(Document):
    choices = (('1', '已完成'), ('2', '连载中'), ('3', '已暂停'))

    url = URLField()
    author_id = IntField(max_length=15, required=True)
    author_name = StringField(max_length=25, required=True)
    column_name = StringField(max_length=50)
    specil_column = BooleanField(default=0)
    column_confession = StringField()
    collected_num = IntField(max_length=10)
    author_notice = StringField()
    author_weibo = URLField()
    send_gift = IntField()
    last_update_novel = StringField()
    last_novel_id = IntField(max_length=10)
    last_novel_status = StringField(max_length=1, choices=choices)
    last_novel_word_count = IntField()
    last_update_time = DateTimeField()
    friend_chain = StringField()
    good_novel = StringField(max_length=50)

    meta = {'collection': 'author_detail'}
