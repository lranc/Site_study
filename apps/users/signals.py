# -*- coding:utf8 -*-

from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import UserProfile


# post_save:接收信号的方式
# sender: 接收信号的model
@receiver(post_save, sender=UserProfile)
def create_user(sender, instance=None, created=False, **kwargs):
    # 是否create，因为update的时候也会进行post_save
    if created:
        password = instance.password
        print(password)
        # instance相当于user
        instance.set_password(password)
        instance.save()
