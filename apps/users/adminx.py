# -*- coding:utf8 -*-

import xadmin
from blog.models import Blog, BlogType
from read_statistic.models import ReadNum, ReadDetail
from operation.models import LikeRecord, Comment
from django.contrib.auth.models import Group, Permission
from .models import UserProfile, InvitationCode
from xadmin.models import Log
# 和X admin的view绑定
from xadmin import views
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
                                       AdminPasswordChangeForm, PasswordChangeForm)
from xadmin.layout import Fieldset, Main, Side, Row
from django.utils.translation import ugettext as _
from django.forms import ModelMultipleChoiceField
from xadmin.views.base import filter_hook


# Xadmin的全局配置信息设置
class BaseSetting(object):
    # 主题功能开启
    enable_themes = True
    use_bootswatch = True


# xadmin 全局配置参数信息设置
class GlobalSettings(object):
    site_title = "lranc"
    site_footer = "lranc"
    # 收起菜单
    # menu_style = "accordion"

    # 修改默认的site_menu, 会导致没有相关权限的菜单也暴露给职员用户

    def get_site_menu(self):
        return (
            {'title': '博客管理', 'menus': (
                {'title': '博客信息', 'perm': self.get_model_perm(
                    Blog, 'view'), 'url': self.get_model_url(Blog, 'changelist')},
                {'title': '博客类型', 'perm': self.get_model_perm(
                    BlogType, 'view'), 'url': self.get_model_url(BlogType, 'changelist')},
                # {'title': '博客点赞', 'url': self.get_model_url(LikeRecord, 'changelist')},
            )},
            {'title': '阅读统计', 'menus': (
                {'title': '阅读次数', 'perm': self.get_model_perm(
                    ReadNum, 'view'), 'url': self.get_model_url(ReadNum, 'changelist')},
                {'title': '阅读记录', 'perm': self.get_model_perm(
                    ReadDetail, 'view'), 'url': self.get_model_url(ReadDetail, 'changelist')},
            )},
            {'title': '用户管理', 'menus': (
                {'title': '用户信息', 'perm': self.get_model_perm(
                    UserProfile, 'view'), 'url': self.get_model_url(UserProfile, 'changelist')},
                {'title': '用户点赞', 'perm': self.get_model_perm(
                    LikeRecord, 'view'), 'url': self.get_model_url(LikeRecord, 'changelist')},
                {'title': '用户评论', 'perm': self.get_model_perm(
                    Comment, 'view'), 'url': self.get_model_url(Comment, 'changelist')},
                {'title': '邀请码', 'perm': self.get_model_perm(
                    InvitationCode, 'view'), 'url': self.get_model_url(InvitationCode, 'changelist')},
            )},
            {'title': '系统管理', 'perm': self.get_model_perm(Permission, 'view'), 'menus': (
                # {'title': '首页轮播', 'url': self.get_model_url(Banner, 'changelist')},
                {'title': '用户分组', 'perm': self.get_model_perm(
                    Group, 'view'), 'url': self.get_model_url(Group, 'changelist')},
                {'title': '用户权限', 'perm': self.get_model_perm(
                    Permission, 'view'), 'url': self.get_model_url(Permission, 'changelist')},
                {'title': '日志记录', 'perm': self.get_model_perm(
                    Log, 'view'), 'url': self.get_model_url(Log, 'changelist')},
            )},
        )


# 创建admin的管理类,这里不再是继承admin，而是继承object
ACTION_NAME = {
    'add': _('Can add %s'),
    'change': _('Can change %s'),
    'edit': _('Can edit %s'),
    'delete': _('Can delete %s'),
    'view': _('Can view %s'),
}


def get_permission_name(p):
    action = p.codename.split('_')[0]
    if action in ACTION_NAME:
        return ACTION_NAME[action] % str(p.content_type)
    else:
        return p.name


class PermissionModelMultipleChoiceField(ModelMultipleChoiceField):

    def label_from_instance(self, p):
        return get_permission_name(p)


class UserProfileAdmin(object):
    change_user_password_template = None
    # 配置后台我们需要显示的列
    list_display = ['username', 'nickname', 'gender',
                    'email', 'mobile', 'is_staff', 'is_superuser']
    # 配置筛选字段
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    # 配置搜索字段,不做时间搜索
    search_fields = ['username', 'nickname', 'mobile', 'email']
    # 可直接修改的部分 由于没搞懂怎么将修改UserProfile的字段加入修改项目内
    list_editable = ['nickname', 'gender', 'mobile', 'usericon']
    ordering = ('username',)
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'
    # fk_fields 设置显示外键字段
    # fk_fields = ['comment']
    # 设置哪些字段可以点击进入编辑界面
    # list_display_links = ('id', 'name')

    def get_field_attrs(self, db_field, **kwargs):
        attrs = super(UserProfileAdmin, self).get_field_attrs(
            db_field, **kwargs)
        if db_field.name == 'user_permissions':
            attrs['form_class'] = PermissionModelMultipleChoiceField
        return attrs

    def get_model_form(self, **kwargs):
        if self.org_obj is None:
            self.form = UserCreationForm
        else:
            self.form = UserChangeForm
        return super(UserProfileAdmin, self).get_model_form(**kwargs)

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserProfileAdmin, self).get_form_layout()


class InvitationCodeAdmin(object):
    list_display = ['code']

# 将model与admin管理器进行关联注册, 先注销UserProfile
# 但这种方法密码不能修改,很多默认的功能需要自己添加
# 因此将xadmin/plugins/auth的UserAdmin复制并加以修改
# xadmin.site.unregister(UserProfile)
# xadmin.site.register(UserProfile, UserProfileAdmin)


# 将Xadmin全局管理器与我们的view绑定注册。
xadmin.site.register(views.BaseAdminView, BaseSetting)
# 将头部与脚部信息进行注册:
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(InvitationCode, InvitationCodeAdmin)
