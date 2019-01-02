# -*- coding:utf8 -*-

import datetime
from django.views.generic import View
from django.shortcuts import render
from django.db.models import Sum
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.core.cache import cache
from read_statistic.utils import get_seven_days_read_data, get_today_hot_data,\
                                 get_yesterday_hot_data


def get_week_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]


class HomeView(View):
    def get(self, request):
        blog_content_type = ContentType.objects.get_for_model(Blog)
        dates, read_nums = get_seven_days_read_data(blog_content_type)
        today_hot_data = get_today_hot_data(blog_content_type)
        yesterday_hot_data = get_yesterday_hot_data(blog_content_type)

        # 获取一周热门博客的缓存数据
        week_hot_blogs = cache.get('week_hot_blogs')
        if week_hot_blogs is None:
            week_hot_blogs = get_week_hot_blogs()
            cache.set('week_hot_blogs', week_hot_blogs, 3600)

        context = {}
        context['dates'] = dates
        context['read_nums'] = read_nums
        context['today_hot_data'] = today_hot_data
        context['yesterday_hot_data'] = yesterday_hot_data
        context['week_hot_blogs'] = week_hot_blogs
        return render(request, 'home.html', context)
