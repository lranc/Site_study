# -*- coding:utf8 -*-

import random
from users.models import UserProfile, VerifyCode
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets, permissions
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from users.serializers import SmsSerializer, RegisterUserSerializer, UserDetailSerializer
from utils.send_sms import TenMessage
from lranc_site.settings import AppID, AppKey
# Create your views here.


# 实现用户名邮箱均可登录
# 继承ModelBackend类，因为它有方法authenticate，可进源码查看
class CustomBackend(ModelBackend):
    '''
    自定义用户认证
    '''
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询
            user = UserProfile.objects.get(
                Q(username=username) | Q(email=username) | Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''
    手机验证码
    '''
    serializer_class = SmsSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 序列化验证是否合法
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        ten_sms = TenMessage(AppID, AppKey)
        # 生成验证码
        code = str(random.randint(1000, 9999))

        sms_status = ten_sms.send_sms(code=code, mobile=mobile)

        if sms_status["result"] != 0:
            return Response({
                "mobile": sms_status["errmsg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    '''
    用户
    '''
    queryset = UserProfile.objects.all()

    def perform_create(self, serializer):
        # create and save当前user, 并返回
        return serializer.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer)
        response_dict = serializer.data
        # 生成jwt
        payload = jwt_payload_handler(user)
        response_dict["token"] = jwt_encode_handler(payload)
        # response_dict["name"] = user.nickname if user.nickname else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(response_dict, status=status.HTTP_201_CREATED, headers=headers)

    # 动态权限配置
    # 用户注册的时候不应该有权限限制
    # 当想获取用户详情信息的时候，必须登录才行
    def get_permissions(self):
        if self.action == "retrieve":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        return []

    # 动态选择序列化方式
    # 用户注册，只返回username和mobile, 会员中心页面需要显示更多字段，使用新的UserDetailSerializer
    # 如果注册的使用userdetailSerializer, 又会导致验证失败, 所以需要动态的使用serializer
    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return RegisterUserSerializer
        return UserDetailSerializer

    # 继承RetrieveModelMixin可以获取用户详情, 但是并不知道用户的id
    # 重写get_object方法, 不管传什么id,都只返回当前用户
    def get_object(self):
        return self.request.user
