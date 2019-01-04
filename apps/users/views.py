# -*- coding:utf8 -*-
import string
import random
import time
from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
from .forms import LoginForm, ForgotPasswordForm, RegisterForm, UploadImageForm
from django.contrib import auth
from users.models import UserProfile, VerifyCode
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from users.serializers import SmsSerializer
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
                Q(username=username) | Q(email=username)|Q(mobile=username))
            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self,
            # raw_password):
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    # 登录
    def get(self, request):
        login_form = LoginForm()
        context = {}
        context['login_form'] = login_form
        return render(request, 'user/user_login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('next', reverse('home')))
        else:
            context = {}
            context['login_form'] = login_form
            return render(request, 'user/user_login.html', context)


class LoginModalView(View):
    def post(sel, request):
        login_form = LoginForm(request.POST)
        data = {}
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            data['status'] = 'SUCCESS'
        else:
            data['status'] = 'ERROR'
        return JsonResponse(data)


class RegisterView(View):
    # 注册视图
    def get(self, request):
        register_form = RegisterForm()
        context = {}
        context['reg_form'] = register_form
        return render(request, 'user/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            # 创建用户
            user = UserProfile.objects.create_user(username, email, password)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('next', reverse('home')))
        context = {}
        context['reg_form'] = register_form
        return render(request, 'user/register.html', context)


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
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


class LogoutView(LoginRequiredMixin, View):
    # 登出, 不需要跳转到登录
    redirect_field_name = 'next'

    def get(self, request):
        auth.logout(request)
        return redirect(request.GET.get('next', reverse('home')))


class ForgetPwdView(View):
    def get(self, request):
        redirect_to = reverse('/user/login/')
        form = ForgotPasswordForm()
        context = {}
        context['page_title'] = '重置密码'
        context['form_title'] = '重置密码'
        context['submit_text'] = '重置'
        context['form'] = form
        context['return_back_url'] = redirect_to
        return render(request, 'user/forgot_password.html', context)


class UserInfoView(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, "user/user_info.html", {
        })


class UserIcon(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, "user/user_icon.html", {
        })


class ChangeIcon(LoginRequiredMixin, View):
    login_url = '/user/login/'
    redirect_field_name = 'next'

    def get(self, request):
        return render(request, "user/user_changeicon.html", {
        })

    def post(self, request):
        data = {}
        image_form = UploadImageForm(
            request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            data['status'] = 'SUCCESS'
        else:
            data['status'] = 'FALSE'
        return JsonResponse(data)




def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}

    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码：%s' % code,
                'testzzaaqq@163.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

# def forgot_password(request):
#     redirect_to = reverse('login')
#     if request.method == 'POST':
#         form = ForgotPasswordForm(request.POST, request=request)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             new_password = form.cleaned_data['new_password']
#             user = UserProfile.objects.get(email=email)
#             user.set_password(new_password)
#             user.save()
#             # 清除session
#             del request.session['forgot_password_code']
#             return redirect(redirect_to)
#     else:
#         form = ForgotPasswordForm()

#     context = {}
#     context['page_title'] = '重置密码'
#     context['form_title'] = '重置密码'
#     context['submit_text'] = '重置'
#     context['form'] = form
#     context['return_back_url'] = redirect_to
#     return render(request, 'user/forgot_password.html', context)
