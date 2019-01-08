# -*- coding:utf8 -*-

from rest_framework import serializers
from operation.models import UserFavNovel, Comment
from novels.serializers import NovelSerializer
from rest_framework.validators import UniqueTogetherValidator


class UserFavNovelDetailSerializer(serializers.ModelSerializer):
    '''
    用户收藏详情
    '''
    # 通过商品id获取收藏的商品，需要嵌套商品的序列化
    novel = NovelSerializer()

    class Meta:
        model = UserFavNovel
        fields = ("novel", "id")


class UserFavNovelsSerializer(serializers.ModelSerializer):
    '''
    用户收藏操作
    '''
    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        # validate实现唯一联合，一个作品只能收藏一次
        # 这个validate是写在meta信息中的，是因为它不是作用于某一个字段之上了。
        validators = [
            UniqueTogetherValidator(
                queryset=UserFavNovel.objects.all(),
                fields=('user', 'novel'),
                # message的信息可以自定义
                message="已经收藏"
            )
        ]
        model = UserFavNovel
        # 收藏的时候需要返回商品的id，因为取消收藏的时候必须知道商品的id是多少
        fields = ("user", "novel", 'id')


class CommentSerializer(serializers.ModelSerializer):
    '''
    用户留言
    '''
    # 获取当前登录的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        # fields = ('user', 'comment_time', 'text', 'root', 'parent', 'reply_to')
        fields = '__all__'
