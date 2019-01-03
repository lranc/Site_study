"""lranc_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from lranc_site.settings import MEDIA_ROOT
from .views import HomeView
from django.views.generic import RedirectView
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from authors.views import NovelAuthorsViewSet, AuthorReaderViewSet
from novels.views import NovelTagsViewSet, NovelViewSet

router = DefaultRouter()
# 配置authors的url
router.register(r'authors', NovelAuthorsViewSet, base_name='authors')
router.register(r'rankreaders', AuthorReaderViewSet, base_name='rankreaders')
router.register(r'noveltags', NovelTagsViewSet, base_name='rankreaders')
router.register(r'novels', NovelViewSet, base_name='novels')

urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('docs/', include_docs_urls(title='lranc文档')),
    path('api-auth/', include('rest_framework.urls')),
    re_path('^', include(router.urls), name='API'),
    # 配置上传文件的访问处理函数
    # 处理图片显示的url
    # 使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)',  serve, {"document_root": MEDIA_ROOT}),
    path('home/', HomeView.as_view(), name="home"),
    path('user/', include('users.urls', namespace='users')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('operation/', include('operation.urls', namespace='operation')),
    # path('novels/', include('novels.urls', namespace='novels')),
    # 验证码url
    path("captcha/", include('captcha.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/img/favicon.ico')),
    # 配置ckeditor路由
    path('ckeditor/', include('ckeditor_uploader.urls')),
]
