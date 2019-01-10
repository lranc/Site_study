# -*- coding:utf8 -*-

import re
from django.utils import timezone
from datetime import datetime, timedelta
from lranc_site.settings import REGEX_MOBILE
from rest_framework import serializers
from users.models import VerifyCode, UserProfile
from rest_framework.validators import UniqueValidator
from django_redis import get_redis_connection


class ImageCodeCheckSerializer(serializers.Serializer):

    """
    图片验证码校验序列化器
    """

    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        """
        校验
        """
        image_code_id = attrs['image_code_id']
        text = attrs['text']
        mobile = self.context['view'].kwargs['mobile']
        # 查询真实图片验证码
        redis_conn = get_redis_connection('verify_codes')
        real_image_code_text = redis_conn.get('img_%s' % image_code_id)
        if not real_image_code_text:
            raise serializers.ValidationError('图片验证码无效')

        # 讲道理，用户只有一次验证机会，这样才显得严谨
        # 在查询验证码之后删除redis中的图片验证码
        try:
            redis_conn.delete(f"img_{image_code_id}")
        except Exception as e:
            raise serializers.ValidationError(e)

        # 比较图片验证码
        real_image_code_text = real_image_code_text.decode()
        if real_image_code_text.lower() != text.lower():
            raise serializers.ValidationError('图片验证码错误')

        # 判断是否在60s内
        send_flag = redis_conn.get("send_flag_%s" % mobile)
        if send_flag:
            raise serializers.ValidationError('请求次数过于频繁')

        return attrs


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
            raise serializers.ValidationError("请输入正确的手机号码")

        # 验证码发送频率
        # 60s内只能发送一次
        one_mintes_ago = timezone.now() - timedelta(hours=0, minutes=5, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            # raise serializers.ValidationError("距离上一次发送未超过60s")
            raise serializers.ValidationError("由于成本问题, 5分钟一条")

        return mobile


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情
    """
    username = serializers.CharField(read_only=True)
    mobile = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ("username", 'nickname', "gender", "email", "mobile")


class RegisterUserSerializer(serializers.ModelSerializer):
    '''
    用户注册
    '''
    # UserProfile中没有code字段，这里需要自定义一个code字段
    # Serializer中添加code字段，这个code是多余字段不会被保存到数据库中
    # 并在其中定义各种验证错误的信息
    code = serializers.CharField(
        required=True, write_only=True, max_length=4, min_length=4,
        label='验证码',
        error_messages={
            "blank": "请输入验证码",
            "required": "请输入验证码",
            "max_length": "验证码格式错误",
            "min_length": "验证码格式错误"
        })

    # 验证用户是否已经存在
    username = serializers.CharField(
        label="用户名", help_text="用户名", required=True, allow_blank=False,
        validators=[
            UniqueValidator(
                queryset=UserProfile.objects.all(), message="用户已经存在"
                )])

    # 密文显示password
    password = serializers.CharField(
        style={'input_type': 'password'}, label='密码', help_text="密码",
        write_only=True
        )
    # 以下为不是用signals的方法, 在serialzer的时候保存
    # 调用父类的create方法，该方法会返回当前model的实例化对象即user。
    # 前面是继承父类原有的create进行执行，后面是加入自己的逻辑
    # 调用set_password方法, 以密文存储
    # def create(self, validated_data):
    #     user = super(RegisterUserSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user

    def validate_code(self, code):
        '''
        验证在数据库中是否存在该验证码
        '''
        # get与filter的区别: get会产生两种异常，①存在多个，②一个都不存在。
        # try:
        #     verify_records = VerifyCode.objects.get(mobile=self.initial_data["username"], code=code)
        # except VerifyCode.DoesNotExist as e:
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e:
        #     pass

        # 用户从前端post过来的值都会放入initial_data里面
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data["mobile"]).order_by("-add_time")
        if verify_records:
            # 获取最新一条验证码
            last_record = verify_records[0]

            # 有效期为五分钟。
            five_mintes_ago = timezone.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_mintes_ago > last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record.code != code:
                raise serializers.ValidationError("验证码错误")

        else:
            raise serializers.ValidationError("验证码错误")

    # 不加字段名的验证器作用于所有字段之上。
    # 处于最后验证, 发生在UserViewset.create()之后
    # attrs是字段验证之后最后的response_dict
    def validate(self, attrs):
        # 博客教程加了这行, 不明白
        # attrs["mobile"] = attrs["username"]
        # code字段是之前的中间变量, 验证完后删除
        del attrs["code"]
        return attrs

    class Meta:
        model = UserProfile
        fields = ("username", "password", "mobile", "code")
