# -*- coding:utf8 -*-
from .models import Novel, NovelTags
from rest_framework import mixins
from rest_framework import viewsets
from novels.serializers import NovelTagsSerializer, NovelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from .filters import NovelFilter
from rest_framework_extensions.cache.mixins import CacheResponseMixin
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle


class NovelTagsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    '''
    标签分类
    '''
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = NovelTags.objects.all()
    serializer_class = NovelTagsSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # search_fields = ('novel__novel_name', '=novel__novel_id')
    search_fields = ('=novel__novel_id',)
    ordering_fields = ('novel_tag', )
    filter_fields = ('novel_tag',)


class NovelViewSet(CacheResponseMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    作品列表
    '''
    throttle_classes = (UserRateThrottle, AnonRateThrottle)
    queryset = Novel.objects.all().order_by('novel_id')
    serializer_class = NovelSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('=novel_id', 'novel_name')
    ordering_fields = ('novip_click', 'total_download', 'current_collect_count', 'nutrient_count','novel_score','novel_word_count')
    filter_class = NovelFilter

    def retrieve(self, request, *args, **kwargs):
        # 记录点击数
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)