from django import template
from django.db.models import Count, Sum

from read_statistic.models import ReadNum
from ..models import Blog, BlogType

# 这样才能在html页面中加载该方法
register = template.Library()


@register.simple_tag
def get_categories():
    # 分类归档
    return BlogType.objects.annotate(num_blog_types=Count('blog'))


@register.simple_tag
def archives():
    # 日期
    blog_dates_dict = {}
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(
            created_time__year=blog_date.year,
            created_time__month=blog_date.month
            ).count()
        blog_dates_dict[blog_date] = blog_count

    return blog_dates_dict


@register.simple_tag
def get_view_nums():
    view_nums = ReadNum.objects.aggregate(Sum('read_num'))
    return view_nums['read_num__sum']
