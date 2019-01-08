# users_operation/signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from operation.models import UserFavNovel


# post_save:接收信号的方式, sender: 接收信号的model
@receiver(post_save, sender=UserFavNovel)
def create_UserFav(sender, instance=None, created=False, **kwargs):
    # 是否新建，因为update的时候也会进行post_save
    if created:
        novel = instance.novel
        novel.fav_num += 1
        novel.save()


@receiver(post_delete, sender=UserFavNovel)
def delete_UserFav(sender, instance=None, created=False, **kwargs):
        novel = instance.novel
        novel.fav_num -= 1
        novel.save()
