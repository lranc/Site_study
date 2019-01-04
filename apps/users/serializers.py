# -*- coding:utf8 -*-

import re
from django.utils import timezone
from datetime import datetime, timedelta
from lranc_site.settings import REGEX_MOBILE
from rest_framework import serializers
from users.models import VerifyCode, UserProfile
from rest_framework.validators import UniqueValidator


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    # 验证手机号码(函数名称必须为 validate_ + 该字段名)
    def validate_mobile(self, mobile):
        """
        手机号码验证
        """
        # 是否已经注册
        if UserProfile.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        # 60s内只能发送一次
        one_mintes_ago = timezone.now() - timedelta(hours=0, minutes=1, seconds=0)
        print(one_mintes_ago)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile
