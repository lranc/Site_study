# -*- coding:utf8 -*-

import xadmin
from .models import ReadNum, ReadDetail
from django.db.models.fields import exceptions


class ReadNumadmin(object):
    list_display = ['read_num', 'content_type', 'get_content_object']

    def get_content_object(self, obj):
        try:
            model_class = obj.content_type.model_class()
            model_obj = model_class.objects.get(pk=obj.object_id)
            return model_obj
        except exceptions.ObjectDoesNotExist:
            return 'None'
    get_content_object.short_description = '阅读对象'


class ReadDetailadmin(object):
    list_display = ['read_num', 'date', 'read_object']
    list_filter = ['date', 'read_object']


xadmin.site.register(ReadNum, ReadNumadmin)
xadmin.site.register(ReadDetail, ReadDetailadmin)