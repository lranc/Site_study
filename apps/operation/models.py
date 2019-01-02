from django.db import models
from users.models import UserProfile
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


# Create your models here.
class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name="接收用户")
    message = models.CharField(max_length=500, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name


class LikeCount(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    liked_num = models.IntegerField(default=0)


class LikeRecord(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='点赞类型')
    object_id = models.PositiveIntegerField(verbose_name='对象id')
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, verbose_name='用户')
    like_time = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    # 用户评论
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='对象类型')
    object_id = models.PositiveIntegerField(verbose_name='对象id')
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField(verbose_name='评论内容')
    comment_time = models.DateTimeField(
        auto_now_add=True, verbose_name='评论时间')
    user = models.ForeignKey(
        UserProfile, related_name='comments', on_delete=models.CASCADE, verbose_name='评论者')

    root = models.ForeignKey(
        'self', related_name='root_comment', null=True, on_delete=models.CASCADE, verbose_name='初始评论')
    parent = models.ForeignKey(
        'self', related_name='parents_comment', null=True, on_delete=models.CASCADE, verbose_name='上级评论')
    reply_to = models.ForeignKey(
        UserProfile, related_name='replies', null=True,
        on_delete=models.CASCADE, verbose_name='被回复者')

    def __str__(self):
        return 'Comment No:{}'.format(self.id)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
        ordering = ['comment_time']
