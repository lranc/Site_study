# -*- coding:utf8 -*-

import django_filters
from .models import NovelAuthor, AuthorReader


class NovelAuthorFilter(django_filters.rest_framework.FilterSet):
    '''
    作者过滤类
    '''
    collected_min = django_filters.NumberFilter(
        field_name="collected_num", lookup_expr='gte')
    collected_max = django_filters.NumberFilter(
        field_name="collected_num", lookup_expr='lte')

    class Meta:
        model = NovelAuthor
        fields = ['collected_min', 'collected_max', 'specil_column']


class AuthorReaderFilter(django_filters.rest_framework.FilterSet):
    scoremin = django_filters.NumberFilter(
        field_name="reader_score", lookup_expr='gte')
    scoremax = django_filters.NumberFilter(
        field_name="reader_score", lookup_expr='lte')

    class Meta:
        model = AuthorReader
        fields = ['scoremin', 'scoremax']
