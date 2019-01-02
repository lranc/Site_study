from django.contrib import admin
from .models import UserProfile, InvitationCode
from django.contrib.auth.admin import UserAdmin


# Register your models here.
# UserProfileAdmin 继承UserAdmin, 密码保存为密文
@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    list_display = (
        'username', 'nickname', 'gender', 'email',
        'mobile', 'usericon', 'is_staff', 'is_active', 'is_superuser')

    # 可直接修改的部分 由于没搞懂怎么将修改UserProfile的字段加入修改项目内
    list_editable = ['nickname', 'gender', 'email', 'mobile', 'usericon']


@admin.register(InvitationCode)
class InvitationCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code', )