# -*- coding:utf8 -*-

import xadmin
from django.db.models.fields import exceptions
from .models import LikeRecord, Comment
# from django.utils.html import format_html
# from django.utils.safestring import mark_safe


# 用户点赞记录
class LikeRecordAdmin(object):
    list_display = ['id', 'user', 'like_time', 'content_type',
                    'get_user_name', 'get_content_object']

    search_fields = ['id', 'user__username', 'user__nickname']
    list_filter = ['user']
    # 只读字段, 不可修改
    readonly_fields = ['object_id', 'content_type', 'user']

    def get_user_name(self, obj):
        return obj.user.get_nickname_or_username()
    # 增加字段描述
    get_user_name.short_description = '用户名'

    def get_content_object(self, obj):
        try:
            model_class = obj.content_type.model_class()
            model_obj = model_class.objects.get(pk=obj.object_id)
            # url = '/xadmin/{}/{}/{}/detail/'.format(obj.content_type,obj.content_type,obj.object_id)
            return model_obj
            # return format_html('<a href="/xadmin/blog/blog/2/update/">{}</a>'.format(model_obj))
        except exceptions.ObjectDoesNotExist:
            return 0
    get_content_object.short_description = '点赞对象'
    # 让其他关联此表的外键搜索功能
    relfield_style = 'fk-ajax'


# 用户评论记录
class CommentAdmin(object):
    list_display = ['id', 'user', 'reply_to', 'comment_time',
                    'text', 'content_type', 'get_content_object']
    search_fields = ['id', 'user__username', 'user__nickname']
    list_filter = ['user']
    # 只读字段, 不可修改
    readonly_fields = ['user', 'reply_to', 'comment_time',
                       'content_type', 'get_content_object', 'root', 'parent']
    # 不显示字段
    exclude = ['object_id']

    def get_content_object(self, obj):
        try:
            model_class = obj.content_type.model_class()
            model_obj = model_class.objects.get(pk=obj.object_id)
            return model_obj
        except exceptions.ObjectDoesNotExist:
            return 0
    get_content_object.short_description = '评论对象'


# 将后台管理器与models进行关联注册
xadmin.site.register(LikeRecord, LikeRecordAdmin)
xadmin.site.register(Comment, CommentAdmin)
