# -*- coding:utf8 -*-
from .models import NovelAuthor
from rest_framework_mongoengine.viewsets import ModelViewSet as MongoModelViewSet
from rest_framework.views import APIView
from authors.serializers import NovelAuthorSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework import mixins
# from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_mongoengine import viewsets, generics
from rest_framework import filters


class AuthorsPagination(PageNumberPagination):
    '''
    商品列表自定义分页
    '''
    # 默认每页显示的个数
    page_size = 2
    # 可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    # 页码参数
    page_query_param = 'page'
    # 最多能显示多少页
    max_page_size = 100


# class NovelAuthorListView(APIView):
#     '''
#     小说作者列表
#     '''
#     def get(self, request, format=None):
#         # pagination_class = AuthorsPagination
#         authors = NovelAuthor.objects.all()[:10]
#         serializer = NovelAuthorSerializer(authors, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#             serializer = NovelAuthorSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class NovelAuthorListView(mixins.ListModelMixin, generics.GenericAPIView):
#     """
#     小说作者列表
#     """
#     # 使用自定义的分页
#     pagination_class = AuthorsPagination
#     queryset = NovelAuthor.objects.all()
#     serializer_class = NovelAuthorSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


# class NovelAuthorListView(generics.ListAPIView):
#     """
#     小说作者列表, ListAPIview继承了mixins.ListModelMixin,GenericAPIView
#     在内部写好了get方法, 因此不需要写get
#     """
#     pagination_class = AuthorsPagination
#     queryset = NovelAuthor.objects.all()
#     serializer_class = NovelAuthorSerializer


# class NovelAuthorsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     """
#     小说作者列表
#     需要配合routers使用, 自动配置url
#     重写get_querset实现过滤
#     """
#     pagination_class = AuthorsPagination
#     serializer_class = NovelAuthorSerializer
#     queryset = NovelAuthor.objects.all()
#     # 添加过滤
#     def get_queryset(self):
#         authors_id_min = self.request.query_params.get('authors_id_min', 0)
#         if authors_id_min:
#             self.queryset = NovelAuthor.objects.filter(authors_id__gt=int(authors_id_min))
#         return self.queryset


# class NovelAuthorsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     """
#     小说作者列表
#     使用django-filter的DjangoFilterBackend, 进行过滤
#     django-filter, mongo数据库下出现错误AttributeError: 'QuerySet' object has no attribute 'model'
#     使用filters.SearchFilter, filters.OrderingFilter进行搜索和排序
#     """
#     queryset = NovelAuthor.objects.all()
#     pagination_class = AuthorsPagination
#     serializer_class = NovelAuthorSerializer
#     filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
#     # 搜索,=name表示精确搜索，也可以使用各种正则表达式
#     search_fields = ('=author_id', 'author_name')
#     ordering_fields = ('author_id')
#     # from .filters import NovelAuthorFilter
#     # # 设置filter的类为我们自定义的类
#     # filter_class = NovelAuthorFilter


class NovelAuthorsViewSet(MongoModelViewSet):
    '''
    小说作者列表
    '''
    pagination_class = AuthorsPagination
    queryset = NovelAuthor.objects.all()
    serializer_class = NovelAuthorSerializer
