# -*- coding:utf8 -*-
from rest_framework import serializers
from .models import NovelAuthor, FriendChain, AuthorReader


class FriendChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendChain
        fields = ['friend_chain']


class AuthorReaderSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)

    def get_author_name(self, obj):
        return obj.author.author_name

    class Meta:
        model = AuthorReader
        fields = '__all__'


class AuthorReaderSerializer2(serializers.ModelSerializer):
    '''
    只显示reader_name, ranking
    '''
    class Meta:
        model = AuthorReader
        fields = ['reader_name', 'ranking', 'reader_level']


class NovelAuthorSerializer(serializers.ModelSerializer):
    friend_chain = FriendChainSerializer(many=True)
    reader_rank = AuthorReaderSerializer2(many=True)  # related_name

    class Meta:
        model = NovelAuthor
        fields = '__all__'
