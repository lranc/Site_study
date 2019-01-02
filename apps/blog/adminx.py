# -*- coding:utf8 -*-

import xadmin
from .models import Blog, BlogType


# 博客信息
class BlogAdmin(object):
    list_display = [
        'title', 'blog_type', 'author', 'get_readnum', 'content',
        'created_time', 'last_updated_time']
    search_fields = ['title', 'blog_type', 'author']
    list_filter = ['blog_type', 'author']
    # 关联该字段的, 在下拉页不能直接展示 而是以ajax搜索展现
    relfield_style = 'fk-ajax'
    refresh_times = [3, 5]

    def get_readnum(self, obj):
        return obj.get_read_num()
    get_readnum.short_description = '阅读次数'


class BlogInline(object):
    model = Blog
    extra = 0


# 博客类型
class BlogTypeAdmin(object):
    list_display = ['type_name', 'get_categories']
    list_filter = ['type_name']

    def get_categories(self, obj):
        # 分类归档
        return Blog.objects.filter(blog_type_id=obj.pk).count()
    get_categories.short_description = '博客数量'
    inlines = [BlogInline]


# 将后台管理器与models进行关联注册
xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(BlogType, BlogTypeAdmin)
