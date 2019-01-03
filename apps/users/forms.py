# -*- coding:utf8 -*-
from django import forms
from django.contrib import auth
from .models import UserProfile, InvitationCode
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='用户名或邮箱',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入用户名或邮箱'}))
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)
        if user is None:
            raise forms.ValidationError('用户名或密码不正确')
        else:
            self.cleaned_data['user'] = user
            return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        max_length=30,
        min_length=3,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入用户名'})
    )
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入邮箱'})
    )
    password = forms.CharField(
        label='密码',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '请输入密码'})
    )
    password_again = forms.CharField(
        label='再输入一次密码',
        min_length=6,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': '再输入一次密码'})
    )
    invitation_code = forms.CharField(
        label='邀请码',
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '请输入邀请码'}
        )
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if UserProfile.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again

    def clean_invitation_code(self):
        invitation_code = self.cleaned_data.get(
            'invitation_code', '').strip()
        if invitation_code == '':
            raise forms.ValidationError('邀请码不能为空')
        elif not InvitationCode.objects.filter(code=invitation_code):
            raise forms.ValidationError('邀请码错误')
        else:
            InvitationCode.objects.filter(code=invitation_code).delete()
        return invitation_code


class ForgotPasswordForm():
    email = forms.EmailField(
        label='邮箱',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': '请输入绑定的邮箱'}
        )
    )
    verification_code = CaptchaField(
        label='验证码',
        error_messages={"invalid": u"验证码错误"},
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '点击“发送验证码”发送到邮箱'}
        )
    )

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get(
            'verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')


# 用于文件上传，修改头像
class UploadImageForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ['usericon']