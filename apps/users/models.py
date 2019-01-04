from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q
from django.utils import timezone
# from operation.models import UserMessage


# Create your models here.
class UserProfile(AbstractUser):
    nickname = models.CharField(
        max_length=10, verbose_name='昵称', default='', null=True, blank=True)
    gender = models.CharField(
        max_length=6, choices=(("male", "男"), ("female", "女")),
        default="female", verbose_name='性别')
    mobile = models.CharField(
        max_length=11, null=True, blank=True, verbose_name='手机')
    # user_sign # 个性签名
    usericon = models.ImageField(
        upload_to="image/%Y/%m",
        default="image/default.png",
        max_length=100,
        verbose_name='头像',
        null=True, blank=True,
    )

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nickname if self.nickname else self.username

    def get_nickname_or_username(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username

    # def unread_nums(self):
    #     # 获取用户未读消息的数量
    #     return UserMessage.objects.filter(user=self.id, has_read=False).count()


class InvitationCode(models.Model):
    code = models.CharField(max_length=6, verbose_name='邀请码')

    class Meta:
        verbose_name = "邀请码"
        verbose_name_plural = verbose_name


class VerifyCode(models.Model):
    """
    验证码
    """
    code = models.CharField("验证码", max_length=10)
    mobile = models.CharField("电话", max_length=11)
    add_time = models.DateTimeField("添加时间",  default=timezone.now)

    class Meta:
        verbose_name = "短信验证"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
