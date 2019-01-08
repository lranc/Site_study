# -*- coding:utf-8 -*-

from rest_framework import viewsets, mixins
from operation.models import UserFavNovel, Comment
from operation.serializers import UserFavNovelsSerializer, \
                                UserFavNovelDetailSerializer, \
                                CommentSerializer
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication


class UserFavNovelsViewset(
        mixins.ListModelMixin, mixins.CreateModelMixin,
        mixins.DestroyModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏作品
    """
    # permission_classes权限认证
    # IsAuthenticated：用户必须登录；IsOwnerOrReadOnly：用户必须是当前登录的
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    queryset = UserFavNovel.objects.all()
    # JSONWebTokenAuthentication认证不应该全局配置, 局部模块才需要
    # authentication_classes用户认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    # 搜索的字段
    lookup_field = 'novel_id'

    # 动态选择serializer
    def get_serializer_class(self):
        if self.action == "list":
            return UserFavNovelDetailSerializer
        elif self.action == "create":
            return UserFavNovelsSerializer
        return UserFavNovelDetailSerializer

    def get_queryset(self):
        # 只能查看当前登录用户的收藏，不会获取所有用户的收藏
        return UserFavNovel.objects.filter(user=self.request.user)

    #  用户收藏的作品数量+1  用信号量实现了
    # def perform_create(self, serializer):
    #     instance = serializer.save()
    #     # 这里instance相当于UserFav model，通过它找到novel
    #     novel = instance.novel
    #     novel.fav_num += 1
    #     novel.save()


class CommentViewset(
        mixins.ListModelMixin, mixins.DestroyModelMixin,
        mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    list:
        获取用户评论
    create:
        添加评论
    delete:
        删除评论
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = CommentSerializer

    # 只能看到自己的评论
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)