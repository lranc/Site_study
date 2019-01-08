# -*- coding:utf8 -*-
from rest_framework import serializers
from .models import Novel, NovelTags


class NovelTagsSerializer(serializers.ModelSerializer):
    novel_tag_name = serializers.SerializerMethodField(read_only=True)
    novel_name = serializers.SerializerMethodField(read_only=True)

    def get_novel_tag_name(self, obj):
        return obj.get_novel_tag_display()

    def get_novel_name(self, obj):
        return obj.novel.novel_name

    class Meta:
        model = NovelTags
        fields = ['novel_tag_name', 'novel', 'novel_name']


class NovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = '__all__'
