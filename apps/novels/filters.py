# -*- coding:utf8 -*-

import django_filters
from .models import Novel


class NovelFilter(django_filters.rest_framework.FilterSet):
    '''
    作品过滤
    '''
    collected_min = django_filters.NumberFilter(
        field_name="current_collect_count", lookup_expr='gte')
    collected_max = django_filters.NumberFilter(
        field_name="current_collect_count", lookup_expr='lte')

    class Meta:
        model = Novel
        fields = [
            'collected_min', 'collected_max', 'copyright', 'gender_view',
            'era', 'noveltype', 'novel_view', 'novel_view', 'novel_style',
            'novel_progress', 'novel_sign']
