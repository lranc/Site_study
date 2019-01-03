# -*- coding:utf8 -*-
from rest_framework_mongoengine import serializers as mongoserializers

from .models import NovelAuthor


# class NovelAuthorSerializer(mongoserializers.DocumentSerializer):
#     class Meta:
#         model = NovelAuthor
#         fields = '__all__'
#         # fields = ['author_id', 'author_name']


class NovelAuthorSerializer(mongoserializers.EmbeddedDocumentSerializer):
    # Skips id field and uniqueness validation.
    class Meta:
        model = NovelAuthor
        fields = '__all__'
