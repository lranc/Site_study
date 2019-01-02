# -*- coding:utf8 -*-
from .models import NovelAuthor, AuthorReader
from authors.serializers import NovelAuthorSerializer, AuthorReaderSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from .filters import AuthorReaderFilter, NovelAuthorFilter


class AuthorsPagination(PageNumberPagination):
    '''
    商品列表自定义分页
    '''
    # 默认每页显示的个数
    page_size = 5
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少条
    max_page_size = 30


class NovelAuthorsViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    作者列表页
    """
    # 使用django-filter的DjangoFilterBackend, 进行过滤
    # 使用filters.SearchFilter, filters.OrderingFilter进行搜索和排序
    queryset = NovelAuthor.objects.all()
    pagination_class = AuthorsPagination
    serializer_class = NovelAuthorSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    # 搜索,=name表示精确搜索，也可以使用各种正则表达式
    search_fields = ('=author_id', 'author_name')
    ordering_fields = ('author_id', 'collected_num', 'send_gift', 'click_num')
    filter_class = NovelAuthorFilter
    def retrieve(self, request, *args, **kwargs):
        # 记录点击数
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class AuthorReaderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''
    作者的读者排行
    '''
    queryset = AuthorReader.objects.all().order_by('author_id')
    serializer_class = AuthorReaderSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('author__author_name', '=author__author_id')
    filter_class = AuthorReaderFilter
